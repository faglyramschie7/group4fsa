"""Generate Group4_Presentation_GOTO.pptx (EN & ID) from presentation_deck*.json."""
from pathlib import Path
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'goto-fsa-study' / 'src' / 'data'
PUBLIC = ROOT / 'goto-fsa-study' / 'public'
LOGO_PATH = PUBLIC / 'goto_logo.png'

GREEN_DARK = RGBColor(0x00, 0x54, 0x19)
GREEN_MAIN = RGBColor(0x00, 0x6B, 0x23)
GREEN_LIGHT = RGBColor(0xED, 0xF6, 0xEF)
GREEN_BORDER = RGBColor(0xDC, 0xE7, 0xDF)
TEXT_DARK = RGBColor(0x15, 0x3B, 0x22)
TEXT_BODY = RGBColor(0x24, 0x38, 0x2B)
TEXT_MUTED = RGBColor(0x5F, 0x72, 0x65)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BG_LIGHT = RGBColor(0xF6, 0xF9, 0xF6)


def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header_footer(slide, section_label, title_text, source_footer, folio_text):
    set_slide_bg(slide, BG_LIGHT)

    # Top green banner
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = GREEN_MAIN
    hdr.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.14), Inches(10.8), Inches(0.92))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = section_label.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(0xC5, 0xF1, 0xCB)

    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    if LOGO_PATH.is_file():
        logo_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(11.65), Inches(0.22), Inches(1.2), Inches(0.7))
        logo_bg.fill.solid()
        logo_bg.fill.fore_color.rgb = WHITE
        logo_bg.line.fill.background()
        slide.shapes.add_picture(str(LOGO_PATH), Inches(11.75), Inches(0.28), width=Inches(1.0))

    # Footer bar
    ft = slide.shapes.add_textbox(Inches(0.5), Inches(7.08), Inches(12.333), Inches(0.32))
    ft_tf = ft.text_frame
    ft_tf.word_wrap = True
    fp = ft_tf.paragraphs[0]
    fp.text = f"GROUP 4  /  IDX: GOTO   |   {source_footer or ''}   |   {folio_text}"
    fp.font.size = Pt(8.5)
    fp.font.color.rgb = TEXT_MUTED


def add_table(slide, headers, rows, left, top, width, height, font_size=10):
    n_rows = 1 + len(rows)
    n_cols = len(headers)
    if n_cols == 0 or n_rows == 0:
        return
    shape = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    tbl = shape.table

    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = GREEN_MAIN
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = str(h)
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for r_idx, row in enumerate(rows):
        bg_color = WHITE if r_idx % 2 == 0 else GREEN_LIGHT
        for c_idx in range(n_cols):
            val = row[c_idx] if c_idx < len(row) else ''
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.size = Pt(font_size - 0.5)
            p.font.bold = (c_idx == 0)
            p.font.color.rgb = TEXT_DARK if c_idx == 0 else TEXT_BODY


def build_cover(prs, slide_data, is_id, total_slides):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, GREEN_DARK)

    if LOGO_PATH.is_file():
        logo_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.45), Inches(1.5), Inches(0.85))
        logo_bg.fill.solid()
        logo_bg.fill.fore_color.rgb = WHITE
        logo_bg.line.fill.background()
        slide.shapes.add_picture(str(LOGO_PATH), Inches(0.72), Inches(0.55), width=Inches(1.25))

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(1.65), Inches(7.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = 'PT GoTo Gojek Tokopedia Tbk (IDX: GOTO)'
    p0.font.size = Pt(14)
    p0.font.color.rgb = RGBColor(0xC5, 0xF1, 0xCB)

    p1 = tf.add_paragraph()
    p1.text = 'GoTo'
    p1.font.size = Pt(54)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = 'Analisis Ekuitas' if is_id else 'Equity Analysis'
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    p3 = tf.add_paragraph()
    p3.text = (
        'Gojek · GoTo Financial · 24,99% Tokopedia'
        if is_id else 'Gojek · GoTo Financial · 24.99% Tokopedia'
    )
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(0xE7, 0xF5, 0xEA)
    p3.space_before = Pt(12)

    p4 = tf.add_paragraph()
    p4.text = (
        'Dari model bisnis hingga arus kas, valuasi, dan keputusan.'
        if is_id else 'From the business model to cash flow, value, and a decision.'
    )
    p4.font.size = Pt(15)
    p4.font.color.rgb = RGBColor(0xE7, 0xF5, 0xEA)
    p4.space_before = Pt(10)

    # Right summary card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(1.6), Inches(4.6), Inches(4.4))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(0x00, 0x6B, 0x23)
    card.line.color.rgb = RGBColor(0x52, 0xA8, 0x68)

    ctb = slide.shapes.add_textbox(Inches(8.35), Inches(1.85), Inches(4.1), Inches(3.9))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    items = [
        ('UNTUK SIAPA' if is_id else 'OUR USER', 'Investor saham publik jangka pendek' if is_id else 'Short-term public equity investor'),
        ('HARGA ACUAN TUGAS' if is_id else 'ASSIGNMENT REFERENCE PRICE', 'Rp 25 per saham' if is_id else 'Rp 25 per share'),
        ('CAKUPAN ANALISIS' if is_id else 'ANALYSIS SCOPE', 'Aktual 2023–2025 · Proyeksi 2026–2028' if is_id else '2023–2025 actuals · 2026–2028 forecasts'),
    ]
    for idx, (lbl, val) in enumerate(items):
        pl = ctf.paragraphs[0] if idx == 0 else ctf.add_paragraph()
        pl.text = lbl
        pl.font.size = Pt(9.5)
        pl.font.bold = True
        pl.font.color.rgb = RGBColor(0xC5, 0xE8, 0xCE)
        if idx > 0:
            pl.space_before = Pt(14)
        pv = ctf.add_paragraph()
        pv.text = val
        pv.font.size = Pt(15)
        pv.font.bold = True
        pv.font.color.rgb = WHITE

    # Team footer
    ftb = slide.shapes.add_textbox(Inches(0.6), Inches(6.45), Inches(12.1), Inches(0.75))
    ftf = ftb.text_frame
    fp0 = ftf.paragraphs[0]
    fp0.text = 'GROUP 4  —  Fagly Ramschie · Anggreini Ruitan · Galatia Rompas  |  Magister Manajemen, Universitas Klabat'
    fp0.font.size = Pt(11)
    fp0.font.color.rgb = RGBColor(0xC5, 0xE8, 0xCE)

    if slide_data.get('speaker_notes'):
        slide.notes_slide.notes_text_frame.text = slide_data['speaker_notes']


def build_main_slide(prs, s, is_id, total_slides):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title_text = s.get('display_title') or s.get('title', '')
    section_label = s.get('section_name') or s.get('section_tag') or ''
    folio = f"{s['slide_num']:02d} / {total_slides}"
    add_header_footer(slide, section_label, title_text, s.get('source_footer', ''), folio)

    # Left evidence area (x=0.5..8.2)
    left_x = Inches(0.5)
    left_w = Inches(7.7)
    cur_y = Inches(1.4)

    if s.get('five_forces'):
        headers = ['Kekuatan' if is_id else 'Force', 'Penilaian' if is_id else 'Rating', 'Dasar penilaian' if is_id else 'Basis for assessment']
        add_table(slide, headers, s['five_forces'], left_x, cur_y, left_w, Inches(3.2), font_size=10)
        cur_y = Inches(4.8)
        cc = s.get('competition_chart', {})
        sc = s.get('competitive_spending_chart', {})
        if cc or sc:
            box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, cur_y, left_w, Inches(2.0))
            box.fill.solid()
            box.fill.fore_color.rgb = WHITE
            box.line.color.rgb = GREEN_BORDER
            bt = slide.shapes.add_textbox(Inches(0.7), cur_y + Inches(0.12), Inches(7.3), Inches(1.75))
            btf = bt.text_frame
            btf.word_wrap = True
            p = btf.paragraphs[0]
            p.text = ('Belanja Bersaing & Provisi Kredit (FY2025)' if is_id else '2025 Spending & Credit-Loss Provisions')
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = TEXT_DARK
            if sc.get('series'):
                p2 = btf.add_paragraph()
                p2.text = ' · '.join(f"{r['label']}: Rp {r['value']}T" for r in sc['series'])
                p2.font.size = Pt(10.5)
                p2.font.color.rgb = TEXT_BODY
                p2.space_before = Pt(6)
            if cc.get('series'):
                p3 = btf.add_paragraph()
                p3.text = f"Provisions: {cc['series'][0]['period']} Rp {cc['series'][0]['value']}bn → {cc['series'][1]['period']} Rp {cc['series'][1]['value']}bn | Net loans: Rp {cc.get('consumer_loans_bn', 2731)}bn"
                p3.font.size = Pt(10.5)
                p3.font.color.rgb = TEXT_BODY
                p3.space_before = Pt(4)
    elif s.get('visual_rows'):
        headers = ['Item', 'Nilai' if is_id else 'Value', 'Keterangan' if is_id else 'Summary']
        rows = [[r.get('name', ''), r.get('value', ''), r.get('text', '')] for r in s['visual_rows']]
        add_table(slide, headers, rows, left_x, cur_y, left_w, Inches(3.6), font_size=11)
    elif s.get('table'):
        tbl = s['table']
        row_h = min(5.3, max(2.2, 0.48 * (1 + len(tbl.get('rows', [])))))
        add_table(slide, tbl.get('headers', []), tbl.get('rows', []), left_x, cur_y, left_w, Inches(row_h), font_size=9.5)
    elif s.get('loss_chart'):
        lc = s['loss_chart']
        headers = [lc.get('title', 'Operating Loss (Rp bn)'), 'Rp bn']
        rows = [[r['label'], f"{r['value']:,}"] for r in lc.get('series', [])]
        add_table(slide, headers, rows, left_x, cur_y, left_w, Inches(3.2), font_size=10.5)
    elif s.get('valuation_range'):
        headers = ['Metode' if is_id else 'Method', 'Nilai (Rp/saham)' if is_id else 'Value (Rp/share)']
        rows = [[r['label'], f"{r['value']:+.1f}" if isinstance(r['value'], (int, float)) else str(r['value'])] for r in s['valuation_range']]
        add_table(slide, headers, rows, left_x, cur_y, left_w, Inches(2.5), font_size=10.5)
        if s.get('peer_exclusions'):
            ex_headers = ['Perusahaan Dikeluarkan' if is_id else 'Excluded Peer', 'Alasan' if is_id else 'Reason']
            ex_rows = [[p['company'], p['reason']] for p in s['peer_exclusions']]
            add_table(slide, ex_headers, ex_rows, left_x, Inches(4.15), left_w, Inches(2.6), font_size=9.5)

    # Right analysis points (x=8.45..12.83)
    right_x = Inches(8.45)
    right_w = Inches(4.38)
    points = s.get('analysis_points', [])
    for idx, pt in enumerate(points[:3]):
        py = Inches(1.4 + idx * 1.85)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, py, right_w, Inches(1.7))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = GREEN_BORDER

        ptb = slide.shapes.add_textbox(right_x + Inches(0.15), py + Inches(0.1), right_w - Inches(0.3), Inches(1.5))
        ptf = ptb.text_frame
        ptf.word_wrap = True
        ph = ptf.paragraphs[0]
        ph.text = pt.get('heading', '')
        ph.font.size = Pt(12)
        ph.font.bold = True
        ph.font.color.rgb = GREEN_MAIN

        pb = ptf.add_paragraph()
        pb.text = pt.get('text', '')
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_BODY
        pb.space_before = Pt(4)

    if s.get('speaker_notes'):
        slide.notes_slide.notes_text_frame.text = s['speaker_notes']


def build_appendix_slides(prs, s, total_slides):
    apx_num = s['slide_num'] - 12
    title_text = s.get('display_title') or s.get('title', '')
    section_label = f"{s.get('section_name', 'APPENDIX')}  /  A{apx_num}"
    schedules = []
    if s.get('table'):
        schedules.append(s['table'])
    schedules.extend(s.get('supporting_schedules', []))

    # Group schedules into slide pages so no table overflows vertically
    pages = []
    current_page = []
    used_h = 0.0
    max_h = 5.4
    for sched in schedules:
        est_h = 0.45 + 0.32 * (1 + len(sched.get('rows', []))) + (0.25 if sched.get('note') else 0.0)
        est_h = min(est_h, max_h)
        if current_page and used_h + est_h > max_h:
            pages.append(current_page)
            current_page = [(sched, est_h)]
            used_h = est_h
        else:
            current_page.append((sched, est_h))
            used_h += est_h + 0.2
    if current_page:
        pages.append(current_page)

    for p_idx, page_scheds in enumerate(pages):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        suffix = f" ({p_idx + 1}/{len(pages)})" if len(pages) > 1 else ''
        folio = f"A{apx_num}{suffix} / {total_slides}"
        add_header_footer(slide, section_label, f"{title_text}{suffix}", s.get('source_footer', ''), folio)

        cur_y = Inches(1.32)
        for sched, est_h in page_scheds:
            tb = slide.shapes.add_textbox(Inches(0.5), cur_y, Inches(12.333), Inches(0.32))
            p = tb.text_frame.paragraphs[0]
            p.text = sched.get('title', '')
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = GREEN_MAIN
            cur_y += Inches(0.32)

            tbl_h = max(1.1, est_h - 0.55)
            add_table(slide, sched.get('headers', []), sched.get('rows', []), Inches(0.5), cur_y, Inches(12.333), Inches(tbl_h), font_size=8.5)
            cur_y += Inches(tbl_h + 0.06)

            if sched.get('note'):
                ntb = slide.shapes.add_textbox(Inches(0.5), cur_y, Inches(12.333), Inches(0.24))
                np = ntb.text_frame.paragraphs[0]
                np.text = sched['note']
                np.font.size = Pt(8)
                np.font.color.rgb = TEXT_MUTED
                cur_y += Inches(0.24)
            cur_y += Inches(0.12)

        if s.get('speaker_notes'):
            slide.notes_slide.notes_text_frame.text = s['speaker_notes']


def generate_pptx(json_path, out_path, is_id):
    deck = json.loads(json_path.read_text(encoding='utf-8'))
    prs = Presentation()
    prs.core_properties.author = 'Fagly Ramschie'
    prs.core_properties.last_modified_by = 'Fagly Ramschie'
    prs.core_properties.title = 'PT GoTo Gojek Tokopedia Tbk (IDX: GOTO) — Equity Analysis'
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total = len(deck)

    for s in deck:
        if s['slide_num'] == 1:
            build_cover(prs, s, is_id, total)
        elif s.get('is_appendix'):
            build_appendix_slides(prs, s, total)
        else:
            build_main_slide(prs, s, is_id, total)

    prs.save(str(out_path))
    print(f'Generated {out_path} ({len(prs.slides)} PowerPoint slides)')


if __name__ == '__main__':
    generate_pptx(DATA / 'presentation_deck.json', PUBLIC / 'Group4_Presentation_GOTO.pptx', is_id=False)
    generate_pptx(DATA / 'presentation_deck_id.json', PUBLIC / 'Group4_Presentation_GOTO_ID.pptx', is_id=True)
