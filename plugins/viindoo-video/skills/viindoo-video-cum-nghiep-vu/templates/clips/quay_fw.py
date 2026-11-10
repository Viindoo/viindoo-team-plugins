"""QUAY THẬT màn Viindoo cho clip cụm Kho và chuỗi cung ứng (chép từ cụm Bán hàng + CRM) (chép engine từ cụm Trao đổi thông tin) (thay cho chụp ảnh tĩnh + kéo máy quay).

Vì sao quay được: đo ngày 29/10/2026 cho thấy Playwright **bắt được biểu đồ canvas của
Viindoo** khi chạy bằng Google Chrome thật trên máy - ghi chép cũ "canvas ra khung trắng"
không còn đúng. Rê chuột lên cột còn hiện bảng chú thích kèm con số, đẹp hơn khoanh vòng.

Vì sao không dính cảnh báo mật khẩu: cảnh báo "Mật khẩu của bạn đang là mặc định (admin)!"
chỉ bắn ở bước chuyển hướng NGAY SAU KHI ĐĂNG NHẬP (`bus/controllers/home.py`
`_login_redirect`). Nên ta đăng nhập ở một phiên riêng, lưu trạng thái phiên ra tệp, rồi
mở phiên QUAY bằng trạng thái đó - phiên quay không hề đăng nhập nên không có cảnh báo.

Chạy:  python3 quay_fw.py [tên cảnh ...]
Kết quả: quay-fw/<tên>.webm  (1920x1080) + quay-fw/<tên>-khung.png để soát nhanh
"""
import json
import os
import subprocess
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cau_hinh as CH  # đường dẫn + tài khoản demo qua biến môi trường, xem cau_hinh.py

BASE = CH.DEMO_URL
HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.environ.get("CLIP_LANG", "vi")

# Nhan man hinh cho `wait=`: ban tieng Anh thi Viindoo hien nhan tieng Anh.
# Nhan lay tu TEN HANH DONG doc o chinh may chu bang en_US, khong doan.
# Thieu mot nhan thi canh do khong cho trang nap xong, quay ra khung dang tai.
WAIT_EN = {
    "Nhiệm vụ": "Tasks", "Báo cáo quản trị": "Analytic Report",
    "Báo cáo tổng quan": "Dashboard", "Bảng giờ công": "Timesheets",
    "Bút toán": "Journal Items", "Dự án": "Projects",
    # "Hoa don" co hai loi bo dau - phai khai CA HAI, thieu mot la canh do khong cho
    # trang nap xong. Man hoa don nha cung cap trong Viindoo goi la "Bills".
    "Hoá đơn": "Invoices", "Hóa đơn": "Bills",
    "Dự toán": "Estimates", "Đơn bán": "Sales Orders", "Mua hàng": "Purchase",
    "Ngân sách": "Budgets Analysis", "Bảng tổng quan": "Dashboards",
    "Phân tích tốc độ": "Velocity Analysis", "Quy tắc tự động": "Automation Rules",
    "Xe nâng": "Forklift",
    # cum Trao doi thong tin (05/11/2026) - ten ban ghi doi tam bang demo-data/dich_en.py
    "Phòng Kinh doanh": "Sales Department", "Họp nhà cung cấp pin": "Battery supplier meeting",
    "Giao ban kinh doanh tuần": "Weekly sales meeting", "Tổng quan hoạt động": "Activity Overview",
    "Hôm nay": "Today",
    # cum Ban hang + CRM (09/11/2026) - ten ban ghi doi tam bang demo-data/dich_en.py
    "Đại lý Xe điện Long Biên": "Long Bien E-Bike Dealer", "Hỏi giá lô hàng đợt Tết": "Price request for the Tet holiday order",
    "Kinh doanh Miền Bắc": "Sales North", "Tất cả yêu cầu hỗ trợ": "All Tickets",
    "Thẻ thành viên Viindoo": "Viindoo membership card", "Khu vực bán hàng": "Sales Regions",
    "Mục tiêu doanh số": "Sales Target", "Phân tích bán hàng": "Sales Analysis", "Báo cáo bảo hành": "Warranty Claim Report",
}
WAIT_EN["Hóa đơn"] = "Invoices"   # cum nay: c09 la hoa don KHACH (action 260 "Invoices"), khong phai "Bills"

# Chu TIENG VIET nam trong bieu thuc JS cua `kich` (regex tim nut/nhom/tab) va chu go vao o tim kiem.
# Ban EN doi sang nhan tieng Anh doc tu may chu (fields_get en_US, 09/11) - thieu la bam truot im lang.
JS_EN = {"/chưa|Chưa/": "/Not Paid/", "/Thành viên/": "/Members/", "/Thêm/": "/More/",
         "/tùy chọn|Tùy chọn/": "/Optional/", "/Chưa giao/": "/Not Delivered/", "/đầu năm/": "/[Yy]ear to [Dd]ate/",
         "/Đại lý Xe điện Long Biên/": "/Long Bien E-Bike Dealer/"}
GO_EN = {"Long Biên": "Long Bien"}


# Chu tren NUT bam trong `kich` (("bam", js tim theo innerText)). Ban tieng Anh thi
# Viindoo hien chu khac -> nut khong bam duoc, ma `bam` nuot ngoai le nen man quay ra
# SAI MUC PHONG ma khong bao gi (thu 31/10: nut "Tuan" khong an, Gantt o muc "All"
# voi 121 viec thay vi 16).
NUT_EN = {"Tuần": "Week", "Tháng": "Month", "Ngày": "Day", "Năm": "Year",
          "Tất cả": "All", "Hôm nay": "Today",
          "thu nhỏ": "zoom out", "phóng to": "zoom in",
          "Toàn màn hình": "Full screen", "Đường găng": "Critical path",
          "Tin nhắn đã ghim": "Pinned Messages", "ghim": "Pinned"}


def dia_chi(c):
    """Dia chi cua mot canh, da gan tien to ngon ngu khi can.

    Trang cong khach (`khach=True`) chay tren WEBSITE chu khong phai giao dien noi
    bo, nen no theo ngon ngu mac dinh cua website (vi_VN) chu khong theo ngon ngu
    tai khoan. Ban tieng Anh phai goi /en/... - thieu tien to nay thi ca trang ra
    tieng Viet du du lieu da dich xong.
    """
    if LANG == "en" and c.get("khach"):
        return "/en" + c["url"]
    return c["url"]


def doi_nut(js):
    """Doi chu tieng Viet trong bieu thuc JS tim nut sang tieng Anh."""
    if LANG != "en":
        return js
    for vi, en in NUT_EN.items():
        js = js.replace(f"'{vi}'", f"'{en}'").replace(f'"{vi}"', f'"{en}"')
    for vi, en in JS_EN.items():
        js = js.replace(vi, en)
    return js


def nhan_cho(t):
    """Nhan chu de cho man hinh nap xong - doi theo ngon ngu giao dien."""
    if LANG != "en" or not t:
        return t
    return WAIT_EN.get(t, t)
OUT = os.path.join(HERE, "quay-fw" + ("-en" if LANG == "en" else ""))
PHIEN = os.path.join(HERE, ".phien-" + LANG + ".json")
CHROME = CH.CHROME
W, H, DSF = 1280, 720, 1.5          # 1280x720 @1.5 => khung 1920x1080, chữ to gấp 1,5

# Mỗi cảnh: địa chỉ + kịch bản thao tác. Kịch bản là danh sách bước, mỗi bước một tuple:
#   ("cho", <mili giây>)                  đứng yên
#   ("re", <js trả về phần tử>)           rê chuột tới giữa phần tử (hiện chú thích)
#   ("cuon", <số pixel>)                  cuộn dọc mượt
#   ("bam", <js trả về phần tử>)          bấm vào phần tử
#   ("xoaloc",)                           gỡ MỌI bộ lọc mặc định đang bám (vd "Nhiệm vụ của tôi")
#   ("di", x, y)                          đưa con trỏ tới toạ độ CSS - PHẢI làm trước khi cuộn
#                                         một khung có thanh cuộn riêng (vd khung 360 bên phải)
# Nhãn sơ đồ phễu nằm trong bpmn_xml của module (không dịch được) -> bản Việt đổi CHỈ TRÊN TRANG
PHEU_VI = {"Enroll Lead": "Nhận tiềm năng", "Send Drip Day 0": "Gửi email ngày 0", "Send Drip Day 3": "Gửi email ngày 3",
    "Send Drip Day 7": "Gửi email ngày 7", "Wait 3 Days": "Chờ 3 ngày", "Wait 7 Days": "Chờ 7 ngày",
    "Engaged?": "Có tương tác?", "Engaged": "Có tương tác", "Hot Lead?": "Khách nóng?", "Hot": "Nóng", "Cold": "Lạnh",
    "Not yet": "Chưa", "Assign Salesperson": "Giao nhân viên", "Convert to Opportunity": "Chuyển thành cơ hội",
    "Create Quotation": "Lập báo giá", "Converted": "Đã chuyển đổi", "Disqualified": "Loại", "New Lead": "Tiềm năng mới",
    # SVG bẻ nhãn dài thành nhiều dòng (tspan) -> khai cả từng mảnh
    "Send Drip Day": "Gửi email ngày", "Convert to": "Chuyển thành", "Opportunity": "cơ hội",
    "Assign": "Giao", "Salesperson": "nhân viên", "Create": "Lập", "Quotation": "báo giá"}


# Nhan nhom quyen chua dich trong ban 18 -> doi tren trang (chi ban VI)
QUYEN_VI = {"Operations": "Vận hành", "OPERATIONS": "VẬN HÀNH", "Sales": "Kinh doanh", "SALES": "KINH DOANH",
            "Quality": "Chất lượng", "Foreign Trade": "Ngoại thương", "Affiliate": "Cộng tác viên",
            "Loyalty": "Khách hàng thân thiết", "Người dùng: chỉ affiliates của chính mình": "Người dùng: chỉ cộng tác viên của mình",
            "Marketing Automation": "Tự động hoá marketing", "Services": "Dịch vụ", "SERVICES": "DỊCH VỤ",
            "Human Resources": "Nhân sự", "HUMAN RESOURCES": "NHÂN SỰ", "Inventory": "Kho vận", "Accounting": "Kế toán",
            "Administration": "Quản trị", "ADMINISTRATION": "QUẢN TRỊ", "Technical": "Kỹ thuật", "TECHNICAL": "KỸ THUẬT",
            "Extra Rights": "Quyền bổ sung", "Budget": "Ngân sách", "Business Trips": "Công tác", "Manufacturing": "Sản xuất", "MANUFACTURING": "SẢN XUẤT", "Website": "Trang web", "WEBSITE": "TRANG WEB", "Productivity": "Năng suất", "PRODUCTIVITY": "NĂNG SUẤT", "EXTRA RIGHTS": "QUYỀN BỔ SUNG", "Other": "Khác", "OTHER": "KHÁC"}

# cuon muot toi mot nhan/khoi (dung cho form nguoi dung, trang khach)
CUON_TOI = ("() => {const e=[...document.querySelectorAll('.o_horizontal_separator, .o_form_label, label, div')]"
            ".find(e=>e.children.length<3 && /^%s$/.test((e.innerText||'').trim())); if(!e) return 'khong thay';"
            " e.scrollIntoView({behavior:'smooth', block:'center'}); return 'ok'}")
CUON_SEL = ("() => {const e=document.querySelector('%s'); if(!e) return 'khong thay';"
            " e.scrollIntoView({behavior:'smooth', block:'center'}); return 'ok'}")

CANH = [
    # C05 Quy tac bo sung: Ac quy graphene 12V-20Ah o NM1 - ton 40, toi thieu 100, toi da 400 -> can dat 400, dat truoc ngay
    dict(name="c05-bo-sung", url="/odoo/action-397", wait=None, fav="VIDEO KHO - C05 Ắc quy cần đặt", xoa_loc=True,
         kich=[("cho", 2000), ("re", "() => document.querySelector('td[name=qty_to_order]')"), ("cho", 2500),
               ("re", "() => document.querySelector('td[name=lead_days_date]')"), ("cho", 3000)]),
    # C06 Du bao ton cua chinh san pham do (bao cao du bao tu nut tren form san pham)
    dict(name="c06-du-bao", url="/odoo/action-390/339", wait=None,
         kich=[("cho", 2000), ("bam", "() => [...document.querySelectorAll('.o-form-buttonbox button, .oe_button_box button')].find(e=>/^\\s*Thêm/.test(e.innerText))"), ("cho", 800), ("bam", "() => document.querySelector('button[name=action_product_forecast_report]')"),
               ("cho", 4000), ("di", 640, 430), ("cuon", 300), ("cho", 3500)]),
    # C07 Don ban (khach dai ly) dat 30 bo sac -> tuyen dat theo don tu sinh don mua: nut Mua hang tren don ban
    dict(name="c07-don-keo", url="/odoo/action-584/4389", wait=None, an_chu=["jvceco", "Giao hàng đúng hẹn"], an=["[name=on_time_rate]"],
         kich=[("cho", 2500), ("re", "() => document.querySelector('button[name=action_view_purchase_orders]')"), ("cho", 1500),
               ("bam", "() => document.querySelector('button[name=action_view_purchase_orders]')"), ("cho", 4500)]),
    # C08 De nghi mua hang cho duyet (APVL00073)
    dict(name="c08-de-nghi-duyet", url="/odoo/action-751/72", wait=None,
         kich=[("cho", 2500), ("re", "() => document.querySelector('.o_statusbar_status, .o_field_statusbar')"), ("cho", 3500)]),
    # C09 Hop dong khung BO00004 - gia chot, 3 dot goi hang
    dict(name="c09-hop-dong-khung", url="/odoo/action-972/4", wait=None,
         kich=[("cho", 2500), ("re", "() => document.querySelector('.oe_button_box button, .o-form-buttonbox button')"), ("cho", 1500),
               ("bam", "() => document.querySelector('.oe_button_box button, .o-form-buttonbox button')"), ("cho", 4000)]),
    # C11 Phieu nhap NM1/IN/00583: kiem dien ap truot (65V, chuan 70-74V) -> bam Xac nhan bi chan
    dict(name="c11-kiem-chan-nhap", url="/odoo/action-358/8738", wait=None, giu_thong_bao=True,
         kich=[("cho", 2500), ("re", "() => [...document.querySelectorAll('.oe_button_box button, .o-form-buttonbox button')].find(e=>/Kiểm tra|Chất lượng|Quality/i.test(e.innerText))"),
               ("cho", 1800), ("bam", "() => document.querySelector('button[name=button_validate]')"), ("cho", 1800), ("bam", "() => document.querySelector('.modal-footer .btn-primary')"), ("cho", 5000)]),
    # C12 Quet ma nhan hang: ung dung ma vach -> phieu KT/IN/00001 (lop 3.5-10, 40 cai), quet 4 lan
    dict(name="c12-quet-ma", url="/odoo/action-1700", wait=None,
         kich=[("cho", 3000), ("go", "KT/IN/00001", True),
               ("cho", 3500), ("go", "8936000820010", True), ("cho", 1300), ("go", "8936000820010", True), ("cho", 1300),
               ("go", "8936000820010", True), ("cho", 1300), ("go", "8936000820010", True), ("cho", 3500)]),
    # C13 Lo + han dung dau phanh: 3 lo, han khac nhau
    dict(name="c13-lo-han", url="/odoo/action-344", wait=None, fav="VIDEO KHO - C13 Lô dầu phanh theo hạn", xoa_loc=True,
         kich=[("cho", 2000), ("bam", "() => document.querySelector('.o_optional_columns_dropdown button, .o_optional_columns_dropdown_toggle')"), ("cho", 700), ("bam", "() => [...document.querySelectorAll('.o_optional_columns_dropdown .dropdown-item, .o-dropdown-item, .o_optional_columns_dropdown label')].find(e=>/Ngày hết hạn/.test(e.innerText))"), ("cho", 500), ("bam", "() => document.querySelector('.o_control_panel_breadcrumbs, .o_breadcrumb')"), ("cho", 1200), ("re", "() => document.querySelector('td[name=expiration_date]')"), ("cho", 3500)]),
    # C14 Hang dang di duong giua hai kho (dia diem trung chuyen) van co gia tri
    dict(name="c14-di-duong", url="/odoo/action-349", wait=None, fav="VIDEO KHO - C14 Hàng đang đi đường", xoa_loc=True,
         kich=[("cho", 2000), ("bam", "() => document.querySelector('.o_optional_columns_dropdown button, .o_optional_columns_dropdown_toggle')"), ("cho", 700), ("bam", "() => [...document.querySelectorAll('.o_optional_columns_dropdown .dropdown-item, .o-dropdown-item, .o_optional_columns_dropdown label')].find(e=>/Giá trị/.test(e.innerText))"), ("cho", 500), ("bam", "() => document.querySelector('.o_control_panel_breadcrumbs, .o_breadcrumb')"), ("cho", 1200), ("re", "() => document.querySelector('td[name=value]')"), ("cho", 3500)]),
    # C15 Xuat cho san xuat: phieu lay thanh phan KT -> NM1 truoc san xuat
    dict(name="c15-xuat-sx", url="/odoo/action-358", wait=None, fav="VIDEO KHO - C15 Xuất cho sản xuất", xoa_loc=True,
         kich=[("cho", 2500), ("bam", "() => document.querySelector('.o_data_row td.o_data_cell')"), ("cho", 4500)]),
    # C18 Gia tri ton theo kho
    dict(name="c18-gia-tri-ton", url="/odoo/action-349", wait=None, fav="VIDEO KHO - C18 Giá trị tồn theo kho", xoa_loc=True,
         kich=[("cho", 2000), ("bam", "() => document.querySelector('.o_optional_columns_dropdown button, .o_optional_columns_dropdown_toggle')"), ("cho", 700), ("bam", "() => [...document.querySelectorAll('.o_optional_columns_dropdown .dropdown-item, .o-dropdown-item, .o_optional_columns_dropdown label')].find(e=>/Giá trị/.test(e.innerText))"), ("cho", 500), ("bam", "() => document.querySelector('.o_control_panel_breadcrumbs, .o_breadcrumb')"), ("cho", 1200), ("re", "() => document.querySelector('.o_group_header')"), ("cho", 3500)]),
    # C19 Tuoi ton: so luong + gia tri theo khoang ngay
    dict(name="c19-tuoi-ton", url="/odoo/action-1036", wait=None,
         kich=[("cho", 6000), ("di", 640, 430), ("cuon", 260), ("cho", 3500)]),
    # C20 Chi phi mua ve cong vao gia von (LC/2026/0608)
    dict(name="c20-chi-phi-mua", url="/odoo/action-1024/608", wait=None,
         kich=[("cho", 2500), ("re", "() => document.querySelector('[name=amount_total]')"), ("cho", 1500),
               ("bam", "() => [...document.querySelectorAll('.o_notebook .nav-link')].find(e=>/Định giá|Phân bổ|Valuation/i.test(e.innerText))"), ("cho", 3500)]),
    # C21 Bang so lieu kho (ban tinh)
    dict(name="c21-bang-kho", url="/odoo/action-309?dashboard_id=2", wait=None,
         kich=[("cho", 7000), ("di", 800, 450), ("cuon", 500), ("cho", 3000)]),
    # C22 Kiem ke: ao mua dem 52 / may 58 -> lech -6, co don gia
    dict(name="c22-kiem-ke", url="/odoo/action-347", wait=None,
         kich=[("cho", 3000), ("bam", "() => document.querySelector('.o_searchview_input')"), ("go", "Áo mưa bộ", True), ("cho", 2500), ("re", "() => document.querySelector('td[name=inventory_diff_quantity]')"), ("cho", 3500)]),
    # C24 Duyet mua va linh vat tu
    dict(name="c24-duyet", url="/odoo/action-751", wait=None, fav="VIDEO KHO - C24 Duyệt mua và lĩnh vật tư", xoa_loc=True,
         kich=[("cho", 3000), ("cho", 3000)]),
    # C25 The kho mau S12-DN
    dict(name="c25-the-kho", url="/odoo/action-472", wait=None,
         kich=[("cho", 4000), ("cho", 2500)]),
]


# Nhan tab tieng Anh chua dich tren ho so Danh ba (09/11): doi chi tren man quay, khong sua du lieu.
DOI_CHUNG = {"Working Schedule": "Lịch làm việc", "Google Drive": "Lưu trữ tệp"}


def che_js(c):
    """JS che CHỈ TRÊN TRANG, chạy lại mỗi khi DOM đổi: ẩn phần tử (an), ẩn khối chứa chữ (an_chu),
    đổi chữ (doi). Luôn ẩn thông báo nổi (cảnh báo mật khẩu mặc định...)."""
    cfg = {"an": c.get("an", []) + ([] if c.get("giu_thong_bao") else [".o_notification_manager .o_notification"]),
           "an_chu": c.get("an_chu", []),
           "doi": (dict(DOI_CHUNG, **(c.get("doi") or {}))) if LANG == "vi" else {}}
    return """(() => { const C = %s;
      const run = () => {
        C.an.forEach(s => document.querySelectorAll(s).forEach(e => e.style.setProperty('display','none','important')));
        if (C.an_chu.length || Object.keys(C.doi).length) {
          const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let n; const hide = [];
          while ((n = w.nextNode())) {
            const t = n.nodeValue.trim();
            if (!t) continue;
            if (C.doi[t] !== undefined) n.nodeValue = n.nodeValue.replace(t, C.doi[t]);
            if (C.an_chu.some(k => t.includes(k))) hide.push(n.parentElement);
          }
          hide.forEach(e => e && (e.style.visibility = 'hidden'));
        }
      };
      const go = () => { run(); new MutationObserver(run).observe(document.body, {subtree:true, childList:true, characterData:true}); };
      if (document.body) go(); else document.addEventListener('DOMContentLoaded', go);
    })();""" % json.dumps(cfg, ensure_ascii=False)


def phien_sach(path):
    """Trạng thái phiên đã lưu, BỎ khoá last_notification_id của bus.

    Giữ khoá đó thì mỗi phiên quay mới phát lại MỌI thông báo bus kể từ lúc đăng nhập - đo
    05/11/2026: khách của các lần thử trước hiện lại thành "Khách đã tham gia kênh" và thành viên
    trực tuyến ma, dù trên máy chủ đã xoá sạch.
    """
    import json as _j
    st = _j.load(open(path))
    for o in st.get("origins", []):
        o["localStorage"] = [x for x in o.get("localStorage", []) if "last_notification_id" not in x["name"]]
    return st


def dang_nhap_luu_phien(p):
    """Dang nhap o mot phien RIENG roi luu trang thai - de phien quay khong phai dang nhap."""
    if os.path.exists(PHIEN):
        return
    b = (p.chromium.launch(headless=True, executable_path=CHROME)
         if os.path.exists(CHROME) else p.chromium.launch(headless=True))
    ctx = b.new_context(viewport={"width": W, "height": H})
    pg = ctx.new_page()
    pg.goto(BASE + "/web/login", wait_until="domcontentloaded", timeout=60000)
    _u, _p = CH.demo_login()
    pg.fill("input#login", _u)
    pg.fill("input#password", _p)
    pg.click('button.btn-primary:has-text("Đăng nhập")')
    pg.wait_for_timeout(5000)
    # Ban 18 hien KHONG gan lang tren the html nua (do 05/11/2026) -> hoi thang phien dang nhap
    ma = (pg.get_attribute("html", "lang") or "").replace("-", "_")
    if not ma:
        ma = pg.evaluate("""async () => { const r = await fetch('/web/session/get_session_info',
            {method:'POST', headers:{'Content-Type':'application/json'},
             body: JSON.stringify({jsonrpc:'2.0', method:'call', params:{}})});
            return (await r.json()).result.user_context.lang; }""") or ""
    mong = "en_US" if LANG == "en" else "vi_VN"
    if not ma.lower().startswith(mong.split("_")[0].lower()):
        ctx.close(); b.close()
        sys.exit(f"NGON NGU GIAO DIEN dang la {ma!r} ma CLIP_LANG={LANG} "
                 f"(can {mong}). Chay: python3 ../demo-data/doi_ngon_ngu.py "
                 f"{'en' if LANG == 'en' else 'vi'}")
    ctx.storage_state(path=PHIEN)
    ctx.close()
    b.close()
    print(f"da dang nhap ({ma}) va luu phien ->", os.path.basename(PHIEN))


# Ten bo loc da luu sau khi chay dich_en_duan.py apply. quay_fw.py bam bo loc BANG
# DUNG CAI TEN, nen thieu bang nay thi canh quay ban Anh lay nham tap ban ghi ma
# khong bao loi gi (bat_bo_loc nuot ngoai le, chi in mot dong).
FAV_EN = {  # ten bo loc sau demo-data/dich_en.py apply (ir.filters 54-61)
    "VIDEO BH-CRM - C09 Hoá đơn của khách": "VIDEO SALES-CRM - C09 Customer invoices",
    "VIDEO BH-CRM - C10 Hỗ trợ của khách": "VIDEO SALES-CRM - C10 Customer tickets",
    "VIDEO BH-CRM - C19 Doanh số theo nhân viên": "VIDEO SALES-CRM - C19 Sales by salesperson",
    "VIDEO BH-CRM - C22 Bảo hành theo sản phẩm": "VIDEO SALES-CRM - C22 Warranty by product",
    "VIDEO BH-CRM - C11 Thẻ thành viên của khách": "VIDEO SALES-CRM - C11 Customer membership card",
    "VIDEO BH-CRM - C15 Khách mới tự chia": "VIDEO SALES-CRM - C15 New leads auto-assigned",
    "VIDEO BH-CRM - C28 Đơn của tôi theo giao hàng": "VIDEO SALES-CRM - C28 My orders by delivery",
}


# Bo loc da duoc dich_en.py dat lam MAC DINH khi quay ban EN -> bam vao la TAT no di.
FAV_MAC_DINH_EN = set()


def bat_bo_loc(pg, ten):
    if not ten:
        return
    if LANG == "en" and ten in FAV_MAC_DINH_EN:
        return
    if LANG == "en":
        if ten not in FAV_EN and QUET:
            FAV_EN[ten] = ten
        if ten not in FAV_EN:
            sys.exit(f"thieu ten tieng Anh cho bo loc {ten!r} - bo sung vao FAV_EN")
        ten = FAV_EN[ten]
    try:
        pg.click(".o_searchview_dropdown_toggler, .o_dropdown_toggler_btn", timeout=8000)
        pg.click(f'span[role="menuitemcheckbox"]:has-text("{ten}")', timeout=8000)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(1500)
    except Exception as e:
        try:
            pg.screenshot(path=os.path.join(OUT, "_loi-bo-loc.png"))
        except Exception:
            pass
        # KHONG nuot: bam truot nghia la man quay ra tap ban ghi SAI, va day dung la
        # cach ban tieng Anh 01/11/2026 hong ma khong ai biet. Dung han, bao ro.
        sys.exit(f"BAM BO LOC TRUOT: {ten!r} ({str(e).splitlines()[0][:70]})\n"
                 f"  -> bo loc tren may chu con mang ten tieng Viet?\n"
                 f"  -> chay: (chua co script dich ban EN cho cum nay)")


# May chu demo tu 23:29 05/11/2026 loi "column viin_approval_request.discount does not
# exist" (cap nhat ma nguon ma chua nang cap module). /mail/data hoi systray_get_activities ->
# dem viec cua MOI model -> cham phieu duyet -> loi, va MOI trang bat hop thoai "Oops!". Bo dung
# yeu cau con do (bieu tuong hoat dong tren thanh tren cung mat so dem), giu nguyen phan con lai.
def bo_systray_loi(route):
    req = route.request
    try:
        d = json.loads(req.post_data or "{}")
        if d.get("params", {}).get("systray_get_activities"):
            d["params"]["systray_get_activities"] = False
            return route.continue_(post_data=json.dumps(d))
    except Exception:
        pass
    route.continue_()


# QUET=1: ghi moi dong chu co dau tieng Viet nhin thay trong tung canh -> <OUT>/_quet.json
# (soat du lieu chua dich TRUOC khi quay that ban tieng Anh - luat "quet HET roi moi quay")
QUET = os.environ.get("QUET") == "1"
_QUET_KQ = {}
_QUET_JS = ("() => (document.body ? document.body.innerText : '').split('\\n')"
            ".map(s => s.trim()).filter(s => /[\u00c0-\u1ef9]/.test(s) && /[\u0102\u0103\u0110\u0111\u01a0\u01a1\u01af\u01b0\u1ea0-\u1ef9\u00e0-\u00e3\u00e8-\u00ea\u00ec\u00ed\u00f2-\u00f5\u00f9\u00fa\u00fd]/i.test(s))")
_QUET_CANH = [None]


def quet(pg):
    if not QUET or not _QUET_CANH[0]:
        return
    try:
        for t in pg.evaluate(_QUET_JS):
            _QUET_KQ.setdefault(_QUET_CANH[0], set()).add(t[:160])
    except Exception:
        pass


def chay_kich(pg, kich):
    for buoc in kich:
        quet(pg)
        viec = buoc[0]
        if viec == "cho":
            pg.wait_for_timeout(buoc[1])
        elif viec == "mo":
            pg.goto(BASE + buoc[1] + ("&" if "?" in buoc[1] else "?") + "cids=1", wait_until="domcontentloaded", timeout=90000)
            pg.wait_for_timeout(buoc[2] if len(buoc) > 2 else 3000)
        elif viec == "loc":
            bat_bo_loc(pg, buoc[1])
        elif viec == "cho_sel":
            try:
                pg.wait_for_selector(buoc[1], timeout=30000)
            except Exception:
                print("    (khong thay", buoc[1], ")")
        elif viec == "di":
            pg.mouse.move(buoc[1], buoc[2], steps=14)
            pg.wait_for_timeout(300)
        elif viec == "cuon":
            # cuon MUOT tung nhip nho, cuon giat mot phat nhin rat xau tren video
            for _ in range(12):
                pg.mouse.wheel(0, buoc[1] / 12)
                pg.wait_for_timeout(45)
        elif viec == "re":
            try:
                el = pg.evaluate_handle(doi_nut(buoc[1])).as_element()
                if el:
                    box = el.bounding_box()
                    if box:
                        pg.mouse.move(box["x"] + box["width"] * 0.22,
                                      box["y"] + box["height"] * 0.45, steps=28)
            except Exception as e:
                print("    (re chuot hong:", str(e).splitlines()[0][:70], ")")
        elif viec == "xoaloc":
            # Odoo bam san mot so bo loc mac dinh (vd "Nhiem vu cua toi"). PHAI CHO cho
            # thanh tim kiem dung xong roi moi go - man Gantt mat ~9 giay moi co facet,
            # go o giay 1,5 thi khong co gi de bam va canh quay ra nham tap ban ghi.
            try:
                pg.wait_for_selector(".o_facet_remove", timeout=20000)
            except Exception:
                pass
            for _ in range(8):
                x = pg.query_selector(".o_facet_remove")
                if not x:
                    break
                try:
                    x.click()
                except Exception:
                    break
                pg.wait_for_timeout(700)
        elif viec == "go":
            # go chu tung phim nhu nguoi that (vd o tim kiem), roi Enter neu co
            try:
                pg.keyboard.type(GO_EN.get(buoc[1], buoc[1]) if LANG == "en" else buoc[1], delay=90)
                if len(buoc) > 2 and buoc[2]:
                    pg.keyboard.press("Enter")
            except Exception as e:
                print("    (go hong:", str(e).splitlines()[0][:70], ")")
        elif viec == "js":
            # chay JS thuan, khong bam gi - dung de keo thanh cuon, dat lai vi tri...
            try:
                print("    js ->", pg.evaluate(doi_nut(buoc[1])))
            except Exception as e:
                print("    (js hong:", str(e).splitlines()[0][:70], ")")
        elif viec == "bam":
            try:
                el = pg.evaluate_handle(doi_nut(buoc[1])).as_element()
                if el:
                    # 09/11 ban EN: chu thich noi "Email" de len tieu de nhom -> click thuong cho 30s roi hong.
                    # Cho toi da 4s, khong duoc thi bam bang JS (van dung phan tu do).
                    try:
                        el.click(timeout=4000)
                    except Exception:
                        el.evaluate("e => e.click()")
                        print("    (bam bang JS)")
            except Exception as e:
                print("    (bam hong:", str(e).splitlines()[0][:70], ")")


def main():
    os.makedirs(OUT, exist_ok=True)
    chon = [x for x in sys.argv[1:] if not x.startswith("-")]
    danh_sach = [c for c in CANH if not chon or c["name"] in chon]

    with sync_playwright() as p:
        dang_nhap_luu_phien(p)
        # --force-device-scale-factor: ep Chrome VE o 1,5 lan -> chu to gap ruoi VA video
        # ra dung 1920x1080. Dat device_scale_factor cua Playwright khong co tac dung voi
        # video: noi dung bi ve o kich thuoc CSS roi dat vao goc tren trai khung quay.
        args = [f"--force-device-scale-factor={DSF}"]
        b = (p.chromium.launch(headless=True, executable_path=CHROME, args=args)
             if os.path.exists(CHROME) else p.chromium.launch(headless=True, args=args))
        for c in danh_sach:
            # moi canh mot ngu canh rieng -> moi canh mot tep video rieng
            ctx = b.new_context(viewport={"width": W, "height": H},
                                **({} if c.get("khach") else {"storage_state": phien_sach(PHIEN)}),
                                record_video_dir=OUT,
                                record_video_size={"width": int(W * DSF),
                                                   "height": int(H * DSF)})
            ctx.route("**/mail/data", bo_systray_loi)
            ctx.add_init_script(che_js(c))
            pg = ctx.new_page()
            _QUET_CANH[0] = c["name"]
            try:
                if c.get("pre"):
                    pg.goto(BASE + c["pre"] + ("&" if "?" in c["pre"] else "?") + "cids=1",
                            wait_until="domcontentloaded", timeout=90000)
                    pg.wait_for_timeout(1800)
                pg.goto(BASE + dia_chi(c) + ("&" if "?" in c["url"] else "?") + "cids=1",
                        wait_until="domcontentloaded", timeout=90000)
                cho = nhan_cho(c.get("wait"))
                if cho:
                    try:
                        pg.wait_for_selector(f"text={cho}", timeout=40000)
                    except Exception:
                        print(f"    (khong thay chu cho '{cho}')")
                pg.wait_for_timeout(2500)
                if c.get("xoa_loc") and c.get("fav"):
                    chay_kich(pg, [("xoaloc",)])
                bat_bo_loc(pg, c.get("fav"))
                chay_kich(pg, c["kich"])
                quet(pg)
                # khung hinh cuoi de soat nhanh khoi phai mo video
                pg.screenshot(path=os.path.join(OUT, c["name"] + "-khung.png"))
            except Exception as e:
                print(f"  {c['name']:22} LOI: {str(e).splitlines()[0][:110]}")
            vid = pg.video.path() if pg.video else None
            ctx.close()
            if vid and os.path.exists(vid):
                dich = os.path.join(OUT, c["name"] + ".webm")
                os.replace(vid, dich)
                kb = os.path.getsize(dich) // 1024
                print(f"  {c['name']:22} -> {os.path.basename(dich)}  ({kb} KB)")
        b.close()
    if QUET:
        f = os.path.join(OUT, "_quet.json")
        cu = json.load(open(f)) if os.path.exists(f) else {}
        cu.update({k: sorted(v) for k, v in _QUET_KQ.items()})
        json.dump(cu, open(f, "w"), ensure_ascii=False, indent=1)
        print("quet ->", f, sum(len(v) for v in _QUET_KQ.values()), "dong")
    print("\nxong. video o:", OUT)


if __name__ == "__main__":
    main()
