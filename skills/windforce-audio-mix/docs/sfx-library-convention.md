# SFX sample naming convention

The cue list in `scripts/mix_sfx_cues.py` references sample files by a short
descriptive name (no extension, resolved to `<W>/<name>.wav` where `W` is
the library root). These are the sample "roles" the cue list relies on —
name your own library's samples to match, or edit the cue list to point at
your actual filenames:

| Role name used in cues | What it should sound like | Typical use |
|---|---|---|
| `Deep_Whoosh_2`, `Deep_Whoosh_3` | Low, heavy whoosh with real weight | Card/illustration "in" transitions |
| `Short_Whoosh_Metal` | Bright, quick metallic whoosh | Line draws, ring/path reveals, quick transitions |
| `Simple_Whoosh_2` | Clean mid-weight whoosh, no metallic tail | Illustration-beat entrances |
| `Whoosh_Short_2` | Short whoosh, slightly softer than Simple_Whoosh_2 | "Out" transitions (card/illustration exits) |
| `Hit_1` | Light, soft hit/tick | Small fades, numeral reveals |
| `Hit_2` | Medium punchy hit | Mid-weight word/phrase lands |
| `Hit_3` | Heavier hit with more decay | Big headline word lands |
| `Deep_Hit_2`, `Deep_Hit_3` | Low, weighty hit with real sub content | Badge/tag pops, major punchline lands |
| `1_Click_Mouse` | Tiny, dry UI click | Caption-box ticks, label-typing ticks, wire-draw ticks |
| `Mouse_Clicks` | A short cluster/run of clicks | Multiple elements popping in near-simultaneously (e.g. satellite nodes) |
| `Riser_2`, `Riser_3` | Rising tension riser, 1-2s | Camera push into a closing line, building to a punchline |

## General rules for picking/placing cues

- Every **visual entrance** (card in, illustration in, element draws on)
  gets a whoosh anchored with `kind='peak'` so the loudest part of the
  whoosh lands exactly on the visual's start frame.
- Every **text landing** (a word or line finishing its reveal) gets a hit
  anchored with `kind='on'` so the hit's attack — not its peak — lands on
  the frame, which reads as tighter sync than peak-anchoring a hit.
- Small mechanical details (a tick as each word types on, a click as a line
  segment draws) get very quiet (-30 to -33dB) single clicks — these should
  be felt more than heard.
- Use `trim_length` (with the built-in 200ms fade-out) on any hit/riser
  whose natural decay would otherwise ring into the next cue less than
  ~0.3s away.
- Gain-stage so the quietest cues (ticks, clicks) sit around -30 to -33dB
  relative to the loudest (card/illustration transitions around -22 to
  -26dB) — the final `pk` normalization in the script brings everything up
  to -6dBFS peak as a group, preserving these relative balances.
