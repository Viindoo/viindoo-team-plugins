"""Xuất khung hình clip qua Playwright -> ffmpeg.
Chạy bằng python có playwright (+ Chrome):
      $VIDEO_PY render.py <clip_dir> sq|v|h preview 3,10,20   (ảnh xem thử vào <clip_dir>/prev/)
      $VIDEO_PY render.py <clip_dir> sq|v|h full              (<clip_dir>/silent_<fmt>.mp4)"""
import os, subprocess, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
clip, fmt, mode = sys.argv[1], sys.argv[2], sys.argv[3]
D = os.path.abspath(clip)
W, H = {"sq": (1080, 1080), "v": (1080, 1920), "h": (1920, 1080)}[fmt]
FPS = 30
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto("file://" + os.path.join(D, f"video_{fmt}.html"))
    pg.wait_for_timeout(800)
    pg.evaluate("document.fonts.ready")
    pg.evaluate("videosReady()")
    dur = pg.evaluate("window.DURATION")
    if mode == "preview":
        os.makedirs(os.path.join(D, "prev"), exist_ok=True)
        for t in map(float, sys.argv[4].split(",")):
            pg.evaluate(f"renderAt({t})")
            pg.screenshot(path=os.path.join(D, "prev", f"{fmt}_{t:05.1f}.png"))
    else:
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                               # ảnh chụp JPEG là sRGB/BT.601 dải đầy đủ -> đổi sang BT.709 dải giới hạn và ghi đủ nhãn màu,
                               # để màu cyan thương hiệu không bị lệch khi YouTube/Facebook/điện thoại phát lại
                               "-vf", "scale=in_color_matrix=bt601:in_range=pc:out_color_matrix=bt709:out_range=tv,format=yuv420p",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
                               "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                               "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709:range=tv",
                               "-movflags", "+faststart",
                               os.path.join(D, f"silent_{fmt}.mp4")], stdin=subprocess.PIPE)
        n = int(dur * FPS)
        for i in range(n):
            pg.evaluate(f"renderAt({i/FPS})")
            for attempt in range(4):
                try:
                    ff.stdin.write(pg.screenshot(type="jpeg", quality=95, timeout=120000)); break
                except Exception as e:
                    print("thử lại khung", i, e.__class__.__name__, flush=True); pg.wait_for_timeout(3000); pg.evaluate(f"renderAt({i/FPS})")
            else:
                raise SystemExit(f"khung {i} lỗi")
            if i % 300 == 0: print(fmt, i, n, flush=True)
        ff.stdin.close(); ff.wait()
    b.close()
