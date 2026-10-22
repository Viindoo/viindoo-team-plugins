# -*- coding: utf-8 -*-
"""Khung tai lieu HTML brand Viindoo dung chung cho bo bon buoc ho so khach hang.

Hai khuon:
  - `tai_lieu()`  : tai lieu dai, doc tren man hinh (buoc 1 Mo hinh hoat dong, buoc 2 Quy trinh va muc dap ung).
                    Header dinh + hero + muc luc dinh + section danh so + footer.
  - `phuong_an()` : tai lieu in/PDF theo mau chuan hien hanh (buoc 4 Phuong an de xuat).
                    Header logo + hero + tom tat dieu hanh + muc luc + section danh so.

Khong hardcode duong dan: CSS va logo doc tu chinh plugin (`kit/css`, `brand/logos`).
"""
from __future__ import annotations

import base64
import html
import os
import re

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


# ----------------------------------------------------------------- khoi cua phuong an (ban Quang Thang)
def nhom_nghiep_vu(tieu_de: str, cau_dan: str, muc, can_lam_ro=()) -> str:
    """Mot nhom trong Muc 2 'Mo ta nghiep vu tren he thong Viindoo'.

    tieu_de     : ten nhom, dat theo dong chay don hang cua khach
    cau_dan     : mot cau noi nhom nay giai quyet gi - viet cho nguoi lam nghe doc
    muc         : gach y tung y, moi y la mot viec he thong lam duoc
    can_lam_ro  : diem phai thong nhat o giai doan Khao sat - khong de lan vao phan khang dinh
    """
    o = [f'<div class="biz"><h3>{esc(tieu_de)}</h3>',
         f'<p class="biz-intro">{esc(cau_dan)}</p>',
         gach_y(muc).replace("<ul>", '<ul class="cell">')]
    if can_lam_ro:
        o.append(khoi_can_lam_ro(can_lam_ro))
    o.append("</div>")
    return "\n".join(o)


def khoi_can_lam_ro(muc) -> str:
    """Khung vang 'Can lam ro o giai doan Khao sat va Lap ke hoach'.

    Chi dua vao day diem ma cau tra loi LAM DOI giai phap, pham vi goi hay chi phi.
    """
    return ('<div class="lamro"><span class="t">Cần làm rõ ở giai đoạn Khảo sát và Lập kế hoạch</span>'
            + gach_y(muc).replace("<ul>", '<ul class="cell">') + "</div>")


def khoi_phat_trien(ten: str, gia: str, tom_tat: str, bai_toan, se_lam, vi_sao: str, gioi_han=()) -> str:
    """Mot hang muc trong Muc 3 'Cac yeu cau can phat trien ngoai pham vi goi'.

    `gia` la chuoi tien da dinh dang - ghi GIA TUNG HANG MUC, tuyet doi khong ghi gio hay ngay cong.
    """
    o = [f'<div class="dev"><h3><span class="price">{gia}</span>{esc(ten)}</h3>',
         f'<p class="biz-intro">{esc(tom_tat)}</p>',
         "<h5>Bài toán hiện nay</h5>", gach_y(bai_toan).replace("<ul>", '<ul class="cell">'),
         "<h5>Hệ thống sẽ làm gì</h5>", gach_y(se_lam).replace("<ul>", '<ul class="cell">'),
         "<h5>Vì sao phải phát triển thêm</h5>", f'<p class="biz-intro">{esc(vi_sao)}</p>']
    if gioi_han:
        o += ["<h5>Giới hạn phạm vi</h5>", gach_y(gioi_han).replace("<ul>", '<ul class="cell">')]
    o.append("</div>")
    return "\n".join(o)


NGUYEN_TAC_PHAT_TRIEN = (
    '<div class="callout success"><strong>Nguyên tắc thiết kế bắt buộc cho hạng mục phát triển</strong> '
    "Mỗi hạng mục được xây dựng mở rộng trên các phân hệ sẵn có thay vì dựng lại từ đầu, nên vẫn thừa hưởng "
    "phân quyền, nhật ký, báo cáo và các bản nâng cấp về sau. Dữ liệu sinh ra đi đúng vào chứng từ gốc của "
    "hệ thống, không tạo một luồng số liệu song song.</div>")


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


# ----------------------------------------------------------------- khuon phuong an (mau chuan)
def phuong_an(tieu_de: str, mo_ta: str, meta: str, the_tag, tom_tat_so, tom_tat_y: str,
              phan, css_them: str = "") -> str:
    """Phuong an de xuat theo mau chuan hien hanh (buoc 4) - in ra PDF gui khach.

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
# Gan nhu chac chan la cach tinh gia noi bo lo ra ngoai
CAM_HAN = ["junior", "senior", "expert", "manday", "man-day", "man day"]

# Co the la nghiep vu cua khach (vi du "lương theo ngày công" cua ho) - chi bao khi dung gan
# tu ngu ve tien, nen tra ve kem trich doan de nguoi doc tu quyet.
CAN_XEM = ["ngày công", "ngay cong", "giờ công", "gio cong", "đơn giá giờ"]
_GAN_TIEN = re.compile(r"(giá|chi phí|đơn giá|thành tiền|báo giá|triệu|đồng|vnđ|/giờ|/ngày)", re.I)


def kiem_ban_gui_khach(duong_dan: str, them=(), bo_qua=()) -> list:
    """Soat tep gui khach: cach tinh gia noi bo khong duoc lo ra ngoai.

    Tra ve list cac phat hien; rong la dat. Moi phat hien la mot dict:
      {"tu": ..., "muc": "cam" hoac "can_xem", "trich": "<doan van quanh cho tim thay>"}

    `muc = "cam"` thi phai sua. `muc = "can_xem"` la cho nguoi doc tu quyet: tu do co the la
    nghiep vu cua chinh khach (vi du "lương theo ngày công"), khong phai cach tinh gia cua Viindoo.
    """
    with open(duong_dan, encoding="utf-8") as f:
        goc = f.read()
    chu = re.sub(r"<[^>]+>", " ", goc)              # bo the HTML de trich doan doc duoc
    chu = re.sub(r"\s+", " ", chu)
    thap = chu.lower()
    bo_qua = [b.lower() for b in bo_qua]

    phat_hien = []
    for tu in list(CAM_HAN) + [t.lower() for t in them]:
        if tu in bo_qua:
            continue
        i = thap.find(tu)
        if i >= 0:
            phat_hien.append({"tu": tu, "muc": "cam", "trich": chu[max(0, i - 60):i + 80].strip()})
    for tu in CAN_XEM:
        if tu in bo_qua:
            continue
        for m in re.finditer(re.escape(tu), thap):
            quanh = chu[max(0, m.start() - 70):m.start() + 90]
            if _GAN_TIEN.search(quanh):
                phat_hien.append({"tu": tu, "muc": "can_xem", "trich": quanh.strip()})
                break
    return phat_hien


def in_ket_qua_soat(phat_hien) -> str:
    """In goi ket qua soat de doc tren dong lenh."""
    if not phat_hien:
        return "Soát bản gửi khách: đạt."
    o = []
    for p in phat_hien:
        nhan = "PHẢI SỬA" if p["muc"] == "cam" else "cần xem"
        o.append(f'[{nhan}] "{p["tu"]}" ... {p["trich"]}')
    return "\n".join(o)
