# -*- coding: utf-8 -*-
"""VÍ DỤ - dữ liệu dự án triển khai cho một khách giả định (Công ty Mẫu, khách mới - nhánh A).

Một tệp cho cả: báo cáo đánh giá hiện trạng và kế hoạch triển khai (build_assessment_report.py), danh sách việc thiết lập nội bộ
(build_setup_worklist.py), bảng nhiệm vụ dự án trên viindoo.com (export_project_tasks.py).
Khách thật: chép vào ~/Documents/project/<Khách>/work/project.py rồi viết lại. Mọi tên, ngày, giờ ở đây là giả định.
Đầu vào: phạm vi và kế hoạch trong phụ lục hợp đồng đã ký (bàn giao từ presales) - giữ đúng tổng giờ và thứ tự gói đã cam kết.
"""

CUSTOMER = "Công ty Cổ phần Mẫu"
SHORT_NAME = "Công ty Mẫu"
DATE = "20/11/2026"
VERSION = "19.0"
BRANCH = "A"                    # A: khách mới, thu thập bằng Excel; B: khách đang dùng hệ thống, rà soát chỉ đọc
OPENING_DATE = "31/12/2026"     # ngày chốt số dư đầu kỳ
WEEK1 = "2026-11-23"            # thứ Hai của tuần 1
SIGNED_HOURS = 60               # giờ trong gói Express đã ký (phụ lục hợp đồng); gói Express chỉ đếm giờ, không tính tiền theo đơn giá cấp
PROJECT_NAME = "SO.000000 - Viindoo Express - Công ty Mẫu"   # tên dự án trên viindoo.com
CONTRACT_REF = "Phụ lục 01 - Kế hoạch triển khai và Phạm vi đáp ứng"
PACKAGE_NAMES = {1: "Gói 1 - Mua hàng, kho, tiền", 2: "Gói 2 - Thu tiền, công nợ phải thu"}

# ------------------------------------------------------------------ 1. kết luận hiện trạng (gửi khách)
CONCLUSIONS = [
    ("Dữ liệu đã thu thập", "đủ danh mục đối tác, sản phẩm, kho; còn thiếu một số thông tin tổ chức và số dư cần bổ sung trước khi nhập."),
    ("Tổ chức và phê duyệt", "phê duyệt đang gắn đích danh người duyệt; chuyển sang tìm người duyệt theo vị trí để không phải sửa khi đổi nhân sự."),
    ("Cách làm", "chốt số dư tại ngày 31/12/2026, ghi sổ trên Viindoo từ kỳ 01/2027; gói 2 bắt đầu khi gói 1 đã chạy chính thức."),
]
# Ghi đè nhận xét theo mảng (tuỳ chọn). Mảng không ghi thì nhận xét lấy tự động từ kết quả phép kiểm.
AREA_NOTES = {}

# ------------------------------------------------------------------ 2. danh mục việc (gửi khách)
# Mỗi việc: code, std (mã việc chuẩn trong checks.TASKS - lấy sẵn tên, loại, cách làm, phần khách làm, phần Viindoo làm), hours.
# Ghi đè bất kỳ trường nào: name, type, method, customer, viindoo, current (hiện trạng), checks (phép kiểm gắn với việc).
TASK_GROUPS = [
    dict(code="1", name="Tổ chức và phân quyền theo vị trí công việc", package=1, tasks=[
        dict(code="1.1", std="org.structure", hours=1),
        dict(code="1.2", std="org.access", hours=1.5),
    ]),
    dict(code="2", name="Danh mục và kiểm soát dữ liệu", package=1, tasks=[
        dict(code="2.1", std="md.partners", hours=1),
        dict(code="2.2", std="md.products", hours=1.5),
        dict(code="2.3", std="md.controls", hours=1),
    ]),
    dict(code="3", name="Thiết lập kế toán, phê duyệt", package=1, tasks=[
        dict(code="3.1", std="acc.setup", hours=2),
        dict(code="3.2", std="acc.bank", hours=1),
        dict(code="3.3", std="appr.rules", hours=1),
    ]),
    dict(code="4", name="Số dư, tài sản, tồn kho đầu kỳ tại 31/12/2026", package=1, tasks=[
        dict(code="4.1", std="bal.opening", hours=3),
        dict(code="4.2", std="bal.assets", hours=1.5),
        dict(code="4.3", std="stock.setup", hours=2),
        dict(code="4.4", std="docs.open", hours=1),
    ]),
    dict(code="5", name="Thu tiền, công nợ phải thu", package=2, tasks=[
        dict(code="5.1", name="Điều khoản thanh toán, nhắc nợ", type="Thiết lập", hours=1.5,
             current="Nhắc nợ làm thủ công trên Excel", method="Điều khoản thanh toán dùng chung; báo cáo tuổi nợ; việc nhắc nợ hằng tuần giao Kế toán viên",
             customer=["Xác nhận các điều khoản thanh toán đang dùng"], viindoo=["Tạo điều khoản thanh toán; đặt nhiệm vụ nhắc nợ định kỳ"]),
    ]),
]

# ------------------------------------------------------------------ 3. kế hoạch (gửi khách; mã kế hoạch = mã nhiệm vụ "[KH] <mã> <việc>" trên viindoo.com)
# (loại, mã, việc, tuần, giờ, kết quả). loại: phase (thành nhiệm vụ cha) / sub (dòng nhóm, không thành nhiệm vụ) / item.
# giờ: số, "group:<mã nhóm việc>" (tổng giờ nhóm việc ở TASK_GROUPS) hoặc "training:<gói>" (tổng giờ đào tạo của gói).
PLAN = [
    ("phase", "0", "KHỞI ĐỘNG, ĐÁNH GIÁ HIỆN TRẠNG, LẬP KẾ HOẠCH", "", None, ""),
    ("item", "0.1", "Họp khởi động, thống nhất cách làm việc và đầu mối hai bên", "T1", 1.5, "Biên bản khởi động"),
    ("item", "0.2", "Gửi workbook thu thập dữ liệu, hướng dẫn khách điền", "T1", 1, "Workbook đã gửi"),
    ("item", "0.3", "Kiểm dữ liệu thu thập, đánh giá hiện trạng, lập kế hoạch chi tiết", "T1-T2", 3, "Báo cáo đánh giá hiện trạng và kế hoạch triển khai"),
    ("phase", "1", "GÓI 1 - MUA HÀNG, KHO, TIỀN", "", None, ""),
    ("sub", "", "Chuẩn hoá quy trình", "", None, ""),
    ("item", "1.1", "Soạn bộ quy trình ứng dụng gói 1", "T2", 4, "Bộ quy trình ứng dụng gói 1 (bản họp)"),
    ("item", "1.2", "Họp thống nhất quy trình với kế toán, mua hàng, kho", "T2", 1.5, "Quy trình đã thống nhất"),
    ("sub", "", "Thiết lập và dữ liệu", "", None, ""),
    ("item", "1.3", "Tổ chức và phân quyền theo vị trí (nhóm việc 1)", "T3", "group:1", "Bộ quyền theo vị trí, người dùng gán đúng"),
    ("item", "1.4", "Danh mục và kiểm soát dữ liệu (nhóm việc 2)", "T3", "group:2", "Danh mục không trùng; chốt chặn và rà soát định kỳ"),
    ("item", "1.5", "Thiết lập kế toán, phê duyệt (nhóm việc 3)", "T3", "group:3", "Thiết lập đúng; phê duyệt theo vị trí"),
    ("item", "1.6", "Số dư, tài sản, tồn kho đầu kỳ (nhóm việc 4)", "T5-T6", "group:4", "Số dư khớp số khách xác nhận; khoá sổ đến ngày chốt"),
    ("sub", "", "Tài liệu, đào tạo, chạy chính thức", "", None, ""),
    ("item", "1.7", "Kiểm thử: đề nghị mua đến thanh toán; đối chiếu sao kê", "T4", 1, "Các kịch bản chạy đúng"),
    ("item", "1.8", "Đào tạo theo mảng nghiệp vụ của gói 1", "T4-T5", "training:1", "Danh sách tham dự, bản ghi hình"),
    ("item", "1.9", "Chạy chính thức gói 1, hỗ trợ những ngày đầu", "T6", 2, "Gói 1 chạy chính thức"),
    ("item", "1.10", "Quản lý dự án gói 1", "T1-T6", 2, "Báo cáo tiến độ hằng tuần"),
    ("phase", "2", "GÓI 2 - THU TIỀN, CÔNG NỢ PHẢI THU", "", None, ""),
    ("item", "2.1", "Soạn và thống nhất quy trình gói 2", "T6", 2, "Quy trình gói 2 đã thống nhất"),
    ("item", "2.2", "Thu tiền, công nợ phải thu (nhóm việc 5)", "T6-T7", "group:5", "Điều khoản thanh toán, nhắc nợ định kỳ"),
    ("item", "2.3", "Đào tạo theo mảng nghiệp vụ của gói 2", "T7", "training:2", "Danh sách tham dự, bản ghi hình"),
    ("item", "2.4", "Chạy chính thức gói 2, hỗ trợ những ngày đầu", "T8", 1.5, "Gói 2 chạy chính thức"),
    ("item", "2.5", "Quản lý dự án gói 2", "T6-T8", 1, "Báo cáo tiến độ"),
    ("phase", "3", "GIÁM SÁT, HỖ TRỢ SAU CHẠY CHÍNH THỨC", "", None, ""),
    ("item", "3.1", "Giám sát, hỗ trợ vận hành; đóng sổ tháng đầu tiên cùng kế toán", "T6-T10", 6, "Vận hành ổn định, đóng sổ tháng đầu"),
]
SCOPE = [
    ("Phạm vi", "mua hàng, kho, tiền mặt - tiền gửi, thu tiền và công nợ phải thu theo phụ lục hợp đồng đã ký."),
    ("Cách làm", "mỗi gói đi trọn từ chuẩn hoá quy trình, thiết lập, dữ liệu đến đào tạo và chạy chính thức; gói sau bắt đầu khi gói trước đã chạy chính thức, "
                 "chỉ gối lên phần giám sát, hỗ trợ của gói trước."),
]

# ------------------------------------------------------------------ 4. đào tạo (theo mảng nghiệp vụ, xếp theo dòng chảy chứng từ)
# Lịch: tối đa 3 buổi/tuần, mỗi buổi 2-3 giờ; học xong một mảng mới sang mảng sau (export_project_tasks.py tự xếp buổi).
TRAINING = [
    dict(package=1, area="Mua hàng và phê duyệt", positions="Nhân viên mua hàng, Trưởng phòng Kinh doanh, Giám đốc", processes="QT01, PD, DT",
         content="Yêu cầu báo giá, đơn mua, gửi và duyệt đề nghị; tạo nhà cung cấp mới", hours=2,
         exercise="Lập một đơn mua, gửi duyệt, xác nhận", criteria="Tự làm trọn một đơn mua"),
    dict(package=1, area="Kho", positions="Thủ kho", processes="QT02 (nhận hàng)",
         content="Nhận hàng theo đơn mua, nhận thiếu, kiểm kê", hours=2,
         exercise="Nhận một đơn mua hai lần", criteria="Tồn kho khớp thực tế"),
    dict(package=1, area="Hoá đơn mua, thanh toán, tiền", positions="Kế toán viên, Kế toán trưởng", processes="QT02, QT03",
         content="Hoá đơn mua từ đơn mua, lịch thanh toán, đối chiếu sao kê, kiểm quỹ", hours=5,
         exercise="Ghi một hoá đơn mua, thanh toán, đối chiếu sao kê", criteria="Tự đối chiếu được một sao kê"),
    dict(package=2, area="Thu tiền, công nợ phải thu", positions="Kế toán viên, Nhân viên kinh doanh, Kế toán trưởng", processes="QT04",
         content="Ghi nhận khách thanh toán, đối trừ, tuổi nợ, nhắc nợ", hours=3,
         exercise="Ghi nhận một khoản trả trước và đối trừ", criteria="Tự đọc được báo cáo tuổi nợ"),
]
TRAINING_RULE = dict(per_week=3, min_hours=2, max_hours=3, weekdays=(0, 2, 4))   # thứ Hai, thứ Tư, thứ Sáu

# ------------------------------------------------------------------ 5. thông tin, dữ liệu khách cần gửi (gói, nội dung, hạn theo tuần)
CUSTOMER_INPUTS = [
    (1, "Cử chủ nhiệm dự án phía khách và đầu mối từng bộ phận: kế toán, mua hàng, kho, kinh doanh.", "T1"),
    (1, "Workbook thu thập dữ liệu đã điền: tổ chức, nhân sự, phê duyệt, đối tác, sản phẩm, ngân hàng, kho.", "T2"),
    (1, "Số dư, tài sản, tồn kho, chứng từ dở dang tại ngày chốt; sao kê và biên bản kiểm quỹ, kiểm kê.", "T5"),
    (2, "Xác nhận điều khoản thanh toán đang dùng, danh sách khách còn công nợ.", "T6"),
    (0, "Bố trí người học đủ các buổi đào tạo; thống nhất quy trình với các bộ phận.", ""),
]

# ------------------------------------------------------------------ 6. nhân sự triển khai phía Viindoo (điền người thật khi lập kế hoạch)
STAFF = [
    dict(role="Chủ nhiệm dự án", name="<Họ tên>", title="<Chức danh>", intro="", phone="<Điện thoại>", email="<email>@viindoo.com"),
    dict(role="Tư vấn triển khai", name="<Họ tên>", title="<Chức danh>", intro="", phone="<Điện thoại>", email="<email>@viindoo.com"),
]
