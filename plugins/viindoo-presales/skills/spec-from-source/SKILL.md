---
name: spec-from-source
description: Extract một file source thô (markdown/text/email/biên bản phỏng vấn/transcript Zoom) thành spec.md có cấu trúc 6 section (Actors / Activities / Decisions / Events / Sequence flow / Gaps) - input chuẩn cho skill spec-to-bpmn. Dùng Gemini 2.5 Flash CLI (oauth gmail free tier, không cần API key) làm parser. Trigger: "extract spec từ file thô KH gửi", "biến biên bản phỏng vấn thành spec.md", "tao có raw doc cần chuyển thành format spec để vẽ BPMN", "phân tích transcript này thành quy trình có cấu trúc". DO NOT use for: (1) sinh BPMN trực tiếp từ source (→ chain spec-from-source → spec-to-bpmn); (2) re-write/dịch source (→ vietnamese-writer agent); (3) source là xlsx/docx - phải convert sang md/text trước; (4) source > 200KB (Gemini context limit 1M token nhưng quality giảm > 200KB; chia nhỏ trước); (5) khi đã có spec.md sẵn chỉ cần điều chỉnh - edit thẳng file, không cần skill.
---

# spec-from-source

Biến source thô (KH gửi, transcript phỏng vấn, email rời rạc, biên bản họp) thành `spec.md` có cấu trúc 6 section - input chuẩn cho skill `spec-to-bpmn` để sinh BPMN diagram.

## Khi nào dùng

- KH gửi 1 file mô tả quy trình bằng văn xuôi, email forward, hoặc transcript phỏng vấn - cần chuẩn hoá trước khi vẽ diagram.
- Junior consultant viết note phỏng vấn dạng prose, muốn convert sang spec có cấu trúc để feed pipeline BPMN.
- Source có thể rất ngắn (vài câu) hoặc khá dài (transcript 1 buổi phỏng vấn ~ 1-5 trang).

KHÔNG dùng khi:

- Đã có `spec.md` chuẩn (chỉ cần sửa nhẹ) - edit thẳng file, không cần skill.
- Source là xlsx/docx/pdf - convert sang md/text trước (qua `textutil` macOS, `libreoffice --convert-to txt`, hoặc paste manual).
- Source > 200KB - quality Gemini giảm, chia file thành chunk theo phòng ban/process rồi extract từng cái.

## Inputs

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-from-source/scripts/extract_spec.py <source.md> [-o <output.spec.md>] [--model gemini-2.5-flash] [--json] [--no-validate]
```

- `input` - đường dẫn source file (`.md` / `.txt` / `.rst` / `.eml`).
- `-o / --output` - đường dẫn spec.md output (default: `<input_basename>.spec.md`).
- `--prompt` - path prompt template tuỳ chỉnh (default: `references/extract-prompt.md`).
- `--model` - Gemini model (default `gemini-2.5-flash`; có thể đổi `gemini-2.5-pro` cho source phức tạp, chậm hơn ~3x).
- `--json` - JSON envelope `{ok, data, error}` cho Agent mode.
- `--no-validate` - skip post-validate (debug only, dùng khi muốn xem raw output Gemini).

Exit code (convention v0.3.0):

- `0` success
- `1` user error - input không tồn tại / path sai
- `2` data error - source rỗng / encoding lỗi / output Gemini thiếu section bắt buộc
- `3` system error - gemini CLI không cài / timeout / API auth fail

## Workflow

### Bước 1 - Load template + source

Đọc `references/extract-prompt.md` (template VI dài ~5KB) và source file. Inject `{{SOURCE_PATH}}` + `{{SOURCE_CONTENT}}` vào template.

### Bước 2 - Call Gemini CLI

```bash
gemini -m gemini-2.5-flash -p "<prompt>" -o text
```

Auth qua biến môi trường `GEMINI_API_KEY` (gói đăng nhập Gmail miễn phí đã bị Google ngừng). Timeout 180s. Stdout = spec.md content.

Lý do chọn Gemini 2.5 Flash:

- Free tier đủ rộng cho consultant work (hàng chục source/ngày).
- Tiếng Việt fluency tốt (nội dung tiếng Việt giao cho Gemini).
- Tốc độ ~25s cho source 5KB, ~60s cho 50KB.
- Output structured markdown ổn định khi prompt cụ thể.

### Bước 3 - Post-process output

`strip_code_fence()` xử lý 2 thói quen Gemini:

1. Prepend "Strategic intent: I will convert..." trước `# Process:` → cắt bỏ, tìm `# Process:` đầu tiên trong text.
2. Wrap output trong ```` ```markdown ... ``` ```` → cắt trailing fence.

Sau strip, kiểm tra 7 regex section bắt buộc:

- `# Process: <tên>`
- `## Actors`
- `## Activities`
- `## Decisions`
- `## Events`
- `## Sequence flow`
- `## Gaps & Assumptions`

Thiếu bất kỳ section nào → exit code 2 + ghi raw output ra `<output>.raw` để debug.

### Bước 4 - Ghi spec.md + báo cáo

Output text được ghi vào `<basename>.spec.md`. Skill in:

- Đường dẫn output
- Input size + spec size (so sánh delta)
- Rough counts: số actor + số activity (regex count, không chính xác 100% - chỉ để consultant ước lượng nhanh)
- Next command: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-to-bpmn/scripts/spec_to_bpmn.py <spec.md>`

### Bước 5 - Consultant review (loose gate)

`spec.md` từ Gemini thường ~85-90% chính xác. Consultant cần:

1. Đọc `## Actors` - kiểm tra có actor nào bịa không, có actor nào missing không.
2. Đọc `## Activities` - kiểm tra verb-object phrase đúng, Type (`userTask`/`serviceTask`/`manualTask`) hợp lý không.
3. Đọc `## Decisions` - branch label có phải condition thật trong source không, hay là "Yes/No" generic.
4. Đọc `## Sequence flow` - số step trong flow khớp Activities không, có loop không, có flow nào chèo lane lạ không.
5. Đọc `## Gaps & Assumptions` - đây là chỉ báo Gemini biết phần nào source không rõ - consultant cần xác minh với KH.

Sau review → feed thẳng vào `spec-to-bpmn` để sinh `.bpmn`.

## Quality bar

- Output spec.md PASS 7 regex section bắt buộc → exit 0 (validate built-in).
- Tiếng Việt → output tiếng Việt; tiếng Anh → output tiếng Anh. KHÔNG dịch chéo.
- Verb-object phrase ngắn ≤ 7 từ.
- Mọi giả định ghi vào Gaps section, prefix `[ ] Assumed:` hoặc tương đương.
- Round-trip test: `spec.md` → `spec-to-bpmn` → `.bpmn` → `bpmn-validate` 0 errors.

## Anti-patterns

- ❌ Bỏ qua review thủ công Gemini output - Gemini có thể bịa actor "Hệ thống" khi source không nói rõ, miss step ngầm định, hoặc gộp 2 activity thành 1.
- ❌ Feed source > 200KB nguyên cục - Gemini context tự cắt, mất nội dung cuối. Chia chunk theo phòng ban/process.
- ❌ Dùng `--no-validate` ở production - chỉ debug. Validate là gate chất lượng quan trọng.
- ❌ Hard-code `--model gemini-2.5-pro` cho mọi case - Pro chậm ~3x mà Flash đã đủ chất lượng cho 90% case.
- ❌ Skill này gọi skill khác (vd auto chain sang `spec-to-bpmn`) - vi phạm governance rule "Skill làm 1 việc". Caller (main Claude hoặc orchestrator) chịu trách nhiệm chain.
- ❌ Edit prompt template `extract-prompt.md` mỗi lần thấy 1 source lỗi - verify root cause: là source thật sự ambiguous hay prompt thiếu instruction nào.

## Gemini quirks đã phát hiện (qua smoke test)

3 thói quen của Gemini Flash đã được hardcode trong prompt để tránh:

1. **Compound actor** - Gemini hay viết `[A, B] X` khi source nói "A và B cùng làm X". Prompt rule #6 yêu cầu tách thành 2 activity riêng. Vi phạm rule này → `spec-to-bpmn` fail "actor không khớp danh sách Actors".

2. **Mix VI keywords** - Gemini hay dịch "after step" → "sau step", "continues at step" → "tiếp tục ở step". Spec-to-bpmn parser strict EN-only. Prompt phần Decisions có dòng "KEYWORDS CỐ ĐỊNH BẰNG TIẾNG ANH - KHÔNG DỊCH" để khoá.

3. **Gateway naming theo source** - Gemini có xu hướng đặt gateway theo nội dung ("D1: Vòng 1?" từ source "vòng 1"). Spec-to-bpmn chỉ accept `G1, G2, G3...`. Prompt phần Sequence flow có dòng "TUYỆT ĐỐI KHÔNG dùng D1, Decision1, hay tên khác".

Nếu gặp lỗi pipeline mới, check 3 quirk này đầu tiên. Update prompt khi phát hiện thêm.

## Pipeline tích hợp

```
raw source (md/text/email)
  → spec-from-source         → spec.md            6 section, VI/EN match source
  → spec-to-bpmn             → .bpmn              auto-layout 4-edge
  → bpmn-validate            → 0 errors, 0 warns
  → bpmn-to-drawio           → .drawio            consultant edit
  → bpmn-to-html             → .html              KH preview qua browser
```

5 skill này chạy đầy đủ chain → 1 source thô → đủ 5 file artifact (spec / bpmn / drawio / html / png) cho deliverable presales.

## Dependencies

- Python 3.9+ (stdlib only).
- `gemini` CLI: `brew install gemini-cli` rồi đặt `export GEMINI_API_KEY=...` trong `~/.zshrc` (lấy key tại https://aistudio.google.com/apikey).
- Internet (Gemini API call qua CLI).

## References

- `references/extract-prompt.md` - prompt template VI (template spec + nguyên tắc cứng + self-check rules).
- `evals/short-quote-request.md` - fixture ngắn (~600B, quy trình báo giá email).
- `evals/long-interview-transcript.md` - fixture dài (~3.8KB, biên bản phỏng vấn HR Viindoo).
- `evals/<name>.spec.md` - output reference (gen sau khi smoke test PASS).

## Cost

Gemini 2.5 Flash (API key):

- ~60 req/phút, 1500 req/ngày
- Input ~600B → ~25s, ~2300 token (well under quota)
- Input ~3.8KB → ~60s, ~10k token
- Source 50KB → ~120s, ~100k token (chậm nhưng vẫn trong limit)

Nếu vượt free tier → upgrade lên paid API key (~$0.075/1M input token với Flash, vẫn rẻ).
