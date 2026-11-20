---
name: viindoo-trien-khai-du-an
description: Điều phối triển khai dự án Viindoo Express sau khi khách đã ký hợp đồng - từ nhận bàn giao, khởi động, đánh giá hiện trạng (khách mới thu thập bằng Excel, khách đang dùng hệ thống thì rà soát chỉ đọc), báo cáo hiện trạng và kế hoạch, bộ quy trình ứng dụng, thiết lập theo gói, đào tạo, chạy chính thức đến giám sát sau vận hành; chỉ đúng công cụ cho từng bước và giữ các cổng nghiệm thu. Dùng khi người dùng nói "bắt đầu triển khai cho khách X", "khách ký rồi, vào triển khai", "lên kế hoạch triển khai dự án", "dự án triển khai đang tới bước nào", "làm tiếp gói 2 cho khách X", "chuẩn bị chạy chính thức". KHÔNG dùng cho - việc trước khi ký hợp đồng (hồ sơ khách, phương án, báo giá, phụ lục: plugin viindoo-presales); dựng riêng một tài liệu đã biết rõ (dùng thẳng viindoo-danh-gia-hien-trang, viindoo-quy-trinh-ung-dung, viindoo-viec-thiet-lap, viindoo-ke-hoach-du-an).
---

# Triển khai dự án Viindoo Express

Quy trình và mẫu biểu gốc nằm trên Viin Brain, không chép lại ở đây:

- **Quy trình triển khai Viindoo Express** (giai đoạn, bước, ai làm gì, đầu vào, đầu ra, cổng nghiệm thu, quy tắc thời gian): Viin Brain, không gian Project Knowledge, trang "Triển khai dự án Viindoo" > "Quy trình triển khai Viindoo Express" - liên kết: https://viindoo.com/web#id=80&model=viin.brain.page&view_type=form.
- Bản xem trước trong repo: `brain/pages/tk-process.html`.

Đọc trang đó trước khi làm bước đầu tiên của một dự án. Skill này chỉ nói công cụ nào cho bước nào và cách giữ dữ liệu dự án.

## Đầu vào từ presales - bàn giao, không làm lại

Hợp đồng, Phụ lục 01 - Kế hoạch triển khai và Phạm vi đáp ứng, phương án đề xuất, danh mục yêu cầu nghiệp vụ (nội bộ), tài liệu mô hình hoạt động và quy trình mức đáp ứng - do plugin viindoo-presales làm ra trước khi ký. Phạm vi, tổng giờ, thứ tự gói trong phụ lục là cam kết: kế hoạch triển khai giữ đúng. Khách nêu hạng mục ngoài phụ lục thì báo chủ nhiệm dự án, không tự thêm.

## Thư mục dự án

```
~/Documents/project/<Khách>/
  work/                      dữ liệu dự án (mã nguồn của tài liệu)
    project.py               kế hoạch, danh mục việc, đào tạo, nhân sự
    handbook.py              bộ quy trình ứng dụng
    setup_tasks.py           việc thiết lập (nội bộ)
    current_state.json       kết quả đánh giá hiện trạng (công cụ ghi)
    groups.json              nhóm quyền đúng chữ trên hệ thống khách (công cụ ghi)
  Triển khai/                tài liệu gửi khách (công cụ ghi)
    Nội bộ/                  tài liệu nội bộ - không gửi khách, không đính kèm dự án
```

Khung dữ liệu: chép `${CLAUDE_PLUGIN_ROOT}/kit/examples/sample/*.py` vào `work/` rồi viết lại toàn bộ nội dung theo khách. Mọi công cụ nhận `--data <thư mục work>`; thư mục ra mặc định `<work>/../Triển khai`, đổi bằng `--out`.

## Bước nào, công cụ nào

| Giai đoạn | Việc | Skill |
|---|---|---|
| 0-1 Nhận bàn giao, khởi động | đọc phụ lục, tạo thư mục, chọn nhánh đánh giá | skill này |
| 2 Đánh giá hiện trạng | khách mới: gửi và kiểm workbook; khách đang dùng: rà soát chỉ đọc; dựng báo cáo hiện trạng và kế hoạch | `viindoo-danh-gia-hien-trang` |
| 2 Lập nhiệm vụ dự án | bảng nhiệm vụ [KH] cho viindoo.com, lịch đào tạo | `viindoo-ke-hoach-du-an` |
| 3 Mỗi gói | bộ quy trình ứng dụng của gói | `viindoo-quy-trinh-ung-dung` |
| 3 Mỗi gói | việc thiết lập và điều chỉnh (nội bộ) | `viindoo-viec-thiet-lap` |
| Trước mỗi lần gửi khách | rà độc lập bản in | agent `viindoo-deliverable-reviewer` (plugin viindoo-presales) hoặc người không tham gia soạn |

Chạy cả chuỗi có điểm dừng: lệnh `/viindoo-implementation:trien-khai-du-an <Khách>`.

## Luật cứng

1. **Dừng sau mỗi tài liệu gửi khách.** Soạn xong là bản nháp; chủ nhiệm dự án đọc, rà độc lập xong mới gửi.
2. **Hệ thống khách: chỉ đọc khi đánh giá.** Thiết lập, nhập liệu chỉ khi người phụ trách duyệt từng lô (số bản ghi, ô sẽ đổi). Xoá, huỷ, lưu trữ công ty, khoá sổ, cài module luôn hỏi riêng. Không ghi gì vào viindoo.com - các công cụ chỉ xuất tệp.
3. **Đăng nhập hệ thống khách đặt trong biến môi trường** (`ODOO_URL`, `ODOO_DB`, `ODOO_LOGIN`, `ODOO_PASSWORD`), không ghi vào tệp, không đưa vào tài liệu.
4. **Tài liệu nội bộ** (Nội bộ/) không gửi khách, không đính kèm vào dự án trên viindoo.com.
5. **Gói nối tiếp**: gói sau bắt đầu khi gói trước đã chạy chính thức, chỉ gối phần giám sát, hỗ trợ.
6. **Không đưa vào kế hoạch gửi khách** việc tác động người, quyền, dữ liệu nhạy cảm chưa thẩm định.
7. **Chỉ gạch ngang ASCII** `-`; tài liệu gửi khách tiếng Việt.

## Cần cài trên máy

- Plugin `viindoo-presales` (brand, logo, khung tài liệu `vdoc`). Công cụ tự tìm: `$VIINDOO_PRESALES_ROOT`, thư mục cạnh plugin này trong repo, rồi bản mới nhất trong bộ nhớ đệm plugin.
- Python 3 với `openpyxl`, `xlsxwriter`, `python-docx`, `Pillow`, `PyYAML`.
- Chrome for Testing trong `~/.cache/chrome-for-testing/` để in PDF, chụp sơ đồ (không dùng Chrome của người dùng): `npx @puppeteer/browsers install chrome@stable --path ~/.cache/chrome-for-testing`.
- Kho tài liệu Viindoo `Viindoo/documentation` clone về máy (`$VIINDOO_DOCS_REPO`, mặc định `~/git/viindoo-documentation`) để kiểm đường dẫn tài liệu ngoại tuyến.
