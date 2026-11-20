# -*- coding: utf-8 -*-
"""Kiểm ngoại tuyến: mọi đường dẫn tài liệu hướng dẫn trong handbook.TRANG có thật trên đúng nhánh phiên bản của kho tài liệu Viindoo.

Không gọi viindoo.com (gửi hàng loạt yêu cầu làm máy chủ chặn IP). Site tài liệu dựng từ kho Viindoo/documentation, mỗi phiên bản
một nhánh, nên đối chiếu bằng `git ls-tree` trên nhánh đó là đủ.
- Kho tài liệu: $VIINDOO_DOCS_REPO (mặc định ~/git/viindoo-documentation).
- Nhánh: phiên bản đọc từ handbook.DOC_BASE (.../documentation/<bản>/...); remote: $VIINDOO_DOCS_REMOTE (mặc định upstream, rồi origin).
"""
import os
import re
import subprocess

import common

D = common.load("handbook")

REPO = os.environ.get("VIINDOO_DOCS_REPO", os.path.expanduser("~/git/viindoo-documentation"))


def _tree(version):
    remotes = [os.environ["VIINDOO_DOCS_REMOTE"]] if os.environ.get("VIINDOO_DOCS_REMOTE") else ["upstream", "origin"]
    for r in remotes:
        res = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", f"{r}/{version}", "content/"],
                             capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return set(res.stdout.split("\n")), f"{r}/{version}"
    raise SystemExit(f"Không đọc được nhánh {version} của kho tài liệu {REPO} (remote {', '.join(remotes)}). "
                     "Clone kho Viindoo/documentation rồi đặt $VIINDOO_DOCS_REPO, hoặc git fetch nhánh đó.")


def kiem():
    """Trả danh sách lỗi; rỗng là đạt."""
    m = re.search(r"/documentation/([0-9.]+)/", D.DOC_BASE)
    if not m:
        return [f"DOC_BASE không có phiên bản: {D.DOC_BASE}"]
    tree, _ref = _tree(m.group(1))
    loi = [f"{k}: {p}" for k, (p, _t) in D.TRANG.items() if f"content/applications/{p}.rst" not in tree]
    loi += [f"TAI_LIEU {m_}: khoá {k} không có trong TRANG" for m_, ks in D.TAI_LIEU.items() for k in ks if k not in D.TRANG]
    loi += [f"HUONG_DAN {c}: khoá {k} không có trong TRANG" for c, ks in D.HUONG_DAN.items() for k in ks if k and k not in D.TRANG]
    codes = {q["code"] for q in D.QUY_TRINH} | {x["code"] for x in (getattr(D, "PD", None), getattr(D, "DT", None)) if x}
    loi += [f"quy trình {c} chưa có TAI_LIEU" for c in sorted(codes) if c not in D.TAI_LIEU]
    return loi


def tom_tat():
    m = re.search(r"/documentation/([0-9.]+)/", D.DOC_BASE)
    return f"{len(D.TRANG)} trang, {len(D.TAI_LIEU)} mục, nhánh {m.group(1) if m else '?'}"
