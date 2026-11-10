"""Cat clip VI Ban hang + CRM thanh 3 clip ngan VUONG 1080x1080 cho Facebook (Lien OK 09/11/2026).
Khuon giong ban vuong day du (dung_vuong.py): clip ngang thu 1080x608 dat giua, tieu de tren (doi theo
tung clip), phu de lay tu video/fb/phu-de-vi.ass doi moc, dong ten + web cuoi.
Doan cat = ranh gioi CANH (ke-hoach-lap.json) - loi doc va hinh dung o khoang lang giua hai canh.
Clip nao doan dau khong tu mo duoc thi them THE CHU (chi nhac) truoc.
Tieng: loi doc cat tu voice/ban-hang-crm-vi-fw.wav (cung moc voi hinh), nhac nen chay LIEN tu dau toi
cuoi clip (khong noi nhac), muc nhac + gain nhu mix.sh, roi chinh ve ~-14 LUFS, dinh that < -1 dB.
Chay: python3 cat_ngan.py [1|2|3]   -> ../video/fb/BanHangCRM-ngan-0N-<ten>-Vuong.mp4
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cau_hinh as CH  # đường dẫn + kết nối dùng chung, xem cau_hinh.py

HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(HERE, "..", "video")
FB = os.path.join(VID, "fb")
SRC = os.path.join(VID, "Ban-Hang-CRM-tong-the-VI.mp4")
VOICE = os.path.join(HERE, "voice", "ban-hang-crm-vi-fw.wav")
MUSIC = os.environ.get("MUSIC") or os.path.join(CH.NHAC, "nang-dong-3-dai.mp3")
ASS_GOC = os.path.join(FB, "phu-de-vi.ass")
FONT_B = CH.FONT_B
GRAPHITE, TIM, CYAN = (33, 39, 43), (127, 66, 130), (0, 187, 206)
CHAN = "Viindoo Bán hàng và CRM  ·  viindoo.com"
VY, VH = 236, 608
THE_DAI = 2.6                       # giay the chu mo dau

ke = json.load(open(os.path.join(HERE, "ke-hoach-lap.json")))
t = 0.0; st = {}
for e in ke:
    if e["kieu"] != "broll": st.setdefault(e["canh"], t)
    t += e["dai"]
TONG = t
# broll muon DUOI canh truoc -> canh truoc ket thuc o dau broll, khong o st cua canh sau
ket = {}
t = 0.0
for e in ke:
    t0 = t; t += e["dai"]
    c = e["canh"]
    if e["kieu"] == "broll":
        ket[c - 1] = t                # canh truoc keo toi het broll (tieng canh truoc chay het)
    else:
        ket[c] = t
def doan(a, b):
    """Canh a..b (gom ca hai) -> (giay dau, giay cuoi) tren dong thoi gian clip ngang."""
    return (st[a], ket[b])

CLIP = {
    1: dict(ten="Khach-o-lai", tieu_de="Khách ở lại với doanh nghiệp", the=None,
            canh=[(0, 2), (5, 8), (12, 13), (28, 28)]),
    2: dict(ten="Bo-may-ban-hang", tieu_de="Bộ máy bán hàng lớn lên",
            the=("Đội bán hàng càng đông,", "càng khó quản?"),
            canh=[(2, 2), (14, 19), (28, 28)]),
    3: dict(ten="Quan-bang-so-va-luat", tieu_de="Quản bằng số và bằng luật",
            the=("Quản lý kinh doanh", "bằng nhắc nhở và cảm tính?"),
            canh=[(20, 27), (28, 28)]),
}


def ts(x):
    h = int(x // 3600); mi = int(x % 3600 // 60); se = x % 60
    return f"{h}:{mi:02d}:{se:05.2f}"

def tsec(s):
    h, m, x = s.split(":"); return int(h) * 3600 + int(m) * 60 + float(x)

def anh_nen(tieu_de, out):
    img = Image.new("RGB", (1080, 1080), "white"); d = ImageDraw.Draw(img)
    def giua(txt, y, size, mau):
        f = ImageFont.truetype(FONT_B, size)
        while d.textlength(txt, font=f) > 1000: size -= 2; f = ImageFont.truetype(FONT_B, size)
        w = d.textlength(txt, font=f); d.text(((1080 - w) / 2, y), txt, font=f, fill=mau)
    giua(tieu_de, 150, 46, GRAPHITE)
    giua(CHAN, 1008, 28, TIM)
    img.save(out)

def anh_the(dong, out):
    img = Image.new("RGB", (1080, 1080), "white"); d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT_B, 64)
    h = 84; y0 = 540 - h * len(dong) / 2 - 20
    for i, txt in enumerate(dong):
        w = d.textlength(txt, font=f)
        d.text(((1080 - w) / 2, y0 + i * h), txt, font=f, fill=GRAPHITE if i == 0 else CYAN)
    d.rounded_rectangle((470, y0 + h * len(dong) + 30, 610, y0 + h * len(dong) + 36), 3, fill=CYAN)
    f2 = ImageFont.truetype(FONT_B, 28)
    w = d.textlength(CHAN, font=f2); d.text(((1080 - w) / 2, 1008), CHAN, font=f2, fill=TIM)
    img.save(out)

def chay(cmd):
    subprocess.run(cmd, check=True)

def do_to(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "ebur128=peak=true:framelog=quiet",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    i = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", r)[-1])
    pk = float(re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", r)[-1])
    return i, pk

def lam(n):
    c = CLIP[n]
    work = os.path.join(HERE, "work", f"ngan-{n}"); os.makedirs(work, exist_ok=True)
    out = os.path.join(FB, f"BanHangCRM-ngan-0{n}-{c['ten']}-Vuong.mp4")
    khoang = [doan(a, b) for a, b in c["canh"]]
    lech = THE_DAI if c["the"] else 0.0
    dai_than = sum(b - a for a, b in khoang)
    dai = lech + dai_than

    # 1) phu de: dong cua ass goc nam trong cac khoang -> doi moc
    goc = [l for l in open(ASS_GOC, encoding="utf-8") if l.startswith("Dialogue:")]
    dau = open(ASS_GOC, encoding="utf-8").read().split("[Events]")[0]
    ass = os.path.join(work, "phu-de.ass")
    with open(ass, "w", encoding="utf-8") as f:
        f.write(dau + "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        moc = 0.0
        for a, b in khoang:
            for l in goc:
                p = l.split(",", 9)
                s, e = tsec(p[1]), tsec(p[2])
                if s >= a - 0.05 and e <= b + 0.2:
                    s2 = moc + max(s, a) - a; e2 = moc + min(e, b) - a
                    f.write(f"Dialogue: 0,{ts(s2)},{ts(e2)},Sub,,0,0,0,,{p[9]}")
            moc += b - a

    chi_tieng = os.environ.get("CHI_TIENG") and os.path.exists(os.path.join(work, "than.mp4"))
    # 2) hinh than: noi cac doan ngang -> thu 1080x608 tren nen co tieu de + phu de
    nen = os.path.join(work, "nen.png"); anh_nen(c["tieu_de"], nen)
    parts = "".join(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps=30[s{i}];" for i, (a, b) in enumerate(khoang))
    cc = "".join(f"[s{i}]" for i in range(len(khoang))) + f"concat=n={len(khoang)}:v=1:a=0[h];"
    fdir = os.path.dirname(FONT_B)
    vf = (parts + cc + f"[h]scale=1080:{VH}:flags=lanczos,setsar=1[v];[1:v][v]overlay=0:{VY}:shortest=1,"
          f"subtitles={ass}:fontsdir={fdir},format=yuv420p[o]")
    than = os.path.join(work, "than.mp4")
    if not chi_tieng: chay(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-loop", "1", "-framerate", "30", "-i", nen,
          "-filter_complex", vf, "-map", "[o]", "-an", "-r", "30", "-c:v", "libx264", "-preset", "medium",
          "-crf", "20", "-pix_fmt", "yuv420p", than])

    # 3) the chu (neu co) + noi
    hinh = than
    if c["the"]:
        pthe = os.path.join(work, "the.png"); anh_the(c["the"], pthe)
        vthe = os.path.join(work, "the.mp4")
        chay(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", f"{THE_DAI}",
              "-i", pthe, "-vf", "fade=t=out:st=%.2f:d=0.35,format=yuv420p" % (THE_DAI - 0.35),
              "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30", vthe])
        ds = os.path.join(work, "ds.txt")
        open(ds, "w").write(f"file '{vthe}'\nfile '{than}'\n")
        hinh = os.path.join(work, "hinh.mp4")
        chay(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", ds, "-c", "copy", hinh])

    # 4) tieng: loi doc cat theo cung khoang (fade 25ms o moi diem noi), nhac lien mach
    va = "".join(f"[1:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.025,"
                 f"afade=t=out:st={b - a - 0.025:.3f}:d=0.025[a{i}];" for i, (a, b) in enumerate(khoang))
    va += "".join(f"[a{i}]" for i in range(len(khoang))) + f"concat=n={len(khoang)}:v=0:a=1[vc];"
    if lech:
        va += f"[vc]adelay={int(lech * 1000)}:all=1[vd];"
    else:
        va += "[vc]anull[vd];"
    fo = max(0, dai - 3)

    def tron(gain, ra):
        af = (va + f"[2:a]atrim=0:{dai:.3f},asetpts=N/SR/TB,volume=0.13,afade=t=in:d=1.2,"
              f"afade=t=out:st={fo:.3f}:d=3[m];[vd]volume=0.92,apad[v];"
              f"[v][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:{dai:.3f},volume={gain:.2f}dB,"
              "aresample=192000,alimiter=limit=0.84:level=disabled,aresample=48000[a]")
        chay(["ffmpeg", "-y", "-loglevel", "error", "-i", hinh, "-i", VOICE, "-stream_loop", "-1", "-i", MUSIC,
              "-filter_complex", af, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
              "-t", f"{dai:.3f}", "-movflags", "+faststart", ra])

    g = 3.0
    for _ in range(4):                       # gioi han dinh nen gain khong tuyen tinh -> lap toi khi trung
        tron(g, out)
        i, pk = do_to(out)
        if abs(-14.0 - i) <= 0.3 and pk <= -1.0:
            break
        g += (-14.0 - i)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                             capture_output=True, text=True).stdout)
    print(f"clip {n}: {out}\n  dai {d:.1f}s (than {dai_than:.1f}s + the {lech:.1f}s), {i:.1f} LUFS, dinh that {pk:.1f} dBFS")
    print("  khoang:", [(round(a, 2), round(b, 2)) for a, b in khoang])

if __name__ == "__main__":
    for n in ([int(x) for x in sys.argv[1:]] or [1, 2, 3]):
        lam(n)
