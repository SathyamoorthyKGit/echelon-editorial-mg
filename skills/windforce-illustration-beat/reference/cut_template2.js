const D = __DATA__;
const C01 = (x) => x < 0 ? 0 : x > 1 ? 1 : x;
const SINE = (x) => 0.5 - 0.5 * Math.cos(Math.PI * C01(x));
const QUART = (x) => 1 - Math.pow(1 - C01(x), 4);
const EXPO = (x) => { x = C01(x); return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); };
const BLUE = '#2F7FEA', RED = '#F2B01C';  // amber bg -> studio-blue box; blue bg -> amber box
const BG = __BG__;
const LEADSEG = __LEAD__;
const leadCol = (t) => { let c = 'L'; for (const [a, k] of LEADSEG) { if (t >= a - 0.001) c = k; else break; } return c === 'D' ? '#1C1C1E' : '#FFFFFF'; };
const boxCol = (t) => { let c = 'R'; for (const [a, k] of BG) { if (t >= a - 0.001) c = k; else break; } return c === 'R' ? BLUE : RED; };
const HF = 96;             // highlight font size
const CSS = '#stage { font-synthesis:none; color:#fff }' +
  '.cap { position:absolute; left:118px; width:880px; display:flex; flex-direction:column; align-items:flex-start }' +
  '.lead { font-family:"InterDisplay-Medium", system-ui, sans-serif; font-size:42px; line-height:1.12; letter-spacing:-0.01em; max-width:880px; margin:0 0 4px 2px }' +
  '.row { position:relative; font-family:"InterDisplay-Bold", system-ui, sans-serif; font-size:' + HF + 'px; line-height:1; letter-spacing:-0.035em; white-space:nowrap; margin-top:-2px }' +
  '.row .bx { position:absolute; left:-22px; top:0.31em; height:0.93em; width:0; background:' + BLUE + ' }' +
  '.row .w { position:relative; display:inline-block; padding:0.32em 0.1em 0.32em 0.04em; margin:-0.32em -0.1em -0.32em -0.04em }' +
  '.row.pf { font-family:"PlayfairDisplay-BlackItalic", Georgia, serif; letter-spacing:-0.005em }' +
  '.row.pf .bx { top:0.36em; height:0.86em }' +
  '.lead .w { display:inline-block }';
const CARDS = __CARDS__;
const CARD_BG = {
  blue: 'radial-gradient(ellipse 78% 46% at 50% 48%, #4A97F7 0%, #2F7FEA 38%, #1A5CC4 68%, #0C3577 100%)',
  amber: 'radial-gradient(ellipse 78% 46% at 50% 48%, #FAC93A 0%, #F2B01C 38%, #D9900C 68%, #8E5604 100%)',
  red: 'radial-gradient(ellipse 78% 46% at 50% 48%, #F0303A 0%, #CF1D29 38%, #96111C 68%, #4A070D 100%)' };
const CSS2 = '.card { position:absolute; inset:0; overflow:hidden }' +
  '.card .bg { position:absolute; inset:-6%; }' +
  '.card .blkq { position:absolute; left:92px; width:880px; top:0; transform-origin:30% 50% }' +
  '.card .sm { font-family:"InterDisplay-Medium", system-ui, sans-serif; font-size:44px; line-height:1.18; color:#fff; margin:0 0 8px 104px; max-width:840px; letter-spacing:-0.01em; text-wrap:balance }' +
  '.card .bg2 { font-family:"InterDisplay-Bold", system-ui, sans-serif; color:#fff; line-height:0.98; letter-spacing:-0.035em; white-space:nowrap; position:relative }' +
  '.card .tl { font-family:"InterDisplay-Medium", system-ui, sans-serif; font-size:46px; color:rgba(225,236,255,.92); margin-top:16px; letter-spacing:-0.01em; white-space:nowrap }' +
  '.card .q { position:absolute; font-family:"InterDisplay-Bold", system-ui, sans-serif; font-size:120px; line-height:1; color:#fff }' +
  '.card .w { display:inline-block }' +
  '.card.ink .sm, .card.ink .bg2, .card.ink .q { color:#0B1E3F } .card.ink .tl { color:rgba(11,30,63,.8) }';
window.CUT = {
  width: 1080, height: 1920, fps: 30, duration: 84.78, background: 'transparent',
  init(kit) {
    kit.css(CSS);
    kit.css(CSS2);
    if (window.XILL) window.XILL.build(kit);
    if (window.GFX) window.GFX.build(kit);
    if (window.ILL) window.ILL.build(kit);
    this.cards = CARDS.map((c) => {
      const el = kit.h('<div class="card' + (c.col === 'amber' ? ' ink' : '') + '"></div>');
      const bg = document.createElement('div'); bg.className = 'bg'; bg.style.background = CARD_BG[c.col]; el.append(bg);
      const blk = document.createElement('div'); blk.className = 'blkq'; el.append(blk);
      const words = [];
      const addWords = (p, list, big) => list.forEach(([w, t], j) => { const s = document.createElement('span'); s.className = 'w'; s.textContent = w; p.append(s); if (j < list.length - 1) p.append(' '); words.push({ st: s.style, t, big }); });
      const sm = document.createElement('p'); sm.className = 'sm'; blk.append(sm); addWords(sm, c.sw, 0);
      const bigs = c.bw.map((l) => { const d = document.createElement('div'); d.className = 'bg2'; d.style.fontSize = '205px'; blk.append(d); addWords(d, l, 1); return d; });
      const tl = document.createElement('p'); tl.className = 'tl'; blk.append(tl); addWords(tl, c.tw, 0);
      kit.stage.append(el);
      const lw = (d) => { const e = d.lastElementChild; return e.offsetLeft + e.offsetWidth; };
      let mw = 0; for (const d of bigs) mw = Math.max(mw, lw(d));
      const fs = Math.min(205, 205 * 820 / mw); for (const d of bigs) d.style.fontSize = fs.toFixed(1) + 'px';
      let mw2 = 0; for (const d of bigs) mw2 = Math.max(mw2, lw(d));
      tl.style.marginLeft = Math.max(104, Math.min(mw2 * 0.42, 960 - tl.scrollWidth - 20)).toFixed(0) + 'px';
      const q1 = document.createElement('div'); q1.className = 'q'; q1.textContent = '\u201C'; q1.style.left = '0px'; q1.style.top = '-14px'; blk.append(q1);
      const last = bigs[bigs.length - 1];
      const q2 = document.createElement('div'); q2.className = 'q'; q2.textContent = '\u201D';
      q2.style.left = (lw(last) + 12).toFixed(0) + 'px'; q2.style.top = (last.offsetTop - 22).toFixed(0) + 'px'; blk.append(q2);
      const bl = c.bw[c.bw.length - 1]; const tq2 = bl[bl.length - 1][1] + 0.25;
      words.push({ st: q1.style, t: Math.min(c.sw[0][1], c.t0 + 0.25) - 0.12, big: 2 }); words.push({ st: q2.style, t: tq2, big: 2 });
      blk.style.top = ((1920 - blk.offsetHeight) / 2 - 40).toFixed(0) + 'px';
      return { el: el.style, bg: bg.style, blk: blk.style, words, c };
    });
    this.caps = D.map((d) => {
      const el = kit.h('<div class="cap"></div>');
      const lead = document.createElement('p'); lead.className = 'lead'; el.append(lead);
      const lw = d.lead.map(([w, t], j) => { const s = document.createElement('span'); s.className = 'w'; s.textContent = w; lead.append(s); if (j < d.lead.length - 1) lead.append(' '); return { st: s.style, t }; });
      if (!d.lead.length) lead.remove();
      if (d.narrow) { lead.style.maxWidth = '400px'; lead.style.textWrap = 'balance'; }
      kit.stage.append(el);
      const rows = d.rows.map((r) => {
        const row = document.createElement('div'); row.className = 'row' + (d.pf ? ' pf' : ''); el.append(row);
        const bx = document.createElement('div'); bx.className = 'bx'; row.append(bx);
        const ws = r.map(([w, t], j) => { const s = document.createElement('span'); s.className = 'w'; s.textContent = w; row.append(s); if (j < r.length - 1) row.append(' '); return { s, st: s.style, t }; });
        return { row, bx: bx.style, ws };
      });
      // fit width
      let maxw = 0; for (const r of rows) maxw = Math.max(maxw, r.row.scrollWidth);
      const base = d.pf ? HF * 1.1 : HF; for (const r of rows) r.row.style.fontSize = base + 'px'; maxw = 0; for (const r of rows) maxw = Math.max(maxw, r.row.scrollWidth);
      const fs = maxw > 770 ? base * 770 / maxw : base; for (const r of rows) r.row.style.fontSize = fs.toFixed(1) + 'px';
      for (const r of rows) for (const w of r.ws) w.right = w.s.offsetLeft + w.s.offsetWidth;
      const pad = fs * 0.2;
      for (const r of rows) for (const w of r.ws) w.target = w.right + 22 + pad * 0.6;
      // vertical placement
      const h = el.offsetHeight;
      el.style.top = (d.split ? d.split - 34 - h : Math.max(1392, 1632 - h)) + 'px';
      return { el: el.style, lw, rows, d, ls: lead.style };
    });
  },
  render(t) {
    const gv2 = window.GFX ? window.GFX.render(t) : 0;
    const iv = window.XILL ? window.XILL.render(t) : 0;
    let cardOn = 0;
    for (const k of this.cards) {
      const c = k.c;
      if (t < c.t0 || t > c.t1) { k.el.display = 'none'; continue; }
      k.el.display = 'block';
      const fi = SINE((t - c.t0) / 0.32), fo = SINE((t - (c.t1 - 0.32)) / 0.32), v = fi * (1 - fo);
      cardOn = Math.max(cardOn, v);
      k.el.opacity = v.toFixed(3);
      k.el.filter = v < 0.999 ? 'blur(' + ((1 - v) * 14).toFixed(2) + 'px)' : 'none';
      const u = C01((t - c.t0) / (c.t1 - c.t0));
      k.bg.transform = 'scale(' + (1.0 + 0.05 * u).toFixed(4) + ') translateY(' + (-12 * u).toFixed(1) + 'px)';
      k.blk.transform = 'scale(' + (1.0 + 0.035 * SINE(u)).toFixed(4) + ')';
      for (const w of k.words) {
        const s = t - w.t + 0.05;
        const d = w.big === 1 ? 0.3 : 0.24, p = QUART(s / d), po = SINE(s / (d * 0.8));
        w.st.opacity = po.toFixed(3);
        w.st.filter = p < 0.999 ? 'blur(' + ((1 - p) * (w.big === 1 ? 12 : 7)).toFixed(2) + 'px)' : 'none';
        w.st.transform = 'scale(' + (w.big === 1 ? 1.06 - 0.06 * p : 1).toFixed(4) + ')';
      }
    }
    for (const k of this.caps) {
      const d = k.d;
      if (t < d.start || t > d.end + 0.02) { k.el.display = 'none'; continue; }
      k.el.display = 'flex';
      const ex = SINE((t - (d.end - 0.28)) / 0.28);
      k.el.opacity = ((1 - ex) * (1 - iv) * (1 - gv2)).toFixed(3);
      k.el.filter = ex > 0.001 ? 'blur(' + (ex * 8).toFixed(2) + 'px)' : 'none';
      k.el.transform = 'translateY(' + (-ex * 10).toFixed(2) + 'px)';
      for (const w of k.lw) {
        const s = t - w.t + 0.06, p = QUART(s / 0.22);
        w.st.opacity = SINE(s / 0.16).toFixed(3);
        w.st.transform = 'translateY(' + ((1 - p) * 10).toFixed(2) + 'px)';
      }
      const col = boxCol(t); const tcol = col === RED ? '#0B1E3F' : '#FFFFFF';
      k.ls.color = leadCol(t);
      for (const r of k.rows) {
        r.bx.background = col; r.row.style.color = tcol;
        // box grows in steps toward each spoken word's right edge
        let wdt = 0, prev = 0;
        for (const w of r.ws) {
          const s = t - (w.t - 0.16);
          if (s <= 0) break;
          wdt = prev + (w.target - prev) * EXPO(s / 0.42); prev = w.target;
        }
        const s0 = t - (r.ws[0].t - 0.16);
        r.bx.width = (s0 > 0 ? Math.max(wdt, 9 * C01(s0 / 0.03)) : 0).toFixed(1) + 'px';
        r.bx.opacity = s0 > 0 ? '1' : '0';
        for (const w of r.ws) {
          // soft left-to-right wipe of the white word, slightly behind the box
          const s = t - (w.t - 0.04), p = QUART(s / 0.34) * 1.45 - 0.3;
          const a = (p * 100).toFixed(1), b = ((p + 0.3) * 100).toFixed(1);
          const m = s <= 0 ? 'linear-gradient(90deg, transparent 0%, transparent 100%)' : (s >= 0.36 ? 'none' : 'linear-gradient(90deg, #000 ' + a + '%, transparent ' + b + '%)');
          w.st.webkitMaskImage = m; w.st.maskImage = m;
        }
      }
    }
  },
};
