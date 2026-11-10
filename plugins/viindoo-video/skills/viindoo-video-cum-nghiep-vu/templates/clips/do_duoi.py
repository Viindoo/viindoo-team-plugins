"""Đo CỬA SỔ DÙNG ĐƯỢC của từng bản quay Playwright.

Mỗi bản quay có hai chỗ hỏng ở hai đầu, và CẢ HAI đều không làm lệnh dựng báo lỗi:

1. ĐUÔI - lúc đóng ngữ cảnh, Playwright vẽ lại mấy khung cuối ở kích thước CSS
   thô: trang co về góc trên-trái, phần còn lại thành NỀN XÁM PHẲNG (rgb 126,
   độ lệch 0). Nhận dạng: góc dưới-phải phẳng lì (lệch < 5) VÀ không trắng
   (trung bình < 200). Hai điều kiện đều cần - chỉ "phẳng" thì trang đang tải
   (trắng trơn rgb 253, lệch 0) cũng dính; chỉ "không trắng" thì màn có biểu đồ
   màu cũng dính. ĐỪNG gọi là "nền đen": mắt nhìn ảnh thu nhỏ ra đen, số đo là xám.

2. ĐẦU - khung chưa phải MÀN HÌNH CẦN QUAY: còn ở trang trung gian của bước
   điều hướng, hoặc đã đúng trang nhưng bộ lọc đã lưu chưa kịp áp nên biểu đồ
   trắng trơn. Nhận dạng: DẢI TRÊN CÙNG (thực đơn + đường dẫn + thẻ bộ lọc) chưa
   giống dải ấy ở cuối đoạn sạch. Dải trên định danh màn hình và KHÔNG đổi khi
   cuộn, nên phép này không nhầm cảnh cuộn thành cảnh sai.
   Liên bắt lỗi này ở phút 2:20 bản 31/10 - biểu đồ Lịch thu chi trắng, vì thẻ
   lọc lúc đó mới là "Đã ghi sổ" chứ chưa phải bộ lọc đã lưu.
   ĐỪNG đo bằng "độ đậm nội dung": trang trung gian cũng đậm y như màn cần quay
   (thử 31/10: kanban ở giây 2 làm phép đo báo "dùng được từ giây 0").

Hai phép đo phải TÁCH RIÊNG: khung hỏng ở đuôi lại cho MỰC RẤT CAO (xám đặc
68%), nên dùng mực để dò đuôi thì ngược dấu.

Chạy:  python3 do_duoi.py [thư-mục]      (mặc định quay-fw)
Ghi:   <thư-mục>/cua-so.json  -> build_seq.py đọc tệp này.
"""
import glob, json, os, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image

# Thu muc theo NGON NGU: ban tieng Anh nam o quay-fw-en. Truoc day mac dinh cung
# la "quay-fw" nen chay voi CLIP_LANG=en van do nham ban tieng Viet, roi build_seq
# lay moc cat cua ban kia -> mp4 rong (02/11/2026).
_lang = os.environ.get("CLIP_LANG", "vi")
B = sys.argv[1] if len(sys.argv) > 1 else ("quay-fw-en" if _lang == "en" else "quay-fw")


def ten_trang_web():
    """Ten cac ban quay la TRANG WEB (cong khach hang), khong phai trang quan tri.

    Phan biet nay can cho phep do "nhan man bang dai tren": trang quan tri Odoo co
    thanh thuc don + duong dan DUNG YEN khi cuon than trang, nen dai tren la dau
    hieu dinh danh man rat tot. Trang web thi ca thanh dau trang cung troi theo
    khi cuon -> phep do hieu nham la DOI MAN, va cat mat phan dau (do 31/10: cong
    khach hang mat 7 giay dang hien dung noi dung). Voi trang web chi dung phep MUC.
    """
    try:
        import importlib.util
        sp = importlib.util.spec_from_file_location(
            "qfw", os.path.join(os.path.dirname(os.path.abspath(__file__)), "quay_fw.py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return {c["name"] for c in m.CANH if c.get("khach")}
    except Exception:
        return set()


WEB = ten_trang_web()
NHIP = 5          # khung mỗi giây
TMP = os.path.join(tempfile.gettempdir(), f"do-duoi-{os.getpid()}")


def dai(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


kq = {}
for p in sorted(glob.glob(os.path.join(B, "*.webm"))):
    ten = os.path.basename(p)[:-5]
    D = dai(p)
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf",
                    f"fps={NHIP},scale=320:180", os.path.join(TMP, "k%05d.png")],
                   check=True)
    ks = sorted(glob.glob(os.path.join(TMP, "k*.png")))
    ims = [Image.open(k).convert("RGB") for k in ks]
    w, h = ims[0].size

    def goc(im):
        a = np.asarray(im.crop((int(w * .8), int(h * .8), w, h)), dtype=np.int16)
        return a.reshape(-1, 3)

    def dai_tren(im):
        return np.asarray(im.crop((0, 0, w, int(h * .22))).convert("L"), dtype=np.int16)

    # ĐUÔI: đi NGƯỢC từ khung cuối, chừng nào còn xám thì lùi tiếp. Mốc kết thúc
    # là khung xám ĐẦU TIÊN của dải xám ở đuôi - không phải khung xám cuối cùng
    # (lấy nhầm cái cuối thì mốc rơi vào giữa đoạn hỏng, thử 31/10 ra 20,65s cho
    # bản mà đoạn hỏng bắt đầu từ giây 19,0).
    def xam(im):
        g = goc(im)
        return g.std(axis=0).max() < 5 and g.mean(axis=0).max() < 200

    i = len(ims) - 1
    while i >= 0 and xam(ims[i]):
        i -= 1
    het = (i + 1) / NHIP - 0.15 if i < len(ims) - 1 else D

    # ĐẦU: đi NGƯỢC từ cuối đoạn sạch, dừng ở khung đầu tiên KHÔNG đạt một trong
    # hai điều kiện. Phải đủ CẢ HAI, mỗi cái bắt một kiểu hỏng khác nhau:
    #  - DẢI TRÊN giống mẫu  -> còn ở trang trung gian thì dải trên khác hẳn;
    #  - MỰC đủ đậm          -> đúng trang rồi nhưng bộ lọc chưa áp, biểu đồ trắng.
    # Thiếu một trong hai là lọt: dải trên một mình bị pha loãng vì thẻ lọc quá
    # nhỏ so với cả dải (thử 31/10: biểu đồ trắng ở giây 30 vẫn lọt qua); mực một
    # mình thì trang kanban trung gian cũng đậm y như màn cần quay.
    def muc(im):
        a = np.asarray(im.convert("L"), dtype=np.int16)[int(h * .22):]
        return float((np.abs(a - 255) > 30).mean())

    cuoi = max(0, min(int(het * NHIP) - 1, len(ims) - 1))
    mau = dai_tren(ims[cuoi])
    dau_cua_so = max(0, cuoi - int(2.0 * NHIP))
    # Nguong 0,40 chu khong phai 0,70: phep nay chi duoc bat man GAN NHU RONG, khong
    # duoc bat "it chu hon doan cuoi". Canh CO CUON doi do dam lien tuc - de 0,70 thi
    # cong khach hang bi cat mat 7 giay dau du dang hien dung noi dung (do 31/10).
    # Ca bieu do trang van bi bat: muc 4,5% so voi 14,5% khi da hien = 31%, duoi 40%.
    muc_du = float(np.median([muc(im) for im in ims[dau_cua_so:cuoi + 1]])) * 0.40
    bat_dau = 0.0
    la_web = ten in WEB
    for i in range(cuoi, -1, -1):
        lech = 0.0 if la_web else float(np.abs(dai_tren(ims[i]) - mau).mean())
        if lech > 6 or muc(ims[i]) < muc_du:
            bat_dau = (i + 1) / NHIP
            break

    kq[ten] = {"bat_dau": round(bat_dau, 2), "het": round(het, 2),
               "dung_duoc": round(het - bat_dau, 2)}
    print(f"  {ten:22} dài {D:5.1f}s   dùng được {bat_dau:5.2f} -> {het:5.2f}s "
          f"= {het - bat_dau:5.2f}s", flush=True)

json.dump(kq, open(os.path.join(B, "cua-so.json"), "w"), indent=1)
print(f"\n  ghi {B}/cua-so.json")
