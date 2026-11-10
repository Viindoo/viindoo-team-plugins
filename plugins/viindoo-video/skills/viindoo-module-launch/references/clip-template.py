"""MẪU clip.py cho skill viindoo-module-launch (ví dụ thật: clip ra mắt Điều hành xưởng sản xuất, bản tiếng Việt).

Chép file này vào <clip_dir>/clip.py rồi sửa. Cấu trúc <clip_dir>:
  clip.py
  assets/photos/<ảnh mở đầu>.jpg, <ảnh nỗi đau>.jpg     (ảnh xưởng, đã xoá logo thật)
  assets/shots/<khoá>.png|jpg [+ <khoá>.mp4]             (quay thao tác thật trên hệ thống demo)
  assets/shots/shots.json  -> [{"file": "output.png", "w": 1600, "h": 2560, "desc": "...",
                               "boxes": [{"label": "numpad", "x0": .., "y0": .., "x1": .., "y1": ..}],
                               "video": "output.mp4"}]   (w/h/toạ độ theo pixel của ảnh; hạ "h" để cắt bớt phần dưới)
  vo/seg*.flac (make_vo.py sinh)

Các biến:
  SLUG, TITLE (HTML, tiêu đề cảnh mở đầu), OUT (đường dẫn xuất, không đuôi), CTA (chữ nút cuối), WEB (+ WEB_FS) địa chỉ ở khung cuối,
  PHOTO (thư mục ảnh xưởng, mặc định assets/photos/), HOOK_PHOTO = (file, {"sq": object-position, "v": ...}),
  VOICE (BẮT BUỘC, cố định "Iapetus" cho clip ra mắt sản phẩm - make_vo.VOICES),
  STYLE / SPOKEN / BATCH_INTRO (STYLE mặc định make_vo.STYLES["nam_tre"]; bản EN đặt STYLE + BATCH_INTRO tiếng Anh, SPOKEN [("Viindoo", "Vin-doo")]),
  MUSIC (BẮT BUỘC) = {"style": <kiểu trong make_music.STYLES>, "seed": <số>, "why": "<vì sao hợp clip này>"} - chọn riêng cho từng clip,
    dùng lại bản đã có trong thư viện (python3 music.py list) chỉ khi nó hợp nội dung clip,
  GAP (nghỉ sau mỗi đoạn, len = len(VO) - 1), VO (lời đọc từng cảnh), CAPS (chữ trên màn hình từng cảnh; CAPS[-1] = dòng chữ ở khung cuối),
  PLAN {cảnh: [(loại, file, cụm từ neo trong VO hoặc None, tuỳ chọn)]}:
    ("hook", None, None, {})
    ("photo", "<ảnh>", None, {"pos": {"sq": "45% 40%", "v": "42% 40%"}, "tag": "<nhãn>"})
    ("shot", "<khoá>.png", None, {"zoom": [("<nhãn ô>", "<cụm từ trong VO>")], "fit": True})   # màn ngang / máy tính để bàn
    ("phone", "<khoá>.png", "<cụm từ>", {"zoom": ("<nhãn ô>", "<cụm từ>")})                    # màn máy tính bảng / điện thoại
    ("cta", None, None, {})
  Lớp thứ hai trong cùng cảnh bắt đầu tại cụm từ neo của nó (phải có nguyên văn trong VO của cảnh, không phân biệt hoa thường).
"""
import os

SLUG = "SF-VI"
TITLE = "Điều hành xưởng<br>ngay tại&nbsp;máy"
OUT = os.path.join(os.path.expanduser(os.environ.get("VIINDOO_VIDEO_WORKDIR", "~/viindoo-video")),
                   "Ra-Mat-Module/dieu-hanh-xuong-18/video/Viindoo-Dieu-Hanh-Xuong-Ra-Mat-VI")
CTA = "Mua trên Viindoo Apps"
VOICE = "Iapetus"   # giọng cố định của clip ra mắt sản phẩm
# STYLE: bản VI để mặc định (make_vo.STYLES["nam_tre"], đúng câu dặn của mẫu giọng đã chốt)
MUSIC = {"style": "nang-dong", "seed": 1, "why": "ra mắt module xưởng: nhịp dồn, mạnh, khớp các đoạn quay thao tác"}
WEB = "viindoo.com/vi/apps/modules/18.0/viin_mrp_workorder"

PHOTO = "assets/photos/"
HOOK_PHOTO = ("mo-dau-cong-nhan-may-tinh-bang.jpg", {"sq": "45% 45%", "v": "46% 45%"})
GAP = [0.8] + [0.9] * 12 + [0.8]
WEB_FS = 25

VO = [
    "Viindoo ra mắt Điều hành xưởng sản xuất, dùng được từ bản Viindoo 18: mọi lệnh công đoạn chạy trên máy tính bảng, ngay tại máy.",
    "Không còn ghi sổ cuối ca rồi hôm sau nhập lại. Số liệu có ngay khi việc vừa xong, do chính người làm ghi.",
    "Mỗi công nhân chọn trạm mình làm một lần. Lựa chọn được nhớ theo từng tài khoản.",
    "Bảng công việc theo từng trạm: sẵn sàng, đang chạy, đang chờ, trạm đang dừng, có số đếm trực tiếp và tìm nhanh theo mã lệnh.",
    "Chỉ nút Mở và bắt đầu mới tính giờ, chạm nhầm vào thẻ không bao giờ bấm giờ. Tạm dừng, tiếp tục chỉ một chạm. Nút đủ lớn để bấm khi đeo găng tay.",
    "Ghi thành phẩm trên bàn phím số, mỗi lần là một dòng riêng. Lô thành phẩm tự tạo hoặc chọn lô mới nhất. Ghi nhầm thì hoàn tác đúng lần ghi cuối.",
    "Vật tư thực dùng ghi theo lô hoặc số sê-ri, quét tem hoặc chọn lô trong kho, thêm vật tư ngoài định mức. Xuất hủy trừ kho ngay khi xác nhận.",
    "Máy dừng thì chạm một ô lý do, không cần xác nhận. Mọi đồng hồ dừng ngay, và chỉ tổ trưởng mới cho trạm chạy lại.",
    "Đóng lệnh ngay tại máy theo quy trình chuẩn, chọn tạo lệnh cho phần còn lại hay đóng luôn.",
    "Khi định mức không cho phép chênh lệch, công nhân sửa số hoặc gửi quản lý phê duyệt ngay trên màn hình.",
    "Tổ trưởng ghi nhận thay cho người khác, thấy trước ảnh hưởng đến chi phí nhân công.",
    "Chi phí nhân công tính theo đơn giá giờ của từng người, chốt lại khi xong việc. Thời gian dừng máy không tính vào giá thành.",
    "Báo cáo Bản ghi xưởng lưu mọi lần ghi: ai ghi, ghi cho ai, đã hoàn tác hay ghi thay.",
    "Mở xưởng ngay từ thẻ trung tâm sản xuất trên máy tính. Cài thêm Chất lượng hoặc Bảo trì là kiểm tra chất lượng và gọi thợ sửa máy ngay trên cùng máy tính bảng.",
    "Điều hành xưởng sản xuất, dùng được từ bản Viindoo 18. Xem chi tiết và mua trên Viindoo Apps.",
]
CAPS = [
    "Mới, từ bản Viindoo 18",
    "Hết cảnh ghi sổ cuối ca",
    "Một máy, nhiều người dùng",
    "Bảng công việc theo trạm",
    "Bấm được khi đeo găng",
    "Ghi thành phẩm theo lô",
    "Vật tư thực dùng",
    "Dừng máy có lý do",
    "Đóng lệnh tại máy",
    "Chênh lệch phải được duyệt",
    "Ghi thay, rõ người làm",
    "Nhân công theo từng người",
    "Mọi lần ghi đều truy được",
    "Mở rộng: Chất lượng, Bảo trì",
    "Điều hành xưởng sản xuất<br>từ bản Viindoo 18",
]

PLAN = {
    0: [("hook", None, None, {})],
    1: [("photo", "ghi-so-giay-to.jpg", None, {"pos": {"sq": "45% 40%", "v": "42% 40%"}, "tag": CAPS[1]})],
    2: [("phone", "choose.jpg", None, {})],
    3: [("shot", "jobboard.jpg", None, {"zoom": [("tabs", "sẵn sàng")]})],
    4: [("phone", "start.jpg", None, {})],
    5: [("phone", "output.jpg", None, {"zoom": ("numpad", "bàn phím số")}),
        ("phone", "undo.jpg", "ghi nhầm", {})],
    6: [("phone", "materials.jpg", None, {"zoom": ("badges", "theo lô")}),
        ("phone", "scrap.jpg", "xuất hủy", {})],
    7: [("phone", "stop.jpg", None, {"zoom": ("tiles", "một ô lý do")}),
        ("phone", "restart.jpg", "chỉ tổ trưởng", {})],
    8: [("phone", "close.jpg", None, {})],
    9: [("phone", "approval.jpg", None, {"zoom": ("diff", "gửi quản lý")})],
    10: [("phone", "behalf.jpg", None, {})],
    11: [("shot", "labour.jpg", None, {"fit": True})],
    12: [("shot", "entries.jpg", None, {"fit": True, "zoom": [("filters", "ai ghi")]})],
    13: [("shot", "desktop.jpg", None, {"fit": True, "zoom": [("card", "thẻ trung tâm")]}),
         ("phone", "maint.jpg", "cài thêm", {})],
    14: [("cta", None, None, {})],
}
