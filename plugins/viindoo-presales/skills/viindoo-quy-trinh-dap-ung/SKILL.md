---
name: viindoo-quy-trinh-dap-ung
description: Dựng tài liệu "Quy trình nghiệp vụ mục tiêu và mức đáp ứng của giải pháp" - bước 2 trong bộ bốn tài liệu presales Viindoo. Vẽ từng quy trình thành sơ đồ làn theo vai trò, rồi chấm mức đáp ứng bốn lớp (Odoo có sẵn / Viindoo bổ sung / Tùy chỉnh không viết code / Phải lập trình) cho từng yêu cầu, có bằng chứng đọc từ mã nguồn và truy vết về mã BR lẫn vị trí gốc trong tài liệu khách gửi. Dùng khi người dùng nói "vẽ quy trình nghiệp vụ cho khách", "đánh giá mức độ đáp ứng của Viindoo", "Viindoo đáp ứng tới đâu yêu cầu của khách này", "làm tài liệu fit-gap dạng quy trình", "tài liệu số 2 của dự án". KHÔNG dùng cho - mô tả doanh nghiệp (→ viindoo-mo-hinh-hoat-dong), bảng BR và bóc giờ (→ viindoo-danh-muc-br), báo giá (→ viindoo-phuong-an-de-xuat), sinh file .bpmn chuẩn OMG (→ spec-to-bpmn).
---

# Bước 2 - Quy trình nghiệp vụ mục tiêu và mức đáp ứng

Tài liệu nặng nhất của bộ bốn. Trả lời hai câu hỏi cùng lúc: **sau khi lên Viindoo thì công việc chạy thế nào** (sơ đồ từng quy trình, ai làm bước nào), và **giải pháp đáp ứng tới đâu** (bốn lớp, có bằng chứng).

Đây là tài liệu khách soi kỹ nhất, cũng là nơi Viindoo dễ hứa quá nhất. Luật xếp lớp ở dưới sinh ra để chặn việc đó.

## Dùng ở đâu trong quy trình presales

| Mốc | Việc | Tài liệu |
|---|---|---|
| Nhận lead, có hồ sơ khách | hiểu doanh nghiệp | bước 1 mô hình hoạt động |
| **Sau khảo sát, đã có danh sách yêu cầu** | **chốt Viindoo hiểu đúng, chấm mức đáp ứng** | **bước 2 - tài liệu này** |
| Nội bộ, trước khi ra giá | bóc giờ, biết giá vốn | bước 3 danh mục BR |
| Chào giá, trình bày với khách | chốt phạm vi và tiền | bước 4 phương án đề xuất |
| Khách đồng ý, chuẩn bị ký | đính kèm hợp đồng | bước 5 phụ lục hợp đồng |
| Sau ký, vào triển khai | thống nhất thao tác từng vị trí | QTUD (ngoài bộ này) |

Làm sau khi khách đã phản hồi tài liệu bước 1 và đã gom đủ yêu cầu từ khảo sát các phòng ban.

## Khi nào dùng

- "Vẽ quy trình nghiệp vụ cho khách X"
- "Đánh giá Viindoo đáp ứng tới đâu"
- "Làm fit-gap nhưng dạng tài liệu đọc được, không phải bảng Excel"
- Đã có bước 1 và đã gom đủ yêu cầu của khách

## Đầu vào

- Tài liệu bước 1 đã gửi và ý kiến khách phản hồi.
- Danh sách yêu cầu của khách: tệp yêu cầu khách gửi, biên bản khảo sát từng phòng ban, blueprint hệ thống cũ nếu có.
- Mã nguồn Viindoo và Odoo của đúng phiên bản sẽ triển khai.

## Cấu trúc tài liệu

**Phần 0 - Tổng quan**
- Mô hình doanh nghiệp rút gọn (một đoạn, thừa kế bước 1).
- Dòng chảy vận hành tổng thể và các mảng hỗ trợ nối vào dòng chính.
- **Bản đồ quy trình**: bảng Mảng | Mã | Quy trình | Mức đáp ứng - đọc một trang là thấy toàn cảnh.
- Cách đọc sơ đồ, cách đọc mức đáp ứng, căn cứ kết luận, cách truy vết yêu cầu.

**Phần thân - mỗi quy trình một khối**, gồm:
- Mã quy trình và tên (ví dụ `PUR-02 Mua nguyên vật liệu theo kế hoạch`).
- Bốn ô ngữ cảnh: ai chạy, khi nào bắt đầu, kết thúc khi nào, chứng từ sinh ra.
- **Sơ đồ làn** - mỗi làn một vai trò, các bước trái sang phải.
- **Nghiệp vụ chi tiết** - diễn giải từng bước bằng lời của người làm nghề.
- **Khối mức đáp ứng** - thanh tỷ lệ bốn lớp, rồi liệt kê từng yêu cầu: phần hệ thống đã làm được, phần còn thiếu, module làm nền, mã BR và vị trí gốc.

**Phần cuối** - tài liệu kèm theo và những điểm cần khách xác nhận.

## Bốn lớp đáp ứng

| Lớp | Nghĩa | Hệ quả về tiền |
|---|---|---|
| `odoo` | Lõi Odoo Community của phiên bản đang xét đã có sẵn | Dùng được sau cấu hình |
| `viindoo` | Phải có phân hệ Viindoo mới lo được | Dùng được sau cấu hình |
| `tuy_chinh` | Phần thiếu làm bằng Trình tùy chỉnh ngay trên hệ thống đang chạy, không viết code | Phải làm thêm |
| `lap_trinh` | Phần thiếu phải viết code | Phải làm thêm |

**Tách phần đã có và phần còn thiếu.** Một yêu cầu đáp ứng một phần thì tính thành **hai hạng mục**: `phan_co` (lớp đã lo được) và `phan_thieu` (lớp phải làm thêm). Có thế tỷ lệ trên thanh mới phản ánh đúng khối lượng phải làm.

## Luật bắt buộc

1. **Đọc mã nguồn, không suy từ tên chức năng.** Dùng MCP `odoo-semantic` (`model_inspect`, `module_inspect`, `find_examples`) trên profile Viindoo của đúng phiên bản, hoặc agent `viindoo-source-explorer`. Mỗi kết luận phải chỉ được ra model, trường, phương thức hoặc view thật. Đánh giá theo Odoo Community thuần sẽ ước lượng thừa - phân hệ Viindoo phủ sâu hơn nhiều.
2. **Mô tả không phải bằng chứng.** Tên module, docstring, README, tóm tắt manifest đều là lời khai chưa kiểm. Nguồn thật là thân phương thức, định nghĩa trường, arch của view.
3. **Xếp lớp `lap_trinh` khi chưa chắc.** Cần trường tính theo công thức, cầu nối hệ thống ngoài, thuật toán nghiệp vụ, chặn chứng từ, báo cáo nối nhiều tầng thì xếp lập trình - kể cả khi một phần hạng mục đó tùy chỉnh được. Thà ước thừa còn hơn hứa quá.
4. **Xếp lớp `tuy_chinh`** chỉ khi phần thiếu nằm trọn trong những việc Trình tùy chỉnh làm được: thêm trường, sửa và thêm loại màn hình, tạo loại dữ liệu mới, trình đơn, mẫu in, phân quyền, quy tắc tự động, bộ lọc.
5. **Tận dụng cái đã có trước khi thiết kế phần mới.** Trước khi xếp một yêu cầu là phải làm thêm, chỉ ra cụm module sẵn có liên quan đã có gì (model, trường, luồng, tệp:dòng), rồi mới thiết kế phần còn thiếu như một mở rộng trên đó. Không dựng đối tượng song song với cái chuẩn đã có.
6. **Không tự thêm yêu cầu.** Chỉ đúng những gì khách nêu trong tài liệu, mô tả lead, khảo sát. Tính năng có sẵn (Tiêu chuẩn, Cấu hình) thì được chủ động đưa vào cho giải pháp trọn vẹn, ghi nguồn "nghiệp vụ chuẩn". Hạng mục **phải phát triển** mà khách chưa nêu thì liệt kê riêng ra chat và hỏi Liên, không tự đưa vào tệp.
7. **Mỗi yêu cầu kèm truy vết** - mã BR trong danh mục và vị trí gốc trong tài liệu khách gửi (`ô E16 · nhóm 5 Mua hàng · cột Yêu cầu chi tiết`). Nhãn truy vết đọc thẳng từ tệp khách gửi, không gõ tay tên nhóm.
8. **Không nêu con số lấy từ hệ thống đang chạy của khách.**
9. **Chỉ dùng dấu gạch ngang ASCII** `-`.

## Cách dựng

Nội dung quy trình tách thành nhiều tệp theo mảng (`qt_mua_kho.py`, `qt_san_xuat.py`...) để mỗi tệp còn đọc được; builder gom lại. Sơ đồ, thanh tỷ lệ và nhãn truy vết lấy từ kit:

```python
import sys, os, glob
KIT = os.environ.get("CLAUDE_PLUGIN_ROOT") or sorted(
    glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/viindoo-presales/*")))[-1]
sys.path.insert(0, os.path.join(KIT, "kit", "lib"))
import vdoc, vsodo, vykien

QT = {
  "ma": "PUR-02", "ten": "Mua nguyên vật liệu theo kế hoạch",
  "lanes": ["Kế hoạch", "Mua hàng", "Giám đốc", "Kho"],
  "steps": [
    ("s1", 0, "Chốt nhu cầu vật tư theo kế hoạch tuần", "task", None),
    ("s2", 1, "Lập đề nghị mua", "task", None),
    ("s3", 2, "Giá trị trên ngưỡng?", "dec", [("s4", "có"), ("s5", "không")]),
    ("s4", 2, "Duyệt", "task", [("s5", None)]),
    ("s5", 1, "Phát hành đơn mua", "task", None),
    ("s6", 3, "Nhận hàng, kiểm đếm", "task", None),
  ],
  "hang_muc": [
    {"br": "BR-MH-01", "nguon": "ô E16 · nhóm 5 Mua hàng · cột Yêu cầu chi tiết",
     "yeu_cau": "Lập đề nghị mua khi tồn dưới định mức",
     "phan_co": "odoo", "co": "purchase.requisition sẵn có trong lõi",
     "phan_thieu": None},
  ],
}
svg = vsodo.so_do(QT["lanes"], QT["steps"])
thanh = vsodo.thanh(QT["hang_muc"], nhan=vsodo.nhan_lop("Odoo Community 20 có sẵn"))
```

Tài liệu hoàn chỉnh dựng bằng `vdoc.tai_lieu(...)` với `css_them=vdoc.css("quy-trinh") + vykien.css()`.
Đủ hàm của kit: `${CLAUDE_PLUGIN_ROOT}/kit/API.md`. Mẫu khối đáp ứng đầy đủ: `references/khoi-dap-ung.md`.

## Giao ra cái gì

`~/Documents/project/<Khách>/[<Khách>] 2. Quy trinh nghiep vu muc tieu va muc dap ung.html`.

Tài liệu này là nguồn để làm bước 3: mỗi hạng mục trong khối đáp ứng thành một dòng BR, lớp đáp ứng thành cột Phân loại, phần còn thiếu thành cột Giải pháp.

## Việc KHÔNG làm ở bước này

- Không ghi giờ, ngày công, giá (bước 3 và 4).
- Không vẽ As-Is của khách cho đủ bộ - tài liệu này là quy trình **mục tiêu** trên Viindoo. Cần As-Is và To-Be theo chuẩn BPMN 2.0 thì dùng `spec-to-bpmn`.
