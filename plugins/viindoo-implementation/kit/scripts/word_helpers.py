# -*- coding: utf-8 -*-
"""Tiện ích Word dùng chung cho bộ quy trình ứng dụng (bản Word)."""
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from PIL import Image


W_SCALE = 1.0   # hệ số nới bề rộng bảng theo khổ trang (tài liệu gọi đặt lại)


# ---------------------------------------------------------------- tiện ích Word
def clear_body(doc):
    body = doc.element.body
    for el in list(body):
        if el.tag != qn("w:sectPr"):
            body.remove(el)


def P(doc, text="", style="Normal", bold=False, italic=False, align=None, size=None):
    p = doc.add_paragraph(style=style)
    if text:
        r = p.add_run(text)
        r.bold, r.italic = bold or None, italic or None
        if size:
            r.font.size = Pt(size)
    if align is not None:
        p.alignment = align
    return p


def label(doc, k, v):
    p = doc.add_paragraph(style="Normal")
    p.add_run(k + ": ").bold = True
    p.add_run(v)
    return p


def table(doc, header, rows, widths, check_cols=()):
    widths = [w * W_SCALE for w in widths]
    t = doc.add_table(rows=1, cols=len(header))
    t.style = doc.styles["Table"]
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), "A6A6A6")
        borders.append(b)
    tblPr.append(borders)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)
    for i, h in enumerate(header):
        cell_set(t.rows[0].cells[i], h, bold=True)
        shade(t.rows[0].cells[i], "D9D9D9")
    for r in rows:
        row = t.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for i, v in enumerate(r):
            if isinstance(v, tuple):  # (đậm, thường)
                cell_set(row.cells[i], v[1], head=v[0])
            else:
                cell_set(row.cells[i], v, box=i in check_cols)
    for row in [t.rows[0]] + (list(t.rows[-2:-1]) if len(t.rows) > 2 else []):   # không để trang chỉ có một dòng cuối, hay tiêu đề bảng đứng một mình
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.keep_with_next = True
    t.autofit = False
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:type"), "dxa")
    tblW.set(qn("w:w"), str(int(sum(widths) * 567)))
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 567)))
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    return t


def shade(cell, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shd)


def cell_set(cell, text, bold=False, head=None, box=False):
    p = cell.paragraphs[0]
    p.style = cell.part.document.styles["Compact"]
    if head:
        p.add_run(head).bold = True
        if text:
            p.add_run("\n")
    for k, line in enumerate(str(text).split("\n")):
        if k:
            p.add_run().add_break()
        if box and line.startswith("□"):
            r = p.add_run("□")
            r.font.name = "Arial"
            line = line[1:]
        p.add_run(line).bold = bold or None


def picture(doc, path, max_w=23.5, max_h=13.0):
    w, h = Image.open(path).size
    width = min(max_w, max_h * w / h)
    doc.add_picture(path, width=Cm(width))
    doc.paragraphs[-1].paragraph_format.space_before = doc.paragraphs[-1].paragraph_format.space_after = 0
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.paragraphs[-1].paragraph_format.keep_with_next = True


def hyperlink(paragraph, url, text, size=None):
    """Thêm liên kết bấm được vào đoạn văn (Word)."""
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), r_id)
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    c = OxmlElement("w:color")
    c.set(qn("w:val"), "0563C1")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rpr.append(c)
    rpr.append(u)
    if size:
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(size * 2)))
        rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    r.append(t)
    h.append(r)
    paragraph._p.append(h)
    return h
