"""Dựng clip KHÔNG giọng đọc: lời đọc trở thành chữ trên hình, nhịp cảnh theo TỐC ĐỘ ĐỌC (Liên chốt 23/10/2026).
Dùng chung cho build.py, mix.py, _calc_gap.py, _nhip_canh.py (một nguồn số liệu, không chép số ở nơi khác).

Chế độ chữ khi clip.py khai NO_VO = True; không khai thì tự nhận: có vo/seg0.flac -> clip cũ có giọng, không có -> chế độ chữ.

Tốc độ đọc (ký tự kể cả dấu cách và dấu câu, trên giây). Chọn thấp hơn chuẩn phụ đề phim vì người xem vừa đọc vừa nhìn thao tác
trên phần mềm họ chưa quen: chuẩn phụ đề Netflix là 17 ký tự/giây tiếng Việt, 20 tiếng Anh (người lớn); giọng đọc thật của
clip này là 18,8 (VI) và 17,2 (EN). Lấy 14 (VI) và 15 (EN) = chậm hơn giọng đọc 20-25 phần trăm. Tiếng Việt chậm hơn vì một từ
là một âm tiết, cùng một ý tiếng Việt cần nhiều từ rời hơn nên mắt phải dừng nhiều hơn."""
import os, re

CPS = {"vi": 14.0, "en": 15.0}
LEAD_READ = 0.7      # mắt tìm tới dòng chữ mới trước khi bắt đầu đọc
MIN_SCENE = 2.2      # cảnh ngắn đến đâu cũng phải đủ thời gian đọc một dòng
MIN_CHUNK = 1.6      # một đoạn chữ hiện không ngắn hơn thế (đoạn ngắn hơn bị gộp vào đoạn kế)


def lang(C, D):
    l = getattr(C, "LANG", None)
    if l: return l
    b = os.path.basename(os.path.abspath(D))
    return b.split("-")[-1] if b.startswith("clip-") and b.split("-")[-1] in CPS else "vi"


def is_text(C, D):
    v = getattr(C, "NO_VO", None)
    return bool(v) if v is not None else not os.path.exists(os.path.join(D, "vo", "seg0.flac"))


def scene_dur(text, l):
    return round(max(MIN_SCENE, len(text) / CPS[l] + LEAD_READ), 2)


def durations(C, D):
    l = lang(C, D)
    return [scene_dur(t, l) for t in C.VO]


def chunks(text, max_chars, l):
    """Cắt lời thành các đoạn chữ vừa hai dòng (max_chars là độ dài tối đa một dòng): theo câu, rồi theo dấu phẩy, rồi theo từ.
    Đoạn quá ngắn (dưới MIN_CHUNK giây đọc) gộp vào đoạn kế. Chữ đầu câu viết hoa, đoạn cắt giữa câu giữ nguyên chữ thường,
    dấu phẩy cuối đoạn bỏ. Trả về danh sách chuỗi."""
    lim = max_chars * 2
    out = []   # (chữ, đầu câu?)
    for p in [p.strip() for p in re.split(r"(?<=[.?!])\s+", text) if p.strip()]:
        first = True
        while len(p) > lim:
            cut = max(p.rfind(", ", 0, lim), p.rfind(": ", 0, lim), p.rfind("; ", 0, lim))   # ưu tiên ngắt ở dấu câu
            if cut < len(p) * 0.3 and len(p) <= lim * 1.6:   # không có dấu câu hợp lý: ngắt ở khoảng trắng gần GIỮA câu cho hai đoạn cân nhau
                mid = len(p) // 2
                cut = min((i for i, ch in enumerate(p) if ch == " " and i < lim), key=lambda i: abs(i - mid), default=-1)
            elif cut < lim * 0.4: cut = p.rfind(" ", 0, lim)
            out.append((p[:cut + 1].strip(), first)); first = False; p = p[cut + 1:].strip()
        out.append((p, first))
    need = MIN_CHUNK * CPS[l]
    merged = []
    for c, f in out:
        if merged and len(merged[-1][0]) < need and len(merged[-1][0]) + 1 + len(c) <= lim: merged[-1] = (merged[-1][0] + " " + c, merged[-1][1])
        else: merged.append((c, f))
    if len(merged) > 1 and len(merged[-1][0]) < need and len(merged[-2][0]) + 1 + len(merged[-1][0]) <= lim:
        c, _ = merged.pop(); merged[-1] = (merged[-1][0] + " " + c, merged[-1][1])
    res = []
    for c, f in merged:
        c = c.rstrip(",;").strip()
        res.append(c[:1].upper() + c[1:] if f else c)
    return res


def timed_chunks(i, text, st0, dur, hold_until, max_chars, l, starts=None):
    """[(bắt đầu, kết thúc, chữ)] của cảnh i: chia dur theo độ dài chữ (hoặc theo `starts` đã khớp hành động, xem sync_starts);
    đoạn cuối giữ tới hold_until (hết cảnh) cho người đọc chậm."""
    cs = chunks(text, max_chars, l); total = sum(len(c) for c in cs); acc = 0; res = []
    for k, c in enumerate(cs):
        a = st0 + dur * acc / total; acc += len(c)
        b = st0 + dur * acc / total
        if starts and len(starts) == len(cs):
            a = st0 + starts[k]; b = st0 + starts[k + 1] if k + 1 < len(cs) else b
        res.append((a, max(b, hold_until) if k == len(cs) - 1 else b, c))
    return res


def chunk_starts(text, max_chars, l, dur):
    """Giây bắt đầu (tính từ đầu cảnh) của từng đoạn chữ trong cảnh: chia dur theo độ dài chữ, như timed_chunks."""
    cs = chunks(text, max_chars, l); total = sum(len(c) for c in cs); acc = 0; out = []
    for c in cs:
        out.append(dur * acc / total); acc += len(c)
    return out


def sync_delay(meta, starts, rate):
    """Số giây phải HOÃN đoạn quay để hành động khớp đoạn chữ của nó. Lúc quay, R.ev("c<k>") ghi mốc bắt đầu hành động
    ứng với đoạn chữ thứ k+1 (đoạn 0 không cần). Đoạn quay chạy lúc cảnh bắt đầu thì hành động tới trước chữ; hoãn d giây
    (đoạn quay đứng ở khung đầu, trang còn nguyên) để mốc c<k> rơi đúng lúc đoạn chữ k hiện. Không có mốc thì không hoãn."""
    ev = (meta or {}).get("events") or {}
    d = 0.0
    for k in range(1, len(starts)):
        e = ev.get(f"c{k}")
        if e is not None:
            d = max(d, starts[k] + 0.05 - e / rate)
    return round(max(0.0, d), 2)


def sync_starts(meta, starts, rate, delay):
    """Giây bắt đầu từng đoạn chữ sau khi khớp hành động: đoạn k hiện KHÔNG SỚM HƠN lúc hành động c<k> diễn ra
    (chữ dẫn không được chạy trước hình, nhưng hành động tới trước chữ thì đã được delay hoãn). Đoạn 0 luôn hiện từ đầu cảnh."""
    ev = (meta or {}).get("events") or {}
    out = [0.0]
    for k in range(1, len(starts)):
        e = ev.get(f"c{k}")
        out.append(max(starts[k], delay + 0.05 + e / rate) if e is not None else starts[k])
        out[-1] = max(out[-1], out[-2] + MIN_CHUNK)
    return out


def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path, items):
    with open(path, "w", encoding="utf-8") as f:
        for n, (a, b, c) in enumerate(items, 1):
            f.write(f"{n}\n{srt_time(a)} --> {srt_time(b)}\n{c}\n\n")
