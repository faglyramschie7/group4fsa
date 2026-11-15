import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import fitz
from PIL import Image, ImageDraw, ImageFont
import os

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
doc = fitz.open(pdf_path)
page = doc[16] # page 17

# Render base page at 200 DPI (approx 2.777x scale)
dpi = 200
scale = dpi / 72.0
pix = page.get_pixmap(dpi=dpi)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

print(f"Rendered image size: {img.size}")
