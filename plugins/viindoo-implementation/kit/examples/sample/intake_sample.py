# -*- coding: utf-8 -*-
"""VÍ DỤ - dữ liệu giả định để điền sẵn workbook thu thập (build_intake_workbook.py --sample) và chạy thử nhánh A.

Có cố ý một số lỗi thường gặp để thấy phép kiểm hoạt động: đối tác trùng tên và trùng mã số thuế, công ty thiếu mã số thuế,
sản phẩm thiếu mã, đơn vị tính viết khác nhau, người thiếu quản lý trực tiếp, bước duyệt gắn đích danh người, số dư không cân,
tồn kho lệch sổ cái, tồn kho âm, sản phẩm theo dõi seri nhưng thiếu seri. Mọi tên, số là giả định.
"""

SAMPLE = {
    "company": {
        "Tên đầy đủ theo đăng ký kinh doanh": "Công ty Cổ phần Mẫu",
        "Tên viết tắt": "Công ty Mẫu",
        "Mã số thuế": "0100000000",
        "Địa chỉ": "Số 1 Đường Mẫu, Quận Mẫu, Hà Nội",
        "Chế độ kế toán (Thông tư 200 hoặc 133)": "Thông tư 200",
        "Tiền tệ hạch toán": "VND",
        "Năm tài chính (từ ngày - đến ngày)": "01/01 - 31/12",
        "Ngày chốt số dư đầu kỳ trên Viindoo": "31/12/2026",
        "Phương pháp tính giá xuất kho (bình quân, nhập trước xuất trước, đích danh)": "Bình quân",
    },
    "departments": [
        ("Ban Giám đốc", "", "Nguyễn Văn A", ""),
        ("Phòng Kế toán", "Ban Giám đốc", "Trần Thị B", ""),
        ("Phòng Kinh doanh", "Ban Giám đốc", "Lê Văn C", ""),
        ("Kho", "Phòng Kinh doanh", "", "Chưa có trưởng kho"),
    ],
    "positions": [
        ("Giám đốc", "Ban Giám đốc", "", "Duyệt đề nghị lớn, xem báo cáo"),
        ("Kế toán trưởng", "Phòng Kế toán", "Giám đốc", "Duyệt thanh toán, khoá sổ"),
        ("Kế toán viên", "Phòng Kế toán", "Kế toán trưởng", "Hoá đơn, thu chi, công nợ"),
        ("Trưởng phòng Kinh doanh", "Phòng Kinh doanh", "Giám đốc", "Duyệt đề nghị mua, đơn bán"),
        ("Nhân viên kinh doanh", "Phòng Kinh doanh", "Trưởng phòng Kinh doanh", "Báo giá, đơn bán"),
        ("Nhân viên mua hàng", "Phòng Kinh doanh", "Trưởng phòng Kinh doanh", "Đơn mua"),
        ("Thủ kho", "Kho", "", "Nhập xuất kho"),
    ],
    "people": [
        ("Nguyễn Văn A", "Ban Giám đốc", "Giám đốc", "", "Có", "a@mau.vn", ""),
        ("Trần Thị B", "Phòng Kế toán", "Kế toán trưởng", "Nguyễn Văn A", "Có", "b@mau.vn", ""),
        ("Phạm Thị D", "Phòng Kế toán", "Kế toán viên", "Trần Thị B", "Có", "d@mau.vn", ""),
        ("Lê Văn C", "Phòng Kinh doanh", "Trưởng phòng Kinh doanh", "Nguyễn Văn A", "Có", "c@mau.vn", ""),
        ("Hoàng Văn E", "Phòng Kinh doanh", "Nhân viên kinh doanh", "Lê Văn C", "Có", "e@mau.vn", ""),
        ("Vũ Thị G", "Phòng Kinh doanh", "Nhân viên mua hàng", "", "Có", "", ""),
        ("Đỗ Văn H", "Kho", "Thủ kho", "Lê Văn K", "Có", "h@mau.vn", ""),
    ],
    "approvals": [
        ("Đơn mua", 1, "Quản lý phòng ban", "", "", "Có"),
        ("Đơn mua", 2, "Nguyễn Văn A", "Giá trị trước thuế lớn hơn 100 triệu", "", "Có"),
    ],
    "partners": [
        ("", "Công ty TNHH Nhà Cung Cấp Một", "Công ty", "Nhà cung cấp", "0100000001", "Hà Nội", "", "", "30 ngày", ""),
        ("", "Công ty TNHH Nhà Cung Cấp Một", "Công ty", "Nhà cung cấp", "0100000001", "Hà Nội", "", "", "30 ngày", ""),
        ("", "Công ty CP Khách Hàng Hai", "Công ty", "Khách hàng", "", "Hải Phòng", "", "", "15 ngày", ""),
        ("", "Công ty CP Khách Hàng Ba", "Công ty", "Khách hàng", "0100000003", "Đà Nẵng", "", "", "", ""),
        ("", "Anh Khách Lẻ", "Cá nhân", "Khách hàng", "", "Hà Nội", "", "", "", ""),
    ],
    "products": [
        ("VT001", "Vật tư mẫu một", "Hàng tồn kho", "Vật tư", "Cái", "", "Không", 120000, 90000, "10%", "10%"),
        ("VT002", "Vật tư mẫu hai", "Hàng tồn kho", "Vật tư", "cái", "", "Không", 50000, 30000, "10%", "10%"),
        ("", "Vật tư mẫu ba", "Hàng tồn kho", "Vật tư", "Kg", "", "Không", 20000, 15000, "", ""),
        ("TB001", "Thiết bị mẫu", "Hàng tồn kho", "Thiết bị", "Cái", "", "Theo số seri", 25000000, 20000000, "10%", "10%"),
        ("DV001", "Dịch vụ vận chuyển", "Dịch vụ", "Dịch vụ", "Lần", "", "Không", 500000, 0, "10%", "10%"),
    ],
    "banks": [
        ("Ngân hàng Mẫu", "Chi nhánh Hà Nội", "0011000000001", "VND", "Công ty Cổ phần Mẫu", "Thu, chi", "1121"),
        ("Ngân hàng Mẫu", "Chi nhánh Hà Nội", "0011000000002", "USD", "Công ty Cổ phần Mẫu", "Thanh toán nhập khẩu", "1122"),
    ],
    "balances": [
        ("1111", "Tiền mặt", "", "", 50000000, "", "", ""),
        ("1121", "Tiền gửi ngân hàng VND", "", "", 300000000, "", "", ""),
        ("131", "Phải thu khách hàng", "Công ty CP Khách Hàng Hai", "HD0001", 80000000, "", "", ""),
        ("131", "Phải thu khách hàng", "", "", 20000000, "", "", ""),
        ("156", "Hàng hoá", "", "", 70000000, "", "", ""),
        ("211", "Tài sản cố định hữu hình", "", "", 400000000, "", "", ""),
        ("214", "Hao mòn tài sản cố định", "", "", "", 100000000, "", ""),
        ("331", "Phải trả người bán", "Công ty TNHH Nhà Cung Cấp Một", "", "", 60000000, "", ""),
        ("411", "Vốn góp của chủ sở hữu", "", "", "", 760000000, "", ""),
    ],
    "assets": [
        ("TS01", "Xe tải mẫu", "Phương tiện vận tải", 400000000, "01/01/2025", 96, 100000000, "Kho", ""),
    ],
    "warehouses": [
        ("KC", "Kho chính", "Hà Nội", "Đỗ Văn H"),
    ],
    "stock": [
        ("KC", "VT001", "Vật tư mẫu một", 500, "Cái", 90000, "", ""),
        ("KC", "VT002", "Vật tư mẫu hai", -10, "Cái", 30000, "", ""),
        ("KC", "TB001", "Thiết bị mẫu", 1, "Cái", 20000000, "", ""),
    ],
    "open_docs": [
        ("Đơn mua chưa nhận hết", "PO0001", "15/12/2026", "Công ty TNHH Nhà Cung Cấp Một", "VT001", 100, 9000000, ""),
    ],
}
