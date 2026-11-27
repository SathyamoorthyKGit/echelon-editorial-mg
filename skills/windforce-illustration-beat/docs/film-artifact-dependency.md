# What's portable, and what isn't

This skill's rendering pipeline was originally run on top of Claude's
internal "Film" Artifact type: a Playwright-driven `render.mjs` script that
loads a product-owned `index.html` ("appifact") harness and calls
`window.__animation.load(files)` / `window.__animation.frame(t, {scale})`
once per frame, screenshotting the result.

**Not included in this repo, and should never be committed to a user repo:**

- `render.mjs` (the Playwright driver)
- `film/index.html` (the appifact harness itself — contains an
  `artifact.json`-style manifest, `capabilities` flags, `appifact-flags`
  vocabulary, and internal monitoring/alerting config). This is Anthropic
  product infrastructure, not user-authored content, and isn't ours to
  redistribute.

**Fully portable and included here:**

- `ill_base.js` — the shared style kit (colors, easing, SVG helpers, text
  factories, grain texture). Pure vanilla JS + inline SVG manipulation, zero
  dependency on the Film harness's API beyond the generic
  `window.__animation.load/frame` call shape it's wrapped in.
- The scene files themselves (`scene_example_I1_I2.js`) — pure
  `XS.push({...})` scene objects, same story.
- All the Python pipeline scripts (caption timing, encode scripts) — these
  operate on PNG frame sequences and don't care how the frames were
  produced.

## Reproducing this in a future Claude session

If you have access to Claude's Film Artifact type in a future session, the
fastest path is: create a new Film artifact, and port `ill_base.js` +
your scene file into it following whatever file layout that artifact type's
own SKILL.md specifies at that time (it may have evolved since this was
written). The scene-registration API (`XS.push`, `xBase`, `xType`, etc.) is
the stable, reusable part — carry it over verbatim.

If you don't have access to that artifact type, the same technique works
with a **self-contained Playwright harness you write yourself** — see
`windforce-lower-third`'s approach in this same repo
(`skills/windforce-lower-third/template/lthird_template.html` +
`skills/windforce-lower-third/scripts/render_frames.py`) as a working
example of a fully portable, no-product-dependency version of the same
"load HTML, call a `window.setT(t)` per frame, screenshot" pattern. Porting
`ill_base.js`'s scene system onto that pattern instead of the Film harness
is a straightforward rewrite: replace `window.__animation.load/frame` calls
with a single `window.setT(t)` that calls `XILL.render(t)` internally, and
render with Playwright's `page.screenshot()` directly instead of the
harness's own screenshot path.
