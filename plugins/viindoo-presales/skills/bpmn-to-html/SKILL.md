---
name: bpmn-to-html
description: Đóng gói file .bpmn (BPMN 2.0 XML có sẵn) thành 1 file .html self-contained, double-click mở browser xem được offline. Trigger phrase người dùng thực tế gõ - "biến cái .bpmn này thành HTML để gửi khách", "đóng gói diagram cho khách double-click xem", "render BPMN dạng HTML đính Viindoo CRM được", "tao có .bpmn rồi, làm bản HTML preview". Output là 1 file ~230KB chứa inline bpmn-js viewer + inline BPMN XML + inline font (base64 woff2). DO NOT use for - sinh BPMN từ requirement (→ skill spec-to-bpmn), sửa nội dung BPMN, apply Viindoo Nasilkmex palette (→ skill bpmn-to-drawio), validate cấu trúc BPMN (→ skill bpmn-validate).
---

# bpmn-to-html - Đóng gói BPMN thành HTML self-contained

Input 1 file `.bpmn` (BPMN 2.0 XML có sẵn) → output 1 file `.html` đứng độc lập. Khách double-click file HTML là mở browser xem diagram được, không cần internet, không cần cài VSCode hay extension.

## Khi nào trigger

- "Có file `.bpmn` rồi, đóng gói thành HTML để gửi khách"
- "Render BPMN ra HTML để đính Viindoo CRM / Project task"
- "Demo khách lúc trình bày, double-click mở browser xịn luôn"
- "Tao có diagram BPMN, muốn bản preview standalone"

## DO NOT use khi

- Cần sinh `.bpmn` từ requirement / spec → dùng **`spec-to-bpmn`**.
- Cần sửa nội dung BPMN (thêm task, đổi flow) → sửa `.bpmn` trực tiếp rồi re-run skill này.
- Cần `.drawio` palette Nasilkmex (cho QTUD Viindoo ký giấy) → dùng **`bpmn-to-drawio`**.
- Cần validate BPMN (split-without-join, ref integrity) → dùng **`bpmn-validate`** trước, qua gate mới đóng HTML.

## Output

```
<input-dir>/
├── <basename>.bpmn         (input, không động vào)
└── <basename>.html         (output, ~230 KB, self-contained)
```

## Workflow

### Bước 1 - Pre-check input

```bash
# Tồn tại + đúng extension
ls -lh <input.bpmn>
# (Khuyến nghị) chạy validator trước nếu BPMN sinh từ pipeline khác
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-validate/scripts/validate_bpmn.py <input.bpmn>
```

Nếu có error → STOP, không đóng HTML từ file lỗi. Warnings (split-without-join…) thì cho qua, ghi vào report cuối.

### Bước 2 - Bundle thành HTML

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-to-html/scripts/build_html.py <input.bpmn>           # default output: <input>.html
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-to-html/scripts/build_html.py <input.bpmn> -o <out.html>
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-to-html/scripts/build_html.py <input.bpmn> --title "Quy trình Kamito v1.0"
python ${CLAUDE_PLUGIN_ROOT}/skills/bpmn-to-html/scripts/build_html.py <input.bpmn> --json    # agent mode
```

Output JSON envelope (theo Viindoo v0.3.0 convention):

```json
{
  "ok": true,
  "data": {
    "input": "/path/to/sales.bpmn",
    "output": "/path/to/sales.html",
    "size_bytes": 241600,
    "title": "Quy trình bán hàng",
    "counts": {"lanes": 2, "tasks": 2, "gateways": 0, "events": 2, "flows": 3}
  },
  "error": null
}
```

Exit code: `0` success, `1` user error (file thiếu / sai extension), `2` data error (BPMN XML không parse được), `3` system error (vendor asset thiếu).

### Bước 3 - Verify nhanh

```bash
open <basename>.html         # macOS - mở default browser
# Linux: xdg-open
# Windows: start
```

Mắt thường check:
- Diagram render đầy đủ (lanes, tasks, gateways, flows).
- Topbar hiển thị title + element counts.
- 4 nút Fit/+/−/100% bấm có phản hồi.

Test offline: tắt wifi → reload page → vẫn render. Nếu fail → vendor inlining có vấn đề, debug `build_html.py`.

### Bước 4 - Báo cáo

Default output ≤ 300 từ. Tin nhắn cho user gồm:

1. Path file `.html` đã tạo.
2. Size (KB).
3. Element counts (lanes / tasks / gateways / events / flows).
4. Lệnh `open <path>` để user mở thử.

Ví dụ:
```
✓ Bundled <path>/sales.html (236 KB)
  2 lanes, 2 tasks, 0 gateways, 2 events, 3 flows
  Mở thử: open '<path>/sales.html'
```

## Quy tắc cứng

- KHÔNG sửa BPMN XML trong quá trình bundle - input bytes phải bằng output XML embedded (sau khi escape `</script>`).
- KHÔNG dùng CDN script - luôn inline. File phải mở được offline.
- KHÔNG bundle dev build (`bpmn-viewer.development.js` 548KB) - luôn dùng `production.min.js` (181KB).
- Font phải base64-inline (woff2), KHÔNG để url() trỏ vào file ngoài.
- Title trên topbar: ưu tiên `<bpmn:participant @name>` → fallback `<bpmn:process @name>` → fallback tên file. KHÔNG tự bịa title.
- KHÔNG override màu sắc BPMN render - default bpmn.io style là chuẩn (deliverable Viindoo brand-palette dùng `bpmn-to-drawio` thay vì skill này).

## Khi gọi Agent

Skill này KHÔNG gọi agent - pure script + template, deterministic. Nếu cần BA / Viindoo source verify thì việc đó thuộc skill `spec-from-source` (upstream).

## Sau khi xong

| Use case | Bước tiếp |
|---|---|
| Gửi khách demo / preview online | Upload `.html` lên Viindoo CRM / Project attachment. Khách click xem. |
| In QTUD ký giấy | KHÔNG dùng skill này - chuyển sang `bpmn-to-drawio` cho palette Nasilkmex. |
| Iterate diagram | Sửa `.bpmn` (hoặc rerun `spec-to-bpmn` từ `.spec.md` đã update) → rerun `build_html.py`. |

## Dependencies

| Tool | Lý do | Cài |
|---|---|---|
| Python 3.10+ | Chạy `build_html.py` | Có sẵn macOS / dùng `pyenv` |
| `xml.etree.ElementTree` | Parse BPMN summary (stdlib) | Built-in |
| Vendor assets | `vendor/bpmn-viewer.production.min.js`, `vendor/diagram-js.css`, `vendor/bpmn-font.css`, `vendor/bpmn.woff2` | Đã commit sẵn trong skill folder |

**KHÔNG cần** `lxml`, `code` CLI, hay VSCode extension. Đó là chủ đích - `bpmn-to-html` là điểm cuối cho người dùng cuối (khách hàng), không cần dev toolchain.

## Versioning vendor

Đang dùng `bpmn-js@17.11.1`. Khi nâng version:

```bash
cd vendor/
curl -fsSL -o bpmn-viewer.production.min.js "https://unpkg.com/bpmn-js@<X.Y.Z>/dist/bpmn-viewer.production.min.js"
curl -fsSL -o diagram-js.css                "https://unpkg.com/bpmn-js@<X.Y.Z>/dist/assets/diagram-js.css"
curl -fsSL -o bpmn-font.css                 "https://unpkg.com/bpmn-js@<X.Y.Z>/dist/assets/bpmn-font/css/bpmn.css"
curl -fsSL -o bpmn.woff2                    "https://unpkg.com/bpmn-js@<X.Y.Z>/dist/assets/bpmn-font/font/bpmn.woff2"
```

Sau đó re-run `build_html.py evals/sales-4step.bpmn` để smoke test.

## Anti-patterns

- ❌ Để file `.html` phụ thuộc CDN - fail khi khách dùng offline hoặc lúc demo onsite không có wifi.
- ❌ Bundle dev build - file 700KB+ không cần thiết, slow load.
- ❌ Tự sửa nội dung BPMN khi bundle ("optimize", "fix label") - quy tắc: input bytes phải đi vào output không đổi. Sửa là việc của upstream.
- ❌ Apply Viindoo brand palette vào HTML này - sai mục đích skill. `.html` cho preview tương tác (default style); `.drawio` cho deliverable in giấy (Nasilkmex palette).
- ❌ Reuse 1 file `.html` cho nhiều `.bpmn` source - luôn 1-1 mapping, basename trùng.

## Khi nào skill này đáng tách thêm

Hiện tại 1 việc (XML → HTML). Sẽ KHÔNG tách trừ khi:
- Cần thêm bookmark / annotation overlay → tách `bpmn-html-annotated` riêng.
- Cần multi-diagram trong 1 HTML (gallery) → tách `bpmn-html-gallery`.

Trong scope hiện tại: giữ single-purpose.

## Cross-references

- Skill upstream sinh `.bpmn`: `spec-to-bpmn`
- Skill upstream validate: `bpmn-validate`
- Skill song song cho QTUD ký giấy: `bpmn-to-drawio` (cùng plugin này)
- Sample: `evals/sales-4step.bpmn` - file BPMN mẫu để smoke test build_html.py
