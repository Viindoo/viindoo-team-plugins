# Viindoo team plugins

Plugin Claude Code dùng chung cho đội presales và marketing Viindoo. Repo private: chỉ thành viên org Viindoo cài được. Danh mục cài đặt nằm ở marketplace công khai [Viindoo/claude-plugins](https://github.com/Viindoo/claude-plugins), trỏ về repo này theo SHA.

| Plugin | Dành cho | Gồm |
|---|---|---|
| `viindoo-presales` | Tư vấn, presales | Skill `spec-from-source`, `spec-to-bpmn`, `bpmn-validate`, `bpmn-to-drawio`, `bpmn-to-html`; lệnh `/viindoo-presales:bpmn-pipeline`; agent `bpmn-builder`, `bpmn-reviewer`, `viindoo-deliverable-reviewer`, `viindoo-source-explorer`; brand Viindoo (`brand/`) |
| `viindoo-marketing` | Marketing, content | Skill `vi` (sinh tiếng Việt qua Gemini), `viindoo-blog-publish` (đăng blog song ngữ viindoo.com dạng nháp); agent `vietnamese-writer` |

## Cài đặt

Trong Claude Code:

```
/plugin marketplace add Viindoo/claude-plugins
/plugin install viindoo-presales@viindoo-plugins
/plugin install viindoo-marketing@viindoo-plugins
```

Chỉ cần plugin nào thì cài plugin đó. Máy phải đăng nhập GitHub có quyền đọc repo này (`gh auth login`). Khi có bản mới: `/plugin marketplace update viindoo-plugins`.

## Chuẩn bị trên máy

| Cần gì | Plugin cần | Cách làm |
|---|---|---|
| Python 3 | presales, marketing | Có sẵn trên macOS |
| Gemini CLI + API key | presales (`spec-from-source`), marketing (`vi`, `vietnamese-writer`) | `brew install gemini-cli`, lấy key tại https://aistudio.google.com/apikey rồi thêm `export GEMINI_API_KEY=...` vào `~/.zshrc`. Đổi model (nếu model mặc định lỗi): `export GEMINI_VI_MODEL=gemini-3.5-flash-lite` |
| Mã nguồn Viindoo | presales (`viindoo-source-explorer`), marketing (`viindoo-blog-publish`) | Clone về `~/viindoo/<phiên bản>/` (ví dụ `~/viindoo/17.0/`), hoặc đặt `export VIINDOO_SRC=<thư mục>` |
| Plugin `odoo-ai-agents` (marketplace `viindoo-plugins`) | nên có | Cho Odoo Semantic MCP (tra mã nguồn nhanh, không cần clone) |
| MCP chrome-devtools + tài khoản quản trị blog viindoo.com | marketing (`viindoo-blog-publish`) | Skill chỉ tạo bài **nháp**; người đăng tự bấm Publish |

## Dùng thế nào

Không cần gõ tên skill, cứ nói việc cần làm:

- "Tao có biên bản họp khách, sinh bộ BPMN giúp" -> chuỗi spec -> BPMN -> drawio/HTML.
- "Review QTUD này trước khi gửi khách" -> `viindoo-deliverable-reviewer`.
- "Viindoo 17 có tính năng X không" -> `viindoo-source-explorer`.
- "Viết caption Facebook cho sự kiện Y" -> `vi`.
- "Đăng bài này lên blog Viindoo" -> `viindoo-blog-publish`.

## Đóng góp

1. Sửa trong `plugins/<tên plugin>/`, tăng `version` trong `.claude-plugin/plugin.json`.
2. Kiểm tra: `claude plugin validate plugins/<tên plugin>`.
3. Chạy thử trên máy: `claude --plugin-dir plugins/<tên plugin>`.
4. Không đưa dữ liệu khách hàng, đường dẫn máy cá nhân hay key vào repo.
5. Merge vào `master` thì workflow `.github/workflows/pin-sha-<tên plugin>.yml` tự mở PR cập nhật SHA bên `Viindoo/claude-plugins` (cần secret `CLAUDE_PLUGINS_PAT`).
