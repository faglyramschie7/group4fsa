import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import json
import pypdf

# Let us extract every single slide for Week 1 and Week 2 with high fidelity
def extract_slides(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    slides = []
    for idx, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        title = lines[0] if lines else f"Slide {idx+1}"
        subtitle = lines[1] if len(lines) > 1 else ""
        content = "\n".join(lines[2:]) if len(lines) > 2 else "\n".join(lines)
        slides.append({
            "slide_num": idx + 1,
            "header": title,
            "subtitle": subtitle,
            "raw_text": raw_text,
            "lines": lines
        })
    return slides

w1_slides = extract_slides("ppt/FSA_Week1_PPT.pdf")
w2_slides = extract_slides("ppt/FSA_Week2_PPT.pdf")

print(f"Extracted {len(w1_slides)} slides for W1 and {len(w2_slides)} slides for W2")
