# Giọng đọc - chọn, thu, chấm

Gemini TTS, model `gemini-2.5-flash-preview-tts`. Khoá ở biến môi trường `GEMINI_API_KEY`.
Đây là chỗ duy nhất trong dây chuyền dùng Gemini API trả phí - nội dung chữ thì dùng Gemini web
miễn phí.

## TIỀN - đọc trước khi gọi lượt thu đầu tiên

**Ngày 30/10/2026 hạn mức Gemini cạn sạch giữa lúc đang làm cụm Dự án.** Đếm lại:

| Việc | Số lượt trong một ngày | Lượng sinh ra |
|---|---|---|
| **Thu giọng (TTS)** | **30** | **~100 phút tiếng** |
| Chép lại để soát (STT) | ~24 | mỗi lượt nuốt trọn một bản ba phút |
| Rà lời bằng Gemini (chữ) | 2 | ~7 KB vào, ~5 KB ra |

Chữ gần như không tốn gì; **tiếng là toàn bộ chi phí**, và mỗi lần thu còn kéo theo một lần chép
lại để soát, tức là nhân đôi. Ba chỗ tiêu hoang đã mắc phải:

1. **Thu 14 lượt cho một bản lời người duyệt còn đang sửa cấu trúc** - sai thứ tự việc, không phải sai
   kỹ thuật.
2. **Thi giọng: 6 giọng × trọn bài = 6 lượt**, chỉ để so cao độ.
3. **Thu lại cả bài vì một chữ đọc sai** - hai lần.

### Ba luật từ 30/10/2026

1. **Giọng đã chốt cho cả bộ clip cụm, KHÔNG thi lại ở từng cụm.**
   Tiếng Việt: **Fenrir**. Tiếng Anh: **Iapetus**. Chỉ thi giọng lại khi thêm một NGÔN NGỮ mới,
   hoặc khi người duyệt nói đổi. Số đo cũ nằm ở bảng dưới, dùng lại được.
2. **Chỉ thu cả bài khi lời đã CHỐT HẲN.** Lời còn có thể đổi cấu trúc thì chưa gọi TTS lượt nào.
   Muốn nghe thử nhịp thì đọc bảng đếm âm tiết (`--text`), không thu.
3. **Soát chữ TRƯỚC khi thu, không soát sau.** Chữ đã biết hay bị đọc sai thì thay ngay từ bản
   viết, đừng thu rồi mới phát hiện rồi thu lại cả bài:

| Viết thế này thì sai | Thay bằng |
|---|---|
| aptomat | *(đã thay)* cầu dao tổng - nhưng "cầu dao" cũng bị nghe thành "cầu giao" |
| cầu dao | **bộ đóng cắt** |
| kho tri thức | **Kho tri thức** viết hoa, đặt sau "trang tài liệu trong" |
| tám mươi mốt / một trên ba | máy chép ghi thành chữ số - **không phải lỗi đọc**, đừng thu lại |
| tên riêng nước ngoài | viết lại theo cách đọc trong bảng `SAY` |

Mỗi cụm mới, bổ sung vào bảng này chữ nào vừa bị đọc sai - đó là cách duy nhất làm nó rẻ dần.

## Chọn giọng cho một ngôn ngữ mới

> Chỉ chạy mục này khi thêm NGÔN NGỮ MỚI. Cụm mới cùng ngôn ngữ thì dùng thẳng giọng đã chốt.


**Giọng duyệt ở ngôn ngữ này KHÔNG mặc nhiên dùng được ở ngôn ngữ kia.** Cùng một giọng, đọc hai thứ
tiếng ra cao độ khác hẳn nhau:

| Giọng | Đọc tiếng Việt | Đọc tiếng Anh |
|---|---|---|
| Fenrir | 137,1 Hz - Liên chọn cho bản Việt | 115,9 Hz - Liên loại: *"trầm quá, gằn, có chữ nghe ko rõ"* |
| Achird | 150,9 Hz - Liên chê **quá sáng** | 127,3 Hz |
| Iapetus | 131,9 Hz | 134,8 Hz - **Liên chọn cho bản Anh** |

Nên xếp hạng giọng phải đo **trên chính ngôn ngữ sẽ dùng**.

Cách làm: thu CẢ BÀI cho từng giọng ứng viên bằng chính script lời đọc (`VOICE_NAME` chọn giọng),
đo bằng `voice_stats.py`, rồi cắt cùng một đoạn đầu của mỗi bản ghép nối lại bằng ffmpeg để nghe liền mạch:

```bash
for g in Puck Iapetus Achird Sadaltager; do CLIP_LANG=en VOICE_NAME=$g python3 tts_en_fw.py; done
python3 voice_stats.py voice/*.wav
```

**Phải thu cả bài rồi mới cắt đoạn đầu ra so.** Đọc riêng một đoạn thì Gemini đẩy cao độ lên
140-169 Hz so với 119-126 Hz khi đọc cả bài - nghe mẫu ngắn sẽ chọn nhầm giọng.

Đưa người duyệt nghe, kèm bảng số đo và một câu nhận xét mỗi giọng. **Để người duyệt chọn bằng tai** - số đo chỉ
loại được giọng dở, không chọn thay được.

Giọng nam sáng đáng thử: `Iapetus`, `Achird`, `Puck`, `Sadaltager`, `Alnilam`, `Zubenelgenubi`.

## Thu bản chính

```bash
CLIP_LANG=en python3 pick_take.py 3    # thu 3 bản, chấm, giữ bản sạch nhất
```

`pick_take.py` thu N bản, nhờ Gemini chép lại từng bản, so với bản viết, đếm chỗ lệch THẬT (bỏ qua
số đếm viết bằng chữ số, biến thể chính tả, tên Viindoo), rồi giữ bản ít lỗi nhất. Hoà thì lấy bản
đọc nhanh hơn.

**Chất giọng đứng trước số lỗi chữ**: bản trầm hoặc đều đều thì nghe là biết ngay, còn sai một chữ
lẻ thì đổi cách viết chữ đó rồi thu lại.

Ngưỡng loại (`F0_SAN`, `DAI_F0_TOI_THIEU`): tiếng Việt 126 Hz, tiếng Anh 126 Hz, dải F0 tối thiểu
85 Hz. Ngưỡng tiếng Anh từng để 112 Hz - quá thấp, lọt đúng bản Liên chê. **Ngưỡng phải cao hơn mức
Liên đã loại**, nếu không nó vô nghĩa.

## Các bẫy của TTS

- **Vá một đoạn lẻ không dùng được.** Đọc riêng một đoạn thì cao độ vọt lên hẳn so với cả bài, ghép
  vào nghe lộ ngay. Sai một chữ thì **đổi cách viết chữ đó rồi thu lại cả bài**.
- **Tiếng Việt sai dấu ngẫu nhiên.** Cùng một bản viết, mỗi lần thu sai dấu ở một chữ khác ("đông
  thêm" -> "đồng thềm"). Nên mới phải chép lại bằng máy để soát chứ không nghe may rủi.
- **`check_tts.py` chép tiếng bằng `gemini-2.5-flash`** phải đặt `thinkingConfig.thinkingBudget=0`
  kèm `maxOutputTokens`, không thì nó nghĩ hết token mà không trả chữ.
- **Chạy `check_tts` kèm `SSL_CERT_FILE` trỏ certifi**, không thì lỗi chứng chỉ - không phải hỏng
  bản thu.
- **Kéo nhịp bằng `atempo` thì cân nhắc.** Giữ cao độ nhưng làm chữ sít lại. Nếu người duyệt vừa chê "nghe
  không rõ chữ" thì **đừng kéo nhịp**, để nhịp tự nhiên và chấp nhận clip dài thêm - Liên đã nói
  *"nếu thiếu có thể nối dài video chút"*.
- **Máy không nghe được.** Không bao giờ tự nhận đã kiểm giọng hay nhạc bằng tai. Nói rõ với người duyệt là
  cần người nghe.
