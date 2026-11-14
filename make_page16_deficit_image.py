import fitz
from PIL import Image, ImageDraw, ImageFont

pdf_path = "GOTO FINANCIAL REPORT/LK GOTO 31 Dec 2025.pdf"
doc = fitz.open(pdf_path)
page = doc[15] # page 16

dpi = 200
scale = dpi / 72.0
pix = page.get_pixmap(dpi=dpi)
base_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

callout_width = 520
total_width = base_img.width + callout_width
total_height = base_img.height

canvas = Image.new("RGB", (total_width, total_height), (255, 255, 255))
canvas.paste(base_img, (0, 0))

draw = ImageDraw.Draw(canvas)
draw.rectangle([(base_img.width, 0), (total_width, total_height)], fill=(248, 250, 252))
draw.line([(base_img.width, 0), (base_img.width, total_height)], fill=(203, 213, 225), width=2)

overlay = Image.new("RGBA", (total_width, total_height), (255, 255, 255, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Numbers coordinates on Page 16:
# Akumulasi rugi: y ≈ 660.1 pt
def_y0 = 658 * scale
def_y1 = 672 * scale

# 2025 amount: 289 to 337 pt -> scale
def25_x0 = 286 * scale
def25_x1 = 338 * scale

# 2024 amount: 350 to 400 pt (214,119,215)
def24_x0 = 350 * scale
def24_x1 = 402 * scale

# Total equity: y ≈ 715.3 pt
eq_y0 = 713 * scale
eq_y1 = 727 * scale

eq25_x0 = 290 * scale
eq25_x1 = 338 * scale

# Row text x coordinates:
label_id_x0 = 68 * scale
label_id_x1 = 230 * scale
label_en_x0 = 410 * scale
label_en_x1 = 552 * scale

# HIGHLIGHT 1: THE 214 DEFICIT (Glowing Crimson Red Highlight)
draw_overlay.rounded_rectangle([def24_x0 - 6, def_y0 - 2, def24_x1 + 6, def_y1 + 2], radius=5, fill=(239, 68, 68, 110), outline=(220, 38, 38, 255), width=3)
draw_overlay.rounded_rectangle([def25_x0 - 6, def_y0 - 2, def25_x1 + 6, def_y1 + 2], radius=5, fill=(239, 68, 68, 90), outline=(220, 38, 38, 255), width=2)
draw_overlay.rounded_rectangle([label_id_x0 - 4, def_y0 - 2, label_id_x1, def_y1 + 2], radius=4, fill=(239, 68, 68, 50))

# HIGHLIGHT 2: TOTAL EQUITY (Emerald Highlight)
draw_overlay.rounded_rectangle([eq25_x0 - 6, eq_y0 - 2, eq25_x1 + 6, eq_y1 + 2], radius=5, fill=(34, 197, 94, 95), outline=(22, 163, 74, 255), width=3)
draw_overlay.rounded_rectangle([label_id_x0 - 4, eq_y0 - 2, label_id_x1, eq_y1 + 2], radius=4, fill=(34, 197, 94, 50))

canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(canvas)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
font_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
font_huge_num = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 38)
font_card_head = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
font_calc_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 17)
font_calc_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)

sb_x = base_img.width + 24
sb_w = callout_width - 48

# Header in sidebar
draw.text((sb_x, int(520 * scale)), "EQUITY & DEFICIT AUDIT", font=font_title, fill=(15, 23, 42))
draw.text((sb_x, int(520 * scale) + 30), "PT GoTo Gojek Tokopedia Tbk (LK p. 16)", font=font_sub, fill=(100, 116, 139))

# --- CARD 1: THE 214 DEFICIT (BURNING CAPITAL) ---
c1_y = int(580 * scale)
c1_h = 220
draw.rounded_rectangle([sb_x, c1_y, sb_x + sb_w, c1_y + c1_h], radius=12, fill=(254, 242, 242), outline=(239, 68, 68), width=3)
# Tag
draw.rounded_rectangle([sb_x + 18, c1_y + 14, sb_x + 150, c1_y + 38], radius=6, fill=(220, 38, 38))
draw.text((sb_x + 24, c1_y + 18), "CRITICAL AUDIT", font=font_tag, fill=(255, 255, 255))
draw.text((sb_x + 160, c1_y + 18), "ACCUMULATED DEFICIT", font=font_card_head, fill=(185, 28, 28))

# Big highlighted number: (Rp 214.1 Trillion)
draw.text((sb_x + 18, c1_y + 46), "(Rp 214.1 Trillion)", font=font_huge_num, fill=(185, 28, 28))
# Plain English breakdown
draw.text((sb_x + 18, c1_y + 98), "Akumulasi Rugi:  (Rp 214,119,215 mn)", font=font_calc_bold, fill=(127, 29, 29))
draw.text((sb_x + 18, c1_y + 124), "Total historical losses burned since inception.", font=font_calc_body, fill=(51, 65, 85))
draw.text((sb_x + 18, c1_y + 146), "Has destroyed 88.4% of paid-in capital (Rp 242T Agio)!", font=font_calc_body, fill=(51, 65, 85))
draw.line([(sb_x + 18, c1_y + 176), (sb_x + sb_w - 18, c1_y + 176)], fill=(254, 202, 202), width=2)
draw.text((sb_x + 18, c1_y + 186), "= Burned Capital: Rp 214,119.2 Billion", font=font_calc_bold, fill=(185, 28, 28))

# Leader lines connecting Card 1 to the Deficit line
draw.line([(int(def24_x1 + 8), int((def_y0 + def_y1) / 2)), (sb_x, c1_y + 60)], fill=(220, 38, 38), width=3)
draw.polygon([(sb_x - 4, c1_y + 60), (sb_x - 14, c1_y + 55), (sb_x - 14, c1_y + 65)], fill=(220, 38, 38))

# --- CARD 2: REMAINING TOTAL EQUITY (Rp 28.7T) ---
c2_y = c1_y + 240
c2_h = 160
draw.rounded_rectangle([sb_x, c2_y, sb_x + sb_w, c2_y + c2_h], radius=12, fill=(240, 253, 244), outline=(34, 197, 94), width=3)
# Tag
draw.rounded_rectangle([sb_x + 18, c2_y + 14, sb_x + 150, c2_y + 38], radius=6, fill=(22, 163, 74))
draw.text((sb_x + 24, c2_y + 18), "NET SURVIVING", font=font_tag, fill=(255, 255, 255))
draw.text((sb_x + 160, c2_y + 18), "TOTAL CONSOLIDATED EQUITY", font=font_card_head, fill=(21, 128, 61))

# Big number: Rp 28,712 mn
draw.text((sb_x + 18, c2_y + 46), "Rp 28,712 bn", font=font_huge_num, fill=(21, 128, 61))
draw.text((sb_x + 18, c2_y + 98), "Total Ekuitas:  Rp 28,711,657 mn (Rp 28.7T)", font=font_calc_bold, fill=(21, 128, 61))
draw.line([(sb_x + 18, c2_y + 124), (sb_x + sb_w - 18, c2_y + 124)], fill=(187, 247, 208), width=2)
draw.text((sb_x + 18, c2_y + 132), "Down from Rp 35.7T (-19.6% contraction YoY)", font=font_calc_body, fill=(51, 65, 85))

# Leader lines connecting Card 2 to Total Equity
draw.line([(int(eq25_x1 + 8), int((eq_y0 + eq_y1) / 2)), (sb_x, c2_y + 60)], fill=(34, 197, 94), width=3)
draw.polygon([(sb_x - 4, c2_y + 60), (sb_x - 14, c2_y + 55), (sb_x - 14, c2_y + 65)], fill=(34, 197, 94))

# Save full image
canvas.save("goto-fsa-study/public/evidence/goto_balance_sheet_liabilities_equity_highlighted.png", "PNG", quality=95)

# Save focused image for Slide 6 (crop around Equity section: y=500 pt to y=760 pt)
crop_y0 = int(480 * scale)
crop_y1 = int(760 * scale)
focused = canvas.crop((160, crop_y0, total_width, crop_y1))
focused.save("goto-fsa-study/public/evidence/goto_equity_deficit_highlighted.png", "PNG", quality=95)

print("Saved page 16 highlighted images!")
print("Full:", canvas.size)
print("Focused:", focused.size)
