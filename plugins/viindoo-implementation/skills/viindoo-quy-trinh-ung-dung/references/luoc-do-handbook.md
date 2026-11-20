# Lược đồ handbook.py

Tệp chạy được đầy đủ: `kit/examples/sample/handbook.py`. Tên biến giữ nguyên như bộ dựng đọc (tiếng Việt không dấu).

| Biến | Bắt buộc | Kiểu | Ý nghĩa |
|---|---|---|---|
| `KHACH`, `KHACH_NGAN` | có | chuỗi | tên đầy đủ; tên ngắn dùng cho tên tệp và tiêu đề Word |
| `NGAY` | có | chuỗi | ngày lập |
| `CAN_CU` | không | chuỗi | căn cứ (sơ đồ tổ chức, quy định phê duyệt...) |
| `GOI_TEN` | có | dict gói -> tên | ví dụ `{1: "Gói 1 - Mua hàng, kho, tiền"}` |
| `HT` | có | chuỗi | tên làn hệ thống tự làm (bước của làn này vẽ là việc tự động) |
| `VI_TRI` | có | list (vị trí, việc chính) | bảng vị trí công việc |
| `VT_MT` | có | list vị trí | cột của ma trận phân quyền, thứ tự từ cao xuống |
| `MA_TRAN` | có | list (cụm, [(mục, nhóm ô đánh dấu hoặc None, [ô theo VT_MT])]) | ô là tên nhóm đúng chữ giao diện, "Có" (ô đánh dấu) hoặc "-" |
| `CAP_TREN` | có | dict vị trí -> cấp trên | đúng một vị trí cao nhất không có cấp trên |
| `NGOAI_LE_KE_THUA` | không | set | mục hoặc nhóm không áp nguyên tắc cấp trên bao trùm (ví dụ "Vai trò") |
| `CAP_CAO_TRONG_VT` | không | dict (vị trí, mục) -> nhóm | một người trong vị trí giữ cấp cao hơn cả vị trí |
| `GHI_CHU_MT`, `NGUYEN_TAC`, `GIOI_HAN`, `CHU_GIAI` | có | list | ghi chú ma trận; nguyên tắc gán quyền; quy tắc giới hạn dữ liệu; (mục, các cấp) |
| `PHE_DUYET` | có | list chuỗi | quy tắc phê duyệt |
| `QUY_TRINH` | có | list dict | mỗi quy trình: `code` (dạng `QTxx`), `goi`, `ten`, `muc_tieu`, `bat_dau`, `ket_thuc`, `luong`, `luu_y` (không bắt buộc), `buoc` = [(vị trí, nhiệm vụ, thao tác trên Viindoo hoặc "-", ngoài phần mềm hoặc "-")] |
| `PD`, `DT` | không | dict `code`, `ten`, `buoc` | quy trình con dùng chung: phê duyệt đề nghị, tạo đối tác mới |
| `DT_MO_TA` | không | chuỗi | câu giới thiệu quy trình con DT |
| `CHOT_CHAN` | có | list (loại dữ liệu, vị trí nhập, bắt buộc, vị trí kiểm tra, kiểm gì, thời điểm, hệ thống hỗ trợ, gói) | mục 3A |
| `RA_SOAT` | có | list (tần suất, [(việc, vị trí làm, xem ở đâu, xử lý, vị trí xác nhận, gói)]) | mục 3B |
| `NHAC_DINH_KY`, `KIEM_SOAT_NGUOI` | có / không | chuỗi | cách giao việc rà soát; ai kiểm soát dữ liệu danh mục |
| `PHOI_HOP_CACH` | có | list chuỗi | cách gửi yêu cầu tạo mới ngay trên chứng từ |
| `PHOI_HOP` | có | list (cần tạo mới, vị trí thường cần, người nhận, thông tin gửi kèm, lưu ý, [(mục, nhóm) quyền tạo]) | người nhận phải có quyền tạo theo ma trận |
| `DOC_BASE` | có | chuỗi | `https://viindoo.com/documentation/<bản>/vi/applications/` - phiên bản khách chạy |
| `TRANG` | có | dict khoá -> (đường dẫn trong `content/applications/` không đuôi, tên hiển thị) | trang tài liệu hướng dẫn |
| `TAI_LIEU` | có | dict mục hoặc mã quy trình -> [khoá TRANG] | khoá mục: `ma_tran`, `phe_duyet`, `kiem_soat`, `chot_chan`, `ra_soat`, `phoi_hop`, `PD`, `DT`, mã quy trình |
| `HUONG_DAN` | có | dict mã quy trình -> [khoá TRANG hoặc None theo từng bước] | số phần tử bằng số bước |
| `SO_DO` | có | dict mã -> [luồng] | luồng tạo bằng `_F(tên, nút, cạnh)` |
| `CHUYEN_CHO_GON` | không | dict (mã, bước) -> chuỗi | câu "Chuyển cho" viết gọn khi bước có nhiều cổng nối tiếp |

## Sơ đồ

- Nút là số bước (`"5"`), việc ngoài phần mềm của bước (`"5n"`, chữ lấy từ cột Ngoài phần mềm), hoặc khai trong `nut`: `(loại, làn, chữ[, số bước])`, loại `start`, `timer`, `end`, `gw`, `join`, `manual`, `call`, `wait`.
- Cạnh `"a>b"` hoặc `"a>b:nhãn"`; với cổng rẽ, cạnh khai đầu tiên là nhánh chính (ra cạnh phải), nhánh khác ra cạnh dưới.
- Mỗi bước xuất hiện đúng một lần trên các luồng của quy trình.
- Ô gọi quy trình con ghi `"<mã> - <tên ngắn>"`, mã phải có trong `SO_DO`.
