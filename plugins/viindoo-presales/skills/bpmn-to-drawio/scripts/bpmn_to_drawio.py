#!/usr/bin/env python3
"""bpmn_to_drawio — convert một file BPMN 2.0 (.bpmn) thành .drawio mxgraph XML.

Mục đích: cho phép consultant Viindoo mở/sửa diagram trong draw.io desktop
(hoặc paste vào QTUD multi-page) mà vẫn giữ chuẩn BPMN 2.0 từ pipeline
spec-to-bpmn. Coords được tái sử dụng từ section BPMNDI — script này KHÔNG
tự layout lại.

Brand palette theo shared-brand/brand.yaml (extract từ Nasilkmex Dệt Lụa QTUD
47-page đã ký).

Zero dependency — stdlib only (xml.etree.ElementTree). JSON envelope khi --json.
Exit codes (convention v0.3.0): 0 success / 1 user / 2 data / 3 system.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from xml.sax.saxutils import escape as xml_escape

NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}

# Brand palette — extract từ shared-brand/brand.yaml (Nasilkmex reference)
STYLE = {
    "pool": "swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;horizontal=0;startSize=30;horizontalStack=0;fontSize=12;verticalAlign=middle;",
    "lane": "swimlane;html=1;startSize=30;horizontal=0;fontSize=12;verticalAlign=middle;",
    "task_user": "shape=mxgraph.bpmn.task;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;fontSize=14;align=center;verticalAlign=middle;fillColor=#dae8fc;strokeColor=#6c8ebf;",
    "task_service": "shape=mxgraph.bpmn.task;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;fontSize=14;align=center;verticalAlign=middle;fillColor=#d5e8d4;strokeColor=#82b366;",
    "task_manual": "shape=mxgraph.bpmn.task;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;fontSize=14;align=center;verticalAlign=middle;fillColor=#fff2cc;strokeColor=#d6b656;",
    "task_generic": "shape=mxgraph.bpmn.task;whiteSpace=wrap;rectStyle=rounded;size=10;html=1;container=1;expand=0;collapsible=0;taskMarker=abstract;fontSize=14;align=center;verticalAlign=middle;fillColor=#ffffff;strokeColor=#666666;",
    "gateway_exclusive": "shape=mxgraph.bpmn.gateway2;html=1;perimeter=rhombusPerimeter;gwType=exclusive;outlineConnect=0;symbol=none;fontSize=12;verticalLabelPosition=bottom;verticalAlign=top;align=center;labelBackgroundColor=#ffffff;",
    "gateway_parallel": "shape=mxgraph.bpmn.gateway2;html=1;perimeter=rhombusPerimeter;gwType=parallel;outlineConnect=0;symbol=none;fontSize=12;verticalLabelPosition=bottom;verticalAlign=top;align=center;labelBackgroundColor=#ffffff;",
    "gateway_inclusive": "shape=mxgraph.bpmn.gateway2;html=1;perimeter=rhombusPerimeter;gwType=inclusive;outlineConnect=0;symbol=none;fontSize=12;verticalLabelPosition=bottom;verticalAlign=top;align=center;labelBackgroundColor=#ffffff;",
    "event_start": "shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=standard;symbol=general;fontSize=12;",
    "event_end": "shape=mxgraph.bpmn.event;html=1;verticalLabelPosition=bottom;labelBackgroundColor=#ffffff;verticalAlign=top;align=center;perimeter=ellipsePerimeter;outlineConnect=0;aspect=fixed;outline=end;symbol=terminate2;fontSize=12;",
    "edge": "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=14;verticalAlign=middle;labelBackgroundColor=#ffffff;",
}

# Map element tag (local name) → style key (taskType/eventType/gatewayType khi cần)
TASK_STYLE_MAP = {
    "userTask": "task_user",
    "serviceTask": "task_service",
    "manualTask": "task_manual",
    "scriptTask": "task_service",
    "businessRuleTask": "task_service",
    "sendTask": "task_service",
    "receiveTask": "task_user",
    "task": "task_generic",
    "callActivity": "task_generic",
    "subProcess": "task_generic",
}
GATEWAY_STYLE_MAP = {
    "exclusiveGateway": "gateway_exclusive",
    "parallelGateway": "gateway_parallel",
    "inclusiveGateway": "gateway_inclusive",
    "eventBasedGateway": "gateway_exclusive",
    "complexGateway": "gateway_exclusive",
}


@dataclass
class Bounds:
    x: float
    y: float
    w: float
    h: float


@dataclass
class FlowNode:
    id: str
    name: str
    elem_type: str  # local tag, e.g., "userTask", "startEvent"
    bounds: Optional[Bounds] = None
    lane_id: Optional[str] = None


@dataclass
class Lane:
    id: str
    name: str
    bounds: Optional[Bounds] = None
    node_refs: list[str] = field(default_factory=list)


@dataclass
class SequenceFlow:
    id: str
    name: str
    source_ref: str
    target_ref: str
    waypoints: list[tuple[float, float]] = field(default_factory=list)


@dataclass
class Diagram:
    participant_id: str
    participant_name: str
    participant_bounds: Optional[Bounds] = None
    lanes: list[Lane] = field(default_factory=list)
    nodes: list[FlowNode] = field(default_factory=list)
    flows: list[SequenceFlow] = field(default_factory=list)


def _local(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _bounds(elem) -> Optional[Bounds]:
    b = elem.find("dc:Bounds", NS)
    if b is None:
        return None
    return Bounds(
        x=float(b.get("x", 0)),
        y=float(b.get("y", 0)),
        w=float(b.get("width", 0)),
        h=float(b.get("height", 0)),
    )


def parse_bpmn(path: Path) -> Diagram:
    """Parse một file .bpmn → Diagram object."""
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        raise SystemExit(_err(2, f"không parse được XML: {e}", json_mode=False))
    root = tree.getroot()

    # Collaboration + participant
    participant = root.find(".//bpmn:collaboration/bpmn:participant", NS)
    if participant is None:
        raise SystemExit(_err(2, "thiếu <bpmn:collaboration> hoặc <bpmn:participant>", json_mode=False))
    diag = Diagram(
        participant_id=participant.get("id"),
        participant_name=participant.get("name", "Process"),
    )
    process_ref = participant.get("processRef")
    process = root.find(f".//bpmn:process[@id='{process_ref}']", NS)
    if process is None:
        raise SystemExit(_err(2, f"không thấy <bpmn:process id='{process_ref}'>", json_mode=False))

    # Lanes
    for lane_elem in process.findall(".//bpmn:lane", NS):
        lane = Lane(id=lane_elem.get("id"), name=lane_elem.get("name", lane_elem.get("id")))
        for ref in lane_elem.findall("bpmn:flowNodeRef", NS):
            if ref.text:
                lane.node_refs.append(ref.text.strip())
        diag.lanes.append(lane)

    node_to_lane: dict[str, str] = {}
    for lane in diag.lanes:
        for ref in lane.node_refs:
            node_to_lane[ref] = lane.id

    # Flow nodes
    flow_node_tags = (
        set(TASK_STYLE_MAP)
        | set(GATEWAY_STYLE_MAP)
        | {"startEvent", "endEvent", "intermediateThrowEvent", "intermediateCatchEvent", "boundaryEvent"}
    )
    for child in process:
        tag = _local(child.tag)
        if tag not in flow_node_tags:
            continue
        node = FlowNode(
            id=child.get("id"),
            name=child.get("name", ""),
            elem_type=tag,
            lane_id=node_to_lane.get(child.get("id")),
        )
        diag.nodes.append(node)

    # Sequence flows
    for flow_elem in process.findall("bpmn:sequenceFlow", NS):
        diag.flows.append(
            SequenceFlow(
                id=flow_elem.get("id"),
                name=flow_elem.get("name", ""),
                source_ref=flow_elem.get("sourceRef"),
                target_ref=flow_elem.get("targetRef"),
            )
        )

    # BPMNDI — gắn bounds vào participant/lane/node, waypoints vào flow
    plane = root.find(".//bpmndi:BPMNPlane", NS)
    if plane is None:
        raise SystemExit(_err(2, "thiếu <bpmndi:BPMNPlane> — không thể giữ coords", json_mode=False))

    by_id_nodes = {n.id: n for n in diag.nodes}
    by_id_lanes = {l.id: l for l in diag.lanes}
    by_id_flows = {f.id: f for f in diag.flows}

    for shape in plane.findall("bpmndi:BPMNShape", NS):
        ref = shape.get("bpmnElement")
        b = _bounds(shape)
        if not b:
            continue
        if ref == diag.participant_id:
            diag.participant_bounds = b
        elif ref in by_id_lanes:
            by_id_lanes[ref].bounds = b
        elif ref in by_id_nodes:
            by_id_nodes[ref].bounds = b

    for edge in plane.findall("bpmndi:BPMNEdge", NS):
        ref = edge.get("bpmnElement")
        if ref not in by_id_flows:
            continue
        pts: list[tuple[float, float]] = []
        for wp in edge.findall("di:waypoint", NS):
            pts.append((float(wp.get("x", 0)), float(wp.get("y", 0))))
        by_id_flows[ref].waypoints = pts

    return diag


def style_for_node(node: FlowNode) -> str:
    t = node.elem_type
    if t in TASK_STYLE_MAP:
        return STYLE[TASK_STYLE_MAP[t]]
    if t in GATEWAY_STYLE_MAP:
        return STYLE[GATEWAY_STYLE_MAP[t]]
    if t == "startEvent":
        return STYLE["event_start"]
    if t == "endEvent":
        return STYLE["event_end"]
    if t in ("intermediateThrowEvent", "intermediateCatchEvent", "boundaryEvent"):
        return STYLE["event_start"]
    return STYLE["task_generic"]


def to_drawio(diag: Diagram) -> str:
    """Render Diagram → drawio mxgraph XML string."""
    pool = diag.participant_bounds
    if pool is None:
        raise SystemExit(_err(2, "participant không có Bounds — không có coords để chuyển", json_mode=False))

    out: list[str] = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>')
    out.append('<mxfile host="bpmn-to-drawio" type="device">')
    diagram_id = f"d_{uuid.uuid4().hex[:8]}"
    out.append(f'  <diagram id="{diagram_id}" name="{xml_escape(diag.participant_name)}">')
    out.append(
        '    <mxGraphModel grid="0" page="1" gridSize="10" guides="1" tooltips="1" connect="1" '
        'arrows="1" fold="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">'
    )
    out.append("      <root>")
    out.append('        <mxCell id="0" />')
    out.append('        <mxCell id="1" parent="0" />')

    # Pool cell
    pool_id = diag.participant_id
    out.append(
        f'        <mxCell id="{pool_id}" value="{xml_escape(diag.participant_name)}" '
        f'style="{STYLE["pool"]}" vertex="1" parent="1">'
    )
    out.append(
        f'          <mxGeometry x="{pool.x:g}" y="{pool.y:g}" width="{pool.w:g}" height="{pool.h:g}" as="geometry" />'
    )
    out.append("        </mxCell>")

    # Lane cells (parent = pool).
    # BUG FIX (2026-09-18): the source .bpmn (isHorizontal=true, title band on TOP,
    # ~30px margin) is re-rendered here as a VERTICAL swimlane (horizontal=0, title
    # band on the LEFT, startSize=60). Reusing the raw "lb.x - pool.x" (~30) as the
    # lane's relative x makes the lane's own 60px-wide left title band overlap the
    # pool's own 60px-wide left title band (they need to sit side by side: [0,60)
    # pool band, [60,120) lane band) — this was rendering as pool/lane labels
    # overlapping each other. Fix: pin lane x to STARTSIZE and shrink its width by
    # the same delta; compensate child node x by the same delta so absolute
    # positions (and edge waypoints, which are pool-relative and unaffected) stay
    # put — no regression to the "coords match .bpmn gốc" quality bar.
    STARTSIZE = 30
    lane_dx: dict[str, float] = {}
    for lane in diag.lanes:
        lb = lane.bounds
        if not lb:
            # lane không có bounds — skip (BPMN có thể omit nếu pool single-lane)
            continue
        orig_margin = lb.x - pool.x
        right_edge = orig_margin + lb.w
        new_w = right_edge - STARTSIZE
        lane_dx[lane.id] = STARTSIZE - orig_margin
        out.append(
            f'        <mxCell id="{lane.id}" value="{xml_escape(lane.name)}" '
            f'style="{STYLE["lane"]}" vertex="1" parent="{pool_id}">'
        )
        out.append(
            f'          <mxGeometry x="{STARTSIZE:g}" y="{lb.y - pool.y:g}" '
            f'width="{new_w:g}" height="{lb.h:g}" as="geometry" />'
        )
        out.append("        </mxCell>")

    # Flow node cells (parent = lane nếu có lane_id, else pool)
    lane_by_id = {l.id: l for l in diag.lanes}
    for node in diag.nodes:
        if not node.bounds:
            continue
        parent_id = node.lane_id if node.lane_id and node.lane_id in lane_by_id else pool_id
        parent_bounds = lane_by_id[node.lane_id].bounds if (node.lane_id and lane_by_id.get(node.lane_id) and lane_by_id[node.lane_id].bounds) else pool
        rel_x = node.bounds.x - parent_bounds.x
        if node.lane_id and node.lane_id in lane_dx:
            rel_x -= lane_dx[node.lane_id]
        rel_y = node.bounds.y - parent_bounds.y
        out.append(
            f'        <mxCell id="{node.id}" value="{xml_escape(node.name)}" '
            f'style="{style_for_node(node)}" vertex="1" parent="{parent_id}">'
        )
        out.append(
            f'          <mxGeometry x="{rel_x:g}" y="{rel_y:g}" '
            f'width="{node.bounds.w:g}" height="{node.bounds.h:g}" as="geometry" />'
        )
        out.append("        </mxCell>")

    # Edges (parent = pool — common ancestor; drawio resolves source/target by ID)
    for flow in diag.flows:
        out.append(
            f'        <mxCell id="{flow.id}" value="{xml_escape(flow.name)}" '
            f'style="{STYLE["edge"]}" edge="1" parent="{pool_id}" '
            f'source="{flow.source_ref}" target="{flow.target_ref}">'
        )
        if len(flow.waypoints) > 2:
            # Intermediate points (drop endpoints — drawio computes from source/target).
            # BUG FIX (2026-09-18): edge.parent = pool_id, and the pool cell itself
            # sits at absolute (pool.x, pool.y) on the canvas (not reset to 0,0) —
            # so waypoints here must be pool-relative, same as lanes/nodes above.
            # The raw absolute BPMN coords were emitted verbatim, shifting every
            # cross-lane bend +pool.x/+pool.y and routing lines outside the pool
            # (e.g. below its bottom edge) before snapping back to the target task.
            mid_points = flow.waypoints[1:-1]
            out.append('          <mxGeometry relative="1" as="geometry">')
            out.append('            <Array as="points">')
            for x, y in mid_points:
                out.append(f'              <mxPoint x="{x - pool.x:g}" y="{y - pool.y:g}" />')
            out.append("            </Array>")
            out.append("          </mxGeometry>")
        else:
            out.append('          <mxGeometry relative="1" as="geometry" />')
        out.append("        </mxCell>")

    out.append("      </root>")
    out.append("    </mxGraphModel>")
    out.append("  </diagram>")
    out.append("</mxfile>")
    return "\n".join(out) + "\n"


def _err(code: int, msg: str, json_mode: bool) -> str:
    """Format error theo --json envelope hoặc plain text. Return message + sys.exit code."""
    if json_mode:
        out = {"ok": False, "data": None, "error": msg}
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(f"ERROR ({code}): {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(
        prog="bpmn_to_drawio",
        description="Convert .bpmn (BPMN 2.0) → .drawio (mxgraph) với Viindoo brand palette.",
    )
    ap.add_argument("input", help="Đường dẫn file .bpmn input")
    ap.add_argument("-o", "--output", help="Đường dẫn file .drawio output (default: <input>.drawio)")
    ap.add_argument("--json", action="store_true", help="Output JSON envelope {ok, data, error}")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        _err(1, f"file input không tồn tại: {in_path}", args.json)
    out_path = Path(args.output) if args.output else in_path.with_suffix(".drawio")

    try:
        diag = parse_bpmn(in_path)
        drawio_xml = to_drawio(diag)
        out_path.write_text(drawio_xml, encoding="utf-8")
    except SystemExit:
        raise
    except Exception as e:
        _err(3, f"lỗi runtime: {type(e).__name__}: {e}", args.json)

    data = {
        "input": str(in_path),
        "output": str(out_path),
        "counts": {
            "lanes": len(diag.lanes),
            "nodes": len(diag.nodes),
            "flows": len(diag.flows),
        },
        "participant": diag.participant_name,
    }
    if args.json:
        print(json.dumps({"ok": True, "data": data, "error": None}, ensure_ascii=False))
    else:
        print(f"OK  → {out_path}")
        print(f"  participant : {diag.participant_name}")
        print(f"  lanes       : {len(diag.lanes)}")
        print(f"  nodes       : {len(diag.nodes)}")
        print(f"  flows       : {len(diag.flows)}")
        print(f"  open with   : open '{out_path}'")
    sys.exit(0)


if __name__ == "__main__":
    main()
