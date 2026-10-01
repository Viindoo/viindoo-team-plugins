# Sự thật về viindoo.com dùng khi đăng blog

> Ghi tại 2026-10-01. Dữ liệu sống trên viindoo.com luôn là chuẩn: id hay attachment nào không còn thì đọc lại trên web và cập nhật file này.

## Hệ thống

- viindoo.com chạy Odoo 17, DB `i2l3lurxd24s`, website id 1. Ngôn ngữ gốc là EN, có thêm VI.
- Chuỗi "Từ dữ liệu đến Kaizen" đăng trong blog **Digital Transformation** (`blog.blog` id 12).
- **Tác giả:** mỗi người đăng dưới partner của chính mình. Hỏi người dùng partner nào trước khi tạo bài; không tự gán tên người khác.
- Tạo bài EN qua JSON-RPC trong phiên trình duyệt đã đăng nhập (`/web/dataset/call_kw`, context `lang=en_US`).
- Auto Translate: `wizard.confirm.auto.translate.action_confirm` với context model/record_ids, mất 35-80 giây, có lúc trả 502.
- Module dịch tự động chỉ dịch `name`, `subtitle`, `content`. SEO title/description/keywords và `seo_name` phải tự ghi VI. Chạy lại Auto Translate sẽ **đè** `name`/`subtitle` VI, nên luôn ghi lại meta VI sau mỗi lần chạy.
- `viin_website_multilingual_multimedia` coi `src` của ảnh là một đoạn dịch, nên mỗi ngôn ngữ có thể dùng ảnh riêng.
- Upload ảnh: `ir.attachment.create` với `public=True`, `res_model=ir.ui.view` (xem `rpc-snippets.md`).

## Ảnh thật có sẵn trên viindoo.com (attachment id)

| Nội dung | EN | VI |
|---|---|---|
| Work orders | 6873118 | 6874649 |
| MPS | 6873095 | 6873115 |
| Quality Checks trên lệnh sản xuất | 7405159 | 7405160 |
| MO có định mức tiêu hao | 7403893 | - |
| BOM có công đoạn | 7403892 | - |
| BoM Overview giá thành | 7403894 | - |
| Báo cáo Quality (webp) | 996970 | - |
| Màn hình xưởng có máy quét (đã cắt đáy) | 7405174 | - |
| Tiến độ lệnh sản xuất (đã cắt đáy) | 7405175 | - |
| Trung tâm sản xuất OEE (đã cắt đáy) | 7405176 | - |
| Lệnh sản xuất Cost Analysis (đã cắt đáy) | 7405177 | - |
| Cảnh báo chất lượng (đã cắt đáy) | 7405178 | - |

## Phạm vi tính năng Viindoo 17 đã rà mã nguồn (dùng lại, vẫn kiểm lại nếu bài cần chi tiết hơn)

- Điểm kiểm soát chất lượng chọn theo sản phẩm, nhóm sản phẩm, loại hoạt động; **không** theo công đoạn. Quality Alert tạo **bằng tay** (nút Make Alert), không tự sinh khi kiểm tra không đạt.
- "Không đi tiếp nếu không đạt" chỉ chặn phiếu kho; ở sản xuất chỉ chặn khi *chưa* kiểm tra. QR chỉ chạy qua máy quét.
- Công nợ vượt hạn mức chỉ **cảnh báo**, không chặn/duyệt. Không tự ưu tiên lịch đơn gấp, không lập lịch ưu tiên máy. Trễ lead time chỉ hiện cờ; muốn cảnh báo chủ động phải dựng Automation Rules.
- Reordering rule tự chạy qua cron hằng ngày; đề nghị mua sắm sinh RFQ nháp.
- Có ECO (Product Lifecycle `to_mrp_plm`) + ECO Approvals. Block công đoạn bắt buộc chọn lý do. Sửa BoM không bắt buộc nhập lý do (`mrp.bom` không có tracking field). Không có thuê ngoài theo công đoạn.
- IoT/barcode công đoạn có; **không** kết nối CNC/cảm biến.
- Viindoo AI: khách tự mang key (BYO key), có trần chi tiêu và usage log; tool ghi (RFQ/hóa đơn nháp, lead, phê duyệt) **chờ xác nhận**; không có connector chất lượng, không có dự báo AI; `detect_stock_anomalies` chỉ là luật SQL.

## Bẫy riêng của site (bổ sung cho mục "Bẫy đã gặp" trong SKILL.md)

- Mảnh dịch ngay sau link có thể bị trim khoảng trắng: đặt chữ trước link, để mảnh sau link chỉ còn dấu câu.
- Mảnh sau link bắt đầu bằng dấu câu dính liền (": ...") thì phần chữ VI phải đưa lên trước link.
- Ảnh tài liệu EN/VI có thể đảo thứ tự giữa 2 bản (cùng tên file, khác nội dung): xem từng ảnh để ghép cặp.
- Ảnh bìa: nếu ảnh có giao diện Viindoo do AI vẽ thì cảnh báo một lần; người dùng vẫn muốn dùng thì làm theo (ảnh bìa do tác giả quyết).
