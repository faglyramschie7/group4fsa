import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import fitz
from PIL import Image, ImageDraw, ImageFont

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
doc = fitz.open(pdf_path)
page = doc[16] # page 17

dpi = 200
pix = page.get_pixmap(dpi=dpi)
base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

scale = dpi / 72.0
sidebar_width = 480
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
num_x0 = 286 * scale
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

opex_y0 = 227.1 * scale
opex_y1 = 272.1 * scale

oploss_y0 = 299.3 * scale
oploss_y1 = 308.2 * scale

netloss_y0 = 497.4 * scale
netloss_y1 = 506.4 * scale

# 1. Revenue: Soft Emerald highlight
draw_overlay.rounded_rectangle([num_x0 - 6, rev_y0 - 2, num_x1 + 6, rev_y1 + 2], radius=4, fill=(34, 197, 94, 85), outline=(22, 163, 74, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, rev_y0 - 2, label_id_x1, rev_y1 + 2], radius=4, fill=(34, 197, 94, 40))

# 2. COGS: Soft Emerald highlight
draw_overlay.rounded_rectangle([num_x0 - 6, cogs_y0 - 2, num_x1 + 6, cogs_y1 + 2], radius=4, fill=(34, 197, 94, 85), outline=(22, 163, 74, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, cogs_y0 - 2, label_id_x1, cogs_y1 + 2], radius=4, fill=(34, 197, 94, 40))

# 3. 5 Operating Expense Accounts: Warm Amber Highlight Box
draw_overlay.rounded_rectangle([num_x0 - 6, opex_y0 - 2, num_x1 + 6, opex_y1 + 2], radius=4, fill=(245, 158, 11, 75), outline=(217, 119, 6, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, opex_y0 - 2, label_id_x1, opex_y1 + 2], radius=4, fill=(245, 158, 11, 40))

# 4. Operating Loss: Clean Rose Red
draw_overlay.rounded_rectangle([num_x0 - 6, oploss_y0 - 2, num_x1 + 6, oploss_y1 + 2], radius=4, fill=(239, 68, 68, 85), outline=(220, 38, 38, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, oploss_y0 - 2, label_id_x1, oploss_y1 + 2], radius=4, fill=(239, 68, 68, 40))

# 5. Net Loss: Clean Rose Red
draw_overlay.rounded_rectangle([num_x0 - 6, netloss_y0 - 2, num_x1 + 6, netloss_y1 + 2], radius=4, fill=(239, 68, 68, 85), outline=(220, 38, 38, 255), width=2)

canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(canvas)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_card_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)
font_big_num = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
font_calc_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
font_calc_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_formula = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)

sb_x = base_img.width + 24
sb_w = sidebar_width - 48

# Position sidebar elements so they align cleanly with the statements
header_y = 190
draw.text((sb_x, header_y), "FSA AUDITED RECONCILIATION", font=font_title, fill=(15, 23, 42))
draw.text((sb_x, header_y + 28), "PT GoTo Gojek Tokopedia Tbk (FY2025 Audited)", font=font_sub, fill=(100, 116, 139))

# --- CARD 1: GROSS PROFIT (10,576) ---
# Aligns with rev_y0 (530) and cogs_y1 (630)
c1_y = 480
c1_h = 165
draw.rounded_rectangle([sb_x, c1_y, sb_x + sb_w, c1_y + c1_h], radius=10, fill=(240, 253, 244), outline=(134, 239, 172), width=2)
# Tag
draw.rounded_rectangle([sb_x + 16, c1_y + 14, sb_x + 120, c1_y + 36], radius=5, fill=(22, 163, 74))
draw.text((sb_x + 22, c1_y + 18), "STATUTORY", font=font_card_tag, fill=(255, 255, 255))
draw.text((sb_x + 130, c1_y + 18), "GROSS PROFIT (LABA BRUTO)", font=font_calc_bold, fill=(21, 128, 61))

# Big highlighted number: 10,576
draw.text((sb_x + 16, c1_y + 44), "Rp 10,576 mn", font=font_big_num, fill=(21, 128, 61))
# Breakdown
draw.text((sb_x + 16, c1_y + 92), "Pendapatan Bersih:    Rp 18,322,117", font=font_calc_body, fill=(51, 65, 85))
draw.text((sb_x + 16, c1_y + 114), "Beban Pokok (COGS):  (Rp 7,746,034)", font=font_calc_body, fill=(51, 65, 85))
draw.line([(sb_x + 16, c1_y + 138), (sb_x + sb_w - 16, c1_y + 138)], fill=(187, 247, 208), width=1)
draw.text((sb_x + 16, c1_y + 142), "= Gross Margin: Rp 10,576,083 mn (57.7%)", font=font_calc_bold, fill=(21, 128, 61))

# Leader lines connecting Card 1 to Revenue and COGS
mid_rev_cogs = (rev_y0 + cogs_y1) / 2
draw.line([(label_en_x1 + 10, rev_y0 + 10), (label_en_x1 + 25, rev_y0 + 10)], fill=(34, 197, 94), width=2)
draw.line([(label_en_x1 + 10, cogs_y1 - 10), (label_en_x1 + 25, cogs_y1 - 10)], fill=(34, 197, 94), width=2)
draw.line([(label_en_x1 + 25, rev_y0 + 10), (label_en_x1 + 25, cogs_y1 - 10)], fill=(34, 197, 94), width=2)
draw.line([(label_en_x1 + 25, mid_rev_cogs), (sb_x, c1_y + 55)], fill=(34, 197, 94), width=2)
draw.polygon([(sb_x - 4, c1_y + 55), (sb_x - 12, c1_y + 51), (sb_x - 12, c1_y + 59)], fill=(34, 197, 94))

# --- CARD 2: OPERATING EXPENSES (10,954) ---
# Aligns with opex rows (630 to 755)
c2_y = 665
c2_h = 195
draw.rounded_rectangle([sb_x, c2_y, sb_x + sb_w, c2_y + c2_h], radius=10, fill=(255, 251, 235), outline=(253, 186, 116), width=2)
# Tag
draw.rounded_rectangle([sb_x + 16, c2_y + 14, sb_x + 120, c2_y + 36], radius=5, fill=(217, 119, 6))
draw.text((sb_x + 22, c2_y + 18), "STATUTORY", font=font_card_tag, fill=(255, 255, 255))
draw.text((sb_x + 130, c2_y + 18), "TOTAL OPERATING EXPENSES", font=font_calc_bold, fill=(180, 83, 9))

# Big highlighted number: 10,954
draw.text((sb_x + 16, c2_y + 44), "Rp 10,954 mn", font=font_big_num, fill=(180, 83, 9))
# Breakdown
draw.text((sb_x + 16, c2_y + 92), "Sum of 5 Operating Accounts (LK p. 17):", font=font_calc_bold, fill=(67, 20, 7))
draw.text((sb_x + 16, c2_y + 114), "G&A (3,989) + Sales & Mktg (3,090) +", font=font_calc_body, fill=(120, 53, 15))
draw.text((sb_x + 16, c2_y + 134), "R&D (2,152) + Ops (974) + D&A (749)", font=font_calc_body, fill=(120, 53, 15))
draw.line([(sb_x + 16, c2_y + 158), (sb_x + sb_w - 16, c2_y + 158)], fill=(254, 215, 170), width=1)
draw.text((sb_x + 16, c2_y + 166), "= Total Opex: Rp 10,954,337 mn (59.8%)", font=font_calc_bold, fill=(180, 83, 9))

# Leader lines connecting Card 2 to the 5 Opex rows
mid_opex = (opex_y0 + opex_y1) / 2
draw.line([(label_en_x1 + 10, opex_y0 + 6), (label_en_x1 + 25, opex_y0 + 6)], fill=(217, 119, 6), width=2)
draw.line([(label_en_x1 + 10, opex_y1 - 6), (label_en_x1 + 25, opex_y1 - 6)], fill=(217, 119, 6), width=2)
draw.line([(label_en_x1 + 25, opex_y0 + 6), (label_en_x1 + 25, opex_y1 - 6)], fill=(217, 119, 6), width=2)
draw.line([(label_en_x1 + 25, mid_opex), (sb_x, c2_y + 55)], fill=(217, 119, 6), width=2)
draw.polygon([(sb_x - 4, c2_y + 55), (sb_x - 12, c2_y + 51), (sb_x - 12, c2_y + 59)], fill=(217, 119, 6))

# --- CARD 3: CORE OPERATING DEFICIT / LOSS (378) ---
# Aligns with oploss_y0 (831)
c3_y = 880
c3_h = 145
draw.rounded_rectangle([sb_x, c3_y, sb_x + sb_w, c3_y + c3_h], radius=10, fill=(254, 242, 242), outline=(252, 165, 165), width=2)
# Tag
draw.rounded_rectangle([sb_x + 16, c3_y + 14, sb_x + 120, c3_y + 36], radius=5, fill=(220, 38, 38))
draw.text((sb_x + 22, c3_y + 18), "STATUTORY", font=font_card_tag, fill=(255, 255, 255))
draw.text((sb_x + 130, c3_y + 18), "LOSS FROM OPERATIONS (RUGI USAHA)", font=font_calc_bold, fill=(185, 28, 28))

# Big highlighted number: (378)
draw.text((sb_x + 16, c3_y + 44), "(Rp 378 mn)", font=font_big_num, fill=(185, 28, 28))
draw.text((sb_x + 16, c3_y + 92), "Gross Profit (10,576) - Total Opex (10,954)", font=font_calc_body, fill=(127, 29, 29))
draw.line([(sb_x + 16, c3_y + 116), (sb_x + sb_w - 16, c3_y + 116)], fill=(254, 202, 202), width=1)
draw.text((sb_x + 16, c3_y + 122), "= Operating Deficit: (Rp 378,254) mn", font=font_calc_bold, fill=(185, 28, 28))

# Leader line connecting Card 3 to Operating Loss
mid_oploss = (oploss_y0 + oploss_y1) / 2
draw.line([(label_en_x1 + 10, mid_oploss), (sb_x, c3_y + 55)], fill=(220, 38, 38), width=2)
draw.polygon([(sb_x - 4, c3_y + 55), (sb_x - 12, c3_y + 51), (sb_x - 12, c3_y + 59)], fill=(220, 38, 38))

# Save full highlighted image
canvas.save("goto-fsa-study/public/evidence/goto_income_statement_highlighted.png", "PNG", quality=95)

# FOCUSED OPERATING CROP FOR SLIDE 5:
# Includes statement header down to operating loss and other income header (y=150 to 1080)
focused = canvas.crop((0, 150, total_width, 1070))
focused.save("goto-fsa-study/public/evidence/goto_gross_profit_opex_highlighted.png", "PNG", quality=95)

print("Saved perfect layouts successfully!")
print("Full:", canvas.size)
print("Focused:", focused.size)
