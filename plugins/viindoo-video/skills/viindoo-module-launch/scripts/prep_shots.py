"""Chuẩn bị ảnh màn hình cho một clip từ ảnh chụp thật trong static/description của module.

Chạy: python3 prep_shots.py <clip_dir> <lang> <static_dir> [<static_dir> ...]
  - <clip_dir>/shots_src.json khai báo ảnh cần lấy và ô phóng (tuỳ chọn):
      {"files": {"jobboard": "guide-job-board-landscape", "stop": "guide-stop-machine-01"},
       "boxes": {"vi": {"stop": ["tiles", 108, 355, 692, 505]}, "en": {...}}}
  - Ảnh được tìm theo <tên>.<lang>.jpg|png (rồi <tên>.jpg|png) trong các static_dir, theo thứ tự.
  - Màn dọc (cao >= 1000 px) được cắt ở khoảng trống dài nhất (>= 150 px, sau y=300) để màn hiện to trong video.
  - Ghi <clip_dir>/assets/shots/<khoá>.jpg và shots.json (định dạng build.py đọc).
Cần: Pillow, numpy."""
import json, os, shutil, sys
import numpy as np
from PIL import Image

clip_dir, lang, static_dirs = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3:]
cfg = json.load(open(os.path.join(clip_dir, "shots_src.json"), encoding="utf-8"))
boxes = cfg.get("boxes", {}).get(lang, {})


def find(name):
    for d in static_dirs:
        for cand in (f"{name}.{lang}.jpg", f"{name}.{lang}.png", f"{name}.jpg", f"{name}.png"):
            p = os.path.join(d, cand)
            if os.path.exists(p):
                return p
    sys.exit(f"không thấy ảnh {name} ({lang}) trong {static_dirs}")


def crop_h(img):
    if img.height < 1000:
        return img.height
    a = np.asarray(img.convert("L"), dtype=float)
    empty = a[:, int(img.width * 0.14):int(img.width * 0.86)].std(axis=1) < 4
    run = 0
    for y in range(300, img.height):
        run = run + 1 if empty[y] else 0
        if run >= 150:
            return min(img.height, y - run + 1 + 30)
    return img.height


out = os.path.join(clip_dir, "assets", "shots")
shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
js = []
for key, name in cfg["files"].items():
    im = Image.open(find(name)).convert("RGB")
    h = crop_h(im); im = im.crop((0, 0, im.width, h)); im.save(os.path.join(out, f"{key}.jpg"), quality=92)
    e = {"file": f"{key}.jpg", "w": im.width, "h": h, "desc": name, "boxes": []}
    if key in boxes:
        label, x0, y0, x1, y1 = boxes[key]
        e["boxes"].append({"label": label, "x0": x0, "y0": y0, "x1": x1, "y1": y1})
    js.append(e); print(lang, key, f"{im.width}x{h}")
json.dump(js, open(os.path.join(out, "shots.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
