# Báo giá - cách trình bày

Số liệu lấy từ bảng giá hiện hành và từ danh mục BR đã chốt ở bước 3. **Không nhớ áng chừng, không gõ lại tay** - đọc thẳng workbook BR bằng `openpyxl` để một con số chỉ khai một nơi.

## Ba dòng dịch vụ

| Dòng | Bản chất | Cách tính |
|---|---|---|
| Thuê bao Cloud | trả định kỳ theo năm | đơn giá gói trên người dùng trên tháng |
| Gói Express | combo giờ trọn gói, **không tính ngày công** | giá gói theo số giờ |
| Dịch vụ phát triển | tùy biến, viết code | nội bộ tính theo ngày công từng cấp; **gửi khách chỉ ghi tổng tiền** |

Gói Express chỉ gồm tính năng có sẵn và cấu hình. Phần viết code tách thành dòng dịch vụ riêng - không gộp giờ tùy biến vào gói Express.

## Mục 8.1 - trả một lần

Bảng: Hạng mục | Đơn giá | Ưu đãi | Thành tiền.

- **Gói Express**: ghi giá gói, ưu đãi (nếu có), thành tiền. Một dòng, kèm ghi chú nhỏ dưới số.
- **Dịch vụ phát triển**: một dòng tổng. Danh sách từng hạng mục và giá từng hạng mục nằm ở Mục 3.
- **Nâng cấp phiên bản** (nếu có): 54.000.000 đ một phiên bản, phiên bản kế tiếp giảm 50%. Ví dụ nâng từ 17 lên 19 là 54 triệu cộng 27 triệu. Viindoo tặng thì vẫn ghi đủ giá rồi ghi ưu đãi 100% - **không ghi "không tính phí" trần**.

Ghi "Không thuộc đối tượng chịu thuế GTGT" theo mẫu.

## Ưu đãi 15% gói Express

Chỉ áp cho gói Express **đầu tiên** của khách dùng Viindoo Cloud. Khách đã từng mua gói Express trước đó thì gói sau tính đủ giá.

**Kiểm trước khi ghi ưu đãi**: tra lịch sử đơn hàng của khách. Đây là lỗi đã xảy ra thật, giảm giá nhầm cho khách cũ.

## Mục 8.2 - trả định kỳ theo năm

Chỉ ghi **đơn giá gói** trên người dùng trên tháng. Không nhân ra tổng tiền năm - số người dùng còn đổi.

## Mục "Chưa gồm"

Luôn có, và luôn có dòng: **chi phí đi lại, ăn ở của chuyên viên Viindoo khi làm việc tại trụ sở Công ty**.

Thêm những gì thực sự nằm ngoài: hạ tầng máy chủ nếu khách tự vận hành, phí bên thứ ba (hóa đơn điện tử, chữ ký số, vận chuyển), dữ liệu khách tự nhập.

## Cách triển khai theo phạm vi

Khách hỏi vì sao không làm theo cách tính theo phạm vi: chi phí cách đó thường gấp hai đến ba lần gói Express, vì phải làm rõ phạm vi, xác định trong và ngoài phạm vi, và dự phòng mở rộng. Nói thẳng con số tương đối, đừng né.

## Những chữ không được xuất hiện trong bản gửi khách

"ngày công", "Junior", "Senior", "Expert", "manday" - ở bất kỳ đâu: thẻ đầu trang, tóm tắt, tiêu đề cột, ghi chú, biểu tiến độ.

```python
con_sot = vdoc.kiem_ban_gui_khach(duong_dan_tep)
assert not con_sot, f"Còn từ cấm: {con_sot}"
```

## Lấy số từ workbook BR

```python
import openpyxl
wb = openpyxl.load_workbook(duong_dan_br, data_only=True)   # data_only: lấy giá trị đã tính
ws = wb["R - Business Requirements"]
gia = {}
for r in range(2, ws.max_row):
    ma, pl, tong = ws.cell(r, 2).value, ws.cell(r, 39).value, ws.cell(r, 38).value
    if pl == "Phát triển" and tong:
        gia[ma] = tong
```

Workbook phải được mở và lưu lại bằng Excel hoặc LibreOffice một lần thì `data_only=True` mới có giá trị - openpyxl không tự tính công thức. Chưa có giá trị thì tính lại trong Python từ chính giờ và bảng giá, đừng đoán.
