import json
import re

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json") as f:
    modules = json.load(f)

def clean_num(s):
    # strip currency, parenthesis, commas
    return re.sub(r"[^\d.]", "", s)

for mod in modules:
    for slide in mod.get("slides", []):
        rep = slide.get("goto_report", {})
        if rep.get("content_type") == "table" and rep.get("analytical_note"):
            note = rep.get("analytical_note")
            rows = rep.get("table_rows", [])
            print(f"=== Slide {slide['slide_num']} ({mod['id']}) ===")
            print("Note:", note)
            # Find numbers in rows
            row_items = []
            for r_idx, r in enumerate(rows):
                name = r[0]
                for c_idx, val in enumerate(r[1:]):
                    c_clean = clean_num(str(val))
                    if c_clean and len(c_clean) >= 2:
                        row_items.append((r_idx, c_idx + 1, str(val), name))
            
            # Find matches in note
            for r_idx, c_idx, val, name in row_items:
                # check if val or portion is in note
                # e.g. 7,742.6 or 875.3 or 214.1 or 90.5
                clean_v = clean_num(val)
                # check various patterns
                matches = []
                # try exact or rounded patterns
                patterns = [val, val.replace(",", ""), val.strip("()")]
                if "." in clean_v:
                    patterns.append(clean_v)
                # check if clean_v[:3] like 214 or 905
                if "214" in clean_v:
                    patterns.append("214")
                if "905" in clean_v:
                    patterns.append("90.5")
                if "1501" in clean_v:
                    patterns.append("1.50")
                    patterns.append("1.5")
                if "35720" in clean_v:
                    patterns.append("35.72")
                    patterns.append("35.7")
                if "28711" in clean_v:
                    patterns.append("28.71")
                    patterns.append("28.7")
                
                for p in patterns:
                    if p in note:
                        matches.append(p)
                        break
                if matches:
                    print(f"  Row {r_idx} Col {c_idx} '{name}': val='{val}' matched '{matches[0]}'")
