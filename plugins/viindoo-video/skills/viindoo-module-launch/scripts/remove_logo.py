"""Xoá logo công ty thật trên ảnh stock (mũ bảo hộ, áo) bằng OpenCV inpaint, vá đúng hình bầu dục của logo.

Chạy: python3 remove_logo.py <ảnh gốc> <ảnh ra> cx,cy,ax,ay,góc [cx,cy,ax,ay,góc ...] [--ref-width 1600] [--clip-below y0,slope,x0]
  - Toạ độ đo trên ảnh rộng --ref-width (mặc định 1600, tức bản xem trước), tự nhân theo ảnh thật.
  - cx,cy: tâm logo; ax,ay: nửa trục; góc: độ (dương = xoay theo chiều kim đồng hồ).
  - --clip-below y0,slope,x0: bỏ phần mặt nạ nằm dưới đường y = y0 + (x - x0) * slope (tránh kéo màu tối của vành mũ vào vùng vá).
Kiểm tra lại bằng mắt: cắt ô quanh logo và xem; còn viền thì nới trục / chỉnh góc rồi chạy lại.
Cần: opencv-python-headless, numpy (venv riêng: python3 -m venv cv && cv/bin/pip install opencv-python-headless numpy)."""
import sys
import cv2
import numpy as np

args = sys.argv[1:]
ref_w = 1600
clip = None
if "--ref-width" in args:
    i = args.index("--ref-width"); ref_w = float(args[i + 1]); del args[i:i + 2]
if "--clip-below" in args:
    i = args.index("--clip-below"); clip = [float(v) for v in args[i + 1].split(",")]; del args[i:i + 2]
src, dst, ovals = args[0], args[1], args[2:]
im = cv2.imread(src); s = im.shape[1] / ref_w
m = np.zeros(im.shape[:2], np.uint8)
for o in ovals:
    cx, cy, ax, ay, ang = (float(v) for v in o.split(","))
    cv2.ellipse(m, (int(cx * s), int(cy * s)), (int(ax * s), int(ay * s)), ang, 0, 360, 255, -1)
if clip:
    y0, slope, x0 = clip
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
    m[(yy / s) > y0 + (xx / s - x0) * slope] = 0
out = cv2.inpaint(im, m, max(3, int(3 * s)), cv2.INPAINT_TELEA)
out = cv2.inpaint(out, m, max(3, int(3 * s)), cv2.INPAINT_NS)
cv2.imwrite(dst, out, [cv2.IMWRITE_JPEG_QUALITY, 93])
print("ok", dst)
