import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import fitz
import os

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
out_dir = "goto-fsa-study/public/evidence"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)

# Helper to highlight terms and render
def highlight_and_export(page_num, search_terms, output_filename):
    page = doc[page_num - 1]
    
    # Reload fresh page to avoid duplicate annotations
    fresh_doc = fitz.open(pdf_path)
    p = fresh_doc[page_num - 1]
    
    for term, color in search_terms:
        # Search text
        rects = p.search_for(term)
        for r in rects:
            annot = p.add_highlight_annot(r)
            annot.set_colors(stroke=color)
            annot.update()
            
    # Render at 200 DPI for high resolution
    pix = p.get_pixmap(dpi=180)
    out_path = os.path.join(out_dir, output_filename)
    pix.save(out_path)
    print(f"Exported highlighted page {page_num} -> {out_path}")

# Colors:
# Yellow: (1, 1, 0)
# Red/Pink highlight for losses/debt: (1, 0.4, 0.4)
# Green highlight for revenue/cash: (0.4, 0.9, 0.4)
# Cyan for totals: (0.4, 0.8, 1)

# 1. Page 15: Balance Sheet Assets (Cash 21,755,165, Associates 10,344,598, Total Assets 45,758,111)
highlight_and_export(
    15,
    [
        ("21.755.165", (0.3, 0.9, 0.3)), # Cash 2025
        ("10.344.598", (1, 0.9, 0.2)), # Investment in Associates
        ("45.758.111", (0.3, 0.8, 1.0)), # Total Assets 2025
    ],
    "goto_balance_sheet_assets_highlighted.png"
)

# 2. Page 16: Balance Sheet Liabilities & Equity (Borrowings, Accumulated Deficit 214,118,810, Total Equity 28,711,657)
highlight_and_export(
    16,
    [
        ("1.523.754", (1, 0.4, 0.4)), # Short-term bank debt
        ("6.218.889", (1, 0.4, 0.4)), # Long-term bank debt
        ("17.046.454", (1, 0.5, 0.5)), # Total Liabilities
        ("214.118.810", (1, 0.2, 0.2)), # Retained Deficit
        ("28.711.657", (0.3, 0.8, 1.0)), # Total Equity
        ("45.758.111", (0.3, 0.8, 1.0)), # Total Liab & Equity
    ],
    "goto_balance_sheet_liabilities_equity_highlighted.png"
)

# 3. Page 17: Income Statement (Revenue 18,322,239, Gross Profit 10,576,013, Operating Loss 378,088, Net Loss 1,501,707)
highlight_and_export(
    17,
    [
        ("18.322.239", (0.3, 0.9, 0.3)), # Net Revenue
        ("7.746.226", (1, 0.8, 0.4)), # COGS
        ("10.576.013", (0.3, 0.9, 0.3)), # Gross Profit
        ("10.954.101", (1, 0.6, 0.4)), # Total Operating Expenses
        ("378.088", (1, 0.3, 0.3)), # Operating Loss
        ("1.501.707", (1, 0.2, 0.2)), # Net Loss
    ],
    "goto_income_statement_highlighted.png"
)

# 4. Page 21: Statement of Cash Flows (CFO 307,025, Capex, Time deposits 1,386,499, Bank borrowings 3,718,000)
highlight_and_export(
    21,
    [
        ("307.025", (0.3, 0.9, 0.3)), # CFO
        ("302.138", (1, 0.4, 0.4)), # Fixed assets capex
        ("880.297", (1, 0.4, 0.4)), # Intangible capex
        ("1.386.499", (1, 0.9, 0.2)), # Withdrawal of time deposits
    ],
    "goto_cash_flows_p1_highlighted.png"
)

# 5. Page 22: Statement of Cash Flows Financing (Bank loans 3,718,000, Ending Cash 21,755,165)
highlight_and_export(
    22,
    [
        ("3.718.000", (1, 0.3, 0.3)), # Proceeds from bank loans
        ("21.755.165", (0.3, 0.9, 0.3)), # Cash at end of year
    ],
    "goto_cash_flows_p2_highlighted.png"
)

print("All highlighted audited financial statement pages exported successfully!")
