# -*- coding: utf-8 -*-
"""Nhánh B (khách đang dùng Viindoo/Odoo): rà soát CHỈ ĐỌC hệ thống đang vận hành, chạy các phép kiểm trong checks.CHECKS
có hỗ trợ nhánh B, ghi current_state.json và groups.json (nhóm quyền đúng tên trên giao diện) vào thư mục dữ liệu dự án.

Kết nối qua odoo_readonly.Client: chỉ phương thức đọc, phương thức ghi bị chặn tại máy. Đăng nhập lấy từ biến môi trường
ODOO_URL, ODOO_DB, ODOO_LOGIN, ODOO_PASSWORD. Phép kiểm nào không đọc được (thiếu ứng dụng, khác phiên bản) ghi "Chưa đọc được",
không làm dừng cả lượt quét.

Chạy: python3 scan_live_system.py --data <thư mục dự án> [--groups-only]
"""
import collections
import datetime
import json
import re

import common

A = common.cli("Rà soát chỉ đọc hệ thống đang vận hành (nhánh B)",
               lambda p: p.add_argument("--groups-only", action="store_true", help="chỉ đọc nhóm quyền (groups.json)"))

import checks as C  # noqa: E402
import odoo_readonly  # noqa: E402

TODAY = datetime.date.today()


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().casefold()


def dup_groups(cl, model, field, domain):
    """Giá trị trùng của một trường: [(giá trị, số bản ghi)]."""
    rows = cl.group(model, domain + [(field, "!=", False)], [field], [field])
    out = []
    for r in rows:
        n = r.get("__count") or r.get(f"{field}_count") or 0
        if n > 1:
            out.append((r[field], n))
    return out


def export_groups(cl):
    sec_field = "privilege_id" if cl.has_field("res.groups", "privilege_id") else "category_id"
    gs = cl.sr("res.groups", [], ["name", "full_name", "implied_ids", sec_field] if cl.has_field("res.groups", "full_name")
               else ["name", "implied_ids", sec_field])
    groups = [{"id": g["id"], "name": g["name"], "section": g[sec_field][1] if g.get(sec_field) else "-",
               "implied_ids": g["implied_ids"]} for g in gs]
    snap = {"server": cl.server_version, "read_at": TODAY.strftime("%d/%m/%Y"), "section_field": sec_field, "groups": groups,
            "roles": {"Người dùng": cl.xmlid("base", "group_user"), "Quản trị viên": cl.xmlid("base", "group_system")}}
    return common.write(common.data_file("groups.json"), json.dumps(snap, ensure_ascii=False, indent=1)), len(groups)


def scan(cl):
    R = []

    def run(cid, fn):
        try:
            v, det, note = fn()
            R.append(C.result(cid, v, det, note))
        except Exception as ex:   # thiếu ứng dụng, khác phiên bản: ghi lại, quét tiếp
            msg = str(ex)
            note = "chưa cài ứng dụng tương ứng" if "404" in msg or "doesn't exist" in msg or "không tồn tại" in msg else f"không đọc được: {msg[:160]}"
            R.append(C.result(cid, None, note=note))

    has_hr = cl.has_model("hr.employee")

    def dept():
        rs = cl.sr("hr.department", [("manager_id", "=", False)], ["name"])
        return len(rs), [r["name"] for r in rs], ""

    def emp_mgr():
        rs = cl.sr("hr.employee", [("parent_id", "=", False)], ["name"])
        return max(len(rs) - 1, 0), [r["name"] for r in rs], "một người đứng đầu không có quản lý là hợp lệ"

    def emp_job():
        rs = cl.sr("hr.employee", [("job_id", "=", False)], ["name"])
        return len(rs), [r["name"] for r in rs], ""

    if has_hr:
        run("org.dept_no_manager", dept)
        run("org.emp_no_manager", emp_mgr)
        run("org.emp_no_job", emp_job)
    else:
        for cid in ("org.dept_no_manager", "org.emp_no_manager", "org.emp_no_job"):
            R.append(C.result(cid, None, note="chưa cài ứng dụng Nhân viên"))

    gf = "group_ids" if cl.has_field("res.users", "group_ids") else "groups_id"

    def users_no_emp():
        rs = cl.sr("res.users", [("share", "=", False), ("employee_ids", "=", False)], ["name"])
        return len(rs), [r["name"] for r in rs], ""

    def admins():
        gid = cl.xmlid("base", "group_system")
        rs = cl.sr("res.users", [("share", "=", False), (gf, "in", [gid])], ["name"])
        return len(rs), [r["name"] for r in rs], ""

    if has_hr:
        run("org.users_no_employee", users_no_emp)
    run("org.admins", admins)

    if cl.has_model("approval.request.type"):
        def appr_types():
            rs = cl.sr("approval.request.type", [], ["name"])
            return len(rs), [r["name"] for r in rs], ""

        def appr_named():
            f = "approver_ids" if cl.has_field("approval.request.type", "approver_ids") else "type_approval_user_line_ids"
            rs = cl.sr("approval.request.type", [(f, "!=", False)], ["name"])
            return len(rs), [r["name"] for r in rs], "loại phê duyệt có người duyệt chỉ định đích danh"
        run("appr.types", appr_types)
        run("appr.named_approver", appr_named)
    else:
        R.append(C.result("appr.types", None, note="chưa cài ứng dụng Phê duyệt"))

    top = ["|", ("is_company", "=", True), ("parent_id", "=", False)]
    run("partner.dup_name", lambda: (lambda d: (len(d), [f"{k} ({n})" for k, n in d], ""))(dup_groups(cl, "res.partner", "name", top)))
    run("partner.dup_vat", lambda: (lambda d: (len(d), [f"{k} ({n})" for k, n in d], ""))(dup_groups(cl, "res.partner", "vat", [])))

    def co_no_vat():
        dom = [("is_company", "=", True), ("vat", "=", False)]
        if cl.has_field("res.partner", "customer_rank"):
            dom += ["|", ("customer_rank", ">", 0), ("supplier_rank", ">", 0)]
        rs = cl.sr("res.partner", dom, ["name"])
        return len(rs), [r["name"] for r in rs], ""
    run("partner.company_no_vat", co_no_vat)

    pt = "product.template"

    def no_code():
        rs = cl.sr(pt, [("default_code", "=", False)], ["name"])
        return len(rs), [r["name"] for r in rs], ""

    def no_categ():
        root = cl.xmlid("product", "product_category_all")
        rs = cl.sr(pt, [("categ_id", "=", root)], ["name"]) if root else []
        return len(rs), [r["name"] for r in rs], "sản phẩm ở nhóm gốc"

    def uom_var():
        rs = cl.sr("uom.uom", [], ["name"])
        g = collections.defaultdict(list)
        for r in rs:
            g[norm(r["name"])].append(r["name"])
        d = [" / ".join(v) for v in g.values() if len(v) > 1]
        return len(d), d, ""

    def no_tax():
        if not cl.has_field(pt, "taxes_id"):
            raise Exception("404 chưa cài Kế toán")
        dom = [("taxes_id", "=", False), ("supplier_taxes_id", "=", False)]
        if cl.has_field(pt, "sale_ok"):
            dom += ["|", ("sale_ok", "=", True), ("purchase_ok", "=", True)]
        rs = cl.sr(pt, dom, ["name"])
        return len(rs), [r["name"] for r in rs], ""

    if cl.has_model(pt):
        run("product.dup_name", lambda: (lambda d: (len(d), [f"{k} ({n})" for k, n in d], ""))(dup_groups(cl, pt, "name", [])))
        run("product.dup_code", lambda: (lambda d: (len(d), [f"{k} ({n})" for k, n in d], ""))(dup_groups(cl, pt, "default_code", [])))
        run("product.no_code", no_code)
        run("product.no_category", no_categ)
        run("product.uom_variants", uom_var)
        run("product.no_tax", no_tax)
    else:
        for cid in ("product.dup_name", "product.dup_code", "product.no_code", "product.no_category", "product.uom_variants", "product.no_tax"):
            R.append(C.result(cid, None, note="chưa cài ứng dụng Sản phẩm"))

    comps = cl.sr("res.company", [("id", "in", cl.companies)] if cl.companies else [], ["partner_id", "currency_id"])
    cpart = [c["partner_id"][0] for c in comps]
    ccur = {c["currency_id"][0] for c in comps}

    def banks():
        rs = cl.sr("res.partner.bank", [("partner_id", "in", cpart)], ["acc_number", "bank_id", "currency_id"])
        return len(rs), [f'{(r["bank_id"] or [0, ""])[1]} {r["acc_number"]}' for r in rs], ""

    def banks_fx():
        rs = cl.sr("res.partner.bank", [("partner_id", "in", cpart), ("currency_id", "!=", False), ("currency_id", "not in", list(ccur))],
                   ["acc_number", "currency_id"])
        return len(rs), [f'{r["acc_number"]} ({r["currency_id"][1]})' for r in rs], ""

    def shared_journal():
        js = cl.sr("account.journal", [("type", "=", "bank")], ["name", "bank_account_id", "default_account_id"])
        n_acc = cl.count("res.partner.bank", [("partner_id", "in", cpart)])
        thieu = [j["name"] for j in js if not j["bank_account_id"] or not j["default_account_id"]]
        thieu += [f"{n_acc} tài khoản ngân hàng, {len(js)} sổ ngân hàng"] if n_acc > len(js) else []
        return len(thieu), thieu, ""

    def no_stmt():
        js = cl.sr("account.journal", [("type", "=", "bank")], ["name"])
        d = [j["name"] for j in js if not cl.count("account.bank.statement.line", [("journal_id", "=", j["id"])])]
        return len(d), d, ""
    run("bank.accounts", banks)
    run("bank.foreign", banks_fx)
    run("bank.shared_journal", shared_journal)
    run("bank.no_statement", no_stmt)

    def no_lock():
        f = [x for x in ("fiscalyear_lock_date", "period_lock_date", "hard_lock_date", "sale_lock_date", "purchase_lock_date")
             if cl.has_field("res.company", x)]
        if not f:
            raise Exception("404 chưa cài Kế toán")
        rs = cl.sr("res.company", [("id", "in", cl.companies)] if cl.companies else [], ["name"] + f)
        d = [r["name"] for r in rs if not any(r.get(x) for x in f)]
        return len(d), d, ""

    def rec_misc():
        rs = cl.sr("account.account", [("reconcile", "=", True), ("account_type", "not in", ["asset_receivable", "liability_payable"])],
                   ["code", "name"])
        return len(rs), [f'{r["code"]} {r["name"]}' for r in rs], "đối soát nên chỉ bật ở tài khoản công nợ, tiền tạm thời"

    def categ_income():
        cs = cl.sr("product.category", [("product_count", ">", 0)] if cl.has_field("product.category", "product_count") else [],
                   ["name", "property_account_income_categ_id"])
        acc = {(c["property_account_income_categ_id"] or [0, "-"])[1] for c in cs}
        return (1 if len(cs) > 1 and len(acc) == 1 else 0), sorted(acc), f"{len(cs)} nhóm sản phẩm"

    def costing():
        f = [x for x in ("property_cost_method", "property_valuation") if cl.has_field("product.category", x)]
        if not f:
            raise Exception("không có trường phương pháp tính giá trên nhóm sản phẩm")
        cs = cl.sr("product.category", [], ["name"] + f)
        combos = collections.Counter(tuple(str(c.get(x)) for x in f) for c in cs)
        return max(len(combos) - 1, 0), [f'{" / ".join(k)}: {n} nhóm' for k, n in combos.items()], ""
    run("acc.no_lock", no_lock)
    run("acc.reconcile_misc", rec_misc)
    run("acc.categ_same_income", categ_income)
    run("acc.costing_mixed", costing)

    def partner_missing():
        n = cl.count("account.move.line", [("parent_state", "=", "posted"), ("partner_id", "=", False),
                                           ("account_type", "in", ["asset_receivable", "liability_payable"])])
        return n, [], "dòng công nợ đã ghi sổ không có đối tác"

    def unreconciled():
        dom = [("is_reconciled", "=", False), ("state", "not in", ["draft", "cancel", "canceled", "rejected"])]
        n = cl.count("account.payment", dom)
        return n, [], "khoản thu, chi chưa đối trừ vào hoá đơn"
    run("bal.partner_missing", partner_missing)
    run("bal.unreconciled", unreconciled)

    def asset_app():
        rs = cl.sr("ir.module.module", [("state", "=", "installed"), ("name", "ilike", "account_asset")], ["name"])
        return (0 if rs else 1), [r["name"] for r in rs], ""
    run("asset.no_app", asset_app)

    if cl.has_model("stock.quant"):
        def neg():
            rs = cl.sr("stock.quant", [("quantity", "<", 0), ("location_id.usage", "=", "internal")], ["product_id", "location_id", "quantity"])
            return len(rs), [f'{r["location_id"][1]} / {r["product_id"][1]}: {r["quantity"]:g}' for r in rs], ""

        def late():
            dom = [("state", "in", ["confirmed", "waiting", "assigned"]),
                   ("scheduled_date", "<", (TODAY - datetime.timedelta(days=7)).strftime("%Y-%m-%d"))]
            return cl.count("stock.picking", dom), [], "chờ quá 7 ngày so với ngày dự kiến"
        run("stock.negative", neg)
        run("docs.late_pickings", late)
    if cl.has_model("sale.order"):
        run("docs.so_to_invoice", lambda: (cl.count("sale.order", [("invoice_status", "=", "to invoice")]), [], ""))
    if cl.has_model("purchase.order"):
        run("docs.po_to_invoice", lambda: (cl.count("purchase.order", [("invoice_status", "=", "to invoice")]), [], ""))
    run("docs.draft_old", lambda: (cl.count("account.move", [("state", "=", "draft"),
                                                              ("date", "<", (TODAY - datetime.timedelta(days=30)).strftime("%Y-%m-%d"))]), [], ""))
    return R


def main():
    cl = odoo_readonly.Client()
    gpath, ng = export_groups(cl)
    print(gpath, f"{ng} nhóm quyền")
    if A.groups_only:
        return
    R = scan(cl)
    snap = {"source": "system", "url": cl.url, "server": cl.server_version, "read_at": TODAY.strftime("%d/%m/%Y"), "checks": R}
    out = common.write(common.data_file("current_state.json"), json.dumps(snap, ensure_ascii=False, indent=1))
    md = ["# Kết quả rà soát hệ thống đang vận hành (nội bộ, chỉ đọc)", "", f"- Hệ thống: {cl.url} (phiên bản {cl.server_version})",
          f"- Ngày đọc: {snap['read_at']}", "", "| Mảng | Phép kiểm | Số | Mức | Chi tiết |", "|---|---|---|---|---|"]
    for x in R:
        md.append(f"| {x['area']} | {x['label']} | {'' if x['value'] is None else x['value']} | {C.LEVELS[x['level']][0]} | "
                  + ("; ".join(map(str, x["detail"][:8])) or x["note"]).replace("|", "/") + " |")
    md_path = common.write(common.internal_dir() / "Kết quả rà soát hệ thống.md", "\n".join(md) + "\n")
    print(out)
    print(md_path)
    for x in R:
        print(f"  [{C.LEVELS[x['level']][0]}] {x['label']}: {'' if x['value'] is None else x['value']} {x['note']}")


if __name__ == "__main__":
    main()
