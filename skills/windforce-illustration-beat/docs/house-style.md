# WindForce / Echelon house illustration style — cheat sheet

## Palette

| Token | Hex | Use |
|---|---|---|
| `XBLUE` | `#2F7FEA` | Studio-blue scene background (`kind:'blue'`) |
| `XPAPER` | `#F6F4F2` | Paper scene background (`kind:'paper'`) |
| `XCREAM` | `#F3EEE4` | Primary text/line color on blue backgrounds |
| `XINK` | `#0B1E3F` | Primary text/line color on paper backgrounds; also badge text color |
| `XAMB` | `#F2B01C` | Amber accent — numerals, highlight badges, "cost" callouts, flash states |

Secondary accents seen in I2: `#2B55E8` (a brighter blue ring/hub color used
on the paper background for contrast).

## Typography

- `.ser` → `font-family:"PlayfairDisplay-Regular"`, `letter-spacing:-.045em`,
  `line-height:.95`. Used for: headline numerals ("01", "02"), big callout
  lines ("I pay only for / the wheeling."), short single-letter node labels
  ("A", "B").
- `.sans` → `font-family:"PlayfairDisplay-Italic"` (the class name is
  historical/misleading — it is the *italic* serif face, not a sans-serif),
  `letter-spacing:-.01em`. Used for: small captions ("generator", "consumer"),
  kicker labels ("power wheeling"), footnotes.
- Both are plain `position:absolute; white-space:nowrap` text, centered via
  `transform:translateX(-50%)` when needed — not flex/grid layout.

## Texture & camera

- A grain-texture PNG (embedded base64 in `ill_base.js`) is composited over
  every scene and given a small per-frame drift
  (`translate(x,y)` cycling via `Math.floor(t*24)*37 % 64` etc.) so it reads
  as filmic noise, not a static overlay.
- Every scene has a "breathing zoom": scale oscillates by ±4.5% across the
  scene's lifetime via `gSIN(u)` where `u` is the scene's local progress
  0→1. This is applied automatically by the shared `XILL.render(t)` loop —
  individual scenes don't need to implement it themselves.
- Scene entrance/exit: opacity and blur both ride `gSIN` over the first/last
  0.3s of the scene's `[t0,t1]` window — scenes fade+blur in and out, they
  never hard-cut.

## Easing cheat-sheet

| Function | Shape | Typical use |
|---|---|---|
| `gOUT` | quartic ease-out | reveals that should feel snappy/decisive (ring draw-on, post draw-on) |
| `gIO` | cubic ease-in-out | continuous motion with soft start+end (the A→B wire drawing on) |
| `gSIN` | cosine 0→1 | symmetric fade in/out (scene opacity, camera breathing) |
| `iBACK` | back-ease with overshoot | "pop" elements — badges, stamps, anything that should feel like it snaps into place with a little bounce |
| `gL` | linear | raw position interpolation (e.g. the traveling pulse dot's x-position along its path) |

## SVG reveal pattern

Lines/paths are drawn on with `drawP(path, path.len, progress)`, which sets
`stroke-dasharray = len` and `stroke-dashoffset = len * (1 - progress)` —
`progress` goes 0→1 over whatever time window you choose (usually via
`gOUT` or `gIO` of `(t - start) / duration`).

## Traveling-pulse pattern (used for "flow" diagrams like power wheeling)

1. A blurred halo circle + a small bright core circle, both `opacity:0` by
   default.
2. Each frame, compute a `phase = ((t - pStart) % loopDuration) / loopDuration`
   and an x-position `gL(startX, endX, phase)`.
3. Fade phase in/out near 0 and 1 (`gC(Math.min(phase, 1-phase) / fadeWidth)`)
   so the loop doesn't pop.
4. Wrap the whole pulse in a life-envelope (`gOUT` in, `gOUT` out over the
   scene's active pulse window) so it doesn't loop forever — it should
   clearly start and stop.
5. If something else (a badge, a label) sits near the pulse's path, compute
   a proximity "flash" value (`gC(1 - abs(px - targetX) / threshold)`) and
   use it to recolor a nearby element (e.g. gate posts flashing amber) —
   this sells the idea that the pulse is "triggering" that element.
