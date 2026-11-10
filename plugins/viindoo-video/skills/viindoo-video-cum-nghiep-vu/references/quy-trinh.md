# Quy trình chi tiết - bước 2 đến 6, 9 đến 10

Khuôn mã mọi đoạn nhắc ở đây nằm ở `templates/` của skill này; `scripts/tao_cum.sh` chép sang thư mục cụm (`clips/`, `demo-data/`). Khuôn lấy từ các cụm đã chạy thật (Nhân sự, Dự án, Bán hàng + CRM, Kho): bảng cảnh, bảng màn và lời đọc trong đó là của cụm gốc, cụm mới phải thay.

## Bước 2 - Chốt góc kể

Góc kể suy ra từ chân dung đối tượng đã chốt ở bước 1 (`references/doi-tuong.md`) - bài toán của họ
thành câu phản đề, kỳ vọng của họ thành hai mục đích. Chưa có chân dung thì chưa viết góc.

Clip cụm nghiệp vụ **không đi theo tính năng**. Nó đi dọc dòng chảy nghiệp vụ của cụm và luôn cho
người xem biết đang đứng ở đâu. Trước khi đụng tới hình, viết ra ba thứ và đưa người duyệt nội dung duyệt:

**a. Một câu phản đề.** Cụm này hay bị hiểu sai thành cái gì. HRM: *"Nhân sự không phải phòng giấy
tờ"*. Kế toán có thể là *"Kế toán không phải phòng ghi sổ"*. Câu này thành tiêu đề clip.

**b. Hai (hoặc ba) mục đích.** Trả lời "dùng cái này để làm gì", đặt TRƯỚC khi đi vào màn hình. Thiếu
nhịp này thì các màn phía sau chỉ là trình diễn tính năng rời rạc. HRM có **Quản** (nối con người
với tiền và vận hành) và **Xây** (dựng hành trình phát triển từng người). Mỗi mục đích về sau thành
một nhãn `PROOF: QUẢN` / `PROOF: XÂY` chạy trên từng cảnh màn hình, và thành hai cột ở cảnh kết.

**c. Dòng chảy 8-10 bước.** Đây là xương sống, hiện thành thanh bước chạy suốt clip. HRM: Tuyển dụng ·
Năng lực · Đào tạo · Chấm công · Tăng ca · Lương · Đánh giá · Chi phí · Giá thành. Bước cuối nên
**bắc sang cụm khác** (HRM kết ở giá thành sản phẩm) - đó là chỗ chứng minh "không đứng một mình".

**Tổng thể trước, ví dụ cụ thể sau** (luật Liên). Mỗi bước một cảnh, mỗi cảnh một con số.

## Bước 3 - Dữ liệu demo

Bơm trên hệ thống demo thật (mặc định `https://sanxuat18.viindoo.cloud`), đúng công ty sẽ quay.
Tên cơ sở dữ liệu và tài khoản đặt qua biến môi trường `VIINDOO_DEMO_URL`, `VIINDOO_DEMO_DB`,
`VIINDOO_DEMO_LOGIN`, `VIINDOO_DEMO_PASSWORD` (xin người quản lý hệ thống demo, không ghi vào tệp).
Kết nối qua `demo-data/conn.py` (XML-RPC); script bơm dữ liệu `demo-data/build*.py` viết riêng cho từng cụm.

- **Ghi lại mọi thứ đã tạo** vào `created.json` để còn gỡ được (`rollback.py`).
- **Số phải tự giải thích được và không mâu thuẫn.** Người duyệt từng bắt lỗi: tiền tăng ca cả xưởng 20
  triệu mà lương một người chỉ 8,9 triệu - nghe vô lý. Hoá ra 20,4 triệu là tổng 76 ca của 40
  người. Trước khi quay, tự hỏi lại từng con số: người xem có hiểu nhầm được không.
- Dữ liệu tạo bằng ngôn ngữ nào thì mang tên ngôn ngữ đó - tạo bằng đúng ngôn ngữ của clip gốc.

## Bước 4 - Bộ lọc đã lưu

Mỗi màn cần một bộ lọc đã lưu, đặt tên theo khuôn `VIDEO <CỤM> - Cxx <mô tả>`, ví dụ
`VIDEO HRM - C9c Tăng ca theo người (pivot)`. Lý do: `quay_fw.py` bật bộ lọc bằng cách bấm đúng
cái tên đó trong trình đơn, nên tên phải ổn định và duy nhất.

Tên bộ lọc hiện thành một chip trong thanh tìm kiếm, người xem đọc được - viết cho gọn gàng.

## Bước 5 - QUAY màn hình (không chụp ảnh tĩnh)

**Luật từ 29/10/2026: QUAY THẬT, không dùng ảnh tĩnh rồi kéo máy quay.** Bộ `clips/quay_fw.py`.
Ảnh tĩnh + kéo máy quay (cảnh `fwscreen` với `pan`) chỉ còn là phương án dự phòng khi quay không ra.

Ghi chép cũ nói "biểu đồ Viindoo vẽ bằng canvas nên quay video ra khung trắng" - **đo lại
29/10 thì sai**: quay bằng **Google Chrome thật trên máy** (không dùng trình duyệt đóng gói của
Playwright) thì biểu đồ hiện đầy đủ cột, trục, chú giải, và cả **chú thích khi rê chuột**.

Vì sao quay hơn hẳn chụp:
- **Rê chuột lên cột biểu đồ là con số tự bật ra** - lộ số tự nhiên hơn khoanh vòng lên ảnh.
- **Cảnh báo của phần mềm tự giải thích chính nó.** Rê lên tam giác cảnh báo xếp trùng giờ,
  Viindoo bung ra tên người và tên việc bị đụng - lời đọc chỉ cần đặt câu hỏi trước đó.
- **Thay đổi trạng thái kể được.** Quay hai lượt trước/sau một thao tác ghi sổ rồi cắt giữa, con
  số tự nhảy cột - không cần một lời giải thích nào.

Mỗi cảnh khai một mục trong bảng `CANH`: `name`, `url`, `pre` (mở app trước), `wait`, `fav`
(bộ lọc đã lưu), và `kich` - kịch bản thao tác gồm các bước `("cho", ms)`, `("di", x, y)`,
`("cuon", px)`, `("re", <js>)`, `("bam", <js>)`, `("xoaloc",)`.

### Tám cái bẫy khi quay - đều đã trả giá

1. **Cảnh báo "Mật khẩu đang là mặc định (admin)" đè góc màn.** Nó chỉ bắn ở bước chuyển hướng
   **ngay sau khi đăng nhập** (`bus/controllers/home.py` `_login_redirect`). Cách sạch: đăng nhập
   ở một phiên RIÊNG, lưu trạng thái phiên ra tệp, rồi mở phiên quay bằng trạng thái đó - phiên
   quay không đăng nhập nên không có cảnh báo. Đừng đi đổi mật khẩu hệ thống dùng chung.
2. **Odoo bám sẵn bộ lọc mặc định.** Màn nhiệm vụ mở ra với "Nhiệm vụ của tôi", không gỡ thì cảnh
   ra đúng mấy việc của admin chứ không phải việc của dự án. Bước `("xoaloc",)` bấm dấu × trên
   mọi chip bộ lọc trước khi quay.
3. **Cảnh dùng bộ lọc đã lưu thì KHÔNG được có bước `("xoaloc",)`.** Bộ lọc được bật TRƯỚC khi
   chạy kịch bản thao tác, nên `xoaloc` gỡ luôn chính nó - cảnh quay ra bảng mặc định.
   `xoaloc` chỉ dùng cho cảnh KHÔNG có `fav`.
4. **Khung bên phải có thanh cuộn RIÊNG.** Phải `("di", x, y)` đưa con trỏ vào trong khung rồi
   mới cuộn, nếu không cuộn trúng trang nền và cảnh đứng nguyên ở đầu bảng.
5. **Cuộn phải chia nhiều nhịp nhỏ.** Cuộn giật một phát nhìn rất xấu trên video.
6. **Playwright làm HỎNG mấy giây cuối của bản quay - mỗi bản một khác, phải ĐO từng tệp.**
   Lúc đóng ngữ cảnh, mấy khung cuối bị vẽ lại ở kích thước CSS thô trên nền xám, nằm gọn
   góc trên-trái khung 1920x1080. Đo 31/10/2026 trên 34 bản: **26 bản dính**, nhưng **8 bản
   sạch hoàn toàn** và bản dính nặng nhất hỏng **2,15 giây**.
   Vì vậy **đừng chừa một con số chung**: chừa thừa thì cắt mất phần đẹp của bản sạch (lần
   đầu tôi để `LE_DUOI = 2.5` và một cảnh báo "bản quay chỉ 12,3s" dù bản ấy sạch tinh);
   chừa thiếu thì bản hỏng nặng vẫn lọt. Chạy `do_duoi.py` sinh `quay-fw/duoi-hong.json`,
   `build_seq.py` đọc số riêng của từng tệp.
   **Nhận dạng đúng dấu hiệu** - đây là chỗ dễ sai nhất:
   - Khung hỏng = góc dưới-phải **phẳng lì** (độ lệch chuẩn ~0) và **không trắng** (trung
     bình < 200). Hai điều kiện đều cần: chỉ "phẳng" thì trang Odoo **đang tải** (trắng
     trơn, rgb 253, lệch 0) cũng dính; chỉ "không trắng" thì màn có biểu đồ màu cũng dính.
   - **Đừng đo bằng cách so với một khung tham chiếu giữa clip.** Trang đang tải cũng làm
     đổi màu dải bên phải, và phép đo sẽ báo hỏng cả đoạn tải trang - thử 31/10 báo nhầm
     9 giây trên `bang-thong-tin-du-an` trong khi thật ra chỉ hỏng 2,15 giây.
   - **Đừng gọi nó là "nền đen".** Nhìn ảnh thu nhỏ thì ra đen, nhưng số đo là **xám 126**.
     Đặt ngưỡng theo cái mắt tưởng là một lần quét trả về "0 / 34 bản dính" - sai trắng trợn.
   - Quét nhanh: **một lượt ffmpeg cho mỗi tệp** (`-sseof` + `crop` góc dưới-phải + `fps=10`)
     rồi đọc bằng PIL. Gọi ffmpeg từng khung một thì 34 bản chạy hàng giờ; gộp lại còn 17 giây.
7. **Ảnh `<tên>-khung.png` KHÔNG chứng minh được bản quay sạch.** Nó là `page.screenshot()`
   chụp TRƯỚC khi đóng trang, nên lúc nào cũng đẹp. Muốn biết video có sạch không thì phải
   **trích khung từ chính tệp video**, và trích NHIỀU MỐC (đầu, giữa, cuối) chứ không chỉ một.
   Cách đo: mở khung bằng PIL, xem điểm góc dưới-phải có phải `(128,128,128)` không.
8. **Luôn trích khung hình ra NHÌN.** Quay xong tự lưu một ảnh khung cuối; mở ra xem đúng bộ lọc,
   đúng tập bản ghi, có con số định khoanh chưa. Tệp video chạy được không có nghĩa là quay đúng.

Vẫn giữ khung 1280x720 nhân `device_scale_factor` 1,5 để ra 1920x1080 chữ to gấp rưỡi, và mọi
địa chỉ vẫn phải kèm `&cids=1`.

## Bước 6 - Viết lời

`clips/tts_<lang>_fw.py`, mảng `SCENES` - **một đoạn một cảnh**, đúng thứ tự cảnh.

- Mỗi đoạn có **đúng một con số làm trụ**, và một câu nói con số đó NGHĨA LÀ GÌ. Clip kể kết quả,
  không dạy cách bấm nút.
- Viết số **bằng chữ** cho máy đọc đúng ("tám triệu chín trăm năm mươi bảy nghìn").
- `SAY` là bảng viết lại theo cách đọc cho tên riêng máy đọc sai: `{"Viindoo": "Vin-doo"}`. Thay cụm
  dài trước cụm ngắn.
- `STYLE` (câu lệnh giọng) để **NGẮN**. Câu lệnh dài làm máy đọc chậm và đều.

## Bước 9 - Tính mốc cảnh

`clips/build_seq.py` sinh `$VIINDOO_VIDEO_WORKDIR/motion/seq/seq-<cụm>-fw[-en].json`.

Mốc cảnh **lấy từ khoảng lặng của chính bản thu**, không gõ tay, không đoán. Đếm âm tiết chỉ là
phương án dự phòng khi dò khoảng lặng hụt quá 25%. Hệ quả quan trọng: **đổi bản thu là phải chạy lại
`build_seq.py` và render lại TOÀN BỘ cảnh**, vì mọi thời lượng đều đổi theo.

Bảng `BROLL = {3: "hop", 9: "doi-ngu", 14: "ra-quyet-dinh"}` nghĩa là b-roll người thật chèn
TRƯỚC cảnh 3, 9, 14 và các cảnh đó render ngắn đi đúng bằng độ dài b-roll.

### Cách đặt hình - ba kiểu, Liên chốt 30/10

| Kiểu | Dùng ở đâu |
|---|---|
| **Toàn khung** | mặc định cho mọi cảnh. Cảnh chỉ có người thật để full, không chèn gì. Cảnh giao diện phần mềm cũng full, **không đè chữ, không khung viền** - ưu tiên nhìn rõ dữ liệu và chữ. |
| **Đặt góc** | chỉ cho nội dung dạng tổng hợp (ý 1 / ý 2, màn tổng kết) hoặc chỗ không cần màn hình rộng. Không bao giờ đặt lên cảnh dữ liệu. |
| **Nền mờ** | chỉ màn mở đầu, và **phải mờ nhẹ để nhìn rõ mặt người**. Lớp phủ chỉ đậm ở dải chữ rồi buông nhanh; từ 70% khung trở ra gần như để nguyên ảnh gốc. Tối đều cả khung là Liên loại. |

**Mỗi cụm lấy b-roll MỚI, không dùng lại đoạn của cụm trước.** NAS Viindoo có nhiều thư mục
quay thô (`/Marketing/Video/Văn phòng Viindoo`, `/Marketing/Video/Họp khối ...`,
`/Marketing/Video/Doanh nghiệp/...`, `/Marketing/03. Sự kiện/...`). **Ưu tiên tệp quay thô** -
các bản dựng sẵn như Storytelling có **phụ đề tiếng Anh cháy vào hình**, phải cắt dải dưới rồi
phóng lại mới dùng được.

Đoạn đã cắt để ở `$VIINDOO_VIDEO_WORKDIR/broll/<cụm>/`, 1920x1080 60fps, **bỏ tiếng**. Đừng đưa
vào git hay thư mục tài liệu dùng chung - ở đó không giữ tệp video nặng. Lệnh cắt:

```bash
ffmpeg -ss <giây bắt đầu> -t <độ dài> -i <tệp gốc> -an \
  -vf "scale=1920:1080:flags=lanczos,fps=60,format=yuv420p" \
  -c:v libx264 -preset slow -crf 18 <đích>.mp4
```

**Vào NAS bằng DSM API, không gắn ổ.** `viindoo.synology.me` mở cổng 5000 (giao diện web DSM)
nhưng **SMB 445 đóng**, không gắn ổ từ máy được. Dùng `SYNO.API.Auth` lấy `sid` rồi
`SYNO.FileStation.List` / `.Search` / `.Download`; tài khoản truyền qua biến môi trường, không
ghi vào tệp. Tệp gốc tải về để riêng (`$VIINDOO_VIDEO_WORKDIR/broll/goc/`), chỉ đoạn đã
cắt mới vào dây chuyền.

**Chọn hình:** ưu tiên cảnh **nhiều người** - họp quanh bàn, dãy bàn làm việc song song, đội thi
công. Tránh cảnh một người ngồi gõ máy một mình giữa khung trống. Người mặc chỉnh tề, không lộ
tên khách hàng thật trên màn hình hay giấy tờ trong khung. **Bỏ đoạn nào quay màn hình Viindoo
phiên bản cũ** - đặt cạnh màn bản đang bán trong cùng clip là lệch.

**Màn mở đầu dùng chính một khung của b-roll làm nền** thì lấy khung có người dồn về phía đối
diện với khối chữ, và để lớp phủ **mờ nhẹ**: chỉ đậm ở dải chữ rồi buông nhanh, từ ~70% khung trở
ra gần như nguyên ảnh gốc.

Mọi thứ gắn ngôn ngữ phải chọn theo `LANG`: đường dẫn ảnh, bảng nhãn thanh bước, bảng chữ trên cảnh.

## Bước 10 - Render và trộn tiếng

```bash
W="${VIINDOO_VIDEO_WORKDIR:-$HOME/viindoo-video}"
node "${CLAUDE_PLUGIN_ROOT}/engine/sequence.mjs" --seq "$W/motion/seq/seq-<cụm>-fw-en.json" \
  --segdir "$W/output/<cụm>-fw-en-seg" --no-concat --no-variants
# render lại vài cảnh: thêm --only 4,5,10
```

Rồi `CLIP_LANG=en bash clips/mix.sh` - nối cảnh, chèn b-roll, trộn lời đọc với nhạc nền, tự soát
đỉnh và độ to.

Nhạc nền lấy ở `$VIINDOO_VIDEO_WORKDIR/Nhac-nen/` (sinh bằng `music.py` của skill `viindoo-module-launch`, hoặc bản có giấy phép dùng thương mại), mỗi clip một bài riêng, để `volume=0.13`. Đặt tệp đã chọn vào biến `MUSIC` khi chạy `mix.sh`.

Chuỗi lọc tiếng đã chốt (đừng đổi nếu không đo lại):

```
[lời]volume=0.92,apad[v]; [v][nhạc]amix=normalize=0,volume=0.9dB,
aresample=96000,alimiter=limit=0.89:level=disabled,aresample=48000
```

Soát sau khi lắp: **đỉnh dưới 0 dB** và **độ to khớp bản ngôn ngữ kia** (clip HRM: -14,6 LUFS bản
Việt, -14,8 bản Anh).
