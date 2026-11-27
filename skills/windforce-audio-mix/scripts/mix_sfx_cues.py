import numpy as np, wave, csv, json
SR=48000; DUR=86.5
W='/tmp/claude-0/-home-claude/41e733ff-2843-57b0-b4ae-04504edb01e7/scratchpad/sfx/wav/'
def load(n):
    w=wave.open(W+n+'.wav'); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float32)/32768
    return x/np.abs(x).max()
def anchor(x,kind):
    m=np.abs(x).max(1); hop=480; env=np.array([m[i:i+hop].max() for i in range(0,len(m),hop)])+1e-9; db=20*np.log10(env); pk=db.max()
    return np.argmax(db)*0.01 if kind=='peak' else np.argmax(db>pk-30)*0.01

G=[]
# caption boxes: block0 (0.15-3.5 "our open market") + block1 (27.03-32.55 "calculate the wheeling cost")
# windows to exclude from the generic caption-pop pass (cards / illustrations handle their own cues)
WIN=[(3.45,8.65),(8.65,26.95),(32.5,42.0),(42.0,52.43)]
for d in json.load(open('data2.json')):
    bs=d['rows'][0][0][1]-0.16
    if any(a-0.2<=bs<=b for a,b in WIN): continue
    G.append((bs+0.12,'Short_Whoosh_Metal','peak',-31,None,None,'caption box: '+' '.join(w for w,_ in d['rows'][0])))
    G.append((bs+0.02,'1_Click_Mouse','on',-33,None,None,'caption box tick'))

G+=[
 # T1 card — "It's / POWER WHEELING. / Under the new Electricity Act." (3.45-8.65)
 (3.48,'Deep_Whoosh_2','peak',-23,None,None,'card in: It\'s power wheeling'),
 (3.891,'1_Click_Mouse','on',-27,None,None,'"It\'s" lands'),
 (4.062,'Hit_2','on',-21,None,1.4,'"POWER" lands'),
 (4.355,'Hit_3','on',-22,None,1.3,'"WHEELING." lands'),
 (5.541,'Short_Whoosh_Metal','peak',-29,None,None,'tail draws: Under the new Electricity Act.'),
 (8.40,'Whoosh_Short_2','peak',-26,None,None,'card out'),
 # I1 illustration — A -> B wheeling-cost wire diagram (8.65-26.95)
 (8.68,'Simple_Whoosh_2','peak',-24,None,None,'illustration in: power wheeling 01'),
 (8.85,'Hit_1','on',-26,None,0.6,'"01" fades in'),
 (9.70,'Short_Whoosh_Metal','peak',-28,None,None,'node A ring draws'),
 (10.0,'1_Click_Mouse','on',-31,None,None,'"A" label types'),
 (11.0,'Short_Whoosh_Metal','peak',-27,None,None,'wire draws A to B'),
 (11.6,'1_Click_Mouse','on',-32,None,None,'wire tick 1'),
 (11.9,'1_Click_Mouse','on',-32,None,None,'wire tick 2'),
 (12.2,'1_Click_Mouse','on',-32,None,None,'wire tick 3'),
 (13.0,'Short_Whoosh_Metal','peak',-28,None,None,'node B ring draws'),
 (13.3,'1_Click_Mouse','on',-31,None,None,'"B" label types'),
 (20.6,'Deep_Hit_2','on',-22,None,1.0,'wheeling-cost tag pops'),
 (20.9,'Hit_1','on',-26,None,0.6,'tag text fades in'),
 (24.3,'Riser_2','peak',-27,None,None,'camera settles for closing line'),
 (24.9,'Hit_3','on',-22,None,1.3,'"the wheeling." lands'),
 (26.7,'Whoosh_Short_2','peak',-26,None,None,'illustration out'),
 # T2 card — "India had this years ago. We're / already late. / But that has to happen." (32.5-42.0)
 (32.53,'Deep_Whoosh_2','peak',-23,None,None,'card in: India had this years ago'),
 (35.211,'1_Click_Mouse','on',-28,None,None,'"India" lands'),
 (38.476,'Short_Whoosh_Metal','peak',-28,None,None,'turn into the punchline'),
 (38.962,'Hit_2','on',-21,None,1.4,'"already" lands'),
 (39.286,'Hit_3','on',-21,None,1.3,'"late." lands'),
 (40.162,'1_Click_Mouse','on',-27,None,None,'tail: But that has to happen.'),
 (41.80,'Whoosh_Short_2','peak',-26,None,None,'card out'),
 # I2 illustration — open-access hub / ring diagram (42.0-52.43)
 (42.0,'Simple_Whoosh_2','peak',-23,None,None,'illustration in: open access 02'),
 (42.05,'Hit_1','on',-26,None,0.6,'"02" fades in'),
 (42.1,'Riser_3','peak',-27,None,None,'ring and hub draw'),
 (42.3,'Mouse_Clicks','on',-30,1.05,0.5,'satellite nodes pop out'),
 (42.3,'1_Click_Mouse','on',-32,None,None,'"OPEN" types'),
 (42.75,'Hit_2','on',-21,None,1.4,'"ACCESS." lands'),
 (44.9,'Short_Whoosh_Metal','peak',-29,None,None,'lead line types: market driven, like India now'),
 (49.6,'Deep_Whoosh_3','peak',-25,None,None,'push into the closing line'),
 (50.1,'Deep_Hit_3','on',-20,None,1.4,'"real competition comes." lands'),
 (52.0,'Whoosh_Short_2','peak',-25,None,None,'illustration out'),
]
F=[]  # footage-cut cues: F1/F2 cutaway footage hasn't been supplied yet for H02

def render(C):
    mix=np.zeros((int(SR*DUR),2),np.float32); rows=[]
    for t,f,k,g,ss,ln,lab in C:
        x=load(f)
        if ss is not None: x=x[int(ss*SR):]
        if ln is not None:
            x=x[:int(ln*SR)].copy(); fl=min(int(0.2*SR),len(x)); x[-fl:]*=np.linspace(1,0,fl)[:,None]
        a=anchor(x,k); st=int(round((t-a)*SR))
        if st<0: x=x[-st:]; st=0
        end=min(len(mix),st+len(x)); mix[st:end]+=x[:end-st]*10**(g/20)
        rows.append((f'{max(0,t-a):.2f}',f'{t:.2f}',f,lab,g))
    return mix,rows
mg,rg=render(G)
mf=np.zeros((int(SR*DUR),2),np.float32); rf=[]
if F: mf,rf=render(F)
pk=max(np.abs(mg).max(),np.abs(mg+mf).max(),1e-6); sc=10**(-6/20)/pk
def wr(p,x):
    o=wave.open(p,'wb'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes()); o.close()
wr('audio/sfx_graphics.wav',mg*sc); wr('audio/sfx_footage.wav',mf*sc)
with open('audio/WF_H02_SFX_cue_sheet.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['stem','clip_start_s','sync_point_s','sfx_file','moment','rel_gain_db'])
    for r in sorted([('graphics',)+r for r in rg]+[('footage cuts',)+r for r in rf],key=lambda r: float(r[2])): w.writerow(r)
print(len(rg),len(rf),'cues')
