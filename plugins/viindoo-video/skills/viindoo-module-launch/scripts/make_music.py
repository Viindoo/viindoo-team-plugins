"""Nhạc nền tự tổng hợp (numpy, không lo bản quyền), nhiều kiểu để mỗi clip chọn bản hợp nội dung.
Chạy: python3 make_music.py <kiểu> <seed> <giây> <file.wav>
      python3 make_music.py --list      -> in các kiểu và lúc nên dùng
Cùng kiểu + seed luôn ra cùng một bản (dùng lại được); đổi seed là đổi giai điệu, nhịp trống và hợp âm."""
import numpy as np, wave, sys

STYLES = {
    # tên: (BPM, gốc giọng (MIDI), các vòng hợp âm (bậc trên gốc, thứ/trưởng), độ dày rải, trống, mô tả)
    "tuoi-vui":  (118, 55, [[0, 7, 9, 5], [0, 5, 7, 5], [0, 9, 5, 7]], 16, "full",
                  "tươi sáng, vui: ra mắt sản phẩm, tính năng mới, tin vui"),
    "nang-dong": (124, 52, [[0, 8, 3, 10], [0, 5, 8, 10], [0, 10, 8, 7]], 16, "full",
                  "dồn dập, mạnh: xưởng, sản xuất, kho, tốc độ, năng suất"),
    "tin-cay":   (96, 50, [[0, 5, 9, 7], [0, 9, 5, 7], [0, 4, 9, 5]], 8, "light",
                  "chắc, điềm tĩnh: kế toán, giá thành, báo cáo, quản trị, lãnh đạo"),
    "am-ap":     (88, 53, [[0, 9, 5, 7], [0, 4, 5, 7], [0, 5, 2, 7]], 8, "soft",
                  "ấm, gần gũi: nhân sự, lương, khách hàng, câu chuyện con người"),
    "cong-nghe": (110, 57, [[0, 8, 3, 10], [0, 3, 8, 7], [0, 10, 3, 8]], 16, "full",
                  "hiện đại, nhiều không gian: AI, dữ liệu, tự động, màn hình trực quan"),
}
MINOR_ROOTS = {"nang-dong", "cong-nghe"}   # hai kiểu này dựng trên giọng thứ


def make(style, seed, dur, out):
    BPM, KEY, PROGS, DENS, DRUMS, _ = STYLES[style]
    SR = 48000; BEAT = 60 / BPM; BAR = 4 * BEAT
    N = int(SR * dur); L = np.zeros(N); R = np.zeros(N)
    rng = np.random.default_rng(seed)
    prog = PROGS[seed % len(PROGS)]
    minor = style in MINOR_ROOTS
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)

    def add(sig, start, pan=0.0, gain=1.0):
        i = int(start * SR)
        if i >= N or i < 0: return
        sig = sig[: N - i] * gain
        L[i:i+len(sig)] += sig * (1 - pan); R[i:i+len(sig)] += sig * (1 + pan)

    def osc(f, d, harm):
        t = np.arange(int(d * SR)) / SR
        return sum(a * np.sin(2 * np.pi * f * k * t) for k, a in harm)

    def env(n, a, decay=None, r=0.02):
        e = np.ones(n); ai = max(1, int(a * SR)); e[:ai] = np.linspace(0, 1, ai)
        if decay: e *= np.exp(-np.arange(n) / SR * decay)
        ri = min(n, int(r * SR)); e[-ri:] *= np.linspace(1, 0, ri); return e

    def chord(deg):
        # bậc 0/5/7 theo tính chất giọng; bậc khác lấy hợp âm thứ/trưởng tự nhiên trong giọng
        third = 3 if (minor and deg in (0, 5, 7)) or (not minor and deg in (2, 4, 9)) else 4
        r = KEY + deg
        return r - 24, [r + 12, r + 12 + third, r + 19]

    timbre = [((1, 1), (2, .6), (3, .35), (5, .12)), ((1, 1), (3, .4), (5, .2)), ((1, 1), (2, .3), (4, .2), (6, .08))][seed % 3]
    pat = rng.permutation([0, 1, 2, 3, 4, 5, 6, 7])
    nb = int(dur / BAR) + 1
    for b in range(nb):
        root, ch = chord(prog[b % 4]); t0 = b * BAR
        last = b >= nb - 1
        if last: root, ch = chord(0)
        for m in ch:   # nền
            s = osc(hz(m - 12), BAR + 0.3, ((1, 1), (2, .5), (3, .3), (4, .15)))
            add(s * env(len(s), 0.25, r=0.4), t0, gain=0.02 if DRUMS != "soft" else 0.026)
        if last:
            for m in ch + [ch[0] + 12]:
                s = osc(hz(m), 3.0, ((1, 1), (2, .4), (3, .15))); add(s * env(len(s), 0.005, decay=1.4), t0, gain=0.07)
            continue
        notes = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[0] + 12, ch[1], ch[2] + 12]
        for k in range(DENS):   # rải hợp âm
            m = notes[pat[k % 8]] + (12 if (b % 8) >= 4 and k % 4 == 3 else 0)
            s = osc(hz(m), 4 * BEAT / DENS * 1.6, timbre)
            add(s * env(len(s), 0.002, decay=16 if DENS == 16 else 7), t0 + k * 4 * BEAT / DENS,
                pan=(-0.3 if k % 2 else 0.3), gain=0.05 * (1.0 if k % 4 == 0 else 0.7))
        if b < 2: continue
        for k in range(8 if DRUMS != "soft" else 4):   # bass
            step = BEAT / 2 if DRUMS != "soft" else BEAT
            f = hz(root + (12 if k % 2 and DRUMS == "full" else 0))
            s = osc(f, step, ((1, 1), (2, .5), (3, .2)))
            add(s * env(len(s), 0.004, decay=6 if DRUMS != "soft" else 3), t0 + k * step, gain=0.12)
        for q in range(4):   # trống
            tq = t0 + q * BEAT; t = np.arange(int(0.3 * SR)) / SR
            kick = np.sin(2 * np.pi * (48 + 90 * np.exp(-t * 35)) * t) * np.exp(-t * 11)
            if DRUMS == "full" or q in (0, 2):
                add(kick, tq, gain={"full": 0.32, "light": 0.24, "soft": 0.14}[DRUMS])
            if q in (1, 3) and DRUMS != "soft":
                n_ = np.diff(rng.standard_normal(int(0.18 * SR)), prepend=0)
                clap = n_ * np.exp(-np.arange(len(n_)) / SR * 22)
                for off in (0, 0.012, 0.024): add(clap, tq + off, pan=0.05, gain=0.035 if DRUMS == "full" else 0.022)
            h = np.diff(rng.standard_normal(int(0.05 * SR)), n=2, prepend=[0, 0]) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90)
            add(h, tq + BEAT / 2, pan=0.35, gain=0.02 if DRUMS != "soft" else 0.008)
            if DRUMS == "full": add(h * 0.6, tq + BEAT / 4 * 3, pan=-0.35, gain=0.012)
    for D, g in ((0.029, .3), (0.043, .25), (0.061, .2)) + (((0.089, .2), (0.13, .15)) if style == "cong-nghe" else ()):
        d = int(D * SR)
        for c in (L, R):
            y = c.copy()
            for i in range(1, 4): y[d*i:] += c[:-d*i] * g ** i
            c[:] = 0.7 * c + 0.3 * y
    mix = np.stack([L, R], 1)
    fo = min(N, int(2.5 * SR)); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    fi = int(0.4 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    mix = np.tanh(mix / np.abs(mix).max() * 1.4) * 0.85
    w = wave.open(out, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()


if __name__ == "__main__":
    if sys.argv[1:2] == ["--list"]:
        for k, v in STYLES.items(): print(f"{k:10} {v[0]:3} BPM  {v[5]}")
        sys.exit()
    style, seed, dur, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    if style not in STYLES: sys.exit(f"kiểu '{style}' không có; chọn: {', '.join(STYLES)}")
    make(style, seed, dur, out); print("ok", style, seed, out)
