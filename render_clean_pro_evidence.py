import fitz
from PIL import Image, ImageDraw, ImageFont

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
doc = fitz.open(pdf_path)
page = doc[16] # page 17

dpi = 200
pix = page.get_pixmap(dpi=dpi)
base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

scale = dpi / 72.0
sidebar_width = 460
total_width = base_img.width + sidebar_width
total_height = base_img.height

canvas = Image.new("RGB", (total_width, total_height), (248, 250, 252))
canvas.paste(base_img, (0, 0))

draw = ImageDraw.Draw(canvas)
# Border between audited statement and sidebar
draw.line([(base_img.width, 0), (base_img.width, total_height)], fill=(203, 213, 225), width=2)

overlay = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Numbers coordinates (2025 column)
num_x0 = 288 * scale
num_x1 = 338 * scale

# Row labels coordinates
label_id_x0 = 68 * scale
label_id_x1 = 230 * scale
label_en_x0 = 410 * scale
label_en_x1 = 552 * scale

rev_y0 = 191.1 * scale
rev_y1 = 200.1 * scale

cogs_y0 = 218.1 * scale
cogs_y1 = 227.1 * scale

# 5 Opex rows
opex_y0 = 227.1 * scale
opex_y1 = 272.1 * scale

# Specific opex row lines
ga_y0, ga_y1 = 227.1 * scale, 236.1 * scale
sm_y0, sm_y1 = 236.1 * scale, 245.1 * scale
rd_y0, rd_y1 = 245.1 * scale, 254.1 * scale
ops_y0, ops_y1 = 254.1 * scale, 263.1 * scale
da_y0, da_y1 = 263.1 * scale, 272.1 * scale

oploss_y0 = 299.3 * scale
oploss_y1 = 308.2 * scale

netloss_y0 = 497.4 * scale
netloss_y1 = 506.4 * scale

# HIGHLIGHTS ON AUDITED TABLE:
# 1. Revenue: Soft Emerald
draw_overlay.rounded_rectangle([num_x0 - 6, rev_y0 - 2, num_x1 + 6, rev_y1 + 2], radius=4, fill=(34, 197, 94, 85), outline=(22, 163, 74, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, rev_y0 - 2, label_id_x1, rev_y1 + 2], radius=4, fill=(34, 197, 94, 45))

# 2. COGS: Soft Emerald / Olive
draw_overlay.rounded_rectangle([num_x0 - 6, cogs_y0 - 2, num_x1 + 6, cogs_y1 + 2], radius=4, fill=(34, 197, 94, 85), outline=(22, 163, 74, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, cogs_y0 - 2, label_id_x1, cogs_y1 + 2], radius=4, fill=(34, 197, 94, 45))

# 3. 5 Operating Expense Accounts: Warm Amber Highlight Box
draw_overlay.rounded_rectangle([num_x0 - 6, opex_y0 - 2, num_x1 + 6, opex_y1 + 2], radius=4, fill=(245, 158, 11, 75), outline=(217, 119, 6, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, opex_y0 - 2, label_id_x1, opex_y1 + 2], radius=4, fill=(245, 158, 11, 40))

# 4. Operating Loss: Clean Rose Red
draw_overlay.rounded_rectangle([num_x0 - 6, oploss_y0 - 2, num_x1 + 6, oploss_y1 + 2], radius=4, fill=(239, 68, 68, 85), outline=(220, 38, 38, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, oploss_y0 - 2, label_id_x1, oploss_y1 + 2], radius=4, fill=(239, 68, 68, 45))

# 5. Net Loss: Clean Rose Red
draw_overlay.rounded_rectangle([num_x0 - 6, netloss_y0 - 2, num_x1 + 6, netloss_y1 + 2], radius=4, fill=(239, 68, 68, 85), outline=(220, 38, 38, 255), width=2)

canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(canvas)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_card_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)
font_big_num = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
font_calc_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
font_calc_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)

sb_x = base_img.width + 24
sb_w = sidebar_width - 48

# Title Header
draw.text((sb_x, 380), "FINANCIAL STATEMENT ANALYSIS", font=font_title, fill=(15, 23, 42))
draw.text((sb_x, 408), "GoTo Audited Statutory Statement Highlights", font=font_sub, fill=(100, 116, 139))

# --- CARD 1: GROSS PROFIT (10,576) ---
c1_y = 445
c1_h = 165
draw.rounded_rectangle([sb_x, c1_y, sb_x + sb_w, c1_y + c1_h], radius=10, fill=(240, 253, 244), outline=(134, 239, 172), width=2)
# Tag
draw.rounded_rectangle([sb_x + 16, c1_y + 14, sb_x + 130, c1_y + 36], radius=5, fill=(22, 163, 74))
draw.text((sb_x + 24, c1_y + 18), "HIGHLIGHT 1", font=font_card_tag, fill=(255, 255, 255))
draw.text((sb_x + 140, c1_y + 18), "GROSS PROFIT", font=font_calc_bold, fill=(21, 128, 61))

# Big highlighted number
draw.text((sb_x + 16, c1_y + 44), "Rp 10,576 mn", font=font_big_num, fill=(21, 128, 61))
# Formula
draw.text((sb_x + 16, c1_y + 92), "Net Revenue:  Rp 18,322,117", font=font_calc_body, fill=(51, 65, 85))
draw.text((sb_x + 16, c1_y + 114), "Cost of Revenue: (Rp 7,746,034)", font=font_calc_body, fill=(51, 65, 85))
draw.line([(sb_x + 16, c1_y + 138), (sb_x + sb_w - 16, c1_y + 138)], fill=(187, 247, 208), width=1)
draw.text((sb_x + 16, c1_y + 142), "= Gross Margin: Rp 10,576,083 mn (57.7%)", font=font_calc_bold, fill=(21, 128, 61))

# Bracket / Callout lines from the 2 audited rows to Card 1
mid_rev_cogs = (rev_y0 + cogs_y1) / 2
draw.line([(label_en_x1 + 10, rev_y0 + 10), (label_en_x1 + 25, rev_y0 + 10)], fill=(34, 197, 94), width=2)
draw.line([(label_en_x1 + 10, cogs_y1 - 10), (label_en_x1 + 25, cogs_y1 - 10)], fill=(34, 197, 94), width=2)
draw.line([(label_en_x1 + 25, rev_y0 + 10), (label_en_x1 + 25, cogs_y1 - 10)], fill=(34, 197, 94), width=2)
draw.line([(label_en_x1 + 25, mid_rev_cogs), (sb_x, c1_y + 55)], fill=(34, 197, 94), width=2)
draw.polygon([(sb_x - 6, c1_y + 55), (sb_x - 14, c1_y + 51), (sb_x - 14, c1_y + 59)], fill=(34, 197, 94))

# --- CARD 2: OPERATING EXPENSES (10,954) ---
c2_y = 630
c2_h = 190
draw.rounded_rectangle([sb_x, c2_y, sb_x + sb_w, c2_y + c2_h], radius=10, fill=(255, 251, 235), outline=(253, 186, 116), width=2)
# Tag
draw.rounded_rectangle([sb_x + 16, c2_y + 14, sb_x + 130, c2_y + 36], radius=5, fill=(217, 119, 6))
draw.text((sb_x + 24, c2_y + 18), "HIGHLIGHT 2", font=font_card_tag, fill=(255, 255, 255))
draw.text((sb_x + 140, c2_y + 18), "TOTAL OPERATING EXPENSES", font=font_calc_bold, fill=(180, 83, 9))

# Big highlighted number
draw.text((sb_x + 16, c2_y + 44), "Rp 10,954 mn", font=font_big_num, fill=(180, 83, 9))
# Formula
draw.text((sb_x + 16, c2_y + 92), "Sum of 5 Operating Accounts (LK p. 17):", font=font_calc_bold, fill=(67, 20, 7))
draw.text((sb_x + 16, c2_y + 114), "G&A (3,989) + Sales & Mktg (3,090) +", font=font_calc_body, fill=(120, 53, 15))
draw.text((sb_x + 16, c2_y + 134), "R&D (2,152) + Ops (974) + D&A (749)", font=font_calc_body, fill=(120, 53, 15))
draw.line([(sb_x + 16, c2_y + 158), (sb_x + sb_w - 16, c2_y + 158)], fill=(254, 215, 170), width=1)
draw.text((sb_x + 16, c2_y + 164), "= Total Opex: Rp 10,954,337 mn (59.8%)", font=font_calc_bold, fill=(180, 83, 9))

# Bracket / Callout lines from the 5 opex accounts to Card 2
mid_opex = (opex_y0 + opex_y1) / 2
draw.line([(label_en_x1 + 10, opex_y0 + 6), (label_en_x1 + 25, opex_y0 + 6)], fill=(217, 119, 6), width=2)
draw.line([(label_en_x1 + 10, opex_y1 - 6), (label_en_x1 + 25, opex_y1 - 6)], fill=(217, 119, 6), width=2)
draw.line([(label_en_x1 + 25, opex_y0 + 6), (label_en_x1 + 25, opex_y1 - 6)], fill=(217, 119, 6), width=2)
draw.line([(label_en_x1 + 25, mid_opex), (sb_x, c2_y + 55)], fill=(217, 119, 6), width=2)
draw.polygon([(sb_x - 6, c2_y + 55), (sb_x - 14, c2_y + 51), (sb_x - 14, c2_y + 59)], fill=(217, 119, 6))

# --- CARD 3: OPERATING LOSS (378) ---
c3_y = 840
c3_h = 135
draw.rounded_rectangle([sb_x, c3_y, sb_x + sb_w, c3_y + c3_h], radius=10, fill=(254, 242, 242), outline=(252, 165, 165), width=2)
# Tag
draw.rounded_rectangle([sb_x + 16, c3_y + 14, sb_x + 130, c3_y + 36], radius=5, fill=(220, 38, 38))
draw.text((sb_x + 24, c3_y + 18), "HIGHLIGHT 3", font=font_card_tag, fill=(255, 255, 255))
draw.text((sb_x + 140, c3_y + 18), "LOSS FROM OPERATIONS", font=font_calc_bold, fill=(185, 28, 28))

# Big highlighted number
draw.text((sb_x + 16, c3_y + 44), "(Rp 378 mn)", font=font_big_num, fill=(185, 28, 28))
draw.text((sb_x + 16, c3_y + 92), "Gross Profit (10,576) - Total Opex (10,954)", font=font_calc_body, fill=(127, 29, 29))
draw.line([(sb_x + 16, c3_y + 114), (sb_x + sb_w - 16, c3_y + 114)], fill=(254, 202, 202), width=1)
draw.text((sb_x + 16, c3_y + 118), "= Operating Loss: (Rp 378,254) mn", font=font_calc_bold, fill=(185, 28, 28))

# Line from Operating Loss row to Card 3
mid_oploss = (oploss_y0 + oploss_y1) / 2
draw.line([(label_en_x1 + 10, mid_oploss), (sb_x, c3_y + 55)], fill=(220, 38, 38), width=2)
draw.polygon([(sb_x - 6, c3_y + 55), (sb_x - 14, c3_y + 51), (sb_x - 14, c3_y + 59)], fill=(220, 38, 38))

# Save full highlighted image
canvas.save("goto-fsa-study/public/evidence/goto_income_statement_highlighted.png", "PNG", quality=95)

# Save focused image for Slide 5 (y=150 to 360 in pt, so header + table headers down through Operating Loss)
focused = canvas.crop((0, int(145 * scale), total_width, int(360 * scale)))
focused.save("goto-fsa-study/public/evidence/goto_gross_profit_opex_highlighted.png", "PNG", quality=95)

print("Exported goto_income_statement_highlighted.png:", canvas.size)
print("Exported goto_gross_profit_opex_highlighted.png:", focused.size)
