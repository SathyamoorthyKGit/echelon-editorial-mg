---
name: windforce-audio-mix
description: Build a finished audio mix (voice-over + anchored SFX cues + ducked background music bed) for a WindForce/Echelon vertical reel, at -14 LUFS / -1.5 dBTP, plus an SFX cue-sheet CSV. Use when a reel's voice-over and visuals are locked and you need the final mixed audio deliverable (stems + cue sheet + loudness-normalized master).
---

# WindForce audio-mix pipeline

Two-stage pipeline: (1) place SFX cues against the locked voice-over/visual
timeline and render SFX stems + a cue-sheet CSV, (2) duck a music bed under
the voice track, combine all stems, and loudness-normalize to broadcast
spec. Both stages are plain numpy/wave Python — no external audio library
dependency beyond numpy.

## Required inputs

- `audio/speech.wav` — the locked voice-over track, 48kHz stereo, full
  reel duration.
- `audio/bgm_src.wav` — a background music bed (any length ≥ reel duration;
  the script trims from 0:00).
- A folder of individual SFX sample `.wav` files (whooshes, hits, clicks,
  risers) — referenced by filename in the cue list. This repo does **not**
  ship the actual sample library (it's a large binary asset); bring your own
  or point `W` in `scripts/mix_sfx_cues.py` at your library's path.
- A `data2.json` (caption/word-timing data, produced by the
  `windforce-illustration-beat` skill's `gen2.py`) if you want the
  "caption box pop" SFX layer auto-generated from caption timing. Optional —
  you can drop that block and write a fully manual cue list instead.

## Stage 1 — SFX cue placement (`scripts/mix_sfx_cues.py`)

This is kept as a **worked example** from WindForce H02 — a real, complete
cue list for an 86.5s reel — rather than a generic templated script, because
every reel's cue list is bespoke to its edit. Copy this file per-project and
edit the cue list (`G`, `F`) for the new reel's timeline.

### The anchor pattern (the key idea worth reusing)

SFX samples don't start with their audible "hit" at sample 0 — a whoosh has
a run-up, a hit sample has a tiny pre-roll. The `anchor(x, kind)` function
finds the actual perceptual onset inside a sample so you can align *that*
point to an exact timecode, not the start of the file:

- `kind='peak'` — find the loudest point in the sample (good for whooshes,
  risers — things that build to an impact).
- `kind='on'` — find the first point that crosses within 30dB of the
  sample's peak (good for hits/clicks — things that are already loud from
  the start, where you want the attack, not the loudest later moment).

Each cue is a tuple:
```python
(t, filename, kind, rel_gain_db, trim_start, trim_length, label)
```
`t` is the timecode you want the anchor point to land on; `trim_start` /
`trim_length` (both optional, in seconds) let you cut a sample short (with a
200ms fade-out) when you only want part of it — useful for long hits where
you want punch without the decay stepping on the next cue.

### Two stems, one purpose

Cues are split into two output stems — `audio/sfx_graphics.wav` (UI/caption/
illustration cues — the "on-screen graphics" layer) and `audio/sfx_footage.wav`
(cues synced to video cutaways, e.g. B-roll cuts) — so a later edit can
re-balance or mute one layer independently. If a reel has no footage
cutaways yet, leave the `F` list empty; the script still writes a silent
`sfx_footage.wav` so the stage-2 script's file layout stays consistent.

### Output

- `audio/sfx_graphics.wav`, `audio/sfx_footage.wav` — rendered SFX stems.
- `audio/WF_<reel>_SFX_cue_sheet.csv` — columns
  `stem, clip_start_s, sync_point_s, sfx_file, moment, rel_gain_db` — a
  human-readable log of every cue placed, sorted by timecode. Useful for a
  sound designer reviewing the mix, or for re-deriving the cue list later.

## Stage 2 — ducking, combining, and loudness normalization (`scripts/duck_mix.py`)

1. Loads `speech.wav`, `bgm_src.wav`, and the two SFX stems from stage 1,
   all padded/trimmed to the same sample count.
2. **Sidechain duck**: envelope-follows the speech track (5ms hop, max of
   abs value per hop), gates at -38dB (speech present vs. not), smooths the
   gate with asymmetric attack/release (`atk=0.25` fast duck-down,
   `rel=0.08` slower recovery, both as a per-5ms-hop interpolation
   coefficient) so the duck doesn't chatter or pump audibly, then applies a
   -9dB duck depth to the music bed wherever speech is present.
3. Combines stems into the standard deliverable set: ducked music bed alone,
   combined SFX stem, music+SFX stem, voice+SFX mix, and the full
   pre-normalization mix (speech -2dB + all SFX + ducked music, soft-limited
   if the peak exceeds 0.98).
4. **Loudness normalize** the full mix with ffmpeg `loudnorm`, two-pass
   (measure, then apply with the measured `I`/`TP`/`LRA`/`thresh` values and
   `linear=true`), targeting **I=-14 LUFS, TP=-1.5 dBTP** — the broadcast/
   social-video spec this house uses. Run as a separate shell step after
   `duck_mix.py`:
   ```bash
   ffmpeg -i audio/WF_<reel>_Full_mix_prenorm.wav -af loudnorm=I=-14:TP=-1.5:print_format=json -f null -
   # read out measured_I / measured_TP / measured_LRA / measured_thresh / offset from stderr
   ffmpeg -i audio/WF_<reel>_Full_mix_prenorm.wav -af loudnorm=I=-14:TP=-1.5:measured_I=<..>:measured_TP=<..>:measured_LRA=<..>:measured_thresh=<..>:offset=<..>:linear=true:print_format=summary audio/WF_<reel>_Full_mix_-14LUFS.wav
   ```

## Deliverable set (what to hand off)

Per reel, the finished audio deliverables are:
`WF_<reel>_Full_mix_-14LUFS.wav` (final master), `WF_<reel>_Voice+SFX_mix.wav`,
`WF_<reel>_Music+SFX_stem.wav`, `WF_<reel>_Music_bed_ducked_<trackname>.wav`,
`WF_<reel>_SFX_all_stem.wav`, `WF_<reel>_SFX_graphics_stem.wav`,
`WF_<reel>_SFX_footage_cuts_stem.wav`, `WF_<reel>_SFX_cue_sheet.csv` — eight
stems/mixes plus the cue sheet, so an editor or sound mixer can rebalance
any layer without redoing the whole mix.

## docs/sfx-library-convention.md

Notes on the sample-naming convention this cue list assumes (e.g.
`Short_Whoosh_Metal`, `Hit_2`, `1_Click_Mouse`, `Deep_Whoosh_2`,
`Riser_2`/`Riser_3`) if you're sourcing a new SFX library and want cues to
drop in with minimal renaming.
