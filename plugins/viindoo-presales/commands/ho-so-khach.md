---
description: Chạy bộ năm tài liệu presales cho một khách - mô hình hoạt động, quy trình và mức đáp ứng, danh mục BR, phương án đề xuất, phụ lục hợp đồng - có điểm dừng giữa các bước
---

Chạy bộ hồ sơ khách hàng cho khách nêu trong `$ARGUMENTS` (tên khách, hoặc đường dẫn thư mục dự án).

## Quy tắc cứng

1. **Dừng sau mỗi bước.** Mỗi tài liệu là một lần gửi khách; bước sau đứng trên bước trước đã được khách xác nhận. Không tự chạy thẳng cả bộ.
2. **Không đọc lại tệp đã sinh** vào ngữ cảnh - chỉ truyền đường dẫn sang bước sau. Tài liệu bước 2 có thể lên vài trăm KB.
3. **Mỗi bước báo cáo tối đa 10 dòng**: đường dẫn tệp, vài con số đếm, việc cần Liên quyết.
4. **Thư mục dự án**: `~/Documents/project/<Khách>/`, mã nguồn dựng tệp để trong `work/` của chính thư mục đó. Chưa có thì tạo theo quy ước thư mục dự án.
5. **Soạn xong là bản nháp.** Liên đọc rồi mới gửi khách - kể cả khi được bảo "trả lời khách nhé".
6. **Giá:** không lấy hệ số hay đơn giá của dự án cũ; hỏi Liên hoặc tra bảng giá hiện hành.

## Bước 0 - Kiểm đầu vào

Liệt kê những gì đang có trong thư mục dự án: tài liệu khách gửi, ghi chú khảo sát, biên bản họp, tài liệu đã gửi khách trước đó. Thiếu hẳn đầu vào thì dừng và nói rõ thiếu gì, không đoán.

Nêu luôn bước nào đã có tệp rồi để khỏi làm lại.

## Bước 1 - Mô hình hoạt động

Skill `viindoo-presales:viindoo-mo-hinh-hoat-dong`.

Ra: `[<Khách>] 1. Phan tich hien trang va mo hinh van hanh.html`.

Báo: đường dẫn, số phần, danh sách giả thuyết cần khách xác nhận. **Dừng.**

## Bước 2 - Quy trình nghiệp vụ và mức đáp ứng

Chỉ chạy khi bước 1 đã chốt. Skill `viindoo-presales:viindoo-quy-trinh-dap-ung`.

Mọi kết luận đáp ứng phải đọc từ mã nguồn (MCP `odoo-semantic` hoặc agent `viindoo-source-explorer`), không suy từ tên chức năng.

Ra: `[<Khách>] 2. Quy trinh nghiep vu muc tieu va muc dap ung.html`.

Báo: đường dẫn, số quy trình, tỷ lệ bốn lớp, số hạng mục phải làm thêm, các điểm cần khách xác nhận. **Dừng.**

## Bước 3 - Danh mục yêu cầu nghiệp vụ

Skill `viindoo-presales:viindoo-danh-muc-br`. Nguồn là khối đáp ứng của bước 2: mỗi hạng mục thành một dòng BR.

Ra: `Danh mục Yêu cầu Nghiệp vụ Phần mềm - <Khách>.xlsx` - **tài liệu nội bộ, không gửi khách**.

Báo: đường dẫn, số yêu cầu theo từng phân loại, tổng giờ phát triển, tổng chi phí nội bộ, hạng mục còn thiếu giải pháp hoặc còn "Cần làm rõ". **Dừng** - Liên duyệt giờ và phân loại trước khi ra giá.

## Bước 4 - Phương án đề xuất

Skill `viindoo-presales:viindoo-phuong-an-de-xuat`. Giá và phạm vi đọc thẳng từ workbook bước 3.

Giá và quy tắc tính giá: hỏi Liên hoặc tra bảng giá hiện hành - không lấy hệ số hay đơn giá của dự án cũ.

Trước khi báo xong, chạy `vdoc.kiem_ban_gui_khach()`; mức PHẢI SỬA thì sửa, mức cần xem thì đọc trích đoạn rồi quyết.

Ra: `Phuong an de xuat trien khai Viindoo - <Khách>.html`.

Báo: đường dẫn, tổng dịch vụ trả một lần, số hạng mục phát triển ngoài gói, kết quả soát, những điểm Liên cần quyết trước khi gửi. **Dừng.**

## Bước 5 - Phụ lục hợp đồng

Chỉ chạy khi khách đã đồng ý phương án và chuẩn bị ký. Skill `viindoo-presales:viindoo-phu-luc-hop-dong`.

Cắt nguyên văn Mục 2, 3, 6 từ chính bản phương án khách đã đọc - không viết lại nội dung.

Ra: `Phu luc 01 - Ke hoach trien khai va Pham vi dap ung.html`.

Báo: đường dẫn, các mục đã cắt và số mục mới, kết quả soát. Nếu cần bản ký thì nhắc chạy tiếp script đóng dấu đầu trang và số trang.

## Sau cả bộ

Nhắc hai việc: lưu ghi chú dự án vào AI-Memory nếu có quyết định mới, và chỉ gửi khách sau khi Liên duyệt.
