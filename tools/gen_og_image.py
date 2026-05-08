"""Generate og-image.png (1200x630) for doneliezer.com social-share previews.

One-shot. Run from any working directory:
    python tools/gen_og_image.py
"""
from pathlib import Path
import urllib.request
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
SITE_ROOT = SCRIPT_DIR.parent
FONT_DIR = SCRIPT_DIR / ".fonts"
FONT_DIR.mkdir(exist_ok=True)

# Variable-font TTFs straight from the google/fonts repo.
FONT_URLS = {
    "Fraunces.ttf":
        "https://github.com/google/fonts/raw/main/ofl/fraunces/"
        "Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf",
    "JetBrainsMono.ttf":
        "https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/"
        "JetBrainsMono%5Bwght%5D.ttf",
}

def font_path(name: str) -> Path:
    p = FONT_DIR / name
    if not p.exists():
        print(f"Downloading {name} from Google Fonts mirror...")
        urllib.request.urlretrieve(FONT_URLS[name], p)
    return p

# Site palette
BG = (0xFB, 0xFA, 0xF7)
TEXT = (0x1A, 0x1A, 0x18)
MUTED = (0x6E, 0x6B, 0x66)
FAINT = (0xA0, 0x9C, 0x95)
ACCENT = (0xB8, 0x54, 0x32)

W, H = 1200, 630
LM = 96  # left margin

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

fraunces = font_path("Fraunces.ttf")
mono = font_path("JetBrainsMono.ttf")

# Eyebrow: short accent rule + label
EYEBROW_Y = 140
RULE_LEN = 40
d.line([(LM, EYEBROW_Y + 12), (LM + RULE_LEN, EYEBROW_Y + 12)],
       fill=ACCENT, width=2)
eyebrow_font = ImageFont.truetype(str(mono), 20)
d.text((LM + RULE_LEN + 18, EYEBROW_Y), "PORTFOLIO", font=eyebrow_font, fill=ACCENT)

# Heading "DonEli Baize"
heading_font = ImageFont.truetype(str(fraunces), 152)
d.text((LM, EYEBROW_Y + 60), "DonEli Baize", font=heading_font, fill=TEXT)

# Subtitle "Senior iOS Engineer"
subtitle_font = ImageFont.truetype(str(fraunces), 56)
d.text((LM, EYEBROW_Y + 60 + 200), "Senior iOS Engineer", font=subtitle_font, fill=MUTED)

# Bottom URL line
url_font = ImageFont.truetype(str(mono), 22)
d.text((LM, H - 80), "doneliezer.com", font=url_font, fill=FAINT)

# Right-side accent strip — a vertical line that visually echoes the patent-card chevron
strip_x = W - 64
d.line([(strip_x, 96), (strip_x, H - 96)], fill=ACCENT, width=4)

out = SITE_ROOT / "og-image.png"
img.save(out, optimize=True)
print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")
