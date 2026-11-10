import json, base64, os, sys, subprocess
def tts(text, out, model=os.environ.get("TTS_MODEL","gemini-3.1-flash-tts-preview"), voice=None):
    gc = {"responseModalities": ["AUDIO"]}
    if voice: gc["speechConfig"] = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
    open(out + ".req.json", "w").write(json.dumps({"contents": [{"parts": [{"text": text}]}], "generationConfig": gc}, ensure_ascii=False))
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={os.environ['GEMINI_API_KEY']}"
    r = subprocess.run(["curl", "-s", "-m", "300", "-w", "\n%{http_code}", "-X", "POST", url, "-H", "Content-Type: application/json; charset=utf-8", "--data-binary", "@" + out + ".req.json"], capture_output=True, text=True)
    body, code = r.stdout.rsplit("\n", 1)
    if code != "200": print(out, "HTTP", code, json.loads(body).get("error",{}).get("message","")[300:700]); return None
    p = json.loads(body)["candidates"][0]["content"]["parts"][0]["inlineData"]
    raw = base64.b64decode(p["data"])
    path = out + (".wav" if "wav" in p["mimeType"] else ".pcm")
    open(path, "wb").write(raw); print(out, p["mimeType"], len(raw)); return path
if __name__ == "__main__":
    tts(sys.argv[1], sys.argv[2], voice=sys.argv[3] if len(sys.argv) > 3 else None)
