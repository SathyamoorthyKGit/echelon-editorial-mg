# WindForce H02 production pipeline

Reusable Claude Skills extracted from the production of Echelon Media's
"WindForce H02" vertical highlight reel (power wheeling / open-access
electricity market reform, for WindForce PLC). Each skill packages one
reusable technique from that project so it can be applied to future reels
without rebuilding the approach from scratch.

This repo intentionally contains **only skills, scripts, templates, and
docs** — no rendered video, no PNG frame sequences, and no SFX sample
library. Those are large binary project assets that belong in project
storage, not source control.

## Skills

- **[`skills/windforce-illustration-beat/`](skills/windforce-illustration-beat/)**
  — the code-animated SVG explainer-diagram system (studio blue / paper
  backgrounds, Playfair serif/italic type, grain texture, "breathing zoom"
  camera) used for the I1 ("power wheeling toll-gate") and I2 ("open access
  ring") illustration beats. Documents the house visual style, the shared
  animation primitives, the scene-registration pattern, and the chunked
  render/encode pipeline — including an explicit note on what parts
  (`render.mjs`, the Film artifact harness) are Claude product
  infrastructure and are deliberately *not* included here.

- **[`skills/windforce-audio-mix/`](skills/windforce-audio-mix/)** — the
  audio-mix pipeline: anchor-based SFX cue placement against a locked
  voice-over timeline, sidechain-ducked music bed, and a two-pass ffmpeg
  `loudnorm` pass to -14 LUFS / -1.5 dBTP. Includes the full H02 cue list as
  a worked example and a cue-sheet CSV format for sound-designer handoff.

- **[`skills/windforce-lower-third/`](skills/windforce-lower-third/)** — a
  self-contained (no product-harness dependency) kinetic-typography
  lower-third generator: a transparent name/title card rendered directly
  with Playwright and encoded to alpha ProRes 4444. Includes the fonts, the
  parameterized HTML template, and the frame-rendering script.

## Background

Built across a single production session covering: the full H02 audio mix
(voice + SFX + ducked music bed), two rounds of visual bug-fixing on the I1
illustration (a pulse/badge timing collision, then a badge/gate-post/text
layout collision), and a from-scratch lower-third animation for WindForce's
Managing Director (Manjula Perera), iterated through several rounds of
feedback (line-break, bold name, designation color, scrim removal).

Each skill's `SKILL.md` documents the technique in enough depth that a
future Claude session — or a human motion designer reading the code — can
reproduce the exact output or adapt it to a new reel.
