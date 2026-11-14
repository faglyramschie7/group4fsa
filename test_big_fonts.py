import fitz
from PIL import Image, ImageDraw, ImageFont

doc = fitz.open("GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf")
page = doc[16] # page 17

dpi = 220
scale = dpi / 72.0
pix = page.get_pixmap(dpi=dpi)
base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

print("Base img with DPI=220:", base_img.size)
