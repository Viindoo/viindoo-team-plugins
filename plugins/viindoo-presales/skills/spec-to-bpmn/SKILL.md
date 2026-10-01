---
name: spec-to-bpmn
description: Chuyển 1 file spec.md (theo template chuẩn - Actors / Activities / Decisions / Events / Sequence flow) thành file .bpmn (BPMN 2.0 XML) có sẵn coordinates render được trong bpmn.io. Trigger phrase người dùng thực tế gõ - "tao có spec.md rồi, sinh BPMN giúp tao", "render spec thành diagram", "compile spec.md ra .bpmn", "vẽ BPMN từ structured spec". Áp dụng layout deterministic theo 4-edge gateway + lane-aware cross-lane routing. DO NOT use for - extract spec từ nguồn lộn xộn của khách (→ skill spec-from-source), bundle BPMN thành HTML preview (→ bpmn-to-html), validate BPMN sau khi sinh (→ bpmn-validate), apply Viindoo Nasilkmex palette (→ bpmn-to-drawio).
---

# spec-to-bpmn - Compile spec.md sang BPMN 2.0

Input là 1 file `spec.md` theo template `references/spec-template.md` (đã structure rõ Actors / Activities / Decisions / Events / Sequence flow). Output là 1 file `.bpmn` có đủ `<bpmndi:BPMNDiagram>` (lanes, shapes, edges, coordinates) - bpmn.io render ngay, không phải drag chỉnh tay.

## Khi nào trigger

- "Tao có spec.md rồi, sinh `.bpmn` giúp tao"
- "Compile spec sang BPMN diagram"
- "Render structured spec thành file `.bpmn` mở bpmn.io được"
- "Đổi `spec.md` mới rồi, re-generate `.bpmn`"

## DO NOT use khi

- Nguồn còn lộn xộn (email/biên bản họp/doc khách thô) - `spec.md` chưa có. Dùng `spec-from-source` trước để normalize.
- Muốn preview tương tác cho khách - sinh xong `.bpmn` rồi chạy `bpmn-to-html` sau.
- Cần `.drawio` palette Viindoo (cho QTUD ký giấy) - sinh xong `.bpmn` rồi chuyển `bpmn-to-drawio`.
- Validate cấu trúc / anti-pattern - skill này KHÔNG validate; gọi `bpmn-validate` sau khi sinh.

## Output

```
<spec_dir>/
├── <basename>.spec.md      (input)
└── <basename>.bpmn         (output, hợp lệ BPMN 2.0)
```

Lệnh:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/spec-to-bpmn/scripts/spec_to_bpmn.py <input.spec.md>
python ${CLAUDE_PLUGIN_ROOT}/skills/spec-to-bpmn/scripts/spec_to_bpmn.py <input.spec.md> -o <out.bpmn>
python ${CLAUDE_PLUGIN_ROOT}/skills/spec-to-bpmn/scripts/spec_to_bpmn.py <input.spec.md> --json
```

JSON envelope:

```json
{
  "ok": true,
  "data": {
    "input": "/path/to/sales.spec.md",
    "output": "/path/to/sales.bpmn",
    "summary": {"actors": 2, "nodes": 4, "flows": 3, "pool_width": 618, "pool_height": 300}
  },
  "error": null
}
```

Exit codes:
- `0` - sinh OK
- `1` - file không tồn tại
- `2` - spec sai cấu trúc (thiếu section Actors / Activities, token sequence flow không resolve)
- `3` - lỗi hệ thống

## Workflow

### Bước 1 - Đảm bảo spec.md hợp lệ

`spec.md` PHẢI có đủ các section theo template:

```markdown
# Process: <name>

## Actors
- **Khách hàng** - ...
- **Nhân viên kinh doanh** - ...

## Activities
1. **[Khách hàng]** Gửi yêu cầu báo giá - Type: `userTask`
2. **[Nhân viên kinh doanh]** Duyệt & phát hành báo giá - Type: `userTask`

## Decisions
(optional - list ## Decisions only if có quyết định trong process)

## Events
- **Start:** Khách có nhu cầu
- **End outcomes:**
  - **Báo giá đã gửi** - reached when ...

## Sequence flow
\`\`\`
start → 1
1 → 2
2 → end:Báo giá đã gửi
\`\`\`
```

Xem template đầy đủ: `~/Downloads/bpmn-from-spec/references/spec-template.md`.

### Bước 2 - Compile

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/spec-to-bpmn/scripts/spec_to_bpmn.py path/to/sales.spec.md
```

Default output: `path/to/sales.bpmn` (strip `.spec.md` → `.bpmn`).

### Bước 3 - Validate ngay sau (BẮT BUỘC)

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-validate/scripts/validate_bpmn.py path/to/sales.bpmn
```

Nếu errors → spec sai, sửa `.spec.md` rồi re-run.
Nếu warnings → semantic issue (split-without-join, gateway anchor collision); sửa spec để loại bỏ trước khi bundle HTML / drawio.

### Bước 4 - (Optional) bundle cho khách

```bash
# Preview HTML self-contained
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-to-html/scripts/build_html.py path/to/sales.bpmn

# Hoặc draw.io cho QTUD ký giấy (chưa build skill)
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-to-drawio/scripts/bpmn_to_drawio.py path/to/sales.bpmn
```

## Layout rules áp dụng

Theo `~/Downloads/bpmn-from-spec/references/layout-algorithm.md`:

| Element | Size (w×h) | Vertical anchor trong lane |
|---|---|---|
| Start / End event | 36×36 | center (lane_y + 75) |
| Task (mọi loại) | 100×80 | center (lane_y + 75) |
| Gateway (diamond) | 50×50 | center (lane_y + 75) |

- **Lane order**: theo first-appearance trong section Actors (top → bottom).
- **Column order**: BFS từ `startEvent` qua sequence flow, mỗi node 1 column. Column 0 ở x=200, mỗi column kế tiếp +150px.
- **Same-lane flow**: 2 waypoints, horizontal.
- **Cross-lane flow**: 4 waypoints với vertical leg ở midpoint giữa source-right và target-left.
- **Gateway 4-edge** (≥2 outgoing):
  - Default branch (col lớn nhất) → **right edge**
  - Alt branch xuống lane dưới → **bottom edge**
  - Alt branch lên lane trên → **top edge**
  - Loop-back (target.col < gateway.col) → **left edge**

## ID conventions

| Element | ID pattern | Ví dụ |
|---|---|---|
| Lane | `Lane_<ActorCamel>` | `Lane_KhachHang` |
| Activity | `Task_<VerbObjectCamel>` | `Task_GuiYeuCauBaoGia` |
| Gateway | `Gateway_<n>` | `Gateway_1` |
| Start event | `StartEvent_1` | (luôn 1) |
| End event | `EndEvent_<OutcomeCamel>` | `EndEvent_BaoGiaDaGui` |
| Sequence flow | `Flow_<n>` | `Flow_1` |
| DI shape | `<id>_di` | `StartEvent_1_di` |
| DI edge | `<flow_id>_di` | `Flow_1_di` |

Đảm bảo tiếng Việt có dấu được fold accent (`Khách` → `Khach`).

## Quy tắc cứng

- Input PHẢI là `.md` hoặc `.spec.md`. KHÔNG accept `.docx` / `.pdf` - đó là việc của `spec-from-source`.
- Sinh xong PHẢI gợi user chạy `bpmn-validate` trước khi bundle / gửi khách.
- KHÔNG suy đoán bước thiếu trong spec - báo lỗi `SpecError` thay vì bịa step / actor.
- KHÔNG translate label sang ngôn ngữ khác - giữ nguyên ngôn ngữ spec.
- Layout coordinates PHẢI deterministic - chạy lại cùng spec PHẢI ra cùng `.bpmn` byte-for-byte (trừ tự sinh ID nếu có).

## Khi gọi Agent

Skill này KHÔNG gọi agent - pure parser/layout/emitter, deterministic. Nếu cần normalize nguồn → việc của `spec-from-source` (upstream).

## Sau khi xong

| Use case | Bước tiếp |
|---|---|
| Preview cho khách / demo browser | `bpmn-to-html` |
| QTUD ký giấy (Viindoo) | `bpmn-to-drawio` |
| Xem nhanh trong VSCode | Cài extension `bpmn-io.vs-code-bpmn-io`, mở `.bpmn` |
| Sửa spec | Edit `.spec.md` → re-run skill này → re-validate |

## Dependencies

| Tool | Lý do | Cài |
|---|---|---|
| Python 3.10+ | Chạy script | Có sẵn macOS |
| `xml.sax.saxutils.escape` | XML attribute escape (stdlib) | Built-in |
| `re`, `unicodedata`, `dataclasses` | Parser + slug | Built-in |

**Zero external dependency** - không cần `lxml`, `markdown`, `pyyaml`.

## Limitations (MVP scope)

Hiện chưa support - sẽ tách skill riêng hoặc nâng cấp khi cần:

| Feature | Trạng thái | Lý do |
|---|---|---|
| `parallelGateway` / `inclusiveGateway` | ❌ chưa | MVP chỉ exclusiveGateway. Workaround: model qua nhiều exclusive. |
| `messageStartEvent` / `timerStartEvent` | ❌ chưa | Default plain start. Spec template hiện không có cú pháp đánh dấu trigger type. |
| Boundary events | ❌ chưa | Hiếm trong domain Viindoo presales; sẽ thêm khi gặp case thực. |
| Auto-insert merge gateway | ❌ chưa | Spec PHẢI declare merge gateway explicit (section `## Merge gateways` trong template). Validator sẽ warn nếu thiếu. |
| Multi-pool collaboration | ❌ chưa | MVP 1 pool. External actor là 1 lane trong cùng pool. |
| Sub-process | ❌ chưa | Flatten vào main process. |

Khi gặp case ngoài MVP → báo user thay vì bịa output.

## Anti-patterns

- ❌ Tự suy đoán actor / step khi spec thiếu - báo `SpecError` để user fix `.spec.md`.
- ❌ Skip validation sau khi sinh - `.bpmn` sai cấu trúc → bpmn.io render blank → mất uy tín.
- ❌ Hardcode coordinates - phải đi qua layout pass deterministic.
- ❌ Translate label tự động sang EN khi spec là VN - vi phạm rule "match source language".
- ❌ Reuse 1 file `.bpmn` cho nhiều `.spec.md` - luôn 1-1 mapping, basename trùng.
- ❌ Gọi agent giữa chừng - skill này phải pure deterministic.

## Cross-references

- Skill upstream: `spec-from-source` (sinh `.spec.md` từ nguồn khách lộn xộn)
- Skill downstream:
  - `bpmn-validate` (gate-keeper, BẮT BUỘC sau khi sinh)
  - `bpmn-to-html` (preview khách online)
  - `bpmn-to-drawio` (QTUD ký giấy)
- Template spec: `~/Downloads/bpmn-from-spec/references/spec-template.md`
- Layout algorithm: `~/Downloads/bpmn-from-spec/references/layout-algorithm.md`
- Element catalog (task vs userTask, gateway types): `~/Downloads/bpmn-from-spec/references/element-catalog.md`
- Sample fixture: `evals/sales-4step.spec.md` - round-trip với `bpmn-to-html/evals/sales-4step.bpmn` (handcrafted) - coords match ±2px
