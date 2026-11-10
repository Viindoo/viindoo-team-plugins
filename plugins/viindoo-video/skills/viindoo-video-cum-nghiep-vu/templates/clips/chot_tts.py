"""Nhat ky so luot goi TTS - de biet da tieu bao nhieu, khong chan.

Vi sao co file nay: 30/10/2026 toi goi 30 luot thu trong mot ngay (~100 phut tieng)
cho mot kich ban Lien van dang sua cau truc, dot gan het han muc thang. Mot clip song
ngu hoan chinh thuc ra chi can 2 LUOT - mot Viet, mot Anh.

Trần không nhỏ. Cách làm mới là chỗ sai. Nên chặn bằng mã, không bằng lời hứa.

Dung:  tu chot_tts import ghi_nhan
       ghi_nhan("Fenrir", so_am_tiet)   # nem SystemExit neu vuot tran ngay

Muon vuot co y thi dat bien moi truong:  TTS_CHO_PHEP=1 python3 ...
"""
import json
import os
import sys
from datetime import date

# Lien bo tran theo ngay (31/10/2026): co ngay dung hai clip, co tuan khong dung clip
# nao - dem theo ngay la sai don vi. Giu NHAT KY de biet da tieu bao nhieu, va chi CANH BAO
# khi mot clip vuot muc hop ly, khong chan nua.
# Ky luat that nam o cho khac: GOM HET SUA ROI MOI THU MOT LUOT.
CANH_BAO_MOI_CLIP = 6
NHAT_KY = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".nhat-ky-tts.json")


def _doc():
    if not os.path.exists(NHAT_KY):
        return {}
    try:
        with open(NHAT_KY, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def ghi_nhan(giong, am_tiet=0):
    """Ghi nhat ky mot luot goi TTS. Khong chan - chi dem va canh bao."""
    hom_nay = date.today().isoformat()
    d = _doc()
    ngay = d.setdefault(hom_nay, {"luot": 0, "am_tiet": 0, "giong": []})
    ngay["luot"] += 1
    ngay["am_tiet"] += int(am_tiet or 0)
    ngay["giong"].append(giong)
    with open(NHAT_KY, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
    print(f"  [nhat ky TTS] luot thu {ngay['luot']} trong ngay"
          f" (~{ngay["luot"] * 10_000:,}d uoc tinh)")
    if ngay["luot"] == CANH_BAO_MOI_CLIP:
        print(f"  [nhat ky TTS] da {CANH_BAO_MOI_CLIP} luot - neu van dang sua LOI DOC thi"
              f" hay DOI CHU trong ban viet\n"
              f"                thay vi thu lai cau may (xem references/giong-doc.md muc TIEN)")


def tom_tat():
    d = _doc()
    if not d:
        print("  chua goi luot nao"); return
    for ngay in sorted(d)[-7:]:
        v = d[ngay]
        print(f"  {ngay}  {v['luot']:2} luot  {v['am_tiet']:5} am tiet  "
              f"{', '.join(sorted(set(v['giong'])))}")


if __name__ == "__main__":
    tom_tat()
