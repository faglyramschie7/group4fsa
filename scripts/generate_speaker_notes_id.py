#!/usr/bin/env python3
"""Generate Group4_GOTO_Speaker_Notes_ID.docx in Bahasa Indonesia with all 20 slides, full popup walkthroughs, and 40 screenshots."""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_PATH = "ASSIGNMENTS/FINAL REPORT/Group4_GOTO_Speaker_Notes_ID.docx"
MEDIA_DIR = "outputs/speaker-notes-screenshots-id"

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


def add_figure(doc, img_filename, caption_text, width_in=6.2):
    img_path = os.path.join(MEDIA_DIR, img_filename)
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"File gambar tidak ditemukan: {img_path}")
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

    p_goal = doc.add_paragraph()
    p_goal.paragraph_format.space_before = Pt(5)
    p_goal.paragraph_format.space_after = Pt(4)
    add_run(p_goal, "Tujuan Utama: ", bold=True, size=10, color=NAVY)
    add_run(p_goal, slide_data["goal"], size=10, color=DARK)

    script_title = (
        "APA YANG HARUS DIUCAPKAN SAAT TANYA-JAWAB (NASKAH MUDAH)"
        if is_appendix
        else "APA YANG HARUS DIUCAPKAN (NASKAH MUDAH)"
    )
    add_callout_box(doc, script_title, [slide_data["script"]])

    p_kn = doc.add_paragraph()
    p_kn.paragraph_format.space_before = Pt(2)
    p_kn.paragraph_format.space_after = Pt(2)
    p_kn.paragraph_format.keep_with_next = True
    add_run(
        p_kn,
        "Jadwal & Angka Kunci di Slide Ini:" if is_appendix else "Angka Kunci yang Perlu Ditunjuk:",
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

    if slide_data.get("slide_fig"):
        sf_file, sf_cap = slide_data["slide_fig"]
        n = fig_counter[0]
        fig_counter[0] += 1
        add_figure(doc, sf_file, f"Gambar {n}: {sf_cap}", width_in=6.2)

    p_pop = doc.add_paragraph()
    p_pop.paragraph_format.space_before = Pt(5)
    p_pop.paragraph_format.space_after = Pt(3)
    p_pop.paragraph_format.keep_with_next = True
    add_run(
        p_pop,
        "Panduan Popup — Setiap Item di Dalam Popup (Dari Atas ke Bawah):",
        bold=True,
        size=10,
        color=EMERALD,
    )
    add_styled_table(
        doc,
        ["Elemen / Tab Popup", "Isi Tampilan & Cara Menjelaskannya di Panggung"],
        slide_data["popup_rows"],
        [1.95, 5.05],
        hdr_hex=HEX_APX_HDR if is_appendix else HEX_EMERALD,
    )

    for pf_file, pf_cap in slide_data.get("popup_figs", []):
        n = fig_counter[0]
        fig_counter[0] += 1
        add_figure(doc, pf_file, f"Gambar {n}: {pf_cap}", width_in=6.2)


MAIN_SLIDES = [
    {
        "header": "SLIDE 1: Analisis Ekuitas GoTo (Pembukaan)  [0,75 menit  |  Ref: Tidak ada]",
        "goal": "Memperkenalkan perusahaan, target investor, harga acuan Rp25, dan alur 6 bagian presentasi secara ringkas (~45 detik).",
        "script": (
            '"Selamat pagi Bapak/Ibu dosen dan teman-teman. Kami dari Kelompok 4, dan hari ini kami akan mempresentasikan analisis ekuitas '
            'PT GoTo Gojek Tokopedia Tbk, kode saham GOTO di Bursa Efek Indonesia. Saat ini GoTo menjalankan dua bisnis utama: Gojek untuk '
            'transportasi dan pesan-antar makanan, serta GoTo Financial untuk pembayaran GoPay dan pinjaman konsumen. GoTo juga masih memegang '
            '24,99% saham minoritas di Tokopedia setelah TikTok mengambil alih kendali pada awal 2024. Analisis ini ditujukan bagi investor saham '
            'publik jangka pendek dengan horizon 12 bulan, menggunakan harga acuan Rp25 per saham. Kami akan membahas model bisnis, profitabilitas, '
            'kualitas arus kas, proyeksi 3 tahun, dan valuasi, lalu menutup dengan rekomendasi investasi final kami."'
        ),
        "bullets": [
            "2 bisnis inti: Gojek (On-Demand) dan GoTo Financial (pembayaran GoPay & pinjaman konsumen)",
            "24,99% kepemilikan pasif sebagai entitas asosiasi di Tokopedia (didekonsolidasi awal 2024)",
            "Target pengguna: Investor saham publik jangka pendek (12 bulan) dengan harga acuan Rp25 per saham",
            "Cakupan: Data aktual 2023–2025 & proyeksi 2026F–2028F pada 14 slide utama + Lampiran A1–A6",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Saat tampil di panggung, cukup ~45 detik tanpa perlu membuka popup. Namun dua elemen sampul BISA diklik jika dibutuhkan: "
                "\"Gojek · GoTo Financial · 24,99% Tokopedia\" dan kotak \"HARGA ACUAN TUGAS: Rp 25 per saham\".",
            ],
            [
                "Header & Footer Popup",
                "Header menampilkan pil \"SLIDE 1 · Opening\", judul item yang diklik, dan pita glosarium \"Istilah:\" di bagian bawah (mis. EBIT). "
                "Tidak ada tombol lompat Appendix pada Slide 1.",
            ],
            [
                "Tab 1: Grafik & Data",
                "Menampilkan grafik batang divergen \"Kontribusi EBIT per Segmen (FY2025, Note 29)\": On-Demand (Gojek) +888,6M, E-Commerce Fee +572,2M, "
                "Fintech (GoPay) −396,6M, Biaya Korporasi −1.442,5M, dan EBIT Konsolidasian −378,3M.",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Tidak aktif pada Slide 1.",
            ],
            [
                "Tab 3 & Tab 4 (Rumus / Bukti)",
                "Tidak ditampilkan pada Slide 1 (0 baris kalkulasi slide dan 0 jadwal pendukung).",
            ],
            [
                "Tab 5: Jejak Tugas & Materi",
                "Aktif dengan 4 tautan jejak (3 slide materi kuliah + 1 referensi tugas) untuk menunjukkan dasar cakupan Minggu 1–2.",
            ],
            [
                "Tampilkan Analisis (Kanan Atas)",
                "Membuka panel samping \"Ringkasan & Analisis\" yang merangkum profil GoTo, harga acuan Rp25, dan alur presentasi.",
            ],
        ],
    },
    {
        "header": "SLIDE 2: Model Bisnis  [1,0 menit  |  Ref: Appendix A1]",
        "goal": "Menunjukkan sumber pendapatan GoTo setelah melepas kendali Tokopedia: Gojek mesin laba utama dan GoPay pendorong pertumbuhan tercepat.",
        "script": (
            '"Mari kita lihat bagaimana GoTo menghasilkan uang saat ini. Pada 2025, total pendapatan bersih tumbuh 15,3% menjadi Rp18,3 triliun. '
            'Pertama, Gojek (transportasi dan makanan) tetap menjadi mesin terbesar dengan Rp12,36 triliun atau sekitar dua pertiga total pendapatan. '
            'Lebih baik lagi, laba operasi segmen Gojek melonjak hampir 13 kali lipat dari Rp69 miliar di 2024 menjadi Rp889 miliar di 2025 berkat '
            'pemangkasan promo dan penghematan biaya cloud di atas 50%. Kedua, GoTo Financial (GoPay dan pinjaman) tumbuh paling cepat, melesat 74% ke '
            'Rp5,19 triliun. Terakhir, GoTo masih menerima sekitar Rp820 miliar imbalan jasa e-commerce dari Tokopedia. Namun setelah memperhitungkan '
            'biaya korporasi Rp1,44 triliun, GoTo secara konsolidasi masih mencatat rugi operasi tipis sebesar Rp378 miliar."'
        ),
        "bullets": [
            "Total Pendapatan Bersih FY2025: Rp18.322,1M / Rp18,32T (+15,27% YoY)",
            "Gojek (On-Demand): Pendapatan Rp12.361M (+13,8% YoY); EBIT segmen melonjak 13x dari +Rp69,4M menjadi +Rp888,6M",
            "GoTo Financial (GoPay): Pendapatan Rp5.191M (+74,1% YoY; 90,96% pertumbuhan grup); rugi EBIT segmen menyusut ke −Rp396,6M",
            "Imbalan Jasa Tokopedia: Rp820M pendapatan (+Rp572,2M EBIT segmen); dikurangi biaya korporasi Rp1.442,5M = EBIT Konsolidasian −Rp378,3M",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 3 baris segmen (Gojek, GoTo Financial, Tokopedia) atau kartu analisis di sebelah kanan.",
            ],
            [
                "Tab 1 Grafik Atas (Jika Klik Gojek)",
                "Menampilkan \"Jembatan Laba Operasi (EBIT) Gojek: FY24 → FY25 (Note 29)\": EBIT FY2024 (+69,4M) + Pendapatan Bruto 3P (+995,8M) + "
                "Pangkas Insentif −15,9% (+504,2M) + Antar-Segmen Bersih (+67,8M) + Alokasi Korporasi (+32,5M) − Kenaikan Biaya 3P (−781,1M) = EBIT FY2025 (+888,6M).",
            ],
            [
                "Tab 1 Grafik Atas (GoPay / Tokopedia)",
                "Jika mengklik GoTo Financial atau Tokopedia, grafik beralih ke \"Kontribusi EBIT per Segmen (FY2025, Note 29)\": "
                "On-Demand (+888,6M), E-Commerce Fee (+572,2M), Fintech (−396,6M), Biaya Korporasi (−1.442,5M), EBIT Konsolidasian (−378,3M).",
            ],
            [
                "Tab 1 Kartu Tren YoY (Di Bawah)",
                "4 kartu kolom vertikal (dengan pemisah \"Exit\" setelah 2023*): (1) EBIT On-Demand Gojek (+Rp69,4M → +Rp888,6M, +1.180% YoY), "
                "(2) Pendapatan FinTech GoPay (Rp2,98T → Rp5,19T, +74,05% YoY), (3) Pendapatan Bersih Konsolidasi (Rp14,79T → Rp15,89T → Rp18,32T), "
                "dan (4) EBIT Konsolidasian (−Rp10,28T → −Rp2,24T → −Rp378M).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Membandingkan 2023 Pra-Exit (Konsolidasi Tokopedia) vs. 2025 Pasca-Exit pada 4 kartu: Pendapatan Bersih (Rp14,79T → Rp18,32T), "
                "Cash OpEx (117,01% → 55,70%, −6.131 bps), EBIT (−Rp10,28T → −Rp0,38T), dan Laba Bersih (−Rp90,52T termasuk goodwill → −Rp1,50T).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan rumus segmen yang diklik (mis. Pendapatan Bersih ODS = Rp15.030,99M Bruto − Rp2.669,74M Insentif = Rp12.361,26M), "
                "rekonsiliasi ke Rp18.322,12M, serta Tabel Perhitungan Slide (Pendapatan Konsolidasi).",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Menampilkan foto Bukti Laporan Keuangan Auditan (Laporan Tahunan 2025 hal. 468 Catatan 29 Segmen Operasi — klik untuk perbesar) "
                "+ Jadwal Pendukung lipat: \"Jembatan pendapatan ke pendapatan konsolidasi GoTo\" (6 baris).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 7 jejak (5 kuliah + 2 tugas). Tombol \"Tampilkan Analisis\" membuka penjelasan ekonomi segmen; \"Appendix A1 ↗\" melompat ke Slide 15.",
            ],
        ],
    },
    {
        "header": "SLIDE 3: Industri dan Persaingan  [1,5 menit  |  Ref: Appendix A1]",
        "goal": "Membuktikan dengan angka laporan keuangan bahwa persaingan ketat membatasi daya harga, sementara pertumbuhan pinjaman cepat menambah risiko kredit.",
        "script": (
            '"Berikutnya, kami menguji Lima Kekuatan Porter terhadap angka keuangan GoTo yang sebenarnya. Tekanan terbesar adalah Rivalitas Persaingan, '
            'bernilai TINGGI. Di Indonesia, GoFood berada di 31% di belakang GrabFood 46%, sambil bertahan dari ShopeeFood 23%. Layanan transportasi bersaing '
            'dengan Maxim dan inDrive, dan GoPay bersaing dengan ShopeePay, DANA, serta OVO. Karena pengguna dapat berpindah aplikasi tanpa biaya, '
            'GoTo tidak punya kekuatan menaikkan harga. Ini terlihat langsung di laba rugi: pada 2025 GoTo masih harus membelanjakan Rp3,09 triliun untuk '
            'penjualan & pemasaran serta Rp2,15 triliun untuk pengembangan produk demi menjaga pangsa pasar. Di saat yang sama, pinjaman konsumen GoPay melonjak '
            '72,6% ke Rp2,73 triliun dan cadangan kerugian kreditnya naik lebih dari dua kali lipat (+135%) menjadi Rp408 miliar."'
        ),
        "bullets": [
            "Penilaian Porter: Rivalitas = TINGGI; Pembeli & Substitusi = SEDANG; Pendatang Baru = RENDAH–SEDANG; Pemasok = RENDAH",
            "Pangsa Pesan-Antar Makanan: GrabFood 46% vs. GoFood 31% vs. ShopeeFood 23%",
            "Belanja Persaingan 2025: Penjualan & Pemasaran Rp3,09T (16,9% pendapatan) | Pengembangan Produk Rp2,15T (11,7%) | Insentif beban S&M Rp1,08T",
            "Risiko Kredit GoPay: Pinjaman konsumen bersih +72,6% YoY (Rp1,58T → Rp2,73T) | Provisi kerugian kredit +134,9% (Rp174M → Rp408M)",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 5 baris tabel Porter, grafik \"Belanja untuk bersaing\", grafik \"Provisi kerugian kredit\", atau poin analisis di kanan.",
            ],
            [
                "Tab 1 Grafik Atas",
                "\"Tekanan Rivalitas: Belanja Persaingan & Provisi Kredit (FY2025, Rp miliar)\" batang horizontal: Penjualan & Pemasaran (Rp3.090M), "
                "Pengembangan Produk (Rp2.152M), Insentif Beban S&M (Rp1.077M), Provisi Kredit 2024 (Rp174M), dan Provisi Kredit 2025 (Rp408M, merah +134,9% YoY).",
            ],
            [
                "Tab 1 Kartu Tren YoY (Di Bawah)",
                "2 kartu vertikal: (1) Provisi Kredit Catatan 7: Rp173,6M (2024) → Rp407,7M (2025, +134,9% YoY, mencapai 12,99% pinjaman bruto); "
                "(2) Cash OpEx / Pendapatan: 117,0% (2023*) → 62,78% (2024) → 55,70% (2025, −708 bps YoY).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Tidak aktif pada Slide 3.",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan rumus item yang diklik (mis. Pertumbuhan Provisi = (407,684 / 173,552 − 1) = +134,9%, dibulatkan 134%) serta Tabel Perhitungan Slide.",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Menampilkan foto bukti LK Auditan (Catatan 7 pinjaman & provisi kredit atau Catatan 26 beban operasi) yang bisa diperbesar.",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 9 jejak (7 kuliah + 2 tugas). \"Tampilkan Analisis\" merinci tiap kekuatan Porter; \"Appendix A1 ↗\" melompat ke Slide 15 (jadwal lengkap Catatan 35 & Porter).",
            ],
        ],
    },
    {
        "header": "SLIDE 4: Profitabilitas dan DuPont  [1,75 menit  |  Ref: Appendix A2]",
        "goal": "Menunjukkan pemulihan tajam GoTo dari 2023 ke 2025, namun margin bersih negatif tetap membuat ROE negatif di bawah Grab.",
        "script": (
            '"Sekarang mari kita lihat profitabilitas dan dekomposisi DuPont. Kabar baiknya jelas: rugi operasi GoTo menyusut tajam dari Rp10,28 triliun '
            'pada 2023 menjadi tinggal Rp378 miliar pada 2025, yaitu margin operasi -2,06%. Rugi bersih total juga turun menjadi Rp1,50 triliun atau margin '
            'laba bersih -8,20%. Dengan rumus DuPont 3-tahap, Margin Bersih (-8,20%) dikali Perputaran Aset (0,40x) dikali Pengganda Ekuitas (1,59x) '
            'menghasilkan ROE Konsolidasian sebesar -5,23%, atau -3,73% pada ekuitas induk. Poin pentingnya dibanding Grab: GoTo sebenarnya lebih efisien '
            'memutar aset daripada Grab (0,40x vs. Grab 0,28x). Satu-satunya alasan ROE GoTo masih negatif sementara Grab positif (+2,96%) adalah karena '
            'margin laba bersih GoTo belum menembus nol."'
        ),
        "bullets": [
            "Rugi Operasi (EBIT): −Rp10,28T (2023) → −Rp2,24T (2024) → −Rp378M (2025, margin operasi −2,06%)",
            "Rugi & Margin Bersih: −Rp90,52T (2023, termasuk impairment goodwill Rp78,8T) → −Rp5,47T (2024) → −Rp1,50T (2025, margin bersih −8,20%)",
            "DuPont FY2025 (Restated): −8,20% Margin Bersih × 0,4004x Perputaran Aset × 1,5937x Pengganda Ekuitas = −5,23% ROE Konsolidasian (−3,73% ROE Induk)",
            "Pembanding Grab: ROE Konsolidasian Grab FY2025 = +2,96% (margin bersih +5,93%, perputaran aset 0,28x) vs. batas Biaya Ekuitas GoTo (Ke) 8,45%",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Gunakan bilah pengalih atas antara \"Dek Awal (Tersubmit)\" dan \"Laporan Akhir (Restated)\" (menambahkan Rp1,58T piutang Catatan 7 di aset 2024: "
                "AT 0,37x, EM 1,42x, EBIT Gojek +Rp888,6M, dan delta YoY 24→25). Klik baris tabel, grafik rugi, atau kartu kanan.",
            ],
            [
                "Tab 1 Grafik Atas",
                "\"Lintasan ROE GoTo (2023–2025) vs. Pembanding Grab\" batang divergen: ROE 2024 Pasca-Exit (−17,97%), 2025 Konsolidasian (−5,23%), "
                "2025 Ekuitas Induk (−3,73%), Grab FY2025 Cons. (+2,96%), Grab FY2025 Parent (+3,98%), dan Batas Cost of Equity (8,45% Hurdle).",
            ],
            [
                "Tab 1 Kartu Tren YoY (Di Bawah)",
                "4 kartu kolom vertikal (dengan pemisah Exit 2023*): (1) Margin Operasi EBIT % (−69,5% → −14,10% → −2,06%, +1.204 bps YoY), "
                "(2) Margin Laba Bersih (−612,2% → −34,38% → −8,20%, +2.618 bps YoY), (3) Perputaran Aset / ATO (0,27x → 0,37x → 0,40x, +8,8% YoY), "
                "dan (4) ROE Konsolidasian vs. Grab +2,96% (−253,4% → −17,97% → −5,23%, +1.274 bps YoY).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Membandingkan 2023 Pra-Exit vs. 2025 Pasca-Exit: Margin Laba Kotor (65,55% → 57,72%), Margin Operasi (−69,52% → −2,06%), "
                "Perputaran Aset (0,273x → 0,400x), dan ROE Konsolidasian (−253,4% → −5,23%; Induk −3,73%).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan rumus metrik yang diklik + 12 baris Tabel Perhitungan Slide (3 baris teratas + tombol \"Lihat semua baris (+9 lagi)\" untuk DuPont 3 & 5 faktor, ROA, beban pajak & bunga).",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Foto bukti Laporan Laba Rugi Auditan + 2 jadwal lipat: \"Ringkasan Keuangan Historis & Pro Forma Konsolidasian (Rp miliar)\" (11 baris) dan \"DuPont 2025\" (4 baris).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 9 jejak (7 kuliah + 2 tugas). \"Tampilkan Analisis\" membahas selisih ROE dengan Grab; \"Appendix A2 ↗\" melompat ke Slide 16.",
            ],
        ],
    },
    {
        "header": "SLIDE 5: Likuiditas dan Z-Score  [1,5 menit  |  Ref: Appendix A3]",
        "goal": "Membuktikan GoTo TIDAK terancam bangkrut (kas kuat Rp21,76T), meski Altman Z-Score terlihat menakutkan akibat akumulasi rugi lama 2023.",
        "script": (
            '"Apakah GoTo berisiko kehabisan kas dalam waktu dekat? Jawabannya tidak. GoTo memegang Rp21,76 triliun kas, menghasilkan Rasio Lancar '
            'yang kuat sebesar 2,73x dan modal kerja positif Rp18,41 triliun. Setelah memasukkan seluruh pinjaman jangka pendek dan liabilitas sewa, '
            'rasio utang terhadap ekuitas masih terkendali di 26,97%. Lalu mengapa Altman Z-Score terbaca -4,72, jauh di zona distress di bawah 1,81? '
            'Lihat rincian lima faktornya: Likuiditas (X1) dan Solvabilitas (X4) keduanya positif dan sehat. Seluruh tarikan negatif berasal dari X2 '
            '(Defisit Akumulasi -Rp215,3 triliun) akibat penghapusan goodwill Tokopedia tahun 2023—bukan krisis kas saat ini."'
        ),
        "bullets": [
            "Kas & Likuiditas: Kas Rp21,76T | Rasio Lancar 2,73x (2024 direvisi dari 2,46x ke 2,62x via Catatan 7) | Modal Kerja Rp18,41T",
            "Efisiensi Modal Kerja (Catatan 6): DSO Piutang Usaha 10,56 hari (2024) → 10,90 hari (2025) | DPO 59,1 hari | CCC negatif −47,5 hari",
            "Solvabilitas & TIE (Catatan 19–20 & 27b): Utang/Ekuitas penuh 26,97% (0,27x; utang+sewa Rp7,74T) | TIE −0,71x (−Rp378M EBIT / Rp535M bunga)",
            "Altman Z-Score: −4,72 (Nilai Buku X4 = 1,68x) / −4,80 (Pasar Rp25 X4 = 1,56x), didorong X2 (−6,59 tertimbang) dari rugi historis 2023",
        ],
        "popup_rows": [
            [
                "Dua Tampilan Popup di Slide 5",
                "Slide 5 memiliki DUA layout popup berbeda tergantung baris yang diklik: (A) klik \"Likuiditas & Siklus Modal Kerja\" / \"Solvabilitas & Cakupan Bunga\" "
                "membuka kartu rasio neraca; (B) klik \"Altman Z-Score\" membuka grafik faktor Z-Score.",
            ],
            [
                "Tab 1 — Tampilan A (Klik Likuiditas / TIE)",
                "Menampilkan 4 kartu kolom vertikal langsung di kartu grafik utama DAN mengaktifkan tombol \"Laporan Lama (Dengan 2023)\" vs. \"Laporan Akhir (Pasca-Exit)\": "
                "(1) Rasio Lancar (Lama: 2,62x / 2,46x merah / 2,73x → Akhir: 2,62x / 2,73x), (2) Utang / Ekuitas (Lama: 9,69% / 12,57% → Akhir: 15,85% / 26,97%), "
                "(3) DSO Piutang (Lama: lonjakan salah 46,88h → Akhir: 10,56h / 10,90h), dan (4) Times Interest Earned (−4,54x → −0,71x live via Catatan 27b).",
            ],
            [
                "Tab 1 — Tampilan B (Klik Altman Z-Score)",
                "Grafik atas menampilkan \"Komponen Tertimbang Altman Z-Score (FY2025)\" batang divergen: 1,2×X1 (+0,48), 1,4×X2 (−6,59 merah), "
                "3,3×X3 (−0,03), 0,6×X4 (+1,01), 1,0×X5 (+0,40), Total Z = −4,72 / −4,80. Di bawahnya terdapat 4 kartu tren YoY Likuiditas & Solvabilitas (2023*–2025).",
            ],
            [
                "Tab 2: Pra vs. Revisi",
                "Perbandingan berdampingan Dek Awal vs. Laporan Akhir: Rasio Lancar 2024 (2,46x → 2,62x), DSO Piutang Usaha 2024 (46,88 hari → 10,56 hari), "
                "Utang / Ekuitas 2024 (12,57% → 15,85%), dan Interest Coverage / TIE (N/M → −0,71x di 2025).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Rumus rasio yang diklik + semua 16 baris Tabel Perhitungan Slide (3 teratas + \"Lihat semua baris (+13 lagi)\" mencakup CR, QR, WC, D/E, TIE, DSO/DIO/DPO/CCC, X1–X5, Z-Score).",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Foto bukti Neraca / Catatan 20 / Defisit Akumulasi + jadwal lipat \"Perhitungan lima faktor Minggu 6 yang lengkap\" (5 baris).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 9 jejak. \"Tampilkan Analisis\" menjelaskan uji sensitivitas X4 buku vs. pasar; \"Appendix A3 ↗\" melompat ke Slide 17.",
            ],
        ],
    },
    {
        "header": "SLIDE 6: Arus Kas dan Kualitas Akuntansi  [2,0 menit  |  Ref: Appendix A3]",
        "goal": "Menjelaskan mengapa kualitas kas masih lemah (FCF −Rp875M) dan menyoroti 3 temuan bendera merah (red flags) akuntansi utama.",
        "script": (
            '"Beralih ke Arus Kas dan Kualitas Akuntansi, kesimpulan utamanya adalah arus kas operasi positif belum cukup mendanai investasi. '
            'Pada 2025, Arus Kas Operasi (CFO) berbalik positif tipis +Rp307 miliar meski sudah menyerap Rp2,02 triliun untuk ekspansi pinjaman GoPay. '
            'Namun GoTo membelanjakan Rp1,18 triliun untuk CapEx tunai, sehingga Arus Kas Bebas (FCF) tetap negatif -Rp875 miliar—artinya CFO baru '
            'menutup 25,97% CapEx. Kami juga mencatat tiga risiko akuntansi: pertama, saham Tokopedia (Rp7,43T) dan Bank Jago (Rp2,89T) mencapai 22,6% '
            'total aset, sehingga penurunan nilai 20% akan memotong ekuitas Rp1,82 triliun (6,3%); kedua, Rp1,08T insentif dicatat di biaya pemasaran dan '
            'pendapatan pihak berelasi mencapai 7,13%; ketiga, provisi kredit GoPay melonjak 135%, sementara pengeluaran Rp5,46T transfer takberwujud '
            'Tokopedia menurunkan CapEx lanjutan 2024 dari 41,0% menjadi 6,63%."'
        ),
        "bullets": [
            "CFO FY2025: +Rp307M (setelah arus keluar pinjaman Rp2,02T) | CapEx Tunai: −Rp1.182M → FCF: −Rp875M (CFO menutup 25,97% CapEx)",
            "Rasio Akrual: −11,21% (2024) → −3,95% (2025 dilaporkan); −3,69% → −1,94% (akrual berulang yang disesuaikan)",
            "3 Risiko Akuntansi: (1) Tokopedia Rp7,43T + Bank Jago Rp2,89T = 22,57% aset (uji pangkas 20% = −Rp1,82T / −6,34% ekuitas); "
            "(2) Rp1,08T promo di S&M & 7,13% pendapatan pihak berelasi; (3) Provisi Catatan 7 +134,9% (+500 bps rugi = −Rp136,5M)",
            "Pembersihan CapEx 2024 (Catatan 12): Menghapus Rp5.465M aset takberwujud Tokopedia menurunkan CapEx 2024 dari 41,01% menjadi 6,63%",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 3 baris visual (\"Arus kas operasi\", \"Capex tunai\", \"Arus kas bebas\") atau 3 kartu Risiko di sebelah kanan "
                "(pada mode Laporan Akhir menampilkan Risiko 1: Tokopedia & Jago, Risiko 2: Biaya Promo & Pihak Berelasi, Risiko 3: Kredit Macet GoPay).",
            ],
            [
                "Tab 1 Grafik Atas",
                "\"Arus Kas FY2025 & Normalisasi CapEx 2024\" batang divergen: CFO FY2025 (+307,0M), CapEx Tunai FY2025 (−1.182,4M), "
                "Arus Kas Bebas FCF (−875,3M merah), Pencairan Deposito (+1.386,5M), dan CFI Inti Ex-Deposito (−867,4M).",
            ],
            [
                "Tab 1 Kartu Tren YoY (Di Bawah)",
                "4 kartu kolom vertikal (dengan pemisah Exit 2023*): (1) Arus Kas Operasi (−Rp4,33T → −Rp622,1M → +Rp307,0M), "
                "(2) CapEx Lanjutan / Pendapatan (1,49% → 6,63% → 6,45%), (3) Rasio Akrual Dilaporkan (−159,3% → −11,21% → −3,95%), "
                "dan (4) Akrual Laba Berulang (−13,73% → −3,69% → −1,94%).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "\"Normalisasi Arus Kas & CapEx: Terdistorsi vs. Berlanjut\": CapEx Tunai (41,01% → 6,45%; lanjutan 2024 = 6,63%), "
                "Arus Kas Operasi (−Rp622,1M → +Rp307,0M), Arus Kas Bebas (−Rp7.141M → −Rp875,3M), Rasio Akrual (−11,21% → −3,95%).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Rumus item yang diklik + 6 baris Tabel Perhitungan Slide (3 teratas + \"Lihat semua baris (+3 lagi)\": FCF, Cakupan CapEx, Akrual, Asosiasi/Aset, Pihak Berelasi, Sensitivitas 20%).",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Foto bukti Laporan Arus Kas hal. 21 + jadwal lipat \"Temuan akuntansi dan catatan kaki Milestone 3\" (6 baris).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 10 jejak (8 kuliah + 2 tugas). Tombol \"Tampilkan Analisis\" kanan atas menjelaskan matematika akrual & impairment; \"Appendix A3 ↗\" melompat ke Slide 17.",
            ],
        ],
    },
    {
        "header": "SLIDE 7: Asumsi Proyeksi  [1,75 menit  |  Ref: Appendix A4]",
        "goal": "Menjelaskan 3 skenario proyeksi dan menunjukkan bagaimana mengeluarkan data 2023 pra-Tokopedia membersihkan asumsi Base Case.",
        "script": (
            '"Sekarang mari kita lihat asumsi proyeksi tiga tahun ke depan. Ini adalah perbaikan paling penting di Laporan Akhir kami. Pada draf awal, '
            'kami merata-ratakan tahun 2023 dengan 2024 dan 2025. Akibatnya, OpEx 2023 pra-Tokopedia sebesar 117% menyeret OpEx Base Case ke 78,5% dan '
            'transfer aset Tokopedia 2024 membuat rata-rata CapEx terlihat 16,3%. Setelah kami menyandarkan Base Case murni pada bisnis Gojek + GoPay '
            'pasca-Tokopedia (2024–2025), pertumbuhan pendapatan menjadi 15,27%, COGS 42,28%, Cash OpEx turun menjadi 55,70%, dan CapEx lanjutan 6,45%. '
            'Skenario Optimistis memakai efisiensi laporan interim 1H 2026 (tumbuh 18,0%, COGS 38,1%, OpEx 51,2%), sedangkan Konservatif kembali ke lantai biaya 2024 (tumbuh 7,5%, OpEx 62,8%)."'
        ),
        "bullets": [
            "Dek Awal (Rata-rata 3 Tahun dengan 2023): Pertumbuhan 11,4% | COGS 41,1% | OpEx 78,5% | CapEx 16,3%",
            "Laporan Akhir Base (Pasca-Exit 2024→2025): Pertumbuhan 15,27% | COGS 42,28% (Margin Kotor 57,72%) | Cash OpEx 55,70% (+202 bps spread) | CapEx 6,45%",
            "Optimistis (Efisiensi 1H 2026): Pertumbuhan 18,00% | COGS 38,10% (Margin Kotor 61,90%) | Cash OpEx 51,20% | CapEx 6,45% (slide) / 5,50% (Tabel 11)",
            "Konservatif (Lantai Transisi 2024): Pertumbuhan 7,50% | COGS 46,64% (Margin Kotor 53,36%) | Cash OpEx 62,78% | CapEx 6,63% | Bunga utang 10,25%",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik baris asumsi mana saja (mis. \"Beban pokok / pendapatan\", \"Beban operasi tunai / pend.\", \"Pertumbuhan pendapatan\", \"CapEx / pendapatan\") "
                "atau 3 kartu kanan. Bilah atas mengubah tabel slide antara Dek Awal (rata-rata 3 thn) dan Laporan Akhir (Pasca-Exit).",
            ],
            [
                "Tab 1 Bagian 1 (Grafik Horizontal Atas)",
                "Memiliki pengalih langsung di header grafik: \"Laporan Lama (Dengan 2023)\" (11,40% tumbuh, 41,10% COGS, 78,50% OpEx merah, 16,30% CapEx merah) vs. "
                "\"Laporan Akhir (Pasca-Exit)\" (15,27% tumbuh, 42,28% COGS, 55,70% OpEx, 6,45% CapEx). Tersinkronisasi dengan bilah atas slide!",
            ],
            [
                "Tab 1 Bagian 2 (Hasil Pro Forma)",
                "\"Hasil Pro Forma Laporan Keuangan (2025A → 2028F)\" menampilkan 4 grafik kolom vertikal tepat di bawah grafik utama: Pendapatan Pro Forma (IS), "
                "Laba Operasi / EBIT (IS), Laba Bersih Konsolidasi (IS), dan Saldo Kas Akhir (BS) — berubah otomatis antara Dek Lama dan Laporan Akhir.",
            ],
            [
                "Tab 1 Bagian 3 (Kartu Driver Historis)",
                "\"Lintasan Historis YoY di Balik Asumsi Driver (2023* | 2024–1H26 Pasca-Exit)\": 4 kartu vertikal (COGS/Pendapatan, Cash OpEx/Pendapatan, "
                "Pertumbuhan Pendapatan, CapEx Lanjutan/Pendapatan). Driver yang Anda klik di slide diberi bingkai sorotan fokus!",
            ],
            [
                "Tab 1 Bagian 4 (Tabel Interaktif Bawah)",
                "\"Tabel Asumsi Kunci Laporan Keuangan (Pasca-Tokopedia · Tabel 11)\": 7 baris driver × 6 kolom (2024A, 2025A, Base, Optimis, Konservatif) "
                "termasuk Modal Kerja (10,9h DSO / 59,1h DPO), Suku Bunga Efektif (6,91%), dan Pajak (22%). Arahkan kursor ke sel mana saja untuk melihat tooltip sumber!",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "4 kartu perbandingan Dek Awal vs. Laporan Akhir: Pertumbuhan (11,40% → 15,27%), COGS (41,10% → 42,28%), Cash OpEx (78,50% → 55,70%, −2.280 bps), CapEx (16,30% → 6,45%, −985 bps).",
            ],
            [
                "Tab 3 & Tab 4 (Rumus / Bukti)",
                "Tab 3: rumus driver + 2 baris Tabel Perhitungan Slide. Tab 4: foto bukti Catatan 26 + 2 jadwal lipat (11 driver skenario & penilaian biaya tetap vs. variabel).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 10 jejak. \"Tampilkan Analisis\" menampilkan paragraf khusus \"Pergerakan YoY\" sesuai driver yang diklik. \"Appendix A4 ↗\" melompat ke Slide 18.",
            ],
        ],
    },
    {
        "header": "SLIDE 8: Proyeksi Tiga Tahun  [2,0 menit  |  Ref: Appendix A5]",
        "goal": "Menunjukkan bahwa Base Case pasca-Tokopedia berbalik mencetak laba bersih positif pada 2028F dan menjaga kas Rp19,42T, namun ROIC (+2,70%) masih kalah dari WACC (7,76%).",
        "script": (
            '"Inilah hasilnya ketika kita menjalankan asumsi pasca-Tokopedia yang bersih ke dalam model 3 tahun. Pendapatan tumbuh dari Rp18,32 triliun '
            'di 2025 menjadi Rp28,07 triliun pada 2028F. Laba operasi berbalik positif sejak 2026F (+Rp427 miliar) dan mencapai +Rp567 miliar pada 2028F. '
            'Laba bersih menjadi positif pada tahun ketiga sebesar +Rp25 miliar, dan saldo kas akhir terjaga kuat di Rp19,42 triliun—tidak ada krisis kas. '
            'Namun ada catatan kritis: GoTo butuh pendapatan Rp20,38 triliun hanya untuk impas pada 2026F, menyisakan margin keamanan tipis 3,5% '
            'dan leverage operasi tinggi (28,56x DOL). Yang terpenting, ROIC 2028F hanya +2,70%, masih tertinggal 506 bps di bawah WACC 7,76%."'
        ),
        "bullets": [
            "Base Case Restated (2025A → 2026F → 2028F): Pendapatan Rp18,32T → Rp21,12T → Rp28,07T | EBIT −Rp378M → +Rp426,9M → +Rp567,2M",
            "Laba Bersih & Kas 2028F: Laba Bersih mencapai +Rp25,0M (mencetak laba bersih positif di Tahun ke-3); Kas Akhir kuat di Rp19,42T (vs. Rp968M dek lama)",
            "Risiko Leverage Operasi: Pendapatan Impas 2026F = Rp20,38T → Margin of Safety tipis +3,50% & Degree of Operating Leverage (DOL) 28,56x",
            "Selisih Imbal Hasil Ekonomi: ROIC Base 2028F (+2,70%) tertinggal −506 bps di bawah WACC (7,76%); ROE (+0,09%) tertinggal −836 bps di bawah Ke (8,45%)",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Gunakan bilah pengalih atas (Dek Awal vs. Laporan Akhir) DAN dropdown \"Skenario:\" langsung di atas tabel (Base, Optimistis, Konservatif; "
                "di mode Dek Awal juga ada Rata-rata 2 Thn). Klik baris tabel atau kartu kanan untuk membuka popup.",
            ],
            [
                "Tab 1 Grafik Atas",
                "Memiliki pengalih \"Laporan Lama (Dengan 2023)\" vs. \"Laporan Akhir (Pasca-Exit)\". Laporan Lama menunjukkan EBIT 2026F–2028F −3.854M hingga −4.967M "
                "dan kas terkuras ke +968M. Laporan Akhir menampilkan EBIT Konservatif 2028F (−2.143M), EBIT Base 2026F (+426,9M), EBIT Base 2028F (+567,2M), "
                "NI Base 2028F (+25,0M), dan EBIT Optimis 1H26 (+3.221M).",
            ],
            [
                "Tab 1 Kartu Lintasan Proyeksi",
                "\"Lintasan Proyeksi Base Case (2025A → 2028F)\": 4 kartu kolom vertikal menampilkan Pendapatan (18,32T → 28,07T), EBIT (−378M → +567M), "
                "Laba Bersih (−1.502M → −84,5M → −33,6M → +25,0M), dan Kas Akhir (21,76T → 19,42T).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "\"Dampak Proyeksi 2028F: Dek Lama vs. Laporan Akhir Pasca-Exit\": EBIT 2028F (−Rp4.967M → +Rp567,2M), Laba Bersih 2028F (−Rp4.348M → +Rp25,0M), "
                "Kas Akhir 2028F (Rp0,97T → Rp19,42T, menghemat +Rp18,45T), dan ROIC vs. WACC 2028F (Negatif → +2,70% vs. 7,76%, selisih −506 bps).",
            ],
            [
                "Tab 3 & Tab 4 (Rumus / Bukti)",
                "Tab 3 menampilkan rumus yang diklik (mis. Titik Impas 2026F = Rp11.764,6M / 57,723% = Rp20.381,1M) + 4 baris Tabel Perhitungan Slide. "
                "Tab 4 berisi 5 jadwal lipat (IS Base, Neraca Base, Arus Kas Base, Titik Impas & DOL, Uji Sensitivitas).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 10 jejak. \"Tampilkan Analisis\" membahas hasil Base, Optimis 1H26, dan Konservatif 2024; \"Appendix A5 ↗\" melompat ke Slide 19.",
            ],
        ],
    },
    {
        "header": "SLIDE 9: Biaya Modal  [1,25 menit  |  Ref: Appendix A6]",
        "goal": "Menjelaskan langkah demi langkah penyusunan Biaya Ekuitas (8,45%), Biaya Utang Setelah Pajak (5,39%), dan WACC (7,76%) dari sumber pasar tertanggal.",
        "script": (
            '"Untuk mendiskontokan arus kas masa depan GoTo, kita membangun tingkat diskonto dari data pasar bertanggal. Pertama, untuk Biaya Ekuitas, '
            'kita mulai dari imbal hasil obligasi pemerintah RI 10 tahun sebesar 6,120% per 30 Desember 2025, lalu dikurangi sovereign default spread '
            'Damodaran 1,618% agar risiko negara tidak dihitung ganda, menghasilkan Risk-Free Rate IDR bersih sebesar 4,502%. Menambahkan Beta GoTo 0,59 '
            'dikali total premi risiko saham Indonesia (4,230% ERP pasar maju + 2,465% CRP Indonesia) menghasilkan Biaya Ekuitas (Ke) sebesar 8,45%. '
            'Kedua, untuk Biaya Utang, beban bunga FY2025 Rp535 miliar dibagi total utang & sewa Rp7,74 triliun memberi 6,91% pra-pajak, atau 5,39% setelah '
            'penghematan pajak 22%. Menggabungkan bobot 77,4% ekuitas pasar dan 22,6% utang menghasilkan WACC dasar sebesar 7,76%."'
        ),
        "bullets": [
            "IDR Risk-Free Rate (Rf): 6,120% (SUN RI 10T, 30 Des 2025) − 1,618% (spread Baa2 Damodaran, 1 Jan 2026) = 4,502%",
            "Biaya Ekuitas (Ke): 4,502% + 0,59 (Beta) × [4,230% (Mature ERP) + 2,465% (CRP Indonesia)] = 8,452% (dibulatkan 8,45%)",
            "Biaya Utang Setelah Pajak (Kd): (Rp535,15M Catatan 27b ÷ Rp7.742,64M Catatan 19–20 = 6,912%) × (1 − 22% pajak) = 5,390% (WACC tanpa tax shield: 8,101%)",
            "Bobot Modal & WACC: 77,42% Ekuitas (Rp26.550,3M @ Rp25/sh) × 8,452% + 22,58% Utang (Rp7.742,6M) × 5,390% = 7,761% (dibulatkan 7,76%)",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik baris mana saja pada tabel Slide 9 (Ke, Biaya utang, Bobot ekuitas, Bobot utang, WACC) atau kartu kanan. "
                "Popup akan langsung membuka sub-tab komponen yang sesuai!",
            ],
            [
                "Sub-Menu Interaktif Khusus Tab 1",
                "Slide 9 mengganti grafik standar dengan tampilan berdampingan tanpa gulir \"Sumber & Perhitungan\" yang memiliki 6 pil sub-tab di atas "
                "(serta tombol navigasi ← dan → di kartu kiri):",
            ],
            [
                "Sub-Tab 1: Risk-Free (4,502%)",
                "Kiri: angka besar 4,502% + rumus + umpan ke Langkah 2 & batas g. Tabel kanan: Yield SUN RI 10T 6,120% (Investing.com 30 Des 2025) − Sovereign Default Spread 1,618% (Damodaran 1 Jan 2026).",
            ],
            [
                "Sub-Tab 2: CAPM / Ke (8,452%)",
                "Tabel kanan merinci Rf (4,502%), Levered Beta 5T (0,59; uji stres s/d 1,30), Mature ERP (4,230%), CRP Indonesia (2,465%), dan 3 langkah matematika hingga 8,452%.",
            ],
            [
                "Sub-Tab 3: Biaya Utang (5,390%)",
                "Tabel kanan menautkan Beban Keuangan FY2025 Rp535,15M (Catatan 27b hal. 131) ÷ Total Utang & Sewa Rp7.742,64M (Catatan 19–20 hal. 105–111) = 6,912% × (1 − 22%) = 5,390% (uji 0% tax shield → WACC 8,101%).",
            ],
            [
                "Sub-Tab 4: Bobot Modal (77,4% / 22,6%)",
                "Tabel kanan: Harga Saham Rp25,00 × 1.062,01M saham (Catatan 31 hal. 16) = Ekuitas Pasar Rp26.550,3M vs. Utang Rp7.742,6M = Total Modal Rp34.292,9M (77,42% E / 22,58% D).",
            ],
            [
                "Sub-Tab 5: WACC (7,761%)",
                "Tabel kanan: Komponen Ekuitas 6,544% (77,42% × 8,452%) + Komponen Utang 1,217% (22,58% × 5,390%) = WACC Dasar 7,761% (Tanpa Tax Shield: 8,101%).",
            ],
            [
                "Sub-Tab 6: Terminal g (3,00%)",
                "Membuktikan g bukan tebakan: NOPAT 2028F (+Rp442,4M) & Reinvestasi Bersih (Rp559,3M) ÷ Invested Capital Awal (Rp16.380,8M) → Reinvestment Rate 126,42% × ROIC 2,70% = plafon +3,41% → dipilih 3,00% (< Rf 4,502% & cocok target inflasi BI 2,5% ± 1%).",
            ],
            [
                "Tab 2–5 & Appendix A6",
                "Catatan: \"Tampilkan Analisis\" disembunyikan di Slide 9 karena Tab 1 sudah menyajikan tata letak 6 langkah. Tab 2 (Pra vs. Pasca Exit), Tab 3 (rumus KaTeX + 7 baris kalkulasi), "
                "Tab 4 (bukti Catatan 20 + 2 jadwal), Tab 5 (5 jejak), dan \"Appendix A6 ↗\" (Slide 20) semuanya aktif.",
            ],
        ],
    },
    {
        "header": "SLIDE 10: DCF dan Residual Income  [2,25 menit  |  Ref: Appendix A6]",
        "goal": "Menjelaskan mengapa Base DCF berbalik positif ke +Rp10,38/saham (ditopang Kas Bersih) sementara Residual Income tetap negatif (−Rp12,23/saham), beserta stabilitas sensitivitas.",
        "script": (
            '"Sekarang mari kita terapkan dua model valuasi intrinsik: Discounted Cash Flow (DCF) dan Residual Income (RI). Pada draf lama, biaya 2023 '
            'menekan DCF menjadi -Rp121,1 dan RI menjadi -Rp75,1. Setelah 2023 dikeluarkan di Laporan Akhir, Base DCF berbalik positif menjadi +Rp10,38 per saham. '
            'Mengapa? Karena GoTo memiliki Kas Bersih Rp14,01 triliun (Rp13,19 per saham). Walau EBIT positif, belanja CapEx yang besar tetap membuat arus kas bebas negatif, '
            'menghasilkan Enterprise Value operasi negatif sebesar -Rp2,99 triliun. Kas Bersih dikurangi EV negatif menyisakan +Rp11,02 triliun atau +Rp10,38 per saham. '
            'Sementara itu, Residual Income tetap -Rp12,23 per saham karena ROE 2028F (+0,09%) jauh di bawah Biaya Ekuitas 8,45%. Dari tabel sensitivitas, di rentang '
            'WACC 6,76%–8,76% dan g 1%–4%, nilai Base DCF bergerak sempit di Rp8,86 hingga Rp11,18 per saham."'
        ),
        "bullets": [
            "Base Case DCF (Laporan Akhir): Kas Bersih (+Rp14.012,5M = +Rp13,19/sh) dikurangi EV Negatif (−Rp2.988,5M) = +Rp11.024,0M → +Rp10,38/saham",
            "Base Case Residual Income: BVE Rp28.711,7M − PV(RI) Rp41.698,6M → −Rp12,23/saham (g = 3,0%) | +Rp0,24/sh (lantai g = 0%) | +Rp21,13/sh (jika ROE = Ke Thn 4+)",
            "Cek Pertumbuhan Terminal Fundamental: Reinvestasi 126,42% × ROIC 2028F +2,70% = plafon +3,41% → ditetapkan 3,00% (< 4,502% Rf, 7,76% WACC, 8,45% Ke)",
            "Matriks Sensitivitas WACC × g: Sepanjang WACC 6,76%–8,76% dan g 1,0%–4,0%, Base DCF terkunci ketat di Rp8,86–Rp11,18/saham",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Gunakan bilah pengalih atas (Dek Awal vs. Laporan Akhir; di mode Dek Awal muncul dropdown \"Basis Proyeksi:\" 3-Thn vs. 2-Thn). "
                "Klik baris tabel DCF vs. RI, grafik rentang valuasi, atau 3 kartu kanan.",
            ],
            [
                "Tab 1 Bagian 1 (Grafik Divergen Atas)",
                "Memiliki pengalih \"Laporan Lama (Dengan 2023)\" vs. \"Laporan Akhir (Pasca-Exit)\" dengan garis putus-putus \"Kas Bersih Rp13,19\". "
                "Laporan Lama menunjukkan DCF −Rp121,10 & RI −Rp75,10. Laporan Akhir menampilkan 5 batang: Base RI g=3,0% (−Rp12,23), Base RI g=0% (+Rp0,24), "
                "Base DCF Pasca-Exit (+Rp10,38), Kas Bersih / Saham (+Rp13,19), dan RI Konvergensi Thn 4+ (+Rp21,13).",
            ],
            [
                "Tab 1 Bagian 2 (Matriks Sensitivitas 2D)",
                "\"Uji Sensitivitas DCF Base Case: WACC × Pertumbuhan Terminal g (Rp / saham · Tabel 16)\": 3 baris (WACC 6,76%, 7,76% Baseline, 8,76%) × 5 kolom "
                "(g = 1,0%, 2,0%, 3,0% Base, 3,5%, 4,0%), berkisar Rp8,86–Rp11,18/saham—menjelaskan mengapa WACC lebih tinggi sedikit menaikkan DCF (mengecilkan EV negatif).",
            ],
            [
                "Tab 1 Bagian 3 (Tabel Uji Stres & Batas)",
                "\"Uji Stres Beta, WACC Tanpa Tax Shield & Batas Residual Income (Tabel 14–16)\": 6 baris membandingkan Beta Dasar 0,59 (+Rp10,38 / −Rp12,23), "
                "WACC Tanpa Tax Shield 8,10% (+Rp10,52), Beta Teknologi Normal 1,01 (+Rp11,09 / −Rp8,45), Beta Tinggi 1,30 (+Rp11,36 / −Rp6,00), "
                "Batas RI g = 0% (+Rp0,24), dan Konvergensi RI Thn 4+ (+Rp21,13).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "4 kartu perbandingan merangkum lonjakan DCF +Rp131,48/sh (−Rp121,10 → +Rp10,38), RI (−Rp54,40 / −Rp75,10 → −Rp12,23), "
                "Rentang Nilai Intrinsik (Negatif → Rp10,38–16,75), dan rekomendasi SELL / AVOID yang tetap utuh.",
            ],
            [
                "Tab 3 & Tab 4 (Rumus / Bukti)",
                "Tab 3 menampilkan rumus jembatan ekuitas + 6 baris Tabel Perhitungan Slide (\"Lihat semua baris (+3 lagi)\"). Tab 4 memuat 7 jadwal lipat "
                "(Jembatan DCF vs. RI, Sensitivitas Beta/WACC/g, Alasan 3% g, Jadwal FCFF, Jadwal RI, Hitungan Grab, Pengecualian Pembanding).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 6 jejak. \"Tampilkan Analisis\" menjelaskan alasan EV negatif meski EBIT positif. \"Appendix A6 ↗\" melompat ke Slide 20.",
            ],
        ],
    },
    {
        "header": "SLIDE 11: Perbandingan Grab dan Valuasi  [2,25 menit  |  Ref: Appendix A6]",
        "goal": "Menjelaskan alasan hanya memakai Grab, mengapa Rp91,02 ditolak, dan bagaimana 7 batang Football Field menjangkarkan rentang Rp10,38–Rp16,75.",
        "script": (
            '"Untuk valuasi relatif, kami memilih Grab Holdings sebagai satu-satunya pembanding karena Grab memiliki kombinasi bisnis terdekat: transportasi, '
            'pesan-antar makanan, dan layanan keuangan digital. Kami mengeluarkan Sea (tercampur game Garena), Bukalapak (terdistorsi laba investasi), '
            'dan Blibli (ritel toko fisik dengan EBITDA negatif). Per 31 Desember 2025, Grab diperdagangkan pada 3,04x Price-to-Book. Mengalikan 3,0391x '
            'dengan Nilai Buku per Saham Induk GoTo sebesar Rp29,95 menghasilkan Rp91,02 per saham. Namun kami menolak Rp91,02 sebagai target wajar karena '
            'Grab sudah mencetak laba (ROE +2,96%), sedangkan ROE GoTo masih negatif (-5,23%) di bawah biaya modalnya. Pada peta Football Field, rentang '
            'nilai wajar yang dapat dipertanggungjawabkan adalah Rp10,38 (Base DCF) hingga Rp16,75 (Optimistic RI), berpusat di Kas Bersih Rp13,19. '
            'Harga acuan pasar Rp25,00 berada 49% hingga 141% di atas rentang nilai intrinsik kami."'
        ),
        "bullets": [
            "P/B Grab (31 Des 2025): US$4,99 ÷ US$1,6419 BVPS = 3,0391x × BVPS Induk GoTo (Rp29,9479) = Rp91,02/saham (Ditolak sebagai target wajar)",
            "Pembanding yang Dikeluarkan: Sea (Shopee tergabung dengan Garena & Monee), BUKA (keuntungan investasi), BELI (ritel fisik & EBITDA negatif)",
            "Rentang Nilai Intrinsik Wajar: Rp10,38 (lantai Base DCF) → Rp13,19 (pusat Kas Bersih) → Rp16,75 (plafon Optimistic RI biaya 1H26)",
            "Harga Acuan Pasar: Rp25,00/saham berada 49%–141% di atas rentang wajar (risiko turun −33% hingga −58%)",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik baris tabel Grab (\"Grab P/B\", \"BVPS Induk GoTo\", \"Rentang Nilai Intrinsik Wajar\"), kartu pembanding yang dikeluarkan (Shopee/Sea, BUKA, BELI), atau kartu kanan.",
            ],
            [
                "Tab 1 Bagian 1 (7 Batang Football Field)",
                "\"Peta Valuasi vs. Harga Pasar Rp25,00 & P/B Grab\" batang divergen dengan garis vertikal putus-putus \"Pasar Rp25,00\": "
                "(1) RI Konservatif (−Rp44,42), (2) Base RI g=3,0% (−Rp12,23), (3) Lantai Base DCF (+Rp10,38), (4) Kas Bersih / Saham (+Rp13,19), "
                "(5) Plafon Opt. RI (+Rp16,75), (6) Opt. DCF 1H26 (+Rp47,34), dan (7) Grab P/B 3,04x (+Rp91,02).",
            ],
            [
                "Tab 1 Bagian 2 (7 Kartu Penjelasan Bar)",
                "\"Rincian Setiap Bar Valuasi Football Field (Rp / Saham)\" menampilkan 7 kartu tepat di bawah grafik. "
                "3 kartu berbingkai hijau menandai rentang wajar inti: Lantai Base DCF (+Rp10,38), Pusat Kas Bersih (+Rp13,19), dan Plafon Opt. RI (+Rp16,75).",
            ],
            [
                "Tab 1 Bagian 3 (Matriks 3 Skenario)",
                "\"Matriks Valuasi 3 Skenario & Rekonsiliasi Rentang Nilai Wajar (Rp / saham · Appendix A6)\": tabel 5 baris membandingkan DCF/sh, RI/sh, dan Interpretasi Ekonomi "
                "untuk Base (+Rp10,38 / −Rp12,23), Optimis 1H26 (+Rp47,34 / +Rp16,75), Konservatif 2024 (−Rp33,95 / −Rp44,42), Kas Bersih (+Rp13,19), dan P/B Grab (Rp91,02).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Menampilkan pergeseran valuasi dari Dek Awal (−Rp121,10 DCF / −Rp75,10 RI) ke rentang Laporan Akhir Rp10,38–Rp16,75.",
            ],
            [
                "Tab 3 & Tab 4 (Rumus / Bukti)",
                "Tab 3 menampilkan rumus P/B Grab + 4 baris Tabel Perhitungan Slide (BVPS Grab, P/B Grab, BVPS GoTo, Tolok Ukur Grab). "
                "Tab 4 memuat bukti Grab 20-F FY2025 / ekuitas GoTo + 2 jadwal lipat (perhitungan Grab & pengecualian pembanding).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 5 jejak. \"Tampilkan Analisis\" merinci matematika \"Basis Rentang Wajar\" (Kas Bersih Rp14.012,5M − EV Rp2.988,5M = +Rp11.024,0M ÷ 1.062,01M sh). \"Appendix A6 ↗\" melompat ke Slide 20.",
            ],
        ],
    },
    {
        "header": "SLIDE 12: Rekomendasi  [2,0 menit  |  Ref: Appendix A6]",
        "goal": "Menyampaikan rekomendasi tegas SELL / AVOID di Rp25,00 lengkap dengan pemicu upgrade ke HOLD / BUY yang terukur serta risiko utama.",
        "script": (
            '"Sebagai penutup bagi investor saham publik jangka pendek: rekomendasi kami adalah SELL / AVOID pada harga acuan Rp25,00. '
            'Bahkan setelah seluruh kesalahan model historis dibersihkan, nilai wajar GoTo berada di Rp10,38 hingga Rp16,75 per saham—artinya Rp25,00 '
            'berada 49% sampai 141% di atas nilai intrinsik dan menghargai saham sebesar 2,4x Base DCF. Apa yang bisa mengubah pandangan kami? Kami menetapkan '
            'pemicu terukur: kami naikkan ke HOLD jika harga turun ke Rp13,20 atau lebih rendah (1,0x Kas Bersih) dengan Arus Kas Bebas positif. Kami baru '
            'naikkan ke BUY jika GoTo mempertahankan efisiensi 1H 2026—Cash OpEx di bawah atau sama dengan 51,2% dan Margin Kotor minimal 61,9%—selama dua '
            'kuartal beruntun. Sebaliknya, jika Cash OpEx naik lagi ke 60%+, provisi kredit GoPay tembus Rp650 miliar, atau nilai Tokopedia turun lebih dari 15%, kasus SELL makin kuat."'
        ),
        "bullets": [
            "Keputusan Final: SELL / AVOID pada Rp25,00 (2,41x Base DCF Rp10,38; 1,90x Kas Bersih Rp13,19; gap −33% s/d −58% ke rentang Rp10,38–Rp16,75)",
            "Pemicu Naik ke HOLD: Harga turun ke ≤ Rp13,20 (1,0x Kas Bersih) DISERTAI Arus Kas Bebas positif (FCF > 0)",
            "Pemicu Naik ke BUY: Cash OpEx ≤ 51,2% DAN Margin Laba Kotor ≥ 61,9% bertahan selama 2 kuartal berturut-turut",
            "Perkuat SELL / Risiko: Cash OpEx ≥ 60,0% ATAU Provisi Kredit ≥ Rp650M ATAU penurunan nilai Tokopedia > 15% (risiko naik: aksi M&A/akuisisi)",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Pastikan bilah atas berada pada \"Laporan Akhir (Restated)\" sehingga 3 baris menampilkan Rekomendasi final (SELL / AVOID), "
                "Spread nilai ekonomi (−506 bps), dan Pemicu re-rating terukur (≤ Rp13,20 / ≤ 51,2%). Klik baris mana saja atau kartu kanan.",
            ],
            [
                "Tab 1 Grafik Atas",
                "\"Spread Ekonomi (ROIC vs. WACC) & Gap Harga Pasar\" batang divergen: 2028F Base ROIC (+2,70%), Base WACC Hurdle (7,76%), "
                "ROIC − WACC Spread (−5,06% merah), 2028F Base ROE (+0,09%), Cost of Equity Ke (8,45%), dan ROE − Ke Spread (−8,36% merah).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Menampilkan 4 kartu perbandingan Dampak Valuasi yang membuktikan SELL / AVOID tetap bertahan di Dek Awal maupun Laporan Akhir.",
            ],
            [
                "Tab 3 & Tab 4 (Rumus / Bukti)",
                "Tab 3 menampilkan rumus spread/pemicu yang diklik (mis. ROIC 2028F +2,70% − WACC 7,76% = −506 bps; ambang BUY/HOLD) dan sumbernya. "
                "Tab 4 tidak diperlukan di Slide 12 (gunakan tombol Appendix A6).",
            ],
            [
                "Tab 5, Analisis & Appendix",
                "Tab 5 berisi 4 jejak. \"Tampilkan Analisis\" merinci alasan SELL, pemicu rating, serta risiko naik/turun. \"Appendix A6 ↗\" melompat ke Slide 20.",
            ],
        ],
    },
    {
        "header": "SLIDE 13: Restatement Forensik: 5 Kesalahan yang Diperbaiki  [1,5 menit  |  Ref: Appendix A6]",
        "goal": "Mengubah temuan kesalahan Milestone 2 dan Milestone 4 menjadi keunggulan dengan transparansi dan ketelitian audit forensik.",
        "script": (
            '"Sebelum menutup, kami ingin transparan mengenai lima kesalahan di draf Milestone 2 dan Milestone 4 sebelumnya yang sudah kami perbaiki '
            'di Laporan Akhir. Pertama dan terbesar: dek lama merata-ratakan biaya 2023 pra-Tokopedia (OpEx 117%) ke dalam Base Case. Mengeluarkan 2023 '
            'menurunkan OpEx Base dari 78,5% menjadi 55,7%, membalik EBIT 2028F dari -Rp4,97 triliun ke +Rp567 miliar, dan mengangkat DCF dari -Rp121,1 menjadi +Rp10,38. '
            'Kedua: kami mengembalikan Rp1,58 triliun piutang pinjaman Catatan 7 tahun 2024 yang terlewat ke aset 2024, membuat selisih neraca menjadi nol '
            'dan menaikkan Rasio Lancar 2024 dari 2,46x ke 2,62x. Ketiga: kami memisahkan Piutang Usaha Catatan 6 dari kredit konsumen Catatan 7, membetulkan '
            'DSO 2024 dari angka bias 46,9 hari menjadi 10,56 hari. Keempat: kami menyelaraskan seluruh utang & sewa Catatan 19–20 dan menautkan beban bunga '
            'Catatan 27b agar TIE terhitung langsung. Kelima: kami mengeluarkan Rp5,46 triliun transfer takberwujud Tokopedia dari CapEx 2024 sehingga CapEx lanjutan turun dari 41,0% menjadi 6,63%."'
        ),
        "bullets": [
            "Koreksi 1 — Keluarkan 2023 Pra-Exit: Rata-rata 3 thn (OpEx 78,5%, CapEx 16,3%) → Pasca-Tokopedia 2024–25 (OpEx 55,70%, CapEx 6,45%); EBIT 2028F −Rp4,97T → +Rp567M; DCF −121,1 → +10,38",
            "Koreksi 2 — Neraca 2024: Kembalikan Rp1.582M pinjaman Catatan 7 → Aset Rp43.208M (Cek = 0); Rasio Lancar 2024 2,46x → 2,62x; EM 1,37x → 1,42x",
            "Koreksi 3 — DSO Piutang Usaha 2024: Pisahkan Piutang Usaha Catatan 6 (Rp460M → 547M) dari pinjaman Catatan 7 → DSO asli 10,56h (vs. lonjakan buatan 46,88h)",
            "Koreksi 4 — Utang Penuh & TIE Live: Masukkan utang jangka pendek + seluruh sewa (Catatan 19–20) + bunga Catatan 27b → D/E 2024 12,57% → 15,85%; TIE live −4,54x → −0,71x",
            "Koreksi 5 — CapEx Lanjutan 2024: Keluarkan Rp5.465M transfer aset takberwujud Tokopedia (Catatan 12) → CapEx lanjutan 41,0% → 6,63%",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 5 baris pada tabel Restatement atau kartu ringkasan di sebelah kanan.",
            ],
            [
                "Tab 1 Grafik Atas (Pengalih Interaktif)",
                "Memiliki pengalih \"Laporan Lama (Dengan 2023)\" vs. \"Laporan Akhir (Pasca-Exit)\" di header grafik: "
                "Laporan Lama menampilkan Base Cash OpEx 78,50% (merah), Raw CapEx 2024 41,00% (merah), Mixed DSO 2024 46,88h (merah), dan Rasio Lancar 2,46x; "
                "Laporan Akhir berubah menjadi OpEx 55,70%, Cont. CapEx 6,63%, Trade DSO 10,56h, dan Rasio Lancar 2,62x.",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Menampilkan 4 kartu perbandingan Dampak Valuasi yang merangkum bagaimana 5 perbaikan restatement mengangkat DCF +Rp131,48/sh namun SELL / AVOID tetap utuh.",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan rumus forensik dan referensi persis (Lampiran B Laporan Akhir Tabel B1 #1–#5 & Catatan LK Auditan 6, 7, 12, 19–20, 27b, 34c).",
            ],
            [
                "Tab 4, Tab 5, Analisis & Appendix",
                "Tab 4 kosong di sini; Tab 5 menyimpan jejak restatement Lampiran B. \"Tampilkan Analisis\" merinci perhitungan sebelum/sesudah koreksi yang diklik. \"Appendix A6 ↗\" melompat ke Slide 20.",
            ],
        ],
    },
    {
        "header": "SLIDE 14: Dek Awal vs. Laporan Akhir: Mengapa SELL Tetap Kuat  [1,5 menit  |  Ref: Appendix A6]",
        "goal": "Menutup presentasi dengan pesan terkuat: memperbaiki seluruh kesalahan justru membuat rekomendasi SELL / AVOID kami JAUH lebih kredibel.",
        "script": (
            '"Sebagai penutup, lihat perbandingan langsung antara Dek Awal dan Laporan Akhir kami. Di dek lama, rekomendasi SELL kami bertumpu pada '
            'DCF -Rp121 yang terdistorsi oleh biaya 2023 pra-Tokopedia. Setelah memperbaiki kelima kesalahan tersebut, Base Case GoTo memang tampak jauh '
            'lebih sehat: EBIT berbalik positif (+Rp567M pada 2028F), kas bertahan kuat di Rp19,4 triliun, dan DCF naik menjadi +Rp10,38. Namun '
            'rekomendasi SELL / AVOID kami justru menjadi jauh lebih kuat sekarang, karena bahkan dengan model pasca-Tokopedia yang benar-benar bersih, '
            'ROIC GoTo 2,70% masih kalah dari WACC 7,76%, dan rentang nilai intrinsiknya Rp10,38 hingga Rp16,75 masih terpaut jauh di bawah Rp25,00. '
            'Terima kasih. Kami siap menjawab pertanyaan Bapak/Ibu dan teman-teman, serta telah menyiapkan Lampiran A1 hingga A6 jika ingin memeriksa jadwal pendukung."'
        ),
        "bullets": [
            "Cash OpEx Base (% Pendapatan): 78,5% (Dek Lama) → 55,70% (Laporan Akhir, −2.280 bps pasca-Tokopedia)",
            "EBIT & Laba Bersih Base 2028F: EBIT −Rp4.967M → +Rp567,2M (positif sejak 2026F) | Laba Bersih −Rp4.489M → +Rp25,0M (laba bersih positif Tahun ke-3)",
            "Saldo Kas Akhir 2028F: Rp968M (Dek Lama) → Rp19.421M / Rp19,42T (Laporan Akhir — tidak ada krisis likuiditas)",
            "Valuasi & Keputusan: Base DCF −Rp121,1 → +Rp10,38 | Base RI −Rp75,1 → −Rp12,23 | Rentang Wajar Rp10,38–Rp16,75 (33%–58% di bawah Rp25,00) → SELL / AVOID tetap kokoh",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 8 baris rekonsiliasi (Base OpEx, EBIT, Laba Bersih, Kas Akhir, DCF, RI, Rentang Wajar, Rekomendasi) atau kartu kanan.",
            ],
            [
                "Tab 1 Grafik Atas",
                "\"Spread Ekonomi (ROIC vs. WACC) & Gap Harga Pasar\" batang divergen: 2028F Base ROIC (+2,70%), Base WACC Hurdle (7,76%), "
                "ROIC − WACC Spread (−5,06% merah), 2028F Base ROE (+0,09%), Cost of Equity Ke (8,45%), dan ROE − Ke Spread (−8,36% merah).",
            ],
            [
                "Tab 2: Pra vs. Pasca Exit",
                "Tidak aktif pada Slide 14 (karena tabel utama Slide 14 itu sendiri sudah merupakan perbandingan berdampingan Dek Awal vs. Laporan Akhir).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan rumus persis dan referensi Laporan Akhir (Tabel 11, 12, 15, 16 & §5.3 / §6.1) untuk baris rekonsiliasi yang diklik.",
            ],
            [
                "Tab 4, Tab 5, Analisis & Appendix",
                "Tab 4 kosong; Tab 5 menyimpan jejak rekonsiliasi Laporan Akhir §6.1. \"Tampilkan Analisis\" merangkum mengapa operasional yang sehat tetap menghancurkan nilai ekonomi. "
                "\"Appendix A6 ↗\" melompat ke Slide 20 untuk cadangan tanya-jawab.",
            ],
        ],
    },
]

APPENDIX_SLIDES = [
    {
        "header": "SLIDE 15 (APPENDIX A1): Lampiran A1 — Jembatan Pendapatan & Risiko Persaingan  [Cadangan Q&A | Tautan dari Slide 2 & 3]",
        "goal": "Menyediakan rincian angka jembatan pendapatan Catatan 29 FY2025 serta matriks pinjaman GoPay Catatan 35 & Porter Five Forces saat sesi tanya-jawab.",
        "script": (
            '"Jika kita melompat ke Lampiran A1, terlihat rekonsiliasi lengkap dari Catatan 29 laporan keuangan auditan FY2025: Gojek menyumbang Rp12.361,3 miliar, '
            'GoTo Financial menambah Rp5.190,6 miliar, dan imbalan jasa Tokopedia sebesar Rp819,7 miliar. Setelah dikurangi eliminasi promo antar-segmen Rp49,5 miliar, '
            'didapat angka pendapatan bersih konsolidasian persis Rp18.322,1 miliar. Di bawahnya, Jadwal 2 menunjukkan pinjaman GoPay Catatan 35 melesat 72,6% ke '
            'Rp2.731 miliar sementara provisi kerugian kredit melonjak 134,9% ke Rp407,7 miliar di samping belanja pemasaran Rp3,09T dan pengembangan produk Rp2,15T."'
        ),
        "bullets": [
            "Tabel 1 — Jembatan Pendapatan (Rp miliar): Gojek 12.361,259 + GoTo Financial 5.190,617 + Imbalan Tokopedia 819,724 = 18.371,600 − Eliminasi 49,483 = 18.322,117",
            "Jadwal 2 — Eksposur Pinjaman GoPay Catatan 35: Piutang pembiayaan bersih Rp1.582M (2024) → Rp2.731M (2025, +72,6%); Cadangan kerugian kredit Rp173,6M → Rp407,7M (+134,9%)",
            "Biaya Persaingan & Matriks Porter: S&M Rp3,09T | R&D Rp2,15T | Pendatang Baru Rendah–Sedang | Pemasok Rendah | Pembeli & Substitusi Sedang | Rivalitas Tinggi",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik baris mana saja pada tabel \"Jembatan pendapatan ke pendapatan konsolidasi GoTo\" atau jadwal \"Eksposur Pinjaman GoPay Catatan 35 & Matriks Porter\" di bawahnya.",
            ],
            [
                "Tab 1: Grafik Angka Lampiran",
                "Menampilkan \"Visualisasi Angka Pendukung Lampiran\" batang divergen dari catatan perhitungan A1: Pendapatan Konsolidasi (Rp18.322,117M) dan Pertumbuhan Provisi (134%).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan sumber baris yang diklik + Tabel Perhitungan Slide 2 baris (Pendapatan Konsolidasi & Pertumbuhan Provisi).",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Menampilkan gambar bukti Catatan 29 / Catatan 35 (klik untuk perbesar) + jadwal lipat Matriks Catatan 35 & Lima Kekuatan Porter.",
            ],
            [
                "Tab 5, Analisis & Navigasi",
                "Tab 5 memuat 15 jejak (kuliah & Milestone 1/4). \"Tampilkan Analisis\" merangkum pendapatan segmen & imbalan Tokopedia. "
                "Footer slide menyediakan tombol \"← Kembali ke Slide 2/3\" serta pil lompat cepat A1–A6.",
            ],
        ],
    },
    {
        "header": "SLIDE 16 (APPENDIX A2): Lampiran A2 — Ringkasan Historis & Pro Forma (FY2023–2028F) & DuPont  [Cadangan Q&A | Tautan dari Slide 4]",
        "goal": "Menampilkan ringkasan 11 baris historis (2023A–2025A) dan proyeksi 3 tahun (2026F–2028F) beserta tabel rumus lengkap DuPont 2025.",
        "script": (
            '"Lampiran A2 menyajikan ringkasan konsolidasian enam tahun lengkap beserta dekomposisi DuPont 2025. Anda bisa menelusuri pendapatan bersih naik '
            'dari Rp14.785 miliar pada 2023 ke Rp18.322 miliar pada 2025, margin kotor pulih dari 53,4% di 2024 menjadi 57,7% di 2025, dan rugi operasi '
            'menyusut dari Rp10.279 miliar menjadi Rp378 miliar. Di bawah tabel ringkasan, jadwal DuPont 2025 membuktikan bagaimana margin bersih -8,2% × '
            'perputaran aset 0,40x × pengganda ekuitas 1,59x menghasilkan ROE konsolidasian -5,23%."'
        ),
        "bullets": [
            "Tabel 1 — Ringkasan 11 Baris (2023A–2028F Base): Pendapatan Bersih, Laba Kotor, Margin Kotor %, EBIT, Laba Bersih, CFO, CapEx Tunai, FCF/FCFF, Kas Akhir, Total Utang, Ekuitas",
            "Jadwal 2 — DuPont 2025 (4 baris): Margin Bersih −8,2% (−1.501.685 / 18.322.117) × Perputaran Aset 0,40x (18.322.117 / 45.757.642) × Pengganda Ekuitas 1,59x (45.757.642 / 28.711.657) = −5,23% ROE",
            "Catatan Kolom Pro Forma Dek Awal: A2 menjaga kolom Milestone 4 yang disubmit untuk ketelusuran, berdampingan dengan angka restatement Laporan Akhir pada Slide 4, 8, dan 14",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 11 baris ringkasan historis/pro forma atau salah satu dari 4 baris pada jadwal \"DuPont 2025\" di bawah.",
            ],
            [
                "Tab 1: Grafik Angka Lampiran",
                "Menampilkan \"Visualisasi Angka Pendukung Lampiran\" dari catatan A2 (Rugi Operasi −378M, Margin Kotor 57,7%, Margin Operasi −2,1%, Margin Bersih −8,2%, ATO 0,40x, EM 1,59x).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan langkah metrik yang diklik + semua 12 baris Tabel Perhitungan Slide (Laba Operasi, GM, OM, NM, ATO, EM, ROA, ROE, DuPont 3-faktor, DuPont 5-faktor, Beban Pajak & Bunga).",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Menampilkan gambar bukti Laba Rugi / Laba Kotor / OpEx yang disorot (klik untuk perbesar) + jadwal lipat \"DuPont 2025\" 4 baris.",
            ],
            [
                "Tab 5, Analisis & Navigasi",
                "Tab 5 berisi 9 jejak (7 kuliah + 2 tugas). \"Tampilkan Analisis\" membahas lintasan rugi 2023–2025 dan pendorong DuPont. "
                "Footer menyediakan \"← Kembali ke Slide 4\" dan pil lompat cepat A1–A6.",
            ],
        ],
    },
    {
        "header": "SLIDE 17 (APPENDIX A3): Lampiran A3 — Likuiditas, Modal Kerja, Z-Score Minggu 6 & Catatan Kaki  [Cadangan Q&A | Tautan dari Slide 5 & 6]",
        "goal": "Menyajikan pembilang, penyebut, bobot, dan kontribusi eksak Altman Z-Score Minggu 6 beserta 6 temuan red flag akuntansi Milestone 3.",
        "script": (
            '"Lampiran A3 memuat bukti matematis lengkap di balik Slide 5 dan Slide 6. Tabel atas merinci setiap pembilang dan penyebut Altman Z-Score Minggu 6 '
            'berbasis angka auditan FY2025: X1 menyumbang +0,483 dari modal kerja Rp18,41 triliun, X4 menyumbang +1,008 dari kuatnya ekuitas terhadap liabilitas, '
            'dan X5 menambah +0,400. Seluruh skor -4,72 semata-mata ditarik oleh X2 (-6,588) dari akumulasi defisit historis Rp215,33 triliun. Di bawahnya, '
            'tabel Milestone 3 mendokumentasikan rasio akrual -3,95%, porsi Tokopedia dan Bank Jago Rp10,33 triliun (22,57% aset), investasi Level 3 Rp1,67 triliun, '
            'pendapatan pihak berelasi 7,13%, serta uji pangkas aset 20% senilai Rp1,82 triliun."'
        ),
        "bullets": [
            "Tabel 1 — Z-Score 5 Faktor Minggu 6 (Penyebut Total Aset = Rp45.757,642M): X1 = +0,482849 (WC 18.411,7M) | X2 = −6,588355 (RE −215.334,0M) | X3 = −0,027279 (EBIT −378,3M) | X4 = +1,010619 (Ekuitas 28.711,7M / Liab 17.046,0M) | X5 = +0,400417 (Rev 18.322,1M) → Total Z = −4,721750",
            "Jadwal 2 — Temuan Akuntansi & Catatan Kaki Milestone 3 (6 baris): Rasio Akrual −3,95% | Tokopedia Rp7.432M + Bank Jago Rp2.895M (22,57% aset) | Investasi Level 3 Rp1.669M | Pendapatan Pihak Berelasi Rp1.306M (7,13%) | Klasifikasi insentif | Uji pangkas 20% = Rp1.820M pra-pajak",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik baris komponen Z-Score (X1–X5) mana saja di tabel utama atau salah satu dari 6 temuan pada jadwal \"Temuan akuntansi dan catatan kaki Milestone 3\".",
            ],
            [
                "Tab 1: Grafik Angka Lampiran",
                "Menampilkan \"Visualisasi Angka Pendukung Lampiran\" dari catatan kalkulasi teratas A3 (Rasio Lancar 2,73x, Quick Ratio 2,73x, Modal Kerja, D/E 0,27x, Utang/Aset 16,9%, TIE −0,71x).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan SEMUA 22 baris Tabel Perhitungan Slide yang menggabungkan matematika likuiditas/Z-Score Slide 5 dan arus kas/akrual/uji pangkas Slide 6 (\"Lihat semua baris (+19 lagi)\").",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Foto bukti Neraca / Defisit Akumulasi + jadwal lipat \"Temuan akuntansi dan catatan kaki Milestone 3\" (6 baris).",
            ],
            [
                "Tab 5, Analisis & Navigasi",
                "Tab 5 berisi 19 jejak (15 kuliah + 4 tugas). \"Tampilkan Analisis\" merangkum likuiditas vs. skor distress. "
                "Footer menyediakan \"← Kembali ke Slide 5/6\" dan pil lompat cepat A1–A6.",
            ],
        ],
    },
    {
        "header": "SLIDE 18 (APPENDIX A4): Lampiran A4 — Pendorong Skenario, Alasan Proyeksi & Perilaku Biaya  [Cadangan Q&A | Tautan dari Slide 7]",
        "goal": "Menampilkan seluruh 11 pendorong skenario Milestone 4 (Base, Optimis, Konservatif) beserta alasan masing-masing plus penilaian biaya tetap vs. variabel Minggu 12.",
        "script": (
            '"Lampiran A4 memuat ke-11 asumsi proyeksi dari workbook Milestone 4 kami—mulai dari pertumbuhan pendapatan, COGS, beban operasi, DSO, DIO, DPO, '
            'CapEx, depresiasi, tarif pajak 22%, suku bunga utang, dan rasio dividen 0%—lengkap dengan alasan untuk skenario Base, Optimistis, dan Konservatif. '
            'Di bawah tabel 11 baris tersebut, kami sertakan pemisahan perilaku biaya Minggu 12: COGS (cloud hosting, insentif pengemudi) bersifat variabel, '
            'sedangkan G&A, gaji teknologi, dan depresiasi bertindak sebagai biaya tetap yang menciptakan leverage operasi tinggi. Perlu diingat pada Slide 7, 8, '
            'dan 14 kami juga menampilkan asumsi bersih pasca-Tokopedia yang mengeluarkan anomali OpEx 2023 sebesar 117%."'
        ),
        "bullets": [
            "Tabel 1 — Semua 11 Pendorong Skenario (Workbook Milestone 4): Pertumbuhan (11,4% / 15,3% / 7,5%), COGS (41,1% / 38,1% / 46,6%), OpEx (78,5% / 55,7% / 85,0%), DSO (24,2h / 10,9h / 30,0h), DIO (4,8h / 0,7h / 8,0h), DPO (67,8h / 75,0h / 59,1h), CapEx (16,3% / 6,5% / 20,0%), D&A (30,6% / 25,0% / 43,9%), Pajak (22,0%), Bunga (10,2% / 6,9% / 12,9%), Dividen (0,0%)",
            "Jadwal 2 — Penilaian Biaya Tetap dan Variabel (4 baris dari Minggu 12): mengklasifikasikan cloud, server, pemrosesan pembayaran, promo S&M, engineering R&D, dan G&A",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 11 baris driver pada tabel utama atau salah satu dari 4 baris perilaku biaya di jadwal pendukung bawah.",
            ],
            [
                "Tab 1: Grafik Angka Lampiran",
                "Menampilkan \"Visualisasi Angka Pendukung Lampiran\" membandingkan Pertumbuhan Pendapatan Base (11,4%) vs. Asumsi Biaya Operasi (78,5%).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan penjelasan & sumber driver yang diklik + 2 baris Tabel Perhitungan Slide (Pertumbuhan Pendapatan Base & Asumsi Biaya Operasi).",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Menampilkan foto bukti Beban Operasi Catatan 26 + jadwal lipat \"Penilaian biaya tetap dan variabel\" (4 baris).",
            ],
            [
                "Tab 5, Analisis & Navigasi",
                "Tab 5 berisi 10 jejak (8 kuliah + 2 tugas). \"Tampilkan Analisis\" menjelaskan anomali rasio biaya 2023 sebesar 117% dan desain skenario. "
                "Footer menyediakan \"← Kembali ke Slide 7\" dan pil lompat cepat A1–A6.",
            ],
        ],
    },
    {
        "header": "SLIDE 19 (APPENDIX A5): Lampiran A5 — Laporan Pro Forma Tiga Tahun & Leverage Operasi  [Cadangan Q&A | Tautan dari Slide 8]",
        "goal": "Menyajikan model pro forma 3 laporan lengkap untuk Base Case (Laba Rugi, Neraca, Arus Kas) plus perhitungan Titik Impas & DOL.",
        "script": (
            '"Lampiran A5 menyimpan model pro forma tiga laporan penuh di balik Slide 8. Tabel atas menunjukkan Laporan Laba Rugi baris demi baris dari Pendapatan '
            'hingga Laba Kotor, EBIT, Beban Bunga, Pajak, dan Laba Bersih untuk 2026F–2028F. Di bawahnya tersedia empat jadwal pendukung lipat: Proyeksi Neraca '
            '(16 baris), Proyeksi Arus Kas (13 baris), jadwal Titik Impas & Degree of Operating Leverage, serta uji sensitivitas Pembekuan Biaya Tetap yang menunjukkan '
            'bagaimana menahan OpEx tetap di Rp10.954 miliar menghasilkan titik impas di Rp18.604 miliar."'
        ),
        "bullets": [
            "Tabel 1 — Proyeksi Laba Rugi Base (9 baris, 2026F–2028F): Pendapatan, COGS, Laba Kotor, Beban Operasi, EBIT, Beban Bunga, EBT, Pajak (22%), Laba Bersih",
            "Jadwal 2 — Proyeksi Neraca Base (16 baris): Kas (plug), Piutang Usaha, Persediaan, Total Aset Lancar, Aset Tetap, Total Aset, Utang, Ekuitas",
            "Jadwal 3 — Proyeksi Arus Kas Base (13 baris): Laba Bersih, D&A, Perubahan Modal Kerja, CFO, CapEx, CFI, CFF, Kas Akhir",
            "Jadwal 4 & 5 — Titik Impas & Leverage Operasi (10 baris) + Uji Sensitivitas Pembekuan Biaya Tetap (6 baris: impas Rp18.604M, DOL 11,31x → 3,77x)",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik baris Laporan Laba Rugi mana saja atau baris pada 4 jadwal pendukung di bawah (Neraca, Arus Kas, Titik Impas/DOL, Sensitivitas).",
            ],
            [
                "Tab 1: Grafik Angka Lampiran",
                "Menampilkan \"Visualisasi Angka Pendukung Lampiran\" dari catatan A5: Pendapatan 2026F (Rp20.408M), Margin Operasi Base (−19,6%), Titik Impas Biaya Tetap (Rp18.604M), Kas Akhir (Rp968M).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan rumus pos yang diklik + 4 baris Tabel Perhitungan Slide (\"Lihat semua baris (+1 lagi)\").",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Menyediakan keempat jadwal pendukung penuh di dalam blok akordeon lipat (Proyeksi Neraca, Proyeksi Arus Kas, Titik Impas & DOL, Sensitivitas Beta/WACC/g).",
            ],
            [
                "Tab 5, Analisis & Navigasi",
                "Tab 5 berisi 10 jejak (8 kuliah + 2 tugas). \"Tampilkan Analisis\" membandingkan skenario OpEx terskala vs. uji pembekuan biaya tetap. "
                "Footer menyediakan \"← Kembali ke Slide 8\" dan pil lompat cepat A1–A6.",
            ],
        ],
    },
    {
        "header": "SLIDE 20 (APPENDIX A6): Lampiran A6 — Jadwal WACC Tertanggal, DCF, Residual Income & P/B Grab FY2025  [Cadangan Q&A | Tautan dari Slide 9–14]",
        "goal": "Menjadi lampiran induk valuasi untuk Q&A yang memuat seluruh input WACC bertanggal, jadwal DCF & RI, uji sensitivitas, perhitungan P/B Grab, dan pengecualian pembanding.",
        "script": (
            '"Lampiran A6 adalah cadangan valuasi lengkap kami untuk Slide 9 sampai 14. Tabel utama mendokumentasikan setiap input Biaya Modal bertanggal—SUN RI 10T '
            'per 30 Desember 2025 (6,120%), spread Damodaran (1,618%), Mature ERP (4,23%), CRP Indonesia (2,465%), Beta Investing.com (0,59), serta biaya utang '
            'efektif FY2025 (6,91% pra-pajak / 5,39% setelah pajak)—menghasilkan WACC 7,76% dan Ke 8,45%. Di bawahnya terdapat tujuh jadwal lengkap: jembatan valuasi '
            'DCF vs. Residual Income berdampingan, uji sensitivitas Beta/WACC/g, alasan pertumbuhan terminal 3,0% berada di bawah Rf dan WACC, penurunan FCFF dan RI '
            'tahun demi tahun, perhitungan P/B Grab 3,0391x (US$4,99 / US$1,6419), serta alasan Sea, Bukalapak, dan Blibli dikeluarkan."'
        ),
        "bullets": [
            "Tabel 1 — Penyusunan CAPM & WACC Bertanggal (7 baris): Rf 4,502%, Beta 0,59, Mature ERP 4,23%, CRP 2,465%, Ke 8,45%, Kd Setelah Pajak 5,39%, Bobot 77,4%/22,6% → WACC 7,76%",
            "Jadwal 1 & 2 — Jembatan Valuasi DCF vs. RI Berdampingan (5 baris) + Uji Sensitivitas Beta / WACC / g & Titik Impas (6 baris)",
            "Jadwal 3, 4 & 5 — Alasan Pertumbuhan Terminal 3,0% (4 baris: 3,0% < 4,502% Rf < 7,76% WACC < 8,45% Ke) + Penurunan FCFF (7 baris) + Penurunan Residual Income (6 baris)",
            "Jadwal 6 & 7 — Perhitungan Tolok Ukur Grab (6 baris: US$4,99 / US$1,6419 = 3,0391x × Rp29,9479 BVPS GoTo = Rp91,02/sh) + Alasan Sea, BUKA & BELI Dikeluarkan (3 baris)",
        ],
        "popup_rows": [
            [
                "Bagian yang Bisa Diklik",
                "Klik salah satu dari 7 baris WACC bertanggal di tabel atas atau baris mana saja pada ke-7 jadwal pendukung di bawah.",
            ],
            [
                "Tab 1: Grafik Angka Lampiran",
                "Menampilkan \"Visualisasi Angka Pendukung Lampiran\" dari catatan teratas A6 (Ke 8,45%, Kd Pra-Pajak 6,91%, Pajak 22,0%, Kd Setelah Pajak 5,39%, Bobot Ekuitas 77,4%, Bobot Utang 22,6%).",
            ],
            [
                "Tab 3: Perhitungan & Rumus",
                "Menampilkan SEMUA 17 baris Tabel Perhitungan Slide (\"Lihat semua baris (+14 lagi)\") yang mencakup setiap rumus WACC, DCF, Residual Income, dan P/B Grab.",
            ],
            [
                "Tab 4: Jadwal & Bukti",
                "Menampilkan gambar bukti Jadwal Utang Catatan 20 & Neraca Ekuitas + seluruh 7 jadwal lipat (Jembatan Valuasi, Sensitivitas, Cek 3%, FCFF, RI, Grab, Pembanding Dikeluarkan).",
            ],
            [
                "Tab 5, Analisis & Navigasi",
                "Tab 5 berisi 16 jejak (12 kuliah + 4 tugas). \"Tampilkan Analisis\" membahas metodologi DCF/RI dan batas nilai terminal. "
                "Footer menyediakan \"← Kembali ke Slide 9–14\" (kembali ke slide asal Anda melompat!) dan pil lompat cepat A1–A6.",
            ],
        ],
    },
]


def build_doc():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    p0 = doc.add_paragraph()
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    add_run(p0, "MMAT613 ANALISIS LAPORAN KEUANGAN  |  NASKAH PEMBICARA PRESENTASI", bold=True, size=9.5, color=EMERALD)

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(2)
    add_run(p1, "PT GoTo Gojek Tokopedia Tbk (IDX: GOTO)\n", bold=True, size=17, color=NAVY)
    add_run(p1, "Naskah Presenter Lengkap 20 Slide, Panduan Penuh Popup & Tanya-Jawab (Bahasa Indonesia)", bold=True, size=12, color=SLATE)

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(8)
    add_run(
        p2,
        "Kelompok 4: Fagly Ramschie, Anggreini Ruitan, Galatia Rompas  |  Magister Manajemen, Universitas Klabat  |  Mencakup Slide Utama 1–14 + Lampiran A1–A6 (Slide 15–20)",
        size=9.5,
        color=MUTED,
    )

    add_callout_box(
        doc,
        "CARA MENGGUNAKAN SLIDE INTERAKTIF DAN POPUP (BACA INI DULU)",
        [
            "1. Berbicaralah dengan santai seperti menjelaskan ke teman. Anda tidak perlu menghafal kata per kata — gunakan Angka Kunci dan tabel Panduan Popup sebagai penuntun di panggung.",
            "2. Bilah Pengalih Atas (Slide 4, 5, 6, 7, 8, 10, 11, 12): Slide dibuka pada \"Dek Awal (Tersubmit)\" (amber). Klik \"Laporan Akhir (Restated)\" (hijau) untuk menampilkan angka pasca-Tokopedia yang sudah dibersihkan. Pada Slide 5, 7, 8, 10, dan 13, tombol di dalam popup (\"Laporan Lama (Dengan 2023)\" vs. \"Laporan Akhir (Pasca-Exit)\") otomatis tersinkronisasi dengan bilah atas ini!",
            "3. Dropdown Langsung di Slide: Slide 8 memiliki dropdown \"Skenario:\" (Base, Optimistis, Konservatif, plus Rata-rata 2 Thn di mode Dek Awal) tepat di atas tabel. Slide 10 & 11 memiliki pemilih \"Basis Proyeksi:\" (3-Thn vs. 2-Thn) di mode Dek Awal.",
            "4. Mengklik Baris, Kartu, Grafik, atau Poin Analisis Membuka Glass Popup (Modal) — Ini Daftar Lengkap Isinya dari Atas ke Bawah:",
            "   • Header Popup: Menampilkan Pil Slide (SLIDE X · Bagian), Judul Item yang Diklik, Subjudul Singkatan Otomatis, Pil Nilai Metrik, dan Tutup (× / Esc).",
            "   • Bilah Ikon Tab Atas (Kiri): (1) Grafik & Data (ikon diagram batang) — grafik SVG, kartu tren YoY, plus widget khusus slide (2 tampilan Slide 5, Pro Forma + Tabel 11 Slide 7, 6 sub-tab Slide 9, matriks sensitivitas Slide 10, Football Field 7 batang + Matriks Slide 11); (2) Pra vs. Pasca Exit / Pra vs. Revisi (ikon panah — aktif pada Slide 2, 4, 5, 6, 7, 8, 9–13); (3) Perhitungan & Rumus (ikon kalkulator — rumus KaTeX, langkah hitung, sumber, dan Tabel Perhitungan Slide dengan \"Lihat semua baris\"); (4) Jadwal & Bukti (ikon dokumen — gambar Laporan Keuangan Auditan klik-perbesar + Jadwal Pendukung lipat); (5) Jejak Tugas & Materi (ikon tautan — kartu \"Buka →\" ke Excel & slide kuliah).",
            "   • Bilah Atas (Kanan): \"Appendix A1–A6 ↗\" melompat langsung ke slide Lampiran terkait (Slide 15–20); \"Tampilkan Analisis\" membuka panel samping kanan \"Ringkasan & Analisis\" (dengan tombol \"Lihat selengkapnya\"; disembunyikan di Slide 9 karena Tab 1 sudah berisi tata letak 6 langkah).",
            "   • Pita Bawah di Dalam Popup: \"Istilah:\" otomatis menampilkan definisi hingga 8 singkatan keuangan yang muncul pada popup yang sedang dibuka.",
            "5. Navigasi Lampiran (Slide 15–20): Setiap slide Lampiran dilengkapi tombol \"← Kembali ke Slide X\" (kembali tepat ke slide asal) serta pil lompat cepat A1–A6 di pojok kanan bawah.",
        ],
        fill_hex=HEX_GUIDE_BG,
        border_hex=HEX_GUIDE_BORDER,
        title_color=NAVY,
    )

    p_part1 = doc.add_paragraph()
    p_part1.paragraph_format.space_before = Pt(4)
    p_part1.paragraph_format.space_after = Pt(6)
    add_run(p_part1, "BAGIAN 1: SLIDE UTAMA PRESENTASI (SLIDE 1 SAMPAI 14)", bold=True, size=13, color=NAVY)

    slide_fig_meta = [
        ("slide_01.png", "Slide 1 — Analisis Ekuitas GoTo (Pembukaan)", []),
        ("slide_02.png", "Slide 2 — Model Bisnis", [("popup_02.png", "Popup Slide 2 — Jembatan EBIT Segmen Gojek (FY24 → FY25) & Kartu Tren YoY")]),
        ("slide_03.png", "Slide 3 — Industri dan Persaingan", [("popup_03.png", "Popup Slide 3 — Belanja Persaingan & Provisi Kredit")]),
        ("slide_04.png", "Slide 4 — Profitabilitas dan DuPont (Laporan Akhir Restated)", [("popup_04.png", "Popup Slide 4 — Lintasan ROE DuPont vs. Grab & Kartu YoY")]),
        ("slide_05.png", "Slide 5 — Likuiditas dan Z-Score (Laporan Akhir Restated)", [
            ("popup_05a.png", "Popup Slide 5 (Tampilan A) — Kartu Kolom Vertikal Rasio Likuiditas & Modal Kerja"),
            ("popup_05b.png", "Popup Slide 5 (Tampilan B) — Rincian Faktor Tertimbang Altman Z-Score (−4,72 / −4,80)"),
        ]),
        ("slide_06.png", "Slide 6 — Arus Kas dan Kualitas Akuntansi (Laporan Akhir Restated)", [("popup_06.png", "Popup Slide 6 — Jembatan Arus Kas Bebas FY2025 & Normalisasi CapEx")]),
        ("slide_07.png", "Slide 7 — Asumsi Proyeksi (Laporan Akhir Restated)", [("popup_07.png", "Popup Slide 7 — Asumsi Base Case, Hasil Pro Forma & Tabel 11 Interaktif")]),
        ("slide_08.png", "Slide 8 — Proyeksi Tiga Tahun (Laporan Akhir Restated)", [("popup_08.png", "Popup Slide 8 — Skenario 2026F–2028F & Kartu Lintasan Proyeksi")]),
        ("slide_09.png", "Slide 9 — Biaya Modal", [("popup_09.png", "Popup Slide 9 — Panduan Interaktif 6 Langkah Biaya Modal (WACC 7,761%)")]),
        ("slide_10.png", "Slide 10 — DCF dan Residual Income (Laporan Akhir Restated)", [("popup_10.png", "Popup Slide 10 — DCF (+Rp10,38) & RI (−Rp12,23) Restated + Tabel Sensitivitas")]),
        ("slide_11.png", "Slide 11 — Perbandingan Grab dan Valuasi (Laporan Akhir Restated)", [("popup_11.png", "Popup Slide 11 — Peta Valuasi Football Field vs. Pasar Rp25,00 & Kartu Penjelasan")]),
        ("slide_12.png", "Slide 12 — Rekomendasi (Laporan Akhir Restated)", [("popup_12.png", "Popup Slide 12 — Spread Ekonomi (ROIC vs. WACC) & Gap Harga Pasar")]),
        ("slide_13.png", "Slide 13 — Restatement Forensik: 5 Kesalahan yang Diperbaiki", [("popup_13.png", "Popup Slide 13 — Angka Auditan Laporan Akhir Setelah 5 Koreksi")]),
        ("slide_14.png", "Slide 14 — Dek Awal vs. Laporan Akhir: Mengapa SELL Tetap Kuat", [("popup_14.png", "Popup Slide 14 — Spread Ekonomi (ROIC 2,70% vs. WACC 7,76%)")]),
    ]
    apx_fig_meta = [
        ("slide_15.png", "Slide 15 (Lampiran A1) — Jembatan Pendapatan & Jadwal Risiko Persaingan", [("popup_15.png", "Popup Lampiran A1 — Visualisasi Angka Jembatan Pendapatan")]),
        ("slide_16.png", "Slide 16 (Lampiran A2) — Ringkasan Historis & Pro Forma (FY2023–2028F) & DuPont", [("popup_16.png", "Popup Lampiran A2 — Visualisasi Angka Profitabilitas & DuPont")]),
        ("slide_17.png", "Slide 17 (Lampiran A3) — Likuiditas, Modal Kerja, Z-Score Minggu 6 & Catatan Kaki", [("popup_17.png", "Popup Lampiran A3 — Visualisasi Angka Likuiditas & Z-Score")]),
        ("slide_18.png", "Slide 18 (Lampiran A4) — Pendorong Skenario, Alasan Proyeksi & Perilaku Biaya", [("popup_18.png", "Popup Lampiran A4 — Visualisasi Angka Pendorong Proyeksi")]),
        ("slide_19.png", "Slide 19 (Lampiran A5) — Laporan Pro Forma Tiga Tahun & Leverage Operasi", [("popup_19.png", "Popup Lampiran A5 — Visualisasi Angka Pro Forma & Titik Impas")]),
        ("slide_20.png", "Slide 20 (Lampiran A6) — Jadwal WACC Tertanggal, DCF, Residual Income & P/B Grab FY2025", [("popup_20.png", "Popup Lampiran A6 — Visualisasi Angka Valuasi & Biaya Modal")]),
    ]

    fig_counter = [1]
    for s, (sf, sc, pfs) in zip(MAIN_SLIDES, slide_fig_meta):
        s_with_figs = {**s, "slide_fig": (sf, sc), "popup_figs": pfs}
        add_slide_block(doc, s_with_figs, fig_counter, is_appendix=False)

    p_part2 = doc.add_paragraph()
    p_part2.paragraph_format.space_before = Pt(8)
    p_part2.paragraph_format.space_after = Pt(6)
    add_run(p_part2, "BAGIAN 2: SLIDE LAMPIRAN / APPENDIX (SLIDE 15 SAMPAI 20 — LAMPIRAN A1–A6)", bold=True, size=13, color=EMERALD)

    p_part2_note = doc.add_paragraph()
    p_part2_note.paragraph_format.space_before = Pt(0)
    p_part2_note.paragraph_format.space_after = Pt(6)
    add_run(
        p_part2_note,
        "Catatan: Lampiran A1–A6 tidak perlu dibacakan berurutan selama presentasi utama kecuali ditanya, atau Anda dapat melompat langsung saat sesi tanya-jawab "
        "dengan mengklik tombol \"Appendix A1–A6 ↗\" di slide maupun di dalam popup, lalu klik \"← Kembali ke Slide X\" untuk kembali ke slide sebelumnya.",
        italic=True,
        size=9.5,
        color=SLATE,
    )

    for s, (sf, sc, pfs) in zip(APPENDIX_SLIDES, apx_fig_meta):
        s_with_figs = {**s, "slide_fig": (sf, sc), "popup_figs": pfs}
        add_slide_block(doc, s_with_figs, fig_counter, is_appendix=True)

    add_section_banner(doc, "BAGIAN 3: CONTEKAN CEPAT TANYA-JAWAB (7 PERTANYAAN UTAMA & JAWABAN MUDAH)", bg_hex=HEX_NAVY)
    p_qa_sp = doc.add_paragraph()
    p_qa_sp.paragraph_format.space_before = Pt(2)
    p_qa_sp.paragraph_format.space_after = Pt(2)

    qa_rows = [
        [
            "1. Mengapa DCF melonjak dari −Rp121 menjadi +Rp10,38?",
            "Draf awal kami tidak sengaja merata-ratakan biaya 2023 pra-Tokopedia (OpEx 117%) dan Rp5,46T transfer takberwujud Tokopedia di CapEx 2024. "
            "Setelah data 2023 dibuang dan model berfokus pada bisnis Gojek + GoPay 2024–2025, DCF berbalik positif menjadi +Rp10,38 per saham.",
            "Slide 13–14 / Appendix A6",
        ],
        [
            "2. Jika GoTo mencetak laba bersih positif pada 2028F (+Rp25M), mengapa tetap SELL?",
            "Laba akuntansi tidak sama dengan laba ekonomi. Bahkan pada 2028F, ROIC GoTo (+2,70%) masih tertinggal 506 bps di bawah WACC 7,76%, "
            "dan ROE (+0,09%) jauh di bawah Biaya Ekuitas 8,45%.",
            "Slide 8, 12 & 14 / Appendix A5",
        ],
        [
            "3. Mengapa menolak kelipatan P/B Grab (Rp91,02)?",
            "Grab sudah membukukan ROE positif (+2,96%) dan EBIT positif, sedangkan ROE GoTo masih negatif (−5,23%) dan EBIT masih rugi. "
            "Memberi perusahaan yang masih merugi kelipatan 3,04x P/B milik pembanding yang sudah untung tidak valid secara ekonomi.",
            "Slide 11 / Appendix A6",
        ],
        [
            "4. Mengapa tidak merata-ratakan OpEx 2024 (62,8%) dengan 2025 (55,7%)?",
            "Tahun 2024 adalah masa transisi: GoTo menjual logistik PAB pada Mei 2024, keluar dari Vietnam pada September 2024, dan menuntaskan penghematan "
            "cloud >50% pada 2025. Jadi 2025 (55,7%) adalah laju operasional terkini, sedangkan 2024 (62,8%) menjadi lantai Skenario Konservatif.",
            "Slide 7 / Appendix A4",
        ],
        [
            "5. Mengapa Altman Z-Score −4,72 jika GoTo punya kas Rp21,76T?",
            "Skor Z ditarik turun hampir seluruhnya oleh X2 (Defisit Akumulasi = −Rp215,3T) akibat penghapusan goodwill historis tahun 2023 "
            "(Rp73,2T Tokopedia + Rp5,5T delivery). Likuiditas (X1 = +0,48 tertimbang) dan solvabilitas (X4 = +1,01 tertimbang) keduanya tetap sehat.",
            "Slide 5 / Appendix A3",
        ],
        [
            "6. Mengapa menambahkan kembali impairment goodwill & JV di Kualitas Akuntansi?",
            "Untuk memisahkan penghapusan non-kas satu kali dari kinerja operasional harian GoTo dan menghitung rasio akrual sebelum/sesudah penyesuaian. "
            "Bahkan setelah semua write-down dikeluarkan, laba bersih berulang inti tetap minus −Rp580M pada 2025.",
            "Slide 6 / Appendix A3",
        ],
        [
            "7. Kapan rekomendasi GOTO berubah dari SELL ke HOLD atau BUY?",
            "Naik ke HOLD jika harga turun ke ≤ Rp13,20 (1,0x Kas Bersih) dengan FCF > 0. Naik ke BUY jika efisiensi 1H 2026 "
            "(Cash OpEx ≤ 51,2% dan Margin Kotor ≥ 61,9%) bertahan selama dua kuartal berturut-turut.",
            "Slide 12 / Appendix A6",
        ],
    ]
    add_styled_table(doc, ["Pertanyaan yang Sering Muncul", "Jawaban Singkat 1–2 Kalimat", "Lompat Ke"], qa_rows, [2.0, 3.85, 1.15])

    add_section_banner(doc, "BAGIAN 4: CONTEKAN SINGKATAN (JIKA LUPA DI PANGGUNG)", bg_hex=HEX_NAVY)
    p_ab_sp = doc.add_paragraph()
    p_ab_sp.paragraph_format.space_before = Pt(2)
    p_ab_sp.paragraph_format.space_after = Pt(2)

    abbr_rows = [
        ["BVPS", "Book Value Per Share — Nilai Buku per Saham (Ekuitas Induk / Saham = Rp29,95)"],
        ["P/B", "Price-to-Book Ratio — Rasio Harga terhadap Nilai Buku (Grab = 3,04x)"],
        ["DCF", "Discounted Cash Flow — Nilai kini Arus Kas Bebas masa depan (= +Rp10,38/saham)"],
        ["RI", "Residual Income — Laba Ekonomi di atas/bawah Biaya Ekuitas (= −Rp12,23/saham)"],
        ["WACC", "Weighted Average Cost of Capital — Biaya modal rata-rata tertimbang (= 7,76%)"],
        ["Ke / Kd / Rf", "Biaya Ekuitas (8,45%) / Biaya Utang setelah pajak (5,39%) / Risk-Free Rate IDR (4,502%)"],
        ["ERP / CRP", "Equity Risk Premium pasar maju (4,23%) / Country Risk Premium Indonesia (2,465%)"],
        ["NOPAT", "Net Operating Profit After Tax — Laba Operasi setelah pajak (EBIT × (1 − 22%) = +Rp442,4M di 2028F)"],
        ["FCFF", "Free Cash Flow to Firm — Arus kas bebas bagi perusahaan setelah pajak, modal kerja & CapEx"],
        ["CFO / FCF", "Arus Kas Operasi (+Rp307M) / Arus Kas Bebas (CFO − CapEx = −Rp875M)"],
        ["ROIC / ROE", "Return on Invested Capital (2,70% di 2028F) / Return on Equity (−5,23% di 2025)"],
        ["EBIT", "Earnings Before Interest & Taxes — Laba Operasi (−Rp378M di 2025; +Rp567M di 2028F)"],
        ["COGS / OpEx / CapEx", "Beban Pokok Pendapatan / Beban Operasi / Belanja Modal"],
        ["DSO / DPO / CCC", "Hari Penagihan Piutang (10,9h) / Hari Pembayaran Pemasok (59,1h) / Siklus Kas (−47,5h)"],
        ["TIE / DOL", "Times Interest Earned (−0,71x) / Degree of Operating Leverage (28,56x di 2026F)"],
        ["PSAK / IFRS", "Standar Akuntansi Keuangan Indonesia (selaras IFRS; dasar laporan auditan GoTo)"],
    ]
    add_styled_table(doc, ["Singkatan", "Kepanjangan & Arti Sederhana"], abbr_rows, [1.6, 5.4])

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_doc()
