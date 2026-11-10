"""Đường dẫn và kết nối dùng chung cho mọi script trong clips/ - KHÔNG ghi cứng đường dẫn máy ai.

Mọi giá trị đọc từ biến môi trường, có mặc định hợp lý:
  VIINDOO_VIDEO_WORKDIR   thư mục làm việc (mặc định ~/viindoo-video)
  VIINDOO_VIDEO_ENGINE    thư mục engine motion của plugin viindoo-video
                          (tao_cum.sh ghi sẵn vào ENGINE_MAC_DINH dưới đây lúc tạo cụm)
  VIINDOO_DEMO_URL / VIINDOO_DEMO_LOGIN / VIINDOO_DEMO_PASSWORD   hệ thống demo để quay
  CHROME_PATH             Google Chrome thật (biểu đồ canvas chỉ quay ra đủ bằng Chrome thật)
  VIINDOO_FONT_BOLD       phông đậm cho phụ đề cháy vào hình (mặc định Montserrat của plugin)
  MUSIC                   tệp nhạc nền đã chọn cho clip này
"""
import os

ENGINE_MAC_DINH = "__ENGINE__"   # tao_cum.sh thay bằng <plugin>/engine

_x = os.path.expanduser
WORKDIR = _x(os.environ.get("VIINDOO_VIDEO_WORKDIR", "~/viindoo-video"))
ENGINE = _x(os.environ.get("VIINDOO_VIDEO_ENGINE", ENGINE_MAC_DINH))
SEQ_DIR = os.path.join(WORKDIR, "motion", "seq")      # seq-*.json build_seq.py sinh ra
OUTPUT = os.path.join(WORKDIR, "output")              # segment + video engine render
BROLL = os.path.join(WORKDIR, "broll")                # b-roll đã cắt, mỗi cụm một thư mục con
NHAC = os.path.join(WORKDIR, "Nhac-nen")              # thư viện nhạc nền + index.json
FONT_B = _x(os.environ.get("VIINDOO_FONT_BOLD") or os.path.join(
    os.path.dirname(ENGINE), "brand", "assets", "fonts", "Montserrat-VF.ttf"))
CHROME = os.environ.get("CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

DEMO_URL = os.environ.get("VIINDOO_DEMO_URL", "https://sanxuat18.viindoo.cloud")


def demo_login():
    """Tài khoản demo lấy từ biến môi trường, không bao giờ ghi vào tệp."""
    u, p = os.environ.get("VIINDOO_DEMO_LOGIN"), os.environ.get("VIINDOO_DEMO_PASSWORD")
    if not (u and p):
        raise SystemExit("thiếu VIINDOO_DEMO_LOGIN / VIINDOO_DEMO_PASSWORD (hỏi người quản lý hệ thống demo)")
    return u, p


for _d in (SEQ_DIR, OUTPUT):
    os.makedirs(_d, exist_ok=True)
