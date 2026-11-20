# -*- coding: utf-8 -*-
"""Kiểm hình học sơ đồ BPMN trên chính SVG đã sinh (độc lập với bộ định tuyến).

Đọc lại SVG: đường (path có mũi tên), ô việc, cổng, sự kiện, đường ngăn làn, viền bể, chữ. Bề rộng chữ đo bằng
phông Roboto thật, đủ dấu tiếng Việt (assets/fonts, đo bằng PIL). Trả danh sách lỗi; rỗng = đạt. Đơn vị: px của viewBox. Tỉ lệ in nhỏ nhất 0,78
(1px viewBox = 0,206mm) nên D_SONG = 10px = 2,06mm trên giấy.

Quy tắc (mã lỗi):
  MUI   đường khác đi qua vùng đầu mũi tên (AZ px cuối, rộng +-AZ_W) của một đường
  SONG  hai đường cùng phương chồng khúc mà cách nhau < D_SONG (kể cả trùng nhau)
  THANG hai đường khác nhau nằm thẳng hàng trên cùng một hàng / cột, hai đầu cách nhau < D_THANG (đọc thành một đường nối tiếp)
  TEN   tên bể (chữ xoay dọc) dài hơn chiều cao bể hoặc lấn ra ngoài dải tên bể
  LAN   đường chạy song song đường ngăn làn / viền bể / vạch tên làn gần hơn D_SONG
  O     đường đi qua ô, cổng, sự kiện không phải đầu mút của nó, hoặc đi qua / gấp / dừng sát nút đó gần hơn D_O
  NHAN  đường cắt chữ (nhãn nhánh, nhãn cổng, nhãn sự kiện); nhãn đè nhau, đè ô, nằm trên đường ngăn làn, ra ngoài bể
  CHAM  góc gấp hoặc đầu mút của đường này nằm trên đường kia (chữ T), giao cắt sát góc gấp / đầu mút (< D_GIAO),
        giao cắt sát ô, cổng, sự kiện (< D_GIAO_O)
  CONG  hai đường dùng chung một cạnh của một nút (chung điểm vào/ra)
  BE    nút hoặc đường ra ngoài bể; đầu đường không bám vào nút
"""
import functools
import html
import os
import re

from PIL import ImageFont

D_SONG = 10.0   # khoảng cách tối thiểu giữa hai đường song song, giữa đường và vạch làn / viền bể
D_O = 10.0      # khoảng hở tối thiểu giữa đường (kể cả chỗ gấp, chỗ dừng) và nút không phải đầu mút của nó
D_THANG = 40.0  # hai đường khác nhau nằm trên cùng một hàng / cột: hai đầu (chỗ gấp) phải cách nhau ít nhất chừng này
D_GIAO_O = 14.0 # điểm giao cắt phải cách mọi ô, cổng, sự kiện ít nhất chừng này
D_GIAO = 10.0   # điểm giao cắt vuông góc phải cách đầu nguồn ít nhất chừng này
D_GIAO_GAP = 30.0  # điểm giao cắt phải cách mọi góc gấp của hai đường ít nhất chừng này
D_LAN = 20.0    # đường chạy song song vạch làn / viền bể phải cách ít nhất chừng này
D_GIAO_NHAN = 20.0  # điểm giao cắt phải cách nhãn nhánh (chữ tím) ít nhất chừng này
D_NHAN = 6.0    # đường không thuộc nút phải cách nhãn sự kiện, nhãn cổng ít nhất chừng này
AZ, AZ_W = 30.0, 6.0   # vùng đầu mũi tên: dài AZ dọc theo đoạn cuối (mũi tên 10px + 20px trước chân mũi tên), rộng mỗi bên AZ_W
MM_PER_PX = 25.4 / 96

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts")   # Roboto đủ dấu tiếng Việt


@functools.lru_cache(None)
def _font(bold, size):
    name = "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"
    p = os.path.join(FONT_DIR, name)
    if not os.path.exists(p):
        raise SystemExit("Thiếu phông Roboto để đo bề rộng chữ: " + p)
    return ImageFont.truetype(p, int(round(size * 8)))


@functools.lru_cache(None)
def text_w(t, size=12, bold=False):
    """Bề rộng chữ (px) theo Roboto thật."""
    return _font(bool(bold), size).getlength(t) / 8.0


def _attrs(tag):
    return dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))


def parse(svg):
    """SVG -> dict(W, H, pool, hdr_x, lanes_y, nodes[(loại, x, y, w, h)], edges[pts], texts[(loại, bbox, chữ)])."""
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    W, H = float(m.group(1)), float(m.group(2))
    g = dict(W=W, H=H, nodes=[], edges=[], texts=[], lanes_y=[], vlines=[])
    body = svg[svg.index("</defs>") + 7:]
    rects = [_attrs(t) for t in re.findall(r"<rect [^>]*>", body)]
    pr = rects[0]
    g["pool"] = (float(pr["x"]), float(pr["y"]), float(pr["width"]), float(pr["height"]))
    for a in rects[1:]:
        if a.get("rx") == "9":
            g["nodes"].append(("task", float(a["x"]), float(a["y"]), float(a["width"]), float(a["height"])))
    for t in re.findall(r"<line [^>]*>", body):
        a = _attrs(t)
        x1, y1, x2, y2 = (float(a[k]) for k in ("x1", "y1", "x2", "y2"))
        if abs(y1 - y2) < 0.01:
            g["lanes_y"].append((y1, min(x1, x2), max(x1, x2)))
        else:
            g["vlines"].append((x1, min(y1, y2), max(y1, y2)))
    g["hdr_x"] = max([v[0] for v in g["vlines"]] + [0])
    for t in re.findall(r"<path [^>]*>", body):
        a = _attrs(t)
        d = a.get("d", "")
        if "marker-end" in a:
            pts = [tuple(float(v) for v in p.split(",")) for p in re.split(r"[ML]", d) if p]
            pts = [p for k, p in enumerate(pts) if k == 0 or p != pts[k - 1]]
            g["edges"].append(pts)
        elif d.endswith("Z") and d.count("L") == 3 and a.get("fill") == "#fff" and "transform" not in t:
            p = [tuple(float(v) for v in q.split(",")) for q in re.split(r"[MLZ]", d) if q]
            xs, ys = [q[0] for q in p], [q[1] for q in p]
            if max(xs) - min(xs) > 30:
                g["nodes"].append(("gw", min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)))
    for t in re.findall(r"<circle [^>]*>", body):
        a = _attrs(t)
        if a.get("fill") == "#fff" and float(a["r"]) >= 12:
            r = float(a["r"])
            g["nodes"].append(("event", float(a["cx"]) - r, float(a["cy"]) - r, 2 * r, 2 * r))
    g["titles"] = []
    for mt in re.finditer(r"<text ([^>]*)>([^<]*)</text>", body):
        a, s = _attrs("<text " + mt.group(1) + ">"), html.unescape(mt.group(2))
        if "transform" in a:
            m2 = re.search(r"translate\(([\d.]+),([\d.]+)\)", a["transform"])
            fs_ = float(a.get("font-size", 12))
            g["titles"].append((float(m2.group(1)), float(m2.group(2)), text_w(s, fs_, True), fs_, s))
            continue
        if not s.strip():
            continue
        fs = float(a.get("font-size", 12))
        x, y = float(a["x"]), float(a["y"])
        bold = a.get("font-weight") in ("600", "700", "bold")
        w = text_w(s, fs, bold)
        x0 = x - w / 2 if a.get("text-anchor") == "middle" else (x - w if a.get("text-anchor") == "end" else x)
        bb = (x0, y - 0.82 * fs, w, 1.06 * fs)
        if x0 + w <= g["hdr_x"] + 1:
            continue  # tên làn
        cx, cy = x0 + w / 2, bb[1] + bb[3] / 2
        if any(n[0] == "task" and n[1] <= cx <= n[1] + n[3] and n[2] <= cy <= n[2] + n[4] for n in g["nodes"]):
            g["texts"].append(("trong_o", bb, s))
            continue
        kind = "nhan_nhanh" if a.get("font-style") == "italic" else ("nhan_cong" if bold else "nhan_su_kien")
        g["texts"].append((kind, bb, s))
    return g


def _segs(pts):
    return [(pts[k], pts[k + 1]) for k in range(len(pts) - 1)]


def _hv(s):
    (x1, y1), (x2, y2) = s
    return "h" if abs(y1 - y2) < 0.01 else ("v" if abs(x1 - x2) < 0.01 else "d")


def _seg_rect(s, r, m=0.0):
    """Đoạn ngang/dọc có đi vào trong hình chữ nhật r nới thêm m không (chạm đúng mép không tính)."""
    (x1, y1), (x2, y2) = s
    rx, ry, rw, rh = r[0] - m, r[1] - m, r[2] + 2 * m, r[3] + 2 * m
    lox, hix, loy, hiy = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
    e = 0.01
    return lox < rx + rw - e and hix > rx + e and loy < ry + rh - e and hiy > ry + e


def _box_hit(a, b, m=0.0):
    return a[0] < b[0] + b[2] - m and b[0] < a[0] + a[2] - m and a[1] < b[1] + b[3] - m and b[1] < a[1] + a[3] - m


def _node_at(g, pt, tol=2.5):
    best = None
    for k, (kind, x, y, w, h) in enumerate(g["nodes"]):
        if x - tol <= pt[0] <= x + w + tol and y - tol <= pt[1] <= y + h + tol:
            on = min(abs(pt[0] - x), abs(pt[0] - x - w), abs(pt[1] - y), abs(pt[1] - y - h)) <= tol
            if on:
                best = k
    return best


def _side(n, pt):
    kind, x, y, w, h = n
    d = {"l": abs(pt[0] - x), "r": abs(pt[0] - x - w), "t": abs(pt[1] - y), "b": abs(pt[1] - y - h)}
    return min(d, key=d.get)


def kiem(svg, ten=""):
    """Danh sách lỗi hình học của một SVG (rỗng = đạt)."""
    g = parse(svg)
    loi = []
    px, py, pw, ph = g["pool"]
    E = g["edges"]
    ends = []
    name = []
    for k, pts in enumerate(E):
        a, b = _node_at(g, pts[0]), _node_at(g, pts[-1])
        ends.append((a, b))
        name.append(f"đường#{k + 1}({pts[0][0]:.0f},{pts[0][1]:.0f}->{pts[-1][0]:.0f},{pts[-1][1]:.0f})")
        if a is None or b is None:
            loi.append(f"BE {name[k]}: đầu đường không bám vào nút")
        if any(_hv(s) == "d" for s in _segs(pts)):
            loi.append(f"BE {name[k]}: có đoạn xiên")
        for x, y in pts:
            if not (g["hdr_x"] - 0.5 <= x <= px + pw + 0.5 and py - 0.5 <= y <= py + ph + 0.5):
                loi.append(f"BE {name[k]}: ra ngoài bể")
                break
    # CONG: mỗi cạnh của một nút chỉ một đường
    used = {}
    for k, pts in enumerate(E):
        a, b = ends[k]
        for nd, pt in ((a, pts[0]), (b, pts[-1])):
            if nd is not None:
                key = (nd, _side(g["nodes"][nd], pt), round(pt[0]), round(pt[1]))
                if key in used and used[key] != k:
                    loi.append(f"CONG {name[k]} và {name[used[key]]}: chung một điểm vào/ra của nút")
                used[key] = k
    # vùng đầu mũi tên
    zones = []
    for k, pts in enumerate(E):
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        if abs(y1 - y2) < 0.01:
            sx = 1 if x2 > x1 else -1
            L = min(AZ, abs(x2 - x1))
            zones.append((min(x2, x2 - sx * L), y2 - AZ_W, L, 2 * AZ_W))
        else:
            sy = 1 if y2 > y1 else -1
            L = min(AZ, abs(y2 - y1))
            zones.append((x2 - AZ_W, min(y2, y2 - sy * L), 2 * AZ_W, L))
    for k1 in range(len(E)):
        for k2 in range(len(E)):
            if k1 == k2:
                continue
            if any(_seg_rect(s, zones[k1]) for s in _segs(E[k2])):
                loi.append(f"MUI {name[k2]} đi qua vùng đầu mũi tên của {name[k1]}")
    # SONG, CHAM
    for k1 in range(len(E)):
        s1s = _segs(E[k1])
        for k2 in range(k1 + 1, len(E)):
            s2s = _segs(E[k2])
            for i1, s1 in enumerate(s1s):
                for i2, s2 in enumerate(s2s):
                    o1, o2 = _hv(s1), _hv(s2)
                    if o1 == o2 and o1 in "hv":
                        ax = 0 if o1 == "h" else 1
                        c1, c2 = s1[0][1 - ax], s2[0][1 - ax]
                        lo = max(min(s1[0][ax], s1[1][ax]), min(s2[0][ax], s2[1][ax]))
                        hi = min(max(s1[0][ax], s1[1][ax]), max(s2[0][ax], s2[1][ax]))
                        cung_nut = False
                        if abs(c1 - c2) < 1 and hi - lo <= 0.5:
                            e1 = min(s1, key=lambda p_: min(abs(p_[ax] - s2[0][ax]), abs(p_[ax] - s2[1][ax])))
                            e2 = min(s2, key=lambda p_: min(abs(p_[ax] - s1[0][ax]), abs(p_[ax] - s1[1][ax])))
                            n1 = _node_at(g, e1) if e1 in (E[k1][0], E[k1][-1]) else None
                            n2 = _node_at(g, e2) if e2 in (E[k2][0], E[k2][-1]) else None
                            cung_nut = n1 is not None and n1 == n2
                        if abs(c1 - c2) < 1 and -D_THANG + 0.01 < hi - lo <= 0.5 and not cung_nut:
                            loi.append(f"THANG {name[k1]} và {name[k2]}: thẳng hàng {'ngang' if ax == 0 else 'dọc'}, hai đầu cách {max(lo - hi, 0):.0f}px")
                        elif hi - lo > -D_SONG / 2 and abs(c1 - c2) < D_SONG - 0.01 and (hi - lo > 0.5 or abs(c1 - c2) < 1):
                            loi.append(f"SONG {name[k1]} và {name[k2]}: {'ngang' if ax == 0 else 'dọc'} cách {abs(c1 - c2):.1f}px, "
                                       f"chồng {max(hi - lo, 0):.0f}px")
                    elif {o1, o2} == {"h", "v"}:
                        h_, v_ = (s1, s2) if o1 == "h" else (s2, s1)
                        X, Y = v_[0][0], h_[0][1]
                        hx = sorted((h_[0][0], h_[1][0]))
                        vy = sorted((v_[0][1], v_[1][1]))
                        if hx[0] - 0.5 <= X <= hx[1] + 0.5 and vy[0] - 0.5 <= Y <= vy[1] + 0.5:
                            dh = min(abs(X - hx[0]), abs(X - hx[1]))
                            dv = min(abs(Y - vy[0]), abs(Y - vy[1]))
                            if dh < 0.6 or dv < 0.6:
                                loi.append(f"CHAM {name[k1]} và {name[k2]}: chữ T tại ({X:.0f},{Y:.0f})")
                            elif dh < D_GIAO - 0.01 or dv < D_GIAO - 0.01:
                                loi.append(f"CHAM {name[k1]} và {name[k2]}: giao cắt sát góc gấp/đầu mút tại ({X:.0f},{Y:.0f})")
                            elif any(abs(pt[0] - X) + abs(pt[1] - Y) < D_GIAO_GAP - 0.01 for kk, sg in ((k1, s1), (k2, s2)) for pt in sg
                                     if pt not in (E[kk][0], E[kk][-1])):
                                loi.append(f"CHAM {name[k1]} và {name[k2]}: giao cắt tại ({X:.0f},{Y:.0f}) cách góc gấp dưới {D_GIAO_GAP:.0f}px")
                            else:
                                for kd_, bb_, s_ in g["texts"]:
                                    if kd_ == "nhan_nhanh":
                                        ddx = max(bb_[0] - X, 0, X - bb_[0] - bb_[2])
                                        ddy = max(bb_[1] - Y, 0, Y - bb_[1] - bb_[3])
                                        if max(ddx, ddy) < D_GIAO_NHAN - 0.01:
                                            loi.append(f"CHAM {name[k1]} và {name[k2]}: giao cắt tại ({X:.0f},{Y:.0f}) sát nhãn nhánh '{s_}' ({max(ddx, ddy):.0f}px)")
                                for nd in g["nodes"]:
                                    ddx = max(nd[1] - X, 0, X - nd[1] - nd[3])
                                    ddy = max(nd[2] - Y, 0, Y - nd[2] - nd[4])
                                    if max(ddx, ddy) < D_GIAO_O - 0.01:
                                        loi.append(f"CHAM {name[k1]} và {name[k2]}: giao cắt tại ({X:.0f},{Y:.0f}) sát {nd[0]} ({max(ddx, ddy):.0f}px)")
    # LAN
    for k, pts in enumerate(E):
        for s in _segs(pts):
            o = _hv(s)
            if o == "h":
                y = s[0][1]
                lo, hi = sorted((s[0][0], s[1][0]))
                for ly, x1, x2 in g["lanes_y"] + [(py, px, px + pw), (py + ph, px, px + pw)]:
                    if abs(y - ly) < D_LAN - 0.01 and min(hi, x2) - max(lo, x1) > 0.5:
                        loi.append(f"LAN {name[k]}: chạy ngang cách vạch làn/viền bể {abs(y - ly):.1f}px (y={ly:.0f})")
            elif o == "v":
                x = s[0][0]
                for lx in (g["hdr_x"], px + pw):
                    if abs(x - lx) < D_LAN - 0.01:
                        loi.append(f"LAN {name[k]}: chạy dọc cách viền bể/vạch tên làn {abs(x - lx):.1f}px")
    # O
    for k, pts in enumerate(E):
        a, b = ends[k]
        ss = _segs(pts)
        for j, nd in enumerate(g["nodes"]):
            r = nd[1:]
            for i, s in enumerate(ss):
                if j in (a, b):
                    own_first = j == a and i == 0
                    own_last = j == b and i == len(ss) - 1
                    if own_first or own_last:
                        continue
                    if _seg_rect(s, r, 0):
                        loi.append(f"O {name[k]}: đi qua chính nút đầu mút")
                elif _seg_rect(s, r, 0):
                    loi.append(f"O {name[k]}: đi qua {nd[0]} tại ({r[0]:.0f},{r[1]:.0f})")
                elif _seg_rect(s, r, D_O):
                    loi.append(f"O {name[k]}: sát {nd[0]} tại ({r[0]:.0f},{r[1]:.0f}) dưới {D_O:.0f}px")
    # NHAN
    T = [t for t in g["texts"] if t[0] != "trong_o"]
    for kind, bb, s in T:
        for k, pts in enumerate(E):
            if any(_seg_rect(sg, bb, 0) for sg in _segs(pts)):
                loi.append(f"NHAN {name[k]} cắt chữ '{s}'")
            elif kind != "nhan_nhanh" and any(_seg_rect(sg, bb, D_NHAN) for sg in _segs(pts)):
                loi.append(f"NHAN {name[k]} sát chữ '{s}' dưới {D_NHAN:.0f}px")
        if not (g["hdr_x"] <= bb[0] and bb[0] + bb[2] <= px + pw and py <= bb[1] and bb[1] + bb[3] <= py + ph):
            loi.append(f"NHAN chữ '{s}' ra ngoài bể")
        for ly, x1, x2 in g["lanes_y"]:
            if bb[1] < ly < bb[1] + bb[3] and bb[0] < x2 and bb[0] + bb[2] > x1:
                loi.append(f"NHAN chữ '{s}' nằm trên đường ngăn làn y={ly:.0f}")
        for nd in g["nodes"]:
            if _box_hit(bb, nd[1:], 0.5):
                loi.append(f"NHAN chữ '{s}' đè {nd[0]} tại ({nd[1]:.0f},{nd[2]:.0f})")
    for i1 in range(len(T)):
        for i2 in range(i1 + 1, len(T)):
            if _box_hit(T[i1][1], T[i2][1], 0.5):
                loi.append(f"NHAN chữ '{T[i1][2]}' đè chữ '{T[i2][2]}'")
    # BE: nút trong bể, không đè nhau; chữ trong ô không tràn ô
    for i1, n1 in enumerate(g["nodes"]):
        if not (g["hdr_x"] < n1[1] and n1[1] + n1[3] < px + pw and py < n1[2] and n1[2] + n1[4] < py + ph):
            loi.append(f"BE nút {n1[0]} tại ({n1[1]:.0f},{n1[2]:.0f}) ra ngoài bể")
        for ly, x1, x2 in g["lanes_y"]:
            if n1[2] - 2 < ly < n1[2] + n1[4] + 2:
                loi.append(f"BE nút {n1[0]} tại ({n1[1]:.0f},{n1[2]:.0f}) nằm trên đường ngăn làn")
        for n2 in g["nodes"][i1 + 1:]:
            if _box_hit(n1[1:], n2[1:], -2):
                loi.append(f"BE hai nút đè hoặc sát nhau tại ({n1[1]:.0f},{n1[2]:.0f})")
    for kind, bb, s in g["texts"]:
        if kind == "trong_o":
            if not any(n[0] == "task" and n[1] + 1 <= bb[0] and bb[0] + bb[2] <= n[1] + n[3] - 1 and n[2] <= bb[1] and bb[1] + bb[3] <= n[2] + n[4]
                       for n in g["nodes"]):
                loi.append(f"NHAN chữ trong ô '{s}' tràn viền ô")
    band = min([v[0] for v in g["vlines"]] + [g["hdr_x"]])
    for tx, ty, tw, fs_, s_ in g["titles"]:
        if tw > ph - 6 or tx - 0.8 * fs_ < px + 1 or tx + 0.25 * fs_ > band - 1:
            loi.append(f"TEN tên bể '{s_}' dài {tw:.0f}px (bể cao {ph:.0f}px) hoặc lấn ra ngoài dải tên bể")
    out, seen = [], set()
    for x in loi:
        if x not in seen:
            seen.add(x)
            out.append(f"{ten}: {x}" if ten else x)
    return out


def tom_tat(loi):
    """Đếm lỗi theo mã."""
    d = {}
    for x in loi:
        m = re.search(r"(?:^|: )(MUI|SONG|THANG|TEN|LAN|O|NHAN|CHAM|CONG|BE) ", x)
        d[m.group(1) if m else "?"] = d.get(m.group(1) if m else "?", 0) + 1
    return d
