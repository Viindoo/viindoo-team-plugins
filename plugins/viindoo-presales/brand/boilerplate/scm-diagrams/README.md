# SCM Principles Diagrams

3 diagram **Viindoo luôn insert vào Section 3 của mọi QTUD**.
Trích từ file Nasilkmex Phòng Kinh doanh BPMN (47-page drawio, KH Dệt Lụa Nam Định đã ký).

## Files

| Code | Title | Source page (Nasilkmex) | File |
|---|---|---|---|
| SCM-01 | Nguyên lý tự động hóa chuỗi cung ứng trên Viindoo | Page 40 | `scm-01-supply-chain-automation.drawio` |
| SCM-02 | Nguyên lý hoạt động MTO, MTS, MPS | Page 41 | `scm-02-mto-mts-mps.drawio` |
| SCM-03 | Tổng quan Định tuyến cung ứng | Page 44 (Tổng quan Định tuyến cung ứng) | `scm-03-supply-routing.drawio` |

## Cần làm để dùng được

**Bước 1**: Render PNG từ 3 file .drawio này (bắt buộc - QTUD .docx embed PNG, không embed .drawio).

Cách 1: cài drawio Desktop và chạy:
```bash
brew install --cask drawio
python scripts/export_png.py shared-brand/boilerplate/scm-diagrams/scm-01-supply-chain-automation.drawio --output-dir shared-brand/boilerplate/scm-diagrams/
# lặp cho 3 file
```

Cách 2: mở từng file `.drawio` bằng [diagrams.net web](https://app.diagrams.net/) → File → Export as → PNG → save vào `shared-brand/boilerplate/scm-diagrams/`.

**Bước 2**: Update `section-3-scm-principles.md` để reference 3 file PNG đã sinh (skill auto-pick lên).

## Khi nào skip section 3

Trong dự án không có hoạt động sản xuất + chuỗi cung ứng phức tạp (vd KH chỉ có Bán hàng + Kế toán đơn giản), QTUD KHÔNG cần section 3. `compose_qtud.py` skip nếu KH không có domain SCM/PM/MO/QA/QC/PUR/INV.
