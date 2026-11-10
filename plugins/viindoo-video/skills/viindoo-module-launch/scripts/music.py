"""Thư viện nhạc nền dùng chung cho mọi clip: mỗi bản = kiểu + seed, kèm sổ ghi clip nào đã dùng.
Thư mục: ${VIINDOO_VIDEO_WORKDIR:-~/viindoo-video}/Nhac-nen/ (index.json + các bản .wav + nghe-thu/).
Chạy: python3 music.py list                         -> các kiểu nhạc + các bản đã có, clip nào đã dùng
      python3 music.py preview <kiểu>:<seed> ...     -> nghe-thu/<kiểu>-<seed>.mp3 (20 giây) để người dùng chọn
mix.py gọi ensure() khi trộn: clip.py PHẢI khai báo MUSIC = {"style": ..., "seed": ..., "why": "..."}."""
import datetime, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_music import STYLES, make

LIB = os.path.join(os.path.expanduser(os.environ.get("VIINDOO_VIDEO_WORKDIR", "~/viindoo-video")), "Nhac-nen")
IDX = os.path.join(LIB, "index.json")


def load():
    return json.load(open(IDX)) if os.path.exists(IDX) else {}


def save(idx):
    os.makedirs(LIB, exist_ok=True)
    json.dump(idx, open(IDX, "w"), ensure_ascii=False, indent=1)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


def ensure(clip_dir, music, end, clip_name):
    """Lấy (hoặc tạo) bản nhạc đủ dài trong thư viện, chép thành <clip_dir>/music.wav, ghi sổ dùng."""
    style, seed = music["style"], int(music["seed"])
    if style not in STYLES: sys.exit(f"MUSIC style '{style}' không có; chọn: {', '.join(STYLES)}")
    key = f"{style}-{seed}"
    wav = os.path.join(LIB, key + ".wav")
    os.makedirs(LIB, exist_ok=True)
    if not os.path.exists(wav) or dur(wav) < end + 1:   # cùng kiểu + seed luôn ra cùng giai điệu, dài hơn thì sinh lại
        make(style, seed, end + 1, wav)
    shutil.copy(wav, os.path.join(clip_dir, "music.wav"))   # mix.py tự cắt + hạ dần theo độ dài clip
    idx = load()
    e = idx.setdefault(key, {"style": style, "seed": seed, "bpm": STYLES[style][0], "dung_cho": []})
    others = [u for u in e["dung_cho"] if u["clip"] != clip_name]
    if others:
        print(f"lưu ý: bản nhạc {key} đã dùng cho: " + "; ".join(f"{u['clip']} ({u['ngay']})" for u in others))
    e["dung_cho"] = others + [{"clip": clip_name, "ngay": datetime.date.today().isoformat(), "ly_do": music.get("why", "")}]
    save(idx)
    return key


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        print("Kiểu nhạc:")
        for k, v in STYLES.items(): print(f"  {k:10} {v[0]:3} BPM  {v[5]}")
        idx = load()
        print(f"\nBản đã có ({LIB}):" if idx else "\nChưa có bản nào trong thư viện.")
        for k, e in idx.items():
            print(f"  {k:14} dùng {len(e['dung_cho'])} lần: " + "; ".join(u["clip"] for u in e["dung_cho"]))
    elif cmd == "preview":
        os.makedirs(os.path.join(LIB, "nghe-thu"), exist_ok=True)
        for spec in sys.argv[2:]:
            style, seed = spec.split(":")
            tmp = os.path.join(LIB, "nghe-thu", f"{style}-{seed}.wav")
            make(style, int(seed), 20, tmp)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-b:a", "160k", tmp[:-4] + ".mp3"], check=True)
            os.remove(tmp); print("ok", tmp[:-4] + ".mp3")
    else:
        sys.exit(__doc__)
