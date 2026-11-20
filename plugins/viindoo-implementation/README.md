# viindoo-implementation (Viindoo Implementation)

Triển khai dự án Viindoo sau khi khách ký hợp đồng. Xem README ở gốc repo: cài đặt, chuẩn bị trên máy.

- **Quy trình và mẫu biểu gốc: Viin Brain**, không gian Project Knowledge, trang "Triển khai dự án Viindoo". Plugin chỉ giữ công cụ chạy được; mỗi skill trỏ về trang Brain của bước đó. Bản xem trước các trang: `brain/pages/` ở gốc repo.
- **Đầu vào từ presales** (plugin `viindoo-presales`): phụ lục hợp đồng, phương án, danh mục yêu cầu - bàn giao, không làm lại.

| Skill | Dùng khi | Ra |
|---|---|---|
| `viindoo-trien-khai-du-an` | bắt đầu, điều phối dự án triển khai | đúng công cụ cho từng bước |
| `viindoo-danh-gia-hien-trang` | đánh giá hiện trạng: khách mới (workbook Excel) hoặc khách đang dùng hệ thống (rà soát chỉ đọc) | Báo cáo đánh giá hiện trạng và kế hoạch triển khai (HTML, PDF) |
| `viindoo-quy-trinh-ung-dung` | bộ quy trình ứng dụng của từng gói | QTUD HTML, PDF, Word |
| `viindoo-viec-thiet-lap` | chuẩn bị thiết lập trên hệ thống | Việc thiết lập và điều chỉnh (nội bộ) |
| `viindoo-ke-hoach-du-an` | dựng dự án trên viindoo.com | CSV nhiệm vụ [KH], lịch đào tạo |

Lệnh: `/viindoo-implementation:trien-khai-du-an <Khách>`.

## Bố cục

- `kit/scripts/` - công cụ (Python). `common.py` tìm thư mục dữ liệu dự án (`--data`), thư mục ra (`--out`), plugin viindoo-presales (brand, `vdoc`).
- `kit/examples/sample/` - dữ liệu ví dụ của một khách giả định, chạy được cả chuỗi; chép làm khung cho khách mới.
- `kit/templates/` - workbook thu thập dữ liệu (mẫu trắng). `kit/assets/` - CSS báo cáo, khuôn Word, phông Roboto (đo bề rộng chữ cho bộ kiểm hình sơ đồ).

## Chạy thử trên dữ liệu ví dụ

```bash
K=plugins/viindoo-implementation/kit
mkdir -p /tmp/vd && cp -r $K/examples/sample /tmp/vd/work
python3 $K/scripts/build_intake_workbook.py --data /tmp/vd/work --sample
python3 $K/scripts/read_intake_workbook.py --data /tmp/vd/work --workbook "/tmp/vd/Triển khai/Công ty Mẫu - Thu thập dữ liệu triển khai.xlsx"
python3 $K/scripts/build_assessment_report.py --data /tmp/vd/work
python3 $K/scripts/export_project_tasks.py --data /tmp/vd/work
python3 $K/scripts/check_handbook.py --data /tmp/vd/work
python3 $K/scripts/build_handbook_html.py --data /tmp/vd/work
python3 $K/scripts/build_handbook_word.py --data /tmp/vd/work
python3 $K/scripts/build_setup_worklist.py --data /tmp/vd/work
```

Không đưa dữ liệu khách thật, đăng nhập hay đường dẫn máy cá nhân vào plugin.
