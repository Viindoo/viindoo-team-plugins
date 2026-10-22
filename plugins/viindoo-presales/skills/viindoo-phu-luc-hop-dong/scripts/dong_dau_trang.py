#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phu dau trang (logo hai ben + vach mau brand) va so trang len mot PDF da in.

    python3 dong_dau_trang.py <vao.pdf> --hop-dong SO.261020.19726 --nhan "Phụ lục 01" \\
        [--logo-khach <anh.png>] [--bat-dau 1] [--tong 24] [--ra <ra.pdf>] [--khong-dau-trang]

Vi sao lam bang lop phu thay vi CSS: khi in bang trinh duyet, `position:fixed` khong lap dung
tren moi trang. Lop phu nay ve theo toa do tuyet doi so voi mep giay nen trang nao cung dung cho.

Can: pypdf va Google Chrome.
"""
import argparse
import base64
import os
import subprocess
import sys
import tempfile

CHROME_MAC = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
KIT = os.path.join(os.environ.get("CLAUDE_PLUGIN_ROOT",
                   os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
                       os.path.abspath(__file__)))))))
LOGO_VIINDOO = os.path.join(KIT, "brand", "logos", "viindoo-logo-color.svg")


def _b64(duong_dan):
    with open(os.path.expanduser(duong_dan), "rb") as f:
        return base64.b64encode(f.read()).decode()


def _tim_chrome():
    for p in (os.environ.get("CHROME_PATH"), CHROME_MAC, "/usr/bin/google-chrome", "/usr/bin/chromium"):
        if p and os.path.exists(p):
            return p
    return None


def dong_dau(pdf_vao, pdf_ra, hop_dong, nhan, logo_khach=None, bat_dau=1, tong=None, dau_trang=True):
    try:
        import pypdf
    except ImportError:
        print("Thiếu pypdf. Cài bằng: python3 -m pip install pypdf")
        return 1
    chrome = _tim_chrome()
    if not chrome:
        print("Không tìm thấy Google Chrome. Đặt biến CHROME_PATH trỏ tới Chrome.")
        return 1

    doc = pypdf.PdfReader(pdf_vao)
    so_trang = len(doc.pages)
    tong = tong or (bat_dau + so_trang - 1)

    vii = _b64(LOGO_VIINDOO)
    khach_img = (f'<img class="kh" src="data:image/png;base64,{_b64(logo_khach)}">'
                 if logo_khach else "")
    head = (f'<div class="hd">{khach_img}'
            f'<img class="vii" src="data:image/svg+xml;base64,{vii}">'
            f'<div class="ct">Hợp đồng số: {hop_dong} - {nhan}</div>'
            f'<div class="bars"><i class="cy"></i><i class="pu"></i></div></div>') if dau_trang else ""

    trang = "".join(
        f'<div class="pg">{head}'
        f'<div class="ft"><div class="bars"><i class="cy"></i><i class="pu"></i></div></div>'
        f'<div class="num">Trang {bat_dau + i}/{tong}</div></div>' for i in range(so_trang))

    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 0; }}
html, body {{ margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; }}
.pg {{ position: relative; width: 210mm; height: 297mm; break-after: page; page-break-after: always; }}
.pg:last-child {{ break-after: auto; page-break-after: auto; }}
.hd {{ position: absolute; left: 14mm; right: 14mm; top: 8mm; }}
.hd .kh {{ height: 30px; }}
.hd .vii {{ height: 22px; float: right; margin-top: 4px; }}
.hd .ct {{ clear: both; text-align: right; font-style: italic; font-size: 9pt; color: #282F33; margin-top: 2px; }}
.bars {{ display: flex; margin-top: 4px; }}
.bars i {{ display: block; height: 3px; }}
.cy {{ background: #00BBCE; flex: 0 0 62%; }}
.pu {{ background: #7F4282; flex: 1 1 auto; }}
.ft {{ position: absolute; left: 14mm; right: 14mm; bottom: 14mm; }}
.num {{ position: absolute; right: 14mm; bottom: 7mm; font: italic 9pt/1 Arial; color: #282F33; }}
</style></head><body>{trang}</body></html>"""

    tmp = tempfile.mkdtemp()
    hp = os.path.join(tmp, "lop-phu.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    op = os.path.join(tmp, "lop-phu.pdf")
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--user-data-dir={tmp}/cr", f"--print-to-pdf={op}", "file://" + hp],
                   capture_output=True)
    if not os.path.exists(op):
        print("Chrome không in được lớp phủ.")
        return 1

    phu = pypdf.PdfReader(op)
    ghi = pypdf.PdfWriter()
    for i, t in enumerate(doc.pages):
        t.merge_page(phu.pages[i])
        ghi.add_page(t)
    with open(pdf_ra, "wb") as f:
        ghi.write(f)
    print(f"Đã ghi: {pdf_ra} | {so_trang} trang | đánh số {bat_dau}-{bat_dau + so_trang - 1}/{tong}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Đóng dấu đầu trang và số trang lên PDF phụ lục")
    p.add_argument("pdf")
    p.add_argument("--hop-dong", required=True)
    p.add_argument("--nhan", default="Phụ lục 01")
    p.add_argument("--logo-khach", default=None)
    p.add_argument("--bat-dau", type=int, default=1)
    p.add_argument("--tong", type=int, default=None)
    p.add_argument("--ra", default=None)
    p.add_argument("--khong-dau-trang", action="store_true")
    a = p.parse_args(argv)
    vao = os.path.abspath(os.path.expanduser(a.pdf))
    ra = a.ra or vao.replace(".pdf", " - da dong dau.pdf")
    return dong_dau(vao, ra, a.hop_dong, a.nhan, a.logo_khach, a.bat_dau, a.tong,
                    dau_trang=not a.khong_dau_trang)


if __name__ == "__main__":
    sys.exit(main())
