"""Ban VUONG 1080x1080 cho Facebook - theo khuon cum Trao doi (video/fb):
clip ngang thu ve 1080x608 dat giua, tieu de tren, phu de lien tuc duoi khung hinh, dong ten + web cuoi.
Phu de: moi doan loi (SCENES) chia theo cau / dau phay, moc lay tu khoang lang THAT cua ban thu.
Chay: python3 dung_vuong.py   -> ../video/Ban-Hang-CRM-tong-the-VI-vuong.mp4
"""
import importlib.util, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cau_hinh as CH  # đường dẫn dùng chung, xem cau_hinh.py
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(HERE, "..", "video")
FB = os.path.join(VID, "fb")
SRC = os.path.join(VID, "Ban-Hang-CRM-tong-the-VI.mp4")
OUT = os.path.join(VID, "Ban-Hang-CRM-tong-the-VI-vuong.mp4")
VOICE = os.path.join(HERE, "voice", "ban-hang-crm-vi-fw.wav")
TIEU_DE = "Khách hàng là tài sản của doanh nghiệp"
CHAN = "Viindoo Bán hàng và CRM  ·  viindoo.com"
FONT_B = CH.FONT_B
GRAPHITE, TIM = (33, 39, 43), (127, 66, 130)
VY, VH = 236, 608            # o video: y 236..844

spec = importlib.util.spec_from_file_location("t", os.path.join(HERE, "tts_vi_fw.py"))
m = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(m)
SCENES = m.SCENES

ke = json.load(open(os.path.join(HERE, "ke-hoach-lap.json")))
t = 0.0; st = {}
for e in ke:                    # b-roll muon DUOI canh dung truoc -> khong tinh la dau canh sau
    if e["kieu"] != "broll": st.setdefault(e["canh"], t)
    t += e["dai"]
TONG = t
starts = [st[i] for i in range(len(SCENES))] + [TONG]

r = subprocess.run(["ffmpeg", "-hide_banner", "-i", VOICE, "-af", "silencedetect=noise=-38dB:d=0.16",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
s_ = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", r)]
e_ = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r)]
lang = list(zip(s_, e_))

def am(s): return len(s.split())

def chia(doan):
    cau = [c.strip() for c in re.split(r"(?<=[.?!:])\s+", doan) if c.strip()]
    out = []
    for c in cau:
        if am(c) <= 13:
            out.append(c); continue
        phan = [p.strip() for p in re.split(r"(?<=,)\s+", c)]
        cur = ""
        for p in phan:
            if cur and am(cur) + am(p) > 13:
                out.append(cur); cur = p
            else:
                cur = (cur + " " + p).strip()
        if cur: out.append(cur)
    return out

def ts(x):
    h = int(x // 3600); mi = int(x % 3600 // 60); se = x % 60
    return f"{h}:{mi:02d}:{se:05.2f}"

dong = []
for i, doan in enumerate(SCENES):
    a, b = starts[i], starts[i + 1]
    trong = [(x, y) for x, y in lang if x > a - 0.05 and y < b + 0.05]
    noi_a = a
    for x, y in trong:                      # lang dau canh -> tieng bat dau sau do
        if x <= a + 0.6: noi_a = max(noi_a, y)
    noi_b = b
    for x, y in reversed(trong):
        if y >= b - 0.6: noi_b = min(noi_b, x)
    ch = chia(doan)
    n = [am(c) for c in ch]; tong = sum(n)
    bien = []; acc = 0
    ung = [(x + y) / 2 for x, y in trong if noi_a + 0.3 < (x + y) / 2 < noi_b - 0.3]
    dai = noi_b - noi_a
    for k in range(len(ch) - 1):
        acc += n[k]
        du = noi_a + dai * acc / tong
        truoc = bien[-1] if bien else noi_a
        con = dai * (tong - acc) / tong            # thoi gian cac cum con lai can
        cands = [u for u in ung if u - truoc >= 0.6 * dai * n[k] / tong
                 and noi_b - u >= 0.6 * con and abs(u - du) <= 1.5]
        bien.append(min(cands, key=lambda u: abs(u - du)) if cands else du)
    moc = [noi_a] + bien + [noi_b]
    for k, c in enumerate(ch):
        dong.append((max(moc[k] - 0.08, a), min(moc[k + 1] + 0.12, b), c))

os.makedirs(FB, exist_ok=True)
ass = os.path.join(FB, "phu-de-vi.ass")
with open(ass, "w", encoding="utf-8") as f:
    f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1080\nWrapStyle: 0\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Sub,Montserrat VN,36,&H002B2721,&H002B2721,&H00FFFFFF,&H00FFFFFF,1,0,0,0,100,100,0,0,1,0,0,8,50,50,866,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    for a, b, c in dong:
        f.write(f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{c}\n")

from PIL import Image, ImageDraw, ImageFont
img = Image.new("RGB", (1080, 1080), "white"); d = ImageDraw.Draw(img)
def giua(txt, y, size, mau):
    f = ImageFont.truetype(FONT_B, size)
    while d.textlength(txt, font=f) > 1000: size -= 2; f = ImageFont.truetype(FONT_B, size)
    w = d.textlength(txt, font=f); d.text(((1080 - w) / 2, y), txt, font=f, fill=mau)
giua(TIEU_DE, 150, 46, GRAPHITE)
giua(CHAN, 1008, 28, TIM)
nen = os.path.join(FB, "chu-vuong-vi.png"); img.save(nen)

if os.environ.get("CHI_PHU_DE"): sys.exit(0)
fdir = os.path.dirname(FONT_B)
vf = (f"[1:v]scale=1080:{VH}:flags=lanczos,setsar=1[v];[0:v][v]overlay=0:{VY},"
      f"subtitles={ass}:fontsdir={fdir},format=yuv420p[o]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", nen,
                "-i", SRC, "-filter_complex", vf, "-map", "[o]", "-map", "1:a",
                "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high",
                "-c:a", "copy", "-shortest", "-movflags", "+faststart", OUT], check=True)
print("xong", OUT, len(dong), "dong phu de")
