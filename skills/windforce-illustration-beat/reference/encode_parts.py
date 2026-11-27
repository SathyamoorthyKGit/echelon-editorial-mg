import subprocess, os

bounds = [0, 8.65, 14.75, 20.85, 26.95, 42.0, 47.2, 52.43, 84.78]
fps = 30
for i in range(len(bounds)-1):
    a, b = bounds[i], bounds[i+1]
    sa = round(a*fps); fc = round(b*fps) - sa
    lbl = f"part{i+1}_{a:.2f}s-{b:.2f}s".replace('.', '_')
    out = f"parts_full/{lbl}.mov"
    cmd = ["ffmpeg", "-y", "-framerate", "30", "-start_number", str(sa),
           "-i", "seq_final/f_%05d.png", "-frames:v", str(fc),
           "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
           "-alpha_bits", "8", "-qscale:v", "11", out]
    r = subprocess.run(cmd, capture_output=True)
    sz = os.path.getsize(out) if os.path.exists(out) else -1
    print(i+1, lbl, "frames", fc, "size MB", round(sz/1e6,1) if sz>0 else sz)
    if sz < 0:
        print(r.stderr.decode()[-2000:])
