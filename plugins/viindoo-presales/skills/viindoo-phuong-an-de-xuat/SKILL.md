---
name: viindoo-phuong-an-de-xuat
description: Dựng "Phương án đề xuất triển khai Viindoo" gửi khách theo bố cục mẫu JVC Eco v3 - bước 4, tài liệu chốt của bộ bốn tài liệu presales Viindoo. Gồm tóm tắt điều hành, bối cảnh và phạm vi, mô tả nghiệp vụ trên hệ thống xếp theo dòng chảy đơn hàng, các yêu cầu cần phát triển ngoài gói, cách tiếp cận, quy trình và kế hoạch triển khai, phân bổ giờ công, báo giá tách gói Express khỏi dịch vụ phát triển, khuyến nghị. Dùng khi người dùng nói "làm phương án đề xuất cho khách", "báo giá triển khai Viindoo", "dựng đề xuất gửi khách", "lên phương án triển khai như mẫu JVC", "tài liệu số 4 của dự án", "làm bản đề xuất phạm vi và dự toán". KHÔNG dùng cho - file BR Excel nội bộ (→ viindoo-danh-muc-br), mô tả doanh nghiệp (→ viindoo-mo-hinh-hoat-dong), đánh giá mức đáp ứng (→ viindoo-quy-trinh-dap-ung), hợp đồng hay QTUD.
---

# Bước 4 - Phương án đề xuất triển khai

Tài liệu khách mang đi họp và ra quyết định. Bố cục theo mẫu JVC Eco v3 - **không tự sáng tác cấu trúc mới**, vì mẫu này khách và đội bán hàng đã quen.

Audience là người ra quyết định: dòng đầu phải đọc 30 giây biết cần quyết gì.

## Khi nào dùng

- "Làm phương án đề xuất / báo giá triển khai cho khách X"
- "Dựng đề xuất gửi khách như mẫu JVC"
- Đã có bước 3 (danh mục BR đã bóc giờ)

## Bố cục - chín mục

| Mục | Nội dung |
|---|---|
| Tóm tắt điều hành | 3-4 thẻ số của Viindoo (tổng đầu tư, thuê bao, tiến độ) + một đoạn gạch ý |
| 1. Bối cảnh và phạm vi | khách là ai, bài toán gì, phạm vi đợt này |
| 2. Mô tả nghiệp vụ trên hệ thống Viindoo | nhóm theo **dòng chảy đơn hàng**, xem luật 3 |
| 3. Các yêu cầu cần phát triển ngoài phạm vi gói | tên hạng mục + giá từng hạng mục, **không giờ** |
| 4. Cách tiếp cận | gạch ý có nhãn |
| 5. Quy trình triển khai | các giai đoạn của phương pháp luận Viindoo |
| 6. Phân bổ giờ công theo giai đoạn | giờ công chuyên viên Viindoo, xem luật 5 |
| 7. Kế hoạch triển khai chi tiết | theo tuần, gói nối tiếp nhau |
| 8. Báo giá | 8.1 trả một lần (tách Express và Phát triển), 8.2 trả định kỳ theo năm |
| 9. Khuyến nghị | gạch ý |
| (cuối) Đề xuất giai đoạn sau | luôn là mục **đánh số cuối cùng**, tiêu đề ghi "(ngoài phạm vi báo giá)" |

## Luật bắt buộc

1. **Phần phát triển chỉ ghi tiền, không ghi giờ.** Ngày công, đơn giá Junior/Senior/Expert, giờ từng hạng mục là nội bộ. Trong tài liệu gửi khách: danh sách "Tên hạng mục (BR-x): số tiền" và tổng. Không được xuất hiện chữ "ngày công", "Junior", "Senior", "Expert", "manday" ở bất kỳ đâu - thẻ đầu trang, tóm tắt, tiêu đề cột, ghi chú, biểu tiến độ. Gọi `vdoc.kiem_ban_gui_khach(<tệp>)` trước khi giao, phải trả về danh sách rỗng.
   Giữ một dòng: chi phí phát triển đã áp dụng AI hỗ trợ lập trình, kiểm thử, viết tài liệu.
2. **Gạch ý thay văn xuôi**, dạng `**Nhãn:** nội dung` - cho tóm tắt điều hành, bối cảnh, giới thiệu từng mục, thẻ cách tiếp cận và khuyến nghị, ô ghi chú, mô tả dài trong ô bảng.
3. **Mục 2 xếp theo dòng chảy đơn hàng của khách**, không theo mã BR: CRM - bán hàng - đề nghị và lệnh sản xuất, định mức - mua nguyên vật liệu - kho - sản xuất và kiểm soát chất lượng - bảo trì - xuất kho giao hàng - kế toán - nhân sự - lương. Trong mỗi nhóm cũng xếp theo thứ tự diễn ra. Ngành đã có bộ quy trình riêng thì nhóm theo bộ quy trình đó và import thẳng tệp quy trình ngành làm nguồn, không chép tay. Luôn có nhóm CRM với tính năng có sẵn dù khách chưa nêu.
   **Khách có sản xuất thì phải có bảo trì** trong phạm vi.
4. **Không nêu con số lấy từ hệ thống đang chạy của khách** - số bản ghi, số tiền của khách. Đánh giá hiện trạng để đầu mục tổng quát theo nghiệp vụ. Giữ số của chính Viindoo: giờ, tuần, giá. Phân biệt "chuẩn hóa quy trình" (quy trình nghiệp vụ) với "chuẩn hóa dữ liệu" (dọn bản ghi) - đừng dán nhầm nhãn.
5. **Giờ công là giờ công chuyên viên Viindoo**, không phải giờ lịch; nhiều chuyên viên song song thì cộng dồn; thời gian khách tự nhập liệu, tự đọc tài liệu không tính. Ghi chú dưới bảng: thời lượng từng hạng mục thống nhất ở giai đoạn Khảo sát và Lập kế hoạch, tổng giờ gói cố định theo hợp đồng.
6. **Không cắt giờ khảo sát** vì đã có tài liệu hay fit-gap làm sẵn. Tài liệu tổng quan ngành không thay thế khảo sát thực địa với từng phòng ban. Giữ tỷ lệ chuẩn theo phương pháp luận triển khai hoặc theo tiền lệ dự án thật đã chạy.
7. **Tách Dịch vụ Triển khai khỏi Dịch vụ Phát triển.** Gói Express chỉ gồm tính năng có sẵn và cấu hình; phần viết code là dòng dịch vụ riêng. Không gộp giờ tùy biến vào gói Express.
8. **Giá và ưu đãi**:
   - Nâng cấp phiên bản: 54.000.000 đ một phiên bản, phiên bản kế tiếp giảm 50%. Viindoo tặng thì vẫn ghi đủ giá rồi ghi ưu đãi 100%, không ghi "không tính phí" trần.
   - Ưu đãi 15% gói Express cho khách dùng Cloud chỉ áp cho gói Express **đầu tiên**. Khách đã từng mua Express thì gói sau tính đủ giá - kiểm lại lịch sử đơn hàng trước khi ghi ưu đãi.
   - Thuê bao chỉ ghi đơn giá gói trên người dùng trên tháng, không nhân ra tổng.
   - Mục "Chưa gồm" luôn có: chi phí đi lại, ăn ở của chuyên viên Viindoo khi làm việc tại khách.
   - Giá ghi "Không thuộc đối tượng chịu thuế GTGT" theo mẫu.
   - Giá dịch vụ và gói lấy từ bảng giá hiện hành, không nhớ áng chừng.
9. **Phạm vi bám theo danh mục BR đã chốt** ở bước 3, không sửa theo lời khách nói sau đó. Khách nhắc hạng mục chưa có trong BR thì báo ra chat, không tự thêm vào báo giá.
10. **Tái dùng khuôn, viết lại nội dung.** Cấu trúc mục và công thức giữ nguyên; mọi dòng nội dung chi tiết viết lại theo khách mới.
11. **Tiến độ: các gói nối tiếp nhau** theo kiểu scrum, chỉ gối phần giám sát. Không chạy song song hai gói.
12. **Chỉ dùng dấu gạch ngang ASCII** `-`.

## Cách dựng

```python
import sys, os, glob
KIT = os.environ.get("CLAUDE_PLUGIN_ROOT") or sorted(
    glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/viindoo-presales/*")))[-1]
sys.path.insert(0, os.path.join(KIT, "kit", "lib"))
import vdoc
import data as D

phan = [
    {"id": "sec-1", "ten": "1. Bối cảnh và phạm vi", "noi_dung": vdoc.gach_y(D.BOI_CANH)},
    # ... các mục còn lại
]
html = vdoc.phuong_an(
    "Phương án đề xuất triển khai Viindoo",
    D.MO_TA,
    f"Phương án đề xuất số: <strong>{D.SO}</strong> &middot; Phiên bản {D.VER}<br>Ngày: {D.NGAY} &middot; Khách hàng: {D.KHACH}",
    D.THE_TAG,
    [(vdoc.tien(D.TONG), "Tổng đầu tư trả một lần"), (f"{D.TUAN} tuần", "Tiến độ triển khai dự kiến")],
    vdoc.gach_y(D.TOM_TAT),
    phan)
open(D.OUT, "w", encoding="utf-8").write(html)

con_sot = vdoc.kiem_ban_gui_khach(D.OUT)
assert not con_sot, f"Còn từ cấm trong bản gửi khách: {con_sot}"
```

Dữ liệu giá và giờ **đọc thẳng từ danh mục BR** của bước 3 (`openpyxl`), không gõ lại tay - một con số khai một nơi.

Xem `references/bo-cuc-phuong-an.md` cho nội dung chi tiết từng mục và `references/bang-gia.md` cho cách trình bày báo giá.

## Giao ra cái gì

`~/Documents/project/<Khách>/Phuong an de xuat trien khai Viindoo - <Khách>.html`.

In ra PDF gửi khách, hoặc gửi thẳng tệp HTML. **Soạn xong là bản nháp - Liên đọc rồi mới gửi khách**, kể cả khi được bảo "trả lời khách nhé".

## Kiểm trước khi giao

1. `vdoc.kiem_ban_gui_khach()` trả về rỗng.
2. Không có số nào lấy từ hệ thống đang chạy của khách.
3. Mục 2 xếp đúng dòng chảy đơn hàng, có nhóm CRM, có bảo trì nếu khách có sản xuất.
4. Mục "Đề xuất giai đoạn sau" nằm cuối và ghi rõ ngoài phạm vi báo giá.
5. Ưu đãi 15% chỉ xuất hiện khi đây là gói Express đầu tiên của khách.
6. Mục "Chưa gồm" có dòng đi lại, ăn ở.
