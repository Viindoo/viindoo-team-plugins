# Bản ngôn ngữ thứ hai

Luật Liên: **bản tiếng Việt duyệt trước, bản tiếng Anh dựng theo** - chỉ sửa chỗ cần sửa, không kể
lại câu chuyện khác. Mọi script chạy được hai ngôn ngữ qua `CLIP_LANG=vi|en`.

Đây là chỗ sai nhiều nhất của cả dây chuyền, vì **mọi lỗi ở đây đều chạy trót lọt**: lệnh không báo
lỗi, file vẫn ra, chỉ sai khi người xem nhìn. Soát lại từng thứ gắn ngôn ngữ, đừng tin là đã có.

## Quét HẾT dữ liệu rồi mới quay - đừng quay trước dịch sau

Bài học đắt nhất của cụm Dự án (31/10-01/11/2026): tôi **quay ba lượt** vì mỗi lượt
lại phát hiện thêm chữ Việt chưa dịch. Mỗi lượt 30 màn, mất nửa tiếng.

Cách đúng: trước khi quay một màn nào, **quét toàn bộ chữ sẽ hiện lên** rồi dịch một
lần. Quét bằng cách dò dấu tiếng Việt trên MỌI mô hình xuất hiện trong clip, không chỉ
mô hình mình tạo ra:

```python
V = r"[àáâãèéêìíòóôõùúăđạảấầệếớợịỉũưồởữặẵẫỗốớờ]"
for model, truong in [("project.task","name"), ("project.milestone","name"),
                      ("project.update","name"), ("mail.activity","summary"),
                      ("ir.filters","name"), ("ir.actions.server","name"),
                      ("res.partner","name"), ("res.company","name"), ...]:
    la = [x for x in call(model,"search_read",[[],[truong]]) 
          if re.search(V, (x[truong] or "").lower())]
```

**Và dù quay ba lượt vẫn còn sót.** Bản tiếng Anh cụm Dự án đăng ngày 01/11/2026 phải
hạ xuống không công khai hôm sau vì tám nhóm dữ liệu nữa còn tiếng Việt - trong đó có
hẳn ba màn hình mà MỌI dòng chữ đều tiếng Việt (danh sách dự toán, quy tắc tự động, cổng
khách hàng). Bài học thật không phải "quét kỹ hơn" mà là **soát bằng mắt trước khi đăng**:
cắt một khung của từng cảnh ra ghép thành vài tấm rồi nhìn. Mất vài phút, bắt được sạch.
Danh sách quét bằng máy luôn thiếu, vì nó chỉ chứa những mô hình mình kịp nghĩ ra.

Nhóm bị sót lần đó, thêm vào danh sách quét: `sale.order.line`, `purchase.order.line`,
`account.move.line` (dòng mô tả hàng), `res.partner` (khách và nhà cung cấp),
dự toán/`account.analytic.plan`, ngân sách, `account.asset`, `base.automation` và
`ir.actions.server` (tên quy tắc tự động), cùng phần chữ của website cổng khách
(`website.menu`, tên giai đoạn `project.task.type`).

Ba thứ tôi bỏ sót lần lượt ở ba lượt quay, đều vì chỉ nhìn bản ghi MÌNH tạo:

1. **38 đầu việc của dự án khác** lọt vào khung Gantt khi bỏ bộ lọc.
2. **Bản tin dự án + 2 mốc** của một dự án cũ hiện trên bảng thông tin.
3. **197 hoạt động** (`mail.activity.summary`) hiện ở cột "Hoạt động tiếp theo" của
   mọi màn danh sách việc, cùng **tên hành động máy chủ** sinh ra chúng.

## Bốn chỗ gắn ngôn ngữ phải soát

1. **Đường dẫn ảnh màn hình.** Mã hay ghi cứng thư mục bản gốc (`captures-fw`) nên bản mới nhúng
   nhầm ảnh giao diện ngôn ngữ cũ. Phải có hậu tố: `"captures-fw" + _hau`.
2. **Nhãn chạy suốt clip** (thanh bước, chân trang, nhãn PROOF). Bảng dịch thường đã khai sẵn mà chỗ
   dùng vẫn gọi bảng gốc: `d["steps"] = STEPS_EN if LANG == "en" else STEPS`.
3. **Tên bộ lọc đã lưu.** `quay_fw.py` bấm bộ lọc bằng đúng cái tên - phải khai `fav_en`.
4. **Dữ liệu trong màn hình.** Xem phần dưới - đây là phần dài nhất.

Soát bằng máy trước khi render cả bài: quét kịch bản đã sinh tìm chữ của ngôn ngữ cũ, rồi trích vài
khung hình ra nhìn.

## Trường KHÔNG dịch được là chuyện thường, không phải ngoại lệ

Đo trên máy chủ 31/10/2026 cho cụm Dự án: trong mọi trường hiện chữ trong clip, **chỉ
`hr.department.name` dịch được**. Tất cả còn lại - tên việc, mốc, bản tin, khách hàng,
bộ lọc, dòng chấm công, dòng hoá đơn, hoạt động - đều `translate=False`.

Nên **mặc định là đổi tên tạm rồi trả lại**, chứ đừng mặc định là đặt song song hai
ngôn ngữ. Kèm theo đó:

- Tệp sao lưu phải ghi **trường nào chứa chữ của mô hình nào**. `mail.activity` dùng
  `summary`, `mail.message` dùng `body`, còn lại `name`. Để sót thì `restore` ghi vào
  trường không tồn tại và việc trả lại hỏng âm thầm - mà đó là bước DUY NHẤT đưa hệ
  thống dùng chung về như cũ.
- Hàm `apply` phải **chặn khi thiếu bản dịch**, không đổi một nửa: đổi dở dang thì màn
  quay ra lẫn lộn hai ngôn ngữ mà lệnh dựng không báo gì.

## Ảnh NỀN của thẻ mô phỏng cũng gắn ngôn ngữ

Thẻ mô phỏng (hộp thoại AI, bảng tri thức) thường chồng lên **một ảnh chụp giao diện**.
Đổi chữ trong thẻ mà quên ảnh nền thì hộp thoại tiếng Anh nói trên một bảng việc tiếng
Việt. Cho đường dẫn ảnh nền đi theo ngôn ngữ như mọi đường dẫn khác.

## Dịch dữ liệu demo

Script mẫu: `demo-data/dich_en.py`. Hai nhóm trường, xử lý khác nhau.

### Trường dịch được

Đọc `ir.model.fields.translate` **của chính máy chủ**, đừng đoán theo mã nguồn. Ví dụ
`to_hr_payroll` khai lại `name` không kèm `translate` mà trường cuối cùng vẫn dịch được, vì thuộc
tính kế thừa qua `_inherit`.

Trong cụm HRM: `hr.skill`, `hr.skill.type`, `hr.job`, `hr.department`, `hr.salary.rule`,
`hr.salary.rule.category`, `hr.payslip.line`, `slide.channel`, `attendance.device(.location)`,
`product.template`, `product.attribute(.value)`.

**Thứ tự ghi là sống còn: ghi bản ngôn ngữ MỚI trước, rồi ghi đè lại bản cũ.**

```python
call(model, "write", [[i], {"name": ten_en}], {"context": {"lang": "en_US"}})
call(model, "write", [[i], {"name": ten_vi}], {"context": {"lang": "vi_VN"}})
```

Lý do: `en_US` là ngôn ngữ GỐC của trường dịch được. Khi ghi lại giá trị gốc, Viindoo kéo theo mọi
bản dịch đang TRÙNG giá trị gốc cũ - mà dữ liệu mình bơm thì bản dịch đúng bằng bản gốc (đều tiếng
Việt). Ghi bản cũ trước cho "chắc" KHÔNG cứu được, vì giá trị không đổi nên lượt ghi đó bị bỏ qua.
Làm sai thứ tự một lần: **321 bản ghi mất sạch tên tiếng Việt**.

**Soát lại cả hai ngôn ngữ ngay trong script sau mỗi lượt ghi, lệch là dừng** - đây là cái chặn duy
nhất, vì lỗi này không báo gì cả.

### Trường KHÔNG dịch được

`hr.skill.level` (bậc Cơ bản/Thành thạo), `ir.filters` (tên bộ lọc), `okr.node`, `hr.payslip`,
`res.company`. Cách làm: **đổi tên tạm để chụp, chép tên gốc ra tệp, chụp xong trả lại**.

```bash
python3 dich_en.py apply     # dịch + đổi tên tạm, chép gốc ra en_rename_backup.json
# ... đổi ngôn ngữ giao diện, chụp màn ...
python3 dich_en.py restore   # trả lại y như cũ
python3 dich_en.py check     # soát hai ngôn ngữ của vài bản ghi mẫu
```

Chạy `restore` ngay sau khi chụp xong, đừng để qua đêm - hệ thống demo còn dùng cho việc khác.

### Trường CHÉP giá trị lúc tạo

Có loại bản ghi **chốt giá trị tại thời điểm tạo**, bản dịch của nguồn không chạm tới được.
`hr.payslip.line.name` chép tên từ `hr.salary.rule` lúc tính lương - dịch quy tắc lương xong thì
chữ trên phiếu vẫn nguyên tiếng Việt. Phải dịch riêng, và chỉ dịch bản ghi xuất hiện trong clip
(một phiếu lương, không phải mấy nghìn dòng của mọi phiếu).

Nguyên tắc chung: thấy chữ không đổi sau khi đã dịch nguồn thì tìm xem có bản ghi trung gian nào
chép lại giá trị không.

## Khung khoanh

**Đo lại trên ảnh mới, không bê từ bản ngôn ngữ kia.** Bảng sắp xếp theo tên nên đổi ngôn ngữ là đổi
thứ tự dòng: khung của bản Việt khoanh đúng hai dòng thiếu kỹ năng, bê sang bản Anh thì khoanh nhầm
sang dòng đã đạt. Hàm `find` phải gom theo **nội dung**, và trước khi render thì vẽ khung đè lên ảnh
để mắt kiểm.

## Giọng

Chọn lại giọng cho ngôn ngữ mới - xem `giong-doc.md`. Giọng duyệt ở ngôn ngữ kia không dùng được.

## Khung/thẻ trên cảnh

Nhãn tiếng Anh dài hơn tiếng Việt ("Công tác" -> "Business trips" xuống hai dòng) nên **đừng đặt
chiều cao cứng cho thẻ**. Đo chiều cao thật của nội dung rồi kéo mọi thẻ cùng hàng cao bằng nhau.

## Tiếng

Đo **đỉnh thật**, không đo từng mẫu: từng mẫu ra -0,74 dB mà đỉnh thật đã +2,05 dB, nén AAC xong
file giao ra +1,24 dB. Hạ trần bộ chặn vô ích vì bộ chặn chưa chạm tới. Cách đúng:
`aresample=96000,alimiter=limit=0.89,aresample=48000` rồi bù `volume` cho khớp độ to bản kia.
