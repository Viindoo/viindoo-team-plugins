---
name: viindoo-motion-video
description: Dựng video motion-graphics brand Viindoo bằng mã, theo CHUẨN FORWARDER Liên chốt 19/10/2026 (clip mẫu "V61. Viindoo Freight Management") - nền trắng nhấn teal, màn phần mềm thật toàn khung (KHÔNG vẽ con trỏ giả), nỗi đau bằng NGƯỜI THẬT toàn khung (không hình vẽ người + vòng tròn công cụ), và kể dọc DÒNG CHẢY NGHIỆP VỤ của ngành với thanh bước chạy suốt. Bộ cảnh fwtitle/fwsteps/fwscreen/fwcta dựng sẵn đúng chuẩn; fwscreen tự làm tối màn, khoanh cyan vào con số, kéo số ra chữ to kèm một câu nghĩa. Dùng skill này bất cứ khi nào cần dựng video tổng thể hoặc video ngành, sơ đồ quy trình động, clip số liệu, khung nền để chèn màn hình demo, hoặc render cùng nội dung ra nhiều ngành/nhiều ngôn ngữ/nhiều tỉ lệ. KHÔNG dùng để: quay màn hình phần mềm thật (quay trên demo), DỰNG BIỂU ĐỒ VIINDOO THAY CHO VIỆC QUAY THẬT, sinh b-roll AI (Gemini), lồng tiếng/nhạc (engine TTS riêng), hay thiết kế tĩnh/social (Canva).
---

# Video motion-graphics brand Viindoo (Viindoo Motion)

> **Cổng nguyên tắc video (bắt buộc, soát trước mọi thứ).** TRƯỚC KHI dựng data/cảnh và TRƯỚC KHI xuất: đọc `${CLAUDE_PLUGIN_ROOT}/references/video-principles.md`, soát checklist A-E (kể chuyện · hình/hiệu ứng · thương hiệu · giọng-nhạc · quy trình-đăng) + bảng giọng theo loại video. Nguyên tắc này có TRƯỚC và THẮNG mọi mặc định generic của skill. Với skill này đặc biệt lưu: "Báo cáo = biểu đồ" (mục B), "Số phải sâu" (mục A), "Hiệu ứng chỉ phục vụ nội dung" (mục B).

Trao đổi bằng tiếng Việt. Kết quả: file MP4 brand Viindoo (cyan `#00BBCE` + tím `#7F4282`, font Montserrat/Roboto), đủ 3 tỉ lệ, lưu trong `$VIINDOO_VIDEO_WORKDIR/output/` (mặc định `~/viindoo-video/output/`). Màu/font lấy từ `${CLAUDE_PLUGIN_ROOT}/brand/brand-tokens.json` - KHÔNG bịa.

---

## CHUẨN FORWARDER (Liên chốt 19/10/2026) - bám cái này, đừng tự nghĩ kiểu khác

Clip mẫu: **"V61. Viindoo Freight Management"** (129s, 1920x1080, 60fps) - video giới thiệu giải pháp
Vận tải giao nhận (freight forwarder) của Viindoo. Tệp gốc nằm trong kho video marketing nội bộ;
chưa có link công khai, cần xem thì xin Liên.
Liên chốt đây là CHUẨN cho video ngành / video tổng thể. Mọi clip mới bám cả **cách nhìn** lẫn
**cách kể** của nó. Bộ cảnh `fw*` dưới đây dựng sẵn đúng chuẩn này - dùng chúng, đừng quay lại
kiểu nền tối ô bên phải cũ.

### Cách nhìn

| Hạng mục | Chuẩn |
|---|---|
| Nền | **Trắng**, lưới mờ rất nhạt, nhấn **teal gần như đơn sắc** (dùng `colors.primary`) |
| Màn phần mềm | **Toàn khung** có đổ bóng, hoặc lồng trong **laptop / điện thoại trong tay**. KHÔNG nhét vào ô nhỏ bên phải |
| Trạng thái màn | **Sống**: tooltip, chatter đang đổi giá trị. Ảnh tĩnh phóng dần đã bị chê |
| Con trỏ chuột | **KHÔNG tự vẽ con trỏ giả** (Liên 19/10: "chuột là chuột thật hay mày tạo ảnh chuột thì bỏ"). Playwright quay video **cũng không ra con trỏ** - Chrome không vẽ con trỏ vào khung. Muốn có chuột thật thì phải người ngồi ghi màn hình. Không có chuột thật thì bỏ hẳn, đừng vẽ |
| Lớp người | **Hình vẽ phẳng** mang cảm xúc (nhân viên ngập việc, bàn tay cầm điện thoại) |
| Chữ | **Rất ít**. Nhãn in hoa ngắn; hình và màn hình mang nội dung, không phải đoạn văn |
| Tốc độ khung | **60 fps** (đã đặt làm mặc định) |

### Cách kể - DÒNG CHẢY NGHIỆP VỤ

Đây là điểm cốt lõi, không phải phần nhìn. Clip chuẩn **không đi theo tính năng, không đi theo
luận điểm** - nó **đi dọc dòng chảy nghiệp vụ của ngành từ đầu đến cuối**, và luôn cho người xem
biết đang đứng ở đâu trong dòng chảy đó.

Khuôn 8 nhịp của clip mẫu:

1. **Nỗi đau bằng NGƯỜI THẬT** - đoạn phim người thật toàn khung (người đang bị ngập việc), lớp chữ chỉ
   một nhãn + một dòng phụ, dải tối nhẹ ở phía chữ rồi buông nhanh, nhìn rõ mặt người. Mẫu:
   `templates/clips/dung_noi_dau.py` + `noi_dau_chu.html` của skill `viindoo-video-cum-nghiep-vu`.
2. **(BỎ) Công cụ rời rạc bủa vây** - KHÔNG còn dùng hình vẽ người + vòng tròn công cụ (`fwpain` +
   `orbit`). Liên 09/11/2026: "xấu quá, trình bày khác đi, bỏ hết cả ở các clip sau". Muốn nói công cụ
   rời rạc thì để lời đọc nói, hình vẫn là người thật.
3. **Thẻ tên sản phẩm** - icon + tên sản phẩm + phụ đề tiếng Việt (`fwtitle`)
4. **Nhãn ngành + nền tảng** - tên đối tượng in hoa + laptop đặt trên bệ teal (`fwtitle` + `shot`)
5. **Sơ đồ toàn quy trình hiện dần** - icon + mũi tên, từng bước một (`fwsteps`)
6. **Đi từng bước nghiệp vụ** - mỗi bước MỘT cảnh: thanh bước trên đầu sáng đúng bước đang nói,
   màn Viindoo thật ở giữa, khoanh cả hàng/cả cột/cả bảng kèm con số, kéo số ra (`fwscreen`)
7. **Góc khách hàng** - màn tra cứu trên điện thoại trong tay vẽ phẳng
8. **Kết** - logo + địa chỉ web + nút kêu gọi (`fwcta`)

**Thanh bước là xương sống.** Lấy đúng các bước nghiệp vụ thật của ngành (clip mẫu: Yêu cầu khách
hàng · Báo giá · Xác nhận đơn · Lô hàng · Booking · Tracking · Báo cáo & tổng hợp doanh thu chi phí),
truyền nguyên mảng đó vào MỌI cảnh `fwscreen`, chỉ đổi `active`. Người xem không bao giờ bị lạc.

**TỔNG THỂ TRƯỚC, VÍ DỤ CỤ THỂ SAU** (Liên 19/10/2026). Hai nhịp bắt buộc chen vào khuôn trên:

- **Trước dòng chảy: nêu MỤC ĐÍCH áp dụng phần mềm** - cảnh `fwtwo`, hai hoặc ba trụ cột trả lời
  "dùng cái này để làm gì". Với HRM là Quản (nối con người với tiền và vận hành) và Xây (dựng
  hành trình phát triển từng người). Không có nhịp này thì các màn hình phía sau chỉ là trình diễn
  tính năng rời rạc.
- **Mỗi ví dụ phải CHỨNG MINH một mục đích** - đặt `goal: "Chứng minh: Quản"` trên cảnh `fwscreen`
  để hiện nhãn, và lời đọc mở bằng "Sang phần quản" / "Quay lại phần xây".
- **Kết phải có TỔNG KẾT + KHÁC BIỆT**, không dừng ở màn kêu gọi. Thêm một cảnh `fwtwo` so sánh
  "phần mềm lẻ" với "Viindoo": phần mềm lẻ làm được tới đâu rồi tắc ở đâu, Viindoo khác chỗ nào.
  Kết cụt lủn là lỗi (Liên 19/10).

- **Trước phần kết: CHO THẤY bức tranh tổng thể** - cảnh `fwapps`, icon các app Viindoo bay vào
  tụ quanh logo. Nói "nằm trên một hệ thống" mà không cho thấy hệ thống đó là nói suông
  (Liên 19/10). Icon phải là **icon thật của module**, tải từ `static/description/icon.png` trên
  chính instance (`curl $BASE/<module>/static/description/icon.png`), không vẽ lại.
- **Cảnh tổng kết khác biệt: XẾP ICON THEO ĐÚNG CÁC TIÊU CHÍ đã nêu ở đầu** - dùng
  `pillars[].groups` của `fwtwo`, mỗi nhóm một nhãn (Quản / Xây). Bên "phần mềm lẻ" để vài icon
  `muted: true` (xám) cho thấy nó dừng ở đâu. Chỉ đổ một dãy icon không phân loại là chưa đạt.

Khuôn đầy đủ sau khi chen các nhịp: nỗi đau -> thẻ tên sản phẩm -> **hai mục đích** -> dòng chảy
-> các ví dụ (mỗi ví dụ gắn nhãn chứng minh) -> **bức tranh tổng thể** -> **tổng kết khác biệt
(icon phân theo tiêu chí)** -> kêu gọi.

### Cách diễn đạt

- **Nỗi đau trước, phần mềm sau.** Mở bằng cảnh người khốn khổ mà khách chưa dùng phần mềm cũng
  thấy mình trong đó. Không mở bằng tính năng.
- **Một cảnh một bước, một bước một con số.** Mỗi cảnh màn hình chốt bằng đúng MỘT con số kéo ra
  chữ to kèm một câu nó nghĩa là gì - không rải nhiều số.
- **Chữ trên màn là nhãn, không phải câu.** Lời giải thích để cho giọng đọc; màn hình chỉ giữ
  nhãn bước, con số và một dòng nghĩa.
- **Kết dẫn tới bán hàng** - đặt demo / trải nghiệm / liên hệ, không dẫn sang blog.

### Chụp màn cho chuẩn này

- **Khung CSS 1280x720 + `device_scale_factor=1.5`** -> ảnh ra vẫn 1920x1080 nhưng **chữ Odoo to
  gấp 1,5 lần**. Chụp thẳng 1920x1080 thì chữ bé không đọc nổi khi thu vào khung (Liên 19/10:
  "màn hình giao diện quá bé, chữ không rõ"). `shotSize` khai **1280x720**, `focus`/`cursor` lấy
  luôn toạ độ CSS từ `getBoundingClientRect`.
- Hàng nằm dưới tầm nhìn (khung chỉ cao 720) thì **cuộn tới chính phần tử đích** bằng
  `scrollIntoView` - đặt `scrollTop` cho container Odoo không ăn.
- **KHOANH CẢ KHOẢNG, KHÔNG KHOANH MẨU** (Liên 19/10): khoanh **trọn dòng** của bảng, **trọn cột**
  của biểu đồ, và vùng khoanh phải **chứa con số**. Khoanh mỗi cái chỏm cột thì người xem không
  hình dung được tổng quan. Cột biểu đồ là canvas nên không đo bằng DOM được -> dò pixel theo màu
  cyan để lấy đúng bao của cột.
- Engine **tự nhúng ảnh thành data URI** (khoá `shot` / `image` / `icon` trong `data`), nên làm tối,
  khoanh vòng, kéo số ra đều bằng CSS/GSAP - KHÔNG overlay bằng ffmpeg nữa.
- `zoom: {x,y,w,h}` (toạ độ ảnh gốc) để phóng vào đúng vùng cần xem khi màn quá rộng;
  `focus`/`cursor` vẫn khai theo ảnh gốc, cảnh tự quy đổi.
- **Màn quá rộng thì KÉO MÁY QUAY, đừng thu nhỏ** (Liên 19/10/2026: "quay nhé đừng chụp - kéo từ trái sang phải rồi zoom tổng thể"). Kanban 6 cột nhét vào khung thì chữ bé; thay vào đó đưa `pan: [{x,y,w,h}, ...]` cho `fwscreen`: mở ở cột đầu (chữ to, đọc được), lướt sang cột cuối, rồi lùi ra thấy trọn. Các khung ngắm phải CÙNG TỈ LỆ, khung cuối là khung dừng lại - vòng khoanh và phần kéo số ra tự đợi máy quay dừng. **Thời lượng cảnh không đổi**, nên không phải thu lại lời.
- **Màn số liệu tổng quát: BIỂU ĐỒ, không danh sách, không pivot** (Liên 19/10/2026 - xem mục
  "Báo cáo = biểu đồ" trong SSOT). Danh sách Odoo nhiều cột hay cắt tiền thành `1.077.827.27…`
  và hàng tổng rơi khỏi khung 720px; pivot thì đủ số nhưng vẫn là bảng. Cách làm: lưu một
  `ir.filters` với `graph_mode` + `graph_measure` + `graph_groupbys` (ưu tiên gộp **theo thời
  gian** để thấy xu hướng) rồi chụp `?view_type=graph`; con số chính xác để phần **kéo số ra**
  của `fwscreen` lo, không trông vào nhãn trên cột. Action thiếu chế độ `graph` thì thêm vào
  `view_mode` của action (ghi lại giá trị cũ để trả lại) - Odoo tự sinh biểu đồ mặc định.
- **Danh sách gom nhóm, THU GỌN HẾT** là cách gọn nhất để lên hình một cái phễu: mỗi bước một
  hàng kèm số lượng (ví dụ phễu tuyển dụng 71 -> 55 -> 33 -> 20 -> 11 -> 13). Kanban chỉ lọt
  3,5 cột trong khung 1280.
- **Mở app menu trước khi vào action lẻ.** Vào thẳng `/odoo/action-1441`, Odoo lấy app của lần
  truy cập trước nên thanh menu trên cùng ra sai tên app (ví dụ "Thảo luận"). Ghé
  `/odoo/action-<action của app>` trước rồi mới mở action cần chụp.

### Thời lượng từng cảnh: ĐO TỪ FILE TIẾNG, đừng gõ tay

Mỗi cảnh ứng với một đoạn lời đọc. Chia tổng thời lượng tiếng theo **tỉ lệ âm tiết** từng đoạn
để ra ranh giới tạm, rồi **nắn mỗi ranh giới về giữa khoảng lặng thật gần nhất** (ffmpeg
`silencedetect=n=-34dB:d=0.28`, chỉ nắn khi lệch <= 1,6s). Thêm hay bớt một cảnh thì chạy lại
script, không phải tính tay cả bài. Mẫu: `templates/clips/build_seq.py` của skill `viindoo-video-cum-nghiep-vu`.

Cảnh nào nhận b-roll người thật thì **render ngắn đi đúng bằng độ dài b-roll** - b-roll chèn vào
trước cảnh đó, tổng thời lượng và lời đọc không đổi nên không phải thu lại tiếng.

### Nhạc nền

Kho nhạc: `$VIINDOO_VIDEO_WORKDIR/Nhac-nen/` kèm `index.json` ghi style, bpm và **clip nào
đã dùng bản nào, vì sao** (sinh và quản lý bằng `music.py` của skill `viindoo-module-launch`). Chọn theo nội dung, ghi lại lượt dùng mới vào `index.json`.
Mức nhạc để rất thấp (~0.13) cho lời đọc nổi lên; nhạc ngắn hơn clip thì cho lặp rồi cắt đúng độ
dài, fade vào 2 giây, fade ra 3 giây. Engine KHÔNG làm tiếng - trộn bằng FFmpeg ở bước cuối.

## Engine

Lõi nằm trong plugin ở `${CLAUDE_PLUGIN_ROOT}/engine/` (chỉ đọc). Mọi thứ ghi ra nằm trong thư mục
làm việc `$VIINDOO_VIDEO_WORKDIR` (mặc định `~/viindoo-video`):

- `engine/src/scenes/<ten>.js` - từng loại cảnh. Thêm cảnh = thêm 1 file ở đây (sửa trong repo plugin rồi gửi PR).
- `engine/src/brand.js` - đọc màu/font từ `${CLAUDE_PLUGIN_ROOT}/brand/brand-tokens.json` và **logo gốc** từ `brand/assets/logo-color.svg`, có fallback khi không đọc được (log `brand=` cho biết đang dùng nguồn nào). Đè đường dẫn bằng `BRAND_TOKENS` / `BRAND_LOGO`.
- `engine/src/template.html` - khung sân khấu (`#stage`) mà mọi cảnh vẽ vào.
- `engine/src/env.js` - đường dẫn: thư mục làm việc, thư viện, Chrome, thư mục tạm.
- `engine/samples/seq-mau.json` - kịch bản mẫu 5 cảnh (23 giây, số minh hoạ) để thử máy.
- Dữ liệu của bạn để ở thư mục làm việc: `$VIINDOO_VIDEO_WORKDIR/motion/data-<ngành>.json` (một cảnh lẻ), `$VIINDOO_VIDEO_WORKDIR/motion/seq/seq-<ngành>.json` (video nhiều cảnh).
- `render.mjs` / `sequence.mjs` / `frameshot.mjs` - ba lối vào, xem dưới. Đường dẫn tương đối trên dòng lệnh tính từ thư mục đang đứng; `--out` bỏ trống thì ra `$VIINDOO_VIDEO_WORKDIR/output/`.

Bộ render: GSAP (animation) + Chrome headless qua puppeteer-core (chụp từng khung) + FFmpeg (xuất).
Cài thư viện một lần: `bash "${CLAUDE_PLUGIN_ROOT}/engine/setup.sh"` (cài vào `$VIINDOO_VIDEO_WORKDIR/.engine-deps`, không cài vào thư mục plugin).
Chrome lấy từ `CHROME_PATH`, mặc định Google Chrome / Chrome for Testing / Chromium ở vị trí cài chuẩn.

## Ba lối vào

### 1. `sequence.mjs` - video nhiều cảnh (lối vào chính CỦA ENGINE NÀY)

```bash
E="${CLAUDE_PLUGIN_ROOT}/engine"; W="${VIINDOO_VIDEO_WORKDIR:-$HOME/viindoo-video}"
node "$E/sequence.mjs" --seq "$E/samples/seq-mau.json"                       # thử máy
node "$E/sequence.mjs" --seq "$W/motion/seq/seq-<ngành>.json" --out "$W/output/<ngành>.mp4"
```

Kịch bản `seq-*.json`:

```jsonc
{ "title": "...", "width": 1920, "height": 1080, "fps": 30,
  "scenes": [ {"scene": "statement", "data": {...}, "duration": 12}, ... ] }
```

`duration` (giây) quyết định độ dài cảnh; dài hơn timeline thì khung cuối tự giữ.
Mỗi cảnh render thành 1 segment rồi `ffmpeg concat -c copy` nối lại, sau đó sinh bản 9:16 và 1:1.

Cờ hữu ích:
- `--only 3,7` - CHỈ render cảnh số 3 và 7 (đếm từ 0). Sửa một cảnh thì dùng cái này, khỏi render lại cả bài.
- `--segdir <thư-mục>` - giữ lại từng segment để soi/ghép tay.
- `--no-concat` - chỉ xuất segment, không nối (lúc này KHÔNG sinh bản dọc/vuông).
- `--no-variants` - chỉ bản 16:9. Thêm `--width --height --fps` để đè giá trị trong seq.

### 2. `render.mjs` - một cảnh lẻ

```bash
node "$E/render.mjs" --scene kpi --data "$W/motion/data-kpi.json" --out "$W/output/kpi.mp4"
```

Cờ: `--width --height --fps --duration --no-variants`. Mặc định xuất 3 file: `<ten>.mp4` (16:9), `<ten>-9x16.mp4`, `<ten>-1x1.mp4`.

### 3. `frameshot.mjs` - chụp 1 khung TĨNH ra PNG

```bash
node "$E/frameshot.mjs" --scene demoframe2 --data "$W/motion/data-x.json" --out "$W/output/nen.png"
```

Chụp trạng thái CUỐI của cảnh. Dùng để lấy ảnh nền `demoframe`/`demoframe2` rồi FFmpeg overlay clip quay màn hình demo thật vào ô trống bên phải - đây là cách trộn đồ hoạ với màn hình thật.

## Bảng cảnh có sẵn (7)

Hợp đồng chung: `window.SCENES[ten](stage, data, brand, gsap) -> gsap.timeline (paused)`.

| Cảnh | Dùng để | `data` |
|---|---|---|
| `statement` | câu khẳng định lớn + ý phụ (mở bài, chuyển đoạn) | `{kicker?, tag?, headline, sub?, points?:[string], accent?:'primary'\|'secondary'}` |
| `flow` | sơ đồ dòng chảy N ô nối bằng mũi tên (quy trình) | `{kicker?, tag?, headline, steps:[{label, note?}], caption?}` |
| `kpi` | thẻ chỉ số đếm lên + biểu đồ cột mọc dần | `{title, subtitle, metrics:[{label,value,prefix?,suffix?,decimals?}], bars:[{label,value}]}` |
| `ai` | hỏi số liệu bằng giọng nói (Viindoo AI), có nhãn "Hình minh hoạ" | `{kicker?, question, answerRows:[{k,v}], note?}` |
| `cta` | màn kết, mời đặt demo, logo Viindoo lớn | `{headline, sub?, button?, closing?}` |
| `demoframe` | nền 16:9 + cột chữ trái, chừa ô VUÔNG bên phải cho clip demo | `{kicker?, tag?, headline, sub?}` |
| `demoframe2` | như trên nhưng chữ gọn, ô demo TO gần full chiều cao | `{kicker?, tag?, headline, sub?}` |

### Bộ cảnh CHUẨN FORWARDER (dùng bộ này cho clip mới)

Tất cả dùng chung `engine/src/scenes/_fw.js` (nền trắng + lưới, logo gốc, thanh bước, con trỏ, khung
laptop, nhấn số) - engine tự nạp trước mọi cảnh, không cần khai báo.

| Cảnh | Dùng để | `data` |
|---|---|---|
| `fw3dkho` (và các cảnh `fw3d*`) | **Mô phỏng IoT / thiết bị / tích hợp riêng bằng 3D theo brand** (Liên 09/11/2026 - mặc định cho mọi clip từ giờ): three.js (nạp offline từ `engine/vendor/`) tự nạp cho cảnh tên `fw3d*`, isometric trắng + teal, quang cảnh xưởng/kho, người vận hành cầm máy tính bảng hiện Viindoo, số chạy đồng bộ về màn Viindoo, nhãn "Mô phỏng - tích hợp theo thiết kế riêng" | xem đầu tệp `engine/src/scenes/fw3dkho.js` |
| `fwpain` | **KHÔNG DÙNG cho clip mới** (Liên 09/11/2026 bỏ hình vẽ người + vòng tròn công cụ); chỉ giữ để dựng lại clip cũ. Cảnh nỗi đau = người thật toàn khung + nhãn chữ | `{label?, image?, orbit?:[{text?,icon?}], sub?}` |
| `fwtitle` | thẻ tên sản phẩm; có `shot` thì thành nhãn ngành + laptop trên bệ teal | `{icon?, name, sub?, audience?, shot?, shotSize?}` |
| `fwtwo` | **mục đích áp dụng** (đặt trước dòng chảy) hoặc **tổng kết so sánh** (đặt trước CTA) | `{kicker?, headline?, pillars:[{tag,title,note?,icon?, icons?:[{icon,label}], groups?:[{label?,muted?,icons:[...]}]}], sub?}` |
| `fwapps` | **bức tranh tổng thể**: icon các app Viindoo bay vào tụ quanh logo | `{kicker?, headline?, sub?, apps:[{icon,label}], highlight?}` |
| `fwsteps` | sơ đồ toàn dòng chảy nghiệp vụ, hiện dần từng bước | `{kicker?, headline?, steps:[{label,note?,icon?}], reveal?}` |
| `fwscreen` | **cảnh xương sống**: thanh bước + màn thật + khoanh/kéo số ra (`zoom` phóng vào vùng cần xem; `pan`+`panDur` KÉO MÁY QUAY qua nhiều khung ngắm) | `{steps?, active?, shot, shotSize?, device?:'full'\|'laptop', focus?{x,y,w,h}, number?, meaning?, cursor?{x,y}, caption?}` |
| `fwcta` | màn kết: logo gốc + địa chỉ web + nút kêu gọi | `{url?, button?, sub?}` |

`focus` và `cursor` lấy **toạ độ trên ảnh gốc**; engine tự quy đổi theo tỉ lệ ảnh đã thu nhỏ.
Mẫu chạy được: `engine/samples/seq-mau.json`. Ngoài bảng trên còn các biến thể khổ dọc/vuông và cảnh phụ (`fwscreenv`, `fwscreens`, `fwcardv`, `fwwrapv`, `fwcards`, `fwcycle`) - hợp đồng `data` ghi ở đầu từng tệp.

Thêm cảnh mới = thêm file trong `engine/src/scenes/` theo đúng hợp đồng trên, rồi đăng ký vào `window.SCENES`. Sửa engine thì sửa trong repo plugin và gửi PR, đừng sửa bản cài trong bộ nhớ đệm plugin (bị ghi đè khi cập nhật).

## Bản mẫu đã chạy thật

Video tổng thể ngành máy tính-máy chủ (bản v2, trước chuẩn forwarder): **13 cảnh, 117 giây**, thứ tự `statement -> flow x4 -> kpi x2 -> flow -> kpi -> flow -> kpi -> ai -> cta`. Kịch bản seq của các video đã làm không đóng gói trong plugin (chứa dữ liệu dự án); cần thì xin Liên. Clip mới theo chuẩn forwarder thì dựng từ `engine/samples/seq-mau.json` và khuôn 8 nhịp ở trên.

## Nhân bản theo ngành / ngôn ngữ (đòn bẩy chính)

KHÔNG dựng tay từng bản. Mỗi phiên bản = 1 file dữ liệu riêng, dùng lại nguyên bộ cảnh:

1. Copy `$W/motion/seq/seq-<ngành>.json` thành `seq-<ngành-mới>.json` (hoặc `-en.json`), đổi phần chữ và số trong `data` từng cảnh.
2. Render: `node "$E/sequence.mjs" --seq "$W/motion/seq/seq-<ngành-mới>.json" --out "$W/output/<ngành-mới>.mp4"`.
3. Số liệu phải là **số thật của khách** khi dùng cho khách; bản mẫu ghi rõ "số minh hoạ".

## Ranh giới (nói thẳng, khỏi kỳ vọng sai)

- **LUẬT LIÊN - đọc trước khi dựng bất kỳ biểu đồ nào:** số liệu và biểu đồ **CỦA VIINDOO phải QUAY THẬT từ phần mềm, KHÔNG BỊA**. Biểu đồ motion-graphics dựng bằng skill này chỉ là **lớp phụ**, dùng khi không quay được; và số trong đó **cũng phải là số thật lấy từ demo**. Chi tiết + bẫy quay: mục B của `references/video-principles.md`.
- Engine này là **MỘT LỚP** trong pipeline video, **không phải cả video**. Pipeline tổng (đối tượng -> dữ liệu demo -> quay -> lời -> TTS -> mốc cảnh -> render -> trộn tiếng -> đăng) nằm ở skill `viindoo-video-cum-nghiep-vu`.
- Skill này dựng **trọn phần HÌNH** của chuỗi cảnh đồ hoạ. **Không có tiếng**: lồng tiếng vẫn engine TTS riêng, nhạc nền chọn riêng từng clip, ghép tiếng vào bằng FFmpeg ở bước sau.
- Màn hình phần mềm thật vẫn **quay trên instance demo**, không dựng bằng đồ hoạ. Cách trộn **mới**: đưa đường dẫn ảnh/clip vào `shot` của cảnh `fwscreen`, engine tự nhúng rồi làm tối + khoanh + kéo số ra. Cách cũ (`frameshot.mjs` lấy nền `demoframe2` rồi overlay bằng ffmpeg vào ô phải) chỉ còn dùng cho clip cũ.
- **Lớp màn hình phần mềm phải nhấn vào CON SỐ, không nhấn thao tác** (Liên 18/10/2026): ảnh giao diện tĩnh phóng dần bị chê tẻ nhạt. Mỗi cảnh chọn đúng MỘT con số khách muốn thấy -> khoanh vào con số + làm tối xung quanh + kéo số ra chữ to kèm một câu nó nghĩa là gì. (Luật con trỏ ĐÃ ĐỔI 19/10: không vẽ con trỏ giả - xem bảng chuẩn forwarder ở trên.) Mượn kỹ thuật `ring`/`tap`/`flash`/`boxes` của bộ quay clip hướng dẫn Docs nhưng **KHÔNG bê cấu trúc "mỗi cảnh một bước thao tác"** của Docs - video tổng thể kể kết quả, không dạy cách làm. Đổi màu đánh dấu sang cyan, quay đúng 1920x1080. Chi tiết + lý do: mục B của `references/video-principles.md`.
- B-roll AI vẫn sinh bằng Gemini, theo quy tắc cảnh quay AI trong SSOT nguyên tắc video.
- Bản dọc/vuông hiện là **letterbox nền trắng** từ bản 16:9. Muốn bố cục dọc riêng (chữ to, xếp dọc) thì dùng các cảnh dọc/vuông chuyên biệt (`fwscreenv`, `fwscreens`, `fwcardv`, `fwwrapv`) hoặc thêm cảnh mới.

## Quy ước

- Chỉ dùng dấu gạch ngang ASCII `-`. Không chữ "Odoo" trong nội dung ra mắt/khách - gọi "Viindoo".
- **Logo:** mọi cảnh dùng **logo gốc** `${CLAUDE_PLUGIN_ROOT}/brand/assets/logo-color.svg`, nạp sẵn bởi `brand.js` và đưa vào cảnh qua `brand.logo.svg`. Trong cảnh gọi `logo(<chiều-cao-px>)`; hàm này ép chiều cao, giữ tỉ lệ (850x201). Cảnh nền tối (`demoframe`, `demoframe2`) đặt logo trên **thẻ trắng bo góc** theo mục C của SSOT. Chỉ khi KHÔNG đọc được file thì mới rơi về gõ chữ bằng font - thêm cảnh mới thì theo đúng khuôn này, đừng gõ chữ "Viindoo" bằng tay.
- **Video xuất TRƯỚC 18/10/2026 mang logo chữ gõ cũ. Liên chốt KHÔNG render lại** - thấy bản cũ logo khác thì đó là cố ý, đừng coi là lỗi và đừng tự dựng lại.
- **Số phải sâu:** mỗi cảnh `kpi` phải trả lời một câu hỏi quản trị - số là gì, đọc ra sao (tăng/giảm, so với cái gì), dẫn tới quyết định nào. Ít số mà sâu hơn nhiều số mà lướt.
- Font Montserrat/Roboto tải qua Google Fonts lúc render (cần mạng). Không mạng -> rơi về Helvetica/Arial.
- Render chậm vì chụp từng khung: 117 giây @30fps = hơn 3500 khung. Sửa một cảnh thì dùng `--only`, đừng render lại cả bài.
