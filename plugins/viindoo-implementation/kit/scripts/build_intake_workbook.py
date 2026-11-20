# -*- coding: utf-8 -*-
"""Dựng workbook thu thập dữ liệu triển khai (khách mới, chưa có hệ thống - nhánh A) theo checks.SHEETS.

Kiểu trình bày theo mẫu phiếu khảo sát PRE01 của Viindoo: logo, tiêu đề tím, hàng tiêu đề nền cyan, ô khách điền nền xanh nhạt,
danh sách chọn ở cột có giá trị cố định, ghi chú cách điền dưới tiêu đề cột. Sheet đầu là Hướng dẫn: mỗi sheet dùng để làm gì,
Viindoo kiểm gì trên dữ liệu đó, nuôi việc thiết lập nào.

Chạy:
  python3 build_intake_workbook.py --blank <tệp.xlsx>                     mẫu trắng (đính kèm Brain, gửi khách)
  python3 build_intake_workbook.py --data <thư mục dự án> [--sample]      mẫu có tên khách (project.py); --sample điền sẵn dữ liệu ví dụ
"""
import argparse
import os
import pathlib
import sys

import xlsxwriter

import checks as C
import common

HEADER_ROW = 4          # hàng tiêu đề cột (0-based) của mọi sheet danh sách; read_intake_workbook.py đọc theo hàng này
INPUT_ROWS = 200        # số dòng kẻ sẵn để khách điền
CYAN, TIM, HEAD, BODY, MUTED, BG = "#00BBCE", "#7F4282", "#21272B", "#282F33", "#6B6D70", "#F2F2F2"
O_DIEN, VIEN = "#E6F8FA", "#D0D5D8"


def build(path, khach="", ngay_chot="", sample=None):
    wb = xlsxwriter.Workbook(str(path))
    wb.set_properties({"title": "Thu thập dữ liệu triển khai Viindoo", "author": "Viindoo", "company": "Viindoo"})
    base = {"font_name": "Roboto", "font_size": 10.5, "font_color": BODY, "valign": "top", "text_wrap": True}

    def fmt(**kw):
        d = dict(base)
        d.update(kw)
        return wb.add_format(d)

    f_title = fmt(font_name="Montserrat", font_size=18, bold=True, font_color=TIM, text_wrap=False, valign="vcenter")
    f_lead = fmt(italic=True, font_color=MUTED)
    f_lbl = fmt(bold=True, font_color=MUTED, text_wrap=False)
    f_hdr = fmt(bold=True, font_color="#FFFFFF", bg_color=CYAN, border=1, border_color=VIEN, valign="vcenter", align="center")
    f_note = fmt(italic=True, font_size=9, font_color=MUTED, bg_color=BG, border=1, border_color=VIEN)
    f_cell = fmt(border=1, border_color=VIEN)
    f_cell_b = fmt(border=1, border_color=VIEN, bold=True)
    f_dien = fmt(border=1, border_color=VIEN, bg_color=O_DIEN)
    f_band = fmt(bold=True, font_color=HEAD, bg_color=BG, border=1, border_color=VIEN, text_wrap=False)
    logo = str(common.presales_root() / "brand" / "logos" / "viindoo-logo-color.png")

    def head(ws, title, lead, ncol):
        ws.hide_gridlines(2)
        ws.set_row(0, 40)
        if os.path.exists(logo):
            ws.insert_image(0, 0, logo, {"x_scale": 0.12, "y_scale": 0.12, "x_offset": 4, "y_offset": 8, "object_position": 3})
        ws.write(0, 2 if ncol > 2 else 1, title, f_title)
        ws.merge_range(1, 0, 1, max(ncol - 1, 1), lead, f_lead)
        ws.set_row(1, 32)

    # ---------------------------------------------------------------- Hướng dẫn
    ws = wb.add_worksheet("Hướng dẫn")
    for i, w in enumerate([22, 44, 58, 44]):
        ws.set_column(i, i, w)
    head(ws, "THU THẬP DỮ LIỆU TRIỂN KHAI VIINDOO", "Doanh nghiệp điền vào các ô nền xanh nhạt. Cột có dấu * là bắt buộc. "
         "Dữ liệu dùng để Viindoo đánh giá hiện trạng, thiết lập hệ thống và nhập số dư đầu kỳ.", 4)
    r = 3
    for nhan, gt in [("Doanh nghiệp", khach), ("Ngày chốt số dư đầu kỳ", ngay_chot), ("Người điền, điện thoại", "")]:
        ws.write(r, 0, nhan, f_lbl)
        ws.merge_range(r, 1, r, 3, gt, f_cell_b if gt else f_dien)
        r += 1
    r += 1
    for t in ["Cách điền:",
              "- Điền theo thực tế tại ngày chốt số dư; dòng nào không có thì để trống, không xoá sheet.",
              "- Tên phòng ban, vị trí, đối tác, mã sản phẩm, mã kho phải viết giống nhau giữa các sheet (các sheet tham chiếu nhau).",
              "- Quy trình và phân quyền ghi theo vị trí công việc, không theo tên người.",
              "- Đã có danh sách sẵn (xuất từ phần mềm cũ, Excel đang dùng) thì dán vào đúng cột, giữ hàng tiêu đề.",
              "- Gửi lại Viindoo cả tệp; Viindoo kiểm tự động và gửi lại danh sách điểm cần bổ sung."]:
        ws.merge_range(r, 0, r, 3, t, f_lead if t.startswith("-") else f_lbl)
        r += 1
    r += 1
    for c, h in enumerate(["Sheet", "Dùng để", "Viindoo kiểm gì trên dữ liệu này", "Nuôi việc thiết lập"]):
        ws.write(r, c, h, f_hdr)
    r += 1
    for s in C.SHEETS:
        kiem = "\n".join("- " + C.CHECKS[k][1] for k in s["checks"])
        viec = "\n".join("- " + C.TASKS[t][1] for t in s["tasks"])
        ws.write(r, 0, s["title"], f_cell_b)
        ws.write(r, 1, s["purpose"], f_cell)
        ws.write(r, 2, kiem, f_cell)
        ws.write(r, 3, viec, f_cell)
        ws.set_row(r, 15 * max(len(s["checks"]), len(s["tasks"]), 2) + 6)
        r += 1

    # ---------------------------------------------------------------- sheet dữ liệu
    for s in C.SHEETS:
        cols = s["columns"]
        ws = wb.add_worksheet(s["title"])
        for i, (_h, _b, _n, _l, w) in enumerate(cols):
            ws.set_column(i, i, w)
        head(ws, s["title"].split(". ", 1)[1].upper(), s["purpose"] + " Viindoo kiểm: " + "; ".join(C.CHECKS[k][1].lower() for k in s["checks"]) + ".", len(cols))
        if s.get("form"):
            for c, (h, b, *_x) in enumerate(cols):
                ws.write(HEADER_ROW - 1, c, h + (" *" if b and c == 1 else ""), f_hdr)
            vals = (sample or {}).get(s["key"], {})
            for i, ten in enumerate(s["rows"]):
                rr = HEADER_ROW + i
                ws.write(rr, 0, ten + (" *" if ten in s.get("required_rows", []) else ""), f_cell_b)
                ws.write(rr, 1, vals.get(ten, ""), f_dien)
                ws.write(rr, 2, "", f_dien)
            ws.freeze_panes(HEADER_ROW, 0)
            continue
        ws.set_row(HEADER_ROW - 1, 30)
        for c, (h, b, n, lst, _w) in enumerate(cols):
            ws.write(HEADER_ROW - 1, c, h + (" *" if b else ""), f_hdr)
            ws.write(HEADER_ROW, c, n or "", f_note)
            if lst:
                ws.data_validation(HEADER_ROW + 1, c, HEADER_ROW + INPUT_ROWS, c,
                                   {"validate": "list", "source": lst, "error_type": "information"})
        rows = (sample or {}).get(s["key"], [])
        for i in range(max(INPUT_ROWS, len(rows))):
            rr = HEADER_ROW + 1 + i
            row = rows[i] if i < len(rows) else ()
            for c in range(len(cols)):
                v = row[c] if c < len(row) else ""
                ws.write(rr, c, v, f_dien)
        ws.freeze_panes(HEADER_ROW + 1, 1)
        ws.autofilter(HEADER_ROW - 1, 0, HEADER_ROW + max(INPUT_ROWS, len(rows)), len(cols) - 1)
    wb.close()
    return path


def main():
    p = argparse.ArgumentParser(description="Dựng workbook thu thập dữ liệu triển khai (nhánh A)")
    p.add_argument("--blank", help="ghi mẫu trắng ra tệp này")
    p.add_argument("--data", help="thư mục dữ liệu dự án (lấy tên khách, ngày chốt từ project.py)")
    p.add_argument("--out", help="thư mục ra")
    p.add_argument("--sample", action="store_true", help="điền sẵn dữ liệu ví dụ (intake_sample.py trong thư mục dữ liệu)")
    a = p.parse_args()
    if a.blank:
        print(build(pathlib.Path(a.blank).expanduser()))
        return
    if not a.data:
        sys.exit("Cần --blank <tệp> hoặc --data <thư mục dự án>")
    os.environ[common.ENV_DATA] = str(pathlib.Path(a.data).expanduser().resolve())
    if a.out:
        os.environ[common.ENV_OUT] = str(pathlib.Path(a.out).expanduser().resolve())
    P = common.load("project")
    sample = common.load("intake_sample").SAMPLE if a.sample else None
    out = common.out_dir() / f"{P.SHORT_NAME} - Thu thập dữ liệu triển khai.xlsx"
    print(build(out, P.CUSTOMER, getattr(P, "OPENING_DATE", ""), sample))


if __name__ == "__main__":
    main()
