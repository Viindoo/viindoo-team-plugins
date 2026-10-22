# Kit tài liệu presales - hàm dùng chung

Năm skill của bộ hồ sơ khách hàng đều dựng tài liệu từ kit này, nên mọi tài liệu gửi đi cùng một bộ màu, font, logo và cùng một cách hành xử của ô ý kiến.

**Kit không giữ công thức giá, hệ số hay đơn giá.** Quy tắc tính giá đổi theo thời điểm và theo từng khách - hỏi Liên hoặc tra bảng giá hiện hành, đừng mang hệ số của dự án cũ sang dự án mới.

## Nạp kit

```python
import sys, os, glob
KIT = os.environ.get("CLAUDE_PLUGIN_ROOT") or sorted(
    glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/viindoo-presales/*")))[-1]
sys.path.insert(0, os.path.join(KIT, "kit", "lib"))
import vdoc, vykien, vsodo, vbr
```

Trong phiên Claude Code, `CLAUDE_PLUGIN_ROOT` đã trỏ sẵn vào thư mục plugin. Chạy ngoài phiên thì nhánh `glob` tự tìm bản mới nhất trong cache; đặt `CLAUDE_PLUGIN_ROOT` thủ công nếu plugin nằm chỗ khác.

## vdoc - khung tài liệu HTML

| Hàm | Dùng để |
|---|---|
| `tai_lieu(tieu_de, mo_ta, khach, ngay, phan, css_them, js_them, mo_dau, chan_trang)` | tài liệu dài đọc trên màn hình (bước 1, bước 2) |
| `phuong_an(tieu_de, mo_ta, meta, the_tag, tom_tat_so, tom_tat_y, phan, css_them)` | phương án in PDF theo mẫu chuẩn (bước 4) |
| `gach_y(muc)` | gạch ý có nhãn; phần tử là chuỗi hoặc cặp `("Nhãn", "nội dung")` |
| `bang(cot, dong, lop)` | bảng bo tròn theo brand |
| `the_so(so, nhan)` | thẻ số lớn - **chỉ cho số của Viindoo**, không cho số lấy từ hệ thống khách |
| `tien(v)` | `382500000` thành `382.500.000 đ` |
| `css(ten)` | đọc CSS trong kit: `tai-lieu`, `phuong-an`, `quy-trinh`, `y-kien` |
| `logo_svg(nen_toi)`, `logo_b64(nen_toi)`, `favicon_b64()` | logo màu (cyan + tím) hoặc bản đảo màu cho nền tối |
| `kiem_ban_gui_khach(duong_dan, them, bo_qua)` | soát tệp gửi khách còn cách tính giá nội bộ không; trả về list phát hiện, rỗng là đạt |
| `in_ket_qua_soat(phat_hien)` | in gọn kết quả soát ra dòng lệnh |
| `nhom_nghiep_vu(tieu_de, cau_dan, muc, can_lam_ro)` | một nhóm trong Mục 2 của phương án |
| `khoi_can_lam_ro(muc)` | khung vàng "Cần làm rõ ở giai đoạn Khảo sát" |
| `khoi_phat_trien(ten, gia, tom_tat, bai_toan, se_lam, vi_sao, gioi_han)` | một hạng mục trong Mục 3, có giá riêng |
| `NGUYEN_TAC_PHAT_TRIEN` | khối nguyên tắc đặt đầu Mục 3 |

`phan` là list dict `{"id", "so", "ten", "noi_dung"}`; mục lục sinh ra từ chính danh sách đó.

## vykien - ô ý kiến và phiếu xác nhận

Khách mở tệp bằng trình duyệt, đánh dấu và ghi ý kiến ngay trên trang; trình duyệt giữ nội dung trên máy khách; một nút in ra phiếu ý kiến PDF để gửi lại.

| Hàm | Dùng để |
|---|---|
| `css()`, `js(khoa, khach)` | nhúng vào `css_them`, `js_them`; `khoa` là tiền tố riêng mỗi dự án |
| `mo_dau(de_lam_gi, co_xac_nhan, bo_tai_lieu, dang_doc)` | ghi chú đầu tài liệu |
| `y_kien(ma, nhan, khach, dong)` | ô ý kiến đặt **cuối mỗi phần** |
| `khoi_xac_nhan(diem)` | mục "những điểm cần công ty xác nhận" |
| `thanh_nut()` | nút in phiếu ý kiến |
| `dong_xlsx(diem)` | cùng dữ liệu đó đổ sang sheet Excel |

Mỗi điểm xác nhận: `{"ma", "ten", "hieu": [...], "tich": [...]}` - `hieu` là **cách hiểu và đề xuất của Viindoo kèm căn cứ**, `tich` là các dòng khách tích. Không hỏi lại những gì đã đọc được từ tài liệu khách gửi; chỉ hỏi câu mà câu trả lời làm đổi giải pháp, phạm vi hay chi phí.

## vsodo - sơ đồ quy trình và mức đáp ứng

| Hàm | Dùng để |
|---|---|
| `so_do(lanes, steps)` | sơ đồ làn dạng SVG |
| `chu_giai_so_do()` | chú giải, đặt một lần ở phần tổng quan |
| `thanh(hang_muc, nho, nhan)` | thanh tỷ lệ bốn lớp đáp ứng |
| `dem_lop(hang_muc)` | đếm hạng mục theo lớp |
| `truy_vet(ma_br, nguon, nguon_day_du)` | nhãn mã BR + vị trí gốc trong tài liệu khách |
| `nhan_lop(nen_odoo)` | nhãn bốn lớp, ghi rõ phiên bản Odoo đối chiếu |

`steps` là list `(ma, chỉ_số_làn, chữ, kiểu, nxt)`; kiểu là `task` (làm trên phần mềm), `ext` (làm bên ngoài), `auto` (hệ thống tự làm), `dec` (điểm quyết định), `start`, `end`. `nxt` là list `(mã_đích, nhãn)` hoặc `None` để nối sang bước kế tiếp.

Hạng mục đáp ứng: `{"br", "nguon", "yeu_cau", "phan_co", "co", "phan_thieu", "thieu"}`. Yêu cầu đáp ứng một phần thì đặt cả `phan_co` lẫn `phan_thieu` - thành hai hạng mục trên thanh tỷ lệ.

## vbr - workbook Danh mục Yêu cầu Nghiệp vụ

| Hàm | Dùng để |
|---|---|
| `dung(rows, out, khach, to_chuc, diem_xac_nhan, ghi_chu_chi_phi, mau, sap_xep)` | dựng workbook từ mẫu chuẩn đã khử dữ liệu khách |
| `COT_GIO`, `TEN_GIAI_DOAN`, `PHAN_LOAI` | tra cứu cột và giá trị hợp lệ |

Mẫu: `kit/mau/danh-muc-br.xlsx`. Schema một dòng BR xem `skills/viindoo-danh-muc-br/references/schema-du-lieu.md`.

## Soát bản gửi khách

`kiem_ban_gui_khach()` trả về list dict `{"tu", "muc", "trich"}`:

- `muc = "cam"` - **phải sửa**: "Junior", "Senior", "Expert", "manday". Cách tính giá nội bộ lọt ra ngoài.
- `muc = "can_xem"` - **đọc rồi tự quyết**: "ngày công", "giờ công" đứng gần từ chỉ tiền. Từ này có thể là nghiệp vụ của chính khách, ví dụ "lương theo ngày công" - không sửa máy móc. Chắc chắn là nghiệp vụ khách thì truyền `bo_qua=["ngày công"]`.

## Quy ước chung cho mọi tài liệu

- Chỉ dùng dấu gạch ngang ASCII `-`.
- Gạch ý có nhãn thay văn xuôi dài.
- Không nêu con số lấy từ hệ thống đang chạy của khách.
- Mỗi mục ghi nguồn truy vết về tài liệu khách gửi.
- Tệp đặt trong `~/Documents/project/<Khách>/`, mã nguồn dựng tệp đặt trong `work/` cùng thư mục đó.
