---
name: viindoo-phuong-an-de-xuat
description: Dựng "Phương án đề xuất triển khai Viindoo" gửi khách theo mẫu chuẩn hiện hành - bước 4 trong bộ năm tài liệu presales Viindoo, dùng khi đã chốt phạm vi và sắp chào giá. Gồm tóm tắt điều hành, bối cảnh và phạm vi, mô tả nghiệp vụ trên hệ thống xếp theo dòng chảy đơn hàng kèm điểm cần làm rõ, các hạng mục phát triển ngoài gói kèm giá từng hạng mục, cách tiếp cận, quy trình và kế hoạch triển khai chi tiết, báo giá tách gói Express khỏi dịch vụ phát triển, khuyến nghị. Dùng khi người dùng nói "làm phương án đề xuất cho khách", "báo giá triển khai Viindoo", "dựng đề xuất gửi khách", "lên phương án triển khai", "làm bản đề xuất phạm vi và dự toán". KHÔNG dùng cho - phụ lục đính kèm hợp đồng (→ viindoo-phu-luc-hop-dong), file BR Excel nội bộ (→ viindoo-danh-muc-br), mô tả doanh nghiệp (→ viindoo-mo-hinh-hoat-dong), đánh giá mức đáp ứng (→ viindoo-quy-trinh-dap-ung), QTUD khi triển khai.
---

# Bước 4 - Phương án đề xuất triển khai

Tài liệu khách mang đi họp và ra quyết định mua.

## Dùng ở đâu trong quy trình presales

| Mốc | Việc | Tài liệu |
|---|---|---|
| Nhận lead, có hồ sơ khách | hiểu doanh nghiệp | bước 1 mô hình hoạt động |
| Sau khảo sát, có danh sách yêu cầu | chốt hiểu đúng, chấm đáp ứng | bước 2 quy trình và mức đáp ứng |
| Nội bộ, trước khi ra giá | bóc giờ, biết giá vốn | bước 3 danh mục BR |
| **Chào giá, trình bày với ban lãnh đạo khách** | **chốt phạm vi và tiền** | **bước 4 - tài liệu này** |
| Khách đồng ý, chuẩn bị ký | đính kèm hợp đồng | bước 5 phụ lục hợp đồng |
| Sau ký, vào triển khai | thống nhất thao tác từng vị trí | QTUD (ngoài bộ này) |

Chỉ làm bước này khi **phạm vi đã đứng**: khách đã phản hồi tài liệu bước 2 và danh mục BR đã bóc giờ xong. Làm sớm hơn là báo giá trên phạm vi chưa chốt.

## Mẫu chuẩn

Bản Quang Thắng (20/10/2026) là mẫu hiện hành - **lấy đúng bố cục và cách trình bày này**, các mẫu cũ hơn đã lỗi thời, không dùng nữa.

| Mục | Nội dung |
|---|---|
| Tóm tắt điều hành | 3-4 thẻ số của Viindoo + một đoạn gạch ý nói phạm vi gồm gì |
| 1. Bối cảnh và phạm vi | khách là ai, bài toán gì, đợt này làm gì |
| 2. Mô tả nghiệp vụ trên hệ thống Viindoo | nhóm theo **dòng chảy đơn hàng**, mỗi nhóm có câu dẫn, gạch ý, và khối **Cần làm rõ ở giai đoạn Khảo sát** |
| 3. Các yêu cầu cần phát triển ngoài phạm vi gói | mỗi hạng mục một khối, **có giá riêng**, bố cục: Bài toán hiện nay / Hệ thống sẽ làm gì / Vì sao phải phát triển thêm / Giới hạn phạm vi |
| 4. Cách tiếp cận | thẻ gạch ý |
| 5. Quy trình triển khai | các giai đoạn theo phương pháp luận Viindoo |
| 6. Kế hoạch triển khai chi tiết | bảng tiến độ theo tuần, các gói nối tiếp nhau |
| 7. Báo giá | 7.1 trả một lần (tách Express và Phát triển), 7.2 trả định kỳ theo năm |
| 8. Khuyến nghị | thẻ gạch ý |
| (cuối) Đề xuất giai đoạn sau | nếu có, luôn là mục đánh số **cuối cùng**, tiêu đề ghi "(ngoài phạm vi báo giá)" |

Mục 3 mở đầu bằng khối nguyên tắc bắt buộc (`vdoc.NGUYEN_TAC_PHAT_TRIEN`): mỗi hạng mục xây mở rộng trên phân hệ sẵn có, không dựng luồng số liệu song song.

## Luật bắt buộc

1. **Phần phát triển chỉ ghi tiền.** Giá từng hạng mục và tổng - không giờ, không ngày công, không đơn giá theo cấp. Các chữ "Junior", "Senior", "Expert", "manday" không được xuất hiện ở bất kỳ đâu. Soát bằng `vdoc.kiem_ban_gui_khach()` trước khi giao.
   Giữ một câu: chi phí phát triển đã áp dụng AI hỗ trợ lập trình, kiểm thử, viết tài liệu.
2. **Giá và quy tắc tính giá: hỏi Liên hoặc tra bảng giá hiện hành tại thời điểm làm.** Plugin không giữ công thức giá, không giữ đơn giá - quy tắc đổi theo thời điểm và theo từng khách. Đừng mang hệ số hay đơn giá của một dự án cũ sang dự án mới. Cách trình bày và các ghi chú bắt buộc: `references/bang-gia.md`.
3. **Gạch ý thay văn xuôi**, dạng `**Nhãn:** nội dung`.
4. **Mục 2 xếp theo dòng chảy đơn hàng của khách**, không theo mã BR: dữ liệu nền - CRM - bán hàng - kế hoạch và lệnh sản xuất - mua hàng - kho - sản xuất và chất lượng - thuê ngoài - bảo trì - giao hàng - nhân sự và lương - kế toán - giá thành - phân quyền. Trong mỗi nhóm xếp theo thứ tự việc diễn ra. Luôn có nhóm CRM dù khách chưa nêu; khách có sản xuất thì phải có bảo trì.
5. **Điểm chưa chắc để vào khối "Cần làm rõ ở giai đoạn Khảo sát"**, không trộn vào phần khẳng định. Chỉ đưa vào đây điểm mà câu trả lời làm đổi giải pháp, phạm vi gói hay chi phí.
6. **Không nêu con số lấy từ hệ thống đang chạy của khách** - số bản ghi, số tiền của khách. Giữ số của chính Viindoo: giờ gói, tuần, giá. Phân biệt "chuẩn hóa quy trình" với "chuẩn hóa dữ liệu".
7. **Giờ công là giờ công chuyên viên Viindoo**, không phải giờ lịch; nhiều chuyên viên song song thì cộng dồn; thời gian khách tự nhập liệu, tự đọc tài liệu không tính. Thời lượng từng hạng mục chốt ở giai đoạn Khảo sát và Lập kế hoạch; tổng giờ gói cố định theo hợp đồng.
8. **Không cắt giờ khảo sát** vì đã có tài liệu phân tích làm sẵn - tài liệu tổng quan không thay thế khảo sát thực địa với từng phòng ban.
9. **Tách Dịch vụ Triển khai khỏi Dịch vụ Phát triển.** Gói Express chỉ gồm tính năng có sẵn và cấu hình.
10. **Phạm vi bám danh mục BR đã chốt** ở bước 3. Khách nhắc hạng mục chưa có trong BR thì báo ra chat, không tự thêm vào báo giá.
11. **Tái dùng khuôn, viết lại nội dung.** Bố cục, bảng, công thức giữ nguyên; mọi dòng nội dung viết lại theo khách mới sau khi đọc lại tài liệu nghiệp vụ của họ.
12. **Các gói nối tiếp nhau** kiểu scrum, chỉ gối phần giám sát.
13. **Chỉ dùng dấu gạch ngang ASCII** `-`.

## Cách dựng

```python
import sys, os, glob
KIT = os.environ.get("CLAUDE_PLUGIN_ROOT") or sorted(
    glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/viindoo-presales/*")))[-1]
sys.path.insert(0, os.path.join(KIT, "kit", "lib"))
import vdoc
import data as D

# Mục 2 - mỗi nhóm: tiêu đề, câu dẫn, gạch ý, điểm cần làm rõ
muc2 = "".join(vdoc.nhom_nghiep_vu(ten, dan, y, lam_ro) for ten, dan, y, lam_ro in D.SEC2)

# Mục 3 - mỗi hạng mục phát triển một khối, có giá riêng
muc3 = vdoc.NGUYEN_TAC_PHAT_TRIEN + "".join(
    vdoc.khoi_phat_trien(x["ten"], vdoc.tien(x["gia"]), x["tom"], x["bai_toan"],
                         x["se_lam"], x["vi_sao"], x.get("gioi_han", []))
    for x in D.DEV)

phan = [
    {"id": "sec-1", "ten": "1. Bối cảnh và phạm vi", "noi_dung": vdoc.gach_y(D.BOI_CANH)},
    {"id": "sec-2", "ten": "2. Mô tả nghiệp vụ trên hệ thống Viindoo", "noi_dung": muc2},
    {"id": "sec-3", "ten": "3. Các yêu cầu cần phát triển ngoài phạm vi gói Viindoo Express", "noi_dung": muc3},
    # 4 cách tiếp cận, 5 quy trình, 6 kế hoạch chi tiết, 7 báo giá, 8 khuyến nghị
]
html = vdoc.phuong_an(
    "Phương án đề xuất triển khai Viindoo", D.MO_TA,
    f"Phương án đề xuất triển khai Phần mềm Quản trị Doanh nghiệp Viindoo<br>Ngày: {D.NGAY} &middot; Khách hàng: {D.KHACH}",
    D.THE_TAG, D.TOM_TAT_SO, vdoc.gach_y(D.TOM_TAT), phan)
open(D.OUT, "w", encoding="utf-8").write(html)

print(vdoc.in_ket_qua_soat(vdoc.kiem_ban_gui_khach(D.OUT)))
```

Giá và phạm vi đọc thẳng từ workbook BR của bước 3 bằng `openpyxl`, không gõ lại tay.

Chi tiết từng mục: `references/bo-cuc-phuong-an.md`. Trình bày báo giá: `references/bang-gia.md`. Hàm của kit: `${CLAUDE_PLUGIN_ROOT}/kit/API.md`.

## Giao ra cái gì

`~/Documents/project/<Khách>/Phuong an de xuat trien khai Viindoo - <Khách>.html`.

**Soạn xong là bản nháp - Liên đọc rồi mới gửi khách**, kể cả khi được bảo "trả lời khách nhé".

Khách đồng ý rồi thì chạy `viindoo-phu-luc-hop-dong` để cắt phụ lục đính kèm hợp đồng ra từ chính bản này.

## Kiểm trước khi giao

1. `vdoc.kiem_ban_gui_khach()` không còn mức PHẢI SỬA; mức "cần xem" thì đọc trích đoạn rồi tự quyết.
2. Không có số nào lấy từ hệ thống đang chạy của khách.
3. Mục 2 xếp đúng dòng chảy đơn hàng, có nhóm CRM, có bảo trì nếu khách có sản xuất; điểm chưa chắc nằm trong khối Cần làm rõ.
4. Mục 3: mỗi hạng mục có giá, có đủ bốn phần, có giới hạn phạm vi.
5. Báo giá đủ năm ghi chú bắt buộc, trong đó có dòng đi lại ăn ở; ưu đãi Cloud nêu rõ điều kiện thu hồi.
6. Mục "giai đoạn sau" (nếu có) nằm cuối và ghi rõ ngoài phạm vi báo giá.
