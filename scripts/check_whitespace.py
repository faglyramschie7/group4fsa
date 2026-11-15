import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import fitz

doc = fitz.open("GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf")
page = doc[16] # page 17
words = page.get_text("words")

# Find max x for each y range
y_ranges = [
    (180, 210, "Revenue"),
    (210, 230, "COGS"),
    (230, 280, "Opex"),
    (280, 315, "Operating Loss")
]

for y0, y1, label in y_ranges:
    in_range = [w for w in words if y0 <= w[1] <= y1 or y0 <= w[3] <= y1]
    if in_range:
        min_x = min(w[0] for w in in_range)
        max_x = max(w[2] for w in in_range)
        print(f"{label} (y={y0}-{y1}): x range = {min_x:.1f} to {max_x:.1f} (page width={page.rect.width})")
