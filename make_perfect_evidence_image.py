import fitz
from PIL import Image, ImageDraw, ImageFont

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
doc = fitz.open(pdf_path)
page = doc[16] # page 17

# High resolution 200 DPI
dpi = 200
scale = dpi / 72.0
pix = page.get_pixmap(dpi=dpi)
base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Expand width properly with white background for right-hand callouts
callout_width = 520
total_width = base_img.width + callout_width
total_height = base_img.height

canvas = Image.new("RGB", (total_width, total_height), (255, 255, 255))
canvas.paste(base_img, (0, 0))

# Right sidebar background: clean soft slate
draw = ImageDraw.Draw(canvas)
draw.rectangle([(base_img.width, 0), (total_width, total_height)], fill=(248, 250, 252))
draw.line([(base_img.width, 0), (base_img.width, total_height)], fill=(203, 213, 225), width=2)

overlay = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Numbers coordinates (2025 column is around x=286 to x=338 pt)
num_x0 = 286 * scale
num_x1 = 338 * scale

# Labels coordinates
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

# 1. Soft green highlight on Revenue & COGS numbers
draw_overlay.rounded_rectangle([num_x0 - 8, rev_y0 - 3, num_x1 + 8, rev_y1 + 3], radius=5, fill=(34, 197, 94, 95), outline=(22, 163, 74, 255), width=3)
draw_overlay.rounded_rectangle([label_id_x0 - 4, rev_y0 - 3, label_id_x1, rev_y1 + 3], radius=4, fill=(34, 197, 94, 50))

draw_overlay.rounded_rectangle([num_x0 - 8, cogs_y0 - 3, num_x1 + 8, cogs_y1 + 3], radius=5, fill=(34, 197, 94, 95), outline=(22, 163, 74, 255), width=3)
draw_overlay.rounded_rectangle([label_id_x0 - 4, cogs_y0 - 3, label_id_x1, cogs_y1 + 3], radius=4, fill=(34, 197, 94, 50))

# 2. Warm amber highlight on the 5 Opex rows
draw_overlay.rounded_rectangle([num_x0 - 8, opex_y0 - 3, num_x1 + 8, opex_y1 + 3], radius=6, fill=(245, 158, 11, 85), outline=(217, 119, 6, 255), width=3)
draw_overlay.rounded_rectangle([label_id_x0 - 4, opex_y0 - 3, label_id_x1, opex_y1 + 3], radius=4, fill=(245, 158, 11, 45))

# 3. Soft red highlight on Operating Loss number
draw_overlay.rounded_rectangle([num_x0 - 8, oploss_y0 - 3, num_x1 + 8, oploss_y1 + 3], radius=5, fill=(239, 68, 68, 95), outline=(220, 38, 38, 255), width=3)
draw_overlay.rounded_rectangle([label_id_x0 - 4, oploss_y0 - 3, label_id_x1, oploss_y1 + 3], radius=4, fill=(239, 68, 68, 50))

# 4. Soft red highlight on Net Loss number
draw_overlay.rounded_rectangle([num_x0 - 8, netloss_y0 - 3, num_x1 + 8, netloss_y1 + 3], radius=5, fill=(239, 68, 68, 95), outline=(220, 38, 38, 255), width=3)

# Merge overlay
canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(canvas)

# Fonts with MUCH BIGGER, HIGH-CONTRAST SIZES
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
font_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
font_huge_num = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 42) # HUGE numbers!
font_card_head = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
font_calc_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 17)
font_calc_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)

sb_x = base_img.width + 24
sb_w = callout_width - 48

# Header
draw.text((sb_x, 180), "AUDITED RECONCILIATION", font=font_title, fill=(15, 23, 42))
draw.text((sb_x, 212), "Official Filing (LK p. 17) vs FSA Breakdown", font=font_sub, fill=(100, 116, 139))

# --- CARD 1: GROSS PROFIT (10,576) ---
c1_y = 460
c1_h = 180
draw.rounded_rectangle([sb_x, c1_y, sb_x + sb_w, c1_y + c1_h], radius=12, fill=(240, 253, 244), outline=(34, 197, 94), width=3)
# Tag
draw.rounded_rectangle([sb_x + 18, c1_y + 14, sb_x + 130, c1_y + 38], radius=6, fill=(22, 163, 74))
draw.text((sb_x + 26, c1_y + 18), "HIGHLIGHT 1", font=font_tag, fill=(255, 255, 255))
draw.text((sb_x + 140, c1_y + 18), "GROSS PROFIT", font=font_card_head, fill=(21, 128, 61))

# HUGE NUMBER: 10,576
draw.text((sb_x + 18, c1_y + 44), "Rp 10,576 mn", font=font_huge_num, fill=(21, 128, 61))
# Formula
draw.text((sb_x + 18, c1_y + 98), "Revenue:  18,322,117  -  COGS: (7,746,034)", font=font_calc_body, fill=(51, 65, 85))
draw.line([(sb_x + 18, c1_y + 128), (sb_x + sb_w - 18, c1_y + 128)], fill=(187, 247, 208), width=2)
draw.text((sb_x + 18, c1_y + 138), "= Gross Margin: Rp 10,576,083 mn (57.7%)", font=font_calc_bold, fill=(21, 128, 61))

# Leader lines
mid_rev_cogs = (rev_y0 + cogs_y1) / 2
draw.line([(label_en_x1 + 10, rev_y0 + 10), (label_en_x1 + 25, rev_y0 + 10)], fill=(34, 197, 94), width=3)
draw.line([(label_en_x1 + 10, cogs_y1 - 10), (label_en_x1 + 25, cogs_y1 - 10)], fill=(34, 197, 94), width=3)
draw.line([(label_en_x1 + 25, rev_y0 + 10), (label_en_x1 + 25, cogs_y1 - 10)], fill=(34, 197, 94), width=3)
draw.line([(label_en_x1 + 25, mid_rev_cogs), (sb_x, c1_y + 60)], fill=(34, 197, 94), width=3)
draw.polygon([(sb_x - 4, c1_y + 60), (sb_x - 14, c1_y + 55), (sb_x - 14, c1_y + 65)], fill=(34, 197, 94))

# --- CARD 2: OPERATING EXPENSES (10,954) ---
c2_y = 660
c2_h = 200
draw.rounded_rectangle([sb_x, c2_y, sb_x + sb_w, c2_y + c2_h], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=3)
# Tag
draw.rounded_rectangle([sb_x + 18, c2_y + 14, sb_x + 130, c2_y + 38], radius=6, fill=(217, 119, 6))
draw.text((sb_x + 26, c2_y + 18), "HIGHLIGHT 2", font=font_tag, fill=(255, 255, 255))
draw.text((sb_x + 140, c2_y + 18), "OPERATING EXPENSES", font=font_card_head, fill=(180, 83, 9))

# HUGE NUMBER: 10,954
draw.text((sb_x + 18, c2_y + 44), "Rp 10,954 mn", font=font_huge_num, fill=(180, 83, 9))
# Formula
draw.text((sb_x + 18, c2_y + 98), "Sum of 5 Operating Expense accounts:", font=font_calc_bold, fill=(67, 20, 7))
draw.text((sb_x + 18, c2_y + 122), "G&A (3,989) + S&M (3,090) + R&D (2,152)", font=font_calc_body, fill=(120, 53, 15))
draw.text((sb_x + 18, c2_y + 144), "+ Operations (974) + D&A (749)", font=font_calc_body, fill=(120, 53, 15))
draw.line([(sb_x + 18, c2_y + 168), (sb_x + sb_w - 18, c2_y + 168)], fill=(254, 215, 170), width=2)
draw.text((sb_x + 18, c2_y + 174), "= Total Opex: Rp 10,954,337 mn (59.8%)", font=font_calc_bold, fill=(180, 83, 9))

# Leader lines
mid_opex = (opex_y0 + opex_y1) / 2
draw.line([(label_en_x1 + 10, opex_y0 + 6), (label_en_x1 + 25, opex_y0 + 6)], fill=(217, 119, 6), width=3)
draw.line([(label_en_x1 + 10, opex_y1 - 6), (label_en_x1 + 25, opex_y1 - 6)], fill=(217, 119, 6), width=3)
draw.line([(label_en_x1 + 25, opex_y0 + 6), (label_en_x1 + 25, opex_y1 - 6)], fill=(217, 119, 6), width=3)
draw.line([(label_en_x1 + 25, mid_opex), (sb_x, c2_y + 60)], fill=(217, 119, 6), width=3)
draw.polygon([(sb_x - 4, c2_y + 60), (sb_x - 14, c2_y + 55), (sb_x - 14, c2_y + 65)], fill=(217, 119, 6))

# --- CARD 3: LOSS FROM OPERATIONS (378) ---
c3_y = 880
c3_h = 160
draw.rounded_rectangle([sb_x, c3_y, sb_x + sb_w, c3_y + c3_h], radius=12, fill=(254, 242, 242), outline=(239, 68, 68), width=3)
# Tag
draw.rounded_rectangle([sb_x + 18, c3_y + 14, sb_x + 130, c3_y + 38], radius=6, fill=(220, 38, 38))
draw.text((sb_x + 26, c3_y + 18), "HIGHLIGHT 3", font=font_tag, fill=(255, 255, 255))
draw.text((sb_x + 140, c3_y + 18), "OPERATING LOSS", font=font_card_head, fill=(185, 28, 28))

# HUGE NUMBER: (378)
draw.text((sb_x + 18, c3_y + 44), "(Rp 378 mn)", font=font_huge_num, fill=(185, 28, 28))
draw.text((sb_x + 18, c3_y + 98), "Gross Profit (10,576) - Total Opex (10,954)", font=font_calc_body, fill=(127, 29, 29))
draw.line([(sb_x + 18, c3_y + 128), (sb_x + sb_w - 18, c3_y + 128)], fill=(254, 202, 202), width=2)
draw.text((sb_x + 18, c3_y + 136), "= Operating Deficit: (Rp 378,254) mn", font=font_calc_bold, fill=(185, 28, 28))

# Leader lines
mid_oploss = (oploss_y0 + oploss_y1) / 2
draw.line([(label_en_x1 + 10, mid_oploss), (sb_x, c3_y + 60)], fill=(220, 38, 38), width=3)
draw.polygon([(sb_x - 4, c3_y + 60), (sb_x - 14, c3_y + 55), (sb_x - 14, c3_y + 65)], fill=(220, 38, 38))

# Export full highlighted image
canvas.save("goto-fsa-study/public/evidence/goto_income_statement_highlighted.png", "PNG", quality=95)

# Export focused cropped image for Slide 5:
# Crop left margin from x = 160 px (eliminates empty space) to right edge
# Crop vertical from y = 140 px to y = 1080 px
focused = canvas.crop((160, 140, total_width, 1080))
focused.save("goto-fsa-study/public/evidence/goto_gross_profit_opex_highlighted.png", "PNG", quality=95)

print("Saved new images!")
print("Full:", canvas.size)
print("Focused:", focused.size)
