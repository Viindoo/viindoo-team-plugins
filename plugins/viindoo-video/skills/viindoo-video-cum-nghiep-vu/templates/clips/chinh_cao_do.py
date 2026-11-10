"""Keo cao do CA BAI ve muc chuan - BUOC CUOI, chi dung khi da doi giong ma van duoi san.
Ba rang buoc (SSOT): keo ca bai mot lan mot he so; GIU NGUYEN thoi luong; chep lai loi soat
sau khi keo vi doi cao do co the lam meo chu.
Chay: python3 -I chinh_cao_do.py voice/du-an-vi-achird.wav 137.1
"""
import subprocess, sys, os
src=sys.argv[1]; dich_f0=float(sys.argv[2]) if len(sys.argv)>2 else 137.1
HERE=os.path.dirname(os.path.abspath(__file__))
def do(p):
    r=subprocess.run([sys.executable,os.path.join(HERE,"voice_stats.py"),p],
                     capture_output=True,text=True).stdout
    for ln in r.strip().split("\n"):
        if os.path.basename(p) in ln:
            c=ln.split()
            return float(c[-3].replace("Hz","")), float(c[-2].replace("Hz",""))
    return None,None
f0,dai=do(src)
if not f0: sys.exit("khong do duoc cao do")
he=dich_f0/f0
print(f"  {os.path.basename(src)}: F0 {f0:.1f}Hz dai {dai:.1f}Hz -> he so {he:.4f}")
if he<1.001: print("  da dat chuan, khong can keo"); sys.exit(0)
if he>1.20: sys.exit(f"  he so {he:.2f} qua lon - doi giong khac thay vi keo")
out=src.replace(".wav","-dachinh.wav")
sr=48000
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src,
   "-af",f"asetrate=24000*{he},aresample={sr},atempo={1/he:.6f}",out],check=True)
f2,d2=do(out)
dur=lambda p: float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
     "-of","csv=p=0",p],capture_output=True,text=True).stdout.strip())
print(f"  -> {os.path.basename(out)}: F0 {f2:.1f}Hz dai {d2:.1f}Hz  "
      f"({dur(src):.1f}s -> {dur(out):.1f}s)")
