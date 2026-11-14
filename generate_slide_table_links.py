import json
import re

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json") as f:
    modules = json.load(f)

# Define explicit, high-precision link rules for the core slides so mapping is 100% accurate
SLIDE_LINKS = {
    "week2-slide 3": [
        {"phrase": "-Rp 90.5T", "row": 6, "col": 1, "label": "2023 Net Loss: (90,516.3)"},
        {"phrase": "-Rp 1.50T", "row": 6, "col": 3, "label": "2025 Net Loss: (1,501.7)"},
        {"phrase": "Rp 7,742.6 bn", "row": 8, "col": 3, "label": "2025 Total Debt: 7,742.6"},
        {"phrase": "(Rp 875.3 bn)", "row": 13, "col": 3, "label": "2025 Free Cash Flow: (875.3)"},
        {"phrase": "Rp 214.1 trillion", "row": 10, "col": 3, "label": "2025 Retained Deficit: (214,142.5)"}
    ],
    "week2-slide 5": [
        {"phrase": "59.8%", "row": 6, "col": 3, "label": "Total Opex: 59.8% of Rev"},
        {"phrase": "57.7%", "row": 2, "col": 3, "label": "Gross Margin: 57.7%"},
        {"phrase": "(Rp 378.1 bn)", "row": 7, "col": 2, "label": "Operating Loss (EBIT): (378.1)"}
    ],
    "week2-slide 6": [
        {"phrase": "(Rp 214.1 trillion)", "row": 4, "col": 3, "label": "Ending Retained Deficit: (214,118.8)"},
        {"phrase": "Rp 35.72T", "row": 7, "col": 1, "label": "Beginning Equity: 35,720.5"},
        {"phrase": "Rp 28.71T", "row": 7, "col": 3, "label": "Ending Equity: 28,711.7"}
    ],
    "week2-slide 8": [
        {"phrase": "Rp 10.4T", "row": 1, "col": 1, "label": "2024 Liabilities: 10,428.1"},
        {"phrase": "Rp 17.0T", "row": 1, "col": 2, "label": "2025 Liabilities: 17,046.5"},
        {"phrase": "+63.5%", "row": 1, "col": 3, "label": "Liabilities Growth: +63.5%"}
    ],
    "week2-slide 10": [
        {"phrase": "Rp 751 bn", "row": 4, "col": 2, "label": "2025 Net Change in Cash: 751.4"},
        {"phrase": "Rp 3.72 trillion", "row": 2, "col": 2, "label": "New Bank Borrowings: 3,718.0"},
        {"phrase": "-Rp 875.3 bn", "row": 0, "col": 2, "label": "Free Cash Flow: (875.3)"}
    ],
    "week2-slide 14": [
        {"phrase": "+Rp 307 bn", "row": 3, "col": 1, "label": "Operating Cash Flow (CFO): 307.0"},
        {"phrase": "Rp 1.8 trillion", "row": 1, "col": 1, "label": "Non-Cash Add-backs: 1,808.7"}
    ]
}

# Verify that all target rows and cols exist
for key, links in SLIDE_LINKS.items():
    mod_id, s_str = key.split("-slide ")
    s_num = int(s_str)
    mod = next(m for m in modules if m["id"] == mod_id)
    slide = next(s for s in mod["slides"] if s["slide_num"] == s_num)
    rep = slide["goto_report"]
    rows = rep["table_rows"]
    note = rep["analytical_note"]
    print(f"Verified {key}:")
    for link in links:
        p = link["phrase"]
        assert p in note, f"Phrase '{p}' not in note!"
        r = link["row"]
        c = link["col"]
        assert r < len(rows), f"Row {r} out of range ({len(rows)})"
        assert c < len(rows[r]), f"Col {c} out of range ({len(rows[r])})"
        print(f"  '{p}' -> Row {r} ({rows[r][0]}) Col {c} = {rows[r][c]}")

print("\nAll predefined links verified successfully!")
