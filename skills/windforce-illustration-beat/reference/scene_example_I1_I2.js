
const describeArc = (cx, cy, r, a0, a1) => {
  const pt = (a) => { const rad = (a - 90) * Math.PI / 180; return [cx + r * Math.cos(rad), cy + r * Math.sin(rad)]; };
  const [x0, y0] = pt(a0), [x1, y1] = pt(a1); const large = (a1 - a0) % 360 > 180 ? 1 : 0;
  return 'M' + x0.toFixed(2) + ' ' + y0.toFixed(2) + ' A' + r + ' ' + r + ' 0 ' + large + ' 1 ' + x1.toFixed(2) + ' ' + y1.toFixed(2);
};

// ---------- I1: power wheeling mechanism — generator sells A to B, pays only the wheeling cost (0:08.65) — studio blue, cream hairlines, amber accent ----------
XS.push({ t0: 8.65, t1: 26.95, kind: 'blue', init(c) {
  const AX = 260, BX = 820, NY = 760, R = 72, TX = AX + (BX - AX) * 0.56;
  c.AX = AX; c.BX = BX; c.NY = NY; c.R = R; c.tagX = TX; c.tagY = NY - 74;
  c.kick = c.sans('power wheeling', 540, 330, 48, XCREAM, 'transform:translateX(-50%)');
  c.num = c.ser('01', 540, 385, 120, XAMB, 'transform:translateX(-50%)');
  // faint shared-grid backdrop — this is a segment of a bigger network, not a private line
  c.gridGrp = sv('g', { opacity: 0 }, c.svg); c.gridGrpS = c.gridGrp.style;
  for (let x = AX - 160; x <= BX + 160; x += 46) { if (Math.abs(x - TX) < 30) continue;
    sv('path', { d: 'M' + x + ' ' + (NY - 16) + ' V' + (NY + 16), stroke: 'rgba(243,238,228,.22)', 'stroke-width': 2, 'stroke-linecap': 'round' }, c.gridGrp); }
  c.wire = c.path('M' + (AX + R) + ' ' + NY + ' H' + (BX - R), XCREAM, 4);
  c.ringA = c.path('M' + (AX + R) + ' ' + NY + ' A' + R + ' ' + R + ' 0 1 1 ' + (AX - R) + ' ' + NY + ' A' + R + ' ' + R + ' 0 1 1 ' + (AX + R) + ' ' + NY, XCREAM, 3.4);
  c.ringB = c.path('M' + (BX + R) + ' ' + NY + ' A' + R + ' ' + R + ' 0 1 1 ' + (BX - R) + ' ' + NY + ' A' + R + ' ' + R + ' 0 1 1 ' + (BX + R) + ' ' + NY, XCREAM, 3.4);
  c.la = c.ser('A', AX, NY - 38, 86, XCREAM, 'transform:translateX(-50%)');
  c.lb = c.ser('B', BX, NY - 38, 86, XCREAM, 'transform:translateX(-50%)');
  c.sa = c.sans('generator', AX, NY + 110, 34, XAMB, 'transform:translateX(-50%)');
  c.sb = c.sans('consumer', BX, NY + 110, 34, XAMB, 'transform:translateX(-50%)');
  // the power actually flowing A -> B through the grid
  c.pulseHalo = sv('circle', { r: 20, cx: 0, cy: NY, fill: XAMB }, c.svg); c.pulseHalo.style.filter = 'blur(9px)'; c.pulseHalo.style.opacity = '0';
  c.pulseCore = sv('circle', { r: 7, cx: 0, cy: NY, fill: '#FFF7E0' }, c.svg); c.pulseCore.style.opacity = '0';
  // a toll gate straddling the wire at the wheeling-cost point, not a floating label
  c.gatePostL = c.path('M' + (TX - 34) + ' ' + (NY - 22) + ' V' + (NY + 22), XCREAM, 3);
  c.gatePostR = c.path('M' + (TX + 34) + ' ' + (NY - 22) + ' V' + (NY + 22), XCREAM, 3);
  c.tagBox = sv('rect', { x: TX - 150, y: NY - 108, width: 300, height: 68, rx: 34, fill: XAMB, opacity: 0 }, c.svg); c.tagBoxS = c.tagBox.style;
  c.tagTx = c.sans('wheeling cost', TX, NY - 95, 30, XINK, 'transform:translateX(-50%);line-height:1.05'); c.tagTx.el.style.opacity = 0;
  c.big1 = c.ser('I pay only for', 540, 1280, 84, XCREAM, 'transform:translateX(-50%)');
  c.big2 = c.ser('the wheeling.', 540, 1366, 84, XCREAM, 'transform:translateX(-50%)');
  c.foot = c.sans('from generator to consumer, through the grid.', 540, 1560, 36, 'rgba(243,238,228,.75)', 'transform:translateX(-50%)');
}, render(t, c) {
  xType(c.kick, t, 8.75, 9.1); xFade(c.num, t, 8.85, 0.4);
  c.gridGrpS.opacity = gOUT((t - 11.0) / 0.8).toFixed(3);
  drawP(c.ringA, c.ringA.len, gOUT((t - 9.7) / 0.6)); xType(c.la, t, 10.0, 10.3); xType(c.sa, t, 10.3, 10.7);
  drawP(c.wire, c.wire.len, gIO((t - 11.0) / 2.2));
  drawP(c.ringB, c.ringB.len, gOUT((t - 13.0) / 0.6)); xType(c.lb, t, 13.3, 13.6); xType(c.sb, t, 13.6, 14.0);
  const postIn = gOUT((t - 12.0) / 0.5);
  const pStart = 11.3, pEnd = 19.9, pLoop = 2.6; let flash = 0;
  if (t >= pStart && t <= pEnd) {
    const lifeEnv = gOUT((t - pStart) / 0.3) * (1 - gOUT((t - (pEnd - 0.4)) / 0.4));
    const phase = ((t - pStart) % pLoop) / pLoop; const px = gL(c.AX + c.R, c.BX - c.R, phase);
    const loopFade = gC(Math.min(phase, 1 - phase) / 0.06); const a = lifeEnv * loopFade;
    c.pulseHalo.setAttribute('cx', px.toFixed(1)); c.pulseHalo.style.opacity = (a * 0.55).toFixed(3);
    c.pulseCore.setAttribute('cx', px.toFixed(1)); c.pulseCore.style.opacity = a.toFixed(3);
    flash = a * gC(1 - Math.abs(px - c.tagX) / 36);
  } else { c.pulseHalo.style.opacity = '0'; c.pulseCore.style.opacity = '0'; }
  drawP(c.gatePostL, c.gatePostL.len, postIn); c.gatePostL.style.stroke = flash > 0.15 ? XAMB : XCREAM;
  drawP(c.gatePostR, c.gatePostR.len, postIn); c.gatePostR.style.stroke = flash > 0.15 ? XAMB : XCREAM;
  const pop = iBACK((t - 20.6) / 0.5); const s = Math.max(0, pop);
  c.tagBoxS.opacity = t > 20.6 ? '1' : '0'; c.tagBoxS.transform = 'scale(' + s.toFixed(3) + ')'; c.tagBoxS.transformOrigin = c.tagX + 'px ' + c.tagY + 'px';
  c.tagTx.el.style.opacity = t > 20.7 ? Math.min(1, (t - 20.7) / 0.2).toFixed(3) : '0';
  xType(c.big1, t, 24.3, 24.9); xType(c.big2, t, 24.9, 25.5); xType(c.foot, t, 25.6, 26.3);
} });

// ---------- I2: open access is the final goal — the market opens, then the real competition comes (0:42.0) — paper, navy ink, blue ring ----------
XS.push({ t0: 42.0, t1: 52.43, kind: 'paper', init(c) {
  const CX = 540, CY = 700, RR = 140;
  c.num = c.ser('02', 980, 290, 72, 'rgba(11,30,63,.35)');
  c.ring = sv('path', { d: describeArc(CX, CY, RR, 26, 334), fill: 'none', stroke: '#2B55E8', 'stroke-width': 5, 'stroke-linecap': 'round' }, c.svg); c.ring.len = c.ring.getTotalLength();
  c.sat = []; const N = 5;
  for (let i = 0; i < N; i++) {
    const a = (-90 + i * (360 / N)) * Math.PI / 180, sx = CX + Math.cos(a) * 330, sy = CY + Math.sin(a) * 330;
    const ex = CX + Math.cos(a) * (RR + 14), ey = CY + Math.sin(a) * (RR + 14);
    const line = c.path('M' + sx + ' ' + sy + ' L' + ex + ' ' + ey, 'rgba(11,30,63,.55)', 2.4);
    const dot = sv('circle', { cx: sx, cy: sy, r: 0, fill: '#2B55E8' }, c.svg);
    c.sat.push({ line, dot, dotS: dot.style, a });
  }
  c.hub = sv('circle', { cx: CX, cy: CY, r: 0, fill: '#2B55E8' }, c.svg); c.hubS = c.hub.style;
  c.t1 = c.ser('OPEN', 540, 980, 118, XINK, 'transform:translateX(-50%)');
  c.t2 = c.ser('ACCESS.', 540, 1096, 118, XINK, 'transform:translateX(-50%)');
  c.lead = c.sans('market driven, like in India now —', 540, 1220, 38, 'rgba(11,30,63,.72)', 'transform:translateX(-50%)');
  c.btn1 = c.ser('then only the', 540, 1430, 70, XINK, 'transform:translateX(-50%)');
  c.btn2 = c.ser('real competition comes.', 540, 1498, 70, XINK, 'transform:translateX(-50%)');
}, render(t, c) {
  const lt = t - 42.0;
  xFade(c.num, t, 42.05, 0.3);
  drawP(c.ring, c.ring.len, gOUT(lt / 1.4));
  c.sat.forEach((s, i) => { const d = gOUT((lt - 0.3 - i * 0.12) / 0.5); drawP(s.line, s.line.len, d); s.dotS.r = (d * 17).toFixed(1); s.dotS.opacity = d.toFixed(3); });
  c.hubS.r = (gOUT((lt - 0.1) / 0.6) * 20).toFixed(1);
  xType(c.t1, t, 42.3, 42.75); xType(c.t2, t, 42.75, 43.35);
  xType(c.lead, t, 44.9, 45.9);
  xType(c.btn1, t, 49.6, 50.1); xType(c.btn2, t, 50.1, 50.9);
} });

window.XILL = {
  build(kit) { kit.css(XCSS); XS.forEach((g) => { g.c = xBase(kit, g.kind); g.init(g.c, kit); }); },
  render(t) {
    let vis = 0;
    for (const g of XS) {
      if (t < g.t0 || t > g.t1) { g.c.rs.display = 'none'; continue; }
      g.c.rs.display = 'block';
      const a = gSIN((t - g.t0) / 0.3) * (1 - gSIN((t - (g.t1 - 0.3)) / 0.3)); vis = Math.max(vis, a);
      g.c.rs.opacity = a.toFixed(3); g.c.rs.filter = a < 0.999 ? 'blur(' + ((1 - a) * 16).toFixed(1) + 'px)' : 'none';
      const u = gC((t - g.t0) / (g.t1 - g.t0)); g.c.ws.transform = 'scale(' + (1.0 + 0.045 * gSIN(u)).toFixed(4) + ')';
      g.c.gr.transform = 'translate(' + ((Math.floor(t * 24) * 37) % 64 - 32) + 'px,' + ((Math.floor(t * 24) * 53) % 64 - 32) + 'px)';
      g.render(t, g.c);
    }
    return vis;
  },
};
