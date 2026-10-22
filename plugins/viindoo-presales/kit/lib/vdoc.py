# -*- coding: utf-8 -*-
"""Khung tai lieu HTML brand Viindoo dung chung cho bo bon buoc ho so khach hang.

Hai khuon:
  - `tai_lieu()`  : tai lieu dai, doc tren man hinh (buoc 1 Mo hinh hoat dong, buoc 2 Quy trinh va muc dap ung).
                    Header dinh + hero + muc luc dinh + section danh so + footer.
  - `phuong_an()` : tai lieu in/PDF theo bo cuc JVC Eco v3 (buoc 4 Phuong an de xuat).
                    Header logo + hero + tom tat dieu hanh + muc luc + section danh so.

Khong hardcode duong dan: CSS va logo doc tu chinh plugin (`kit/css`, `brand/logos`).
"""
from __future__ import annotations

import base64
import html
import os

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.dirname(KIT)

esc = html.escape


# ----------------------------------------------------------------- tai nguyen
def css(ten: str) -> str:
    """Doc mot tep CSS trong kit: 'tai-lieu' hoac 'phuong-an'."""
    with open(os.path.join(KIT, "css", f"{ten}.css"), encoding="utf-8") as f:
        return f.read()


def bien_brand() -> str:
    """Khai bao bien mau/font Viindoo - dung cho moi tai lieu HTML."""
    return """:root{
  --viindoo-primary:#00BBCE; --viindoo-secondary:#7F4282;
  --viindoo-grey:#8F8F8F; --viindoo-grey-light-bg:#F2F2F2; --viindoo-white:#FFFFFF;
  --viindoo-text-heading:#21272B; --viindoo-text-body:#282F33; --viindoo-text-muted:#6B6D70;
  --viindoo-success:#00B365; --viindoo-warning:#C99700; --viindoo-info:#0099E6;
  --viindoo-font-heading:"Montserrat","Helvetica Neue",Arial,sans-serif;
  --viindoo-font-body:"Roboto","Helvetica Neue",Arial,sans-serif;
}
body{font-family:var(--viindoo-font-body);color:var(--viindoo-text-body)}
h1,h2,h3,h4,h5{font-family:var(--viindoo-font-heading);color:var(--viindoo-text-heading)}
"""


def logo_b64(nen_toi: bool = False) -> str:
    """Logo Viindoo dang data-uri SVG - nhung thang vao tep, khong phu thuoc mang.

    Mac dinh la ban mau (cyan + tim) theo chuan thuong hieu; ban dao mau danh cho nen toi.
    """
    ten = "viindoo-logo-inverted.svg" if nen_toi else "viindoo-logo-color.svg"
    with open(os.path.join(PLUGIN, "brand", "logos", ten), "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()


def logo_svg(nen_toi: bool = True) -> str:
    """Logo SVG noi tuyen - dung cho header tai lieu doc tren man hinh (nen trang: nen_toi=False)."""
    ten = "viindoo-logo-inverted.svg" if nen_toi else "viindoo-logo-color.svg"
    with open(os.path.join(PLUGIN, "brand", "logos", ten), encoding="utf-8") as f:
        return f.read()


def favicon_b64() -> str:
    """Favicon PNG nho (5 KB) - khong dung logo hi-res de tep khong phinh."""
    with open(os.path.join(PLUGIN, "brand", "logos", "viindoo-favicon.png"), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


# ----------------------------------------------------------------- tien ich noi dung
def tien(v, don_vi: str = "&nbsp;đ") -> str:
    """Dinh dang tien theo kieu Viet Nam: 382.500.000 d."""
    return f"{int(round(v)):,}".replace(",", ".") + don_vi


def gach_y(muc) -> str:
    """Gach y co nhan - quy tac trinh bay bat buoc cua moi tai lieu gui khach.

    `muc` la list, moi phan tu la chuoi, hoac cap (nhan, noi dung) -> '<b>Nhan:</b> noi dung'.
    """
    o = ["<ul>"]
    for m in muc:
        if isinstance(m, (tuple, list)):
            o.append(f"<li><b>{esc(str(m[0]))}:</b> {m[1]}</li>")
        else:
            o.append(f"<li>{m}</li>")
    o.append("</ul>")
    return "\n".join(o)


def bang(cot, dong, lop: str = "") -> str:
    """Bang co vien bo tron theo brand. `cot` la list tieu de, `dong` la list cac list o."""
    o = [f'<div class="tbl"><table class="{lop}">', "<tr>" + "".join(f"<th>{c}</th>" for c in cot) + "</tr>"]
    for d in dong:
        o.append("<tr>" + "".join(f"<td>{c}</td>" for c in d) + "</tr>")
    o.append("</table></div>")
    return "\n".join(o)


def the_so(so, nhan, lop: str = "card accent") -> str:
    """The so lieu lon - chi dung cho so CUA VIINDOO (gio, tuan, gia), khong dung cho so
    lay tu he thong dang chay cua khach (so don, so hoa don, so may...)."""
    return f'<div class="{lop}"><div class="big">{so}</div><div class="lbl">{esc(str(nhan))}</div></div>'


# ----------------------------------------------------------------- khuon tai lieu dai
def tai_lieu(tieu_de: str, mo_ta: str, khach: str, ngay: str, phan, css_them: str = "",
             js_them: str = "", mo_dau: str = "", chan_trang: str = "") -> str:
    """Tai lieu dai doc tren man hinh (buoc 1, buoc 2).

    `phan` la list dict: {"id","so","ten","noi_dung"}; muc luc sinh tu chinh danh sach nay.
    """
    toc = "".join(f'<a href="#{p["id"]}">{esc(p["ten"])}</a>' for p in phan)
    than = []
    for p in phan:
        than.append(f'<section id="{p["id"]}">')
        than.append(f'<h2><span class="no">{p.get("so", "")}</span>{esc(p["ten"])}</h2>')
        than.append(p["noi_dung"])
        than.append("</section>")
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(tieu_de)}</title>
<link rel="icon" type="image/png" href="{favicon_b64()}">
<style>
{bien_brand()}
{css('tai-lieu')}
{css_them}
</style>
</head>
<body>
<header class="top"><div class="wrap">{logo_svg(nen_toi=False)}<div class="meta">{esc(khach)}<br>{esc(ngay)}</div></div></header>
<div class="hero"><div class="wrap"><h1>{tieu_de}</h1><p>{mo_ta}</p></div></div>
<nav class="toc"><div class="wrap">{toc}</div></nav>
<main class="wrap">
{mo_dau}
{"".join(than)}
</main>
<footer><div class="wrap">{chan_trang or "Viindoo Technology JSC &middot; " + esc(khach)}</div></footer>
{js_them}
</body>
</html>
"""


# ----------------------------------------------------------------- khuon phuong an (bo cuc JVC v3)
def phuong_an(tieu_de: str, mo_ta: str, meta: str, the_tag, tom_tat_so, tom_tat_y: str,
              phan, css_them: str = "") -> str:
    """Phuong an de xuat theo bo cuc JVC Eco v3 (buoc 4) - in ra PDF gui khach.

    `the_tag`    : list nhan ngan duoi tieu de.
    `tom_tat_so` : list (so, nhan) cho khoi Tom tat dieu hanh - CHI so cua Viindoo
                   (tong dau tu, thue bao, tien do), khong phai so lay tu he thong khach.
    `phan`       : list dict {"id","ten","noi_dung"} - da danh so san trong "ten".
    """
    toc = "".join(f'<a href="#{p["id"]}">{esc(p["ten"])}</a>' for p in phan)
    tags = "".join(f'<span class="tag">{t}</span>' for t in the_tag)
    cards = "".join(f'<div class="exec-card"><div class="num">{s}</div><div class="lbl">{esc(str(n))}</div></div>'
                    for s, n in tom_tat_so)
    than = []
    for p in phan:
        than.append(f'<section><h2 id="{p["id"]}">{esc(p["ten"])}</h2>{p["noi_dung"]}</section>')
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{esc(tieu_de)}</title>
<style>
{css('phuong-an')}
{css_them}
</style>
</head>
<body>
<div class="page">
<div class="header">
  <img src="{logo_b64()}" alt="Viindoo">
  <div class="doc-meta">{meta}</div>
</div>
<div class="hero">
  <h1>{tieu_de}</h1>
  <p>{mo_ta}</p>
  <div class="tags">{tags}</div>
</div>
<div class="exec-summary">
  <h2>Tóm tắt điều hành</h2>
  <div class="exec-grid">{cards}</div>
  {tom_tat_y}
</div>
<div class="toc"><div class="toc-title">Mục lục</div>{toc}</div>
{"".join(than)}
</div>
</body>
</html>
"""


# ----------------------------------------------------------------- cong cu kiem tra truoc khi gui
CAM_TRONG_BAN_GUI_KHACH = ["ngày công", "ngay cong", "Junior", "Senior", "Expert", "manday", "man-day"]


def kiem_ban_gui_khach(duong_dan: str, them=()) -> list:
    """Soat tep gui khach: phan phat trien chi duoc ghi TONG TIEN.

    Tra ve danh sach tu cam con sot lai (rong = dat). Goi truoc khi giao tep cho khach.
    """
    with open(duong_dan, encoding="utf-8") as f:
        noi_dung = f.read().lower()
    return [t for t in list(CAM_TRONG_BAN_GUI_KHACH) + list(them) if t.lower() in noi_dung]
