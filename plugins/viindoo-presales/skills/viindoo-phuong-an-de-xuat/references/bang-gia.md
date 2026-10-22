# Báo giá - cách trình bày

> **Plugin này không giữ công thức giá và không giữ đơn giá.** Quy tắc tính giá thay đổi theo thời điểm và theo từng khách; hỏi Liên hoặc đọc bảng giá hiện hành trước mỗi lần báo giá. Dưới đây chỉ là **cách trình bày** - phần ổn định giữa các dự án.
>
> Số giờ và giá của từng hạng mục lấy từ danh mục BR đã chốt ở bước 3, đọc thẳng bằng `openpyxl`, không gõ lại tay.

## Ba dòng dịch vụ - tách bạch

| Dòng | Bản chất | Trong tài liệu gửi khách |
|---|---|---|
| Thuê bao Cloud | trả định kỳ theo năm | chỉ ghi đơn giá gói trên người dùng trên tháng hoặc năm, **không nhân ra tổng** |
| Gói Express | combo giờ trọn gói, không tính ngày công | giá gói, ưu đãi (nếu đủ điều kiện), thành tiền |
| Dịch vụ phát triển | tùy biến, viết code | **chỉ tổng tiền và giá từng hạng mục**, không giờ, không đơn giá theo cấp |

Gói Express chỉ gồm tính năng có sẵn và cấu hình. Phần viết code là dòng dịch vụ riêng - không gộp giờ tùy biến vào gói Express.

## Bố cục mục Báo giá (theo mẫu Quang Thắng)

**Thẻ tổng nổi bật** trước bảng: tổng dịch vụ trả một lần, kèm một dòng phụ nói gồm những gì (mấy gói Express, bao nhiêu giờ, mấy hạng mục phát triển).

**7.1 Dịch vụ trả một lần** - bảng bốn cột: Dịch vụ | Đơn giá | Số lượng | Thành tiền.

- Dòng Express ghi rõ trong ô mô tả: nguyên giá mỗi gói nhân số gói, rồi dòng ưu đãi. Mô tả kèm "phạm vi tại Mục 2".
- Mỗi hạng mục phát triển một dòng, ghi "mô tả tại Mục 3".
- Dòng tổng in đậm.

**Năm ghi chú bắt buộc dưới bảng** (gạch ý có nhãn):

1. **Ưu đãi Cloud** - nêu rõ số tiền ưu đãi và **điều kiện thu hồi**: ưu đãi áp dụng với điều kiện khách dùng thuê bao Cloud trong suốt thời gian triển khai và thời gian hỗ trợ hậu triển khai; ngừng trước thời hạn thì phần ưu đãi được thu lại.
2. **Thuế** - không thuộc đối tượng chịu thuế giá trị gia tăng theo quy định hiện hành.
3. **Phát triển** - tính theo hạng mục, đã gồm phân tích thiết kế, lập trình, kiểm thử, đào tạo nghiệm thu, bảo hành và tài liệu hướng dẫn. Thêm câu: chi phí đã áp dụng AI hỗ trợ lập trình, kiểm thử và viết tài liệu.
4. **Chưa gồm** - phí thuê bao và hạ tầng Cloud; **chi phí đi lại, ăn ở của chuyên viên Viindoo khi làm việc tại Công ty**; thiết bị phần cứng; bảo trì phần phát triển sau thời hạn bảo hành.
5. **Số liệu chính thức** - phạm vi và thời lượng từng hạng mục chốt sau giai đoạn Khảo sát và Lập kế hoạch; tổng giờ của gói cố định theo hợp đồng.

**7.2 Dịch vụ trả định kỳ theo năm** - bảng hai cột: Dịch vụ | Đơn giá. Ghi chú: số lượng người dùng chốt tại thời điểm chạy chính thức theo danh sách nhân sự thực tế - **không nhân sẵn ra tổng năm thứ nhất** để tránh đưa ra một con số trông như chính xác trong khi số người dùng chưa được xác nhận. Thêm: gói thuê bao bao trọn ứng dụng trong bản tiêu chuẩn cho các nghiệp vụ nêu tại Mục 2; hạ tầng, sao lưu, nâng cấp do Viindoo đảm nhiệm.

## Nâng cấp phiên bản

Khi có hạng mục nâng cấp, ghi **đủ giá theo bảng giá** rồi ghi ưu đãi thành một dòng riêng - kể cả khi Viindoo tặng thì vẫn ghi đủ giá rồi ưu đãi 100%, **không ghi "không tính phí" trần**. Mức giá và mức giảm cho phiên bản kế tiếp: hỏi Liên hoặc tra bảng giá hiện hành.

## Ưu đãi gói Express

Chỉ áp cho gói Express **đầu tiên** của khách dùng Cloud. Khách đã từng mua Express trước đó thì gói sau tính đủ giá. **Tra lịch sử đơn hàng của khách trước khi ghi ưu đãi** - đây là lỗi đã xảy ra thật, giảm giá nhầm cho khách cũ.

## Khi giá đã bị chốt trước

Có dự án giá tổng đã chốt trong hợp đồng trước khi phương án hoàn thiện. Khi đó phần phát triển được phân bổ ngược từ tổng đã chốt chứ không tính xuôi - đây là **trường hợp đặc biệt của từng deal**, không phải cách làm chuẩn, và không mang sang dự án khác.

## Soát trước khi giao

```python
phat_hien = vdoc.kiem_ban_gui_khach(duong_dan_tep)
print(vdoc.in_ket_qua_soat(phat_hien))
```

- Mức **PHẢI SỬA**: "Junior", "Senior", "Expert", "manday" - cách tính giá nội bộ lọt ra ngoài.
- Mức **cần xem**: "ngày công", "giờ công" đứng gần từ chỉ tiền. Từ này có thể là **nghiệp vụ của chính khách** (ví dụ "lương theo ngày công" của họ) - đọc trích đoạn rồi tự quyết, đừng sửa máy móc. Chỗ nào chắc chắn là nghiệp vụ khách thì truyền `bo_qua=["ngày công"]`.
