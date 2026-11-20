# -*- coding: utf-8 -*-
"""VÍ DỤ - nội dung bộ quy trình ứng dụng Viindoo cho một khách giả định (Công ty Mẫu).

Đây là tệp mẫu để chạy thử và để chép làm khung cho khách mới: mọi tên, con số, ngưỡng là giả định.
Khách thật: chép tệp này vào thư mục dữ liệu dự án (~/Documents/project/<Khách>/work/handbook.py) rồi viết lại toàn bộ nội dung
theo quy trình đã thống nhất với khách. Lược đồ đầy đủ: skills/viindoo-quy-trinh-ung-dung/references/luoc-do-handbook.md.

Nguyên tắc nội dung (bắt buộc với mọi khách):
- Tài liệu để người dùng hiểu vận hành HẰNG NGÀY. Việc dựng một lần (ô bắt buộc, quy tắc tự động, cài module, số dư đầu kỳ)
  không ghi ở đây mà ghi ở setup_tasks.py (nội bộ) và danh mục việc của báo cáo gửi khách.
- Chỉ ghi vị trí công việc, không ghi tên người. Tên mục, tên nhóm quyền đúng chữ trên giao diện phiên bản khách chạy (groups.json).
- Mỗi mục, mỗi quy trình, mỗi bước có liên kết tài liệu hướng dẫn Viindoo đúng phiên bản (kiểm ngoại tuyến bằng doc_link_check).
"""

NGAY = "20/11/2026"
KHACH = "Công ty Cổ phần Mẫu"
KHACH_NGAN = "Công ty Mẫu"
CAN_CU = "sơ đồ tổ chức và quy định phê duyệt của Công ty; báo cáo đánh giá hiện trạng và kế hoạch triển khai"
GOI_TEN = {1: "Gói 1 - Mua hàng, kho, tiền", 2: "Gói 2 - Thu tiền, công nợ phải thu"}

# ------------------------------------------------------------------ vị trí công việc (làn sơ đồ)
GD = "Giám đốc"
KTT = "Kế toán trưởng"
KTV = "Kế toán viên"
TPKD = "Trưởng phòng Kinh doanh"
NVKD = "Nhân viên kinh doanh"
NVMH = "Nhân viên mua hàng"
TK = "Thủ kho"
QTHT = "Quản trị hệ thống"
HT = "Hệ thống (tự động)"
TBP = "Trưởng bộ phận của người trình"
NLD = "Người lập chứng từ"

VI_TRI = [
    (GD, "Duyệt đề nghị trên 100 triệu đồng; xem báo cáo điều hành"),
    (KTT, "Duyệt đề nghị của phòng Kế toán; duyệt lịch thanh toán; khoá sổ; tạo điều khoản thanh toán"),
    (KTV, "Hoá đơn mua, bán; thu chi, ngân hàng; đối trừ công nợ; kiểm soát danh mục"),
    (TPKD, "Duyệt đề nghị của phòng Kinh doanh; quản lý bảng giá; xem công nợ khách"),
    (NVKD, "Báo giá, đơn bán; nhắc khách thanh toán"),
    (NVMH, "Yêu cầu báo giá, đơn mua; xác nhận dịch vụ đã nhận"),
    (TK, "Nhập, xuất kho; kiểm kê"),
    (QTHT, "Người dùng, phân quyền, loại phê duyệt, thiết lập hệ thống"),
]

# ------------------------------------------------------------------ ma trận phân quyền
# Tên mục và tên nhóm quyền ghi ĐÚNG như màn hình phân quyền người dùng của phiên bản khách chạy (groups.json).
# "-" = không chọn. Nhóm dạng ô đánh dấu ghi "Có".
VT_MT = [GD, KTT, KTV, TPKD, NVKD, NVMH, TK, QTHT]
_QTV = "Quản trị viên"
_S1, _S2 = "Người dùng: Chỉ tài liệu của chính mình", "Người dùng: Tất cả tài liệu"
MA_TRAN = [
    ("Bán hàng", [
        ("Bán hàng", None, [_QTV, _S2, _S2, _QTV, _S1, "-", "-", _QTV]),
    ]),
    ("Mua hàng, tồn kho, sản phẩm", [
        ("Mua hàng", None, [_QTV, _QTV, "Người dùng", _QTV, "-", "Người dùng", "-", _QTV]),
        ("Tồn kho", None, [_QTV, _QTV, "Người dùng", _QTV, "-", "Người dùng", "Người dùng", _QTV]),
        ("Sản phẩm", "Tạo", ["Có", "Có", "Có", "Có", "-", "-", "-", "Có"]),
    ]),
    ("Kế toán, phê duyệt, liên hệ, vai trò", [
        ("Kế toán", None, [_QTV, _QTV, "Kế toán chứng từ", "Hóa đơn", "-", "-", "-", _QTV]),
        ("Phê duyệt", None, [_QTV, "Cán bộ", "-", "Cán bộ", "-", "-", "-", _QTV]),
        ("Liên hệ", "Tạo", ["Có", "Có", "Có", "Có", "Có", "Có", "-", "Có"]),
        ("Vai trò", None, ["Người dùng"] * 7 + [_QTV]),
    ]),
]
GHI_CHU_MT = [
    "Tên mục và tên nhóm quyền ghi đúng như màn hình phân quyền người dùng trên Viindoo.",
    "\"-\": không chọn. Người dùng nội bộ không chọn nhóm vẫn tạo và theo dõi được đề nghị phê duyệt của chính mình.",
    "\"Có\": đánh dấu nhóm quyền ghi ở cột Ứng dụng.",
]
# Cây quản lý (vị trí -> cấp trên); đúng một vị trí cao nhất không có cấp trên.
CAP_TREN = {KTT: GD, TPKD: GD, QTHT: GD, KTV: KTT, NVKD: TPKD, NVMH: TPKD, TK: TPKD}
# Ngoại lệ không kế thừa: quản trị kỹ thuật chỉ Quản trị hệ thống giữ.
NGOAI_LE_KE_THUA = {"Vai trò"}

CHU_GIAI = [
    ("Bán hàng", "Người dùng: Chỉ tài liệu của chính mình -> Người dùng: Tất cả tài liệu -> Quản trị viên."),
    ("Mua hàng", "Người dùng -> Quản trị viên."),
    ("Tồn kho", "Người dùng -> Quản trị viên. Kho, địa điểm kho chỉ Quản trị viên tạo được."),
    ("Sản phẩm", "Tạo: tạo, sửa sản phẩm, nhóm sản phẩm, đơn vị tính."),
    ("Kế toán", "Hóa đơn -> Hóa đơn & Ngân hàng -> Kế toán chứng từ -> Quản trị viên. Điều khoản thanh toán, thuế, ngày khoá sổ chỉ Quản trị viên sửa được."),
    ("Phê duyệt", "Duyệt cho nhóm -> Cán bộ -> Quản trị viên (cấu hình loại phê duyệt). Người duyệt theo phòng ban phải có cấp Cán bộ."),
    ("Liên hệ", "Tạo: tạo, sửa khách hàng, nhà cung cấp."),
    ("Vai trò", "Người dùng -> Quản trị viên (Thiết lập, quyền truy cập: tạo người dùng, phân quyền)."),
]
NGUYEN_TAC = [
    "Phân quyền tuyến tính: cấp trên luôn có đủ quyền của các vị trí dưới mình, cộng thêm Quản trị viên ở các mục thuộc lĩnh vực mình phụ trách. "
    "Ngoại lệ: quản trị kỹ thuật hệ thống (tạo người dùng, sửa phân quyền) chỉ Quản trị hệ thống làm.",
    "Người mới hoặc người thay thế được Quản trị hệ thống gán vị trí là có đủ quyền đúng quy trình; người kiêm nhiều vị trí được gán nhiều vị trí.",
    "Danh sách ai giữ vị trí nào do Công ty quản lý và cập nhật khi thay đổi nhân sự, không ghi trong tài liệu quy trình.",
]
GIOI_HAN = [
    "Nhân viên kinh doanh chỉ thấy báo giá, đơn bán của mình; Trưởng phòng Kinh doanh, Giám đốc thấy tất cả.",
    "Chỉ Quản trị hệ thống sửa được người dùng, phân quyền.",
]
PHE_DUYET = [
    "Áp dụng cho đơn mua. Người trình chọn loại phê duyệt \"Đơn mua\", không phải chọn người duyệt; hệ thống tự tìm theo người trình.",
    "Bước 1 - Trưởng bộ phận của người trình duyệt (quản lý phòng ban của người trình).",
    "Bước 2 - Giám đốc duyệt khi giá trị trước thuế lớn hơn 100 triệu đồng.",
    "Chưa duyệt đủ thì không xác nhận được đơn mua. Bị từ chối ở bước nào thì đề nghị dừng ở bước đó, người trình sửa rồi gửi lại.",
]

# ------------------------------------------------------------------ quy trình
# Mỗi quy trình: code, goi, ten, muc_tieu, bat_dau, ket_thuc, luong, buoc[(vị trí, nhiệm vụ, thao tác trên Viindoo, ngoài phần mềm)]
QUY_TRINH = [
    dict(code="QT01", goi=1, ten="Đề nghị mua, phê duyệt, đơn mua",
         muc_tieu="Mọi khoản mua đều có đơn mua được duyệt đúng cấp trước khi đặt hàng; kế toán thấy được đơn mua.",
         bat_dau="Phát sinh nhu cầu mua hàng, dịch vụ.",
         ket_thuc="Đơn mua đã duyệt đủ cấp, đã xác nhận và gửi nhà cung cấp.",
         luong="Nhân viên mua hàng kiểm, tạo nhà cung cấp theo quy trình con DT, tạo yêu cầu báo giá -> gửi phê duyệt theo quy trình con PD "
               "-> bị từ chối thì sửa, gửi lại; được duyệt thì xác nhận đơn mua, gửi nhà cung cấp -> Kế toán viên kiểm tra",
         buoc=[
             (NVMH, "Tạo yêu cầu báo giá", "Mua hàng > Đơn hàng > Yêu cầu báo giá > Mới: Nhà cung cấp, Ngày dự kiến nhận; dòng sản phẩm: Sản phẩm, Số lượng, Đơn giá, Thuế",
              "Lấy báo giá của nhà cung cấp"),
             (NVMH, "Đính kèm báo giá của nhà cung cấp", "Biểu tượng đính kèm trên chứng từ > tải lên file báo giá", "-"),
             (NVMH, "Gửi phê duyệt loại Đơn mua (theo quy trình con PD)", "Nút tạo đề nghị phê duyệt trên đơn mua, loại phê duyệt \"Đơn mua\" > Gửi phê duyệt", "-"),
             (NVMH, "Sửa theo lý do từ chối, gửi phê duyệt lại", "Mở đơn mua > sửa theo lý do từ chối > Gửi phê duyệt lại", "Trao đổi lại với người duyệt nếu cần"),
             (NVMH, "Xác nhận đơn mua khi đã duyệt đủ", "Mở đơn mua > Xác nhận đơn hàng", "-"),
             (NVMH, "Gửi đơn mua cho nhà cung cấp", "Gửi PO (gửi email từ hệ thống) hoặc in đơn mua", "Ký, gửi đơn đặt hàng nếu nhà cung cấp yêu cầu bản ký"),
             (KTV, "Kiểm tra đơn mua đã xác nhận: giá, thuế, điều khoản thanh toán", "Mua hàng > Đơn hàng > Đơn mua: lọc theo trạng thái; ghi nhận xét vào trao đổi trên đơn nếu sai", "-"),
         ]),
    dict(code="QT02", goi=1, ten="Nhận hàng, dịch vụ; hoá đơn mua; thanh toán nhà cung cấp",
         muc_tieu="Nhận đúng hàng theo đơn; hoá đơn mua đủ chứng từ, đúng tài khoản; trả tiền đúng hạn và đối trừ đúng hoá đơn.",
         bat_dau="Nhà cung cấp giao hàng hoặc hoàn thành dịch vụ theo đơn mua đã xác nhận.",
         ket_thuc="Hoá đơn mua đã ghi sổ, đã thanh toán và đối trừ.",
         luong="Thủ kho xác nhận phiếu nhập kho hoặc Nhân viên mua hàng xác nhận dịch vụ -> Kế toán viên tạo hoá đơn mua từ đơn mua, kiểm chứng từ, ghi sổ "
               "-> đến hạn: Kế toán trưởng duyệt lịch thanh toán, Kế toán viên ghi nhận thanh toán",
         buoc=[
             (TK, "Nhận hàng: kiểm số lượng, chủng loại theo đơn mua", "Tồn kho > Nghiệp vụ > Phiếu nhập kho > mở phiếu theo số đơn mua",
              "Kiểm đếm hàng thực tế; ký biên bản giao nhận với nhà cung cấp"),
             (TK, "Xác nhận phiếu nhập kho", "Nhập Số lượng thực nhận > Xác nhận; nhận thiếu thì chọn tạo phiếu nhận phần còn lại hoặc không", "-"),
             (NVMH, "Xác nhận dịch vụ đã nhận", "Mở đơn mua > dòng dịch vụ: nhập Số lượng đã nhận", "Xác nhận khối lượng với nhà cung cấp"),
             (KTV, "Nhận hoá đơn và chứng từ của nhà cung cấp", "-", "Nhận hoá đơn GTGT, biên bản giao nhận"),
             (KTV, "Tạo hoá đơn mua từ đơn mua", "Mua hàng > Đơn hàng > Đơn mua > mở đơn > Tạo hóa đơn", "-"),
             (KTV, "Nhập thông tin hoá đơn, đính kèm chứng từ", "Hóa đơn mua hàng: Số hoá đơn, Ngày hoá đơn, Ngày kế toán; kiểm Số lượng, Đơn giá, Thuế; "
              "biểu tượng đính kèm > tải lên hoá đơn GTGT", "-"),
             (KTV, "Ghi sổ hoá đơn mua", "Nút Xác nhận", "-"),
             (KTV, "Lập lịch thanh toán theo hạn", "Kế toán > Nhà cung cấp > Hóa đơn mua hàng: lọc hoá đơn đến hạn", "Trình Kế toán trưởng lịch thanh toán"),
             (KTT, "Duyệt lịch thanh toán", "-", "Duyệt theo quy định tài chính của Công ty"),
             (KTV, "Thanh toán hoá đơn mua", "Mở hoá đơn mua > Thanh toán: Sổ nhật ký, Ngày thanh toán, Số tiền > Tạo thanh toán",
              "Chuyển khoản trên ngân hàng điện tử"),
         ]),
    dict(code="QT03", goi=1, ten="Tiền mặt, tiền gửi: thu chi, đối chiếu sao kê",
         luu_y=["Mỗi tài khoản ngân hàng một sổ ngân hàng; tài khoản ngoại tệ ghi theo đúng tiền tệ."],
         muc_tieu="Số dư từng quỹ, từng tài khoản ngân hàng trên hệ thống khớp sổ quỹ và sao kê; không còn khoản thu chi treo.",
         bat_dau="Có khoản thu, chi tiền mặt hoặc chuyển khoản; cuối ngày, cuối tháng.",
         ket_thuc="Mọi giao dịch trên sao kê đã đối chiếu với chứng từ trên hệ thống.",
         luong="Kế toán viên ghi nhận thu chi trên đúng sổ -> nhập sao kê -> đối chiếu từng giao dịch -> Kế toán trưởng kiểm số dư cuối tháng",
         buoc=[
             (KTV, "Ghi nhận khoản thu, chi không gắn hoá đơn (phí, lãi ngân hàng)", "Kế toán > Kế toán > Bút toán hoặc sổ ngân hàng > dòng giao dịch: Đối tác, Tài khoản đối ứng, Số tiền", "-"),
             (KTV, "Nhập sao kê ngân hàng", "Kế toán > tổng quan > sổ ngân hàng > nhập file sao kê (hoặc nhập tay từng dòng)", "Tải sao kê từ ngân hàng điện tử"),
             (KTV, "Đối chiếu từng giao dịch trên sao kê", "Đối chiếu sao kê ngân hàng: mỗi dòng sao kê chọn khoản thanh toán, hoá đơn tương ứng > Xác nhận", "-"),
             (KTV, "Xử lý giao dịch chưa có chứng từ", "Tạo bút toán đối ứng ngay trên dòng sao kê (phí, lãi) hoặc để lại hỏi người phụ trách", "Hỏi bộ phận liên quan về khoản lạ"),
             (KTV, "Kiểm quỹ tiền mặt cuối ngày", "Kế toán > Báo cáo > Sổ quỹ tiền mặt", "Đếm tiền, lập biên bản kiểm quỹ"),
             (KTT, "Kiểm số dư tiền cuối tháng", "Kế toán > Báo cáo > Sổ tiền gửi ngân hàng theo từng tài khoản", "So với sao kê cuối tháng của ngân hàng"),
         ]),
    dict(code="QT04", goi=2, ten="Thu tiền, đối trừ công nợ phải thu, nhắc nợ",
         muc_tieu="Mọi khoản tiền khách trả được đối trừ đúng hoá đơn; biết chính xác khách còn nợ bao nhiêu, quá hạn bao lâu.",
         bat_dau="Hoá đơn bán đã ghi sổ; khách chuyển tiền hoặc trả trước.",
         ket_thuc="Tiền đã ghi nhận, đối trừ đúng hoá đơn; nợ quá hạn đã được nhắc.",
         luong="Kế toán viên ghi nhận tiền khách trả, đối trừ hoá đơn -> hằng tuần lọc nợ quá hạn -> Nhân viên kinh doanh nhắc khách -> Kế toán trưởng theo dõi",
         buoc=[
             (KTV, "Ghi nhận khách thanh toán một hoá đơn", "Mở hoá đơn bán > Thanh toán: Sổ nhật ký, Ngày, Số tiền > Tạo thanh toán", "-"),
             (KTV, "Ghi nhận khách thanh toán nhiều hoá đơn", "Kế toán > Khách hàng > Hóa đơn: chọn nhiều hoá đơn > Thanh toán", "-"),
             (KTV, "Ghi nhận khách trả trước", "Kế toán > Khách hàng > Thanh toán > Mới: Khách hàng, Số tiền, Sổ nhật ký > Xác nhận", "-"),
             (KTV, "Đối trừ khoản trả trước khi hoá đơn ghi sổ", "Mở hoá đơn bán > khoản trả trước hiện ở mục khoản chưa đối trừ > Thêm", "-"),
             (KTV, "Lọc công nợ quá hạn", "Kế toán > Báo cáo > Tuổi nợ phải thu", "-"),
             (NVKD, "Nhắc khách thanh toán", "Ghi kết quả nhắc nợ vào phần trao đổi trên hoá đơn", "Gọi điện, gửi email nhắc khách"),
             (KTT, "Theo dõi công nợ quá hạn hằng tuần", "Kế toán > Báo cáo > Tuổi nợ phải thu", "Báo Giám đốc khoản khó thu"),
         ]),
]

# ------------------------------------------------------------------ kiểm soát dữ liệu
# (loại dữ liệu, vị trí nhập, bắt buộc / điều kiện, vị trí kiểm tra, kiểm tra gì, thời điểm, hệ thống hỗ trợ (điều người dùng thấy), gói)
CHOT_CHAN = [
    ("Khách hàng, nhà cung cấp", f"{NVKD}, {NVMH}", "Tên đầy đủ theo đăng ký kinh doanh, Mã số thuế, Địa chỉ", KTV,
     "Trùng tên, trùng mã số thuế, sai địa chỉ xuất hoá đơn", "Ngay khi tạo",
     "Không lưu được nếu thiếu Mã số thuế; Kế toán viên nhận việc \"Kiểm tra đối tác mới\"", 1),
    ("Sản phẩm, dịch vụ", KTV, "Tên, Mã nội bộ, Nhóm sản phẩm, Đơn vị tính, Loại", KTT,
     "Trùng tên, thiếu mã, sai nhóm", "Ngay khi tạo", "Không lưu được nếu thiếu Mã nội bộ hoặc Nhóm sản phẩm", 1),
    ("Đơn mua", NVMH, "Nhà cung cấp, Ngày dự kiến nhận; đính kèm báo giá; đề nghị phê duyệt loại \"Đơn mua\"", TBP,
     "Giá, số lượng, báo giá đính kèm", "Trước khi xác nhận đơn", "Không xác nhận được đơn khi chưa duyệt đủ", 1),
    ("Thanh toán của khách", KTV, "Đúng sổ nhật ký, đúng khách, đối trừ đúng hoá đơn", KTT,
     "Khoản thu chưa đối trừ", "Hằng tuần", "Hoá đơn hiện trạng thái Đã thanh toán khi đối trừ đủ", 2),
]
# tần suất -> (việc, vị trí làm, xem ở đâu, xử lý, vị trí xác nhận, gói)
RA_SOAT = [
    ("Hằng ngày", [
        ("Thu chi chưa đối chiếu với sao kê", KTV, "Kế toán > tổng quan > từng sổ ngân hàng > Đối chiếu sao kê ngân hàng", "Đối chiếu ngay; khoản lạ hỏi bộ phận liên quan", KTT, 1),
    ]),
    ("Hằng tuần", [
        ("Đối tác trùng tên, trùng mã số thuế", KTV, "Liên hệ (danh sách) > nhóm theo Mã số thuế; chọn các bản trùng > Thao tác > Hợp nhất", "Gộp về một bản đúng", KTT, 1),
        ("Đơn mua đã nhận chưa có hoá đơn", KTV, "Mua hàng > Đơn hàng > Đơn mua: bộ lọc Chờ hóa đơn", "Đòi hoá đơn nhà cung cấp, tạo hoá đơn mua", KTT, 1),
        ("Khoản khách trả chưa đối trừ", KTV, "Kế toán > Khách hàng > Thanh toán: lọc chưa đối chiếu", "Đối trừ vào hoá đơn tương ứng", KTT, 2),
    ]),
    ("Hằng tháng", [
        ("Tồn kho âm", TK, "Tồn kho > Báo cáo > Tồn kho: lọc số lượng âm", "Tìm phiếu nhập thiếu, xác nhận bổ sung", KTT, 1),
    ]),
]
NHAC_DINH_KY = ("Người giữ vị trí làm nhận mỗi việc rà soát dưới dạng một nhiệm vụ định kỳ trong dự án \"Kiểm soát dữ liệu\" (ứng dụng Dự án); "
                "làm xong thì đánh dấu hoàn thành, đến kỳ sau hệ thống tự tạo lại nhiệm vụ.")
KIEM_SOAT_NGUOI = "Người kiểm soát dữ liệu danh mục là Kế toán viên, người xác nhận là Kế toán trưởng, trừ việc thuộc kho."

PHOI_HOP_CACH = [
    "Đang làm chứng từ mà thiếu một mục chưa có trên hệ thống: để chứng từ ở trạng thái nháp, không chọn tạm một mục gần giống.",
    "Ngay trên chứng từ đó bấm \"Lên lịch hoạt động\": loại Việc cần làm, giao cho người nhận yêu cầu theo bảng dưới, đặt hạn, ghi đủ thông tin cần gửi.",
    "Người nhận kiểm trùng, tạo mục mới, rồi \"Đánh dấu hoàn thành\" hoạt động kèm tên mục vừa tạo; người yêu cầu nhận được thông báo và làm tiếp.",
]
# (cần tạo mới, vị trí thường cần, người nhận yêu cầu, thông tin phải gửi kèm, lưu ý, quyền tạo [(mục, nhóm)])
PHOI_HOP = [
    ("Điều khoản thanh toán", f"{TPKD}, {NVKD} (đơn bán); {NVMH} (đơn mua)", KTT,
     "Đối tác, số đợt, phần trăm và số ngày từng đợt, số hợp đồng", "Dùng chung cho mọi đối tác cùng điều kiện", [("Kế toán", "Quản trị viên")]),
    ("Sản phẩm, dịch vụ mới", f"{NVMH}, {TK}, {NVKD}", KTV,
     "Tên, mã (nếu có), loại hàng tồn kho hay dịch vụ, nhóm sản phẩm, đơn vị tính", "Kiểm trùng tên, mã trước khi tạo", [("Sản phẩm", "Tạo")]),
    ("Khách hàng, nhà cung cấp", TK, KTV, "Tên đầy đủ, mã số thuế, địa chỉ, người liên hệ", "Kiểm trùng tên, mã số thuế trước khi tạo", [("Liên hệ", "Tạo")]),
    ("Người dùng, phân quyền", "Trưởng bộ phận", QTHT, "Họ tên, email, vị trí theo sơ đồ tổ chức", "Gán theo vị trí trong ma trận phân quyền",
     [("Vai trò", "Quản trị viên")]),
]

# ------------------------------------------------------------------ quy trình con dùng chung
PD = dict(code="PD", ten="Phê duyệt đề nghị (đơn mua)", buoc=[
    (HT, "Xác định người duyệt theo người trình và giá trị", "Hệ thống tự tìm người duyệt: bước 1 quản lý phòng ban của người trình; bước 2 Giám đốc khi giá trị trên 100 triệu đồng", "-"),
    (TBP, "Duyệt hoặc từ chối", "Phê duyệt > Đề nghị phê duyệt > mở đề nghị > Duyệt, hoặc Từ chối kèm lý do", "Trao đổi lại với người trình nếu cần"),
    (GD, "Duyệt hoặc từ chối đề nghị trên 100 triệu đồng", "Phê duyệt > Đề nghị phê duyệt > Duyệt hoặc Từ chối", "-"),
])
DT = dict(code="DT", ten="Tạo đối tác mới (nhà cung cấp, khách hàng)", buoc=[
    (NLD, "Kiểm tra đối tác đã có trên hệ thống chưa", "Liên hệ: tìm theo tên hoặc mã số thuế", "Nếu chưa có: lấy tên, địa chỉ, mã số thuế của đối tác"),
    (NLD, "Tạo đối tác mới (chỉ khi chưa có)", "Liên hệ > Mới: Tên, Địa chỉ, Mã số thuế > Lưu", "-"),
    (HT, "Giao việc cho Kế toán viên kiểm tra đối tác mới", "Kế toán viên nhận hoạt động \"Kiểm tra đối tác mới\" trên đối tác vừa tạo", "-"),
    (KTV, "Kiểm tra đối tác mới: trùng tên, mã số thuế, địa chỉ xuất hoá đơn", "Mở hoạt động được giao > sửa thông tin nếu sai > đánh dấu Hoàn thành", "Tra cứu mã số thuế trên cổng thông tin thuế"),
])
DT_MO_TA = "quy trình con dùng chung khi lập đơn mua (QT01) hoặc chứng từ khác cần nhà cung cấp, khách hàng chưa có trên hệ thống"

# ------------------------------------------------------------------ tài liệu hướng dẫn Viindoo (đúng phiên bản khách chạy)
# Đường dẫn = file content/applications/<path>.rst trên nhánh phiên bản của kho tài liệu Viindoo; URL = DOC_BASE + path + ".html".
DOC_BASE = "https://viindoo.com/documentation/19.0/vi/applications/"
_F = "finance/accounting-and-invoicing/"
_W = "supply-chain/inventory/warehouse-management/"
TRANG = {
    "contact_over": ("productivity/contact/overview-and-configuration-in-viindoo-contact", "Tổng quan ứng dụng Liên hệ"),
    "contact_create": ("productivity/contact/create-a-new-contact-in-viindoo", "Tạo liên hệ mới"),
    "contact_dup": ("productivity/contact/handling-duplicate-contacts-in-viindoo", "Xử lý liên hệ trùng"),
    "purchase_start": ("supply-chain/purchase/overview/getting-started", "Bắt đầu với ứng dụng Mua hàng"),
    "po_create": ("supply-chain/purchase/manage-deals/how-to-create-a-purchase-order", "Tạo yêu cầu báo giá, đơn mua"),
    "appr_over": ("operation/approval/approval-overview", "Tổng quan ứng dụng Phê duyệt"),
    "appr_req": ("operation/approval/manage-approval-requests", "Tạo và duyệt đề nghị phê duyệt"),
    "appr_type": ("operation/approval/create-approval-types-and-set-up-approval-levels", "Loại phê duyệt và các bước duyệt"),
    "appr_po": ("operation/approval/manage-procurement-approval", "Phê duyệt đơn mua"),
    "receipt": (_W + "incoming-shipments/receipt-with-one-step-flow-receive", "Nhận hàng một bước"),
    "vb_ctrl": ("supply-chain/purchase/manage-deals/vendor-bills-control", "Kiểm soát lập hoá đơn mua"),
    "vendor_bill": (_F + "account-payables/vendor-bills/vendor-bills-management", "Quản lý hoá đơn mua"),
    "ap_process": (_F + "account-payables/steps-to-record-payment-in-purchase", "Hoá đơn mua, thanh toán, đối trừ"),
    "recon": (_F + "bank-cash/bank-reconciliation/steps-in-the-bank-reconciliation-process", "Đối chiếu sao kê ngân hàng"),
    "stmt": (_F + "bank-cash/bank-reconciliation/manage-bank-statements", "Sao kê ngân hàng"),
    "cash": (_F + "bank-cash/bank-reconciliation/cash-on-hand-management", "Quản lý tiền mặt"),
    "recon_model": (_F + "bank-cash/bank-reconciliation/reconcile-deposit-interest-and-bank-fees", "Mẫu đối chiếu phí, lãi ngân hàng"),
    "vn_reports": (_F + "reporting/reports/reports-according-to-vietnam-accounting-standard", "Báo cáo theo chuẩn mực kế toán Việt Nam"),
    "ar_process": (_F + "account-receivables/steps-to-record-customer-s-payment", "Hoá đơn bán, thu tiền, đối trừ"),
    "cust_pay": (_F + "account-receivables/customer-payments/how-to-create-customer-payment-in-viindoo-accounting", "Ghi nhận khách hàng thanh toán"),
    "so_adv": ("sales/sales/payment/advanced-features-related-to-payment", "Tiền khách trả trước theo đơn bán"),
    "aged": (_F + "reporting/reports/accounting-data-analysis-report", "Báo cáo tuổi nợ"),
    "payterm": (_F + "account-receivables/customer-invoices/settings/configure-payment-terms", "Điều khoản thanh toán"),
    "users": ("getting-started/manage-users/user-account-setting-and-management", "Quản lý tài khoản người dùng"),
    "groups": ("getting-started/manage-users/advance-access-setting-up-for-user-account", "Phân quyền theo nhóm"),
    "prod_new": ("getting-started/products/step-to-create-a-new-product", "Tạo sản phẩm mới"),
    "prod_cat": ("getting-started/products/managing-product-categories", "Nhóm sản phẩm"),
    "filters": ("getting-started/filter-groups-and-search-use-cases", "Bộ lọc, nhóm và tìm kiếm"),
    "activities": ("productivity/scheduled-activities", "Hoạt động được lên lịch"),
    "project": ("services/project/guideline-to-basic-features-of-viindoo-project", "Dự án và nhiệm vụ"),
    "collab": ("getting-started/communication-and-collaboration-in-viindoo", "Trao đổi và phối hợp trên chứng từ"),
}
TAI_LIEU = {
    "ma_tran": ["users", "groups"],
    "phe_duyet": ["appr_over", "appr_req", "appr_po"],
    "PD": ["appr_req"],
    "kiem_soat": ["contact_over", "prod_new", "filters"],
    "chot_chan": ["contact_create", "prod_new", "prod_cat"],
    "ra_soat": ["filters", "activities", "project", "contact_dup"],
    "phoi_hop": ["collab", "activities", "payterm", "prod_new"],
    "DT": ["contact_over", "contact_create", "contact_dup"],
    "QT01": ["purchase_start", "po_create", "appr_po"],
    "QT02": ["receipt", "vendor_bill", "ap_process"],
    "QT03": ["recon", "stmt", "cash"],
    "QT04": ["ar_process", "cust_pay", "aged"],
}
# trang hướng dẫn theo từng bước (None = việc ngoài phần mềm, việc tự động, nghiệp vụ riêng của khách)
HUONG_DAN = {
    "QT01": ["po_create", "po_create", "appr_req", "appr_req", "po_create", "po_create", None],
    "QT02": ["receipt", "receipt", "vb_ctrl", None, "ap_process", "vendor_bill", "vendor_bill", None, None, "ap_process"],
    "QT03": ["recon_model", "stmt", "recon", "recon_model", "cash", "vn_reports"],
    "QT04": ["cust_pay", "cust_pay", "so_adv", "ar_process", "aged", None, "aged"],
    "PD": ["appr_type", "appr_req", "appr_req"],
    "DT": [None, "contact_create", None, "contact_dup"],
}


# ------------------------------------------------------------------ sơ đồ BPMN theo luồng
# Mỗi quy trình: một hoặc nhiều luồng. Nút: số bước ("5"), việc ngoài phần mềm của bước ("5n", chữ lấy cột Ngoài phần mềm),
# hoặc khai trong "nut": (loại, làn, chữ[, số bước]) với loại start, timer, end, gw (rẽ nhánh), join (gộp), manual, call, wait.
# Cạnh "a>b" hoặc "a>b:nhãn"; với cổng rẽ, cạnh khai đầu tiên là nhánh chính (ra cạnh phải), các nhánh khác ra cạnh dưới.
# Việc độc lập (không nối tiếp nhau trong thực tế) thì tách thành luồng riêng, không nối chuỗi.
def _F(ten, nut, canh):
    return dict(ten=ten, nut=nut, canh=[c.strip() for c in canh.split(";") if c.strip()])


_PDC = "PD - Phê duyệt đề nghị"
_DTN = "DT - Kiểm tra, tạo nhà cung cấp"
SO_DO = {
    "PD": [_F("Phê duyệt đề nghị", {
        "s": ("start", HT, "Đề nghị đã gửi phê duyệt"),
        "g2": ("gw", TBP, "Kết quả?"), "e2": ("end", TBP, "Từ chối"),
        "g4": ("gw", HT, "Trên 100 triệu?"), "j2": ("join", HT),
        "g5": ("gw", GD, "Kết quả?"), "e5": ("end", GD, "Từ chối"), "e": ("end", HT, "Đã duyệt")},
        "s>1; 1>2; 2>g2; g2>g4:Duyệt; g2>e2:Từ chối; g4>3:Có; g4>j2:Không; 3>g5; g5>j2:Duyệt; g5>e5:Từ chối; j2>e")],
    "DT": [_F("Tạo đối tác mới", {
        "s": ("start", NLD, "Cần nhà cung cấp hoặc khách hàng trên chứng từ"), "g": ("gw", NLD, "Đối tác đã có?"),
        "j": ("join", NLD), "e": ("end", NLD, "Đối tác dùng được trên chứng từ")},
        "s>1; 1>g; g>j:Đã có; g>1n:Chưa có; 1n>2; 2>3; 3>4n; 4n>4; 4>j; j>e")],
    "QT01": [_F("Đề nghị mua, đơn mua", {
        "s": ("start", NVMH, "Phát sinh nhu cầu mua"), "d": ("call", NVMH, _DTN),
        "c": ("call", NVMH, _PDC), "g": ("gw", NVMH, "Kết quả duyệt?"),
        "e": ("end", KTV, "Đơn mua đã gửi, kế toán đã kiểm")},
        "s>d; d>1n; 1n>1; 1>2; 2>3; 3>c; c>g; g>5:Duyệt; g>4:Từ chối; 4>c; 5>6; 6>6n; 6n>7; 7>e")],
    "QT02": [
        _F("Nhận hàng, dịch vụ và hoá đơn mua", {
            "s": ("start", TK, "Nhà cung cấp giao hàng hoặc hoàn thành dịch vụ"),
            "g1": ("gw", TK, "Hàng hay dịch vụ?"), "j1": ("join", KTV),
            "g2": ("gw", KTV, "Đủ chứng từ?"), "m": ("manual", KTV, "Trả lại người mua bổ sung chứng từ"),
            "e": ("end", KTV, "Hoá đơn mua đã ghi sổ")},
            "s>g1; g1>1n:Hàng; g1>3n:Dịch vụ; 1n>1; 1>2; 2>j1; 3n>3; 3>j1; j1>4; 4>5; 5>6; 6>g2; g2>7:Đủ; g2>m:Thiếu; m>4; 7>e"),
        _F("Thanh toán nhà cung cấp", {
            "t": ("timer", KTV, "Đến hạn thanh toán"), "g": ("gw", KTT, "Kết quả duyệt?"),
            "e": ("end", KTV, "Hoá đơn đã thanh toán, đối trừ")},
            "t>8; 8>8n; 8n>9; 9>g; g>10:Duyệt; g>8:Từ chối; 10>10n; 10n>e")],
    "QT03": [
        _F("Thu, chi không gắn hoá đơn", {"s": ("start", KTV, "Có phí, lãi ngân hàng, thu chi khác"), "e": ("end", KTV, "Đã ghi nhận đúng sổ")},
           "s>1; 1>e"),
        _F("Đối chiếu sao kê", {"s": ("start", KTV, "Có sao kê mới"), "g": ("gw", KTV, "Có chứng từ?"), "j": ("join", KTV),
                               "e": ("end", KTV, "Sao kê đã đối chiếu hết")},
           "s>2n; 2n>2; 2>3; 3>g; g>j:Có; g>4n:Chưa có; 4n>4; 4>j; j>e"),
        _F("Kiểm quỹ tiền mặt", {"t": ("timer", KTV, "Cuối ngày"), "e": ("end", KTV, "Quỹ đã kiểm")}, "t>5; 5>5n; 5n>e"),
        _F("Kiểm số dư tiền", {"t": ("timer", KTT, "Cuối tháng"), "e": ("end", KTT, "Số dư đã khớp")}, "t>6; 6>6n; 6n>e")],
    "QT04": [
        _F("Thu tiền khách trả", {"s": ("start", KTV, "Khách chuyển tiền"), "g": ("gw", KTV, "Khách trả cho?"),
                                 "j": ("join", KTV), "e": ("end", KTV, "Tiền đã ghi nhận")},
           "s>g; g>1:Một hoá đơn; g>2:Nhiều hoá đơn; g>3:Trả trước; 1>j; 2>j; 3>j; j>e"),
        _F("Đối trừ khoản trả trước", {"s": ("start", KTV, "Hoá đơn ghi sổ, khách có khoản trả trước"), "e": ("end", KTV, "Hoá đơn đã đối trừ")},
           "s>4; 4>e"),
        _F("Nhắc nợ", {"t": ("timer", KTV, "Hằng tuần"), "g": ("gw", KTV, "Có nợ quá hạn?"), "j": ("join", KTT),
                      "e": ("end", KTT, "Công nợ đã theo dõi")},
           "t>5; 5>g; g>6:Có; g>j:Không; 6>6n; 6n>j; j>7; 7>7n; 7n>e")],
}
