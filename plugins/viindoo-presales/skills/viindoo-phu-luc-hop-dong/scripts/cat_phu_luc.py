#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cat Phu luc hop dong ra tu chinh ban phuong an da gui khach.

    python3 cat_phu_luc.py <phuong-an.html> --hop-dong SO.261020.19726 \\
        [--muc "2,3,6"] [--ten "PHỤ LỤC 01 - KẾ HOẠCH TRIỂN KHAI VÀ PHẠM VI ĐÁP ỨNG"] \\
        [--ngay "___/___/2026"] [--ra <duong-dan-ra.html>]

Nguyen tac: KHONG viet lai noi dung. Phu luc la LAT CAT cua phuong an, cat nguyen van cac muc
da duoc khach doc va dong y, chi danh lai so muc cho phu luc dung doc lap. Phu luc lech voi
phuong an mot chu nao la mam mong tranh chap ve sau.

Mac dinh cat Muc 2 (pham vi dap ung), Muc 3 (hang muc phat trien), Muc 6 (ke hoach chi tiet).
"""
import argparse
import os
import re
import sys


def tim_muc(src: str, so: int):
    """Vi tri bat dau cua '<h2 ...> <so>. ' - lay lan xuat hien CUOI (bo qua muc luc o dau trang)."""
    vt = [m.start() for m in re.finditer(rf'<h2[^>]*>\s*{so}\.\s', src)]
    return vt[-1] if vt else None


def lat_cat(src: str, so: int, so_ke_tiep):
    dau = tim_muc(src, so)
    if dau is None:
        return None
    cuoi = None
    for s in so_ke_tiep:
        cuoi = tim_muc(src, s)
        if cuoi is not None and cuoi > dau:
            break
        cuoi = None
    phan = src[dau:cuoi] if cuoi else src[dau:]
    # bo the <section> mo thua o cuoi lat cat - neu khong se sinh mot trang trang khi in
    return re.sub(r"<section[^>]*>\s*$", "", phan.rstrip())


def danh_lai_so(x: str, anh_xa: dict) -> str:
    """Doi so muc theo anh_xa {cu: moi}. Dung ma trung gian de khong map chong len nhau."""
    cap = []
    for cu, moi in anh_xa.items():
        cap += [(f"{cu}. ", f"@@{moi}@@. "), (f"Mục {cu}", f"Mục @@{moi}@@"),
                (f'id="sec-{cu}"', f'id="sec-@@{moi}@@"'), (f'href="#sec-{cu}"', f'href="#sec-@@{moi}@@"')]
    for a, b in cap:
        x = x.replace(a, b)
    for moi in anh_xa.values():
        x = x.replace(f"@@{moi}@@", str(moi))
    return x


def main(argv=None):
    p = argparse.ArgumentParser(description="Cắt phụ lục hợp đồng từ bản phương án đề xuất")
    p.add_argument("phuong_an", help="đường dẫn bản phương án HTML đã gửi khách")
    p.add_argument("--hop-dong", required=True, help="số hợp đồng, ví dụ SO.261020.19726")
    p.add_argument("--muc", default="2,3,6", help="các mục cắt từ phương án, mặc định 2,3,6")
    p.add_argument("--ten", default="PHỤ LỤC 01 - KẾ HOẠCH TRIỂN KHAI VÀ PHẠM VI ĐÁP ỨNG")
    p.add_argument("--so-phu-luc", default="01")
    p.add_argument("--ngay", default="___/___/2026", help="ngày ký hợp đồng, để trống cho khách điền")
    p.add_argument("--ra", default=None)
    a = p.parse_args(argv)

    nguon = os.path.abspath(os.path.expanduser(a.phuong_an))
    src = open(nguon, encoding="utf-8").read()
    styles = "\n".join(re.findall(r"<style.*?</style>", src, re.S))
    if not styles:
        print("Không tìm thấy <style> trong bản phương án - phụ lục sẽ mất định dạng.")
        return 1

    so_muc = [int(s.strip()) for s in a.muc.split(",") if s.strip()]
    toi_da = max(so_muc) + 6
    anh_xa = {cu: i + 1 for i, cu in enumerate(so_muc)}

    phan = []
    for cu in so_muc:
        ke_tiep = [s for s in range(cu + 1, toi_da)]
        x = lat_cat(src, cu, ke_tiep)
        if x is None:
            print(f"Không tìm thấy Mục {cu} trong bản phương án.")
            return 1
        phan.append(danh_lai_so(x, anh_xa))

    ra = a.ra or os.path.join(os.path.dirname(nguon),
                              f"Phu luc {a.so_phu_luc} - {a.ten.split(' - ')[-1]}.html")
    html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<title>{a.ten}</title>
{styles}
<style>
@page {{ size: A4; margin: 32mm 14mm 24mm 14mm; }}
body {{ margin: 28px; background: #fff; }}
h1.pl {{ text-align: center; font-size: 15pt; margin: 0 0 4px; }}
p.pl {{ text-align: center; font-style: italic; margin: 0 0 20px; }}
</style></head>
<body>
<h1 class="pl">{a.ten}</h1>
<p class="pl">Số: {a.hop_dong}-{a.so_phu_luc} - đi kèm Hợp đồng Cung cấp Dịch vụ số {a.hop_dong} ngày {a.ngay}</p>
{"".join(phan)}
</body></html>
"""
    open(ra, "w", encoding="utf-8").write(html)
    print("Đã ghi:", ra)
    print("Cắt từ:", os.path.basename(nguon), "| mục", " -> ".join(f"{c} thành {m}" for c, m in anh_xa.items()))

    con_sot = [t for t in ("ngày công", "Junior", "Senior", "Expert", "manday") if t.lower() in html.lower()]
    if con_sot:
        print("CẢNH BÁO - phụ lục còn từ chỉ dành cho bản nội bộ:", ", ".join(con_sot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
