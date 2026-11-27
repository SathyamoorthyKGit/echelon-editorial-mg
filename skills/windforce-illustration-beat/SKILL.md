---
name: windforce-illustration-beat
description: Build a single animated "illustration beat" (an SVG explainer diagram sequence) in the Echelon/WindForce house visual style, rendered as a chunked frame sequence and encoded to ProRes 4444 with alpha. Use when a video needs an original, hand-animated explainer diagram (not stock footage, not AI video) that matches the WindForce reel look — studio blue / paper backgrounds, cream/ink/amber accents, Playfair Display serif+italic type, grain texture, "breathing zoom" camera.
---

# WindForce illustration-beat animation system

This skill documents the technique used to build the "I1" / "I2" style
illustration beats in the WindForce H01/H02 vertical reels — small, fully
original, code-animated explainer diagrams (e.g. "power wheeling: generator
sells A to B, pays only the wheeling cost", or "open access" ring diagram).

It is **not a standalone renderer**. It was built and rendered inside a Claude
session using Claude's internal "Film" Artifact harness (a Playwright-driven
`render.mjs` that loads an `index.html` appifact manifest and calls
`window.__animation.load(files)` / `.frame(t, {scale})` per frame). That
harness is Anthropic product infrastructure, not user-owned code, so it is
intentionally **not included** in this repo. What *is* included is all of the
original, portable animation code and the full recipe, so a future Claude
session with access to the Film artifact type (or an equivalent custom
Playwright harness you build) can reproduce the exact technique and output.

## When to use this

- A new illustration beat is needed for a reel in this house style (a new
  concept diagram, not a reuse of I1/I2 verbatim).
- An existing beat needs a visual fix (layout bug, timing bug, new badge/label).
- Someone wants to understand how the "toll-gate power wheeling" (I1) or
  "open access ring" (I2) animations in WindForce H02 were built.

## House visual style (reference/ill_base.js)

`reference/ill_base.js` is the shared kit: colors, easing functions, SVG
helpers, and the two text classes. Read this file first — it's the style
bible. Key constants:

- `XBLUE = '#2F7FEA'` (studio blue background), `XPAPER = '#F6F4F2'` (paper
  background) — each scene picks one via its `kind: 'blue'|'paper'`.
- `XCREAM = '#F3EEE4'`, `XINK = '#0B1E3F'`, `XAMB = '#F2B01C'` — cream/ink/amber
  accent colors used for text, lines, and highlight badges.
- Typography: `.ser` = `PlayfairDisplay-Regular` (upright serif, headlines,
  big numbers), `.sans` = `PlayfairDisplay-Italic` (despite the class name —
  it's actually the italic face, used for captions/labels/taglines).
- A large embedded base64 grain-texture PNG (~88KB, inline in `ill_base.js`)
  is overlaid on every scene for a filmic paper-grain look. A stippled SVG
  filter is available for human figures (not used in I1/I2, but available).
- Camera: every scene gets a subtle "breathing zoom" — `gSIN` (cosine-based
  0→1→0 ease) drives a small scale pulse across the scene's lifetime, plus a
  drifting grain-texture offset, so nothing feels perfectly static.

### Shared primitives (all in `ill_base.js`)

| Function | Purpose |
|---|---|
| `gC(x)` | clamp to [0,1] |
| `gIO(x)` | cubic ease-in-out |
| `gOUT(x)` | quartic ease-out (snappy reveal) |
| `gSIN(x)` | cosine-based 0→1 (smooth in/out, used for camera breathing & scene fade) |
| `gL(a,b,t)` | linear interpolation |
| `sv(tag, attrs, parent)` | SVG element factory |
| `drawP(path, len, x)` | stroke-dasharray/dashoffset reveal (x in 0..1 draws the path from 0% to x%) |
| `iBACK(x)` | back-easing overshoot pop (badges, stamps) |
| `xBase(kit, kind)` | scene root builder — returns context `c` with `c.ser`/`c.sans` (text factories), `c.path` (path factory with `.len` precomputed), `c.svg` (root `<svg>`) |
| `xType(textObj, t, t0, t1)` | word-by-word fade+blur+translateY reveal between t0 and t1 |
| `xFade(obj, t, t0, dur)` | simple fade+blur reveal |

## Scene registration pattern

Each beat is one `XS.push({ t0, t1, kind, init(c) {...}, render(t, c) {...} })`
call. See `reference/scene_example_I1_I2.js` (the real I1 + I2 scenes from
WindForce H02) for a complete worked example, including:

- I1: a toll-gate power-wheeling diagram (grid backdrop, a traveling light
  pulse A→B via a sawtooth loop + per-frame `setAttribute('cx', ...)`, gate
  posts that flash amber when the pulse passes under them, and an amber badge
  that pops in via `iBACK`).
- I2: an "open access" ring diagram (radial satellites animating in with
  staggered delay, a central hub growing via `drawP`-style radius tween).

**Critical gotcha**: `init(c)` and `render(t, c)` do **not** share lexical
scope — they're two separate functions on the same object. Any geometry
constant computed in `init` that `render` needs (e.g. an x-coordinate used
for a hit-test or threshold) must be stored onto `c` in `init`
(`c.tagX = TX`) and read back from `c` in `render`, never closed over as a
local variable.

**Known fix pattern — badge/label collisions**: when a pill/badge overlaps a
line or another element, check for insufficient clearance between the
badge's bounding box and whatever it sits near, remembering that serif text
with descenders (g, y, p) needs real line-height room above its baseline —
don't just nudge y, actually recompute the pill height/position and the
competing element's extents together. See `reference/scene_example_I1_I2.js`
for the final corrected I1 badge coordinates (pill lifted to clear the wire,
gate posts shortened to stay below the pill, text repositioned with explicit
`line-height:1.05`).

## Pipeline scripts (reference/)

These are the supporting Python scripts used around the actual scene file,
in the order they run:

1. `srt_to_csv.py` — convert a subtitle/transcript `.srt` into a per-word
   timing CSV (`tr.csv`) used to drive caption timing.
2. `blocks2.py` — groups words from `tr.csv` into caption "blocks" (`B` list)
   for on-screen captions, independent of the illustration beats.
3. `mk_bgsegs.py` — computes background color/kind segments across the whole
   timeline (which ranges are blue-kind vs paper-kind vs plain footage).
4. `gen2.py` — the main build script. Reads `tr.csv` + `blocks2.py`'s output,
   builds `CARDS` / `GWIN` / `data2.json` (caption + timing data), then
   **concatenates `ill_base.js` + your scene file (e.g.
   `scene_example_I1_I2.js`) + `cut_template2.js`**, replacing placeholders,
   to produce `film/cut.js` — the single JS file the Film-artifact harness
   loads. **Re-run `gen2.py` after every edit to the scene file.**
5. `encode_parts.py` / `encode_iparts.py` — ffmpeg encode scripts: take a
   rendered PNG frame sequence and produce ProRes 4444 (`yuva444p10le`,
   `-alpha_bits 8 -qscale:v 11`) video parts, split at fixed timecodes so
   each part stays under ~370-420MB.

`cut_template2.js` is the template wrapper that turns the concatenated scene
code into something the Film-artifact harness can call
(`window.__animation.load/frame`) — kept here as reference for the expected
call shape, since the harness itself isn't shipped.

## Rendering recipe (requires a Playwright-capable harness — e.g. Claude's Film artifact type)

1. Build `film/cut.js` via `gen2.py` (see above).
2. Render in **short chunks** (≤8 seconds each) — a known Playwright/browser
   rendering-degradation bug means long single-pass renders silently produce
   garbage frames after a while. Each chunk is a **fresh browser process**:
   `node render.mjs <cut.js> <index.html> seq a:b:30 outdir` (30fps, time
   range a:b).
3. Verify each chunk before moving on: check frame file sizes
   (`os.path.getsize`) and flag any frame under ~20000 bytes as a likely
   blank/corrupt frame; re-render that chunk if so.
4. Merge chunks into one global frame sequence by computed offset
   (`chunk_idx * chunk_frames + local_idx`), renumber into `seq_final/`.
5. Encode with `encode_parts.py` (ProRes 4444 + alpha), split at scene
   boundaries to keep file sizes manageable.

## Docs

See `docs/house-style.md` for the condensed style reference (colors, type,
easing cheat-sheet) and `docs/film-artifact-dependency.md` for exactly what
is and isn't portable about the rendering harness.
