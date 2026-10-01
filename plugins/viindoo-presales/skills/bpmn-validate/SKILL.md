---
name: bpmn-validate
description: Kiểm tra 1 file BPMN 2.0 (.bpmn) về (a) cấu trúc XML & integrity tham chiếu, (b) semantic anti-pattern (split-without-join, gateway anchor sharing, unreachable nodes). Trả punch list errors (block hand-off) + warnings (phải sửa trước khi giao khách). Trigger phrase người dùng thực tế gõ - "kiểm tra cái .bpmn này có lỗi không", "validate BPMN trước khi gửi khách", "check diagram có integrity OK chưa", "soi .bpmn xem có anti-pattern". DO NOT use for - sinh .bpmn (→ skill spec-to-bpmn), sửa lỗi tự động (chỉ ra issue, không fix), validate file format khác (.drawio / .vsd / .png), review nội dung nghiệp vụ của process (→ agent BA).
---

# bpmn-validate - Gate-keeper cho file .bpmn

Đầu vào 1 file `.bpmn`. Đầu ra punch list **errors** (cấu trúc sai, file render blank trong bpmn.io) + **warnings** (semantic anti-pattern phải sửa trước khi giao khách). Pure script, deterministic, không gọi LLM.

## Khi nào trigger

- "Kiểm tra cái `.bpmn` này có lỗi không"
- "Validate BPMN trước khi đóng HTML / drawio"
- "Soi diagram xem có split-without-join không"
- "Check integrity tham chiếu trong file BPMN"

## DO NOT use khi

- Cần **sinh** `.bpmn` từ spec - dùng `spec-to-bpmn`, skill này chỉ kiểm.
- Cần **sửa lỗi tự động** - skill này không fix. Issue được surface, sửa ở upstream (spec.md hoặc `.bpmn` thủ công) rồi re-run.
- Cần kiểm `.drawio` / `.vsd` - sai format. Skill này chỉ BPMN 2.0 XML chuẩn OMG.
- Cần review **nội dung nghiệp vụ** (process đúng/sai logic ngành) - đó là việc của BA agent (`viindoo-deliverable-reviewer` hoặc tương đương domain).

## Output

```bash
# Plain mode (human-friendly)
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-validate/scripts/validate_bpmn.py <file.bpmn>

# Agent / pipeline mode (JSON envelope)
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-validate/scripts/validate_bpmn.py <file.bpmn> --json
```

JSON envelope (theo Viindoo v0.3.0 convention):

```json
{
  "ok": true,
  "data": {
    "file": "/path/to/sales.bpmn",
    "summary": {"flow_nodes": 4, "flows": 3, "lanes": 2, "shapes": 7, "edges": 3},
    "errors": [],
    "warnings": []
  },
  "error": null
}
```

Khi có errors → `ok=false`, `error="N validation error(s)"`, `data.errors` chứa list.

## Exit codes

| Code | Khi nào | Ý nghĩa |
|---|---|---|
| `0` | Errors = 0 (warnings OK) | File hợp lệ, có thể chuyển sang `bpmn-to-html` / `bpmn-to-drawio`. |
| `1` | File không tồn tại hoặc args sai | User error - sửa command. |
| `2` | XML không parse được HOẶC có errors validation | **BLOCK hand-off.** Sửa file rồi re-run. |
| `3` | Lỗi hệ thống (đọc file fail) | Kiểm permission / disk. |

Warnings KHÔNG block exit code - chúng quan trọng nhưng skill này coi là "phải sửa trước khi gửi khách", không phải "block render". User/orchestrator quyết định.

## 11 check thực hiện

### Errors (block hand-off - exit 2)

| # | Check | Lý do block |
|---|---|---|
| 1 | XML parse được | File hỏng → mọi tool downstream fail |
| 2 | `sequenceFlow @sourceRef / @targetRef` resolve | Dangling ref → bpmn.io render blank |
| 3 | `<bpmn:flowNodeRef>` trong lane resolve | Sai lane membership → render lỗi |
| 4 | Mỗi flow node trong đúng 1 lane (trừ boundaryEvent) | 0 lane → node bay ngoài pool; >1 lane → ambiguous |
| 5 | Mỗi flow node có `<bpmndi:BPMNShape>` | Thiếu DI → node không hiện trên canvas |
| 6 | Mỗi sequenceFlow có `<bpmndi:BPMNEdge>` | Thiếu DI → flow không hiện |
| 7 | `@bpmnElement` của shape/edge resolve | Dangling DI → render lỗi |
| 8 | `<dc:Bounds>` có `x/y/width/height` | Thiếu coords → bpmn.io không vẽ được |

### Warnings (phải sửa trước khi gửi khách - exit 0 nhưng surface)

| # | Check | Anti-pattern |
|---|---|---|
| 9 | Mọi node reachable từ startEvent | Node cô lập = chết flow |
| 10 | Node non-gateway / non-endEvent nhận ≥2 incoming flow | **Split-without-join** - phải insert merge gateway |
| 11 | Gateway ≥2 outgoing với waypoint đầu trùng tọa độ | Vi phạm **four-edge diamond rule** - flow chồng cạnh, label overlap |

## Workflow

### Bước 1 - Chạy validator

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-validate/scripts/validate_bpmn.py path/to/file.bpmn
```

Hoặc trong pipeline (gọi từ skill khác):

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-validate/scripts/validate_bpmn.py path/to/file.bpmn --json > /tmp/validation.json
exit_code=$?
```

### Bước 2 - Xử lý kết quả

| Exit code | Hành động |
|---|---|
| `0` + 0 warnings | OK tuyệt đối. Chuyển skill kế tiếp. |
| `0` + warnings ≥1 | Surface warnings cho user. Nếu user OK risk → tiếp; mặc định **không** auto-tiếp. |
| `2` | STOP. Báo errors cho user. Quay về upstream sửa (spec.md hoặc .bpmn). |
| `1` / `3` | Báo lỗi hệ thống - kiểm path / permission. |

### Bước 3 - Báo cáo

Default ≤ 300 từ. Format:

```
✓ valid-sales-4step.bpmn - PASS (0 errors, 0 warnings)
  4 nodes, 3 flows, 2 lanes

× broken.bpmn - FAIL (1 error, 2 warnings)
  errors:
    - sequenceFlow Flow_X: targetRef 'Ghost' does not resolve
  warnings:
    ! Task_Merge has 2 incoming flows - missing merge gateway
    ! Gateway_Split: 2 outgoing flows share same anchor (350, 175)
```

## Quy tắc cứng

- KHÔNG sửa file đầu vào - read-only, write file ra `/tmp/` nếu cần annotate.
- KHÔNG suy đoán / fix lỗi - chỉ chỉ ra. Sửa là việc upstream.
- KHÔNG block exit code vì warning - warning ≠ error, để orchestrator quyết.
- Warnings PHẢI có context cụ thể (ID node, tọa độ, số incoming) - không in chung chung.
- Errors PHẢI in vào `stderr` ở plain mode (để pipe dễ); JSON mode in tất ra `stdout` (1 dòng).

## Khi gọi Agent

Skill này KHÔNG gọi agent - pure script, deterministic. Tách bạch với BA review (nội dung nghiệp vụ).

## Sau khi xong

| Output | Bước tiếp |
|---|---|
| Exit 0 + 0 warnings | `bpmn-to-html` (preview khách) hoặc `bpmn-to-drawio` (QTUD ký giấy) |
| Exit 0 + warnings | Báo user → fix `.bpmn` thủ công hoặc sửa `.spec.md` rerun `spec-to-bpmn` |
| Exit 2 | STOP - sửa lỗi cấu trúc trước |

## Dependencies

| Tool | Lý do | Cài |
|---|---|---|
| Python 3.10+ | Chạy script | Có sẵn macOS |
| `xml.etree.ElementTree` | Parse XML (stdlib) | Built-in |

**KHÔNG cần** `lxml` (validator gốc trong skill `bpmn-from-spec` cũ dùng lxml; phiên bản này refactor sang stdlib để zero-dep).

## Anti-patterns

- ❌ Thử auto-fix lỗi (vd thêm merge gateway thiếu) - sai mục đích skill. Fix thuộc upstream.
- ❌ Block exit code vì warning - warning là cảnh báo chất lượng, không phải lỗi cấu trúc.
- ❌ Skip skill này trong pipeline (chuyển thẳng `bpmn-to-html`) - file lỗi → HTML render blank → mất uy tín với khách.
- ❌ Validate nội dung nghiệp vụ ("process này thiếu bước phê duyệt") - đó là BA review, ngoài scope.
- ❌ Thêm dependency lxml lại - đã refactor stdlib, giữ nguyên cho portability.

## Cross-references

- Skill upstream sinh `.bpmn`: `spec-to-bpmn`
- Skill consumer (sau khi PASS): `bpmn-to-html`, `bpmn-to-drawio`
- Sample fixture:
  - `evals/valid-sales-4step.bpmn` - file hợp lệ (0 errors, 0 warnings)
  - `evals/broken-multi-incoming.bpmn` - file lỗi cố ý (1 error + 2 warnings) để smoke test
