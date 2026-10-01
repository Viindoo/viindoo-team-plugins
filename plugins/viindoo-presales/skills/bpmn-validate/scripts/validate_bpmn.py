#!/usr/bin/env python3
"""Validate a BPMN 2.0 file (structural + semantic).

Returns ERRORS (block hand-off) and WARNINGS (must address before delivering).

Checks:
  1.  XML parses.
  2.  sequenceFlow @sourceRef / @targetRef resolve to flow node IDs.
  3.  <bpmn:flowNodeRef> inside a lane resolves to a flow node.
  4.  Every flow node is in exactly one lane (boundary events excluded).
  5.  Every flow node has a <bpmndi:BPMNShape>.
  6.  Every sequenceFlow has a <bpmndi:BPMNEdge>.
  7.  BPMNShape/@bpmnElement & BPMNEdge/@bpmnElement resolve.
  8.  BPMNShape has <dc:Bounds> with x/y/width/height attributes.
  9.  Reachability — every node reached from at least one startEvent (warning).
 10.  Semantic — non-gateway/non-endEvent node with ≥2 incoming flows is a
      split-without-join anti-pattern (warning).
 11.  Semantic — gateway with ≥2 outgoing flows starting at the same waypoint
      violates the four-edge diamond routing rule (warning).

Usage:
    validate_bpmn.py <file.bpmn> [--json]

Exit codes (Viindoo v0.3.0 convention):
    0 — valid (warnings allowed; check stderr or JSON `data.warnings`)
    1 — user error (bad args, file not found)
    2 — data error (XML invalid OR validation errors found)
    3 — system error
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}

FLOW_NODE_TAGS = {
    "startEvent", "endEvent", "intermediateCatchEvent", "intermediateThrowEvent",
    "boundaryEvent",
    "task", "userTask", "serviceTask", "manualTask", "scriptTask",
    "receiveTask", "sendTask", "businessRuleTask", "callActivity", "subProcess",
    "exclusiveGateway", "parallelGateway", "inclusiveGateway", "eventBasedGateway",
    "complexGateway",
}

GATEWAY_TAGS = {
    "exclusiveGateway", "parallelGateway", "inclusiveGateway",
    "eventBasedGateway", "complexGateway",
}


def emit_json(ok: bool, data=None, error: str | None = None) -> None:
    print(json.dumps({"ok": ok, "data": data, "error": error}, ensure_ascii=False))


def localname(el: ET.Element) -> str:
    """Return the local (un-namespaced) tag name."""
    tag = el.tag
    return tag.split("}", 1)[1] if "}" in tag else tag


def validate(xml_text: str) -> tuple[list[str], list[str], dict]:
    """Return (errors, warnings, summary_counts). Raises ET.ParseError on bad XML."""
    root = ET.fromstring(xml_text)
    errors: list[str] = []
    warnings: list[str] = []

    flow_nodes: dict[str, str] = {}  # id -> local tag
    for el in root.iter():
        if "}" not in el.tag:
            continue
        ns, local = el.tag[1:].split("}", 1)
        if ns != NS["bpmn"]:
            continue
        if local in FLOW_NODE_TAGS:
            nid = el.get("id")
            if nid:
                flow_nodes[nid] = local

    flows: dict[str, tuple[str, str]] = {}
    for sf in root.iter("{%s}sequenceFlow" % NS["bpmn"]):
        fid = sf.get("id")
        src = sf.get("sourceRef") or ""
        tgt = sf.get("targetRef") or ""
        if not fid:
            errors.append("sequenceFlow without @id")
            continue
        if not src or not tgt:
            errors.append(f"sequenceFlow {fid}: missing sourceRef/targetRef")
        flows[fid] = (src, tgt)
        if src and src not in flow_nodes:
            errors.append(f"sequenceFlow {fid}: sourceRef '{src}' does not resolve")
        if tgt and tgt not in flow_nodes:
            errors.append(f"sequenceFlow {fid}: targetRef '{tgt}' does not resolve")

    node_lanes: dict[str, list[str]] = defaultdict(list)
    lane_ids: set[str] = set()
    for lane in root.iter("{%s}lane" % NS["bpmn"]):
        lid = lane.get("id")
        if lid:
            lane_ids.add(lid)
        for fnr in lane.findall("bpmn:flowNodeRef", NS):
            ref = (fnr.text or "").strip()
            if not ref:
                continue
            if ref not in flow_nodes:
                errors.append(f"lane {lid}: flowNodeRef '{ref}' does not resolve")
            else:
                node_lanes[ref].append(lid or "?")

    for nid, tag in flow_nodes.items():
        if tag == "boundaryEvent":
            continue
        lanes_for = node_lanes.get(nid, [])
        if len(lanes_for) == 0:
            errors.append(f"flow node {nid} ({tag}) is not assigned to any lane")
        elif len(lanes_for) > 1:
            errors.append(f"flow node {nid} ({tag}) is in multiple lanes: {lanes_for}")

    shapes = list(root.iter("{%s}BPMNShape" % NS["bpmndi"]))
    edges = list(root.iter("{%s}BPMNEdge" % NS["bpmndi"]))

    shape_for: dict[str, ET.Element] = {}
    for sh in shapes:
        ref = sh.get("bpmnElement")
        if not ref:
            errors.append("BPMNShape without @bpmnElement")
            continue
        shape_for[ref] = sh
        bounds = sh.find("dc:Bounds", NS)
        if bounds is None:
            errors.append(f"BPMNShape for '{ref}' missing <dc:Bounds>")
        else:
            for attr in ("x", "y", "width", "height"):
                if bounds.get(attr) is None:
                    errors.append(f"BPMNShape for '{ref}': dc:Bounds missing @{attr}")

    edge_for: dict[str, ET.Element] = {}
    edge_waypoints: dict[str, list[tuple[float, float]]] = {}
    for ed in edges:
        ref = ed.get("bpmnElement")
        if not ref:
            errors.append("BPMNEdge without @bpmnElement")
            continue
        edge_for[ref] = ed
        waypoints = ed.findall("di:waypoint", NS)
        if len(waypoints) < 2:
            errors.append(f"BPMNEdge for '{ref}': needs at least 2 di:waypoint (got {len(waypoints)})")
        coords: list[tuple[float, float]] = []
        for wp in waypoints:
            try:
                coords.append((float(wp.get("x", "0")), float(wp.get("y", "0"))))
            except ValueError:
                pass
        if coords:
            edge_waypoints[ref] = coords

    for nid in flow_nodes:
        if nid not in shape_for:
            errors.append(f"flow node {nid} has no corresponding BPMNShape")
    for fid in flows:
        if fid not in edge_for:
            errors.append(f"sequenceFlow {fid} has no corresponding BPMNEdge")
    for lid in lane_ids:
        if lid not in shape_for:
            errors.append(f"lane {lid} has no corresponding BPMNShape")

    process_element_ids: set[str] = set(flow_nodes) | lane_ids | set(flows)
    for p in root.iter("{%s}participant" % NS["bpmn"]):
        if p.get("id"):
            process_element_ids.add(p.get("id"))
    for c in root.iter("{%s}collaboration" % NS["bpmn"]):
        if c.get("id"):
            process_element_ids.add(c.get("id"))

    for sh in shapes:
        ref = sh.get("bpmnElement")
        if ref and ref not in process_element_ids:
            errors.append(f"BPMNShape @bpmnElement='{ref}' does not resolve")
    for ed in edges:
        ref = ed.get("bpmnElement")
        if ref and ref not in process_element_ids:
            errors.append(f"BPMNEdge @bpmnElement='{ref}' does not resolve")

    incoming_count: dict[str, int] = defaultdict(int)
    for fid, (src, tgt) in flows.items():
        if tgt:
            incoming_count[tgt] += 1
    for nid, n_in in incoming_count.items():
        if n_in < 2:
            continue
        tag = flow_nodes.get(nid, "")
        if tag in GATEWAY_TAGS or tag == "endEvent":
            continue
        warnings.append(
            f"node '{nid}' ({tag or 'unknown'}) has {n_in} incoming sequence flows — "
            f"missing merge gateway? (BPMN split-without-join anti-pattern)"
        )

    by_source: dict[str, list[str]] = defaultdict(list)
    for fid, (src, _tgt) in flows.items():
        if flow_nodes.get(src, "") in GATEWAY_TAGS:
            by_source[src].append(fid)
    for src, fids in by_source.items():
        if len(fids) < 2:
            continue
        first_points: dict[tuple[float, float], list[str]] = defaultdict(list)
        for fid in fids:
            wps = edge_waypoints.get(fid, [])
            if wps:
                first_points[wps[0]].append(fid)
        for pt, sharing in first_points.items():
            if len(sharing) >= 2:
                warnings.append(
                    f"gateway '{src}' has {len(sharing)} outgoing flows starting at the same "
                    f"point {pt}: {sharing} — use distinct diamond edges (right/top/bottom/left)"
                )

    if flow_nodes:
        starts = [nid for nid, tag in flow_nodes.items() if tag == "startEvent"]
        if not starts:
            warnings.append("no startEvent found in process")
        if not any(tag == "endEvent" for tag in flow_nodes.values()):
            warnings.append("no endEvent found in process")
        reachable: set[str] = set()
        stack = list(starts)
        while stack:
            n = stack.pop()
            if n in reachable:
                continue
            reachable.add(n)
            for _fid, (src, tgt) in flows.items():
                if src == n and tgt not in reachable:
                    stack.append(tgt)
        unreached = set(flow_nodes) - reachable
        if unreached:
            sample = sorted(unreached)[:5]
            more = "..." if len(unreached) > 5 else ""
            warnings.append(
                f"{len(unreached)} node(s) not reachable from any startEvent: {sample}{more}"
            )

    summary = {
        "flow_nodes": len(flow_nodes),
        "flows": len(flows),
        "lanes": len(lane_ids),
        "shapes": len(shapes),
        "edges": len(edges),
    }
    return errors, warnings, summary


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", help="Path to BPMN file")
    parser.add_argument("--json", action="store_true", help="Emit JSON I/O envelope on stdout")
    args = parser.parse_args(argv)

    as_json = args.json
    path = Path(args.input).expanduser()
    if not path.exists():
        if as_json:
            emit_json(False, None, f"file not found: {path}")
        else:
            print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    try:
        xml_text = path.read_text(encoding="utf-8")
        errors, warnings, summary = validate(xml_text)
    except ET.ParseError as e:
        if as_json:
            emit_json(False, None, f"XML syntax error: {e}")
        else:
            print(f"FAIL: XML syntax error: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        if as_json:
            emit_json(False, None, f"cannot read file: {e}")
        else:
            print(f"ERROR: cannot read file: {e}", file=sys.stderr)
        return 3

    payload = {
        "file": str(path),
        "summary": summary,
        "errors": errors,
        "warnings": warnings,
    }

    if errors:
        if as_json:
            emit_json(False, payload, f"{len(errors)} validation error(s)")
        else:
            print(f"FAIL: {len(errors)} error(s) in {path.name}", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            if warnings:
                print(f"  ({len(warnings)} warning(s) also)", file=sys.stderr)
                for w in warnings:
                    print(f"  ! {w}", file=sys.stderr)
        return 2

    if as_json:
        emit_json(True, payload, None)
    else:
        print(f"OK: {path.name} is valid")
        for k, v in summary.items():
            print(f"  {k:11s}: {v}")
        if warnings:
            print(f"  warnings   : {len(warnings)}")
            for w in warnings:
                print(f"    ! {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
