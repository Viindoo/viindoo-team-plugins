---
name: viindoo-mo-hinh-hoat-dong
description: Dựng tài liệu "Phân tích hiện trạng và mô hình vận hành" của một khách hàng - bước 1 trong bộ bốn tài liệu presales Viindoo. Từ tài liệu khách gửi, ghi chú khảo sát, biên bản họp và thông tin công khai, viết ra mô hình kinh doanh, dòng chảy vận hành, bộ máy và vai trò, đặc tính dữ liệu quyết định hình giải pháp, hiện trạng công nghệ, điểm đứt gãy - kèm ô ý kiến để khách sửa trực tiếp trên trang. Dùng khi người dùng nói "làm mô hình hoạt động của khách", "phân tích hiện trạng doanh nghiệp", "mô hình kinh doanh của khách này ra sao", "dựng hồ sơ doanh nghiệp trước khi làm BR", "viết tài liệu số 1 cho dự án X". KHÔNG dùng cho - vẽ quy trình nghiệp vụ và chấm mức đáp ứng (→ viindoo-quy-trinh-dap-ung), lập danh mục yêu cầu (→ viindoo-danh-muc-br), báo giá (→ viindoo-phuong-an-de-xuat), vẽ BPMN As-Is/To-Be (→ spec-to-bpmn).
---

# Bước 1 - Mô hình hoạt động của khách hàng

Tài liệu đầu tiên gửi khách. Trả lời đúng một câu hỏi: **doanh nghiệp này kiếm tiền và vận hành bằng cách nào, và điều đó buộc giải pháp phải có hình dạng gì.**

Khách đọc để xác nhận "Viindoo hiểu đúng về chúng tôi chưa". Ba tài liệu sau đều đứng trên tài liệu này, nên sai ở đây là sai cả bộ.

## Dùng ở đâu trong quy trình presales

| Mốc | Việc | Tài liệu |
|---|---|---|
| **Nhận lead, có hồ sơ khách gửi** | **hiểu doanh nghiệp làm gì, vận hành ra sao** | **bước 1 - tài liệu này** |
| Sau khảo sát, có danh sách yêu cầu | chốt hiểu đúng, chấm đáp ứng | bước 2 quy trình và mức đáp ứng |
| Nội bộ, trước khi ra giá | bóc giờ, biết giá vốn | bước 3 danh mục BR |
| Chào giá, trình bày với khách | chốt phạm vi và tiền | bước 4 phương án đề xuất |
| Khách đồng ý, chuẩn bị ký | đính kèm hợp đồng | bước 5 phụ lục hợp đồng |
| Sau ký, vào triển khai | thống nhất thao tác từng vị trí | QTUD (ngoài bộ này) |

Làm ngay khi nhận hồ sơ khách, trước mọi tài liệu khác. Ba tài liệu sau đều đứng trên tài liệu này.

## Khi nào dùng

- "Làm mô hình hoạt động / hiện trạng của khách X"
- "Phân tích doanh nghiệp này trước khi làm BR"
- "Dựng tài liệu số 1 cho dự án X"
- Vừa nhận hồ sơ khách (RFI, tài liệu yêu cầu, biên bản khảo sát) và chưa có tài liệu nào gửi đi

## Đầu vào

Đọc **hết** những gì có trước khi viết một dòng nào:

| Nguồn | Tìm ở đâu |
|---|---|
| Tài liệu khách gửi | `~/Documents/project/<Khách>/Ho so khach hang/`, `Dữ liệu khách gửi/` |
| Ghi chú khảo sát, biên bản họp, tin nhắn | `~/Documents/project/<Khách>/*.md` |
| Thông tin công khai | website khách, cổng thông tin doanh nghiệp, báo chí ngành |
| Bộ nhớ dự án | `~/git/obsidian-vault/Engineering/AI-Memory/auto/` - ghi chú `<khách>-project-folder` |

Chưa có thư mục dự án thì tạo theo quy ước trong ghi chú `customer-project-folder-convention`.

## Cấu trúc tài liệu

Mười phần dưới đây là khuôn đã dùng với khách thật. Phần nào không có dữ liệu thì bỏ hẳn, **không viết phần rỗng**, không bịa.

1. **Nhận diện pháp nhân** - tên đầy đủ, mã số thuế, năm thành lập, người đại diện, các pháp nhân trong nhóm và quan hệ giữa chúng.
2. **Ngành hàng, sản phẩm và thương hiệu** - bán cái gì, cho ai, thương hiệu nào.
3. **Mô hình kinh doanh - một đoạn** - viết được thành một đoạn thì mới hiểu đúng. Ví dụ: "vừa sản xuất vừa phân phối, sản xuất theo đơn cho khách công nghiệp và sản xuất tồn kho cho kênh bán lẻ".
4. **Bản đồ chuỗi giá trị** - từ nhu cầu đến tiền về, đi qua những khâu nào.
5. **Các dòng chảy nghiệp vụ** - mỗi dòng một tiểu mục: dòng nhu cầu và đơn hàng, dòng kế hoạch, dòng mua hàng, dòng vật tư và bán thành phẩm, dòng ngược (phế, tái sinh, đổi trả), dòng giá thành. Số dòng tùy ngành.
6. **Bộ máy - vai và ai giữ số** - phòng ban, vị trí, và quan trọng nhất: **số liệu nào do ai giữ**. Đây là thứ quyết định phân quyền và ai nhập liệu sau này.
7. **Đặc tính dữ liệu quyết định hình giải pháp** - phần giá trị nhất của tài liệu. Ví dụ đã gặp: đơn vị đo kép (kg và mét, nối nhau bằng định lượng), quy cách nằm trong mã hàng làm số mã bùng nổ, định danh từng cuộn/từng vỏ bình, công thức phối liệu đổi theo lô. Mỗi đặc tính ghi rõ: nó là gì, nó buộc hệ thống phải làm gì.
8. **Hiện trạng công nghệ** - đang dùng phần mềm gì, dữ liệu nằm ở đâu, chỗ nào còn trên giấy hoặc Excel, Zalo.
9. **Điểm đứt gãy của mô hình hiện tại** - chỗ dữ liệu đứt, chỗ phải nhập hai lần, chỗ không ai biết số thật.
10. **Dữ kiện và giả thuyết** - tách bạch: cái nào đọc được từ tài liệu khách (ghi nguồn), cái nào là suy luận của Viindoo (ghi rõ là giả thuyết cần khách xác nhận).

Kết thúc bằng một phần ngắn: **mô hình đổi thì gì đổi theo** - nếu khách chuẩn hóa lại một điểm, phạm vi giải pháp đổi ra sao.

## Luật bắt buộc

1. **Không nêu con số lấy từ hệ thống đang chạy của khách.** Số bản ghi (bao nhiêu đơn, hóa đơn, máy, tài khoản) và số tiền của khách thay đổi hàng ngày, đưa vào tài liệu là sai ngay. Mô tả định tính theo đầu mục nghiệp vụ. Giữ được: mã tài khoản theo thông tư, tên module, phiên bản, và số của chính Viindoo (giờ, tuần, giá).
2. **Mỗi mục ghi nguồn truy vết** - tên tệp khách gửi, mục, dòng. Chỗ nào là suy luận thì nói thẳng là suy luận.
3. **Tài liệu khách gửi thắng ghi chú khảo sát** khi hai nguồn lệch nhau; nêu chỗ lệch ra thay vì chọn ngầm.
4. **Không tự thêm nhu cầu.** Tài liệu này mô tả khách đang làm gì, không phải nơi gợi ý tính năng.
5. **Gạch ý có nhãn** thay văn xuôi dài: `**Nhãn:** nội dung`.
6. **Chỉ dùng dấu gạch ngang ASCII** `-`.

## Cách dựng

Viết một builder trong `~/Documents/project/<Khách>/work/build_mo_hinh.py`, nội dung tách sang `mo_hinh_data.py`. Khung HTML, brand, ô ý kiến lấy từ kit của plugin - không chép CSS tay:

```python
import sys, os, glob
KIT = os.environ.get("CLAUDE_PLUGIN_ROOT") or sorted(
    glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/viindoo-presales/*")))[-1]
sys.path.insert(0, os.path.join(KIT, "kit", "lib"))
import vdoc, vykien
import mo_hinh_data as D

KHACH = "Công ty cổ phần ABC"
phan = [
    {"id": "phap-nhan", "so": "1", "ten": "Nhận diện pháp nhân",
     "noi_dung": vdoc.gach_y(D.PHAP_NHAN) + vykien.y_kien("phap-nhan", "nhận diện pháp nhân", KHACH)},
    # ... các phần còn lại
]
html = vdoc.tai_lieu(
    "Phân tích hiện trạng<br>và mô hình vận hành", D.MO_TA, KHACH, "Ngày 22 tháng 10 năm 2026", phan,
    css_them=vykien.css(), js_them=vykien.js("abc", KHACH),
    mo_dau=vykien.mo_dau(D.DE_LAM_GI, co_xac_nhan=False, bo_tai_lieu=D.BO_TAI_LIEU, dang_doc="1"))
open(D.OUT, "w", encoding="utf-8").write(html)
```

Đủ hàm của kit: `${CLAUDE_PLUGIN_ROOT}/kit/API.md`. Ví dụ nội dung từng phần: `references/vi-du-cau-truc.md`.

## Giao ra cái gì

Một tệp HTML trong `~/Documents/project/<Khách>/`, đặt tên `[<Khách>] 1. Phan tich hien trang va mo hinh van hanh.html`. Khách mở bằng trình duyệt, ghi ý kiến ngay trên trang, bấm một nút để in phiếu ý kiến ra PDF gửi lại.

Khi khách gửi phiếu ý kiến về: sửa tài liệu, rồi mới chạy bước 2.

## Việc KHÔNG làm ở bước này

- Không chấm mức đáp ứng của Viindoo (bước 2).
- Không đánh mã BR (bước 3).
- Không nói giá, giờ, gói (bước 4).
