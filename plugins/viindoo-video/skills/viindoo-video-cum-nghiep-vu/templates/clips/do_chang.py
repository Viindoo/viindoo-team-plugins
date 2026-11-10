"""Do cao do (F0) va dai F0 TUNG CHANG cua mot ban thu - chung minh giong khong troi.

Vi sao: Lien nghe ra "giong cac chang dang khac nhau" (09/11/2026) - ban thu chia 3 khoi goi API
rieng roi noi, moi khoi mot am sac. Luat: doc ca bai MOT luot; ban cuoi phai co cac chang
lech nhau khong qua ~5 Hz (F0 giua).

Chay:  python3 -I do_chang.py voice/a.wav [voice/b.wav ...] [--chang 35]
Thoat ma 1 neu co ban lech qua nguong.
"""
import os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from voice_stats import doc_wav, f0_khung  # noqa: E402

NGUONG_HZ = 5.0


def do_chang(p, chang_s=35.0):
    x, sr = doc_wav(p)
    win, hop = int(0.04 * sr), int(0.02 * sr)
    n = int(chang_s * sr)
    kq = []
    for a in range(0, len(x), n):
        seg = x[a:a + n]
        if len(seg) < 10 * sr:  # duoi 10s: gop vao chang truoc thi khong can, bo qua
            break
        f0s = [f for i in range(0, len(seg) - win, hop) if (f := f0_khung(seg[i:i + win], sr))]
        f0s = np.array(f0s)
        if len(f0s) < 50:
            continue
        kq.append((a / sr, (a + len(seg)) / sr, float(np.median(f0s)),
                   float(np.percentile(f0s, 90) - np.percentile(f0s, 10))))
    return kq


def main():
    args = sys.argv[1:]
    chang = 35.0
    if "--chang" in args:
        i = args.index("--chang"); chang = float(args[i + 1]); del args[i:i + 2]
    loi = 0
    for p in args:
        kq = do_chang(p, chang)
        f0 = [k[2] for k in kq]
        lech = max(f0) - min(f0) if f0 else 0
        dat = lech <= NGUONG_HZ
        loi |= not dat
        print(f"{os.path.basename(p)}: lech F0 giua cac chang {lech:.1f} Hz "
              f"({'DAT' if dat else 'VUOT'} nguong {NGUONG_HZ:.0f} Hz)")
        for a, b, f, d in kq:
            print(f"   {a:6.0f}-{b:4.0f}s  F0 {f:6.1f} Hz  dai {d:6.1f} Hz")
    sys.exit(1 if loi else 0)


if __name__ == "__main__":
    main()
