# -*- coding: utf-8 -*-
"""Dựng '<Khách> - Quy trình ứng dụng Viindoo.html' (+ PDF) từ handbook.py trong thư mục dữ liệu dự án.

Trước khi dựng: kiểm ma trận phân quyền (permission_check), đồ thị sơ đồ (bpmn_engine.kiem_do_thi), hình học từng hình
(bpmn_geometry_check) và đường dẫn tài liệu hướng dẫn (doc_link_check, ngoại tuyến); lỗi nào cũng dừng.
Chạy: python3 build_handbook_html.py --data <thư mục dữ liệu dự án> [--out <thư mục ra>]
PDF in bằng Chrome for Testing (chrome_headless.py), không đụng Chrome của người dùng.
"""
import html
import json
import re

import common

if __name__ == "__main__":
    common.cli("Dựng bộ quy trình ứng dụng Viindoo (HTML + PDF)")

import bpmn_engine as B  # noqa: E402
import chrome_headless  # noqa: E402
import doc_link_check  # noqa: E402
import permission_check as phan_quyen_kiem  # noqa: E402

D = common.load("handbook")
OUT = common.out_dir() / f"{getattr(D, 'KHACH_NGAN', D.KHACH)} - Quy trình ứng dụng Viindoo.html"
NEN = {}   # mã quy trình -> mức nén bảng bước (1, 2) để phần đuôi bảng không tràn sang một trang gần trống


def e(s):
    return html.escape(str(s), quote=False)


def all_procs():
    """Quy trình theo gói và các quy trình con dùng chung (PD phê duyệt, DT tạo đối tác) nếu dự án có."""
    return D.QUY_TRINH + [x for x in (getattr(D, "PD", None), getattr(D, "DT", None)) if x]


def doc_link(key):
    if not key:
        return "-"
    path, ten = D.TRANG[key]
    return f'<a href="{D.DOC_BASE}{path}.html">{e(ten)}</a>'


CONTENT_W = 1030      # bề rộng nội dung khi in A4 ngang (px CSS)
FONT_LOG = []         # (mã, tên hình, cỡ chữ nhỏ nhất pt) để báo cáo


def tl(key):
    """Dòng 'Tài liệu hướng dẫn' của một mục: liên kết tới các trang tài liệu Viindoo 19 khai ở D.TAI_LIEU."""
    ks = D.TAI_LIEU.get(key, [])
    if not ks:
        return ""
    return '<p class="tl">Tài liệu hướng dẫn: ' + " · ".join(f'<a href="{D.DOC_BASE}{D.TRANG[k][0]}.html">{e(D.TRANG[k][1])}</a>' for k in ks) + "</p>"


def legend_html(syms):
    """Một chú giải cho cả quy trình (các ký hiệu có trong mọi hình của quy trình), đặt dưới hình cuối."""
    lg = "".join(f"<li>{B.ky_hieu_svg(k)}<span>{e(t)}</span></li>" for k, t in B.chu_giai(syms))
    return f'<div class="lg-box"><b>Chú giải ký hiệu trong sơ đồ</b><ul class="lg">{lg}</ul></div>'


def figure_html(q, f, avail_h):
    """Một hình: tỉ lệ in = min(1, bề rộng trang, chiều cao còn lại); trả HTML và tỉ lệ."""
    sc = min(0.8, CONTENT_W / f["w"])  # hình rộng <= B.MAX_W_HTML nên tỉ lệ >= 0,78 -> chữ nhỏ nhất >= 7pt
    svg = f["svg"].replace('<svg class="bpmn"', f'<svg class="bpmn" style="width:{f["w"] * sc:.0f}px;max-width:100%;height:auto"', 1)
    ph = f" (phần {f['phan']}/{f['tong']})" if f["tong"] > 1 else ""
    FONT_LOG.append((q["code"], f["ten"] + ph, round(B.font_min_pt(sc), 1)))
    return f'<figure>{svg}<figcaption><b>Sơ đồ {q["code"]} - {e(f["ten"])}{ph}.</b></figcaption></figure>', sc


def steps_table(q):
    s = q["buoc"]
    out = [f'<table class="buoc nen{NEN.get(q["code"], 0)}"><colgroup><col style="width:5%"><col style="width:11%"><col style="width:16%"><col style="width:30%">'
           '<col style="width:14%"><col style="width:10%"><col style="width:14%"></colgroup>'
           "<thead><tr><th>Bước</th><th>Vị trí</th><th>Việc</th><th>Thao tác trên Viindoo</th><th>Ngoài phần mềm</th>"
           "<th>Chuyển cho</th><th>Tài liệu hướng dẫn</th></tr></thead><tbody>"]
    hd = D.HUONG_DAN[q["code"]]
    kinds = B.step_kinds(q)
    dks = B.nhan_dieu_kien(q)
    cc = B.chuyen_cho(q)
    for k, (v, nv, vd, ngoai) in enumerate(s):
        dk = dks.get(k + 1)
        loai, them = kinds[k]
        ic = B.icon_svg(loai) + (B.icon_svg("manual") if them else "")
        tag = f'<span class="tag">{e(dk)}</span>' if dk else ""
        out.append(f'<tr><td class="n">{k + 1}<br>{ic}</td><td><b>{e(v)}</b></td><td>{e(nv)}{tag}</td><td>{e(vd)}</td><td>{e(ngoai)}</td>'
                   f"<td>{e(cc.get(k + 1, '-')).replace('; ', ';<br>')}</td><td>{doc_link(hd[k])}</td></tr>")
    out.append("</tbody></table>")
    return "".join(out)


def proc(q, truoc=""):
    """Tiêu đề + hình đầu giữ chung một khối (không để trang chỉ có tiêu đề); hình tiếp theo; rồi mục tiêu và bảng bước."""
    figs = B.figures(q, B.MAX_W_HTML)
    meta = ['<table class="meta"><tbody>',
            f'<tr><th>Mục tiêu</th><td>{e(q["muc_tieu"])}</td></tr>',
            f'<tr><th>Bắt đầu</th><td>{e(q["bat_dau"])}</td></tr>',
            f'<tr><th>Kết thúc</th><td>{e(q["ket_thuc"])}</td></tr>',
            f'<tr><th>Luồng chứng từ</th><td>{e(q["luong"])}</td></tr>']
    for t in q.get("luu_y", []):
        meta.append(f'<tr><th>Lưu ý</th><td>{e(t)}</td></tr>')
    meta.append("</tbody></table>")
    out = [f'<section class="qt" id="{q["code"]}"><div class="head-blk">{truoc}<h3><span class="code">{q["code"]}</span> {e(q["ten"])}</h3>{tl(q["code"])}'
           + figure_html(q, figs[0], 470 if truoc else 540)[0] + "</div>"]
    for f in figs[1:]:
        out.append(figure_html(q, f, 600)[0])
    out.append(legend_html(set().union(*(f["syms"] for f in figs))))
    out.append("".join(meta) + steps_table(q) + "</section>")
    return "".join(out)


def matrix():
    vt = D.VT_MT
    out = ['<table class="mtx"><colgroup><col style="width:12%">' + '<col>' * len(vt) + "</colgroup><thead><tr><th>Ứng dụng</th>"
           + "".join(f"<th>{e(v)}</th>" for v in vt) + "</tr></thead><tbody>"]
    for cum, rows in D.MA_TRAN:
        out.append(f'<tr class="grp"><td colspan="{len(vt) + 1}">{e(cum)}</td></tr>')
        for muc, nhom_dau, vals in rows:
            ten = f"<b>{e(muc)}</b>" + (f'<br><span class="nd">{e(nhom_dau)}</span>' if nhom_dau else "")
            cells = "".join(f'<td class="{"no" if x == "-" else ""}">{e(x)}</td>' for x in vals)
            out.append(f"<tr><td>{ten}</td>{cells}</tr>")
    out.append("</tbody></table>")
    return "".join(out)


EXTRA_CSS = """

table.kd{table-layout:fixed;font-size:12px}
table.kd td{word-break:break-word;padding:5px 6px}
table.kd th{font-size:12px;padding:6px}
.dg{display:inline-block;border-radius:5px;padding:1px 5px;font-size:10.5px;font-weight:600;line-height:1.3;max-width:100%}
.dg.vt{background:#E6F8FA;color:#007F8C;border:1px solid #00BBCE}
.dg.ng{background:#F2F2F2;color:#555;border:1px solid #cfcfcf}
.tag2{display:inline-block;border:1px solid var(--sec);color:var(--sec);border-radius:5px;font-size:10.5px;padding:0 5px;margin-left:4px}
@page{size:A4 landscape}
.wrap{max-width:1180px}
.code{display:inline-block;background:var(--sec);color:#fff;border-radius:6px;padding:1px 8px;font-size:.85em;margin-right:6px}
section.qt{padding:14px 0 6px}
section.qt h3{font-size:18px;margin:0 0 10px;border-left:4px solid var(--pri);padding-left:10px}
table.meta th{width:150px;background:#F7F7F7;color:var(--h);border:1px solid #e3e3e3;border-bottom:1px solid #e3e3e3;font-weight:600}
table.meta{font-size:13.5px;break-inside:avoid;page-break-inside:avoid}
table.buoc thead{break-after:avoid;page-break-after:avoid}
figure{margin:4px 0 8px;break-inside:avoid}
figcaption{font-size:10px;color:#6B6D70;line-height:1.3}
.lg-box{margin:2px 0 10px;padding:4px 8px;border:1px solid #E3E5E8;border-radius:4px;break-inside:avoid;font-size:11px;color:#21272B}
ul.lg{list-style:none;margin:3px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px 12px}
ul.lg li{display:flex;align-items:center;gap:5px;font-size:10px;color:#6B6D70;break-inside:avoid}
ul.lg svg.kh{flex:none;width:34px;height:20px}
@media screen and (max-width:800px){ul.lg{grid-template-columns:repeat(2,minmax(0,1fr))}}
.head-blk{break-inside:avoid}
figure svg{break-inside:avoid}
table.buoc td.n{text-align:center}
figcaption{break-before:avoid}
p.tl{font-size:12px;color:#6B6D70;margin:-4px 0 8px;break-after:avoid;page-break-after:avoid}
p.tl a{color:#007F8C}
h3,h4{break-after:avoid;page-break-after:avoid}
table.cg{font-size:12.5px}table.cg td,table.cg th{padding:4px 8px}
figure svg.bpmn{display:block;margin:0 auto 6px}
svg.ic{vertical-align:-2px;margin:2px 1px 0 0}
.legend-box{background:#FAFAFA;border:1px solid #e3e3e3;border-radius:8px;padding:10px 14px;margin:10px 0 4px;font-size:13px}
.legend-box svg.legend-bpmn{width:100%;max-width:980px;height:auto;display:block;margin:6px 0}
.legend-box p{margin:4px 0 0}
figcaption{font-size:12px;color:var(--mut);margin-top:4px}
svg text.ln{font:600 11.5px Roboto,Arial,sans-serif;fill:#21272B}
svg text.bx{font:11px Roboto,Arial,sans-serif;fill:#282F33;text-anchor:middle}
svg text.dk{font:italic 600 10px Roboto,Arial,sans-serif;fill:#7F4282;text-anchor:middle}
table.buoc,table.mtx{table-layout:fixed;font-size:12.5px}
table.buoc td,table.mtx td{word-break:break-word;padding:5px 7px}
table.buoc th,table.mtx th{padding:6px 7px;font-size:12.5px}
tr{break-inside:avoid}
table.nen1{font-size:11.5px}table.nen1 td{padding:3px 6px;line-height:1.35}
table.nen2{font-size:11px}table.nen2 td{padding:2px 6px;line-height:1.3}
table.buoc tbody tr:nth-last-child(2),table.kd tbody tr:nth-last-child(2){break-after:avoid;page-break-after:avoid}
thead{display:table-header-group}
.ck{display:block;white-space:nowrap;font-size:12px}
.tag{display:block;margin-top:3px;color:var(--sec);font-size:11.5px;font-style:italic}
table.mtx{font-size:11px;line-height:1.25;margin:4px 0 8px}
table.mtx td{text-align:center;font-size:10px;padding:1px 4px;line-height:1.2}
table.mtx tr.grp,table.kd tr.grp{break-after:avoid;page-break-after:avoid}
table.mtx th{font-size:11px;padding:4px 5px;line-height:1.25}
table.mtx tr.grp td{font-size:11.5px;padding:2px 8px}
table.mtx td:first-child{text-align:left}
table.mtx .nd{font-weight:400;font-size:10px;color:#6B6D70}
ul.kv.nho>li{font-size:12.5px;padding:1px 0 1px 16px}
table.mtx td.no{color:#b3b3b3}
table.mtx tr.xn td{background:#FAFAFA}
table.mtx tr.xn .ck{display:block;font-size:11px}
section.mtx-sec .lead{margin-bottom:6px}
.toc ul{list-style:none;margin:6px 0 0;padding:0;columns:3 !important;column-gap:28px}
.toc li{padding:2px 0;font-size:14px}.toc li.p{font:600 13px Montserrat,Arial,sans-serif;color:var(--sec);margin-top:6px}
ul.kv>li{font-size:14px}
section.mtx-sec{break-before:page}
.mtx-trang{break-before:page;page-break-before:always}
section.pd-sec{break-before:page}
section.vt-sec{break-before:page}
h2.phan{break-before:page}
section.pd-sec figure{break-inside:avoid}
.head-blk h2.phan{break-before:avoid;margin-top:0}
.head-blk:has(h2.phan){break-before:page}
.head-blk .legend-box{margin:6px 0 8px;padding:4px 10px;display:flex;align-items:center;gap:12px}
.head-blk .legend-box svg.legend-bpmn{width:78%;margin:0}
.head-blk h2.phan{padding:6px 14px;font-size:15px}
.head-blk table.meta td,.head-blk table.meta th{padding:4px 8px}
@media (max-width:800px){.toc ul{columns:1}.scroll{overflow-x:auto}}
"""


def build():
    loi = phan_quyen_kiem.kiem() + phan_quyen_kiem.kiem_phoi_hop() + doc_link_check.kiem()
    loi += [x for q in all_procs() for x in B.kiem_do_thi(q)]
    if loi:
        raise SystemExit("Ma trận phân quyền, đường dẫn tài liệu hoặc sơ đồ sai:\n" + "\n".join(loi))
    hinh = [x for q in all_procs() for x in B.kiem_hinh(q, B.MAX_W_HTML)]
    if hinh:
        raise SystemExit("Sơ đồ lỗi hình học (qtud_kiem_hinh: MUI, SONG, LAN, O, NHAN, CHAM, CONG, BE; hoặc không tìm được đường):\n" + "\n".join(hinh))
    ul = lambda xs: '<ul class="kv">' + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"  # noqa: E731

    toc, body = [], []
    n = 0

    def sec(title, inner, cls="", tai_lieu=""):
        nonlocal n
        n += 1
        toc.append(f'<li><a href="#m{n}">{n}. {e(title)}</a></li>')
        body.append(f'<section id="m{n}" class="{cls}"><h2>{n}. {e(title)}</h2>{tl(tai_lieu)}{inner}</section>')

    pd_html = dt_html = ""
    if getattr(D, "PD", None):
        figs = B.figures(D.PD, B.MAX_W_HTML)
        pdf_ = [figure_html(D.PD, f, 600)[0] for f in figs]
        pd_html = (f'<div class="head-blk"><h3 id="PD">PD - {e(D.PD["ten"])}</h3>{tl("PD")}{pdf_[0]}</div>' + "".join(pdf_[1:])
                   + legend_html(set().union(*(f["syms"] for f in figs))) + steps_table(D.PD))
    if getattr(D, "DT", None):
        figs = B.figures(D.DT, B.MAX_W_HTML)
        dtf = [figure_html(D.DT, f, 600)[0] for f in figs]
        dt_html = (f'<div class="head-blk"><h3 id="DT">DT - {e(D.DT["ten"])} <span style="font-weight:400;font-size:12.5px">- '
                   + e(getattr(D, "DT_MO_TA", "quy trình con dùng chung khi cần đối tác chưa có trên hệ thống"))
                   + f'</span></h3>{tl("DT")}{dtf[0]}</div>' + "".join(dtf[1:])
                   + legend_html(set().union(*(f["syms"] for f in figs))) + steps_table(D.DT))
    sec("Ma trận phân quyền theo vị trí",
        '<h3>Vị trí công việc và việc chính</h3>'
        '<table><colgroup><col style="width:28%"><col></colgroup><thead><tr><th>Vị trí công việc</th><th>Việc chính trên Viindoo</th></tr></thead><tbody>'
        + "".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>" for a, b in D.VI_TRI) + "</tbody></table>"
        + f'<div class="scroll mtx-trang"><h3>Ma trận phân quyền</h3>{matrix()}</div>' + ul(D.GHI_CHU_MT).replace('class="kv"', 'class="kv nho"')
        + "<h3>Nguyên tắc gán quyền theo vị trí</h3>" + ul(D.NGUYEN_TAC)
        + "<h3>Quy tắc giới hạn dữ liệu</h3>" + ul(D.GIOI_HAN)
        + '<h3>Chú giải cấp nhóm quyền</h3><table class="cg"><colgroup><col style="width:18%"><col></colgroup>'
        "<thead><tr><th>Mục trên phần mềm</th><th>Các cấp (cấp sau gồm quyền của cấp trước)</th></tr></thead><tbody>"
        + "".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td></tr>" for a, b in D.CHU_GIAI) + "</tbody></table>",
        "vt-sec", "ma_tran")
    sec("Quy tắc phê duyệt", ul(D.PHE_DUYET) + pd_html, "pd-sec", "phe_duyet")
    goi2 = lambda g: ' <span class="tag2">Gói 2</span>' if g == 2 else ""  # noqa: E731
    a_rows = "".join(
        f"<tr><td><b>{e(a)}</b>{goi2(g)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td><td>{e(k)}</td><td>{e(t)}</td><td>{e(h)}</td></tr>"
        for a, b, c, d, k, t, h, g in D.CHOT_CHAN)
    b_rows = []
    for ts, items in D.RA_SOAT:
        b_rows.append(f'<tr class="grp"><td colspan="5">{e(ts)}</td></tr>')
        b_rows += [f"<tr><td><b>{e(v)}</b>{goi2(g)}</td><td>{e(l)}</td><td>{e(w)}</td><td>{e(x)}</td><td>{e(c)}</td></tr>"
                   for v, l, w, x, c, g in items]
    sec("Kiểm soát dữ liệu: chốt chặn khi nhập, rà soát định kỳ, phối hợp khi cần tạo mới",
        '<p class="lead">Mục đích: dữ liệu nhập lên đủ và sạch. Mỗi chốt chặn gắn với một vị trí nhập, một vị trí kiểm tra; '
        'cột Hệ thống hỗ trợ ghi điều người dùng thấy trên phần mềm khi nhập. '
        + e(getattr(D, "KIEM_SOAT_NGUOI", "")) + "</p>"
        "<h3>A. Chốt chặn khi nhập</h3>" + tl("chot_chan") +
        '<table class="kd"><colgroup><col style="width:12%"><col style="width:10%"><col style="width:21%"><col style="width:10%"><col style="width:15%">'
        '<col style="width:11%"><col style="width:21%"></colgroup>'
        "<thead><tr><th>Loại dữ liệu</th><th>Vị trí nhập</th><th>Thông tin bắt buộc / điều kiện</th><th>Vị trí kiểm tra</th><th>Kiểm tra những gì</th>"
        "<th>Thời điểm</th><th>Hệ thống hỗ trợ</th></tr></thead><tbody>" + a_rows + "</tbody></table>"
        "<h3>B. Bảng kiểm định kỳ</h3>" + tl("ra_soat") +
        f'<p style="font-size:13px">{e(D.NHAC_DINH_KY)}</p>'
        '<table class="kd"><colgroup><col style="width:23%"><col style="width:12%"><col style="width:33%"><col style="width:19%"><col style="width:13%">'
        '</colgroup>'
        "<thead><tr><th>Việc rà soát</th><th>Vị trí làm</th><th>Xem ở đâu trên Viindoo</th><th>Xử lý khi phát hiện</th><th>Vị trí xác nhận</th>"
        "</tr></thead><tbody>" + "".join(b_rows) + "</tbody></table>"
        "<h3>C. Phối hợp khi cần tạo mới (sản phẩm, nhóm sản phẩm, bảng giá, điều khoản thanh toán...)</h3>" + tl("phoi_hop")
        + ul(D.PHOI_HOP_CACH)
        + '<table class="kd"><colgroup><col style="width:13%"><col style="width:16%"><col style="width:18%"><col style="width:14%">'
        '<col style="width:22%"><col style="width:17%"></colgroup>'
        "<thead><tr><th>Cần tạo mới</th><th>Vị trí thường cần</th><th>Vị trí có quyền tạo (theo ma trận)</th><th>Gửi yêu cầu cho</th>"
        "<th>Thông tin phải gửi kèm</th><th>Lưu ý</th></tr></thead><tbody>"
        + "".join(f"<tr><td><b>{e(t)}</b></td><td>{e(c)}</td><td>{e('; '.join(phan_quyen_kiem.ai_co_quyen(q)))}</td><td><b>{e(n)}</b></td>"
                  f"<td>{e(tt)}</td><td>{e(lu)}</td></tr>" for t, c, n, tt, lu, q in D.PHOI_HOP)
        + "</tbody></table>" + dt_html, "mtx-sec", "kiem_soat")

    for g in sorted({q["goi"] for q in D.QUY_TRINH}):
        n += 1
        qs = [q for q in D.QUY_TRINH if q["goi"] == g]
        toc.append(f'<li class="p"><a href="#m{n}">{n}. Quy trình {e(D.GOI_TEN[g])}</a></li>')
        toc += [f'<li><a href="#{q["code"]}">{q["code"]} {e(q["ten"])}</a></li>' for q in qs]
        leg = ""  # chú giải đầy đủ đã có dưới từng hình
        h2 = f'<h2 class="phan" id="m{n}">{n}. Quy trình {e(D.GOI_TEN[g])}</h2>' + leg
        body.append("".join(proc(q, h2 if j == 0 else "") for j, q in enumerate(qs)))

    intro = ('<p class="lead" style="margin-top:18px">Mỗi quy trình gồm sơ đồ chia làn theo vị trí và bảng các bước. Mỗi dòng là một bước '
             "do một vị trí làm: làm gì, vào menu nào trên Viindoo, bấm nút nào, nhập ô nào, chứng từ chuyển cho ai tiếp theo. Cột Tài liệu hướng dẫn "
             "dẫn tới trang hướng dẫn tương ứng trên tài liệu Viindoo.</p>")
    sub = f"{e(D.KHACH)} · Ngày lập {e(D.NGAY)}" + (f" · Căn cứ: {e(D.CAN_CU)}" if getattr(D, "CAN_CU", "") else "")
    doc = common.page(f"{getattr(D, 'KHACH_NGAN', D.KHACH)} - Quy trình ứng dụng Viindoo", "Quy trình ứng dụng Viindoo", sub,
                      "".join(body), EXTRA_CSS, "".join(toc), intro=intro)
    sai = common.check_text(doc, OUT.name, ban_words=("AI", "Odoo"))
    if sai:
        raise SystemExit("\n".join(sai))
    OUT.write_text(doc, encoding="utf-8")
    pdf = OUT.with_suffix(".pdf")
    chrome_headless.print_pdf(OUT, pdf)
    print(OUT, pdf, "| quy trình:", len(D.QUY_TRINH), "| bước:", sum(len(q["buoc"]) for q in D.QUY_TRINH))
    (common.work_dir() / "handbook_font_html.json").write_text(json.dumps(FONT_LOG, ensure_ascii=False, indent=0), encoding="utf-8")


def trang_thua(pdf):
    """Mã quy trình có đuôi bảng bước tràn sang một trang gần trống (dưới 12 dòng chữ, không có sơ đồ)."""
    import subprocess
    pages = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout.split("\f")[:-1]
    out, code = set(), None
    for p in pages:
        caps = re.findall(r"Sơ đồ (QT\d\d|PD|DT) - ", p)
        ls = [x for x in p.splitlines() if x.strip() and not x.strip().startswith("Trang ")]
        if not caps and code and len(ls) < 12 and re.match(r"\s*(Bước\s|\d+\s)", ls[0] if ls else ""):
            out.add(code)
        if caps:
            code = caps[-1]
    return out


if __name__ == "__main__":
    build()
    for _ in range(2):   # nén dần bảng của quy trình còn tràn
        thua = trang_thua(OUT.with_suffix(".pdf"))
        if not thua:
            break
        for c in thua:
            NEN[c] = min(2, NEN.get(c, 0) + 1)
        FONT_LOG.clear()
        build()
