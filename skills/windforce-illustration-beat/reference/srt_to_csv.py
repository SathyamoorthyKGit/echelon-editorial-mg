import re, csv

def tms(s):
    h, m, rest = s.split(':')
    sec, ms = rest.split(',')
    return (int(h)*3600 + int(m)*60 + int(sec))*1000 + int(ms)

text = open('/root/.claude/uploads/41e733ff-2843-57b0-b4ae-04504edb01e7/89d7edbc-WindForce_HL_02.srt', encoding='utf-8-sig').read()
blocks = re.split(r'\n\s*\n', text.strip())
rows = []
for b in blocks:
    lines = [l for l in b.splitlines() if l.strip()]
    if len(lines) < 2:
        continue
    # lines[0] = index, lines[1] = timecodes, rest = text
    tc = lines[1]
    m = re.match(r'(\d\d:\d\d:\d\d,\d+)\s*-->\s*(\d\d:\d\d:\d\d,\d+)', tc)
    if not m:
        continue
    start = tms(m.group(1)); end = tms(m.group(2))
    txt = ' '.join(lines[2:]).strip()
    rows.append((start, end, ' ' + txt))

with open('/tmp/claude-0/-home-claude/41e733ff-2843-57b0-b4ae-04504edb01e7/scratchpad/wf2/tr.csv', 'w', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(['start', 'end', 'text'])
    for s, e, t in rows:
        w.writerow([s, e, t])

print(len(rows), 'rows written')
for r in rows[:5]:
    print(r)
print('...')
for r in rows[-5:]:
    print(r)
