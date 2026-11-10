"""Đo CAO ĐỘ và NHỊP của bản thu - để so giọng bằng số, không cãi nhau bằng cảm giác.

Vì sao cần: Liên nghe ra "giọng quá trầm", "như hết hơi", "bản lần trước ổn hơn". Máy không
nghe được, nhưng ĐO được: cao độ trung bình (F0) cho biết trầm hay sáng, tỉ lệ khung có tiếng
cho biết đọc liền hơi hay hụt, số âm tiết/giây cho biết nhanh chậm.

Chạy:  python voice_stats.py voice/*.wav
"""
import glob, struct, sys, wave

import numpy as np


def doc_wav(p):
    with wave.open(p, "rb") as w:
        n, sr = w.getnframes(), w.getframerate()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(axis=1)
    return x, sr


def f0_khung(seg, sr, lo=70, hi=330):
    """Cao độ một khung bằng tự tương quan. Trả None nếu khung không phải giọng."""
    seg = seg - seg.mean()
    if np.sqrt((seg ** 2).mean()) < 0.01:
        return None
    r = np.correlate(seg, seg, mode="full")[len(seg) - 1:]
    if r[0] <= 0:
        return None
    r /= r[0]
    i0, i1 = int(sr / hi), int(sr / lo)
    if i1 >= len(r):
        return None
    k = int(np.argmax(r[i0:i1])) + i0
    return sr / k if r[k] > 0.35 else None


def do(p):
    x, sr = doc_wav(p)
    win, hop = int(0.04 * sr), int(0.02 * sr)
    f0s, co_tieng = [], 0
    tong_khung = 0
    for i in range(0, len(x) - win, hop):
        seg = x[i:i + win]
        tong_khung += 1
        rms = np.sqrt((seg ** 2).mean())
        if rms >= 0.01:
            co_tieng += 1
        f = f0_khung(seg, sr)
        if f:
            f0s.append(f)
    f0s = np.array(f0s)
    return {
        "dai": len(x) / sr,
        "f0": float(np.median(f0s)) if len(f0s) else 0.0,
        "f0_do_rong": float(np.percentile(f0s, 90) - np.percentile(f0s, 10)) if len(f0s) else 0,
        "ty_le_co_tieng": co_tieng / max(tong_khung, 1),
    }


def main():
    files = sys.argv[1:] or sorted(glob.glob("voice/*.wav"))
    print(f"{'file':34} {'dài':>7} {'F0 giữa':>8} {'dải F0':>7} {'có tiếng':>9}")
    for p in files:
        try:
            s = do(p)
        except Exception as e:
            print(f"  {p}: lỗi {e}"); continue
        print(f"{p.split('/')[-1]:34} {s['dai']:6.1f}s {s['f0']:7.1f}Hz "
              f"{s['f0_do_rong']:6.1f}Hz {s['ty_le_co_tieng']*100:7.1f}%")


if __name__ == "__main__":
    main()
