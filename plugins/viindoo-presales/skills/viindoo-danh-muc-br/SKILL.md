---
name: viindoo-danh-muc-br
description: Dựng Danh mục Yêu cầu Nghiệp vụ Phần mềm (BRL, file Excel theo mẫu chuẩn Viindoo) - bước 3 trong bộ bốn tài liệu presales Viindoo. Mỗi yêu cầu của khách thành một dòng có mã BR, phân loại nghiệp vụ, phòng ban đề xuất và sử dụng, phân loại đáp ứng (Tiêu chuẩn / Cấu hình / Tích hợp / Tùy chỉnh / Phát triển / Cần làm rõ), giải pháp kèm cơ sở mã nguồn, và giờ công chín giai đoạn theo cấp Junior/Senior/Expert để ra giá vốn. Đây là tài liệu NỘI BỘ, không gửi khách. Dùng khi người dùng nói "làm BR cho khách này", "lập danh mục yêu cầu nghiệp vụ", "dựng file Excel BR như các dự án khác", "bóc giờ các hạng mục phát triển", "làm bảng fit-gap để tính giá vốn". KHÔNG dùng cho - tài liệu gửi khách (→ viindoo-phuong-an-de-xuat), mô tả doanh nghiệp (→ viindoo-mo-hinh-hoat-dong), vẽ quy trình (→ viindoo-quy-trinh-dap-ung).
---

# Bước 3 - Danh mục Yêu cầu Nghiệp vụ (BRL)

File Excel theo cấu trúc chuẩn Viindoo (bản Quang Thắng 20/10/2026 dùng đúng cấu trúc này). Mỗi yêu cầu một dòng, bóc giờ từng cấp bậc để biết **giá vốn** trước khi ra giá bán.

**Đây là tài liệu nội bộ.** Giữ nguyên cột giờ, cấp bậc và sheet bảng giá; không ẩn, không gửi khách, không đề xuất sửa cho khách. Bản gửi khách là phương án HTML ở bước 4, ở đó phần phát triển chỉ ghi tổng tiền.

## Dùng ở đâu trong quy trình presales

| Mốc | Việc | Tài liệu |
|---|---|---|
| Nhận lead, có hồ sơ khách | hiểu doanh nghiệp | bước 1 mô hình hoạt động |
| Sau khảo sát, có danh sách yêu cầu | chốt hiểu đúng, chấm đáp ứng | bước 2 quy trình và mức đáp ứng |
| **Nội bộ, trước khi ra giá** | **bóc giờ từng cấp, biết giá vốn** | **bước 3 - tài liệu này** |
| Chào giá, trình bày với khách | chốt phạm vi và tiền | bước 4 phương án đề xuất |
| Khách đồng ý, chuẩn bị ký | đính kèm hợp đồng | bước 5 phụ lục hợp đồng |
| Sau ký, vào triển khai | thống nhất thao tác từng vị trí | QTUD (ngoài bộ này) |

Làm sau khi tài liệu bước 2 đã chốt với khách. Đây là tài liệu nội bộ, không gửi khách.

## Khi nào dùng

- "Làm BR cho khách X", "danh mục yêu cầu nghiệp vụ"
- "Dựng file Excel BR như các dự án khác"
- "Bóc giờ hạng mục phát triển để xem giá vốn"
- Đã có bước 2 (hoặc ít nhất đã có danh sách yêu cầu đã đối chiếu mã nguồn)

## Cấu trúc file - giữ đúng mẫu

Mẫu sạch nằm sẵn trong plugin: `kit/mau/danh-muc-br.xlsx` - đã khử dữ liệu khách, giữ nguyên công thức, bảng, dropdown, bảng giá, danh mục phòng ban và phân loại nghiệp vụ, kèm chú thích hướng dẫn điền ngay trong ô.

| Sheet | Vai trò | Hiển thị |
|---|---|---|
| `Dashboard (Chart)` | 10 biểu đồ số lượng và chi phí | hiện |
| `R - Business Requirements` | bảng chính 40 cột A-AN, có dòng Tổng | hiện |
| `Phân loại Nghiệp vụ` | danh mục nghiệp vụ và nhóm chuẩn | hiện |
| `Bảng giá theo manday` | Junior / Senior / Expert | hiện |
| `Dashboard` | số liệu nuôi biểu đồ | ẩn |
| `Phòng ban`, `Tổ chức  Công ty` | danh mục | ẩn |
| `Điểm cần xác nhận` | khi có điểm cần khách chốt | hiện |

**Không thêm cột ngoài AN, không thêm sheet** kiểu Tổng hợp / Gói triển khai / Cần làm rõ / Đề xuất. Phạm vi gói ghi ở đầu cột Giải pháp. Các mở rộng khác chỉ làm khi Liên yêu cầu riêng.

### Chín giai đoạn giờ công

Khảo sát · Phân tích & Thiết kế · Lập trình & Phát triển · QA & Kiểm thử thủ công · Đào tạo và Kiểm thử chấp thuận · Cấu hình & Triển khai · Bảo hành · Tài liệu / video hướng dẫn · Giám sát hậu triển khai.

Mỗi giai đoạn ba cột: giờ, cấp bậc, chi phí (chi phí có công thức sẵn). Bảo hành tự tính bằng 15% giờ lập trình.

## Cách dựng

Dữ liệu tách sang `data.py`, builder gọi kit:

```python
import sys, os, glob
KIT = os.environ.get("CLAUDE_PLUGIN_ROOT") or sorted(
    glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/viindoo-presales/*")))[-1]
sys.path.insert(0, os.path.join(KIT, "kit", "lib"))
import vbr
import data as D

vbr.dung(D.R, os.path.expanduser(f"~/Documents/project/{D.KHACH}/Danh mục Yêu cầu Nghiệp vụ Phần mềm - {D.KHACH}.xlsx"),
         khach=D.KHACH, to_chuc=D.TO_CHUC, diem_xac_nhan=D.XAC_NHAN,
         ghi_chu_chi_phi=D.GHI_CHU)
```

Mỗi dòng trong `D.R`:

```python
{"id": "BR-MH-01",
 "ten": "Đề nghị mua hàng theo định mức tồn",
 "ct": "Nguyên văn ý khách, không diễn rộng.",
 "dep": "BR-KV-02",
 "nv": "Mua hàng",                      # lấy từ sheet Phân loại Nghiệp vụ
 "nhom": "Chuỗi cung ứng",
 "pbd": "Kho vận", "pbs": "Mua hàng",   # lấy từ sheet Phòng ban
 "pl": "Tiêu chuẩn",
 "gp": "Phạm vi: gói Viindoo Express. purchase.requisition sẵn có, cấu hình ngưỡng tồn.",
 "gio": {"tk": (3, "Expert"), "lt": (4, "Senior"), "qa": (2, "Junior")}}   # giờ đã chốt
```

Xem `references/schema-du-lieu.md` cho đủ trường và `references/vi-du-data.py` cho một tệp dữ liệu chạy được.

## Luật bắt buộc

1. **Chỉ những gì khách nêu.** Không tự thêm, không diễn rộng yêu cầu của khách thành yêu cầu cụ thể hơn. Tính năng **có sẵn** (Tiêu chuẩn, Cấu hình) được chủ động đưa vào cho trọn giải pháp, ghi nguồn "nghiệp vụ chuẩn". Hạng mục **phải phát triển** mà khách chưa nêu thì liệt kê ra chat hỏi Liên trước, không đưa vào tệp.
2. **Phân loại phải đọc từ mã nguồn.** Dùng MCP `odoo-semantic` trên profile đúng phiên bản, hoặc agent `viindoo-source-explorer`. Cột Giải pháp ghi được model, trường, phương thức hoặc module làm cơ sở.
3. **Yêu cầu chưa rõ thì để `Cần làm rõ`, không gán giờ bừa.** Tổng giờ chỉ gồm hạng mục đã định giá chắc.
4. **Tận dụng module sẵn có trước.** Hạng mục phải làm thêm phải ghi rõ mở rộng trên cụm module nào, chỉ ước giờ cho phần chênh.
5. **Quy tắc tính giờ và giá: hỏi Liên hoặc tra quy tắc hiện hành tại thời điểm làm.** Plugin không giữ công thức giá, không giữ hệ số, không giữ đơn giá - những thứ này đổi theo thời điểm và theo từng khách. Đừng mang hệ số của một dự án cũ sang dự án mới. Workbook chỉ nhận **số giờ đã chốt**.
6. **Cơ cấu cấp bậc theo mức chạm vào lõi**, không theo số giờ: hạng mục ghi đè phương thức lõi (luồng kho, sản xuất, kế toán) nặng hơn hạng mục thường. Tỷ lệ cụ thể hỏi Liên.
7. **Mã BR** đặt theo mảng cho dễ đọc (`BR-MH-01` mua hàng, `BR-SX-01` sản xuất) hoặc đánh số phẳng `BR-001` khi dự án nhỏ. Giữ một kiểu trong cả dự án; mã đã gửi khách thì không đổi.
8. **Tái dùng khuôn, viết lại nội dung.** Cấu trúc sheet, cột, công thức giữ nguyên; mọi dòng nội dung viết lại 100% theo khách mới sau khi đọc lại tài liệu nghiệp vụ của họ.
9. **Chỉ dùng dấu gạch ngang ASCII** `-`.

## Sheet "Điểm cần xác nhận"

Chỉ đưa vào câu mà **câu trả lời làm đổi giải pháp, phạm vi gói hay chi phí**. Mọi cách khách chọn đều làm được bằng tính năng có sẵn, hoặc đằng nào cũng phải phát triển cùng một hạng mục, thì chọn phương án mặc định hợp lý, ghi vào cột Giải pháp và bỏ câu hỏi đi. Dữ liệu chỉ cần lúc triển khai (công thức đầy đủ, danh sách người dùng chi tiết) cũng không hỏi ở giai đoạn này.

Mỗi điểm viết theo khuôn: Viindoo **nêu cách hiểu và đề xuất** của mình kèm căn cứ, khách chỉ tích chọn. Dùng chung dữ liệu với mục xác nhận trong tài liệu HTML bước 2 - khai báo một lần, hai nơi cùng dùng.

Điểm nào còn treo ở bước này thì sang bước 4 nó thành một dòng trong khối **Cần làm rõ ở giai đoạn Khảo sát** của phương án.

## Kiểm trước khi dùng tiếp

- Mở file, xem dòng Tổng và 10 biểu đồ có số.
- Soát: hạng mục `Phát triển` nào cũng có giờ; hạng mục `Tiêu chuẩn`, `Cấu hình` thì không có giờ phát triển.
- Soát cột Giải pháp: dòng nào cũng có cơ sở mã nguồn hoặc lý do rõ.
