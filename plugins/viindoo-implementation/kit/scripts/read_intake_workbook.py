# -*- coding: utf-8 -*-
"""Nhánh A (khách mới): đọc workbook thu thập dữ liệu khách đã điền, chạy các phép kiểm trong checks.CHECKS,
ghi current_state.json vào thư mục dữ liệu dự án và bản tóm tắt nội bộ (điểm cần khách bổ sung) vào thư mục Nội bộ.

Chạy: python3 read_intake_workbook.py --data <thư mục dự án> --workbook <tệp khách điền.xlsx>
"""
import collections
import datetime
import json
import re

import common

A = common.cli("Đọc workbook thu thập dữ liệu (nhánh A) thành current_state.json",
               lambda p: p.add_argument("--workbook", required=True, help="tệp Excel khách đã điền"))

import openpyxl  # noqa: E402

import build_intake_workbook as BW  # noqa: E402
import checks as C  # noqa: E402

TK_CONG_NO = ("131", "331", "136", "336", "138", "338", "141", "244", "344")


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().casefold()


def num(v):
    if v in (None, ""):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(" ", "")
    if re.fullmatch(r"-?[\d.]+,\d+", s):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
        if s.count(".") > 1:
            s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def read(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    data = {}
    for s in C.SHEETS:
        if s["title"] not in wb.sheetnames:
            data[s["key"]] = None
            continue
        ws = wb[s["title"]]
        hdr_row = BW.HEADER_ROW   # 1-based hàng tiêu đề = HEADER_ROW (0-based HEADER_ROW - 1)
        heads = [re.sub(r"\s*\*$", "", str(c.value or "")).strip() for c in ws[hdr_row]]
        if s.get("form"):
            data[s["key"]] = {re.sub(r"\s*\*$", "", str(r[0] or "")).strip(): r[1] for r in ws.iter_rows(min_row=hdr_row + 1, values_only=True) if r[0]}
            continue
        rows = []
        for r in ws.iter_rows(min_row=hdr_row + 2, values_only=True):
            if not any(v not in (None, "") for v in r):
                continue
            rows.append({h: r[i] if i < len(r) else None for i, h in enumerate(heads) if h})
        data[s["key"]] = rows
    return data


def dup(values):
    c = collections.Counter(norm(v) for v in values if norm(v))
    return {k: n for k, n in c.items() if n > 1}


def run(d):
    R = []
    add = lambda cid, items, note="": R.append(C.result(cid, len(items), items, note))  # noqa: E731
    co = d.get("company") or {}
    req = C.sheet("company")["required_rows"]
    add("company.missing", [k for k in req if not str(co.get(k) or "").strip()])

    deps, poss, ppl = d.get("departments") or [], d.get("positions") or [], d.get("people") or []
    ten_ng = {norm(p.get("Họ tên")) for p in ppl}
    ten_vt = {norm(p.get("Vị trí công việc")) for p in poss}
    add("org.dept_no_manager", [x.get("Phòng ban") for x in deps if not norm(x.get("Quản lý phòng ban (họ tên)"))])
    no_mgr = [p.get("Họ tên") for p in ppl if not norm(p.get("Quản lý trực tiếp (họ tên)"))]
    add("org.emp_no_manager", no_mgr[1:], "người đầu tiên không có quản lý được coi là người đứng đầu" if no_mgr else "")
    add("org.emp_no_job", [p.get("Họ tên") for p in ppl if not norm(p.get("Vị trí công việc"))])
    add("org.manager_unknown", [f'{p.get("Họ tên")}: {p.get("Quản lý trực tiếp (họ tên)")}' for p in ppl
                                if norm(p.get("Quản lý trực tiếp (họ tên)")) and norm(p.get("Quản lý trực tiếp (họ tên)")) not in ten_ng])
    add("org.job_unknown", [f'{p.get("Họ tên")}: {p.get("Vị trí công việc")}' for p in ppl
                            if norm(p.get("Vị trí công việc")) and ten_vt and norm(p.get("Vị trí công việc")) not in ten_vt])
    no_sup = [x.get("Vị trí công việc") for x in poss if not norm(x.get("Vị trí cấp trên"))]
    add("org.job_no_superior", no_sup[1:], "vị trí đầu tiên không có cấp trên được coi là vị trí cao nhất" if no_sup else "")
    can_tk = [p for p in ppl if norm(p.get("Cần tài khoản đăng nhập")) == "có"]
    emails = [norm(p.get("Email đăng nhập")) for p in can_tk]
    trung = dup(emails)
    add("org.user_email", [p.get("Họ tên") for p in can_tk if not norm(p.get("Email đăng nhập")) or norm(p.get("Email đăng nhập")) in trung])

    apprs = d.get("approvals") or []
    kieu_vt = ("quản lý", "trưởng", "giám đốc") + tuple(ten_vt)
    add("appr.named_approver", [f'{a.get("Loại chứng từ cần duyệt")} bước {a.get("Bước")}: {a.get("Người duyệt")}' for a in apprs
                                if norm(a.get("Người duyệt")) in ten_ng or not any(k and k in norm(a.get("Người duyệt")) for k in kieu_vt)])
    add("appr.no_threshold", [f'{a.get("Loại chứng từ cần duyệt")} bước {a.get("Bước")}' for a in apprs
                              if re.search(r"\d", str(a.get("Điều kiện áp dụng bước") or "")) and num(a.get("Ngưỡng giá trị (đồng)")) is None])

    pts = d.get("partners") or []
    names = dup(p.get("Tên đầy đủ") for p in pts)
    add("partner.dup_name", [f"{k} ({n} dòng)" for k, n in names.items()])
    vats = dup(p.get("Mã số thuế") for p in pts)
    add("partner.dup_vat", [f"{k} ({n} dòng)" for k, n in vats.items()])
    add("partner.company_no_vat", [p.get("Tên đầy đủ") for p in pts if norm(p.get("Công ty / Cá nhân")) == "công ty" and not norm(p.get("Mã số thuế"))])
    ten_dt = {norm(p.get("Tên đầy đủ")) for p in pts}

    prs = d.get("products") or []
    add("product.dup_name", [f"{k} ({n} dòng)" for k, n in dup(p.get("Tên sản phẩm") for p in prs).items()])
    add("product.dup_code", [f"{k} ({n} dòng)" for k, n in dup(p.get("Mã nội bộ") for p in prs).items()])
    add("product.no_code", [p.get("Tên sản phẩm") for p in prs if not norm(p.get("Mã nội bộ"))])
    add("product.no_category", [p.get("Tên sản phẩm") for p in prs if not norm(p.get("Nhóm sản phẩm"))])
    uoms = collections.defaultdict(set)
    for p in prs:
        for k in ("Đơn vị tính", "Đơn vị mua (nếu khác)"):
            if str(p.get(k) or "").strip():
                uoms[norm(p.get(k))].add(str(p.get(k)).strip())
    add("product.uom_variants", [" / ".join(sorted(v)) for v in uoms.values() if len(v) > 1])
    add("product.no_tax", [p.get("Tên sản phẩm") for p in prs if not norm(p.get("Thuế bán")) and not norm(p.get("Thuế mua"))])
    ma_sp = {norm(p.get("Mã nội bộ")): p for p in prs}

    bks = d.get("banks") or []
    add("bank.dup_account", [f"{k} ({n} dòng)" for k, n in dup(re.sub(r"\D", "", str(b.get("Số tài khoản") or "")) for b in bks).items()])
    add("bank.accounts", [f'{b.get("Ngân hàng")} {b.get("Số tài khoản")} ({b.get("Tiền tệ") or "VND"})' for b in bks])
    add("bank.foreign", [f'{b.get("Ngân hàng")} {b.get("Số tài khoản")} ({b.get("Tiền tệ")})' for b in bks if norm(b.get("Tiền tệ")) not in ("", "vnd")])

    bal = d.get("balances") or []
    no, co_ = sum(num(b.get("Dư Nợ")) or 0 for b in bal), sum(num(b.get("Dư Có")) or 0 for b in bal)
    add("bal.not_balanced", [f"Nợ {no:,.0f} - Có {co_:,.0f} = {no - co_:,.0f}".replace(",", ".")] if bal and abs(no - co_) >= 1 else [])
    cong_no = [b for b in bal if str(b.get("Số tài khoản") or "").strip().startswith(TK_CONG_NO)]
    add("bal.partner_missing", [f'{b.get("Số tài khoản")}: {num(b.get("Dư Nợ")) or num(b.get("Dư Có")) or 0:,.0f}'.replace(",", ".")
                                for b in cong_no if not norm(b.get("Đối tác (công nợ)"))])
    add("bal.partner_unknown", sorted({str(b.get("Đối tác (công nợ)")) for b in cong_no
                                       if norm(b.get("Đối tác (công nợ)")) and ten_dt and norm(b.get("Đối tác (công nợ)")) not in ten_dt}))

    def du_tk(prefixes):
        return sum((num(b.get("Dư Nợ")) or 0) - (num(b.get("Dư Có")) or 0) for b in bal
                   if str(b.get("Số tài khoản") or "").strip().startswith(prefixes))

    stk = d.get("stock") or []
    gia_tri_kho = sum((num(s.get("Số lượng")) or 0) * (num(s.get("Đơn giá vốn")) or 0) for s in stk)
    if bal and stk:
        lech = gia_tri_kho - du_tk(("152", "153", "155", "156"))
        add("bal.stock_vs_gl", [f"tồn kho {gia_tri_kho:,.0f}, sổ cái 152-156 {du_tk(('152', '153', '155', '156')):,.0f}, lệch {lech:,.0f}".replace(",", ".")]
            if abs(lech) >= 1 else [])
    else:
        R.append(C.result("bal.stock_vs_gl", None, note="chưa đủ sheet số dư và tồn kho"))
    ass = d.get("assets") or []
    if bal and ass:
        ng, kh = sum(num(a.get("Nguyên giá")) or 0 for a in ass), sum(num(a.get("Khấu hao luỹ kế đến ngày chốt")) or 0 for a in ass)
        sai = []
        if abs(ng - du_tk(("211",))) >= 1:
            sai.append(f"nguyên giá {ng:,.0f}, tài khoản 211 {du_tk(('211',)):,.0f}".replace(",", "."))
        if abs(kh + du_tk(("214",))) >= 1:
            sai.append(f"khấu hao luỹ kế {kh:,.0f}, tài khoản 214 {-du_tk(('214',)):,.0f}".replace(",", "."))
        add("bal.asset_vs_gl", sai)
    else:
        R.append(C.result("bal.asset_vs_gl", None, note="chưa đủ sheet số dư và tài sản"))
    add("asset.missing", [a.get("Tên tài sản") for a in ass if num(a.get("Nguyên giá")) is None
                          or not a.get("Ngày bắt đầu khấu hao") or num(a.get("Số tháng khấu hao")) is None])
    add("asset.depr_over", [a.get("Tên tài sản") for a in ass if (num(a.get("Khấu hao luỹ kế đến ngày chốt")) or 0) > (num(a.get("Nguyên giá")) or 0)])

    whs = {norm(w.get("Mã kho")) for w in (d.get("warehouses") or [])}
    add("stock.negative", [f'{s.get("Mã kho")} / {s.get("Mã sản phẩm")}: {s.get("Số lượng")}' for s in stk if (num(s.get("Số lượng")) or 0) < 0])
    add("stock.unknown_product", sorted({str(s.get("Mã sản phẩm")) for s in stk if norm(s.get("Mã sản phẩm")) not in ma_sp}))
    add("stock.unknown_wh", sorted({str(s.get("Mã kho")) for s in stk if norm(s.get("Mã kho")) not in whs}))
    add("stock.serial_missing", [f'{s.get("Mã kho")} / {s.get("Mã sản phẩm")}' for s in stk
                                 if norm((ma_sp.get(norm(s.get("Mã sản phẩm"))) or {}).get("Theo dõi")) in ("theo lô", "theo số seri")
                                 and not norm(s.get("Lô / số seri"))])
    add("docs.unknown_partner", sorted({str(x.get("Đối tác")) for x in (d.get("open_docs") or [])
                                        if norm(x.get("Đối tác")) and ten_dt and norm(x.get("Đối tác")) not in ten_dt}))
    for s in C.SHEETS:
        if d.get(s["key"]) is None:
            for cid in s["checks"]:
                if not any(x["id"] == cid for x in R):
                    R.append(C.result(cid, None, note=f"thiếu sheet {s['title']}"))
    return R


def main():
    d = read(A.workbook)
    R = run(d)
    so_dong = {s["key"]: (len(d[s["key"]]) if isinstance(d.get(s["key"]), list) else None) for s in C.SHEETS}
    snap = {"source": "excel", "file": str(A.workbook), "read_at": datetime.date.today().strftime("%d/%m/%Y"),
            "row_counts": so_dong, "checks": R}
    out = common.write(common.data_file("current_state.json"), json.dumps(snap, ensure_ascii=False, indent=1))
    md = [f"# Kết quả kiểm dữ liệu thu thập (nội bộ)", "", f"- Tệp: {A.workbook}", f"- Ngày đọc: {snap['read_at']}", "",
          "| Mảng | Phép kiểm | Số | Mức | Chi tiết |", "|---|---|---|---|---|"]
    for x in R:
        md.append(f"| {x['area']} | {x['label']} | {'' if x['value'] is None else x['value']} | {C.LEVELS[x['level']][0]} | "
                  + ("; ".join(map(str, x["detail"][:8])) or x["note"]).replace("|", "/") + " |")
    cn = common.write(common.internal_dir() / "Kết quả kiểm dữ liệu thu thập.md", "\n".join(md) + "\n")
    can = [x for x in R if x["level"] in ("vua", "kem")]
    print(out)
    print(cn)
    print(f"{len(R)} phép kiểm; cần khách bổ sung, sửa: {len(can)}")
    for x in can:
        print(f"  [{C.LEVELS[x['level']][0]}] {x['label']}: {x['value']}")


if __name__ == "__main__":
    main()
