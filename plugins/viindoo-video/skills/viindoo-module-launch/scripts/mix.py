"""Trộn lời đọc với nhạc nền (nhạc tự hạ khi có giọng) rồi ghép vào hình. Clip không giọng (NO_VO, xem readtime.py): chỉ nhạc nền.
Chạy: python3 mix.py <clip_dir> sq|v|h   -> <OUT>-<Vuong|Doc|Ngang>.mp4 (OUT khai báo trong clip.py; mặc định <clip_dir>/<SLUG>)
Nhạc: clip.py PHẢI khai báo MUSIC = {"style": ..., "seed": ..., "why": "..."} (chọn cùng người dùng, xem music.py);
lấy từ thư viện nhạc chung, thiếu MUSIC thì dừng, không tự gán bản mặc định."""
import importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from music import ensure
import readtime
clip, fmt = sys.argv[1], sys.argv[2]
SUF = {'sq': 'Vuong', 'v': 'Doc', 'h': 'Ngang'}[fmt]
D = os.path.abspath(clip)
spec = importlib.util.spec_from_file_location("clip", os.path.join(D, "clip.py")); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
T = json.load(open(os.path.join(D, "timeline.json")))
st, END = T["starts"], T["END"]
n = len(st)
if not getattr(C, "MUSIC", None):
    sys.exit("clip.py chưa có MUSIC: chọn nhạc nền hợp nội dung clip cùng người dùng (python3 music.py list / preview) rồi khai báo, "
             'ví dụ MUSIC = {"style": "nang-dong", "seed": 2, "why": "clip xưởng, nhịp nhanh"}')
print("nhạc nền:", ensure(D, C.MUSIC, END, getattr(C, "OUT", None) and os.path.basename(C.OUT) or C.SLUG))
MV = getattr(C, "MUSIC_VOL", 0.30)   # âm lượng nhạc nền; clip hướng dẫn tài liệu dùng 0.15 (Liên 14/10: nhạc to)
TEXT_LUFS = getattr(C, "TEXT_LUFS", -23.0)   # clip không giọng: nhạc là thứ duy nhất trong tiếng, đo rồi chỉnh tới khi đạt mục tiêu (Liên 23/10/2026)


def lufs(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = out[out.rindex("Summary"):]
    return float(tail.split("I:")[1].split("LUFS")[0])


if readtime.is_text(C, D):
    # Khi còn giọng, nhạc ở 0.15 để không át lời. Hết giọng thì lý do đó mất; 0.15 chỉ còn -32 LUFS, gần như im trên điện thoại.
    # Không đoán theo hệ số nhân: dựng với gain 1, đo tích hợp (EBU R128), tính gain bù, dựng lại, đo lại, lặp tới khi lệch dưới 0,3 LU.
    gain_db = 0.0
    for lan in range(4):
        fl = (f"[0:a]atrim=0:{END},afade=t=out:st={END-2.5}:d=2.5,volume={gain_db}dB,aformat=channel_layouts=stereo,"
              "alimiter=limit=0.89[a]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "music.wav", "-filter_complex", fl, "-map", "[a]", "-ar", "48000", "-c:a", "pcm_s16le", "mix.wav"],
                       cwd=D, check=True)
        got = lufs(os.path.join(D, "mix.wav")); print(f"nhạc lần {lan}: gain {gain_db:+.1f} dB -> {got:.1f} LUFS (mục tiêu {TEXT_LUFS})")
        if abs(got - TEXT_LUFS) <= 0.3: break
        gain_db += TEXT_LUFS - got
else:
    ins = ["-i", "music.wav"] + sum((["-i", f"vo/seg{i}.flac"] for i in range(n)), [])
    fl = "".join(f"[{i+1}:a]adelay={int(st[i]*1000)}|{int(st[i]*1000)},aformat=channel_layouts=stereo[v{i}];" for i in range(n))
    fl += "".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,apad=whole_dur={END},asplit=2[vo][sc];"
    fl += (f"[0:a]atrim=0:{END},afade=t=out:st={END-2.5}:d=2.5,volume={MV}[m];"
           "[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=450[md];"
           "[md][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fl, "-map", "[a]", "-ar", "48000", "-c:a", "pcm_s16le", "mix.wav"],
                   cwd=D, check=True)
out = os.path.join(D, f"{C.SLUG}-{SUF}.mp4")
if getattr(C, "OUT", None):   # clip ngoài bộ cơ khí: tự chọn nơi xuất (đường dẫn gốc, chưa có đuôi khổ)
    out = f"{C.OUT}-{SUF}.mp4"; os.makedirs(os.path.dirname(out), exist_ok=True)
# -c:v copy giữ nguyên hình; h264_metadata ghi đủ nhãn màu BT.709 dải giới hạn (cyan không lệch trên nền tảng phát)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"silent_{fmt}.mp4", "-i", "mix.wav", "-c:v", "copy",
                "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", out], cwd=D, check=True)
print("ok", os.path.normpath(out))
