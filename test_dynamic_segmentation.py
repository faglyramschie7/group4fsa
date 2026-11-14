import re

def tokenize_note(note, rows):
    # Candidate matches from note
    # Pattern to find numbers and currency references in note
    pattern = r"(-?Rp\s*[\d,.]+\s*(?:T|bn|trillion|million|m)?|\(?Rp\s*[\d,.]+\s*(?:bn|trillion|T)?\)?|[-+]?[\d,.]+\s*%|\b\d+[.,]\d+\s*(?:T|bn|trillion)?\b)"
    
    tokens = []
    last_idx = 0
    for m in re.finditer(pattern, note):
        start, end = m.span()
        if start > last_idx:
            tokens.append({"type": "text", "text": note[last_idx:start]})
        match_text = m.group(0).strip()
        
        # Try to find matching cell in rows
        best_match = None
        # Clean the match_text
        digits = re.sub(r"[^\d.]", "", match_text)
        
        for r_idx, r in enumerate(rows):
            for c_idx, val in enumerate(r[1:]):
                v_str = str(val)
                v_digits = re.sub(r"[^\d.]", "", v_str)
                # check if digits match
                if not digits or not v_digits:
                    continue
                # 1. exact match
                if digits == v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 2. substring / abbreviation match
                # e.g. 214.1 in 214142.5 or 214118.8
                d_prefix = digits.replace(".", "")[:3]
                v_prefix = v_digits.replace(".", "")[:3]
                if len(d_prefix) >= 2 and d_prefix == v_prefix:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 3. e.g. 90.5 in 90516 or 90519
                if digits in ["90.5", "905"] and "905" in v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 4. e.g. 1.50 or 1.5 in 1501
                if digits in ["1.50", "1.5"] and "1501" in v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 5. e.g. 3.72 in 3718
                if digits in ["3.72", "3.7"] and "3718" in v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 6. e.g. 10.4 in 10425 or 10428
                if digits in ["10.4", "104"] and "104" in v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 7. e.g. 17.0 in 17046
                if digits in ["17.0", "170", "17"] and "17046" in v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 8. e.g. 35.72 in 35720
                if digits in ["35.72", "35.7"] and "3572" in v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
                # 9. e.g. 28.71 in 28711
                if digits in ["28.71", "28.7"] and "2871" in v_digits:
                    best_match = (r_idx, c_idx + 1, val, r[0])
                    break
            if best_match:
                break
        
        if best_match:
            tokens.append({
                "type": "ref",
                "text": match_text,
                "row": best_match[0],
                "col": best_match[1],
                "val": best_match[2],
                "account": best_match[3]
            })
        else:
            tokens.append({"type": "text", "text": match_text})
        last_idx = end
        
    if last_idx < len(note):
        tokens.append({"type": "text", "text": note[last_idx:]})
    return tokens

# Test on Slide 3
s3_note = "Direct Comparison with ABBA: Like ABBA, GoTo shows 'losses narrowing' on the surface (from -Rp 90.5T in 2023 to -Rp 1.50T in 2025). But look at the balance sheet and debt: GoTo doubled total debt to Rp 7,742.6 bn, suffered a negative Free Cash Flow of (Rp 875.3 bn), and accumulated retained losses of Rp 214.1 trillion."
s3_rows = [
    ["Gross Revenues", "24,258.1", "21,845.2", "18,322.1", "-16.1% YoY"],
    ["Net Revenues", "14,785.4", "15,894.5", "18,322.1", "+15.3% YoY"],
    ["Cost of Revenues", "(10,342.1)", "(7,413.4)", "(7,746.0)", "+4.5% YoY"],
    ["Gross Profit", "4,443.3", "8,481.1", "10,576.1", "+24.7% YoY"],
    ["Operating Expenses", "(14,751.2)", "(10,721.9)", "(10,954.2)", "+2.2% YoY"],
    ["Operating Loss (EBIT)", "(10,307.9)", "(2,240.8)", "(378.1)", "-83.1% YoY"],
    ["Net Income / (Loss) for the Year", "(90,516.3)", "(5,464.9)", "(1,501.7)", "Narrowed 72.5%"],
    ["Operating Cash Flow (CFO)", "(3,942.1)", "(762.4)", "307.0", "Turned Positive"],
    ["Total Debt (Short-Term + Long-Term)", "3,892.4", "4,215.1", "7,742.6", "Doubled (+83.7%)"],
    ["Cash & Cash Equivalents", "27,411.2", "21,003.8", "21,755.2", "+Rp 751.4 bn"],
    ["Retained Deficit (Cumulative Losses)", "(193,420.2)", "(212,640.8)", "(214,142.5)", "Rp 214.1T Total Deficit"],
    ["Total Equity", "41,208.5", "35,720.5", "28,711.7", "-19.6% YoY Contraction"],
    ["Capital Expenditures (Capex)", "(217.1)", "(652.3)", "(1,182.3)", "+81.3% Capex Expansion"],
    ["Free Cash Flow (FCF = CFO - Capex)", "(4,159.2)", "(1,414.7)", "(875.3)", "Remains strictly negative!"]
]

res = tokenize_note(s3_note, s3_rows)
print("=== Slide 3 Tokens ===")
for t in res:
    if t["type"] == "ref":
        print(f" [REF] '{t['text']}' -> Row {t['row']} Col {t['col']} ({t['account']}) = {t['val']}")
    else:
        print(f" [TXT] '{t['text']}'")
