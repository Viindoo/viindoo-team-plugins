# -*- coding: utf-8 -*-
"""Mô hình kế hoạch dùng chung: đọc project.py, handbook.py, current_state.json của dự án; tính giờ, tuần, danh mục việc.
Dùng bởi build_assessment_report.py, export_project_tasks.py, build_setup_worklist.py."""
import datetime
import json

import checks as C
import common

P = common.load("project")
H = common.load("handbook", required=False)


def state():
    f = common.data_file("current_state.json")
    if not f.exists():
        raise SystemExit(f"Thiếu {f}: chạy read_intake_workbook.py (khách mới) hoặc scan_live_system.py (khách đang dùng hệ thống) trước")
    return json.loads(f.read_text(encoding="utf-8"))


def tasks():
    """Danh mục việc đã trộn với việc chuẩn: list (nhóm, [việc đầy đủ trường])."""
    out = []
    for grp in P.TASK_GROUPS:
        rows = []
        for t in grp["tasks"]:
            std = C.TASKS.get(t.get("std"), (None, "", "", "", [], []))
            rows.append(dict(code=t["code"], name=t.get("name") or std[1], type=t.get("type") or std[2], method=t.get("method") or std[3],
                             customer=t.get("customer") or std[4], viindoo=t.get("viindoo") or std[5], hours=t.get("hours") or 0,
                             std=t.get("std"), checks=t.get("checks"), current=t.get("current"), package=grp["package"]))
        out.append((grp, rows))
    return out


def group_hours(code):
    return sum(t.get("hours") or 0 for grp in P.TASK_GROUPS if grp["code"] == code for t in grp["tasks"])


def training_hours(pkg):
    return sum(t["hours"] for t in P.TRAINING if t["package"] == pkg)


def item_hours(h):
    if isinstance(h, str):
        kind, _, key = h.partition(":")
        return group_hours(key) if kind == "group" else training_hours(int(key))
    return h or 0


def weeks(t):
    t = (t or "").replace(" ", "")
    s = set()
    for part in filter(None, t.split(",")):
        part = part.replace("T", "")
        a, _, b = part.partition("-")
        if a.isdigit():
            s.update(range(int(a), int(b or a) + 1))
    return s


def week_start(n):
    return datetime.date.fromisoformat(P.WEEK1) + datetime.timedelta(weeks=n - 1)


def processes():
    """(mã, tên, gói, vị trí tham gia) - từ handbook.py nếu có, nếu không từ project.PROCESSES."""
    if H:
        out = []
        for q in H.QUY_TRINH:
            vt = []
            for b in q["buoc"]:
                if b[0] != getattr(H, "HT", None) and b[0] not in vt:
                    vt.append(b[0])
            out.append((q["code"], q["ten"], q["goi"], ", ".join(vt)))
        return out
    return list(getattr(P, "PROCESSES", []))


def current_text(row, res_by_id):
    if row.get("current"):
        return row["current"]
    ids = row.get("checks") or [cid for cid, c in C.CHECKS.items() if row.get("std") in c[4]]
    rs = [res_by_id[i] for i in ids if i in res_by_id]
    bad = [f'{r["label"]}: {r["value"]}' for r in rs if r["level"] in ("vua", "kem")]
    info = [f'{r["label"]}: {r["value"]}' for r in rs if r["level"] == "tt" and r["value"]]
    if bad or info:
        return "; ".join(bad + info)
    return "Đạt" if rs and all(r["level"] == "tot" for r in rs) else "-"
