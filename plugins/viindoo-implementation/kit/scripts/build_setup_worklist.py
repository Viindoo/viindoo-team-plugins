# -*- coding: utf-8 -*-
"""Dựng 'Nội bộ/<Khách> - Việc thiết lập và điều chỉnh (nội bộ).html' (+ PDF): danh sách việc trên hệ thống theo từng gói.
NỘI BỘ Viindoo - không gửi khách, không đính kèm vào nhiệm vụ dự án (dự án trên viindoo.com khách xem được qua cổng thông tin).

Mỗi gói: thống nhất quy trình (quy trình của gói, vị trí cần có mặt), kế hoạch theo mã gửi khách, việc điều chỉnh dữ liệu và thiết lập
(danh mục việc + phân công), việc thiết lập phục vụ bộ quy trình, module cần cài, quyết định cần lấy từ khách, dữ liệu khách giao.
Kiểm chéo: mã việc trong setup_tasks.py phải có trong danh mục việc của project.py.
Chạy: python3 build_setup_worklist.py --data <thư mục dữ liệu dự án> [--no-pdf]
"""
import common

A = common.cli("Dựng danh sách việc thiết lập và điều chỉnh (nội bộ)",
               lambda p: p.add_argument("--no-pdf", action="store_true", help="không in PDF"))

import chrome_headless  # noqa: E402
import plan_model as M  # noqa: E402

P, H = M.P, M.H
S = common.load("setup_tasks")
e, g = common.e, common.hours
TU_QUYET = ("xác nhận", "chốt", "chọn bản giữ", "giao người", "duyệt")


def ma_viec_le(ma):
    """'3.1-3.4' hoặc '2.5, 4.3' -> danh sách mã lẻ."""
    out = []
    for part in str(ma).replace(" ", "").split(","):
        a, _, b = part.partition("-")
        if b and a.rsplit(".", 1)[0] == b.rsplit(".", 1)[0]:
            pre = a.rsplit(".", 1)[0]
            out += [f"{pre}.{i}" for i in range(int(a.rsplit(".", 1)[1]), int(b.rsplit(".", 1)[1]) + 1)]
        elif part:
            out.append(part)
    return out


def build():
    tk = M.tasks()
    codes = {t["code"]: t for _g, rs in tk for t in rs}
    loi = [f"setup_tasks.PHAN_CONG: mã {m} không có trong danh mục việc" for m in S.PHAN_CONG if m not in codes]
    loi += [f"setup_tasks.THIET_LAP '{v}': mã {m} không có trong danh mục việc" for _app, rows in S.THIET_LAP for v, _c, _p, ma, _g in rows
            for m in ma_viec_le(ma) if m not in codes]
    loi += [f"việc {c} chưa có phân công trong setup_tasks.PHAN_CONG" for c in codes if c not in S.PHAN_CONG]
    if loi:
        raise SystemExit("Danh sách việc lệch danh mục việc gửi khách:\n" + "\n".join(loi))
    ul = common.ul
    tag = lambda a: f'<span class="ai {"ai1" if a == S.AI else "ai2"}">{e(a)}</span>'  # noqa: E731

    def bang_nguoi(goi):
        rows = [r for r in S.VIEC_NGUOI if goi in r[3]]
        if not rows:
            return "<p>-</p>"
        return ('<table><colgroup><col style="width:6%"><col><col style="width:30%"></colgroup><thead><tr><th>#</th><th>Việc</th><th>Vì sao người làm</th></tr></thead><tbody>'
                + "".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c, _g in rows) + "</tbody></table>")

    def goi_html(pkg, so):
        qs = [q for q in (H.QUY_TRINH if H else []) if q["goi"] == pkg]
        vt = []
        for q in qs + ([x for x in (getattr(H, "PD", None), getattr(H, "DT", None)) if x] if H and pkg == min(P.PACKAGE_NAMES) else []):
            for b in q["buoc"]:
                if b[0] != getattr(H, "HT", None) and b[0] not in vt:
                    vt.append(b[0])
        o = [f"<section><h2>{so}. {e(P.PACKAGE_NAMES[pkg])}</h2>", f"<h3>{so}.1 Thống nhất quy trình</h3>",
             "<p><b>Quy trình cần thống nhất:</b> " + ("; ".join(f'{q["code"]} {e(q["ten"])}' for q in qs) or "-") + ".</p>",
             "<p><b>Vị trí cần có mặt hoặc cử người:</b> " + (e("; ".join(vt)) or "-") + ".</p>"]
        o.append(f"<h3>{so}.2 Kế hoạch theo mã gửi khách (mã nhiệm vụ [KH] trên viindoo.com)</h3>"
                 '<table><colgroup><col style="width:8%"><col style="width:44%"><col style="width:9%"><col style="width:7%"><col></colgroup>'
                 "<thead><tr><th>Mã KH</th><th>Việc</th><th>Tuần</th><th>Giờ</th><th>Kết quả</th></tr></thead><tbody>")
        trong, tong = False, 0
        for kind, ma, ten, tuan, h, kq in P.PLAN:
            if kind == "phase":
                trong = ma == str(pkg)
                continue
            if not trong:
                continue
            if kind == "sub":
                o.append(f'<tr class="grp"><td colspan="5">{e(ten)}</td></tr>')
            else:
                tong += M.item_hours(h)
                o.append(f"<tr><td><b>{e(ma)}</b></td><td>{e(ten)}</td><td>{e(tuan)}</td><td>{g(M.item_hours(h))}</td><td>{e(kq)}</td></tr>")
        o.append(f"<tr><td></td><td><b>Tổng gói {pkg}</b></td><td></td><td><b>{g(tong)}</b></td><td></td></tr></tbody></table>")
        o.append(f"<h3>{so}.3 Việc điều chỉnh dữ liệu và thiết lập</h3>"
                 '<table><colgroup><col style="width:7%"><col style="width:22%"><col style="width:6%"><col style="width:9%"><col><col style="width:16%"></colgroup>'
                 "<thead><tr><th>Mã việc</th><th>Việc</th><th>Giờ</th><th>Ai làm</th><th>Làm gì</th><th>Chờ</th></tr></thead><tbody>")
        for grp, rs in tk:
            if grp["package"] != pkg:
                continue
            o.append(f'<tr class="grp"><td colspan="6">{e(grp["code"])}. {e(grp["name"])}</td></tr>')
            for t in rs:
                ai, lam, cho = S.PHAN_CONG[t["code"]]
                o.append(f"<tr><td><b>{e(t['code'])}</b></td><td>{e(t['name'])}</td><td>{g(t['hours'])}</td><td>{tag(ai)}</td><td>{e(lam)}</td><td>{e(cho)}</td></tr>")
        o.append("</tbody></table>")
        o.append(f"<h3>{so}.4 Việc thiết lập phục vụ bộ quy trình</h3>"
                 '<table><colgroup><col style="width:20%"><col style="width:42%"><col style="width:28%"><col style="width:10%"></colgroup>'
                 "<thead><tr><th>Việc thiết lập</th><th>Cấu hình gì</th><th>Phục vụ (bộ quy trình)</th><th>Mã việc</th></tr></thead><tbody>")
        for app, rows in S.THIET_LAP:
            rs = [r for r in rows if r[4] == pkg]
            if rs:
                o.append(f'<tr class="grp"><td colspan="4">{e(app)}</td></tr>'
                         + "".join(f"<tr><td><b>{e(v)}</b></td><td>{e(c)}</td><td>{e(pv)}</td><td>{e(ma)}</td></tr>" for v, c, pv, ma, _g in rs))
        o.append("</tbody></table>")
        mods = [m for m in S.MODULES if m[3] == pkg]
        if mods:
            o.append(f"<h3>{so}.5 Module cần cài</h3>"
                     '<table><colgroup><col style="width:24%"><col style="width:20%"><col><col style="width:11%"></colgroup>'
                     "<thead><tr><th>Module</th><th>Tên trên Viindoo</th><th>Dùng cho</th><th>Hệ thống khách</th></tr></thead><tbody>"
                     + "".join(f"<tr><td><code>{e(m)}</code></td><td><b>{e(t)}</b></td><td>{e(d)}</td><td>{e(st)}</td></tr>" for m, t, d, _g, st in mods)
                     + "</tbody></table>")
        quyet = [(t["code"], x) for grp, rs in tk if grp["package"] == pkg for t in rs for x in t["customer"] if any(w in x.lower() for w in TU_QUYET)]
        o.append(f"<h3>{so}.6 Quyết định, xác nhận cần lấy từ khách</h3>"
                 '<table><colgroup><col style="width:8%"><col></colgroup><thead><tr><th>Mã việc</th><th>Khách xác nhận, chốt</th></tr></thead><tbody>'
                 + "".join(f"<tr><td><b>{e(m)}</b></td><td>{e(x)}</td></tr>" for m, x in quyet) + "</tbody></table>")
        o.append(f"<h3>{so}.7 Việc người làm</h3>" + bang_nguoi(pkg))
        o.append(f"<h3>{so}.8 Dữ liệu khách phải giao</h3>" + ul([f"{('tuần ' + w + ': ') if w else ''}{x}" for pk, x, w in P.CUSTOMER_INPUTS if pk == pkg])
                 + "</section>")
        return "".join(o)

    n_ai = sum(1 for v in S.PHAN_CONG.values() if v[0] == S.AI)
    body = ['<section><h2>1. Cách làm và việc chung</h2>' + ul(S.CACH_LAM + [f"AI làm {n_ai} / {len(S.PHAN_CONG)} việc của danh mục việc; còn lại người làm cùng khách.",
                                                                            "Không đính kèm tài liệu này vào nhiệm vụ dự án trên viindoo.com: dự án khách xem được qua cổng thông tin."])
            + "<h3>Việc chung của người</h3>" + bang_nguoi(0) + "</section>"]
    for so, pkg in enumerate(sorted(P.PACKAGE_NAMES), 2):
        body.append(goi_html(pkg, so))
    title = f"{P.SHORT_NAME} - Việc thiết lập và điều chỉnh (nội bộ)"
    css = """.wrap{max-width:1100px} table{table-layout:fixed} td{word-break:break-word} code{font-size:12.5px;color:var(--sec)}
.ai{display:inline-block;border-radius:5px;padding:1px 7px;font-size:12px;font-weight:600}
.ai1{background:#E6F8FA;color:#007F8C;border:1px solid #00BBCE}.ai2{background:#F2F2F2;color:#555;border:1px solid #cfcfcf}
tr{break-inside:avoid} tr.grp{break-after:avoid} h2,h3{break-after:avoid} main p{font-size:13.5px;margin:6px 0} @page{size:A4 landscape}"""
    doc = common.page(title, "Việc thiết lập và điều chỉnh trên hệ thống", f"{e(P.SHORT_NAME)} · Nội bộ Viindoo, không gửi khách · Lập ngày {e(P.DATE)}",
                      "".join(body), css)
    out = common.internal_dir() / f"{title}.html"
    errs = common.check_text(doc, out.name)
    if errs:
        raise SystemExit("\n".join(errs))
    common.write(out, doc)
    print(out)
    if not A.no_pdf:
        chrome_headless.print_pdf(out, out.with_suffix(".pdf"))
        print(out.with_suffix(".pdf"))


if __name__ == "__main__":
    build()
