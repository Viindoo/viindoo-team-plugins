"""Tính lại các chỗ cắt như make_vo.batch, cho phép dời chỗ cắt k sang khoảng lặng thứ +n kế tiếp, rồi cắt lại seg*.flac.
Chạy: recut.py <clipdir> [k=+n ...]   (không đối số: chỉ in các chỗ cắt)"""
import importlib.util, os, re, subprocess, sys
D = sys.argv[1]; shift = {int(a.split("=")[0]): int(a.split("=")[1]) for a in sys.argv[2:]}
s = importlib.util.spec_from_file_location("c", os.path.join(D, "clip.py")); C = importlib.util.module_from_spec(s); s.loader.exec_module(C)
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
full = os.path.join(D, "vo", "all.flac")
T = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", full]))
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", full, "-af", "silencedetect=noise=-40dB:d=0.25", "-f", "null", "-"], capture_output=True, text=True).stderr
sil = list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)], [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]))
L = [len(t) for t in C.VO]; cuts = []; last = 0
for k in range(1, len(C.VO)):
    exp = T * sum(L[:k]) / sum(L)
    cand = [((b - a) - abs((a + b) / 2 - exp) * 0.35, a, b) for a, b in sil if a > last + 0.5]
    best = max(cand)
    idx = sil.index((best[1], best[2])) + shift.get(k, 0)
    a, b = sil[idx]; cuts.append((a, b)); last = b
for k, (a, b) in enumerate(cuts, 1): print(f"cut {k}: {a:.2f}-{b:.2f}")
if shift:
    bounds = [(0, cuts[0][0])] + [(cuts[i][1], cuts[i + 1][0]) for i in range(len(cuts) - 1)] + [(cuts[-1][1], T)]
    for i, (a, b) in enumerate(bounds):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", full, "-ss", f"{max(0, a - 0.03):.3f}", "-to", f"{b + 0.05:.3f}", "-af", TRIM,
                        os.path.join(D, "vo", f"seg{i}.flac")], check=True)
    print("recut done")
