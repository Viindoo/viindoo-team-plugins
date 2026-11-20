# -*- coding: utf-8 -*-
"""Xuất kế hoạch triển khai thành bảng nhiệm vụ để người tư vấn dựng dự án trên viindoo.com. KHÔNG ghi vào hệ thống nào.

Quy ước nhiệm vụ (đã thống nhất):
- Mỗi dòng kế hoạch (PLAN, loại item) một nhiệm vụ tên "[KH] <mã kế hoạch> <việc>" - trùng mã trong báo cáo gửi khách.
- Mỗi giai đoạn, gói (PLAN, loại phase) là nhiệm vụ cha; gói sau có thể gối lên cuối gói trước (phần giám sát, hỗ trợ).
- Giờ phân bổ = giờ kế hoạch. Giờ chỉ đặt ở nhiệm vụ nhận chấm công: nhiệm vụ cha (gói) và nhiệm vụ đào tạo có buổi con để 0,
  giờ nằm ở việc con / buổi con, nên tổng giờ phân bổ của dự án đúng bằng tổng giờ kế hoạch.
- Mô tả = việc + kết quả. Bắt đầu = thứ Hai của tuần đầu; kết thúc và hạn = thứ Sáu của tuần cuối (buổi đào tạo: đúng ngày học).
  Cột ngày theo nhiệm vụ của viindoo.com: planned_date_start, planned_date_end, date_deadline. Cơ sở dữ liệu khác tên trường thì đổi
  bằng --start-field, --end-field (đặt chuỗi rỗng để bỏ cột).
- Đào tạo: tối đa N buổi/tuần (TRAINING_RULE), mỗi buổi 2-3 giờ; học xong một mảng mới sang mảng sau, theo thứ tự trong TRAINING
  (thứ tự dòng chảy chứng từ). Mỗi buổi là nhiệm vụ con của nhiệm vụ đào tạo của gói.

Ra (thư mục Nội bộ):
- '<Khách> - Nhiệm vụ dự án (nhập viindoo.com).csv' : nhập bằng chức năng Nhập của danh sách nhiệm vụ trong dự án
  (cột id, parent_id/id để Odoo tạo nhiệm vụ cha trước, gắn con sau).
- '<Khách> - Lịch nhiệm vụ và buổi đào tạo.csv'     : bảng xem lịch: ngày bắt đầu, hạn, giờ, buổi đào tạo.
Chạy: python3 export_project_tasks.py --data <thư mục dữ liệu dự án> [--start-field <trường>] [--end-field <trường>]
"""
import csv
import datetime
import html
import math
import re
import unicodedata

import common

A = common.cli("Xuất bảng nhiệm vụ dự án viindoo.com từ kế hoạch triển khai",
               lambda p: (p.add_argument("--start-field", default="planned_date_start",
                                         help="trường ngày bắt đầu trên nhiệm vụ (mặc định planned_date_start của viindoo.com; '' để bỏ cột)"),
                          p.add_argument("--end-field", default="planned_date_end",
                                         help="trường ngày kết thúc trên nhiệm vụ (mặc định planned_date_end của viindoo.com; '' để bỏ cột)")))

import plan_model as R  # noqa: E402

P = R.P


def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]+", "_", s.encode("ascii", "ignore").decode().lower()).strip("_")[:40]


def friday(week):
    return R.week_start(week) + datetime.timedelta(days=4)


def split_hours(h, rule):
    n = max(1, math.ceil(h / rule["max_hours"]))
    while n > 1 and h / n < rule["min_hours"]:
        n -= 1
    base = round(h / n * 4) / 4
    return [base] * (n - 1) + [round(h - base * (n - 1), 2)]


def schedule_training(pkg, start_week):
    """Buổi đào tạo của một gói: [(mảng, buổi, số buổi, giờ, ngày)], xếp liên tiếp, mảng sau bắt đầu khi mảng trước xong."""
    rule = P.TRAINING_RULE
    days = list(rule["weekdays"])[: rule["per_week"]]
    slots = (R.week_start(w) + datetime.timedelta(days=d) for w in range(start_week, start_week + 200) for d in days)
    out, warn = [], []
    for t in [x for x in P.TRAINING if x["package"] == pkg]:
        parts = split_hours(t["hours"], rule)
        if t["hours"] < rule["min_hours"]:
            warn.append(f'Mảng "{t["area"]}" chỉ {t["hours"]:g} giờ, ngắn hơn một buổi tối thiểu - cân nhắc ghép với mảng kế tiếp')
        for i, h in enumerate(parts, 1):
            out.append((t, i, len(parts), h, next(slots)))
    return out, warn


def main():
    proj = getattr(P, "PROJECT_NAME", "")
    key = slug(P.SHORT_NAME)
    tasks, lich, warn = [], [], []
    grp_by_code = {grp["code"]: grp for grp in P.TASK_GROUPS}
    cur_parent, parent_rows = None, {}
    items_by_parent = {}
    for kind, ma, viec, tuan, h, kq in P.PLAN:
        if kind == "phase":
            name = P.PACKAGE_NAMES.get(int(ma), viec.capitalize()) if ma.isdigit() and int(ma) in P.PACKAGE_NAMES else viec.capitalize()
            cur_parent = f"kh_{key}_{slug(ma)}"
            parent_rows[cur_parent] = dict(id=cur_parent, name=f"[KH] {ma} {name}", parent="", hours=0, weeks=set(),
                                           desc=f"<p><b>Việc:</b> {html.escape(name)}</p><p><b>Kết quả:</b> các việc con hoàn thành</p>")
            tasks.append(parent_rows[cur_parent])
            continue
        if kind != "item":
            continue
        ws = R.weeks(tuan)
        hours = R.item_hours(h)
        desc = f"<p><b>Việc:</b> {html.escape(viec)}</p>"
        if isinstance(h, str) and h.startswith("group:"):
            grp = grp_by_code[h.split(":")[1]]
            desc += "<ul>" + "".join(f"<li>{html.escape(t['code'])} {html.escape(t.get('name') or R.C.TASKS[t['std']][1])}</li>" for t in grp["tasks"]) + "</ul>"
        desc += f"<p><b>Kết quả:</b> {html.escape(kq)}</p>"
        row = dict(id=f"kh_{key}_{slug(ma)}", name=f"[KH] {ma} {viec}", parent=cur_parent, hours=hours, weeks=ws, desc=desc)
        tasks.append(row)
        parent_rows[cur_parent]["weeks"] |= ws
        items_by_parent.setdefault(cur_parent, []).append(row)
        if isinstance(h, str) and h.startswith("training:"):
            pkg = int(h.split(":")[1])
            sessions, w = schedule_training(pkg, min(ws))
            warn += w
            row["hours"] = 0
            row["session_total"] = hours
            for t, i, n, sh, day in sessions:
                sid = f"{row['id']}_{slug(t['area'])}_{i}"
                tasks.append(dict(id=sid, name=f"[KH] {ma} Đào tạo {t['area']} - buổi {i}/{n}", parent=row["id"], hours=sh,
                                  weeks=set(), day=day,
                                  desc=f"<p><b>Việc:</b> đào tạo {html.escape(t['area'])} - {html.escape(t['content'])}; người học: {html.escape(t['positions'])}; "
                                       f"quy trình {html.escape(t['processes'])}</p><p><b>Kết quả:</b> bài thực hành: {html.escape(t['exercise'])}; "
                                       f"danh sách tham dự, bản ghi hình</p>"))
                if day > friday(max(ws)):
                    warn.append(f"Buổi {t['area']} {i}/{n} ({day.strftime('%d/%m/%Y')}) rơi sau tuần cuối của mục {ma} ({tuan}) - nới tuần trong kế hoạch")

    def dates(t):
        if t.get("day"):
            return t["day"], t["day"]
        if not t["weeks"]:
            return None, None
        return R.week_start(min(t["weeks"])), friday(max(t["weeks"]))

    ngay = [f for f in (A.start_field, A.end_field) if f]
    head = ["id", "name", "project_id", "parent_id/id", "allocated_hours"] + ngay + ["date_deadline", "description"]
    out_dir = common.internal_dir()
    f_imp = out_dir / f"{P.SHORT_NAME} - Nhiệm vụ dự án (nhập viindoo.com).csv"
    f_lich = out_dir / f"{P.SHORT_NAME} - Lịch nhiệm vụ và buổi đào tạo.csv"
    with open(f_imp, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(head)
        for t in tasks:
            b, d = dates(t)
            w.writerow([f"__import__.{t['id']}", t["name"], proj, f"__import__.{t['parent']}" if t["parent"] else "", f"{t['hours']:g}"]
                       + ([b.strftime("%Y-%m-%d 08:00:00") if b else ""] if A.start_field else [])
                       + ([d.strftime("%Y-%m-%d 17:00:00") if d else ""] if A.end_field else [])
                       + [d.strftime("%Y-%m-%d 17:00:00") if d else "", t["desc"]])
    with open(f_lich, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["Nhiệm vụ", "Nhiệm vụ cha", "Giờ phân bổ", "Bắt đầu", "Hạn"])
        names = {t["id"]: t["name"] for t in tasks}
        for t in tasks:
            b, d = dates(t)
            w.writerow([t["name"], names.get(t["parent"], ""), f"{t['hours']:g}".replace(".", ","),
                        b.strftime("%d/%m/%Y") if b else "", d.strftime("%d/%m/%Y") if d else ""])
    tong = sum(t["hours"] for t in tasks)
    ke_hoach = sum(R.item_hours(r[4]) for r in P.PLAN if r[0] == "item")
    print(f_imp)
    print(f_lich)
    print(f"{len(tasks)} nhiệm vụ ({sum(1 for t in tasks if not t['parent'])} nhiệm vụ cha, "
          f"{sum(1 for t in tasks if t.get('day'))} buổi đào tạo); tổng giờ phân bổ {tong:g} = tổng giờ kế hoạch {ke_hoach:g}: {'ĐẠT' if abs(tong - ke_hoach) < 0.01 else 'LỆCH'}")
    ky = getattr(P, "SIGNED_HOURS", None)
    if ky and ke_hoach > ky:
        print(f"Cảnh báo: kế hoạch {ke_hoach:g} giờ vượt gói đã ký {ky:g} giờ")
    for x in warn:
        print("Cảnh báo:", x)
    if abs(tong - ke_hoach) >= 0.01:
        raise SystemExit("Tổng giờ phân bổ lệch kế hoạch")


if __name__ == "__main__":
    main()
