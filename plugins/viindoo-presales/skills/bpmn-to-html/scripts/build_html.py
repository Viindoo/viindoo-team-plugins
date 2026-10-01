#!/usr/bin/env python3
"""Bundle a .bpmn file into a self-contained .html viewer.

The output HTML works offline: bpmn-js viewer + diagram CSS + bpmn icon font
(base64-inlined woff2) are embedded directly. Double-click the .html in
Finder/Explorer to open in the default browser. No internet required.

Usage:
    build_html.py <input.bpmn> [-o <output.html>] [--title "..."] [--json]

Exit codes:
    0 — success
    1 — user error (bad args, file not found)
    2 — data error (input is not valid BPMN XML)
    3 — system error (vendor assets missing)
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
VENDOR_DIR = SKILL_ROOT / "vendor"
TEMPLATE_PATH = SKILL_ROOT / "references" / "html-template.html"

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"


def emit_json(ok: bool, data=None, error: str | None = None) -> None:
    print(json.dumps({"ok": ok, "data": data, "error": error}, ensure_ascii=False))


def fail(code: int, msg: str, as_json: bool) -> int:
    if as_json:
        emit_json(False, None, msg)
    else:
        print(f"ERROR: {msg}", file=sys.stderr)
    return code


def read_vendor_assets() -> dict[str, str]:
    """Load and return inlined vendor assets. Raises FileNotFoundError if missing."""
    js_path = VENDOR_DIR / "bpmn-viewer.production.min.js"
    diagram_css_path = VENDOR_DIR / "diagram-js.css"
    font_css_path = VENDOR_DIR / "bpmn-font.css"
    woff2_path = VENDOR_DIR / "bpmn.woff2"

    for p in (js_path, diagram_css_path, font_css_path, woff2_path):
        if not p.exists():
            raise FileNotFoundError(f"vendor asset missing: {p}")

    viewer_js = js_path.read_text(encoding="utf-8")
    diagram_css = diagram_css_path.read_text(encoding="utf-8")
    font_css = font_css_path.read_text(encoding="utf-8")

    # Inline woff2 as base64 data URL, drop the other @font-face src formats.
    woff2_b64 = base64.b64encode(woff2_path.read_bytes()).decode("ascii")
    data_url = f"data:font/woff2;base64,{woff2_b64}"
    # Replace the entire `src:` block in @font-face with a single woff2 data URL.
    # The original block spans multiple lines from "src: url('../font/bpmn.eot..."
    # to "format('svg');" — match it as one chunk.
    font_css = re.sub(
        r"src:\s*url\(['\"]\.\./font/bpmn\.eot[^;]+;\s*"
        r"src:[^;]+;",
        f"src: url('{data_url}') format('woff2');",
        font_css,
        count=1,
        flags=re.DOTALL,
    )

    return {
        "viewer_js": viewer_js,
        "diagram_css": diagram_css,
        "bpmn_font_css": font_css,
    }


def parse_bpmn_summary(xml_text: str) -> dict[str, int]:
    """Extract simple element counts from BPMN. Raises ET.ParseError on bad XML."""
    root = ET.fromstring(xml_text)
    ns = {"bpmn": BPMN_NS}
    counts = {
        "lanes": len(root.findall(".//bpmn:lane", ns)),
        "tasks": sum(
            len(root.findall(f".//bpmn:{t}", ns))
            for t in ("task", "userTask", "serviceTask", "manualTask", "scriptTask",
                      "receiveTask", "sendTask", "businessRuleTask", "callActivity")
        ),
        "gateways": sum(
            len(root.findall(f".//bpmn:{g}", ns))
            for g in ("exclusiveGateway", "parallelGateway", "inclusiveGateway",
                      "eventBasedGateway", "complexGateway")
        ),
        "events": sum(
            len(root.findall(f".//bpmn:{e}", ns))
            for e in ("startEvent", "endEvent", "intermediateCatchEvent",
                      "intermediateThrowEvent", "boundaryEvent")
        ),
        "flows": len(root.findall(".//bpmn:sequenceFlow", ns)),
    }
    return counts


def derive_title(xml_text: str, fallback: str) -> str:
    """Pick a human title: <bpmn:participant @name> > <bpmn:process @name> > fallback."""
    try:
        root = ET.fromstring(xml_text)
        ns = {"bpmn": BPMN_NS}
        p = root.find(".//bpmn:participant", ns)
        if p is not None and p.get("name"):
            return p.get("name") or fallback
        proc = root.find(".//bpmn:process", ns)
        if proc is not None and proc.get("name"):
            return proc.get("name") or fallback
    except ET.ParseError:
        pass
    return fallback


def escape_for_script_tag(xml_text: str) -> str:
    """Embed XML inside <script type=application/xml>. Browsers don't parse it,
    but a literal </script> would close the tag. Escape just that sequence."""
    return xml_text.replace("</script", "<\\/script")


def build(input_bpmn: Path, output_html: Path, title_override: str | None) -> dict:
    xml_text = input_bpmn.read_text(encoding="utf-8")
    counts = parse_bpmn_summary(xml_text)  # raises on bad XML

    assets = read_vendor_assets()

    title = title_override or derive_title(xml_text, input_bpmn.stem)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    counts_str = (
        f"{counts['lanes']} lanes · {counts['tasks']} tasks · "
        f"{counts['gateways']} gateways · {counts['events']} events · "
        f"{counts['flows']} flows"
    )

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    html = (template
            .replace("{{TITLE}}", html_escape(title))
            .replace("{{SOURCE_NAME}}", html_escape(input_bpmn.name))
            .replace("{{GENERATED_AT}}", generated_at)
            .replace("{{ELEMENT_COUNTS}}", html_escape(counts_str))
            .replace("{{DIAGRAM_CSS}}", assets["diagram_css"])
            .replace("{{BPMN_FONT_CSS}}", assets["bpmn_font_css"])
            .replace("{{BPMN_VIEWER_JS}}", assets["viewer_js"])
            .replace("{{BPMN_XML}}", escape_for_script_tag(xml_text)))

    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")

    return {
        "input": str(input_bpmn),
        "output": str(output_html),
        "size_bytes": output_html.stat().st_size,
        "title": title,
        "counts": counts,
    }


def html_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", help="Path to input .bpmn file")
    parser.add_argument("-o", "--output", help="Output .html path (default: <input>.html)")
    parser.add_argument("--title", help="Override the title shown in the topbar")
    parser.add_argument("--json", action="store_true", help="Emit JSON I/O envelope on stdout")
    args = parser.parse_args(argv)

    as_json = args.json
    input_bpmn = Path(args.input).expanduser().resolve()
    if not input_bpmn.exists():
        return fail(1, f"input file not found: {input_bpmn}", as_json)
    if input_bpmn.suffix.lower() not in (".bpmn", ".xml"):
        return fail(1, f"expected .bpmn or .xml input, got: {input_bpmn.suffix}", as_json)

    if args.output:
        output_html = Path(args.output).expanduser().resolve()
    else:
        output_html = input_bpmn.with_suffix(".html")

    try:
        result = build(input_bpmn, output_html, args.title)
    except ET.ParseError as e:
        return fail(2, f"input is not valid BPMN XML: {e}", as_json)
    except FileNotFoundError as e:
        return fail(3, str(e), as_json)

    if as_json:
        emit_json(True, result, None)
    else:
        print(f"OK: wrote {output_html}")
        print(f"  size : {result['size_bytes'] / 1024:.1f} KB")
        print(f"  title: {result['title']}")
        c = result["counts"]
        print(f"  counts: {c['lanes']} lanes, {c['tasks']} tasks, "
              f"{c['gateways']} gateways, {c['events']} events, {c['flows']} flows")
        print(f"  open with: open '{output_html}'")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
