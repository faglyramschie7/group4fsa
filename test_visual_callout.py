import fitz
from PIL import Image, ImageDraw, ImageFont

doc = fitz.open("GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf")
page = doc[16]

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
draw.line([(base_img.width, 0), (base_img.width, total_height)], fill=(226, 232, 240), width=2)

overlay = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Numbers coordinates
num_x0 = 286 * scale
num_x1 = 338 * scale

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

# 1. Revenue highlight: soft green fill + border
draw_overlay.rounded_rectangle([num_x0 - 6, rev_y0 - 3, num_x1 + 6, rev_y1 + 3], radius=4, fill=(34, 197, 94, 80), outline=(22, 163, 74, 255), width=2)
# 2. COGS highlight: soft green fill + border
draw_overlay.rounded_rectangle([num_x0 - 6, cogs_y0 - 3, num_x1 + 6, cogs_y1 + 3], radius=4, fill=(34, 197, 94, 80), outline=(22, 163, 74, 255), width=2)

# 3. 5 Opex rows highlight: soft amber fill + border
draw_overlay.rounded_rectangle([num_x0 - 6, opex_y0 - 3, num_x1 + 6, opex_y1 + 3], radius=4, fill=(245, 158, 11, 75), outline=(217, 119, 6, 255), width=2)

# 4. Operating loss highlight: soft red fill + border
draw_overlay.rounded_rectangle([num_x0 - 6, oploss_y0 - 3, num_x1 + 6, oploss_y1 + 3], radius=4, fill=(239, 68, 68, 80), outline=(220, 38, 38, 255), width=2)

# 5. Net loss highlight: soft red fill + border
draw_overlay.rounded_rectangle([num_x0 - 6, netloss_y0 - 3, num_x1 + 6, netloss_y1 + 3], radius=4, fill=(239, 68, 68, 80), outline=(220, 38, 38, 255), width=2)

# Merge overlay
canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(canvas)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
font_card_h = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
font_num_big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
font_body_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
font_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
font_sm = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 14)

# DIRECT ON-TABLE PILLS (Right between 2025 and 2024 columns or pointing right from the numbers)
# Let's draw pill between rows for Gross Profit:
gp_pill_x = num_x1 + 12
gp_pill_y = (rev_y1 + cogs_y0) / 2 - 12
draw.rounded_rectangle([gp_pill_x, gp_pill_y, gp_pill_x + 195, gp_pill_y + 28], radius=6, fill=(22, 163, 74), outline=(21, 128, 61), width=1)
draw.text((gp_pill_x + 8, gp_pill_y + 6), "Gross Profit: 10,576", font=font_badge, fill=(255, 255, 255))

# Opex pill next to the 5 opex rows:
op_pill_x = num_x1 + 12
op_pill_y = (opex_y0 + opex_y1) / 2 - 14
draw.rounded_rectangle([op_pill_x, op_pill_y, op_pill_x + 215, op_pill_y + 28], radius=6, fill=(217, 119, 6), outline=(180, 83, 9), width=1)
draw.text((op_pill_x + 8, op_pill_y + 6), "Total Opex: 10,954 (5 rows)", font=font_badge, fill=(255, 255, 255))

# Operating loss pill:
ol_pill_x = num_x1 + 12
ol_pill_y = oploss_y0 - 2
draw.rounded_rectangle([ol_pill_x, ol_pill_y, ol_pill_x + 210, ol_pill_y + 28], radius=6, fill=(220, 38, 38), outline=(185, 28, 28), width=1)
draw.text((ol_pill_x + 8, ol_pill_y + 6), "Operating Loss: (378)", font=font_badge, fill=(255, 255, 255))

# SIDEBAR RECONCILIATION
sb_x = base_img.width + 24
sb_w = sidebar_width - 48

draw.text((sb_x, 380), "AUDITED RECONCILIATION", font=font_title, fill=(30, 41, 59))
draw.text((sb_x, 410), "Step 1: Gross Profit vs Operating Overhead", font=font_sm, fill=(100, 116, 139))

# Card 1: Gross Profit 10,576
c1_y = 450
c1_h = 160
draw.rounded_rectangle([sb_x, c1_y, sb_x + sb_w, c1_y + c1_h], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=2)
draw.rounded_rectangle([sb_x + 16, c1_y + 14, sb_x + 150, c1_y + 36], radius=5, fill=(22, 163, 74))
draw.text((sb_x + 24, c1_y + 17), "GROSS PROFIT", font=font_badge, fill=(255, 255, 255))
draw.text((sb_x + 16, c1_y + 46), "Rp 10,576 mn", font=font_num_big, fill=(21, 128, 61))
draw.text((sb_x + 16, c1_y + 94), "Net Revenue:  18,322,117", font=font_body, fill=(51, 65, 85))
draw.text((sb_x + 16, c1_y + 118), "Cost of Revenue: (7,746,034)", font=font_body, fill=(51, 65, 85))
draw.text((sb_x + 16, c1_y + 138), "= Rp 10,576,083 million", font=font_body_bold, fill=(21, 128, 61))

# Card 2: Operating Expenses 10,954
c2_y = 630
c2_h = 185
draw.rounded_rectangle([sb_x, c2_y, sb_x + sb_w, c2_y + c2_h], radius=10, fill=(255, 251, 235), outline=(254, 215, 170), width=2)
draw.rounded_rectangle([sb_x + 16, c2_y + 14, sb_x + 195, c2_y + 36], radius=5, fill=(217, 119, 6))
draw.text((sb_x + 24, c2_y + 17), "OPERATING EXPENSES", font=font_badge, fill=(255, 255, 255))
draw.text((sb_x + 16, c2_y + 46), "Rp 10,954 mn", font=font_num_big, fill=(180, 83, 9))
draw.text((sb_x + 16, c2_y + 94), "Sum of 5 Operating Accounts:", font=font_body_bold, fill=(67, 20, 7))
draw.text((sb_x + 16, c2_y + 118), "G&A (3,989) + S&M (3,090) +", font=font_sm, fill=(120, 53, 15))
draw.text((sb_x + 16, c2_y + 138), "R&D (2,152) + Ops (974) + D&A (749)", font=font_sm, fill=(120, 53, 15))
draw.text((sb_x + 16, c2_y + 158), "= Rp 10,954,337 million", font=font_body_bold, fill=(180, 83, 9))

# Card 3: Operating Deficit (378)
c3_y = 835
c3_h = 135
draw.rounded_rectangle([sb_x, c3_y, sb_x + sb_w, c3_y + c3_h], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=2)
draw.rounded_rectangle([sb_x + 16, c3_y + 14, sb_x + 165, c3_y + 36], radius=5, fill=(220, 38, 38))
draw.text((sb_x + 24, c3_y + 17), "OPERATING LOSS", font=font_badge, fill=(255, 255, 255))
draw.text((sb_x + 16, c3_y + 46), "(Rp 378 mn)", font=font_num_big, fill=(185, 28, 28))
draw.text((sb_x + 16, c3_y + 94), "10,576 (GP) - 10,954 (Opex)", font=font_body, fill=(127, 29, 29))
draw.text((sb_x + 16, c3_y + 114), "= (Rp 378,254) million", font=font_body_bold, fill=(185, 28, 28))

# Connector lines from table pills to sidebar cards
draw.line([(gp_pill_x + 195, gp_pill_y + 14), (sb_x, c1_y + 55)], fill=(34, 197, 94), width=2)
draw.line([(op_pill_x + 215, op_pill_y + 14), (sb_x, c2_y + 55)], fill=(217, 119, 6), width=2)
draw.line([(ol_pill_x + 210, ol_pill_y + 14), (sb_x, c3_y + 55)], fill=(220, 38, 38), width=2)

# Full image
canvas.save("goto-fsa-study/public/evidence/goto_income_statement_highlighted.png", "PNG", quality=95)

# Focused image for Slide 5 (Operating section from header down through operating loss)
focused = canvas.crop((0, int(150 * scale), total_width, int(355 * scale)))
focused.save("goto-fsa-study/public/evidence/goto_gross_profit_opex_highlighted.png", "PNG", quality=95)

print("Saved full and focused images successfully!")
print("Focused size:", focused.size)
