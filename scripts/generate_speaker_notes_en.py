#!/usr/bin/env python3
"""Generate Group4_GOTO_Speaker_Notes_EN.docx with full coverage of Slides 1-20 and every popup item."""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_PATH = "ASSIGNMENTS/FINAL REPORT/Group4_GOTO_Speaker_Notes_EN.docx"
MEDIA_DIR = "outputs/speaker-notes-screenshots"

NAVY = RGBColor(0x0F, 0x29, 0x42)
EMERALD = RGBColor(0x0F, 0x76, 0x6E)
SLATE = RGBColor(0x33, 0x41, 0x55)
MUTED = RGBColor(0x64, 0x74, 0x8B)
DARK = RGBColor(0x1E, 0x29, 0x3B)

HEX_NAVY = "0F2942"
HEX_EMERALD = "0F766E"
HEX_SCRIPT_BG = "ECFDF5"
HEX_SCRIPT_BORDER = "10B981"
HEX_GUIDE_BG = "EFF6FF"
HEX_GUIDE_BORDER = "3B82F6"
HEX_TBL_HDR = "0F2942"
HEX_TBL_ALT = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_APX_HDR = "115E59"


def set_cell_shading(cell, fill_hex: str):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=90, bottom=90, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for name, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{name}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color=HEX_BORDER, sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f"</w:tblBorders>"
    )
    tblPr.append(borders)


def set_callout_borders(cell, border_hex: str):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f"</w:tcBorders>"
    )
    tcPr.append(borders)


def add_run(p, text, bold=False, italic=False, size=10, color=DARK):
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.name = "Calibri"
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return r


def add_callout_box(doc, title, lines, fill_hex=HEX_SCRIPT_BG, border_hex=HEX_SCRIPT_BORDER, title_color=EMERALD):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_shading(cell, fill_hex)
    set_cell_margins(cell, top=110, bottom=110, left=160, right=160)
    set_callout_borders(cell, border_hex)

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(4)
    add_run(p0, title, bold=True, size=9.5, color=title_color)

    for idx, line in enumerate(lines):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3 if idx < len(lines) - 1 else 0)
        p.paragraph_format.line_spacing = 1.15
        add_run(p, line, size=10, color=DARK)

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)


def add_section_banner(doc, title_text, bg_hex=HEX_NAVY):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_shading(cell, bg_hex)
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.keep_with_next = True
    add_run(p, title_text, bold=True, size=11.5, color=RGBColor(0xFF, 0xFF, 0xFF))


def add_styled_table(doc, headers, rows, col_widths, hdr_hex=HEX_TBL_HDR):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl)

    # Header row
    hdr_cells = tbl.rows[0].cells
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))
    for i, h in enumerate(headers):
        c = hdr_cells[i]
        c.width = Inches(col_widths[i])
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(c, hdr_hex)
        set_cell_margins(c, top=80, bottom=80, left=110, right=110)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        add_run(p, h, bold=True, size=9, color=RGBColor(0xFF, 0xFF, 0xFF))

    for r_idx, row in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        r_trPr = tbl.rows[r_idx + 1]._tr.get_or_add_trPr()
        r_trPr.append(OxmlElement("w:cantSplit"))
        for c_idx, val in enumerate(row):
            c = row_cells[c_idx]
            c.width = Inches(col_widths[c_idx])
            c.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            if r_idx % 2 == 1:
                set_cell_shading(c, HEX_TBL_ALT)
            set_cell_margins(c, top=70, bottom=70, left=110, right=110)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            is_first = c_idx == 0
            add_run(p, val, bold=is_first, size=9, color=NAVY if is_first else DARK)

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)


def add_figure(doc, img_filename, caption_text, width_in=6.6):
    img_path = os.path.join(MEDIA_DIR, img_filename)
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Missing media file: {img_path}")
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(img_path, width=Inches(width_in))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(8)
    add_run(p_cap, caption_text, italic=True, size=9, color=MUTED)


def add_slide_block(doc, slide_data, fig_counter, is_appendix=False):
    header_bg = HEX_APX_HDR if is_appendix else HEX_NAVY
    add_section_banner(doc, slide_data["header"], bg_hex=header_bg)

    # Main goal
    p_goal = doc.add_paragraph()
    p_goal.paragraph_format.space_before = Pt(5)
    p_goal.paragraph_format.space_after = Pt(4)
    add_run(p_goal, "Main Goal: ", bold=True, size=10, color=NAVY)
    add_run(p_goal, slide_data["goal"], size=10, color=DARK)

    # Script callout
    script_title = (
        "WHAT TO SAY IF ASKED IN Q&A (EASY ENGLISH SCRIPT)"
        if is_appendix
        else "WHAT TO SAY (EASY ENGLISH SCRIPT)"
    )
    add_callout_box(doc, script_title, [slide_data["script"]])

    # Key numbers / schedules
    p_kn = doc.add_paragraph()
    p_kn.paragraph_format.space_before = Pt(2)
    p_kn.paragraph_format.space_after = Pt(2)
    p_kn.paragraph_format.keep_with_next = True
    add_run(
        p_kn,
        "Key Schedules & Figures on This Slide:" if is_appendix else "Key Numbers to Point At:",
        bold=True,
        size=10,
        color=NAVY,
    )
    for b in slide_data["bullets"]:
        pb = doc.add_paragraph(style="List Bullet")
        pb.paragraph_format.space_before = Pt(0)
        pb.paragraph_format.space_after = Pt(2)
        pb.paragraph_format.line_spacing = 1.12
        add_run(pb, b, size=9.5, color=DARK)

    # Slide screenshot right below Key Numbers
    if slide_data.get("slide_fig"):
        sf_file, sf_cap = slide_data["slide_fig"]
        n = fig_counter[0]
        fig_counter[0] += 1
        add_figure(doc, sf_file, f"Figure {n}: {sf_cap}", width_in=6.2)

    # Popup Walkthrough table (EVERY item inside the popup from top to bottom)
    p_pop = doc.add_paragraph()
    p_pop.paragraph_format.space_before = Pt(5)
    p_pop.paragraph_format.space_after = Pt(3)
    p_pop.paragraph_format.keep_with_next = True
    add_run(
        p_pop,
        "Popup Walkthrough — Every Item Inside the Popup (Top to Bottom):",
        bold=True,
        size=10,
        color=EMERALD,
    )
    add_styled_table(
        doc,
        ["Popup Element / Tab", "What It Shows & How to Explain It on Stage"],
        slide_data["popup_rows"],
        [1.95, 5.05],
        hdr_hex=HEX_APX_HDR if is_appendix else HEX_EMERALD,
    )

    for pf_file, pf_cap in slide_data.get("popup_figs", []):
        n = fig_counter[0]
        fig_counter[0] += 1
        add_figure(doc, pf_file, f"Figure {n}: {pf_cap}", width_in=6.2)


MAIN_SLIDES = [
    {
        "header": "SLIDE 1: GoTo Equity Analysis (Opening)  [0.75 min  |  Ref: None]",
        "goal": "Introduce the company, our target investor, the Rp 25 reference price, and our 6-part roadmap cleanly in ~45 seconds.",
        "script": (
            '"Good morning everyone. We are Group 4, and today we are presenting our equity analysis of PT GoTo Gojek Tokopedia Tbk, '
            'ticker GOTO on the Indonesia Stock Exchange. Today, GoTo runs two main businesses: Gojek for rides and food delivery, '
            'and GoTo Financial for GoPay payments and consumer lending. GoTo also still holds a 24.99% minority stake in Tokopedia '
            'after TikTok took control in early 2024. Our analysis is written for a short-term public equity investor with a 12-month horizon, '
            'using Rp 25 per share as our benchmark price. We will walk through the business model, profitability, cash flow quality, '
            '3-year forecast, and valuation, and then end with our final recommendation."'
        ),
        "bullets": [
            "2 core businesses: Gojek (On-Demand) and GoTo Financial (GoPay payments & consumer lending)",
            "24.99% passive associate stake in Tokopedia (deconsolidated in early 2024 after TikTok took control)",
            "Target user: Short-term public equity investor (12-month horizon) at Rp 25 per share benchmark",
            "Scope: 2023–2025 actuals and 2026F–2028F forecasts across 14 main slides + Appendices A1–A6",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "On stage, keep Slide 1 brisk (~45s) with no popup needed. However, two cover pills ARE clickable if clicked: "
                "\"Gojek · GoTo Financial · 24.99% Tokopedia\" and \"ASSIGNMENT REFERENCE PRICE: Rp 25 per share\".",
            ],
            [
                "Popup Header & Footer",
                "Header shows \"SLIDE 1 · Opening\", the clicked item title, and (at the bottom) the Terms glossary strip (e.g., EBIT). "
                "No Appendix jump button is shown on Slide 1.",
            ],
            [
                "Tab 1: Charts & Data",
                "Renders \"FY2025 Segment Operating Profit / Loss (Note 29)\" diverging bars: On-Demand (Gojek) +888.6B, E-Commerce Fee +572.2B, "
                "Fintech (GoPay) −396.6B, Unalloc. Corporate −1,442.5B, Consolidated EBIT −378.3B.",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Not active on Slide 1.",
            ],
            [
                "Tab 3 & Tab 4 (Calc / Proof)",
                "Not shown on Slide 1 (0 slide calc rows and 0 supporting schedules).",
            ],
            [
                "Tab 5: Workbook & Lectures",
                "Active with 4 traceable links (3 lecture slides + 1 assignment workbook reference) if you need to show Week 1–2 scope.",
            ],
            [
                "Show Analysis (Top Right)",
                "Opens the right-hand \"Executive Takeaway & Analysis\" panel explaining GoTo's scope, Rp 25 reference price, and presentation flow.",
            ],
        ],
    },
    {
        "header": "SLIDE 2: Business Model  [1.0 min  |  Ref: Appendix A1]",
        "goal": "Show where GoTo makes money today after leaving Tokopedia: Gojek is the biggest profit engine, while GoPay is the fastest grower.",
        "script": (
            '"Let us look at how GoTo makes money today. In 2025, total net revenue grew 15.3% to Rp 18.3 trillion. First, Gojek (rides and food delivery) '
            'is still the biggest engine at Rp 12.36 trillion, which is about two-thirds of total revenue. Even better, Gojek segment operating profit '
            'jumped almost 13 times, from Rp 69 billion in 2024 to Rp 889 billion in 2025, thanks to lower promos and over 50% cloud cost savings. '
            'Second, GoTo Financial (GoPay payments and consumer lending) is the fastest-growing segment, surging 74% to Rp 5.19 trillion. '
            'Finally, GoTo still collects about Rp 820 billion in e-commerce service fees from Tokopedia. However, once we include Rp 1.44 trillion '
            'of corporate overhead, GoTo as a whole still ended 2025 with a small operating loss of Rp 378 billion."'
        ),
        "bullets": [
            "Total FY2025 Net Revenue: Rp 18,322.1B / Rp 18.32T (+15.27% YoY)",
            "Gojek (On-Demand): Rp 12,361B revenue (+13.8% YoY); Segment EBIT jumped 13x from +Rp 69.4B to +Rp 888.6B",
            "GoTo Financial (GoPay): Rp 5,191B revenue (+74.1% YoY, 90.96% of group growth); Segment EBIT loss narrowed to −Rp 396.6B",
            "Tokopedia Service Fee: Rp 820B revenue (+Rp 572.2B segment EBIT); less Rp 1,442.5B corporate overhead = −Rp 378.3B Consolidated EBIT",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click any of the 3 business rows (Gojek, GoTo Financial, Tokopedia) or the right-hand analysis cards.",
            ],
            [
                "Tab 1 Top Chart (Gojek Clicked)",
                "If you click Gojek, the top chart shows \"Gojek Segment EBIT Bridge: FY24 → FY25 (Note 29)\": FY2024 EBIT (+69.4B) + 3P Gross Revenue "
                "(+995.8B) + Incentive Cut (−15.9%, +504.2B) + Inter-Segment Net (+67.8B) + Corp. Alloc. Cut (+32.5B) − 3P Cost Growth (−781.1B) = FY2025 EBIT (+888.6B).",
            ],
            [
                "Tab 1 Top Chart (GoPay / Tokopedia)",
                "If you click GoTo Financial or Tokopedia, the top chart switches to \"FY2025 Segment Operating Profit / Loss (Note 29)\": "
                "On-Demand (+888.6B), E-Commerce Fee (+572.2B), Fintech (−396.6B), Unalloc. Corporate (−1,442.5B), Consolidated EBIT (−378.3B).",
            ],
            [
                "Tab 1 YoY Trajectory Cards (Below)",
                "4 vertical column cards (with an \"Exit\" divider after 2023*): (1) On-Demand (Gojek) EBIT (+Rp 69.4B → +Rp 888.6B, +1,180% YoY), "
                "(2) FinTech (GoPay) Revenue (Rp 2.98T → Rp 5.19T, +74.05% YoY), (3) Consolidated Net Revenue (Rp 14.79T → Rp 15.89T → Rp 18.32T, +15.27% YoY), "
                "and (4) Consolidated EBIT (−Rp 10.28T → −Rp 2.24T → −Rp 378B, +83.1% YoY).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Compares 2023 Pre-Exit (With Tokopedia) vs. 2025 Post-Exit across 4 cards: Net Revenue (Rp 14.79T → Rp 18.32T), Cash OpEx (117.01% → 55.70%, "
                "−6,131 bps), EBIT (−Rp 10.28T → −Rp 0.38T), and Consolidated Net Income (−Rp 90.52T ex-Rp 78.8T goodwill → −Rp 1.50T).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows the clicked segment formula (e.g., ODS Net Revenue = Rp 15,030.99B Gross − Rp 2,669.74B Incentives = Rp 12,361.26B), "
                "step-by-step tie-out to Rp 18,322.12B, and the Slide Calculation Table (Consolidated Revenue).",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Shows clickable Audited Proof image (2025 Annual Report p. 468 Note 29 Segment Operations — click to zoom) plus collapsible "
                "Supporting Schedule: \"Revenue bridge to consolidated GoTo revenue\" (6 rows).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 7 traces (5 lectures + 2 assignments). Top-right \"Show Analysis\" explains segment economics; \"Appendix A1 ↗\" jumps to Slide 15.",
            ],
        ],
    },
    {
        "header": "SLIDE 3: Industry and Competition  [1.5 min  |  Ref: Appendix A1]",
        "goal": "Prove with real numbers that intense rivalry limits GoTo's pricing power, while rapid GoPay lending expansion brings rising credit risk.",
        "script": (
            '"Next, we tested Porter Five Forces against GoTo actual financial numbers. The biggest pressure on GoTo is Competitive Rivalry, rated HIGH. '
            'In Indonesia, GoFood holds 31% share behind GrabFood at 46%, while defending against ShopeeFood at 23%. Ride-hailing competes with Maxim '
            'and inDrive, and GoPay competes with ShopeePay, DANA, and OVO. Because Indonesian users can switch apps for free, GoTo has very little pricing power. '
            'We can see this directly in the income statement. In 2025, GoTo still had to spend Rp 3.09 trillion on sales and marketing and Rp 2.15 trillion '
            'on product development just to defend market share. At the same time, GoPay fast growth brings a new risk: consumer loans jumped 72.6% '
            'to Rp 2.73 trillion, and bad-loan provisions more than doubled by 135% to Rp 408 billion."'
        ),
        "bullets": [
            "Five Forces Ratings: Rivalry = HIGH; Buyers & Substitutes = MEDIUM; New Entrants = LOW–MODERATE; Suppliers = LOW",
            "Food Delivery Market Share: GrabFood 46% vs. GoFood 31% vs. ShopeeFood 23%",
            "2025 Competitive Spending: Sales & Marketing Rp 3.09T (16.9% of revenue) | Product Dev Rp 2.15T (11.7%) | Expensed Incentives Rp 1.08T",
            "GoPay Lending Risk: Net consumer loans +72.6% YoY (Rp 1.58T → Rp 2.73T) | Credit-loss provisions +134.9% (Rp 174B → Rp 408B)",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click any of the 5 Porter's Five Forces table rows, the \"Spending to compete\" chart, the \"Credit-loss provisions\" chart, "
                "or any right-hand analysis point.",
            ],
            [
                "Tab 1 Top Chart",
                "\"Competitive Rivalry Cost & Credit Provision Burden (FY2025, Rp billion)\" horizontal bars: Sales & Marketing (Rp 3,090B), "
                "Product Development (Rp 2,152B), Expensed Incentives inside S&M (Rp 1,077B), 2024 Loan Provisions (Rp 174B), and 2025 Provisions "
                "(Rp 408B, highlighted red +134.9% YoY).",
            ],
            [
                "Tab 1 YoY Trajectory Cards (Below)",
                "2 vertical cards: (1) Credit-Loss Provisions (Note 7): Rp 173.6B (2024) → Rp 407.7B (2025, +134.9% YoY, reaching 12.99% of gross loans); "
                "(2) Cash OpEx / Revenue: 117.0% (2023*) → 62.78% (2024) → 55.70% (2025, −708 bps YoY).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Not active on Slide 3.",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows the clicked item formula (e.g., Provision Growth = (407.684 / 173.552 − 1) = +134.9%, rounded 134%) plus Slide Calculation Table.",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Displays Audited Proof screenshot (Note 7 lending & credit-loss allowance or Note 26 operating expenses) with click-to-enlarge lightbox.",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 9 traces (7 lectures + 2 assignments). Top-right \"Show Analysis\" gives full Porter force & lending commentary; "
                "\"Appendix A1 ↗\" jumps to Slide 15 (which holds the full Note 35 & Five Forces schedule).",
            ],
        ],
    },
    {
        "header": "SLIDE 4: Profitability and DuPont  [1.75 min  |  Ref: Appendix A2]",
        "goal": "Show that GoTo improved sharply from 2023 to 2025, but negative net profit margin still keeps ROE negative compared to Grab.",
        "script": (
            '"Now let us look at profitability and our DuPont breakdown. The good news is clear: GoTo operating loss narrowed sharply from Rp 10.28 trillion '
            'in 2023 down to just Rp 378 billion in 2025, which is a -2.06% operating margin. Total net loss also shrank to Rp 1.50 trillion, '
            'or a -8.20% net profit margin. Using the 3-step DuPont formula, Net Margin (-8.20%) times Asset Turnover (0.40x) times Equity Multiplier (1.59x) '
            'gives a Consolidated Return on Equity (ROE) of -5.23%, or -3.73% on parent equity. Here is the key comparison with Grab: GoTo actually beats '
            'Grab on Asset Turnover (0.40x vs. Grab 0.28x). The only reason GoTo ROE is negative while Grab is positive (+2.96%) is that GoTo net profit margin '
            'is still below zero."'
        ),
        "bullets": [
            "Operating Loss (EBIT): −Rp 10.28T (2023) → −Rp 2.24T (2024) → −Rp 378B (2025, −2.06% operating margin)",
            "Net Loss & Margin: −Rp 90.52T (2023, with Rp 78.8T goodwill write-off) → −Rp 5.47T (2024) → −Rp 1.50T (2025, −8.20% net margin)",
            "DuPont FY2025 (Restated): −8.20% Net Margin × 0.4004x Asset Turnover × 1.5937x Equity Multiplier = −5.23% Consol. ROE (−3.73% Parent ROE)",
            "Peer Benchmark: Grab FY2025 ROE = +2.96% (+5.93% net margin, 0.28x asset turnover) vs. GoTo Cost of Equity (Ke) hurdle of 8.45%",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Toggle the top Switcher Bar between \"Original Deck\" (2023–2025 summary) and \"Final Report (Restated)\" (adds 2024 Note 7 Rp 1.58T asset fix, "
                "showing AT 0.37x, EM 1.42x, Gojek +Rp 888.6B EBIT, and YoY 24→25 deltas). Click any table row, loss chart, or right-hand card.",
            ],
            [
                "Tab 1 Top Chart",
                "\"DuPont ROE Trajectory (2023–2025) vs. Grab Peer\" diverging bars: 2024 Post-Exit ROE (−17.97%), 2025 Consol. ROE (−5.23%), "
                "2025 Parent ROE (−3.73%), Grab FY2025 Cons. (+2.96%), Grab FY2025 Parent (+3.98%), and GoTo Cost of Equity Ke (8.45% Hurdle).",
            ],
            [
                "Tab 1 YoY Trajectory Cards (Below)",
                "4 vertical column cards (with 2023* Exit divider): (1) Operating Margin EBIT % (−69.5% → −14.10% → −2.06%, +1,204 bps YoY), "
                "(2) Net Profit Margin (−612.2% → −34.38% → −8.20%, +2,618 bps YoY), (3) Total Asset Turnover (0.27x → 0.37x → 0.40x, +8.8% YoY), "
                "and (4) Cons. ROE vs Grab +2.96% (−253.4% → −17.97% → −5.23%, +1,274 bps YoY).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Compares 2023 Pre-Exit vs. 2025 Post-Exit across 4 cards: Gross Profit Margin (65.55% → 57.72%), Operating Margin (−69.52% → −2.06%), "
                "Total Asset Turnover (0.273x → 0.400x), and Consolidated ROE (−253.4% → −5.23% vs. Parent −3.73%).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows the clicked metric formula plus 12 Slide Calculation rows (top 3 shown + \"View more (+9 rows)\" for 3-factor & 5-factor DuPont, ROA, Tax/Interest Burden).",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Audited Income Statement proof image + 2 collapsible schedules: \"Consolidated Historical & Pro Forma Financial Summary (Rp bn)\" "
                "(11 rows) and \"2025 DuPont\" (4 rows).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 9 traces (7 lectures + 2 assignments). \"Show Analysis\" covers profitability & peer ROE gaps; \"Appendix A2 ↗\" jumps to Slide 16.",
            ],
        ],
    },
    {
        "header": "SLIDE 5: Liquidity and Z-Score  [1.5 min  |  Ref: Appendix A3]",
        "goal": "Prove GoTo is NOT about to go bankrupt (strong Rp 21.76T cash cushion), even though the Altman Z-Score looks scary from sunk 2023 losses.",
        "script": (
            '"Is GoTo in danger of running out of cash? The short answer is no. GoTo sits on Rp 21.76 trillion in cash, giving it a strong Current Ratio '
            'of 2.73x and Rp 18.41 trillion in positive working capital. After adding back all short-term loans and lease obligations, total debt-to-equity '
            'is manageable at 26.97%. Now, why does the Altman Z-Score read -4.72, which sits in the distress zone below 1.81? Look at the five components: '
            'Working Capital (X1) and Solvency (X4) are both positive. The entire negative pull comes from X2 (Accumulated Deficit of -Rp 215.3 trillion), '
            'which comes from sunk 2023 goodwill write-offs on Tokopedia—not a cash crisis today."'
        ),
        "bullets": [
            "Cash & Liquidity: Rp 21.76T cash | Current Ratio 2.73x (2024 restated from 2.46x to 2.62x via Note 7) | Working Capital Rp 18.41T",
            "Working Capital Efficiency (Note 6): Trade DSO 10.56d (2024) → 10.90d (2025) | DPO 59.1d | Negative CCC −47.5 days",
            "Solvency & TIE (Notes 19–20 & 27b): Full Debt/Equity 26.97% (0.27x; Rp 7.74T debt+leases) | TIE −0.71x (−Rp 378B EBIT / Rp 535B interest)",
            "Altman Z-Score: −4.72 (Book X4 = 1.68x) / −4.80 (Market Rp 25 X4 = 1.56x), driven by X2 (−6.59 weighted) from sunk 2023 write-offs",
        ],
        "popup_rows": [
            [
                "Two Different Popups on Slide 5",
                "Slide 5 has TWO distinct popup layouts depending on what you click: (A) clicking \"Current ratio\" / \"Liquidity & Working Capital\" or "
                "\"Interest coverage (TIE)\" / \"Leverage\" opens the Balance-Sheet Ratio Cards popup; (B) clicking \"Week 6 Z-score\" opens the Z-Score breakdown.",
            ],
            [
                "Tab 1 — View A (Click Current Ratio / TIE)",
                "Shows 4 vertical column charts directly in the top card AND activates the \"Previous Report (With 2023)\" vs. \"Current Report (Post-Exit)\" toggle: "
                "(1) Current Ratio (Prior: 2.62x / 2.46x red / 2.73x → Restated: 2.62x / 2.73x), (2) Debt / Equity (Prior: 9.69% / 12.57% → Restated: 15.85% / 26.97%), "
                "(3) Trade DSO (Prior: 46.88d spike → Restated: 10.56d / 10.90d), and (4) Times Interest Earned (−4.54x → −0.71x live via Note 27b).",
            ],
            [
                "Tab 1 — View B (Click Week 6 Z-score)",
                "Top chart shows \"Altman Z-Score Weighted Factor Breakdown (FY2025)\" diverging bars: 1.2 × X1 (+0.48), 1.4 × X2 (−6.59 red), "
                "3.3 × X3 (−0.03), 0.6 × X4 (+1.01), 1.0 × X5 (+0.40), Total Z = −4.72 / −4.80. Below it sits the 4-card YoY Liquidity & Leverage grid (2023*–2025).",
            ],
            [
                "Tab 2: Prior vs. Restated",
                "Side-by-side comparison of Prior Deck vs. Final Report fixes: 2024 Current Ratio (2.46x → 2.62x), 2024 Trade DSO (46.88d → 10.56d), "
                "2024 Debt/Equity (12.57% → 15.85%), and TIE (N/M → −0.71x in 2025).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Displays the clicked ratio formula plus all 16 Slide Calculation rows (top 3 + \"View more (+13 rows)\" covering CR, QR, WC, D/E, TIE, DSO/DIO/DPO/CCC, X1–X5, Z-Score).",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Audited Balance Sheet / Note 20 / Accumulated Deficit proof image + collapsible \"Completed Week 6 five-factor calculation\" table (5 rows).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 9 traces (7 lectures + 2 assignments). \"Show Analysis\" explains X4 sensitivity; \"Appendix A3 ↗\" jumps to Slide 17.",
            ],
        ],
        "figure": ("image2.png", "Figure 2: Slide 5 Popup (\"Current ratio\") showing clean vertical column charts for each post-exit balance-sheet ratio."),
    },
    {
        "header": "SLIDE 6: Cash Flow and Accounting Quality  [2.0 min  |  Ref: Appendix A3]",
        "goal": "Explain why cash flow quality is still weak (FCF is −Rp 875B) and highlight the 3 main accounting & footnote red flags.",
        "script": (
            '"Moving to Cash Flow and Accounting Quality, the headline is that positive operating cash flow does not yet fund investment. '
            'In 2025, Operating Cash Flow turned slightly positive at +Rp 307 billion, even after absorbing Rp 2.02 trillion for GoPay consumer lending. '
            'However, GoTo spent Rp 1.18 trillion on CapEx, leaving negative Free Cash Flow of -Rp 875 billion—meaning operations only cover 26% of CapEx. '
            'We also flagged three accounting risks: first, Tokopedia (Rp 7.43T) and Bank Jago (Rp 2.89T) make up 22.6% of total assets, so a 20% haircut '
            'would wipe out Rp 1.82 trillion (6.3%) of equity; second, Rp 1.08T of customer promos sit in marketing expense and related-party revenue is 7.13%; '
            'third, GoPay loan-loss reserves surged 135% while stripping out Rp 5.46 trillion of Tokopedia intangibles cleans up 2024 CapEx from 41.0% to 6.63%."'
        ),
        "bullets": [
            "FY2025 CFO: +Rp 307B (after −Rp 2.02T lending outflow) | Cash CapEx: −Rp 1,182B → FCF: −Rp 875B (CFO covers only 25.97% of CapEx)",
            "Accrual Ratio: −11.21% (2024) → −3.95% (2025 reported); −3.69% → −1.94% (adjusted recurring ex-one-offs)",
            "3 Accounting Red Flags: (1) Tokopedia Rp 7.43T + Bank Jago Rp 2.89T = 22.57% of assets (20% haircut = −Rp 1.82T / −6.34% equity); "
            "(2) Rp 1.08T expensed incentives & 7.13% related-party revenue; (3) Note 7 provisions +134.9% (+500 bps loss = −Rp 136.5B)",
            "2024 CapEx Cleanup (Note 12): Removing Rp 5,465B of deconsolidated Tokopedia intangibles drops 2024 CapEx from 41.01% to 6.63%",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click any of the 3 visual rows (\"Operating cash flow\", \"Cash capex\", \"Free cash flow\") or the 3 right-hand Risk cards (in Restated mode, "
                "these explicitly list Risk 1: Tokopedia & Jago, Risk 2: Promo Costs & Related-Party Fees, Risk 3: Rising GoPay Loan Losses).",
            ],
            [
                "Tab 1 Top Chart",
                "\"FY2025 Free Cash Flow Bridge & CapEx Normalization\" diverging bars: FY2025 Operating CF (+307.0B), FY2025 Cash CapEx (−1,182.4B), "
                "FY2025 Free Cash Flow (−875.3B red), Time Deposit Maturities (+1,386.5B), and Core CFI Ex-Deposits (−867.4B).",
            ],
            [
                "Tab 1 YoY Trajectory Cards (Below)",
                "4 vertical column cards (with 2023* Exit divider): (1) Operating Cash Flow (−Rp 4.33T → −Rp 622.1B → +Rp 307.0B), "
                "(2) Continuing CapEx / Rev (1.49% → 6.63% → 6.45%, showing the clean post-Note 12 trend), (3) Reported Accrual Ratio (−159.3% → −11.21% → −3.95%), "
                "and (4) Adj. Recurring Accrual (−13.73% → −3.69% → −1.94%).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "\"Cash Flow & CapEx Normalization: Distorted vs. Continuing\": Cash CapEx % (41.01% → 6.45%; cont. 2024 = 6.63%), "
                "Operating Cash Flow (−Rp 622.1B → +Rp 307.0B), Free Cash Flow (−Rp 7,141B → −Rp 875.3B), Reported Accrual Ratio (−11.21% → −3.95%).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows the clicked risk/cash-flow formula plus 6 Slide Calculation rows (top 3 + \"View more (+3 rows)\": FCF, Capex Coverage, Accrual Ratio, "
                "Associates/Assets, Related-Party Share, 20% Asset Haircut Sensitivity).",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Audited Cash Flow Statement p. 21 proof image + collapsible \"Milestone 3 accounting and footnote findings\" schedule (6 rows).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 10 traces (8 lectures + 2 assignments). Top-right \"Show Analysis\" panel walks through the accrual & impairment math; "
                "\"Appendix A3 ↗\" jumps to Slide 17.",
            ],
        ],
        "figure": ("image3.png", "Figure 3: Slide 6 Popup (\"Operating cash flow\") showing the FCF Bridge, YoY cards, and collapsible Executive Takeaway panel on the right."),
    },
    {
        "header": "SLIDE 7: Forecast Assumptions  [1.75 min  |  Ref: Appendix A4]",
        "goal": "Explain our 3 scenarios and demonstrate how quarantining 2023 Tokopedia costs and 2024 intangible transfers cleans up the Base Case.",
        "script": (
            '"Now let us look at how we forecast the next three years. Here is the most important restatement in our Final Report. In our earlier draft, '
            'we mechanically averaged 2023 with 2024 and 2025. That dragged 2023 pre-Tokopedia OpEx of 117% into the Base Case (78.5% OpEx) and included '
            'one-time Tokopedia intangible transfers inside 2024 CapEx (16.3% average). Once we anchor the Base Case strictly on the real post-Tokopedia '
            'Gojek + GoPay business (2024 to 2025), Base revenue growth becomes 15.27%, COGS is 42.28%, Cash OpEx drops to 55.70%, and continuing CapEx is 6.45%. '
            'Our Optimistic Case uses GoTo interim 1H 2026 cost efficiency (18.0% growth, 38.1% COGS, 51.2% OpEx), while Conservative uses the 2024 transition floor (7.5% growth, 62.8% OpEx)."'
        ),
        "bullets": [
            "Original Deck (3-Yr Avg with 2023): 11.4% growth | 41.1% COGS | 78.5% OpEx | 16.3% CapEx",
            "Final Report Base (Post-Exit 2024→2025): 15.27% growth | 42.28% COGS (57.72% Gross Margin) | 55.70% Cash OpEx (+202 bps spread) | 6.45% CapEx",
            "Optimistic (1H 2026 Efficiency): 18.00% growth | 38.10% COGS (61.90% GM) | 51.20% Cash OpEx | 6.45% (slide) / 5.50% (Table 11 CapEx)",
            "Conservative (2024 Transition Floor): 7.50% growth | 46.64% COGS (53.36% GM) | 62.78% Cash OpEx | 6.63% CapEx | 10.25% borrowing rate",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click any assumption row (e.g., \"COGS / revenue\", \"Cash OpEx / revenue\", \"Revenue growth\", \"CapEx / revenue\") or the 3 right-hand cards. "
                "Top Switcher Bar toggles the slide table between Original Deck (3-yr avg) and Final Report (Post-Exit).",
            ],
            [
                "Tab 1 Section 1 (Top Horizontal Chart)",
                "Has an in-chart toggle: \"Previous Report (With 2023)\" (11.40% growth, 41.10% COGS, 78.50% OpEx red, 16.30% CapEx red) vs. "
                "\"Current Report (Post-Exit)\" (15.27% growth, 42.28% COGS, 55.70% OpEx, 6.45% CapEx). Stays synced with the slide switcher!",
            ],
            [
                "Tab 1 Section 2 (Pro Forma Outcomes)",
                "\"Pro Forma Key Financial Statement Outcomes (2025A → 2028F)\" shows 4 vertical column charts directly below the top chart: "
                "Pro Forma Revenue (IS), Operating Profit / EBIT (IS), Consolidated Net Income (IS), and Ending Cash Balance (BS) — dynamically updating between Old Deck and Final Report.",
            ],
            [
                "Tab 1 Section 3 (Historical Driver Cards)",
                "\"Historical YoY Driver Trajectory Behind Forecast Inputs (2023* | 2024–1H26 Post-Exit)\": 4 vertical cards (COGS/Revenue, Cash OpEx/Revenue, "
                "Revenue Growth Rate, Continuing CapEx/Rev). Whichever row you clicked on the slide gets a highlighted border (focused card)!",
            ],
            [
                "Tab 1 Section 4 (Bottom Interactive Table)",
                "\"Key Financial Statement Forecast Assumptions (Post-Tokopedia · Table 11)\": 7 driver rows × 6 columns (2024A, 2025A, Base, Optimistic, Conservative) "
                "including Working Capital (10.9d DSO / 59.1d DPO), Effective Debt Rate (6.91%), and Tax Rate (22%). Hover over ANY cell to pop up a cursor-following source note!",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "4 comparison cards pitting Original Deck (2023–25 Avg) vs. Final Report (Post-Exit): Growth (11.40% → 15.27%), COGS (41.10% → 42.28%), "
                "Cash OpEx (78.50% → 55.70%, −2,280 bps), and CapEx (16.30% → 6.45%, −985 bps).",
            ],
            [
                "Tab 3 & Tab 4 (Calc / Proof)",
                "Tab 3: clicked driver formula + 2 Slide Calculation rows. Tab 4: Income Statement / Note 26 proof image + 2 collapsible schedules (11 scenario drivers + fixed/variable cost judgments).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 10 traces. \"Show Analysis\" includes a custom \"YoY Driver Story\" paragraph tailored to whichever driver you clicked. \"Appendix A4 ↗\" jumps to Slide 18.",
            ],
        ],
    },
    {
        "header": "SLIDE 8: Three-Year Forecast  [2.0 min  |  Ref: Appendix A5]",
        "goal": "Show that the clean post-Tokopedia Base Case turns net-profitable by 2028F and keeps Rp 19.42T cash, yet ROIC (+2.70%) still trails WACC (7.76%).",
        "script": (
            '"Here is what happens when we run those clean post-Tokopedia assumptions through our 3-year model. Revenue grows from Rp 18.32 trillion '
            'in 2025 to Rp 28.07 trillion in 2028F. Operating profit turns positive immediately in 2026F at +Rp 427 billion and reaches +Rp 567 billion '
            'in 2028F. Net income turns positive in year three at +Rp 25 billion, and ending cash stays strong at Rp 19.42 trillion—no cash crisis. '
            'However, notice the critical catch: GoTo needs Rp 20.38 trillion just to break even in 2026F, leaving only a thin 3.5% margin of safety '
            'and high operating leverage (28.56x DOL). Most importantly, 2028F Return on Invested Capital (ROIC) is only +2.70%, still 506 basis points below our 7.76% WACC."'
        ),
        "bullets": [
            "Restated Base Case (2025A → 2026F → 2028F): Revenue Rp 18.32T → Rp 21.12T → Rp 28.07T | EBIT −Rp 378B → +Rp 426.9B → +Rp 567.2B",
            "2028F Net Profit & Cash: Net Income reaches +Rp 25.0B (turns net-profitable in Year 3); Ending Cash holds strong at Rp 19.42T (vs. Rp 968B old deck)",
            "Operating Leverage Catch: 2026F Breakeven Revenue = Rp 20.38T → thin +3.50% Margin of Safety & 28.56x Degree of Operating Leverage (DOL)",
            "Economic Return Spread: 2028F Base ROIC (+2.70%) trails WACC (7.76%) by −506 bps; ROE (+0.09%) trails Ke (8.45%) by −836 bps",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Use the top Switcher Bar (Original vs. Restated) AND the live \"Scenario:\" dropdown directly above the table (Base, Optimistic, Conservative; "
                "in Original mode also includes 2-Yr Avg). Click any table row or right-hand card to open the popup.",
            ],
            [
                "Tab 1 Top Chart",
                "Includes the \"Previous Report (With 2023)\" vs. \"Current Report (Post-Exit)\" toggle. Previous shows 2026F–2028F EBIT falling from −3,854B to −4,967B "
                "and cash draining to +968B. Current shows Conservative 2028F EBIT (−2,143B), Base 2026F EBIT (+426.9B), Base 2028F EBIT (+567.2B), Base 2028F Net Income (+25.0B), "
                "and Optimistic 2028F EBIT (+3,221B).",
            ],
            [
                "Tab 1 Forecast Trajectory Cards",
                "\"Restated Base Forecast Trajectory (2025A → 2028F)\": 4 vertical column cards showing Revenue (18.32T → 28.07T), EBIT (−378B → +567B), "
                "Net Income (−1,502B → −84.5B → −33.6B → +25.0B), and Ending Cash (21.76T → 19.42T).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "\"2028F Forecast Impact: Old Deck vs. Clean Post-Exit Model\": 2028F EBIT (−Rp 4,967B → +Rp 567.2B), 2028F Net Income (−Rp 4,348B → +Rp 25.0B), "
                "2028F Ending Cash (Rp 0.97T → Rp 19.42T, +Rp 18.45T saved), and 2028F ROIC vs. WACC (Negative → +2.70% vs. 7.76%, −506 bps spread).",
            ],
            [
                "Tab 3 & Tab 4 (Calc / Proof)",
                "Tab 3 shows clicked formula (e.g., 2026F Breakeven = Rp 11,764.6B / 57.723% = Rp 20,381.1B) + 4 Slide Calculation rows. "
                "Tab 4 contains 5 collapsible schedules (Base IS, Base BS, Base CF, Breakeven & DOL, Sensitivity Check).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 10 traces. \"Show Analysis\" explains Scenario outcomes (Base, 1H26 Optimistic, 2024 Conservative); \"Appendix A5 ↗\" jumps to Slide 19.",
            ],
        ],
    },
    {
        "header": "SLIDE 9: Cost of Capital  [1.25 min  |  Ref: Appendix A6]",
        "goal": "Walk cleanly through how we built Cost of Equity (8.45%), After-Tax Cost of Debt (5.39%), and WACC (7.76%) using dated market inputs.",
        "script": (
            '"To value GoTo future cash flows, we need a discount rate built from dated market data. First, for Cost of Equity, we start with Indonesia '
            '10-year government bond yield of 6.120% as of December 30, 2025, subtract Damodaran 1.618% sovereign default spread to avoid double-counting '
            'country risk, leaving a clean IDR risk-free rate of 4.502%. Adding GoTo levered beta of 0.59 times Indonesia total equity risk premium '
            '(4.230% mature ERP + 2.465% country risk premium) gives a Cost of Equity of 8.45%. Next, for Cost of Debt, we divide FY2025 finance costs '
            'of Rp 535 billion by total borrowings and leases of Rp 7.74 trillion to get 6.91% pre-tax, or 5.39% after the 22% tax shield. Blending 77.4% '
            'market equity and 22.6% debt gives our baseline WACC of 7.76%."'
        ),
        "bullets": [
            "IDR Risk-Free Rate (Rf): 6.120% (ID 10Y SUN, Dec 30, 2025) − 1.618% (Damodaran Baa2 spread, Jan 1, 2026) = 4.502%",
            "Cost of Equity (Ke): 4.502% + 0.59 (Beta) × [4.230% (Mature ERP) + 2.465% (Indonesia CRP)] = 8.452% (rounded 8.45%)",
            "After-Tax Cost of Debt (Kd): (Rp 535.15B Note 27b ÷ Rp 7,742.64B Notes 19–20 = 6.912%) × (1 − 22% tax) = 5.390% (Zero-tax-shield WACC: 8.101%)",
            "Capital Weights & WACC: 77.42% Equity (Rp 26,550.3B @ Rp 25/sh) × 8.452% + 22.58% Debt (Rp 7,742.6B) × 5.390% = 7.761% (rounded 7.76%)",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click ANY row on the Slide 9 table (e.g., \"Shareholder return: Ke\", \"Debt cost after tax\", \"Equity weight\", \"Debt weight\", \"Combined rate: WACC\") "
                "or any right-hand card. The popup automatically jumps straight to the matching sub-tab!",
            ],
            [
                "Special Interactive Tab 1 Sub-Menu",
                "Slide 9 replaces the standard chart with a clean zero-scroll side-by-side \"Sources & Math\" walkthrough featuring 6 clickable top pills "
                "(plus Previous ← and Next → buttons inside the left card):",
            ],
            [
                "Sub-Tab 1: Risk-Free Rate (4.502%)",
                "Left: big 4.502% card + formula + feeds Step 2 & caps g. Right table: ID 10Y Bond Yield 6.120% (Investing.com Dec 30, 2025) − Sovereign Default Spread 1.618% (Damodaran Jan 1, 2026).",
            ],
            [
                "Sub-Tab 2: CAPM / Ke (8.452%)",
                "Right table lists Rf (4.502%), 5Y Levered Beta (0.59, stress-tested to 1.30), Mature ERP (4.230%), Indonesia CRP (2.465%), and 3-step math totaling 8.452%.",
            ],
            [
                "Sub-Tab 3: Cost of Debt (5.390%)",
                "Right table links FY2025 Finance Costs Rp 535.15B (Note 27b p. 131) ÷ Total Debt & Leases Rp 7,742.64B (Notes 19–20 pp. 105–111) = 6.912% × (1 − 22%) = 5.390% (also notes 8.101% WACC at 0% tax shield).",
            ],
            [
                "Sub-Tab 4: Capital Weights (77.4% / 22.6%)",
                "Right table shows Market Share Price Rp 25.00 × 1,062.01B shares (Note 31 p. 16) = Rp 26,550.3B Equity vs. Rp 7,742.6B Debt = Rp 34,292.9B Total Capital (77.42% E / 22.58% D).",
            ],
            [
                "Sub-Tab 5: WACC (7.761%)",
                "Right table shows Equity Component 6.544% (77.42% × 8.452%) + Debt Component 1.217% (22.58% × 5.390%) = 7.761% Baseline (8.101% zero-tax-shield check).",
            ],
            [
                "Sub-Tab 6: Terminal Growth g (3.00%)",
                "Proves g is not arbitrary: 2028F NOPAT (+Rp 442.4B) & Net Reinvestment (Rp 559.3B) ÷ Beg. IC (Rp 16,380.8B) → Reinvestment Rate 126.42% × ROIC 2.70% = +3.41% fundamental ceiling → capped at 3.00% (< 4.502% Rf cap; fits BI 2.5% ± 1% inflation).",
            ],
            [
                "Tabs 2–5, Show Analysis & Appendix",
                "Note: \"Show Analysis\" is hidden on Slide 9 because Tab 1 already has the 6-step layout. Tab 2 (Pre vs. Post Exit), Tab 3 (KaTeX formulas + 7 calc rows), "
                "Tab 4 (Note 20 debt proof + 2 schedules), Tab 5 (5 traces), and \"Appendix A6 ↗\" (Slide 20) are all active.",
            ],
        ],
    },
    {
        "header": "SLIDE 10: DCF and Residual Income  [2.25 min  |  Ref: Appendix A6]",
        "goal": "Explain why Base DCF flips to +Rp 10.38/share (powered entirely by Net Cash) while Residual Income stays negative (−Rp 12.23/share), and prove sensitivity stability.",
        "script": (
            '"Now let us apply two intrinsic valuation models: Discounted Cash Flow (DCF) and Residual Income (RI). In our earlier draft, 2023 costs '
            'pushed DCF to -Rp 121.1 and RI to -Rp 75.1. Once we remove 2023 in the Final Report, Base DCF turns positive to +Rp 10.38 per share. '
            'Why? Because GoTo holds Rp 14.01 trillion of Net Cash (Rp 13.19 per share). Even though EBIT turns positive, heavy CapEx keeps free cash flow '
            'negative, creating a negative Enterprise Value of -Rp 2.99 trillion. Net Cash minus negative EV leaves +Rp 11.02 trillion, or +Rp 10.38 per share. '
            'Meanwhile, Residual Income equals -Rp 12.23 per share because GoTo 2028F ROE (+0.09%) falls far short of our 8.45% Cost of Equity hurdle. '
            'Notice from our sensitivity grid that across WACC from 6.76% to 8.76% and growth from 1% to 4%, Base DCF barely moves: Rp 8.86 to Rp 11.18 per share."'
        ),
        "bullets": [
            "Base Case DCF (Final Report): Net Cash (+Rp 14,012.5B = +Rp 13.19/sh) minus Negative EV (−Rp 2,988.5B) = +Rp 11,024.0B → +Rp 10.38/share",
            "Base Case Residual Income: BVE Rp 28,711.7B − PV(RI) Rp 41,698.6B → −Rp 12.23/share (g = 3.0%) | +Rp 0.24/sh (g = 0% floor) | +Rp 21.13/sh (if ROE = Ke Yr 4+)",
            "Fundamental Terminal Growth Check: Reinvestment 126.42% × 2028F ROIC +2.70% = +3.41% ceiling → capped at 3.00% (< 4.502% Rf, 7.76% WACC, 8.45% Ke)",
            "WACC × g Sensitivity Grid: Across WACC 6.76%–8.76% and g 1.0%–4.0%, Base DCF stays tightly bounded between Rp 8.86 and Rp 11.18/share",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Use the top Switcher Bar (Original vs. Restated; in Original mode a \"Base Basis:\" 3-Yr vs. 2-Yr dropdown appears). "
                "Click any row of the DCF vs. RI table, the valuation range bar chart, or the 3 right-hand cards.",
            ],
            [
                "Tab 1 Section 1 (Top Diverging Chart)",
                "Has the \"Previous Report (With 2023)\" vs. \"Current Report (Post-Exit)\" toggle with a dashed vertical \"Net Cash Rp13.19\" reference line. "
                "Previous shows −Rp 121.10 DCF and −Rp 75.10 RI. Current plots 5 bars: Base RI g=3.0% (−Rp 12.23), Base RI g=0% (+Rp 0.24), "
                "Base DCF Post-Exit (+Rp 10.38), Net Cash / Share (+Rp 13.19), and RI Yr4+ Convergence (+Rp 21.13).",
            ],
            [
                "Tab 1 Section 2 (2D Sensitivity Matrix)",
                "\"Base DCF Sensitivity Matrix: WACC × Terminal Growth g (Rp / share · Table 16)\": 3 rows (WACC 6.76%, 7.76% Baseline, 8.76%) × 5 columns "
                "(g = 1.0%, 2.0%, 3.0% Base, 3.5%, 4.0%), spanning Rp 8.86 to Rp 11.18/share—explaining why higher WACC slightly raises DCF (discounts negative EV).",
            ],
            [
                "Tab 1 Section 3 (Stress & Boundary Table)",
                "\"Beta Stress, Zero-Tax-Shield WACC & Residual Income Boundary Checks (Tables 14–16)\": 6 rows comparing Base Beta 0.59 (+Rp 10.38 / −Rp 12.23), "
                "Zero-Tax-Shield WACC 8.10% (+Rp 10.52), Normalized Tech Beta 1.01 (+Rp 11.09 / −Rp 8.45), High-Vol Beta 1.30 (+Rp 11.36 / −Rp 6.00), "
                "RI g = 0% Floor (+Rp 0.24), and RI Yr 4+ ROE=Ke Convergence (+Rp 21.13).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "4 comparison cards summarizing the +Rp 131.48/sh DCF jump (−Rp 121.10 → +Rp 10.38), RI (−Rp 54.40 / −Rp 75.10 → −Rp 12.23), "
                "Defensible Range (Negative → Rp 10.38–16.75), and intact SELL / AVOID thesis.",
            ],
            [
                "Tab 3 & Tab 4 (Calc / Proof)",
                "Tab 3 displays clicked bridge formula + 6 Slide Calculation rows (\"View more (+3 rows)\"). Tab 4 holds 7 collapsible schedules "
                "(Side-by-Side Valuation Bridge, Beta/WACC/g sensitivity, 3% growth rationale, FCFF build-up, RI build-up, Grab P/B, Excluded peers).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 6 traces. \"Show Analysis\" walks through why EV is negative despite positive EBIT. \"Appendix A6 ↗\" jumps to Slide 20.",
            ],
        ],
    },
    {
        "header": "SLIDE 11: Grab Comparison and Valuation  [2.25 min  |  Ref: Appendix A6]",
        "goal": "Explain why we benchmarked only against Grab, why Rp 91.02 is rejected, and how all 7 Football Field bars anchor our Rp 10.38–Rp 16.75 range.",
        "script": (
            '"For relative valuation, we chose Grab Holdings as our sole comparable because Grab shares GoTo exact mix of rides, food delivery, and digital '
            'financial services. We excluded Sea (skewed by Garena gaming), Bukalapak (investment gains), and Blibli (physical retail stores and negative EBITDA). '
            'On December 31, 2025, Grab traded at 3.04x Price-to-Book. Multiplying 3.0391x by GoTo parent Book Value per Share of Rp 29.95 gives Rp 91.02 per share. '
            'However, we reject Rp 91.02 as a fair target because Grab is already profitable (+2.96% ROE), whereas GoTo still earns negative ROE (-5.23%) and sits '
            'well below its cost of capital. Looking at the Valuation Football Field, our defensible intrinsic range is Rp 10.38 (Base DCF) to Rp 16.75 (Optimistic RI), '
            'centered around Rp 13.19 Net Cash. The Rp 25.00 benchmark price sits 49% to 141% above intrinsic value."'
        ),
        "bullets": [
            "Grab P/B (Dec 31, 2025): US$4.99 ÷ US$1.6419 BVPS = 3.0391x × GoTo Parent BVPS (Rp 29.9479) = Rp 91.02/share (Rejected as an actionable target)",
            "Excluded Peers: Sea (Shopee bundled with Garena gaming & Monee), BUKA (investment gains distort earnings), BELI (inventory-led physical retail & negative EBITDA)",
            "Defensible Intrinsic Range: Rp 10.38 (Base DCF floor) → Rp 13.19 (Net Cash center) → Rp 16.75 (Optimistic RI ceiling using 1H26 costs)",
            "Benchmark Market Price: Rp 25.00/share sits 49% to 141% above our intrinsic range (requiring −33% to −58% downside to reach fair value)",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click any row in the Grab table (\"Grab P/B\", \"GoTo parent BVPS\", \"Defensible Intrinsic Range\"), any excluded peer card (Shopee/Sea, BUKA, BELI), "
                "or the right-hand cards.",
            ],
            [
                "Tab 1 Section 1 (7-Bar Football Field)",
                "\"Valuation Football Field vs. Rp25.00 Market & Grab P/B\" diverging bars with a dashed vertical \"Market Rp25.00\" line: "
                "(1) Conservative RI (−Rp 44.42), (2) Base RI g=3.0% (−Rp 12.23), (3) Base DCF Floor (+Rp 10.38), (4) Net Cash / Share (+Rp 13.19), "
                "(5) Opt. RI Ceiling (+Rp 16.75), (6) Opt. DCF 1H26 (+Rp 47.34), and (7) Grab P/B 3.04x (+Rp 91.02).",
            ],
            [
                "Tab 1 Section 2 (7 Driver Cards Below)",
                "\"What Drives Each Football Field Valuation Bar (Rp / Share)\" displays 7 explanatory cards right underneath the chart. "
                "The 3 green-highlighted cards mark our core range: Floor Base DCF (+Rp 10.38), Center Net Cash (+Rp 13.19), and Ceiling Opt. RI (+Rp 16.75).",
            ],
            [
                "Tab 1 Section 3 (3-Scenario Matrix)",
                "\"3-Scenario Valuation Matrix & Defensible Range Reconciliation (Rp / share · Appendix A6)\": 5-row table comparing DCF/sh, RI/sh, and Economic Driver "
                "for Base (+Rp 10.38 / −Rp 12.23), Optimistic 1H26 (+Rp 47.34 / +Rp 16.75), Conservative 2024 (−Rp 33.95 / −Rp 44.42), Net Cash (+Rp 13.19), and Grab P/B (Rp 91.02).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Shows the valuation shift from Original Deck (−Rp 121.10 DCF / −Rp 75.10 RI) to the Rp 10.38–Rp 16.75 Final Report range.",
            ],
            [
                "Tab 3 & Tab 4 (Calc / Proof)",
                "Tab 3 shows Grab P/B formula + 4 Slide Calculation rows (Grab BVPS, Grab P/B, GoTo BVPS, Grab Benchmark). "
                "Tab 4 includes Grab FY2025 20-F / GoTo equity proof + 2 collapsible schedules (Grab calculation & peer exclusions).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 5 traces. \"Show Analysis\" includes the explicit \"Defensible Range Basis\" math (Rp 14,012.5B Net Cash − Rp 2,988.5B EV = +Rp 11,024.0B ÷ 1,062.01B sh). \"Appendix A6 ↗\" jumps to Slide 20.",
            ],
        ],
        "figure": ("image4.png", "Figure 4: Slide 11 Popup showing the Valuation Football Field vs. Market Rp 25.00, with every bar explained right underneath."),
    },
    {
        "header": "SLIDE 12: Recommendation  [2.0 min  |  Ref: Appendix A6]",
        "goal": "Deliver a clear SELL / AVOID verdict at Rp 25.00 with measurable HOLD/BUY upgrade triggers and downside risks.",
        "script": (
            '"To conclude for our short-term public equity investor: our recommendation is SELL / AVOID at the Rp 25.00 reference price. '
            'Even after cleaning up all historical model errors, GoTo fair value sits between Rp 10.38 and Rp 16.75 per share, meaning Rp 25.00 '
            'trades 49% to 141% above intrinsic value and prices in 2.4x Base DCF. What would change our mind? We set clear, measurable triggers: '
            'we would upgrade to HOLD if the stock pulls back to Rp 13.20 or lower (1.0x Net Cash) with positive Free Cash Flow. We would upgrade to BUY '
            'only if GoTo holds its 1H 2026 efficiency—Cash OpEx at or below 51.2% and Gross Margin at or above 61.9%—for two straight quarters. '
            'Conversely, if Cash OpEx slips above 60%, GoPay loan provisions exceed Rp 650 billion, or Tokopedia suffers a write-down above 15%, our SELL case deepens."'
        ),
        "bullets": [
            "Final Verdict: SELL / AVOID at Rp 25.00 (2.41x Base DCF Rp 10.38; 1.90x Net Cash Rp 13.19; −33% to −58% gap to Rp 10.38–Rp 16.75 range)",
            "Upgrade to HOLD: Share price pulls back to ≤ Rp 13.20 (1.0x Net Cash) WITH positive Free Cash Flow (FCF > 0)",
            "Upgrade to BUY: Cash OpEx ≤ 51.2% AND Gross Margin ≥ 61.9% sustained for 2 consecutive quarters (proving 1H 2026 run-rate)",
            "Reinforce SELL / Downside Risks: Cash OpEx ≥ 60.0% OR Credit Provisions ≥ Rp 650B OR Tokopedia write-down > 15% (upside risk: M&A/buyout)",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Toggle the top Switcher Bar to \"Final Report (Restated)\" so the 3 rows show Final verdict (SELL / AVOID), Economic spread (−506 bps), "
                "and Upgrade triggers (≤ Rp 13.20 / ≤ 51.2%). Click any row or right-hand card.",
            ],
            [
                "Tab 1 Top Chart",
                "\"Economic Return Spread (ROIC vs. WACC) & Valuation Gap\" diverging bars: 2028F Base ROIC (+2.70%), Base WACC Hurdle (7.76%), "
                "ROIC − WACC Spread (−5.06% red), 2028F Base ROE (+0.09%), Cost of Equity Ke (8.45%), and ROE − Ke Spread (−8.36% red).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Shows the 4-card Valuation Impact comparison proving why SELL / AVOID holds across both Original Deck and Restated Final Report.",
            ],
            [
                "Tab 3 & Tab 4 (Calc / Proof)",
                "Tab 3 shows the clicked trigger/spread formula (e.g., 2028F ROIC +2.70% − WACC 7.76% = −506 bps; BUY/HOLD thresholds) and origin. "
                "Tab 4 is not needed on Slide 12 (use Appendix A6 button instead).",
            ],
            [
                "Tab 5, Show Analysis & Appendix",
                "Tab 5 has 4 traces. \"Show Analysis\" details the exact SELL verdict, rating triggers, and upside/downside risks. \"Appendix A6 ↗\" jumps to Slide 20.",
            ],
        ],
    },
    {
        "header": "SLIDE 13: Forensic Restatement: 5 Mistakes Corrected  [1.5 min  |  Ref: Appendix A6]",
        "goal": "Turn our earlier Milestone 2 and Milestone 4 errors into a strength by demonstrating complete transparency and audited forensic rigor.",
        "script": (
            '"Before we close, we want to be completely transparent about five errors in our earlier Milestone 2 and Milestone 4 drafts that we fixed '
            'in our Final Report. First and biggest: our old deck averaged 2023 pre-Tokopedia costs (117% OpEx) into our Base Case. Removing 2023 drops '
            'Base OpEx from 78.5% to 55.7%, flips 2028F EBIT from -Rp 4.97 trillion to +Rp 567 billion, and lifts DCF from -Rp 121.1 to +Rp 10.38. '
            'Second: we restored Rp 1.58 trillion of omitted Note 7 lending receivables to 2024 assets, fixing the balance sheet check to zero and lifting '
            '2024 Current Ratio from 2.46x to 2.62x. Third: we separated Note 6 Trade Receivables from Note 7 loans, fixing 2024 DSO from a distorted 46.9 days '
            'down to 10.56 days. Fourth: we harmonized full debt and leases across Notes 19 and 20 and linked Note 27b interest expense so Times Interest Earned '
            'calculates live. Fifth: we stripped Rp 5.46 trillion of deconsolidated Tokopedia intangibles out of 2024 CapEx, bringing continuing CapEx from 41.0% down to 6.63%."'
        ),
        "bullets": [
            "Fix 1 — Remove 2023 Pre-Exit: 3-yr avg (78.5% OpEx, 16.3% CapEx) → Post-Tokopedia 2024–25 (55.70% OpEx, 6.45% CapEx); 2028F EBIT −Rp 4.97T → +Rp 567B; DCF −121.1 → +10.38",
            "Fix 2 — 2024 Balance Sheet: Restored Rp 1,582B omitted Note 7 loans → Assets Rp 43,208B (Check = 0); 2024 Current Ratio 2.46x → 2.62x; Equity Multiplier 1.37x → 1.42x",
            "Fix 3 — 2024 Trade AR DSO: Separated strict Note 6 Trade AR (Rp 460B → 547B) from Note 7 consumer loans → True DSO 10.56d (vs. 46.88d artificial spike)",
            "Fix 4 — Debt & Live TIE: Included current debt + all leases (Notes 19–20) + live Note 27b interest → 2024 D/E 12.57% → 15.85%; live TIE −4.54x → −0.71x",
            "Fix 5 — 2024 Continuing CapEx: Excluded Rp 5,465B Tokopedia Note 12 intangible transfer → Continuing CapEx 41.0% → 6.63%",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click any of the 5 rows in the Restatement table or any right-hand summary card.",
            ],
            [
                "Tab 1 Top Chart (Interactive Toggle)",
                "Has the \"Previous Report (With 2023)\" vs. \"Current Report (Post-Exit)\" switcher right inside the chart header: "
                "Previous shows 78.50% Base Cash OpEx (red), 41.00% 2024 Raw CapEx (red), 46.88d 2024 Mixed DSO (red), and 2.46x Current Ratio; "
                "Current flips to 55.70% OpEx, 6.63% Cont. CapEx, 10.56d Trade DSO, and 2.62x Current Ratio.",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Shows the 4-card Valuation Impact comparison summarizing how the 5 restatement fixes move DCF +Rp 131.48/sh while preserving SELL / AVOID.",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Displays the exact forensic formula and origin (e.g., Final Report Appendix B Table B1 #1–#5 & Audited Notes 6, 7, 12, 19–20, 27b, 34c).",
            ],
            [
                "Tab 4 & Tab 5",
                "Tab 4 is empty here; Tab 5 holds the Appendix B restatement trace. \"Show Analysis\" explains the exact before/after math for the clicked fix. \"Appendix A6 ↗\" jumps to Slide 20.",
            ],
        ],
    },
    {
        "header": "SLIDE 14: Old Deck vs. Final Report: Why SELL Still Holds  [1.5 min  |  Ref: Appendix A6]",
        "goal": "Close with our strongest takeaway: fixing every historical mistake actually makes our SELL / AVOID thesis MORE credible, not weaker.",
        "script": (
            '"To wrap up, look at our side-by-side comparison of the Original Deck versus our Final Report. In the old deck, our SELL call relied '
            'on an artificial -Rp 121 DCF driven by obsolete 2023 Tokopedia costs. After fixing all five errors, GoTo Base Case looks much healthier. '
            'EBIT turns positive (+Rp 567B in 2028F), cash stays strong at Rp 19.4 trillion, and DCF rises to +Rp 10.38. Yet our SELL / AVOID '
            'recommendation is actually stronger now, because even on a completely clean post-Tokopedia model, GoTo 2.70% ROIC still trails its 7.76% WACC, '
            'and its Rp 10.38 to Rp 16.75 intrinsic value range still sits far below Rp 25.00. Thank you. We are now happy to take your questions, '
            'and we have Appendices A1 through A6 ready if you would like to inspect any supporting schedule."'
        ),
        "bullets": [
            "Base Cash OpEx (% Rev): 78.5% (Old) → 55.70% (Final Report, −2,280 bps post-Tokopedia)",
            "2028F Base EBIT & Net Income: EBIT −Rp 4,967B → +Rp 567.2B (turns positive 2026F) | Net Income −Rp 4,489B → +Rp 25.0B (positive Year 3)",
            "2028F Ending Cash: Rp 968B (Old) → Rp 19,421B / Rp 19.42T (Final Report — no liquidity crisis)",
            "Valuation & Verdict: Base DCF −Rp 121.1 → +Rp 10.38 | Base RI −Rp 75.1 → −Rp 12.23 | Defensible Range Rp 10.38–Rp 16.75 (33%–58% below Rp 25.00) → SELL / AVOID stands firm",
        ],
        "popup_rows": [
            [
                "What to Click on Slide",
                "Click any of the 8 reconciliation rows (Base OpEx, EBIT, Net Income, Ending Cash, DCF, RI, Defensible Range, Verdict) or right-hand cards.",
            ],
            [
                "Tab 1 Top Chart",
                "\"Economic Return Spread (ROIC vs. WACC) & Valuation Gap\" diverging bars: 2028F Base ROIC (+2.70%), Base WACC Hurdle (7.76%), "
                "ROIC − WACC Spread (−5.06% red), 2028F Base ROE (+0.09%), Cost of Equity Ke (8.45%), and ROE − Ke Spread (−8.36% red).",
            ],
            [
                "Tab 2: Pre vs. Post Exit",
                "Not active on Slide 14 (because the main Slide 14 table itself already IS the side-by-side Old vs. Final Report comparison).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows the exact formula and Final Report table reference (Tables 11, 12, 15, 16 & §5.3 / §6.1) for whichever reconciliation row you clicked.",
            ],
            [
                "Tab 4, Tab 5, Show Analysis & Appendix",
                "Tab 4 is empty; Tab 5 holds the Final Report §6.1 reconciliation trace. \"Show Analysis\" summarizes why clean operations still destroy economic value. "
                "\"Appendix A6 ↗\" jumps to Slide 20 for Q&A backup schedules.",
            ],
        ],
    },
]

APPENDIX_SLIDES = [
    {
        "header": "SLIDE 15 (APPENDIX A1): Revenue Bridge & Competitive Risk Schedules  [Q&A Backup | Linked from Slides 2 & 3]",
        "goal": "Provide the exact line-by-line FY2025 Note 29 revenue bridge and Note 35 GoPay lending & Porter Five Forces numbers during Q&A.",
        "script": (
            '"If we jump to Appendix A1, you can see the exact tie-out from Note 29 of the audited FY2025 statements: Gojek contributes Rp 12,361.3 billion, '
            'GoTo Financial adds Rp 5,190.6 billion, and Tokopedia service fees contribute Rp 819.7 billion. Subtracting Rp 49.5 billion of group promo eliminations '
            'gives our exact Rp 18,322.1 billion consolidated net revenue. Below that, Schedule 2 shows Note 35 GoPay lending jumping 72.6% to Rp 2,731 billion '
            'while credit-loss allowances rose 134.9% to Rp 407.7 billion alongside Rp 3.09T marketing and Rp 2.15T R&D spending."'
        ),
        "bullets": [
            "Table 1 — Revenue Bridge (Rp bn): Gojek 12,361.259 + GoTo Financial 5,190.617 + Tokopedia Service Fee 819.724 = 18,371.600 − Eliminations 49.483 = 18,322.117",
            "Schedule 2 — Note 35 GoPay Lending Exposure: Net financing receivables Rp 1,582B (2024) → Rp 2,731B (2025, +72.6%); ECL allowance Rp 173.6B → Rp 407.7B (+134.9%)",
            "Competitive Cost & Five Forces Matrix: S&M Rp 3.09T | Product Dev Rp 2.15T | New Entrants Low-Mod | Suppliers Low | Buyers & Substitutes Medium | Rivalry High",
        ],
        "popup_rows": [
            [
                "What to Click on Appendix A1",
                "Click any row in the \"Revenue bridge to consolidated GoTo revenue\" table or any row in the lower \"Note 35 GoPay Lending Exposure & Porter Five Forces Matrix\" schedule.",
            ],
            [
                "Tab 1: Appendix Supporting Metrics",
                "Displays the \"Appendix Supporting Metrics Overview\" diverging chart parsed from A1 calculation notes: Consolidated Revenue (Rp 18,322.117bn) and Provision Growth (134% rounded).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows clicked row origin/steps plus the 2-row Slide Calculation Table (Consolidated Revenue = Rp 18,322.117bn; Provision Growth = 134% rounded).",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Shows the Audited Note 29 / Note 35 statement proof image (click to zoom) plus the collapsible Note 35 & Five Forces schedule.",
            ],
            [
                "Tab 5, Show Analysis & Navigation",
                "Tab 5 lists 15 traces (lectures & Milestone 1/4 references). \"Show Analysis\" summarizes segment revenue & Tokopedia fee structure. "
                "Slide footer has \"← Back to Slide 2/3\" and A1–A6 quick-jump pills.",
            ],
        ],
    },
    {
        "header": "SLIDE 16 (APPENDIX A2): Historical & Pro Forma Summary (FY2023–2028F) & DuPont  [Q&A Backup | Linked from Slide 4]",
        "goal": "Display the complete 11-line historical (2023A–2025A) and 3-year forecast (2026F–2028F) summary plus the full 2025 DuPont formula table.",
        "script": (
            '"Appendix A2 presents our complete six-year consolidated summary alongside the exact 2025 DuPont decomposition. You can trace net revenue '
            'rising from Rp 14,785 billion in 2023 to Rp 18,322 billion in 2025, gross margin recovering from 53.4% in 2024 to 57.7% in 2025, '
            'and operating loss shrinking from Rp 10,279 billion to Rp 378 billion. Below the summary table, the DuPont breakdown confirms how '
            '-8.2% net margin × 0.40x asset turnover × 1.59x equity multiplier produces our -5.23% consolidated ROE."'
        ),
        "bullets": [
            "Table 1 — 11-Line Consolidated Financial Summary (2023A–2028F Base): Net Revenue, Gross Profit, Gross Margin %, EBIT, Net Income, CFO, Cash CapEx, FCF/FCFF, Ending Cash, Total Debt, Equity",
            "Schedule 2 — 2025 DuPont Breakdown (4 rows): Net Margin −8.2% (−1,501,685 / 18,322,117) × Asset Turnover 0.40x (18,322,117 / 45,757,642) × Equity Multiplier 1.59x (45,757,642 / 28,711,657) = −5.23% ROE",
            "Note on Old-Deck Pro Forma Columns: A2 preserves the submitted Milestone 4 columns (2026F–2028F Base) for traceability alongside the Final Report restatement on Slides 4, 8, and 14",
        ],
        "popup_rows": [
            [
                "What to Click on Appendix A2",
                "Click any of the 11 historical/pro forma rows in the main table or any of the 4 rows in the \"2025 DuPont\" supporting schedule.",
            ],
            [
                "Tab 1: Appendix Supporting Metrics",
                "Displays \"Appendix Supporting Metrics Overview\" diverging chart built from A2 calculation notes (Operating Loss −378B, Gross Margin 57.7%, Operating Margin −2.1%, Net Margin −8.2%, ATO 0.40x, EM 1.59x).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows clicked metric steps/origin plus all 12 Slide Calculation rows (Operating Profit, GM, OM, NM, ATO, EM, ROA, ROE, 3-factor DuPont, 5-factor DuPont, Tax & Interest Burden).",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Displays Audited Income Statement / Gross Profit / OpEx highlighted proof image (click to zoom) + collapsible \"2025 DuPont\" 4-row schedule.",
            ],
            [
                "Tab 5, Show Analysis & Navigation",
                "Tab 5 lists 9 traces (7 lectures + 2 assignments). \"Show Analysis\" explains the 2023–2025 loss trajectory and DuPont drivers. "
                "Footer provides \"← Back to Slide 4\" and A1–A6 quick-jump pills.",
            ],
        ],
    },
    {
        "header": "SLIDE 17 (APPENDIX A3): Liquidity, Working Capital, Week 6 Z-Score & Footnotes  [Q&A Backup | Linked from Slides 5 & 6]",
        "goal": "Provide the exact numerators, denominators, weights, and contributions for the Week 6 Altman Z-Score plus all 6 Milestone 3 accounting red flags.",
        "script": (
            '"Appendix A3 shows the full mathematical proof behind Slide 5 and Slide 6. The top table lists every numerator and denominator for our Week 6 '
            'Altman Z-Score using FY2025 audited figures: X1 contributes +0.483 from Rp 18.41 trillion of working capital, X4 contributes +1.008 from strong equity '
            'over liabilities, and X5 adds +0.400. The entire -4.72 score is caused by X2 (-6.588) from Rp 215.33 trillion of historical accumulated deficit. '
            'Below it, our Milestone 3 table documents the -3.95% accrual ratio, the Rp 10.33 trillion Tokopedia and Bank Jago stakes (22.57% of assets), '
            'Rp 1.67 trillion in Level 3 unquoted investments, 7.13% related-party revenue, and the Rp 1.82 trillion 20% asset haircut test."'
        ),
        "bullets": [
            "Table 1 — Completed Week 6 Five-Factor Z-Score (Denominator Assets = Rp 45,757.642B): X1 = +0.482849 (WC 18,411.7B) | X2 = −6.588355 (RE −215,334.0B) | X3 = −0.027279 (EBIT −378.3B) | X4 = +1.010619 (Eq 28,711.7B / Liab 17,046.0B) | X5 = +0.400417 (Rev 18,322.1B) → Total Z = −4.721750",
            "Schedule 2 — Milestone 3 Accounting & Footnote Findings (6 rows): Accrual Ratio −3.95% | Tokopedia Rp 7,432B + Bank Jago Rp 2,895B (22.57% of assets) | Level 3 investments Rp 1,669B | Related-party revenue Rp 1,306B (7.13%) | Incentives classification | 20% haircut test = Rp 1,820B pre-tax",
        ],
        "popup_rows": [
            [
                "What to Click on Appendix A3",
                "Click any Z-Score component row (X1–X5) in the main table or any of the 6 findings in the \"Milestone 3 accounting and footnote findings\" schedule.",
            ],
            [
                "Tab 1: Appendix Supporting Metrics",
                "Displays \"Appendix Supporting Metrics Overview\" diverging chart built from A3's top calculation notes (Current Ratio 2.73x, Quick Ratio 2.73x, WC, D/E 0.27x, Debt/Assets 16.9%, TIE −0.71x).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Displays ALL 22 Slide Calculation rows combining Slide 5 liquidity/working-capital/Z-score math and Slide 6 cash flow/accrual/haircut math (\"View more (+19 rows)\").",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Audited Balance Sheet / Deficit proof image + collapsible \"Milestone 3 accounting and footnote findings\" table (6 rows).",
            ],
            [
                "Tab 5, Show Analysis & Navigation",
                "Tab 5 holds 19 traces (15 lectures + 4 assignments). \"Show Analysis\" summarizes liquidity vs. distress score. "
                "Footer provides \"← Back to Slide 5/6\" and A1–A6 quick-jump pills.",
            ],
        ],
    },
    {
        "header": "SLIDE 18 (APPENDIX A4): Scenario Drivers, Forecast Rationales & Cost Behavior  [Q&A Backup | Linked from Slide 7]",
        "goal": "Show all 11 Milestone 4 scenario drivers (Base, Optimistic, Conservative) with their exact rationales plus Week 12 fixed vs. variable cost judgments.",
        "script": (
            '"Appendix A4 provides all 11 forecast assumptions from our Milestone 4 workbook—covering revenue growth, COGS, operating costs, '
            'DSO, DIO, DPO, CapEx, depreciation, 22% tax rate, debt interest rate, and 0% dividend payout—alongside the exact reason for each Base, Optimistic, '
            'and Conservative number. Below the 11-row table, we show our Week 12 cost behavior split: COGS (cloud hosting, driver incentives) is mostly variable, '
            'while G&A, technology salaries, and depreciation act as fixed costs creating high operating leverage. Remember that on Slides 7, 8, and 14 we also '
            'show our restated post-Tokopedia drivers removing the 2023 117% OpEx anomaly."'
        ),
        "bullets": [
            "Table 1 — All 11 Scenario Drivers (Submitted Milestone 4 Workbook): Revenue Growth (11.4% / 15.3% / 7.5%), COGS (41.1% / 38.1% / 46.6%), OpEx (78.5% / 55.7% / 85.0%), DSO (24.2d / 10.9d / 30.0d), DIO (4.8d / 0.7d / 8.0d), DPO (67.8d / 75.0d / 59.1d), CapEx (16.3% / 6.5% / 20.0%), D&A (30.6% / 25.0% / 43.9%), Tax (22.0%), Interest (10.2% / 6.9% / 12.9%), Dividends (0.0%)",
            "Schedule 2 — Fixed and Variable Cost Judgments (4 rows from Week 12): classifies cloud, server, payment processing, S&M promos, R&D engineering, and G&A fixed vs. variable behavior",
        ],
        "popup_rows": [
            [
                "What to Click on Appendix A4",
                "Click any of the 11 driver rows in the main table or any of the 4 cost-behavior rows in the supporting schedule below.",
            ],
            [
                "Tab 1: Appendix Supporting Metrics",
                "Displays \"Appendix Supporting Metrics Overview\" comparing Base Revenue Growth (11.4% displayed) vs. Operating-Cost Assumption (78.5% displayed).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows clicked driver explanation/origin plus the 2 Slide Calculation rows (Base Revenue Growth & Operating-Cost Assumption).",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Displays Note 26 Operating Expenses proof image + collapsible \"Fixed and variable cost judgments\" schedule (4 rows).",
            ],
            [
                "Tab 5, Show Analysis & Navigation",
                "Tab 5 holds 10 traces (8 lectures + 2 assignments). \"Show Analysis\" explains the historical 117% 2023 OpEx anomaly and scenario design. "
                "Footer provides \"← Back to Slide 7\" and A1–A6 quick-jump pills.",
            ],
        ],
    },
    {
        "header": "SLIDE 19 (APPENDIX A5): Three-Year Pro Forma Statements & Operating Leverage  [Q&A Backup | Linked from Slide 8]",
        "goal": "Provide the full 3-statement Base Case pro forma projections (Income Statement, Balance Sheet, Cash Flow) plus Breakeven & DOL checks.",
        "script": (
            '"Appendix A5 houses the full three-statement pro forma model behind Slide 8. On the top table, you see the line-by-line Income Statement '
            'from Revenue down to Gross Profit, EBIT, Interest Expense, Taxes, and Net Income for 2026F through 2028F. Beneath it sit four collapsible supporting '
            'schedules: the Projected Balance Sheet (16 lines), the Projected Cash Flow Statement (13 lines), the Breakeven & Degree of Operating Leverage schedule, '
            'and the Fixed-Cost Freeze sensitivity check showing how holding OpEx fixed at Rp 10,954 billion produces an Rp 18,604 billion breakeven point."'
        ),
        "bullets": [
            "Table 1 — Base Projected Income Statement (9 rows, 2026F–2028F): Revenue, COGS, Gross Profit, Operating Expenses, EBIT, Interest Expense, EBT, Tax (22%), Net Income",
            "Schedule 2 — Base Projected Balance Sheet (16 rows): Cash plug, AR, Inventory, Total Current Assets, PP&E, Total Assets, Debt, Equity",
            "Schedule 3 — Base Projected Cash Flow Statement (13 rows): Net Income, D&A, Working Capital changes, CFO, CapEx, CFI, CFF, Ending Cash",
            "Schedules 4 & 5 — Breakeven & Operating Leverage (10 rows) + Sensitivity & Fixed-OpEx Freeze Check (6 rows: Rp 18,604B breakeven, DOL 11.31x → 3.77x)",
        ],
        "popup_rows": [
            [
                "What to Click on Appendix A5",
                "Click any Income Statement row or any row across the 4 supporting schedules below (Balance Sheet, Cash Flow, Breakeven/DOL, Sensitivity).",
            ],
            [
                "Tab 1: Appendix Supporting Metrics",
                "Displays \"Appendix Supporting Metrics Overview\" diverging chart built from A5 calculation notes: 2026F Revenue (Rp 20,408B), Base Operating Margin (−19.6%), Fixed-Cost Breakeven (Rp 18,604B), Ending Cash (Rp 968B).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Shows clicked line-item formula + 4 Slide Calculation rows (\"View more (+1 row)\").",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Provides all 4 full supporting schedules inside collapsible accordion blocks (Projected Balance Sheet, Projected Cash Flow, Breakeven & DOL, Beta/WACC/g Sensitivity).",
            ],
            [
                "Tab 5, Show Analysis & Navigation",
                "Tab 5 has 10 traces (8 lectures + 2 assignments). \"Show Analysis\" contrasts scaled-OpEx losses with the Fixed-Cost Freeze breakeven check. "
                "Footer provides \"← Back to Slide 8\" and A1–A6 quick-jump pills.",
            ],
        ],
    },
    {
        "header": "SLIDE 20 (APPENDIX A6): Dated WACC, DCF, Residual Income & FY2025 Grab P/B Schedules  [Q&A Backup | Linked from Slides 9–14]",
        "goal": "Serve as the master valuation appendix for Q&A, containing every dated WACC input, DCF & RI schedules, sensitivity checks, Grab P/B math, and peer exclusions.",
        "script": (
            '"Appendix A6 is our complete valuation backup for Slides 9 through 14. The main table documents every dated Cost of Capital input—Indonesia 10Y SUN '
            'on December 30, 2025 (6.120%), Damodaran sovereign spread (1.618%), Mature ERP (4.23%), Indonesia CRP (2.465%), Investing.com Beta (0.59), and effective '
            'FY2025 debt cost (6.91% pre-tax / 5.39% after-tax)—giving our 7.76% WACC and 8.45% Ke. Below that are seven complete schedules: the DCF vs. Residual Income '
            'side-by-side bridge, Beta/WACC/g sensitivity, why 3.0% terminal growth sits below Rf and WACC, the exact FCFF and Residual Income year-by-year build-ups, '
            'our Grab 3.0391x P/B math (US$4.99 / US$1.6419), and why Sea, Bukalapak, and Blibli are excluded."'
        ),
        "bullets": [
            "Table 1 — Dated CAPM & WACC Build-Up (7 rows): Rf 4.502%, Beta 0.59, Mature ERP 4.23%, CRP 2.465%, Ke 8.45%, After-Tax Kd 5.39%, Capital Weights 77.4%/22.6% → WACC 7.76%",
            "Schedule 1 & 2 — DCF vs. RI Side-by-Side Valuation Bridge (5 rows) + Beta / WACC / Terminal Growth Sensitivity & Breakeven Check (6 rows)",
            "Schedule 3, 4 & 5 — Why 3.0% Terminal Growth (4 rows: 3.0% < 4.502% Rf < 7.76% WACC < 8.45% Ke) + FCFF Build-Up (7 rows) + Residual Income Build-Up (6 rows)",
            "Schedule 6 & 7 — Grab Benchmark Calculation (6 rows: US$4.99 / US$1.6419 = 3.0391x × Rp 29.9479 GoTo BVPS = Rp 91.02/sh) + Why Sea, BUKA & BELI are Excluded (3 rows)",
        ],
        "popup_rows": [
            [
                "What to Click on Appendix A6",
                "Click any of the 7 dated WACC rows in the top table or any row across the 7 supporting schedules below.",
            ],
            [
                "Tab 1: Appendix Supporting Metrics",
                "Displays \"Appendix Supporting Metrics Overview\" diverging chart built from A6's top calculation notes (Ke 8.45%, Pre-Tax Kd 6.91%, Tax 22.0%, After-Tax Kd 5.39%, Equity Weight 77.4%, Debt Weight 22.6%).",
            ],
            [
                "Tab 3: Calculations & Formula",
                "Displays ALL 17 Slide Calculation rows (\"View more (+14 rows)\") covering every WACC, DCF, Residual Income, and Grab P/B formula.",
            ],
            [
                "Tab 4: Schedules & Proof",
                "Displays Note 20 Debt Schedule & Equity Balance Sheet proof images + all 7 collapsible schedules (Valuation Bridge, Sensitivity, 3% Growth Check, FCFF, RI, Grab, Excluded Peers).",
            ],
            [
                "Tab 5, Show Analysis & Navigation",
                "Tab 5 holds 16 traces (12 lectures + 4 assignments). \"Show Analysis\" explains DCF/RI methodology and terminal value limits. "
                "Footer provides \"← Back to Slide 9–14\" (returns to whichever slide you jumped from!) and A1–A6 quick-jump pills.",
            ],
        ],
    },
]


def build_doc():
    doc = Document()

    # Page setup: clean 0.65 in margins so tables and popup walkthroughs fit comfortably
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    # Top Title Banner
    p0 = doc.add_paragraph()
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    add_run(p0, "MMAT613 FINANCIAL STATEMENT ANALYSIS  |  PRESENTATION SPEAKER NOTES", bold=True, size=9.5, color=EMERALD)

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    add_run(p1, "PT GoTo Gojek Tokopedia Tbk (IDX: GOTO)\n", bold=True, size=17, color=NAVY)
    add_run(p1, "Complete 20-Slide Presenter Script, Full Popup Walkthrough & Q&A Guide", bold=True, size=12, color=SLATE)

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(8)
    add_run(
        p2,
        "Group 4: Fagly Ramschie, Anggreini Ruitan, Galatia Rompas  |  Magister Manajemen, Universitas Klabat  |  Covers Main Slides 1–14 + Appendix A1–A6 (Slides 15–20)",
        size=9.5,
        color=MUTED,
    )

    # Section 0: How to Use Interactive Slides and Popups (complete top-to-bottom guide)
    add_callout_box(
        doc,
        "HOW TO USE THE INTERACTIVE SLIDES AND POPUPS (READ THIS FIRST)",
        [
            "1. Speak naturally like you are explaining to a friend. You do not need to memorize every word — use the Key Numbers and Popup Walkthrough tables as live stage cues.",
            "2. Top Switcher Bar (Slides 4, 5, 6, 7, 8, 10, 11, 12): Slides open on \"Original Deck\" (amber). Click \"Final Report (Restated)\" (green) to show the clean post-Tokopedia numbers. On Slides 5, 7, 8, 10, and 13, the in-popup chart toggle (\"Previous Report (With 2023)\" vs. \"Current Report (Post-Exit)\") stays automatically synced with this top bar!",
            "3. Live Slide Dropdowns: Slide 8 has a \"Scenario:\" dropdown (Base, Optimistic, Conservative, plus 2-Yr Avg in Original mode) right above its table. Slides 10 & 11 have a \"Base Basis:\" (3-Yr vs. 2-Yr Avg) selector in Original mode.",
            "4. Clicking Any Row, Card, Chart, or Analysis Point Opens the Glass Popup (Modal) — Here Is Every Item Inside from Top to Bottom:",
            "   • Popup Header: Shows Slide Pill (SLIDE X · Section Tag), Clicked Item Title, automatic Abbreviation Subtitle, Metric Value Pill, and Close (× / Esc).",
            "   • Top Icon Tab Bar (Left): (1) Charts & Data (bar-chart icon) — SVG bars, YoY trajectory cards, plus slide-specific widgets (Slide 5 dual views, Slide 7 Pro Forma + Assumptions table, Slide 9 6-step walkthrough, Slide 10 sensitivity tables, Slide 11 7-bar Football Field + Matrix); (2) Pre vs. Post Exit / Prior vs. Restated (arrows icon — active on Slides 2, 4, 5, 6, 7, 8, 9–13); (3) Calculations & Formula (calculator icon — KaTeX formula, step-by-step math, origin, and Slide Calculation Table with \"View more\"); (4) Schedules & Proof (document icon — clickable Audited Financial Statement screenshot zoom + collapsible Supporting Schedules); (5) Workbook & Lectures (link icon — direct \"Open →\" jump cards to Excel sheets & lecture slides).",
            "   • Top Bar (Right): \"Appendix A1–A6 ↗\" jumps straight to the matching Appendix slide (Slides 15–20); \"Show Analysis\" opens the separate right-side \"Executive Takeaway & Analysis\" panel (with a \"View more\" button; hidden on Slide 9 because Tab 1 already shows the 6-step layout).",
            "   • Bottom Strip Inside Popup: \"Terms:\" automatically defines up to 8 financial abbreviations shown in the current popup.",
            "5. Appendix Navigation (Slides 15–20): Every Appendix slide includes \"← Back to Slide X\" (returns to the exact slide you jumped from) plus A1–A6 quick-jump pills in the bottom right.",
        ],
        fill_hex=HEX_GUIDE_BG,
        border_hex=HEX_GUIDE_BORDER,
        title_color=NAVY,
    )

    # Part 1: Main Deck Slides 1-14
    p_part1 = doc.add_paragraph()
    p_part1.paragraph_format.space_before = Pt(4)
    p_part1.paragraph_format.space_after = Pt(6)
    add_run(p_part1, "PART 1: MAIN PRESENTATION DECK (SLIDES 1 TO 14)", bold=True, size=13, color=NAVY)

    slide_fig_meta = [
        ("slide_01.png", "Slide 1 — GoTo Equity Analysis (Opening)", []),
        ("slide_02.png", "Slide 2 — Business Model", [("popup_02.png", "Slide 2 Popup — Gojek Segment EBIT Bridge (FY24 → FY25) & YoY Segment Cards")]),
        ("slide_03.png", "Slide 3 — Industry and Competition", [("popup_03.png", "Slide 3 Popup — Competitive Rivalry Cost & Credit Provision Burden")]),
        ("slide_04.png", "Slide 4 — Profitability and DuPont (Final Report Restated)", [("popup_04.png", "Slide 4 Popup — DuPont ROE Trajectory vs. Grab Peer & YoY Cards")]),
        ("slide_05.png", "Slide 5 — Liquidity and Z-Score (Final Report Restated)", [
            ("popup_05a.png", "Slide 5 Popup (View A) — Liquidity & Working Capital Vertical Balance-Sheet Ratio Cards"),
            ("popup_05b.png", "Slide 5 Popup (View B) — Altman Z-Score Weighted Factor Breakdown (−4.72 / −4.80)"),
        ]),
        ("slide_06.png", "Slide 6 — Cash Flow and Accounting Quality (Final Report Restated)", [("popup_06.png", "Slide 6 Popup — FY2025 Free Cash Flow Bridge & CapEx Normalization")]),
        ("slide_07.png", "Slide 7 — Forecast Assumptions (Final Report Restated)", [("popup_07.png", "Slide 7 Popup — Base Case Drivers, Pro Forma Outcomes & Hoverable Table 11")]),
        ("slide_08.png", "Slide 8 — Three-Year Forecast (Final Report Restated)", [("popup_08.png", "Slide 8 Popup — 2026F–2028F Scenarios & Restated Forecast Trajectory Cards")]),
        ("slide_09.png", "Slide 9 — Cost of Capital", [("popup_09.png", "Slide 9 Popup — Interactive 6-Step Cost of Capital Walkthrough (WACC 7.761%)")]),
        ("slide_10.png", "Slide 10 — DCF and Residual Income (Final Report Restated)", [("popup_10.png", "Slide 10 Popup — Restated DCF (+Rp 10.38) & RI (−Rp 12.23) + Sensitivity Tables")]),
        ("slide_11.png", "Slide 11 — Grab Comparison and Valuation (Final Report Restated)", [("popup_11.png", "Slide 11 Popup — Valuation Football Field vs. Market Rp 25.00 & Breakdown Cards")]),
        ("slide_12.png", "Slide 12 — Recommendation (Final Report Restated)", [("popup_12.png", "Slide 12 Popup — Economic Return Spread (ROIC vs. WACC) & Valuation Gap")]),
        ("slide_13.png", "Slide 13 — Forensic Restatement: 5 Mistakes Corrected", [("popup_13.png", "Slide 13 Popup — Current Final Report Audited Figures After 5 Fixes")]),
        ("slide_14.png", "Slide 14 — Old Deck vs. Final Report: Why SELL Still Holds", [("popup_14.png", "Slide 14 Popup — Economic Return Spread (2.70% ROIC vs. 7.76% WACC)")]),
    ]
    apx_fig_meta = [
        ("slide_15.png", "Slide 15 (Appendix A1) — Revenue Bridge & Competitive Risk Schedules", [("popup_15.png", "Appendix A1 Popup — Revenue Bridge Metrics Overview")]),
        ("slide_16.png", "Slide 16 (Appendix A2) — Historical & Pro Forma Summary (FY2023–2028F) & DuPont", [("popup_16.png", "Appendix A2 Popup — Profitability & DuPont Metrics Overview")]),
        ("slide_17.png", "Slide 17 (Appendix A3) — Liquidity, Working Capital, Week 6 Z-Score & Footnotes", [("popup_17.png", "Appendix A3 Popup — Liquidity & Z-Score Metrics Overview")]),
        ("slide_18.png", "Slide 18 (Appendix A4) — Scenario Drivers, Forecast Rationales & Cost Behavior", [("popup_18.png", "Appendix A4 Popup — Forecast Drivers Overview")]),
        ("slide_19.png", "Slide 19 (Appendix A5) — Three-Year Pro Forma Statements & Operating Leverage", [("popup_19.png", "Appendix A5 Popup — Pro Forma & Breakeven Metrics Overview")]),
        ("slide_20.png", "Slide 20 (Appendix A6) — Dated WACC, DCF, Residual Income & FY2025 Grab P/B Schedules", [("popup_20.png", "Appendix A6 Popup — Valuation & Cost of Capital Metrics Overview")]),
    ]

    fig_counter = [1]
    for s, (sf, sc, pfs) in zip(MAIN_SLIDES, slide_fig_meta):
        s_with_figs = {**s, "slide_fig": (sf, sc), "popup_figs": pfs}
        add_slide_block(doc, s_with_figs, fig_counter, is_appendix=False)

    # Part 2: Appendix Deck Slides 15-20 (A1-A6)
    p_part2 = doc.add_paragraph()
    p_part2.paragraph_format.space_before = Pt(8)
    p_part2.paragraph_format.space_after = Pt(6)
    add_run(p_part2, "PART 2: APPENDIX SUPPORTING SLIDES (SLIDES 15 TO 20 — APPENDIX A1 THROUGH A6)", bold=True, size=13, color=EMERALD)

    p_part2_note = doc.add_paragraph()
    p_part2_note.paragraph_format.space_before = Pt(0)
    p_part2_note.paragraph_format.space_after = Pt(6)
    add_run(
        p_part2_note,
        "Note: Appendix A1–A6 are not presented linearly during the main 20-minute talk unless asked, OR you can jump directly to any of them "
        "during Q&A by clicking the \"Appendix A1–A6 ↗\" pill on the slide or inside any popup, then click \"← Back to Slide X\" to return immediately.",
        italic=True,
        size=9.5,
        color=SLATE,
    )

    for s, (sf, sc, pfs) in zip(APPENDIX_SLIDES, apx_fig_meta):
        s_with_figs = {**s, "slide_fig": (sf, sc), "popup_figs": pfs}
        add_slide_block(doc, s_with_figs, fig_counter, is_appendix=True)

    # Part 3: Quick Q&A Cheat Sheet
    add_section_banner(doc, "PART 3: QUICK Q&A CHEAT SHEET (TOP 7 QUESTIONS & EASY ANSWERS)", bg_hex=HEX_NAVY)
    p_qa_sp = doc.add_paragraph()
    p_qa_sp.paragraph_format.space_before = Pt(2)
    p_qa_sp.paragraph_format.space_after = Pt(2)

    qa_rows = [
        [
            "1. Why did your DCF jump from −Rp 121 to +Rp 10.38?",
            "Our old draft accidentally averaged 2023 pre-Tokopedia costs (117% OpEx) and Rp 5.46T of one-time Tokopedia intangibles inside 2024 CapEx. "
            "Once we removed 2023 and focused on the real 2024–2025 Gojek + GoPay business, DCF turned positive at +Rp 10.38 per share.",
            "Slides 13–14 / Appendix A6",
        ],
        [
            "2. If GoTo turns net-profitable in 2028F (+Rp 25B), why still SELL?",
            "Accounting profit is not the same as economic profit. Even in 2028F, GoTo ROIC (+2.70%) is still 506 bps below its 7.76% WACC, "
            "and ROE (+0.09%) is far below its 8.45% Cost of Equity.",
            "Slides 8, 12 & 14 / Appendix A5",
        ],
        [
            "3. Why did you reject Grab P/B multiple (Rp 91.02)?",
            "Grab already earns positive ROE (+2.96%) and positive EBIT, while GoTo still has negative ROE (−5.23%) and negative EBIT. "
            "Giving a loss-making company a profitable peer's 3.04x P/B multiple is not economically valid.",
            "Slide 11 / Appendix A6",
        ],
        [
            "4. Why did you not average 2024 OpEx (62.8%) with 2025 (55.7%)?",
            "2024 was a transition year. GoTo sold PAB logistics in May 2024, exited Vietnam in September 2024, and finished its >50% cloud savings in 2025. "
            "So 2025 (55.7%) is the true current run-rate, while 2024 (62.8%) is our Conservative Case floor.",
            "Slide 7 / Appendix A4",
        ],
        [
            "5. Why is Altman Z-Score −4.72 if GoTo has Rp 21.76T cash?",
            "The Z-Score is pulled down almost entirely by X2 (Accumulated Deficit = −Rp 215.3T), which comes from sunk 2023 goodwill write-offs "
            "(Rp 73.2T Tokopedia + Rp 5.5T delivery). Liquidity (X1 = +0.48 weighted) and solvency (X4 = +1.01 weighted) are both healthy.",
            "Slide 5 / Appendix A3",
        ],
        [
            "6. Why did you add back goodwill & JV impairment in Accounting Quality?",
            "To separate one-time non-cash paper write-downs from GoTo's core day-to-day business and compute before/after accrual ratios. "
            "Even after adding back every write-down, core recurring net income was still −Rp 580B in 2025.",
            "Slide 6 / Appendix A3",
        ],
        [
            "7. What would make you upgrade GOTO from SELL to HOLD or BUY?",
            "Upgrade to HOLD if price drops to ≤ Rp 13.20 (1.0x Net Cash) with positive FCF. Upgrade to BUY if GoTo sustains 1H 2026 cost efficiency "
            "(Cash OpEx ≤ 51.2% and Gross Margin ≥ 61.9%) for two straight quarters.",
            "Slide 12 / Appendix A6",
        ],
    ]
    add_styled_table(doc, ["Likely Question", "Easy 1–2 Sentence Answer", "Jump To"], qa_rows, [2.0, 3.85, 1.15])

    # Part 4: Quick Abbreviation Cheat Sheet
    add_section_banner(doc, "PART 4: QUICK ABBREVIATION CHEAT SHEET (IN CASE YOU BLANK ON STAGE)", bg_hex=HEX_NAVY)
    p_ab_sp = doc.add_paragraph()
    p_ab_sp.paragraph_format.space_before = Pt(2)
    p_ab_sp.paragraph_format.space_after = Pt(2)

    abbr_rows = [
        ["BVPS", "Book Value Per Share (Parent Equity / Shares = Rp 29.95)"],
        ["P/B", "Price-to-Book Ratio (Share Price / BVPS; Grab = 3.04x)"],
        ["DCF", "Discounted Cash Flow (Today's value of future Free Cash Flows = +Rp 10.38/sh)"],
        ["RI", "Residual Income / Economic Profit (Profit above or below Cost of Equity = −Rp 12.23/sh)"],
        ["WACC", "Weighted Average Cost of Capital (Blended cost of equity & debt = 7.76%)"],
        ["Ke / Kd / Rf", "Cost of Equity (8.45%) / Cost of Debt (5.39% after-tax) / IDR Risk-Free Rate (4.502%)"],
        ["ERP / CRP", "Mature-Market Equity Risk Premium (4.23%) / Indonesia Country Risk Premium (2.465%)"],
        ["NOPAT", "Net Operating Profit After Tax (EBIT × (1 − 22% tax) = +Rp 442.4B in 2028F)"],
        ["FCFF", "Free Cash Flow to Firm (Cash left after taxes, working capital, and CapEx)"],
        ["CFO / FCF", "Operating Cash Flow (+Rp 307B) / Free Cash Flow (CFO − CapEx = −Rp 875B)"],
        ["ROIC / ROE", "Return on Invested Capital (2.70% in 2028F) / Return on Equity (−5.23% in 2025)"],
        ["EBIT", "Earnings Before Interest & Taxes (Operating Profit = −Rp 378B in 2025; +Rp 567B in 2028F)"],
        ["COGS / OpEx / CapEx", "Cost of Goods Sold / Operating Expenses / Capital Expenditures"],
        ["DSO / DPO / CCC", "Days Sales Outstanding (10.9d) / Days Payable (59.1d) / Cash Conversion Cycle (−47.5d)"],
        ["TIE / DOL", "Times Interest Earned (−0.71x) / Degree of Operating Leverage (28.56x in 2026F)"],
        ["PSAK / IFRS", "Indonesian Financial Accounting Standards (aligned with IFRS; basis of GoTo's audited statements)"],
    ]
    add_styled_table(doc, ["Abbreviation", "Full Term & Simple Meaning"], abbr_rows, [1.6, 5.4])

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_doc()
