"""Regenerate audited statement evidence PNGs with 1-to-1 color-matched callout cards."""

import os
from pathlib import Path
import fitz
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
OUT_DIR = ROOT / "goto-fsa-study/public/evidence"

DPI = 200
SCALE = DPI / 72.0
SIDEBAR_W = 520

PALETTES = {
    "green": {
        "box_fill": (34, 197, 94, 85),
        "box_outline": (22, 163, 74, 255),
        "row_tint": (34, 197, 94, 38),
        "card_bg": (240, 253, 244),
        "card_border": (134, 239, 172),
        "badge": (22, 163, 74),
        "text_dark": (21, 128, 61),
        "line": (22, 163, 74),
    },
    "blue": {
        "box_fill": (59, 130, 246, 80),
        "box_outline": (37, 99, 235, 255),
        "row_tint": (59, 130, 246, 35),
        "card_bg": (239, 246, 255),
        "card_border": (147, 197, 253),
        "badge": (37, 99, 235),
        "text_dark": (29, 78, 216),
        "line": (37, 99, 235),
    },
    "orange": {
        "box_fill": (245, 158, 11, 80),
        "box_outline": (217, 119, 6, 255),
        "row_tint": (245, 158, 11, 38),
        "card_bg": (255, 251, 235),
        "card_border": (253, 186, 116),
        "badge": (217, 119, 6),
        "text_dark": (180, 83, 9),
        "line": (217, 119, 6),
    },
    "red": {
        "box_fill": (239, 68, 68, 85),
        "box_outline": (220, 38, 38, 255),
        "row_tint": (239, 68, 68, 38),
        "card_bg": (254, 242, 242),
        "card_border": (252, 165, 165),
        "badge": (220, 38, 38),
        "text_dark": (185, 28, 28),
        "line": (220, 38, 38),
    },
}

FONT_TITLE = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 21)
FONT_SUB = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
FONT_TAG = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 12)
FONT_CARD_HEAD = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 14)
FONT_BIG = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 31)
FONT_BODY = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
FONT_FOOTER = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)


def find_rect(page, term, target_y=None, target_x=None):
    rects = page.search_for(term)
    if not rects:
        raise ValueError(f"Term {term!r} not found on page {page.number + 1}")
    if target_y is not None:
        rects = [r for r in rects if abs(r.y0 - target_y) < 4.5]
    if target_x is not None:
        rects = [r for r in rects if abs(r.x0 - target_x) < 6.0]
    if not rects:
        raise ValueError(
            f"Term {term!r} not found near y={target_y}, x={target_x} on page {page.number + 1}"
        )
    return rects[0]


def draw_highlight_box(draw_overlay, rect, pal, row_tint_x=None):
    x0, y0, x1, y1 = (
        rect.x0 * SCALE - 5,
        rect.y0 * SCALE - 2,
        rect.x1 * SCALE + 5,
        rect.y1 * SCALE + 2,
    )
    if row_tint_x is not None:
        lx0, lx1 = row_tint_x[0] * SCALE, row_tint_x[1] * SCALE
        draw_overlay.rounded_rectangle(
            [lx0, y0, lx1, y1], radius=4, fill=pal["row_tint"]
        )
    draw_overlay.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=4,
        fill=pal["box_fill"],
        outline=pal["box_outline"],
        width=3,
    )
    return (x0, y0, x1, y1)


def draw_card(draw, sb_x, sb_w, y, h, pal, badge, title, big_num, line1, line2, footer):
    draw.rounded_rectangle(
        [sb_x, y, sb_x + sb_w, y + h],
        radius=10,
        fill=pal["card_bg"],
        outline=pal["card_border"],
        width=2,
    )
    draw.rounded_rectangle(
        [sb_x + 14, y + 12, sb_x + 114, y + 34],
        radius=5,
        fill=pal["badge"],
    )
    draw.text((sb_x + 22, y + 16), badge, font=FONT_TAG, fill=(255, 255, 255))
    draw.text((sb_x + 124, y + 16), title, font=FONT_CARD_HEAD, fill=pal["text_dark"])
    draw.text((sb_x + 14, y + 40), big_num, font=FONT_BIG, fill=pal["text_dark"])
    draw.text((sb_x + 14, y + 82), line1, font=FONT_BODY, fill=(51, 65, 85))
    draw.text((sb_x + 14, y + 102), line2, font=FONT_BODY, fill=(51, 65, 85))
    draw.line(
        [(sb_x + 14, y + h - 32), (sb_x + sb_w - 14, y + h - 32)],
        fill=pal["card_border"],
        width=1,
    )
    draw.text((sb_x + 14, y + h - 25), footer, font=FONT_FOOTER, fill=pal["text_dark"])
    return y + 54


def draw_orthogonal_connectors(draw, dot_points, bus_x, sb_x, target_y, color):
    dot_x = dot_points[0][0]
    ys = [p[1] for p in dot_points]
    for dx, dy in dot_points:
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=color)
        draw.line([(dx, dy), (bus_x, dy)], fill=color, width=2)
    min_y = min(min(ys), target_y)
    max_y = max(max(ys), target_y)
    draw.line([(bus_x, min_y), (bus_x, max_y)], fill=color, width=2)
    draw.line([(bus_x, target_y), (sb_x - 6, target_y)], fill=color, width=2)
    draw.polygon(
        [(sb_x, target_y), (sb_x - 9, target_y - 5), (sb_x - 9, target_y + 5)],
        fill=color,
    )


def prepare_canvas(doc, page_num):
    page = doc[page_num - 1]
    pix = page.get_pixmap(dpi=DPI)
    base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    total_w = base_img.width + SIDEBAR_W
    total_h = base_img.height
    canvas = Image.new("RGB", (total_w, total_h), (248, 250, 252))
    canvas.paste(base_img, (0, 0))
    overlay = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 0))
    return page, base_img, canvas, overlay


def render_portrait_page(doc, spec):
    page, base_img, canvas, overlay = prepare_canvas(doc, spec["page"])
    draw_ov = ImageDraw.Draw(overlay)
    sb_x = base_img.width + 24
    sb_w = SIDEBAR_W - 48
    dot_x = int(555 * SCALE)

    group_dots = []
    for g in spec["groups"]:
        pal = PALETTES[g["color"]]
        dots = []
        for box in g["boxes"]:
            term, ty, tx = box[0], box[1], box[2]
            skip_tint = box[3] if len(box) > 3 else False
            rect = find_rect(page, term, target_y=ty, target_x=tx)
            draw_highlight_box(
                draw_ov,
                rect,
                pal,
                row_tint_x=None if skip_tint else spec.get("row_tint_x"),
            )
            dots.append((dot_x, int((rect.y0 + rect.y1) * 0.5 * SCALE)))
        group_dots.append(dots)

    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    draw.line(
        [(base_img.width, 0), (base_img.width, base_img.height)],
        fill=(203, 213, 225),
        width=2,
    )

    for hx, hy, htitle, hsub in spec["headers"]:
        draw.text((sb_x, hy), htitle, font=FONT_TITLE, fill=(15, 23, 42))
        draw.text((sb_x, hy + 28), hsub, font=FONT_SUB, fill=(100, 116, 139))

    bus_offsets = [44, 34, 24, 14]
    for idx, g in enumerate(spec["groups"]):
        pal = PALETTES[g["color"]]
        target_y = draw_card(
            draw,
            sb_x,
            sb_w,
            g["card_y"],
            g.get("card_h", 156),
            pal,
            g["badge"],
            g["title"],
            g["big"],
            g["line1"],
            g["line2"],
            g["footer"],
        )
        if "custom_connector" in g:
            g["custom_connector"](draw, page, base_img, sb_x, target_y, pal["line"])
        else:
            bus_x = base_img.width - bus_offsets[idx % len(bus_offsets)]
            draw_orthogonal_connectors(
                draw, group_dots[idx], bus_x, sb_x, target_y, pal["line"]
            )

    out_path = OUT_DIR / spec["filename"]
    canvas.save(out_path, "PNG", quality=95)
    print(f"Saved {spec['filename']} ({canvas.size[0]}x{canvas.size[1]})")

    if "crop" in spec:
        c = spec["crop"]
        crop_box = (
            c["x0"],
            int(c["y0_pt"] * SCALE),
            canvas.size[0],
            int(c["y1_pt"] * SCALE),
        )
        cropped = canvas.crop(crop_box)
        crop_path = OUT_DIR / c["filename"]
        cropped.save(crop_path, "PNG", quality=95)
        print(f"Saved {c['filename']} ({cropped.size[0]}x{cropped.size[1]})")


def note34_red_connector(draw, page, base_img, sb_x, target_y, color):
    rect = find_rect(page, "(356,830)", target_y=330.2)
    cx = int((rect.x0 + rect.x1) * 0.5 * SCALE)
    by = int(rect.y1 * SCALE) + 3
    lane_y = int(361 * SCALE)
    bus_x = base_img.width - 34
    draw.ellipse([cx - 4, by - 4, cx + 4, by + 4], fill=color)
    draw.line([(cx, by), (cx, lane_y)], fill=color, width=2)
    draw.line([(cx, lane_y), (bus_x, lane_y)], fill=color, width=2)
    draw.line([(bus_x, lane_y), (bus_x, target_y)], fill=color, width=2)
    draw.line([(bus_x, target_y), (sb_x - 6, target_y)], fill=color, width=2)
    draw.polygon(
        [(sb_x, target_y), (sb_x - 9, target_y - 5), (sb_x - 9, target_y + 5)],
        fill=color,
    )


def render_page133_segment_note29(doc):
    page, base_img, canvas, overlay = prepare_canvas(doc, 133)
    draw_ov = ImageDraw.Draw(overlay)
    sb_x = base_img.width + 24
    sb_w = SIDEBAR_W - 48
    target_row_y = 321.0

    groups = [
        {
            "color": "green",
            "boxes": [("12,361,259", target_row_y, None)],
            "card_y": 320,
            "badge": "HIGHLIGHT 1",
            "title": "GOJEK (ON-DEMAND SERVICES)",
            "big": "Rp 12,361.3 bn",
            "line1": "Gross 3rd-party Rp 15,031.0 bn - Incentives (Rp 2,669.7 bn)",
            "line2": "Operating engine #1; segment operating profit +Rp 888.6 bn",
            "footer": "= Net Third-Party ODS Revenue: Rp 12,361,259 mn",
            "lane_y": int(333 * SCALE),
            "bus_x": base_img.width - 18,
        },
        {
            "color": "blue",
            "boxes": [("5,190,617", target_row_y, None)],
            "card_y": 506,
            "badge": "HIGHLIGHT 2",
            "title": "GOTO FINANCIAL (FINTECH)",
            "big": "Rp 5,190.6 bn",
            "line1": "Gross 3rd-party Rp 5,460.8 bn - Incentives (Rp 270.2 bn)",
            "line2": "Operating engine #2 (rounded Rp 5,191 bn on slide)",
            "footer": "= Net Third-Party FinTech Revenue: Rp 5,190,617 mn",
            "lane_y": int(336.5 * SCALE),
            "bus_x": base_img.width - 30,
        },
        {
            "color": "orange",
            "boxes": [
                ("819,724", target_row_y, None),
                ("(49,483)", target_row_y, None),
            ],
            "card_y": 692,
            "badge": "HIGHLIGHT 3",
            "title": "TOKOPEDIA FEE & ELIMINATION",
            "big": "+819.7 / -49.5 bn",
            "line1": "Passive e-commerce service fee from Tokopedia: Rp 819,724 mn",
            "line2": "Cross-platform promo elimination: -(Rp 49,483 mn)",
            "footer": "= Reconciles Standalone Segments to Consolidated Total",
            "lane_y": int(340 * SCALE),
            "bus_x": base_img.width - 42,
        },
        {
            "color": "red",
            "boxes": [("18,322,117", target_row_y, None)],
            "card_y": 878,
            "badge": "HIGHLIGHT 4",
            "title": "CONSOLIDATED NET REVENUE",
            "big": "Rp 18,322.1 bn",
            "line1": "12,361.26 + 5,190.62 + 819.72 - 49.48 = Rp 18,322.12 bn",
            "line2": "Ties directly to Consolidated Income Statement top line",
            "footer": "= Audited FY2025 Net Revenue: Rp 18,322,117 mn",
            "lane_y": int(343.5 * SCALE),
            "bus_x": base_img.width - 54,
        },
    ]

    box_centers = []
    for g in groups:
        pal = PALETTES[g["color"]]
        pts = []
        for term, ty, tx in g["boxes"]:
            rect = find_rect(page, term, target_y=ty, target_x=tx)
            draw_highlight_box(draw_ov, rect, pal, row_tint_x=None)
            pts.append((int((rect.x0 + rect.x1) * 0.5 * SCALE), int(rect.y1 * SCALE) + 3))
        box_centers.append(pts)

    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    draw.line(
        [(base_img.width, 0), (base_img.width, base_img.height)],
        fill=(203, 213, 225),
        width=2,
    )
    draw.text((sb_x, 224), "AUDITED RECONCILIATION", font=FONT_TITLE, fill=(15, 23, 42))
    draw.text(
        (sb_x, 252),
        "NOTE 29: SEGMENT OPERATIONS (Annual Report p. 468 / LK p. 133)",
        font=FONT_SUB,
        fill=(100, 116, 139),
    )

    for idx, g in enumerate(groups):
        pal = PALETTES[g["color"]]
        target_y = draw_card(
            draw,
            sb_x,
            sb_w,
            g["card_y"],
            162,
            pal,
            g["badge"],
            g["title"],
            g["big"],
            g["line1"],
            g["line2"],
            g["footer"],
        )
        lane_y = g["lane_y"]
        bus_x = g["bus_x"]
        c = pal["line"]
        for cx, by in box_centers[idx]:
            draw.ellipse([cx - 4, by - 4, cx + 4, by + 4], fill=c)
            draw.line([(cx, by), (cx, lane_y)], fill=c, width=2)
        min_x = min(cx for cx, _ in box_centers[idx])
        draw.line([(min_x, lane_y), (bus_x, lane_y)], fill=c, width=2)
        draw.line([(bus_x, lane_y), (bus_x, target_y)], fill=c, width=2)
        draw.line([(bus_x, target_y), (sb_x - 6, target_y)], fill=c, width=2)
        draw.polygon(
            [(sb_x, target_y), (sb_x - 9, target_y - 5), (sb_x - 9, target_y + 5)],
            fill=c,
        )

    out_path = OUT_DIR / "annual_report_p468_segment_note29.png"
    canvas.save(out_path, "PNG", quality=95)
    print(f"Saved annual_report_p468_segment_note29.png ({canvas.size[0]}x{canvas.size[1]})")


PORTRAIT_SPECS = [
    {
        "page": 15,
        "filename": "goto_balance_sheet_assets_highlighted.png",
        "row_tint_x": (66, 224),
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "BALANCE SHEET ASSETS (LK p. 15)"),
        ],
        "groups": [
            {
                "color": "green",
                "boxes": [("21,755,165", 209.3, None)],
                "card_y": 465,
                "badge": "HIGHLIGHT 1",
                "title": "CASH & EQUIVALENTS",
                "big": "Rp 21,755.2 bn",
                "line1": "Cash and cash equivalents (Note 4): Rp 21,755,165 mn",
                "line2": "47.5% of Total Assets; Net Cash = +Rp 14,012.5 bn",
                "footer": "= Cash Buffer Before Forecast Burn: Rp 21,755.2 bn",
            },
            {
                "color": "blue",
                "boxes": [("2,730,813", 273.7, None), ("29,059,226", 384.1, None)],
                "card_y": 700,
                "badge": "HIGHLIGHT 2",
                "title": "CONSUMER LOANS & CURRENT ASSETS",
                "big": "Rp 2,730.8 bn",
                "line1": "Net consumer loans (Note 7): Rp 2,730,813 mn (+72.6% YoY)",
                "line2": "Total current assets: Rp 29,059,226 mn (Current Ratio 2.73x)",
                "footer": "= Lending Expansion Adds Credit-Loss Exposure",
            },
            {
                "color": "orange",
                "boxes": [("10,594,799", 439.3, None), ("45,757,642", 522.1, None)],
                "card_y": 1160,
                "badge": "HIGHLIGHT 3",
                "title": "ASSOCIATES & TOTAL ASSETS",
                "big": "Rp 45,757.6 bn",
                "line1": "Investments in associates (Note 14): Rp 10,594,799 mn",
                "line2": "Tokopedia (7,432.3) + Bank Jago (2,894.9) = 22.57% of Assets",
                "footer": "= Total Consolidated Assets: Rp 45,757,642 mn",
            },
        ],
    },
    {
        "page": 16,
        "filename": "goto_balance_sheet_liabilities_equity_highlighted.png",
        "row_tint_x": (66, 224),
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "LIABILITIES & DEBT BASE (LK p. 16)"),
            (0, 1435, "EQUITY & DEFICIT AUDIT", "PT GoTo Gojek Tokopedia Tbk (LK p. 16)"),
        ],
        "groups": [
            {
                "color": "orange",
                "boxes": [
                    ("1,001,625", 328.9, None),
                    ("318,389", 356.5, None),
                    ("137,475", 365.7, None),
                    ("66,269", 375.0, None),
                    ("3,343,953", 448.6, None),
                    ("2,785,644", 457.7, None),
                    ("89,288", 466.9, None),
                ],
                "card_y": 890,
                "badge": "HIGHLIGHT 1",
                "title": "TOTAL DEBT & LEASES",
                "big": "Rp 7,742.6 bn",
                "line1": "ST Debt & Leases: Rp 1,523.8 bn | LT Debt & Leases: Rp 6,218.9 bn",
                "line2": "Total Interest-Bearing Debt: Rp 7,742,643 mn (WACC weight 22.6%)",
                "footer": "= Net Cash Position: +Rp 14,012.5 bn",
            },
            {
                "color": "red",
                "boxes": [("(215,334,000)", 660.1, None)],
                "card_y": 1525,
                "badge": "HIGHLIGHT 2",
                "title": "ACCUMULATED DEFICIT (X2)",
                "big": "-(Rp 215.3T)",
                "line1": "FY2025 Accumulated Deficit: -(Rp 215,334,000 mn)",
                "line2": "Drives Altman Z-Score X2 penalty (-6.59) and Z = -4.72",
                "footer": "= Cumulative Historical Losses Since Inception",
            },
            {
                "color": "green",
                "boxes": [("31,805,025", 678.5, None, True), ("28,711,657", 715.3, None)],
                "card_y": 1730,
                "badge": "HIGHLIGHT 3",
                "title": "PARENT & TOTAL EQUITY",
                "big": "Rp 28,711.7 bn",
                "line1": "Parent Equity: Rp 31,805,025 mn (BVPS Rp 29.95 / 1,062.01B sh)",
                "line2": "Total Consolidated Equity: Rp 28,711,657 mn",
                "footer": "= Residual Income Year-0 Anchor: Rp 28,711.7 bn",
            },
        ],
        "crop": {
            "filename": "goto_equity_deficit_highlighted.png",
            "x0": 140,
            "y0_pt": 480,
            "y1_pt": 760,
        },
    },
    {
        "page": 21,
        "filename": "goto_cash_flows_p1_highlighted.png",
        "row_tint_x": (66, 224),
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "CASH FLOWS PART 1 (LK p. 21)"),
        ],
        "groups": [
            {
                "color": "green",
                "boxes": [
                    ("20,931,399", 190.4, None),
                    ("500,270", 309.9, None),
                    ("307,025", 374.4, None),
                ],
                "card_y": 540,
                "badge": "HIGHLIGHT 1",
                "title": "OPERATING CASH FLOW (CFO)",
                "big": "+Rp 307.0 bn",
                "line1": "Cash generated from operations: +Rp 500,270 mn",
                "line2": "Net Operating Cash Flow (after tax/interest): +Rp 307,025 mn",
                "footer": "= Positive Headline CFO (+Rp 307.2 bn in M3)",
            },
            {
                "color": "orange",
                "boxes": [("(880,289)", 402.0, None), ("(302,071)", 411.1, None)],
                "card_y": 1060,
                "badge": "HIGHLIGHT 2",
                "title": "CAPEX & FREE CASH FLOW",
                "big": "-(Rp 1,182.4 bn)",
                "line1": "Intangible Capex (880.3 bn) + Fixed Capex (302.1 bn)",
                "line2": "CFO (+307.0 bn) covers only 26.0% of total Capex",
                "footer": "= Free Cash Flow Shortfall: -Rp 875.3 bn",
            },
            {
                "color": "blue",
                "boxes": [("1,386,520", 576.7, None)],
                "card_y": 1520,
                "badge": "HIGHLIGHT 3",
                "title": "TIME DEPOSIT LIQUIDATION",
                "big": "+Rp 1,386.5 bn",
                "line1": "Settlement of time deposits, net: +Rp 1,386,520 mn",
                "line2": "Non-operating liquidity drawdown supporting cash",
                "footer": "= Masks Underlying Operating-to-Capex Deficit",
            },
        ],
    },
    {
        "page": 22,
        "filename": "goto_cash_flows_p2_highlighted.png",
        "row_tint_x": (66, 224),
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "CASH FLOWS PART 2 (LK p. 22)"),
        ],
        "groups": [
            {
                "color": "blue",
                "boxes": [("3,718,013", 211.3, None), ("(682,000)", 248.0, None)],
                "card_y": 540,
                "badge": "HIGHLIGHT 1",
                "title": "BANK LOAN DRAWDOWNS",
                "big": "+Rp 3,036.0 bn",
                "line1": "Proceeds from third-party loans: +Rp 3,718,013 mn",
                "line2": "Repayment of third-party loans: -(Rp 682,000 mn)",
                "footer": "= Net New Debt Financing Inflow",
            },
            {
                "color": "orange",
                "boxes": [("(971,404)", 349.2, None)],
                "card_y": 900,
                "badge": "HIGHLIGHT 2",
                "title": "TREASURY SHARE BUYBACKS",
                "big": "-(Rp 971.4 bn)",
                "line1": "Acquisition of treasury shares (Note 22): -(Rp 971,404 mn)",
                "line2": "Net cash provided by financing activities: +Rp 1,887,575 mn",
                "footer": "= Reduces Outstanding Share Count to 1,062.01B",
            },
            {
                "color": "green",
                "boxes": [
                    ("2,713,717", 422.9, None),
                    ("18,827,578", 450.5, 293.0),
                    ("21,755,165", 514.8, 293.0),
                ],
                "card_y": 1180,
                "badge": "HIGHLIGHT 3",
                "title": "ENDING CASH RECONCILIATION",
                "big": "Rp 21,755.2 bn",
                "line1": "Beginning Cash: Rp 18,827,578 mn + Net Increase: Rp 2,713,717 mn",
                "line2": "Plus FX effect (+Rp 213,870 mn) = Rp 21,755,165 mn",
                "footer": "= Matches Balance Sheet Cash (LK p. 15)",
            },
        ],
    },
    {
        "page": 100,
        "filename": "goto_note14_associates_tokopedia_jago.png",
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "NOTE 14: ASSOCIATES (LK p. 100)"),
        ],
        "groups": [
            {
                "color": "green",
                "boxes": [("24.99%", 249.5, 338.2), ("7,432,326", 249.5, None)],
                "card_y": 560,
                "badge": "HIGHLIGHT 1",
                "title": "PT TOKOPEDIA ASSOCIATE",
                "big": "24.99% Stake",
                "line1": "Retained equity-method stake after Feb 2024 TikTok deal",
                "line2": "FY2025 carrying value: Rp 7,432,326 mn (Rp 7.43T)",
                "footer": "= Generates Rp 819.7 bn E-Commerce Service Fee",
            },
            {
                "color": "blue",
                "boxes": [("21.40%", 325.3, 338.2), ("2,894,921", 325.3, None)],
                "card_y": 790,
                "badge": "HIGHLIGHT 2",
                "title": "PT BANK JAGO TBK ASSOCIATE",
                "big": "21.40% Stake",
                "line1": "Digital banking partner for GoPay consumer lending",
                "line2": "Carrying value: Rp 2,894,921 mn (IDX fair value Rp 5,857.3 bn)",
                "footer": "= Tokopedia + Jago = Rp 10,327.2 bn (22.57% of Assets)",
            },
            {
                "color": "orange",
                "boxes": [("10,594,799", 394.3, None)],
                "card_y": 1030,
                "badge": "HIGHLIGHT 3",
                "title": "TOTAL ASSOCIATES CARRYING VALUE",
                "big": "Rp 10,594.8 bn",
                "line1": "Tokopedia (7,432.3) + Bank Jago (2,894.9) + Others (267.6)",
                "line2": "Matches Balance Sheet Non-Current Associates line (LK p. 15)",
                "footer": "= Subject to Equity-Method & Impairment Testing",
            },
        ],
    },
    {
        "page": 105,
        "filename": "goto_note19_leases_audited.png",
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "NOTE 19: LEASES (LK p. 105)"),
        ],
        "groups": [
            {
                "color": "blue",
                "boxes": [("170,656", 336.9, None), ("(15,099)", 362.6, None)],
                "card_y": 820,
                "badge": "HIGHLIGHT 1",
                "title": "GROSS LEASE COMMITMENTS",
                "big": "Rp 170.7 bn",
                "line1": "Gross minimum lease payments: Rp 170,656 mn",
                "line2": "Less future finance charges on leases: -(Rp 15,099 mn)",
                "footer": "= Undiscounted Contractual Lease Outflows",
            },
            {
                "color": "green",
                "boxes": [
                    ("155,557", 379.7, None),
                    ("66,269", 430.9, None),
                    ("89,288", 448.1, None),
                ],
                "card_y": 1060,
                "badge": "HIGHLIGHT 2",
                "title": "PRESENT VALUE OF LEASE LIABILITIES",
                "big": "Rp 155.6 bn",
                "line1": "Current lease liabilities (<1 yr): Rp 66,269 mn",
                "line2": "Non-current lease liabilities (1-5 yrs): Rp 89,288 mn",
                "footer": "= Total Leases Rp 155,557 mn Included in Total Debt",
            },
        ],
    },
    {
        "page": 106,
        "filename": "goto_note20_borrowings_summary.png",
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "NOTE 20: BORROWINGS (LK p. 106)"),
        ],
        "groups": [
            {
                "color": "orange",
                "boxes": [("1,001,625", 261.0, None), ("1,001,625", 278.1, None)],
                "card_y": 640,
                "badge": "HIGHLIGHT 1",
                "title": "SHORT-TERM BANK BORROWINGS",
                "big": "Rp 1,001.6 bn",
                "line1": "Third-party short-term bank loans: Rp 1,001,625 mn",
                "line2": "Included in GoTo's Rp 7,742.6 bn total debt base",
                "footer": "= Working Capital Facility (MAB / Jago)",
            },
            {
                "color": "blue",
                "boxes": [("10.25%", 388.9, None), ("10.50%", 519.3, None)],
                "card_y": 1020,
                "badge": "HIGHLIGHT 2",
                "title": "COST OF DEBT (WACC INPUT)",
                "big": "5.39% After-Tax",
                "line1": "Facility contractual interest rates: 10.25% - 10.50% p.a.",
                "line2": "Effective FY2025 Pre-Tax Kd = 535,152 / 7,742,643 = 6.91%",
                "footer": "= After-Tax Kd: 6.91% x (1 - 22%) = 5.39%",
            },
        ],
    },
    {
        "page": 147,
        "filename": "goto_note34_goodwill_impairment.png",
        "headers": [
            (0, 390, "AUDITED RECONCILIATION", "NOTE 34: GOODWILL (LK p. 147)"),
        ],
        "groups": [
            {
                "color": "red",
                "boxes": [("(356,830)", 330.2, None)],
                "card_y": 640,
                "badge": "HIGHLIGHT 1",
                "title": "2025 FINTECH GOODWILL IMPAIRMENT",
                "big": "-(Rp 356.8 bn)",
                "line1": "FY2025 impairment on Midtrans Financial Technology CGU",
                "line2": "Charged to P&L based on Level-3 value-in-use discount model",
                "footer": "= Non-Cash Impairment Charge (Note 34a)",
                "custom_connector": note34_red_connector,
            },
            {
                "color": "green",
                "boxes": [("372,575", 330.2, None), ("15,745", 330.2, None)],
                "card_y": 840,
                "badge": "HIGHLIGHT 2",
                "title": "REMAINING GOODWILL BALANCE",
                "big": "Rp 15.7 bn",
                "line1": "Beginning 2025 FinTech goodwill: Rp 372,575 mn",
                "line2": "Less 2025 impairment -(Rp 356,830 mn) = Rp 15,745 mn",
                "footer": "= Matches Balance Sheet Goodwill (LK p. 15)",
            },
            {
                "color": "orange",
                "boxes": [("(3,384,860)", 427.0, None)],
                "card_y": 1100,
                "badge": "HIGHLIGHT 3",
                "title": "2024 TOKOPEDIA DECONSOLIDATION",
                "big": "-(Rp 3,384.9 bn)",
                "line1": "E-commerce goodwill derecognized upon losing control of TOKO",
                "line2": "Reduced group goodwill from Rp 4,065.5 bn to Rp 372.6 bn",
                "footer": "= Structural Perimeter Shift in FY2024",
            },
        ],
    },
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = fitz.open(PDF_PATH)
    for spec in PORTRAIT_SPECS:
        render_portrait_page(doc, spec)
    render_page133_segment_note29(doc)
    print("All audited statement evidence PNGs regenerated with 1-to-1 callout parity.")


if __name__ == "__main__":
    main()
