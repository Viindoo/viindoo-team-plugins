# -*- coding: utf-8 -*-
"""Sơ đồ BPMN 2.0 (SVG) cho bộ quy trình ứng dụng, sinh từ dữ liệu luồng tường minh (handbook.SO_DO của dự án).

Mỗi quy trình có một hoặc nhiều luồng; mỗi luồng là các nút (bước trong bảng, việc ngoài phần mềm, sự kiện, cổng, quy trình con)
và các cạnh có nhãn điều kiện. Quy ước theo brand.yaml activity_colors của Viindoo (đọc file, không viết cứng màu):
user task, service task, manual task, call activity; start mảnh, timer start, end đậm, link ném đặc / bắt rỗng, cổng X.
Cổng rẽ nhánh và cổng gộp là hai nút riêng (không cổng nào vừa gộp vừa rẽ). Cổng: nhánh chính ra cạnh phải, nhánh khác ra cạnh dưới.
Dùng chung cho bản HTML (SVG nhúng) và bản Word (SVG -> PNG qua Chrome for Testing, xem chrome_headless.py).
"""
import html
import os
import pathlib
import re
import textwrap

import yaml

import bpmn_geometry_check as K
import common

D = common.load("handbook")

BRAND_YAML = os.environ.get("VIINDOO_BRAND_YAML") or str(common.brand_yaml())   # màu BPMN của brand Viindoo (viindoo-presales)


def _colors():
    ac = yaml.safe_load(open(BRAND_YAML, encoding="utf-8"))["bpmn_palette"]["activity_colors"]
    if "call_activity" not in ac:
        raise SystemExit(f"{BRAND_YAML} chưa có bpmn_palette.activity_colors.call_activity (ô gọi quy trình con) - "
                         "cần bản viindoo-presales có khai báo này")
    m = {"user": "user_task", "service": "service_task", "manual": "manual_task", "call": "call_activity"}
    col = {k: (ac[v]["fill"], ac[v]["stroke"]) for k, v in m.items()}
    return col, int(ac["call_activity"].get("stroke_width", 3))


COL, CALL_W = _colors()
LABEL_COL = "#7F4282"  # nhãn điều kiện trên mũi tên (tím thương hiệu)
TEN_LOAI = {"user": "Làm trên Viindoo", "service": "Hệ thống tự làm", "manual": "Làm ngoài phần mềm", "call": "Làm theo quy trình con"}

# kích thước (px trong viewBox). G: bước lưới định tuyến; tâm mọi nút nằm trên lưới. Cỡ chữ nhỏ nhất trên sơ đồ là F_MIN.
G = 12
X0, TOP = 2, 12
BW, BH, POOL_W, LANE_W = 108, 52, 34, 108   # BW 108: viền ô lệch nửa bước lưới, rãnh giữa hai cột luôn có một vạch giao cắt hợp lệ
GW, EW = 44, 34
LINE, F_TASK, F_LBL, F_MIN, LBL_H = 16, 13, 12, 12, 14
EV_LBL_W, GW_LBL_W = 100, 104       # bề rộng tối đa của nhãn sự kiện, nhãn câu hỏi của cổng
C_BEND, C_CROSS, N_ORDER = 5, 9, 5  # chi phí góc gấp, giao cắt (đơn vị: bước lưới); số thứ tự định tuyến ngẫu nhiên thử thêm
MAX_W = 1320          # HTML/PDF và Word cùng khổ A4 ngang: 1030px / 1320 = 0,78 -> chữ 12px = 7,02pt
MAX_W_HTML = MAX_W
XEP_CHONG = True      # xếp việc ngoài phần mềm đi kèm ngay dưới / trên bước của nó (bớt cột, bớt phần)
MAX_H = 714           # cao tối đa một hình để vừa một trang A4 ngang ở tỉ lệ 0,78

EVENTS = ("start", "timer", "end", "link_throw", "link_catch", "wait")


def e(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- biểu tượng
def icon(kind, x, y, s=1.0):
    f, c = COL.get(kind, ("#fff", "#666"))
    if kind == "user":
        return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{c}" stroke-width="1.4">'
                '<circle cx="7" cy="5" r="3.2"/><path d="M1.5,15 C1.5,9.5 12.5,9.5 12.5,15 Z"/></g>')
    if kind == "service":
        return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{c}" stroke-width="1.4">'
                '<circle cx="7.5" cy="7.5" r="5.2" stroke-width="3" stroke-dasharray="2.2 1.9"/><circle cx="7.5" cy="7.5" r="2.2"/></g>')
    if kind == "manual":
        return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{c}" stroke-width="1.3" stroke-linejoin="round">'
                '<path d="M3,15 L3,6.5 M3,8 L3,3 M5.6,8 L5.6,1.5 M8.2,8 L8.2,2 M10.8,8.5 L10.8,3.5 M3,15 L11,15 C12.5,13 13.8,10 14.5,7.5 '
                'L13,6.8 L10.8,10 M10.8,8.5 L10.8,10" stroke-linecap="round"/></g>')
    return ""


def icon_svg(kind, size=14):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 16 16" class="ic">{icon(kind, 0.5, 0.5)}</svg>'


def _plus(cx, by, c):
    return (f'<rect x="{cx - 6}" y="{by - 13}" width="12" height="12" fill="#fff" stroke="{c}" stroke-width="1.2"/>'
            f'<path d="M{cx - 3.5},{by - 7}H{cx + 3.5}M{cx},{by - 10.5}V{by - 3.5}" stroke="{c}" stroke-width="1.3"/>')


def _event(kind, cx, cy, r):
    sw = {"start": 1.3, "timer": 1.3, "end": 3.6, "link_throw": 1.3, "link_catch": 1.3, "wait": 1.3}[kind]
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#333" stroke-width="{sw}"/>']
    if kind in ("link_throw", "link_catch", "wait"):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 3.5}" fill="none" stroke="#333" stroke-width="1"/>')
    if kind in ("link_throw", "link_catch"):
        fill = "#333" if kind == "link_throw" else "#fff"
        o.append(f'<path d="M{cx - 7},{cy - 3.5}H{cx + 1}V{cy - 8}L{cx + 8},{cy}L{cx + 1},{cy + 8}V{cy + 3.5}H{cx - 7}Z" '
                 f'fill="{fill}" stroke="#333" stroke-width="1.2"/>')
    if kind == "wait":
        o.append(f'<rect x="{cx - 5.5}" y="{cy - 7}" width="11" height="14" fill="#fff" stroke="#333" stroke-width="1.1"/>'
                 f'<path d="M{cx - 3.5},{cy - 3.5}H{cx + 3.5}M{cx - 3.5},{cy}H{cx + 3.5}M{cx - 3.5},{cy + 3.5}H{cx + 3.5}" stroke="#333" stroke-width="1"/>')
    if kind == "timer":
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 5}" fill="none" stroke="#333" stroke-width="1.2"/>'
                 f'<path d="M{cx},{cy}V{cy - r + 8}M{cx},{cy}H{cx + r - 9}" stroke="#333" stroke-width="1.3"/>')
    return "".join(o)


# ---------------------------------------------------------------- đồ thị từ dữ liệu
def _steps(q):
    return q["buoc"]


def build_flows(q):
    """Danh sách luồng: dict(ten, nodes{id: node}, edges[(a, b, nhãn)]). node: kind, lane, text, step, goi."""
    steps = _steps(q)
    out = []
    for fl in D.SO_DO[q["code"]]:
        nodes, edges = {}, []

        def node(i):
            if i in nodes:
                return nodes[i]
            spec = fl["nut"].get(i)
            m = re.fullmatch(r"(\d+)(n?)", i)
            if m and (spec is None or spec[0] == "manual"):
                k = int(m.group(1))
                vt, viec, vd, ngoai = steps[k - 1]
                if m.group(2):
                    lane = spec[1] if spec else vt
                    text = (spec[2] if spec and len(spec) > 2 and spec[2] else ngoai)
                    nd = dict(kind="manual", lane=lane, text=text, step=k, num=False)
                else:
                    kind = "service" if vt == D.HT else ("manual" if vd == "-" else "user")
                    nd = dict(kind=kind, lane=vt, text=viec, step=k, num=True)
            elif spec is None:
                raise ValueError(f"{q['code']} - {fl['ten']}: nút '{i}' chưa khai")
            else:
                kind, lane = spec[0], spec[1]
                text = spec[2] if len(spec) > 2 else ""
                step = spec[3] if len(spec) > 3 else None
                nd = dict(kind=kind, lane=lane, text=text, step=step, num=step is not None)
                if kind == "call" and step:
                    nd["text"] = text
            nd["id"] = i
            nodes[i] = nd
            return nd

        for c in fl["canh"]:
            ab, _, lb = c.partition(":")
            a, b = [x.strip() for x in ab.split(">")]
            node(a), node(b)
            edges.append((a, b, lb.strip()))
        out.append(dict(ten=fl["ten"], nodes=nodes, edges=edges))
    return out


def kiem_do_thi(q):
    """Lỗi cấu trúc: bước thiếu/trùng, cổng vừa gộp vừa rẽ, nút không tới được, ngõ cụt."""
    loi, seen = [], {}
    n = len(_steps(q))
    for fl in build_flows(q):
        N, E = fl["nodes"], fl["edges"]
        ins = {i: [a for a, b, _ in E if b == i] for i in N}
        outs = {i: [b for a, b, _ in E if a == i] for i in N}
        for i, nd in N.items():
            if nd["num"]:
                seen.setdefault(nd["step"], []).append(fl["ten"])
            k = nd["kind"]
            if k == "gw" and (len(ins[i]) != 1 or len(outs[i]) < 2):
                loi.append(f"{fl['ten']}: cổng rẽ '{nd['text']}' phải có 1 vào, >= 2 ra")
            if k == "join" and (len(ins[i]) < 2 or len(outs[i]) != 1):
                loi.append(f"{fl['ten']}: cổng gộp {i} phải có >= 2 vào, 1 ra")
            if k in ("start", "timer") and ins[i]:
                loi.append(f"{fl['ten']}: sự kiện bắt đầu {i} có cạnh vào")
            if k == "call":
                m_ = re.match(r"(QT\d\d|PD|DT) - ", nd["text"] or "")
                if not m_ or (m_.group(1) not in D.SO_DO):
                    loi.append(f"{fl['ten']}: ô gọi '{nd['text']}' không trỏ tới quy trình có thật")
            if k == "end" and outs[i]:
                loi.append(f"{fl['ten']}: kết thúc {i} có cạnh ra")
            if k not in ("end",) and not outs[i]:
                loi.append(f"{fl['ten']}: nút {i} ({nd['text'][:30]}) là ngõ cụt")
        starts = [i for i, nd in N.items() if nd["kind"] in ("start", "timer")]
        if not starts:
            loi.append(f"{fl['ten']}: không có sự kiện bắt đầu")
        reach, st = set(), list(starts)
        while st:
            x = st.pop()
            if x not in reach:
                reach.add(x)
                st += outs[x]
        for i in N:
            if i not in reach:
                loi.append(f"{fl['ten']}: nút {i} không tới được từ sự kiện bắt đầu")
    for k in range(1, n + 1):
        if len(seen.get(k, [])) != 1:
            loi.append(f"bước {k} xuất hiện {len(seen.get(k, []))} lần trên sơ đồ")
    return [f"{q['code']}: {x}" for x in loi]


# ---------------------------------------------------------------- bố cục trên lưới + định tuyến mê cung (A*)
# Mọi đường chỉ chạy trên các vạch lưới cách nhau G px, nên hai đường song song luôn cách nhau >= G (2,5mm khi in ở tỉ lệ
# nhỏ nhất 0,78). Mỗi cạnh của một nút chỉ nhận một đường (không nhập chữ T). Đường chỉ được cắt đường khác vuông góc, ở
# điểm cả hai đang đi thẳng, cách đầu mũi tên >= 20px và cách đầu nguồn >= 10px. Nhãn nhánh đặt cố định cạnh lối ra của cổng
# và là vật cản. Kết quả cuối cùng được kiểm lại bằng bpmn_geometry_check.kiem trên chính SVG.
def label(nd):
    return (f'{nd["step"]}. ' if nd.get("num") else "") + nd["text"]


def wrap_px(t, maxw, size, bold=False):
    out, cur = [], ""
    for w in (t or "").split():
        thu = (cur + " " + w).strip()
        if cur and K.text_w(thu, size, bold) > maxw:
            out.append(cur)
            cur = w
        else:
            cur = thu
    if cur:
        out.append(cur)
    return out


def _task_lines(nd):
    return wrap_px(label(nd), BW - 14, F_TASK) or [""]


def size(nd):
    k = nd["kind"]
    if k in ("gw", "join"):
        return GW, GW
    if k in EVENTS:
        return EW, EW
    return BW, max(BH, (22 if k == "call" else 26) + LINE * len(_task_lines(nd)) + (8 if k == "call" else 0))


def _ev_lines(nd):
    return wrap_px(nd.get("text") or "", EV_LBL_W, F_LBL)


def _gw_lines(nd):
    return wrap_px(nd.get("text") or "", GW_LBL_W, F_LBL, True)


def _lbl_w(t):
    return K.text_w(t, F_LBL, True) + 2


def _order(fl):
    """Thứ tự duyệt, cạnh quay lui, cột (lớp dài nhất theo cạnh tiến)."""
    ck = ("_order", XEP_CHONG)
    if ck in fl:
        fl["_pair"] = fl[ck][3]
        return fl[ck][:3]
    N, E = fl["nodes"], fl["edges"]
    outs = {i: [b for a, b, _ in E if a == i] for i in N}
    starts = [i for i, nd in N.items() if nd["kind"] in ("start", "timer", "link_catch")]
    back, order, state = set(), [], {}

    def dfs(u):
        state[u] = 1
        order.append(u)
        for v in outs[u]:
            if state.get(v) == 1:
                back.add((u, v))
            elif v not in state:
                dfs(v)
        state[u] = 2

    for s in starts:
        if s not in state:
            dfs(s)
    for i in N:
        if i not in state:
            dfs(i)
    fwd = [(a, b) for a, b, _ in E if (a, b) not in back]
    # cặp xếp chồng: bước và việc ngoài phần mềm đi kèm bước đó (cùng làn, nối thẳng nhau) đứng chung một cột, trên - dưới
    ins = {i: [a for a, b, _ in E if b == i] for i in N}
    pair = set()
    for a, b in fwd:
        ka, kb = re.fullmatch(r"(\d+)(n?)", a), re.fullmatch(r"(\d+)(n?)", b)
        if (XEP_CHONG and ka and kb and ka.group(2) != kb.group(2) and N[a]["lane"] == N[b]["lane"]
                and len(outs[a]) == 1 and len(ins[b]) == 1 and not any(a in p_ or b in p_ for p_ in pair)):
            pair.add((a, b))
    col = {i: 0 for i in N}
    changed = True
    while changed:
        changed = False
        for a, b in fwd:
            d_ = 0 if (a, b) in pair else 1
            if col[b] < col[a] + d_:
                col[b] = col[a] + d_
                changed = True
            if (a, b) in pair and col[a] < col[b]:
                col[a] = col[b]
                changed = True
    fl["_pair"] = pair
    # kéo nút về sát nút sau nó (bớt đường dài): nút không phải bắt đầu, mọi cạnh ra đều tiến
    for i in reversed(order):
        nx = [col[b] for a, b in fwd if a == i]
        if nx and N[i]["kind"] in ("start", "timer") and min(nx) - 1 > col[i]:
            col[i] = min(nx) - 1
    fl[ck] = (order, back, col, pair)
    return fl[ck][:3]


def _ceil(v):
    return int(-(-v // G)) * G


def _wrap_title(title, h):
    for n in (1, 2):
        ls = wrap_px(title, h - 10, F_LBL, True)
        if len(ls) <= n:
            return ls
    return None


SIDES = {"r": (1, 0), "b": (0, 1), "l": (-1, 0), "t": (0, -1)}
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
J_OUT, K_IN = 10, 20     # điểm gấp đầu tiên cách viền nguồn >= J_OUT; đoạn thẳng cuối trước mũi tên >= K_IN
NOX_IN, NOX_O = 34, 14   # không đường nào cắt qua đoạn cuối trong NOX_IN px trước mũi tên; không giao cắt trong NOX_O px quanh nút
CLR, CLR_LBL = 11, 2     # khoảng hở giữa đường và nút không phải đầu mút / chữ
C_NEAR, C_PAR = 1, 1     # chi phí thêm mỗi bước khi đi sát nút (< 24px) hoặc đi kề song song một đường khác / vạch làn


class LoiBoCuc(Exception):
    pass


def _layout(fl, lo, hi, links, extra=None):
    """Bố cục một phần (các cột lo..hi của luồng) trên lưới. extra: nới thêm rãnh {("gap", c) | ("ch", làn, k): số rãnh}."""
    extra = extra or {}
    N0, E0 = fl["nodes"], fl["edges"]
    order0, back, col0 = _order(fl)
    N = {i: dict(nd) for i, nd in N0.items() if lo <= col0[i] <= hi}
    col = {i: col0[i] for i in N}
    sub = {}   # cạnh vắt sang phần khác -> nút nối
    for lk in links:
        N[lk["id"]] = dict(id=lk["id"], kind=lk["kind"], lane=lk["lane"], text=lk["text"], step=None, num=False)
        for k in lk["edges"]:
            sub[k] = lk["id"]
    E = []   # (a, b, nhãn)
    for k, (a, b, lb) in enumerate(E0):
        if a in N and b in N and a in N0 and b in N0:
            E.append((a, b, lb))
        elif k in sub and (a in N or b in N):
            E.append((a, sub[k], lb) if a in N else (sub[k], b, ""))
    E = list(dict.fromkeys(E))
    while True:   # cổng gộp chỉ còn một đường vào trong phần này (các nhánh khác nhập ở nút nối): bỏ cổng, nối thẳng
        j = next((i for i, nd in N.items() if nd["kind"] == "join" and sum(1 for a, b, _ in E if b == i) == 1
                  and not all(x not in N0 for e_ in E if i in e_[:2] for x in e_[:2] if x != i)), None)
        if j is None:
            break
        (a1, _j, lb1), = [x for x in E if x[1] == j]
        (_j, b1, _lb), = [x for x in E if x[0] == j]
        E = [(a1, b1, lb1) if x[1] == j else x for x in E if x[0] != j]
        del N[j]
        col.pop(j, None)
    for lk in links:  # cột của nút nối: sát ô nguồn / ô đích
        oth = [b if a == lk["id"] else a for a, b, _ in E if lk["id"] in (a, b)]
        col[lk["id"]] = (max(col[o] for o in oth) + 1) if lk["kind"] == "link_throw" else (min(col[o] for o in oth) - 1)
    used = sorted(set(col.values()))
    remap = {c: k for k, c in enumerate(used)}
    col = {i: remap[c] for i, c in col.items()}
    ncol = len(used)
    order = [i for i in order0 if i in N] + [lk["id"] for lk in links]
    lanes = []  # thứ tự làn theo cả luồng, giống nhau ở mọi phần
    for i in order0 + order:
        ln = (N0.get(i) or N[i])["lane"]
        if ln not in lanes and ln != D.HT:
            lanes.append(ln)
    lanes.append(D.HT)
    lanes = [ln for ln in lanes if any(nd["lane"] == ln for nd in N.values())]
    li = {ln: k for k, ln in enumerate(lanes)}
    # hàng trong làn: theo hàng của ô trước cùng làn, trùng thì xuống hàng dưới
    pair = {(a, b) for a, b in fl["_pair"] if a in N and b in N}
    duoi = {a: b for a, b in pair}
    row, taken, base = {}, set(), {}
    real = sorted([i for i in order if i in N0], key=lambda i: (col[i], order.index(i)))
    moc = {}   # làn -> (hàng, cột) của nút nối đặt gần nhất: nút nối cùng làn xếp theo chữ cái từ trên xuống, cùng hàng thì trái sang phải
    for i in real + [lk["id"] for lk in sorted(links, key=lambda lk: lk["text"])]:
        if i in row:
            continue
        ln = N[i]["lane"]
        if i in N0:
            pr = [a for a, b, _ in E if b == i and a in row and N[a]["lane"] == ln and col[a] < col[i]]
            want = base[max(pr, key=lambda a: col[a])] if pr else 0
        else:
            oth = [b if a == i else a for a, b, _ in E if i in (a, b)]
            same = [o for o in oth if N[o]["lane"] == ln and o in row]
            want = row[same[0]] if same else 0
        r = want
        if i in N0:
            while (ln, col[i], r) in taken or (i in duoi and (ln, col[i], r + 1) in taken):
                r += 1
        else:  # nút nối: hàng trống gần nhất, dưới rồi trên (hàng âm được chuẩn hoá sau), không đứng trước nút nối có chữ cái nhỏ hơn
            def duoc(r_):
                if (ln, col[i], r_) in taken:
                    return False
                return ln not in moc or r_ > moc[ln][0] or (r_ == moc[ln][0] and col[i] > moc[ln][1])
            r = next(want + d_ for n_ in range(40) for d_ in ((n_, -n_) if n_ else (0,)) if duoc(want + d_))
            moc[ln] = (r, col[i])
        row[i] = base[i] = r
        taken.add((ln, col[i], r))
        if i in duoi:
            row[duoi[i]], base[duoi[i]] = r + 1, r
            taken.add((ln, col[i], r + 1))
    # nút có 3 nhánh toả ra (hoặc 3 đường gộp vào) cùng làn: đưa về hàng giữa để nhánh ra trên - phải - dưới, không vòng
    def dich(g, nb, lui):
        rs = sorted(row[t] for t in nb)
        if len(nb) != 3 or len(set(rs)) != 3 or row[g] == rs[1]:
            return
        U, st = {g}, [g]
        while st:
            u = st.pop()
            for a, b, _ in E:
                v = a if lui else b
                if (b if lui else a) == u and v not in U and v not in nb and N[v]["lane"] == N[g]["lane"] and row[v] == row[g] \
                        and (col[v] < col[u] if lui else col[v] > col[u]):
                    U.add(v)
                    st.append(v)
        if any(u in base and (u in duoi or base[u] != row[u]) for u in U):
            return
        cells = {(N[u]["lane"], col[u], rs[1]) for u in U}
        if cells & (taken - {(N[u]["lane"], col[u], row[u]) for u in U}):
            return
        for u in U:
            taken.discard((N[u]["lane"], col[u], row[u]))
            row[u] = base[u] = rs[1]
        taken.update(cells)

    for ln in lanes:
        m_ = min(row[i] for i in N if N[i]["lane"] == ln)
        if m_:
            taken = {(l_, c_, r_ - (m_ if l_ == ln else 0)) for l_, c_, r_ in taken}
            for i in N:
                if N[i]["lane"] == ln:
                    row[i] -= m_
                    base[i] = base.get(i, 0) - m_
    for g in [i for i in real if N[i]["kind"] == "gw"]:
        dich(g, [b for a, b, _ in E if a == g and N[b]["lane"] == N[g]["lane"] and col[b] > col[g]], True)
    for g in [i for i in real if N[i]["kind"] == "join"]:
        dich(g, [a for a, b, _ in E if b == g and N[a]["lane"] == N[g]["lane"] and col[a] < col[g]], False)
    key = {i: (li[N[i]["lane"]], row[i]) for i in N}
    # ---- cổng: mỗi đường một cạnh của nút
    port, busy = {}, {i: set() for i in N}   # port[(k, 's'|'t')] = cạnh

    def is_back(a, b):
        return col[b] <= col[a] and (a, b) not in pair

    def take(i, prefs, what):
        for s in prefs:
            if s not in busy[i]:
                busy[i].add(s)
                return s
        raise LoiBoCuc(f"nút {i} ({N[i]['text'][:25]}) không còn cạnh trống cho {what}")

    outs = {}
    for k, (a, b, lb) in enumerate(E):
        if (a, b) in pair:
            port[(k, "s")], port[(k, "t")] = take(a, "b", "cặp"), take(b, "t", "cặp")
        else:
            outs.setdefault(a, []).append(k)
    for a, ks in outs.items():
        if N[a]["kind"] == "gw" or len(ks) > 1:
            fw = [k for k in ks if not is_back(a, E[k][1])]
            if len(ks) == 3 and len(fw) == 3 and (all(key[E[k][1]] > key[a] for k in ks) or all(key[E[k][1]] < key[a] for k in ks)):
                for k, sd in zip(sorted(ks, key=lambda k: (key[E[k][1]], col[E[k][1]])), "trb"):
                    port[(k, "s")] = take(a, sd, "nhánh ra")
                continue
            same = [k for k in fw if key[E[k][1]] == key[a]] or [k for k in fw if N[E[k][1]]["lane"] == N[a]["lane"]] or fw
            main = min(same, key=lambda k: (col[E[k][1]], row[E[k][1]])) if same else None
            if main is not None:
                port[(main, "s")] = take(a, "r", "nhánh chính")
            for k in ks:
                if k == main:
                    continue
                b = E[k][1]
                up = key[b] < key[a] or (key[b] == key[a] and is_back(a, b))
                port[(k, "s")] = take(a, "tb" if up else "bt", "nhánh ra")
        else:
            k = ks[0]
            b = E[k][1]
            if is_back(a, b):
                port[(k, "s")] = take(a, "tb" if key[b] <= key[a] else "bt", "đường quay lui")
            else:
                port[(k, "s")] = take(a, "r", "đường ra")
    ins = {}
    for k, (a, b, lb) in enumerate(E):
        if (a, b) not in pair:
            ins.setdefault(b, []).append(k)
    for b, ks in ins.items():
        fw = sorted([k for k in ks if not is_back(E[k][0], b)],
                    key=lambda k: (key[E[k][0]] != key[b], port[(k, "s")] != "r", abs(key[E[k][0]][0] - key[b][0]), abs(row[E[k][0]] - row[b]), -col[E[k][0]]))
        ev = N[b]["kind"] in EVENTS
        for n_, k in enumerate(fw):
            a = E[k][0]
            if n_ == 0:
                port[(k, "t")] = take(b, "ltb", "đường vào")
            elif key[a] < key[b]:
                port[(k, "t")] = take(b, "tbl", "đường vào")
            else:
                port[(k, "t")] = take(b, "tbl" if ev else "btl", "đường vào")
        for k in ks:
            if k in fw:
                continue
            a = E[k][0]
            if key[a] == key[b]:
                pr = port[(k, "s")] + ("b" if port[(k, "s")] == "t" else "t")
            else:
                pr = "bt" if key[a] > key[b] else "tb"
            port[(k, "t")] = take(b, pr + "l", "đường quay lui vào")
    # ---- kích thước, nhãn, phần lấn của từng nút
    geo = {}
    for i, nd in N.items():
        w, h = size(nd)
        g = dict(w=w, h=h, top=h / 2, bot=h / 2, left=w / 2, right=w / 2, lbl=None)
        vao = {port[(k, "t")] for k, (a, b, lb) in enumerate(E) if b == i}
        if "t" in busy[i]:
            g["top"] += 2 * G if "t" in vao else G
        if "b" in busy[i]:
            g["bot"] += 2 * G if "b" in vao else G
        if nd["kind"] in EVENTS and nd.get("text"):
            ls = _ev_lines(nd)
            lw = max(K.text_w(t, F_LBL) for t in ls)
            tren = "b" in busy[i]
            if tren and "t" in busy[i]:
                raise LoiBoCuc(f"sự kiện {i} có đường ở cả cạnh trên và dưới, không còn chỗ đặt nhãn")
            g["lbl"] = ("tren" if tren else "duoi", ls, lw)
            if tren:
                g["top"] = h / 2 + len(ls) * LBL_H + 6
            else:
                g["bot"] = h / 2 + len(ls) * LBL_H + 6
            g["left"] = max(g["left"], lw / 2 + 2)
            g["right"] = max(g["right"], lw / 2 + 2)
        if nd["kind"] == "gw" and nd.get("text"):
            ls = _gw_lines(nd)
            lw = max(K.text_w(t, F_LBL, True) for t in ls)
            lech = "t" in busy[i]
            g["lbl"] = ("trai" if lech else "giua", ls, lw)
            g["top"] = max(g["top"], h / 2 + len(ls) * LBL_H + 6)
            if lech:
                g["left"] = max(g["left"], lw + 10)
            else:
                g["left"] = max(g["left"], lw / 2 + 2)
                g["right"] = max(g["right"], lw / 2 + 2)
        geo[i] = g
    stub = {}  # độ dài đoạn thẳng bắt buộc ở đầu nguồn (để đặt nhãn nhánh)
    for k, (a, b, lb) in enumerate(E):
        s = port[(k, "s")]
        if lb:
            lw = _lbl_w(lb)
            if s == "r":
                stub[k] = lw + 8
                geo[a]["right"] = max(geo[a]["right"], geo[a]["w"] / 2 + lw + 8 - J_OUT)
            else:
                stub[k] = 22
                geo[a]["right"] = max(geo[a]["right"], lw + 10)
                geo[a]["top" if s == "t" else "bot"] = max(geo[a]["top" if s == "t" else "bot"], geo[a]["h"] / 2 + 22 - 8)
    # ---- cột
    Lc = [max(geo[i]["left"] for i in N if col[i] == c) for c in range(ncol)]
    Rc = [max(geo[i]["right"] for i in N if col[i] == c) for c in range(ncol)]
    direct = set()
    for k, (a, b, lb) in enumerate(E):
        if (port[(k, "s")] == "r" and port[(k, "t")] == "l" and col[b] == col[a] + 1 and key[a] == key[b]) or (a, b) in pair:
            direct.add(k)
    Tg = []
    for c in range(ncol - 1):
        n = 0
        for k, (a, b, lb) in enumerate(E):
            if k in direct:
                continue
            if (port[(k, "s")] == "r" and col[a] == c) or (port[(k, "t")] == "l" and col[b] == c + 1):
                n += 1
        Tg.append(max(1, min(4, n)) + extra.get(("gap", c), 0))
    hdr = X0 + POOL_W + LANE_W
    cx = [hdr + _ceil(Lc[0] + 14 + G * extra.get(("gap", -1), 0))]
    for c in range(ncol - 1):
        cx.append(cx[-1] + _ceil(Rc[c] + J_OUT) + G * (Tg[c] - 1) + _ceil(Lc[c + 1] + NOX_IN))
    pool_r = cx[-1] + _ceil(Rc[-1] + 14 + G * extra.get(("gap", ncol - 1), 0))
    # ---- làn, hàng
    nrow = {ln: max(row[i] for i in N if N[i]["lane"] == ln) + 1 for ln in lanes}
    ly, cy, tracks = [TOP], {}, {}
    for ln in lanes:
        y = ly[-1]
        y0 = y
        for r in range(nrow[ln] + 1):
            cnt = sum(1 for k, (a, b, lb) in enumerate(E)
                      if (r < nrow[ln] and ((N[a]["lane"] == ln and row[a] == r and port[(k, "s")] == "t") or (N[b]["lane"] == ln and row[b] == r and port[(k, "t")] == "t")))
                      or (r > 0 and ((N[a]["lane"] == ln and row[a] == r - 1 and port[(k, "s")] == "b") or (N[b]["lane"] == ln and row[b] == r - 1 and port[(k, "t")] == "b"))))
            T = max(1 if 0 < r < nrow[ln] else 0, min(3, cnt)) + extra.get(("ch", ln, r), 0)   # rãnh sát vạch làn: chỉ mở khi có đường cần
            if r == nrow[ln]:
                y = y + G * (T + 1 + (1 if T else 0))
                break
            ids = [i for i in N if N[i]["lane"] == ln and row[i] == r]
            te = max([geo[i]["top"] for i in ids] + [BH / 2])
            be = max([geo[i]["bot"] for i in ids] + [BH / 2])
            yc = _ceil(y + G * (T + (1 if T and r == 0 else 0)) + CLR + 1 + te)
            for i in ids:
                cy[i] = yc
            y = _ceil(yc + be + CLR + 1) - G
        nl = len(wrap_px(ln, LANE_W - 10, F_TASK, True))
        y = max(y, y0 + _ceil(nl * 15 + 14))
        ly.append(y)
    pos = {i: (cx[col[i]] - geo[i]["w"] / 2, cy[i] - geo[i]["h"] / 2, geo[i]["w"], geo[i]["h"]) for i in N}
    # ---- hộp chữ (nhãn sự kiện, nhãn cổng, nhãn nhánh): (x, y, w, h, [(chữ, x, y nền)], loại)
    lbls = []
    for i, nd in N.items():
        g = geo[i]
        x, y, w, h = pos[i]
        if g["lbl"] and nd["kind"] in EVENTS:
            where, ls, lw = g["lbl"]
            y0 = y + h + 4 if where == "duoi" else y - 4 - len(ls) * LBL_H
            lbls.append(dict(kind="ev", node=i, bb=(cx[col[i]] - lw / 2, y0, lw, len(ls) * LBL_H),
                             lines=[(t, cx[col[i]], y0 + 11 + j * LBL_H) for j, t in enumerate(ls)], anchor="middle"))
        elif g["lbl"]:
            where, ls, lw = g["lbl"]
            y0 = y - 4 - len(ls) * LBL_H
            if where == "giua":
                lbls.append(dict(kind="gw", bb=(cx[col[i]] - lw / 2, y0, lw, len(ls) * LBL_H),
                                 lines=[(t, cx[col[i]], y0 + 11 + j * LBL_H) for j, t in enumerate(ls)], anchor="middle"))
            else:
                lbls.append(dict(kind="gw", bb=(cx[col[i]] - 8 - lw, y0, lw, len(ls) * LBL_H),
                                 lines=[(t, cx[col[i]] - 8, y0 + 11 + j * LBL_H) for j, t in enumerate(ls)], anchor="end"))
    for k, (a, b, lb) in enumerate(E):
        if not lb:
            continue
        x, y, w, h = pos[a]
        lw = _lbl_w(lb)
        s = port[(k, "s")]
        if s == "r":
            bb = (x + w + 4, cy[a] - 17, lw, 13)
        elif s == "b":
            bb = (cx[col[a]] + 6, y + h + 5, lw, 13)
        else:
            bb = (cx[col[a]] + 6, y - 18, lw, 13)
        lbls.append(dict(kind="canh", bb=bb, lines=[(lb, bb[0] + 1, bb[1] + 10.5)], anchor="start"))
    return dict(N=N, E=E, col=col, ncol=ncol, row=row, lanes=lanes, ly=ly, cx=cx, cy=cy, pos=pos, geo=geo, port=port, stub=stub,
                lbls=lbls, hdr=hdr, pool_r=pool_r, W=pool_r + 3, H=ly[-1] + 3, direct=direct, key=key)


def _ray(L, i, side, dmin):
    """Điểm bám trên viền nút i ở cạnh side, và điểm lưới đầu tiên trên tia đi ra cách viền >= dmin."""
    x, y, w, h = L["pos"][i]
    cxx, cyy = x + w / 2, y + h / 2
    dx, dy = SIDES[side]
    bx, by = cxx + dx * w / 2, cyy + dy * h / 2
    half = w / 2 if dx else h / 2
    n = int(-(-(half + dmin) // G))
    return (bx, by), (int(round(cxx / G)) + dx * n, int(round(cyy / G)) + dy * n), n


def _route(L, seq):
    """Định tuyến mọi cạnh theo thứ tự seq. Trả (đường {k: pts}, cạnh hỏng [k], chi phí)."""
    import heapq
    N, E, pos = L["N"], L["E"], L["pos"]
    blocked, res = set(), {}
    for i, (x, y, w, h) in pos.items():
        for ix in range(int((x - CLR) // G), int((x + w + CLR) // G) + 2):
            for iy in range(int((y - CLR) // G), int((y + h + CLR) // G) + 2):
                if x - CLR < ix * G < x + w + CLR and y - CLR < iy * G < y + h + CLR:
                    blocked.add((ix, iy))
    for lb in L["lbls"]:
        x, y, w, h = lb["bb"]
        m_ = CLR_LBL if lb["kind"] == "canh" else 7
        for ix in range(int((x - m_) // G), int((x + w + m_) // G) + 2):
            for iy in range(int((y - m_) // G), int((y + h + m_) // G) + 2):
                if x - m_ < ix * G < x + w + m_ and y - m_ < iy * G < y + h + m_:
                    blocked.add((ix, iy))
    nocross, near = set(), set()
    for i, (x, y, w, h) in pos.items():
        for ix in range(int((x - 24) // G), int((x + w + 24) // G) + 2):
            for iy in range(int((y - 24) // G), int((y + h + 24) // G) + 2):
                if x - 24 < ix * G < x + w + 24 and y - 24 < iy * G < y + h + 24:
                    near.add((ix, iy))
                    if x - NOX_O < ix * G < x + w + NOX_O and y - NOX_O < iy * G < y + h + NOX_O:
                        nocross.add((ix, iy))
    for lb in L["lbls"]:
        if lb["kind"] == "canh":
            x, y, w, h = lb["bb"]
            for ix in range(int((x - 21) // G), int((x + w + 21) // G) + 2):
                for iy in range(int((y - 21) // G), int((y + h + 21) // G) + 2):
                    if x - 21 < ix * G < x + w + 21 and y - 21 < iy * G < y + h + 21:
                        nocross.add((ix, iy))
    ix0, ix1 = L["hdr"] // G + 1, L["pool_r"] // G - 1
    iy0, iy1 = L["ly"][0] // G + 1, L["ly"][-1] // G - 1
    occ = {}
    for y in L["ly"]:   # vạch lưới kề vạch làn / viền bể: chỉ được cắt ngang qua, không chạy dọc theo, không gấp
        for ix in range(ix0, ix1 + 1):
            for dy in (-1, 1):
                occ[(ix, y // G + dy)] = "H"
    for iy in range(iy0, iy1 + 1):
        occ[(ix0, iy)] = occ[(ix1, iy)] = "V"
    for y in L["ly"][1:-1]:
        for ix in range(ix0, ix1 + 1):
            occ[(ix, y // G)] = "L"
    ends, nox_in = {}, {}
    for k, (a, b, lb) in enumerate(E):
        ps, pt = L["port"][(k, "s")], L["port"][(k, "t")]
        B1, S, n1 = _ray(L, a, ps, L["stub"].get(k, J_OUT))
        B2, T, n2 = _ray(L, b, pt, K_IN)
        n2x = _ray(L, b, pt, NOX_IN)[2]
        ds = "rblt".index(ps)
        dt = ("rblt".index(pt) + 2) % 4
        ends[k] = (B1, S, ds, B2, T, dt)
        c1 = (int(round((pos[a][0] + pos[a][2] / 2) / G)), int(round((pos[a][1] + pos[a][3] / 2) / G)))
        c2 = (int(round((pos[b][0] + pos[b][2] / 2) / G)), int(round((pos[b][1] + pos[b][3] / 2) / G)))
        for n in range(1, n1):
            res[(c1[0] + DIRS[ds][0] * n, c1[1] + DIRS[ds][1] * n)] = k
        for n in range(1, n2):
            res[(c2[0] - DIRS[dt][0] * n, c2[1] - DIRS[dt][1] * n)] = k
        for n in range(n2, n2x):   # đoạn thẳng cuối trước mũi tên: đường của chính nó đi được, đường khác không cắt qua
            nox_in.setdefault((c2[0] - DIRS[dt][0] * n, c2[1] - DIRS[dt][1] * n), k)

    def ok(q, d, k):
        if not (ix0 <= q[0] <= ix1 and iy0 <= q[1] <= iy1):
            return False
        r = res.get(q)
        if r is not None:
            return r == k
        if q in blocked or nox_in.get(q, k) != k:
            return False
        o = occ.get(q)
        if o is None:
            return True
        if o in "hv" and q in nocross:
            return False
        if o in "hHL":
            return d in (1, 3)
        if o in "vV":
            return d in (0, 2)
        return False

    def them(q, d):
        c = C_NEAR if q in near else 0
        px_, py_ = DIRS[(d + 1) % 4]
        for sgn in (1, -1):
            o = occ.get((q[0] + sgn * px_, q[1] + sgn * py_))
            if o and ((d in (0, 2) and o in "hHL") or (d in (1, 3) and o in "vV")):
                c += C_PAR
        return c

    routes, fail, cost, ncross = {}, [], 0, 0
    for k in seq:
        B1, S, ds, B2, T, dt = ends[k]
        path = None
        if ok(S, ds, k) and (res.get(T) in (None, k)):
            if S == T and ds == dt:
                path = [S]
            else:
                # trạng thái: (điểm, hướng, số bước từ chỗ gấp gần nhất, số bước từ chỗ giao cắt gần nhất), hai số đếm chặn ở 3
                st0 = (S, ds, 3, 3)
                hq = [(abs(S[0] - T[0]) + abs(S[1] - T[1]), 0, st0)]
                best = {st0: 0}
                prev = {}
                while hq:
                    f, gc, st = heapq.heappop(hq)
                    if gc > best.get(st, 1e9):
                        continue
                    p, d, sb, sc = st
                    if p == T and d == dt:
                        path = []
                        while st in prev:
                            if not path or path[-1] != st[0]:
                                path.append(st[0])
                            st = prev[st]
                        if not path or path[-1] != S:
                            path.append(S)
                        path.reverse()
                        cost += gc
                        break
                    q = (p[0] + DIRS[d][0], p[1] + DIRS[d][1])
                    if ok(q, d, k):
                        cat = occ.get(q) in ("h", "v")
                        if not cat or sb >= 2:   # giao cắt phải cách chỗ gấp của chính nó >= 3 bước lưới
                            nc = gc + 1 + (C_CROSS if cat else 0) + them(q, d)
                            ns = (q, d, min(3, sb + 1), 0 if cat else min(3, sc + 1))
                            if nc < best.get(ns, 1e9):
                                best[ns] = nc
                                prev[ns] = st
                                heapq.heappush(hq, (nc + abs(q[0] - T[0]) + abs(q[1] - T[1]), nc, ns))
                    if occ.get(p) is None and sc >= 3:
                        for nd in ((d + 1) % 4, (d + 3) % 4):
                            nc = gc + C_BEND
                            ns = (p, nd, 0, sc)
                            if nc < best.get(ns, 1e9):
                                best[ns] = nc
                                prev[ns] = st
                                heapq.heappush(hq, (nc + abs(p[0] - T[0]) + abs(p[1] - T[1]), nc, ns))
        if path is None:
            fail.append(k)
            continue
        # đánh dấu chiếm chỗ
        for j, p in enumerate(path):
            din = ds if j == 0 else next(n for n, dd in enumerate(DIRS) if dd == (p[0] - path[j - 1][0], p[1] - path[j - 1][1]))
            dout = dt if j == len(path) - 1 else next(n for n, dd in enumerate(DIRS) if dd == (path[j + 1][0] - p[0], path[j + 1][1] - p[1]))
            o = occ.get(p)
            if o == "L":
                continue
            ncross += 1 if o in ("h", "v") else 0
            occ[p] = "x" if (din != dout or o in ("h", "v")) else ("h" if din in (0, 2) else "v")
            if din != dout:   # chỗ gấp: 3 điểm lưới kế tiếp trên phần kéo dài của hai đoạn không cho đường khác đi thẳng hàng nối vào
                for dd, ch in ((DIRS[din], "H" if din in (0, 2) else "V"), ((-DIRS[dout][0], -DIRS[dout][1]), "H" if dout in (0, 2) else "V")):
                    for n_ in (1, 2, 3):
                        q_ = (p[0] + dd[0] * n_, p[1] + dd[1] * n_)
                        if q_ in res or q_ in blocked:
                            break
                        if occ.get(q_) is None:
                            occ[q_] = ch
                for t_ in (1, 2):   # 2 điểm lưới hai bên chỗ gấp: đường khác không được cắt qua
                    for jj in (j - t_, j + t_):
                        if 0 <= jj < len(path) and occ.get(path[jj]) in ("h", "v"):
                            occ[path[jj]] = "x"
        pts = [B1] + [(p[0] * G, p[1] * G) for p in path] + [B2]
        simp = [pts[0]]
        for j in range(1, len(pts) - 1):
            a_, b_, c_ = simp[-1], pts[j], pts[j + 1]
            if (abs(a_[0] - b_[0]) < .01 and abs(b_[0] - c_[0]) < .01) or (abs(a_[1] - b_[1]) < .01 and abs(b_[1] - c_[1]) < .01):
                continue
            simp.append(b_)
        simp.append(pts[-1])
        routes[k] = [p for j, p in enumerate(simp) if j == 0 or p != simp[j - 1]]
    return routes, fail, cost, ncross


def _orders(L):
    import random
    E = L["E"]

    def span(k):
        a, b = E[k][0], E[k][1]
        return abs(L["cx"][L["col"][a]] - L["cx"][L["col"][b]]) + abs(L["cy"][a] - L["cy"][b])
    ks = list(range(len(E)))
    d = [k for k in ks if k in L["direct"]]
    o = [k for k in ks if k not in L["direct"]]
    yield d + sorted(o, key=span)
    yield d + sorted(o, key=lambda k: -span(k))
    yield d + sorted(o, key=lambda k: (L["col"][E[k][0]], span(k)))
    rnd = random.Random(7)
    for _ in range(N_ORDER):
        o2 = o[:]
        rnd.shuffle(o2)
        yield d + o2


def _solve(fl, lo, hi, links):
    """Bố cục + định tuyến, tự nới rãnh quanh cạnh chưa đi được. Trả (bố cục, đường, lỗi)."""
    extra = {}
    best = None
    for _round in range(7):
        L = _layout(fl, lo, hi, links, extra)
        cand = None
        for n_, seq in enumerate(_orders(L)):
            routes, fail, cost, cross = _route(L, seq)
            bends = sum(len(p) - 2 for p in routes.values())
            sc = (len(fail), cost + 2 * bends)
            if cand is None or sc < cand[0]:
                cand = (sc, routes, fail)
            if not fail and cross == 0 and n_ >= 2:
                break
        if best is None or cand[0][0] < best[1][0][0]:
            best = (L, cand)
        if not cand[2]:
            break
        for k in cand[2]:
            a, b = L["E"][k][0], L["E"][k][1]
            for i in (a, b):
                ln, r, c = L["N"][i]["lane"], L["row"][i], L["col"][i]
                extra[("ch", ln, r)] = extra.get(("ch", ln, r), 0) + 1
                extra[("ch", ln, r + 1)] = extra.get(("ch", ln, r + 1), 0) + 1
                extra[("gap", c - 1)] = extra.get(("gap", c - 1), 0) + 1
                extra[("gap", c)] = extra.get(("gap", c), 0) + 1
    L, (sc, routes, fail) = best
    loi = [f"ROUTE không tìm được đường cho {L['E'][k][0]}->{L['E'][k][1]}" for k in fail]
    return L, routes, loi


def _draw(q, fl, L, routes, pno, ptotal):
    N, E, pos, ly, lanes = L["N"], L["E"], L["pos"], L["ly"], L["lanes"]
    W, H, hdr, pool_r = L["W"], L["H"], L["hdr"], L["pool_r"]
    o = [f'<svg class="bpmn" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="Roboto, Arial, sans-serif" role="img" aria-label="Sơ đồ {e(q["code"])} {e(fl["ten"])} phần {pno}">',
         '<defs><marker id="a" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
         '<path d="M0,0L10,5L0,10z" fill="#333"/></marker></defs>',
         f'<rect x="{X0}" y="{TOP}" width="{pool_r - X0}" height="{ly[-1] - TOP}" fill="#fff" stroke="#333" stroke-width="1.2"/>',
         f'<line x1="{X0 + POOL_W}" y1="{TOP}" x2="{X0 + POOL_W}" y2="{ly[-1]}" stroke="#333"/>']
    ph = f" ({pno}/{ptotal})" if ptotal > 1 else ""
    tl = _wrap_title(f'[{q["code"]}] {fl["ten"]}{ph}', ly[-1] - TOP) or _wrap_title(f'[{q["code"]}]{ph}', ly[-1] - TOP) or [q["code"]]
    ty = (TOP + ly[-1]) / 2
    for j, t in enumerate(tl):
        o.append(f'<text transform="translate({X0 + POOL_W / 2 + (j - (len(tl) - 1) / 2) * 13 + 4},{ty}) rotate(-90)" text-anchor="middle" '
                 f'font-size="{F_LBL}" font-weight="700" fill="#21272B">{e(t)}</text>')
    for k_, ln in enumerate(lanes):
        y = ly[k_]
        if k_:
            o.append(f'<line x1="{X0 + POOL_W}" y1="{y}" x2="{pool_r}" y2="{y}" stroke="#333"/>')
        o.append(f'<line x1="{hdr}" y1="{y}" x2="{hdr}" y2="{ly[k_ + 1]}" stroke="#333"/>')
        ll = wrap_px(ln, LANE_W - 10, F_TASK, True)
        for j, t in enumerate(ll):
            o.append(f'<text x="{X0 + POOL_W + LANE_W / 2}" y="{(y + ly[k_ + 1]) / 2 + (j - (len(ll) - 1) / 2) * 15 + 4}" text-anchor="middle" '
                     f'font-size="{F_TASK}" font-weight="700" fill="#21272B">{e(t)}</text>')
    for k in sorted(routes):
        d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in routes[k])
        o.append(f'<path d="{d}" fill="none" stroke="#333" stroke-width="1.3" marker-end="url(#a)"/>')
    for i, nd in N.items():
        x, y, w, h = pos[i]
        k = nd["kind"]
        if k in ("user", "service", "manual", "call"):
            f, c = COL[k]
            sw = CALL_W if k == "call" else 1.3
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{f}" stroke="{c}" stroke-width="{sw}"/>')
            lines = _task_lines(nd)
            if k == "call":
                o.append(_plus(x + w / 2, y + h, c))
                ty0 = y + (h - 12) / 2 - (len(lines) - 1) * LINE / 2 + 4.5
            else:
                o.append(icon(k, x + 4, y + 3))
                ty0 = y + 14 + (h - 16) / 2 - (len(lines) - 1) * LINE / 2 + 4.5
            for j, t in enumerate(lines):
                o.append(f'<text x="{x + w / 2}" y="{ty0 + j * LINE}" text-anchor="middle" font-size="{F_TASK}" fill="#282F33">{e(t)}</text>')
        elif k in ("gw", "join"):
            cx_, cy_ = x + w / 2, y + h / 2
            o.append(f'<path d="M{cx_},{y}L{x + w},{cy_}L{cx_},{y + h}L{x},{cy_}Z" fill="#fff" stroke="#333" stroke-width="1.3"/>')
            o.append(f'<path d="M{cx_ - 7},{cy_ - 7}L{cx_ + 7},{cy_ + 7}M{cx_ + 7},{cy_ - 7}L{cx_ - 7},{cy_ + 7}" stroke="#333" stroke-width="2.4"/>')
        else:
            o.append(_event(k, x + w / 2, y + h / 2, w / 2))
    for lb in L["lbls"]:
        for t, x, y in lb["lines"]:
            if lb["kind"] == "ev":
                o.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="{F_LBL}" fill="#21272B">{e(t)}</text>')
            elif lb["kind"] == "gw":
                o.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{lb["anchor"]}" font-size="{F_LBL}" font-weight="600" fill="#21272B">{e(t)}</text>')
            else:
                o.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{F_LBL}" font-style="italic" font-weight="600" fill="{LABEL_COL}">{e(t)}</text>')
    o.append("</svg>")
    syms = {"lane", "arrow"} | {nd["kind"] for nd in N.values()}
    if any(lb for a, b, lb in E):
        syms.add("label")
    if any(nd.get("num") for nd in N.values()):
        syms.add("num")
    if any(nd["kind"] == "manual" and not nd.get("num") for nd in N.values()):
        syms.add("nonum")
    if "join" in syms:
        syms.add("gw")
    return "".join(o), syms


def _links_for(fl, parts, lo, hi, letters=None):
    """Nút nối của phần [lo, hi]: mỗi ô đích ở phần khác một nút bắt (nhiều nút ném cùng chữ được phép).
    Nút ném đặt ở làn của ô đích (làn sẽ làm tiếp), nên thứ tự làn của các nút nối giống nhau ở mọi phần."""
    order, back, col = _order(fl)
    N = fl["nodes"]

    def part_of(i):
        return next((k for k, (a, b) in enumerate(parts) if a <= col[i] <= b), None) if parts else None
    out = {}
    for k, (a, b, lb) in enumerate(fl["edges"]):
        ia, ib = lo <= col[a] <= hi, lo <= col[b] <= hi
        if ia == ib:
            continue
        ch = (letters or {}).get(b, "?")
        pa, pb = part_of(a), part_of(b)
        if ia:
            lid = f"_t{k}"
            out[lid] = dict(id=lid, kind="link_throw", lane=N[b]["lane"], text=f"{ch}: sang phần {(pb + 1) if pb is not None else 9}", edges=[k])
        else:
            lid = f"_c{b}"
            if lid not in out:
                out[lid] = dict(id=lid, kind="link_catch", lane=N[b]["lane"], text="", edges=[], src=set())
            out[lid]["edges"].append(k)
            out[lid]["src"].add((pa + 1) if pa is not None else 9)
            out[lid]["text"] = f"{ch}: từ phần {', '.join(str(x) for x in sorted(out[lid]['src']))}"
    return list(out.values())


def _split(fl, max_w):
    """Chia các cột thành ít phần nhất (mỗi phần <= max_w theo bố cục thật); cùng số phần thì ít phần dưới 3 ô việc nhất, rồi ít đường quay lui vắt qua chỗ cắt
    nhất, rồi ít đường vắt qua nhất, rồi các phần rộng đều nhau. Không phần nào chỉ có cổng hoặc kết thúc."""
    order, back, col = _order(fl)
    mx = max(col.values())
    if _layout(fl, 0, mx, [])["W"] <= max_w:
        return [(0, mx)]
    E = fl["edges"]
    nb = [sum(1 for a, b, _ in E if (a, b) in back and min(col[a], col[b]) <= c < max(col[a], col[b])) for c in range(mx + 1)]
    nf = [sum(1 for a, b, _ in E if (a, b) not in back and min(col[a], col[b]) <= c < max(col[a], col[b])) for c in range(mx + 1)]
    kinds = {c: {fl["nodes"][i]["kind"] for i in fl["nodes"] if col[i] == c} for c in range(mx + 1)}
    wid = {}

    def width(lo, hi):
        if (lo, hi) not in wid:
            try:
                wid[(lo, hi)] = _layout(fl, lo, hi, _links_for(fl, None, lo, hi))["W"]
            except LoiBoCuc:
                wid[(lo, hi)] = 10 ** 6
        return wid[(lo, hi)]
    viec = [sum(1 for i in fl["nodes"] if col[i] == c and fl["nodes"][i]["kind"] in ("user", "service", "manual", "call")) for c in range(mx + 1)]
    best = {-1: (0, 0, 0, 0, 0, [])}
    for hi in range(mx + 1):
        for lo in range(hi, -1, -1):
            if lo - 1 not in best:
                continue
            w = width(lo, hi)
            if w > max_w and lo != hi:
                if w < 10 ** 6:
                    break
                continue
            if set().union(*(kinds[c] for c in range(lo, hi + 1))) <= {"join", "gw", "end"}:
                continue
            n, it, cb, cf, sq, parts = best[lo - 1]
            cand = (n + 1, it + (1 if sum(viec[lo:hi + 1]) < 3 else 0), cb + (nb[hi] if hi < mx else 0), cf + (nf[hi] if hi < mx else 0),
                    sq + w * w, parts + [(lo, hi)])
            if hi not in best or cand[:5] < best[hi][:5]:
                best[hi] = cand
    if mx not in best:
        return [(c, c) for c in range(mx + 1)]
    return best[mx][5]


def _flow_figs(q, fl, lim):
    try:
        parts = _split(fl, lim)
    except LoiBoCuc as ex:
        return [dict(ten=fl["ten"], svg="", w=0, h=0, syms=set(), phan=1, tong=1, loi=[f"BOCUC {ex}"])]
    order, back, col = _order(fl)
    # chữ cái nút nối: theo phần có nút ném rồi vị trí nút ném (trên xuống, trái sang phải)
    tg = []
    for a, b, lb in fl["edges"]:
        pa = next(k for k, (x, y) in enumerate(parts) if x <= col[a] <= y)
        pb = next(k for k, (x, y) in enumerate(parts) if x <= col[b] <= y)
        if pa != pb and b not in tg:
            tg.append(b)
    letters = {}
    if tg:
        import itertools
        seqs = []   # mỗi phần: các ô đích của nút nối, xếp theo vị trí nút (trên xuống, trái sang phải)
        for k, (lo, hi) in enumerate(parts):
            L = _layout(fl, lo, hi, _links_for(fl, parts, lo, hi))
            ds = []
            for lk in [i for i in L["N"] if i.startswith("_t") or i.startswith("_c")]:
                dich_ = fl["edges"][int(lk[2:])][1] if lk.startswith("_t") else lk[2:]
                ds.append((L["cy"][lk], L["cx"][L["col"][lk]], dich_, L["N"][lk]["lane"]))
            seqs.append([(d_, ln_) for _y, _x, d_, ln_ in sorted(ds)])
        first = []
        for sq in seqs:
            first += [d_ for d_, _ln in sq if d_ not in first]

        def lech(perm):   # chỉ đếm cặp khác làn: cặp cùng làn được bố cục xếp lại theo chữ cái
            rank = {b: n_ for n_, b in enumerate(perm)}
            return sum(1 for sq in seqs for x in range(len(sq)) for y in range(x + 1, len(sq))
                       if sq[x][1] != sq[y][1] and rank[sq[x][0]] > rank[sq[y][0]])
        best_p = first
        if lech(first) and len(first) <= 7:
            best_p = min(itertools.permutations(first), key=lambda p_: (lech(p_), [first.index(b) for b in p_]))
        for n_, b in enumerate(best_p):
            letters[b] = chr(ord("A") + n_)
    out = []
    for k, (lo, hi) in enumerate(parts):
        links = _links_for(fl, parts, lo, hi, letters)
        try:
            out.append(_solve(fl, lo, hi, links))
        except LoiBoCuc as ex:
            out.append(ex)
    # chữ cái nút nối: dồn lại cho liên tục A, B, C... (giữ nguyên thứ tự) theo các chữ thật sự có trên hình
    dung = sorted({nd["text"][0] for r in out if not isinstance(r, LoiBoCuc) for nd in r[0]["N"].values() if nd["kind"] in ("link_throw", "link_catch")})
    moi = {ch: chr(ord("A") + n_) for n_, ch in enumerate(dung)}
    res = []
    for k, r in enumerate(out):
        if isinstance(r, LoiBoCuc):
            res.append(dict(ten=fl["ten"], svg="", w=0, h=0, syms=set(), phan=k + 1, tong=len(parts), loi=[f"BOCUC {r}"]))
            continue
        L, routes, loi = r
        vt = []
        for i, nd in L["N"].items():
            if nd["kind"] in ("link_throw", "link_catch"):
                nd["text"] = moi[nd["text"][0]] + nd["text"][1:]
                vt.append((L["cy"][i], L["cx"][L["col"][i]], nd["text"][0]))
        for lb in L["lbls"]:
            if lb.get("node") in L["N"] and L["N"][lb["node"]]["kind"] in ("link_throw", "link_catch"):
                t0, x0, y0 = lb["lines"][0]
                lb["lines"][0] = (L["N"][lb["node"]]["text"][0] + t0[1:], x0, y0)
        seq = [c for _y, _x, c in sorted(vt)]
        if seq != sorted(seq):
            loi = loi + [f"CHU chữ cái nút nối không theo thứ tự trên xuống: {seq}"]
        svg, syms = _draw(q, fl, L, routes, k + 1, len(parts))
        res.append(dict(ten=fl["ten"], svg=svg, w=L["W"], h=L["H"], syms=syms, phan=k + 1, tong=len(parts), loi=loi + K.kiem(svg)))
    return res


_FIG_CACHE = {}


def figures(q, max_w=None):
    """Mọi hình của một quy trình: list dict(ten, svg, w, h, syms, phan, tong, loi). Mỗi hình rộng <= max_w
    (nới rãnh khi định tuyến có thể làm hình rộng hơn ước tính lúc chia, khi đó chia lại với giới hạn chặt hơn)."""
    max_w = max_w or MAX_W
    ck = (q["code"], max_w)
    if ck in _FIG_CACHE:
        return _FIG_CACHE[ck]
    global XEP_CHONG
    out = []
    for fl in build_flows(q):
        best = None
        for lim in (max_w, int(max_w * 0.85), int(max_w * 0.7), int(max_w * 0.55)):
            for chong in (True, False):
                XEP_CHONG = chong
                try:
                    fs = _flow_figs(q, fl, lim)
                    for _ in range(4):
                        over = max(f["w"] for f in fs) - max_w
                        if over <= 0:
                            break
                        fs = _flow_figs(q, fl, lim - over - G)
                finally:
                    XEP_CHONG = True
                bad = sum(1 for f in fs if f["w"] > max_w or f["h"] > MAX_H or f["loi"])
                sc = (bad, len(fs))
                if best is None or sc < best[0]:
                    best = (sc, fs)
                if not bad:
                    break
            if best[0][0] == 0:
                break
        fs = best[1]
        for f in fs:
            if f["w"] > max_w:
                f["loi"] = f["loi"] + [f"RONG rộng {int(f['w'])}px, quá khổ {max_w}px (chữ in sẽ dưới 7pt)"]
            if f["h"] > MAX_H:
                f["loi"] = f["loi"] + [f"CAO cao {int(f['h'])}px, quá khổ {MAX_H}px (không vừa một trang A4 ngang cùng tiêu đề, tên hình)"]
        out += fs
    _FIG_CACHE[ck] = out
    return out


def kiem_hinh(q, max_w=None):
    """Lỗi hình học của mọi hình một quy trình (rỗng = đạt): lỗi định tuyến + kết quả bpmn_geometry_check.kiem trên SVG."""
    return [f'{q["code"]} {f["ten"]} ({f["phan"]}/{f["tong"]}): {x}' for f in figures(q, max_w) for x in f["loi"]]


# ---------------------------------------------------------------- bảng bước
def step_kinds(q):
    them = set()
    for fl in build_flows(q):
        for i, nd in fl["nodes"].items():
            if re.fullmatch(r"\d+n", i):
                them.add(nd["step"])
    out = []
    for k, (vt, viec, vd, ngoai) in enumerate(q["buoc"], 1):
        loai = "service" if vt == D.HT else ("manual" if vd == "-" else "user")
        out.append((loai, k in them))
    return out


def _dk(nd_gw, lb):
    """Nhãn nhánh đọc được một mình: nhánh Có/Không ghép với câu hỏi của cổng."""
    if lb in ("Có", "Không") and nd_gw.get("text"):
        q_ = nd_gw["text"].rstrip("?").strip()
        return f"{q_[0].lower() + q_[1:]} ({lb.lower()})"
    return lb[0].lower() + lb[1:] if lb else lb


def chuyen_cho(q):
    """Bước -> 'Chuyển cho' lấy từ cạnh sơ đồ: đi qua cổng và việc ngoài phần mềm của bước, gom đủ điều kiện trên đường đi,
    dừng ở bước có số, quy trình con, việc xử lý nhánh không số hoặc kết thúc."""
    res = {}
    for fl in build_flows(q):
        N, E = fl["nodes"], fl["edges"]
        outs = {}
        for a, b, lb in E:
            outs.setdefault(a, []).append((b, lb))
        for i, nd in N.items():
            if not nd.get("num"):
                continue
            found, st, seen = [], [(i, [])], {i}
            while st:
                u, conds = st.pop(0)
                for v, lb in outs.get(u, []):
                    c2 = conds + ([_dk(N[u], lb)] if lb and N[u]["kind"] == "gw" else [])
                    w = N[v]
                    rieng = w["kind"] == "manual" and not w.get("num") and not re.fullmatch(r"\d+n", v)
                    if w.get("num") or w["kind"] in ("end", "call") or rieng:
                        found.append((c2, w, rieng))
                    elif v not in seen:
                        seen.add(v)
                        st.append((v, c2))
            items, dich_ = [], []
            for conds, w, rieng in found:
                if w["kind"] == "end":
                    ten_ = (w["text"][0].lower() + w["text"][1:]) if w.get("text") else ""
                    t = "Kết thúc" if not ten_ else (f"Kết thúc - {ten_}" if "(" in ten_ else f"Kết thúc ({ten_})")
                elif rieng:
                    t = (w["text"] if w["lane"] == nd["lane"] else f"{w['lane']}: {w['text'][0].lower() + w['text'][1:]}")
                elif w["kind"] == "call" and not w.get("num"):
                    t = w["text"]
                elif w["lane"] == nd["lane"]:
                    t = "Tự làm tiếp"
                else:
                    t = w["lane"]
                c = ", ".join(conds)
                c = c[0].upper() + c[1:] if c else c
                s_ = f"{c}: {t}" if c else t
                if s_ not in items:
                    items.append(s_)
                    dich_.append(t)
            if len(set(dich_)) == 1:  # mọi nhánh về cùng một nơi: không cần kể điều kiện
                items = [dich_[0]]
            res[nd["step"]] = "; ".join(items) if items else "Kết thúc"
            gon = getattr(D, "CHUYEN_CHO_GON", {}).get((q["code"], nd["step"]))
            if gon:
                thieu = [t_ for t_ in set(dich_) if t_ not in gon]
                if thieu or gon.count(";") + 1 != len(items):
                    raise SystemExit(f"CHUYEN_CHO_GON {q['code']} bước {nd['step']} không khớp sơ đồ: thiếu {thieu}, sơ đồ có {len(items)} nhánh")
                res[nd["step"]] = gon
    return res


def nhan_dieu_kien(q):
    """Bước -> điều kiện để làm bước đó: chỉ ghi khi mọi đường tiến vào bước đều là nhánh có nhãn của cổng rẽ."""
    out = {}
    for fl in build_flows(q):
        N = fl["nodes"]
        back = _order(fl)[1]
        for i, nd in N.items():
            if not nd.get("num"):
                continue
            vao = [(a, lb) for a, b, lb in fl["edges"] if b == i and (a, b) not in back]  # chỉ đường tiến; đường quay lui là làm lại
            for _ in range(3):  # đi ngược qua ô không số đứng ngay trước bước (việc ngoài phần mềm đi kèm) để lấy điều kiện của nhánh
                vao = [x for a, lb in vao for x in (
                    [(a2, lb2) for a2, b2, lb2 in fl["edges"] if b2 == a and (a2, b2) not in back]
                    if (N[a]["kind"] == "manual" and not N[a].get("num") and not lb) else [(a, lb)])]
            if vao and all(lb and N[a]["kind"] == "gw" for a, lb in vao):
                out[nd["step"]] = "; ".join(f'{N[a]["text"]} {lb}' for a, lb in vao)
            elif len(vao) > 1 and any(lb and N[a]["kind"] == "gw" for a, lb in vao) \
                    and all((lb and N[a]["kind"] == "gw") or (N[a]["kind"] in ("start", "timer") and N[a].get("text")) for a, lb in vao):
                out[nd["step"]] = "; hoặc ".join(f'{N[a]["text"]} {lb}' if lb else N[a]["text"] for a, lb in vao)
    return out


# ---------------------------------------------------------------- chú giải
CHU_GIAI_KY_HIEU = [
    ("user", "Ô xanh dương, hình người: việc vị trí đó làm trên Viindoo."),
    ("service", "Ô xanh lá, bánh răng (làn Hệ thống): hệ thống tự làm, người dùng không phải thao tác."),
    ("manual", "Ô vàng, bàn tay: việc làm ngoài phần mềm (giấy tờ, gặp đối tác, cổng thuế, ngân hàng...)."),
    ("call", "Ô viền đậm có dấu [+]: làm theo quy trình con ghi trong ô."),
    ("start", "Vòng nét mảnh: bắt đầu quy trình."),
    ("timer", "Vòng có đồng hồ: bắt đầu theo lịch (cuối ngày, cuối tháng, đến hạn...)."),
    ("wait", "Vòng đôi: chờ một sự kiện rồi mới làm tiếp."),
    ("end", "Vòng nét đậm: kết thúc quy trình hoặc kết thúc nhánh."),
    ("link_throw", "Vòng đôi có mũi tên đặc: đi tiếp ở phần sau, cùng chữ cái."),
    ("link_catch", "Vòng đôi có mũi tên rỗng: tiếp từ phần trước, cùng chữ cái."),
    ("gw", "Hình thoi dấu X: rẽ theo một nhánh có nhãn, hoặc gộp các nhánh lại."),
    ("arrow", "Mũi tên liền: thứ tự thực hiện."),
    ("label", "Chữ tím nghiêng trên mũi tên: điều kiện của nhánh."),
    ("lane", "Làn ngang: vị trí công việc thực hiện các ô trong làn."),
    ("num", "Số trước tên ô: số bước trong bảng bên dưới."),
    ("nonum", "Ô không số: việc kèm theo bước liền kề hoặc việc xử lý nhánh, không có dòng riêng trong bảng."),
]


def ky_hieu_svg(k):
    body = ""
    if k in ("user", "service", "manual"):
        f, c = COL[k]
        body = f'<rect x="1" y="1" width="32" height="18" rx="4" fill="{f}" stroke="{c}" stroke-width="1"/>{icon(k, 3, 2.5, 0.85)}'
    elif k == "call":
        f, c = COL["call"]
        body = (f'<rect x="1.5" y="1.5" width="31" height="17" rx="4" fill="{f}" stroke="{c}" stroke-width="{CALL_W}"/>'
                f'<rect x="13" y="10" width="8" height="8" fill="#fff" stroke="{c}"/><path d="M15,14H19M17,12V16" stroke="{c}"/>')
    elif k in EVENTS:
        body = _event(k, 17, 10, 8.5).replace('stroke-width="3.6"', 'stroke-width="2.8"')
    elif k == "gw":
        body = '<path d="M17,1L26,10L17,19L8,10Z" fill="#fff" stroke="#333" stroke-width="1"/><path d="M14,7L20,13M20,7L14,13" stroke="#333" stroke-width="1.6"/>'
    elif k == "arrow":
        body = '<path d="M3,10H28" stroke="#333" stroke-width="1.2"/><path d="M33,10L26,6.5V13.5Z" fill="#333"/>'
    elif k == "label":
        body = ('<path d="M3,14H28" stroke="#333" stroke-width="1"/><path d="M33,14L27,11V17Z" fill="#333"/>'
                f'<text x="3" y="10" font-size="12" font-style="italic" font-weight="600" fill="{LABEL_COL}">Có</text>')
    elif k == "lane":
        body = '<rect x="1" y="2" width="32" height="16" fill="#fff" stroke="#333"/><line x1="9" y1="2" x2="9" y2="18" stroke="#333"/>'
    elif k == "num":
        f, c = COL["user"]
        body = f'<rect x="1" y="1" width="32" height="18" rx="4" fill="{f}" stroke="{c}"/><text x="17" y="14.5" font-size="12" text-anchor="middle" fill="#282F33">3.</text>'
    elif k == "nonum":
        f, c = COL["manual"]
        body = f'<rect x="1" y="1" width="32" height="18" rx="4" fill="{f}" stroke="{c}"/>{icon("manual", 3, 2.5, 0.85)}'
    return (f'<svg class="kh" width="34" height="20" viewBox="0 0 34 20" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Roboto, Arial, sans-serif">{body}</svg>')


def chu_giai(syms):
    return [(k, t) for k, t in CHU_GIAI_KY_HIEU if k in syms]


def legend_svg():
    items, x = [], 6
    for k in ("user", "service", "manual", "call"):
        items.append(f'<g transform="translate({x},6) scale(1.3)">{ky_hieu_svg(k)[ky_hieu_svg(k).index(">") + 1:-6]}</g>'
                     f'<text x="{x + 50}" y="25" font-size="13" fill="#21272B">{TEN_LOAI[k]}</text>')
        x += 50 + len(TEN_LOAI[k]) * 7.2 + 22
    for k, t in (("start", "Bắt đầu"), ("timer", "Theo lịch"), ("end", "Kết thúc"), ("gw", "Cổng điều kiện")):
        items.append(f'<g transform="translate({x},6) scale(1.3)">{ky_hieu_svg(k)[ky_hieu_svg(k).index(">") + 1:-6]}</g>'
                     f'<text x="{x + 50}" y="25" font-size="13" fill="#21272B">{t}</text>')
        x += 50 + len(t) * 7.2 + 18
    return (f'<svg class="legend-bpmn" viewBox="0 0 {x} 40" width="{x}" height="40" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Roboto, Arial, sans-serif">{"".join(items)}</svg>')


def _font_css():
    """@font-face trỏ tới Roboto đủ dấu trong assets/fonts để ảnh PNG dùng đúng phông đã đo."""
    d = pathlib.Path(K.FONT_DIR)
    return "".join(f'@font-face{{font-family:Roboto;font-weight:{w};src:url("{(d / f).as_uri()}")}}'
                   for w, f in ((400, "Roboto-Regular.ttf"), (500, "Roboto-Medium.ttf"), (700, "Roboto-Bold.ttf")))


def export_png(svg, w, h, path):
    """SVG -> PNG (x2) bằng Chrome for Testing với hồ sơ tạm; không mở Chrome của người dùng."""
    import chrome_headless
    page = pathlib.Path(path).with_suffix(".html")
    page.write_text(f'<!doctype html><meta charset="utf-8"><style>{_font_css()}html,body{{margin:0;background:#fff}}</style>{svg}', encoding="utf-8")
    try:
        chrome_headless.screenshot(page, path, w, h)
    finally:
        page.unlink(missing_ok=True)


def export_many(items, workdir):
    """Nhiều SVG -> PNG (x2) trong ít lần chạy Chrome for Testing: xếp chồng trên một trang, chụp, cắt."""
    import chrome_headless
    from PIL import Image
    workdir = pathlib.Path(workdir)
    batch, h_sum = [], 0
    batches = []
    for it in items:
        if batch and h_sum + it[2] + 10 > 7000:
            batches.append(batch)
            batch, h_sum = [], 0
        batch.append(it)
        h_sum += it[2] + 10
    if batch:
        batches.append(batch)
    for k, bt in enumerate(batches):
        W = int(max(w for _, w, _, _ in bt)) + 2
        y, parts, boxes = 0, [], []
        for svg, w, h, path in bt:
            parts.append(f'<div style="position:absolute;left:0;top:{y}px;width:{w}px;height:{h}px">{svg}</div>')
            boxes.append((y, w, h, path))
            y += int(h) + 10
        page = workdir / f"_batch{k}.html"
        page.write_text(f'<!doctype html><meta charset="utf-8"><style>{_font_css()}html,body{{margin:0;background:#fff}}</style>' + "".join(parts), encoding="utf-8")
        shot = workdir / f"_batch{k}.png"
        try:
            chrome_headless.screenshot(page, shot, W, y)
            im = Image.open(shot)
            for y0, w, h, path in boxes:
                im.crop((0, int(y0 * 2), int(-(-w * 2 // 1)), int(-(-(y0 + h) * 2 // 1)))).save(path)
        finally:
            page.unlink(missing_ok=True)
            shot.unlink(missing_ok=True)


def font_min_pt(scale):
    """Cỡ chữ nhỏ nhất (pt) khi hình in ở tỉ lệ scale so với viewBox."""
    return F_MIN * scale * 0.75
