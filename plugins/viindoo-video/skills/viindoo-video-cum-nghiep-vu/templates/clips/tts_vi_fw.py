"""Lồng tiếng clip cụm BÁN HÀNG + CRM - tiếng Việt (chép khuôn cụm Trao đổi thông tin).

Hai vế: KHÁCH Ở LẠI (hành trình bảy chặng) - DOANH NGHIỆP LỚN LÊN (bộ máy bốn mặt).
Slogan: "Khách ở lại, doanh nghiệp lớn lên." Lời = mục 7 kịch bản. Clip làm chung mọi ngành;
nói về ngôn ngữ của khách thì dùng "ngôn ngữ", không dùng "tiếng" (Liên 08/11).

Chạy:  python3 tts_vi_fw.py --text   -> in lời, đếm âm tiết
       python3 pick_take.py 2        -> thu, chấm, giữ bản sạch nhất -> voice/kho-vi-fw.wav
"""
import base64
import json
import os
import re
import ssl
import struct
import sys
import urllib.request

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CTX = ssl.create_default_context()

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "voice")
MODEL = "gemini-2.5-flash-preview-tts"
VOICE = os.environ.get("VOICE_NAME", "Achird")   # cum Ban hang + CRM 09/11: Achird + cau lenh sang

# Mỗi phần tử = MỘT đoạn = MỘT cảnh. Thứ tự khớp bảng cảnh trong kịch bản.
SCENES = [
    # NHAP 10/11/2026 - cum Kho va chuoi cung ung, 28 doan theo bang canh; CHUA qua ChatGPT web.
    # Tranh chu may hay doc sai: ky thuat, nhac mieng, bat ky. So tru lay tu du lieu demo da bom (seed_kho.py).
    # 0
    'Kho báo còn một nghìn hai trăm cái. Nhưng một nghìn hai trăm cái đó đang giữ bao nhiêu tiền, và đã nằm đó bao lâu?',
    # 1
    'Hàng cần thì thiếu, hàng không cần thì chất đầy. Tiền của doanh nghiệp nằm im trong kho.',
    # 2
    'Viindoo Kho và Chuỗi cung ứng đưa hàng về đúng lúc cần.',
    # 3
    'Câu chuyện có hai vế: hàng đến đúng lúc, và không gì bị lãng phí.',
    # 4
    'Hãy theo chân một món hàng qua tám chặng: cần, đề nghị, duyệt, đặt mua, nhận và kiểm, cất kho, điều chuyển, rồi xuất.',
    # 5
    'Ắc quy trong kho còn bốn mươi, mức tối thiểu là một trăm. Hệ thống tính sẵn cần đặt bốn trăm, và đặt trước ngày nào để hàng về kịp.',
    # 6
    'Biểu đồ dự báo cho thấy trước ngày tồn chạm đáy, không phải đợi đến lúc hết hàng mới chạy đi mua.',
    # 7
    'Đại lý đặt ba mươi bộ sạc. Đơn bán vừa xác nhận đã tự sinh đơn mua. Có nhu cầu thật mới kéo hàng về.',
    # 8
    'Mỗi đề nghị mua đều qua người có quyền duyệt trước khi tiền được chi ra.',
    # 9
    'Giá chốt một lần trong hợp đồng khung, hàng gọi về thành nhiều đợt nhỏ, đúng lúc cần.',
    # 10
    'Mỗi nhà cung cấp có tỷ lệ giao đúng hẹn, biết ngay nhà nào giữ lời, nhà nào hay trễ.',
    # 11
    'Bộ điều khiển về kho đo được sáu mươi lăm vôn, dưới chuẩn bảy mươi. Phiếu kiểm không đạt, hàng không được nhập.',
    # 12
    'Thủ kho quét mã là hàng được nhận, không phải gõ lại từng dòng.',
    # 13
    'Dầu phanh chia ba lô, mỗi lô một hạn dùng. Lô nào gần hết hạn thì xuất trước.',
    # 14
    'Bốn mươi bộ bát phanh đang trên đường giữa hai kho, vẫn biết hàng ở đâu và đáng hai triệu tám trăm nghìn đồng.',
    # 15
    'Xuất kho cho sản xuất đúng lượng định mức, không xuất dư.',
    # 16
    'Máy quét, cân, dụng cụ đo dùng được ngay. RFID, băng chuyền, PLC kết nối theo thiết kế riêng của từng doanh nghiệp.',
    # 17
    'Hàng đã về đúng lúc. Việc tiếp theo là không để gì lãng phí.',
    # 18
    'Tồn kho được nói bằng tiền. Nhìn theo từng kho là thấy tiền đang nằm ở đâu.',
    # 19
    'Báo cáo tuổi tồn cho biết hàng nào đã nằm quá chín mươi ngày và đang giữ bao nhiêu tiền.',
    # 20
    'Tiền chở hàng về và thuế nhập khẩu được cộng thẳng vào giá vốn. Gần mười tám triệu chi phí của lô này nằm đúng trong giá từng món.',
    # 21
    'Một bảng số liệu nhìn toàn bộ tiền đang nằm trong kho.',
    # 22
    'Kiểm kê áo mưa đếm được năm mươi hai, máy ghi năm mươi tám. Lệch sáu cái, quy ra tiền ngay.',
    # 23
    'Hàng giao lỗi trả lại nhà cung cấp kèm lý do, có dấu vết để đòi đền.',
    # 24
    'Duyệt mua, duyệt lĩnh vật tư theo đúng luồng. Mỗi người chỉ làm đúng phần việc của mình.',
    # 25
    'Thẻ kho theo đúng mẫu quy định có sẵn, kế toán không phải làm lại.',
    # 26
    'Kho nối với mua hàng, bán hàng, sản xuất và kế toán trên cùng một dữ liệu.',
    # 27
    'Hàng đến đúng lúc, dòng vốn sinh lời. Đặt lịch tư vấn Viindoo ngay hôm nay.',
]


SAY = {"Viindoo": "Vin-đu", "AI": "Ây Ai"}  # "AI" de nguyen thi giong doc thanh chu "ai" (ai nhac?)   # Gemini doc "Vin du" o hau het cho; phu de van giu "Viindoo"

# Cau lenh giong de NGAN va dut khoat - ban dai lam may doc cham va deu (bai hoc bo HRM).
STYLE = ("Đọc bằng giọng nam trẻ, CHUẨN GIỌNG HÀ NỘI. Giọng CHẮC, KHOẺ, ĐẦY HƠI, vang và "
         "tự tin, như người cầm trịch một buổi báo cáo. TÔNG SÁNG, hơi cao - không trầm, "
         "không rè. Mỗi câu đọc TRỌN HƠI rồi mới nghỉ; lấy hơi ở dấu chấm, KHÔNG hụt hơi, "
         "KHÔNG thều thào, KHÔNG nhỏ dần hay yếu đi ở cuối câu và cuối bài. "
         "NHỊP NHANH, gọn, dứt khoát - không kéo dài chữ, không ngân cuối câu. Giữ ĐỀU một "
         "nhịp và một mức hơi từ câu đầu đến câu cuối. Lên xuống rõ ràng, không đọc đều một cao độ. "
         "Đây là lời dẫn cho video giới thiệu cách bán hàng và giữ khách trong doanh nghiệp:\n\n")
# Cau lenh SANG (09/11): Lien che ban Fenrir "giong dam qua"; cau lenh tren nhan "CHAC, DAY HOI,
# cam trich bao cao" de keo giong xuong tram. Ban ngan theo cong thuc HRM (137 Hz Lien khen).
STYLE_SANG = ("Đọc bằng giọng nam trẻ, chuẩn giọng Hà Nội. Giọng SÁNG và VANG, tươi, KHOẺ, ĐỦ HƠI, "
              "nhịp RẤT NHANH; KHÔNG trầm, KHÔNG thều thào, KHÔNG hụt hơi:\n\n")
if os.environ.get("TTS_STYLE") == "sang":
    STYLE = STYLE_SANG


def loi_doc():
    t = "\n\n".join(SCENES)
    for k, v in SAY.items():
        t = t.replace(k, v)
    return t


spoken_text = loi_doc   # bi danh cho check_tts.py


def pcm_sang_wav(pcm, rate=24000, ch=1, width=2):
    hdr = b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVEfmt "
    hdr += struct.pack("<IHHIIHH", 16, 1, ch, rate, rate * ch * width, ch * width, width * 8)
    return hdr + b"data" + struct.pack("<I", len(pcm)) + pcm


SO_KHOI = 1       # thu lam may khoi; ranh gioi khoi LUON trung ranh gioi doan
NGHI_KHOI = 0.60  # giay im lang chen vao cho noi hai khoi

# NEN NHIP sau khi thu. Giong Gemini KHONG nghe lenh "doc nhanh": cau lenh da ghi
# "NHIP NHANH, gon, dut khoat" ma ban thu van ra 3,72 am tiet/giay (cham hon ca
# ban truoc do). Nen thoi gian bang atempo thi chac chan va GIU NGUYEN CAO DO,
# nen tong sang van con.
# Muc 1.32 do Lien chon 31/10/2026: nghe bon mau x1.00 / x1.12 / x1.22 / x1.32,
# chi noi hai muc cuoi "giong nhau" - tuc chenh 8% khong phan biet duoc bang tai,
# nen lay muc nhanh hon vi loi che goc la "giong bi cham qua".
NHIP = 1.12  # Lien 09/11 "toc do dang hoi cham" -> nhanh hon ~12% (atempo giu cao do)


def chia_khoi(n_khoi):
    """Chia SCENES thanh n_khoi doan lien tiep, can bang theo so am tiet."""
    syl = [dem_am_tiet(x) for x in SCENES]
    moi_khoi = sum(syl) / n_khoi
    khoi, dau, don = [], 0, 0
    for i, n in enumerate(syl):
        don += n
        if don >= moi_khoi * (len(khoi) + 1) and len(khoi) < n_khoi - 1:
            khoi.append((dau, i + 1)); dau = i + 1
    khoi.append((dau, len(SCENES)))
    return khoi


def _goi(key, giong, van_ban):
    body = {"contents": [{"parts": [{"text": STYLE + van_ban}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": giong}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=600, context=SSL_CTX) as r:
        res = json.load(r)
    try:
        return base64.b64decode(res["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    except Exception:
        sys.exit("phản hồi không có audio: " + json.dumps(res)[:400])


def _cat_im(pcm, rate=24000):
    """Bo im lang o hai dau mot khoi, de cho noi khong bi hut mot quang dai."""
    import array
    a = array.array("h"); a.frombytes(pcm)
    nguong = max(abs(x) for x in a) * 0.02
    dau = 0
    while dau < len(a) and abs(a[dau]) < nguong:
        dau += 1
    cuoi = len(a) - 1
    while cuoi > dau and abs(a[cuoi]) < nguong:
        cuoi -= 1
    # chua lai 0,06s hai dau cho tieng khong bi cut ngon
    chua = int(0.06 * rate)
    dau = max(0, dau - chua); cuoi = min(len(a) - 1, cuoi + chua)
    return a[dau:cuoi + 1].tobytes()


def thu(out_path=None, voice=None, so_khoi=SO_KHOI):
    """Thu ca bai, nhung chia lam `so_khoi` KHOI doc lien tiep roi noi lai.

    Vi sao khong thu mot hoi: mot bai 4 phut doc lien mot luot thi giong TROI
    DAN - Lien nghe ra ngay (31/10/2026: "doan dau doc cham doan sau nhanh thi
    lai nhu het hoi", "doan cuoi cam giac bi theu thao nhu het hoi"). Doi cau
    lenh giong khong chua duoc, vi van la mot luot doc dai.

    Khoi nho thi moi khoi bat dau lai bang hoi day, nen nhip va muc hoi deu hon.
    KHONG chia nho hon mot DOAN: ranh gioi khoi luon trung ranh gioi doan, de
    build_seq.py van dem nhip am tiet tren ca bai nhu cu. Cung KHONG va mot doan
    le (bai hoc bo HRM): doan doc rieng co ngu dieu khac han.
    """
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("thiếu GEMINI_API_KEY")
    giong = voice or VOICE
    import importlib.util as _ilu
    _sp = _ilu.spec_from_file_location("chot_tts", os.path.join(HERE, "chot_tts.py"))
    _ch = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_ch)
    _ch.ghi_nhan(giong, sum(dem_am_tiet(x) for x in SCENES))

    im = b"\x00\x00" * int(NGHI_KHOI * 24000)
    phan = []
    for k, (a, b) in enumerate(chia_khoi(so_khoi)):
        van_ban = "\n\n".join(SCENES[a:b])
        for cu, vo in SAY.items():
            van_ban = van_ban.replace(cu, vo)
        pcm = _cat_im(_goi(key, giong, van_ban))
        print(f"  khối {k + 1}/{so_khoi}: đoạn {a}-{b - 1}, "
              f"{len(pcm) / 2 / 24000:.1f} giây", flush=True)
        phan.append(pcm)

    os.makedirs(OUT_DIR, exist_ok=True)
    out = out_path or os.path.join(OUT_DIR, f"ban-hang-crm-vi-{giong.lower()}.wav")
    tho = out + ".tho.wav"
    with open(tho, "wb") as f:
        f.write(pcm_sang_wav(im.join(phan)))
    if abs(NHIP - 1.0) < 1e-6:
        os.replace(tho, out)
        return out
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tho,
                    "-af", f"atempo={NHIP}", out], check=True)
    os.remove(tho)
    return out


def dem_am_tiet(s):
    """Tieng Viet don am: moi 'tu' cach nhau bang khoang trang la mot am tiet.
    Bo dau cau, bo gach ngang dung lam dau ngat."""
    s = re.sub(r"[.,;:!?\"'()]", " ", s)
    s = re.sub(r"\s-\s", " ", s)
    return len([t for t in s.split() if t.strip()])


def in_loi():
    tong = 0
    print(f"{'#':>3}  {'âm tiết':>7}  {'~giây':>6}  lời")
    print("-" * 94)
    for i, s in enumerate(SCENES):
        n = dem_am_tiet(s)
        tong += n
        # nhip bo HRM: ~4,5 am tiet/giay
        print(f"{i:>3}  {n:>7}  {n/4.5:>6.1f}  {s[:62]}{'...' if len(s) > 62 else ''}")
    print("-" * 94)
    print(f"     {tong:>7}  {tong/4.5:>6.1f}  TỔNG  (bộ HRM: 769 âm tiết -> 169,5 giây)")
    if tong < 700:
        print(f"\n  ngắn hơn chuẩn {700-tong} âm tiết - cân nhắc nới thêm một hai câu")
    elif tong > 820:
        print(f"\n  dài hơn chuẩn {tong-820} âm tiết - cân nhắc cắt bớt")
    else:
        print("\n  nằm trong tầm 700-820 âm tiết, khớp thời lượng bộ HRM")
    return tong


if __name__ == "__main__":
    if "--text" in sys.argv:
        in_loi()
        sys.exit(0)
    in_loi()
    import subprocess
    out = thu()
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(f"\nxong: {out}  ({float(d):.1f} giây)  giọng {VOICE}")
    print("Giọng TTS tiếng Việt KHÔNG ổn định - soát bằng check_tts.py trước khi dựng.")
