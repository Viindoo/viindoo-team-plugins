# Ví dụ nội dung từng phần - tài liệu mô hình hoạt động

Lấy từ các dự án thật đã gửi khách. Cấu trúc tái dùng được; nội dung thì mỗi khách viết lại 100%.

## Phần 3 - Mô hình kinh doanh trong một đoạn

Viết được thành một đoạn thì mới là hiểu đúng. Mỗi mệnh đề phải kéo theo một hệ quả cho giải pháp.

> Công ty vừa sản xuất vừa phân phối. Hàng sản xuất theo đơn cho khách công nghiệp đi theo một đường; hàng sản xuất sẵn cho kênh bán lẻ đi theo đường khác. Hai kiểu này khác nhau về bản chất: một bên kế hoạch chạy theo đơn đã ký, một bên chạy theo dự báo và mức tồn.

Hệ quả nêu ngay dưới: hệ thống phải chạy song song hai kiểu kế hoạch, không ép về một.

## Phần 5 - Các dòng chảy nghiệp vụ

Mỗi dòng một tiểu mục, viết bằng lời người làm nghề, bám đúng thứ tự xảy ra:

- **Dòng nhu cầu và đơn hàng** - nhu cầu đến từ đâu, ai nhận, chốt giá thế nào, đơn vào hệ thống lúc nào.
- **Dòng kế hoạch** - ai cân đối, cân theo gì, chốt theo chu kỳ nào.
- **Dòng mua hàng** - đề nghị mua sinh ra từ đâu, duyệt ở cấp nào, hàng về ai nhận.
- **Dòng vật tư và bán thành phẩm** - vật tư đi qua những công đoạn nào, chỗ nào đổi đơn vị đo, chỗ nào đổi định danh.
- **Dòng ngược** - phế, tái sinh, trả hàng, đổi hàng.
- **Dòng giá thành** - chi phí tụ về đâu, ai chốt giá thành, chốt theo kỳ nào.

Số dòng tùy ngành: thương mại phân phối thường năm dòng, sản xuất liên tục thường sáu đến bảy.

## Phần 6 - Bộ máy: vai và ai giữ số

Bảng ba cột: **Vị trí | Việc đang làm | Số liệu người này giữ**.

Cột thứ ba quyết định phân quyền và ai nhập liệu sau này, nên không được bỏ. Ví dụ: thủ kho giữ số tồn thực tế; kế toán kho giữ số tồn trên sổ; hai số này lệch nhau là một điểm đứt gãy phải ghi ở phần 9.

## Phần 7 - Đặc tính dữ liệu quyết định hình giải pháp

Phần có giá trị nhất. Mỗi đặc tính viết theo khuôn: **nó là gì** - **nó buộc hệ thống phải làm gì**.

Các đặc tính đã gặp ở dự án thật:

| Đặc tính | Buộc hệ thống phải |
|---|---|
| Đơn vị đo kép (kg và mét), nối nhau bằng định lượng | khai đơn vị kép và hệ số quy đổi theo từng mã, không quy đổi cứng |
| Quy cách nằm trong mã hàng làm số mã bùng nổ | dùng biến thể sản phẩm thay vì tạo mã rời |
| Định danh từng đơn vị (cuộn, vỏ bình, máy) | theo dõi theo số seri, kèm chủ sở hữu tách khỏi người đang giữ |
| Công thức phối liệu đổi theo lô | định mức theo phiên bản, không sửa đè lên định mức gốc |
| Một pháp nhân bán hộ pháp nhân khác | nhiều công ty trên cùng hệ thống, có bút toán nội bộ |

## Phần 10 - Dữ kiện và giả thuyết

Hai cột rõ ràng:

- **Dữ kiện** - đọc được từ tài liệu khách gửi, ghi nguồn: tên tệp, mục, dòng.
- **Giả thuyết** - suy luận của Viindoo, ghi rõ là suy luận và cần khách xác nhận.

Đừng trộn hai loại vào một gạch đầu dòng. Khách đọc thấy một giả thuyết bị trình bày như dữ kiện là mất tin ở cả tài liệu.

## Ô ý kiến

Cuối mỗi phần đặt một ô `vykien.y_kien(ma, nhan, khach)`. Nhãn viết theo đúng tên phần, để phiếu ý kiến in ra khách đọc biết đang góp ý chỗ nào.
