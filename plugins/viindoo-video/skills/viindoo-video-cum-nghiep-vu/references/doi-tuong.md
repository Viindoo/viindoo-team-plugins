# Bước 1 - Tìm đối tượng sử dụng

Đây là việc ĐẦU TIÊN, làm trước khi viết một chữ kịch bản. Lý do: góc kể, hai mục đích, dòng chảy
nghiệp vụ, chọn màn hình nào, khoanh con số nào - tất cả đều suy ra từ chân dung người xem. Viết góc
trước rồi mới đi tìm người xem là làm ngược, và kết quả luôn là một clip trình diễn tính năng.

Kết quả bước này: một file `<Cum>-Doi-Tuong-Va-Nhu-Cau.md` trong thư mục cụm, người duyệt nội dung duyệt bằng chữ.

## Bốn câu phải trả lời

1. **Ai xem** - ngành nào, công ty cỡ nào, ai là người quyết (giám đốc, trưởng bộ phận, chủ đầu tư).
2. **Đang dùng gì** - tên phần mềm lẻ cụ thể họ đang trả tiền, và Excel đứng ở đâu trong đó.
3. **Bài toán của họ** - chỗ đứt gãy thật trong công việc hằng ngày, nói bằng chữ của nghề.
4. **Kỳ vọng khi dùng cụm này** - họ mong thấy gì sau khi đổi sang Viindoo. Đây là thứ sẽ thành
   **hai mục đích** ở bước 2, nên phải rút được thành hai, ba chữ.

Một cụm thường có **vài nhóm đối tượng khác hẳn nhau** đứng chung một tên. Phải tách ra rồi CHỌN
một nhóm làm nhân vật chính, không gộp - gộp là clip nói với tất cả và không chạm được ai. Nhóm bị
loại cũng ghi lại kèm lý do loại.

## LUẬT GỐC: đo thị trường, không đo Viindoo

**Lượt đọc blog viindoo.com và cơ hội trong CRM KHÔNG được dùng làm bằng chứng nhu cầu thị trường.**
Liên chốt 26/10/2026, sau khi bản đầu của cụm Dự án lấy hai nguồn đó ra làm căn cứ.

Lý do: ta làm lại cách tiếp cận một cụm chính vì đang làm chưa tốt ở cụm đó. Hai nguồn nội bộ chỉ
đo được chỗ Viindoo đã chạm tới - tức là chỗ yếu - nên lấy chúng chứng minh nhu cầu là lập luận
vòng, và luôn dẫn tới kết luận "cứ làm tiếp như cũ". Blog và CRM dùng được ở một việc khác: đối
chiếu xem Viindoo đang lệch đâu so với thị trường, và chỉ ghi ở mục "chỗ còn yếu".

Nguồn hợp lệ là nguồn bên ngoài:

| Nguồn | Đo được gì | Không đo được gì |
|---|---|---|
| **Gợi ý tự động Google** | độ RỘNG của nhu cầu, tên hãng đang chiếm sóng, ý định mua hay tìm bản miễn phí | số lượt tìm tuyệt đối |
| **Trang sản phẩm và bảng giá của ĐỐI THỦ** | danh mục đã hình thành chưa, họ đã chiếm câu nào, giá thị trường | họ làm tốt tới đâu (trang tiếp thị tự nói) |
| **Báo ngành, hiệp hội, báo cáo nhà nước** | nỗi đau THẬT bằng chữ của ngành, có nguồn trích được | nỗi đau nào phần mềm giải được |
| **Thống kê doanh nghiệp (GSO)** | quy mô tập khách | cơ cấu chi tiết nếu ngành bị gộp nhóm |

## Bắt buộc: đọc xem đối thủ ĐÃ CHIẾM CÂU NÀO

Làm trước khi nghĩ góc kể, không phải sau. Vào thẳng trang sản phẩm của hai, ba hãng đang chiếm
sóng và chép lại **đúng câu họ quảng cáo**.

Lý do: góc hay nhất mình nghĩ ra thường đã là khẩu hiệu của đối thủ. Cụm Dự án 26/10: góc đề xuất
ban đầu là "Viindoo cho biết công trình lãi hay lỗ" - đọc trang FastCons thì họ đang bán đúng
"theo dõi lãi lỗ công trình thời gian thực", "cảnh báo hạng mục vượt dự toán", có cả bản riêng cho
cơ điện và nội thất. Mở clip bằng câu đó là nói lại quảng cáo của đối thủ bằng giọng yếu hơn.

Chỗ trống thật thường nằm **ngay dưới câu đối thủ đã chiếm**, ở thứ họ không có: FastCons không có
phân hệ kế toán, nối sang kế toán bằng API - nên khách của họ vẫn nuôi hai bộ số. Đó mới là cú lật.

**Hai thước đo khi đọc trang đối thủ:** câu nào họ nói to nhất (đã chiếm, đừng tranh), và thứ nào
họ im lặng hoặc đẩy sang "tích hợp với bên thứ ba" (chỗ trống, kiểm rồi vào).

Mọi điều đọc từ trang tiếp thị đối thủ là **họ nói họ làm được**, chưa phải họ làm tốt. Trước khi
đưa vào lời đọc của clip thì phải xác minh thêm (dùng thử, đọc tài liệu API), và ghi rõ chỗ nào
chưa xác minh.

### Cách chạy phép đo gợi ý tự động

Gọi `https://suggestqueries.google.com/complete/search?client=firefox&hl=vi&gl=vn&q=<cụm từ>`, rải
thêm a-z sau mỗi cụm từ gốc (27 truy vấn một cụm từ), đếm **số gợi ý duy nhất**. Có gợi ý nghĩa là
có người gõ thật. Vắng gợi ý là dưới ngưỡng, không chứng minh bằng không.

Bốn điều bắt buộc, cả bốn đều đã trả giá:

- **Dùng TLS bình thường** (`SSL_CERT_FILE` trỏ certifi nếu máy báo lỗi chứng chỉ). Đừng tắt kiểm
  chứng chỉ - máy sẽ chặn, và chặn đúng.
- **Rải nhiều cụm từ gốc, mỗi lớp ý định một cụm** - tên chung của cụm, tên theo ngành, tên theo
  việc cụ thể. Một cụm từ gốc chỉ cho thấy một góc.
- **LỌC NHIỄU rồi mới đếm.** Ba loại nhiễu luôn có và luôn lớn: sinh viên (giáo trình, bài tập lớn,
  đồ án, tên trường), cơ quan nhà nước trùng tên (ban quản lý dự án tỉnh X), và nghề nghiệp (JD, CV,
  mức lương, ngành học). Cụm Dự án đo 25/10 ra 144 gợi ý cho "quản lý dự án xây dựng", lọc xong còn
  61 - hơn một nửa là sinh viên và ban quản lý dự án nhà nước.
- **Đọc nội dung gợi ý, đừng chỉ đếm.** Con số nói độ rộng; danh sách nói đối tượng là ai, đang dùng
  hãng nào, và đang tìm bản miễn phí hay đang đi mua.

### Hai dấu hiệu quyết định nhất trong danh sách gợi ý

- **Tỷ lệ chứa "miễn phí / free / crack / tải"** - cao thì nhóm đó không trả tiền, clip nhắm vào là
  phí. Thấp thì họ đang đi mua.
- **Tên hãng chiếm sóng** - nhiều hãng nội địa chuyên sâu nghĩa là danh mục đã hình thành và cạnh
  tranh gắt; không hãng nào xuất hiện nghĩa là danh mục chưa hình thành ở Việt Nam, bán bằng tìm
  kiếm sẽ rất chậm.

## Bẫy: cụm người ta TÌM không phải cụm mình MUỐN BÁN

Hay gặp nhất, và là lý do bước này tồn tại. Người mua gõ cái họ đã biết tên; cái Viindoo mạnh thì họ
chưa biết nên không gõ bao giờ. Cụm Dự án đo 25/10: "phần mềm quản lý chi phí dự án" đúng **1** gợi
ý, "phần mềm chấm công theo dự án" **0** - trong khi lãi lỗ dự án chính là chỗ Viindoo hơn hẳn công
cụ quản lý công việc.

Xử lý: **lấy cụm họ tìm làm cửa vào, lấy cụm mình mạnh làm cú lật trong clip.** Đừng đổi tiêu đề
sang cụm không ai tìm, và cũng đừng bỏ thế mạnh chỉ vì nó không có lượt tìm.

## Cổng ra

Trước khi sang bước 2, file đối tượng phải trả lời được: nhắm nhóm nào, loại nhóm nào và vì sao,
bài toán nói bằng chữ của nghề **kèm nguồn trích được**, kỳ vọng rút gọn được thành hai hoặc ba
chữ, cụm từ nào làm cửa vào, **câu nào đối thủ đã chiếm nên phải tránh**, và cú lật nằm ở đâu.
Người duyệt chốt chân dung này rồi mới viết góc.

Tự soát ba câu trước khi đưa người duyệt:

1. Có câu nào trong này chỉ dựa vào dữ liệu của chính Viindoo không? Có thì bỏ ra khỏi phần căn cứ.
2. Góc định đề xuất có trùng khẩu hiệu của hãng nào đang bán không?
3. Nỗi đau viết ra có trích được từ nguồn ngoài không, hay là mình tự suy?
