"""Dựng kịch bản lắp clip cụm BÁN HÀNG + CRM (chép khuôn cụm Trao đổi thông tin). Hai thanh bước: Phần 1 bảy chặng hành trình khách, Phần 2 bốn mặt bộ máy.

(Ghi chú gốc của khuôn:) Dựng kịch bản lắp clip cụm TRAO ĐỔI THÔNG TIN VÀ PHỐI HỢP - chuẩn forwarder.

Chép khuôn cụm Dự án (`Du-An/clips/build_seq.py`): cảnh màn hình là BẢN QUAY THẬT, không
đi qua engine; cảnh đồ hoạ đi qua `sequence.mjs`. Sinh hai tệp:
  1. `$VIINDOO_VIDEO_WORKDIR/motion/seq/seq-<cụm>-fw.json` - các cảnh ĐỒ HOẠ cho `sequence.mjs`
  2. `clips/ke-hoach-lap.json`                    - thứ tự lắp đầy đủ cho `mix.sh`

Khác cụm Dự án ở ba chỗ:
  - **Thanh bước + nhãn "Chứng minh: ĐÚNG/XONG/NHỚ" trên mọi cảnh màn hình.** Cụm Dự án bỏ
    hai thứ này khi chuyển sang quay thật. Ở đây giữ lại đúng như cảnh `fwscreen` của bộ HRM:
    engine vẽ KHUNG (nền trắng, thanh bước sáng đúng bước, nhãn chứng minh, dòng chú thích
    nhỏ) với ô màn hình để trống, rồi `mix.sh` đặt bản quay vào đúng ô đó. Thanh bước nằm
    NGOÀI màn hình - không đè chữ lên dữ liệu (luật "toàn khung, không đè chữ").
  - **Mỗi mảnh quay có thể khai cửa sổ riêng** (`tu`/`den`) và **vùng cắt** (`crop`, toạ độ
    trên khung 1920x1080) - cảnh Zalo phải phóng vào nhóm "Zalo" + luồng tin vì đầu thanh bên
    bản 19 còn chữ tiếng Anh.
  - **Bản quay ngắn hơn đoạn lời thì GIỮ KHUNG CUỐI** (`giu` giây) thay vì đòi quay lại -
    các màn này đứng yên ở trạng thái cuối nên giữ khung không lộ.

Mốc cảnh ĐO TỪ CHÍNH BẢN THU (đếm nhịp âm tiết rồi nắn vào khoảng nghỉ), không gõ tay.
Đổi bản thu là phải chạy lại file này VÀ render lại toàn bộ cảnh đồ hoạ.

Chạy:  python3 build_seq.py --dry   -> chỉ in bảng thời lượng
       python3 build_seq.py         -> hai tệp trên + các khung PNG (khung/)
       VOICE=<tệp.wav> python3 build_seq.py   -> dùng bản thu khác (thử)
"""
import base64, hashlib, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cau_hinh as CH  # đường dẫn + kết nối dùng chung, xem cau_hinh.py

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.environ.get("CLIP_LANG", "vi")
_hau = "-en" if LANG == "en" else ""
VOICE = os.environ.get("VOICE") or os.path.join(HERE, "voice", f"ban-hang-crm-{LANG}-fw.wav")
QUAY = os.path.join(HERE, "quay-fw" + _hau)
ANH = os.path.join(HERE, "mo-phong" + _hau)
KHUNG = os.path.join(HERE, "khung" + _hau)
OUT = os.path.join(CH.SEQ_DIR, f"seq-ban-hang-crm-fw{_hau}.json")
KE_HOACH = os.path.join(HERE, f"ke-hoach-lap{_hau}.json")
MOTION = CH.ENGINE

# Icon app: dùng chung kho của bộ HRM (một bộ icon, không chép thành bản thứ hai).
APPS = os.path.join(HERE, "assets", "apps")  # icon that cua module: curl $BASE/<module>/static/description/icon.png
ic = lambda n: os.path.normpath(os.path.join(APPS, n + ".png"))
# (09/11/2026) bỏ ảnh hoạt hình người ngập giấy tờ - cảnh nỗi đau giờ là người thật (quay-fw/noi-dau.webm)


def L(vi, en):
    """Mọi chuỗi hiện trên màn PHẢI đi qua hàm này (bẫy số 1 của bản ngôn ngữ thứ hai)."""
    return en if LANG == "en" else vi


# Phần 1: hành trình bảy chặng của MỘT khách; Phần 2: bốn mặt của bộ máy
STEPS1 = [L("Biết đến", "Discover"), L("Hỏi", "Ask"), L("Báo giá", "Quote"), L("Nhận hàng", "Receive"),
          L("Thanh toán", "Pay"), L("Hỗ trợ", "Support"), L("Mua lại", "Buy again")]
STEPS2 = [L("Tổ chức", "Organisation"), L("Tiếp thị", "Marketing"), L("Quản lý", "Management"), L("Hỗ trợ", "Support")]  # EN khop loi doan 14 de bat moc
STEPS = STEPS1
QUAY_FW = QUAY
WEB = os.path.join(HERE, "assets", f"khach-{LANG}.mp4")   # vi du: doan quay khach dien form Lien he tren website (lay tu clip Docs, 1600x900)
SANKEY = os.path.join(QUAY, "c16-sankey-viindoo-cat.mp4")       # so do chuyen doi tren he thong Viindoo that
# Ban EN (09/11): ban quay tren Viindoo noi bo co nhan giai doan tieng Viet va can Lien dang nhap ->
# dung ban quay tren demo (action 1110, ten giai doan dich duoc) - quay-fw-en/c16-sankey.webm
SANKEY_EN = LANG == "en"
AICHAT = os.path.join(QUAY, "c06-ai-chat-cat.mp4")               # tro ly AI that tren viindoo.com (da cat doan cho)
K1 = lambda b: (b, 1)
K2 = lambda b: (b, 2)

# 29 cảnh (09/11/2026: thêm bán thêm, phân quyền, công nợ NVKD, tổng thể, tra 360 độ), ĐÚNG THỨ TỰ với SCENES trong tts_vi_fw.py (bảng cảnh mục 2 của kịch bản).
#   src dạng {"tep": <đường dẫn tuyệt đối>, "tu", "den"} -> tệp ngoài quay-fw, cửa sổ khai tay
CANH = [
    dict(kind="quay", src=[dict(ten="mo-dau", dau=True, tu=0.0)]),                         # 0 mở đầu người thật
    dict(kind="quay", chuyen_y=True, src=[dict(ten="noi-dau", dau=True, tu=0.0)]),        # 1 nỗi đau: người thật + chữ (dung_noi_dau.py)
    dict(kind="engine", scene="fwtitle", data={                                     # 2 thẻ tên
        "icon": ic("crm"), "name": L("Bán hàng và CRM", "Sales and CRM"),
        "sub": L("Khách ở lại, doanh nghiệp lớn lên", "Customers stay, the business grows")}),
    dict(kind="engine", scene="fwtwo", cues=L(["Khách ở lại", "Doanh nghiệp lớn lên"], ["Customers stay", "The business grows"]), data={
        "kicker": L("Hai hướng của câu chuyện", "Two sides of the story"),
        "headline": L("Khách ở lại, doanh nghiệp lớn lên", "Customers stay, the business grows"),
        "pillars": [
            {"tag": L("Khách ở lại", "Customers stay"), "title": L("Phục vụ liền mạch trọn đời", "Served seamlessly for life"),
             "note": L("Từ lần hỏi đầu tiên tới lần mua lại", "From the first question to the next order")},
            {"tag": L("Doanh nghiệp lớn lên", "The business grows"), "title": L("Bộ máy mở rộng, quản bằng số", "A sales machine that scales, run by numbers"),
             "note": L("Tổ chức, tiếp thị, quản lý, hỗ trợ", "Organise, market, manage, support")}]}),
    dict(kind="engine", scene="fwsteps", data={                                     # 4 bảy chặng
        "kicker": L("Một khách, bảy chặng", "One customer, seven stages"),
        "steps": [{"label": x} for x in STEPS1]}),
    dict(kind="quay", khung=K1(0), src=[dict(ten="c05-ho-so-mong", tu=4.0)]),       # 5 hồ sơ mỏng
    dict(kind="quay", khung=K1(1), src=[                                            # 6 hỏi: Zalo, web, AI, nhận ra khách cũ
        dict(ten="zalo", crop=(320, 180, 1600, 900)),
        dict(tep=WEB, tu=14.0, den=21.0),
        dict(tep=AICHAT, tu=7.5, den=16.4, crop=(945, 540, 960, 540)),
        dict(ten="c06-nhan-ra-khach")]),
    dict(kind="quay", khung=K1(2), src=[dict(ten="c07-bao-gia-ngoai", tu=6.0, den=12.0),   # 7 báo giá
                                        dict(ten="c07-bao-gia-ngoai")]),
    dict(kind="quay", khung=K1(3), src=[dict(ten="c08-nhan-hang", tu=3.0)]),        # 8 nhận hàng
    dict(kind="quay", khung=K1(4), src=["c09-thanh-toan"]),                          # 9 thanh toán
    dict(kind="quay", khung=K1(5), src=[dict(ten="c10-ho-tro", tu=24.5)]),  # 10 hỗ trợ
    dict(kind="quay", khung=K1(6), src=[dict(ten="c11-diem-thuong", tu=5.0)]),                         # 11 mua lại
    dict(kind="quay", khung=K1(6), src=[dict(ten="c27-ban-them", tu=4.0, den=16.5),      # 12 MỚI bán thêm: tab Sản phẩm tùy chọn
                                        dict(ten="c27-ban-them-portal", tu=1.0)]),  #    -> khách bấm thêm trên báo giá trực tuyến
    dict(kind="quay", khung=K1(6), src=[dict(ten="c24-ho-so-day", tu=2.4, den=10.5)]),  # 13 hồ sơ dày
    dict(kind="engine", scene="fwsteps", data={                                     # 14 chuyển ý: bốn mặt bộ máy
        "kicker": L("Doanh nghiệp lớn lên: bộ máy bốn mặt", "The business grows: a machine with four sides"),
        "steps": [{"label": x} for x in STEPS2]}),
    dict(kind="quay", khung=K2(0), src=["c14-doi", "c14-vung"]),                     # 15 vùng, đội
    # cửa sổ đo trên TỪNG bản quay - bản EN (09/11) chuyển người nhanh hơn: đo lại bằng lưới khung 3 giây
    dict(kind="quay", khung=K2(0), src=[dict(ten="c26-phan-quyen", tu=L(5.0, 5.0), den=L(15.5, 11.7)),   # 16 MỚI phân quyền: nhân viên
                                        dict(ten="c26-phan-quyen", tu=L(16.5, 12.6), den=L(24.3, 18.9)),  #    trưởng đội
                                        dict(ten="c26-phan-quyen", tu=L(25.5, 19.9), den=L(33.2, 26.5)),  #    giám đốc khu vực
                                        dict(ten="c26-phan-quyen", tu=L(34.0, 27.4), den=L(42.6, 37.4))]),  #  người marketing  (EN 09/11: cửa sổ đo lại theo khoảng trắng lúc nạp trang 11.8-12.4, 19.0-19.8, 26.6-27.2)
    dict(kind="quay", khung=K2(0), src=[dict(ten="c15-tu-chia", tu=8.0, den=L(21.0, 18.5)),   # 17 tự chia (EN: từ 19s là màn chờ trống)
                                        dict(ten="c15-tu-chia")]),
    dict(kind="quay", khung=K2(1), src=[dict(ten="c16-sankey") if SANKEY_EN else dict(tep=SANKEY, tu=0.0, den=7.2, dau=True)]),  # 18 chuyển đổi
    dict(kind="quay", khung=K2(1), src=["c17-crm-dash", "c17-pheu"]),  # 17
    dict(kind="quay", khung=K2(2), src=["c18-chi-tieu"]),                            # 20 chỉ tiêu
    dict(kind="quay", khung=K2(2), src=["c19-phan-tich"]),                           # 21 phân tích
    dict(kind="quay", khung=K2(2), src=["c20-han-muc", "c20-duyet"]),                # 22 luật
    dict(kind="quay", khung=K2(2), src=[dict(ten="c28-cong-no-nvkd", tu=L(25.0, 26.8), den=L(32.8, 31.4)),  # 23 MỚI đơn của tôi theo giao hàng
                                        dict(ten="c28-cong-no-nvkd", tu=L(34.0, 32.6))]),          #    công nợ khách của tôi
    dict(kind="quay", khung=K2(3), src=["c21-ho-tro-dash"]),                         # 24 bảng hỗ trợ
    dict(kind="quay", khung=K2(3), src=["c22-bao-hanh"]),                            # 25 bảo hành
    dict(kind="engine", scene="fwcycle", data={                                     # 26 MỚI tổng thể: khách ở trung tâm
        "kicker": L("Giải pháp tổng thể", "One complete solution"),
        "headline": L("Khách hàng ở trung tâm", "The customer at the centre"),
        "center": {"title": L("Khách hàng", "Customer"), "note": L("Một hồ sơ cho mọi phòng ban", "One record for every team")},
        "steps": [
            {"label": L("Kinh doanh", "Sales"), "note": L("Báo giá, đơn, chiết khấu", "Quotes, orders, discounts")},
            {"label": L("Marketing", "Marketing"), "note": L("Nguồn khách, chiến dịch", "Sources, campaigns")},
            {"label": L("Kho", "Warehouse"), "note": L("Địa chỉ và lịch giao", "Delivery address and dates")},
            {"label": L("Kế toán", "Accounting"), "note": L("Hoá đơn, công nợ", "Invoices, receivables")},
            {"label": L("Hỗ trợ", "Support"), "note": L("Yêu cầu, cam kết thời gian", "Tickets, response times")},
            {"label": L("Bảo hành", "Warranty"), "note": L("Phiếu theo sản phẩm", "Claims by product")}],
        "loopLabel": L("Mua lại", "Buys again")}),
    dict(kind="quay", khung=K1(6), src=[dict(ten="c25-tra-360", tu=2.8, den=6.4),      # 27 MỚI tra 360 độ trong Danh bạ
                                        dict(ten="c25-tra-360", tu=6.2)]),
    dict(kind="engine", scene="fwcta", data={                                       # 28 kêu gọi
        "sub": L("Khách ở lại, doanh nghiệp lớn lên.", "Customers stay, the business grows."),
        "button": L("Đặt lịch tư vấn", "Book a consultation"), "url": "https://viindoo.com/"}),
]

# B-roll người thật (Pexels, $VIINDOO_VIDEO_WORKDIR/broll/ban-hang-crm/NGUON.md), mượn ĐUÔI cảnh đứng trước.
# Chỉ đặt sau cảnh đồ hoạ có câu cuối là câu CHUNG:
#   15 - sau chuyển ý bốn mặt bộ máy: trưởng nhóm trình bày trước đội
#   27 - sau tổng thể ("...không phải bắt đầu lại ở bất kỳ khâu nào."): bắt tay
BROLL = {15: "hop-doi", 27: "bat-tay"}   # 09/11: bỏ b-roll sau nỗi đau (cảnh nỗi đau giờ đã là người thật)
BROLL_DIR = os.path.join(CH.BROLL, "ban-hang-crm")
GIU_KET = 3.0

try:
    CUA_SO = json.load(open(os.path.join(QUAY, "cua-so.json")))
except FileNotFoundError:
    sys.exit("thiếu quay-fw/cua-so.json - chạy do_duoi.py trước")


def cua_so(ten):
    c = CUA_SO.get(ten)
    if c is None:
        sys.exit(f"chưa đo cửa sổ cho bản quay {ten} - chạy lại do_duoi.py")
    that = duration(os.path.join(QUAY, ten + ".webm"))
    if c["het"] > that + 0.05:
        sys.exit(f"cua-so.json ĐÃ CŨ cho {ten} - quay lại rồi thì PHẢI đo lại (do_duoi.py)")
    return c["bat_dau"], c["het"]


# ---- KHUNG có thanh bước (cùng công thức với fwscreen.js) -------------------------
def _trang():
    import io
    from PIL import Image
    buf = io.BytesIO(); Image.new("RGB", (16, 9), "white").save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


TRANG = _trang()


def o_man(co_chu_thich):
    """Ô màn hình trong khung: đúng phép tính của fwscreen.js (có thanh bước, không kéo số)."""
    avail_w, avail_h = 1780, (830 if co_chu_thich else 892)
    w, h = avail_w, round(avail_w * 1080 / 1920)
    if h > avail_h:
        h = avail_h; w = round(h * 1920 / 1080)
    return {"x": round((1920 - w) / 2), "y": 164, "w": w, "h": h}


def lam_khung(buoc, phan=1, chu_thich=None):
    os.makedirs(KHUNG, exist_ok=True)
    steps = STEPS1 if phan == 1 else STEPS2
    ten = f"p{phan}-buoc{buoc}" \
          f"{'-ct' + hashlib.md5(chu_thich.encode()).hexdigest()[:6] if chu_thich else ''}.png"
    dich = os.path.join(KHUNG, ten)
    data = {"steps": steps, "active": buoc, "shot": TRANG}
    if chu_thich:
        data["caption"] = chu_thich
    if not os.path.exists(dich) or "--khung" in sys.argv:
        tam = dich[:-4] + ".json"
        json.dump(data, open(tam, "w", encoding="utf-8"), ensure_ascii=False)
        subprocess.run(["node", "frameshot.mjs", "--scene", "fwscreen", "--data", tam,
                        "--out", dich], cwd=MOTION, check=True, capture_output=True)
        os.remove(tam)
    return {"anh": dich, "o": o_man(bool(chu_thich))}


def dem_am_tiet(doan):
    """Số ÂM TIẾT của một đoạn - phải khớp với cái `nhip_am_tiet()` đếm được trên file tiếng.

    Tiếng Việt đơn âm nên mỗi từ là một âm tiết. Tiếng Anh thì không: "recruitment" là ba
    âm tiết, "and" là một - đếm theo từ sẽ lệch, và lệch dồn lại thành 2-4 giây (đo 20/10,
    mốc các đoạn đều sớm hơn thực tế). Với tiếng Anh đếm theo CỤM NGUYÊN ÂM.
    """
    if LANG != "en":
        return len(doan.split())
    tong = 0
    for tu in re.findall(r"[a-zA-Z']+", doan.lower()):
        nhom = re.findall(r"[aeiouy]+", tu)
        n = len(nhom)
        if tu.endswith("e") and n > 1 and not tu.endswith(("le", "ee", "ye")):
            n -= 1                      # "e" câm cuối từ
        tong += max(1, n)
    return tong


def moc_loi(doan, cum_tu, dai_doan):
    """Giọng đọc tới cụm từ này vào GIÂY THỨ MẤY của đoạn (chia theo vị trí âm tiết).

    Liên 19/10: "dòng chảy đang nhanh hơn giọng đọc". Trước đây các bước/thẻ hiện ra theo
    nhịp cố định, xong sạch trong 4 giây trong khi giọng còn đọc tiếp 5 giây nữa. Giờ mỗi
    phần chờ đúng lúc giọng gọi tên nó.
    """
    tu = doan.lower().split()
    can = cum_tu.lower().split()
    for k in range(len(tu) - len(can) + 1):
        if [re.sub(r"[^0-9a-zà-ỹđ]", "", x) for x in tu[k:k + len(can)]] == \
           [re.sub(r"[^0-9a-zà-ỹđ]", "", x) for x in can]:
            return round(max(0.0, k / max(len(tu), 1) * dai_doan - 0.35), 2)
    return None


def narration():
    import importlib.util
    spec = importlib.util.spec_from_file_location("tts", os.path.join(HERE, f"tts_{LANG}_fw.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.SCENES


def silences(path):
    """Các khoảng lặng thật trong file tiếng -> dùng để nắn ranh giới cảnh."""
    p = subprocess.run(["ffmpeg", "-i", path, "-af", "silencedetect=n=-34dB:d=0.28",
                        "-f", "null", "-"], capture_output=True, text=True)
    out, cur = [], None
    for ln in p.stderr.splitlines():
        a = re.search(r"silence_start: ([\d.]+)", ln)
        b = re.search(r"silence_end: ([\d.]+)", ln)
        if a: cur = float(a.group(1))
        elif b and cur is not None:
            out.append((cur, float(b.group(1)))); cur = None
    return out


def duration(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(p.stdout.strip())


def nhip_am_tiet(path):
    """Thời điểm từng NHỊP ÂM TIẾT trong file tiếng.

    Tiếng Việt đơn âm: mỗi âm tiết là một nhịp năng lượng. Đếm nhịp thì biết giọng đã đọc
    tới chữ thứ mấy - chính xác hơn hẳn chia đều theo thời gian.

    (Đã thử và BỎ hai cách khác: nắn theo khoảng lặng thì nghỉ giữa câu lẫn với nghỉ giữa
     đoạn, lệch 7-34 giây; hỏi mô hình mốc thời gian thì nó trả cả mốc 245 giây cho file
     dài 169 giây. Chi tiết: mục D của SSOT nguyên tắc video.)
    """
    import wave
    import numpy as np
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    x /= 32768.0
    hop, win = int(0.01 * sr), int(0.025 * sr)
    e = np.array([np.sqrt((x[i:i + win] ** 2).mean()) for i in range(0, len(x) - win, hop)])
    k = np.hanning(9); k /= k.sum()
    s_ = np.convolve(e, k, mode="same")
    thr = s_.max() * 0.06
    nhip = []
    for i in range(1, len(s_) - 1):
        if s_[i] > thr and s_[i] >= s_[i - 1] and s_[i] > s_[i + 1]:
            if not nhip or (i - nhip[-1]) * 0.01 >= 0.11:
                nhip.append(i)
    return [i * 0.01 for i in nhip]


CUA = 5        # cửa sổ tìm khoảng nghỉ, tính bằng nhịp âm tiết
CUA_RONG = 24  # cửa sổ nới ra khi quanh vị trí ước lượng không có chỗ nghỉ
PHAT = 0.05    # phạt mỗi nhịp lệch khỏi vị trí ước lượng (giây)


def khe_nghi(nhip, i):
    """Độ dài khoảng nghỉ NGAY TRƯỚC nhịp thứ i."""
    return nhip[i] - nhip[i - 1]


def boundaries(text_scenes, total, sil, voice=None):
    """Ranh giới giữa các đoạn - đặt vào GIỮA khoảng nghỉ, tính theo NHỊP ÂM TIẾT.

    KHÔNG dò khe lặng bằng ngưỡng dB cố định nữa. Đo 31/10/2026 trên bản thu 242,9s:
    `silencedetect=-34dB` tìm được 42 khe nhưng KHÔNG CÓ KHE NÀO sau giây 152 - nửa
    sau bài giọng đọc liền hơi hơn nên nền không bao giờ xuống dưới ngưỡng. Hậu quả:
    **20 trên 25 mốc cảnh cắt đúng lúc giọng đang đọc dở** - Liên nghe ra ngay
    ("rất nhiều cảnh lời chưa đọc xong đã chuyển cảnh"). Hạ ngưỡng xuống -38dB còn
    tệ hơn: 0 khe sau giây 123.

    Nhịp âm tiết là phép đo TƯƠNG ĐỐI (đỉnh năng lượng so với đỉnh lớn nhất) nên
    không dính bẫy đó: cùng bản thu ấy nó bắt được 1043 nhịp cho 1035 âm tiết (101%),
    và khoảng nghỉ rải đều cả bài. Khoảng nghỉ = quãng cách giữa hai nhịp liền nhau.
    """
    syl = [dem_am_tiet(t) for t in text_scenes]
    tong = sum(syl)
    nhip = nhip_am_tiet(voice) if voice else []

    if len(nhip) < tong * 0.75:          # đếm hụt quá thì đành chia theo tỉ lệ
        acc, s = [], 0
        for n in syl[:-1]:
            s += n
            acc.append(total * s / tong)
        return [(x, False) for x in acc]

    # Đi lần lượt từng mốc, mỗi lần chọn xong thì NẮN LẠI ĐIỂM NEO cho phần còn lại
    # (sai số đếm nhịp dồn lại tới ~1%; neo cố định thì cuối bài lệch 8-10 nhịp).
    out, truoc, nhip_con, syl_con = [], 0, len(nhip), tong
    for n in syl[:-1]:
        j = max(1, min(truoc + round(n * nhip_con / syl_con), len(nhip) - 1))
        # Chọn khoảng nghỉ trong cửa sổ ±5 nhịp, nhưng PHẠT theo khoảng cách: nếu
        # chỉ lấy "khe dài nhất" thì mốc với sang câu bên cạnh để vồ khe to hơn
        # (đo 31/10: cửa sổ ±8 không phạt làm nhịp đọc lệch 3,4 lần giữa các đoạn).
        def tim(cua):
            tot, diem = None, -9e9
            for k in range(max(truoc + 1, j - cua), min(j + cua + 1, len(nhip))):
                d = khe_nghi(nhip, k) - PHAT * abs(k - j)
                if d > diem:
                    tot, diem = k, d
            return tot

        tot = tim(CUA)
        # Quanh đây không có chỗ nghỉ nào tử tế -> nới cửa sổ. Mốc rơi vào khe
        # ngắn hơn 0,40s thì chỉ cách âm tiết liền kề ~0,1s, tai nghe ra là cắt
        # ngang tiếng. Phạt theo khoảng cách vẫn giữ cho nó không với đi quá xa.
        if tot is None or khe_nghi(nhip, tot) < 0.55:
            tot2 = tim(CUA_RONG)
            if tot2 is not None and khe_nghi(nhip, tot2) > khe_nghi(nhip, tot or j):
                tot = tot2
        if tot is None:
            tot = j
        # Cắt vào GIỮA khoảng nghỉ: chắc chắn sau âm tiết cuối của đoạn này, trước
        # âm tiết đầu của đoạn sau. Chừa tối thiểu 0,22s cho âm tiết cuối tắt hẳn.
        t = (nhip[tot - 1] + nhip[tot]) / 2
        t = min(max(t, nhip[tot - 1] + 0.22), nhip[tot] - 0.12)
        out.append(round(t, 2))
        nhip_con -= tot - truoc
        syl_con -= n
        truoc = tot

    # Thử lại: nhịp đọc của các đoạn phải xấp xỉ nhau. Lệch quá 2,2 lần nghĩa là
    # có mốc bắt nhầm sang câu khác.
    moc = [0.0] + out + [total]
    nd = [syl[i] / max(moc[i + 1] - moc[i], 0.1) for i in range(len(syl))]
    if max(nd) / min(nd) > 2.2:
        sys.exit(f"mốc cảnh bắt nhầm: nhịp đọc lệch {max(nd)/min(nd):.1f} lần "
                 f"(nhanh nhất {max(nd):.1f}, chậm nhất {min(nd):.1f} âm tiết/giây)")

    return [(t, True) for t in out]


def main():
    texts = narration()
    if len(texts) != len(CANH):
        sys.exit(f"lệch bảng: {len(texts)} đoạn lời / {len(CANH)} cảnh")
    tong = duration(VOICE)
    bd = boundaries(texts, tong, silences(VOICE), VOICE)
    marks = [0.0] + [t for t, _ in bd] + [tong]

    seq = {"width": 1920, "height": 1080, "fps": 60, "scenes": []}
    ke_hoach, giu_khung = [], []
    print(f"{'#':>3}  {'kiểu':7} {'dài':>7}  nguồn")
    print("-" * 78)
    for i, c in enumerate(CANH):
        dai = round(marks[i + 1] - marks[i], 2)
        dai_loi = dai                      # độ dài THẬT của đoạn lời - mốc hiện thẻ/bước tính theo số này
        if i == len(CANH) - 1:             # màn kết: giữ thêm sau khi lời dứt, nhạc ngân (mix.sh đệm lặng)
            dai = round(dai + GIU_KET, 2)
        ghi = ""
        if i + 1 in BROLL:                 # cảnh sau có b-roll -> cảnh này nhường đuôi
            if c["kind"] == "quay" and not c.get("chuyen_y"):   # chuyen_y: cảnh quay chỉ để chuyển ý
                sys.exit(f"cảnh {i} là cảnh DỮ LIỆU - không được nhường đuôi cho b-roll")
            ten = BROLL[i + 1]
            bdai = duration(os.path.join(BROLL_DIR, ten + ".mp4"))
            dai = round(dai - bdai, 2)
            ghi = f"  (- {bdai:.1f}s nhường đuôi cho b-roll {ten})"
            if dai < 2.5:
                sys.exit(f"cảnh {i} còn {dai}s sau khi nhường b-roll - quá ngắn")
        khung = lam_khung(*c["khung"]) if c.get("khung") and "--dry" not in sys.argv else None

        if c["kind"] == "engine":
            d = dict(c["data"])
            if c["scene"] == "fwsteps":
                mocs = [moc_loi(texts[i], b["label"], dai) for b in d["steps"]]
                if all(m is not None for m in mocs):
                    d["cueTimes"] = mocs
                else:
                    # Lời cảnh này KHÔNG đọc tên từng bước ("chín chặng") mà chỉ dài ~4s:
                    # nhịp mặc định 0,42s/bước cần 4,4s nên hai bước cuối không kịp hiện.
                    # Rải đều các bước cho XONG trước cuối cảnh 0,8s.
                    n = len(d["steps"])
                    d["cueTimes"] = [round(0.3 + k * max(dai - 1.6, 1.0) / max(n - 1, 1), 2)
                                     for k in range(n)]
            if c["scene"] == "fwtwo" and c.get("cues"):
                # Liên 05/11 "từ giây 20 giọng chậm hơn màn hình, không khớp 3 trụ": trước đây chia theo
                # `dai` ĐÃ trừ phần nhường b-roll -> thẻ hiện sớm. Chia theo độ dài đoạn lời thật.
                mocs = [moc_loi(texts[i], q, dai_loi) for q in c["cues"]]
                if any(m is not None and m > dai - 0.6 for m in mocs):
                    sys.exit(f"cảnh {i}: lời gọi tên thẻ rơi vào phần đã nhường b-roll - bỏ b-roll sau cảnh này")
                if all(m is not None for m in mocs):
                    d["cueTimes"] = mocs
                else:
                    print(f"  (cảnh {i}: không bắt được mốc lời cho thẻ, dùng nhịp mặc định)")
            ten_seg = f"seg{len(seq['scenes']):02d}"
            seq["scenes"].append({"scene": c["scene"], "data": d, "duration": dai})
            ke_hoach.append({"canh": i, "kieu": "seg", "ten": ten_seg, "dai": dai})
            nguon = c["scene"]
        elif c["kind"] == "quay":
            srcs = [x if isinstance(x, dict) else {"ten": x} for x in c["src"]]
            phan = round(dai / len(srcs), 2)
            for k, s_ in enumerate(srcs):
                if s_.get("tep"):
                    tep = s_["tep"]
                    s_.setdefault("ten", os.path.basename(tep).rsplit(".", 1)[0])
                    a, b = s_["tu"], s_["den"]
                else:
                    tep = os.path.join(QUAY, s_["ten"] + ".webm")
                    if not os.path.exists(tep):
                        sys.exit(f"thiếu bản quay {tep}")
                    a, b = cua_so(s_["ten"])
                # `tu` khai tay ĐÈ cửa sổ đo máy: do_duoi.py lấy dải trên cùng làm mốc nên với cảnh
                # CUỘN biểu mẫu (dải trên trôi theo) nó báo bắt đầu quá muộn - đã soát bằng mắt.
                a = s_.get("tu", a)
                b = min(b, s_.get("den", b))
                dung = round(b - a, 2)
                m = {"canh": i, "kieu": "quay", "ten": s_["ten"], "tep": tep, "dai": phan}
                if s_.get("dau") and dung >= phan:   # màn mở đầu: LẤY TỪ ĐẦU để giữ nhịp chữ hiện dần
                    m["bat_dau"] = round(a, 2)
                elif dung >= phan:
                    m["bat_dau"] = round(b - phan, 2)       # LẤY PHẦN ĐUÔI
                else:                                       # ngắn hơn lời -> giữ khung cuối
                    m["bat_dau"], m["giu"] = round(a, 2), round(phan - dung, 2)
                    giu_khung.append(f"  cảnh {i} {s_['ten']}: giữ khung cuối {m['giu']:.2f}s")
                if s_.get("crop"):
                    m["crop"] = s_["crop"]
                if khung:
                    m["khung"] = khung
                ke_hoach.append(m)
            nguon = " + ".join(x["ten"] for x in srcs)
        else:                               # anh
            phan = round(dai / len(c["src"]), 2)
            for s_ in c["src"]:
                if not os.path.exists(s_):
                    sys.exit(f"thiếu ảnh {s_}")
                m = {"canh": i, "kieu": "anh", "ten": os.path.basename(s_)[:-4], "tep": s_,
                     "dai": phan}
                if khung:
                    m["khung"] = khung
                ke_hoach.append(m)
            nguon = " + ".join(os.path.basename(x) for x in c["src"])
        print(f"  {i:3}  {c['kind']:7} {dai:6.2f}s  {nguon}{ghi}")

    day_du, da_chen = [], set()
    for m in ke_hoach:
        if m["canh"] in BROLL and m["canh"] not in da_chen:
            ten = BROLL[m["canh"]]
            tep = os.path.join(BROLL_DIR, ten + ".mp4")
            day_du.append({"canh": m["canh"], "kieu": "broll", "ten": ten, "tep": tep,
                           "dai": round(duration(tep), 2)})
            da_chen.add(m["canh"])
        day_du.append(m)

    tong_hinh = sum(x["dai"] for x in day_du)
    broll = sum(x["dai"] for x in day_du if x["kieu"] == "broll")
    print("-" * 78)
    print(f"  tổng hình {tong_hinh:.1f}s / tiếng {tong:.1f}s  ({len(day_du)} mảnh, "
          f"{len(seq['scenes'])} cảnh đồ hoạ, b-roll {broll:.1f}s = {broll / tong * 100:.1f}%)")
    if giu_khung:
        print("\n".join(giu_khung))
    if "--dry" in sys.argv:
        return
    json.dump(seq, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(day_du, open(KE_HOACH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ghi", OUT)
    print("ghi", KE_HOACH)


if __name__ == "__main__":
    main()
