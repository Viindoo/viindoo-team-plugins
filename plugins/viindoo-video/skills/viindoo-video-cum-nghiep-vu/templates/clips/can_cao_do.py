"""Can cao do TUNG CHANG cua MOT ban thu tron bai - chong giong troi xuong dan ve cuoi bai.

Vi sao (09/11/2026): doc ca bai MOT luot thi het chuyen "moi khoi mot am sac", nhung Gemini van
ha giong dan tu dau toi cuoi bai (do: 133 Hz chang dau -> 125 Hz chang cuoi). Lien nghe ra
"giong cac chang dang khac nhau".

Cach lam: cat ban thu thanh cac chang ~35 s, CAT DUNG O KHOANG LANG (nen khong co cho noi nghe
duoc), do F0 giua tung chang, keo moi chang mot he so nho ve cung mot muc dich (gioi han
-3%..+5%), giu nguyen thoi luong tung chang (asetrate + atempo), roi noi lai.

Chay:  python3 can_cao_do.py voice/vao.wav voice/ra.wav [F0_dich=131]
"""
import os, subprocess, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from voice_stats import doc_wav, f0_khung  # noqa: E402

CHANG_S, KEO_MIN, KEO_MAX = 35.0, 0.97, 1.05


def khoang_lang(p):
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "silencedetect=noise=-40dB:d=0.25", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    bat, ket = [], []
    for ln in r.splitlines():
        if "silence_start:" in ln:
            bat.append(float(ln.split("silence_start:")[1]))
        elif "silence_end:" in ln:
            ket.append(float(ln.split("silence_end:")[1].split("|")[0]))
    return [(a + b) / 2 for a, b in zip(bat, ket)]


def f0_doan(x, sr):
    win, hop = int(0.04 * sr), int(0.02 * sr)
    f = [v for i in range(0, len(x) - win, hop) if (v := f0_khung(x[i:i + win], sr))]
    return float(np.median(f)) if len(f) > 50 else None


def main():
    src, out = sys.argv[1], sys.argv[2]
    dich = float(sys.argv[3]) if len(sys.argv) > 3 else 131.0
    x, sr = doc_wav(src)
    dai = len(x) / sr
    lang = khoang_lang(src)
    moc, t = [0.0], CHANG_S
    while t < dai - 15:
        moc.append(min(lang, key=lambda s: abs(s - t)) if lang else t)
        t = moc[-1] + CHANG_S
    moc.append(dai)
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), "_can")
    os.makedirs(tmp, exist_ok=True)
    phan = []
    for i, (a, b) in enumerate(zip(moc, moc[1:])):
        f = f0_doan(x[int(a * sr):int(b * sr)], sr)
        he = min(max(dich / f, KEO_MIN), KEO_MAX) if f else 1.0
        p = os.path.join(tmp, f"p{i:02d}.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-af", f"asetrate={sr}*{he:.5f},aresample={sr},atempo={1 / he:.6f}",
                        "-ar", str(sr), "-ac", "1", p], check=True)
        print(f"  chang {i}: {a:6.1f}-{b:6.1f}s  F0 {f or 0:6.1f} Hz  he so {he:.3f}")
        phan.append(p)
    ds = os.path.join(tmp, "ds.txt")
    open(ds, "w").write("".join(f"file '{p}'\n" for p in phan))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", ds,
                    "-c", "copy", out], check=True)
    print("ra", out)


if __name__ == "__main__":
    main()
