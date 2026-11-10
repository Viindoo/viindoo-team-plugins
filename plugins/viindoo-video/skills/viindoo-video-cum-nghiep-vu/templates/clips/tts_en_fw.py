"""Lồng tiếng clip cụm BÁN HÀNG + CRM - TIẾNG ANH (chép từ tts_vi_fw.py, 29 đoạn khớp bản Việt đã đăng 09/11).

Hai vế: KHÁCH Ở LẠI (hành trình bảy chặng) - DOANH NGHIỆP LỚN LÊN (bộ máy bốn mặt).
Slogan: "Khách ở lại, doanh nghiệp lớn lên." Lời = mục 7 kịch bản. Clip làm chung mọi ngành;
nói về ngôn ngữ của khách thì dùng "ngôn ngữ", không dùng "tiếng" (Liên 08/11).

Chạy:  python3 tts_vi_fw.py --text   -> in lời, đếm âm tiết
       CLIP_LANG=en python3 pick_take.py 2  -> voice/ban-hang-crm-en-fw.wav
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
VOICE = os.environ.get("VOICE_NAME", "Iapetus")   # giong EN clip tong (Lien chon 20/10/2026)

# Mỗi phần tử = MỘT đoạn = MỘT cảnh. Thứ tự khớp bảng cảnh trong kịch bản.
SCENES = [
    # Lời EN 09/11/2026 - đã qua ChatGPT web (tài khoản Liên); sửa tay: đoạn 5 giữ 'ask' (khớp nhãn bước Ask), đoạn 11 'so the customer never has to start over' (rõ chủ ngữ).
    # 0
    "Customers are a company's most valuable asset. But where does that asset really live?",
    # 1
    "In each salesperson's phone, a few spreadsheets, or the seller's memory. When people leave, customers leave with them.",
    # 2
    'Viindoo Sales and Customer Care keeps your customers with your company.',
    # 3
    'The story has two sides: customers stay, and the business grows.',
    # 4
    "Let's follow one customer through seven stages: discover, ask, get a quote, receive, pay, get support, and buy again.",
    # 5
    'A business customer is more than a phone number. The record keeps track of all four people on their side: the director, accountant, receiver, and operations manager.',
    # 6
    "Customers reach out on Zalo, the website, or the chat box, and everything lands in one place. After hours, the AI assistant replies in the customer's own language. When a known number messages, the system recognises the returning customer and links them to the right record.",
    # 7
    'Your team prepares quotes as usual. Customers abroad receive the email and quote in their own language, sent straight to their purchasing contact.',
    # 8
    "Goods go to the customer's warehouse, and the invoice goes to their accountant. The receiver and payer are different people, but nothing gets mixed up.",
    # 9
    'Ninety invoices paid, one still open, nine days overdue. Anyone opening the record can see right away what the customer owes.',
    # 10
    'Twelve support requests from this customer, all in one place. Support knows what the customer bought, so the customer never has to start over.',
    # 11
    'Every order earns points on a membership card. Next time, the customer has one more reason to come back.',
    # 12
    'The record shows what the customer usually buys, so the next quote already suggests add-on products. The customer can add them right on the online quote.',
    # 13
    "Ninety-four orders, over two billion dong invoiced. Customers are the company's asset, and that asset grows with every sale.",
    # 14
    'To keep customers as the business grows, you need a sales machine with four parts: organisation, marketing, management, and support.',
    # 15
    'Sales teams are organised by region, each with its own manager. Add a region or team, and everything stays in order.',
    # 16
    'Access follows the organisation: salespeople see their own customers and orders, team leaders see their teams, and regional managers see their regions. Marketing sends mass emails without needing access to orders.',
    # 17
    "New leads are assigned automatically based on each person's capacity. Six leads come in: the person with more capacity gets four, the other gets two. No one hoards leads, and none are forgotten.",
    # 18
    'The report shows how customers move from first contact to a closed deal, and where they drop off. Find the leak, then fix it.',
    # 19
    "Eighty-four customers from Facebook brought in over four billion. Twenty-four referred customers brought in nearly ten billion. Automated emails nurture leads, then pass them to the right salesperson when they're ready.",
    # 20
    "Quarterly targets by team: one team is at twelve percent, another is close to forty percent. Who's ahead and who's falling behind is clear at a glance.",
    # 21
    'Sales by salesperson, all on one chart. The leader sells twice as much as the runner-up.',
    # 22
    'This customer is over their three and a half billion credit limit, so the new quote shows a warning right away. A twelve percent discount waits for someone with approval rights. The rules run in the software, not through reminders.',
    # 23
    'Salespeople can check which orders have shipped, which customers still owe, and how long payments are overdue, for their own customers only, without asking accounting or the warehouse.',
    # 24
    'Since the start of the year: three hundred and sixty-six support requests, ninety-three percent resolved, all within the promised response time.',
    # 25
    'One hundred and forty-seven warranty claims, grouped by product. Whatever product keeps needing repairs, the people who make it know right away.',
    # 26
    'Viindoo puts the customer at the centre. Everything about a customer connects to the work of every team: sales, marketing, warehouse, accounting, support, and warranty. The customer moves through the whole journey without starting over at any step.',
    # 27
    'Open the customer in Contacts and see the full three hundred and sixty degree view: what they asked, what they bought, what they owe, and every support and warranty request. Each person sees only what their role allows.',
    # 28
    'Customers stay, the business grows. Book a Viindoo consultation today.',
]


SAY = {"Zalo": "Zah-lo"}   # 09/11: lượt 1 Iapetus đọc Zalo nghe thành "Solo" (2 bộ chép đều nghe vậy); phụ đề vẫn giữ "Zalo"

# Cau lenh giong de NGAN va dut khoat - ban dai lam may doc cham va deu (bai hoc bo HRM).
STYLE = ("Read in a young, confident male voice with a clear, neutral international English accent. "
         "BRIGHT and LIVELY, upbeat, full of energy, FAST pace; not deep, not breathy, "
         "keep the same energy to the very last sentence. "
         "This is the narration of a business software video about selling and keeping customers:\n\n")


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
    out = out_path or os.path.join(OUT_DIR, f"ban-hang-crm-en-{giong.lower()}.wav")
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
    """Am tiet tieng Anh: dem cum nguyen am (khop build_seq.dem_am_tiet khi CLIP_LANG=en)."""
    tong = 0
    for tu in re.findall(r"[a-zA-Z']+", s.lower()):
        n = len(re.findall(r"[aeiouy]+", tu))
        if tu.endswith("e") and n > 1 and not tu.endswith(("le", "ee", "ye")):
            n -= 1
        tong += max(1, n)
    return tong


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
    print("Soát bằng check_tts.py (CLIP_LANG=en) trước khi dựng.")
