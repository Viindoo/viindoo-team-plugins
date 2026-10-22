---
name: viindoo-phu-luc-hop-dong
description: Dựng Phụ lục hợp đồng (Phụ lục 01 - Kế hoạch triển khai và Phạm vi đáp ứng) bằng cách cắt nguyên văn các mục phạm vi, hạng mục phát triển và kế hoạch chi tiết ra từ bản phương án đề xuất đã gửi khách - bước 5, tài liệu đính kèm hợp đồng khi khách đồng ý ký. Đánh lại số mục cho phụ lục đứng độc lập, thêm dòng số hợp đồng, giữ nguyên định dạng và nội dung để phụ lục không lệch một chữ nào so với bản khách đã đọc; kèm script đóng dấu đầu trang hai logo và số trang khi in PDF. Dùng khi người dùng nói "làm phụ lục hợp đồng cho khách", "cắt phụ lục 01 từ phương án", "phạm vi đáp ứng đính kèm hợp đồng", "khách ký rồi, chuẩn bị phụ lục", "làm phụ lục kế hoạch triển khai". KHÔNG dùng cho - soạn hợp đồng hay điều khoản thương mại, phương án đề xuất (→ viindoo-phuong-an-de-xuat), QTUD khi triển khai, báo giá mới.
---

# Bước 5 - Phụ lục hợp đồng

Phụ lục đính kèm hợp đồng, chốt **phạm vi đáp ứng và kế hoạch triển khai** mà hai bên cam kết.

## Dùng ở đâu trong quy trình presales

| Mốc | Việc | Tài liệu |
|---|---|---|
| Nhận lead, có hồ sơ khách | hiểu doanh nghiệp | bước 1 mô hình hoạt động |
| Sau khảo sát, có danh sách yêu cầu | chốt hiểu đúng, chấm đáp ứng | bước 2 quy trình và mức đáp ứng |
| Nội bộ, trước khi ra giá | bóc giờ, biết giá vốn | bước 3 danh mục BR |
| Chào giá, trình bày với khách | chốt phạm vi và tiền | bước 4 phương án đề xuất |
| **Khách đồng ý, chuẩn bị ký hợp đồng** | **đưa phạm vi vào cam kết pháp lý** | **bước 5 - tài liệu này** |
| Sau ký, vào triển khai | thống nhất thao tác từng vị trí | QTUD (ngoài bộ này) |

Chỉ làm khi khách đã đồng ý phương án. Phụ lục là **lát cắt** của phương án, không phải tài liệu viết mới.

## Nguyên tắc số một

**Không viết lại nội dung.** Cắt nguyên văn các mục khách đã đọc và đồng ý, chỉ đánh lại số mục cho phụ lục đứng độc lập.

Phụ lục lệch với phương án một chữ là mầm mống tranh chấp về sau: khách ký trên phạm vi A, phụ lục ghi phạm vi A' - lúc nghiệm thu mới vỡ ra. Muốn sửa nội dung thì sửa ở phương án rồi cắt lại, đừng sửa thẳng vào phụ lục.

## Cắt những mục nào

Mặc định ba mục, theo bản Quang Thắng:

| Trong phương án | Thành | Vì sao vào phụ lục |
|---|---|---|
| Mục 2 - Mô tả nghiệp vụ trên hệ thống Viindoo | Mục 1 | phạm vi đáp ứng hai bên cam kết |
| Mục 3 - Các yêu cầu cần phát triển ngoài gói | Mục 2 | hạng mục phát triển và giới hạn phạm vi |
| Mục 6 - Kế hoạch triển khai chi tiết | Mục 3 | tiến độ cam kết |

Không đưa vào phụ lục: tóm tắt điều hành, bối cảnh, cách tiếp cận, khuyến nghị (phần bán hàng), và **bảng báo giá** (giá nằm ở điều khoản hợp đồng, không nhắc lại ở phụ lục trừ khi hợp đồng yêu cầu).

## Cách dựng

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/viindoo-phu-luc-hop-dong/scripts/cat_phu_luc.py \
  "~/Documents/project/<Khách>/Phuong an de xuat trien khai Viindoo - <Khách>.html" \
  --hop-dong SO.261020.19726 \
  --ngay "___/___/2026"
```

Tham số khác: `--muc "2,3,6"` đổi các mục cắt, `--ten` đổi tiêu đề phụ lục, `--so-phu-luc 02`, `--ra` đổi đường dẫn ra.

Script tự: lấy `<style>` của phương án nên định dạng y hệt, bỏ thẻ `<section>` thừa ở cuối lát cắt (không thì in ra thừa một trang trắng), đánh lại số mục kèm mọi tham chiếu chéo "Mục 2", "Mục 3", và soát từ chỉ dành cho bản nội bộ.

Ngày ký để trống `___/___/2026` cho khách điền tay khi ký bản cứng.

## Đóng dấu đầu trang và số trang

Hợp đồng in ra thường cần đầu trang có logo hai bên, số hợp đồng, và số trang chạy suốt. In bằng trình duyệt thì `position:fixed` không lặp đúng trên mọi trang, nên làm bằng cách phủ một lớp lên PDF đã in:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/viindoo-phu-luc-hop-dong/scripts/dong_dau_trang.py \
  phu-luc.pdf --ra phu-luc-da-dong-dau.pdf \
  --hop-dong SO.261020.19726 --nhan "Phụ lục 01" \
  --logo-khach "~/Documents/project/<Khách>/Hồ sơ khách hàng/logo-khach.png" \
  --bat-dau 1 --tong 24
```

Cần `pypdf` và Google Chrome. Không có logo khách thì bỏ `--logo-khach`, chỉ đóng logo Viindoo.

## Kiểm trước khi giao

1. **Đối chiếu với phương án**: mở hai tệp cạnh nhau, phần nội dung phải khớp từng chữ. Khác nhau chỗ nào là sai, trừ số mục.
2. Số hợp đồng ở dòng đầu đúng với hợp đồng thật.
3. In thử ra PDF: không có trang trắng thừa, bảng không bị cắt ngang trang, đầu trang và số trang chạy đúng.
4. Các tham chiếu chéo trong nội dung ("xem Mục 2") đã trỏ đúng số mục mới của phụ lục.
5. Soát không còn chữ "Junior", "Senior", "Expert", "manday".

## Việc KHÔNG làm ở bước này

- Không soạn điều khoản hợp đồng, điều khoản thanh toán, phạt vi phạm - đó là việc của bộ phận hợp đồng.
- Không thêm hay bớt phạm vi so với phương án khách đã đồng ý. Phạm vi đổi thì sửa phương án, gửi lại khách, rồi cắt phụ lục mới.
- Không nhắc lại giá trong phụ lục trừ khi hợp đồng yêu cầu rõ.
