---
name: windforce-lower-third
description: Generate a transparent, kinetic-typography lower-third (name + title card animation) in the WindForce/Echelon house style, as a self-contained HTML/CSS/JS file rendered to an alpha-channel video — no dependency on any product-specific rendering harness. Use when a video needs a "name / title" caption card that types on and off over footage, delivered as a transparent overlay.
---

# WindForce lower-third generator

Produces a 5-second (adjustable), fully transparent kinetic-typography
lower-third: a short amber tick-mark, a bold name line, a thin rule, and one
or two italic role/title lines — all typing on word-by-word with a
fade+blur+rise reveal, holding, then reversing out the same way.

Unlike `windforce-illustration-beat`, this is **not** built on Claude's Film
Artifact harness — it's a plain, portable HTML file you can render with any
Playwright setup, with zero product-specific dependency. This is the
reference pattern to follow if you want to port the illustration-beat system
off the Film harness too (see that skill's
`docs/film-artifact-dependency.md`).

## Quick start

1. Copy `template/lthird_template.html` to a working file (e.g. `lthird.html`).
2. Replace the three placeholders in its `<script>` block:
   `{{NAME}}`, `{{ROLE_LINE_1}}`, `{{ROLE_LINE_2}}` (set `ROLE_LINE_2` to
   `''` and remove the `#role2` div/CSS if you only need one role line).
3. Make sure `fonts/PlayfairDisplay-Regular.ttf` and
   `fonts/PlayfairDisplay-Italic.ttf` sit one directory above your working
   HTML file (i.e. at `../fonts/...` relative to it), or adjust the
   `@font-face src` paths. Both are included in this skill's `fonts/`
   directory.
4. If any line is noticeably longer/shorter than the originals ("Manjula
   Perera" / "Managing Director," / "WindForce PLC."), you may need to widen
   `#rule`'s target width (currently a hardcoded `420px` in the `setT`
   function, two places) or adjust the type-on duration constants (below) so
   the reveal pacing still feels right for the new line lengths.
5. Run `scripts/render_frames.py` (edit its `HTML_FILE`/`DURATION_S`
   constants at the top first) to produce a PNG-with-alpha frame sequence.
6. Encode to transparent ProRes 4444 with the ffmpeg command printed at the
   bottom of `render_frames.py`.

## Timing constants (all in seconds, all editable in the `<script>` block)

| Constant | Controls |
|---|---|
| `T_IN0`, `TICK_D` | Amber tick-mark scale-in start/duration |
| `NAME0`, `NAME1` | Name line's word-by-word type-on window |
| `RULE0`, `RULE1` | Horizontal rule's width-grow window |
| `ROLE1_0`, `ROLE1_1` | Role line 1's type-on window |
| `ROLE2_0`, `ROLE2_1` | Role line 2's type-on window (starts slightly before role line 1 finishes, for a natural cascade) |
| `EXIT0`, `EXIT1` | When the whole card starts/finishes reversing out |

The reveal itself (`typeOn`/`exitOut`) is the same word-span pattern as
`windforce-illustration-beat`'s `xType`, reimplemented standalone here so
this file has no external JS dependency: each word is its own `<span>`,
staggered by `(t1-t0)/n` per word, each fading in from `opacity:0,
blur(8px), translateY(10px)` to fully resolved over a fixed 0.3s window per
word.

## Styling notes (this project's specific choices — see `windforce-illustration-beat/docs/house-style.md` for the fuller palette)

- Name line: `PlayfairDisplay-Regular` at `font-weight:700` (no true bold
  face was available — see "synthetic bold" below), color `#F3EEE4`
  (cream), `font-size:54px`.
- Role lines: `PlayfairDisplay-Italic`, color `#F3EEE4` (cream/white — not
  the amber `#F2B01C` used elsewhere in the house style; this was a
  deliberate choice for this card so the role text reads as equally
  important as the name rather than as a secondary accent).
- Tick mark: solid `#F2B01C` (amber), the one remaining amber accent on the
  card, scale-Y animated in from the top.
- **No background scrim.** Earlier drafts of this card included a dark
  gradient scrim behind the text for legibility over bright footage — this
  was explicitly removed so the delivered file is pure alpha typography with
  nothing else baked in, leaving all backdrop/legibility decisions to
  whoever composites the card over their footage.

### Synthetic bold technique

Only Regular/Italic/BoldItalic/BlackItalic weights of Playfair Display were
available (no plain upright Bold). To get a bold-looking upright name line
anyway: `font-weight:700` plus a CSS `text-shadow` stroke trick —
`text-shadow: 0.6px 0 0 currentColor, -0.6px 0 0 currentColor` — which
offsets a duplicate of the glyph 0.6px left and right in the same color,
faking extra stroke weight. If you do have a real Bold TTF available,
prefer it and drop this hack.

## Why `omit_background=True` matters

Playwright's `page.screenshot()` will flatten a page's "transparent" CSS
background to opaque white unless you pass `omit_background=True` — this is
what actually produces a true per-pixel alpha channel in the output PNGs,
which is what lets the ffmpeg ProRes 4444 encode carry real transparency
through to the final video.
