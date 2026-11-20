---
name: viindoo-quy-trinh-ung-dung
description: Dựng Bộ quy trình ứng dụng Viindoo (QTUD) giao khách khi triển khai dự án - tài liệu người dùng của khách đọc để vận hành hằng ngày - bản HTML, PDF A4 ngang và Word, gồm ma trận phân quyền theo vị trí (tự kiểm tuyến tính, đúng tên nhóm quyền trên hệ thống khách), quy tắc phê duyệt, kiểm soát dữ liệu (chốt chặn, rà soát định kỳ, phối hợp khi cần tạo mới), các quy trình theo gói với sơ đồ BPMN chia làn theo vị trí có bộ tự kiểm hình học, bảng bước có liên kết tài liệu hướng dẫn Viindoo đúng phiên bản (kiểm ngoại tuyến). Dùng khi người dùng nói "làm bộ quy trình ứng dụng cho khách", "soạn QTUD gói 1", "vẽ lại sơ đồ quy trình triển khai", "cập nhật ma trận phân quyền", "xuất QTUD ra Word". KHÔNG dùng cho - quy trình mục tiêu và mức đáp ứng trước khi ký (viindoo-presales), việc thiết lập trên hệ thống (viindoo-viec-thiet-lap), sinh tệp .bpmn chuẩn OMG (spec-to-bpmn).
---

# Bộ quy trình ứng dụng Viindoo (QTUD)

Chuẩn nội dung gốc trên Viin Brain: không gian Project Knowledge > "Triển khai dự án Viindoo" > "Bộ quy trình ứng dụng (QTUD) - chuẩn" - https://viindoo.com/web#id=84&model=viin.brain.page&view_type=form (xem trước: `brain/pages/tk-qtud.html`). Đọc trước khi soạn; tóm tắt điểm hay sai:

- Để người dùng hiểu vận hành **hằng ngày**; việc thiết lập ban đầu không ghi ở đây (sang `setup_tasks.py`).
- Thứ tự: 1 Ma trận phân quyền, 2 Quy tắc phê duyệt, 3 Kiểm soát dữ liệu, 4+ quy trình theo gói.
- Chỉ vị trí công việc, không tên người; không cột xác nhận của khách.

## Dữ liệu

`work/handbook.py` của dự án; khung chạy được: `${CLAUDE_PLUGIN_ROOT}/kit/examples/sample/handbook.py`. Lược đồ: `references/luoc-do-handbook.md`.
`work/groups.json`: nhóm quyền đúng chữ trên hệ thống khách - khách đang dùng hệ thống lấy bằng `scan_live_system.py`; khách mới lấy từ hệ thống đã cấp cho khách (`scan_live_system.py --groups-only`) sau khi bật tiếng Việt và cài các ứng dụng của gói.

## Chạy

```bash
K=${CLAUDE_PLUGIN_ROOT}/kit/scripts
D=~/Documents/project/<Khách>/work
python3 $K/check_handbook.py --data $D          # kiểm, không sinh tệp; mã thoát 1 khi lỗi
python3 $K/build_handbook_html.py --data $D     # HTML + PDF
python3 $K/build_handbook_word.py --data $D     # Word (khuôn kit/assets/handbook-template.docx)
```

Cả hai bộ dựng chạy lại toàn bộ phép kiểm và dừng khi lỗi:

| Kiểm | Lỗi nghĩa là |
|---|---|
| Ma trận phân quyền | ô không đúng tên nhóm trên hệ thống; cấp trên thấp hơn cấp dưới ở một mục (ngoài `NGOAI_LE_KE_THUA`); vị trí thiếu cấp trên |
| Phối hợp khi cần tạo mới | người nhận yêu cầu không có quyền tạo mục đó theo ma trận |
| Tài liệu hướng dẫn | đường dẫn không có trên nhánh phiên bản của kho tài liệu (kiểm bằng `git ls-tree`, không gọi viindoo.com) |
| Đồ thị sơ đồ | bước thiếu hoặc lặp trên sơ đồ, nút không tới được từ sự kiện bắt đầu, ngõ cụt, cổng rẽ / cổng gộp sai số cạnh vào ra, ô gọi quy trình con không trỏ tới quy trình có thật |
| Hình học sơ đồ | đường xuyên ô, chồng nhau, đi chung hàng, cắt sát mũi tên, nhãn đè chữ, ra ngoài bể, chữ in dưới 7pt, hình quá trang |

Bản HTML tự nén bảng bước khi đuôi bảng tràn sang trang gần trống; từ "AI", "Odoo" trong bản gửi khách làm dừng dựng.

## Sơ đồ - cách khai luồng

- Việc độc lập (không nối tiếp nhau trong thực tế) tách thành luồng riêng của cùng quy trình, không nối chuỗi.
- Lựa chọn dùng cổng rẽ `gw`, gộp dùng cổng `join` riêng; sau mỗi bước duyệt có nhánh từ chối.
- Việc theo lịch dùng `timer`; gọi quy trình con dùng `call` (chữ "PD - ...", "DT - ...").
- Một người nhận hai vai trong cùng quy trình thì dùng một làn, đúng tên vị trí có thật.

## Trước khi gửi

Rà độc lập từng trang PDF và Word (agent `viindoo-deliverable-reviewer` của viindoo-presales, hoặc người không tham gia soạn), lặp tới khi hết Blocker, Major. Danh mục rà: trang Brain "Rà soát độc lập trước khi gửi khách".
