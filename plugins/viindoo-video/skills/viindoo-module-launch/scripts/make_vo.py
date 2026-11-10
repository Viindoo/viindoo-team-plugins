"""Sinh lời đọc cho một clip bằng Gemini TTS (gemini-3.1-flash-tts-preview). clip.py PHẢI khai báo VOICE = "Iapetus"
(giọng cố định của clip ra mắt sản phẩm); STYLE mặc định theo giọng, clip.py ghi đè được STYLE/SPOKEN/BATCH_INTRO.
Chạy: python3 make_vo.py <clip_dir> [số đoạn ...]   -> <clip_dir>/vo/seg*.flac (mỗi đoạn một lượt gọi)
      python3 make_vo.py <clip_dir> --batch          -> cả clip MỘT lượt gọi, tự cắt theo chỗ ngắt giữa các đoạn
      python3 make_vo.py <clip_dir> --batch --from <file.pcm|wav>  -> dùng lại bản đọc có sẵn
Gemini miễn phí chỉ 10 lượt/ngày/mô hình: dùng --batch để mỗi clip tốn một lượt.
Dùng một mô hình cho cả loạt clip: khác mô hình là khác chất giọng."""
import importlib.util, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tts import tts
# Giọng cố định cho mọi clip ra mắt sản phẩm (Liên chốt 12/10/2026, mẫu nghe ở kho nội bộ)
VOICES = {"Iapetus": "nam_tre"}
STYLES = {
    "nam_tre": "Giọng nam trẻ Hà Nội, khoảng 23-28 tuổi, nhịp nhanh, dứt khoát, gọn gàng, rõ chữ, năng lượng tươi, nhấn nhẹ vào từ khóa, không kéo dài cuối câu, như người dẫn video ra mắt sản phẩm công nghệ: ",
    "nu": "Giọng nữ Hà Nội, khoảng 28-35 tuổi, tự nhiên, rõ ràng, tự tin, nhịp vừa phải, như người dẫn video giới thiệu phần mềm cho doanh nghiệp: ",
    "nam": "Giọng nam Hà Nội, khoảng 28-35 tuổi, tự nhiên, rõ ràng, tự tin, nhịp vừa phải, như người dẫn video giới thiệu phần mềm cho doanh nghiệp: ",
}
MODEL = os.environ.get("TTS_MODEL", "gemini-3.1-flash-tts-preview")   # mô hình đã thu mẫu giọng chốt; khác mô hình là khác chất giọng
SPOKEN = [("KCS", "ca xê ét"), ("Viindoo", "Vin đu")]   # chỉ đổi trong lời đọc, phụ đề giữ chữ gốc

TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"


def spoken(t):
    for a, b in SPOKEN:
        t = t.replace(a, b)
    return t


def call(text, out):
    for attempt in range(6):   # 429 theo phút thì chờ rồi thử lại; hết lượt ngày thì dừng
        p = tts(text, out, model=MODEL, voice=VOICE)
        if p: return p
        time.sleep(35)
    sys.exit(f"{out}: lỗi (hết lượt Gemini?)")


def to_flac(p, out, af=TRIM):
    pre = ["-f", "s16le", "-ar", "24000", "-ac", "1"] if p.endswith(".pcm") else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", *pre, "-i", p, "-af", af, "-ar", "48000", "-ac", "1", out], check=True)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


def batch(D, VO):
    """Một lượt gọi cho cả clip, cắt tại chỗ lặng gần vị trí dự kiến (tỉ lệ theo số chữ) và dài nhất quanh đó."""
    full = os.path.join(D, "vo", "all")
    text = STYLE + getattr(C, "BATCH_INTRO", "đọc lần lượt các đoạn dưới đây, nghỉ khoảng một giây giữa hai đoạn.") + "\n\n" + "\n\n".join(spoken(t) for t in VO)
    src = sys.argv[sys.argv.index("--from") + 1] if "--from" in sys.argv else None   # dùng lại bản đọc có sẵn (cùng giọng, cùng câu dặn, cùng lời)
    to_flac(src or call(text, full), full + ".flac")
    T = dur(full + ".flac")
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", full + ".flac", "-af", "silencedetect=noise=-40dB:d=0.25", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s0 = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    s1 = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    sil = [(a, b) for a, b in zip(s0, s1)]
    L = [len(t) for t in VO]; cuts = []; last = 0
    for k in range(1, len(VO)):
        exp = T * sum(L[:k]) / sum(L)
        best = max(((b - a) - abs((a + b) / 2 - exp) * 0.35, a, b) for a, b in sil if a > last + 0.5) if any(a > last + 0.5 for a, _ in sil) else None
        if not best: sys.exit("không tìm được chỗ cắt, chạy lại từng đoạn")
        cuts.append((best[1], best[2])); last = best[2]
    bounds = [(0, cuts[0][0])] + [(cuts[i][1], cuts[i + 1][0]) for i in range(len(cuts) - 1)] + [(cuts[-1][1], T)]
    for i, (a, b) in enumerate(bounds):
        out = os.path.join(D, "vo", f"seg{i}.flac")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", full + ".flac", "-ss", f"{max(0, a - 0.03):.3f}", "-to", f"{b + 0.05:.3f}",
                        "-af", TRIM, out], check=True)
    ds = [dur(os.path.join(D, "vo", f"seg{i}.flac")) for i in range(len(VO))]
    rate = [l / d for l, d in zip(L, ds)]
    med = sorted(rate)[len(rate) // 2]
    for i, (d, r) in enumerate(zip(ds, rate)):
        flag = "" if 0.65 < r / med < 1.5 else "  <-- lệch nhịp, kiểm tra chỗ cắt"
        print(f"  seg{i} {d:5.2f}s {r:5.1f} ký tự/giây{flag}")


clip = sys.argv[1]
D = os.path.abspath(clip)
spec = importlib.util.spec_from_file_location("clip", os.path.join(D, "clip.py")); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
VOICE = getattr(C, "VOICE", None)
if VOICE not in VOICES:
    sys.exit(f"clip.py: VOICE = {VOICE!r}; clip ra mắt sản phẩm dùng giọng cố định {', '.join(VOICES)}")
STYLE = getattr(C, "STYLE", STYLES[VOICES[VOICE]]); SPOKEN = getattr(C, "SPOKEN", SPOKEN)   # clip tiếng Anh: câu dặn + cách đọc riêng
os.makedirs(os.path.join(D, "vo"), exist_ok=True)
if "--batch" in sys.argv:
    batch(D, C.VO); print("ok", clip, "batch", MODEL)
else:
    for i in [int(x) for x in sys.argv[2:]] or range(len(C.VO)):
        out = os.path.join(D, "vo", f"seg{i}")
        to_flac(call(STYLE + spoken(C.VO[i]), out), out + ".flac")
        print("ok", clip, i, flush=True)
        time.sleep(22)
