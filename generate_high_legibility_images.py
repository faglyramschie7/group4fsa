import fitz
from PIL import Image, ImageDraw, ImageFont

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
doc = fitz.open(pdf_path)
page = doc[16] # page 17

# High resolution 220 DPI for razor sharp text
dpi = 220
scale = dpi / 72.0
pix = page.get_pixmap(dpi=dpi)
base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

overlay = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
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

# Merge overlay onto base image
highlighted_doc = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(highlighted_doc)

# Fonts
font_badge_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
font_badge_num = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
font_badge_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)

# Prominent badges on the right of the table (between English text and margin)
# Tag 1: Gross Profit 10,576
gp_badge_x = int(label_en_x1 + 18)
gp_badge_y = int((rev_y0 + cogs_y1) / 2 - 32)
draw.rounded_rectangle([gp_badge_x, gp_badge_y, gp_badge_x + 290, gp_badge_y + 64], radius=8, fill=(240, 253, 244), outline=(22, 163, 74), width=2)
draw.text((gp_badge_x + 12, gp_badge_y + 8), "Gross Profit:", font=font_badge_sub, fill=(21, 128, 61))
draw.text((gp_badge_x + 115, gp_badge_y + 6), "10,576 mn", font=font_badge_num, fill=(21, 128, 61))
draw.text((gp_badge_x + 12, gp_badge_y + 36), "18,322 - 7,746 (57.7% margin)", font=font_badge_sub, fill=(51, 65, 85))

# Connector line from Revenue and COGS
draw.line([(int(num_x1 + 8), int(rev_y0 + 10)), (gp_badge_x, gp_badge_y + 20)], fill=(22, 163, 74), width=2)
draw.line([(int(num_x1 + 8), int(cogs_y1 - 10)), (gp_badge_x, gp_badge_y + 44)], fill=(22, 163, 74), width=2)

# Tag 2: Total Opex 10,954
op_badge_x = int(label_en_x1 + 18)
op_badge_y = int((opex_y0 + opex_y1) / 2 - 32)
draw.rounded_rectangle([op_badge_x, op_badge_y, op_badge_x + 290, op_badge_y + 64], radius=8, fill=(255, 251, 235), outline=(217, 119, 6), width=2)
draw.text((op_badge_x + 12, op_badge_y + 8), "Total Opex:", font=font_badge_sub, fill=(180, 83, 9))
draw.text((op_badge_x + 105, op_badge_y + 6), "10,954 mn", font=font_badge_num, fill=(180, 83, 9))
draw.text((op_badge_x + 12, op_badge_y + 36), "Sum of 5 opex rows (59.8%)", font=font_badge_sub, fill=(120, 53, 15))

# Connector line from Opex bracket
draw.line([(int(num_x1 + 8), int((opex_y0 + opex_y1) / 2)), (op_badge_x, op_badge_y + 32)], fill=(217, 119, 6), width=2)

# Tag 3: Operating Loss (378)
ol_badge_x = int(label_en_x1 + 18)
ol_badge_y = int(oploss_y0 - 20)
draw.rounded_rectangle([ol_badge_x, ol_badge_y, ol_badge_x + 290, ol_badge_y + 64], radius=8, fill=(254, 242, 242), outline=(220, 38, 38), width=2)
draw.text((ol_badge_x + 12, ol_badge_y + 8), "Operating Loss:", font=font_badge_sub, fill=(185, 28, 28))
draw.text((ol_badge_x + 130, ol_badge_y + 6), "(378 mn)", font=font_badge_num, fill=(185, 28, 28))
draw.text((ol_badge_x + 12, ol_badge_y + 36), "10,576 GP - 10,954 Opex", font=font_badge_sub, fill=(127, 29, 29))

# Connector line from Operating Loss
draw.line([(int(num_x1 + 8), int((oploss_y0 + oploss_y1) / 2)), (ol_badge_x, ol_badge_y + 32)], fill=(220, 38, 38), width=2)

# Crop tight to eliminate wasted margins!
# Left: start at label_id_x0 - 25 pt (around x=130 px in DPI=220)
# Right: end right after the badges (gp_badge_x + 300)
crop_x0 = int(50 * scale)
crop_x1 = int(gp_badge_x + 305)

# Save full highlighted statement (cropped horizontally to remove white margins)
full_statement = highlighted_doc.crop((crop_x0, 0, crop_x1, base_img.height))
full_statement.save("goto-fsa-study/public/evidence/goto_income_statement_highlighted.png", "PNG", quality=95)

# Save focused statement for Slide 5:
# Vertical range: from header down to operating loss (y=55 pt to y=325 pt)
crop_y0 = int(55 * scale)
crop_y1 = int(325 * scale)
focused_statement = highlighted_doc.crop((crop_x0, crop_y0, crop_x1, crop_y1))
focused_statement.save("goto-fsa-study/public/evidence/goto_gross_profit_opex_highlighted.png", "PNG", quality=95)

print("Exported full statement size:", full_statement.size)
print("Exported focused statement size:", focused_statement.size)
