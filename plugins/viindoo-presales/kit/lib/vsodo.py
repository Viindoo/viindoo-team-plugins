# -*- coding: utf-8 -*-
"""So do quy trinh dang lan (swimlane) ve bang SVG, va thanh muc dap ung bon lop.

So do: moi lan ngang la mot VAI TRO, cac buoc di tu trai sang phai, mui ten net dut la quay lai.
Duong noi tu tranh o: doan doc di trong khe giua hai cot, vuong o thi vong qua mep lan.

Muc dap ung bon lop (thu tu tu re den dat):
    odoo        loi Odoo Community da co san
    viindoo     phai co phan he Viindoo moi lo duoc
    tuy_chinh   phan thieu lam bang Trinh tuy chinh ngay tren he thong dang chay, khong viet code
    lap_trinh   phan thieu phai viet code

Mot yeu cau dap ung MOT PHAN thi tach lam HAI hang muc: phan da co (phan_co) va phan con thieu
(phan_thieu). Nho the ty le tren thanh moi phan anh dung khoi luong phai lam them.
"""
from __future__ import annotations

import html

esc = html.escape

# kich thuoc so do - doi o day thi doi ca tai lieu
RONG_LAN = 118          # be ngang cot ten vai tro
RONG_COT = 140          # khoang cach giua hai buoc
RONG_O = 124            # be ngang mot o buoc
CAO_LAN = 100
CO_CHU = 10.5
CAO_DONG = 12.5
KY_TU_MOI_DONG = 21

KIEU = {
    "task": ("#ffffff", "#00BBCE", ""),       # ghi nhan tren phan mem
    "ext": ("#f6f6f6", "#8F8F8F", "4 3"),     # lam ben ngoai: thuc dia, giay to, khach
    "auto": ("#F3ECF3", "#7F4282", ""),       # he thong tu lam
    "dec": ("#FBF4DF", "#C99700", ""),        # diem quyet dinh
    "start": ("#00BBCE", "#00BBCE", ""),
    "end": ("#21272B", "#21272B", ""),
}

LOP = ["odoo", "viindoo", "tuy_chinh", "lap_trinh"]
LOP_CSS = {"odoo": "odoo", "viindoo": "viin", "tuy_chinh": "tuy", "lap_trinh": "lap"}
LOP_MAU = {"odoo": "#7A8B99", "viindoo": "#00BBCE", "tuy_chinh": "#7F4282", "lap_trinh": "#C99700"}


def nhan_lop(nen_odoo: str = "Odoo Community có sẵn") -> dict:
    """Nhan hien thi cua bon lop. `nen_odoo` ghi ro phien ban doi chieu, vi du 'Odoo Community 20 có sẵn'."""
    return {"odoo": nen_odoo, "viindoo": "Viindoo bổ sung",
            "tuy_chinh": "Tùy chỉnh, không viết code", "lap_trinh": "Phải lập trình"}


def _xuong_dong(t: str, toi_da: int = None):
    toi_da = toi_da or KY_TU_MOI_DONG
    dong, cur = [], ""
    for w in t.split():
        if len(cur) + len(w) + (1 if cur else 0) <= toi_da:
            cur = (cur + " " + w).strip()
        else:
            dong.append(cur)
            cur = w
    if cur:
        dong.append(cur)
    return dong


def so_do(lanes, steps) -> str:
    """Ve so do lan.

    lanes : list ten vai tro, theo thu tu tu tren xuong.
    steps : list tuple (ma, chi_so_lan, chu, kieu, nxt)
            kieu trong KIEU; nxt la list (ma_dich, nhan) hoac None de noi sang buoc ke tiep.
    """
    idx = {s[0]: i for i, s in enumerate(steps)}
    W = RONG_LAN + RONG_COT * (max(idx.values()) + 1) + 20
    H = CAO_LAN * len(lanes)
    pos = {}
    for sid, lane, text, kind, _nxt in steps:
        dong = _xuong_dong(text) if kind not in ("start", "end") else [text]
        cao = 30 if kind in ("start", "end") else min(max(34, len(dong) * CAO_DONG + 14), CAO_LAN - 10)
        x = RONG_LAN + idx[sid] * RONG_COT + (RONG_COT - RONG_O) / 2
        y = lane * CAO_LAN + (CAO_LAN - cao) / 2
        pos[sid] = (x, y, RONG_O, cao, dong, kind)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         'font-family="Roboto, Arial, sans-serif">',
         '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#6B6D70"/></marker></defs>']
    for li, ln in enumerate(lanes):
        y = li * CAO_LAN
        o.append(f'<rect x="0" y="{y}" width="{W}" height="{CAO_LAN}" '
                 f'fill="{"#FAFAFA" if li % 2 else "#FFFFFF"}" stroke="#E3E5E8"/>')
        o.append(f'<rect x="0" y="{y}" width="{RONG_LAN-8}" height="{CAO_LAN}" fill="#E5F8FA" stroke="#E3E5E8"/>')
        dong = _xuong_dong(ln, 13)[:3]
        for k, l in enumerate(dong):
            o.append(f'<text x="{(RONG_LAN-8)/2}" y="{y + CAO_LAN/2 - (len(dong)-1)*7 + k*14 + 4}" '
                     f'text-anchor="middle" font-size="11.5" font-weight="600" fill="#21272B">{esc(l)}</text>')

    thu_tu = [s[0] for s in steps]
    lan_cua = {s[0]: s[1] for s in steps}
    o_tren_lan = {}
    for sid, (x, y, w, _h, _d, _k) in pos.items():
        o_tren_lan.setdefault(lan_cua[sid], []).append((x, x + w))

    def cham(lane, xa, xb):
        lo, hi = min(xa, xb), max(xa, xb)
        return any(b1 < hi - 2 and b2 > lo + 2 for b1, b2 in o_tren_lan.get(lane, []))

    KHE = (RONG_COT - RONG_O) / 2
    for i, (sid, lane, _text, kind, nxt) in enumerate(steps):
        if kind == "end":
            continue
        dich = nxt if nxt else ([(thu_tu[i + 1], None)] if i + 1 < len(thu_tu) else [])
        for tid, nhan in dich:
            if tid not in pos:
                continue
            x1, y1, w1, h1, _, _ = pos[sid]
            x2, y2, w2, h2, _, _ = pos[tid]
            sy, ty = y1 + h1 / 2, y2 + h2 / 2
            lui = x2 < x1 or (abs(x2 - x1) < 1 and lan_cua[tid] <= lane)
            if lui:
                yb = max(y1 + h1, y2 + h2) + 14
                sx, tx = x1 + w1 / 2, x2 + w2 / 2
                d = f"M{sx},{y1+h1} V{yb} H{tx} V{y2+h2}"
                lx, ly = (sx + tx) / 2, yb - 5
            else:
                sx, tx = x1 + w1, x2
                if abs(sy - ty) < 1:
                    d = f"M{sx},{sy} H{tx}"
                    lx, ly = (sx + tx) / 2, sy - 6
                else:
                    xm = x2 - KHE
                    if xm <= sx + 6:
                        xm = (sx + tx) / 2
                    if cham(lane, sx, xm):
                        xg = sx + 8
                        ymep = (lane + 1) * CAO_LAN - 3 if lan_cua[tid] > lane else lane * CAO_LAN + 3
                        d = f"M{sx},{sy} H{xg} V{ymep} H{xm} V{ty} H{tx}"
                    else:
                        d = f"M{sx},{sy} H{xm} V{ty} H{tx}"
                    lx, ly = xm + 5, (sy + ty) / 2
            net = ' stroke-dasharray="5 4"' if lui else ""
            o.append(f'<path d="{d}" fill="none" stroke="#6B6D70" stroke-width="1.3"{net} '
                     'stroke-linejoin="round" marker-end="url(#ah)"/>')
            if nhan:
                o.append(f'<text x="{lx}" y="{ly}" font-size="10" fill="#7F4282" font-weight="600" '
                         f'paint-order="stroke" stroke="#fff" stroke-width="3">{esc(nhan)}</text>')

    for sid, (x, y, w, h, dong, kind) in pos.items():
        to, vien, net = KIEU[kind]
        if kind in ("start", "end"):
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{to}"/>')
            o.append(f'<text x="{x+w/2}" y="{y+h/2+4}" text-anchor="middle" font-size="{CO_CHU}" '
                     f'font-weight="600" fill="#fff">{esc(dong[0][:24])}</text>')
            continue
        if kind == "dec":
            o.append(f'<polygon points="{x+10},{y} {x+w-10},{y} {x+w},{y+h/2} {x+w-10},{y+h} {x+10},{y+h} {x},{y+h/2}" '
                     f'fill="{to}" stroke="{vien}" stroke-width="1.4"/>')
        else:
            da = f' stroke-dasharray="{net}"' if net else ""
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{to}" '
                     f'stroke="{vien}" stroke-width="1.4"{da}/>')
        y0 = y + h / 2 - (len(dong) - 1) * CAO_DONG / 2 + 3.5
        for k, l in enumerate(dong):
            o.append(f'<text x="{x+w/2}" y="{y0+k*CAO_DONG}" text-anchor="middle" '
                     f'font-size="{CO_CHU}" fill="#21272B">{esc(l)}</text>')
    o.append("</svg>")
    return "".join(o)


def chu_giai_so_do() -> str:
    """Chu giai cach doc so do - dat mot lan o phan tong quan."""
    return ('<div class="legend">'
            '<span><i style="background:#fff;border-color:#00BBCE"></i>Ghi nhận trên phần mềm</span>'
            '<span><i style="background:#f6f6f6;border-color:#8F8F8F;border-style:dashed"></i>'
            'Làm bên ngoài (thực địa, giấy tờ, khách)</span>'
            '<span><i style="background:#F3ECF3;border-color:#7F4282"></i>Tự động</span>'
            '<span><i style="background:#FBF4DF;border-color:#C99700"></i>Điểm quyết định</span>'
            "</div>")


# ----------------------------------------------------------------- muc dap ung
def dem_lop(hang_muc) -> dict:
    """Dem hang muc theo lop. Moi phan tu co 'phan_co' va/hoac 'phan_thieu' la ten lop."""
    d = {k: 0 for k in LOP}
    for r in hang_muc:
        if r.get("phan_co"):
            d[r["phan_co"]] += 1
        if r.get("phan_thieu"):
            d[r["phan_thieu"]] += 1
    return d


def thanh(hang_muc, nho: bool = False, nhan: dict = None) -> str:
    """Thanh ty le bon lop cua mot quy trinh (hoac cua toan bo tai lieu khi nho=False)."""
    nhan = nhan or nhan_lop()
    d = dem_lop(hang_muc)
    n = sum(d.values()) or 1
    o = ['<div class="pb mini">' if nho else '<div class="pb">']
    for k in LOP:
        if not d[k]:
            continue
        pct = d[k] * 100 / n
        chu = "" if nho or pct < 8 else f"{round(pct)}%"
        o.append(f'<div class="seg {LOP_CSS[k]}" style="width:{pct:.2f}%" '
                 f'title="{esc(nhan[k])}: {d[k]} hạng mục">{chu}</div>')
    o.append("</div>")
    if not nho:
        o.append('<div class="pbl">')
        for k in LOP:
            if d[k]:
                o.append(f'<span><i style="background:{LOP_MAU[k]}"></i>{esc(nhan[k])}: <b>{d[k]}</b></span>')
        o.append("</div>")
    return "".join(o)


def truy_vet(ma_br: str, nguon: str = "", nguon_day_du: str = "") -> str:
    """Nhan truy vet: ma yeu cau trong danh muc BR + vi tri goc trong tai lieu khach gui.

    `nguon` dang 'ô E16 · nhóm 5 Mua hàng · cột Yêu cầu chi tiết';
    `nguon_day_du` la ten tep day du, hien khi dua con tro len.
    """
    o = [f'<span class="brc">{esc(ma_br)}</span>']
    if nguon:
        o.append(f'<span class="src" title="{esc(nguon_day_du)}">{esc(nguon)}</span>')
    return " ".join(o)
