"""Dựng cảnh NỖI ĐAU cụm Bán hàng + CRM: người thật (Pexels 3129424, lật ngang) + lớp chữ noi_dau_chu.html, chạy được bằng MỘT lệnh.

Lý do có script (bài học cụm Dự án 31/10): đổi lời đọc thì chữ trên màn phải đổi theo - làm tay thì
quên. Đổi câu trong noi_dau_chu.html rồi chạy lại là xong.


Chạy:  python3 dung_noi_dau.py   (CLIP_LANG=en cho bản Anh)
Ra:    quay-fw/noi-dau.webm  (12s, 1920x1080, 60fps) - build_seq.py lấy TỪ ĐẦU (dau=True) để chữ hiện dần.
"""
import os, subprocess
from playwright.sync_api import sync_playwright

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cau_hinh as CH  # đường dẫn dùng chung, xem cau_hinh.py

HERE = os.path.dirname(os.path.abspath(__file__))
NEN = os.path.join(CH.BROLL, "kho-chuoi-cung-ung", "noi-dau-goc.mp4")  # Pexels - ghi nguồn vào NGUON.md cùng thư mục
LANG = os.environ.get("CLIP_LANG", "vi")
_hau = "-en" if LANG == "en" else ""
TMP = os.path.join(HERE, "mo-phong" + _hau)
RA = os.path.join(HERE, "quay-fw" + _hau, "noi-dau.webm")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def anh_chu():
    ra = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5)
        for n in (1, 2):
            pg.goto(f"file://{os.path.join(HERE, 'noi_dau_chu.html')}?n={n}" + ("&lang=en" if LANG == "en" else ""), wait_until="networkidle")
            pg.wait_for_timeout(600)
            d = os.path.join(TMP, f"noi-dau-chu-{n}.png")
            pg.screenshot(path=d, omit_background=True)
            ra.append(d)
        b.close()
    return ra


if __name__ == "__main__":
    c1, c2 = anh_chu()
    vf = ("[0:v]tpad=stop_mode=clone:stop_duration=2,scale=1920:1080,fps=60,format=yuv420p[n];"
          "[1:v]format=rgba,fade=in:st=0.3:d=0.6:alpha=1[a];"
          "[2:v]format=rgba,fade=in:st=1.8:d=0.6:alpha=1[b];"
          "[n][a]overlay=0:0:shortest=1[x];[x][b]overlay=0:0:shortest=1[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", NEN,
                    "-loop", "1", "-framerate", "60", "-t", "12", "-i", c1,
                    "-loop", "1", "-framerate", "60", "-t", "12", "-i", c2,
                    "-filter_complex", vf, "-map", "[v]", "-an", "-t", "12",
                    "-c:v", "libvpx-vp9", "-b:v", "6M", "-row-mt", "1", RA], check=True)
    print("->", RA)
