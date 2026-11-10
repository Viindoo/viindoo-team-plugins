#!/bin/bash
# Lắp bản giao clip cụm TRAO ĐỔI THÔNG TIN VÀ PHỐI HỢP (chép khuôn cụm Dự án): nối cảnh đồ hoạ + BẢN QUAY THẬT + ảnh + B-ROLL NGƯỜI THẬT,
# rồi trộn lời đọc với nhạc nền.
#
# Khác bộ HRM: phần lớn cảnh là BẢN QUAY THẬT chứ không phải ảnh tĩnh đi qua engine.
# Thứ tự lắp KHÔNG gõ tay ở đây - đọc từ `ke-hoach-lap.json` do `build_seq.py` sinh ra
# (một nguồn sự thật: đổi bảng cảnh hay đổi bản thu thì chạy lại build_seq.py là xong).
#
# B-roll "mượn ĐUÔI cảnh đứng trước" - cảnh đó đã được tính ngắn đi đúng bằng độ dài
# b-roll, nên TỔNG THỜI LƯỢNG VÀ LỜI ĐỌC KHÔNG ĐỔI, không phải thu lại tiếng.
#
# Bản quay cắt LẤY PHẦN ĐUÔI: trạng thái cuối là trạng thái đã soát bằng ảnh khung.
#
# volume: chỉnh theo ĐỘ TO ĐO ĐƯỢC của chính bản thu, không để cố định. Bộ HRM
# để 0.9dB; bản Fenrir 31/10 của cụm này ra -15,8 LUFS ở mức -0.6dB nên nâng
# lên 1.7dB cho khớp mốc -14 LUFS của cả bộ (bản thu theo khối nhỏ tiếng hơn). Bộ chặn đỉnh alimiter giữ đỉnh
# ở -1,0 dB nên nâng không vỡ tiếng.
# thì ra -12,0 LUFS, chênh bản HRM 2,6 dB. Hạ xuống -1,7dB ra -14,3 LUFS.
# Lời đọc để 0.92 + chặn đỉnh trên tần số lấy mẫu GẤP BỐN rồi hạ về: đo từng mẫu thì thấy
# "an toàn" nhưng đỉnh THẬT giữa hai mẫu vẫn vượt trần, và AAC dựng lại đúng cái đỉnh đó.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
LANG_CLIP="${CLIP_LANG:-vi}"
if [ "$LANG_CLIP" = "en" ]; then HAU="-en"; MA="EN"; else HAU=""; MA="VI"; fi
# Mức bù độ to khác nhau theo NGÔN NGỮ, vì bản thu hai thứ tiếng không cùng độ to.
# Đo 02/11/2026: cùng 1,7 dB thì bản Việt ra -13,7 LUFS còn bản Anh chỉ -15,8 LUFS
# (lệch 2,1 dB - quá ngưỡng "độ to khớp bản ngôn ngữ kia"). 4,5 dB kéo bản Anh về
# -13,8 LUFS, đỉnh thật -0,95 dB. Đo lại mỗi khi thu giọng mới, đừng chép mù.
# Ban EN cum nay (Iapetus 142 Hz, 06/11): 4,5 dB ra -12,8 LUFS; 1,6 dB ra -14,7 LUFS, dinh that -0,8 dBFS
if [ "$LANG_CLIP" = "en" ]; then GAIN_MAC_DINH=1.6; else GAIN_MAC_DINH=3.0; fi  # Ban-Hang-CRM 08/11: Fenrir keo 136,8Hz, 3.9dB ra -13,6 LUFS -> 3.0dB  # Achird kéo 137Hz, đo 05/11: -14,9 LUFS, đỉnh -0,82 dB
WORKDIR="${VIINDOO_VIDEO_WORKDIR:-$HOME/viindoo-video}"
SEG="$WORKDIR/output/ban-hang-crm-fw${HAU}-seg"
KE_HOACH="$HERE/ke-hoach-lap${HAU}.json"
VOICE="${VOICE:-$HERE/voice/ban-hang-crm-${LANG_CLIP}-fw.wav}"
# Nhạc: nang-dong-3 (124 bpm) - Liên 09/11 chê tin-cay-12 "chậm chạp, không hợp style kinh doanh";
# bản dài 240s tạo bằng make_music.py nang-dong 3 240; ghi lượt dùng ở Nhac-nen/index.json
MUSIC="${MUSIC:-$WORKDIR/Nhac-nen/nang-dong-3-dai.mp3}"
OUT="${OUT:-$HERE/../video/Ban-Hang-CRM-tong-the-${MA}.mp4}"
WORK="$HERE/work${HAU}"; rm -rf "$WORK"; mkdir -p "$WORK" "$(dirname "$OUT")"

[ -f "$KE_HOACH" ] || { echo "thiếu $KE_HOACH - chạy build_seq.py trước"; exit 1; }

echo "== Dựng từng mảnh =="
python3 - "$KE_HOACH" "$SEG" "$WORK" <<'PY'
import json, os, subprocess, sys
ke_hoach, seg_dir, work = sys.argv[1], sys.argv[2], sys.argv[3]
VF = "scale=1920:1080:flags=lanczos,fps=60,format=yuv420p"
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "60"]
danh_sach = []
for i, m in enumerate(json.load(open(ke_hoach, encoding="utf-8"))):
    dich = os.path.join(work, f"{i:02d}-{m['kieu']}-{m['ten']}.mp4")
    if m["kieu"] == "seg":
        nguon = os.path.join(seg_dir, m["ten"] + ".mp4")
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", nguon, "-an", *ENC, dich]
    elif m["kieu"] in ("anh", "quay"):
        # Nguon -> mot luong hinh [s]: anh dung yen (-framerate 60 BAT BUOC, xem ghi chu cu
        # Du-An) hoac ban quay cat LAY DUOI; co `crop` thi cat vung truoc khi phong;
        # co `giu` thi giu khung cuoi cho du loi (tpad clone).
        if m["kieu"] == "anh":
            vao = ["-loop", "1", "-framerate", "60", "-t", str(m["dai"]), "-i", m["tep"]]
        else:
            vao = ["-ss", str(m["bat_dau"]), "-t", str(round(m["dai"] - m.get("giu", 0), 3)),
                   "-i", m["tep"]]
        loc = []
        if m.get("crop"):
            x, y, w, h = m["crop"]
            loc.append(f"crop={w}:{h}:{x}:{y}")
        if m.get("khung"):
            o = m["khung"]["o"]
            loc.append(f"scale={o['w']}:{o['h']}:flags=lanczos,fps=60")
        else:
            loc.append("scale=1920:1080:flags=lanczos,fps=60")
        if m.get("giu"):
            loc.append(f"tpad=stop_mode=clone:stop_duration={m['giu']}")
        if m.get("khung"):
            # KHUNG: nen trang + thanh buoc sang dung buoc + nhan chung minh (engine ve, o man
            # de trong), ban quay dat vao dung o. Thanh buoc nam NGOAI man - khong de chu len du lieu.
            o = m["khung"]["o"]
            fc = (f"[1:v]{','.join(loc)},setpts=PTS-STARTPTS[s];"
                  f"[0:v][s]overlay={o['x']}:{o['y']}:eof_action=repeat,format=yuv420p[v]")
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "60",
                   "-t", str(m["dai"]), "-i", m["khung"]["anh"], *vao, "-filter_complex", fc,
                   "-map", "[v]", "-an", "-t", str(m["dai"]), *ENC, dich]
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", *vao, "-an",
                   "-vf", ",".join(loc) + ",format=yuv420p", "-t", str(m["dai"]), *ENC, dich]
    else:                                   # broll - đã 1920x1080 60fps, chỉ cắt đúng dài
        cmd = ["ffmpeg", "-v", "error", "-y", "-t", str(m["dai"]), "-i", m["tep"],
               "-an", "-vf", VF, *ENC, dich]
    subprocess.run(cmd, check=True)
    # CHOT CHAN: ffmpeg KHONG bao loi khi -ss roi ra ngoai tep - no de ra mot tep
    # mp4 rong 261 byte va tra ve 0. Ngay 02/11/2026 chin manh hong kieu nay, clip
    # ngan di 73 giay ma lenh dung van in "XONG". Do bang SO KHUNG, khong tin
    # format=duration (tep rong van khai duration = N/A).
    ra = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams",
                         "v:0", "-show_entries", "stream=nb_read_frames", "-of",
                         "csv=p=0", dich], capture_output=True, text=True).stdout.strip()
    # Lay SO DAU TIEN: tep tu may quay co the in them dong trong / dau phay (track timecode,
    # side data xoay hinh) - "156\n\n156" hay "168," tung lam phep do ra 0 (05/11/2026).
    import re as _re
    _so = _re.search(r"\d+", ra)
    khung = int(_so.group()) if _so else 0
    if abs(khung / 60.0 - m["dai"]) > 0.15:
        sys.exit(f"MANH {i:02d} {m['ten']} HONG: ra {khung/60.0:.2f}s, can {m['dai']:.2f}s\n"
                 f"  nguon: {m.get('tep')}\n"
                 f"  -> moc cat bat_dau={m.get('bat_dau')} co the roi ra ngoai ban quay.\n"
                 f"  -> chay lai: CLIP_LANG=$CLIP_LANG python3 build_seq.py")
    danh_sach.append(dich)
    print(f"  {i:2} {m['kieu']:6} {m['dai']:6.2f}s  {m['ten']}")
with open(os.path.join(work, "danh-sach.txt"), "w") as f:
    for d in danh_sach:
        f.write(f"file '{d}'\n")
PY

echo "== Nối =="
ffmpeg -y -loglevel error -f concat -safe 0 -i "$WORK/danh-sach.txt" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 60 "$WORK/hinh.mp4"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$WORK/hinh.mp4")
VDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE")
echo "  hình ${DUR}s / tiếng ${VDUR}s"

echo "== Trộn lời đọc + nhạc nền =="
FO=$(python3 -c "print(max(0, $DUR - 3))")
ffmpeg -y -loglevel error \
  -i "$WORK/hinh.mp4" -i "$VOICE" -stream_loop -1 -i "$MUSIC" \
  -filter_complex "\
[2:a]atrim=0:${DUR},asetpts=N/SR/TB,volume=0.13,afade=t=in:d=2,afade=t=out:st=${FO}:d=3[m];\
[1:a]volume=0.92,apad[v];\
[v][m]amix=inputs=2:duration=first:normalize=0,volume=${GAIN:-$GAIN_MAC_DINH}dB,\
aresample=96000,alimiter=limit=0.89:level=disabled,aresample=48000[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "$OUT"

echo "XONG: $OUT"
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of default=nw=1 "$OUT" | head -5

echo "== Soát tiếng =="
ffmpeg -i "$OUT" -af astats=metadata=1:reset=0 -f null /dev/null 2>&1 | grep -i "Peak level dB" | head -1
ffmpeg -i "$OUT" -af ebur128=framelog=quiet -f null /dev/null 2>&1 | grep -A1 "Integrated loudness" | head -2
