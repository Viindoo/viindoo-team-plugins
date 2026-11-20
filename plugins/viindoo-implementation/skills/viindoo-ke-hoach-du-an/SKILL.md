---
name: viindoo-ke-hoach-du-an
description: Xuất kế hoạch triển khai dự án Viindoo thành bảng nhiệm vụ để dựng dự án trên viindoo.com - nhiệm vụ "[KH] <mã kế hoạch> <việc>" trùng mã kế hoạch gửi khách, gói là nhiệm vụ cha, giờ phân bổ bằng giờ kế hoạch, mô tả gồm việc và kết quả, ngày theo tuần kế hoạch - kèm lịch đào tạo tự xếp (tối đa 3 buổi mỗi tuần, mỗi buổi 2-3 giờ, học xong một mảng mới sang mảng sau theo dòng chảy chứng từ). Ra tệp CSV nhập được bằng chức năng Nhập của Odoo; không ghi vào hệ thống nào. Dùng khi người dùng nói "tạo nhiệm vụ dự án trên viindoo.com", "chia nhiệm vụ theo kế hoạch", "xếp lịch đào tạo cho khách", "giờ phân bổ từng nhiệm vụ". KHÔNG dùng cho - lập kế hoạch gửi khách (viindoo-danh-gia-hien-trang), chấm công hay ghi trực tiếp lên viindoo.com.
---

# Kế hoạch dự án trên viindoo.com

Quy ước gốc trên Viin Brain: Project Knowledge > "Triển khai dự án Viindoo" > "Dự án trên viindoo.com: nhiệm vụ, đào tạo, chấm công" - https://viindoo.com/web#id=86&model=viin.brain.page&view_type=form (xem trước: `brain/pages/tk-project.html`).

## Chạy

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/kit/scripts/export_project_tasks.py --data ~/Documents/project/<Khách>/work [--start-field <trường>] [--end-field <trường>]
```

Đọc `project.py`: `PLAN` (mỗi `phase` thành nhiệm vụ cha, mỗi `item` một nhiệm vụ), `TASK_GROUPS` (danh sách việc trong mô tả), `TRAINING`, `TRAINING_RULE`, `WEEK1`, `PROJECT_NAME`. Ra trong `Triển khai/Nội bộ/`:

- `<Khách> - Nhiệm vụ dự án (nhập viindoo.com).csv`: cột `id`, `name`, `project_id`, `parent_id/id`, `allocated_hours`, `planned_date_start`, `planned_date_end`, `date_deadline`, `description`. Mở danh sách nhiệm vụ của dự án > Nhập > chọn tệp; `id` và `parent_id/id` giúp Odoo tạo cha trước, gắn con sau; nhập lại cùng tệp thì cập nhật, không tạo trùng.
- `<Khách> - Lịch nhiệm vụ và buổi đào tạo.csv`: bắt đầu, hạn, giờ từng nhiệm vụ và buổi đào tạo - để xem, không để nhập.

## Quy tắc công cụ áp

- Giờ chỉ đặt ở nhiệm vụ nhận chấm công: nhiệm vụ cha (gói) 0 giờ; nhiệm vụ đào tạo của gói 0 giờ, giờ nằm ở từng buổi con. Tổng giờ phân bổ = tổng giờ kế hoạch; công cụ dừng nếu lệch, cảnh báo nếu vượt `SIGNED_HOURS`.
- Bắt đầu (`planned_date_start`) = thứ Hai tuần đầu; kết thúc (`planned_date_end`) và hạn (`date_deadline`) = thứ Sáu tuần cuối; buổi đào tạo lấy đúng ngày học. Tên trường mặc định theo nhiệm vụ của viindoo.com; cơ sở dữ liệu khác thì đổi bằng `--start-field`, `--end-field` (chuỗi rỗng để bỏ cột).
- Buổi đào tạo xếp vào các ngày trong `TRAINING_RULE.weekdays` kể từ tuần đầu của nhiệm vụ đào tạo, liên tiếp theo thứ tự `TRAINING`; cảnh báo khi buổi rơi sau tuần cuối của nhiệm vụ hoặc một mảng ngắn hơn một buổi tối thiểu. Công cụ không biết lịch nghỉ lễ - soát lại ngày trước khi nhập.

## Khi vận hành dự án

- Tài liệu hoàn thành đính kèm vào nhiệm vụ tương ứng dưới dạng ghi chú nội bộ; tài liệu nội bộ không đính kèm.
- Chấm công theo từng nhiệm vụ.
- Lỗi, hỗ trợ ngoài kế hoạch ghi vào dự án Customer Support (không tính vào gói).
- Ngày kết thúc dự án gồm cả thời gian hỗ trợ sau chạy chính thức.
