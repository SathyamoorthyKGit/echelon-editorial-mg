from playwright.sync_api import sync_playwright
import os

# ---- EDIT PER PROJECT ----
HTML_FILE = 'lthird.html'      # your filled-in copy of template/lthird_template.html
DURATION_S = 5.0               # total lower-third duration, must match EXIT1 in the HTML
FPS = 30
OUT_DIR = 'frames'
# ---------------------------

N = int(DURATION_S * FPS)
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    # These launch args keep text rendering consistent/deterministic across runs
    # (no subpixel LCD hinting, fixed color profile) so frame-to-frame text
    # positioning doesn't jitter.
    browser = p.chromium.launch(args=['--font-render-hinting=none', '--force-color-profile=srgb', '--disable-lcd-text'])
    page = browser.new_page(viewport={'width': 1080, 'height': 1920})
    page.goto('file://' + os.path.abspath(HTML_FILE))
    page.wait_for_function('typeof window.setT === "function"')
    for i in range(N):
        t = i / FPS
        page.evaluate(f'window.setT({t})')
        # omit_background=True is what gives a true alpha-transparent PNG —
        # without it Playwright fills the page's CSS background (even
        # "transparent") with white before screenshotting.
        page.screenshot(path=f'{OUT_DIR}/f_{i:05d}.png', omit_background=True)
    browser.close()
print('rendered', N, 'frames to', OUT_DIR)

# Next step (not run here) — encode the alpha PNG sequence to a transparent
# ProRes 4444 .mov, which both DaVinci/Premiere/AE and most social platforms'
# upload pipelines accept with alpha intact:
#
#   ffmpeg -framerate 30 -i frames/f_%05d.png \
#     -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -alpha_bits 8 -qscale:v 11 \
#     output_TRANSPARENT.mov
