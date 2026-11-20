# -*- coding: utf-8 -*-
"""Kiểm bộ quy trình ứng dụng trước khi dựng, không sinh tệp: ma trận phân quyền tuyến tính và đúng tên nhóm trên phần mềm,
người nhận yêu cầu phối hợp có quyền tạo, đường dẫn tài liệu hướng dẫn (ngoại tuyến), đồ thị và hình học từng sơ đồ.

Chạy: python3 check_handbook.py --data <thư mục dữ liệu dự án>     (mã thoát 1 khi có lỗi)
"""
import sys

import common

if __name__ == "__main__":
    common.cli("Kiểm bộ quy trình ứng dụng (phân quyền, tài liệu, sơ đồ)")

import bpmn_engine as B  # noqa: E402
import doc_link_check  # noqa: E402
import permission_check  # noqa: E402

D = common.load("handbook")


def run():
    procs = D.QUY_TRINH + [x for x in (getattr(D, "PD", None), getattr(D, "DT", None)) if x]
    groups = [
        ("Ma trận phân quyền", permission_check.kiem()),
        ("Phối hợp khi cần tạo mới", permission_check.kiem_phoi_hop()),
        ("Tài liệu hướng dẫn (" + doc_link_check.tom_tat() + ")", doc_link_check.kiem()),
        ("Đồ thị sơ đồ", [x for q in procs for x in B.kiem_do_thi(q)]),
        ("Hình học sơ đồ (HTML)", [x for q in procs for x in B.kiem_hinh(q, B.MAX_W_HTML)]),
        ("Hình học sơ đồ (Word)", [x for q in procs for x in B.kiem_hinh(q, B.MAX_W)]),
    ]
    bad = 0
    for name, errs in groups:
        print(f"[{'ĐẠT' if not errs else 'LỖI'}] {name}" + ("" if not errs else f": {len(errs)}"))
        for x in errs:
            print("    " + x)
        bad += len(errs)
    print(f"{len(D.QUY_TRINH)} quy trình, {sum(len(q['buoc']) for q in D.QUY_TRINH)} bước, {sum(len(B.figures(q, B.MAX_W_HTML)) for q in procs)} hình")
    return bad


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
