#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dung Danh muc Yeu cau Nghiep vu tu mot tep data.py.

    python3 build_br.py <duong-dan-data.py> [duong-dan-ra.xlsx]

Tep data.py khai: KHACH, R, va tuy chon TO_CHUC, XAC_NHAN, GHI_CHU, SAP_XEP.
Khong truyen duong dan ra thi ghi vao ~/Documents/project/<KHACH>/.
"""
import importlib.util
import os
import sys

KIT = os.path.join(os.environ.get("CLAUDE_PLUGIN_ROOT",
                   os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
                       os.path.abspath(__file__)))))), "kit", "lib")
sys.path.insert(0, KIT)
import vbr  # noqa: E402


def nap(duong_dan):
    duong_dan = os.path.abspath(os.path.expanduser(duong_dan))
    sys.path.insert(0, os.path.dirname(duong_dan))
    spec = importlib.util.spec_from_file_location("du_lieu_br", duong_dan)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    D = nap(argv[1])
    thieu = [t for t in ("KHACH", "R") if not getattr(D, t, None)]
    if thieu:
        print("Thiếu biến bắt buộc trong tệp dữ liệu:", ", ".join(thieu))
        return 1

    out = argv[2] if len(argv) > 2 else os.path.expanduser(
        f"~/Documents/project/{D.KHACH}/Danh mục Yêu cầu Nghiệp vụ Phần mềm - {D.KHACH}.xlsx")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)

    duong_dan = vbr.dung(
        D.R, out, khach=D.KHACH,
        to_chuc=getattr(D, "TO_CHUC", None),
        diem_xac_nhan=getattr(D, "XAC_NHAN", None),
        ghi_chu_chi_phi=getattr(D, "GHI_CHU", ""),
        sap_xep=getattr(D, "SAP_XEP", None))

    dem = {}
    for x in D.R:
        dem[x.get("pl", "?")] = dem.get(x.get("pl", "?"), 0) + 1
    print("Đã ghi:", duong_dan)
    print("Số yêu cầu:", len(D.R), "|", ", ".join(f"{k} {v}" for k, v in sorted(dem.items())))
    chua_co_gp = [x["id"] for x in D.R if not x.get("gp")]
    if chua_co_gp:
        print("Thiếu cột Giải pháp:", ", ".join(chua_co_gp))
    sai_gio = [x["id"] for x in D.R if x.get("pl") == "Phát triển" and not x.get("gio")]
    if sai_gio:
        print("Hạng mục Phát triển chưa có giờ:", ", ".join(sai_gio))
    co_gio_sai = [x["id"] for x in D.R if x.get("pl") == "Cần làm rõ" and x.get("gio")]
    if co_gio_sai:
        print("Hạng mục Cần làm rõ không được gán giờ:", ", ".join(co_gio_sai))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
