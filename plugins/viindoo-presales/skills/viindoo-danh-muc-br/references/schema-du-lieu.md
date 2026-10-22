# Schema một dòng BR

Mỗi phần tử của `D.R` là một dict. Trường nào không có thì bỏ, đừng để chuỗi rỗng.

| Trường | Cột | Bắt buộc | Nội dung |
|---|---|---|---|
| `id` | B | có | mã yêu cầu: `BR-MH-01` (theo mảng) hoặc `BR-001` (phẳng). Giữ một kiểu trong cả dự án |
| `ten` | C | có | mô tả yêu cầu - một câu ngắn, đọc là hiểu |
| `ct` | D | có | mô tả chi tiết - **nguyên văn ý khách**, không diễn rộng |
| `dep` | E | | phụ thuộc: mã BR khác |
| `nv` | F | có | phân loại theo nghiệp vụ - lấy đúng giá trị trong sheet `Phân loại Nghiệp vụ` |
| `nhom` | G | có | phân loại theo Nhóm - cột Phân loại của cùng sheet đó |
| `pbd` | H | có | phòng ban đề xuất - lấy từ sheet `Phòng ban` |
| `pbs` | I | có | phòng ban sử dụng |
| `pl` | AM | có | `Tiêu chuẩn` / `Cấu hình` / `Tích hợp` / `Tùy chỉnh` / `Phát triển` / `Cần làm rõ` / `Loại bỏ` |
| `gp` | AN | có | giải pháp: phạm vi + cách đáp ứng + cơ sở mã nguồn |
| `note` | D | | ghi chú, nối vào cuối mô tả chi tiết |
| `gio` | J..AJ | | giờ công theo giai đoạn, chỉ cho hạng mục phải làm thêm |

## Phân loại - chọn đúng giá trị

| Giá trị | Khi nào | Có giờ phát triển? |
|---|---|---|
| `Tiêu chuẩn` | dùng được ngay, không phải khai gì đặc biệt | không |
| `Cấu hình` | dùng được sau khi khai báo, bật tính năng, khai danh mục | không |
| `Tích hợp` | nối với hệ thống ngoài bằng cầu nối đã có | tùy |
| `Tùy chỉnh` | làm bằng Trình tùy chỉnh trên hệ thống đang chạy, không viết code | có, ít |
| `Phát triển` | phải viết code | có |
| `Cần làm rõ` | chưa đủ cơ sở để kết luận | **không** - không gán giờ bừa |
| `Loại bỏ` | đã bàn và thống nhất không làm | không |

## Cột Giải pháp viết thế nào

Ba phần, theo thứ tự:

1. **Phạm vi** - `Phạm vi: gói Viindoo Express 400 giờ.` hoặc `Cần làm rõ trước khi đưa vào phạm vi.` hoặc `Phạm vi: triển khai khi có nhu cầu.`
2. **Cách đáp ứng** - viết cho người đọc nghiệp vụ hiểu.
3. **Cơ sở mã nguồn** - model, trường, phương thức hoặc module thật đã đọc được. Hạng mục phải làm thêm thì ghi rõ **mở rộng trên cụm module nào**, không dựng đối tượng song song với cái chuẩn đã có.

Ví dụ:

> Phạm vi: gói Viindoo Express 400 giờ. Hệ thống sinh đề nghị mua khi tồn xuống dưới mức tối thiểu, cấu hình trên quy tắc đặt hàng lại sẵn có (`stock.warehouse.orderpoint`). Mức tối thiểu đổi theo mùa: thêm một trường và một quy tắc tự động bằng Trình tùy chỉnh trên chính danh mục đó, không viết code.

## Giờ công

```python
"gio": vbr.ap_he_so_ai({
    "tk": (3, "Expert"),      # Phân tích & Thiết kế - giữ nguyên, không nhân hệ số
    "lt": (10, "Senior"),     # Lập trình - x0.4
    "qa": (4, "Junior"),      # QA - x0.5
    "tl": (2, "Junior"),      # Tài liệu, video - x0.3
    "ch": (2, "Senior"),      # Cấu hình & Triển khai
    "dt": (2, "Senior"),      # Đào tạo, nghiệm thu với khách - giữ nguyên
})
```

Khóa hợp lệ: `ks` khảo sát, `tk` phân tích thiết kế, `lt` lập trình, `qa` kiểm thử, `dt` đào tạo và nghiệm thu, `ch` cấu hình triển khai, `tl` tài liệu và video, `gs` giám sát hậu triển khai. **Bảo hành tự tính** bằng 15% giờ lập trình, không khai tay.

`ap_he_so_ai` nhân hệ số cho `lt`, `qa`, `tl`; các giai đoạn khác giữ nguyên. Gọi **đúng một lần** trên giờ gốc - gọi hai lần là giảm giá hai lần.

### Chọn cấp bậc

Theo mức chạm vào lõi, không theo số giờ:

- **Phức tạp** (ghi đè phương thức lõi: luồng kho, sản xuất, kế toán) - cơ cấu Junior/Senior/Expert khoảng 40/40/20, cộng thêm đệm kiểm thử khoảng 20%.
- **Tiêu chuẩn** - khoảng 55/35/10.
- **Đơn giản** - khoảng 65/30/5.

Đơn giá từng cấp nằm ở sheet `Bảng giá theo manday` trong chính workbook; chi phí tính bằng tổng của từng cấp nhân đơn giá cấp đó, không dùng đơn giá bình quân.

## Các biến khác trong data.py

```python
KHACH = "Công ty cổ phần ABC"
TO_CHUC = ["Công ty cổ phần ABC", "Chi nhánh Hà Nội - Công ty cổ phần ABC"]
GHI_CHU = "Phương án dùng gói Viindoo Express 400 giờ, phần phát triển thêm 3 hạng mục."
XAC_NHAN = [ ... ]   # dùng chung với tài liệu bước 2
R = [ ... ]
```

Muốn sắp xếp dòng theo gói hoặc theo mảng thì truyền `sap_xep=lambda x: (...)` vào `vbr.dung()`.
