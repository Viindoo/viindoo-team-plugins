# -*- coding: utf-8 -*-
"""Tự kiểm ma trận phân quyền (handbook.MA_TRAN) theo nguyên tắc tuyến tính: ở mọi mục, cấp trên phải bao trùm nhóm quyền
của cấp dưới (trừ các mục trong handbook.NGOAI_LE_KE_THUA).

Tên mục, tên nhóm và quan hệ bao trùm lấy từ ảnh chụp nhóm quyền của chính hệ thống khách (groups.json trong thư mục dữ liệu dự án,
do scan_live_system.py đọc, chỉ đọc). Nhóm A bao trùm nhóm B khi B nằm trong bao đóng implied_ids của A. "-" (không chọn nhóm) thấp nhất.
Mọi ô của ma trận phải là đúng tên một nhóm có trên hệ thống, "Có" (ô đánh dấu) hoặc "-".

groups.json: {"server": "19.0", "groups": [{"id", "name", "implied_ids", "section"}], "roles": {"Người dùng": id, "Quản trị viên": id}}
("section" = tên mục trên màn hình phân quyền người dùng: res.groups.privilege ở bản 19, ir.module.category ở bản 17-18).
"""
import json

import common

D = common.load("handbook")


def _load():
    path = common.data_file("groups.json")
    if not path.exists():
        raise SystemExit(f"Thiếu {path}: chạy scan_live_system.py --groups-only trên hệ thống của khách (chỉ đọc) để lấy nhóm quyền")
    raw = path.read_text(encoding="utf-8")
    try:
        snap = json.loads(raw)
        groups, roles = snap["groups"], snap.get("roles", {})
    except (ValueError, KeyError, TypeError):   # dạng cũ: dòng 1 thông tin máy chủ, dòng 2 danh sách nhóm
        groups, roles = json.loads(raw.splitlines()[1]), {}
    by_id, by_name = {}, {}
    for g in groups:
        by_id[g["id"]] = g["implied_ids"]
        sec = g.get("section")
        if sec is None:
            ref = g.get("privilege_id") or g.get("category_id")
            sec = ref[1] if ref else "-"
        by_name[(sec or "-", g["name"])] = g["id"]
    # Vai trò trên màn hình người dùng: Người dùng = nhóm người dùng nội bộ, Quản trị viên = quản trị hệ thống
    by_name[("Vai trò", "Người dùng")] = roles.get("Người dùng") or by_name.get(("-", "Người dùng Nội bộ"))
    by_name[("Vai trò", "Quản trị viên")] = roles.get("Quản trị viên") or by_name.get(("-", "Vai trò/Quản trị viên"))
    return by_id, by_name


BY_ID, BY_NAME = _load()


def _closure(gid):
    seen, stack = set(), [gid]
    while stack:
        g = stack.pop()
        if g not in seen:
            seen.add(g)
            stack += BY_ID.get(g, [])
    return seen


def _nhom(muc, nhom_dau, o):
    """Ô -> id nhóm (None nếu "-"); lỗi nếu tên không có trên hệ thống."""
    if o == "-":
        return None
    if nhom_dau:  # ô đánh dấu
        if o != "Có":
            raise ValueError(f"{muc} / {nhom_dau}: ô đánh dấu chỉ nhận 'Có' hoặc '-', gặp '{o}'")
        cat = "-" if muc == "Nhóm riêng" else muc
        key = (cat, nhom_dau)
    else:
        key = (muc, o)
    if key not in BY_NAME:
        raise ValueError(f"Không có nhóm '{key[1]}' trong mục '{key[0]}' trên hệ thống")
    return BY_NAME[key]


def kiem():
    """Trả danh sách lỗi; rỗng nghĩa là ma trận đúng tên phần mềm và tuyến tính."""
    loi = []
    dinh = [vt for vt in D.VT_MT if vt not in D.CAP_TREN]
    if len(dinh) > 1:   # chỉ vị trí cao nhất được không có cấp trên
        loi.append("Các vị trí chưa có cấp trên trong CAP_TREN (chỉ được một vị trí cao nhất): " + ", ".join(dinh))
    for _cum, rows in D.MA_TRAN:
        for muc, nhom_dau, vals in rows:
            if len(vals) != len(D.VT_MT):
                loi.append(f"{muc}: số ô {len(vals)} khác số vị trí {len(D.VT_MT)}")
                continue
            o = dict(zip(D.VT_MT, vals))
            try:
                g = {vt: _nhom(muc, nhom_dau, x) for vt, x in o.items()}
            except ValueError as err:
                loi.append(str(err))
                continue
            if muc in getattr(D, 'NGOAI_LE_KE_THUA', set()) or nhom_dau in getattr(D, 'NGOAI_LE_KE_THUA', set()):
                continue
            for duoi, tren in D.CAP_TREN.items():
                gd = g[duoi]
                cao = getattr(D, 'CAP_CAO_TRONG_VT', {}).get((duoi, muc))
                if cao:
                    gd = _nhom(muc, nhom_dau, cao)
                if gd is not None and (g[tren] is None or gd not in _closure(g[tren])):
                    loi.append(f"{muc}{' / ' + nhom_dau if nhom_dau else ''}: '{tren}' ({o[tren]}) thấp hơn '{duoi}' ({cao or o[duoi]})")
    return loi


def ai_co_quyen(quyen):
    """Danh sách vị trí có ít nhất một (mục, nhóm) trong quyen, tính theo MA_TRAN và bao đóng implied; kèm ghi chú
    nếu chỉ một người trong vị trí giữ cấp đó (CAP_CAO_TRONG_VT)."""
    can = []
    for muc, nhom in quyen:
        cat = "-" if muc == "Nhóm riêng" else muc
        if (cat, nhom) not in BY_NAME:
            raise ValueError(f"Không có nhóm '{nhom}' trong mục '{muc}' trên hệ thống")
        can.append(BY_NAME[(cat, nhom)])
    o_by = {}
    for _cum, rows in D.MA_TRAN:
        for muc, nhom_dau, vals in rows:
            for vt, x in zip(D.VT_MT, vals):
                g = _nhom(muc, nhom_dau, x)
                if g is not None:
                    o_by.setdefault(vt, set()).update(_closure(g))
                cao = getattr(D, 'CAP_CAO_TRONG_VT', {}).get((vt, muc))
                if cao:
                    o_by.setdefault(("1", vt), set()).update(_closure(_nhom(muc, nhom_dau, cao)))
    out = []
    for vt in D.VT_MT:
        if o_by.get(vt, set()) & set(can):
            out.append(vt)
        elif o_by.get(("1", vt), set()) & set(can):
            out.append(vt + " (một người được giao)")
    return out


def kiem_phoi_hop():
    """Người nhận yêu cầu thiết lập phải là vị trí có quyền tạo mục đó."""
    loi = []
    for ten, _can, nhan, _tt, _lu, quyen in D.PHOI_HOP:
        try:
            co = ai_co_quyen(quyen)
        except ValueError as err:   # tên nhóm sai trong ma trận hoặc trong quyền tạo: báo lỗi, kiểm tiếp
            loi.append(f"Phối hợp '{ten}': {err}")
            continue
        for vt in D.VT_MT:
            if vt in nhan and not any(x.startswith(vt) for x in co):
                loi.append(f"Phối hợp '{ten}': người nhận '{vt}' không có quyền tạo")
        if not any(any(x.startswith(vt) for x in co) for vt in D.VT_MT if vt in nhan):
            loi.append(f"Phối hợp '{ten}': người nhận không thuộc vị trí có quyền ({', '.join(co)})")
    return loi


if __name__ == "__main__":
    print("Dùng: python3 check_handbook.py --data <thư mục dữ liệu dự án>")
