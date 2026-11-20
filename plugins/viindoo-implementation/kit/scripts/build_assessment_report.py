# -*- coding: utf-8 -*-
"""Dựng '<Khách> - Báo cáo đánh giá hiện trạng và kế hoạch triển khai.html' (+ PDF) gửi khách.

Nguồn:
- current_state.json (thư mục dữ liệu dự án): kết quả phép kiểm, từ workbook thu thập (nhánh A) hoặc rà soát chỉ đọc (nhánh B).
- project.py: kết luận, danh mục việc, kế hoạch, đào tạo, dữ liệu khách cần gửi, nhân sự.
- handbook.py (nếu có): danh sách quy trình của bộ quy trình ứng dụng - khai một lần, báo cáo đọc lại, không chép.

Phần A. Hiện trạng | B. Danh mục việc cần làm | C. Kế hoạch chi tiết. Soát trước khi ghi: chỉ gạch ngang ASCII, không lộ cách tính giá nội bộ
(vdoc.kiem_ban_gui_khach của viindoo-presales), tổng giờ kế hoạch so với giờ trong gói đã ký.
Chạy: python3 build_assessment_report.py --data <thư mục dữ liệu dự án> [--out <thư mục ra>] [--no-pdf]
"""
import common

A = common.cli("Dựng báo cáo đánh giá hiện trạng và kế hoạch triển khai",
               lambda p: p.add_argument("--no-pdf", action="store_true", help="không in PDF"))

import checks as C  # noqa: E402
import chrome_headless  # noqa: E402
from plan_model import H, P, current_text, item_hours, processes, state, tasks, week_start, weeks  # noqa: E402,F401

e, g = common.e, common.hours


# ------------------------------------------------------------------ dựng
LOAI_MAU = {"Thiết lập": "#00BBCE", "Dữ liệu": "#C99700", "Phân quyền": "#7F4282", "Thiết lập + Dữ liệu": "#0099E6"}


def build():
    st = state()
    res = st["checks"]
    res_by_id = {r["id"]: r for r in res}
    nguon = ("workbook thu thập dữ liệu do doanh nghiệp điền" if st["source"] == "excel"
             else f"hệ thống đang vận hành (đọc, không ghi), phiên bản {st.get('server', '')}")
    body, toc = [], []
    n = 0

    def sec(phan, title, inner):
        nonlocal n
        n += 1
        if phan:
            body.append(f'<h2 class="phan">{e(phan)}</h2>')
            toc.append(f'<li class="p">{e(phan)}</li>')
        toc.append(f'<li><a href="#m{n}">{n}. {e(title)}</a></li>')
        body.append(f'<section><h2 id="m{n}">{n}. {e(title)}</h2>{inner}</section>')

    # A1 tổng quan
    kpis = "".join(f'<div class="kpi"><b>{e(b)}</b><span>{e(s)}</span><small>{e(sm)}</small></div>' for b, s, sm in getattr(P, "KPIS", []))
    sec("A. HIỆN TRẠNG", "Tổng quan hiện trạng",
        (f'<div class="kpis">{kpis}</div>' if kpis else "")
        + f'<p class="lead">Nguồn: {e(nguon)}; số liệu tại ngày {e(st["read_at"])}.</p><ul class="kv">'
        + "".join(f'<li><b class="k">{e(k)}:</b> {e(v)}</li>' for k, v in P.CONCLUSIONS) + "</ul>")
    # A2 theo mảng
    rows = []
    rank = {"kem": 3, "vua": 2, "tot": 1}
    for area in C.AREAS:
        rs = [r for r in res if r["area"] == area]
        graded = [r for r in rs if r["level"] in rank]
        if not graded and area not in getattr(P, "AREA_NOTES", {}):
            continue
        lv = max(graded, key=lambda r: rank[r["level"]])["level"] if graded else "tt"
        note = getattr(P, "AREA_NOTES", {}).get(area) or "; ".join(
            f'{r["label"]}: {r["value"]}' for r in rs if r["level"] in ("vua", "kem") or (r["level"] == "tt" and r["value"])) or "Đạt"
        t, c = C.LEVELS[lv]
        rows.append(f'<tr class="row"><td><b>{e(area)}</b></td><td><span class="badge" style="--c:{c}">{t}</span></td><td>{e(note)}</td></tr>')
    sec(None, "Đánh giá theo mảng", '<table><thead><tr><th>Mảng</th><th>Mức</th><th>Nhận xét</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")

    # B3 danh mục việc
    tk = tasks()
    tong_viec = sum(t["hours"] for _g, rs in tk for t in rs)
    o = [f'<p class="lead">{sum(len(rs) for _g, rs in tk)} việc, tổng {g(tong_viec)} giờ công Viindoo. Mỗi việc ghi phần doanh nghiệp làm và phần Viindoo làm.</p>',
         '<table class="viec"><colgroup><col style="width:46px"><col style="width:14%"><col style="width:84px"><col style="width:20%"><col><col><col style="width:50px"></colgroup>'
         "<thead><tr><th>Mã</th><th>Việc</th><th>Loại</th><th>Hiện trạng</th><th>Doanh nghiệp làm</th><th>Viindoo làm</th><th>Giờ</th></tr></thead><tbody>"]
    for grp, rs in tk:
        o.append(f'<tr class="grp"><td colspan="6">{e(grp["code"])}. {e(grp["name"])} ({e(P.PACKAGE_NAMES.get(grp["package"], ""))})</td>'
                 f'<td class="n">{g(sum(t["hours"] for t in rs))}</td></tr>')
        for t in rs:
            o.append(f'<tr class="row"><td class="code">{e(t["code"])}</td><td><b>{e(t["name"])}</b></td>'
                     f'<td><span class="badge" style="--c:{LOAI_MAU.get(t["type"], "#8F8F8F")}">{e(t["type"])}</span></td>'
                     f'<td>{e(current_text(t, res_by_id))}</td><td>{common.ul(t["customer"])}</td><td>{common.ul(t["viindoo"])}</td><td class="n">{g(t["hours"])}</td></tr>')
    o.append(f'<tr class="grp"><td colspan="6">Tổng</td><td class="n">{g(tong_viec)}</td></tr></tbody></table>')
    sec("B. DANH MỤC VIỆC CẦN LÀM", "Danh mục việc thiết lập và chuẩn hoá dữ liệu", "".join(o))

    # C4 kế hoạch
    items = [r for r in P.PLAN if r[0] == "item"]
    tong = sum(item_hours(r[4]) for r in items)
    nw = max(max(weeks(r[3]) or {0}) for r in items)
    ph_h, cur = {}, None
    for r in P.PLAN:
        if r[0] == "phase":
            cur = r[1]
            ph_h[cur] = 0
        elif r[0] == "item":
            ph_h[cur] += item_hours(r[4])
    o = ['<ul class="plan-list">',
         f'<li><strong>Tổng thời gian dự kiến:</strong> {nw} tuần, tuần 1 bắt đầu {week_start(1).strftime("%d/%m/%Y")}; tổng {g(tong)} giờ công.</li>']
    o += [f"<li><strong>{e(k)}:</strong> {e(v)}</li>" for k, v in getattr(P, "SCOPE", [])]
    o.append("</ul>")
    o.append('<div class="scroll"><table class="gantt-table"><thead><tr><th>Nội dung công việc</th><th>Thời lượng</th>'
             + "".join(f"<th>{i}<small>{week_start(i).strftime('%d/%m')}</small></th>" for i in range(1, nw + 1)) + "</tr></thead><tbody>")
    for kind, ma, viec, tuan, h, _kq in P.PLAN:
        if kind == "phase":
            o.append(f'<tr class="phase"><td>{e(viec)}</td><td class="hrs">{g(ph_h[ma])}h</td><td colspan="{nw}"></td></tr>')
        elif kind == "sub":
            o.append(f'<tr class="sub"><td colspan="{nw + 2}">{e(viec)}</td></tr>')
        else:
            ws = weeks(tuan)
            o.append(f'<tr><td class="label"><b>{e(ma)}</b>{e(viec)}</td><td class="hrs">{g(item_hours(h))}h</td>'
                     + "".join(f'<td class="{"wk" if i in ws else ""}"></td>' for i in range(1, nw + 1)) + "</tr>")
    o.append(f'<tr class="total"><td>TỔNG</td><td class="hrs">{g(tong)}h</td><td colspan="{nw}"></td></tr></tbody></table></div>')
    o.append('<p class="price-note">Kế hoạch dự kiến; hai bên cân đối lại phạm vi, giờ công và tiến độ khi có đủ thông tin, dữ liệu doanh nghiệp gửi.</p>')
    sec("C. KẾ HOẠCH CHI TIẾT", "Kế hoạch triển khai dự kiến", "".join(o))

    pr = processes()
    if pr:
        sec(None, "Bộ quy trình ứng dụng",
            f'<p class="lead">{len(pr)} quy trình xếp theo dòng chảy chứng từ. Mỗi quy trình gồm sơ đồ theo vị trí và các bước trên Viindoo; là nền của đào tạo.</p>'
            '<table class="kh"><thead><tr><th>Mã</th><th>Quy trình</th><th>Vị trí tham gia</th><th>Gói</th></tr></thead><tbody>'
            + "".join(f'<tr class="row"><td class="code">{e(c)}</td><td>{e(t)}</td><td>{e(v)}</td><td class="n">{e(pk)}</td></tr>' for c, t, pk, v in pr)
            + "</tbody></table>")
    sec(None, "Chương trình đào tạo theo mảng nghiệp vụ",
        f'<p class="lead">Đào tạo theo quy trình, thực hành trên dữ liệu thật; học xong một mảng mới sang mảng sau, theo thứ tự dòng chảy chứng từ. '
        f'Tối đa {P.TRAINING_RULE["per_week"]} buổi mỗi tuần, mỗi buổi {P.TRAINING_RULE["min_hours"]}-{P.TRAINING_RULE["max_hours"]} giờ. '
        f'Tổng {g(sum(t["hours"] for t in P.TRAINING))} giờ.</p>'
        '<table class="kh"><thead><tr><th>Gói</th><th>Mảng</th><th>Người học</th><th>Quy trình</th><th>Nội dung</th><th>Giờ</th><th>Bài thực hành</th></tr></thead><tbody>'
        + "".join(f'<tr class="row"><td class="n">{t["package"]}</td><td><b>{e(t["area"])}</b></td><td>{e(t["positions"])}</td><td>{e(t["processes"])}</td>'
                  f'<td>{e(t["content"])}</td><td class="n">{g(t["hours"])}</td><td>{e(t["exercise"])}</td></tr>' for t in P.TRAINING)
        + "</tbody></table>")
    sec(None, "Thông tin, dữ liệu doanh nghiệp cần gửi",
        '<ul class="kv">' + "".join(f"<li>{e(('Gói ' + str(pk) + ', ') if pk else '')}{e(('tuần ' + w + ': ') if w else '')}{e(x)}</li>"
                                    for pk, x, w in P.CUSTOMER_INPUTS) + "</ul>")
    sec(None, "Nhân sự triển khai phía Viindoo",
        '<div class="ns">' + "".join(
            f'<div class="card"><div class="av">{e("".join(w[0] for w in s["name"].split()[-2:]) if s["name"][:1] != "<" else "V")}</div><div>'
            f'<span class="lab">{e(s["role"])}</span><b class="n">{e(s["name"])}</b><i>{e(s["title"])}</i>'
            + (f'<p>{e(s["intro"])}</p>' if s.get("intro") else "")
            + f'<div class="ct"><span>Điện thoại: <b>{e(s["phone"])}</b></span><span>Email: <b>{e(s["email"])}</b></span></div></div></div>'
            for s in P.STAFF) + "</div>")

    title = f"{P.SHORT_NAME} - Báo cáo đánh giá hiện trạng và kế hoạch triển khai"
    sub = f"{e(P.CUSTOMER)} · Viindoo {e(P.VERSION)} · Lập ngày {e(P.DATE)} · Ngày chốt số dư {e(P.OPENING_DATE)}"
    css = """
.ns{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ns .card{display:flex;gap:14px;border:1px solid #dcdcdc;border-left:5px solid var(--pri);border-radius:10px;padding:14px 16px;background:#fff;break-inside:avoid}
.ns .av{width:64px;height:64px;border-radius:50%;flex:0 0 64px;background:var(--bg2);color:var(--sec);font:700 22px Montserrat,Arial,sans-serif;display:flex;align-items:center;justify-content:center}
.ns .lab{display:block;font:600 11.5px Roboto,Arial,sans-serif;color:var(--sec);text-transform:uppercase;letter-spacing:.05em}
.ns b.n{display:block;font:700 16px Montserrat,Arial,sans-serif;color:var(--h)}
.ns i{display:block;color:var(--mut);font-size:13.5px}
.ns .ct span{display:block;font-size:13.5px}
td small{color:var(--mut)}
@media (max-width:700px){.ns{grid-template-columns:1fr}}
"""
    doc = common.page(title, "Báo cáo đánh giá hiện trạng và kế hoạch triển khai", sub, "".join(body), css, "".join(toc))
    out = common.out_dir() / f"{title}.html"
    errs = common.check_text(doc, out.name)
    if errs:
        raise SystemExit("\n".join(errs))
    common.write(out, doc)
    soat = common.vdoc().kiem_ban_gui_khach(str(out))
    print(out)
    print(common.vdoc().in_ket_qua_soat(soat))
    if any(x["muc"] == "cam" for x in soat):
        raise SystemExit("Bản gửi khách còn từ chỉ cách tính giá nội bộ - sửa trước khi gửi")
    if not A.no_pdf:
        chrome_headless.print_pdf(out, out.with_suffix(".pdf"))
        print(out.with_suffix(".pdf"))
    ky = getattr(P, "SIGNED_HOURS", None)
    print(f"Tổng giờ kế hoạch {g(tong)}" + (f" / giờ trong gói đã ký {g(ky)}" + (" - VƯỢT GÓI, chủ nhiệm dự án phải quyết trước khi gửi" if tong > ky else "") if ky else ""))


if __name__ == "__main__":
    build()
