# Bố cục phương án - chi tiết từng mục

Mẫu chuẩn hiện hành (bản Quang Thắng, 20/10/2026). Giữ đúng thứ tự và cách đánh số; nội dung viết lại theo từng khách. Các mẫu cũ hơn không dùng nữa.

## Tóm tắt điều hành

- Ba đến bốn thẻ số, **chỉ số của Viindoo**: tổng dịch vụ trả một lần, thuê bao trên người dùng, tiến độ dự kiến, số gói Express.
- Một khối gạch ý ngắn nói phạm vi gồm gì. Người quyết định đọc 30 giây phải biết cần quyết gì.

## 1. Bối cảnh và phạm vi

Gạch ý có nhãn: khách là ai, đang vướng gì, đợt này làm gì, không làm gì. Mô tả định tính theo đầu mục nghiệp vụ - **không nêu số bản ghi hay số tiền lấy từ hệ thống đang chạy của khách**.

## 2. Mô tả nghiệp vụ trên hệ thống Viindoo

Mục dài nhất, cũng là mục khách đọc kỹ nhất, và là mục sẽ đi thẳng vào phụ lục hợp đồng ở bước 5 - nên viết như một cam kết, không phải lời quảng cáo.

Mỗi nhóm một khối `vdoc.nhom_nghiep_vu(tieu_de, cau_dan, muc, can_lam_ro)`:

- **Câu dẫn** - một câu nói nhóm này giải quyết gì, viết cho người làm nghề đọc. Ví dụ: "Mỗi yêu cầu sản phẩm mới hình thành một hồ sơ có mã, tên và model riêng; hồ sơ này là chứng từ gốc cho mọi bước phía sau."
- **Gạch ý** - mỗi ý là một việc hệ thống làm được, nói bằng ngôn ngữ nghiệp vụ, không nêu tên model.
- **Khối Cần làm rõ** - điểm phải thống nhất ở giai đoạn Khảo sát. Để riêng ra, không trộn vào phần khẳng định.

**Xếp theo dòng chảy đơn hàng của khách**, không theo mã BR:

dữ liệu nền - CRM - bán hàng và báo giá - kế hoạch và ngày giao - hồ sơ kỹ thuật - điều hành xưởng - chất lượng - thuê ngoài gia công - mua hàng - kho vận - bảo trì - giao hàng - chấm công, nhân sự và lương - kế toán - giá thành - phân quyền.

Trong mỗi nhóm xếp theo thứ tự việc diễn ra. Ngành đã có bộ quy trình riêng thì nhóm theo bộ quy trình ngành và import thẳng tệp quy trình đó làm nguồn. Luôn có nhóm CRM dù khách chưa nêu; khách có sản xuất thì phải có bảo trì.

Nếu có bảng đối chiếu từng yêu cầu với mức đáp ứng, đặt trong nhóm tương ứng, mỗi dòng kèm mã yêu cầu để truy ngược về danh mục BR.

## 3. Các yêu cầu cần phát triển ngoài phạm vi gói

Mở đầu bằng một đoạn nói vì sao chúng không nằm trong gói, rồi khối nguyên tắc bắt buộc (`vdoc.NGUYEN_TAC_PHAT_TRIEN`): mỗi hạng mục xây mở rộng trên phân hệ sẵn có nên vẫn thừa hưởng phân quyền, nhật ký, báo cáo và các bản nâng cấp; dữ liệu đi vào chứng từ gốc, không tạo luồng số liệu song song.

Mỗi hạng mục một khối `vdoc.khoi_phat_trien(...)`, **giá hiển thị ngay cạnh tên**:

| Phần | Viết gì |
|---|---|
| Tóm tắt | một đoạn nói hạng mục này làm được gì cho khách |
| Bài toán hiện nay | khách đang phải làm thủ công ra sao, sai ở đâu |
| Hệ thống sẽ làm gì | kết quả quan sát được, không mô tả kỹ thuật |
| Vì sao phải phát triển thêm | vì sao cấu hình không đủ - đây là chỗ chống câu hỏi "sao không có sẵn" |
| Giới hạn phạm vi | cái gì **không** nằm trong hạng mục - chống phình việc lúc nghiệm thu |

Không ghi giờ, ngày công, đơn giá theo cấp ở bất kỳ đâu trong mục này.

## 4. Cách tiếp cận

Thẻ gạch ý: làm theo gói nối tiếp nhau, chốt phạm vi từng gói ở giai đoạn khảo sát, vận hành thật rồi mới mở rộng.

## 5. Quy trình triển khai

Các giai đoạn theo phương pháp luận triển khai của Viindoo, dạng dải bước có số thứ tự. Giữ nguyên tên giai đoạn chuẩn, không tự đặt tên mới.

## 6. Kế hoạch triển khai chi tiết

Bảng tiến độ theo tuần: hạng mục | giờ | các cột tuần tô màu theo giai đoạn. Các gói **nối tiếp nhau** kiểu scrum, chỉ gối phần giám sát.

Ghi chú bắt buộc dưới bảng:

- Giờ là **giờ công chuyên viên Viindoo**, không phải giờ lịch; nhiều chuyên viên song song thì cộng dồn.
- Thời gian khách tự nhập liệu, tự đọc tài liệu không tính vào giờ gói.
- Thời lượng từng hạng mục chốt ở giai đoạn Khảo sát và Lập kế hoạch; tổng giờ gói cố định theo hợp đồng.

**Không cắt giờ khảo sát** vì đã có tài liệu phân tích làm sẵn.

## 7. Báo giá

7.1 trả một lần, 7.2 trả định kỳ theo năm. Chi tiết cách trình bày và năm ghi chú bắt buộc: `bang-gia.md`.

## 8. Khuyến nghị

Thẻ gạch ý: nên bắt đầu từ đâu, cần khách chuẩn bị gì, rủi ro nào cần để ý.

## Mục cuối - Đề xuất giai đoạn sau (ngoài phạm vi báo giá)

Nếu có, **luôn là mục đánh số cuối cùng**, sau Báo giá và Khuyến nghị, tiêu đề ghi rõ "(ngoài phạm vi báo giá)" kèm khung nói rõ phần này không nằm trong tổng chi phí. Đặt ở giữa tài liệu là khách hiểu nhầm đã tính tiền.

## In ra PDF

Các mục lớn bắt đầu trang mới (`style="break-before:page"`), đầu bảng lặp lại khi bảng tràn trang, khối phát triển và thẻ không bị cắt ngang. CSS trong `kit/css/phuong-an.css` đã lo sẵn; đừng bỏ phần `@media print`.
