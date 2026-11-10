# viindoo-video

Bộ skill làm video Viindoo cho đội marketing: video ngành và video tổng thể bằng motion-graphics, clip tổng thể theo cụm nghiệp vụ, clip ra mắt module. Mọi skill dùng chung một bộ nguyên tắc video (`references/video-principles.md`), một bộ brand (`brand/`) và một engine dựng hình (`engine/`).

## Gồm những gì

| Skill | Làm ra cái gì | Dùng khi |
|---|---|---|
| `viindoo-motion-video` | Video motion-graphics brand Viindoo theo chuẩn forwarder: nền trắng nhấn teal, thanh bước nghiệp vụ chạy suốt, màn phần mềm thật toàn khung, khoanh và kéo con số ra chữ to. Xuất MP4 16:9 + 9:16 + 1:1 | video ngành, video tổng thể, sơ đồ quy trình động, cảnh 3D mô phỏng IoT, nhân bản một video ra nhiều ngành / ngôn ngữ |
| `viindoo-video-cum-nghiep-vu` | Trọn bộ clip tổng thể cho một cụm nghiệp vụ (Nhân sự, Kế toán, Kho, Bán hàng...), song ngữ Việt - Anh: đối tượng -> góc kể -> dữ liệu demo -> quay màn thật -> lời + TTS -> mốc cảnh theo bản thu -> render -> trộn tiếng, b-roll, nhạc -> ảnh bìa -> đăng YouTube | làm clip cho một mảng nghiệp vụ, làm bản tiếng Anh, thu lại giọng, quay lại màn demo |
| `viindoo-module-launch` | Bộ nội dung ra mắt một module trên Viindoo Apps: kiểm tra sẵn sàng, danh sách "nói được / không nói" từ mã nguồn, kịch bản, bài tin VI + EN, clip có lời đọc khổ vuông / dọc / ngang, nhúng video vào trang module | module mới hoặc vừa lên phiên bản mới, cần clip giới thiệu / thông báo ra mắt |

Thư mục khác:

- `references/video-principles.md` - nguyên tắc làm video (kể chuyện, hình, brand, giọng - nhạc, đăng tải). Skill nào cũng đọc trước khi dựng và trước khi xuất.
- `brand/` - `brand-tokens.json` (màu, font), `assets/logo-color.svg`, `assets/logo-inverted.svg`, `assets/fonts/` (Montserrat, Roboto - giấy phép OFL / Apache). Chỉ gồm phần video cần; bộ brand đầy đủ ở https://viindoo.com/vi/page/brand-assets.
- `engine/` - bộ dựng motion-graphics (GSAP + Chrome headless + FFmpeg), bộ cảnh `fw*`, mẫu thử `engine/samples/seq-mau.json`.
- `skills/viindoo-video-cum-nghiep-vu/templates/` - khuôn script cho một cụm (quay, lời, mốc cảnh, trộn tiếng, dữ liệu demo).

## Chuẩn bị trên máy

| Cần gì | Skill cần | Cách làm |
|---|---|---|
| Node.js 18+ | cả ba | `brew install node` |
| Thư viện engine (gsap, puppeteer-core) | `viindoo-motion-video`, `viindoo-video-cum-nghiep-vu` | Một lần: `bash "<thư mục plugin>/engine/setup.sh"` - cài vào `~/viindoo-video/.engine-deps`, không cài vào thư mục plugin. Chạy lại sau khi cập nhật plugin nếu `package-lock.json` đổi |
| FFmpeg | cả ba | `brew install ffmpeg` |
| Google Chrome | cả ba | Cài Chrome bình thường. Ở chỗ khác (Chrome for Testing, Chromium, Linux) thì `export CHROME_PATH=<đường dẫn file chạy>`. Quay màn Viindoo phải dùng Chrome thật: biểu đồ canvas mới ra đủ |
| Python 3 + `playwright`, `Pillow`, `numpy` | `viindoo-video-cum-nghiep-vu`, `viindoo-module-launch` | `python3 -m venv ~/viindoo-video/.venv && ~/viindoo-video/.venv/bin/pip install playwright pillow numpy`, rồi `export VIDEO_PY=~/viindoo-video/.venv/bin/python`. Xoá logo trên ảnh stock (`remove_logo.py`) cần thêm `opencv-python` |
| Gemini API key | lời đọc TTS, soát lời (`check_tts`, `stt_check`) | Lấy key tại https://aistudio.google.com/apikey, thêm `export GEMINI_API_KEY=...` vào `~/.zshrc`. TTS là phần duy nhất tốn tiền - đọc mục "TIỀN" trong `references/giong-doc.md` của skill cụm trước khi thu |
| Hệ thống demo Viindoo + tài khoản | quay màn, bơm dữ liệu demo | `export VIINDOO_DEMO_URL=https://<demo>.viindoo.cloud VIINDOO_DEMO_DB=... VIINDOO_DEMO_LOGIN=... VIINDOO_DEMO_PASSWORD=...` - xin người quản lý hệ thống demo, không ghi vào tệp |
| Thư mục làm việc | cả ba | Mặc định `~/viindoo-video` (video xuất, b-roll, nhạc nền, thư mục từng cụm / từng module). Đổi bằng `export VIINDOO_VIDEO_WORKDIR=<thư mục>` |
| Plugin `odoo-ai-agents` (marketplace `viindoo-plugins`) | nên có | MCP `odoo-media` (giọng đọc, đăng YouTube `youtube_upload`), skill `odoo-demo-recording`, MCP chrome-devtools, Odoo Semantic MCP để kiểm tính năng theo mã nguồn |
| MCP chrome-devtools | soát màn, chụp biểu đồ | Có sẵn khi cài `odoo-ai-agents` |
| Mã nguồn Viindoo | `viindoo-module-launch` | Clone về `~/viindoo/<phiên bản>/`, hoặc `export VIINDOO_SRC=<thư mục>` |
| Plugin `viindoo-marketing` | `viindoo-module-launch` (đăng blog) | Skill `viindoo-blog-publish` đăng bài tin lên blog viindoo.com dạng nháp |

Thử máy sau khi chuẩn bị (23 giây, số minh hoạ, ra `~/viindoo-video/output/seq-mau.mp4`):

```bash
node "<thư mục plugin>/engine/sequence.mjs" --seq "<thư mục plugin>/engine/samples/seq-mau.json"
```

Trong Claude Code, thư mục plugin là `${CLAUDE_PLUGIN_ROOT}`; cứ nói "thử engine video" là Claude tự chạy.

## Dùng thế nào

Không cần gõ tên skill, cứ nói việc cần làm:

- "Dựng video tổng thể ngành cơ khí theo chuẩn forwarder" -> `viindoo-motion-video`.
- "Làm sơ đồ quy trình động 8 bước cho ngành giao nhận, ra cả bản dọc" -> `viindoo-motion-video`.
- "Làm cảnh 3D mô phỏng cân điện tử đẩy số về Viindoo" -> `viindoo-motion-video` (cảnh `fw3d*`).
- "Làm clip kế toán đi" / "dựng clip tổng thể cụm Kho" -> `viindoo-video-cum-nghiep-vu`, bắt đầu từ chân dung đối tượng.
- "Sang bản tiếng Anh của clip Nhân sự" / "thu lại giọng clip Dự án" -> `viindoo-video-cum-nghiep-vu`.
- "Module viin_xxx vừa lên bản 19, làm clip ra mắt" / dán link `viindoo.com/apps/modules/...` rồi hỏi "cần làm gì cho marketing" -> `viindoo-module-launch`.

Mỗi skill dừng lại hỏi ở những chỗ cần người quyết (chân dung đối tượng, góc kể, giọng, nghe duyệt bản cuối, đăng công khai); việc kỹ thuật tự quyết.

## Lưu ý

- Không đưa video, b-roll, bản thu, dữ liệu khách hay key vào repo. Mọi thứ đó nằm trong thư mục làm việc.
- Sửa engine, cảnh hay nguyên tắc thì sửa trong repo này và gửi PR - bản cài của plugin bị ghi đè mỗi lần cập nhật.
- Clip mẫu chuẩn forwarder ("V61. Viindoo Freight Management") và các kịch bản đã làm nằm ở kho nội bộ, cần xem thì xin Liên.
