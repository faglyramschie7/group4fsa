import pypdf
import docx
import openpyxl
import json
import os
import glob
import re

print("Starting deep extraction of all FSA materials and GoTo datasets...")

# Helper to clean strings
def clean_str(s):
    if not s: return ""
    return re.sub(r'\s+', ' ', str(s)).strip()

# 1. Parse all 11 PPTs
ppt_files = [
    ("Week 1", "The FSA Mindset & Six-Step Framework", "ppt/FSA_Week1_PPT.pdf"),
    ("Week 2", "Refresher & Five Forces Strategy Analysis", "ppt/FSA_Week2_PPT.pdf"),
    ("Week 3", "Asset/Liability Valuation & Income Recognition (PSAK/IFRS)", "ppt/FSA_Week3_PPT.pdf"),
    ("Week 4", "Analyzing Statement of Cash Flows (CFO/CFI/CFF & FCF)", "ppt/FSA_Week4_PPT.pdf"),
    ("Week 5", "Profitability Analysis I: Common-Size & 3-Step DuPont ROE", "ppt/FSA_Week5_PPT.pdf"),
    ("Week 6", "Profitability Analysis II & Solvency: Altman Z-Score", "ppt/FSA_Week6_PPT.pdf"),
    ("Week 7", "Accounting Quality, Red Flags & Earnings Management", "ppt/FSA_Week7_PPT.pdf"),
    ("Week 9", "Analyzing Financing Activities (Debt vs Equity, Bonds & Leases)", "ppt/FSA_Week9_PPT.pdf"),
    ("Week 10", "Analyzing Investing Activities & Intercorporate Investments", "ppt/FSA_Week10_PPT.pdf"),
    ("Week 12", "Operating Activities: Revenue, Operating Leverage (DOL) & Segments", "ppt/FSA_Week12_PPT.pdf"),
    ("Week 13", "Forecasting Financial Statements (Sales-Driven & Pro Forma)", "ppt/FSA_Week13_PPT.pdf"),
    ("Week 14", "Cost of Capital & Valuation (WACC, DCF, Residual Income, Multiples)", "ppt/FSA_Week14_PPT.pdf"),
]

ppt_data = []
for wk_code, wk_title, path in ppt_files:
    reader = pypdf.PdfReader(path)
    slides = []
    for idx, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        lines = [clean_str(l) for l in raw_text.split('\n') if clean_str(l)]
        header = lines[0] if lines else f"Slide {idx+1}"
        slides.append({
            "slide_num": idx + 1,
            "header": header,
            "full_text": raw_text
        })
    ppt_data.append({
        "week": wk_code,
        "title": wk_title,
        "path": path,
        "total_slides": len(slides),
        "slides": slides
    })

print(f"Parsed {len(ppt_data)} lecture presentations.")

# 2. Extract GoTo Specific Data from our Completed Assignments
# Milestone 1 (Assignment 3): Five Forces & Strategy
m1_doc = docx.Document("ASSIGNMENTS/ASSIGNMENT 3/Group4_Milestone1_GOTO.docx")
m1_paragraphs = [clean_str(p.text) for p in m1_doc.paragraphs if clean_str(p.text)]

# Milestone 2 (Assignment 7): Financial Ratios & DuPont
m2_wb = openpyxl.load_workbook("ASSIGNMENTS/ASSIGNMENT 7/Group4_Milestone2_GOTO.xlsx", data_only=True)
m2_sheets = {}
for sheetname in m2_wb.sheetnames:
    ws = m2_wb[sheetname]
    grid = []
    for r in range(1, min(ws.max_row+1, 60)):
        row_vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column+1, 15))]
        if any(v is not None for v in row_vals):
            grid.append([str(v) if v is not None else "" for v in row_vals])
    m2_sheets[sheetname] = grid

# Milestone 3 (Assignment 10): Accounting Quality, Non-recurring, Cash flow reconciliation
m3_doc = docx.Document("ASSIGNMENTS/ASSIGNMENT 10/Group4_Milestone3_GOTO.docx")
m3_paragraphs = [clean_str(p.text) for p in m3_doc.paragraphs if clean_str(p.text)]

# Week 12 Assignment (Assignment 11): Operating Leverage & Segments
w12_doc = docx.Document("ASSIGNMENTS/ASSIGNMENT 11/Group4_FSA_Week12_DOL_Segment_Completed.docx")
w12_paragraphs = [clean_str(p.text) for p in w12_doc.paragraphs if clean_str(p.text)]

# Milestone 4 (Assignment 13): 3-Year Pro Forma Forecast
m4_wb = openpyxl.load_workbook("ASSIGNMENTS/ASSIGNMENT 13/Group4_Milestone4_GOTO.xlsx", data_only=True)
m4_sheets = {}
for sheetname in m4_wb.sheetnames:
    ws = m4_wb[sheetname]
    grid = []
    for r in range(1, min(ws.max_row+1, 50)):
        row_vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column+1, 12))]
        if any(v is not None for v in row_vals):
            grid.append([str(v) if v is not None else "" for v in row_vals])
    m4_sheets[sheetname] = grid

# Assignment 14: Valuation Workbook
a14_wb = openpyxl.load_workbook("ASSIGNMENTS/ASSSIGNMENT 14/Group4_FSA_Valuation_Workbook_GOTO.xlsx", data_only=True)
a14_sheets = {}
for sheetname in a14_wb.sheetnames:
    ws = a14_wb[sheetname]
    grid = []
    for r in range(1, min(ws.max_row+1, 40)):
        row_vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column+1, 10))]
        if any(v is not None for v in row_vals):
            grid.append([str(v) if v is not None else "" for v in row_vals])
    a14_sheets[sheetname] = grid

# Assignment 15: Final Report (Comprehensive Synthesis)
a15_doc = docx.Document("ASSIGNMENTS/ASSSIGNMENT 15/Group4_FinalReport_GOTO.docx")
a15_paragraphs = [clean_str(p.text) for p in a15_doc.paragraphs if clean_str(p.text)]

compiled_dataset = {
    "lectures": ppt_data,
    "goto_analysis": {
        "milestone1_strategy": m1_paragraphs[:40],
        "milestone2_ratios": m2_sheets,
        "milestone3_accounting_quality": m3_paragraphs[:50],
        "week12_operating_leverage": w12_paragraphs[:40],
        "milestone4_proforma": m4_sheets,
        "assignment14_valuation": a14_sheets,
        "assignment15_final_report": a15_paragraphs[:60]
    }
}

os.makedirs("goto-fsa-study/src/data", exist_ok=True)
with open("goto-fsa-study/src/data/fsa_knowledgebase.json", "w", encoding="utf-8") as f:
    json.dump(compiled_dataset, f, ensure_ascii=False, indent=2)

print("Saved fsa_knowledgebase.json successfully! File size:", os.path.getsize("goto-fsa-study/src/data/fsa_knowledgebase.json"), "bytes")
