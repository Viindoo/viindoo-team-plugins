# Khối mức đáp ứng - mẫu đầy đủ

Khối này nằm cuối mỗi quy trình. Khách đọc để biết quy trình vừa xem thì phần mềm lo được tới đâu, phần nào phải làm thêm, và tin được vì mỗi dòng đều truy ngược được.

## Thứ tự trong khối

1. **Thanh tỷ lệ bốn lớp** của riêng quy trình đó - `vsodo.thanh(hang_muc)`.
2. **Phần hệ thống đã làm được** - gạch đầu dòng, mỗi dòng một yêu cầu, kèm nhãn lớp và module làm nền.
3. **Phần còn thiếu** - gạch đầu dòng, mỗi dòng ghi rõ làm bằng Trình tùy chỉnh hay phải viết code, và mở rộng trên cái gì.
4. **Truy vết** - mỗi dòng kèm mã BR và vị trí gốc trong tài liệu khách gửi.

## Dữ liệu một hạng mục

```python
{
  "br": "BR-MH-03",
  "nguon": "ô E16 · nhóm 5 Mua hàng · cột Yêu cầu chi tiết",
  "nguon_day_du": "Yeu cau nghiep vu ERP - Cong ty ABC (T10.2026).xlsx",
  "yeu_cau": "Đề nghị mua tự sinh khi tồn xuống dưới mức tối thiểu",
  "phan_co": "odoo",
  "co": "Quy tắc đặt hàng lại trong stock đã sinh đề nghị mua theo mức tối thiểu và tối đa.",
  "mod_co": ["stock", "purchase"],
  "phan_thieu": "tuy_chinh",
  "thieu": "Khách cần mức tối thiểu đổi theo mùa - khai thêm trường và một quy tắc tự động trên "
           "chính danh mục hiện có, không viết code.",
}
```

Yêu cầu đáp ứng trọn vẹn thì để `phan_thieu = None`. Yêu cầu hoàn toàn chưa có thì để `phan_co = None` và `phan_thieu` là lớp phải làm thêm.

## Cách viết từng lớp

**`odoo`** - lõi Odoo Community của đúng phiên bản đã có. Dẫn được model hoặc trường thật.

**`viindoo`** - phải có phân hệ Viindoo mới lo được. Ghi tên phân hệ, ví dụ: nền Odoo lo phần kho, phân hệ Viindoo bổ sung phần kiểm soát chất lượng theo công đoạn.

**`tuy_chinh`** - phần thiếu nằm trọn trong những việc Trình tùy chỉnh làm được: thêm trường, sửa và thêm loại màn hình, tạo loại dữ liệu mới, trình đơn, mẫu in, phân quyền, quy tắc tự động, bộ lọc. Viết rõ là **làm ngay trên hệ thống đang chạy, không viết code** - đây là điểm khách quan tâm.

**`lap_trinh`** - phần thiếu phải viết code. Xếp vào đây khi cần: trường tính theo công thức, cầu nối hệ thống ngoài, thuật toán nghiệp vụ, chặn chứng từ theo điều kiện, báo cáo nối nhiều tầng. Kể cả khi một phần hạng mục tùy chỉnh được, vẫn xếp lập trình để không hứa quá.

## Lời văn

Viết cho người làm nghề đọc, không viết cho lập trình viên:

- Được: "Hệ thống tự sinh đề nghị mua khi tồn xuống dưới mức tối thiểu; mức tối thiểu đổi theo mùa thì khai thêm một trường và một quy tắc tự động, không phải viết code."
- Tránh: "Dùng `stock.warehouse.orderpoint` với `product_min_qty` compute theo `season_id`."

Tên model chỉ xuất hiện ở phần dẫn chứng ngắn hoặc trong file BR nội bộ.

## Phần tổng quan phải có

Đặt một lần ở phần 0, trước khi vào từng quy trình:

- **Cách đọc sơ đồ** - `vsodo.chu_giai_so_do()`.
- **Cách đọc mức đáp ứng** - bốn lớp nghĩa là gì, và nguyên tắc tách phần đã có khỏi phần còn thiếu.
- **Căn cứ kết luận** - nói thẳng: đọc trực tiếp mã nguồn, không suy từ tên chức năng; nêu rõ lớp nền đọc trên mã nguồn nào, lớp bổ sung đọc trên mã nguồn nào.
- **Cách truy vết yêu cầu** - giải thích nhãn `BR-MH-03` và nhãn vị trí gốc.

## Bản đồ quy trình

Bảng ở đầu tài liệu: **Mảng | Mã | Quy trình | Mức đáp ứng** (cột cuối là thanh tỷ lệ thu nhỏ, `vsodo.thanh(hang_muc, nho=True)`). Khách đọc một trang thấy toàn cảnh rồi mới đi vào chi tiết.
