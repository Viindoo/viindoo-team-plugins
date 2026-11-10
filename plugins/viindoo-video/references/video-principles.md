# Video Principles - SSOT nguyên tắc làm video Viindoo

> Nguồn sự thật duy nhất cho MỌI video/clip Viindoo (video tổng thể, video ngành, video theo vai trò, clip ra mắt sản phẩm, clip hướng dẫn Docs, Reels/Shorts).
>
> Bất kỳ task làm video nào - dù chạy skill `viindoo-motion-video`, `viindoo-video-cum-nghiep-vu`, `viindoo-module-launch`, `odoo-demo-recording` hay script dựng riêng của từng clip - PHẢI đọc file này và tự soát checklist TRƯỚC KHI dựng kịch bản và TRƯỚC KHI xuất/đăng.
>
> Đây là bản gom các nguyên tắc Liên đã chốt (ghi kèm ngày chốt). Có nguyên tắc mới hoặc lệch thực tế thì sửa file này trong repo plugin và gửi PR, đừng sửa lẻ trong từng skill. Brand (màu/font/logo) là nguồn riêng: `${CLAUDE_PLUGIN_ROOT}/brand/brand-tokens.json` + `brand/assets/`.

---

## 0. Loại video quyết giọng và vài quy tắc

| Loại video | Giọng mặc định | Ghi chú |
|---|---|---|
| Clip RA MẮT sản phẩm/module | **Iapetus** (nam trẻ Hà Nội), model `gemini-3.1-flash-tts-preview`, nhịp nhanh dứt khoát - CỐ ĐỊNH | ghi đè quy tắc 5-giọng, chỉ cho clip ra mắt |
| Video ngành / video tổng thể | **Fenrir** ưu tiên thử trước (nam trẻ, sáng - Liên duyệt 19/10/2026), model `gemini-2.5-flash-preview-tts`; nhạc riêng từng clip. **Nhưng cao độ mới là thứ phải đạt**: Fenrir đọc bài nào ra dưới chuẩn thì đổi giọng cho bài đó, xem luật cao độ ở mục D | |
| Video theo vai trò | Bộ 5 giọng (nữ Despina/Sulafat/Leda, nam Algenib/Schedar), chọn theo vai trò | |
| Clip hướng dẫn Viindoo Docs | Iapetus, nhạc tin-cay | theo mẫu chuẩn |

Giọng/nhạc đã chốt riêng cho từng dự án ghi trong thư mục dự án đó - không đổi bảng này khi chưa hỏi người duyệt.

### 0b. CLIP NGÀNH khác CLIP CỤM NGHIỆP VỤ - đừng dựng lẫn (Liên 23/10/2026)

Hai loại này nhìn giống nhau (đều "clip tổng thể", đều dùng bộ cảnh `fw*`) nhưng kể khác nhau từ gốc:

| | **Clip NGÀNH** (cơ khí, lắp ráp, giao nhận, cho thuê) | **Clip CỤM nghiệp vụ / module** (HRM, kế toán, kho) |
|---|---|---|
| Người xem | Doanh nghiệp của đúng ngành đó | Người phụ trách chức năng, không gắn ngành |
| Mở bài | Nỗi đau ĐẶC THÙ của nghề, dùng chữ của nghề | MỤC ĐÍCH dùng cụm phần mềm (HRM: Quản / Xây) |
| Thanh bước chạy suốt | Các bước nghiệp vụ CỦA NGÀNH (cho thuê: báo giá -> đơn thuê -> giao máy -> trong kỳ -> thu hồi -> hoá đơn -> tài sản -> báo cáo) | Dòng chảy của chính cụm (HRM: tuyển dụng -> năng lực -> đào tạo -> chấm công -> lương -> đánh giá -> chi phí -> giá thành) |
| Dữ liệu demo | Phải là dữ liệu đúng ngành | Ngành nào cũng được, miễn số thật |
| Hay sai chỗ nào | Biến thành trình diễn module, mất giọng của nghề | Bị kéo về một ngành cụ thể, hẹp mất người xem |

Giống nhau ở: chuẩn hình (mục B), số phải sâu, tổng thể trước ví dụ sau, kết phải có bức tranh
tổng thể + khác biệt.

### 0c. Kịch bản viết TRƯỚC 19/10/2026 phải nâng lên chuẩn trước khi quay

Chuẩn forwarder và giọng Fenrir mới chốt 19/10/2026. Kịch bản ngành viết trước mốc đó (ví dụ
kịch bản ngành Cho thuê thiết bị ngày 16/10 - còn ghi "khuôn video lắp ráp", giọng Charon/Kore)
**giữ nguyên NỘI DUNG** (đã kiểm nguồn, đã bám nghiệp vụ) nhưng **phải đổi CÁCH DỰNG**:

- [ ] Bố cục: bộ cảnh `fw*` nền trắng nhấn teal, KHÔNG dùng khuôn cũ "tiêu đề trái + màn hình phải".
- [ ] Thêm **thanh bước nghiệp vụ chạy suốt** mọi cảnh màn hình - khuôn cũ không có.
- [ ] Thêm nhịp **hai mục đích** (`fwtwo`) trước dòng chảy, và **bức tranh tổng thể** (`fwapps`) +
      **tổng kết khác biệt** (`fwtwo`) trước CTA. Kết cụt lủn là lỗi.
- [ ] Giọng đổi sang **Fenrir**; bỏ chỉ định giọng cũ trong kịch bản.
- [ ] Màn phần mềm: khoanh vào CON SỐ, kéo số ra chữ to - khuôn cũ chỉ "zoom chậm vào kết quả".
- [ ] Thời lượng từng cảnh ĐO TỪ FILE TIẾNG, không giữ mốc giây gõ tay trong bảng cảnh cũ.

**Bài học gốc:** bản 1 video máy tính-máy chủ hỏng đúng vì làm ngược - quay màn hình trước rồi mới
nghĩ hình chính, nên mỗi cảnh thành một ảnh giao diện tĩnh ("nhàm, đơn điệu, dừng lâu chán"), hụt
46 giây và thiếu 7/13 hình chính. Quyết hình chính TRƯỚC, màn hình chỉ là cận cảnh chứng minh.

---

## A. Nội dung / Kể chuyện (quan trọng nhất - soát trước khi dựng hình)

- [ ] **Vấn đề -> Viindoo giải quyết -> lợi ích.** Mỗi cảnh nêu rõ (1) VẤN ĐỀ đặc thù cụ thể của khách (bám quy trình/pain thật, không chung chung), (2) VIINDOO GIẢI QUYẾT ra sao - cơ chế cụ thể, (3) lợi ích kinh doanh.
- [ ] **Kể kết quả, không dạy cách làm.** Mở bằng nỗi đau kinh doanh mà cả khách CHƯA dùng phần mềm cũng thấy (chậm báo giá, sót dòng, làm sai, máy chờ). KHÔNG quay từng bước cấu hình/thao tác (menu, mẫu nhập, chạy thử) kiểu hướng dẫn - lộ cách làm cho đối thủ. Phần mềm chỉ hiện ở màn kết quả.
- [ ] **Góc nhìn khách.** Zoom/nhấn vào thao tác mấu chốt, kể theo TRẢI NGHIỆM/TIỆN ÍCH khách ("chỉ vài cú click, báo giá đính kèm sẵn"), không tường thuật "mở menu X > click Y > điền Z".
- [ ] **Gần gũi người làm nghề.** Dùng chữ của ngành (bản vẽ, phôi, KCS, dòng chảy sản phẩm), không khoe tính năng kiểu bán công nghệ, không đọc tên menu. Trộn 3 lớp hình: giao diện thật + sơ đồ luồng + ảnh thật. Trục kể: mỗi bước/vai trò cần THÔNG TIN gì và Viindoo đưa tới ra sao.
- [ ] **CTA dẫn tới bán hàng.** Lời kêu gọi = đặt demo / liên hệ / để lại thông tin. KHÔNG dẫn người xem sang blog (blog là đầu phễu, đứng trước giai đoạn bán).
- [ ] **Video theo vai trò nhắm đúng kỳ vọng.** 3 tầng riêng: Lãnh đạo / Quản lý điều hành / Tác nghiệp; mỗi video mở bằng kỳ vọng của vai trò đó khi dùng phần mềm. Không làm video chung cho mọi đối tượng.
- [ ] **Số phải sâu.** Mỗi cảnh = một câu hỏi quản trị -> một con số trên màn hình thật -> cách đọc (tăng/giảm, so với gì) -> quyết định đi kèm. Ít số mà sâu hơn nhiều số mà lướt. Không "mở ra là thấy", "số tự chảy lên".
- [ ] **Tổng thể trước, ví dụ cụ thể sau** (Liên 19/10/2026). Nêu MỤC ĐÍCH áp dụng phần mềm (2-3 trụ cột) và DÒNG CHẢY NGHIỆP VỤ trọn vẹn TRƯỚC, rồi mới lấy từng màn hình thật ra chứng minh từng mục đích (gắn nhãn "Chứng minh: X"). Vào thẳng tính năng là trình diễn rời rạc.
- [ ] **Kết phải có BỨC TRANH TỔNG THỂ + KHÁC BIỆT** (Liên 19/10/2026). Không dừng ở màn kêu gọi. Nói "nằm trên một hệ thống" thì phải CHO THẤY hệ thống đó (icon các app Viindoo tụ lại, icon thật tải từ module). Cảnh tổng kết so sánh "phần mềm lẻ" với Viindoo, và **xếp icon theo đúng các tiêu chí đã nêu ở đầu** (ví dụ Quản / Xây), mỗi nhóm một nhãn. Kết cụt lủn là lỗi.
- [ ] **Video tổng thể: Viindoo là gốc, AI là phần thêm.** Phần lớn thời lượng dành cho giải pháp tổng thể Viindoo; AI chỉ là đoạn ngắn ở cuối, trước CTA.

---

## B. Hình ảnh / Hiệu ứng / Màn hình

- [ ] **Mô phỏng IoT / thiết bị / tích hợp theo thiết kế riêng = cảnh 3D theo brand Viindoo** (Liên 09/11/2026: "từ giờ những chỗ mô phỏng dạng IoT thế này cứ làm 3D nhé, theo brand của viindoo"). RFID, băng chuyền, PLC, cân, máy đo, hộp IoT... dựng 3D isometric bằng three.js (cảnh `fw3d*` của engine plugin, mẫu `engine/src/scenes/fw3dkho.js`): tông trắng + teal + tím theo brand-tokens, logo Viindoo, có quang cảnh xưởng/kho và người vận hành cầm máy tính bảng hiện giao diện Viindoo, số liệu chạy đồng bộ về màn Viindoo; luôn có nhãn "Mô phỏng - tích hợp theo thiết kế riêng" khi phần đó không có sẵn trong mã nguồn. Không dùng kho phim 3D có sẵn (không mang brand), không dùng hình vẽ phẳng.
- [ ] **Cảnh nỗi đau: người thật, KHÔNG hình vẽ** (Liên 09/11/2026). Bỏ hẳn kiểu hình vẽ người + vòng tròn công cụ quây quanh (`fwpain` + `orbit`): "xấu quá, trình bày khác đi, bỏ hết cả ở các clip sau". Cảnh nỗi đau dùng đoạn phim người thật toàn khung + một nhãn chữ + một dòng phụ, dải tối nhẹ phía chữ, nhìn rõ mặt người.

- [ ] **Hiệu ứng chỉ phục vụ nội dung.** Motion, khung, nhạc, chuyển cảnh KHÔNG được là điểm nhấn; không để hình đẹp che nội dung nông.
- [ ] **Màn hình phần mềm: nhấn vào CON SỐ, không nhấn thao tác.** Ảnh giao diện tĩnh phóng dần là tẻ nhạt. Mỗi cảnh chọn ĐÚNG MỘT con số khách muốn thấy -> khoanh vào con số + làm tối xung quanh + kéo số ra chữ to kèm một câu nó nghĩa là gì với việc kinh doanh. **KHÔNG tự vẽ con trỏ chuột giả** (Liên 19/10/2026: "chuột là chuột thật hay mày tạo ảnh chuột thì bỏ") - Chrome headless không vẽ con trỏ vào khung, muốn có chuột thật thì phải người ngồi ghi màn hình. Kỹ thuật mượn từ clip hướng dẫn Docs (`clip_rec.py`: `ring` / `tap` / `flash` / `boxes`) nhưng KHÔNG bê cấu trúc "mỗi cảnh một bước thao tác" của Docs - video tổng thể kể kết quả, không dạy cách làm; đổi màu đánh dấu sang cyan, quay đúng 1920x1080; biểu đồ canvas vẫn phải chụp tĩnh bằng chrome-devtools.
- [ ] **Khoanh CẢ KHOẢNG, không khoanh một mẩu** (Liên 19/10/2026). Vùng đánh dấu phải trùm **trọn hàng**, **trọn cột** hoặc **trọn bảng**, và phải **thấy con số**. Khoanh cái chỏm cột hay một ô bé thì người xem không hình dung được tổng quan. Toạ độ khoanh ĐO TRÊN DOM (`getBoundingClientRect`), không ước lượng bằng mắt; cột biểu đồ là canvas nên dò pixel theo màu.
- [ ] **Màn phần mềm phải TO và đọc được** (Liên 19/10/2026). Chụp khung CSS 1280x720 với `device_scale_factor=1.5` -> ảnh vẫn 1920x1080 nhưng chữ Odoo to gấp 1,5 lần; màn quá rộng thì phóng vào đúng vùng cần xem. Chụp thẳng 1920x1080 rồi thu vào khung là chữ bé không đọc nổi.
- [ ] **Số của MỘT NGƯỜI thì bảng, số của CẢ CÔNG TY thì biểu đồ** (Liên 19/10/2026). Báo cáo tổng quát (quỹ lương theo tháng, tiền tăng ca theo ngày) -> biểu đồ cột, thấy xu hướng. Còn số liệu của một nhân sự cụ thể (chấm công, phiếu lương, năng lực của anh A) thì **bảng pivot chuẩn hơn biểu đồ** - người xem cần đọc đúng con số của người đó, không cần xu hướng.
- [ ] **Báo cáo = biểu đồ.** Mọi màn số liệu tổng quát/báo cáo chụp dạng BIỂU ĐỒ (graph cột/đường/tròn, dashboard có chart), ưu tiên đồ thị THEO THỜI GIAN để thấy xu hướng; không bảng pivot/danh sách số. Màn nghiệp vụ ưu tiên trực quan: Gantt, kanban, sơ đồ truy xuất lô/sê-ri.
- [ ] **Biểu đồ Viindoo phải QUAY THẬT, không bịa.** Số liệu và biểu đồ CỦA VIINDOO phải lấy thật từ phần mềm. Biểu đồ motion-graphics tự dựng (skill `viindoo-motion-video`) chỉ là LỚP PHỤ, dùng khi không quay được; số trong đó cũng phải là số thật từ demo. Dữ liệu chưa đẹp thì được THÊM DỮ LIỆU / đổi khoảng thời gian trước khi quay (vẫn là bản ghi thật).
- [ ] **QUAY THẬT được, kể cả biểu đồ** (đo lại 29/10/2026 - LẬT luật cũ). Luật cũ ghi "biểu đồ Viindoo render bằng `<canvas>`, Playwright quay ra khung TRẮNG". Đo lại trên bản 18: quay bằng **Google Chrome thật trên máy** (`executable_path`, không dùng trình duyệt đóng gói của Playwright) thì biểu đồ hiện **đầy đủ** cột, trục, chú giải, và cả **chú thích khi rê chuột** kèm con số. Nên mặc định của mọi clip là **QUAY**, ảnh tĩnh + kéo máy quay chỉ là phương án dự phòng. Ba cái lợi: rê chuột lên cột là con số tự bật ra (hơn hẳn khoanh vòng lên ảnh); cảnh báo của phần mềm tự giải thích chính nó; và thay đổi trạng thái kể được bằng cách quay hai lượt trước/sau rồi cắt giữa. Bốn cái bẫy: cảnh báo "Mật khẩu đang là mặc định" (đăng nhập ở phiên riêng rồi lưu phiên, phiên quay không đăng nhập thì không có cảnh báo); Odoo bám sẵn bộ lọc mặc định (phải gỡ trước khi quay); khung bên phải có thanh cuộn riêng (đưa con trỏ vào trong khung rồi mới cuộn); cuộn phải chia nhiều nhịp nhỏ. Quay xong **luôn trích khung hình ra nhìn** - tệp chạy được không có nghĩa là quay đúng. Khuôn: `templates/clips/quay_fw.py` của skill `viindoo-video-cum-nghiep-vu`.
- [ ] **Clip hướng dẫn Docs: màn phần mềm PHỦ KÍN khung, mở bằng ẢNH BÌA, khoảng im tua nhanh hơn** (Liên 06/11/2026). Không khung cửa sổ giả thu nhỏ giữa nền trống; cảnh đầu là ảnh bìa (logo + tiêu đề trên màn thật); phần quay chạy tiếp sau khi lời đọc dứt tua 1,6 lần, phần có lời giữ tốc độ.
- [ ] **Chụp trên hệ thống thật.** Màn hình phần mềm chụp trên instance demo thật (ví dụ sanxuat18) bằng Playwright, không dùng ảnh static/description của module. Instance của khách thật -> che tên khách.
- [ ] **Chờ lâu thì mô phỏng.** Cảnh cần dữ liệu demo chưa có và phải chờ hàng giờ -> dựng ảnh mô phỏng theo giao diện thật, số liệu hợp lý nhất quán. Không đứng chờ, không ghi đè dữ liệu phiên khác.
- [ ] **KHÔNG còn bắt buộc gắn nhãn "Hình minh họa"** (Liên 24/10/2026). Luật cũ bắt gắn nhãn; nay bỏ. Đổi lại, **điều kiện để được mô phỏng chặt hơn**: tính năng đó phải CÓ THẬT và ĐANG BÁN ở một phiên bản nào đó, và từng chi tiết trên ảnh phải có cơ sở mã nguồn. Ví dụ đúng: cụm AI `installable=False` ở bản 18 và 19 nên không quay được, nhưng `viin_ai` đang bán trên Viindoo Apps cho bản 17 (199,90 EUR) - mô phỏng được. Ví dụ SAI: mô phỏng một tính năng chưa viết, hoặc đã gỡ khỏi sản phẩm.
- [ ] **Mô phỏng phải có cơ sở mã nguồn.** Mọi chi tiết ảnh mô phỏng (AI, duyệt...) phải có cơ sở trong thiết kế + mã nguồn Viindoo (đọc qua agent `viindoo-source-explorer`); mức duyệt luôn nói rõ do doanh nghiệp tự cấu hình.
- [ ] **Cảnh quay AI (Veo/Gemini):** lật ngang để dấu Gemini sang góc trái rồi đặt logo Viindoo đè (soát chữ bị ngược sau khi lật); tiêu đề chữ to đặt vào khoảng trống; cảnh AI chỉ làm hook 15-20s hoặc dưới 10% tổng thời lượng.
- [ ] **Ảnh xưởng chuyên nghiệp.** Xưởng rộng, nhiều máy/công đoạn, công nhân bảo hộ đầy đủ (mũ, kính, áo/găng); tránh góc hẹp, người mặc thường phục, logo công ty thật.
- [ ] **Clip SX/lắp ráp luôn có cảnh ghi nhận tại xưởng** bằng máy tính bảng (`viin_mrp_workorder`), nối lệnh SX -> ghi tại tổ/máy -> kho/giá thành/lãnh đạo, để dòng chảy thông suốt.
- [ ] **Mọi clip phải có lớp hình NGƯỜI THẬT.** Ba lớp hình bắt buộc trộn: giao diện thật + sơ đồ đồ hoạ + người thật. Clip toàn màn hình phần mềm là clip cứng. Liều lượng khoảng **5% tổng thời lượng** (clip ~170s thì ~8-9s, chia làm ba đoạn 2,5-3s).
- [ ] **B-roll người thật: mỗi clip lấy nguyên liệu MỚI, không dùng lại đoạn của clip trước.** Kho trên NAS `viindoo.synology.me` (DSM API cổng 5000, SMB 445 đóng): `/Marketing/Video/Văn phòng Viindoo`, `/Marketing/Video/Họp khối ...`, `/Marketing/Video/Doanh nghiệp/...`, `/Marketing/Video/Source Video sự kiện`, `/Marketing/03. Sự kiện/...`. **Ưu tiên tệp quay thô** - bản đã dựng (Storytelling) có **phụ đề tiếng Anh cháy vào hình**, phải cắt dải dưới rồi phóng lại (`crop=1600:900:160:0,scale=1920:1080`) mới dùng được.
- [ ] **Chọn hình: ưu tiên cảnh NHIỀU NGƯỜI.** Họp quanh bàn, dãy bàn làm việc song song, đội thi công. Tránh cảnh một người ngồi gõ máy một mình giữa khung trống - đó là hình của clip năng suất cá nhân, không phải clip quản trị. Người mặc chỉnh tề, bối cảnh gọn, **không lộ tên khách hàng thật** trên màn hình hay giấy tờ trong khung.
- [ ] **Không lấy cảnh quay màn hình phiên bản CŨ.** Đoạn b-roll có màn Viindoo giao diện đời trước đặt cạnh màn bản đang bán trong cùng clip là lệch - bỏ đoạn đó.
- [ ] **Ba kiểu đặt hình** (Liên 30/10/2026): **Toàn khung** là mặc định - cảnh chỉ có người thật để full không chèn gì, cảnh giao diện phần mềm cũng full **không đè chữ không khung viền**, ưu tiên nhìn rõ dữ liệu và chữ. **Đặt góc** (ảnh nhỏ một góc) chỉ cho nội dung dạng tổng hợp (ý 1 / ý 2, màn tổng kết) hoặc chỗ không cần màn hình rộng - không bao giờ đặt lên cảnh dữ liệu. **Nền mờ** (người thật làm nền, chữ đè lên) chỉ dùng ở màn mở đầu và **phải mờ NHẸ để nhìn rõ mặt người** - lớp phủ chỉ đậm ở dải chữ rồi buông nhanh, từ ~70% khung trở ra gần như để nguyên ảnh gốc; tối đều cả khung là Liên loại.
- [ ] **Kỹ thuật chèn: b-roll mượn ĐUÔI cảnh đứng trước**, cảnh đó render ngắn đi đúng bằng độ dài b-roll - nhờ vậy tổng thời lượng và lời đọc không đổi, không phải thu lại tiếng. Mượn đầu cảnh nó chen vào thì cảnh đó lên hình sớm hơn đoạn lời của chính nó. Đoạn cắt đưa về **1920x1080 60fps, BỎ TIẾNG**, để ở `$VIINDOO_VIDEO_WORKDIR/broll/<cụm>/`, không đưa vào git.
- [ ] **Phần AI thể hiện hỏi bằng giọng nói** (nút micro, dải sóng âm), không chỉ gõ.

---

## C. Thương hiệu (trỏ về Brand Assets SSOT)

- [ ] **Logo màu xanh + tím.** Dùng `${CLAUDE_PLUGIN_ROOT}/brand/assets/logo-color.svg` (Viin cyan `#00BBCE` + doo tím `#7F4282`) đặt trên nền trắng; nền tối/xanh thì đặt logo trên thẻ trắng bo góc. KHÔNG dùng `logo-inverted.svg` trừ khi người duyệt yêu cầu. Soát logo ở mở đầu, góc màn hình, màn kết trước khi xuất.
- [ ] **Màu/font lấy từ `${CLAUDE_PLUGIN_ROOT}/brand/brand-tokens.json`** - không bịa hex/font.
- [ ] **Nội dung ra mắt gọi "Viindoo", không "Odoo"** (lời đọc, chữ màn hình, tiêu đề, bài tin): "dùng được từ bản Viindoo 18".

---

## D. Giọng / Nhạc / Lồng tiếng

- [ ] **Một video một giọng, đọc cả bài một lượt.** Một giọng, một mô hình TTS, đọc liền mạch cả bài. Sai một chữ/đổi một câu -> đọc lại CẢ BÀI rồi cắt theo khoảng nghỉ; KHÔNG vá lẻ đoạn, KHÔNG dịch cao độ (asetrate) từng đoạn. Kiểm F0 cùng một lượt trước khi dựng.
- [ ] **CAO ĐỘ LÀ LUẬT CỨNG: lấy giọng SÁNG, không để trầm** (Liên 24/10/2026: *"lấy giọng sáng chứ ko để trầm, cao độ phải bằng HRM hoặc lên xuống ko đáng kể"*). Mức chuẩn là bản HRM tiếng Việt đã duyệt: **F0 137,1 Hz, dải 116,7 Hz** (đo bằng `voice_stats.py` trong khuôn `templates/clips/`). Ba điều cấm:
      1. **Không hạ sàn.** Cả loạt bản thu đều dưới sàn thì LOẠI cả loạt, thu lại hoặc đổi giọng - không được lập luận "sàn đo trên bài khác nên bỏ qua". Đúng lỗi này mắc ngày 24/10/2026 trên clip ngành Cho thuê.
      2. **Không lấy bản trầm vì nó đọc đúng chữ hơn.** Chất giọng đứng TRƯỚC số lỗi chữ: trầm và đều thì người nghe nhận ra ngay, còn sai một chữ lẻ thì đổi từ rồi thu lại được.
      3. **Không chọn giọng bằng đoạn mẫu ngắn.** Đọc một đoạn lẻ thì cao độ vọt lên 140-169 Hz; phải thu TRỌN BÀI cho từng giọng ứng viên rồi mới đo.
    Thu nhiều bản mà mức cao nhất vẫn thấp hơn chuẩn thì **đổi giọng trước**, kéo cao độ sau. Đo thật trên clip ngành Cho thuê (bài 143 giây, 12 bản trọn bài): Achird 129,0 - Fenrir 127,0 - Iapetus 120,0 - Sadachbia 113,2 - Puck 109,1 Hz. **Cùng một giọng đọc hai bài khác nhau ra cao độ khác nhau** - Fenrir đạt 137,1 Hz trên bài HRM nhưng chỉ 112-127 Hz trên bài Cho thuê, nên phải chọn lại giọng cho TỪNG bài chứ không mặc định dùng lại.
- [ ] **Kéo cao độ cả bài về mức chuẩn - được, nhưng là bước CUỐI** (dựng 24/10/2026). Đổi hết giọng mà bản sáng nhất vẫn thấp hơn chuẩn thì kéo TRỌN bản thu bằng `asetrate` rồi `atempo` kéo thời lượng về như cũ - đúng kỹ thuật bộ HRM đã dùng; chính bản HRM Liên duyệt cũng đi qua bước này (trước ghép 126,3 Hz, bản giao 137,1 Hz). Ba ràng buộc: kéo **cả bài một lần** với cùng một hệ số (kéo lẻ từng đoạn vẫn CẤM - xem luật một giọng một lượt ở trên); **giữ nguyên thời lượng** để không phải tính lại mốc cảnh; và **chép lời soát lại sau khi kéo** vì đổi cao độ có thể làm méo chữ. Công cụ: `chinh_cao_do.py` (đo trước bằng `can_cao_do.py`) trong khuôn `templates/clips/`.
- [ ] **Giọng TTS tiếng Việt KHÔNG ổn định - phải SOÁT bằng máy, không nghe may rủi** (Liên 19/10/2026: "dòng dự liệu", "nguồn gức", "bật đầu"). Cùng một bản viết, mỗi lần thu lại sai dấu ở một chữ khác và độ dài chênh tới 20 giây. Quy trình bắt buộc trước khi dựng: (1) cho Gemini **chép lại chính file tiếng** rồi so với bản viết - lệch chữ nào là đọc sai chữ đó; (2) hỏi thêm **có chủ đích từng từ rủi ro** (bản chép tự do hay tự sửa chính tả nên không bắt được lỗi sai dấu); (3) từ nào sai dấu thì **đổi sang từ khác** chứ đừng thu đi thu lại; (4) thu vài bản rồi lấy bản ít lỗi nhất. Công cụ: `check_tts.py`, `pick_take.py` trong khuôn `templates/clips/`.
- [ ] **Hình phải bám LỜI, không bám đồng hồ** (Liên 19/10/2026: "dòng chảy nhanh hơn giọng đọc", "giọng trễ hẳn so với hình từ giây 16"). Hai luật con: (1) cảnh hiện dần từng phần (sơ đồ bước, thẻ trụ cột) thì **mỗi phần chờ đúng lúc giọng gọi tên nó**, không dùng nhịp cố định; (2) b-roll chèn giữa hai cảnh phải **mượn thời lượng của cảnh ĐỨNG TRƯỚC**, không mượn đầu cảnh nó chen vào - mượn đầu thì cảnh đó lên hình sớm hơn đoạn lời của chính nó đúng bằng độ dài b-roll.
- [ ] **Cắt cảnh theo đoạn lời: ĐẾM NHỊP ÂM TIẾT, đừng chia đều và đừng tin khoảng lặng** (đo 19/10/2026). Tiếng Việt đơn âm nên mỗi âm tiết là một nhịp năng lượng; đếm nhịp thì biết giọng đã đọc tới chữ thứ mấy, rồi chỉ nắn nhẹ (<= 0,9s) vào khe lặng gần nhất. Đã thử và LOẠI hai cách khác: nắn theo khoảng lặng thì nghỉ giữa câu lẫn với nghỉ giữa đoạn (lệch 7-34 giây tuỳ ngưỡng); hỏi mô hình mốc thời gian thì nó trả cả mốc 245 giây cho file dài 169 giây.
- [ ] **Vá lẻ đoạn: CHỈ trong khe lặng, trọn một đoạn** (Liên hỏi 19/10). Luật "đọc cả bài một lượt" vẫn giữ; ngoại lệ duy nhất là thay TRỌN một đoạn của chính giọng đó rồi nối đúng giữa quãng lặng giữa hai đoạn, có đo nhịp và kéo khớp lại đúng độ dài khe cũ. Không ghép giữa câu, không trộn hai giọng. 
- [ ] **Giọng + nhạc theo loại video** (xem bảng mục 0). Nhạc nền chọn RIÊNG cho từng clip theo nội dung (được dùng lại bản cũ khi hợp, nhưng không mặc định chung). Bản VI và EN của một clip dùng chung giọng + nhạc.
- [ ] **Bẫy TTS:** cả bộ thu bằng MỘT mô hình (đổi mô hình là đổi chất giọng); "Viindoo" đọc "Vin đu" (phụ đề giữ "Viindoo"); viết tắt tiếng Anh đọc theo tiếng Anh (VGM = "Vi Zi Em"); giọng miền Bắc (không Edge TTS NamMinh).
- [ ] **Soát đỉnh tiếng phải đo ĐỈNH THẬT, không đo từng mẫu** (đo 20/10/2026, clip HRM bản Anh). Đo từng mẫu ra -0,74 dB (yên tâm) nhưng đỉnh thật giữa hai mẫu đã +2,05 dB, nén AAC xong file giao ra +1,24 dB - dễ rè ở chỗ to nhất. Hạ trần bộ chặn không cứu được vì bộ chặn còn chưa chạm tới. Cách đúng: **chặn đỉnh trên tần số lấy mẫu gấp bốn rồi hạ về** (`aresample=96000,alimiter=limit=0.89,aresample=48000`), rồi bù `volume` cho khớp độ to bản kia. Sau khi lắp phải tự soát hai số: **đỉnh dưới 0 dB** và **độ to khớp bản ngôn ngữ còn lại** (clip HRM: -14,6 LUFS bản Việt, -14,8 bản Anh).
- [ ] **Dựng bản ngôn ngữ thứ hai: soát LẠI TỪNG THỨ gắn ngôn ngữ, đừng tin là đã có** (đo 20/10/2026). Ba chỗ hay lọt, cả ba đều "chạy được" nên không báo lỗi: (1) **đường dẫn ảnh màn hình** - mã ghi cứng thư mục bản gốc thì bản mới nhúng nhầm ảnh giao diện ngôn ngữ cũ; (2) **nhãn chạy suốt clip** (thanh bước, chân trang) - bảng dịch có sẵn mà chỗ dùng vẫn gọi bảng gốc; (3) **dữ liệu trong màn hình** - dữ liệu demo tạo bằng ngôn ngữ nào thì mang tên ngôn ngữ đó, dịch được thì dịch, trường không dịch được (bậc kỹ năng, tên bộ lọc đã lưu, tên công ty) thì **đổi tên tạm để chụp rồi trả lại**, có tệp chép tên gốc. Soát bằng máy: quét kịch bản đã sinh tìm chữ của ngôn ngữ cũ, và trích vài khung hình ra xem trước khi render cả bài.
- [ ] **Dịch dữ liệu demo: ghi bản ngôn ngữ MỚI trước, rồi ghi đè lại bản cũ** (đo 20/10/2026, clip HRM bản Anh). Ngôn ngữ gốc của trường dịch được là en_US; ghi lại giá trị gốc thì Viindoo kéo theo mọi bản dịch đang TRÙNG giá trị gốc cũ - mà dữ liệu mình bơm thì bản dịch đúng bằng bản gốc. Ghi bản cũ trước cho "chắc" KHÔNG cứu được vì giá trị không đổi nên lượt ghi bị bỏ qua. Làm sai thứ tự một lần: 321 bản ghi mất sạch tên tiếng Việt. Trường nào dịch được thì **đọc `ir.model.fields.translate` của chính máy chủ**, đừng đoán theo mã nguồn. Script mẫu: `templates/demo-data/dich_en.py`.
- [ ] **Vùng khoanh phải ĐO LẠI trên ảnh mới, không bê từ bản ngôn ngữ kia** (đo 20/10/2026). Bảng sắp theo tên nên đổi ngôn ngữ là đổi thứ tự dòng: khung của bản Việt khoanh đúng hai dòng thiếu kỹ năng, bê sang bản Anh thì khoanh nhầm sang dòng đã đạt. Hàm dò phải gom theo **nội dung** (mọi dòng có 0 %) chứ không theo vị trí, và trước khi render thì **vẽ khung đè lên ảnh chụp** để mắt kiểm đúng chỗ.
- [ ] **Giọng duyệt ở ngôn ngữ này phải NGHE LẠI ở ngôn ngữ kia** (đo 20/10/2026, clip HRM). Cùng giọng Fenrir: đọc tiếng Việt 137,1 Hz (Liên khen), đọc tiếng Anh tụt còn 115,9 Hz (Liên loại: "trầm quá, gằn, có chữ nghe không rõ"). Ngược lại Achird ở tiếng Việt bị chê **quá sáng** 150,9 Hz mà đọc tiếng Anh chỉ 127,3 Hz. Cách chọn: thu **CẢ BÀI** cho từng giọng ứng viên rồi cắt cùng một đoạn đầu ghép lại cho người duyệt nghe liền mạch (cách làm: `references/giong-doc.md` của skill `viindoo-video-cum-nghiep-vu`) - KHÔNG thu đoạn mẫu ngắn, vì đọc riêng một đoạn thì cao độ vọt lên 140-169 Hz, nghe mẫu sẽ chọn nhầm. Bản tiếng Anh clip tổng thể: **Iapetus** (134,8 Hz).
- [ ] **Khung/thẻ trên cảnh không được đặt chiều cao cứng** (đo 20/10/2026). Nhãn tiếng Anh dài hơn tiếng Việt ("Business trips" xuống hai dòng) nên chữ **tràn ra ngoài khung trắng**. Sửa tận gốc: đo chiều cao thật của nội dung rồi kéo mọi thẻ cùng hàng cao bằng nhau, đừng cắt bớt chữ cho vừa khung.
- [ ] **Text free, voice trả phí.** Nội dung text (lời đăng, caption, blog, bình luận) soạn bằng Gemini web miễn phí; Gemini API trả phí CHỈ dùng cho voice/TTS.

---

## E. Quy trình sản xuất / Đăng tải

- [ ] **Duyệt kịch bản trước khi quay** (trừ khi người duyệt đã nói "không cần hỏi lại" cho đúng video đang làm).
- [ ] **Song ngữ: làm VI trước, duyệt rồi mới EN.** Khi người duyệt góp ý, chỉ sửa chỗ sai, không làm lại cả bài.
- [ ] **Tự làm trọn khi được ủy quyền.** Người duyệt đã duyệt kịch bản + ảnh và nói "làm trọn, không hỏi lại" -> tự quyết các lựa chọn kỹ thuật/thẩm mỹ theo kịch bản đã duyệt, tự kiểm và sửa, báo một lần (đường dẫn video + đã tự quyết gì + còn lấn cấn gì). Vẫn KHÔNG làm việc khó đảo ngược ngoài phạm vi (xóa dữ liệu thật, đăng công khai).
- [ ] **Clip hướng dẫn Docs theo mẫu chuẩn C-DB-03** (thẻ tiêu đề -> vấn đề/lợi ích -> đường vào -> mỗi cảnh một bước -> lưu ý -> thẻ kết).
- [ ] **Đăng là hành động công khai: xác nhận trước mỗi lần đăng** (bản nào, tiêu đề, công khai hay không). Video ra mắt sản phẩm/module đăng YouTube `@viindoodocs`; bản dọc Shorts đăng kênh chính `@Viindoo`.
- [ ] **Bài Facebook ra mắt viết tổng quan cho người quản lý**, không thuật ngữ kỹ thuật; mở bằng nỗi đau quen thuộc + 3-5 lợi ích lời đời thường + link mua.

---

## Quy tắc chung xuyên suốt

- Chỉ nói điều CÓ THẬT trong mã nguồn Viindoo; tính năng chưa xác minh phải kiểm qua Odoo Semantic MCP / `viindoo-source-explorer` trước khi đưa vào, hoặc bỏ.
- Dùng dấu gạch ngang ASCII `-` trong mọi lời đọc/phụ đề/chữ màn hình.
- Khi thiếu giá trị brand (CMYK, clear-space...) -> hỏi người phụ trách brand, không bịa.
