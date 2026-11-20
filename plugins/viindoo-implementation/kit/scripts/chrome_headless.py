# -*- coding: utf-8 -*-
"""Chạy Chrome headless để in PDF, chụp PNG mà KHÔNG đụng tới Chrome của người dùng.

Chỉ dùng Chrome for Testing trong ~/.cache/chrome-for-testing/, mỗi lần chạy một thư mục hồ sơ tạm riêng
(--user-data-dir), chờ tiến trình kết thúc rồi dọn hồ sơ tạm và mọi tiến trình còn sót của hồ sơ đó.
Không bao giờ gọi /Applications/Google Chrome.app.
"""
import glob
import os
import pathlib
import shutil
import subprocess
import tempfile

CFT_GLOB = os.path.expanduser(
    "~/.cache/chrome-for-testing/chrome/*/chrome-*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")


def chrome_bin():
    if os.environ.get("CHROME_FOR_TESTING"):   # máy không phải macOS hoặc cài chỗ khác: trỏ thẳng tới tệp chạy Chrome for Testing
        return os.environ["CHROME_FOR_TESTING"]
    found = sorted(glob.glob(CFT_GLOB)) or sorted(glob.glob(os.path.expanduser(
        "~/.cache/chrome-for-testing/chrome/*/chrome-linux64/chrome")))
    if not found:
        raise SystemExit("Không tìm thấy Chrome for Testing trong ~/.cache/chrome-for-testing/ - không dùng Chrome của người dùng")
    return found[-1]


def run(args, timeout=180):
    """Chạy Chrome for Testing headless với hồ sơ tạm; luôn dọn tiến trình và hồ sơ khi xong."""
    prof = tempfile.mkdtemp(prefix="cft-viindoo-")
    cmd = [chrome_bin(), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           "--disable-extensions", "--disable-background-networking", f"--user-data-dir={prof}"] + list(args)
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=timeout)
    finally:
        subprocess.run(["pkill", "-f", prof], capture_output=True)  # tiến trình con còn sót của đúng hồ sơ tạm này
        shutil.rmtree(prof, ignore_errors=True)


def print_pdf(html_path, pdf_path, budget_ms=8000):
    run(["--no-pdf-header-footer", f"--virtual-time-budget={budget_ms}", f"--print-to-pdf={pathlib.Path(pdf_path).resolve()}",
         pathlib.Path(html_path).resolve().as_uri()])


def screenshot(html_path, png_path, w, h, scale=2):
    run(["--hide-scrollbars", f"--force-device-scale-factor={scale}", f"--window-size={int(w)},{int(h)}",
         f"--screenshot={pathlib.Path(png_path).resolve()}", pathlib.Path(html_path).resolve().as_uri()])
