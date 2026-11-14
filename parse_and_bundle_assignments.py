import docx
import openpyxl
import json
import os
import glob
import re

print("Extracting all completed assignments into a rich interactive dossier...")

def docx_to_structured(path):
    doc = docx.Document(path)
    sections = []
    current_sec = {"heading": "Overview", "paragraphs": [], "tables": []}
    
    for element in doc.element.body:
        if element.tag.endswith('p'):
            p = docx.text.paragraph.Paragraph(element, doc)
            text = p.text.strip()
            if not text:
                continue
            if p.style.name.startswith('Heading 1') or p.style.name.startswith('Heading 2') or (len(text) < 70 and text.endswith(':')):
                if current_sec["paragraphs"] or current_sec["tables"]:
                    sections.append(current_sec)
                current_sec = {"heading": text, "paragraphs": [], "tables": []}
            else:
                current_sec["paragraphs"].append(text)
        elif element.tag.endswith('tbl'):
            table = docx.table.Table(element, doc)
            grid = []
            for row in table.rows:
                row_data = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
                grid.append(row_data)
            current_sec["tables"].append(grid)
            
    if current_sec["paragraphs"] or current_sec["tables"]:
        sections.append(current_sec)
    return sections

def xlsx_to_structured(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    sheets = {}
    for name in wb.sheetnames:
        ws = wb[name]
        grid = []
        for r in range(1, min(ws.max_row+1, 50)):
            row_vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column+1, 15))]
            if any(v is not None for v in row_vals):
                formatted_vals = []
                for v in row_vals:
                    if v is None:
                        formatted_vals.append("")
                    elif isinstance(v, float):
                        formatted_vals.append(f"{v:,.2f}" if abs(v) < 10000 else f"{v:,.0f}")
                    else:
                        formatted_vals.append(str(v))
                grid.append(formatted_vals)
        sheets[name] = grid
    return sheets

assignments = [
    {
        "id": "m1",
        "code": "Milestone 1",
        "folder": "ASSIGNMENT 3",
        "title": "Business Strategy Analysis & Porter's Five Forces (GOTO)",
        "week": "Weeks 1–3",
        "summary": "Industry economics, market position, and Porter's Five Forces evaluation showing why GoTo lacks cost leadership and faces high rivalry.",
        "docx_file": "ASSIGNMENTS/ASSIGNMENT 3/Group4_Milestone1_GOTO.docx",
        "sections": docx_to_structured("ASSIGNMENTS/ASSIGNMENT 3/Group4_Milestone1_GOTO.docx")
    },
    {
        "id": "m2",
        "code": "Milestone 2",
        "folder": "ASSIGNMENT 7",
        "title": "Financial Ratio Package & 3-Step DuPont ROE Analysis",
        "week": "Weeks 4–6",
        "summary": "Comprehensive ratio package (Liquidity, Solvency, Efficiency, Profitability), DuPont ROE decomposition, and Altman Z''-score (-10.90).",
        "docx_file": "ASSIGNMENTS/ASSIGNMENT 7/Group4_Milestone2_GOTO.docx",
        "xlsx_file": "ASSIGNMENTS/ASSIGNMENT 7/Group4_Milestone2_GOTO.xlsx",
        "sections": docx_to_structured("ASSIGNMENTS/ASSIGNMENT 7/Group4_Milestone2_GOTO.docx"),
        "workbook": xlsx_to_structured("ASSIGNMENTS/ASSIGNMENT 7/Group4_Milestone2_GOTO.xlsx")
    },
    {
        "id": "m3",
        "code": "Milestone 3",
        "folder": "ASSIGNMENT 10",
        "title": "Accounting Quality, Cash Flow Forensic & Non-Recurring Items",
        "week": "Weeks 7–10",
        "summary": "Audit of Tokopedia deconsolidation, consumer loan-loss provisions, software capitalization, and proving negative Free Cash Flow.",
        "docx_file": "ASSIGNMENTS/ASSIGNMENT 10/Group4_Milestone3_GOTO.docx",
        "sections": docx_to_structured("ASSIGNMENTS/ASSIGNMENT 10/Group4_Milestone3_GOTO.docx")
    },
    {
        "id": "w12",
        "code": "Assignment 11",
        "folder": "ASSIGNMENT 11",
        "title": "Degree of Operating Leverage (DOL) & Segment Performance",
        "week": "Week 12",
        "summary": "Revenue recognition triggers, On-Demand vs Fintech segment dynamics, and proving why negative operating leverage crushes margins.",
        "docx_file": "ASSIGNMENTS/ASSIGNMENT 11/Group4_FSA_Week12_DOL_Segment_Completed.docx",
        "sections": docx_to_structured("ASSIGNMENTS/ASSIGNMENT 11/Group4_FSA_Week12_DOL_Segment_Completed.docx")
    },
    {
        "id": "m4",
        "code": "Milestone 4",
        "folder": "ASSIGNMENT 13",
        "title": "Three-Year Linked Pro Forma Forecasting Model (2026F–2028F)",
        "week": "Week 13",
        "summary": "Base Case, Optimistic, and Conservative scenarios showing GoTo operating below breakeven and burning cash down to Rp 968 bn.",
        "docx_file": "ASSIGNMENTS/ASSIGNMENT 13/Group4_Milestone4_GOTO.docx",
        "xlsx_file": "ASSIGNMENTS/ASSIGNMENT 13/Group4_Milestone4_GOTO.xlsx",
        "sections": docx_to_structured("ASSIGNMENTS/ASSIGNMENT 13/Group4_Milestone4_GOTO.docx"),
        "workbook": xlsx_to_structured("ASSIGNMENTS/ASSIGNMENT 13/Group4_Milestone4_GOTO.xlsx")
    },
    {
        "id": "a14",
        "code": "Assignment 14",
        "folder": "ASSSIGNMENT 14",
        "title": "Valuation Package: WACC, DCF, Residual Income & Multiples",
        "week": "Week 14",
        "summary": "CAPM Ke 8.45%, WACC 7.76%, DCF (-Rp 100.9), Residual Income (-Rp 75.1), Multiples (Rp 39.7), and reading the gap against Rp 25.00 market price.",
        "docx_file": "ASSIGNMENTS/ASSSIGNMENT 14/Group4_Assignment14_Valuation_Summary.docx",
        "xlsx_file": "ASSIGNMENTS/ASSSIGNMENT 14/Group4_FSA_Valuation_Workbook_GOTO.xlsx",
        "sections": docx_to_structured("ASSIGNMENTS/ASSSIGNMENT 14/Group4_Assignment14_Valuation_Summary.docx"),
        "workbook": xlsx_to_structured("ASSIGNMENTS/ASSSIGNMENT 14/Group4_FSA_Valuation_Workbook_GOTO.xlsx")
    },
    {
        "id": "a15",
        "code": "Assignment 15",
        "folder": "ASSSIGNMENT 15",
        "title": "Comprehensive Final Financial Statement Analysis Report",
        "week": "Week 15",
        "summary": "Complete term synthesis covering Steps 1 to 6, final valuation reconciliation, and formal SELL / AVOID recommendation for Public Equity Investors.",
        "docx_file": "ASSIGNMENTS/ASSSIGNMENT 15/Group4_FinalReport_GOTO.docx",
        "sections": docx_to_structured("ASSIGNMENTS/ASSSIGNMENT 15/Group4_FinalReport_GOTO.docx")
    }
]

with open("goto-fsa-study/src/data/all_assignments_bundle.json", "w", encoding="utf-8") as f:
    json.dump(assignments, f, ensure_ascii=False, indent=2)

print("Saved all_assignments_bundle.json successfully! Total assignments:", len(assignments))
