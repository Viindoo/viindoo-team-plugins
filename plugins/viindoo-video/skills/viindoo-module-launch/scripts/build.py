"""Dựng video.html cho một clip chi tiết ở khổ vuông (sq, 1080x1080) hoặc dọc (v, 1080x1920).
Nội dung clip khai báo trong <clip_dir>/clip.py (VO, CAPS, PLAN); lời đọc ở <clip_dir>/vo/seg*.flac, hoặc (NO_VO) thành chữ trên hình + <OUT>.srt.
Chạy: python3 build.py <clip_dir> sq|v|h   -> <clip_dir>/video_<fmt>.html, <clip_dir>/timeline.json"""
import importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import readtime
clip, fmt = sys.argv[1], sys.argv[2]
D = os.path.abspath(clip)
# Brand dùng chung của plugin: <plugin>/brand/assets (logo-color.svg, logo-inverted.svg, fonts/)
ASSETS = "file://" + os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "brand", "assets")
spec = importlib.util.spec_from_file_location("clip", os.path.join(D, "clip.py")); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)

TEXT = readtime.is_text(C, D)   # clip không giọng: lời đọc thành chữ trên hình, nhịp theo tốc độ đọc (readtime.py)
LG = readtime.lang(C, D)
W, H = {"sq": (1080, 1080), "v": (1080, 1920), "h": (1920, 1080)}[fmt]
# Bố cục từng khổ: khung phần mềm, chữ trên màn hình, phụ đề. Khổ dọc chừa trên/dưới cho giao diện Reels/TikTok/Shorts.
L = {
    "sq": dict(fx=30, fy=112, fw=1020, vh=770, cap_y=34, cap_fs=30, sub_bottom=34, sub_fs=33, sub_w=980, sub_chars=46,
               title_y=600, title_fs=62, logo_y=60, tag_y=760),
    # h: khổ ngang 16:9 cho YouTube / khung nhúng trên trang module
    "h": dict(fx=300, fy=88, fw=1320, vh=760, cap_y=26, cap_fs=32, sub_bottom=30, sub_fs=36, sub_w=1500, sub_chars=70,
              title_y=640, title_fs=78, logo_y=60, tag_y=800),
    "v": dict(fx=30, fy=390, fw=1020, vh=980, cap_y=250, cap_fs=34, sub_bottom=330, sub_fs=40, sub_w=960, sub_chars=34,
              title_y=980, title_fs=72, logo_y=230, tag_y=1270),
}[fmt]
if TEXT:   # chữ là kênh truyền đạt duy nhất: to hơn, tối đa hai dòng, nằm dưới khung phần mềm (khung kết thúc trước vùng chữ)
    L.update({"h": dict(sub_fs=48, sub_w=1560, sub_chars=46, sub_bottom=34),
              "sq": dict(sub_fs=40, sub_w=1000, sub_chars=34, sub_bottom=26),
              "v": dict(sub_fs=44, sub_w=980, sub_chars=30, sub_bottom=330)}[fmt])
# FULL = True (clip hướng dẫn Docs, Liên chốt 06/11/2026): màn phần mềm phủ kín khung hình để người xem
# làm theo được - không khung cửa sổ giả, không nền trống hai bên. Nhãn cảnh xuống đáy để không che menu.
# Mức phóng khoanh vùng chia theo tỷ lệ khung cũ (1320 px) để chữ giao diện hiện cùng cỡ như trước.
FULL = bool(getattr(C, "FULL", False)) and fmt == "h"
ZR = 1.0
if FULL:
    ZR = L["fw"] / W
    L.update(fx=0, fy=0, fw=W, vh=H, cap_y=H - 104, cap_fs=28)
BAR = "" if FULL else '<div class="bbar"><i></i><i></i><i></i><span>Viindoo</span></div>'
FCLS = " full" if FULL else ""
PHOTO = getattr(C, "PHOTO", "assets/photos/")
# Logo màu chuẩn (Viin #00BBCE + doo #7F4282): dùng trên nền trắng (thẻ trắng ở cảnh mở đầu, màn kết).
# logo-inverted.svg (Viin trắng + doo tím) chỉ hợp nền cyan phẳng #00BBCE; giữ biến để dùng khi cần.
LOGO = ASSETS + "/logo-color.svg"
LOGO_ON_CYAN = ASSETS + "/logo-inverted.svg"

N = len(C.VO)
if TEXT:
    dur = readtime.durations(C, D)
else:
    dur = [float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                          os.path.join(D, "vo", f"seg{i}.flac")])) for i in range(N)]
GAP = getattr(C, "GAP", [0.7] + [1.1] * (N - 3) + [0.9])   # nghỉ sau mỗi đoạn: phần màn hình cần thêm thời gian để đọc
st = [getattr(C, "LEAD", 1.6)]                              # chữ tiêu đề hiện trước khi bắt đầu đọc
for i in range(N - 1):
    st.append(st[-1] + dur[i] + GAP[i])
END = round(st[-1] + dur[-1] + 3.2, 2)
SHOTS = {s["file"]: s for s in json.load(open(os.path.join(D, "assets/shots/shots.json")))}


def kw(seg, phrase):
    t = C.VO[seg]; o = t.lower().index(phrase.lower())
    return st[seg] + dur[seg] * (o / len(t)) * 0.97 + 0.1


def win(i):
    a = 0 if i == 0 else st[i] - 0.35
    b = END if i == N - 1 else st[i + 1] - 0.2
    return a, b


AI = getattr(C, "AI_DIR", "assets/ai/")


def vrate(m, t0, t1, delay=0.0):
    """Tốc độ phát đoạn quay (tua nhanh tối đa 2,5 lần) trong cửa sổ [t0, t1], sau khi hoãn delay giây."""
    if t1 and m.get("duration"):
        return round(min(2.5, max(1.0, m["duration"] / max(0.5, t1 - t0 - 0.9 - delay))), 3)
    return 1.0


# SILENT_RATE (Liên 06/11/2026: "các khoảng không có tiếng đang hơi kéo dài, để nhanh hơn một chút"):
# cảnh chỉ có MỘT đoạn quay thì phần quay khớp lời đọc giữ tốc độ cũ, phần chạy tiếp sau khi lời đọc
# dứt (khoảng im) tua lên SILENT_RATE; nhịp nghỉ GAP rút lại đúng bằng phần đã tua để đoạn quay vẫn
# chạy hết tới màn kết quả. Mốc thời gian đổi nên phải trộn lại tiếng (mix.py) sau khi dựng.
SR = float(getattr(C, "SILENT_RATE", 0) or 0)
PIECE = {}      # cảnh -> (tốc độ khi có lời, tốc độ khoảng im)
if SR and not TEXT:
    for i in range(1, N - 1):
        lay = C.PLAN[i]
        if len(lay) != 1 or lay[0][0] != "shot" or lay[0][2] is not None: continue
        m = SHOTS.get(lay[0][1], {})
        if not m.get("video") or GAP[i] < 1.5: continue
        a, b = win(i)
        r = vrate(m, a, b)
        if SR <= r: continue
        GAP = list(GAP); GAP[i] = round(max(1.0, GAP[i] * r / SR), 3)
        PIECE[i] = (r, SR)
    st = [getattr(C, "LEAD", 1.6)]
    for i in range(N - 1):
        st.append(st[-1] + dur[i] + GAP[i])
    END = round(st[-1] + dur[-1] + 3.2, 2)
CUR = [None]    # cảnh đang dựng, để media()/zoom_times() biết cảnh nào có tốc độ hai khúc


def vt_to_t(i, base, e, rate):
    """Thời điểm trên clip khi đoạn quay (bắt đầu ở base) tới giây e của chính nó."""
    if i in PIECE:
        r, r2 = PIECE[i]; ts = st[i] + dur[i]; e_ts = max(0.0, ts - base) * r
        return base + e / r if e <= e_ts else ts + (e - e_ts) / r2
    return base + e / rate


def scene_delay(i, fname, t0, t1):
    """Chế độ chữ: hoãn đoạn quay của cảnh i để hành động khớp đoạn chữ (xem readtime.sync_delay). Lặp vì tốc độ phụ thuộc độ hoãn."""
    m = SHOTS.get(fname, {})
    if not (TEXT and m.get("video") and m.get("events")): return 0.0
    starts = readtime.chunk_starts(C.VO[i], L["sub_chars"], LG, dur[i]); d = 0.0
    for _ in range(4):
        d = readtime.sync_delay(m, starts, vrate(m, t0, t1, d))
    return d


def media(fname, w, h, t0, t1=None, delay=0.0):
    """Ảnh tĩnh, hoặc đoạn quay thao tác thật nếu shots.json có "video" cho ảnh này. Đoạn quay chạy từ khi lớp hiện ra;
    dài hơn thời gian của lớp thì tua nhanh (tối đa 2,5 lần) để luôn kết thúc ở màn kết quả."""
    m = SHOTS.get(fname, {})
    rate = 1.0
    if m.get("video"):
        rate = vrate(m, t0, t1, delay)
        two = ""
        if CUR[0] in PIECE:
            rate, r2 = PIECE[CUR[0]]
            two = f'data-ts="{st[CUR[0]] + dur[CUR[0]]:.2f}" data-rate2="{r2}" '
        return (f'<video src="assets/shots/{m["video"]}" muted playsinline preload="auto" data-t0="{t0 + 0.3 + delay:.2f}" data-rate="{rate}" {two}'
                f'style="width:{w:.0f}px;height:{h:.0f}px;object-fit:cover;object-position:top"></video>')
    # object-fit cover + top: hạ "h" trong shots.json là cắt bớt phần dưới (màn dọc nhiều khoảng trống) mà không phải sửa file ảnh
    return f'<img src="assets/shots/{fname}" style="width:{w:.0f}px;height:{h:.0f}px;object-fit:cover;object-position:top">'


def zoom_times(i, fname, t0, t1, delay, zs):
    """Thời điểm camera phóng vào từng ô. Mốc theo cụm từ lời đọc (kw) như cũ; mốc "@tên" là hành động đã ghi lúc quay (R.ev),
    camera tới trước hành động 0,7 giây để ô đã nằm trong khung khi người dùng bấm. Hai lần phóng cách nhau tối thiểu 1,8 giây."""
    m = SHOTS.get(fname, {}); rate = vrate(m, t0, t1, delay); out = []
    has_ev = any(z[1] and z[1].startswith('@') for z in zs)
    for z in zs:
        if z[1] and z[1].startswith("@"):
            e = (m.get("events") or {}).get(z[1][1:])
            if e is None: print("  !! thiếu mốc", fname, z[1]); e = 0.0
            t = vt_to_t(i, t0 + 0.3 + delay, e, rate) - 0.7
        else:
            t = kw(i, z[1]) if z[1] else t0 + 1.0
        if out and has_ev: t = max(t, out[-1][1] + 1.8)
        out.append((z[0], t))
    return out


def shot_layer(fname, t0, t1, zooms, mock=None, fit=False, delay=0.0):
    """Khung trình duyệt chứa ảnh màn hình; camera phóng vào từng ô (nhãn) đúng lúc lời đọc nhắc tới.
    mock=(fx, fy, S): ảnh minh họa AI 1600x900 trong AI_DIR (mặc định <clip_dir>/assets/ai/), phóng chậm vào điểm (fx, fy), có nhãn Hình minh họa."""
    m = SHOTS[fname] if not mock else {"w": 1600, "h": 900, "boxes": []}
    FW, VH = L["fw"], L["vh"]
    K = FW / m["w"]; ch = m["h"] * K
    base = max(1.0, VH / ch)                       # ảnh luôn phủ kín khung (khổ dọc: luôn đang phóng)
    if fit: base = 1.0                             # fit=True: hiện trọn chiều ngang ảnh (màn máy tính để bàn), không cắt hai bên
    boxes = {b["label"]: b for b in m.get("boxes", [])}

    def target(b):
        bw, bh = (b["x1"] - b["x0"]) * K, (b["y1"] - b["y0"]) * K
        S = max(base, min(2.6 * ZR, max(1.9 * ZR, 0.86 * FW / bw), 0.75 * VH / bh))   # tối thiểu 1,9 lần (khung 1320) để chữ giao diện đọc được
        if bw * S <= FW * 0.95:
            fx = (b["x0"] + b["x1"]) / 2 / m["w"]
        else:                                      # ô rộng hơn khung: nhìn nửa trái, nơi có chữ nhãn
            fx = b["x0"] / m["w"] + 0.46 * FW / (S * FW)
        fy = (b["y0"] + b["y1"]) / 2 / m["h"] if bh * S <= VH * 0.9 else b["y0"] / m["h"] + 0.42 * VH / (S * ch)
        return S, fx, fy

    if mock:
        fx, fy, S = mock
        cam = f"{t0:.2f},{base},{fx},{fy};{t0+1.0:.2f},{base},{fx},{fy};{t0+3.2:.2f},{max(base, S)},{fx},{fy};{t1:.2f},{max(base, S)+0.08:.2f},{fx},{fy}"
        return (f'<div class="abs frame{FCLS}" data-win="{t0:.2f},{t1:.2f}" style="left:{L["fx"]}px;top:{L["fy"]}px;width:{FW}px">'
                f'{BAR}'
                f'<div class="view" style="height:{VH}px"><div class="cam" data-cam="{cam}" style="width:{FW}px;height:{ch:.0f}px">'
                f'<img src="{AI}{fname}" style="width:{FW}px;height:{ch:.0f}px"></div><div class="illus">Hình minh họa</div></div></div>')
    first = next((boxes[z[0]] for z in zooms if z[0] in boxes), None)
    s0 = (base, *(target(first)[1:] if first and base > 1.2 else (.5, .5)))
    cam = [(t0, *s0)]; rings = []
    for k, (lab, t) in enumerate(zooms):
        nxt = zooms[k + 1][1] if k + 1 < len(zooms) else t1
        b = boxes.get(lab)
        if not b: print("  !! thiếu ô", fname, lab); continue
        S, fx, fy = target(b)
        cam += [(t - 0.05, *cam[-1][1:]), (t + 0.8, S, fx, fy), (nxt - 0.3, S, fx, fy)]
        rings.append((b, t + 0.7, nxt - 0.2))
    cam.append((t1, *cam[-1][1:]))
    if m.get("video"): rings = []                 # đoạn quay: màn đổi liên tục, vòng khoanh theo ảnh tĩnh sẽ lệch -> chỉ giữ camera
    camtxt = ";".join(f"{t:.2f},{s:.3f},{x:.4f},{y:.4f}" for t, s, x, y in cam)
    rs = "".join(f'<div class="ring" data-win="{a:.2f},{z:.2f}" style="left:{b["x0"]*K-5:.0f}px;top:{b["y0"]*K-5:.0f}px;'
                 f'width:{(b["x1"]-b["x0"])*K+10:.0f}px;height:{(b["y1"]-b["y0"])*K+10:.0f}px"></div>' for b, a, z in rings)
    return (f'<div class="abs frame{FCLS}" data-win="{t0:.2f},{t1:.2f}" style="left:{L["fx"]}px;top:{L["fy"]}px;width:{FW}px">'
            f'{BAR}'
            f'<div class="view" style="height:{VH}px"><div class="cam" data-cam="{camtxt}" style="width:{FW}px;height:{ch:.0f}px">'
            f'{media(fname, FW, ch, t0, t1, delay)}{rs}</div></div></div>')


def phone_layer(fname, t0, t1, lab=None, tz=None):
    """Ảnh chụp màn hình điện thoại đặt trong khung máy, giữa vùng nội dung; ô nhãn lab sáng lên tại tz."""
    m = SHOTS[fname]; PH = min(L["vh"] + 16, (W - 180) * m["h"] / m["w"]); PW = PH * m["w"] / m["h"]; K = PW / m["w"]
    x = (W - PW) / 2; y = L["fy"] + 10 + (L["vh"] + 16 - PH) / 2
    ring = ""
    b = next((b for b in m.get("boxes", []) if b["label"] == lab), None)
    if b and tz and not m.get("video"):
        ring = (f'<div class="ring" data-win="{tz:.2f},{t1-0.2:.2f}" style="left:{b["x0"]*K-5:.0f}px;top:{b["y0"]*K-5:.0f}px;'
                f'width:{(b["x1"]-b["x0"])*K+10:.0f}px;height:{(b["y1"]-b["y0"])*K+10:.0f}px"></div>')
    return (f'<div class="abs phone" data-win="{t0:.2f},{t1:.2f}" style="left:{x-14:.0f}px;top:{y-14:.0f}px;padding:14px;'
            f'animation:popIn .6s {t0:.2f}s"><div style="position:relative;width:{PW:.0f}px;height:{PH:.0f}px;overflow:hidden;border-radius:30px">'
            f'{media(fname, PW, PH, t0, t1)}{ring}</div></div>')


def photo_layer(img, t0, t1, pos, tag=None):
    s = (f'<div class="abs photo" data-win="{t0:.2f},{t1:.2f}"><img src="{PHOTO}{img}" '
         f'style="object-position:{pos};animation:kb {t1-t0+0.6:.1f}s linear {t0:.2f}s"></div>'
         f'<div class="abs shade" data-win="{t0:.2f},{t1:.2f}"></div>')
    if tag:
        s += (f'<div class="abs ptag" data-win="{t0:.2f},{t1:.2f}" style="left:60px;top:{L["tag_y"]}px">'
              f'<span style="font-size:{L["title_fs"]*0.62:.0f}px;animation:popIn .5s {t0+0.4:.2f}s">{tag}</span></div>')
    return s


def pill(text, t0, t1):
    return (f'<div class="abs cap" data-win="{t0:.2f},{t1:.2f}" style="left:0;right:0;top:{L["cap_y"]}px;text-align:center">'
            f'<span style="font-size:{L["cap_fs"]}px;padding:12px 30px;animation:upIn .5s {t0+0.15:.2f}s">{text}</span></div>')


def hook_layer(t0, t1):
    img, pos = C.HOOK_PHOTO
    return (photo_layer(img, t0, t1, pos.get(fmt, pos["sq"]))
            + f'<div class="abs hlogo" data-win="{t0:.2f},{t1:.2f}" style="left:60px;top:{L["logo_y"]}px"><img src="{LOGO}"></div>'
            + f'<h1 class="abs htitle" style="left:60px;right:60px;top:{L["title_y"]}px;font-size:{L["title_fs"]}px;animation:upIn .7s .2s">{C.TITLE}</h1>')


def before_after(i, arg, t0, t1):
    pt, ps, ht, hs = arg
    h = f'<div class="abs ba" data-win="{t0:.2f},{t1:.2f}" style="inset:0">'
    if fmt in ("sq", "h"):
        h += f'<div class="bt" style="top:150px;font-size:44px;animation:upIn .5s {t0:.2f}s">{C.CAPS[i]}</div>'
        cards = [(40, 300, 440, 380), (600, 300, 440, 380)]; arr = (480, 430, 120, '→', 80)
        if fmt == "h": cards = [(x + 420, y, w, hh) for x, y, w, hh in cards]; arr = (arr[0] + 420, *arr[1:])
    else:
        h += f'<div class="bt" style="top:360px;font-size:54px;padding:0 60px;animation:upIn .5s {t0:.2f}s">{C.CAPS[i]}</div>'
        cards = [(90, 560, 900, 330), (90, 1020, 900, 330)]; arr = (0, 890, 1080, '↓', 100)
    for k, (cls, role, txt, sub) in enumerate([("pain", "Trước", pt, ps), ("hi", "Sau", ht, hs)]):
        x, y, w, hh = cards[k]
        tp = t0 + 0.3 + k * 1.3
        h += (f'<div class="card {cls}" style="left:{x}px;top:{y}px;width:{w}px;min-height:{hh}px;animation:popIn .5s {tp:.2f}s">'
              f'<div class="role">{role}</div><div class="txt" style="font-size:{46 if fmt=="v" else 40}px">{txt}</div>'
              f'<div class="sub" style="font-size:{32 if fmt=="v" else 27}px">{sub}</div></div>')
    x, y, w, ch, fs = arr
    h += f'<div class="arr" style="left:{x}px;top:{y}px;width:{w}px;font-size:{fs}px;animation:fadeIn .4s {t0+1.4:.2f}s">{ch}</div>'
    return h + '</div>'


def cover_layer(img, t0, t1, opt):
    """Ảnh bìa mở đầu clip (Liên 06/11/2026): màn phần mềm thật phủ kín làm nền, bên trái logo,
    dòng nhỏ (kicker) và tiêu đề lớn (TITLE). Cùng bố cục với ảnh thumbnail YouTube của clip."""
    fs = {"sq": 72, "h": 96, "v": 84}[fmt]
    x = {"sq": 70, "h": 120, "v": 70}[fmt]
    w = {"sq": 940, "h": 980, "v": 940}[fmt]
    k = opt.get("kicker") or getattr(C, "KICKER", "")
    return (f'<div class="abs cvbg" data-win="{t0:.2f},{t1:.2f}"><img src="assets/shots/{img}"></div>'
            f'<div class="abs cvwash" data-win="{t0:.2f},{t1:.2f}"></div>'
            f'<div class="abs" data-win="{t0:.2f},{t1:.2f}" style="left:{x}px;top:0;bottom:0;width:{w}px;display:flex;'
            f'flex-direction:column;justify-content:center;gap:40px">'
            f'<img class="cvlogo" src="{LOGO}" style="align-self:flex-start;animation:fadeIn .6s {t0+0.05:.2f}s both">'
            + (f'<div class="cvk" style="font-size:{fs*0.32:.0f}px;animation:upIn .5s {t0+0.2:.2f}s both">{k}</div>' if k else "")
            + f'<div class="cvt" style="font-size:{fs}px;animation:upIn .6s {t0+0.35:.2f}s both">{opt.get("title") or C.TITLE}</div>'
            f'</div>')


def section_layer(i, img, t0, t1, kicker=None):
    """Thẻ chuyển phần: ảnh màn hình làm mờ phía sau, tiêu đề lớn ở giữa (CAPS[i]), dòng nhỏ phía trên (kicker)."""
    fs = {"sq": 76, "h": 92, "v": 88}[fmt]
    k = f'<div class="seck" style="font-size:{fs*0.36:.0f}px;animation:upIn .5s {t0+0.1:.2f}s">{kicker}</div>' if kicker else ""
    return (f'<div class="abs secbg" data-win="{t0:.2f},{t1:.2f}"><img src="assets/shots/{img}"></div>'
            f'<div class="abs secwash" data-win="{t0:.2f},{t1:.2f}"></div>'
            f'<div class="abs secbox" data-win="{t0:.2f},{t1:.2f}">{k}'
            f'<div class="sect" style="font-size:{fs}px;animation:popIn .6s {t0+0.25:.2f}s">{C.CAPS[i]}</div></div>')


# Biểu tượng nét cho màn danh sách: vẽ thẳng bằng SVG, không phụ thuộc bộ phông ngoài.
GLYPH = {
    "cong-ty": '<path d="M3 21h18M5 21V5a1 1 0 011-1h7a1 1 0 011 1v16M14 21V9h4a1 1 0 011 1v11"/><path d="M8 7h2M8 11h2M8 15h2M17 13h0M17 17h0"/>',
    "nguoi-dung": '<path d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>',
    "san-pham": '<path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><path d="M3.3 7L12 12l8.7-5M12 22V12"/>',
    "danh-ba": '<path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/><circle cx="12" cy="9" r="2"/><path d="M9 14c.6-1.2 1.7-2 3-2s2.4.8 3 2"/>',
    "du-lieu": '<path d="M3 3v18h18"/><path d="M7 15l3-4 3 3 4-6"/>',
    "email": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/>',
    "gio-hang": '<circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/><path d="M1 1h3l2.6 12.4a2 2 0 002 1.6h8.7a2 2 0 002-1.6L21 6H6"/>',
    "hoa-don": '<path d="M5 2v20l3-2 2 2 2-2 2 2 2-2 3 2V2l-3 2-2-2-2 2-2-2-2 2z"/><path d="M9 8h6M9 12h6"/>',
    "bao-cao": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 17v-5M12 17V7M16 17v-8"/>',
    "tu-dong": '<path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/><circle cx="12" cy="12" r="4"/>',
    "ung-dung": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "kho": '<path d="M3 21V9l9-6 9 6v12"/><path d="M9 21v-7h6v7"/>',
}


def bullets_layer(i, img, t0, t1, opt):
    """Màn tổng quát của clip cụm nghiệp vụ: tiêu đề lớn + danh sách đánh số, mỗi mục hiện đúng lúc
    lời đọc nhắc tới nó. `items` là list chữ; `at` là cụm từ trong lời đọc của chính đoạn này (thiếu
    thì rải đều). Mục chưa tới lượt bị ẩn nhờ animation-fill-mode both, nên phải bọc trong một lớp
    riêng mang data-win - renderAt ghi đè opacity của mọi phần tử có data-win."""
    items = opt["items"]
    at = (opt.get("at") or []) + [None] * len(items)
    ts = [kw(i, at[k]) if at[k] else t0 + 1.0 + k * 1.4 for k in range(len(items))]
    bieu = (opt.get("icons") or []) + [None] * len(items)
    fs = {"sq": 34, "h": 40, "v": 36}[fmt]
    x = {"sq": 70, "h": 200, "v": 60}[fmt]
    top = {"sq": 265, "h": 300, "v": 600}[fmt]   # chừa khoảng thở giữa tiêu đề và danh sách
    buoc = (fs + 46)
    h = (f'<div class="abs secbg" data-win="{t0:.2f},{t1:.2f}"><img src="assets/shots/{img}"></div>'
         f'<div class="abs secwash" data-win="{t0:.2f},{t1:.2f}"></div>'
         f'<div class="abs" data-win="{t0:.2f},{t1:.2f}" style="inset:0">')
    if opt.get("kicker"):
        h += (f'<div class="abs seck" style="left:{x}px;top:{top-150}px;font-size:{fs*0.62:.0f}px;'
              f'animation:upIn .5s {t0+0.1:.2f}s both">{opt["kicker"]}</div>')
    h += (f'<div class="abs mont" style="left:{x}px;top:{top-95}px;font-weight:800;font-size:{fs+26}px;'
          f'color:var(--heading);animation:upIn .5s {t0+0.25:.2f}s both">{opt["title"]}</div>')
    # xếp chồng bằng flex chứ không đặt toạ độ từng dòng: mục dài xuống dòng thì các mục sau tự đẩy
    # xuống, không đè lên nhau
    h += (f'<div class="abs" style="left:{x}px;right:{x}px;top:{top}px;display:flex;flex-direction:column;'
          f'gap:{buoc - fs - 20}px">')
    for k, txt in enumerate(items):
        g = GLYPH.get(bieu[k], "")
        icon = (f'<span style="flex:0 0 auto;margin-left:auto;opacity:.5"><svg width="{fs+14}" height="{fs+14}" '
                f'viewBox="0 0 24 24" fill="none" stroke="var(--secondary)" stroke-width="1.6" '
                f'stroke-linecap="round" stroke-linejoin="round">{g}</svg></span>') if g else ""
        h += (f'<div style="display:flex;align-items:center;gap:22px;background:rgba(255,255,255,.72);'
              f'border-radius:{fs}px;padding:{fs*0.42:.0f}px {fs*0.7:.0f}px;box-shadow:0 6px 20px rgba(33,39,43,.07);'
              f'animation:upIn .45s {ts[k]:.2f}s both">'
              f'<span class="mont" style="flex:0 0 auto;width:{fs+14}px;height:{fs+14}px;border-radius:50%;'
              f'background:var(--primary);color:#fff;font-weight:800;font-size:{fs-8}px;display:flex;'
              f'align-items:center;justify-content:center">{k+1}</span>'
              f'<span class="mont" style="font-weight:700;font-size:{fs}px;line-height:1.3;'
              f'color:var(--heading)">{txt}</span>{icon}</div>')
    return h + "</div></div>"


def badge(text, t0, t1):
    """Nhãn góc cố định cho cả một phần (BADGE trong clip.py): góc phải trên khung phần mềm."""
    right = W - (L["fx"] + L["fw"]) + 14
    return (f'<div class="abs badge" data-win="{t0:.2f},{t1:.2f}" style="right:{right}px;top:{L["fy"]-22}px">'
            f'<span style="font-size:{26 if fmt=="v" else 22}px">{text}</span></div>')


def cta_layer(t0, t1):
    y = {"sq": (150, 380, 600, 800), "h": (140, 380, 590, 780), "v": (520, 760, 1030, 1260)}[fmt]
    return (f'<div class="abs endbg"></div>'
            f'<div class="abs elogo" style="top:{y[0]}px;animation:popIn .6s {t0+0.1:.2f}s"><img src="{LOGO}" style="width:{520 if fmt=="v" else 440}px"></div>'
            f'<div class="abs etag" style="top:{y[1]}px;font-size:{60 if fmt=="v" else 50}px;animation:upIn .5s {t0+0.3:.2f}s">{C.CAPS[-1]}</div>'
            f'<div class="abs ectaw" style="top:{y[2]}px"><span class="ecta" style="font-size:{46 if fmt=="v" else 40}px;padding:22px 52px;animation:popIn .5s {t0+0.9:.2f}s">{getattr(C, "CTA", "Đặt lịch demo")}</span></div>'
            f'<div class="abs eweb" style="top:{y[3]}px;font-size:{getattr(C, "WEB_FS", 36)+6 if fmt=="v" else getattr(C, "WEB_FS", 36)}px;animation:fadeIn .6s {t0+1.4:.2f}s">{getattr(C, "WEB", "viindoo.com")}</div>')


SYNC = {}   # cảnh -> (độ hoãn, tốc độ) của đoạn quay, để đoạn chữ khớp hành động (readtime.sync_starts)
S = []
for i in range(N):
    a, b = win(i)
    CUR[0] = i
    layers = C.PLAN[i]
    ts = [a if ph is None else kw(i, ph) for _, _, ph, _ in layers] + [b]
    h = ""
    for k, (kind, arg, ph, opt) in enumerate(layers):
        t0, t1 = ts[k], ts[k + 1] + (0.35 if k + 1 < len(layers) else 0)
        if kind == "hook":
            h += hook_layer(t0, t1)
        elif kind == "photo":
            h += photo_layer(arg, t0, t1, opt["pos"].get(fmt, opt["pos"]["sq"]), opt.get("tag"))
        elif kind == "shot":
            dl = scene_delay(i, arg, t0, t1) if k == 0 and ph is None else 0.0
            if dl or SHOTS.get(arg, {}).get("events"): SYNC[i] = (dl, vrate(SHOTS.get(arg, {}), t0, t1, dl), arg)
            h += shot_layer(arg, t0, t1, zoom_times(i, arg, t0, t1, dl, opt.get("zoom", [])), fit=opt.get("fit", False), delay=dl)
            h += pill(C.CAPS[i], t0, t1)
        elif kind == "mock":
            h += shot_layer(arg, t0, t1, [], mock=opt["focus"])
            h += pill(C.CAPS[i], t0, t1)
        elif kind == "phone":
            z = opt.get("zoom")
            h += phone_layer(arg, t0, t1, z[0] if z else None, kw(i, z[1]) if z else None)
            h += pill(C.CAPS[i], t0, t1)
        elif kind == "before_after":
            h += before_after(i, arg, t0, t1)
        elif kind == "section":
            h += section_layer(i, arg, t0, t1, opt.get("kicker"))
        elif kind == "cover":
            h += cover_layer(arg, t0, t1, opt)
        elif kind == "bullets":
            h += bullets_layer(i, arg, t0, t1, opt)
        elif kind == "cta":
            h += cta_layer(t0, t1)
    B = getattr(C, "BADGE", None)   # (cảnh đầu, cảnh cuối, chữ): nhãn góc cho cả một phần, thay cho việc nói "mới" ở từng cảnh
    if B and B[0] <= i <= B[1]:
        h += badge(B[2], a + 0.2 if i == B[0] else a, b)
    S.append((a, b, h))

# phụ đề: cắt theo câu rồi theo độ dài dòng của khổ hình
subs = []
srt_items = []
if TEXT:
    # chữ trên hình: mỗi đoạn hiện đủ thời gian đọc, đoạn cuối của cảnh giữ tới hết cảnh
    for i, t in enumerate(C.VO):
        hold = (st[i + 1] - 0.25) if i + 1 < N else (st[i] + dur[i] + 1.5)
        sy = None
        if i in SYNC:
            m_ = SHOTS[SYNC[i][2]]
            sy = readtime.sync_starts(m_, readtime.chunk_starts(t, L["sub_chars"], LG, dur[i]), SYNC[i][1], SYNC[i][0])
        for x0, x1, c in readtime.timed_chunks(i, t, st[i], dur[i], hold, L["sub_chars"], LG, sy):
            srt_items.append((x0, x1, c))
            subs.append(f'<span data-win="{x0:.2f},{x1:.2f}" style="font-size:{L["sub_fs"]}px;max-width:{L["sub_w"]}px;'
                        f'padding:12px 30px;line-height:1.3;font-weight:500;text-wrap:balance">{c}</span>')
    if fmt == "h" and getattr(C, "OUT", None):   # tệp phụ đề cho YouTube, cùng tên gốc với video, cùng nhịp với chữ trên hình
        readtime.write_srt(C.OUT + ".srt", srt_items); print("srt", C.OUT + ".srt")
else:
  for i, t in enumerate(C.VO):
    parts = [p.strip() for p in re.split(r"(?<=[.?!:])\s+", t) if p.strip()]
    chunks = []
    for p in parts:
        while len(p) > L["sub_chars"] * 2:
            cut = p.rfind(", ", 0, L["sub_chars"] * 2)
            if cut < 15: cut = p.rfind(" ", 0, L["sub_chars"] * 2)
            chunks.append(p[:cut + 1].strip()); p = p[cut + 1:].strip()
        chunks.append(p)
    total = sum(len(c) for c in chunks); acc = 0
    for c in chunks:
        x0 = st[i] + dur[i] * acc / total; acc += len(c); x1 = st[i] + dur[i] * acc / total
        c = c.rstrip(":"); c = c[0].upper() + c[1:]
        subs.append(f'<span data-win="{x0:.2f},{x1+0.12:.2f}" style="font-size:{L["sub_fs"]}px;max-width:{L["sub_w"]}px;'
                    f'padding:10px 26px;line-height:1.32">{c}</span>')

body = "\n".join(f'<div class="scene" data-in="{a:.2f}" data-out="{b:.2f}">{h}</div>' for a, b, h in S)
tpl = open(os.path.join(HERE, "template.html")).read()
for k, v in {"[[W]]": W, "[[H]]": H, "[[END]]": END, "[[FMT]]": fmt, "[[TITLE]]": f"{C.SLUG} - {re.sub('<[^>]+>', ' ', C.TITLE)}",
             "[[ASSETS]]": ASSETS, "[[FMT_CSS]]": f'#sub{{bottom:{L["sub_bottom"]}px;height:60px}}'}.items():
    tpl = tpl.replace(k, str(v))
# NO_SUB = True trong clip.py: bo han phu de dong duoi
# (clip cum nghe bang giong doc, chu chay duoi lam nguoi xem roi mat khoi thao tac)
if getattr(C, "NO_SUB", False): subs = []
tpl = tpl.replace("<!--SCENES-->", body).replace("<!--SUBS-->", "\n".join(subs))
open(os.path.join(D, f"video_{fmt}.html"), "w").write(tpl)
json.dump({"starts": st, "dur": dur, "END": END, "text_mode": TEXT}, open(os.path.join(D, "timeline.json"), "w"))
print(clip, fmt, "END", END, [round(x, 1) for x in st])
