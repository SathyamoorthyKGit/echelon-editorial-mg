import json, sys, csv, re, difflib
H=sys.argv[1]; END=84.7
exec(open(H+'/blocks2.py').read())
raw=[]
for r in csv.DictReader(open(H+'/tr.csv')):
    s=int(r['start'])/1000; e=int(r['end'])/1000; ws=r['text'].split()
    L=[len(w)+1.5 for w in ws]; tot=sum(L); acc=0
    for w,l in zip(ws,L): raw.append((w, s+(e-s)*acc/tot)); acc+=l
def norm(w): return re.sub(r"[^a-z0-9]","",w.lower())
EXP={}
Rn=[norm(w) for w,_ in raw]; Rt=[t for _,t in raw]
data=[]; pos=0
CARDS=[
  dict(t0=3.45,t1=8.65,col='blue',small="It's",big=["POWER","WHEELING."],tail="Under the new Electricity Act."),
  dict(t0=32.5,t1=42.0,col='amber',small="India had this years ago. We're",big=["already","late."],tail="But that has to happen."),
]
def align_range(words,a,b):
    idx=[k for k,t in enumerate(Rt) if a<=t<=b]
    toks=[norm(w) for w in words]; win=[Rn[k] for k in idx]
    sm=difflib.SequenceMatcher(None,toks,win,autojunk=False); tt=[None]*len(toks)
    for x,y,n in sm.get_matching_blocks():
        for q in range(n): tt[x+q]=Rt[idx[y+q]]
    kn=[q for q in range(len(tt)) if tt[q] is not None]
    for q in range(len(tt)):
        if tt[q] is None:
            lo=max([k for k in kn if k<q],default=None); hi=min([k for k in kn if k>q],default=None)
            tt[q]= tt[hi]-0.2*(hi-q) if lo is None else (tt[lo]+0.22*(q-lo) if hi is None else tt[lo]+(tt[hi]-tt[lo])*(q-lo)/(hi-lo))
    return [round(t,3) for t in tt]
for c in CARDS:
    sw=c['small'].split(); bw=[w for l in c['big'] for w in l.split()]; tw=c['tail'].split()
    tt=align_range(sw+bw+tw,c['t0']-0.6,c['t1']+0.3)
    c['sw']=list(zip(sw,tt[:len(sw)])); k=len(sw); c['bw']=[]
    for l in c['big']:
        n=len(l.split()); c['bw'].append(list(zip(l.split(),tt[k:k+n]))); k+=n
    c['tw']=list(zip(tw,tt[k:]))
    if c.get('tail_t') is not None: c['tw']=[(w,round(c['tail_t']+0.09*i,3)) for i,w in enumerate(tw)]
    _all=[t for _,t in c['sw']]+[t for l in c['bw'] for _,t in l]+[t for _,t in c['tw']]
    _f0,_l0=min(_all),max(_all); _tg=c['t1']-1.0
    if _l0>_tg:
        _m=lambda t: round(_f0+(t-_f0)*(_tg-_f0)/(_l0-_f0),3)
        c['sw']=[(w,_m(t)) for w,t in c['sw']]; c['bw']=[[(w,_m(t)) for w,t in l] for l in c['bw']]; c['tw']=[(w,_m(t)) for w,t in c['tw']]
    print('card',c['t0'],c['sw'][0],c['bw'],c['tw'][-1] if c['tw'] else '')
for i,(lead,hl) in enumerate(B):
    units=[('l',w) for w in lead.split()]+[('h%d'%k,w) for k,line in enumerate(hl) for w in line.split()]
    toks=[]; owner=[]
    for j,(k,w) in enumerate(units):
        for x in EXP.get(w.lower(),[w]): toks.append(norm(x)); owner.append(j)
    best=None
    for st in range(pos, len(Rn)):
        win=Rn[st:st+len(toks)+12]
        sm=difflib.SequenceMatcher(None,toks,win,autojunk=False); sc=sum(b.size for b in sm.get_matching_blocks())
        if best is None or sc>best[0]: best=(sc,st,sm)
        if st>pos+400: break
    sc,st,sm=best
    tt=[None]*len(toks)
    _big=max([n for a,b,n in sm.get_matching_blocks()]+[0])
    for a,b,n in sm.get_matching_blocks():
        if n<2 and _big>=3: continue
        for q in range(n): tt[a+q]=Rt[st+b+q]
    known=[q for q in range(len(tt)) if tt[q] is not None]
    if not known: print('NO MATCH block',i,toks); tt[0]=Rt[min(pos,len(Rt)-1)]; known=[0]
    for q in range(len(tt)):
        if tt[q] is None:
            lo=max([k for k in known if k<q],default=None); hi=min([k for k in known if k>q],default=None)
            tt[q]= tt[hi]-0.2*(hi-q) if lo is None else (tt[lo]+0.22*(q-lo) if hi is None else tt[lo]+(tt[hi]-tt[lo])*(q-lo)/(hi-lo))
    wt=[None]*len(units)
    for q,o in enumerate(owner):
        if wt[o] is None: wt[o]=tt[q]
    _mb=[(n,st+b+n) for a,b,n in sm.get_matching_blocks() if n]
    if _mb: pos=max(_mb)[1]
    lw=[(w,round(t,3)) for (k,w),t in zip(units,wt) if k=='l']
    rows=[[ (w,round(t,3)) for (k,w),t in zip(units,wt) if k=='h%d'%r] for r in range(len(hl))]
    print(i, sc,'/',len(toks), lw[0][1] if lw else '', rows[0][0])
    data.append(dict(lead=lw, rows=rows))
GWIN=[
  dict(t0=8.65,t1=26.95),   # I1 - wheeling mechanism diagram
  dict(t0=42.0,t1=52.43),   # I2 - open access / competition
  dict(t0=52.43,t1=55.53),  # P1 - youtube plug
  dict(t0=55.53,t1=63.17),  # P2 - october issue / magzter
  dict(t0=63.17,t1=71.67),  # P3 - people's bank spotlight
  dict(t0=71.67,t1=84.7),   # P4 - tourism collection carousel
]
WINS=CARDS+GWIN
def _f(d): return min([t for _,t in d['lead']]+[d['rows'][0][0][1]])
_v5=list(data)
for k,d in enumerate(_v5): d['pf']=k%2
def _h(d): return min(d['rows'][0][0][1], (max(t for _,t in d['lead'])+1.0) if d['lead'] else 1e9)
data=[d for d in data if not any(c['t0']-0.3<=_h(d)<=c['t1'] for c in WINS)]
for i,d in enumerate(data):
    first=min([t for _,t in d['lead']]+[d['rows'][0][0][1]])
    last=max(t for r in d['rows'] for _,t in r)
    d['start']=round(first-0.12,3)
    nxt=(min([t for _,t in data[i+1]['lead']]+[data[i+1]['rows'][0][0][1]])-0.12) if i+1<len(data) else END
    end=min(nxt-0.1, last+2.6, END)
    d['split']=0
    for a,b,y in SPLITS:
        if a-0.3<=first<b:
            d['split']=y; end=min(end,b-0.05)
        elif first<a<end: end=min(end,a-0.05)
    for c in WINS:
        if first<c['t0']<end: end=min(end,c['t0']+0.05)
    d['end']=round(end,3)
    _ls=json.load(open(H+'/leadsegs.json')); _c='L'
    for _a,_k in _ls:
        if first>=_a-0.001: _c=_k
    _st=d['start']; _en=d['end']; _dd=0
    for _i,(_a,_k) in enumerate(_ls):
        _b=_ls[_i+1][0] if _i+1<len(_ls) else 999
        if _k=='D': _dd+=max(0,min(_en,_b)-max(_st,_a))
    d['narrow']=0
    tgt=end-min(0.95,0.45*(end-first))
    if last>tgt:
        f=lambda t: round(first+(t-first)*(tgt-first)/(last-first),3)
        d['lead']=[(w,f(t)) for w,t in d['lead']]; d['rows']=[[(w,f(t)) for w,t in r] for r in d['rows']]
        last=tgt
    print(i,'%.2f-%.2f'%(d['start'],d['end']),'L%.2f'%last,'hold %.2f'%(d['end']-last),'split' if d['split'] else '', d['rows'])
open(H+'/data2.json','w').write(json.dumps(data))
open(H+'/film/cut.js','w').write(open(H+'/ill_full.js').read()+'\n'+open(H+'/cut_template2.js').read().replace('__DATA__',json.dumps(data)).replace('__BG__',open(H+'/bgsegs.json').read()).replace('__LEAD__',open(H+'/leadsegs.json').read()).replace('__CARDS__',json.dumps(CARDS)))
