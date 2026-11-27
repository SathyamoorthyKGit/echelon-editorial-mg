import glob, json
from PIL import Image

BLUE = (47, 127, 234)
AMBER = (242, 176, 28)

def dist2(a, b):
    return sum((a[i]-b[i])**2 for i in range(3))

files = sorted(glob.glob('/tmp/claude-0/-home-claude/41e733ff-2843-57b0-b4ae-04504edb01e7/scratchpad/wf2/bgsample/f_*.png'))
fps = 6.0
labels = []
for i, fp in enumerate(files):
    im = Image.open(fp).convert('RGB')
    w, h = im.size
    pts = [im.getpixel((int(w*0.5), int(h*0.02))), im.getpixel((int(w*0.12), int(h*0.02))), im.getpixel((int(w*0.88), int(h*0.02)))]
    avg = tuple(sum(p[c] for p in pts)/3 for c in range(3))
    db = dist2(avg, BLUE); da = dist2(avg, AMBER)
    lab = 'B' if db < da else 'R'
    t = i / fps
    labels.append((t, lab, avg, db, da))

# collapse to segments, dropping flickers shorter than min_dur by majority-smoothing
MIN = 2  # frames minimum (0.33s) run to accept a flip
smoothed = [l[1] for l in labels]
changed = True
while changed:
    changed = False
    i = 0
    n = len(smoothed)
    while i < n:
        j = i
        while j < n and smoothed[j] == smoothed[i]:
            j += 1
        run = j - i
        if run < MIN and 0 < i and j < n and smoothed[i-1] == smoothed[j if j < n else j-1]:
            for k in range(i, j):
                smoothed[k] = smoothed[i-1]
            changed = True
        i = j

segs = []
prev = None
for (t, _, *_rest), lab in zip(labels, smoothed):
    if lab != prev:
        segs.append([round(t, 4), lab])
        prev = lab

print(len(segs), 'segments')
for s in segs:
    print(s)

json.dump(segs, open('/tmp/claude-0/-home-claude/41e733ff-2843-57b0-b4ae-04504edb01e7/scratchpad/wf2/bgsegs.json', 'w'))
