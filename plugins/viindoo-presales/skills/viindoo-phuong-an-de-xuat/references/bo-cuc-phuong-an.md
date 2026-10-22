# Bố cục phương án - chi tiết từng mục

Theo mẫu JVC Eco v3. Giữ đúng thứ tự và cách đánh số; nội dung viết lại theo từng khách.

## Tóm tắt điều hành

- Ba đến bốn thẻ số, **chỉ số của Viindoo**: tổng đầu tư trả một lần, thuê bao trên người dùng, tiến độ dự kiến, số pháp nhân cùng chạy trên một hệ thống.
- Một khối gạch ý ngắn nói phạm vi gồm gì. Người quyết định đọc 30 giây phải biết cần quyết gì.

## 1. Bối cảnh và phạm vi

Gạch ý có nhãn: khách là ai, đang vướng gì, đợt này làm gì, không làm gì. Mô tả định tính theo đầu mục nghiệp vụ - **không nêu số bản ghi hay số tiền lấy từ hệ thống đang chạy của khách**.

## 2. Mô tả nghiệp vụ trên hệ thống Viindoo

Mục dài nhất, cũng là mục khách đọc kỹ nhất. Mỗi nhóm một khối, trong khối liệt kê từng nghiệp vụ kèm nhãn mức đáp ứng (Có sẵn - dùng ngay / Có sẵn - cấu hình / Có sẵn - tích hợp).

**Xếp theo dòng chảy đơn hàng của khách**, không theo mã BR:

CRM - bán hàng - đề nghị và lệnh sản xuất, định mức - mua nguyên vật liệu - kho và cấp liệu - sản xuất và kiểm soát chất lượng - bảo trì - xuất kho và giao hàng - kế toán - nhân sự - lương.

Trong mỗi nhóm cũng xếp theo thứ tự việc diễn ra. Ngành đã có bộ quy trình riêng thì nhóm theo bộ quy trình ngành và import thẳng tệp quy trình đó làm nguồn, không chép tay tên quy trình.

Luôn có nhóm CRM với tính năng có sẵn, kể cả khi khách chưa nêu. Khách có sản xuất thì phải có nhóm bảo trì.

## 3. Các yêu cầu cần phát triển ngoài phạm vi gói

Danh sách "Tên hạng mục (BR-x): số tiền" và tổng tiền. **Không giờ, không ngày công, không đơn giá theo cấp.**

Thêm một dòng: chi phí phát triển đã áp dụng AI hỗ trợ lập trình, kiểm thử, viết tài liệu.

## 4. Cách tiếp cận

Thẻ gạch ý: làm theo gói nối tiếp nhau, chốt phạm vi từng gói ở giai đoạn khảo sát, vận hành thật rồi mới mở rộng.

## 5. Quy trình triển khai

Các giai đoạn theo phương pháp luận triển khai của Viindoo. Giữ nguyên tên giai đoạn chuẩn, không tự đặt tên mới.

## 6. Phân bổ giờ công theo giai đoạn

Bảng: giai đoạn | giờ | phần việc chính. Ghi chú bắt buộc dưới bảng:

- Giờ ở đây là **giờ công chuyên viên Viindoo**, không phải giờ lịch; nhiều chuyên viên làm song song thì cộng dồn.
- Thời gian Công ty tự nhập liệu, tự đọc tài liệu không tính vào giờ gói.
- Thời lượng từng hạng mục được thống nhất ở giai đoạn Khảo sát và Lập kế hoạch; tổng giờ gói cố định theo hợp đồng.

**Không cắt giờ khảo sát** vì đã có tài liệu phân tích làm sẵn - khảo sát thực địa với từng phòng ban là việc khác.

## 7. Kế hoạch triển khai chi tiết

Theo tuần. Các gói **nối tiếp nhau** kiểu scrum, chỉ gối phần giám sát; không chạy song song hai gói. Mỗi tuần ghi phần việc chính và kết quả bàn giao.

## 8. Báo giá

- **8.1 Dịch vụ trả một lần** - tách rõ: gói Viindoo Express (có ưu đãi nếu đủ điều kiện) và Dịch vụ phát triển (chỉ tổng tiền). Nâng cấp phiên bản nếu có.
- **8.2 Dịch vụ trả định kỳ theo năm** - thuê bao, chỉ ghi đơn giá gói trên người dùng trên tháng.
- **Chưa gồm** - luôn có dòng chi phí đi lại, ăn ở của chuyên viên Viindoo khi làm việc tại khách.

Chi tiết cách trình bày: `bang-gia.md`.

## 9. Khuyến nghị

Gạch ý: nên bắt đầu từ đâu, cần Công ty chuẩn bị gì, rủi ro nào cần để ý.

## Mục cuối - Đề xuất giai đoạn sau (ngoài phạm vi báo giá)

**Luôn là mục đánh số cuối cùng**, sau Báo giá và Khuyến nghị. Tiêu đề ghi rõ "(ngoài phạm vi báo giá)" kèm một khung nói rõ phần này không nằm trong tổng chi phí. Đặt ở giữa tài liệu là khách hiểu nhầm đã tính tiền.

## Khối chuyên gia

Nếu có, đặt cuối tài liệu: ảnh và một đoạn ngắn giới thiệu người phụ trách tư vấn. Dùng lại khối `.expert` trong CSS `phuong-an`.
