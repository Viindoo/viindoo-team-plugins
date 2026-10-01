# Quy tắc deliverable presales Viindoo

> Trích từ bộ luật domain presales. Màu/font/logo: xem `brand.yaml` cùng thư mục.

## Brand Identity Compliance [BẮT BUỘC]

> Mọi deliverable presales Viindoo MUST tuân thủ. Single source of truth: `brand.yaml` (cùng thư mục).

### Trang bìa

- Logo: `logos/viindoo-logo-color.png` (nền sáng) hoặc `viindoo-logo-inverted.png` (nền tối)
- Tên đầy đủ: **CÔNG TY CỔ PHẦN CÔNG NGHỆ VIINDOO**
- Slogan: "One solution for every need"
- Website: viindoo.com

### Color palette

| Vai trò | Hex | Tên |
|---|---|---|
| Primary | `#00BBCE` | Viindoo Cyan |
| Secondary | `#7F4282` | Viindoo Purple |
| Supporting | `#8F8F8F` | Gray |
| BG off-white | `#F2F2F2` | |
| Text heading | `#21272B` | |
| Text body | `#282F33` | |
| Success / Warning / Info | `#00B365` / `#C99700` / `#0099E6` | |

### Font

| Loại deliverable | Font | Size | Style |
|---|---|---|---|
| **QTUD / hợp đồng / hành chính** (theo NĐ 30/2020/NĐ-CP) | **Times New Roman** | 13pt body / 14pt heading | Heading bold ALL CAPS, line-spacing 1.3 |
| Marketing / brochure | Montserrat (heading) + Roboto (body) | tuỳ design | Bold heading, regular body |

### Margin A4 cho tài liệu hành chính

- Top: 2.5 cm
- Bottom: 2.5 cm
- Left: 3.0 cm
- Right: 2.0 cm

### BPMN palette (extract từ Nasilkmex Dệt Lụa QTUD - 47 page reference đã ký)

```yaml
user_task:    fill #dae8fc / stroke #6c8ebf  → Activity người dùng làm trên Viindoo
service_task: fill #d5e8d4 / stroke #82b366  → Activity hệ thống tự (cron, automation)
manual_task:  fill #ffe6cc / stroke #d79b00  → Activity ngoài Viindoo (phải làm tay)
```

Shape: `mxgraph.bpmn.task`, gateway `mxgraph.bpmn.gateway2`, event `mxgraph.bpmn.event`, data `mxgraph.bpmn.data`.

### Boilerplate bắt buộc

| File | Khi nào dùng |
|---|---|
| `boilerplate/section-1-noi-dung.md` | Section 1 mọi QTUD |
| `boilerplate/signature-page.md` | Trang chữ ký cuối mọi deliverable |
| `boilerplate/scm-diagrams/*.png` | Diagram SCM (3 ảnh sẵn) |

## Template Compliance [BẮT BUỘC]

### Mẫu Viindoo VIIN-XXX

- Master list ở Google Sheet nội bộ (hỏi trưởng nhóm presales để lấy link).
- Naming convention: `[MẪU VIIN-XXX]` cho file gốc, `<Loại>-<slug>-v<n>.docx` cho file dùng dự án.
- Loại mẫu: BRD / SRS / SyRS / ITA / LoI / RM / QTUD / Du-toan-tuy-bien / Proposal / executive-summary
- 9 phòng ban chuẩn để cross-reference

**Quy tắc cứng:**
- Khi đã có mẫu VIIN-XXX phù hợp → dùng **Y NGUYÊN**, không sửa structure.
- KHÔNG tự sáng template mới khi đã có VIIN-XXX.
- Khi không chắc dùng template nào → hỏi trưởng nhóm presales, không đoán.

### Reference Drawio

- `reference-drawio/ref-as-is-quy-trinh-ban-hang.drawio`
- `reference-drawio/ref-to-be-viindoo-quy-trinh-ban-hang.drawio`

→ Apply BPMN palette + cấu trúc multi-page swimlane theo các file này.

