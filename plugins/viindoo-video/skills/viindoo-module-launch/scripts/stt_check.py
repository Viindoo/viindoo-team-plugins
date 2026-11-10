"""Nghe lại từng seg*.flac bằng Gemini 2.5 Flash (văn bản), in chữ nghe được để so với VO."""
import base64, json, os, subprocess, sys, importlib.util, time, urllib.request
clipdir = sys.argv[1]; segs = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None
s = importlib.util.spec_from_file_location("c", os.path.join(clipdir, "clip.py")); C = importlib.util.module_from_spec(s); s.loader.exec_module(C)
key = os.environ["GEMINI_API_KEY"]
for i in segs if segs is not None else range(len(C.VO)):
    mp3 = f"/tmp/_seg{i}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(clipdir, "vo", f"seg{i}.flac"), "-b:a", "64k", mp3], check=True)
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(open(mp3, "rb").read()).decode()}},
                                    {"text": "Transcribe this audio verbatim, in its original language. Output only the transcript."}]}]}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    txt = r["candidates"][0]["content"]["parts"][0]["text"].strip().replace("\n", " ")
    print(f"seg{i} NGHE: {txt}\n      VO  : {C.VO[i]}\n", flush=True)
    time.sleep(1)
