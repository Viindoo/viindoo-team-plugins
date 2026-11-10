"""Soát lời đọc: cho Gemini CHÉP LẠI file tiếng rồi đối chiếu với bản viết.

Vì sao có file này: máy không nghe được, nên không được phép nói "giọng đọc ổn". Cách kiểm duy
nhất đáng tin là chép lại âm thanh THẬT ra chữ rồi so với bản viết - lệch ở đâu là đọc sai ở đó
(Liên 19/10: "dòng dự liệu", "nguồn gức"... nhiều chỗ đọc sai).

Chạy:  python check_tts.py                 -> chép + đối chiếu voice/ban-hang-crm-vi-fw.wav
       python check_tts.py <file.wav>      -> chép file khác
Kết quả: in bảng lệch + ghi voice/<ten>.transcript.txt
"""
import base64, difflib, json, os, re, ssl, subprocess, sys, tempfile, urllib.request

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CTX = ssl.create_default_context()

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.environ.get("CLIP_LANG", "vi")
MODEL = "gemini-2.5-flash"
PROMPT = ("Chép lại CHÍNH XÁC từng chữ những gì người đọc PHÁT ÂM trong file tiếng này, "
          "tiếng Việt có dấu. Ghi đúng cái TAI NGHE ĐƯỢC, kể cả khi từ đó sai chính tả hay vô "
          "nghĩa - ví dụ nghe thành 'dự liệu' thì ghi 'dự liệu', KHÔNG được tự sửa thành "
          "'dữ liệu'. Mỗi đoạn ngắt hơi xuống một dòng. Chỉ trả lời bằng phần lời chép, "
          "không thêm lời bình.")
if LANG == "en":
    PROMPT = ("Transcribe EXACTLY, word for word, what the speaker PRONOUNCES in this English audio. "
              "Write what the EAR hears, even when it is a wrong or meaningless word - do NOT correct "
              "it. Write numbers as words, the way they are spoken. One line per breath group. Reply "
              "with the transcript only, no comments.")


def to_mp3(wav):
    out = os.path.join(tempfile.gettempdir(), "tts-check.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-ac", "1", "-ar", "24000",
                    "-b:a", "64k", out], check=True)
    return out


def transcribe(path):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("thiếu GEMINI_API_KEY")
    mp3 = to_mp3(path)
    data = base64.b64encode(open(mp3, "rb").read()).decode()
    body = {"contents": [{"parts": [
        {"text": PROMPT},
        {"inlineData": {"mimeType": "audio/mpeg", "data": data}}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 4096,
                             "thinkingConfig": {"thinkingBudget": 0}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=600, context=SSL_CTX) as r:
        res = json.load(r)
    try:
        return "".join(p.get("text", "")
                       for p in res["candidates"][0]["content"]["parts"]).strip()
    except Exception:
        sys.exit("không lấy được lời chép: " + json.dumps(res)[:400])


# Nghe có chủ đích: bản chép tự do hay TỰ SỬA chính tả nên không bắt được lỗi sai DẤU.
# Hỏi thẳng từng từ rủi ro thì mô hình buộc phải nghe kỹ chỗ đó.
# Từ rủi ro của bài Trao đổi thông tin (đo 05/11: "làm"->"lào", "ngay"->"ngày", "thông"->"thu", "Cần"->"Kênh")
RISKY = ["ngay hôm nay", "phải làm", "khơi thông", "Viindoo AI", "kênh", "ghi chép", "giơ tay", "Đúng", "Xong", "Nhớ", "đối tác", "soát lỗi"]
WORD_PROMPT = ("Nghe kỹ file tiếng tiếng Việt này. Với MỖI từ/cụm dưới đây, cho biết người đọc "
               "phát âm ĐÚNG hay SAI dấu thanh, và nếu sai thì nghe thành gì. Trả lời mỗi dòng "
               "một mục theo mẫu: <từ> | ĐÚNG hoặc SAI | nghe thành <...> | xuất hiện <n> lần. "
               "Tuyệt đối không tự sửa cho hay - ghi đúng cái tai nghe được.\n\nDanh sách: ")
if LANG == "en":
    # Tu rui ro ban tieng Anh: ten rieng Viet, ten san pham, so tien, nhan ba tru
    RISKY = ["Viindoo", "Zalo", "Bien Hoa", "Hai Duong", "storekeeper", "eighty-four million dong",
             "twenty-one", "Right", "Done", "Remember", "Getting Things Done", "unblocks"]
    WORD_PROMPT = ("Listen carefully to this English audio. For EACH word or phrase below, say whether "
                   "the speaker pronounces it CLEARLY and CORRECTLY, or not, and if not what it sounds "
                   "like. One line per item: <word> | OK or WRONG | sounds like <...> | occurs <n> times. "
                   "Do not tidy it up - write what the ear hears.\n\nList: ")


def check_words(path):
    key = os.environ.get("GEMINI_API_KEY")
    mp3 = to_mp3(path)
    data = base64.b64encode(open(mp3, "rb").read()).decode()
    body = {"contents": [{"parts": [
        {"text": WORD_PROMPT + ", ".join(RISKY)},
        {"inlineData": {"mimeType": "audio/mpeg", "data": data}}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 4096,
                             "thinkingConfig": {"thinkingBudget": 0}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=600, context=SSL_CTX) as r:
        res = json.load(r)
    return "".join(p.get("text", "")
                   for p in res["candidates"][0]["content"]["parts"]).strip()


# ---- MỐC THỜI GIAN TỪNG ĐOẠN -------------------------------------------------------
# Nắn mốc theo khoảng lặng KHÔNG đáng tin: giọng TTS nghỉ giữa câu cũng lâu bằng nghỉ giữa
# đoạn, thử mọi ngưỡng đều lệch 7-34 giây (đo 19/10). Hỏi thẳng mô hình nghe file rồi báo
# giây bắt đầu từng đoạn thì chắc hơn nhiều - sau đó chỉ cần nắn nhẹ vào khe lặng gần nhất.
MOC_PROMPT = ("Đây là file đọc một bài gồm {n} đoạn, đọc liền mạch theo đúng thứ tự dưới đây. "
              "Nghe và cho biết GIÂY BẮT ĐẦU của từng đoạn (tính từ đầu file).\n"
              "Trả lời đúng {n} dòng, mỗi dòng: <số thứ tự đoạn>|<giây, số thập phân>\n"
              "Không thêm chữ nào khác.\n\n")


def moc_doan(path, doan):
    key = os.environ.get("GEMINI_API_KEY")
    mp3 = to_mp3(path)
    data = base64.b64encode(open(mp3, "rb").read()).decode()
    txt = MOC_PROMPT.format(n=len(doan)) + "\n".join(
        f"{i}. {d[:70]}" for i, d in enumerate(doan))
    body = {"contents": [{"parts": [{"text": txt},
            {"inlineData": {"mimeType": "audio/mpeg", "data": data}}]}],
            "generationConfig": {"temperature": 0, "maxOutputTokens": 2048,
                                 "thinkingConfig": {"thinkingBudget": 0}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=600, context=SSL_CTX) as r:
        res = json.load(r)
    raw = "".join(p.get("text", "")
                  for p in res["candidates"][0]["content"]["parts"])
    moc = {}
    for ln in raw.splitlines():
        m = re.match(r"\s*(\d+)\s*\|\s*([\d.]+)", ln)
        if m:
            moc[int(m.group(1))] = float(m.group(2))
    return [moc.get(i) for i in range(len(doan))]


def words(t):
    t = t.lower().replace("’", "'")
    return re.findall(r"[0-9a-zà-ỹđ']+", t)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    wav = args[0] if args else os.path.join(HERE, "voice", f"ban-hang-crm-{LANG}-fw.wav")
    if "--words" in sys.argv:
        print("=== NGHE CÓ CHỦ ĐÍCH TỪNG TỪ RỦI RO ===")
        print(check_words(wav)); return
    import importlib.util
    spec = importlib.util.spec_from_file_location("tts", os.path.join(HERE, f"tts_{LANG}_fw.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    want = m.spoken_text()

    print(f"đang chép lại {os.path.basename(wav)} ...")
    got = transcribe(wav)
    out = os.path.splitext(wav)[0] + ".transcript.txt"
    open(out, "w", encoding="utf-8").write(got)
    print("đã ghi", out, f"({len(got)} ký tự)\n")

    a, b = words(want), words(got)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    n = 0
    print("=== CHỖ LỆCH (bản viết -> tai nghe được) ===")
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        ctx = " ".join(a[max(0, i1 - 4):i1])
        viet = " ".join(a[i1:i2]) or "(không có)"
        nghe = " ".join(b[j1:j2]) or "(mất)"
        print(f"  ...{ctx}|  VIẾT: {viet!r}   NGHE: {nghe!r}")
        n += 1
    r = sm.ratio()
    print(f"\n{n} chỗ lệch · khớp {r*100:.1f}% ({len(a)} âm tiết viết / {len(b)} nghe được)")


if __name__ == "__main__":
    main()
