# -*- coding: utf-8 -*-
"""VÍ DỤ - việc thiết lập trên hệ thống để bộ quy trình ứng dụng chạy được (NỘI BỘ Viindoo, không gửi khách).

Bộ quy trình gửi khách chỉ ghi việc người dùng làm hằng ngày; mọi việc dựng một lần (ô bắt buộc, quy tắc tự động, loại phê duyệt,
nhóm quyền, số dư đầu kỳ, cài module) khai ở đây. Mã việc = mã trong danh mục việc của báo cáo gửi khách (project.TASK_GROUPS).
build_setup_worklist.py dựng '<Khách> - Việc thiết lập và điều chỉnh (nội bộ).html' từ tệp này cùng project.py, handbook.py.
"""

AI, NGUOI = "AI", "Tư vấn"

# Cách làm chung (ghi đầu tài liệu)
CACH_LAM = [
    "AI chỉ thiết lập, nhập liệu trên hệ thống khách khi người phụ trách đã duyệt từng lô ghi (số bản ghi, các ô sẽ đổi); làm trên bản thử trước nếu có.",
    "Xoá, huỷ, lưu trữ công ty, khoá sổ, cài module: luôn hỏi chủ nhiệm dự án riêng, không gộp vào lô ghi.",
    "Mỗi gói một mục: thống nhất quy trình của gói trước, rồi mới điều chỉnh dữ liệu và thiết lập.",
]

# Phân công từng việc của danh mục việc: mã việc -> (ai làm, làm gì cụ thể, chờ gì)
PHAN_CONG = {
    "1.1": (AI, "Tạo phòng ban, vị trí công việc; gán vị trí, phòng ban, quản lý cho từng nhân viên theo workbook đã kiểm", "Khách bổ sung quản lý trực tiếp còn thiếu"),
    "1.2": (AI, "Gán nhóm quyền theo ma trận trong bộ quy trình; người dùng theo vị trí", "1.1"),
    "2.1": (AI, "Nhập đối tác sau khi khách chọn bản giữ cho dòng trùng", "Khách sửa workbook"),
    "2.2": (AI, "Nhập sản phẩm, nhóm, đơn vị tính thống nhất", "Khách sửa workbook"),
    "2.3": (AI, "Ô bắt buộc, quy tắc tự động giao việc kiểm tra, nhiệm vụ rà soát định kỳ", "-"),
    "3.1": (AI, "Cấu hình tài khoản theo nhóm sản phẩm, thuế, phương pháp tính giá", "Kế toán trưởng chốt thiết lập"),
    "3.2": (AI, "Sổ quỹ, sổ ngân hàng; bật ngoại tệ", "-"),
    "3.3": (AI, "Loại phê duyệt Đơn mua hai bước, ngưỡng 100 triệu", "1.1"),
    "4.1": (AI, "Nhập số dư, công nợ theo đối tác ở trạng thái nháp để kế toán kiểm", "Khách gửi số dư tại ngày chốt"),
    "4.2": (AI, "Nhóm tài sản, danh sách tài sản, lịch khấu hao", "Kế toán trưởng chốt thời gian khấu hao"),
    "4.3": (AI, "Kho, tồn đầu kỳ, xử lý tồn âm", "Kiểm kê tại ngày chốt"),
    "4.4": (AI, "Nhập chứng từ dở dang còn hiệu lực", "Khách xác nhận danh sách"),
    "5.1": (AI, "Điều khoản thanh toán, nhiệm vụ nhắc nợ định kỳ", "-"),
}

# ứng dụng -> [(việc thiết lập, cấu hình gì, phục vụ mục nào của bộ quy trình, mã việc, gói)]
THIET_LAP = [
    ("Liên hệ", [
        ("Mã số thuế bắt buộc khi tạo công ty", "Đặt bắt buộc ô Mã số thuế trên form Liên hệ (đối tác là công ty)", "Mục 3A chốt chặn Khách hàng, nhà cung cấp; DT bước 2", "2.3", 1),
        ("Giao việc kiểm tra đối tác mới", "Quy tắc tự động khi tạo đối tác: hoạt động \"Kiểm tra đối tác mới\" giao Kế toán viên", "Mục 3A; DT bước 3", "2.3", 1),
    ]),
    ("Nhân viên, phân quyền", [
        ("Phòng ban, vị trí, quản lý trực tiếp", "Mỗi phòng ban có quản lý; mỗi nhân viên có vị trí, phòng ban, quản lý", "Mục 2 Quy tắc phê duyệt; PD bước 1", "1.1", 1),
        ("Bộ quyền theo vị trí", "Nhóm quyền theo ma trận mục 1; chỉ Quản trị hệ thống giữ Vai trò: Quản trị viên", "Mục 1 Ma trận phân quyền", "1.2", 1),
    ]),
    ("Phê duyệt", [
        ("Loại phê duyệt Đơn mua", "Bước 1 theo phòng ban của người trình (quản lý phòng ban); bước 2 Giám đốc khi giá trị trước thuế trên 100 triệu", "Mục 2; PD; QT01", "3.3", 1),
    ]),
    ("Kế toán", [
        ("Số dư đầu kỳ và khoá sổ", "Số dư tại ngày chốt; khoá sổ đến ngày chốt sau khi khách xác nhận", "QT03 (số dư tiền khớp sao kê)", "4.1", 1),
        ("Điều khoản thanh toán, nhắc nợ", "Điều khoản dùng chung; nhiệm vụ định kỳ \"Nhắc nợ\" hằng tuần giao Kế toán viên", "QT04", "5.1", 2),
    ]),
    ("Dự án", [
        ("Dự án \"Kiểm soát dữ liệu\"", "Nhiệm vụ định kỳ cho từng việc rà soát ở mục 3B, giao người giữ vị trí", "Mục 3B Bảng kiểm định kỳ", "2.3", 1),
    ]),
]

# module cần cài: (module kỹ thuật, tên trên Viindoo, dùng cho, gói, trạng thái trên hệ thống khách)
MODULES = [
    ("to_account_asset", "Quản lý Tài sản", "Tài sản cố định, khấu hao (việc 4.2)", 1, "Chưa cài"),
]

# Việc người làm (AI không thay được): (mã, việc, vì sao không giao AI, các gói; 0 = việc chung)
VIEC_NGUOI = [
    ("N1", "Quyết tài khoản Viindoo dùng trên hệ thống khách (tài khoản riêng, không dùng tài khoản người dùng khách)", "Quyết định tài khoản, mật khẩu", (0,)),
    ("N2", "Duyệt từng lô ghi AI báo trước", "Mọi lô ghi có người duyệt", (0,)),
    ("N3", "Chốt với kế toán trưởng: phương pháp tính giá, tài khoản theo nhóm hàng, số dư tại ngày chốt", "Quyết định nghiệp vụ của khách", (1,)),
    ("N4", "Đăng nhập thử từng vai trò, chạy thử quy trình cùng người dùng, đào tạo", "Cần người dùng khách ngồi cùng", (1, 2)),
]
