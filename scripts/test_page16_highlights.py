import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import fitz

doc = fitz.open("GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf")
p = doc[15] # page 16

for target in ["215,334,000", "214,119,215", "28,711,657", "17,046,454", "45,758,111", "242,108,542"]:
    rects = p.search_for(target)
    print(f"Target '{target}': rects = {rects}")
