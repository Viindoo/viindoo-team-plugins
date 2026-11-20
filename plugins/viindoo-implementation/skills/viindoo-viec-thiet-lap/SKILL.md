---
name: viindoo-viec-thiet-lap
description: Dựng danh sách "Việc thiết lập và điều chỉnh" NỘI BỘ của dự án triển khai Viindoo - theo từng gói: quy trình cần thống nhất và vị trí cần có mặt, kế hoạch theo mã gửi khách, việc điều chỉnh dữ liệu và thiết lập kèm phân công AI hay tư vấn và việc phải chờ, việc thiết lập phục vụ bộ quy trình ứng dụng (ô bắt buộc, quy tắc tự động, loại phê duyệt, nhóm quyền, nhiệm vụ rà soát định kỳ), module cần cài, quyết định cần lấy từ khách, dữ liệu khách phải giao. Dùng khi người dùng nói "lên danh sách việc thiết lập cho gói 1", "những gì phải cấu hình trên hệ thống khách", "việc nào AI làm được, việc nào người làm", "chuẩn bị thiết lập sau khi thống nhất quy trình". KHÔNG dùng cho - tài liệu gửi khách (viindoo-danh-gia-hien-trang, viindoo-quy-trinh-ung-dung), nhiệm vụ trên viindoo.com (viindoo-ke-hoach-du-an).
---

# Việc thiết lập và điều chỉnh (nội bộ)

Quy tắc gốc trên Viin Brain: Project Knowledge > "Triển khai dự án Viindoo" > "Việc thiết lập và điều chỉnh (nội bộ)" - https://viindoo.com/web#id=85&model=viin.brain.page&view_type=form (xem trước: `brain/pages/tk-setup.html`).

**Nội bộ Viindoo.** Không gửi khách, không đính kèm vào dự án trên viindoo.com (khách xem dự án qua cổng thông tin).

## Dữ liệu

- `work/setup_tasks.py` (khung: `${CLAUDE_PLUGIN_ROOT}/kit/examples/sample/setup_tasks.py`): `CACH_LAM`, `PHAN_CONG` (mã việc -> ai làm, làm gì, chờ gì), `THIET_LAP` (ứng dụng -> việc thiết lập, cấu hình gì, phục vụ mục nào của bộ quy trình, mã việc, gói), `MODULES`, `VIEC_NGUOI`.
- Đọc thêm `project.py` (danh mục việc, kế hoạch, dữ liệu khách giao) và `handbook.py` (quy trình của từng gói, vị trí tham gia).

Mỗi việc dựng một lần mà bộ quy trình nhắc tới (ô bắt buộc trong chốt chặn, việc kiểm tra được giao tự động, loại phê duyệt, nhiệm vụ rà soát định kỳ) phải có một dòng ở `THIET_LAP`, ghi rõ phục vụ mục nào.

## Chạy

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/kit/scripts/build_setup_worklist.py --data ~/Documents/project/<Khách>/work
```

Ra `Triển khai/Nội bộ/<Khách> - Việc thiết lập và điều chỉnh (nội bộ).html` và `.pdf`. Dừng khi mã việc trong `setup_tasks.py` không có trong danh mục việc gửi khách, hoặc việc nào của danh mục chưa có phân công.

## Làm trên hệ thống khách

1. AI chỉ ghi khi người phụ trách đã duyệt từng lô: báo trước số bản ghi và các ô sẽ đổi; làm trên bản thử trước nếu có.
2. Xoá, huỷ, lưu trữ công ty, khoá sổ, cài module: hỏi chủ nhiệm dự án riêng.
3. Đăng nhập trong biến môi trường, tài khoản riêng của Viindoo.
