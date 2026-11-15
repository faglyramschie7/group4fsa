import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import fitz

doc = fitz.open("GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf")
page = doc[16] # page 17

# Find rects
rev_rects = page.search_for("18,322,117")
cogs_rects = page.search_for("7,746,034")
ga_rects = page.search_for("3,988,925")
sm_rects = page.search_for("3,090,124")
rd_rects = page.search_for("2,152,272")
ops_rects = page.search_for("974,464")
da_rects = page.search_for("748,552")
total_cost_rects = page.search_for("18,700,371")
op_loss_rects = page.search_for("378,254")

print("Found all rects:", bool(rev_rects and cogs_rects and ga_rects and op_loss_rects))
