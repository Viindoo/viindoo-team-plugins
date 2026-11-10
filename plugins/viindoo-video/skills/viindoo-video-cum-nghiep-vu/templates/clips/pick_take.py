"""Thu NHIỀU bản rồi tự chấm, giữ bản đọc sạch nhất.

Vì sao cần: Gemini TTS đọc tiếng Việt KHÔNG ổn định - cùng một bản viết, mỗi lần thu lại sai
dấu ở một chữ khác ("đông thêm" -> "đồng thềm", "phòng" -> "phóng", "cổng" -> "công"...), và
độ dài chênh nhau tới 20 giây. Sửa chữ nào thì lần sau lại sai chữ khác, nên không thể cứ thu
một bản rồi nghe may rủi.

Cách làm: thu N bản -> cho Gemini chép lại từng bản -> đếm chỗ lệch THẬT (bỏ qua số đếm,
'khoá/khóa', cách viết 'Viindoo') -> giữ bản ít lỗi nhất, hoà thì lấy bản ĐỌC NHANH hơn.

Chạy:  python pick_take.py [số bản, mặc định 3]
Kết quả: voice/ban-hang-crm-vi-fw.wav là bản tốt nhất; các bản thử nằm ở voice/takes/
"""
import importlib.util, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.environ.get("CLIP_LANG", "vi")
TAKES = os.path.join(HERE, "voice", "takes" + ("-en" if LANG == "en" else ""))
FINAL = os.path.join(HERE, "voice", f"ban-hang-crm-{LANG}-fw.wav")

_load = lambda n: (lambda s: (s.loader.exec_module(s_m := importlib.util.module_from_spec(s))
                              or s_m))(importlib.util.spec_from_file_location(
                                  n, os.path.join(HERE, n + ".py")))
tts = _load(f"tts_{LANG}_fw")
chk = _load("check_tts")
vs = _load("voice_stats")

# Lệch KHÔNG tính là lỗi đọc: số đếm (máy chép ghi bằng chữ số), biến thể chính tả 'khoá/khóa',
# và tên Viindoo (chép kiểu gì cũng được vì nghe vẫn đúng).
SO = (r"(không|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|mươi|trăm|nghìn|ngàn|triệu|tỷ|"
      r"lẻ|linh|tư|lăm|rưỡi|phần|đồng|giờ|lượt|phiếu)")
BO_QUA = [re.compile(rf"^{SO}(\s+{SO})*$"), re.compile(r"^kho[áa]$"),
          re.compile(r"^vin\s*[đd]u$"), re.compile(r"^vin+doo$"), re.compile(r"^\d[\d\s]*$")]


def that_su_lech(viet, nghe):
    if viet.replace("á", "a").replace("ó", "o") == nghe.replace("á", "a").replace("ó", "o"):
        return False
    return not (any(p.match(viet) for p in BO_QUA) and any(p.match(nghe) for p in BO_QUA)) \
        and not any(p.match(viet) for p in BO_QUA)


# Chất giọng Liên duyệt (bản 19/10 chị khen): F0 khoảng 122Hz, dải F0 ~90Hz.
# Bản trầm hơn 112Hz hoặc dải dưới 60Hz nghe "trầm và hụt hơi" -> LOẠI, dù đọc đúng chữ.
# Doi sang giong Fenrir (Lien chon 19/10): sang hon, nen nang san len.
# Ban tieng Anh doi sang Iapetus (Lien chon 20/10): Fenrir doc tieng Anh chi ra 115,9Hz,
# Lien nghe la "tram qua, gan, co chu nghe khong ro" -> san 112Hz CU QUA THAP, da nang len
# theo muc Iapetus do duoc (134,8Hz). San thap hon muc Lien da loai la san vo nghia.
F0_MONG_MUON, F0_SAN = (134.0, 126.0) if LANG == "en" else (136.0, 126.0)
DAI_F0_TOI_THIEU = 85.0


def cham(wav, want):
    import difflib
    got = chk.transcribe(wav)
    a, b = chk.words(want), chk.words(got)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    loi = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        viet, nghe = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        if that_su_lech(viet, nghe):
            loi.append((viet or "(trống)", nghe or "(mất)"))
    return loi, got


def dai(wav):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", wav], capture_output=True, text=True)
    return float(p.stdout.strip())


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3
    os.makedirs(TAKES, exist_ok=True)
    want = tts.spoken_text()
    ket_qua = []
    for i in range(1, n + 1):
        wav = os.path.join(TAKES, f"take{i}.wav")
        print(f"\n--- thu bản {i}/{n} ---")
        tts.thu(wav)
        loi, _ = cham(wav, want)
        d = dai(wav)
        st = vs.do(wav)
        bi_loai = st["f0"] < F0_SAN or st["f0_do_rong"] < DAI_F0_TOI_THIEU
        # Chất giọng đứng TRƯỚC số lỗi chữ: bản trầm/đều thì nghe là biết ngay, còn sai
        # một chữ lẻ thì vá được (fix_para.py) hoặc đổi từ rồi thu lại.
        print(f"  {d:.1f}s · {st['f0']:.1f}Hz · dải {st['f0_do_rong']:.1f}Hz · "
              f"{len(loi)} lỗi đọc" + ("  [LOẠI: trầm/đều quá]" if bi_loai else ""))
        for v, g in loi:
            print(f"     {v!r} -> nghe thành {g!r}")
        ket_qua.append((1 if bi_loai else 0, len(loi), d, wav, loi, st))

    ket_qua.sort(key=lambda x: (x[0], x[1], x[2]))
    _, nloi, d, wav, loi, st = ket_qua[0]
    print(f"\n   chất giọng bản chọn: {st['f0']:.1f}Hz, dải {st['f0_do_rong']:.1f}Hz "
          f"(mong muốn ~{F0_MONG_MUON:.0f}Hz, dải >= {DAI_F0_TOI_THIEU:.0f}Hz)")
    shutil.copy(wav, FINAL)
    print(f"\n=== CHỌN {os.path.basename(wav)}: {d:.1f}s, {nloi} lỗi đọc ===")
    for v, g in loi:
        print(f"   còn lệch: {v!r} -> {g!r}")
    print("đã ghi đè", FINAL)


if __name__ == "__main__":
    main()
