import fitz
from PIL import Image, ImageDraw, ImageFont

doc = fitz.open("GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf")
page = doc[16] # page 17

# High resolution 200 DPI
pix = page.get_pixmap(dpi=200)
base = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).convert("RGBA")

# Create overlay for semi-transparent highlights
overlay = Image.new("RGBA", base.size, (255, 255, 255, 0))
draw_overlay = ImageDraw.Draw(overlay)
draw_solid = ImageDraw.Draw(base)

scale = 200.0 / 72.0

# Fonts
font_bold_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
font_bold_md = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
font_reg_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)

print("Base dimensions:", base.size)
