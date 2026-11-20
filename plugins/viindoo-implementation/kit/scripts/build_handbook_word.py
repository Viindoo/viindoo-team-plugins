# -*- coding: utf-8 -*-
"""Dựng '<Khách> - Quy trình ứng dụng Viindoo.docx' (bản Word, khổ A4 ngang) từ handbook.py trong thư mục dữ liệu dự án.

Khuôn Word (kiểu chữ, đầu trang logo Viindoo, chân trang số trang): kit/assets/handbook-template.docx.
Sơ đồ: SVG của bpmn_engine chụp thành PNG bằng Chrome for Testing; kiểm cỡ chữ in >= 7pt và chiều cao hình vừa trang.
Chạy: python3 build_handbook_word.py --data <thư mục dữ liệu dự án> [--out <thư mục ra>]
"""
import json
import os

import common

if __name__ == "__main__":
    common.cli("Dựng bộ quy trình ứng dụng Viindoo (Word)")

from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402

import bpmn_engine as B  # noqa: E402
import doc_link_check  # noqa: E402
import permission_check as phan_quyen_kiem  # noqa: E402
import word_helpers as qtud_word  # noqa: E402
from word_helpers import P, clear_body, hyperlink, label, picture, shade, table  # noqa: E402

D = common.load("handbook")
TRANG_W = 27.2   # bề rộng phần nội dung (cm): A4 ngang 29,7 trừ lề 1,25 mỗi bên
qtud_word.W_SCALE = TRANG_W / 23.9   # các bảng khai bề rộng theo khổ 23,9cm, nới đều theo khổ A4 ngang

TEMPLATE = str(common.ASSETS / "handbook-template.docx")
OUT = str(common.out_dir() / f"{getattr(D, 'KHACH_NGAN', D.KHACH)} - Quy trình ứng dụng Viindoo.docx")
IMG = str(common.work_dir() / "handbook_img")


def all_procs():
    return D.QUY_TRINH + [x for x in (getattr(D, "PD", None), getattr(D, "DT", None)) if x]


# ---------------------------------------------------------------- bảng bước
def legend_table(doc, items, ncol=4):
    """Chú giải dạng bảng nhỏ không viền: mỗi mục hai ô (biểu tượng | một câu), căn giữa theo chiều dọc, chữ 7,5pt màu ghi."""
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
    rows = (len(items) + ncol - 1) // ncol
    t = doc.add_table(rows=rows, cols=ncol * 2)
    t.autofit = False
    w_ic, w_tx = 1.3, TRANG_W / ncol - 1.3
    for row in t.rows:
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for n_, cell in enumerate(row.cells):   # cả chú giải nằm chung một trang
            cell.width = Cm(w_ic if n_ % 2 == 0 else w_tx)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            pf = cell.paragraphs[0].paragraph_format
            pf.keep_with_next = row is not t.rows[-1]
            pf.space_after = pf.space_before = Pt(1)
    for gc, n_ in zip(t._tbl.tblGrid.findall(qtud_word.qn("w:gridCol")), range(ncol * 2)):
        gc.set(qtud_word.qn("w:w"), str(int((w_ic if n_ % 2 == 0 else w_tx) * 567)))
    for j, (k, txt) in enumerate(items):
        c1, c2 = t.rows[j // ncol].cells[(j % ncol) * 2], t.rows[j // ncol].cells[(j % ncol) * 2 + 1]
        mar = OxmlElement("w:tcMar")   # ô biểu tượng không lề để ảnh không bị cắt
        for side in ("top", "left", "bottom", "right"):
            m_ = OxmlElement(f"w:{side}")
            m_.set(qtud_word.qn("w:w"), "40")
            m_.set(qtud_word.qn("w:type"), "dxa")
            mar.append(m_)
        c1._tc.get_or_add_tcPr().append(mar)
        c1.paragraphs[0].add_run().add_picture(icon_png(k), width=Cm(0.85))  # 34px -> 0,85cm, vừa ô 1,3cm
        r = c2.paragraphs[0].add_run(txt)
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(0x6B, 0x6D, 0x70)
    P(doc)


_ICON = {}


def icon_png(k):
    if k not in _ICON:
        os.makedirs(IMG, exist_ok=True)
        path = os.path.join(IMG, f"ky_hieu_{k}.png")
        B.export_png(B.ky_hieu_svg(k), 34, 20, path)
        _ICON[k] = path
    return _ICON[k]


ANH_CAO_TOI_DA = 14.7   # cm: phần cao còn dùng được dưới logo đầu trang, sau khi trừ tiêu đề quy trình và tên hình
def tl(doc, key):
    """Dòng 'Tài liệu hướng dẫn' dưới tiêu đề mục: liên kết tới trang tài liệu Viindoo 19 khai ở D.TAI_LIEU."""
    ks = D.TAI_LIEU.get(key, [])
    if not ks:
        return
    p = P(doc, style="Body Text")
    r = p.add_run("Tài liệu hướng dẫn: ")
    r.font.size = Pt(8.5)
    for n_, k in enumerate(ks):
        if n_:
            p.add_run(" · ").font.size = Pt(8.5)
        hyperlink(p, f"{D.DOC_BASE}{D.TRANG[k][0]}.html", D.TRANG[k][1], size=8.5)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_after = Pt(2)


WORD_SCALE = 0.8   # in hình ở 80% viewBox (1px = 1/37,8 cm) -> chữ nhỏ nhất 7,2pt, giống bản HTML
FONT_LOG = []


def diagrams(doc, q, heading=None):
    """Chèn mọi hình của quy trình: ảnh, tên hình, chú giải; tiêu đề dính với hình đầu."""
    figs = B.figures(q, B.MAX_W)
    os.makedirs(IMG, exist_ok=True)
    items = [(f["svg"], f["w"], f["h"], os.path.join(IMG, f"{q['code']}_{i}.png")) for i, f in enumerate(figs, 1)]
    B.export_many(items, IMG)
    for i, f in enumerate(figs):
        sc = min(WORD_SCALE, TRANG_W * 37.795 / f["w"], ANH_CAO_TOI_DA * 37.795 / f["h"])  # hình trong khổ B.MAX_W x B.MAX_H nên tỉ lệ >= 0,778
        if B.font_min_pt(sc) < 7:
            raise SystemExit(f"Hình {q['code']} {f['ten']} ({f['phan']}/{f['tong']}): chữ in {B.font_min_pt(sc):.2f}pt, dưới 7pt")
        FONT_LOG.append((q["code"], f["ten"], f["phan"], round(B.font_min_pt(sc), 1)))
        if f["h"] * sc / 37.795 > ANH_CAO_TOI_DA + 0.01:
            raise SystemExit(f"Hình {q['code']} {f['ten']} ({f['phan']}/{f['tong']}) cao {f['h'] * sc / 37.795:.1f}cm, quá phần cao dùng được "
                             f"của trang Word ({ANH_CAO_TOI_DA}cm): sẽ bị cắt đáy")
        picture(doc, items[i][3], max_w=f["w"] * sc / 37.8, max_h=f["h"] * sc / 37.8 + 0.01)
        ph = f" (phần {f['phan']}/{f['tong']})" if f["tong"] > 1 else ""
        cap = P(doc, f"Sơ đồ {q['code']} - {f['ten']}{ph}", style="Caption", align=WD_ALIGN_PARAGRAPH.CENTER)
        cap.paragraph_format.keep_with_next = False
    P(doc, "Chú giải ký hiệu trong sơ đồ", style="Body Text", bold=True).paragraph_format.keep_with_next = True
    legend_table(doc, B.chu_giai(set().union(*(f["syms"] for f in figs))))


def steps(doc, q):
    s = q["buoc"]
    kinds = B.step_kinds(q)
    cc = B.chuyen_cho(q)
    ten = {"user": "Viindoo", "service": "Tự động", "manual": "Ngoài"}
    hd = D.HUONG_DAN[q["code"]]
    rows = [[f"{k + 1}\n{ten[kinds[k][0]]}" + ("\n+ Ngoài" if kinds[k][1] else ""), v, nv, vd, ngoai, cc.get(k + 1, "-").replace("; ", ";\n"), "" if hd[k] else "-"]
            for k, (v, nv, vd, ngoai) in enumerate(s)]
    t = table(doc, ["Bước", "Vị trí công việc", "Mô tả nhiệm vụ", "Tác vụ trên Viindoo (menu > nút > ô cần nhập)",
                    "Tác vụ ngoài phần mềm", "Chuyển cho", "Tài liệu hướng dẫn"],
              rows, [1.8, 2.5, 3.7, 6.8, 3.2, 2.8, 3.1])
    dks = B.nhan_dieu_kien(q)
    for k, row in enumerate(t.rows[1:]):
        shade(row.cells[0], B.COL[kinds[k][0]][0].lstrip("#"))
        if dks.get(k + 1):   # điều kiện của nhánh dẫn tới bước, chữ tím nghiêng như bản HTML
            p_ = row.cells[2].paragraphs[0]
            p_.add_run().add_break()
            r_ = p_.add_run(dks[k + 1])
            r_.italic = True
            r_.font.size = Pt(8)
            r_.font.color.rgb = RGBColor(0x7F, 0x42, 0x82)
        if hd[k]:
            path, ten_trang = D.TRANG[hd[k]]
            hyperlink(row.cells[6].paragraphs[0], f"{D.DOC_BASE}{path}.html", ten_trang)
    P(doc)


def proc(doc, q, first=False):
    h = doc.add_paragraph(f"[{q['code']}] Quy trình {q['ten'][0].lower() + q['ten'][1:]}", style="Heading 3")
    h.paragraph_format.page_break_before = False
    h.paragraph_format.keep_with_next = True
    tl(doc, q["code"])
    diagrams(doc, q)
    for t in [("Mục tiêu", q["muc_tieu"]), ("Bắt đầu", q["bat_dau"]), ("Kết thúc", q["ket_thuc"]), ("Luồng chứng từ", q["luong"])]:
        label(doc, *t).paragraph_format.keep_with_next = True   # các dòng tóm tắt dính nhau và dính với bảng bước
    for t in q.get("luu_y", []):
        label(doc, "Lưu ý", t).paragraph_format.keep_with_next = True
    steps(doc, q)


def main():
    loi = phan_quyen_kiem.kiem() + phan_quyen_kiem.kiem_phoi_hop() + doc_link_check.kiem()
    loi += [x for q in all_procs() for x in B.kiem_do_thi(q)]
    if loi:
        raise SystemExit("Ma trận phân quyền, đường dẫn tài liệu hoặc sơ đồ sai:\n" + "\n".join(loi))
    hinh = [x for q in all_procs() for x in B.kiem_hinh(q, B.MAX_W)]
    if hinh:
        raise SystemExit("Sơ đồ lỗi hình học (qtud_kiem_hinh: MUI, SONG, LAN, O, NHAN, CHAM, CONG, BE; hoặc không tìm được đường):\n" + "\n".join(hinh))
    doc = Document(TEMPLATE)
    clear_body(doc)
    for sec in doc.sections:  # A4 ngang
        sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
        sec.left_margin = sec.right_margin = Cm((29.7 - TRANG_W) / 2)
        sec.top_margin = sec.bottom_margin = Cm(1.5)
        sec.header_distance = sec.footer_distance = Cm(0.5)
    doc.add_paragraph(f"QUY TRÌNH ỨNG DỤNG VIINDOO CHO {getattr(D, 'KHACH_NGAN', D.KHACH).upper()}", style="Heading 1")
    label(doc, "Khách hàng", D.KHACH)
    label(doc, "Ngày lập", D.NGAY)
    if getattr(D, "CAN_CU", ""):
        label(doc, "Căn cứ", D.CAN_CU)
    P(doc, "Mỗi quy trình gồm sơ đồ và bảng các bước. Mỗi dòng là một bước do một vị trí làm: làm gì, vào menu nào trên Viindoo, "
           "bấm nút nào, nhập ô nào, chứng từ chuyển cho ai tiếp theo; cột Tài liệu hướng dẫn dẫn tới trang hướng dẫn "
           "tương ứng trên tài liệu Viindoo.", style="Body Text")

    doc.add_paragraph("1. Ma trận phân quyền theo vị trí", style="Heading 2")
    tl(doc, "ma_tran")
    doc.add_paragraph("Vị trí công việc và việc chính", style="Heading 3")
    table(doc, ["Vị trí công việc", "Việc chính trên Viindoo"], [[(a, ""), b] for a, b in D.VI_TRI], [6.5, 17.4])
    P(doc)
    doc.add_paragraph("Ma trận phân quyền", style="Heading 3")
    vt = D.VT_MT
    rows, nhom = [], []
    for cum, items in D.MA_TRAN:
        nhom.append(len(rows) + 1)
        rows.append([(cum, "")] + [""] * len(vt))
        rows += [[(muc, nhom_dau or "")] + list(vals) for muc, nhom_dau, vals in items]
    w = round((23.9 - 3.4) / len(vt), 2)
    t = table(doc, ["Ứng dụng"] + vt, rows, [3.4] + [w] * len(vt))
    for i in nhom:  # dòng tiêu đề cụm: gộp ô, tô nền
        cells = t.rows[i].cells
        m = cells[0].merge(cells[-1])
        for extra in m.paragraphs[1:]:
            extra._element.getparent().remove(extra._element)
        m.paragraphs[0].paragraph_format.keep_with_next = True   # dòng tên nhóm không đứng một mình cuối trang
        shade(m, "EDEDED")
    for g in D.GHI_CHU_MT:
        P(doc, "- " + g, style="Body Text")
    P(doc)
    P(doc, "Nguyên tắc gán quyền theo vị trí:", style="Body Text", bold=True).paragraph_format.keep_with_next = True
    for t in D.NGUYEN_TAC:
        P(doc, "- " + t, style="Body Text")
    P(doc)
    doc.add_paragraph("Chú giải cấp nhóm quyền", style="Heading 3")
    table(doc, ["Mục trên phần mềm", "Các cấp (cấp sau gồm quyền của cấp trước)"],
          [[(a, ""), b] for a, b in D.CHU_GIAI], [4.5, 19.4])
    P(doc)
    doc.add_paragraph("Quy tắc giới hạn dữ liệu", style="Heading 3")
    for t in D.GIOI_HAN:
        P(doc, "- " + t, style="Body Text")
    P(doc)
    doc.add_paragraph("2. Quy tắc phê duyệt", style="Heading 2")
    tl(doc, "phe_duyet")
    for t in D.PHE_DUYET:
        P(doc, "- " + t, style="Body Text")
    if getattr(D, "PD", None):
        doc.add_paragraph(f"PD - {D.PD['ten']}", style="Heading 3").paragraph_format.keep_with_next = True
        tl(doc, "PD")
        diagrams(doc, D.PD)
        steps(doc, D.PD)
    doc.add_paragraph("3. Kiểm soát dữ liệu: chốt chặn khi nhập, rà soát định kỳ, phối hợp khi cần tạo mới", style="Heading 2")
    tl(doc, "kiem_soat")
    P(doc, "Mỗi chốt chặn gắn với một vị trí nhập, một vị trí kiểm tra; cột Hệ thống hỗ trợ ghi điều người dùng thấy trên phần mềm khi nhập. "
           + getattr(D, "KIEM_SOAT_NGUOI", ""), style="Body Text")
    P(doc, "A. Chốt chặn khi nhập", style="Body Text", bold=True).paragraph_format.keep_with_next = True
    tl(doc, "chot_chan")
    goi2 = lambda g: " (gói 2)" if g == 2 else ""  # noqa: E731
    table(doc, ["Loại dữ liệu", "Vị trí nhập", "Thông tin bắt buộc / điều kiện", "Vị trí kiểm tra", "Kiểm tra những gì", "Thời điểm",
                "Hệ thống hỗ trợ"],
          [[(a + goi2(g), ""), b, c, d, k, t, h] for a, b, c, d, k, t, h, g in D.CHOT_CHAN],
          [2.8, 2.4, 5.0, 2.4, 3.6, 2.6, 5.1])
    pb = P(doc, "B. Bảng kiểm định kỳ", style="Body Text", bold=True)
    pb.paragraph_format.keep_with_next = True
    pb.paragraph_format.space_before = Pt(10)
    tl(doc, "ra_soat")
    P(doc, D.NHAC_DINH_KY, style="Body Text").paragraph_format.keep_with_next = True
    rows, grp = [], []
    for ts, items in D.RA_SOAT:
        grp.append(len(rows) + 1)
        rows.append([(ts, "")] + [""] * 4)
        rows += [[(v + goi2(g), ""), l, w, x, c] for v, l, w, x, c, g in items]
    t = table(doc, ["Việc rà soát", "Vị trí làm", "Xem ở đâu trên Viindoo", "Xử lý khi phát hiện", "Vị trí xác nhận"],
              rows, [5.3, 2.9, 8.1, 4.5, 3.1])
    for i in grp:
        cells = t.rows[i].cells
        m = cells[0].merge(cells[-1])
        for extra in m.paragraphs[1:]:
            extra._element.getparent().remove(extra._element)
        m.paragraphs[0].paragraph_format.keep_with_next = True   # dòng tên nhóm không đứng một mình cuối trang
        shade(m, "EDEDED")
    pc = P(doc, "C. Phối hợp khi cần tạo mới (sản phẩm, nhóm sản phẩm, bảng giá, điều khoản thanh toán...)", style="Body Text", bold=True)
    pc.paragraph_format.keep_with_next = True
    pc.paragraph_format.space_before = Pt(12)
    tl(doc, "phoi_hop")
    for x in D.PHOI_HOP_CACH:
        P(doc, "- " + x, style="Body Text")
    table(doc, ["Cần tạo mới", "Vị trí thường cần", "Vị trí có quyền tạo (theo ma trận)", "Gửi yêu cầu cho", "Thông tin phải gửi kèm", "Lưu ý"],
          [[(t, ""), c, "; ".join(phan_quyen_kiem.ai_co_quyen(q)), (n, ""), tt, lu] for t, c, n, tt, lu, q in D.PHOI_HOP],
          [3.1, 3.8, 4.3, 3.4, 5.2, 4.1])
    P(doc)
    if getattr(D, "DT", None):
        doc.add_paragraph(f"DT - {D.DT['ten']}", style="Heading 3").paragraph_format.keep_with_next = True
        tl(doc, "DT")
        diagrams(doc, D.DT)
        dt_mo_ta = getattr(D, "DT_MO_TA", "quy trình con dùng chung khi cần đối tác chưa có trên hệ thống")
        P(doc, dt_mo_ta[0].upper() + dt_mo_ta[1:] + ".", style="Body Text")
        steps(doc, D.DT)
    for so, g in enumerate(sorted({q["goi"] for q in D.QUY_TRINH}), 4):
        doc.add_paragraph(f"{so}. Quy trình {D.GOI_TEN[g]}", style="Heading 2")
        for j, q in enumerate([x for x in D.QUY_TRINH if x["goi"] == g]):
            proc(doc, q, first=j == 0)

    doc.save(OUT)
    n = sum(len(q["buoc"]) for q in D.QUY_TRINH)
    print(OUT, "| quy trình:", len(D.QUY_TRINH), "| bước:", n)
    with open(common.work_dir() / "handbook_font_word.json", "w", encoding="utf-8") as fh:
        json.dump(FONT_LOG, fh, ensure_ascii=False)


if __name__ == "__main__":
    main()
