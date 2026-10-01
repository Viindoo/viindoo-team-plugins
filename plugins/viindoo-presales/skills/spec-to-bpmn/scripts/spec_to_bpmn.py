#!/usr/bin/env python3
"""Convert a spec.md (per spec-template.md) into a BPMN 2.0 .bpmn file.

Pipeline: parse spec.md → build in-memory model → compute layout coords
(per layout-algorithm.md) → emit BPMN 2.0 XML with laneSet + flow nodes +
sequenceFlows + BPMNShape + BPMNEdge.

MVP scope:
  - Actors/lanes (top-down by first-appearance order)
  - Activities (userTask | serviceTask | manualTask | task)
  - Decisions (exclusiveGateway) with branches
  - Start event (1) + end events (1+ per distinct outcome)
  - Same-lane and cross-lane sequence flows (2-leg vertical routing)
  - Gateway 4-edge anchor selection (default→right, alt→bottom/top, loop→left)

Not yet supported (will warn or error):
  - parallelGateway / inclusiveGateway
  - message / timer start events
  - boundary events
  - auto-insert merge gateway when branches converge (must be declared in spec)

Usage:
    spec_to_bpmn.py <spec.md> [-o <output.bpmn>] [--json]

Exit codes:
    0 — ok
    1 — user error (bad args, missing file)
    2 — spec error (cannot parse, missing required section)
    3 — system error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

# ---------- Model ----------------------------------------------------------

@dataclass
class Actor:
    slug: str
    name: str
    lane_id: str  # "Lane_<Slug>"


@dataclass
class Node:
    id: str
    kind: str       # startEvent | endEvent | userTask | serviceTask | manualTask | task | exclusiveGateway
    name: str
    actor_slug: str
    step: int = -1  # activity step number from spec; -1 for events/gateways
    col: int = -1   # global column index assigned during layout
    cx: float = 0.0 # center x after layout
    cy: float = 0.0 # center y after layout


@dataclass
class Flow:
    id: str
    src: str
    tgt: str
    name: str = ""              # condition label on gateway branches
    waypoints: list[tuple[float, float]] = field(default_factory=list)


@dataclass
class Spec:
    title: str
    actors: list[Actor]
    nodes: list[Node]                  # all flow nodes (events + activities + gateways)
    flows: list[Flow]
    notes: list[str]                   # informational notes during parse


# ---------- Slug & ID helpers ---------------------------------------------

def _strip_accents(s: str) -> str:
    # Vietnamese D-bar (Đ/đ) does NOT decompose via NFKD — pre-replace before normalize.
    s = s.replace("Đ", "D").replace("đ", "d")
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch)
    )

def camel_slug(s: str) -> str:
    """'Khách hàng' → 'KhachHang'."""
    s = _strip_accents(s)
    parts = re.split(r"[^A-Za-z0-9]+", s)
    return "".join(p[:1].upper() + p[1:].lower() for p in parts if p) or "X"

def unique(seen: set[str], candidate: str) -> str:
    if candidate not in seen:
        seen.add(candidate)
        return candidate
    n = 2
    while f"{candidate}_{n}" in seen:
        n += 1
    new = f"{candidate}_{n}"
    seen.add(new)
    return new


# ---------- Parser ---------------------------------------------------------

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

def _section_blocks(md: str) -> dict[str, str]:
    """Split a markdown doc into {section_heading_lower: body_text}."""
    blocks: dict[str, str] = {}
    matches = list(_SECTION_RE.finditer(md))
    for i, m in enumerate(matches):
        heading = m.group(1).strip().lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        blocks[heading] = md[start:end].strip()
    return blocks


def _parse_title(md: str) -> str:
    m = re.search(r"^#\s*Process:\s*(.+?)\s*$", md, re.MULTILINE)
    return m.group(1).strip() if m else "Untitled Process"


def _parse_actors(body: str) -> list[Actor]:
    actors: list[Actor] = []
    seen: set[str] = set()
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        # Form: - **Name** — description     OR     - Name — description
        m = re.match(r"-\s*\*\*([^*]+?)\*\*\s*(?:[—–-]\s*(.*))?$", line)
        if not m:
            m = re.match(r"-\s*([^—–-]+?)\s*(?:[—–-]\s*(.*))?$", line)
        if not m:
            continue
        name = m.group(1).strip()
        if name.lower().startswith("rules"):
            continue
        slug = unique(seen, camel_slug(name))
        actors.append(Actor(slug=slug, name=name, lane_id=f"Lane_{slug}"))
    return actors


def _parse_activities(body: str, actors: list[Actor], seen_ids: set[str]) -> list[Node]:
    nodes: list[Node] = []
    actor_by_name = {a.name.lower(): a for a in actors}
    for line in body.splitlines():
        line = line.strip()
        # Form: "1. **[Actor]** Verb-object — Type: `userTask`"
        m = re.match(
            r"(\d+)\.\s*\*\*\[\s*([^\]]+?)\s*\]\*\*\s*(.+?)\s*(?:—\s*Type:\s*[`']?(\w+)[`']?)?\s*$",
            line,
        )
        if not m:
            continue
        step = int(m.group(1))
        actor_name = m.group(2).strip()
        verb = m.group(3).strip()
        kind = (m.group(4) or "task").strip()
        if kind not in ("task", "userTask", "serviceTask", "manualTask"):
            kind = "task"
        actor = actor_by_name.get(actor_name.lower())
        if not actor:
            raise SpecError(f"Activity step {step}: actor '{actor_name}' không khớp danh sách Actors")
        node_id = unique(seen_ids, f"Task_{camel_slug(verb)}")
        nodes.append(Node(id=node_id, kind=kind, name=verb, actor_slug=actor.slug, step=step))
    return nodes


_DECISION_HEADER_RE = re.compile(
    r"^-\s*\*\*(.+?\?)\*\*\s*after\s+(?:step\s+(\d+|start)|decision\s+G(\d+))\s*$",
    re.IGNORECASE,
)
_BRANCH_RE = re.compile(
    r"^\s+-\s*\*\*([^*]+?)\*\*(?:\s*\((default|mặc định)\))?\s*"
    r"(?:→|->)\s*(?:continues at step\s+(\d+)|continues at decision\s+G(\d+)|ends at\s+(.+?)|goes to\s+(.+?))\s*$",
    re.IGNORECASE,
)


@dataclass
class _Decision:
    id: str
    name: str
    after: str            # "start" or step number string
    branches: list[dict]  # {"label","target","is_default"}


def _parse_decisions(body: str, seen_ids: set[str]) -> list[_Decision]:
    decisions: list[_Decision] = []
    cur: _Decision | None = None
    g_index = 0
    for raw in body.splitlines():
        line = raw.rstrip()
        hm = _DECISION_HEADER_RE.match(line.strip())
        if hm:
            g_index += 1
            gid = unique(seen_ids, f"Gateway_{g_index}")
            after_step = hm.group(2)
            after_decision = hm.group(3)
            if after_step:
                after_val = after_step.strip().lower()
            else:
                after_val = f"decision:{int(after_decision)}"
            # Strip "G1:", "G2: ", etc. prefix if Gemini/author embedded ID in name.
            raw_name = hm.group(1).strip()
            raw_name = re.sub(r"^G\d+\s*[:：]\s*", "", raw_name).strip()
            cur = _Decision(id=gid, name=raw_name, after=after_val, branches=[])
            decisions.append(cur)
            continue
        if cur is None:
            continue
        bm = _BRANCH_RE.match(raw)
        if bm:
            label = bm.group(1).strip()
            is_default = bool(bm.group(2))
            target_step = bm.group(3)
            target_decision = bm.group(4)
            target_end = bm.group(5)
            target_goto = bm.group(6)
            if target_step:
                tgt = ("step", int(target_step))
            elif target_decision:
                tgt = ("decision", int(target_decision))
            elif target_end:
                tgt = ("end", target_end.strip().strip("`'\""))
            elif target_goto:
                tgt = ("step_name", target_goto.strip().strip("`'\""))
            else:
                continue
            cur.branches.append({"label": label, "target": tgt, "is_default": is_default})
    return decisions


_EVENT_START_RE = re.compile(r"^-\s*\*\*Start:\*\*\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
_EVENT_END_RE   = re.compile(r"^\s*-\s*\*\*([^*]+?)\*\*\s*(?:—|-).*?$", re.MULTILINE)


def _parse_events(body: str, seen_ids: set[str]) -> tuple[Node, list[Node]]:
    start_m = _EVENT_START_RE.search(body)
    start_name = start_m.group(1).strip() if start_m else "Start"
    start = Node(id=unique(seen_ids, "StartEvent_1"), kind="startEvent",
                 name=start_name, actor_slug="")  # actor assigned later
    ends: list[Node] = []
    # Find the "End outcomes:" sub-block (accept bare label or **bold** with optional trailing markdown)
    em = re.search(r"End outcomes:\**\s*$", body, re.IGNORECASE | re.MULTILINE)
    if em:
        rest = body[em.end():]
        for line in rest.splitlines():
            mm = re.match(r"\s*-\s*\*\*([^*]+?)\*\*\s*(?:[—–-]\s*.+)?$", line)
            if mm:
                outcome = mm.group(1).strip()
                eid = unique(seen_ids, f"EndEvent_{camel_slug(outcome)}")
                ends.append(Node(id=eid, kind="endEvent", name=outcome, actor_slug=""))
    if not ends:
        ends.append(Node(id=unique(seen_ids, "EndEvent_1"), kind="endEvent",
                         name="End", actor_slug=""))
    return start, ends


# ---------- Sequence flow parser ------------------------------------------

_FLOW_LINE_RE = re.compile(
    r"^\s*(start|end:[^→\->]+|(?:decision\s+)?G\d+(?:\s*\[[^\]]+\])?|\d+)\s*(?:→|->)\s*(start|end:[^→\->]+|(?:decision\s+)?G\d+(?:\s*\[[^\]]+\])?|\d+)\s*$",
    re.IGNORECASE,
)

def _parse_flow_lines(body: str) -> list[tuple[str, str]]:
    """Return list of (token_a, token_b) raw flow edges from the code-block section."""
    edges: list[tuple[str, str]] = []
    # First try code block; else read every matching line in the section.
    code = re.search(r"```[a-z]*\s*\n(.*?)\n```", body, re.DOTALL)
    text = code.group(1) if code else body
    for line in text.splitlines():
        m = _FLOW_LINE_RE.match(line)
        if m:
            edges.append((m.group(1).strip(), m.group(2).strip()))
    return edges


# ---------- Resolve tokens to node IDs ------------------------------------

class SpecError(Exception):
    pass


def _resolve_token(
    tok: str,
    by_step: dict[int, Node],
    by_step_name: dict[str, Node],
    by_end: dict[str, Node],
    start_node: Node,
    decisions: list[_Decision],
) -> tuple[str, str | None]:
    """Return (node_id, branch_label_if_gateway)."""
    s = tok.strip()
    low = s.lower()
    if low == "start":
        return start_node.id, None
    if low.startswith("end:"):
        outcome = s[4:].strip()
        node = by_end.get(outcome.lower())
        if not node:
            # If only one end event exists, accept any "end:..." token
            if len(by_end) == 1:
                node = next(iter(by_end.values()))
            else:
                raise SpecError(f"Sequence flow references unknown end outcome: {outcome}")
        return node.id, None
    # Gateway: "G1", "G1 [branch label]", or "decision G1" (optional prefix)
    s_clean = re.sub(r"^decision\s+", "", s, flags=re.IGNORECASE).strip()
    gm = re.match(r"G(\d+)(?:\s*\[([^\]]+)\])?\s*$", s_clean, re.IGNORECASE)
    if gm:
        idx = int(gm.group(1))
        if idx < 1 or idx > len(decisions):
            raise SpecError(f"Sequence flow references unknown gateway: {s}")
        return decisions[idx - 1].id, (gm.group(2).strip() if gm.group(2) else None)
    # Numeric step
    if s.isdigit():
        step = int(s)
        node = by_step.get(step)
        if not node:
            raise SpecError(f"Sequence flow references unknown step: {step}")
        return node.id, None
    # Activity name fallback
    node = by_step_name.get(low)
    if node:
        return node.id, None
    raise SpecError(f"Sequence flow token unrecognized: {tok}")


# ---------- Main parse ----------------------------------------------------

def parse_spec(md: str) -> Spec:
    title = _parse_title(md)
    sections = _section_blocks(md)

    seen_ids: set[str] = set()

    actors = _parse_actors(sections.get("actors (= bpmn lanes, top to bottom in first-appearance order)", "")
                           or sections.get("actors", ""))
    if not actors:
        raise SpecError("Section ## Actors is missing or empty")

    activities = _parse_activities(sections.get("activities (per actor, in process order)", "")
                                   or sections.get("activities", ""),
                                   actors, seen_ids)
    if not activities:
        raise SpecError("Section ## Activities is missing or empty")

    decisions = _parse_decisions(sections.get("decisions", ""), seen_ids)

    start, ends = _parse_events(sections.get("events", ""), seen_ids)

    # Assign actor to events: start → lane of activity step 1; end → lane of latest activity
    if activities:
        start.actor_slug = activities[0].actor_slug
        for e in ends:
            e.actor_slug = activities[-1].actor_slug

    # Create gateway nodes; assign actor = lane of the step they appear "after"
    # Support "after decision GX" — gateway inherits actor from the referenced gateway.
    # Process in order so "decision:N" can only refer to a previously-declared gateway.
    gateway_nodes: list[Node] = []
    by_step_map = {a.step: a for a in activities}
    for idx, d in enumerate(decisions):
        if d.after == "start":
            gw_actor = start.actor_slug
        elif d.after.startswith("decision:"):
            ref_idx = int(d.after.split(":", 1)[1])
            if ref_idx < 1 or ref_idx > idx:
                raise SpecError(
                    f"Decision G{idx + 1} ('{d.name}') references G{ref_idx} which is "
                    f"either undefined or a forward-reference (must point to an earlier gateway)"
                )
            gw_actor = gateway_nodes[ref_idx - 1].actor_slug
        else:
            try:
                gw_actor = by_step_map[int(d.after)].actor_slug
            except (ValueError, KeyError):
                gw_actor = activities[0].actor_slug
        gateway_nodes.append(Node(id=d.id, kind="exclusiveGateway", name=d.name, actor_slug=gw_actor))

    nodes: list[Node] = [start] + activities + gateway_nodes + ends

    # Build lookup tables for flow resolution
    by_step: dict[int, Node] = {a.step: a for a in activities}
    by_step_name: dict[str, Node] = {a.name.lower(): a for a in activities}
    by_end: dict[str, Node] = {e.name.lower(): e for e in ends}

    # Compose flows
    flows: list[Flow] = []
    seen_flow_ids: set[str] = set()
    flow_lines = _parse_flow_lines(sections.get("sequence flow", "")
                                   or sections.get("sequence flow (one transition per line)", ""))
    if not flow_lines:
        # Fallback: linearize activities in order, prepend start, append end
        chain: list[Node] = [start] + activities + [ends[0]]
        flow_lines = []
        for a, b in zip(chain, chain[1:]):
            flow_lines.append((_token_for(a), _token_for(b)))

    # Convert decision branches (declared in ## Decisions) into flow entries
    # if the user didn't restate them in the Sequence flow block.
    # Normalize tokens (lowercase + strip whitespace + drop "decision " prefix)
    # so explicit form "G1 [Khách cũ]" dedups against auto form "G1[Khách cũ]".
    def _norm(tok: str) -> str:
        t = re.sub(r"^decision\s+", "", tok.strip(), flags=re.IGNORECASE)
        return re.sub(r"\s+", "", t).lower()

    explicit_pairs = {(_norm(a), _norm(b)) for a, b in flow_lines}
    for d in decisions:
        for br in d.branches:
            tgt = br["target"]
            if tgt[0] == "step":
                tok_b = str(tgt[1])
            elif tgt[0] == "end":
                tok_b = f"end:{tgt[1]}"
            elif tgt[0] == "decision":
                tok_b = f"G{tgt[1]}"
            else:
                tok_b = str(tgt[1])
            tok_a = f"G{decisions.index(d)+1}[{br['label']}]"
            # Only add if not already present (allow user to be explicit in flow block)
            pair = (_norm(tok_a), _norm(tok_b))
            if pair not in explicit_pairs:
                flow_lines.append((tok_a, tok_b))
                explicit_pairs.add(pair)

    for a, b in flow_lines:
        try:
            src_id, _ = _resolve_token(a, by_step, by_step_name, by_end, start, decisions)
            tgt_id, branch = _resolve_token(b, by_step, by_step_name, by_end, start, decisions)
        except SpecError:
            raise
        # branch label can come from a (gateway with [label]) OR b (gateway with [label])
        gm_a = re.match(r"G\d+\s*\[([^\]]+)\]", a, re.IGNORECASE)
        branch_label = gm_a.group(1).strip() if gm_a else ""
        fid = unique(seen_flow_ids, f"Flow_{len(flows)+1}")
        flows.append(Flow(id=fid, src=src_id, tgt=tgt_id, name=branch_label))

    return Spec(title=title, actors=actors, nodes=nodes, flows=flows, notes=[])


def _token_for(n: Node) -> str:
    if n.kind == "startEvent":
        return "start"
    if n.kind == "endEvent":
        return f"end:{n.name}"
    if n.kind == "exclusiveGateway":
        return f"G?"
    return str(n.step)


# ---------- Layout --------------------------------------------------------

POOL_X = 100
POOL_Y = 100
LANE_HEIGHT = 200
COL_WIDTH = 280
POOL_HEADER = 30
LANE_HEADER = 30
LEFT_PADDING = 50
EVENT_W = EVENT_H = 36
# TASK_W/TASK_H bumped up from 100x80 (2026-09-18): Vietnamese business-process
# labels ("Mo ta nhiem vu" cells) routinely run 60-100+ chars/multi-clause, and
# at the old size the wrapped text overflowed past the rounded-rect border
# instead of staying inside it. LANE_HEIGHT/COL_WIDTH grown proportionally so
# the vertical/horizontal margin-to-box ratio (and inter-column gap) stays the
# same as before, with no new node-to-node collisions.
TASK_W, TASK_H = 160, 140
GATEWAY_W = GATEWAY_H = 50


def assign_columns(spec: Spec) -> None:
    """Walk the flow graph from the startEvent and assign each node.col."""
    by_id: dict[str, Node] = {n.id: n for n in spec.nodes}
    out_edges: dict[str, list[str]] = {n.id: [] for n in spec.nodes}
    for f in spec.flows:
        if f.src in out_edges:
            out_edges[f.src].append(f.tgt)
    start = next((n for n in spec.nodes if n.kind == "startEvent"), None)
    if not start:
        raise SpecError("No startEvent in spec")

    col = 0
    visited: set[str] = set()
    stack = [start.id]
    order: list[str] = []
    while stack:
        nid = stack.pop(0)  # BFS keeps left-to-right reading order
        if nid in visited:
            continue
        visited.add(nid)
        order.append(nid)
        for tgt in out_edges.get(nid, []):
            if tgt not in visited:
                stack.append(tgt)
    for nid in order:
        by_id[nid].col = col
        col += 1
    # Any unreachable node — append with rising cols (validator will warn later)
    for n in spec.nodes:
        if n.col < 0:
            n.col = col
            col += 1


def assign_coords(spec: Spec) -> tuple[int, int]:
    """Compute cx/cy for each node. Return (pool_width, pool_height)."""
    lane_index = {a.slug: i for i, a in enumerate(spec.actors)}
    max_right = 0
    for n in spec.nodes:
        li = lane_index.get(n.actor_slug, 0)
        lane_y = POOL_Y + li * LANE_HEIGHT
        n.cx = 200 + n.col * COL_WIDTH
        n.cy = lane_y + LANE_HEIGHT / 2
        if n.kind in ("startEvent", "endEvent"):
            right_edge = n.cx + EVENT_W / 2
        elif n.kind == "exclusiveGateway":
            right_edge = n.cx + GATEWAY_W / 2
        else:
            right_edge = n.cx + TASK_W / 2
        if right_edge > max_right:
            max_right = right_edge
    pool_width = int(max_right - POOL_X + 50)  # 50px right margin
    pool_height = LANE_HEIGHT * max(1, len(spec.actors))
    return pool_width, pool_height


def compute_waypoints(spec: Spec) -> None:
    by_id: dict[str, Node] = {n.id: n for n in spec.nodes}
    # Group outgoing flows per gateway to apply four-edge rule
    gw_outgoing: dict[str, list[Flow]] = {}
    for f in spec.flows:
        src = by_id[f.src]
        if src.kind in ("exclusiveGateway", "parallelGateway", "inclusiveGateway"):
            gw_outgoing.setdefault(f.src, []).append(f)

    # Assign edge anchor for each gateway outgoing flow
    flow_anchor: dict[str, str] = {}  # flow.id -> "right"|"top"|"bottom"|"left"
    lane_index = {a.slug: i for i, a in enumerate(spec.actors)}
    for gw_id, outs in gw_outgoing.items():
        gw = by_id[gw_id]
        gw_li = lane_index.get(gw.actor_slug, 0)
        # Pick default — first outgoing, or the one with greatest target.col
        # (largest column = continues main flow rightward)
        outs_sorted = sorted(outs, key=lambda f: by_id[f.tgt].col, reverse=True)
        default_flow = outs_sorted[0]
        flow_anchor[default_flow.id] = "right"
        bottom_taken = False
        top_taken = False
        for f in outs_sorted[1:]:
            tgt = by_id[f.tgt]
            tgt_li = lane_index.get(tgt.actor_slug, gw_li)
            if tgt.col < gw.col:
                flow_anchor[f.id] = "left"  # loop-back
            elif tgt_li > gw_li and not bottom_taken:
                flow_anchor[f.id] = "bottom"; bottom_taken = True
            elif tgt_li < gw_li and not top_taken:
                flow_anchor[f.id] = "top"; top_taken = True
            elif not bottom_taken:
                flow_anchor[f.id] = "bottom"; bottom_taken = True
            elif not top_taken:
                flow_anchor[f.id] = "top"; top_taken = True
            else:
                flow_anchor[f.id] = "left"

    for f in spec.flows:
        src = by_id[f.src]; tgt = by_id[f.tgt]
        src_li = lane_index.get(src.actor_slug, 0)
        tgt_li = lane_index.get(tgt.actor_slug, 0)
        anchor = flow_anchor.get(f.id, "right")
        # Compute source exit point and target entry point
        src_pt = _exit_point(src, anchor)
        tgt_pt = _entry_point(tgt, src, anchor)
        if src_li == tgt_li:
            # Same lane — straight horizontal (2 waypoints)
            f.waypoints = [src_pt, tgt_pt]
        else:
            # Cross lane — vertical leg at midpoint x
            mid_x = (src_pt[0] + tgt_pt[0]) / 2
            f.waypoints = [
                src_pt,
                (mid_x, src_pt[1]),
                (mid_x, tgt_pt[1]),
                tgt_pt,
            ]


def _exit_point(node: Node, anchor: str) -> tuple[float, float]:
    if node.kind == "exclusiveGateway":
        half = GATEWAY_W / 2
        if anchor == "right":  return (node.cx + half, node.cy)
        if anchor == "left":   return (node.cx - half, node.cy)
        if anchor == "top":    return (node.cx, node.cy - half)
        if anchor == "bottom": return (node.cx, node.cy + half)
    if node.kind in ("startEvent", "endEvent"):
        return (node.cx + EVENT_W / 2, node.cy)
    return (node.cx + TASK_W / 2, node.cy)


def _entry_point(node: Node, src: Node, anchor: str) -> tuple[float, float]:
    # Approach from the left for default left-to-right reading.
    if node.kind in ("startEvent", "endEvent"):
        return (node.cx - EVENT_W / 2, node.cy)
    if node.kind == "exclusiveGateway":
        return (node.cx - GATEWAY_W / 2, node.cy)
    return (node.cx - TASK_W / 2, node.cy)


# ---------- Emitter --------------------------------------------------------

def emit_bpmn(spec: Spec, pool_width: int, pool_height: int) -> str:
    title = spec.title
    actor_lanes = ""
    for actor in spec.actors:
        refs = "".join(
            f"        <bpmn:flowNodeRef>{n.id}</bpmn:flowNodeRef>\n"
            for n in spec.nodes if n.actor_slug == actor.slug
        )
        actor_lanes += (
            f'      <bpmn:lane id="{actor.lane_id}" name="{xml_escape(actor.name)}">\n'
            f"{refs}"
            f"      </bpmn:lane>\n"
        )

    node_xml = ""
    for n in spec.nodes:
        attrs = f'id="{n.id}" name="{xml_escape(n.name)}"'
        if n.kind == "exclusiveGateway":
            node_xml += f"    <bpmn:{n.kind} {attrs} />\n"
        else:
            node_xml += f"    <bpmn:{n.kind} {attrs} />\n"

    flow_xml = ""
    for f in spec.flows:
        name_attr = f' name="{xml_escape(f.name)}"' if f.name else ""
        flow_xml += (
            f'    <bpmn:sequenceFlow id="{f.id}" sourceRef="{f.src}" '
            f'targetRef="{f.tgt}"{name_attr} />\n'
        )

    di_shapes = ""
    # Participant pool
    di_shapes += (
        f'      <bpmndi:BPMNShape id="Participant_1_di" bpmnElement="Participant_1" isHorizontal="true">\n'
        f'        <dc:Bounds x="{POOL_X}" y="{POOL_Y}" width="{pool_width}" height="{pool_height}" />\n'
        f"      </bpmndi:BPMNShape>\n"
    )
    # Lanes
    lane_index = {a.slug: i for i, a in enumerate(spec.actors)}
    for actor in spec.actors:
        i = lane_index[actor.slug]
        ly = POOL_Y + i * LANE_HEIGHT
        di_shapes += (
            f'      <bpmndi:BPMNShape id="{actor.lane_id}_di" bpmnElement="{actor.lane_id}" isHorizontal="true">\n'
            f'        <dc:Bounds x="{POOL_X + 30}" y="{ly}" width="{pool_width - 30}" height="{LANE_HEIGHT}" />\n'
            f"      </bpmndi:BPMNShape>\n"
        )
    # Nodes
    # Cap label width to COL_WIDTH - 40 so labels don't overflow into neighbor columns.
    # When text would naturally be wider, allow vertical wrap (height = lines * 14).
    MAX_LABEL_W = COL_WIDTH - 40
    CHAR_W = 7
    LINE_H = 14
    def _label_bounds(name: str, cx: float, cy_below: float) -> tuple[int, int, int, int]:
        text_w = max(60, len(name) * CHAR_W)
        w = min(text_w, MAX_LABEL_W)
        lines = max(1, (len(name) * CHAR_W + w - 1) // w)
        h = lines * LINE_H + (lines - 1) * 2
        return int(cx - w / 2), int(cy_below), w, h

    for n in spec.nodes:
        if n.kind in ("startEvent", "endEvent"):
            w, h = EVENT_W, EVENT_H
            x = n.cx - w / 2
            y = n.cy - h / 2
            lx, ly, lw, lh = _label_bounds(n.name, n.cx, int(y + h + 7))
            label = (
                f'        <bpmndi:BPMNLabel><dc:Bounds '
                f'x="{lx}" y="{ly}" width="{lw}" height="{lh}" /></bpmndi:BPMNLabel>\n'
            )
            di_shapes += (
                f'      <bpmndi:BPMNShape id="{n.id}_di" bpmnElement="{n.id}">\n'
                f'        <dc:Bounds x="{int(x)}" y="{int(y)}" width="{w}" height="{h}" />\n'
                f"{label}"
                f"      </bpmndi:BPMNShape>\n"
            )
        elif n.kind == "exclusiveGateway":
            w, h = GATEWAY_W, GATEWAY_H
            x = n.cx - w / 2
            y = n.cy - h / 2
            lx, ly, lw, lh = _label_bounds(n.name, n.cx, int(y + h + 7))
            label = (
                f'        <bpmndi:BPMNLabel><dc:Bounds '
                f'x="{lx}" y="{ly}" width="{lw}" height="{lh}" /></bpmndi:BPMNLabel>\n'
            )
            di_shapes += (
                f'      <bpmndi:BPMNShape id="{n.id}_di" bpmnElement="{n.id}" isMarkerVisible="true">\n'
                f'        <dc:Bounds x="{int(x)}" y="{int(y)}" width="{w}" height="{h}" />\n'
                f"{label}"
                f"      </bpmndi:BPMNShape>\n"
            )
        else:
            w, h = TASK_W, TASK_H
            x = n.cx - w / 2
            y = n.cy - h / 2
            di_shapes += (
                f'      <bpmndi:BPMNShape id="{n.id}_di" bpmnElement="{n.id}">\n'
                f'        <dc:Bounds x="{int(x)}" y="{int(y)}" width="{w}" height="{h}" />\n'
                f"      </bpmndi:BPMNShape>\n"
            )

    di_edges = ""
    for f in spec.flows:
        wps = "".join(
            f'        <di:waypoint x="{int(round(x))}" y="{int(round(y))}" />\n'
            for (x, y) in f.waypoints
        )
        di_edges += (
            f'      <bpmndi:BPMNEdge id="{f.id}_di" bpmnElement="{f.id}">\n'
            f"{wps}"
            f"      </bpmndi:BPMNEdge>\n"
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
    xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
    xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
    xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
    id="Definitions_1"
    targetNamespace="http://bpmn.io/schema/bpmn"
    exporter="spec-to-bpmn"
    exporterVersion="0.1">

  <bpmn:collaboration id="Collaboration_1">
    <bpmn:participant id="Participant_1" name="{xml_escape(title)}" processRef="Process_1" />
  </bpmn:collaboration>

  <bpmn:process id="Process_1" isExecutable="false">
    <bpmn:laneSet id="LaneSet_1">
{actor_lanes}    </bpmn:laneSet>

{node_xml}
{flow_xml}  </bpmn:process>

  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_1">
{di_shapes}{di_edges}    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
"""


# ---------- CLI ------------------------------------------------------------

def emit_json(ok: bool, data=None, error: str | None = None) -> None:
    print(json.dumps({"ok": ok, "data": data, "error": error}, ensure_ascii=False))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", help="Path to spec.md")
    parser.add_argument("-o", "--output", help="Output .bpmn path (default: <input_basename>.bpmn)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    as_json = args.json

    inp = Path(args.input).expanduser()
    if not inp.exists():
        msg = f"file not found: {inp}"
        if as_json: emit_json(False, None, msg)
        else: print(f"ERROR: {msg}", file=sys.stderr)
        return 1

    if args.output:
        out = Path(args.output).expanduser()
    else:
        # Strip .spec.md → .bpmn (or .md → .bpmn)
        name = inp.name
        if name.endswith(".spec.md"):
            name = name[:-len(".spec.md")]
        elif name.endswith(".md"):
            name = name[:-len(".md")]
        else:
            name = inp.stem
        out = inp.with_name(name + ".bpmn")

    try:
        md = inp.read_text(encoding="utf-8")
        spec = parse_spec(md)
        assign_columns(spec)
        pool_w, pool_h = assign_coords(spec)
        compute_waypoints(spec)
        xml = emit_bpmn(spec, pool_w, pool_h)
    except SpecError as e:
        if as_json: emit_json(False, None, str(e))
        else: print(f"FAIL: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        if as_json: emit_json(False, None, f"unexpected: {e!r}")
        else: print(f"ERROR: unexpected: {e!r}", file=sys.stderr)
        return 3

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(xml, encoding="utf-8")

    summary = {
        "actors": len(spec.actors),
        "nodes": len(spec.nodes),
        "flows": len(spec.flows),
        "pool_width": pool_w,
        "pool_height": pool_h,
    }
    if as_json:
        emit_json(True, {"input": str(inp), "output": str(out), "summary": summary}, None)
    else:
        print(f"OK: wrote {out}")
        for k, v in summary.items():
            print(f"  {k:12s}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
