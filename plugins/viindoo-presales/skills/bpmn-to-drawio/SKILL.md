---
name: bpmn-to-drawio
description: Convert một file BPMN 2.0 chuẩn (.bpmn) sang định dạng .drawio (mxgraph XML) để mở/sửa trong draw.io desktop, paste vào QTUD Viindoo multi-page, hoặc xuất PNG/SVG cho deliverable presales. Giữ nguyên coords từ section BPMNDI - KHÔNG tự layout lại. Apply Viindoo brand palette (user task xanh dương #dae8fc, service task xanh lá #d5e8d4, manual task vàng #fff2cc, gateway2 hình thoi mxgraph.bpmn) extract từ Nasilkmex Dệt Lụa QTUD đã ký. Trigger: "convert .bpmn sang .drawio", "đổi BPMN sang drawio để paste vào QTUD", "biến file .bpmn thành drawio Viindoo brand", "tao có .bpmn từ spec-to-bpmn cần mở trong draw.io". DO NOT use for: (1) sinh diagram từ spec (→ spec-to-bpmn); (2) xem nhanh trong browser standalone (→ bpmn-to-html); (3) validate (→ bpmn-validate); (4) re-layout / tự sinh coords (skill này yêu cầu BPMNDI có sẵn); (5) convert ngược .drawio → .bpmn (chưa hỗ trợ).
---

# bpmn-to-drawio

Chuyển file `.bpmn` (BPMN 2.0 XML chuẩn) sang `.drawio` (mxgraph XML) để consultant Viindoo mở/sửa trong draw.io desktop, paste vào QTUD multi-page hoặc export PNG/SVG. Coords giữ nguyên từ BPMNDI, không tự layout lại.

## Khi nào dùng

- Có file `.bpmn` (output từ `spec-to-bpmn`, hoặc từ Camunda Modeler, hoặc bpmn.io export) cần đưa vào pipeline Viindoo presales QTUD.
- Muốn consultant sửa diagram thủ công trong draw.io desktop (drag, thêm gateway, đổi color) thay vì sửa text spec.md.
- Cần multi-page diagram trong QTUD: convert nhiều `.bpmn` thành nhiều `.drawio` rồi merge.
- Cần export PNG/SVG/PDF qua drawio CLI để chèn vào deliverable Word.

KHÔNG dùng khi:

- Source chỉ có spec/intake text (→ `spec-to-bpmn` để có `.bpmn`, rồi mới convert).
- Chỉ cần preview trong browser, không sửa (→ `bpmn-to-html`).
- File `.bpmn` thiếu section `<bpmndi:BPMNDiagram>` (no coords) - skill sẽ exit code 2 "thiếu BPMNPlane". Phải bổ sung coords trước.

## Inputs

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-to-drawio/scripts/bpmn_to_drawio.py <input.bpmn> [-o <output.drawio>] [--json]
```

- `input` - đường dẫn file `.bpmn`.
- `-o / --output` - đường dẫn `.drawio` (default `<input>.drawio` cùng folder).
- `--json` - output JSON envelope `{ok, data, error}` thay vì plain text (cho Agent mode).

Exit code (convention v0.3.0):

- `0` success
- `1` user error - file input không tồn tại / arg sai
- `2` data error - XML không parse / thiếu collaboration / thiếu BPMNPlane / participant không có Bounds
- `3` system error - runtime exception khác

## Workflow

### Bước 1 - Parse .bpmn

Đọc XML bằng `xml.etree.ElementTree` (stdlib, zero-dep). Extract:

- `bpmn:collaboration / bpmn:participant` → pool id + name + processRef
- `bpmn:process` → lanes (id, name, flowNodeRefs), flow nodes (task/event/gateway), sequenceFlows (source/target/name)
- `bpmndi:BPMNDiagram / BPMNPlane` → BPMNShape (Bounds cho participant/lane/node), BPMNEdge (waypoints cho flow)

Nếu thiếu section bắt buộc → exit code 2 với message cụ thể.

### Bước 2 - Map sang mxgraph element + style

Element BPMN → mxgraph (giữ coords gốc):

| BPMN element | drawio mxCell | Style key |
|---|---|---|
| `bpmn:participant` | pool swimlane (parent=root) | `pool` |
| `bpmn:lane` | lane swimlane (parent=pool) | `lane` |
| `bpmn:userTask` | rounded rect | `task_user` (fill #dae8fc) |
| `bpmn:serviceTask` / `scriptTask` / `businessRuleTask` / `sendTask` | rounded rect | `task_service` (fill #d5e8d4) |
| `bpmn:manualTask` / `receiveTask` | rounded rect | `task_manual` (fill #fff2cc) |
| `bpmn:task` / `callActivity` / `subProcess` | rounded rect | `task_generic` (fill #ffffff) |
| `bpmn:exclusiveGateway` | mxgraph.bpmn.gateway2 | `gateway_exclusive` |
| `bpmn:parallelGateway` | mxgraph.bpmn.gateway2 | `gateway_parallel` |
| `bpmn:inclusiveGateway` | mxgraph.bpmn.gateway2 | `gateway_inclusive` |
| `bpmn:startEvent` | ellipse thin | `event_start` |
| `bpmn:endEvent` | ellipse thick (strokeWidth=3) | `event_end` |
| `bpmn:sequenceFlow` | edge orthogonal | `edge` |

Brand palette extract từ `shared-brand/brand.yaml` (Nasilkmex 47-page QTUD đã ký).

### Bước 3 - Tính relative coords

drawio yêu cầu mxGeometry **relative to parent**, BPMN dùng **absolute coords**. Quy đổi:

- Pool: dùng absolute từ Participant BPMNShape
- Lane (parent=pool): `lane.x - pool.x, lane.y - pool.y`
- Flow node (parent=lane chứa nó): `node.x - lane.x, node.y - lane.y`
- Flow node không có lane_id (single-lane pool): dùng pool làm parent, coords relative pool
- Edge: `parent=pool`, `source/target` là node ID. Drawio resolve qua ID.
- Edge waypoints: drop endpoint đầu+cuối (drawio tự compute từ source/target shape), giữ intermediate vertices vào `<Array as="points">`. Edge ≤2 waypoint → không có Array.

### Bước 4 - Emit drawio XML

Template skeleton:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="bpmn-to-drawio" type="device">
  <diagram id="d_<random>" name="<participant name>">
    <mxGraphModel ...>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- pool, lanes, nodes, edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

XML escaping: dùng `xml.sax.saxutils.escape` cho mọi `name` attribute (xử lý `&`, `<`, `>`).

### Bước 5 - Visual verify

```bash
# Trên máy có drawio CLI (brew install --cask drawio):
drawio --no-sandbox --export --format png --output diagram.png diagram.drawio

# Hoặc mở UI:
open diagram.drawio
```

Verify checklist:

1. Pool + lane render đúng số lượng, vertical (horizontal=0).
2. Mỗi node ở đúng lane.
3. Task fill color đúng theo type (user/service/manual).
4. Gateway hình thoi với X/+/O bên trong.
5. Start event mảnh, end event dày.
6. Sequence flow có mũi tên, cross-lane có vertical leg.

## Quality bar

- Coords match `.bpmn` gốc - chỉ chênh nhỏ do startSize/header offset, không re-layout.
- Brand color áp đúng theo task type - KHÔNG tự đổi.
- File mở được trong draw.io desktop **và** drawio CLI export PNG không lỗi.
- XML escape mọi label - pass test với label chứa `&`, `<`, `>`.
- Lane vertical (`horizontal=0`) - Viindoo brand mặc định lane chạy theo chiều ngang (actor ở header trái).
- Skill zero-dep stdlib - chạy được trên máy junior consultant chưa cài lxml/openpyxl.

## Anti-patterns

- ❌ Tự re-layout coords khi BPMN đã có BPMNDI. Nếu BPMN thiếu BPMNDI → exit data error, force user dùng `spec-to-bpmn` trước.
- ❌ Skip `xml_escape` cho name attributes → drawio mở file lỗi parse khi label chứa `&`.
- ❌ Đặt edge.parent = root cell (`"1"`) khi source/target ở cùng pool → drawio không resolve được visual edge. Dùng pool làm parent.
- ❌ Đổi brand color cho "đẹp hơn" - bỏ tính nhất quán với QTUD đã ký Nasilkmex. Tôn trọng palette từ `shared-brand/brand.yaml`.
- ❌ Bỏ qua waypoints giữa của edge khi flow cross-lane → drawio tự routing có thể chèo qua node khác. Giữ intermediate waypoints.
- ❌ Translate label tiếng Việt sang tiếng Anh - giữ ngôn ngữ gốc của .bpmn (đặc biệt deliverable Viindoo VN-only).
- ❌ Hardcode pool/lane size - dùng exact Bounds từ BPMNDI, kể cả khi nhìn "rộng quá".

## Pipeline tích hợp

```
spec.md          spec-to-bpmn          .bpmn          bpmn-to-drawio          .drawio
              ─────────────────────►              ─────────────────────►
                                                  
                  bpmn-validate ↑                  ↓ bpmn-to-html (browser preview)
                  (gate check)                     ↓ drawio CLI export PNG (QTUD chèn Word)
```

Vị trí trong workflow Viindoo presales:

1. Consultant viết `spec.md` (hoặc dùng BA agent normalize từ intake KH).
2. `spec-to-bpmn` → `.bpmn` chuẩn 2.0 + auto-layout 4-edge.
3. `bpmn-validate` gate - sửa lỗi structural/semantic nếu có.
4. **`bpmn-to-drawio`** → `.drawio` để consultant tinh chỉnh trong draw.io (đặt label gateway, edit waypoints, thêm Data Object).
5. Export PNG qua drawio CLI → chèn vào QTUD `.docx` cuối.
6. Optional: `bpmn-to-html` để gửi standalone .html cho KH xem trên browser.

## References

- `scripts/bpmn_to_drawio.py` - converter, ~270 LOC stdlib.
- `evals/sales-4step.bpmn` - fixture input (copy từ `bpmn-to-html/evals/`).
- `evals/sales-4step.drawio` - output reference (đã smoke test PASS visual).
- `evals/sales-4step.png` - PNG export reference (drawio CLI render OK).

## Dependencies

- Python 3.9+ (stdlib `xml.etree.ElementTree`, `xml.sax.saxutils`, `dataclasses`).
- (Optional) `drawio` CLI cho export PNG/SVG: `brew install --cask drawio`.
- KHÔNG cần lxml / openpyxl / pyyaml.
