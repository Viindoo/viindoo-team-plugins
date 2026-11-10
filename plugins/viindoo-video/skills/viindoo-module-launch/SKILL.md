---
name: viindoo-module-launch
description: Đóng gói trọn bộ nội dung bán module Viindoo trên kho ứng dụng (Viindoo Apps) khi có module mới hoặc module vừa lên phiên bản Odoo mới - kiểm tra module đã bán được chưa, lấy sự thật từ mã nguồn và hướng dẫn, viết kịch bản clip + bài tin song ngữ, quay thao tác thật trên hệ thống demo, dựng clip VI/EN khổ vuông và dọc có lời đọc, phụ đề, nút mua. Dùng skill này bất cứ khi nào người dùng nói về ra mắt / giới thiệu / quảng bá / bán một module, app, tính năng mới của Viindoo, hoặc module vừa có trên Odoo 18, 19..., kể cả khi chỉ dán link trang module viindoo.com/apps/modules/... và hỏi "cần làm gì cho marketing", "làm clip giới thiệu", "thông báo ra mắt".
---

# Ra mắt module trên Viindoo Apps

> **Cổng nguyên tắc video (bắt buộc).** TRƯỚC KHI viết kịch bản và TRƯỚC KHI xuất/đăng: đọc `${CLAUDE_PLUGIN_ROOT}/references/video-principles.md` (bảng giọng theo loại video ở mục 0, checklist A-E). Nguyên tắc này thắng mọi mặc định generic.

Kết quả: một bộ nội dung bán module, song ngữ tiếng Việt và tiếng Anh, sẵn sàng đăng ở mọi kênh, trỏ về trang bán module. Trao đổi với người dùng bằng tiếng Việt. Người duyệt là người dùng; **mỗi sản phẩm phải được duyệt riêng trước khi làm bước tốn công sau nó**.

Thư mục làm việc mặc định: `${VIINDOO_VIDEO_WORKDIR:-~/viindoo-video}/Ra-Mat-Module/<slug>/` (slug ngắn, không dấu, ví dụ `dieu-hanh-xuong-18`). Bên trong: `kich-ban-clip-ra-mat.md`, `bai-tin-ra-mat.md`, `anh-mo-dau/` (kèm `NGUON.md`), `mau-giong/`, `clip-vi/`, `clip-en/`, `video/` (file xuất).

## Hợp đồng đầu ra

| Sản phẩm | Yêu cầu |
|---|---|
| Kiểm tra sẵn sàng | Bảng ngắn: module installable trên nhánh `origin/<phiên bản>` (không tin bản sao cục bộ khi chưa `git status -sb`), trang module đã công khai (`odoo.module.version.is_published`), có mô tả VI và EN, giá hiển thị đúng đơn vị, demo trực tuyến trên trang có cài module. Thiếu gì thì báo trước khi làm nội dung. |
| Danh sách "Nói được / Không nói" | Rút từ `doc/index.rst`, `doc/index_vi_VN.rst`, `__manifest__.py` (description) và mã nguồn của module cùng module đi kèm. Mỗi câu trong clip và bài tin phải nằm trong cột "Nói được". "Không nói" gồm những thứ người mua dễ tưởng có nhưng không có (ví dụ: tự đếm sản lượng, chạy khi mất mạng, barcode chưa có). |
| Kịch bản clip | Bảng cảnh: hình, lời dẫn VI, lời dẫn EN, chữ trên màn hình VI/EN. Mẫu: `references/kich-ban-mau.md`. Chi tiết đủ cho người mua app (họ đã biết Odoo, đang so sánh module): mỗi cảnh một tính năng thật, có cảnh điều kiện chạy / mở rộng, cảnh cuối là nút mua. |
| Bài tin ra mắt | VI + EN, khoảng 250-350 chữ mỗi bản, mở bằng nỗi đau, gạch đầu dòng tính năng, dẫn về trang module. Mẫu: `references/bai-tin-mau.md`. Đăng blog thì theo skill `viindoo-blog-publish` của plugin `viindoo-marketing` (EN gốc, Auto Translate, ghi đè VI, đăng nháp). |
| Clip | 6 file: VI/EN x vuông 1080x1080 / dọc 1080x1920 (mạng xã hội) / ngang 1920x1080 (YouTube + khung nhúng trên trang module), có lời đọc, nhạc nền, phụ đề, khung cuối có nút mua và địa chỉ trang module. |
| Video trên trang bán | Bản ngang EN + VI đăng YouTube, nhúng vào `static/description/index.html` (EN) và `index_vi_VN.html` (VI) của module. |

## Quy tắc đã chốt (không tự đổi)

- **Viindoo thay Odoo (người dùng chốt 11/10/2026):** nội dung ra mắt (lời đọc, chữ màn hình, bài tin, tiêu đề video) gọi tên sản phẩm và phiên bản là Viindoo, không nhắc "Odoo". Địa chỉ trang module giữ nguyên.
- **Phiên bản:** ghi "từ bản Viindoo <N>" / "from Viindoo <N>" (lời đọc: "dùng được từ bản Viindoo <N>" / "available from Viindoo <N>"); không ghi "tương thích", "cho", "for", "compatible with". Không nêu Community hay Enterprise. <N> là bản thấp nhất đã installable thật (kiểm `__manifest__.py` trên nhánh origin).
- **Màn hình phần mềm = quay thao tác thật trên hệ thống demo** (dữ liệu mang tên Viindoo), không dùng bộ ảnh chụp trong `static/description` hay tài liệu. Mỗi cảnh là một đoạn quay ngắn từ màn bắt đầu tới kết quả, có vòng chạm hiện ở chỗ bấm, nhịp như người thật demo. Ảnh tài liệu chỉ dùng tạm khi chưa có hệ thống, và phải nói rõ là tạm.
- **Làm trên bản sao, dọn sạch:** sao chép chứng từ (lệnh sản xuất, đơn hàng...) để thao tác, ghi id mọi bản ghi tạo ra vào file trạng thái, dọn trong `finally`, in rõ cái gì còn sót. Không xác nhận thao tác không hoàn tác được (xuất hủy, hoàn thành lệnh, vào sổ) trừ khi người dùng cho phép. Không đổi cấu hình hay dữ liệu gốc (định mức, sản phẩm); đổi tên hiển thị tạm cho bản EN thì phải có lệnh hoàn tác. Instance của khách thật thì phải che tên khách.
- **Ảnh xưởng (mở đầu, nỗi đau):** nhà xưởng chuyên nghiệp, không gian rộng, nhiều máy và công đoạn, công nhân bảo hộ đầy đủ. Nguồn miễn phí dùng thương mại (Pexels; Unsplash chỉ ảnh không phải Unsplash+). Xoá logo công ty thật trên mũ/áo bằng `scripts/remove_logo.py`, xem lại bằng mắt. Ghi nguồn vào `anh-mo-dau/NGUON.md`.
- **Giọng (người dùng chốt 12/10/2026):** mọi clip ra mắt sản phẩm dùng **cố định** giọng nam trẻ `Iapetus`, mô hình `gemini-3.1-flash-tts-preview`, câu dặn `STYLES["nam_tre"]` (nhịp nhanh, dứt khoát, gọn, như video ra mắt sản phẩm công nghệ). Mẫu nghe đã chốt nằm ở kho nội bộ, cần thì xin Liên. Bản VI và EN dùng chung giọng. Không đề xuất giọng khác trừ khi người dùng yêu cầu.
- **Nhạc nền:** mỗi clip chọn nhạc riêng hợp nội dung (`MUSIC` trong `clip.py`; `mix.py` dừng nếu thiếu, không có bản mặc định). Các kiểu: `python3 $S/music.py list` (tươi vui, năng động, tin cậy, ấm áp, công nghệ; đổi `seed` là đổi giai điệu). Được **dùng lại** một bản trong thư viện chung `${VIINDOO_VIDEO_WORKDIR:-~/viindoo-video}/Nhac-nen/` khi nó thật sự hợp clip mới, nhưng không mặc định dùng lại: các clip cùng một loạt đăng gần nhau nên khác bản. Bản VI và EN của cùng một clip dùng chung nhạc. Thư viện ghi lại clip nào đã dùng bản nào (`index.json`).
- **Logo và màn kết:** logo màu chuẩn `${CLAUDE_PLUGIN_ROOT}/brand/assets/logo-color.svg` (Viin #00BBCE + doo #7F4282). Cảnh mở đầu (ảnh xưởng tối) đặt logo trên thẻ trắng bo góc; màn kết nền trắng, chữ màu tiêu đề, nút cyan chữ trắng. `logo-inverted.svg` (Viin trắng + doo tím) chỉ dùng trên nền cyan phẳng. `render.py` xuất BT.709 dải giới hạn, có nhãn màu, để cyan không lệch khi phát trên nền tảng.
- **Lời mời cuối:** nút "Mua trên Viindoo Apps" / "Get it on Viindoo Apps" + địa chỉ trang module (`viindoo.com/vi/apps/modules/<ver>/<module>` và bản EN không có `/vi`).
- **Không nêu những điều gợi rủi ro bảo mật / phân quyền** dù tài liệu module có ghi, ví dụ "nhiều người dùng chung một máy tính bảng": chỉ nói dùng máy tính bảng tại máy, mỗi người một tài khoản là chuyện của phần thiết lập.
- **Chữ:** chỉ dùng gạch nối ASCII `-`. Tên tính năng dùng đúng nhãn giao diện. Không con số tiết kiệm khi chưa có khách thật đồng ý.

## Quy trình

1. **Kiểm tra sẵn sàng.** `git -C ${VIINDOO_SRC:-~/viindoo}/<ver>/<repo> fetch` rồi `git show origin/<ver>:<module>/__manifest__.py`; kiểm tra trang module (MCP `odoo` trên viindoo.com: `odoo.module.version` theo `technical_name`, hoặc tải trang `/vi/apps/modules/...` và `/apps/modules/...`). Lập bảng, báo thiếu.
2. **Lấy sự thật.** `git archive origin/<ver> <module> <module_phụ...> | tar -x -C <scratch>`; đọc trọn `doc/index_vi_VN.rst` và `doc/index.rst` (cả phần tổ trưởng / kế toán / xử lý sự cố / câu hỏi thường gặp), manifest, các module đi kèm (`*_quality`, `*_maintenance`...). Viết danh sách "Nói được / Không nói".
3. **Kịch bản clip** theo `references/kich-ban-mau.md` -> người dùng duyệt (`approve` / `refine:`).
4. **Bài tin** theo `references/bai-tin-mau.md` -> duyệt.
5. **Ảnh mở đầu + nhạc nền:** chọn 2 ảnh theo quy tắc, xoá logo. Giọng cố định `Iapetus`. Đề xuất 2-3 phương án nhạc cho riêng clip này: kiểu + seed mới, hoặc bản đã có trong thư viện nếu hợp. Mỗi phương án có lý do một câu, kèm file nghe thử (`python3 $S/music.py preview <kiểu>:<seed> ...` -> `Nhac-nen/nghe-thu/`). Người dùng chọn, rồi ghi `VOICE` + `MUSIC` vào `clip.py`.
6. **Cài và chuẩn bị demo:** cài module trên instance demo (XML-RPC `button_immediate_install`, khoá do cron thì thử lại sau 40 giây), bổ sung dữ liệu module cần để màn hình có số liệu (ví dụ đơn giá giờ nhân viên), ghi manifest hoàn tác.
7. **Quay thao tác thật** (Playwright): mỗi cảnh một context ghi video riêng, đăng nhập trước bằng storage state để không quay màn đăng nhập; ẩn con trỏ, vẽ vòng chạm; chờ 0,8-1,2 giây sau mỗi thao tác, gõ số từng chữ; giữ 1,5 giây ở màn kết quả; 4-12 giây mỗi đoạn; chuyển webm -> mp4 H.264 30 fps. Kèm ảnh tĩnh cùng cảnh. Viewport: máy tính bảng dọc 800x1280, ngang 1280x800, máy tính để bàn 1280x800. Ghi `shots.json` (định dạng ở `references/clip-template.py`), mỗi ảnh có `video`, ô phóng `boxes` lấy từ DOM. Bản EN: đổi ngôn ngữ người dùng sang en_US khi quay rồi trả lại. Ví dụ đầy đủ (16 cảnh, sao chép lệnh, dừng/chạy lại trạm, đóng lệnh tới câu hỏi phần còn lại rồi quay lại): `references/capture-example-shopfloor.py`. Nút chỉ người không phải quản lý mới thấy (ví dụ "Nhờ quản lý phê duyệt") cần quay bằng tài khoản công nhân không có quyền Quản trị Sản xuất.
8. **Dựng clip** bằng `scripts/` (xem phần dưới). Kiểm lời đọc bằng `stt_check.py`, xem ảnh xem thử các cảnh, sửa rồi mới xuất.
9. **Đưa video lên trang bán:** trang viindoo.com/apps lấy mô tả từ `static/description/index.html` và `index_vi_VN.html` trong mã nguồn module (đồng bộ từ nhánh git); không có chỗ tải file video lên. Cách đang dùng (hàng trăm module bản 17-19): đăng video lên YouTube (video app cũ ở kênh "Viindoo Docs" `@viindoodocs`, tiêu đề cũ dạng "Odoo Apps - <Tên> | Odoo <N> ...", video mới đặt tiêu đề theo Viindoo, ví dụ "Viindoo Apps - <Tên> | Viindoo <N>"; kênh chính là `@Viindoo` - hỏi người dùng chọn kênh), rồi chèn khung nhúng vào 2 file mô tả theo mẫu sẵn có:
   `<div style="position:relative; padding-top:56.25%; border-radius:14px; overflow:hidden; box-shadow:0 6px 20px rgba(0,0,0,0.08); margin-bottom:20px;"><iframe src="https://www.youtube.com/embed/<ID>" title="<Tên> demo video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute; inset:0; width:100%; height:100%;"></iframe></div>`
   Sửa trên nhánh riêng của repo module (tạo từ `origin/<ver>`), để đội phát triển duyệt; không đẩy thẳng nhánh chính.
10. **Bàn giao:** đường dẫn 4 file, thời lượng, những gì đã kiểm, những gì chưa kiểm. Cập nhật bài tin nếu cần, đăng blog bằng `viindoo-blog-publish` (plugin `viindoo-marketing`) khi được duyệt.

## Dựng clip bằng scripts

Cần: `ffmpeg`, Google Chrome, một python có `playwright` (`$VIDEO_PY`), `GEMINI_API_KEY`. `python3` hệ thống chạy được `build.py`, `mix.py`, `make_vo.py`, `stt_check.py`; `prep_shots.py` cần Pillow + numpy; `remove_logo.py` cần opencv. `S=${CLAUDE_PLUGIN_ROOT}/skills/viindoo-module-launch/scripts`.

1. Tạo `clip-vi/clip.py` và `clip-en/clip.py` từ `references/clip-template.py` (VOICE, MUSIC đã chọn ở bước 5, VO, CAPS, PLAN, OUT, CTA, WEB, ảnh mở đầu trong `assets/photos/`, màn hình trong `assets/shots/` + `shots.json`). Kiểm mọi cụm từ neo trong PLAN có trong VO tương ứng.
2. Lời đọc: `python3 $S/make_vo.py <clip_dir> --batch` (một lượt gọi cho cả clip; Gemini TTS miễn phí ~10 lượt/ngày/mô hình, làm mới khoảng 7 giờ sáng giờ Việt Nam).
3. **Kiểm từng đoạn lời đọc:** `python3 $S/stt_check.py <clip_dir>` (Gemini 2.5 Flash nghe lại từng `vo/seg*.flac`, in cạnh lời kịch bản). Nếu một câu bị dồn sang đoạn sau: `python3 $S/recut.py <clip_dir>` in các chỗ cắt, `recut.py <clip_dir> 5=+1 6=+1 ...` dời chỗ cắt sang khoảng lặng kế tiếp; chỗ ngắt quá ngắn thì cắt tay bằng ffmpeg theo `silencedetect -40dB d=0.08`. Âm đầu đoạn bị mất (ví dụ "Re" của "Record") thì cắt lại đoạn đó sớm hơn 0,2-0,3 giây.
4. `python3 $S/build.py <clip_dir> sq|v|h` -> `video_<fmt>.html`; xem thử: `$VIDEO_PY $S/render.py <clip_dir> sq preview 3,12,25` -> `prev/`, ghép ảnh xem bằng ffmpeg tile và **xem từng khung**: khung bị cắt mép, màn quá nhỏ, chữ tràn, địa chỉ tràn ở khổ dọc (`WEB_FS`).
5. Xuất: `$VIDEO_PY $S/render.py <clip_dir> sq|v full` rồi `python3 $S/mix.py <clip_dir> sq|v` (chạy nền, 2 luồng song song; mỗi phút clip mất vài phút xuất). `mix.py` lấy nhạc theo `MUSIC` từ thư viện (thiếu hoặc ngắn hơn clip thì tự sinh lại đúng bản đó), in "lưu ý" nếu bản này đã dùng cho clip khác: báo người dùng nếu đó là clip cùng loạt.

Lớp hình trong PLAN: `hook` (ảnh mở đầu + tiêu đề), `photo` (ảnh xưởng + nhãn), `shot` (khung trình duyệt, phóng theo `zoom`, `"fit": True` để hiện trọn màn máy tính để bàn), `phone` (khung thiết bị cho màn máy tính bảng), `before_after`, `cta`. `shot`/`phone` tự dùng đoạn quay nếu `shots.json` có `video`; hạ `h` trong `shots.json` là cắt bớt phần trống phía dưới màn dọc.

## Bẫy đã gặp

- Bản sao mã nguồn cục bộ có thể kẹt (lệch nhánh) và báo module chưa installable trong khi `origin` đã có. Luôn kiểm `origin/<ver>`.
- `make_vo.py --batch` cắt theo tỉ lệ chữ: khi giọng không nghỉ đủ giữa các đoạn, chỗ cắt trượt sớm một câu cho cả chuỗi đoạn. Luôn chạy `stt_check.py`.
- Trong zsh, `for x in $bien` không tách từ; dùng `bash -c` hoặc mảng.
- Không đặt tên file nháp trùng thư viện chuẩn Python (`inspect.py`, `json.py`): chạy python với `-I` từ thư mục có file đó sẽ nạp nhầm.
- Ảnh stock nhà máy đẹp thường có logo tập đoàn thật trên mũ (ví dụ NLMK): xoá trước khi dùng; vá phủ khối màu lộ vết, dùng inpaint theo hình bầu dục và chặn mặt nạ trên vành mũ.
- Python framework 3.14 trên macOS lỗi SSL khi gọi XML-RPC: dùng `/usr/bin/python3`.
- Dữ liệu demo nhiều công ty: nạp số liệu (đơn giá giờ...) cho đúng công ty sẽ quay, kiểm lại bằng `search_read` theo `company_id`.
- Đoạn quay dài hơn lời đọc được tự tua nhanh (tối đa 2,5 lần); vòng khoanh không vẽ trên lớp video vì màn hình đổi liên tục, chỉ dùng camera phóng cho màn có bố cục cố định.
