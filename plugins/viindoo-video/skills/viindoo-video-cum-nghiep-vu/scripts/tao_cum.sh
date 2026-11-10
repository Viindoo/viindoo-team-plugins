#!/bin/bash
# Tạo bộ khung thư mục cho một CỤM NGHIỆP VỤ mới, chép khuôn script từ templates/ của skill.
#
# Chép chứ không trỏ: mỗi cụm có bảng cảnh, bảng màn hình và lời đọc riêng, nên script phải
# sửa được tại chỗ. Khuôn lấy từ các cụm đã chạy thật - bảng cảnh, màn và lời trong đó là của cụm
# gốc, phải thay cho cụm mới.
#
# Chạy:  bash "${CLAUDE_PLUGIN_ROOT}/skills/viindoo-video-cum-nghiep-vu/scripts/tao_cum.sh" Ke-Toan
# Tạo:   ${VIINDOO_VIDEO_WORKDIR:-~/viindoo-video}/Cum/<Ten-Cum>/{clips,demo-data,anh-bia,cat-kenh,video}
set -euo pipefail

CUM="${1:-}"
[ -n "$CUM" ] || { echo "Thiếu tên cụm. Ví dụ: tao_cum.sh Ke-Toan"; exit 1; }

SKILL="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN="$(cd "$SKILL/../.." && pwd)"
GOC="$SKILL/templates"
WORKDIR="${VIINDOO_VIDEO_WORKDIR:-$HOME/viindoo-video}"
DICH="$WORKDIR/Cum/$CUM"

[ -d "$GOC/clips" ] || { echo "Không thấy khuôn: $GOC/clips"; exit 1; }
[ -e "$DICH" ] && { echo "Đã có $DICH - dừng để khỏi ghi đè"; exit 1; }

mkdir -p "$DICH"/{clips,demo-data,anh-bia,cat-kenh,video}
cp "$GOC"/clips/* "$DICH/clips/"
cp "$GOC"/demo-data/* "$DICH/demo-data/"
chmod +x "$DICH"/clips/*.sh 2>/dev/null || true
# Ghi đường dẫn engine của plugin vào cau_hinh.py (đè được bằng biến VIINDOO_VIDEO_ENGINE
# nếu sau này plugin đổi chỗ khi cập nhật).
sed -i.bak "s#__ENGINE__#$PLUGIN/engine#" "$DICH/clips/cau_hinh.py" && rm -f "$DICH/clips/cau_hinh.py.bak"

cat > "$DICH/$CUM-Doi-Tuong-Va-Nhu-Cau.md" <<MD
# Cụm $CUM - đối tượng sử dụng và nhu cầu thị trường

Bước 1 của skill \`viindoo-video-cum-nghiep-vu\` (xem \`references/doi-tuong.md\`).
Chốt xong chân dung này mới viết góc kể.

## 1. Phép đo nhu cầu

## 2. Nguồn đối chiếu (trang đối thủ, báo ngành, thống kê)

## 3. Chân dung đối tượng - CHỌN

- **Ai xem:**
- **Đang dùng gì:**
- **Bài toán:**
- **Kỳ vọng, rút thành hai chữ:**
- **Nhóm bị loại và vì sao:**

## 4. Chỗ Viindoo đứng được (đối chiếu mã nguồn)

## 5. Cửa vào và cú lật

## 6. Chỗ còn yếu trong số liệu
MD

cat > "$DICH/$CUM-Kich-Ban-Clip-Tong.md" <<MD
# Clip tổng thể cụm $CUM

Theo skill \`viindoo-video-cum-nghiep-vu\`. Engine motion: skill \`viindoo-motion-video\`.

## 1. Góc kể (chờ người duyệt nội dung duyệt trước khi dựng hình)

- **Câu phản đề:** $CUM không phải ...
- **Hai mục đích:**
  1.
  2.
- **Dòng chảy 8-10 bước:**

## 2. Bảng cảnh

| # | Cảnh | Màn hình | Con số | Ý nghĩa một câu |
|---|---|---|---|---|

## 3. Nhật ký quyết định

## 4. Việc còn nợ
MD

echo "Đã tạo $DICH"
echo
echo "Việc tiếp theo:"
echo "  1. Dựng chân dung đối tượng vào $CUM-Doi-Tuong-Va-Nhu-Cau.md rồi đưa người duyệt"
echo "     (bước 1 - xem references/doi-tuong.md; chưa chốt đối tượng thì chưa viết góc)"
echo "  2. Viết góc kể vào $CUM-Kich-Ban-Clip-Tong.md rồi đưa người duyệt"
echo "  3. Sửa bảng CANH trong clips/quay_fw.py cho các màn của cụm này"
echo "  4. Sửa bảng cảnh + chữ trong clips/build_seq.py (đổi cả tên tệp seq/voice của cụm gốc)"
echo "  5. Viết lời vào clips/tts_vi_fw.py"
