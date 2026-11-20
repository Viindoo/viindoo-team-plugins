---
name: viindoo-danh-gia-hien-trang
description: Đánh giá hiện trạng khi triển khai dự án Viindoo và dựng "Báo cáo đánh giá hiện trạng và kế hoạch triển khai" gửi khách. Hai nhánh - khách mới chưa có hệ thống thì gửi workbook Excel thu thập dữ liệu (tổ chức, phòng ban, vị trí, nhân sự, quản lý trực tiếp, phê duyệt, đối tác, sản phẩm, tài khoản ngân hàng, số dư đầu kỳ, tài sản cố định, kho, tồn kho, chứng từ dở dang) rồi kiểm tự động; khách đang dùng Viindoo/Odoo thì rà soát hệ thống đang chạy, chỉ đọc. Cả hai ra cùng một bộ phép kiểm, danh mục việc thiết lập và kế hoạch theo gói. Dùng khi người dùng nói "gửi file thu thập dữ liệu cho khách mới", "kiểm file khách điền", "rà soát hệ thống khách đang dùng", "đánh giá dữ liệu hiện trạng", "làm báo cáo hiện trạng và kế hoạch triển khai", "khách gửi lại file dữ liệu rồi". KHÔNG dùng cho - phân tích mô hình hoạt động trước khi ký (viindoo-presales), bộ quy trình ứng dụng (viindoo-quy-trinh-ung-dung), nhiệm vụ dự án viindoo.com (viindoo-ke-hoach-du-an).
---

# Đánh giá hiện trạng và kế hoạch triển khai

Quy tắc và cách dùng gốc trên Viin Brain (không gian Project Knowledge, trang "Triển khai dự án Viindoo"):

- "Đánh giá hiện trạng - khách mới: thu thập dữ liệu bằng Excel" - https://viindoo.com/web#id=81&model=viin.brain.page&view_type=form (xem trước: `brain/pages/tk-intake.html`)
- "Đánh giá hiện trạng - khách đang dùng hệ thống: rà soát chỉ đọc" - https://viindoo.com/web#id=82&model=viin.brain.page&view_type=form (`brain/pages/tk-scan.html`)
- "Báo cáo đánh giá hiện trạng và kế hoạch triển khai" - https://viindoo.com/web#id=83&model=viin.brain.page&view_type=form (`brain/pages/tk-report.html`)

Danh mục phép kiểm, sheet của workbook và việc thiết lập chuẩn khai một lần ở `${CLAUDE_PLUGIN_ROOT}/kit/scripts/checks.py`; workbook, công cụ kiểm, báo cáo và trang Brain cùng đọc từ đó.

## Nhánh A - khách mới

```bash
K=${CLAUDE_PLUGIN_ROOT}/kit/scripts
python3 $K/build_intake_workbook.py --data ~/Documents/project/<Khách>/work          # workbook có tên khách, ngày chốt (project.py)
# khách điền, gửi lại
python3 $K/read_intake_workbook.py --data ~/Documents/project/<Khách>/work --workbook "<tệp khách điền>.xlsx"
```

Ra `work/current_state.json` và `Triển khai/Nội bộ/Kết quả kiểm dữ liệu thu thập.md`. Tóm tắt cho khách những điểm Cần chỉnh, Cần làm lại (không gửi tệp nội bộ); khách sửa, kiểm lại tới khi đạt. Mẫu trắng: `--blank <tệp.xlsx>` (bản trong plugin: `kit/templates/`).

## Nhánh B - khách đang dùng hệ thống

```bash
export ODOO_URL=https://<hệ thống khách> ODOO_DB=<cơ sở dữ liệu> ODOO_LOGIN=<tài khoản riêng của Viindoo>
read -s ODOO_PASSWORD && export ODOO_PASSWORD
python3 $K/scan_live_system.py --data ~/Documents/project/<Khách>/work
```

- Chỉ đọc: `odoo_readonly.Client` chặn mọi phương thức không phải đọc ngay tại máy.
- Ra `current_state.json`, `groups.json` (nhóm quyền đúng chữ giao diện, cho ma trận phân quyền của bộ quy trình), `Triển khai/Nội bộ/Kết quả rà soát hệ thống.md`.
- Phép kiểm không đọc được (chưa cài ứng dụng, khác phiên bản) ghi "Chưa đọc được", lượt rà vẫn chạy hết.
- Rà lại sau khi nâng cấp phiên bản, trước ngày chốt số dư.

## Báo cáo gửi khách

Viết `work/project.py` (khung: `kit/examples/sample/project.py`): kết luận, danh mục việc (`TASK_GROUPS`, mỗi việc trỏ mã việc chuẩn trong `checks.TASKS` để lấy sẵn mô tả, phần khách làm, phần Viindoo làm; giờ tư vấn đặt), kế hoạch (`PLAN`, giờ nhóm việc ghi `"group:<mã>"`, giờ đào tạo `"training:<gói>"` để không gõ hai nơi), đào tạo, dữ liệu khách cần gửi, nhân sự.

```bash
python3 $K/build_assessment_report.py --data ~/Documents/project/<Khách>/work
```

- Ra `Triển khai/<Khách> - Báo cáo đánh giá hiện trạng và kế hoạch triển khai.html` và `.pdf`.
- Đánh giá theo mảng tự tính từ phép kiểm; ghi đè nhận xét bằng `AREA_NOTES`. Cột Hiện trạng của danh mục việc tự lấy từ phép kiểm gắn với việc; ghi đè bằng `current`.
- Có `handbook.py` thì danh sách quy trình lấy từ đó.
- Tự soát: gạch ngang ASCII, từ chỉ cách tính giá nội bộ (dừng nếu có). Báo tổng giờ kế hoạch so với `SIGNED_HOURS`; vượt gói thì chủ nhiệm dự án quyết với khách trước khi gửi. Giờ kế hoạch là giờ đếm vào gói Express, không quy ra tiền theo đơn giá cấp chuyên viên; hạng mục tùy biến, trọn gói tính theo ngày công thì chi phí theo bảng đơn giá cấp của danh mục yêu cầu (presales).

## Luật

1. Phạm vi, tổng giờ, thứ tự gói giữ đúng phụ lục hợp đồng đã ký.
2. Số liệu lấy từ hệ thống khách chỉ có trong báo cáo này và ghi rõ ngày đọc.
3. Phân biệt chuẩn hoá quy trình với chuẩn hoá dữ liệu.
4. Không đưa vào kế hoạch việc tác động người, quyền, dữ liệu nhạy cảm chưa thẩm định.
5. Rà độc lập bản PDF trước khi gửi.
