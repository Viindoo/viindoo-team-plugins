#!/usr/bin/env python3
"""extract_spec — biến source thô (md/text/email/transcript) → spec.md có cấu trúc.

Pipeline:
1. Đọc source file + extract-prompt template.
2. Inject SOURCE_PATH + SOURCE_CONTENT vào prompt.
3. Gọi gemini CLI (gemini-2.5-flash, cần biến môi trường GEMINI_API_KEY).
4. Validate output có header `# Process:` + 6 section bắt buộc.
5. Ghi spec.md.

Zero Python dependency (stdlib only). Phụ thuộc external: `gemini` CLI (brew install gemini-cli).
JSON envelope qua --json. Exit code: 0 success / 1 user / 2 data / 3 system.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_PROMPT = SKILL_DIR / "references" / "extract-prompt.md"

# Section bắt buộc trong spec.md output — dùng để validate Gemini không skip section
REQUIRED_HEADERS = [
    re.compile(r"^# Process:\s+.+", re.MULTILINE),
    re.compile(r"^## Actors\s*$", re.MULTILINE),
    re.compile(r"^## Activities\s*$", re.MULTILINE),
    re.compile(r"^## Decisions\s*$", re.MULTILINE),
    re.compile(r"^## Events\s*$", re.MULTILINE),
    re.compile(r"^## Sequence flow\s*$", re.MULTILINE),
    re.compile(r"^## Gaps & Assumptions\s*$", re.MULTILINE),
]


def _err(code: int, msg: str, json_mode: bool):
    if json_mode:
        print(json.dumps({"ok": False, "data": None, "error": msg}, ensure_ascii=False))
    else:
        print(f"ERROR ({code}): {msg}", file=sys.stderr)
    sys.exit(code)


def build_prompt(template: str, source_path: Path, source_content: str) -> str:
    return template.replace("{{SOURCE_PATH}}", str(source_path)).replace(
        "{{SOURCE_CONTENT}}", source_content
    )


def call_gemini(prompt: str, model: str = "gemini-2.5-flash", timeout_sec: int = 300) -> str:
    """Gọi gemini CLI, return stdout. Throws RuntimeError nếu CLI fail."""
    if not shutil.which("gemini"):
        raise RuntimeError(
            "Không tìm thấy `gemini` CLI. Cài qua `brew install gemini-cli` rồi đặt biến môi trường GEMINI_API_KEY."
        )
    try:
        result = subprocess.run(
            ["gemini", "-m", model, "-p", prompt, "-o", "text"],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"gemini CLI timeout sau {timeout_sec}s — source quá lớn hoặc API chậm. "
            f"Thử --timeout 600 hoặc chia nhỏ source."
        )
    if result.returncode != 0:
        raise RuntimeError(
            f"gemini CLI exit {result.returncode}: {result.stderr.strip()[:500]}"
        )
    return result.stdout


def strip_code_fence(text: str) -> str:
    """Bóc preamble (eg 'Strategic intent...') và code fence Gemini thường wrap quanh output.

    Quy tắc: tìm `# Process:` đầu tiên, cắt bỏ mọi thứ trước. Cắt trailing ``` nếu có.
    """
    text = text.strip()
    # Cắt preamble trước `# Process:`
    m = re.search(r"^# Process:", text, re.MULTILINE)
    if m:
        text = text[m.start():]
    # Cắt trailing code fence (Gemini hay wrap output trong ```markdown ... ```)
    text = text.rstrip()
    if text.endswith("```"):
        text = text[: -3].rstrip()
    return text


def validate_spec(text: str) -> list[str]:
    """Return list các header bị thiếu (empty list = OK)."""
    missing = []
    for pat in REQUIRED_HEADERS:
        if not pat.search(text):
            missing.append(pat.pattern)
    return missing


def main():
    ap = argparse.ArgumentParser(
        prog="extract_spec",
        description="Extract source thô (md/text/email) → spec.md có cấu trúc qua Gemini 2.5 Flash.",
    )
    ap.add_argument("input", help="Đường dẫn source file (md/text/rst/eml)")
    ap.add_argument(
        "-o", "--output", help="Đường dẫn spec.md output (default: <input_basename>.spec.md cùng folder)"
    )
    ap.add_argument(
        "--prompt", default=str(DEFAULT_PROMPT), help=f"Path prompt template (default: {DEFAULT_PROMPT})"
    )
    ap.add_argument("--model", default="gemini-2.5-flash", help="Gemini model (default: 2.5-flash)")
    ap.add_argument("--timeout", type=int, default=300, help="gemini CLI timeout (giây, default 300)")
    ap.add_argument("--json", action="store_true", help="Output JSON envelope")
    ap.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip post-validate (cho phép spec.md thiếu section — debug only)",
    )
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        _err(1, f"source không tồn tại: {in_path}", args.json)
    if in_path.is_dir():
        _err(1, f"input phải là file, không phải folder: {in_path}", args.json)

    prompt_path = Path(args.prompt)
    if not prompt_path.exists():
        _err(1, f"prompt template không tồn tại: {prompt_path}", args.json)

    # Output path
    if args.output:
        out_path = Path(args.output)
    else:
        stem = in_path.stem
        out_path = in_path.parent / f"{stem}.spec.md"

    # Build prompt
    try:
        template = prompt_path.read_text(encoding="utf-8")
        source_content = in_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        _err(2, f"không đọc được file (encoding): {e}", args.json)
    except OSError as e:
        _err(3, f"lỗi I/O đọc input: {e}", args.json)

    if not source_content.strip():
        _err(2, f"source rỗng: {in_path}", args.json)

    prompt = build_prompt(template, in_path, source_content)

    # Call Gemini
    try:
        raw_output = call_gemini(prompt, model=args.model, timeout_sec=args.timeout)
    except RuntimeError as e:
        _err(3, str(e), args.json)

    spec_text = strip_code_fence(raw_output)

    # Validate
    if not args.no_validate:
        missing = validate_spec(spec_text)
        if missing:
            # Ghi raw output ra .raw cho debug
            raw_path = out_path.with_suffix(out_path.suffix + ".raw")
            raw_path.write_text(spec_text, encoding="utf-8")
            _err(
                2,
                f"output Gemini thiếu section: {', '.join(missing)}. Raw saved at: {raw_path}",
                args.json,
            )

    # Write spec.md
    try:
        out_path.write_text(spec_text + ("\n" if not spec_text.endswith("\n") else ""), encoding="utf-8")
    except OSError as e:
        _err(3, f"lỗi I/O ghi output: {e}", args.json)

    # Compute counts (rough)
    actors_count = len(re.findall(r"^\s*-\s+\*\*[^*]+\*\*", spec_text, re.MULTILINE))
    activities_count = len(re.findall(r"^\s*\d+\.\s+\*\*\[", spec_text, re.MULTILINE))

    data = {
        "input": str(in_path),
        "output": str(out_path),
        "input_size_bytes": len(source_content.encode("utf-8")),
        "spec_size_bytes": len(spec_text.encode("utf-8")),
        "model": args.model,
        "rough_counts": {"actors_ish": actors_count, "activities_ish": activities_count},
    }
    if args.json:
        print(json.dumps({"ok": True, "data": data, "error": None}, ensure_ascii=False))
    else:
        print(f"OK  → {out_path}")
        print(f"  input       : {in_path} ({data['input_size_bytes']:,} bytes)")
        print(f"  spec        : {out_path} ({data['spec_size_bytes']:,} bytes)")
        print(f"  model       : {args.model}")
        print(f"  rough counts: ~{actors_count} actors, ~{activities_count} activities")
        print(f"  next step   : python3 ../spec-to-bpmn/scripts/spec_to_bpmn.py '{out_path}'")
    sys.exit(0)


if __name__ == "__main__":
    main()
