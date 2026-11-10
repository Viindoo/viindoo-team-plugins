"""KHUÔN THAM KHẢO (lấy từ cụm Nhân sự - id bản ghi là của dữ liệu demo cụm đó, cụm mới phải thay).

Dựng bản tiếng Anh của DỮ LIỆU demo HRM (không phải nhãn giao diện).

Vì sao cần: `doi_ngon_ngu.py en` chỉ đổi NHÃN giao diện Viindoo. Dữ liệu do mình bơm
(tên kỹ năng, tên khoá học, chức danh, phòng ban, dòng lương, OKR, bộ lọc đã lưu) được
tạo bằng giao diện tiếng Việt nên trong màn tiếng Anh vẫn hiện tiếng Việt.
Xem `references/ban-ngon-ngu-hai.md` của skill viindoo-video-cum-nghiep-vu. Bản Việt đã đăng vẫn phải nguyên vẹn, nên:

  - Trường DỊCH ĐƯỢC (translate=True): ghim lại bản vi_VN rồi mới ghi bản en_US.
    Hai lượt ghi chứ không một: nếu bản ghi mới chỉ có một giá trị thì vi_VN đang ĂN THEO
    en_US, ghi thẳng en_US sẽ kéo cả tiếng Việt sang tiếng Anh.
  - Trường KHÔNG dịch được (hr.skill.level, ir.filters, okr.node, attendance.device,
    hr.payslip, res.company): đổi tên tạm để chụp bản Anh, chép tên cũ ra
    `en_rename_backup.json`, chụp xong chạy `restore` để trả lại y như cũ.

Danh sách trường dịch được/không là ĐỌC TỪ ir.model.fields của chính máy chủ
(xem `kiem_truong()`), không chép tay theo trí nhớ.

Chạy:  python3 dich_en.py apply     -> dịch + đổi tên tạm (trước khi chụp bản Anh)
       python3 dich_en.py restore   -> trả lại tên tiếng Việt (sau khi chụp xong)
       python3 dich_en.py check     -> in trạng thái hai ngôn ngữ của vài bản ghi mẫu
"""
import importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("conn", os.path.join(HERE, "conn.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
call = c.call
BACKUP = os.path.join(HERE, "en_rename_backup.json")
VI = {"context": {"lang": "vi_VN"}}
EN = {"context": {"lang": "en_US"}}

# ---------------------------------------------------------------- trường dịch được
# {model: {id hoặc tên tiếng Việt: tên tiếng Anh}}  - khoá là tên thì áp cho MỌI bản ghi
# trùng tên (dòng lương lặp lại ở từng cơ cấu lương nên phải khớp theo tên).
DICH_THEO_ID = {
    "hr.skill.type": {
        3: "EV production skills", 4: "Quality control",
        5: "Safety & compliance", 6: "Engineering & maintenance",
    },
    "hr.skill": {
        37: "Frame assembly", 38: "Wiring and connection",
        39: "Lithium battery pack assembly", 40: "Jigging and welding",
        41: "Powder coating", 42: "Power screwdriver operation",
        43: "Line assembly", 44: "Packing and warehousing",
        45: "Final inspection (QC)", 46: "Dimensional inspection",
        47: "Electrical safety testing", 48: "Vehicle test drive",
        49: "Occupational safety", 50: "5S on the shop floor",
        51: "Fire prevention and fighting", 52: "Vehicle registration procedure",
        53: "Technical drawing reading", 54: "Equipment maintenance",
        55: "Line troubleshooting", 56: "Machine calibration",
    },
    "slide.channel": {
        3: "Occupational safety in the assembly plant",
        4: "5S on the shop floor",
        5: "Frame assembly - Basic",
        6: "Line assembly - Basic",
        7: "Lithium battery pack assembly - Safety and procedure",
        8: "Wiring and connection",
        9: "Power screwdriver operation",
        10: "Final inspection (QC)",
    },
    "product.template": {
        1431: "Viindoo Aura Electric Motorbike",
        1432: "Viindoo Nova Electric Bicycle",
        1210: "Powder-coated frame assembly - Lumi",
        1211: "Electrical harness assembly - Lumi",
        1212: "Powder-coated frame assembly - Aura",
        1213: "Electrical harness assembly - Aura",
        1214: "Powder-coated frame assembly - Nova",
    },
    "attendance.device.location": {
        1: "EV assembly plant gate", 2: "Plant office",
    },
    "attendance.device": {
        1: "ZKTeco time clock - Assembly plant gate",
        2: "ZKTeco time clock - Plant office",
    },
    "product.attribute": {1: "Vehicle colour", 2: "Vehicle version"},
    "product.attribute.value": {
        1: "Pearl white", 2: "Matte black", 3: "Moss green",
        4: "Burgundy", 5: "Cement grey", 6: "Standard", 7: "Premium",
    },
}

# Tên tiếng Việt GỐC của nhóm dịch theo id. Phải ghi ra đây chứ không đọc từ máy chủ:
# sau lượt ghi bản tiếng Anh thì máy chủ không còn bản tiếng Việt để mà đọc lại.
VI_GOC = {
    "hr.skill.type": {
        3: "Kỹ năng sản xuất xe điện", 4: "Kiểm soát chất lượng",
        5: "An toàn & Tuân thủ", 6: "Kỹ thuật & Bảo trì",
    },
    "hr.skill": {
        37: "Lắp ráp khung xe", 38: "Đi dây điện - đấu nối",
        39: "Lắp cụm pin lithium", 40: "Gá - hàn chi tiết",
        41: "Sơn tĩnh điện", 42: "Vận hành máy bắt vít",
        43: "Lắp ráp trên chuyền", 44: "Đóng gói - nhập kho",
        45: "Kiểm tra xuất xưởng (KCS)", 46: "Đo kiểm kích thước",
        47: "Kiểm tra an toàn điện", 48: "Chạy thử xe (test drive)",
        49: "An toàn lao động (ATLĐ)", 50: "5S tại xưởng",
        51: "Phòng cháy chữa cháy", 52: "Quy trình đăng kiểm",
        53: "Đọc bản vẽ kỹ thuật", 54: "Bảo trì thiết bị",
        55: "Khắc phục sự cố dây chuyền", 56: "Hiệu chuẩn máy móc",
    },
    "slide.channel": {
        3: "An toàn lao động tại xưởng lắp ráp",
        4: "5S tại xưởng",
        5: "Lắp ráp khung xe - Cơ bản",
        6: "Lắp ráp trên chuyền - Cơ bản",
        7: "Lắp cụm pin lithium - An toàn và quy trình",
        8: "Đi dây điện và đấu nối",
        9: "Vận hành máy bắt vít",
        10: "Kiểm tra xuất xưởng (KCS)",
    },
    "product.template": {
        1431: "Xe máy điện Viindoo Aura",
        1432: "Xe đạp điện Viindoo Nova",
        1210: "Cụm khung sơn tĩnh điện Lumi",
        1211: "Cụm điện - bộ dây Lumi",
        1212: "Cụm khung sơn tĩnh điện Aura",
        1213: "Cụm điện - bộ dây Aura",
        1214: "Cụm khung sơn tĩnh điện Nova",
    },
    "attendance.device.location": {
        1: "Cổng xưởng lắp ráp xe điện", 2: "Văn phòng nhà máy",
    },
    "attendance.device": {
        1: "Máy chấm công ZKTeco - Cổng xưởng lắp ráp",
        2: "Máy chấm công ZKTeco - Văn phòng nhà máy",
    },
    "product.attribute": {1: "Màu xe", 2: "Phiên bản xe"},
    "product.attribute.value": {
        1: "Trắng ngọc trai", 2: "Đen nhám", 3: "Xanh rêu",
        4: "Đỏ đô", 5: "Xám xi măng", 6: "Tiêu chuẩn", 7: "Cao cấp",
    },
}

DICH_THEO_TEN = {
    "hr.job": {
        "Chuyên viên tuyển dụng": "Recruitment Specialist",
        "Kỹ thuật viên": "Technician",
        "Công nhân lắp ráp": "Assembly Worker",
        "Nhân viên QC": "QC Inspector",
        "Nhân viên kinh doanh": "Sales Executive",
        "Chuyên viên C&B": "C&B Specialist",
        "Chuyên viên Digital Marketing": "Digital Marketing Specialist",
        "Chuyên viên tài chính": "Finance Specialist",
        "Chuyên viên văn hóa doanh nghiệp": "Corporate Culture Specialist",
        "Chủ tịch Hội đồng quản trị": "Chairman of the Board",
        "Giám đốc": "Director",
        "Giám đốc kinh doanh JP": "Sales Director - JP",
        "Giám đốc kinh doanh Viindoo": "Sales Director - Viindoo",
        "Giám đốc sản xuất JP": "Production Director - JP",
        "Giám đốc sản xuất Viindoo": "Production Director - Viindoo",
        "Kiểm soát viên": "Internal Controller",
        "Kế toán bán hàng JP": "Sales Accountant - JP",
        "Kế toán bán hàng Viindoo": "Sales Accountant - Viindoo",
        "Kế toán mua hàng": "Purchase Accountant",
        "Kế toán quỹ - ngân hàng": "Cash and Bank Accountant",
        "Kế toán thuế": "Tax Accountant",
        "Kế toán trưởng": "Chief Accountant",
        "Nhân viên CSKH JP": "Customer Care Officer - JP",
        "Nhân viên CSKH Viindoo": "Customer Care Officer - Viindoo",
        "Nhân viên KCS": "Final Inspection Officer",
        "Nhân viên Media": "Media Officer",
        "Nhân viên QC kiểm soát chất lượng": "QC Officer",
        "Nhân viên Thiết kế": "Designer",
        "Nhân viên bảo hành": "Warranty Officer",
        "Nhân viên cung ứng vật tư": "Material Supply Officer",
        "Nhân viên công nợ": "Receivables Officer",
        "Nhân viên hành chính": "Administrative Officer",
        "Nhân viên kho": "Warehouse Officer",
        "Nhân viên xử lý đơn hàng": "Order Processing Officer",
        "Quản lý khu vực": "Area Manager",
        "Quản đốc phân xưởng": "Shop Floor Supervisor",
        "Trưởng ban kiểm soát": "Head of the Supervisory Board",
        "Trưởng phòng Chăm sóc khách hàng": "Customer Care Manager",
        "Trưởng phòng Hành chính - Nhân sự": "HR and Administration Manager",
        "Trưởng phòng Kỹ thuật": "Engineering Manager",
        "Trưởng phòng Marketing": "Marketing Manager",
        "Trưởng phòng Vật tư - Kho": "Materials and Warehouse Manager",
        "Tổ trưởng sản xuất": "Production Team Leader",
        "Tổ trưởng Đăng kiểm": "Vehicle Registration Team Leader",
        "Đăng kiểm viên": "Vehicle Registration Inspector",
    },
    "hr.department": {
        "Ban giám đốc": "Executive Board",
        "Ban kiểm soát": "Supervisory Board",
        "Bộ phận KCS": "Final Inspection Unit",
        "Chăm sóc khách hàng": "Customer Care",
        "Hành chính - Nhân sự": "Administration - HR",
        "Kinh doanh phía Bắc": "Sales - North",
        "Kinh doanh phía Nam": "Sales - South",
        "Kế toán - Tài chính": "Accounting - Finance",
        "Kỹ thuật": "Engineering",
        "Phòng kinh doanh": "Sales Department",
        "Phòng mua hàng": "Purchasing Department",
        "Sản xuất Khoái Châu": "Khoai Chau Production",
        "Sản xuất Yên Mỹ": "Yen My Production",
        "Vật tư - Kho": "Materials - Warehouse",
        "Đăng kiểm": "Vehicle Registration",
    },
    "hr.salary.rule.category": {
        "Cơ bản": "Basic",
        "Phụ cấp": "Allowance",
        "Tổng": "Gross",
        "Giảm trừ (trước thuế)": "Deduction (pre-tax)",
        "Cơ sở tính thuế thu nhập cá nhân": "Personal income tax base",
        "Thuế thu nhập cá nhân": "Personal income tax",
        "Giảm trừ (sau thuế)": "Deduction (post-tax)",
        "Thực lĩnh": "Net",
        "Công ty đóng góp": "Company contribution",
        "Phụ cấp (không chịu thuế)": "Allowance (non-taxable)",
        "Khác (vd: làm cơ sở cho các tính toán khác)": "Other (e.g. a base for further calculations)",
        "Phụ cấp đi lại, xăng xe": "Travel and fuel allowance",
        "Phụ cấp điện thoại": "Phone allowance",
        "Phụ cấp ăn": "Meal allowance",
        "Phụ cấp trách nhiệm": "Responsibility allowance",
        "Thưởng chuyên cần": "Attendance bonus",
        "Thưởng hiệu quả công việc": "Performance bonus",
        "Bảo hiểm người lao động (bởi NLĐ)": "Employee insurance (paid by employee)",
        "Công đoàn (NLĐ đóng)": "Trade union (paid by employee)",
        "Bảo hiểm người lao động (bởi công ty)": "Employee insurance (paid by company)",
        "Công đoàn (Công ty đóng)": "Trade union (paid by company)",
        "Trợ cấp độc hại / đặc thù nghề": "Hazard / job-specific allowance",
        "Giờ công": "Working hours",
        "Khấu trừ đặt suất ăn": "Meal order deduction",
        "Làm thêm giờ chịu thuế": "Taxable overtime",
        "Làm thêm giờ không chịu thuế": "Non-taxable overtime",
    },
    "hr.salary.rule": {
        "Lương cơ bản": "Basic salary",
        "Tổng": "Gross",
        "Lương thực lĩnh": "Net salary",
        "Phụ cấp đi lại, xăng xe": "Travel and fuel allowance",
        "Phụ cấp điện thoại": "Phone allowance",
        "Phụ cấp ăn": "Meal allowance",
        "Phụ cấp trách nhiệm": "Responsibility allowance",
        "Thưởng chuyên cần": "Attendance bonus",
        "Thưởng hiệu quả công việc": "Performance bonus",
        "Bảo hiểm xã hội NLĐ đóng": "Social insurance - employee share",
        "Bảo hiểm xã hội cty đóng": "Social insurance - company share",
        "Bảo hiểm Y tế NLĐ đóng": "Health insurance - employee share",
        "Bảo hiểm Y tế cty đóng": "Health insurance - company share",
        "Bảo hiểm thất nghiệp NLĐ đóng": "Unemployment insurance - employee share",
        "Bảo hiểm thất nghiệp cty đóng": "Unemployment insurance - company share",
        "Phí công đoàn NLĐ đóng": "Trade union fee - employee share",
        "Phí công đoàn công ty đóng": "Trade union fee - company share",
        "Giảm trừ cơ sở tính thuế thu nhập cá nhân": "Personal income tax base deduction",
        "Cơ sở tính thuế thu nhập cá nhân": "Personal income tax base",
        "Thuế thu nhập cá nhân": "Personal income tax",
        "Trợ cấp độc hại / đặc thù nghề": "Hazard / job-specific allowance",
        "Tổng tiền giờ công": "Total timesheet pay",
        "Giờ công PoW thiếu": "Missing PoW timesheet hours",
        "Tổng khấu trừ đặt suất ăn": "Total meal order deduction",
        "Làm việc ngoài giờ chịu thuế": "Taxable overtime",
        "Làm thêm giờ không chịu thuế": "Non-taxable overtime",
    },
}

# --------------------------------------------------- trường KHÔNG dịch được: đổi tên tạm
DOI_TEN = {
    # bậc kỹ năng: chỉ 4 bậc của bốn nhóm kỹ năng nhà máy (nhóm Ngôn ngữ/Kỹ năng mềm
    # vốn đã là A1..C2 / Beginner..Expert nên để nguyên)
    "hr.skill.level": {
        12: "Novice", 13: "Basic", 14: "Proficient", 15: "Expert",
        16: "Novice", 17: "Basic", 18: "Proficient", 19: "Expert",
        20: "Novice", 21: "Basic", 22: "Proficient", 23: "Expert",
        24: "Novice", 25: "Basic", 26: "Proficient", 27: "Expert",
    },
    "ir.filters": {
        15: "VIDEO HRM - C5a Payroll by month (Jul-Sep)",
        16: "VIDEO HRM - C5b Payroll by department (Sep)",
        18: "VIDEO HRM - C6 Productivity by worker (Sep)",
        19: "VIDEO HRM - C4 Finalised appraisals",
        21: "VIDEO HRM - C5c Proficient in lithium pack assembly",
        22: "VIDEO HRM - C6b Aggregate productivity by employee",
        23: "VIDEO HRM - C2b Skills of Bui Thanh Binh",
        24: "VIDEO HRM - C5c People proficient in lithium pack assembly",
        25: "VIDEO HRM - C8 Payroll by run",
        26: "VIDEO HRM - C9 October overtime",
        27: "VIDEO HRM - C10 Applicants by position",
        31: "VIDEO HRM - C9b Overtime by day (chart)",
        32: "VIDEO HRM - C3b September attendance of Binh",
        33: "VIDEO HRM - C9c Overtime by person (pivot)",
    },
    "okr.node": {
        1: "Lead the mass-market EV segment in 2026",
        2: "Raise assembly output to 20,000 vehicles a year",
        3: "Final inspection (QC) pass rate >= 99%",
        4: "Cut assembly time per vehicle by 15%",
        5: "100% of line workers certified in occupational safety",
        6: "Complete the Aura 2026 EV model",
    },
    # phiếu lương tháng 9 của Bình - hiện ở vết điều hướng VÀ ở thẻ lọc của màn `luong`
    "hr.payslip": {
        1780: "Payslip of Bui Thanh Binh for September 2026",
    },
    # tên công ty nằm ở góc phải thanh trên của MỌI màn
    "res.company": {
        1: "Viindoo Manufacturing JSC",
    },
}


# Dòng phiếu lương CHÉP tên quy tắc lương vào một trường riêng lúc tính, nên dịch
# hr.salary.rule KHÔNG đổi được chữ đã hiện trên phiếu. Chỉ dịch dòng của đúng phiếu
# xuất hiện trong clip (màn `luong`), không đụng mấy nghìn dòng của các phiếu khác.
PHIEU_LUONG_TRONG_CLIP = 1780

def kiem_truong():
    """Đọc ir.model.fields xem trường `name` của từng model có dịch được thật không.

    Đây là cái chặn sai lầm: xếp nhầm một model vào nhóm dịch được thì bản tiếng Việt
    sẽ bị kéo sang tiếng Anh mà không ai thấy cho tới lúc dựng lại clip Việt.
    """
    models = sorted(set(DICH_THEO_ID) | set(DICH_THEO_TEN) | set(DOI_TEN))
    rows = call("ir.model.fields", "search_read",
                [[["model", "in", models], ["name", "=", "name"]]],
                {"fields": ["model", "translate"]})
    co = {r["model"]: r["translate"] for r in rows}
    loi = []
    for m in set(DICH_THEO_ID) | set(DICH_THEO_TEN):
        if not co.get(m):
            loi.append(f"  {m}: xếp vào nhóm DỊCH nhưng translate={co.get(m)}")
    for m in DOI_TEN:
        if co.get(m):
            loi.append(f"  {m}: xếp vào nhóm ĐỔI TÊN nhưng translate=True (nên dịch thay vì đổi)")
    if loi:
        print("SAI PHÂN NHÓM TRƯỜNG:"); print("\n".join(loi)); sys.exit(1)
    thieu = {m: sorted(set(DICH_THEO_ID[m]) - set(VI_GOC.get(m, {}))) for m in DICH_THEO_ID}
    thieu = {m: v for m, v in thieu.items() if v}
    if thieu:
        print("THIẾU TÊN TIẾNG VIỆT GỐC:", thieu); sys.exit(1)
    print(f"kiểm trường: {len(models)} model, phân nhóm khớp ir.model.fields")


def dich(model, cap_en, cap_vi):
    """Ghi bản tiếng Anh TRƯỚC rồi mới ghi đè lại bản tiếng Việt.

    Thứ tự này là bắt buộc. en_US là ngôn ngữ GỐC của trường dịch được: khi ghi lại giá
    trị gốc, Viindoo kéo theo mọi bản dịch đang TRÙNG giá trị gốc cũ - mà dữ liệu mình bơm
    thì vi_VN đúng bằng en_US (đều tiếng Việt), nên bản Việt bị kéo sang tiếng Anh.
    Ghi vi_VN trước không cứu được vì giá trị không đổi thì Viindoo bỏ qua lượt ghi đó.
    (20/10: lần đầu làm ngược thứ tự, 321 bản ghi mất tên tiếng Việt - đã dựng lại.)
    """
    ids = sorted(cap_en)
    n = 0
    for i in ids:
        if i not in cap_vi:
            print(f"  ! {model} {i}: thiếu tên tiếng Việt gốc"); continue
        call(model, "write", [[i], {"name": cap_en[i]}], EN)
        call(model, "write", [[i], {"name": cap_vi[i]}], VI)
        n += 1
    # soát lại ngay: sai một bản ghi là hỏng âm thầm cả bản Việt lẫn bản Anh
    vi = {r["id"]: r["name"] for r in call(model, "read", [ids, ["name"]], VI)}
    en = {r["id"]: r["name"] for r in call(model, "read", [ids, ["name"]], EN)}
    lech = [i for i in ids if vi.get(i) != cap_vi.get(i) or en.get(i) != cap_en[i]]
    print(f"  {model:28} dịch {n} bản ghi" + (f"  LỆCH {lech}" if lech else ""))
    return lech


def dich_theo_ten(model, cap):
    """cap: {tên tiếng Việt: tên tiếng Anh}. Tìm bản ghi theo tên ở CẢ HAI ngôn ngữ để
    chạy lại được sau một lượt chạy hỏng (lúc đó bản ghi đang mang tên tiếng Anh)."""
    nguoc = {en: vi for vi, en in cap.items()}
    rs = call(model, "search_read", [[["name", "in", list(cap)]]],
              dict(VI, fields=["name"]))
    theo_vi = {r["id"]: r["name"] for r in rs}
    rs2 = call(model, "search_read", [[["name", "in", list(nguoc)]]],
               dict(EN, fields=["name"]))
    for r in rs2:
        theo_vi.setdefault(r["id"], nguoc[r["name"]])
    thieu = set(cap) - set(theo_vi.values())
    if thieu:
        print(f"  ! {model}: không thấy tên {sorted(thieu)}")
    cap_vi = theo_vi
    cap_en = {i: cap[v] for i, v in theo_vi.items()}
    return dich(model, cap_en, cap_vi)


def dich_dong_luong():
    """Dịch tên các dòng của phiếu lương hiện trong clip, lấy bảng từ hr.salary.rule."""
    cap = DICH_THEO_TEN["hr.salary.rule"]
    nguoc = {en: vi for vi, en in cap.items()}
    rs = call("hr.payslip.line", "search_read",
              [[["slip_id", "=", PHIEU_LUONG_TRONG_CLIP]]], dict(VI, fields=["name"]))
    cap_vi, cap_en = {}, {}
    for r in rs:
        ten = r["name"] if r["name"] in cap else nguoc.get(r["name"])
        if not ten:
            print(f"  ! hr.payslip.line {r['id']}: không có bản dịch cho {r['name']!r}"); continue
        cap_vi[r["id"]] = ten
        cap_en[r["id"]] = cap[ten]
    return dich("hr.payslip.line", cap_en, cap_vi)


def apply():
    kiem_truong()
    print("\n== Dịch các trường dịch được (bản tiếng Việt giữ nguyên) ==")
    lech = []
    for model, cap in DICH_THEO_ID.items():
        lech += [(model, i) for i in dich(model, cap, VI_GOC[model])]
    for model, cap in DICH_THEO_TEN.items():
        lech += [(model, i) for i in dich_theo_ten(model, cap)]
    lech += [("hr.payslip.line", i) for i in dich_dong_luong()]
    if lech:
        sys.exit(f"\nDỪNG: {len(lech)} bản ghi không ra đúng hai ngôn ngữ: {lech[:10]}")

    print("\n== Đổi tên tạm các trường không dịch được ==")
    luu = {}
    if os.path.exists(BACKUP):
        luu = json.load(open(BACKUP, encoding="utf-8"))
        print(f"  (đã có {BACKUP} - giữ tên gốc lần đầu, không ghi đè)")
    for model, cap in DOI_TEN.items():
        ids = sorted(cap)
        cu = {str(r["id"]): r["name"]
              for r in call(model, "read", [ids, ["name"]], VI)}
        luu.setdefault(model, cu)
        for i in ids:
            call(model, "write", [[i], {"name": cap[i]}])
        print(f"  {model:28} đổi {len(ids)} bản ghi")
    with open(BACKUP, "w", encoding="utf-8") as f:
        json.dump(luu, f, ensure_ascii=False, indent=1)
    print(f"\nđã chép tên gốc -> {BACKUP}")
    print("CHỤP XONG NHỚ CHẠY: python3 dich_en.py restore")


def restore():
    if not os.path.exists(BACKUP):
        sys.exit(f"không thấy {BACKUP} - không biết trả lại tên gì")
    luu = json.load(open(BACKUP, encoding="utf-8"))
    for model, cap in luu.items():
        for i, ten in cap.items():
            call(model, "write", [[int(i)], {"name": ten}])
        print(f"  {model:28} trả lại {len(cap)} bản ghi")
    os.rename(BACKUP, BACKUP + ".da-tra")
    print(f"\nđã trả tên tiếng Việt; chuyển {os.path.basename(BACKUP)} -> .da-tra")


def check():
    mau = [("hr.skill.type", 3), ("hr.skill", 39), ("slide.channel", 5),
           ("hr.job", 48), ("hr.department", 4), ("hr.salary.rule", 1),
           ("hr.skill.level", 14), ("ir.filters", 33), ("okr.node", 1),
           ("res.company", 1), ("hr.payslip", 1780), ("product.template", 1431)]
    for model, i in mau:
        try:
            vi = call(model, "read", [[i], ["name"]], VI)[0]["name"]
            en = call(model, "read", [[i], ["name"]], EN)[0]["name"]
            print(f"{model:26} {i:>5}  vi={vi!r}\n{'':33}en={en!r}")
        except Exception as ex:
            print(f"{model:26} {i:>5}  LỖI {str(ex)[:60]}")


if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else "check"
    {"apply": apply, "restore": restore, "check": check}[lenh]()
