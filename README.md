# Viindoo team plugins

Plugin Claude Code dùng chung cho đội presales và marketing Viindoo. Repo private: chỉ thành viên org Viindoo cài được. Danh mục cài đặt nằm ở marketplace công khai [Viindoo/claude-plugins](https://github.com/Viindoo/claude-plugins), trỏ về repo này theo SHA.

| Plugin | Dành cho | Gồm |
|---|---|---|
| `viindoo-presales` | Tư vấn, presales | **Bộ năm tài liệu hồ sơ khách hàng**: `viindoo-mo-hinh-hoat-dong`, `viindoo-quy-trinh-dap-ung`, `viindoo-danh-muc-br`, `viindoo-phuong-an-de-xuat`, `viindoo-phu-luc-hop-dong`, lệnh `/viindoo-presales:ho-so-khach`. **Bộ BPMN**: `spec-from-source`, `spec-to-bpmn`, `bpmn-validate`, `bpmn-to-drawio`, `bpmn-to-html`, lệnh `/viindoo-presales:bpmn-pipeline`. Agent `bpmn-builder`, `bpmn-reviewer`, `viindoo-deliverable-reviewer`, `viindoo-source-explorer`. Brand (`brand/`) và kit khung tài liệu (`kit/`) |
| `viindoo-implementation` | Tư vấn triển khai, sau khi ký hợp đồng | Skill `viindoo-trien-khai-du-an`, `viindoo-danh-gia-hien-trang` (khách mới: workbook Excel; khách đang dùng hệ thống: rà soát chỉ đọc), `viindoo-quy-trinh-ung-dung` (QTUD HTML/PDF/Word, sơ đồ tự kiểm), `viindoo-viec-thiet-lap` (nội bộ), `viindoo-ke-hoach-du-an` (nhiệm vụ viindoo.com, lịch đào tạo); lệnh `/viindoo-implementation:trien-khai-du-an`. Quy trình và mẫu biểu gốc trên Viin Brain (xem trước: `brain/`). Cần cài cùng `viindoo-presales` |
| `viindoo-marketing` | Marketing, content | Skill `vi` (sinh tiếng Việt qua Gemini), `viindoo-blog-publish` (đăng blog song ngữ viindoo.com dạng nháp); agent `vietnamese-writer` |

## Bộ năm tài liệu hồ sơ khách hàng

Trình tự chuẩn khi tiếp một khách mới, theo mẫu hiện hành (bản Quang Thắng 20/10/2026). Mỗi bước gắn với một mốc trong quy trình presales; bước sau đứng trên bước trước đã được khách xác nhận.

| Bước | Dùng khi | Skill | Ra cái gì | Gửi khách |
|---|---|---|---|---|
| 1 | nhận lead, có hồ sơ khách | `viindoo-mo-hinh-hoat-dong` | Phân tích hiện trạng và mô hình vận hành (HTML) | có |
| 2 | sau khảo sát, có danh sách yêu cầu | `viindoo-quy-trinh-dap-ung` | Quy trình nghiệp vụ mục tiêu và mức đáp ứng (HTML, sơ đồ làn + bốn lớp đáp ứng) | có |
| 3 | nội bộ, trước khi ra giá | `viindoo-danh-muc-br` | Danh mục Yêu cầu Nghiệp vụ (Excel, bóc giờ từng cấp) | **không** |
| 4 | chào giá, trình bày với khách | `viindoo-phuong-an-de-xuat` | Phương án đề xuất triển khai (HTML, báo giá) | có |
| 5 | khách đồng ý, chuẩn bị ký | `viindoo-phu-luc-hop-dong` | Phụ lục 01 - Kế hoạch triển khai và Phạm vi đáp ứng (HTML, PDF đóng dấu) | có |

Sau ký là triển khai dự án - plugin `viindoo-implementation`, nhận phụ lục hợp đồng và danh mục yêu cầu làm đầu vào.

Tài liệu khách mở bằng trình duyệt, đánh dấu và ghi ý kiến ngay trên trang, bấm một nút in phiếu ý kiến ra PDF gửi lại.

Chạy cả bộ có điểm dừng: `/viindoo-presales:ho-so-khach <Khách>`. Khung tài liệu, brand, sơ đồ, mẫu Excel dùng chung nằm ở `plugins/viindoo-presales/kit/` - xem `kit/API.md`.

**Giá:** Triển khai trọn gói hoặc tùy biến tính theo công: chi phí dùng bảng đơn giá theo cấp (Junior / Senior / Expert) có sẵn trong mẫu danh mục yêu cầu (`plugins/viindoo-presales/kit/mau/danh-muc-br.xlsx`, sheet Bảng giá theo manday). Gói Express: chỉ đếm giờ vào gói, không tính tiền theo đơn giá cấp. Giá gói, thuê bao, ưu đãi: hỏi Liên hoặc tra bảng giá hiện hành tại thời điểm báo giá, không mang hệ số của dự án cũ sang.

## Cài đặt

Trong Claude Code:

```
/plugin marketplace add Viindoo/claude-plugins
/plugin install viindoo-presales@viindoo-plugins
/plugin install viindoo-marketing@viindoo-plugins
/plugin install viindoo-implementation@viindoo-plugins
```

Chỉ cần plugin nào thì cài plugin đó. Máy phải đăng nhập GitHub có quyền đọc repo này (`gh auth login`). Khi có bản mới: `/plugin marketplace update viindoo-plugins`.

## Chuẩn bị trên máy

| Cần gì | Plugin cần | Cách làm |
|---|---|---|
| Python 3 | presales, marketing, implementation | Có sẵn trên macOS; implementation cần thêm `pip install openpyxl xlsxwriter python-docx pillow pyyaml` |
| Chrome for Testing | implementation (in PDF, chụp sơ đồ) | `npx @puppeteer/browsers install chrome@stable --path ~/.cache/chrome-for-testing` (không dùng Chrome của người dùng) |
| Kho tài liệu Viindoo | implementation (kiểm liên kết tài liệu ngoại tuyến) | Clone `Viindoo/documentation` về `~/git/viindoo-documentation` hoặc đặt `VIINDOO_DOCS_REPO` |
| Gemini CLI + API key | presales (`spec-from-source`), marketing (`vi`, `vietnamese-writer`) | `brew install gemini-cli`, lấy key tại https://aistudio.google.com/apikey rồi thêm `export GEMINI_API_KEY=...` vào `~/.zshrc`. Đổi model (nếu model mặc định lỗi): `export GEMINI_VI_MODEL=gemini-3.5-flash-lite` |
| Mã nguồn Viindoo | presales (`viindoo-source-explorer`), marketing (`viindoo-blog-publish`) | Clone về `~/viindoo/<phiên bản>/` (ví dụ `~/viindoo/17.0/`), hoặc đặt `export VIINDOO_SRC=<thư mục>` |
| Plugin `odoo-ai-agents` (marketplace `viindoo-plugins`) | nên có | Cho Odoo Semantic MCP (tra mã nguồn nhanh, không cần clone) |
| MCP chrome-devtools + tài khoản quản trị blog viindoo.com | marketing (`viindoo-blog-publish`) | Skill chỉ tạo bài **nháp**; người đăng tự bấm Publish |

## Dùng thế nào

Không cần gõ tên skill, cứ nói việc cần làm:

- "Làm mô hình hoạt động của khách X" -> tài liệu 1 trong bộ bốn.
- "Viindoo đáp ứng tới đâu yêu cầu của khách này" -> tài liệu 2, sơ đồ quy trình + mức đáp ứng bốn lớp.
- "Làm BR cho khách X" -> workbook Excel chuẩn (nội bộ).
- "Làm phương án đề xuất / báo giá cho khách X" -> tài liệu 4 gửi khách.
- "Khách ký rồi, làm phụ lục hợp đồng" -> cắt phụ lục ra từ chính bản phương án.
- "Chạy cả bộ hồ sơ cho khách X" -> `/viindoo-presales:ho-so-khach <Khách>` (dừng giữa các bước để duyệt).
- "Tao có biên bản họp khách, sinh bộ BPMN giúp" -> chuỗi spec -> BPMN -> drawio/HTML.
- "Review QTUD này trước khi gửi khách" -> `viindoo-deliverable-reviewer`.
- "Viindoo 17 có tính năng X không" -> `viindoo-source-explorer`.
- "Khách ký rồi, bắt đầu triển khai cho khách X" -> `viindoo-trien-khai-du-an`.
- "Kiểm file dữ liệu khách mới điền" / "rà soát hệ thống khách đang dùng" -> `viindoo-danh-gia-hien-trang`.
- "Làm bộ quy trình ứng dụng gói 1" -> `viindoo-quy-trinh-ung-dung`.
- "Viết caption Facebook cho sự kiện Y" -> `vi`.
- "Đăng bài này lên blog Viindoo" -> `viindoo-blog-publish`.

## Đóng góp

1. Sửa trong `plugins/<tên plugin>/`, tăng `version` trong `.claude-plugin/plugin.json`.
2. Kiểm tra: `claude plugin validate plugins/<tên plugin>`.
3. Chạy thử trên máy: `claude --plugin-dir plugins/<tên plugin>`.
4. Không đưa dữ liệu khách hàng, đường dẫn máy cá nhân hay key vào repo.
5. Merge vào `master` thì workflow `.github/workflows/pin-sha-<tên plugin>.yml` tự mở PR cập nhật SHA bên `Viindoo/claude-plugins` (cần secret `CLAUDE_PLUGINS_PAT`).
