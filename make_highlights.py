import fitz
from PIL import Image, ImageDraw, ImageFont

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
doc = fitz.open(pdf_path)
page = doc[16] # page 17

dpi = 200
pix = page.get_pixmap(dpi=dpi)
base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

scale = dpi / 72.0 # 2.7777777777777777

# Expand width by 460px to host the analytical reconciliation sidebar
sidebar_width = 460
total_width = base_img.width + sidebar_width
total_height = base_img.height

canvas = Image.new("RGB", (total_width, total_height), (248, 250, 252))
# Paste base image on the left
canvas.paste(base_img, (0, 0))

# Draw separator line between document and sidebar
draw = ImageDraw.Draw(canvas)
draw.line([(base_img.width, 0), (base_img.width, total_height)], fill=(226, 232, 240), width=2)

# Create an overlay for highlights on the document
overlay = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Bounding boxes in PDF pt coordinates
# Revenue: 18,322,117
rev_y0 = 191.1 * scale
rev_y1 = 200.1 * scale
# COGS: (7,746,034)
cogs_y0 = 218.1 * scale
cogs_y1 = 227.1 * scale

# Opex lines:
# G&A (227.1) down to D&A (272.1)
opex_y0 = 227.1 * scale
opex_y1 = 272.1 * scale

# Operating loss: (378,254)
oploss_y0 = 299.3 * scale
oploss_y1 = 308.2 * scale

# Net loss: (1,501,685)
netloss_y0 = 497.4 * scale
netloss_y1 = 506.4 * scale

# Number column x range (2025 column is around x=288 to x=336 pt)
num_x0 = 286 * scale
num_x1 = 338 * scale

# Full row x range (from Indonesian text at x=70 pt to English text at x=550 pt)
row_x0 = 68 * scale
row_x1 = 552 * scale

# 1. Soft green highlight on Revenue number and row
draw_overlay.rounded_rectangle([num_x0 - 4, rev_y0 - 2, num_x1 + 4, rev_y1 + 2], radius=4, fill=(34, 197, 94, 90), outline=(22, 163, 74, 255), width=2)
# 2. Soft green highlight on COGS number
draw_overlay.rounded_rectangle([num_x0 - 4, cogs_y0 - 2, num_x1 + 4, cogs_y1 + 2], radius=4, fill=(34, 197, 94, 90), outline=(22, 163, 74, 255), width=2)

# 3. Amber/Orange highlight on the 5 Opex rows
draw_overlay.rounded_rectangle([num_x0 - 4, opex_y0 - 2, num_x1 + 4, opex_y1 + 2], radius=4, fill=(245, 158, 11, 75), outline=(217, 119, 6, 255), width=2)

# 4. Red highlight on Operating Loss number
draw_overlay.rounded_rectangle([num_x0 - 4, oploss_y0 - 2, num_x1 + 4, oploss_y1 + 2], radius=4, fill=(239, 68, 68, 80), outline=(220, 38, 38, 255), width=2)

# 5. Red highlight on Net Loss number
draw_overlay.rounded_rectangle([num_x0 - 4, netloss_y0 - 2, num_x1 + 4, netloss_y1 + 2], radius=4, fill=(239, 68, 68, 80), outline=(220, 38, 38, 255), width=2)

# Merge overlay onto canvas
canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(canvas)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
font_card_h = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
font_num_big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
font_body_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
font_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)

# SIDEBAR CONTENT
sb_x = base_img.width + 24
sb_w = sidebar_width - 48

# Header in sidebar
draw.text((sb_x, 400), "FSA AUDITED RECONCILIATION", font=font_title, fill=(30, 41, 59))
draw.text((sb_x, 430), "Step 1: Gross Margin vs Operating Overhead", font=font_sm, fill=(100, 116, 139))

# --- CARD 1: GROSS PROFIT (10,576) ---
c1_y = 480
c1_h = 160
# Card background
draw.rounded_rectangle([sb_x, c1_y, sb_x + sb_w, c1_y + c1_h], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=2)
# Badge
draw.rounded_rectangle([sb_x + 16, c1_y + 16, sb_x + 160, c1_y + 40], radius=6, fill=(22, 163, 74))
draw.text((sb_x + 24, c1_y + 19), "GROSS PROFIT", font=font_sm, fill=(255, 255, 255))
# Big Number: 10,576
draw.text((sb_x + 16, c1_y + 50), "Rp 10,576 mn", font=font_num_big, fill=(21, 128, 61))
# Formula / Reconciliation
draw.text((sb_x + 16, c1_y + 100), "Net Revenue: Rp 18,322,117", font=font_body, fill=(51, 65, 85))
draw.text((sb_x + 16, c1_y + 124), "Cost of Revenue: (Rp 7,746,034)", font=font_body, fill=(51, 65, 85))

# Connector line from Gross Profit Card to Revenue/COGS rows
draw.line([(base_img.width - 20, (rev_y0 + cogs_y1) / 2), (sb_x, c1_y + 70)], fill=(34, 197, 94), width=3)
draw.polygon([(base_img.width - 20, (rev_y0 + cogs_y1) / 2), (base_img.width - 10, (rev_y0 + cogs_y1) / 2 - 6), (base_img.width - 10, (rev_y0 + cogs_y1) / 2 + 6)], fill=(34, 197, 94))

# --- CARD 2: OPERATING EXPENSES (10,954) ---
c2_y = 660
c2_h = 180
# Card background
draw.rounded_rectangle([sb_x, c2_y, sb_x + sb_w, c2_y + c2_h], radius=10, fill=(255, 251, 235), outline=(254, 215, 170), width=2)
# Badge
draw.rounded_rectangle([sb_x + 16, c2_y + 16, sb_x + 200, c2_y + 40], radius=6, fill=(217, 119, 6))
draw.text((sb_x + 24, c2_y + 19), "OPERATING EXPENSES", font=font_sm, fill=(255, 255, 255))
# Big Number: 10,954
draw.text((sb_x + 16, c2_y + 50), "Rp 10,954 mn", font=font_num_big, fill=(180, 83, 9))
# Breakdown
draw.text((sb_x + 16, c2_y + 100), "Sum of 5 Operating Accounts:", font=font_body_bold, fill=(67, 20, 7))
draw.text((sb_x + 16, c2_y + 124), "G&A (3,989) + S&M (3,090) +", font=font_sm, fill=(120, 53, 15))
draw.text((sb_x + 16, c2_y + 146), "R&D (2,152) + Ops (974) + D&A (749)", font=font_sm, fill=(120, 53, 15))

# Connector line from Opex Card to Opex bracket
draw.line([(base_img.width - 20, (opex_y0 + opex_y1) / 2), (sb_x, c2_y + 70)], fill=(217, 119, 6), width=3)
draw.polygon([(base_img.width - 20, (opex_y0 + opex_y1) / 2), (base_img.width - 10, (opex_y0 + opex_y1) / 2 - 6), (base_img.width - 10, (opex_y0 + opex_y1) / 2 + 6)], fill=(217, 119, 6))

# --- CARD 3: OPERATING DEFICIT / LOSS (378) ---
c3_y = 860
c3_h = 140
draw.rounded_rectangle([sb_x, c3_y, sb_x + sb_w, c3_y + c3_h], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=2)
# Badge
draw.rounded_rectangle([sb_x + 16, c3_y + 16, sb_x + 175, c3_y + 40], radius=6, fill=(220, 38, 38))
draw.text((sb_x + 24, c3_y + 19), "OPERATING LOSS", font=font_sm, fill=(255, 255, 255))
# Big Number: (378)
draw.text((sb_x + 16, c3_y + 50), "(Rp 378 mn)", font=font_num_big, fill=(185, 28, 28))
# Explanation
draw.text((sb_x + 16, c3_y + 100), "10,576 (Gross Profit) - 10,954 (Opex)", font=font_body, fill=(127, 29, 29))

# Connector line from Card 3 to Operating Loss row
draw.line([(base_img.width - 20, (oploss_y0 + oploss_y1) / 2), (sb_x, c3_y + 60)], fill=(220, 38, 38), width=3)
draw.polygon([(base_img.width - 20, (oploss_y0 + oploss_y1) / 2), (base_img.width - 10, (oploss_y0 + oploss_y1) / 2 - 6), (base_img.width - 10, (oploss_y0 + oploss_y1) / 2 + 6)], fill=(220, 38, 38))

# Save full highlighted image
canvas.save("test_full_highlighted.png", "PNG", quality=95)
print("Saved test_full_highlighted.png successfully, size:", canvas.size)

# Focused Crop for Slide 5: Operating Statement Focus
# Crop region: y=250 to y=1160 (captures table headers down through Operating Loss and Finance income)
focused_crop = canvas.crop((0, 240, total_width, 1140))
focused_crop.save("test_focused_highlighted.png", "PNG", quality=95)
print("Saved test_focused_highlighted.png, size:", focused_crop.size)
