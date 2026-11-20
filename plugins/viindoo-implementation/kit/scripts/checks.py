# -*- coding: utf-8 -*-
"""Danh mục dùng chung của bước đánh giá hiện trạng - một nơi khai, ba nơi dùng:

- SHEETS : các sheet của workbook thu thập dữ liệu (khách mới, nhánh A) - mỗi sheet ghi rõ nuôi phép kiểm nào, việc thiết lập nào.
- CHECKS : các phép kiểm hiện trạng. Nhánh A chạy trên workbook khách điền (read_intake_workbook.py); nhánh B chạy trên hệ thống
           đang vận hành của khách, chỉ đọc (scan_live_system.py). Cả hai ghi cùng một dạng current_state.json.
- TASKS  : việc thiết lập chuẩn mà phép kiểm gợi ý. Danh mục việc của báo cáo gửi khách (project.py) tham chiếu mã ở đây để lấy
           sẵn mô tả, cách làm, phần khách làm, phần Viindoo làm; giờ do người tư vấn đặt trong project.py.

Không có giá, đơn giá hay định mức giờ ở đây.
"""

AREAS = ["Tổ chức, phân quyền", "Phê duyệt", "Đối tác", "Sản phẩm", "Tiền, ngân hàng", "Thiết lập kế toán", "Số dư đầu kỳ",
         "Tài sản cố định", "Kho, tồn kho", "Chứng từ dở dang"]

LEVELS = {"tot": ("Tốt", "#00B365"), "vua": ("Cần chỉnh", "#C99700"), "kem": ("Cần làm lại", "#7F4282"),
          "tt": ("Thông tin", "#8F8F8F"), "chua": ("Chưa đọc được", "#8F8F8F")}

# ------------------------------------------------------------------ việc thiết lập chuẩn
# id: (nhóm, tên việc, loại, cách điều chỉnh, [khách làm], [Viindoo làm])
TASKS = {
    "org.structure": ("Tổ chức", "Phòng ban, vị trí công việc, quản lý trực tiếp", "Dữ liệu",
                      "Phòng ban theo sơ đồ tổ chức, mỗi phòng ban có quản lý; vị trí công việc theo bộ quy trình; mỗi nhân viên có vị trí, phòng ban, quản lý trực tiếp. Đây là căn cứ để phê duyệt tự tìm đúng người duyệt",
                      ["Xác nhận sơ đồ tổ chức, danh sách nhân sự kèm vị trí, phòng ban, quản lý trực tiếp"],
                      ["Tạo hoặc chỉnh phòng ban, vị trí công việc; gán cho từng nhân viên", "Kiểm tra mỗi người tạo đề nghị thử đều tìm đúng người duyệt"]),
    "org.access": ("Tổ chức", "Bộ quyền theo vị trí công việc, gán người dùng", "Phân quyền",
                   "Một bộ quyền cho mỗi vị trí theo ma trận phân quyền tuyến tính (cấp trên có đủ quyền cấp dưới); chỉ Quản trị hệ thống giữ quyền quản trị kỹ thuật",
                   ["Duyệt ma trận phân quyền và danh sách người dùng theo vị trí", "Mỗi vị trí cử người đăng nhập thử"],
                   ["Dựng bộ quyền theo ma trận; gán người dùng vào vị trí", "Đăng nhập thử từng vai trò, chỉnh theo phản hồi"]),
    "appr.rules": ("Phê duyệt", "Loại phê duyệt và người duyệt theo vị trí", "Thiết lập",
                   "Mỗi loại chứng từ một luồng; người duyệt tìm theo vị trí, phòng ban của người trình, không gắn đích danh; ngưỡng giá trị hệ thống tự áp",
                   ["Xác nhận các loại chứng từ cần duyệt, các bước và ngưỡng giá trị"],
                   ["Tạo loại phê duyệt và các bước; lưu trữ loại cũ không dùng", "Kiểm thử đề nghị dưới và trên ngưỡng"]),
    "md.partners": ("Danh mục", "Danh mục khách hàng, nhà cung cấp", "Dữ liệu",
                    "Không trùng tên, trùng mã số thuế; công ty có mã số thuế; địa chỉ xuất hoá đơn đúng",
                    ["Chọn bản giữ cho các đối tác trùng; bổ sung mã số thuế còn thiếu"],
                    ["Xuất danh sách trùng, thiếu", "Nhập mới hoặc gộp trùng (giữ nguyên chứng từ), bổ sung mã số thuế"]),
    "md.products": ("Danh mục", "Danh mục sản phẩm, dịch vụ, đơn vị tính", "Dữ liệu",
                    "Mỗi sản phẩm có mã nội bộ, đúng nhóm, đúng đơn vị tính, thuế mặc định; không trùng",
                    ["Chọn bản giữ cho sản phẩm trùng; điền mã, nhóm theo file Viindoo gửi"],
                    ["Xuất danh sách trùng, thiếu", "Nhập mới hoặc gộp, đặt mã, chuyển nhóm; gộp đơn vị tính trùng"]),
    "md.controls": ("Danh mục", "Chốt chặn khi nhập và rà soát định kỳ", "Thiết lập",
                    "Thông tin bắt buộc khi tạo đối tác, sản phẩm; giao việc kiểm tra khi có đối tác mới; việc rà soát định kỳ giao cho vị trí phụ trách theo bộ quy trình",
                    ["Giao người kiểm soát cho từng loại dữ liệu và từng việc rà soát (theo vị trí)"],
                    ["Đặt ô bắt buộc, quy tắc tự động giao việc kiểm tra", "Tạo nhiệm vụ định kỳ cho các việc rà soát"]),
    "acc.setup": ("Kế toán", "Thiết lập kế toán: tài khoản, thuế, phương pháp tính giá", "Thiết lập",
                  "Tài khoản doanh thu, chi phí theo nhóm sản phẩm; thuế mặc định; đối soát chỉ ở tài khoản công nợ, tiền tạm thời; phương pháp tính giá thống nhất theo loại hàng",
                  ["Kế toán trưởng xác nhận chế độ kế toán, tài khoản theo nhóm hàng, phương pháp tính giá"],
                  ["Cấu hình theo thiết lập đã chốt; kiểm bút toán thử ra đúng tài khoản"]),
    "acc.bank": ("Kế toán", "Sổ quỹ, sổ ngân hàng, ngoại tệ", "Thiết lập",
                 "Mỗi tài khoản ngân hàng một sổ gắn đúng tài khoản tiền; bật ngoại tệ và tỷ giá khi có tài khoản ngoại tệ",
                 ["Gửi danh sách tài khoản ngân hàng, tiền tệ"], ["Tạo sổ quỹ, sổ ngân hàng; bật ngoại tệ, tỷ giá"]),
    "bal.opening": ("Số dư", "Số dư đầu kỳ tại ngày chốt", "Dữ liệu",
                    "Số dư từng tài khoản tại ngày chốt; công nợ theo từng đối tác, từng hoá đơn; tồn kho khớp sổ cái; khoá sổ đến ngày chốt",
                    ["Gửi bảng cân đối phát sinh, sao kê, kiểm quỹ, đối chiếu công nợ, kiểm kê tại ngày chốt", "Kế toán trưởng xác nhận số dư sau khi nhập"],
                    ["Nhập số dư, công nợ theo đối tác, tồn kho; đối chiếu với sổ cái", "Khoá sổ đến ngày chốt sau khi khách xác nhận"]),
    "bal.assets": ("Số dư", "Tài sản cố định đầu kỳ và khấu hao", "Thiết lập + Dữ liệu",
                   "Nhóm tài sản theo loại; danh sách tài sản với nguyên giá, khấu hao luỹ kế đến ngày chốt; lịch khấu hao",
                   ["Gửi danh sách tài sản; Kế toán trưởng chốt thời gian khấu hao từng nhóm"],
                   ["Cài ứng dụng tài sản nếu chưa có; tạo nhóm tài sản; nhập danh sách; chạy thử khấu hao kỳ đầu"]),
    "stock.setup": ("Kho", "Kho, địa điểm kho, tồn kho đầu kỳ", "Thiết lập + Dữ liệu",
                    "Kho và địa điểm đúng thực tế; tồn đầu kỳ theo kho, theo lô/seri, đơn giá vốn; không tồn âm",
                    ["Thủ kho xác nhận danh sách kho; kiểm kê tại ngày chốt"],
                    ["Tạo kho, địa điểm; nhập tồn đầu kỳ; xử lý tồn âm; đối chiếu giá trị kho với sổ cái"]),
    "docs.open": ("Chứng từ", "Chứng từ dở dang tại ngày chốt", "Dữ liệu",
                  "Đơn bán, đơn mua chưa giao, chưa nhận, chưa có hoá đơn được nhập hoặc đóng theo xác nhận của khách",
                  ["Xác nhận danh sách chứng từ còn hiệu lực"],
                  ["Nhập chứng từ dở dang còn hiệu lực; đóng chứng từ treo theo danh sách khách xác nhận"]),
}

# ------------------------------------------------------------------ phép kiểm
# id: (mảng, tên phép kiểm, nhánh hỗ trợ, ngưỡng "Cần làm lại" (None = chỉ thông tin), [việc gợi ý])
CHECKS = {
    "company.missing": ("Thiết lập kế toán", "Thông tin doanh nghiệp còn thiếu (mã số thuế, chế độ kế toán, ngày chốt số dư, tiền tệ)", "A", 1, ["acc.setup"]),
    "org.dept_no_manager": ("Tổ chức, phân quyền", "Phòng ban chưa có quản lý", "AB", 3, ["org.structure"]),
    "org.emp_no_manager": ("Tổ chức, phân quyền", "Nhân viên chưa có quản lý trực tiếp (ngoài người đứng đầu)", "AB", 5, ["org.structure"]),
    "org.emp_no_job": ("Tổ chức, phân quyền", "Nhân viên chưa có vị trí công việc", "AB", 5, ["org.structure"]),
    "org.manager_unknown": ("Tổ chức, phân quyền", "Quản lý trực tiếp không có trong danh sách nhân sự", "A", 1, ["org.structure"]),
    "org.job_unknown": ("Tổ chức, phân quyền", "Vị trí của nhân viên không có trong danh sách vị trí", "A", 1, ["org.structure", "org.access"]),
    "org.job_no_superior": ("Tổ chức, phân quyền", "Vị trí chưa có cấp trên (ngoài vị trí cao nhất)", "A", 1, ["org.access"]),
    "org.user_email": ("Tổ chức, phân quyền", "Người cần tài khoản thiếu email đăng nhập hoặc email trùng", "A", 1, ["org.access"]),
    "org.users_no_employee": ("Tổ chức, phân quyền", "Người dùng chưa gắn hồ sơ nhân viên", "B", 5, ["org.structure"]),
    "org.admins": ("Tổ chức, phân quyền", "Người dùng giữ quyền quản trị hệ thống", "B", 3, ["org.access"]),
    "appr.named_approver": ("Phê duyệt", "Bước duyệt gắn đích danh người thay vì vị trí, phòng ban", "AB", 3, ["appr.rules"]),
    "appr.no_threshold": ("Phê duyệt", "Ngưỡng giá trị chỉ ghi bằng chữ, chưa là điều kiện hệ thống tự áp", "A", 1, ["appr.rules"]),
    "appr.types": ("Phê duyệt", "Loại phê duyệt đang dùng", "B", None, ["appr.rules"]),
    "partner.dup_name": ("Đối tác", "Đối tác trùng tên", "AB", 10, ["md.partners", "md.controls"]),
    "partner.dup_vat": ("Đối tác", "Đối tác trùng mã số thuế", "AB", 10, ["md.partners", "md.controls"]),
    "partner.company_no_vat": ("Đối tác", "Công ty chưa có mã số thuế", "AB", 20, ["md.partners", "md.controls"]),
    "product.dup_name": ("Sản phẩm", "Sản phẩm trùng tên", "AB", 10, ["md.products", "md.controls"]),
    "product.dup_code": ("Sản phẩm", "Sản phẩm trùng mã nội bộ", "AB", 1, ["md.products", "md.controls"]),
    "product.no_code": ("Sản phẩm", "Sản phẩm chưa có mã nội bộ", "AB", 20, ["md.products", "md.controls"]),
    "product.no_category": ("Sản phẩm", "Sản phẩm chưa xếp nhóm (nằm ở nhóm gốc)", "AB", 20, ["md.products"]),
    "product.uom_variants": ("Sản phẩm", "Đơn vị tính viết khác nhau cho cùng một đơn vị", "AB", 1, ["md.products"]),
    "product.no_tax": ("Sản phẩm", "Sản phẩm chưa có thuế bán hoặc thuế mua mặc định", "AB", 10, ["md.products", "acc.setup"]),
    "bank.dup_account": ("Tiền, ngân hàng", "Số tài khoản ngân hàng khai trùng", "A", 1, ["acc.bank"]),
    "bank.accounts": ("Tiền, ngân hàng", "Tài khoản ngân hàng của công ty", "AB", None, ["acc.bank"]),
    "bank.foreign": ("Tiền, ngân hàng", "Tài khoản ngân hàng bằng ngoại tệ", "AB", None, ["acc.bank"]),
    "bank.shared_journal": ("Tiền, ngân hàng", "Sổ ngân hàng dùng chung cho nhiều tài khoản hoặc chưa gắn tài khoản tiền", "B", 1, ["acc.bank"]),
    "bank.no_statement": ("Tiền, ngân hàng", "Sổ ngân hàng chưa có sao kê nào", "B", 1, ["acc.bank"]),
    "acc.no_lock": ("Thiết lập kế toán", "Chưa đặt ngày khoá sổ", "B", 1, ["bal.opening"]),
    "acc.reconcile_misc": ("Thiết lập kế toán", "Tài khoản bật đối soát ngoài công nợ và tiền tạm thời", "B", 10, ["acc.setup"]),
    "acc.categ_same_income": ("Thiết lập kế toán", "Mọi nhóm sản phẩm cùng một tài khoản doanh thu", "B", 1, ["acc.setup"]),
    "acc.costing_mixed": ("Thiết lập kế toán", "Phương pháp tính giá hoặc cách ghi sổ kho khác nhau giữa các nhóm sản phẩm", "B", 1, ["acc.setup"]),
    "bal.not_balanced": ("Số dư đầu kỳ", "Tổng Nợ khác tổng Có của bảng số dư", "A", 1, ["bal.opening"]),
    "bal.partner_missing": ("Số dư đầu kỳ", "Dòng số dư công nợ chưa ghi đối tác", "AB", 1, ["bal.opening"]),
    "bal.partner_unknown": ("Số dư đầu kỳ", "Đối tác ở số dư không có trong danh mục đối tác", "A", 1, ["bal.opening", "md.partners"]),
    "bal.unreconciled": ("Số dư đầu kỳ", "Khoản thanh toán chưa đối trừ vào hoá đơn", "B", 20, ["bal.opening"]),
    "bal.stock_vs_gl": ("Số dư đầu kỳ", "Giá trị tồn kho lệch số dư tài khoản hàng tồn kho", "A", 1, ["bal.opening", "stock.setup"]),
    "bal.asset_vs_gl": ("Số dư đầu kỳ", "Nguyên giá, khấu hao luỹ kế tài sản lệch số dư tài khoản 211, 214", "A", 1, ["bal.opening", "bal.assets"]),
    "asset.missing": ("Tài sản cố định", "Tài sản thiếu nguyên giá, ngày bắt đầu hoặc thời gian khấu hao", "A", 1, ["bal.assets"]),
    "asset.depr_over": ("Tài sản cố định", "Khấu hao luỹ kế lớn hơn nguyên giá", "A", 1, ["bal.assets"]),
    "asset.no_app": ("Tài sản cố định", "Chưa cài ứng dụng quản lý tài sản", "B", 1, ["bal.assets"]),
    "stock.negative": ("Kho, tồn kho", "Dòng tồn kho âm", "AB", 1, ["stock.setup"]),
    "stock.unknown_product": ("Kho, tồn kho", "Sản phẩm ở tồn kho không có trong danh mục sản phẩm", "A", 1, ["stock.setup", "md.products"]),
    "stock.unknown_wh": ("Kho, tồn kho", "Kho ở tồn kho không có trong danh sách kho", "A", 1, ["stock.setup"]),
    "stock.serial_missing": ("Kho, tồn kho", "Sản phẩm theo dõi lô/seri nhưng tồn kho chưa ghi lô/seri", "A", 1, ["stock.setup"]),
    "docs.unknown_partner": ("Chứng từ dở dang", "Chứng từ dở dang có đối tác không có trong danh mục", "A", 1, ["docs.open", "md.partners"]),
    "docs.so_to_invoice": ("Chứng từ dở dang", "Đơn bán chờ lập hoá đơn", "B", None, ["docs.open"]),
    "docs.po_to_invoice": ("Chứng từ dở dang", "Đơn mua chờ hoá đơn", "B", None, ["docs.open"]),
    "docs.draft_old": ("Chứng từ dở dang", "Bút toán, hoá đơn nháp quá 30 ngày", "B", 10, ["docs.open"]),
    "docs.late_pickings": ("Chứng từ dở dang", "Phiếu kho chờ quá hạn", "B", 10, ["docs.open", "stock.setup"]),
}

# ------------------------------------------------------------------ workbook thu thập dữ liệu (nhánh A)
# Mỗi cột: (tiêu đề, bắt buộc, ghi chú cách điền, danh sách chọn hoặc None, độ rộng)
_LOAI_DT = ["Khách hàng", "Nhà cung cấp", "Khách hàng và nhà cung cấp"]
_CTY_CN = ["Công ty", "Cá nhân"]
_CO_KHONG = ["Có", "Không"]
SHEETS = [
    dict(key="company", title="1. Doanh nghiệp", form=True,
         purpose="Thông tin pháp lý và nguyên tắc kế toán dùng để thiết lập công ty trên Viindoo.",
         checks=["company.missing"], tasks=["acc.setup", "bal.opening"],
         columns=[("Thông tin", True, "", None, 34), ("Nội dung doanh nghiệp điền", True, "", None, 60), ("Ghi chú", False, "", None, 40)],
         rows=["Tên đầy đủ theo đăng ký kinh doanh", "Tên viết tắt", "Mã số thuế", "Địa chỉ", "Điện thoại", "Email", "Website",
               "Chế độ kế toán (Thông tư 200 hoặc 133)", "Tiền tệ hạch toán", "Năm tài chính (từ ngày - đến ngày)",
               "Ngày chốt số dư đầu kỳ trên Viindoo", "Phương pháp tính giá xuất kho (bình quân, nhập trước xuất trước, đích danh)",
               "Phương pháp kê khai thuế GTGT", "Chi nhánh, công ty con dùng chung hệ thống (nếu có)"],
         required_rows=["Tên đầy đủ theo đăng ký kinh doanh", "Mã số thuế", "Chế độ kế toán (Thông tư 200 hoặc 133)", "Tiền tệ hạch toán",
                        "Ngày chốt số dư đầu kỳ trên Viindoo"]),
    dict(key="departments", title="2. Phòng ban",
         purpose="Phòng ban theo sơ đồ tổ chức; quản lý phòng ban là người duyệt mặc định của nhân viên trong phòng.",
         checks=["org.dept_no_manager"], tasks=["org.structure"],
         columns=[("Phòng ban", True, "Tên theo sơ đồ tổ chức", None, 30), ("Thuộc phòng ban (cấp trên)", False, "Để trống nếu là cấp cao nhất", None, 30),
                  ("Quản lý phòng ban (họ tên)", True, "Đúng họ tên ở sheet 4. Nhân sự", None, 30), ("Ghi chú", False, "", None, 36)]),
    dict(key="positions", title="3. Vị trí công việc",
         purpose="Vị trí công việc là căn cứ phân quyền (ma trận phân quyền) và tìm người duyệt; quy trình ghi theo vị trí, không theo tên người.",
         checks=["org.job_no_superior", "org.job_unknown"], tasks=["org.structure", "org.access"],
         columns=[("Vị trí công việc", True, "Ví dụ: Kế toán viên, Thủ kho", None, 30), ("Phòng ban", True, "Đúng tên ở sheet 2", None, 26),
                  ("Vị trí cấp trên", True, "Để trống chỉ với vị trí cao nhất", None, 28),
                  ("Việc chính trên hệ thống", True, "Làm gì, duyệt gì, xem báo cáo gì", None, 50)]),
    dict(key="people", title="4. Nhân sự",
         purpose="Danh sách người, vị trí, quản lý trực tiếp; người cần tài khoản đăng nhập.",
         checks=["org.emp_no_manager", "org.emp_no_job", "org.manager_unknown", "org.job_unknown", "org.user_email"], tasks=["org.structure", "org.access"],
         columns=[("Họ tên", True, "", None, 26), ("Phòng ban", True, "Đúng tên ở sheet 2", None, 22), ("Vị trí công việc", True, "Đúng tên ở sheet 3", None, 26),
                  ("Quản lý trực tiếp (họ tên)", True, "Để trống chỉ với người đứng đầu", None, 26), ("Cần tài khoản đăng nhập", True, "", _CO_KHONG, 14),
                  ("Email đăng nhập", False, "Bắt buộc khi cần tài khoản; mỗi người một email", None, 30), ("Kiêm nhiệm vị trí (nếu có)", False, "", None, 24)]),
    dict(key="approvals", title="5. Phê duyệt",
         purpose="Loại chứng từ cần duyệt, các bước, người duyệt theo vị trí và ngưỡng giá trị.",
         checks=["appr.named_approver", "appr.no_threshold"], tasks=["appr.rules"],
         columns=[("Loại chứng từ cần duyệt", True, "Ví dụ: Đơn mua, Tạm ứng, Báo giá dưới giá bán", None, 28), ("Bước", True, "1, 2, 3...", None, 8),
                  ("Người duyệt", True, "Quản lý trực tiếp / Quản lý phòng ban / tên vị trí - không ghi tên người", None, 34),
                  ("Điều kiện áp dụng bước", False, "Ví dụ: giá trị trước thuế lớn hơn", None, 30), ("Ngưỡng giá trị (đồng)", False, "Số, để trống nếu luôn duyệt", None, 18),
                  ("Bắt buộc", True, "", _CO_KHONG, 10)]),
    dict(key="partners", title="6. Đối tác",
         purpose="Khách hàng, nhà cung cấp đang giao dịch và đối tác còn công nợ tại ngày chốt.",
         checks=["partner.dup_name", "partner.dup_vat", "partner.company_no_vat"], tasks=["md.partners", "md.controls"],
         columns=[("Mã đối tác (nếu có)", False, "", None, 14), ("Tên đầy đủ", True, "Theo đăng ký kinh doanh", None, 36), ("Công ty / Cá nhân", True, "", _CTY_CN, 13),
                  ("Loại", True, "", _LOAI_DT, 22), ("Mã số thuế", False, "Bắt buộc với công ty có hoá đơn", None, 16), ("Địa chỉ", True, "Địa chỉ xuất hoá đơn", None, 40),
                  ("Điện thoại", False, "", None, 14), ("Email", False, "", None, 24), ("Điều khoản thanh toán", False, "Ví dụ: 30 ngày", None, 18),
                  ("Người liên hệ", False, "", None, 20)]),
    dict(key="products", title="7. Sản phẩm, dịch vụ",
         purpose="Hàng hoá, vật tư, thành phẩm, dịch vụ mua và bán.",
         checks=["product.dup_name", "product.dup_code", "product.no_code", "product.no_category", "product.uom_variants", "product.no_tax"],
         tasks=["md.products", "md.controls"],
         columns=[("Mã nội bộ", True, "Mỗi sản phẩm một mã, không trùng", None, 14), ("Tên sản phẩm", True, "", None, 36),
                  ("Loại", True, "", ["Hàng tồn kho", "Hàng tiêu dùng", "Dịch vụ"], 16), ("Nhóm sản phẩm", True, "Nhóm quyết định tài khoản kế toán", None, 22),
                  ("Đơn vị tính", True, "Viết thống nhất (ví dụ Cái, Kg)", None, 12), ("Đơn vị mua (nếu khác)", False, "", None, 14),
                  ("Theo dõi", True, "", ["Không", "Theo lô", "Theo số seri"], 13), ("Giá bán", False, "", None, 14), ("Giá vốn", False, "", None, 14),
                  ("Thuế bán", False, "Ví dụ: 10%", None, 10), ("Thuế mua", False, "Ví dụ: 10%", None, 10)]),
    dict(key="banks", title="8. Tài khoản ngân hàng",
         purpose="Mỗi tài khoản ngân hàng thành một sổ ngân hàng trên Viindoo.",
         checks=["bank.dup_account", "bank.accounts", "bank.foreign"], tasks=["acc.bank"],
         columns=[("Ngân hàng", True, "", None, 22), ("Chi nhánh", False, "", None, 20), ("Số tài khoản", True, "", None, 20), ("Tiền tệ", True, "VND, USD...", None, 9),
                  ("Chủ tài khoản", True, "", None, 30), ("Mục đích", False, "Thu, chi, vay thấu chi...", None, 22), ("Tài khoản kế toán", False, "Ví dụ 1121, 1122", None, 14)]),
    dict(key="balances", title="9. Số dư đầu kỳ",
         purpose="Số dư từng tài khoản tại ngày chốt; công nợ chi tiết từng đối tác (từng hoá đơn nếu có).",
         checks=["bal.not_balanced", "bal.partner_missing", "bal.partner_unknown", "bal.stock_vs_gl", "bal.asset_vs_gl"], tasks=["bal.opening"],
         columns=[("Số tài khoản", True, "Theo chế độ kế toán đã chọn", None, 12), ("Tên tài khoản", False, "", None, 30),
                  ("Đối tác (công nợ)", False, "Bắt buộc với 131, 331, 141...; đúng tên ở sheet 6", None, 32), ("Số hoá đơn (nếu có)", False, "", None, 16),
                  ("Dư Nợ", False, "Số, đồng", None, 16), ("Dư Có", False, "Số, đồng", None, 16), ("Tiền tệ", False, "Để trống nếu VND", None, 9),
                  ("Số dư ngoại tệ", False, "", None, 14)]),
    dict(key="assets", title="10. Tài sản cố định",
         purpose="Tài sản đang dùng tại ngày chốt, để ghi tăng và lập lịch khấu hao.",
         checks=["asset.missing", "asset.depr_over", "bal.asset_vs_gl"], tasks=["bal.assets"],
         columns=[("Mã tài sản", False, "", None, 12), ("Tên tài sản", True, "", None, 32), ("Nhóm tài sản", True, "Ví dụ: Máy móc thiết bị, Phương tiện vận tải", None, 24),
                  ("Nguyên giá", True, "Số, đồng", None, 16), ("Ngày bắt đầu khấu hao", True, "dd/mm/yyyy", None, 14), ("Số tháng khấu hao", True, "", None, 12),
                  ("Khấu hao luỹ kế đến ngày chốt", True, "Số, đồng", None, 18), ("Bộ phận sử dụng", False, "", None, 20), ("Số seri", False, "", None, 16)]),
    dict(key="warehouses", title="11. Kho",
         purpose="Kho và địa điểm lưu hàng thực tế.",
         checks=["stock.unknown_wh"], tasks=["stock.setup"],
         columns=[("Mã kho", True, "Ngắn, 2-5 ký tự", None, 10), ("Tên kho", True, "", None, 28), ("Địa chỉ", False, "", None, 40), ("Thủ kho (họ tên)", False, "", None, 24)]),
    dict(key="stock", title="12. Tồn kho đầu kỳ",
         purpose="Tồn kho từng kho tại ngày chốt, kèm lô/seri và giá vốn.",
         checks=["stock.negative", "stock.unknown_product", "stock.unknown_wh", "stock.serial_missing", "bal.stock_vs_gl"], tasks=["stock.setup", "bal.opening"],
         columns=[("Mã kho", True, "Đúng mã ở sheet 11", None, 10), ("Mã sản phẩm", True, "Đúng mã ở sheet 7", None, 14), ("Tên sản phẩm", False, "", None, 32),
                  ("Số lượng", True, "", None, 12), ("Đơn vị tính", False, "", None, 11), ("Đơn giá vốn", True, "Số, đồng", None, 14),
                  ("Lô / số seri", False, "Bắt buộc với sản phẩm theo dõi lô, seri", None, 18), ("Hạn dùng", False, "dd/mm/yyyy", None, 12)]),
    dict(key="open_docs", title="13. Chứng từ dở dang",
         purpose="Đơn bán, đơn mua còn hiệu lực tại ngày chốt chưa giao, chưa nhận hoặc chưa có hoá đơn.",
         checks=["docs.unknown_partner"], tasks=["docs.open"],
         columns=[("Loại chứng từ", True, "", ["Đơn bán chưa giao hết", "Đơn bán chưa xuất hoá đơn", "Đơn mua chưa nhận hết", "Đơn mua chưa có hoá đơn", "Khác"], 26),
                  ("Số chứng từ", True, "", None, 16), ("Ngày", True, "dd/mm/yyyy", None, 12), ("Đối tác", True, "Đúng tên ở sheet 6", None, 32),
                  ("Mã sản phẩm", False, "", None, 14), ("Số lượng còn lại", False, "", None, 14), ("Giá trị còn lại", False, "Số, đồng", None, 16), ("Ghi chú", False, "", None, 30)]),
]


def sheet(key):
    return next(s for s in SHEETS if s["key"] == key)


def level(check_id, value):
    """Mức của một phép kiểm theo giá trị đếm được; None = chưa đọc được."""
    if value is None:
        return "chua"
    nguong = CHECKS[check_id][3]
    if nguong is None:
        return "tt"
    if not value:
        return "tot"
    return "kem" if value >= nguong else "vua"


def result(check_id, value, detail=(), note=""):
    area, label, _br, _ng, tasks = CHECKS[check_id]
    return {"id": check_id, "area": area, "label": label, "value": value, "level": level(check_id, value),
            "detail": list(detail)[:15], "note": note, "tasks": tasks}
