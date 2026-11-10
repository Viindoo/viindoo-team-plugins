---
name: viindoo-video-cum-nghiep-vu
description: Dây chuyền dựng TRỌN BỘ clip tổng thể cho một CỤM NGHIỆP VỤ của Viindoo (Nhân sự, Kế toán, Sản xuất, Bán hàng, Kho, Mua hàng, Dự án, Bảo trì...), song ngữ Việt - Anh, từ bơm dữ liệu demo, chụp màn hình thật trên hệ thống thật, viết lời, chọn giọng và thu TTS, tính mốc cảnh theo chính bản thu, render, trộn tiếng với b-roll người thật và nhạc nền, làm ảnh bìa, đến đăng YouTube. Dùng skill này bất cứ khi nào người dùng nhắc tới việc làm clip/video cho một mảng nghiệp vụ hay một bộ module của Viindoo, làm bản tiếng Anh của một clip đã có, thu lại giọng cho clip, chụp lại màn hình demo cho clip, hay nối tiếp một clip cụm đang làm dở - kể cả khi chỉ nói ngắn gọn kiểu "làm clip kế toán đi", "sang bản tiếng Anh", "đổi giọng khác", "dựng tiếp clip sản xuất". KHÔNG dùng cho clip ra mắt một module lẻ, clip hướng dẫn Docs, Reels/Shorts, hay bài đăng mạng xã hội.
---

# Clip tổng thể theo cụm nghiệp vụ Viindoo

Trao đổi bằng tiếng Việt. Kết quả mỗi cụm: **hai file MP4 1920x1080@60** (một Việt một
Anh), ảnh bìa hai ngôn ngữ, nội dung đăng, và clip đã lên YouTube kênh `@Viindoo`.

> **Cổng nguyên tắc video (soát trước, thắng mọi mặc định).** Đọc
> `${CLAUDE_PLUGIN_ROOT}/references/video-principles.md` TRƯỚC khi dựng kịch bản và TRƯỚC khi
> xuất/đăng. Màu/font/logo theo `${CLAUDE_PLUGIN_ROOT}/brand/brand-tokens.json` và
> `${CLAUDE_PLUGIN_ROOT}/brand/assets/`. Phần ENGINE motion-graphics (bộ cảnh `fwpain` `fwtitle`
> `fwtwo` `fwsteps` `fwscreen` `fwapps` `fwcta`, chuẩn hình, chuẩn kể) nằm ở skill
> **`viindoo-motion-video`** - đọc skill đó, đừng chép lại ở đây.

## Bản mẫu đã chạy thật

Cụm **Nhân sự** là bản hoàn chỉnh đầu tiên, cả hai ngôn ngữ, đã đăng. Xem clip Việt để biết đích
đến: https://youtu.be/VdlnJ_qpqBw

Khuôn script nằm ở `templates/` của skill này (lấy từ cụm làm gần nhất - Kho, dựng trên khuôn Bán
hàng + CRM): `templates/clips/` (quay, lời, mốc cảnh, trộn tiếng) và `templates/demo-data/` (kết nối,
đổi ngôn ngữ, dịch dữ liệu). Cụm mới chép sang rồi sửa bảng cảnh, đừng viết lại từ đầu. Đường dẫn và
tài khoản đọc từ biến môi trường qua `clips/cau_hinh.py` - không ghi cứng đường dẫn máy ai.

Tạo bộ khung cho cụm mới:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/viindoo-video-cum-nghiep-vu/scripts/tao_cum.sh" <Ten-Cum>
# ví dụ: tao_cum.sh Ke-Toan -> $VIINDOO_VIDEO_WORKDIR/Cum/Ke-Toan/{clips,demo-data,anh-bia,cat-kenh,video}
```

Biến môi trường cần (xem README của plugin): `VIINDOO_VIDEO_WORKDIR` (mặc định `~/viindoo-video`),
`GEMINI_API_KEY`, `VIINDOO_DEMO_URL` / `VIINDOO_DEMO_DB` / `VIINDOO_DEMO_LOGIN` /
`VIINDOO_DEMO_PASSWORD`, `CHROME_PATH` nếu Chrome không nằm chỗ mặc định. Python cần `playwright`,
`Pillow`, `numpy`.

## Dòng chảy công việc

Mười bước. Bước nào cũng có một thứ **phải kiểm bằng máy rồi mới đi tiếp** - cột cuối. Lý do: gần
như mọi lỗi của dây chuyền này đều **không làm hỏng lệnh dựng**, file vẫn ra, vẫn phát được, chỉ sai
khi người xem nhìn hoặc nghe. Không có cổng kiểm thì chỉ phát hiện sau khi đã đăng.

| # | Bước | Làm gì | Kiểm trước khi đi tiếp |
|---|---|---|---|
| 1 | **Tìm đối tượng** | **Ai xem clip này**: ngành nào, công ty cỡ nào, đang dùng gì, **bài toán** của họ là gì, **kỳ vọng** gì khi dùng cụm này | Người duyệt nội dung duyệt chân dung đối tượng bằng chữ. Chưa có đối tượng thì CHƯA được viết góc |
| 2 | **Chốt góc** | Từ chân dung đó viết **hai mục đích** của cụm và **dòng chảy 8-10 bước** | Người duyệt duyệt góc + dòng chảy bằng chữ, trước khi đụng tới hình |
| 3 | **Dữ liệu demo** | Bơm dữ liệu thật trên hệ thống demo (`VIINDOO_DEMO_URL`, mặc định `sanxuat18.viindoo.cloud`) | Số trên màn phải tự giải thích được, không mâu thuẫn nhau |
| 4 | **Bộ lọc đã lưu** | Mỗi màn một bộ lọc tên `VIDEO <CỤM> - Cxx ...` | Mở lại bằng tên, ra đúng số định khoanh |
| 5 | **QUAY màn** | `quay_fw.py` - quay thật 1280x720 @1.5, kịch bản thao tác từng cảnh | Trích khung hình ra **nhìn tận mắt**: đúng bộ lọc, đúng tập bản ghi, có số chưa |
| 6 | **Viết lời** | `tts_<lang>_fw.py` - một đoạn một cảnh | Đọc to lên: mỗi đoạn có đúng một con số làm trụ |
| 7 | **Chọn giọng** | Giọng đã chốt cho cả bộ (Việt Fenrir, Anh Iapetus); chỉ thi lại khi thêm ngôn ngữ mới - thu CẢ BÀI vài giọng, ghép đoạn đầu cho người duyệt nghe | Người duyệt chọn bằng tai - số đo chỉ loại giọng dở |
| 8 | **Thu lời** | `pick_take.py N` - thu nhiều bản, chấm, giữ bản sạch nhất | 0 lỗi đọc thật + cao độ đạt ngưỡng ngôn ngữ đó |
| 9 | **Tính cảnh** | `build_seq.py` - mốc cảnh lấy từ khoảng lặng của CHÍNH bản thu | Tổng thời lượng khớp bản thu |
| 10 | **Render + trộn** | `sequence.mjs` (engine của plugin) rồi `mix.sh` | Đỉnh tiếng dưới 0 dB, độ to khớp bản ngôn ngữ kia |
| 11 | **Bìa + đăng** | Ảnh bìa 1920, nội dung đăng, YouTube `@Viindoo` | **Người duyệt nghe bằng tai** rồi mới đăng |

Chi tiết từng bước nằm ở `references/`:

- `references/doi-tuong.md` - bước 1: đo nhu cầu thật, dựng chân dung đối tượng, bài toán, kỳ vọng
- `references/quy-trinh.md` - bước 2-6 và 9-10: góc kể, dữ liệu demo, quay màn, mốc cảnh, trộn tiếng
- `references/giong-doc.md` - bước 7-8: chọn giọng, thu, chấm, các bẫy của TTS
- `references/ban-ngon-ngu-hai.md` - làm bản ngôn ngữ thứ hai (đây là chỗ hay sai nhất)
- `references/dang-tai.md` - bước 11: ảnh bìa, nội dung đăng, đăng YouTube

## Mười hai cái bẫy đã trả giá

Đây là phần đáng giá nhất của skill. Đọc trước khi bắt tay, đừng đợi vấp lại.

1. **Giọng duyệt ở ngôn ngữ này không dùng được cho ngôn ngữ kia.** Cùng giọng Fenrir: tiếng Việt
   137 Hz (Liên khen), tiếng Anh 116 Hz (Liên loại - "trầm quá, gằn, có chữ nghe ko rõ"). Phải chọn
   lại giọng cho từng ngôn ngữ, đo trên chính ngôn ngữ đó.
2. **Thu đoạn mẫu ngắn để so giọng là chọn nhầm.** Đọc riêng một đoạn thì cao độ vọt lên 140-169 Hz
   so với 119-126 Hz khi đọc cả bài. Thu CẢ BÀI rồi mới cắt đoạn đầu ra so.
3. **Vá một đoạn TTS lẻ không dùng được** - cùng lý do trên. Sai một chữ thì đổi cách viết chữ đó
   rồi thu lại cả bài.
4. **Dữ liệu demo mang ngôn ngữ lúc tạo ra nó.** Tạo kho bằng giao diện tiếng Anh thì clip tiếng
   Việt mãi hiện "Input/DN". Tạo bằng đúng ngôn ngữ của clip gốc, bản thứ hai thì dịch (xem
   `references/ban-ngon-ngu-hai.md`).
5. **Khung khoanh phải đo lại trên ảnh mới, không bê từ bản ngôn ngữ kia.** Bảng sắp theo tên nên
   đổi ngôn ngữ là đổi thứ tự dòng - khung cũ khoanh nhầm sang dòng khác. Hàm dò phải gom theo
   **nội dung** (mọi dòng có 0 %), không theo vị trí.
6. **Đỉnh tiếng phải đo ĐỈNH THẬT.** Đo từng mẫu ra -0,74 dB mà đỉnh thật đã +2,05 dB, nén AAC xong
   file giao ra +1,24 dB, nghe rè. Chặn đỉnh trên tần số lấy mẫu gấp bốn rồi hạ về.
7. **Khung/thẻ trên cảnh đừng đặt chiều cao cứng.** Nhãn tiếng Anh dài hơn tiếng Việt, chữ tràn ra
   ngoài khung trắng. Đo chiều cao thật của nội dung rồi kéo mọi thẻ cùng hàng cao bằng nhau.
8. **Mọi địa chỉ chụp màn phải kèm `&cids=1`.** Thiếu là Viindoo lấy công ty đang hoạt động của
   admin và cho ra màn mẫu TRỐNG của Odoo (tên giả Henry Campbell, nhãn lorem ipsum).
9. **Không vẽ con trỏ chuột giả** (Liên 19/10/2026). Playwright quay cũng không ra con trỏ. Không có
   chuột thật thì bỏ hẳn.
10. **B-roll người thật mượn ĐUÔI cảnh đứng trước**, cảnh đó render ngắn đi đúng bằng độ dài b-roll.
    Nhờ vậy tổng thời lượng và lời đọc không đổi - không phải thu lại tiếng.
11. **Mỗi cụm lấy b-roll MỚI trên NAS, không dùng lại đoạn của cụm trước** (Liên 30/10/2026). Ưu
    tiên tệp quay thô - bản đã dựng (Storytelling) có phụ đề tiếng Anh cháy vào hình. Ưu tiên cảnh
    NHIỀU NGƯỜI; tránh một người ngồi gõ máy một mình.
12. **Ba kiểu đặt hình, đừng đặt nhầm chỗ** (Liên 30/10/2026). Toàn khung là mặc định - cảnh người
    thật để full không chèn gì, cảnh giao diện phần mềm cũng full không đè chữ. Đặt góc chỉ cho
    nội dung dạng tổng hợp. Nền mờ chỉ ở màn mở đầu và phải mờ NHẸ, nhìn rõ mặt người.
    Chi tiết: `references/quy-trinh.md` bước 9.

## Khi nào hỏi người duyệt, khi nào tự quyết

Liên đã chốt: **việc kỹ thuật tự quyết, đừng hỏi**. Chỉ dừng lại hỏi người duyệt nội dung ở năm chỗ:

- **Chân dung đối tượng** (bước 1) - chốt nhắm ai là quyết định kinh doanh, không phải kỹ thuật.
- **Góc kể và dòng chảy** (bước 2) - đây là nội dung, không phải kỹ thuật.
- **Chọn giọng** (bước 7, chỉ khi thêm ngôn ngữ mới) - phải tai người nghe, máy không nghe được.
- **Duyệt bản cuối bằng tai** trước khi đăng - nói rõ là mình không nghe được, đừng tự nhận đã kiểm.
- **Đăng công khai** - hành động khó đảo ngược, xác nhận trước mỗi lần.

Mọi thứ khác (chọn màn nào, khoanh chỗ nào, nhịp cảnh, cách trộn tiếng) tự quyết và báo lại kết quả.

## Cấu trúc một cụm

```
$VIINDOO_VIDEO_WORKDIR/Cum/<Cum>/
├── <Cum>-Doi-Tuong-Va-Nhu-Cau.md   bước 1: chân dung đối tượng, bài toán, kỳ vọng, số đo nhu cầu
├── <Cum>-Kich-Ban-Clip-Tong.md     kịch bản + nhật ký quyết định + việc còn nợ
├── clips/
│   ├── cau_hinh.py                 đường dẫn + tài khoản demo qua biến môi trường
│   ├── quay_fw.py                  QUAY màn thật + kịch bản thao tác (bảng CANH)
│   ├── do_duoi.py                  đo đuôi hỏng của từng bản quay Playwright
│   ├── dung_noi_dau.py / dung_mo_dau.py (+ *_chu.html)  cảnh người thật + lớp chữ
│   ├── build_seq.py                bảng cảnh + chữ hai ngôn ngữ + mốc lời
│   ├── tts_vi_fw.py / tts_en_fw.py lời đọc + gọi Gemini TTS (VOICE_NAME đổi giọng)
│   ├── pick_take.py / chot_tts.py  thu nhiều bản, chấm, giữ bản sạch nhất
│   ├── check_tts.py voice_stats.py soát đọc sai + đo chất giọng
│   ├── can_cao_do.py chinh_cao_do.py  đo + kéo cao độ CẢ BÀI (bước cuối, xem nguyên tắc mục D)
│   ├── mix.sh                      nối cảnh + chèn b-roll + trộn tiếng + soát đỉnh
│   ├── cat_ngan.py / dung_vuong.py bản cắt ngắn / bản vuông cho mạng xã hội
│   ├── captures-fw[-en]/           ảnh màn + shots.json (toạ độ khoanh)
│   └── voice/                      bản thu
├── demo-data/                      conn.py + script bơm dữ liệu + doi_ngon_ngu.py + dich_en.py
├── anh-bia/                        bìa hai ngôn ngữ
├── cat-kenh/DANG-YOUTUBE-*.md      nội dung đăng
└── video/<Cum>-tong-the-{VI,EN}-forwarder.mp4
```

Engine render ở `${CLAUDE_PLUGIN_ROOT}/engine/` (dùng chung mọi cụm, cài thư viện một lần bằng
`engine/setup.sh`) - xem skill `viindoo-motion-video`. B-roll đã cắt để ở
`$VIINDOO_VIDEO_WORKDIR/broll/<cụm>/`, nhạc nền ở `$VIINDOO_VIDEO_WORKDIR/Nhac-nen/`.
