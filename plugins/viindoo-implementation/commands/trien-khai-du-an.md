---
description: Chạy chuỗi triển khai dự án Viindoo cho một khách đã ký hợp đồng - đánh giá hiện trạng, báo cáo và kế hoạch, nhiệm vụ viindoo.com, bộ quy trình ứng dụng, việc thiết lập - có điểm dừng sau mỗi tài liệu
---

Chạy triển khai dự án cho khách nêu trong `$ARGUMENTS` (tên khách hoặc đường dẫn thư mục dự án). Quy trình gốc: skill `viindoo-implementation:viindoo-trien-khai-du-an` và trang Viin Brain "Quy trình triển khai Viindoo Express".

## Quy tắc cứng

1. **Dừng sau mỗi bước có tài liệu gửi khách**; chủ nhiệm dự án đọc, rà độc lập xong mới gửi.
2. **Không đọc lại tệp đã sinh vào ngữ cảnh** - chỉ báo đường dẫn và con số đếm. Mỗi bước báo tối đa 10 dòng.
3. **Hệ thống khách chỉ đọc**; không ghi gì vào viindoo.com.
4. Thư mục dự án `~/Documents/project/<Khách>/`, dữ liệu trong `work/`.

## Bước 0 - Kiểm đầu vào

Có phụ lục hợp đồng (phạm vi, tổng giờ, thứ tự gói) chưa; có `work/project.py`, `handbook.py`, `setup_tasks.py` chưa (chưa có thì chép khung từ `${CLAUDE_PLUGIN_ROOT}/kit/examples/sample/`). Khách mới hay đang dùng hệ thống. Thiếu phụ lục thì dừng, nói rõ thiếu gì.

## Bước 1 - Đánh giá hiện trạng

Skill `viindoo-danh-gia-hien-trang`: nhánh A (workbook) hoặc nhánh B (rà soát chỉ đọc). Báo: số phép kiểm, số điểm Cần chỉnh / Cần làm lại. Nhánh A còn điểm cần khách bổ sung thì **dừng** chờ khách.

## Bước 2 - Báo cáo hiện trạng và kế hoạch

`build_assessment_report.py`. Báo: đường dẫn PDF, tổng giờ kế hoạch so với gói đã ký, kết quả soát. **Dừng** - chủ nhiệm dự án duyệt, rà độc lập, gửi khách.

## Bước 3 - Nhiệm vụ dự án viindoo.com

Skill `viindoo-ke-hoach-du-an`. Báo: số nhiệm vụ, số buổi đào tạo, tổng giờ phân bổ, cảnh báo lịch.

## Bước 4 - Bộ quy trình ứng dụng của gói

Skill `viindoo-quy-trinh-ung-dung`: `check_handbook.py` rồi bản HTML/PDF và Word. Báo: số quy trình, bước, hình, kết quả kiểm. **Dừng** - họp thống nhất với khách, rà độc lập.

## Bước 5 - Việc thiết lập (nội bộ)

Skill `viindoo-viec-thiet-lap`. Báo: đường dẫn, số việc AI làm / người làm, quyết định cần lấy từ khách.

Lặp bước 4-5 cho từng gói. Sau cả chuỗi: nhắc đính kèm tài liệu đã gửi vào nhiệm vụ tương ứng (ghi chú nội bộ), không đính kèm tài liệu nội bộ.
