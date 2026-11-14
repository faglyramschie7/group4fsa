<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import fullModulesData from './data/full_slides_knowledgebase.json'
import assignmentsData from './data/all_assignments_bundle.json'
import assignmentsIdData from './data/all_assignments_bundle_id.json'
import presentationDeckData from './data/presentation_deck.json'
import presentationDeckIdData from './data/presentation_deck_id.json'
import supportingTablesIdData from './data/supporting_tables_id.json'

const lang = ref('en') // 'en' | 'id'
const modules = ref(fullModulesData)
const assignments = computed(() => lang.value === 'id' ? assignmentsIdData : assignmentsData)
const presentationSlides = computed(() => lang.value === 'id' ? presentationDeckIdData : presentationDeckData)

const uiText = computed(() => lang.value === 'id' ? {
  brandSub: 'Studi & Riset FSA GoTo',
  searchDeckPlaceholder: 'Cari slide dek presentasi...',
  searchSlidesPlaceholder: 'Cari slide kuliah, topik...',
  searchTasksPlaceholder: 'Cari tugas, dokumen...',
  switchDeck: 'Dek',
  switchSlides: 'Kuliah',
  switchTasks: 'Tugas',
  deckSectionLabel: 'DEK WEB TUGAS 16',
  slidesSuffix: 'SLIDE',
  lectureSectionLabel: 'SLIDE KULIAH (12 MINGGU)',
  tasksSectionLabel: 'BERKAS TUGAS SELESAI (7)',
  slideWord: 'Slide',
  slidesWord: 'slide',
  apxWord: 'LAMP',
  mainDeckWord: 'DEK UTAMA',
  appendixWord: 'LAMPIRAN',
  visualSlides: 'Slide Visual',
  financials: 'Keuangan',
  takeaways: 'Intisari',
  roadmap: 'Peta Kurikulum',
  presContextPill: 'Dek Web Tugas 16 • Ketertelusuran Sumber Asli Aktif',
  asgContextPill: 'Tugas & Buku Kerja Kelompok 4',
  prevBtn: 'Sebelumnya',
  nextBtn: 'Lanjut',
  ofWord: 'dari',
  presentBtn: 'Presentasi',
  presentTitle: 'Fokus pada Presentasi di dalam Jendela Browser (Gunakan Panah Kiri/Kanan)',
  sourceLabel: 'Sumber:',
  showSpeaker: 'Tampilkan Naskah Pembicara',
  hideSpeaker: 'Sembunyikan Naskah Pembicara',
  showAudit: 'Tampilkan Referensi & Info Audit Pendukung',
  hideAudit: 'Sembunyikan Referensi & Info Audit Pendukung',
  speakerTag: 'NASKAH PEMBICARA',
  auditScopeTag: 'PANEL VERIFIKASI EKSTERNAL • BUKAN BAGIAN DARI SLIDE',
  auditTitlePrefix: 'Asal Angka pada Slide',
  auditDescPrefix: 'Periksa silang setiap angka pada Slide',
  auditDescMid: 'terhadap Slide Kuliah asli (Kiri) dan Buku Kerja Tugas / Laporan Auditan (Kanan).',
  lectureColTitle: 'LETAKNYA DI SLIDE KULIAH',
  lectureColSub: 'Slide Kuliah Terkait Terverifikasi',
  asgColTitle: 'LETAKNYA DI TUGAS & LAPORAN AUDITAN',
  asgColSub: 'Bukti Tugas & Laporan Auditan Terkait',
  openWord: 'Buka',
  liveExtract: 'Kutipan Basis Pengetahuan Kuliah Langsung:',
  presentFocusBadge: 'FOKUS PRESENTASI',
  exitEsc: 'Keluar (Esc)',
  clickHintDbl: 'Klik ganda untuk membuka laci asal sumber →',
  closeWord: 'Tutup',
  drawerSubtitlePrefix: 'INSPEKTOR SUMBER SLIDE',
  drawerWhatMeans: 'Arti & Penjelasan Lengkap:',
  drawerHowCalculated: 'Bagaimana Angka Ini Dihitung? (Rumus & Langkah)',
  drawerFormulaLabel: 'Rumus:',
  drawerOriginLabel: 'Asal Data:',
  drawerLkProofTitle: 'Bukti Halaman Laporan Keuangan Auditan (Di-Highlight)',
  drawerClickZoomHint: 'Klik gambar untuk memperbesar angka & kotak kalkulasi',
  drawerSupportBadge: 'DATA PENDUKUNG',
  drawerSupportTableLabel: 'Baris Kertas Kerja Excel (Data Pendukung Di-Highlight):',
  drawerLectureTableLabel: 'Tabel Slide Kuliah (Baris Pendukung Di-Highlight):',
  drawerLectureTitle: 'Sumber Slide Kuliah',
  drawerAsgTitle: 'Sumber Tugas & Laporan Auditan',
  locationLabel: 'Lokasi:',
  liveExcelPreview: 'Pratinjau Sheet Excel Langsung:',
  auditedProofLabel: 'BUKTI LK GOTO 2025 AUDITAN:',
  drawerEmptyTitle: 'Tautan Sumber Tingkat Slide Umum',
  drawerEmptyDesc: 'Semua sumber slide kuliah dan tugas untuk slide ini tersedia di panel Referensi & Info Audit Pendukung di bawah kanvas.',
  asgSectionsBadge: 'Bagian Analisis',
  asgTablesBadge: 'Tabel Keuangan',
  asgSheetsBadge: 'Sheet Excel',
  asgQuickJumpLabel: 'Lompat ke Bagian:',
  asgWorkbookBtn: 'Buku Kerja Excel',
  asgWorkbookTitle: 'Buku Kerja Keuangan Interaktif:',
  asgWorkbookSub: 'Model Excel Terhubung • Seluruh Rumus & Tabel Telah Dievaluasi',
  asgSourceRefLabel: 'Referensi Sumber:',
  asgSecTableBadge: 'TABEL DATA & ANALISIS TERSTRUKTUR',
  asgProofBadge: 'BUKTI LAPORAN KEUANGAN AUDITAN (LK GOTO 2025)',
  asgZoomHint: 'Klik gambar untuk memperbesar dokumen asli →'
} : {
  brandSub: 'GoTo Study & Research Suite',
  searchDeckPlaceholder: 'Search deck slides...',
  searchSlidesPlaceholder: 'Search slides, topics...',
  searchTasksPlaceholder: 'Search assignments, dossiers...',
  switchDeck: 'Deck',
  switchSlides: 'Slides',
  switchTasks: 'Tasks',
  deckSectionLabel: 'ASSIGNMENT 16 WEB DECK',
  slidesSuffix: 'SLIDES',
  lectureSectionLabel: 'LECTURE SLIDES (12 WEEKS)',
  tasksSectionLabel: 'COMPLETED ASSIGNMENTS DOSSIER (7)',
  slideWord: 'Slide',
  slidesWord: 'slides',
  apxWord: 'APX',
  mainDeckWord: 'MAIN DECK',
  appendixWord: 'APPENDIX',
  visualSlides: 'Visual Slides',
  financials: 'Financials',
  takeaways: 'Takeaways',
  roadmap: 'Roadmap',
  presContextPill: 'Assignment 16 Web Deck • Source-of-Truth Traceability Active',
  asgContextPill: 'Group 4 Assignments & Workbooks',
  prevBtn: 'Prev',
  nextBtn: 'Next',
  ofWord: 'of',
  presentBtn: 'Present',
  presentTitle: 'Focus on Presentation inside Browser Window (Use Left/Right Arrows)',
  sourceLabel: 'Source:',
  showSpeaker: 'Show Speaker Script',
  hideSpeaker: 'Hide Speaker Script',
  showAudit: 'Show Supporting Reference & Audit Info',
  hideAudit: 'Hide Supporting Reference & Audit Info',
  speakerTag: 'SPEAKER SCRIPT',
  auditScopeTag: 'EXTERNAL VERIFICATION PANEL • NOT PART OF SLIDE',
  auditTitlePrefix: 'Where Slide',
  auditDescPrefix: 'Cross-check every figure on Slide',
  auditDescMid: 'against the original Lecture Slides (Left) and Assignment Workbooks / Audited Filings (Right).',
  lectureColTitle: 'WHERE THIS BELONGS ON LECTURE SLIDES',
  lectureColSub: 'Linked Lecture Slide(s) Verified',
  asgColTitle: 'WHERE THIS BELONGS ON ASSIGNMENTS & FILINGS',
  asgColSub: 'Linked Assignment & Audited Proof(s)',
  openWord: 'Open',
  liveExtract: 'Live Lecture Knowledge Base Extract:',
  presentFocusBadge: 'PRESENTATION FOCUS',
  exitEsc: 'Exit (Esc)',
  clickHintDbl: 'Double-click to open source origin drawer →',
  closeWord: 'Close',
  drawerSubtitlePrefix: 'SLIDE',
  drawerWhatMeans: 'Detailed Meaning & Explanation:',
  drawerHowCalculated: 'How Was This Calculated? (Formula & Steps)',
  drawerFormulaLabel: 'Formula:',
  drawerOriginLabel: 'Data Origin:',
  drawerLkProofTitle: 'Highlighted Audited Financial Statement Page (LK GOTO 2025)',
  drawerClickZoomHint: 'Click image to zoom highlighted rows & calculation callouts',
  drawerSupportBadge: 'SUPPORTING DATA',
  drawerSupportTableLabel: 'Excel Workbook Rows (Matching Data Highlighted):',
  drawerLectureTableLabel: 'Lecture Knowledge Base Table (Matching Rows Highlighted):',
  drawerLectureTitle: 'Lecture Slide Sources',
  drawerAsgTitle: 'Assignment & Audited Filing Sources',
  locationLabel: 'Location:',
  liveExcelPreview: 'Live Excel Sheet Preview:',
  auditedProofLabel: 'AUDITED LK GOTO 2025 PROOF:',
  drawerEmptyTitle: 'General Slide-Level Source Link',
  drawerEmptyDesc: 'All lecture and assignment sources for this slide are available in the Supporting Reference & Audit Info drawer below the canvas.',
  asgSectionsBadge: 'Analytical Sections',
  asgTablesBadge: 'Financial Tables',
  asgSheetsBadge: 'Excel Sheets',
  asgQuickJumpLabel: 'Jump to Section:',
  asgWorkbookBtn: 'Excel Workbook',
  asgWorkbookTitle: 'Interactive Financial Workbook:',
  asgWorkbookSub: 'Linked Excel Model • All Formula Cells & Schedules Evaluated',
  asgSourceRefLabel: 'Source Reference:',
  asgSecTableBadge: 'STRUCTURED FINANCIAL & ANALYTICAL SCHEDULE',
  asgProofBadge: 'AUDITED FINANCIAL STATEMENT PROOF (LK GOTO 2025)',
  asgZoomHint: 'Click image to zoom full-resolution filing proof →'
})

watch(lang, () => {
  clickPopup.value = null
  detailDrawerItem.value = null
})

const selectedWeekId = ref('week14')
const selectedPresSlideNum = ref(1)
const showSpeakerNotes = ref(false)
const showAuditDrawer = ref(false)
const isPresentMode = ref(false)
const clickPopup = ref(null)
const detailDrawerItem = ref(null)
const activeTab = ref('presentation') // 'presentation', 'slides', 'assignments', 'goto', 'flashcards', 'roadmap'
const searchQuery = ref('')
const sidebarMode = ref('presentation') // 'presentation', 'slides', 'assignments'

// For assignments tab
const selectedAssignmentId = ref('m1')
const selectedWorkbookSheet = ref('')

// Image zoom & lightbox modal states
const isActualSize = ref(false)
const lightboxImage = ref(null)
const lightboxZoom = ref(1)

const openLightbox = (src, title, caption) => {
  lightboxImage.value = { src, title, caption }
  lightboxZoom.value = 1
}

const closeLightbox = () => {
  lightboxImage.value = null
  lightboxZoom.value = 1
}

const zoomInLightbox = () => {
  if (lightboxZoom.value < 2.5) lightboxZoom.value += 0.25
}

const zoomOutLightbox = () => {
  if (lightboxZoom.value > 0.75) lightboxZoom.value -= 0.25
}

const resetLightboxZoom = () => {
  lightboxZoom.value = 1
}

// Financial Highlight Detectors (for friends/group defense)
const isDeficitRow = (rVals) => {
  if (!rVals || !rVals[0]) return false
  const title = String(rVals[0]).toLowerCase()
  return title.includes('accumulated loss') || title.includes('retained deficit') || title.includes('defisit') || title.includes('akumulasi rugi')
}


// Interactive Table-to-Text Hover Cross-Linking & Formula Bar (Inspired by efficient-diversification-react)
const hoveredCellRef = ref(null)
const hoveredRowIdx = ref(null)

// Week 4 Slide 4 Interactive GoTo Cash Flow Chart
const gotoChartScale = ref('operating') // 'operating' (-6T to +2T) or 'macro' (-100T to +10T)
const hoveredChartPoint = ref(null)

const onHoverChartPoint = (point) => {
  hoveredChartPoint.value = point
  if (point) {
    activeFormulaCell.value = {
      ref: point.ref || 'FX',
      formula: point.formula || `= ${point.series} (${point.year}): ${point.val}`,
      val: point.val,
      sources: point.sources || []
    }
    if (point.rowIdx !== undefined) {
      hoveredRowIdx.value = point.rowIdx
    }
  } else {
    hoveredRowIdx.value = null
  }
}

const activeFormulaCell = ref({
  ref: 'D7',
  formula: '= D5 - D6  (Operating Cash Flow Rp 307.0 bn - Capex Rp 1,182.4 bn = -(Rp 875.3 bn))',
  val: '(875.3)',
  sources: ['D5', 'D6']
})

const getColLetter = (index) => {
  const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
  return letters[index] || 'A'
}

const getColLetters = (count) => {
  const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
  return letters.slice(0, count)
}

const getCellFormulaInfo = (slideNum, rIdx, cIdx, rVals) => {
  const rowNum = rIdx + 2
  const colChar = getColLetter(cIdx)
  const cellRef = `${colChar}${rowNum}`
  const val = cIdx === 0 ? rVals[0] : rVals[cIdx]
  const rowTitle = String(rVals[0] || '').toLowerCase()

  let formula = `= Audited Filing LK GOTO 31 Dec 2025`
  let sources = []

  // YoY column or % change column
  if (colChar === 'E' || (cIdx > 1 && String(val).includes('%') && !rowTitle.includes('revenue') && !rowTitle.includes('margin'))) {
    const dCell = `D${rowNum}`
    const cCell = `C${rowNum}`
    formula = `= (${dCell} - ${cCell}) / |${cCell}|  [Percentage YoY Change]`
    sources = [dCell, cCell]
    return { ref: cellRef, formula, val: String(val), sources }
  }

  // Week 14 Formulas (Cost of Capital & Valuation Applications)
  if (selectedWeekId.value === 'week14') {
    if (slideNum === 1) {
      if (rowTitle.includes('discounted cash flow')) {
        formula = `= PV(FCFF) + PV(Terminal Value) + Net Cash (+14,012.5 bn) / 1,062,012.1M shares = ${val}`
        sources = []
      } else if (rowTitle.includes('residual income')) {
        formula = `= Beginning Book Equity (28,711.7 bn) + PV(Future Residual Income) / 1,062,012.1M shares = ${val}`
        sources = []
      } else if (rowTitle.includes('market multiples')) {
        formula = `= AVERAGE(P/B Valuation Rp 62.17, Net-Cash-Adj. EV/EBITDA Valuation Rp 17.43) = ${val}`
        sources = []
      } else if (rowTitle.includes('net cash liquidation floor')) {
        formula = `= (Cash 21,755.1 bn - Total Debt 7,742.6 bn) / 1,062,012.1M shares = ${val}`
        sources = []
      }
    } else if (slideNum === 7) {
      if (rowTitle.includes('observed beta')) {
        formula = `= Rf (4.502%) + Beta (0.59) * Mature ERP (4.23%) + Indonesia CRP (2.465%) = 9.46% (or CAPM 8.45% w/ 4.502% Rf & 6.695% Total ERP)`
        sources = []
      }
    } else if (slideNum === 9) {
      if (rowTitle.includes('total enterprise capital')) {
        formula = `= Market Equity (${colChar}1) + Total Debt (${colChar}2) = ${val}`
        sources = [`${colChar}1`, `${colChar}2`]
      }
    } else if (slideNum === 11) {
      if (rowTitle.includes('less: tax on ebit')) {
        formula = `= IF(EBIT > 0, -EBIT * 22%, 0) -> Zero cash tax refund on negative EBIT = ${val}`
        sources = [`${colChar}1`]
      } else if (rowTitle.includes('ebiat')) {
        formula = `= EBIT (${colChar}1) + Tax (${colChar}2) = ${val}`
        sources = [`${colChar}1`, `${colChar}2`]
      } else if (rowTitle.includes('free cash flow to firm')) {
        formula = `= EBIAT (${colChar}3) + D&A (${colChar}4) - Capex (${colChar}5) - Increase in NWC (${colChar}6) = ${val}`
        sources = [`${colChar}3`, `${colChar}4`, `${colChar}5`, `${colChar}6`]
      }
    } else if (slideNum === 15) {
      if (rowTitle.includes('equity charge')) {
        formula = `= Beginning BVE (${colChar}1) * Cost of Equity (8.45%) = ${val}`
        sources = [`${colChar}1`]
      } else if (rowTitle.includes('residual income (economic profit)')) {
        formula = `= Forecast Net Income (${colChar}2) - Equity Charge (${colChar}3) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`]
      }
    } else if (slideNum === 18) {
      if (rowTitle.includes('eps')) {
        formula = `= IF(EPS <= 0, "n.m.", EPS * Peer Median P/E) -> FY2025 EPS = -(1,501.7 bn) / 1,062.0B sh = -(Rp 1.41)`
        sources = []
      } else if (rowTitle.includes('bvps')) {
        formula = `= BVPS (Rp 27.03) * Peer Median P/B (2.30x) = Rp 62.17/share`
        sources = []
      } else if (rowTitle.includes('ebitda per share')) {
        formula = `= (EBITDA/sh Rp 0.32 * Peer EV/EBITDA 13.25x) + Net Cash/sh (+Rp 13.20) = Rp 17.43/share`
        sources = []
      } else if (rowTitle.includes('market multiples summary')) {
        formula = `= AVERAGE(P/B Rp 62.17, EV/EBITDA Rp 17.43) = Rp 39.80/share`
        sources = [`${colChar}2`, `${colChar}3`]
      }
    }
  }

  // Week 13 Formulas (Forecasting Financial Statements & Three-Statement Modeling)
  else if (selectedWeekId.value === 'week13') {
    if (slideNum === 1) {
      if (rowTitle.includes('gross profit')) {
        formula = `= Net Revenue (${colChar}1) - Cost of Revenue (${colChar}2) = ${val}`
        sources = [`${colChar}1`, `${colChar}2`]
      } else if (rowTitle.includes('operating income')) {
        formula = `= Gross Profit (${colChar}3) - Operating Expenses (${colChar}4) = ${val}`
        sources = [`${colChar}3`, `${colChar}4`]
      }
    } else if (slideNum === 8) {
      if (rowTitle.includes('2026f projected revenue')) {
        formula = `= FY2025A Revenue (18,322.2) * (1 + Revenue Growth Rate ${colChar}1) = ${val}`
        sources = [`${colChar}1`]
      } else if (rowTitle.includes('2026f net income')) {
        formula = `= 2026F Operating EBIT (${colChar}5) + Interest & Non-Op (${colChar}6) - Tax = ${val}`
        sources = [`${colChar}5`, `${colChar}6`]
      }
    } else if (slideNum === 11) {
      if (rowTitle.includes('net change in cash')) {
        formula = `= CFO (${colChar}2) + CFI (${colChar}3) + CFF (${colChar}4) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`]
      } else if (rowTitle.includes('ending cash balance')) {
        formula = `= Beginning Cash (${colChar}1) + Net Change in Cash (${colChar}5) = ${val}`
        sources = [`${colChar}1`, `${colChar}5`]
      }
    } else if (slideNum === 13) {
      if (rowTitle.includes('cash flow from operations')) {
        formula = `= Net Income (${colChar}1) + D&A (${colChar}2) + NWC Cash Flow (${colChar}3) = ${val}`
        sources = [`${colChar}1`, `${colChar}2`, `${colChar}3`]
      } else if (rowTitle.includes('net change in cash')) {
        formula = `= CFO (${colChar}4) + CFI (${colChar}5) + CFF (${colChar}6) = ${val}`
        sources = [`${colChar}4`, `${colChar}5`, `${colChar}6`]
      }
    }
  }

  // Week 12 Formulas (Analyzing Operating Activities: Revenue, Operating Leverage & Segments)
  else if (selectedWeekId.value === 'week12') {
    if (slideNum === 1) {
      if (rowTitle.includes('consolidated net revenue')) {
        formula = `= Gross Platform Fees (${colChar}2) - User Promos & Subsidies (${colChar}3) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`]
      } else if (rowTitle.includes('gross profit margin')) {
        formula = `= Gross Profit (${colChar}5) / Consolidated Net Revenue (${colChar}4) = ${val}`
        sources = [`${colChar}5`, `${colChar}4`]
      } else if (rowTitle.includes('operating loss')) {
        formula = `= Gross Profit (${colChar}5) - Total Operating Expenses = ${val}`
        sources = [`${colChar}5`]
      }
    } else if (slideNum === 3) {
      if (rowTitle.includes('incremental flow-through')) {
        formula = `= Absolute Operating Improvement (1,862.6) / Incremental Gross Profit (2,095.0) = 88.9%`
        sources = []
      }
    } else if (slideNum === 7) {
      if (rowTitle.includes('total consolidated net revenue')) {
        formula = `= ODS (${colChar}2) + Fintech (${colChar}3) + E-Commerce (${colChar}4) + Eliminations (${colChar}6) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`, `${colChar}6`]
      }
    } else if (slideNum === 10) {
      if (rowTitle.includes('fy2025')) {
        formula = `= Gross Profit (12,465.6) / Net Revenue (18,322.2) = 68.04% (+279 bps expansion)`
        sources = []
      }
    } else if (slideNum === 12) {
      if (rowTitle.includes('implied empirical dol')) {
        formula = `= % Change in Operating Loss (83.12%) / % Change in Net Revenue (15.27%) = 5.44x`
        sources = []
      } else if (rowTitle.includes('sensitivity simulation')) {
        formula = `= Simulation assuming -10% revenue drop with fixed overhead = -(Rp 1,435.9 bn)`
        sources = []
      }
    } else if (slideNum === 14) {
      if (rowTitle.includes('breakeven threshold')) {
        formula = `= Required Gross Profit (378.1) / Gross Margin (68.04%) = +Rp 555.8 bn (+4.46% revenue growth)`
        sources = []
      }
    } else if (slideNum === 15) {
      if (rowTitle.includes('consolidated total')) {
        formula = `= ODS (${colChar}2) + Fintech (${colChar}3) + E-Com (${colChar}4) - Corporate Overhead (${colChar}6) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`, `${colChar}6`]
      }
    }
  }

  // Week 10 Formulas (Analyzing Investing Activities & Intercorporate Investments)
  else if (selectedWeekId.value === 'week10') {
    if (slideNum === 1) {
      if (rowTitle.includes('total long-term investing')) {
        formula = `= PP&E (${colChar}2) + Intangibles (${colChar}3) + Associates (${colChar}4) + JVs (${colChar}5) + Other (${colChar}6) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`, `${colChar}5`, `${colChar}6`]
      } else if (rowTitle.includes('investment in associates')) {
        formula = `= Tokopedia (7,432.3) + Bank Jago (2,894.9) + Other (267.6) = Rp 10,594.8 bn (23.2% of assets)`
        sources = []
      }
    } else if (slideNum === 3) {
      if (rowTitle.includes('total investment in associates')) {
        formula = `= Tokopedia (${colChar}2) + Bank Jago (${colChar}3) + Other (${colChar}4) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`]
      }
    } else if (slideNum === 4) {
      if (rowTitle.includes('total cash capital expenditure')) {
        formula = `= Software (${colChar}2) + Hardware (${colChar}3) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`]
      } else if (rowTitle.includes('net reinvestment rate')) {
        formula = `= Cash Capex (${colChar}4) - Annual D&A (${colChar}5) = ${val} (Asset base expanding)`
        sources = [`${colChar}4`, `${colChar}5`]
      }
    } else if (slideNum === 8) {
      if (rowTitle.includes('calculated impairment loss')) {
        formula = `= Carrying Value (${colChar}2) - Value in Use DCF (${colChar}4) = ${val}`
        sources = [`${colChar}2`, `${colChar}4`]
      } else if (rowTitle.includes('adjusted ending carrying value')) {
        formula = `= Post-impairment recoverable amount carried forward = Rp 15,745 mn`
        sources = []
      }
    } else if (slideNum === 10) {
      if (rowTitle.includes('ending net software carrying value')) {
        formula = `= Opening (${colChar}2) + Additions (${colChar}3) - Amortization (${colChar}4) - Impairment (${colChar}5) - FX (${colChar}6) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`, `${colChar}5`, `${colChar}6`]
      }
    } else if (slideNum === 11) {
      if (rowTitle.includes('historic impairment write-down')) {
        formula = `= 2023 Goodwill write-down on Tokopedia = -(Rp 79,481.2 bn) (83% of peak goodwill erased)`
        sources = []
      } else if (rowTitle.includes('final fintech cleanup')) {
        formula = `= 2025 Fintech goodwill write-down = -(Rp 356.8 bn); Remaining goodwill = Rp 15.7 bn`
        sources = []
      }
    } else if (slideNum === 14) {
      if (rowTitle.includes('ending carrying value')) {
        formula = `= Initial Cost + Share of Associate Net Profits (+178.5 bn) - Dividends (0.0) = Rp 10,594.8 bn`
        sources = []
      }
    } else if (slideNum === 16) {
      if (rowTitle.includes('combined goto exposure')) {
        formula = `= Tokopedia (${colChar}2) + Bank Jago (${colChar}3) = ${val} (97.5% of associate portfolio)`
        sources = [`${colChar}2`, `${colChar}3`]
      }
    } else if (slideNum === 20) {
      if (rowTitle.includes('debt-to-equity ratio')) {
        formula = `= Total Debt (7,742.6) / Parent Equity (15,626.6) = 49.5% (Parent) vs 27.0% (Consolidated)`
        sources = []
      } else if (rowTitle.includes('dupont equity multiplier')) {
        formula = `= Assets (45,757.6) / Parent Equity (15,626.6) = 2.928x (Parent) vs 1.593x (Consolidated)`
        sources = []
      } else if (rowTitle.includes('return on equity')) {
        formula = `= Parent Net Loss (-1,501.7) / Parent Equity (15,626.6) = -9.61% (Parent ROE)`
        sources = []
      }
    }
  }

  // Week 9 Formulas (Analyzing Financing Activities: Debt vs Equity, Bonds & Leases)
  else if (selectedWeekId.value === 'week9') {
    if (slideNum === 1) {
      if (rowTitle.includes('total borrowings')) {
        formula = `= Short-Term (${colChar}2) + Bank Loans (${colChar}3) + Convertibles (${colChar}4) + Other (${colChar}5) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`, `${colChar}5`]
      } else if (rowTitle.includes('total interest-bearing')) {
        formula = `= Total Borrowings (${colChar}6) + Lease Liabilities (${colChar}7) = ${val}`
        sources = [`${colChar}6`, `${colChar}7`]
      } else if (rowTitle.includes('debt-to-equity')) {
        formula = `= Total Debt (${colChar}8) / Consolidated Equity (${colChar}9) = ${val}`
        sources = [`${colChar}8`, `${colChar}9`]
      }
    } else if (slideNum === 3) {
      if (rowTitle.includes('total financial debt stack')) {
        formula = `= Weighted Average Pre-Tax Cost: Rp 535.2 bn Interest / Rp 7,742.6 bn Total Debt = 6.91%`
        sources = []
      } else if (rowTitle.includes('short-term secured loan')) {
        formula = `= Bank Mandiri credit facility with marketable securities pledge = Rp 1,001.6 bn`
        sources = []
      } else if (rowTitle.includes('long-term syndicated')) {
        formula = `= UOB & DBS facility secured by GoFood commission rights = Rp 3,662.3 bn`
        sources = []
      } else if (rowTitle.includes('equity-linked convertible')) {
        formula = `= USD 185M notes (IFC USD 150M + WAF USD 35M) = Rp 2,876.3 bn`
        sources = []
      }
    } else if (slideNum === 4) {
      if (rowTitle.includes('liquidity coverage')) {
        formula = `= Unrestricted Cash (21,755.2) / Current Debt (1,457.5) = 14.9x Coverage`
        sources = []
      }
    } else if (slideNum === 5) {
      if (rowTitle.includes('required rate of return')) {
        formula = `= Pre-Tax Rd (6.91%) vs After-Tax Rd (5.39%) vs Cost of Equity (8.45%)`
        sources = []
      } else if (rowTitle.includes('tax shield benefit')) {
        formula = `= Interest Expense (535.2) * Corporate Tax Rate (22%) = Rp 117.7 bn (Unused due to losses)`
        sources = []
      }
    } else if (slideNum === 6) {
      if (rowTitle.includes('debt issuance costs')) {
        formula = `= Net Carrying Value (2,247.2) = Gross Proceeds (2,304.2) - Issuance Fees (57.0)`
        sources = []
      }
    } else if (slideNum === 8) {
      if (rowTitle.includes('carrying value vs face')) {
        formula = `= IFC (2,396.9) + WAF (479.4) = Rp 2,876.3 bn total equity-linked debt`
        sources = []
      }
    } else if (slideNum === 9) {
      if (rowTitle.includes('balance sheet: liabilities')) {
        formula = `= Current Lease (66.3) + Non-Current Lease (89.3) = Rp 155.6 bn Total PSAK 73 Lease Debt`
        sources = []
      } else if (rowTitle.includes('statement of cash flows')) {
        formula = `= Shifted ~Rp 85 bn lease principal repayment from CFO into Financing Cash Flows (CFF)`
        sources = []
      }
    } else if (slideNum === 10) {
      if (rowTitle.includes('total fy2025 audited leases')) {
        formula = `= Gross Undiscounted (${colChar}2) - Future Finance Charges (${colChar}3) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`]
      }
    } else if (slideNum === 13) {
      if (rowTitle.includes('share dilution impact')) {
        formula = `= Conversion of USD 185M notes = ~33.5 billion Series A shares (~2.81% dilution)`
        sources = []
      }
    } else if (slideNum === 14) {
      if (rowTitle.includes('debt-to-assets')) {
        formula = `= Total Debt (7,742.6) / Total Assets (45,757.6) = 16.9% (+810 bps YoY)`
        sources = []
      } else if (rowTitle.includes('debt-to-parent equity')) {
        formula = `= Total Debt (7,742.6) / Parent Equity (15,626.6) = 49.5% (+3,260 bps YoY)`
        sources = []
      } else if (rowTitle.includes('dupont equity multiplier')) {
        formula = `= Total Assets (45,757.6) / Consolidated Equity (28,711.7) = 1.593x (+12.1% YoY)`
        sources = []
      } else if (rowTitle.includes('times interest earned')) {
        formula = `= Operating EBIT (-(378.1)) / Finance Costs (245.8) = -1.54x (Operating loss)`
        sources = []
      } else if (rowTitle.includes('cash debt service coverage')) {
        formula = `= Operating Cash Flow (+307.0) / Debt Service (3,024.0) = 0.10x`
        sources = []
      }
    } else if (slideNum === 15) {
      if (rowTitle.includes('rule 5')) {
        formula = `= Cash & Equivalents (21,755.2) - Total Debt (7,742.6) = Net Cash +Rp 14,012.6 bn`
        sources = []
      }
    }
  }

  // Week 7 Formulas (Accounting Quality, Earnings Management & Midterm Toolkit)
  else if (selectedWeekId.value === 'week7') {
    if (slideNum === 1) {
      if (rowTitle.includes('revenue recognition')) {
        formula = `= Net Platform Revenue (18,322.2) = Gross (24,500.0) - Promos (6,177.8) [PSAK 72 Agent]`
        sources = []
      } else if (rowTitle.includes('one-time')) {
        formula = `= Rp 70.3T Tokopedia Deconsolidation Paper Gain in FY2024 (Zero recurring cash)`
        sources = []
      } else if (rowTitle.includes('capitalized software')) {
        formula = `= FY2025 (880.3) vs FY2024 (447.7) = +96.6% YoY Surge (Intangibles Note 12)`
        sources = []
      } else if (rowTitle.includes('related-party')) {
        formula = `= Tokopedia E-Commerce Service Fee = Rp 740.0 bn (Note 38 Related Parties)`
        sources = []
      } else if (rowTitle.includes('sloan accrual')) {
        formula = `= (Net Income - CFO) / Avg Assets = (-1,501.7 - 307.0) / 45,952.3 = -3.94% (Decile 2)`
        sources = []
      }
    } else if (slideNum === 8) {
      if (rowTitle.includes('statutory net revenue')) {
        formula = `= Gross Fees (~24,500.0) - User Promos & Subsidies (6,177.8) = Rp 18,322.2 bn`
        sources = [`${colChar}2`, `${colChar}3`]
      } else if (rowTitle.includes('user promos')) {
        formula = `= Contractual reduction of transaction price under PSAK 72 = -(Rp 6,177.8 bn)`
        sources = []
      }
    } else if (slideNum === 9) {
      if (rowTitle.includes('fy2023')) {
        formula = `= Reported Loss (-90,516.3) - Goodwill Impairment (-79,481.2) = Normalized EBIT (-10,313.6)`
        sources = []
      } else if (rowTitle.includes('fy2024')) {
        formula = `= Reported Loss (-5,471.2) - Tokopedia Gain (+70,300.0) = Normalized EBIT (-2,239.5)`
        sources = []
      } else if (rowTitle.includes('fy2025')) {
        formula = `= Reported Loss (-1,501.7) with Zero One-Off Impairments = Operating EBIT (-378.1)`
        sources = []
      }
    } else if (slideNum === 12) {
      if (rowTitle.includes('total accounting accruals')) {
        formula = `= Net Income (-1,501.7) - CFO (+307.0) = -(Rp 1,808.7 bn)`
        sources = [`${colChar}2`, `${colChar}3`]
      } else if (rowTitle.includes('average total assets')) {
        formula = `= (FY2024 Assets 46,146.4 + FY2025 Assets 45,758.1) / 2 = Rp 45,952.3 bn`
        sources = []
      } else if (rowTitle.includes('calculated sloan accrual')) {
        formula = `= Total Accruals (-1,808.7) / Average Total Assets (45,952.3) = -3.94% (High Quality)`
        sources = [`${colChar}4`, `${colChar}5`]
      }
    } else if (slideNum === 16) {
      if (rowTitle.includes('impact on cash flow')) {
        formula = `= Reported CFO (+307.0) - Software Capitalized (880.3) = Adjusted CFO -(573.3 bn)`
        sources = []
      } else if (rowTitle.includes('impact on operating profit')) {
        formula = `= Operating Loss (-378.1) without Capitalization = True Operating Loss -(1,258.4 bn)`
        sources = []
      }
    } else if (slideNum === 17) {
      if (rowTitle.includes('rule 1')) {
        formula = `= Cash Collected (18,339.5) / Reported Net Revenue (18,322.2) = 100.1% (PASSED)`
        sources = []
      } else if (rowTitle.includes('rule 2')) {
        formula = `= Receivables Growth (-12.0%) vs Net Revenue Growth (+15.3%) = High Quality (PASSED)`
        sources = []
      } else if (rowTitle.includes('rule 3')) {
        formula = `= Capitalized Software (+96.6% YoY to Rp 880.3 bn) shifted from Opex to Capex (FLAGGED)`
        sources = []
      }
    } else if (slideNum === 20) {
      if (rowTitle.includes('week 4')) {
        formula = `= CFO (+307.0) - Capex (1,182.4) = FCF -(Rp 875.3 bn)`
        sources = []
      } else if (rowTitle.includes('week 5')) {
        formula = `= NPM (-8.20%) * ATO (0.400x) * EM (1.593x) = Consolidated ROE (-5.23%)`
        sources = []
      } else if (rowTitle.includes('week 6')) {
        formula = `= 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5 = -2.81 (Altman Distress)`
        sources = []
      } else if (rowTitle.includes('week 7')) {
        formula = `= (Net Income - CFO) / Assets = (-1,501.7 - 307.0) / 45,952.3 = -3.94% (Decile 2)`
        sources = []
      }
    }
  }

  // Week 6 Formulas (Liquidity, Solvency & Altman Z-Score)
  else if (selectedWeekId.value === 'week6') {
    if (slideNum === 1) {
      if (rowTitle.includes('current ratio')) {
        formula = `= Current Assets (25,755.6) / Current Liabilities (10,042.7) = 2.56x`
        sources = []
      } else if (rowTitle.includes('quick ratio')) {
        formula = `= Quick Assets (23,637.6) / Current Liabilities (10,042.7) = 2.35x`
        sources = []
      } else if (rowTitle.includes('total debt')) {
        formula = `= Short-Term (2,778.2) + Long-Term (4,964.4) = Rp 7,742.6 bn (+102.7% YoY)`
        sources = []
      } else if (rowTitle.includes('debt-to-equity')) {
        formula = `= Total Debt (7,742.6) / Parent Equity (15,626.6) = 49.5%`
        sources = []
      } else if (rowTitle.includes('times interest')) {
        formula = `= EBIT (-(378.1)) / Interest (245.8) = -1.54x (Operating loss)`
        sources = []
      } else if (rowTitle.includes('cash dscr')) {
        formula = `= CFO (+307.0) / Debt Service (3,024.0) = 0.10x (Covers only 10%)`
        sources = []
      } else if (rowTitle.includes('altman z-score')) {
        formula = `= 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5 = -2.81 (Distress Zone)`
        sources = []
      }
    } else if (slideNum === 4) {
      if (rowTitle.includes('total consolidated debt')) {
        formula = `= ${colChar}2 + ${colChar}3  [Short-Term Debt + Long-Term Debt]`
        sources = [`${colChar}2`, `${colChar}3`]
      } else if (rowTitle.includes('debt-to-equity (consolidated)')) {
        formula = `= Total Debt (${colChar}4) / Consolidated Equity (${colChar}5) = ${val}`
        sources = [`${colChar}4`, `${colChar}5`]
      } else if (rowTitle.includes('debt-to-equity (parent')) {
        formula = `= Total Debt (${colChar}4) / Parent Equity (${colChar}6) = ${val}`
        sources = [`${colChar}4`, `${colChar}6`]
      }
    } else if (slideNum === 6) {
      if (rowTitle.includes('total current assets')) {
        formula = `= Cash (${colChar}2) + Receivables (${colChar}3) + Other (${colChar}4) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`]
      } else if (rowTitle.includes('total current liabilities')) {
        formula = `= Short-Term Debt (${colChar}6) + Payables (${colChar}7) = ${val}`
        sources = [`${colChar}6`, `${colChar}7`]
      } else if (rowTitle.includes('net working capital')) {
        formula = `= Current Assets (${colChar}5) - Current Liabilities (${colChar}8) = ${val}`
        sources = [`${colChar}5`, `${colChar}8`]
      }
    } else if (slideNum === 7) {
      if (rowTitle.includes('current ratio')) {
        formula = `= Current Assets (${colChar}2) / Current Liabilities (${colChar}3) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`]
      }
    } else if (slideNum === 8) {
      if (rowTitle.includes('calculated quick ratio')) {
        formula = `= Quick Assets (23,637.6) / Current Liabilities (10,042.7) = 2.35x`
        sources = []
      }
    } else if (slideNum === 10) {
      if (rowTitle.includes('debt-to-assets')) {
        formula = `= Total Debt (${colChar}2) / Total Assets = ${val}`
        sources = []
      } else if (rowTitle.includes('debt-to-parent')) {
        formula = `= Total Debt (${colChar}2) / Parent Equity = ${val}`
        sources = []
      }
    } else if (slideNum === 12) {
      if (rowTitle.includes('tie ratio')) {
        formula = `= EBIT (${colChar}2) / Interest (${colChar}3) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`]
      }
    } else if (slideNum === 13) {
      if (rowTitle.includes('cash debt service coverage')) {
        formula = `= CFO (+307.0) / Debt Service (3,024.0) = 0.102x`
        sources = []
      }
    } else if (slideNum === 15) {
      if (rowTitle.includes('total altman z-score')) {
        formula = `= SUM(F2:F6)  [+0.4121 - 6.5519 - 0.0274 + 2.9591 + 0.4000 = -2.8081]`
        sources = ['F2', 'F3', 'F4', 'F5', 'F6']
      } else if (rowTitle.includes('x1')) {
        formula = `= Working Capital (15,712.9) / Assets (45,758.1) * 1.20 = +0.4121`
        sources = []
      } else if (rowTitle.includes('x2')) {
        formula = `= Retained Deficit (-214,142.5) / Assets (45,758.1) * 1.40 = -6.5519`
        sources = []
      } else if (rowTitle.includes('x3')) {
        formula = `= EBIT (-378.1) / Assets (45,758.1) * 3.30 = -0.0274`
        sources = []
      } else if (rowTitle.includes('x4')) {
        formula = `= Market Cap (84,070.0) / Liabilities (17,046.4) * 0.60 = +2.9591`
        sources = []
      } else if (rowTitle.includes('x5')) {
        formula = `= Revenue (18,322.2) / Assets (45,758.1) * 0.999 = +0.4000`
        sources = []
      }
    } else if (slideNum === 17) {
      if (rowTitle.includes('total altman z-score')) {
        formula = `= Working Capital (+0.41) - Deficit (-6.55) - EBIT (-0.03) + Mcap (+2.96) + Turns (+0.40) = -2.81`
        sources = []
      }
    } else if (slideNum === 18) {
      if (rowTitle.includes('altman z (1968)')) {
        formula = `= 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5 = -2.81`
        sources = []
      } else if (rowTitle.includes('altman z\'\'')) {
        formula = `= 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4(book) = -11.29`
        sources = []
      }
    }
  }

  // Week 5 Formulas (Profitability Analysis & DuPont Framework)
  else if (selectedWeekId.value === 'week5') {
    if (slideNum === 1) {
      if (rowTitle.includes('return on equity')) {
        formula = `= Net Income / Equity  [Consolidated Return on Equity = ${val}]`
        sources = []
      } else if (rowTitle.includes('asset turnover')) {
        formula = `= Net Revenue / Total Assets = ${val}`
        sources = []
      } else if (rowTitle.includes('equity multiplier')) {
        formula = `= Total Assets / Total Equity = ${val}`
        sources = []
      } else if (rowTitle.includes('net profit margin')) {
        formula = `= Net Loss / Net Revenue = ${val}`
        sources = []
      } else if (rowTitle.includes('gross profit margin')) {
        formula = `= Gross Profit / Net Revenue = ${val}`
        sources = []
      }
    } else if (slideNum === 3) {
      if (rowTitle.includes('return on equity')) {
        formula = `= NPM * ATO * EM  [Decomposed Return on Equity]`
        sources = []
      }
    } else if (slideNum === 5) {
      if (rowTitle.includes('gross profit')) {
        formula = `= Rev (100.0%) - COGS (${colChar}3)  [Gross Margin = Gross Profit / Revenue]`
        sources = [`${colChar}2`, `${colChar}3`]
      } else if (rowTitle.includes('operating loss')) {
        formula = `= Gross Margin (${colChar}4) - Total Opex (${colChar}8)  [Operating EBIT Margin]`
        sources = [`${colChar}4`, `${colChar}8`]
      } else if (rowTitle.includes('total operating expenses')) {
        formula = `= S&M (${colChar}5) + G&A (${colChar}6) + Tech (${colChar}7)  [Total Overhead Burden]`
        sources = [`${colChar}5`, `${colChar}6`, `${colChar}7`]
      } else if (rowTitle.includes('net loss margin')) {
        formula = `= Net Loss (${colChar}2) / Revenue  [Net Profit Margin for Year]`
        sources = [`${colChar}2`]
      }
    } else if (slideNum === 6) {
      formula = `= (${colChar}${rowNum} - 100.0) / 100.0  [Horizontal Growth Relative to 2023 Base Year]`
      sources = [`B${rowNum}`]
    } else if (slideNum === 8) {
      if (rowTitle.includes('product = return')) {
        formula = `= D2 * D3 * D4  [NPM (-8.20%) * ATO (0.400x) * EM (1.593x) = -5.23% ROE]`
        sources = ['D2', 'D3', 'D4']
      } else if (rowTitle.includes('step 1')) {
        formula = `= Net Income (-(Rp 1,501.7 bn)) / Revenue (Rp 18,322.2 bn) = -8.20%`
        sources = []
      } else if (rowTitle.includes('step 2')) {
        formula = `= Revenue (Rp 18,322.2 bn) / Total Assets (Rp 45,758.1 bn) = 0.400x`
        sources = []
      } else if (rowTitle.includes('step 3')) {
        formula = `= Total Assets (Rp 45,758.1 bn) / Total Equity (Rp 28,711.7 bn) = 1.593x`
        sources = []
      }
    } else if (slideNum === 9) {
      if (rowTitle.includes('final net profit')) {
        formula = `= Net Loss (-(Rp 1,501.7 bn)) / Revenue (Rp 18,322.2 bn) = -8.20%`
        sources = []
      }
    } else if (slideNum === 10) {
      if (rowTitle.includes('calculated asset turnover')) {
        formula = `= Revenue (Rp 18,322.2 bn) / Total Assets (${colChar}7) = ${val}`
        sources = [`${colChar}2`, `${colChar}7`]
      }
    } else if (slideNum === 11) {
      if (rowTitle.includes('equity multiplier (consolidated)')) {
        formula = `= Total Assets (${colChar}2) / Consolidated Equity (${colChar}5) = ${val}`
        sources = [`${colChar}2`, `${colChar}5`]
      } else if (rowTitle.includes('equity multiplier (parent')) {
        formula = `= Total Assets (${colChar}2) / Parent Equity (${colChar}6) = ${val}`
        sources = [`${colChar}2`, `${colChar}6`]
      }
    } else if (slideNum === 12) {
      if (rowTitle.includes('return on equity')) {
        formula = `= ${colChar}2 * ${colChar}3 * ${colChar}4  [NPM * ATO * EM = ROE]`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`]
      } else if (rowTitle.includes('asset turnover')) {
        formula = `= Revenue / Total Assets = ${val}`
        sources = []
      } else if (rowTitle.includes('equity multiplier')) {
        formula = `= Total Assets / Equity = ${val}`
        sources = []
      }
    } else if (slideNum === 17) {
      if (rowTitle.includes('return on equity')) {
        formula = `= NPM (${colChar}2) * ATO (${colChar}3) * EM (${colChar}4) = ${val}`
        sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`]
      }
    }
  }

  // Week 4 Formulas (Statement of Cash Flows)
  else if (selectedWeekId.value === 'week4') {
    if (slideNum === 4) {
      if (rowTitle.includes('free cash flow')) {
        formula = `= D5 - D6  (CFO +Rp 307.0 bn - Capex Rp 1,182.4 bn = -(Rp 875.3 bn))`
        sources = ['D5', 'D6']
      } else if (rowTitle.includes('operating cash flow')) {
        formula = `= Customer Collections Rp 18,339.5 bn - Payments Rp 18,032.5 bn = +307.0 bn`
        sources = ['D2']
      } else if (rowTitle.includes('capital expenditures')) {
        formula = `= PP&E Purchases (Rp 302.1 bn) + Capitalized Software (Rp 880.3 bn) = Rp 1,182.4 bn`
        sources = []
      } else if (rowTitle.includes('retained deficit')) {
        formula = `= Beginning Deficit (212,640.8) + Current Net Loss (1,501.7) = -(Rp 214,142.5 bn)`
        sources = ['C8', 'D4']
      } else if (rowTitle.includes('operating loss')) {
        formula = `= Gross Profit Rp 10,576.0 bn - Operating Expenses Rp 10,954.1 bn = -(Rp 378.1 bn)`
        sources = []
      }
    } else if (slideNum === 5) {
      if (rowTitle.includes('net increase')) {
        formula = `= B2 + B3 + B4 + B5  (CFO 307.0 + CFI 1,094.6 + CFF 2,494.4 - FX 20.2 = +751.4 bn)`
        sources = ['C2', 'C3', 'C4', 'C5']
      } else if (rowTitle.includes('financing activities')) {
        formula = `= Borrowed Rp 3,718.0 bn in new bank debt less debt repayments`
        sources = []
      } else if (rowTitle.includes('investing activities')) {
        formula = `= Liquidated Rp 1,386.5 bn of time deposits less Rp 1,182.4 bn capex`
        sources = []
      }
    } else if (slideNum === 11) {
      if (rowTitle.includes('sebelum pajak')) {
        formula = `= B2 - B3  (Customer Receipts 18,339.5 - Supplier Payments 17,987.3 = 352.2)`
        sources = ['C2', 'C3']
      } else if (rowTitle.includes('arus kas bersih')) {
        formula = `= B4 - B5 - B6  (Operations 352.2 - Tax 415.1 - Interest 30.1 = 307.0)`
        sources = ['C4', 'C5', 'C6']
      }
    } else if (slideNum === 12) {
      if (rowTitle.includes('arus kas bersih')) {
        formula = `= B2 + B3 + B4 + B5 + B6 - B7  (Net Loss + D&A + Stock Comp + Associates - Working Capital)`
        sources = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7']
      } else if (rowTitle.includes('penyusutan')) {
        formula = `= Non-cash addback of software amortization and server depreciation`
        sources = []
      }
    } else if (slideNum === 14) {
      if (rowTitle.includes('total capital expenditures')) {
        formula = `= B3 + B4  (PP&E Capex 302.1 + Capitalized Software Capex 880.3 = 1,182.4)`
        sources = ['C3', 'C4']
      } else if (rowTitle.includes('free cash flow')) {
        formula = `= B2 - B5  (CFO 307.0 - Total Capex 1,182.4 = -(Rp 875.3 bn))`
        sources = ['C2', 'C5']
      }
    } else if (slideNum === 17) {
      if (rowTitle.includes('total mandatory outflows')) {
        formula = `= B3 + B4 + B5  (Capex 1,182.4 + Short-Term Debt 2,778.2 + Dividends 0 = 3,960.6)`
        sources = ['B3', 'B4', 'B5']
      } else if (rowTitle.includes('adequacy ratio')) {
        formula = `= B2 / B6  (CFO 307.0 / Mandatory Outflows 3,960.6 = 0.078x)`
        sources = ['B2', 'B6']
      }
    } else if (slideNum === 18) {
      if (rowTitle.includes('total consolidated debt')) {
        formula = `= B3 + B4  (Short-Term Borrowings 2,778.2 + Long-Term Debt 4,964.4 = 7,742.6)`
        sources = ['C3', 'C4']
      } else if (rowTitle.includes('cash flow to debt ratio')) {
        formula = `= B2 / B5  (CFO 307.0 / Total Debt 7,742.6 = 0.040x)`
        sources = ['C2', 'C5']
      } else if (rowTitle.includes('amortization period')) {
        formula = `= 1 / 0.040x = 25.2 Years of 2025 CFO required to retire debt`
        sources = ['C6']
      }
    } else if (slideNum === 19) {
      if (rowTitle.includes('calculated return')) {
        formula = `= B2 / B3  (CFO 307.0 / Total Assets 45,758.1 = 0.67% Cash ROA)`
        sources = ['B2', 'B3']
      }
    } else if (slideNum === 22) {
      if (rowTitle.includes('total capital expenditures')) {
        const ppe = `${colChar}3`
        const soft = `${colChar}4`
        formula = `= ${ppe} + ${soft}  [PP&E Purchases + Capitalized Software]`
        sources = [ppe, soft]
      } else if (rowTitle.includes('calculated free cash flow')) {
        const cfo = `${colChar}2`
        const capex = `${colChar}5`
        formula = `= ${cfo} - ${capex}  [CFO +307.0 - Capex 1,182.4 = -(Rp 875.3 bn)]`
        sources = [cfo, capex]
      } else if (rowTitle.includes('cumulative retained deficit')) {
        formula = `= Statutory Audited Retained Earnings Deficit (LK GOTO Note 21, p. 104)`
        sources = []
      }
    } else if (slideNum === 24) {
      if (rowTitle.includes('reconstructed cfo')) {
        formula = `= Step 1 (Loss) + Steps 2-6 (Addbacks) - Step 7 (Working Capital) = +307.0`
        sources = ['D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8']
      }
    }
  }

  // Week 3 Formulas (Asset & Liability Valuation)
  else if (selectedWeekId.value === 'week3') {
    if (slideNum === 3) {
      if (rowTitle.includes('abba net fixed assets')) {
        if (colChar === 'C') {
          formula = `= B2 + Surplus  (Rp 19.67 bn + Rp 55.08 bn Revaluation = Rp 70.36 bn)`
          sources = ['B2']
        } else if (colChar === 'D') {
          formula = `= (C2 - B2) / B2  [(70.36 - 19.67) / 19.67 = +257.7% (3.6x Surge)]`
          sources = ['C2', 'B2']
        }
      } else if (rowTitle.includes('revaluation surplus')) {
        formula = `= Direct Credit to Equity / OCI (PSAK 16 Revaluation Model, Bypasses P&L)`
        sources = []
      } else if (rowTitle.includes('goto property')) {
        if (colChar === 'C') {
          formula = `= B5 - Depreciation  (Beginning 712.4 bn - Depr 285.2 bn + Additions = 622.1 bn)`
          sources = ['B5']
        } else if (colChar === 'D') {
          formula = `= (C5 - B5) / B5  [(622.1 - 712.4) / 712.4 = -12.7% Contraction]`
          sources = ['C5', 'B5']
        }
      } else if (rowTitle.includes('pp&e as %')) {
        formula = `= Net PP&E (622.1) / Total Assets (45,758.1) = 1.4% (Asset-Light Platform)`
        sources = ['C5']
      }
    } else if (slideNum === 6) {
      if (rowTitle.includes('total assets')) {
        formula = `= SUM(B2:B8)  [Cash + Associates + Other + Software + PP&E + Receivables + Inventory]`
        sources = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
      } else if (colChar === 'C') {
        formula = `= B${rowNum} / B9  [% of Total Assets (Rp 45,758.1 billion)]`
        sources = [`B${rowNum}`, 'B9']
      }
    } else if (slideNum === 10) {
      formula = `= Audited Accounting Policy Schedule (LK Note 2, p. 66)`
      sources = []
    } else if (slideNum === 12) {
      formula = `= Statutory Citation under DSAK-IAI Indonesian SAK Framework`
      sources = []
    } else if (slideNum === 13) {
      if (rowTitle.includes('revaluation surplus')) {
        formula = `= ABBA credited Rp 55.1 bn to OCI; GoTo has Rp 0.0 property revaluation surplus`
        sources = []
      } else if (rowTitle.includes('total shareholders')) {
        formula = `= Share Capital + Agio + Surplus - Cumulative Retained Deficit`
        sources = []
      }
    } else if (slideNum === 14) {
      if (rowTitle.includes('psak 71')) {
        formula = `= Mark-to-Market Loss on Startup Equity & Derivatives flowing directly through P&L`
        sources = []
      } else if (rowTitle.includes('psak 15')) {
        formula = `= Proportional Share of Tokopedia & Bank Jago Net Operating Losses`
        sources = []
      }
    }
  }

  // Week 1 Formulas (The FSA Mindset & Six-Step Framework)
  else if (selectedWeekId.value === 'week1') {
    if (slideNum === 1) {
      if (rowTitle.includes('operating income')) {
        formula = `= Gross Profit - Total Operating Expenses -> FY2025 loss narrowed 96.3% from -(10,279.6) to -(378.1)`
        sources = []
      } else if (rowTitle.includes('operating cash flow')) {
        formula = `= Direct Cash Receipts - Cash Operating Payments = +Rp 1,354.5 bn (FY2025 Positive Inflection)`
        sources = []
      }
    } else if (slideNum === 10) {
      if (rowTitle.includes('asset turnover')) {
        formula = `= Net Revenue (18,322.2) / Total Assets (45,677.7) = 0.40x (up from 0.27x in FY2023)`
        sources = []
      } else if (rowTitle.includes('liquidity')) {
        formula = `= Current Assets / Current Liabilities = 2.89x (vs 2.52x in FY2023)`
        sources = []
      }
    } else if (slideNum === 12) {
      if (rowTitle.includes('net cash floor')) {
        formula = `= (Cash 21,755.1 bn - Total Debt 7,742.6 bn) / 1,062,012.1M shares = Rp 13.20/share`
        sources = []
      }
    }
  }

  // Week 2: Slide 3 Comparative Financial Snapshot
  else if (slideNum === 3) {
    if (rowTitle.includes('gross profit')) {
      if (cIdx === 0) {
        formula = `= Row 2 - Row 3  [Gross Revenue - Cost of Revenue (COGS)]`
        sources = ['D2', 'D3']
      } else {
        const revCell = `${colChar}2`
        const cogsCell = `${colChar}3`
        formula = `= ${revCell} - ${cogsCell}  (Gross Revenue - Cost of Revenue)`
        sources = [revCell, cogsCell]
      }
    } else if (rowTitle.includes('operating loss') || rowTitle.includes('ebit')) {
      if (cIdx === 0) {
        formula = `= Row 4 - Row 5  [Gross Profit - Total Operating Expenses]`
        sources = ['D4', 'D5']
      } else {
        const gpCell = `${colChar}4`
        const opexCell = `${colChar}5`
        formula = `= ${gpCell} - ${opexCell}  (Gross Profit - Operating Expenses)`
        sources = [gpCell, opexCell]
      }
    } else if (rowTitle.includes('net income') || rowTitle.includes('net loss')) {
      if (cIdx === 0) {
        formula = `= Operating Loss + Financial Net - Taxes - Associates`
        sources = ['D6']
      } else {
        const ebitCell = `${colChar}6`
        formula = `= ${ebitCell} + Net Non-Operating & Tax Items`
        sources = [ebitCell]
      }
    } else if (rowTitle.includes('total debt')) {
      formula = `= Short-Term Borrowings + Long-Term Debt (Bank loans doubled to Rp 7,742.6 bn)`
      sources = []
    } else if (rowTitle.includes('shareholders\' equity')) {
      formula = `= Total Assets (${colChar}9) - Total Liabilities`
      sources = [`${colChar}9`]
    } else if (rowTitle.includes('retained deficit') || rowTitle.includes('accumulated')) {
      if (colChar === 'D') {
        formula = `= C12 + D8  (Prior Deficit (212,640.8) + 2025 Loss (1,501.7))`
        sources = ['C12', 'D8']
      } else {
        formula = `= Cumulative Capital Burned Since Inception (-Rp 214.1 Trillion)`
        sources = []
      }
    } else if (rowTitle.includes('free cash flow')) {
      if (cIdx === 0) {
        formula = `= Cash Flow from Operations (CFO) - Capex`
        sources = ['D14']
      } else {
        const cfoCell = `${colChar}14`
        formula = `= ${cfoCell} - Capex  (CFO - Capital Expenditures)`
        sources = [cfoCell]
      }
    } else if (rowTitle.includes('cash flow from operations')) {
      formula = `= Net Loss (${colChar}8) + Non-Cash D&A + Working Capital Adjustments`
      sources = [`${colChar}8`]
    } else if (rowTitle.includes('gross revenue')) {
      formula = `= Audited Top-Line Revenue from On-Demand, E-Commerce, Fintech`
      sources = []
    } else if (rowTitle.includes('cost of revenue')) {
      formula = `= Direct Processing Fees, Driver Incentives, IT Hosting`
      sources = []
    } else if (rowTitle.includes('operating expenses')) {
      formula = `= Sales & Marketing + General & Administrative + Product Development`
      sources = []
    }
  }
  // Slide 5: Income Statement Decomposition
  else if (slideNum === 5) {
    if (rowTitle.includes('gross profit')) {
      if (colChar === 'D') {
        formula = `= C4 / C2  [Gross Profit 10,576.0 / Net Revenue 18,322.2 = 57.7%]`
        sources = ['C4', 'C2']
      } else {
        formula = `= ${colChar}2 - ${colChar}3  (Net Revenue - Cost of Revenue)`
        sources = [`${colChar}2`, `${colChar}3`]
      }
    } else if (rowTitle.includes('total operating expenses')) {
      if (colChar === 'D') {
        formula = `= C8 / C2  [Opex 10,954.1 / Net Revenue 18,322.2 = 59.8%]`
        sources = ['C8', 'C2']
      } else {
        formula = `= SUM(${colChar}5:${colChar}7)  (Sales & Mktg + G&A + R&D)`
        sources = [`${colChar}5`, `${colChar}6`, `${colChar}7`]
      }
    } else if (rowTitle.includes('operating loss')) {
      if (colChar === 'D') {
        formula = `= C9 / C2  [Loss (378.1) / Net Revenue 18,322.2 = -2.1%]`
        sources = ['C9', 'C2']
      } else {
        formula = `= ${colChar}4 - ${colChar}8  (Gross Profit - Operating Expenses)`
        sources = [`${colChar}4`, `${colChar}8`]
      }
    } else if (rowTitle.includes('net loss')) {
      if (colChar === 'D') {
        formula = `= C12 / C2  [Net Loss (1,501.7) / Net Revenue 18,322.2 = -8.2%]`
        sources = ['C12', 'C2']
      } else {
        formula = `= ${colChar}9 + Financial Net - ${colChar}10 - ${colChar}11`
        sources = [`${colChar}9`, `${colChar}10`, `${colChar}11`]
      }
    } else if (colChar === 'D') {
      formula = `= C${rowNum} / C2  [% of 2025 Net Revenue]`
      sources = [`C${rowNum}`, 'C2']
    }
  }
  // Slide 6: Changes in Equity
  else if (slideNum === 6) {
    if (colChar === 'D') {
      formula = `= B${rowNum} + C${rowNum}  (Beginning Equity + Net Movements)`
      sources = [`B${rowNum}`, `C${rowNum}`]
    } else if (rowTitle.includes('consolidated equity')) {
      formula = `= Total Parent Equity (Row 7) + Non-Controlling Interests (Row 8)`
      sources = [`${colChar}7`, `${colChar}8`]
    }
  }
  // Slide 8: Balance Sheet
  else if (slideNum === 8) {
    if (rowTitle.includes('total assets')) {
      formula = `= SUM(${colChar}2:${colChar}8)  [Cash + Receivables + Assoc + PP&E + Goodwill]`
      sources = [`${colChar}2`, `${colChar}3`, `${colChar}4`, `${colChar}5`, `${colChar}6`, `${colChar}7`, `${colChar}8`]
    } else if (rowTitle.includes('total liabilities')) {
      formula = `= ${colChar}10 + ${colChar}11  [Short-Term Debt + Long-Term Debt]`
      sources = [`${colChar}10`, `${colChar}11`]
    } else if (rowTitle.includes('equity')) {
      formula = `= ${colChar}9 - ${colChar}12  (Total Assets - Total Liabilities)`
      sources = [`${colChar}9`, `${colChar}12`]
    } else if (colChar === 'D') {
      formula = `= C${rowNum} / C9  [% of Total Assets]`
      sources = [`C${rowNum}`, 'C9']
    }
  }
  // Slide 10: Cash Flows
  else if (slideNum === 10) {
    if (rowTitle.includes('free cash flow')) {
      formula = `= ${colChar}2 + ${colChar}3  (CFO + Capex)`
      sources = [`${colChar}2`, `${colChar}3`]
    } else if (rowTitle.includes('net increase in cash')) {
      formula = `= ${colChar}2 + ${colChar}3 + ${colChar}5 + ${colChar}6  (CFO + Investing + Financing)`
      sources = [`${colChar}2`, `${colChar}3`, `${colChar}5`, `${colChar}6`]
    }
  }
  // Slide 14: Net Income to CFO
  else if (slideNum === 14) {
    if (rowTitle.includes('operating cash flow')) {
      formula = `= B2 + SUM(B3:B7)  (Net Loss + Non-Cash D&A/Stock/Assoc + Working Capital)`
      sources = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
    }
  }

  return { ref: cellRef, formula, val: String(val), sources }
}

const onHoverCell = (slideNum, rIdx, cIdx, rVals) => {
  activeFormulaCell.value = getCellFormulaInfo(slideNum, rIdx, cIdx, rVals)
}

const setHoveredRef = (slideNum, rowIdx, colIdx, rows) => {
  hoveredRowIdx.value = rowIdx
  hoveredCellRef.value = `${rowIdx}-${colIdx}`
  if (rows && rows[rowIdx]) {
    activeFormulaCell.value = getCellFormulaInfo(slideNum, rowIdx, colIdx, rows[rowIdx])
  }
}

const clearHoveredRef = () => {
  hoveredRowIdx.value = null
  hoveredCellRef.value = null
}

const noteTokensCache = new Map()

const getNoteTokens = (note, rows) => {
  if (!note) return []
  if (!rows || rows.length === 0) return [{ type: 'text', text: note }]
  if (noteTokensCache.has(note)) return noteTokensCache.get(note)

  const pattern = /(-?Rp\s*[\d,.]+\s*(?:trillion|billion|million|bn|m|t)?|\(?Rp\s*[\d,.]+\s*(?:trillion|billion|million|bn|m|t)?\)?|[-+]?[\d,.]+\s*%|\b\d+[.,]\d+\s*(?:trillion|billion|million|bn|m|t)?\b)/gi
  const tokens = []
  let lastIdx = 0
  let match

  while ((match = pattern.exec(note)) !== null) {
    const start = match.index
    const end = pattern.lastIndex
    if (start > lastIdx) {
      tokens.push({ type: 'text', text: note.slice(lastIdx, start) })
    }
    const matchText = match[0].trim()
    const digits = matchText.replace(/[^\d.]/g, '')

    let bestMatch = null
    // 1. Exact match first
    for (let rIdx = 0; rIdx < rows.length; rIdx++) {
      const r = rows[rIdx]
      for (let cIdx = 1; cIdx < r.length; cIdx++) {
        const valStr = String(r[cIdx])
        const vDigits = valStr.replace(/[^\d.]/g, '')
        if (digits && vDigits && digits === vDigits) {
          bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
          break
        }
      }
      if (bestMatch) break
    }

    // 2. Prefix & scale heuristics
    if (!bestMatch) {
      for (let rIdx = 0; rIdx < rows.length; rIdx++) {
        const r = rows[rIdx]
        for (let cIdx = 1; cIdx < r.length; cIdx++) {
          const valStr = String(r[cIdx])
          const vDigits = valStr.replace(/[^\d.]/g, '')
          if (!digits || !vDigits) continue

          const dPfx = digits.replace('.', '').slice(0, 3)
          const vPfx = vDigits.replace('.', '').slice(0, 3)
          if (dPfx.length >= 2 && dPfx === vPfx) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if (digits.includes('214') && (vDigits.includes('214142') || vDigits.includes('214118') || valStr.includes('214'))) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if (digits === '63.5' && valStr.includes('63.5')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if (digits === '0.8' && String(r[0]).toUpperCase().includes('TOTAL ASSETS')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if ((digits === '90.5' || digits === '905') && vDigits.includes('905')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if ((digits === '1.50' || digits === '1.5') && vDigits.includes('1501')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if ((digits === '3.72' || digits === '3.7') && vDigits.includes('3718')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if ((digits === '10.4' || digits === '104') && vDigits.includes('104')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if ((digits === '17.0' || digits === '17') && vDigits.includes('1704')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if ((digits === '35.72' || digits === '35.7') && vDigits.includes('3572')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
          if ((digits === '28.71' || digits === '28.7') && vDigits.includes('2871')) {
            bestMatch = { row: rIdx, col: cIdx, val: valStr, account: r[0] }
            break
          }
        }
        if (bestMatch) break
      }
    }

    if (bestMatch) {
      tokens.push({
        type: 'ref',
        text: matchText,
        row: bestMatch.row,
        col: bestMatch.col,
        val: bestMatch.val,
        account: bestMatch.account
      })
    } else {
      tokens.push({ type: 'text', text: matchText })
    }
    lastIdx = end
  }

  if (lastIdx < note.length) {
    tokens.push({ type: 'text', text: note.slice(lastIdx) })
  }
  noteTokensCache.set(note, tokens)
  return tokens
}

const currentLecture = computed(() => {
  return modules.value.find(m => m.id === selectedWeekId.value) || modules.value[0]
})

const currentAssignment = computed(() => {
  return assignments.value.find(a => a.id === selectedAssignmentId.value) || assignments.value[0]
})

const currentPresSlide = computed(() => {
  return presentationSlides.value.find(s => s.slide_num === selectedPresSlideNum.value) || presentationSlides.value[0]
})

const filteredPresSlides = computed(() => {
  if (!searchQuery.value.trim()) return presentationSlides.value
  const q = searchQuery.value.toLowerCase()
  return presentationSlides.value.filter(s =>
    s.section_tag.toLowerCase().includes(q) ||
    s.title.toLowerCase().includes(q) ||
    s.subtitle.toLowerCase().includes(q)
  )
})

const getLectureSlideObj = (weekId, slideNum) => {
  const mod = modules.value.find(m => m.id === weekId)
  if (!mod || !mod.slides) return null
  return mod.slides.find(s => s.slide_num === slideNum) || null
}

const getLectureReportObj = (weekId, slideNum) => {
  if (lang.value === 'id') {
    const key = `${weekId}_${slideNum}`
    if (supportingTablesIdData.lecture_id && supportingTablesIdData.lecture_id[key]) {
      return supportingTablesIdData.lecture_id[key]
    }
  }
  return getLectureSlideObj(weekId, slideNum)?.goto_report || null
}

const getAssignmentObj = (asgId) => {
  return assignments.value.find(a => a.id === asgId) || null
}

const getWorkbookGrid = (asgId, sheetName) => {
  if (lang.value === 'id' && supportingTablesIdData.workbook_id?.[asgId]?.[sheetName]) {
    return supportingTablesIdData.workbook_id[asgId][sheetName]
  }
  const asg = getAssignmentObj(asgId)
  if (!asg || !asg.workbook || !sheetName || !asg.workbook[sheetName]) return null
  return asg.workbook[sheetName]
}

const normalizeHighlightTokens = (highlightTerms, fallbackKeywords) => {
  const raw = Array.isArray(highlightTerms) && highlightTerms.length
    ? highlightTerms
    : String(fallbackKeywords || '').split(/\s+/)
  const tokens = new Set()
  raw.forEach(item => {
    const clean = String(item || '').toLowerCase().trim()
    if (clean.length >= 2) tokens.add(clean)
    const stripped = clean.replace(/,/g, '')
    if (stripped.length >= 2) tokens.add(stripped)
  })
  return Array.from(tokens).filter(t => t.length >= 2 && !['rp', 'bn', 'sh', 'the', 'and', 'for', 'dan', 'untuk', 'yang', 'dari'].includes(t))
}

const isCellHighlighted = (cellVal, highlightTerms, fallbackKeywords) => {
  const s = String(cellVal ?? '').toLowerCase().trim()
  if (!s) return false
  const sFlat = s.replace(/,/g, '')
  const tokens = normalizeHighlightTokens(highlightTerms, fallbackKeywords)
  return tokens.some(t => {
    // Prevent "week 1" or "slide 1" from matching "week 14" or "slide 14"
    if (/\d$/.test(t)) {
      const escaped = t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      const re = new RegExp(`(?<![0-9])${escaped}(?![0-9])`)
      return re.test(s) || re.test(sFlat)
    }
    return s.includes(t) || sFlat.includes(t)
  })
}

const isRowHighlighted = (rowCells, highlightTerms, fallbackKeywords) => {
  if (!Array.isArray(rowCells)) return false
  return rowCells.some(c => isCellHighlighted(c, highlightTerms, fallbackKeywords))
}

const getSupportingWorkbookRows = (asgId, sheetName, highlightTerms, fallbackKeywords) => {
  const grid = getWorkbookGrid(asgId, sheetName)
  if (!grid) return []
  const nonEmpty = grid.filter(r => r && r.some(c => String(c || '').trim() !== ''))
  const trimmed = nonEmpty.map((r, idx) => {
    let lastNonEmpty = r.length - 1
    while (lastNonEmpty > 0 && String(r[lastNonEmpty] || '').trim() === '') {
      lastNonEmpty--
    }
    const cells = r.slice(0, Math.min(lastNonEmpty + 1, 6))
    const matched = idx > 2 && isRowHighlighted(cells, highlightTerms, fallbackKeywords)
    return { cells, matched, origIdx: idx }
  })
  const headerRows = trimmed.slice(0, 3)
  const hitRows = trimmed.slice(3).filter(r => r.matched)
  if (hitRows.length > 0) {
    const combined = [...headerRows, ...hitRows]
    if (combined.length < 8) {
      for (const r of trimmed.slice(3)) {
        if (!r.matched && combined.length < 8) combined.push(r)
      }
    }
    const uniqueByIdx = new Map()
    combined.forEach(r => uniqueByIdx.set(r.origIdx, r))
    return Array.from(uniqueByIdx.values()).sort((a, b) => a.origIdx - b.origIdx).slice(0, 14)
  }
  return trimmed.slice(0, 10)
}

const getWorkbookPreviewRows = (asgId, sheetName) => {
  const grid = getWorkbookGrid(asgId, sheetName)
  if (!grid) return []
  const nonEmpty = grid.filter(r => r && r.some(c => String(c || '').trim() !== ''))
  return nonEmpty.slice(0, 8).map(r => {
    let lastNonEmpty = r.length - 1
    while (lastNonEmpty > 0 && String(r[lastNonEmpty] || '').trim() === '') {
      lastNonEmpty--
    }
    return r.slice(0, Math.min(lastNonEmpty + 1, 6))
  })
}

const selectPresSlide = (num) => {
  selectedPresSlideNum.value = num
  activeTab.value = 'presentation'
  sidebarMode.value = 'presentation'
}

const prevPresSlide = () => {
  if (selectedPresSlideNum.value > 1) selectedPresSlideNum.value -= 1
}

const nextPresSlide = () => {
  if (selectedPresSlideNum.value < presentationSlides.value.length) selectedPresSlideNum.value += 1
}

const findItemTraces = (slide, searchText) => {
  if (!slide) return { matchedLectures: [], matchedAssignments: [] }
  const stopWords = new Set(['the', 'and', 'for', 'with', 'from', 'into', 'this', 'that', 'per', 'net', 'goto', 'base', 'case', 'fy2025', '2025'])
  const tokens = String(searchText || '')
    .toLowerCase()
    .replace(/[^a-z0-9.%]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 2 && !stopWords.has(w))

  const scoreTrace = (txt) => {
    const low = String(txt || '').toLowerCase()
    return tokens.reduce((acc, tk) => acc + (low.includes(tk) ? 1 : 0), 0)
  }

  const scoredLectures = (slide.lecture_traces || []).map(lt => ({
    ...lt,
    _score: scoreTrace(`${lt.week_label} ${lt.mapping_note}`)
  })).sort((a, b) => b._score - a._score)

  const scoredAsgs = (slide.assignment_traces || []).map(at => ({
    ...at,
    _score: scoreTrace(`${at.assignment_code} ${at.sheet_name} ${at.cell_or_section_ref} ${at.mapping_note} ${at.evidence_caption}`)
  })).sort((a, b) => b._score - a._score)

  return {
    matchedLectures: scoredLectures.some(x => x._score > 0) ? scoredLectures.filter(x => x._score > 0) : scoredLectures,
    matchedAssignments: scoredAsgs.some(x => x._score > 0) ? scoredAsgs.filter(x => x._score > 0) : scoredAsgs
  }
}

const buildPresItemPayload = (kind, item, idx = 0) => {
  const slide = currentPresSlide.value
  if (kind === 'kpi') {
    return {
      title: item.label,
      value: item.val,
      explanation: item.detail_explanation || (item.sub + ' - ' + slide.section_tag),
      detail_explanation: item.detail_explanation || (item.sub + ' - ' + slide.section_tag),
      formula: item.formula || '',
      calc_steps: item.calc_steps || [],
      data_origin: item.data_origin || '',
      highlight_terms: item.highlight_terms || [item.val, item.label],
      evidence_img: item.evidence_img || null,
      evidence_caption: item.evidence_caption || '',
      keywords: item.label + ' ' + item.val + ' ' + item.sub
    }
  }
  if (kind === 'row') {
    const rd = (slide.table && slide.table.row_details && slide.table.row_details[idx]) || {}
    return {
      title: item[0],
      value: item.slice(1).join(' | '),
      explanation: rd.detail_explanation || (slide.table ? slide.table.title : ''),
      detail_explanation: rd.detail_explanation || (slide.table ? slide.table.title : ''),
      formula: rd.formula || '',
      calc_steps: rd.calc_steps || [],
      data_origin: rd.data_origin || '',
      highlight_terms: rd.highlight_terms || item.slice(0, 3),
      evidence_img: rd.evidence_img || null,
      evidence_caption: rd.evidence_caption || '',
      keywords: item.join(' ')
    }
  }
  if (kind === 'card') {
    const bulletSummary = (item.bullets || []).map(b => b.bold + ' ' + b.text).join(' ')
    return {
      title: item.title,
      value: (item.bullets ? item.bullets.length : 0) + (lang.value === 'id' ? ' Poin Utama' : ' Key Points'),
      explanation: item.detail_explanation || bulletSummary,
      detail_explanation: item.detail_explanation || bulletSummary,
      formula: item.formula || '',
      calc_steps: item.calc_steps || [],
      data_origin: item.data_origin || '',
      highlight_terms: item.highlight_terms || (item.bullets || []).map(b => b.bold),
      evidence_img: item.evidence_img || null,
      evidence_caption: item.evidence_caption || '',
      keywords: item.title + ' ' + (item.bullets || []).map(b => b.bold).join(' ')
    }
  }
  // chart
  const cd = slide.chart_details || {}
  return {
    title: (lang.value === 'id' ? 'Grafik Analitis: ' : 'Analytical Chart: ') + slide.section_tag,
    value: uiText.value.slideWord + ' ' + slide.slide_num,
    explanation: cd.detail_explanation || slide.title,
    detail_explanation: cd.detail_explanation || slide.title,
    formula: cd.formula || '',
    calc_steps: cd.calc_steps || [],
    data_origin: cd.data_origin || '',
    highlight_terms: cd.highlight_terms || [],
    evidence_img: cd.evidence_img || null,
    evidence_caption: cd.evidence_caption || '',
    keywords: slide.title + ' ' + slide.subtitle
  }
}

const onPresItemClick = (event, payload) => {
  const x = Math.min(Math.max(event.clientX, 180), window.innerWidth - 180)
  const y = Math.max(event.clientY - 14, 110)
  clickPopup.value = {
    ...payload,
    x,
    y,
    slideNum: currentPresSlide.value.slide_num
  }
}

const onPresItemDblClick = (payload) => {
  clickPopup.value = null
  const searchTerms = Array.isArray(payload.highlight_terms) && payload.highlight_terms.length
    ? payload.highlight_terms.join(' ') + ' ' + (payload.keywords || '')
    : (payload.keywords || `${payload.title} ${payload.value || ''}`)
  const traces = findItemTraces(currentPresSlide.value, searchTerms)
  const fallbackEvImg = payload.evidence_img || traces.matchedAssignments.find(a => a.evidence_img)?.evidence_img || null
  const fallbackEvCap = payload.evidence_caption || traces.matchedAssignments.find(a => a.evidence_img)?.evidence_caption || ''
  detailDrawerItem.value = {
    ...payload,
    evidence_img: fallbackEvImg,
    evidence_caption: fallbackEvCap,
    slide: currentPresSlide.value,
    ...traces
  }
}

const closeClickPopup = () => {
  clickPopup.value = null
}

const handlePresentKeydown = (e) => {
  if (e.key === 'Escape') {
    if (clickPopup.value) {
      clickPopup.value = null
      return
    }
    if (detailDrawerItem.value) {
      detailDrawerItem.value = null
      return
    }
    if (isPresentMode.value) {
      isPresentMode.value = false
      return
    }
  }
  if (!isPresentMode.value) return
  if (e.key === 'ArrowLeft') {
    e.preventDefault()
    clickPopup.value = null
    prevPresSlide()
  } else if (e.key === 'ArrowRight') {
    e.preventDefault()
    clickPopup.value = null
    nextPresSlide()
  }
}

watch(selectedPresSlideNum, () => {
  clickPopup.value = null
})

onMounted(() => {
  window.addEventListener('keydown', handlePresentKeydown)
  window.addEventListener('click', closeClickPopup)
})
onUnmounted(() => {
  window.removeEventListener('keydown', handlePresentKeydown)
  window.removeEventListener('click', closeClickPopup)
})

const jumpToLectureSlide = (weekId, slideNum) => {
  selectedWeekId.value = weekId
  activeTab.value = 'slides'
  sidebarMode.value = 'slides'
  nextTick(() => {
    const el = document.getElementById(`lecture-slide-${weekId}-${slideNum}`)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

const jumpToAssignmentSheet = (asgId, sheetName) => {
  selectAssignment(asgId)
  if (sheetName) {
    nextTick(() => {
      selectedWorkbookSheet.value = sheetName
    })
  }
}

const filteredModules = computed(() => {
  if (!searchQuery.value.trim()) return modules.value
  const q = searchQuery.value.toLowerCase()
  return modules.value.filter(m => 
    m.week.toLowerCase().includes(q) ||
    m.title.toLowerCase().includes(q) ||
    m.category.toLowerCase().includes(q) ||
    m.core_question.toLowerCase().includes(q)
  )
})

const filteredAssignments = computed(() => {
  if (!searchQuery.value.trim()) return assignments.value
  const q = searchQuery.value.toLowerCase()
  return assignments.value.filter(a => 
    a.title.toLowerCase().includes(q) ||
    a.code.toLowerCase().includes(q) ||
    a.summary.toLowerCase().includes(q)
  )
})

watch(activeTab, (newTab) => {
  if (newTab === 'assignments') {
    sidebarMode.value = 'assignments'
  } else if (newTab === 'slides') {
    sidebarMode.value = 'slides'
  } else if (newTab === 'presentation') {
    sidebarMode.value = 'presentation'
  }
})

watch(selectedWeekId, (newWeek) => {
  if (newWeek === 'week4') {
    activeFormulaCell.value = {
      ref: 'C6',
      formula: '= C2 - C5  (Operating Cash Flow Rp 307.0 bn - Capex Rp 1,182.4 bn = -(Rp 875.3 bn))',
      val: '(875.3)',
      sources: ['C2', 'C5']
    }
  } else if (newWeek === 'week3') {
    activeFormulaCell.value = {
      ref: 'C2',
      formula: '= B2 + Surplus  (Rp 19.67 bn + Rp 55.08 bn Revaluation = Rp 70.36 bn)',
      val: '70.36',
      sources: ['B2']
    }
  } else if (newWeek === 'week2') {
    activeFormulaCell.value = {
      ref: 'D4',
      formula: '= D2 - D3  (Gross Revenue Rp 18,322.2 bn - COGS Rp 7,746.2 bn)',
      val: '10,576.0',
      sources: ['D2', 'D3']
    }
  }
})

const selectWeek = (id) => {
  selectedWeekId.value = id
  activeTab.value = 'slides'
  sidebarMode.value = 'slides'
}

const selectAssignment = (id) => {
  selectedAssignmentId.value = id
  activeTab.value = 'assignments'
  sidebarMode.value = 'assignments'
  const a = assignments.value.find(item => item.id === id)
  if (a && a.workbook) {
    selectedWorkbookSheet.value = Object.keys(a.workbook)[0] || ''
  } else {
    selectedWorkbookSheet.value = ''
  }
}

// Initialize sheet for m2 if loaded
if (currentAssignment.value && currentAssignment.value.workbook) {
  selectedWorkbookSheet.value = Object.keys(currentAssignment.value.workbook)[0] || ''
}

const scrollToAsgSection = (elId) => {
  const el = document.getElementById(elId)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const getWbRowClass = (row, rIdx) => {
  if (!row || row.length === 0) return ''
  const first = String(row[0] ?? '').trim()
  const low = first.toLowerCase()
  const nonEmptyCols = row.filter(c => String(c ?? '').trim() !== '').length
  if (rIdx === 0) return 'wb-title-banner-row'
  if (
    rIdx === 2 ||
    low === 'line item' ||
    low === 'pos laporan keuangan' ||
    low === 'komponen' ||
    low === 'input / result' ||
    low === 'input / hasil' ||
    low.startsWith('ratio') ||
    low.startsWith('rasio') ||
    low.startsWith('valuation methodology') ||
    low.startsWith('metode valuasi') ||
    low.startsWith('comparable company') ||
    low.startsWith('perusahaan pembanding') ||
    low.startsWith('pro forma') ||
    low.startsWith('projection driver') ||
    low.startsWith('penggerak proyeksi') ||
    low.startsWith('metric') ||
    low.startsWith('metrik') ||
    low.startsWith('key financial item') ||
    low.startsWith('pos keuangan utama') ||
    low.startsWith('component') ||
    low.startsWith('section') ||
    low.startsWith('bagian') ||
    low.startsWith('step / tab') ||
    low.startsWith('langkah / sheet')
  ) {
    return 'wb-col-header-row'
  }
  if (
    nonEmptyCols === 1 &&
    first.length > 0 &&
    (first === first.toUpperCase() || low.startsWith('case') || low.startsWith('skenario') || low.startsWith('base case') || low.startsWith('step ') || low.startsWith('langkah '))
  ) {
    return 'wb-section-divider-row'
  }
  if (
    low.includes('total') ||
    low.includes('gross profit') ||
    low.includes('laba kotor') ||
    low.includes('ebit') ||
    low.includes('net income') ||
    low.includes('laba / (rugi) bersih') ||
    low.includes('enterprise value') ||
    low.includes('nilai perusahaan') ||
    low.includes('equity value') ||
    low.includes('nilai ekuitas') ||
    low.includes('value per share') ||
    low.includes('nilai per saham') ||
    low.includes('cost of equity') ||
    low.includes('biaya ekuitas') ||
    low === 'wacc' ||
    low.startsWith('wacc ') ||
    low.startsWith('blended') ||
    low.startsWith('rata-rata tertimbang') ||
    low.startsWith('balance check') ||
    low.startsWith('uji keseimbangan') ||
    low.includes('return on equity') ||
    low.includes('altman z') ||
    low.includes('free cash flow') ||
    low.includes('arus kas bebas') ||
    low.includes('ending cash') ||
    low.includes('kas akhir')
  ) {
    return 'wb-total-row'
  }
  return ''
}

const getSecTableRowClass = (row) => {
  if (!row || row.length === 0) return ''
  const first = String(row[0] ?? '').trim()
  const low = first.toLowerCase()
  const trailingNonEmpty = row.slice(1).filter(c => String(c ?? '').trim() !== '').length
  if (trailingNonEmpty === 0 && first.length > 0) {
    return 'fin-subheader-row'
  }
  if (
    low.includes('total') ||
    low.includes('subtotal') ||
    low.includes('net investing') ||
    low.includes('investasi bersih') ||
    low.includes('excluding time deposits') ||
    low.includes('tanpa deposito') ||
    low.includes('balance check') ||
    low.includes('uji keseimbangan') ||
    low.includes('enterprise value') ||
    low.includes('nilai perusahaan') ||
    low.includes('equity value') ||
    low.includes('nilai ekuitas') ||
    low.includes('implied') ||
    low.includes('nilai per saham') ||
    low.includes('ebit') ||
    low.includes('net income') ||
    low.includes('laba bersih') ||
    low.includes('rugi bersih') ||
    low.includes('wacc') ||
    low.includes('overall') ||
    low.includes('keseluruhan') ||
    low.includes('concluded') ||
    low.includes('kesimpulan') ||
    low.includes('net cash') ||
    low.includes('kas bersih')
  ) {
    return 'fin-total-row'
  }
  if (
    low.includes('ratio') ||
    low.includes('rasio') ||
    low.includes('margin') ||
    low.includes('marjin') ||
    low.includes('divided by') ||
    low.includes('dibagi') ||
    low.includes('breakeven') ||
    low.includes('impas') ||
    low.includes('roe') ||
    low.includes('roa') ||
    low.includes('z\'\'-score') ||
    low.includes('status') ||
    low.includes('rekomendasi') ||
    low.includes('stance')
  ) {
    return 'fin-ratio-row'
  }
  return ''
}

const getCellClass = (val, cIdx) => {
  if (cIdx === 0) return 'bold-cell'
  const s = String(val ?? '').trim()
  if (!s) return ''
  const strippedUnits = s.replace(/\b(juta|miliar|triliun|billion|million|trillion|hari|days|yrs|thn|sh|lbr|rp|usd|bn|mn)\b/gi, '')
  const looksNumeric =
    s === 'N/M' ||
    s === '-' ||
    (/\d/.test(s) && s.length <= 26 && !/[a-z]{4,}/i.test(strippedUnits))
  const classes = [looksNumeric ? 'num-cell' : 'text-data-cell']
  const isNegVal =
    /^\([\d\.,]+%?\)$/.test(s) ||
    /^-\([\d\.,]+/.test(s) ||
    /^-[\d\.,]+/.test(s) ||
    /^-Rp\s*[\d\.,]+/i.test(s) ||
    /^Rp\s*\([\d\.,]+/i.test(s)
  if (isNegVal && !s.toLowerCase().includes('step')) {
    classes.push('neg-val-cell')
  } else if (/^\+[\d\.,]+[%x]?$/.test(s)) {
    classes.push('pos-growth-cell')
  }
  return classes.join(' ')
}

const isColNumeric = (tbl, cIdx) => {
  if (!tbl || tbl.length <= 1 || cIdx === 0) return false
  const rows = tbl.slice(1)
  let numHits = 0
  let nonEmpty = 0
  for (const r of rows) {
    const v = String(r[cIdx] ?? '').trim()
    if (!v) continue
    nonEmpty++
    if (getCellClass(v, cIdx).includes('num-cell')) numHits++
  }
  return nonEmpty > 0 && numHits >= Math.ceil(nonEmpty * 0.5)
}
</script>

<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="brand">
        <div class="logo-wrap">
          <img src="/goto_logo.png" alt="GoTo Logo" class="brand-logo" />
        </div>
        <div class="brand-text">
          <h2>FSA MASTER</h2>
          <p>{{ uiText.brandSub }}</p>
        </div>
      </div>

      <!-- Language Switcher (Positioned above search input box) -->
      <div class="lang-switcher-row" role="group" aria-label="Language Switcher">
        <button
          type="button"
          :class="['lang-btn', { active: lang === 'en' }]"
          @click="lang = 'en'"
        >
          English (EN)
        </button>
        <button
          type="button"
          :class="['lang-btn', { active: lang === 'id' }]"
          @click="lang = 'id'"
        >
          Indonesia (ID)
        </button>
      </div>

      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          :placeholder="sidebarMode === 'assignments' ? uiText.searchTasksPlaceholder : (sidebarMode === 'presentation' ? uiText.searchDeckPlaceholder : uiText.searchSlidesPlaceholder)" 
        />
      </div>

      <!-- Top Switcher Menu for Final Deck / Slides / Assignments -->
      <div class="sidebar-top-switcher">
        <button 
          :class="['sidebar-switch-btn pres-switch', { active: sidebarMode === 'presentation' }]"
          @click="sidebarMode = 'presentation'; activeTab = 'presentation'"
        >
          <span>{{ uiText.switchDeck }}</span>
          <span class="switcher-badge">14</span>
        </button>

        <button 
          :class="['sidebar-switch-btn slides-switch', { active: sidebarMode === 'slides' }]"
          @click="sidebarMode = 'slides'; activeTab = 'slides'"
        >
          <span>{{ uiText.switchSlides }}</span>
          <span class="switcher-badge">12</span>
        </button>

        <button 
          :class="['sidebar-switch-btn asg-switch', { active: sidebarMode === 'assignments' }]"
          @click="sidebarMode = 'assignments'; activeTab = 'assignments'"
        >
          <span>{{ uiText.switchTasks }}</span>
          <span class="switcher-badge">7</span>
        </button>
      </div>

      <div class="lecture-nav">
        <!-- Final Web Presentation Deck Section (Shown when sidebarMode === 'presentation') -->
        <div v-if="sidebarMode === 'presentation'">
          <div class="nav-section-label">{{ uiText.deckSectionLabel }} ({{ filteredPresSlides.length }} {{ uiText.slidesSuffix }})</div>
          <div 
            v-for="ps in filteredPresSlides" 
            :key="ps.slide_num"
            :class="['nav-item pres-nav-item', { active: activeTab === 'presentation' && selectedPresSlideNum === ps.slide_num }]"
            @click="selectPresSlide(ps.slide_num)"
          >
            <div class="nav-item-top">
              <span :class="['week-badge', ps.is_appendix ? 'apx-badge' : 'pres-badge']">
                {{ ps.is_appendix ? uiText.apxWord + ' ' + ps.slide_num : uiText.slideWord.toUpperCase() + ' ' + ps.slide_num }}
              </span>
              <span class="slide-count-badge">
                L:{{ ps.lecture_traces.length }} | A:{{ ps.assignment_traces.length }}
              </span>
            </div>
            <div class="nav-item-title">{{ ps.title }}</div>
            <div class="category-tag">{{ ps.section_tag }}</div>
          </div>
        </div>

        <!-- Lecture Slides Section (Shown when sidebarMode === 'slides') -->
        <div v-if="sidebarMode === 'slides'">
          <div class="nav-section-label">{{ uiText.lectureSectionLabel }}</div>
          <div 
            v-for="item in filteredModules" 
            :key="item.id"
            :class="['nav-item', { active: activeTab === 'slides' && selectedWeekId === item.id }]"
            @click="selectWeek(item.id)"
          >
            <div class="nav-item-top">
              <span class="week-badge">{{ item.week }}</span>
              <span class="slide-count-badge">{{ item.slides.length }} {{ uiText.slidesWord }}</span>
            </div>
            <div class="nav-item-title">{{ item.title }}</div>
            <div class="category-tag">{{ item.category }}</div>
          </div>
        </div>

        <!-- Assignments Section (Shown when sidebarMode === 'assignments') -->
        <div v-if="sidebarMode === 'assignments'">
          <div class="nav-section-label">{{ uiText.tasksSectionLabel }}</div>
          <div 
            v-for="a in filteredAssignments" 
            :key="a.id"
            :class="['nav-item assignment-nav-item', { active: activeTab === 'assignments' && selectedAssignmentId === a.id }]"
            @click="selectAssignment(a.id)"
          >
            <div class="nav-item-top">
              <span class="week-badge asg-badge">{{ a.code }}</span>
              <span class="slide-count-badge">{{ a.week }}</span>
            </div>
            <div class="nav-item-title">{{ a.title }}</div>
          </div>
        </div>
      </div>

      <div class="sidebar-footer">
        <div class="group-info">
          <span>Group 4 (GOTO)</span>
          <p>Fagly Ramschie • Anggreini Ruitan • Galatia Rompas</p>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="content-area">
      <!-- Sleek Top Header Navigation -->
      <header class="top-nav">
        <!-- Left: Crisp Breadcrumb Pill -->
        <div class="header-left">
          <div class="breadcrumb-container">
            <span :class="['context-badge', activeTab === 'assignments' ? 'asg-badge-pill' : (activeTab === 'presentation' ? 'pres-badge-pill' : 'week-badge-pill')]">
              {{ activeTab === 'assignments' ? currentAssignment.code : (activeTab === 'presentation' ? (uiText.slideWord + ' ' + currentPresSlide.slide_num + ' / ' + presentationSlides.length) : currentLecture.week) }}
            </span>
            <span class="crumb-separator">/</span>
            <span class="crumb-topic">
              {{ activeTab === 'assignments' ? currentAssignment.folder : (activeTab === 'presentation' ? currentPresSlide.section_tag : currentLecture.category) }}
            </span>
          </div>
        </div>

        <!-- Center: Contextual Sub-Navigation (Changes based on Active Left Sidebar Mode) -->
        <div class="header-center">
          <!-- Mode 1: Lecture Weeks Sub-Views (Slides / Financials / Takeaways / Roadmap) -->
          <nav v-if="sidebarMode === 'slides'" class="segmented-control" aria-label="Lecture Week Sub-Views">
            <button 
              :class="['segmented-btn', { active: activeTab === 'slides' }]" 
              @click="activeTab = 'slides'"
              title="Lecture Slides & Theory Analysis"
            >
              <svg class="tab-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="3" width="20" height="14" rx="2"/>
                <line x1="8" y1="21" x2="16" y2="21"/>
                <line x1="12" y1="17" x2="12" y2="21"/>
              </svg>
              <span>{{ uiText.visualSlides }}</span>
            </button>

            <button 
              :class="['segmented-btn', { active: activeTab === 'goto' }]" 
              @click="activeTab = 'goto'"
              title="GoTo Empirical Financial Models for this Week"
            >
              <svg class="tab-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 3v18h18"/>
                <path d="m19 9-5 5-4-4-3 3"/>
              </svg>
              <span>{{ uiText.financials }}</span>
            </button>

            <button 
              :class="['segmented-btn', { active: activeTab === 'flashcards' }]" 
              @click="activeTab = 'flashcards'"
              title="Core Key Takeaways for this Week"
            >
              <svg class="tab-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
              </svg>
              <span>{{ uiText.takeaways }}</span>
            </button>

            <button 
              :class="['segmented-btn', { active: activeTab === 'roadmap' }]" 
              @click="activeTab = 'roadmap'"
              title="16-Week FSA Curriculum Roadmap"
            >
              <svg class="tab-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/>
                <line x1="8" y1="2" x2="8" y2="18"/>
                <line x1="16" y1="6" x2="16" y2="22"/>
              </svg>
              <span>{{ uiText.roadmap }}</span>
            </button>
          </nav>

          <!-- Mode 2: Final Presentation Mode -->
          <div v-else-if="sidebarMode === 'presentation'" class="mode-context-pill pres-context">
            <span class="mode-dot pres-dot"></span>
            <span>{{ uiText.presContextPill }}</span>
          </div>

          <!-- Mode 3: Assignments Mode -->
          <div v-else-if="sidebarMode === 'assignments'" class="mode-context-pill asg-context">
            <span class="mode-dot asg-dot"></span>
            <span>{{ uiText.asgContextPill }} • {{ currentAssignment.week }}</span>
          </div>
        </div>

        <!-- Right: Status / Context Indicator -->
        <div class="header-right">
          <div class="ticker-badge" title="Audited Financial Statements FY2025">
            <span class="ticker-dot"></span>
            <span class="ticker-name">IDX: GOTO</span>
            <span class="ticker-divider"></span>
            <span class="ticker-audit">FY2025</span>
          </div>
        </div>
      </header>

      <!-- Main Body Container -->
      <div class="scroll-container">

        <!-- ================= TAB 0: INTERACTIVE WEB PRESENTATION (ASSIGNMENT 16) ================= -->
        <div v-if="activeTab === 'presentation'" class="tab-pane pres-tab-pane">
          <!-- Slide Control Bar -->
          <div class="pres-controls-bar">
            <div class="pres-nav-buttons">
              <button class="pres-nav-btn" :disabled="selectedPresSlideNum <= 1" @click="prevPresSlide">
                &larr; {{ uiText.prevBtn }}
              </button>
              <span class="pres-counter-pill">
                {{ uiText.slideWord }} {{ currentPresSlide.slide_num }} {{ uiText.ofWord }} {{ presentationSlides.length }}
              </span>
              <button class="pres-nav-btn" :disabled="selectedPresSlideNum >= presentationSlides.length" @click="nextPresSlide">
                {{ uiText.nextBtn }} &rarr;
              </button>
            </div>

            <div class="pres-slide-strip">
              <button
                v-for="ps in presentationSlides"
                :key="ps.slide_num"
                :class="['pres-dot-btn', { active: ps.slide_num === selectedPresSlideNum, apx: ps.is_appendix }]"
                @click="selectPresSlide(ps.slide_num)"
                :title="ps.section_tag + ': ' + ps.title"
              >
                {{ ps.is_appendix ? 'A' + (ps.slide_num - 11) : ps.slide_num }}
              </button>
            </div>

            <div class="pres-meta-pills">
              <span class="pres-time-badge">⏱ {{ currentPresSlide.time_budget }}</span>
              <span class="pres-pts-badge">🏆 {{ currentPresSlide.rubric_points }}</span>
              <button class="pres-present-btn" @click="isPresentMode = true" :title="uiText.presentTitle">
                ▶ {{ uiText.presentBtn }}
              </button>
            </div>
          </div>

          <!-- 16:9 Web PowerPoint Canvas -->
          <section class="pres-canvas">
            <div class="pres-slide-header">
              <div class="pres-header-top-row">
                <span class="pres-section-tag">{{ currentPresSlide.section_tag }}</span>
                <span class="pres-slide-index">{{ currentPresSlide.is_appendix ? uiText.appendixWord : uiText.mainDeckWord }} | {{ uiText.slideWord.toUpperCase() }} {{ currentPresSlide.slide_num }} / {{ presentationSlides.length }}</span>
              </div>
              <h1 class="pres-action-title">{{ currentPresSlide.title }}</h1>
              <p class="pres-slide-subtitle">{{ currentPresSlide.subtitle }}</p>
            </div>
            <div class="pres-emerald-bar"></div>

            <div class="pres-slide-body">
              <!-- KPI Row -->
              <div v-if="currentPresSlide.kpis && currentPresSlide.kpis.length" class="pres-kpi-grid">
                <div
                  v-for="(k, kIdx) in currentPresSlide.kpis"
                  :key="kIdx"
                  :class="['pres-kpi-card pres-interactive-item', 'tone-' + k.tone]"
                  @click.stop="onPresItemClick($event, buildPresItemPayload('kpi', k))"
                  @dblclick.stop="onPresItemDblClick(buildPresItemPayload('kpi', k))"
                  title="Click to explain | Double-click for full source drawer"
                >
                  <div class="pres-kpi-val">{{ k.val }}</div>
                  <div class="pres-kpi-lbl">{{ k.label }}</div>
                  <div class="pres-kpi-sub">{{ k.sub }}</div>
                </div>
              </div>

              <!-- Main Content Split (Chart / Table / Cards) -->
              <div class="pres-content-grid">
                <!-- Chart Panel if Present -->
                <div
                  v-if="currentPresSlide.chart_url"
                  class="pres-chart-card pres-interactive-item"
                  @click.stop="onPresItemClick($event, buildPresItemPayload('chart', currentPresSlide))"
                  @dblclick.stop="onPresItemDblClick(buildPresItemPayload('chart', currentPresSlide))"
                  title="Click to explain | Double-click for full source drawer"
                >
                  <div class="pres-chart-toolbar">
                    <span class="pres-chart-badge">HIGH-RES ANALYTICAL CHART (DOUBLE-CLICK IMAGE TO ZOOM)</span>
                  </div>
                  <img
                    :src="currentPresSlide.chart_url"
                    :alt="currentPresSlide.title"
                    class="pres-chart-img"
                    @dblclick.stop="openLightbox(currentPresSlide.chart_url, currentPresSlide.title, currentPresSlide.source_footer)"
                  />
                </div>

                <!-- Structured Financial Table if Present -->
                <div v-if="currentPresSlide.table" class="pres-table-card">
                  <div class="pres-table-title">{{ currentPresSlide.table.title }}</div>
                  <div class="wb-table-wrap">
                    <table class="data-table pres-data-table">
                      <thead>
                        <tr>
                          <th v-for="(th, hIdx) in currentPresSlide.table.headers" :key="hIdx">{{ th }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(rVals, rIdx) in currentPresSlide.table.rows"
                          :key="rIdx"
                          class="pres-interactive-row"
                          @click.stop="onPresItemClick($event, buildPresItemPayload('row', rVals, rIdx))"
                          @dblclick.stop="onPresItemDblClick(buildPresItemPayload('row', rVals, rIdx))"
                          title="Click to explain | Double-click for full source drawer"
                        >
                          <td v-for="(val, cIdx) in rVals" :key="cIdx" :class="{ 'bold-cell': cIdx === 0, 'num-cell': cIdx > 0 }">
                            {{ val }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <!-- Analytical Cards -->
                <div v-if="currentPresSlide.cards && currentPresSlide.cards.length" class="pres-cards-col">
                  <div
                    v-for="(card, cIdx) in currentPresSlide.cards"
                    :key="cIdx"
                    :class="['pres-info-card pres-interactive-item', 'card-tone-' + card.tone]"
                    @click.stop="onPresItemClick($event, buildPresItemPayload('card', card))"
                    @dblclick.stop="onPresItemDblClick(buildPresItemPayload('card', card))"
                    title="Click to explain | Double-click for full source drawer"
                  >
                    <h3 class="pres-card-title">{{ card.title }}</h3>
                    <ul class="pres-card-bullets">
                      <li v-for="(b, bIdx) in card.bullets" :key="bIdx">
                        <strong>{{ b.bold }}</strong> {{ b.text }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div class="pres-slide-footer">
              <span>Group 4 (Fagly Ramschie) | IDX: GOTO</span>
              <span>{{ uiText.sourceLabel }} {{ currentPresSlide.source_footer }}</span>
            </div>
          </section>

          <!-- ================= BOTTOM REVEAL CONTROLS (SPEAKER SCRIPT & AUDIT DRAWER) ================= -->
          <div class="pres-bottom-reveal-bar">
            <button
              v-if="currentPresSlide.speaker_notes"
              :class="['pres-reveal-btn speaker-reveal', { active: showSpeakerNotes }]"
              @click="showSpeakerNotes = !showSpeakerNotes"
            >
              <span>🎤 {{ showSpeakerNotes ? uiText.hideSpeaker : uiText.showSpeaker }}</span>
              <span class="reveal-sub-pill">{{ currentPresSlide.time_budget }}</span>
            </button>

            <button
              :class="['pres-reveal-btn audit-reveal', { active: showAuditDrawer }]"
              @click="showAuditDrawer = !showAuditDrawer"
            >
              <span>🔍 {{ showAuditDrawer ? uiText.hideAudit : uiText.showAudit }}</span>
              <span class="reveal-sub-pill">L:{{ currentPresSlide.lecture_traces.length }} | A:{{ currentPresSlide.assignment_traces.length }}</span>
            </button>
          </div>

          <!-- Speaker Notes Bar (Revealed on Click) -->
          <div v-if="showSpeakerNotes && currentPresSlide.speaker_notes" class="pres-speaker-box">
            <span class="speaker-tag">🎤 {{ uiText.speakerTag }} ({{ currentPresSlide.time_budget }}):</span>
            <p>{{ currentPresSlide.speaker_notes }}</p>
          </div>

          <!-- ================= DUAL SOURCE-OF-TRUTH AUDIT DRAWER (Revealed on Click) ================= -->
          <div v-if="showAuditDrawer" class="audit-drawer-wrapper">
            <div class="traceability-banner">
              <div class="trace-banner-title">
                <span class="drawer-scope-tag">{{ uiText.auditScopeTag }} {{ currentPresSlide.slide_num }}</span>
                <h2>{{ uiText.auditTitlePrefix }} {{ currentPresSlide.slide_num }}</h2>
                <p>{{ uiText.auditDescPrefix }} {{ currentPresSlide.slide_num }} {{ uiText.auditDescMid }}</p>
              </div>
            </div>

            <div class="traceability-columns">
            <!-- LEFT COLUMN: WHERE THIS BELONGS ON LECTURE SLIDES -->
            <div class="trace-col trace-lecture-col">
              <div class="trace-col-header lecture-hdr">
                <span class="trace-col-icon">🖥️</span>
                <div>
                  <h3>{{ uiText.lectureColTitle }}</h3>
                  <p>{{ currentPresSlide.lecture_traces.length }} {{ uiText.lectureColSub }}</p>
                </div>
              </div>

              <div v-for="(lt, ltIdx) in currentPresSlide.lecture_traces" :key="ltIdx" class="trace-item-card">
                <div class="trace-item-top">
                  <span class="trace-pill lecture-pill">{{ lt.week_label }} | {{ uiText.slideWord }} {{ lt.slide_num }}</span>
                  <button class="trace-jump-btn lecture-jump" @click="jumpToLectureSlide(lt.week_id, lt.slide_num)">
                    {{ uiText.openWord }} {{ lt.week_label }} {{ uiText.slideWord }} {{ lt.slide_num }} &rarr;
                  </button>
                </div>

                <div v-if="lt.trace_role" class="trace-role-badge lecture-role">{{ lt.trace_role }}</div>
                <p class="trace-mapping-note">{{ lt.mapping_note }}</p>

                <template v-if="getLectureSlideObj(lt.week_id, lt.slide_num)">
                  <div class="trace-slide-meta">
                    <strong>{{ getLectureSlideObj(lt.week_id, lt.slide_num).header }}</strong>
                    <span v-if="getLectureSlideObj(lt.week_id, lt.slide_num).subtitle"> - {{ getLectureSlideObj(lt.week_id, lt.slide_num).subtitle }}</span>
                  </div>

                  <div class="trace-thumb-row">
                    <img
                      :src="getLectureSlideObj(lt.week_id, lt.slide_num).image_url"
                      :alt="lt.week_label + ' Slide ' + lt.slide_num"
                      class="trace-slide-thumb"
                      @click="openLightbox(getLectureSlideObj(lt.week_id, lt.slide_num).image_url, lt.week_label + ' - Slide ' + lt.slide_num, lt.mapping_note)"
                    />
                  </div>

                  <!-- Live Pull of Lecture Slide's GoTo Table -->
                  <div v-if="getLectureReportObj(lt.week_id, lt.slide_num)?.table_rows" class="trace-mini-table-wrap">
                    <div class="trace-mini-title">
                      {{ uiText.liveExtract }} {{ getLectureReportObj(lt.week_id, lt.slide_num).title }}
                    </div>
                    <table class="data-table trace-mini-table">
                      <thead>
                        <tr>
                          <th v-for="(th, hIdx) in getLectureReportObj(lt.week_id, lt.slide_num).table_headers" :key="hIdx">{{ th }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(row, rIdx) in getLectureReportObj(lt.week_id, lt.slide_num).table_rows.slice(0, 6)" :key="rIdx">
                          <td v-for="(cell, cIdx) in row" :key="cIdx" :class="{ 'bold-cell': cIdx === 0 }">{{ cell }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </template>
              </div>
            </div>

            <!-- RIGHT COLUMN: WHERE THIS BELONGS ON ASSIGNMENTS & AUDITED FILINGS -->
            <div class="trace-col trace-asg-col">
              <div class="trace-col-header asg-hdr">
                <span class="trace-col-icon">📊</span>
                <div>
                  <h3>{{ uiText.asgColTitle }}</h3>
                  <p>{{ currentPresSlide.assignment_traces.length }} {{ uiText.asgColSub }}</p>
                </div>
              </div>

              <div v-for="(at, atIdx) in currentPresSlide.assignment_traces" :key="atIdx" class="trace-item-card">
                <div class="trace-item-top">
                  <span class="trace-pill asg-pill">{{ at.assignment_code }}</span>
                  <button class="trace-jump-btn asg-jump" @click="jumpToAssignmentSheet(at.assignment_id, at.sheet_name)">
                    {{ uiText.openWord }} {{ at.sheet_name || at.assignment_code }} &rarr;
                  </button>
                </div>

                <div v-if="at.trace_role" class="trace-role-badge asg-role">{{ at.trace_role }}</div>
                <div class="trace-cell-ref">
                  <strong>{{ uiText.locationLabel }}</strong> <code>{{ at.cell_or_section_ref }}</code>
                </div>
                <p class="trace-mapping-note">{{ at.mapping_note }}</p>

                <!-- Live Workbook Grid Preview if sheet_name exists -->
                <div v-if="at.sheet_name && getWorkbookPreviewRows(at.assignment_id, at.sheet_name).length" class="trace-mini-table-wrap">
                  <div class="trace-mini-title">
                    {{ uiText.liveExcelPreview }} '{{ at.sheet_name }}' ({{ getAssignmentObj(at.assignment_id)?.xlsx_file }})
                  </div>
                  <table class="data-table trace-mini-table">
                    <tbody>
                      <tr v-for="(wbRow, wrIdx) in getWorkbookPreviewRows(at.assignment_id, at.sheet_name)" :key="wrIdx" :class="{ 'trace-wb-hdr': wrIdx === 0 || wrIdx === 2 }">
                        <td v-for="(wbCell, wcIdx) in wbRow" :key="wcIdx" :class="{ 'bold-cell': wcIdx === 0 }">{{ wbCell }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <!-- Audited IDX Financial Statement Proof -->
                <div v-if="at.evidence_img" class="trace-evidence-box">
                  <div class="trace-ev-label">
                    <span>🔍 {{ uiText.auditedProofLabel }}</span> {{ at.evidence_caption }}
                  </div>
                  <img
                    :src="at.evidence_img"
                    :alt="at.evidence_caption"
                    class="trace-ev-thumb"
                    @click="openLightbox(at.evidence_img, at.assignment_code + ' - ' + at.cell_or_section_ref, at.evidence_caption)"
                  />
                </div>
              </div>
            </div>
          </div>
          </div>
        </div>

        <!-- ================= TAB: FULL ASSIGNMENTS VIEWER (INTERACTIVE) ================= -->
        <div v-if="activeTab === 'assignments'" class="tab-pane">
          <div class="hero-banner asg-hero-banner">
            <div class="hero-header-row">
              <span class="hero-tag asg-hero-tag">{{ currentAssignment.code }} • {{ currentAssignment.folder }}</span>
              <span class="hero-reading">📅 {{ currentAssignment.week }}</span>
            </div>
            <h1 class="hero-title">{{ currentAssignment.title }}</h1>
            <p class="goto-subtitle">{{ currentAssignment.summary }}</p>
            <div class="asg-kpi-badges-row">
              <span class="asg-kpi-pill">
                📑 {{ currentAssignment.sections.length }} {{ uiText.asgSectionsBadge }}
              </span>
              <span class="asg-kpi-pill">
                📋 {{ currentAssignment.sections.reduce((acc, s) => acc + (s.tables ? s.tables.length : 0), 0) }} {{ uiText.asgTablesBadge }}
              </span>
              <span v-if="currentAssignment.workbook" class="asg-kpi-pill asg-kpi-pill-green">
                📊 {{ Object.keys(currentAssignment.workbook).length }} {{ uiText.asgSheetsBadge }}
              </span>
              <span v-if="currentAssignment.docx_file" class="asg-kpi-pill asg-kpi-pill-muted">
                📄 {{ currentAssignment.docx_file }}
              </span>
            </div>
          </div>

          <!-- Top Horizontal Slide Menu for Assignments -->
          <div class="asg-top-slide-container">
            <div class="asg-slide-track">
              <button 
                v-for="a in assignments" 
                :key="a.id"
                :class="['asg-slide-card', { active: selectedAssignmentId === a.id }]"
                @click="selectAssignment(a.id)"
              >
                <div class="slide-card-top">
                  <span class="slide-card-code">{{ a.code }}</span>
                  <span class="slide-card-week">{{ a.week }}</span>
                </div>
                <div class="slide-card-title">{{ a.title }}</div>
              </button>
            </div>
          </div>

          <!-- Section Quick-Jump Navigation Bar -->
          <div class="asg-sec-toc-bar">
            <span class="asg-toc-label">{{ uiText.asgQuickJumpLabel }}</span>
            <button
              v-if="currentAssignment.workbook"
              class="asg-toc-btn asg-toc-wb-btn"
              @click="scrollToAsgSection('asg-workbook-anchor')"
            >
              📊 {{ uiText.asgWorkbookBtn }}
            </button>
            <button
              v-for="(sec, sIdx) in currentAssignment.sections"
              :key="'toc-' + sIdx"
              class="asg-toc-btn"
              @click="scrollToAsgSection('asg-sec-' + sIdx)"
            >
              <span class="asg-toc-num">{{ String(sIdx + 1).padStart(2, '0') }}</span>
              <span class="asg-toc-text">{{ sec.heading }}</span>
            </button>
          </div>

          <!-- Document Render Sections -->
          <div class="asg-content-wrapper">
            
            <!-- Excel Workbook Viewer if Present -->
            <div v-if="currentAssignment.workbook" id="asg-workbook-anchor" class="card workbook-card">
              <div class="wb-header">
                <div class="wb-title-group">
                  <span class="wb-icon">📊</span>
                  <div>
                    <h3>{{ uiText.asgWorkbookTitle }} {{ currentAssignment.xlsx_file }}</h3>
                    <div class="wb-subtitle">{{ uiText.asgWorkbookSub }}</div>
                  </div>
                </div>
                <!-- Sheet selector tabs -->
                <div class="sheet-tabs">
                  <button 
                    v-for="(grid, sheetName) in currentAssignment.workbook" 
                    :key="sheetName"
                    :class="['sheet-tab-btn', { active: selectedWorkbookSheet === sheetName }]"
                    @click="selectedWorkbookSheet = sheetName"
                  >
                    {{ sheetName }}
                  </button>
                </div>
              </div>

              <!-- Selected Sheet Grid Table -->
              <div v-if="selectedWorkbookSheet && currentAssignment.workbook[selectedWorkbookSheet]" class="wb-table-wrap">
                <table class="wb-data-table">
                  <tbody>
                    <tr 
                      v-for="(row, rIdx) in currentAssignment.workbook[selectedWorkbookSheet]" 
                      :key="rIdx"
                      :class="getWbRowClass(row, rIdx)"
                    >
                      <td v-for="(val, cIdx) in row" :key="cIdx" :class="getCellClass(val, cIdx)">
                        {{ val }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Report Document Sections -->
            <div class="asg-sections-stream">
              <div 
                v-for="(sec, sIdx) in currentAssignment.sections" 
                :key="sIdx"
                :id="'asg-sec-' + sIdx"
                class="card asg-section-card"
              >
                <div class="sec-card-header-bar">
                  <div class="sec-heading-group">
                    <span class="sec-num-badge">{{ String(sIdx + 1).padStart(2, '0') }}</span>
                    <h2 class="sec-card-heading">{{ sec.heading }}</h2>
                  </div>
                  <div v-if="sec.source_citation" class="sec-cite-pill">
                    <strong>{{ uiText.asgSourceRefLabel }}</strong> {{ sec.source_citation }}
                  </div>
                </div>

                <!-- Section Paragraphs -->
                <div class="sec-paragraphs">
                  <p v-for="(p, pIdx) in sec.paragraphs" :key="pIdx" class="sec-paragraph-text">
                    {{ p }}
                  </p>
                </div>

                <!-- Structured Financial Tables -->
                <div v-for="(tbl, tIdx) in sec.tables" :key="tIdx" class="asg-fin-table-card">
                  <div class="asg-fin-table-topbar">
                    <span class="asg-fin-table-badge">📋 {{ uiText.asgSecTableBadge }}</span>
                  </div>
                  <div class="asg-fin-table-scroll">
                    <table class="asg-fin-table">
                      <thead>
                        <tr v-if="tbl.length > 0">
                          <th
                            v-for="(th, hIdx) in tbl[0]"
                            :key="hIdx"
                            :class="{ 'th-left': !isColNumeric(tbl, hIdx), 'th-right': isColNumeric(tbl, hIdx) }"
                          >
                            {{ th }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(rVals, rIdx) in tbl.slice(1)"
                          :key="rIdx"
                          :class="getSecTableRowClass(rVals)"
                        >
                          <td v-for="(val, cIdx) in rVals" :key="cIdx" :class="getCellClass(val, cIdx)">
                            {{ val }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <!-- Audited LK GOTO 2025 Visual Proof Card -->
                <div v-if="sec.evidence_img" class="asg-evidence-card">
                  <div class="asg-evidence-head">
                    <span class="asg-proof-badge">🔍 {{ uiText.asgProofBadge }}</span>
                    <span class="asg-proof-zoom">{{ uiText.asgZoomHint }}</span>
                  </div>
                  <div
                    class="asg-evidence-body"
                    @click="openLightbox(sec.evidence_img, sec.heading, sec.evidence_caption || sec.source_citation)"
                  >
                    <img
                      :src="sec.evidence_img"
                      :alt="sec.evidence_caption || sec.heading"
                      class="asg-evidence-thumb"
                    />
                    <div class="asg-evidence-meta">
                      <div v-if="sec.evidence_caption" class="asg-evidence-caption">{{ sec.evidence_caption }}</div>
                      <div v-if="sec.source_citation" class="asg-evidence-cite">{{ sec.source_citation }}</div>
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div>


        <!-- ================= TAB 1: VISUAL SLIDE STREAM WITH EMBEDDED GOTO REPORT ================= -->
        <div v-if="activeTab === 'slides'" class="tab-pane">
          <div class="hero-banner">
            <div class="hero-header-row">
              <span class="hero-tag">{{ currentLecture.week }} • Slide by Slide Visual Deck</span>
              <span class="hero-reading">📚 {{ currentLecture.reading }}</span>
            </div>
            <h1 class="hero-title">{{ currentLecture.title }}</h1>
            <div class="core-question-box">
              <span class="cq-icon">❓</span>
              <div class="cq-content">
                <strong>Core Analytical Question:</strong>
                <p>{{ currentLecture.core_question }}</p>
              </div>
            </div>
          </div>

          <!-- Slide-by-Slide Stream with Real Slide Images + Embedded GoTo Reports -->
          <div class="slides-stream">
            <div 
              v-for="slide in currentLecture.slides" 
              :key="slide.slide_num"
              :id="'lecture-slide-' + currentLecture.id + '-' + slide.slide_num"
              class="slide-entry-card"
            >
              <!-- Card Header -->
              <div class="slide-card-header">
                <div class="slide-badge-title">
                  <span class="slide-number-pill">SLIDE {{ slide.slide_num }} OF {{ currentLecture.slides.length }}</span>
                  <h2 class="slide-main-header">{{ slide.header }}</h2>
                </div>
                <div v-if="slide.subtitle" class="slide-sub-pill">{{ slide.subtitle }}</div>
              </div>

              <!-- High-Resolution Real Slide Image Screenshot -->
              <div class="slide-image-wrapper">
                <img 
                  :src="slide.image_url" 
                  :alt="slide.header" 
                  class="actual-slide-image"
                  loading="lazy"
                />
              </div>

              <!-- Two-Column Conceptual Foundation -->
              <div class="slide-dual-explanation">
                <!-- Theoretical Concept Column -->
                <div class="exp-col theory-col">
                  <div class="exp-header">
                    <span class="exp-icon">📖</span>
                    <h3>Lecture Theory & Academic Concept</h3>
                  </div>
                  <p class="exp-body">{{ slide.theory_explanation }}</p>
                </div>

                <!-- GoTo Application Column -->
                <div class="exp-col goto-col">
                  <div class="exp-header">
                    <span class="exp-icon">🟢</span>
                    <h3>Application to PT GoTo Gojek Tokopedia Tbk</h3>
                  </div>
                  <p class="exp-body">{{ slide.goto_explanation }}</p>
                </div>
              </div>

              <!-- ================= SPECIFIC GOTO REPORT EMBEDDED BELOW ================= -->
              <div v-if="slide.goto_report" class="goto-report-container">
                <div class="report-header-banner">
                  <div class="report-title-group">
                    <span class="report-badge">{{ slide.goto_report.badge }}</span>
                    <h3 class="report-title">{{ slide.goto_report.title }}</h3>
                  </div>
                  <div class="report-org-tag">PT GoTo Gojek Tokopedia Tbk (IDX: GOTO)</div>
                </div>

                <!-- Case 1: Table Content Type -->
                <div v-if="slide.goto_report.content_type === 'table'" class="report-table-section">
                  <!-- Week 4 Slide 4: Interactive GoTo Cash Flow Chart (100% Pure GoTo) -->
                  <div v-if="selectedWeekId === 'week4' && slide.slide_num === 4" class="lecture-chart-card">
                    <div class="chart-card-topbar">
                      <div class="chart-heading-group">
                        <span class="chart-pill-badge">GOTO CASH FLOW DISCOVERY</span>
                        <h4 class="chart-main-title">
                          PT GoTo Gojek Tokopedia Tbk (GOTO), 2023 - 2025
                        </h4>
                        <p class="chart-sub-title">
                          Three-Year Trajectory: Operating Cash Flow (CFO) vs Free Cash Flow (FCF) vs Net Loss
                        </p>
                      </div>

                      <div class="chart-entity-tabs">
                        <button 
                          type="button" 
                          class="chart-tab-btn" 
                          :class="{ active: gotoChartScale === 'operating' }"
                          @click="gotoChartScale = 'operating'"
                        >
                          Operating Focus Scale (-6T to +2T)
                        </button>
                        <button 
                          type="button" 
                          class="chart-tab-btn" 
                          :class="{ active: gotoChartScale === 'macro' }"
                          @click="gotoChartScale = 'macro'"
                        >
                          Macro Deficit Scale (-100T to +10T)
                        </button>
                      </div>
                    </div>

                    <div class="chart-card-body">
                      <!-- Left Column: The Interactive SVG Plot -->
                      <div class="chart-svg-column">
                        <div class="chart-y-axis-label">
                          {{ gotoChartScale === 'operating' ? 'Rp trillion (Operating Cash & FCF Focus)' : 'Rp trillion (Full Impairment Scale)' }}
                        </div>

                        <!-- View 1: Operating Focus Scale (-6T to +2T) -->
                        <div v-if="gotoChartScale === 'operating'" class="svg-container">
                          <svg viewBox="0 0 580 260" class="trend-svg" preserveAspectRatio="xMidYMid meet">
                            <!-- Background Accent for Positive Operating Region (Above Y = 80) -->
                            <rect x="70" y="35" width="470" height="45" fill="#f0fdf4" opacity="0.6" />
                            <text x="530" y="52" fill="#16a34a" font-size="10" font-weight="700" text-anchor="end">POSITIVE CASH FLOW REGION</text>

                            <!-- Horizontal Grid Lines & Y-ticks -->
                            <g class="grid-lines">
                              <!-- +2T -->
                              <line x1="70" y1="35" x2="540" y2="35" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="39" class="axis-tick" text-anchor="end">+2T</text>

                              <!-- +1T -->
                              <line x1="70" y1="57.5" x2="540" y2="57.5" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="61.5" class="axis-tick" text-anchor="end">+1T</text>

                              <!-- 0T (Zero Line Bold) -->
                              <line x1="70" y1="80" x2="540" y2="80" stroke="#059669" stroke-width="1.8" />
                              <text x="60" y="84" class="axis-tick font-bold" text-anchor="end" fill="#059669">0.0</text>

                              <!-- -1T -->
                              <line x1="70" y1="102.5" x2="540" y2="102.5" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="106.5" class="axis-tick" text-anchor="end">-1T</text>

                              <!-- -2T -->
                              <line x1="70" y1="125" x2="540" y2="125" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="129" class="axis-tick" text-anchor="end">-2T</text>

                              <!-- -3T -->
                              <line x1="70" y1="147.5" x2="540" y2="147.5" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="151.5" class="axis-tick" text-anchor="end">-3T</text>

                              <!-- -4T -->
                              <line x1="70" y1="170" x2="540" y2="170" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="174" class="axis-tick" text-anchor="end">-4T</text>

                              <!-- -5T -->
                              <line x1="70" y1="192.5" x2="540" y2="192.5" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="196.5" class="axis-tick" text-anchor="end">-5T</text>

                              <!-- -6T -->
                              <line x1="70" y1="215" x2="540" y2="215" stroke="#cbd5e1" stroke-width="1" />
                              <text x="60" y="219" class="axis-tick" text-anchor="end">-6T</text>
                            </g>

                            <!-- Vertical Ticks & X Labels -->
                            <g class="x-axis">
                              <line x1="140" y1="215" x2="140" y2="221" stroke="#64748b" stroke-width="1" />
                              <text x="140" y="237" class="x-axis-label" text-anchor="middle">2023</text>

                              <line x1="310" y1="215" x2="310" y2="221" stroke="#64748b" stroke-width="1" />
                              <text x="310" y="237" class="x-axis-label" text-anchor="middle">2024</text>

                              <line x1="480" y1="215" x2="480" y2="221" stroke="#64748b" stroke-width="1" />
                              <text x="480" y="237" class="x-axis-label" text-anchor="middle">2025</text>
                            </g>

                            <!-- Polylines -->
                            <!-- Net Loss Polyline: angle from 2023 off-chart (-90.5T) up to 2024 (-5.5T) -> 2025 (-1.5T) -->
                            <polyline 
                              points="170,225 310,203.75 480,113.75" 
                              fill="none" 
                              stroke="#1e3a5f" 
                              stroke-width="2.5" 
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            />
                            <!-- Dash line down towards 2023 -90.5T -->
                            <line x1="140" y1="240" x2="170" y2="225" stroke="#1e3a5f" stroke-width="2" stroke-dasharray="3 3" />
                            <text x="140" y="254" font-size="10.5" font-weight="700" fill="#1e3a5f" text-anchor="middle">2023: -(Rp 90.5T) Goodwill Crash ↓</text>

                            <!-- Free Cash Flow (FCF) Polyline (dashed red): 140,174.5 -> 310,111.5 -> 480,100.25 -->
                            <polyline 
                              points="140,174.5 310,111.5 480,100.25" 
                              fill="none" 
                              stroke="#ef4444" 
                              stroke-width="3" 
                              stroke-dasharray="6 4"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            />

                            <!-- Operating Cash Flow (CFO) Polyline (solid emerald): 140,167.75 -> 310,98.0 -> 480,73.25 -->
                            <polyline 
                              points="140,167.75 310,98.0 480,73.25" 
                              fill="none" 
                              stroke="#10b981" 
                              stroke-width="3.5" 
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            />

                            <!-- 2025 Capex Divergence Bracket between CFO (73.25) and FCF (100.25) -->
                            <line x1="500" y1="73.25" x2="500" y2="100.25" stroke="#f59e0b" stroke-width="2" stroke-dasharray="2 2" />
                            <circle cx="500" cy="73.25" r="2.5" fill="#f59e0b" />
                            <circle cx="500" cy="100.25" r="2.5" fill="#f59e0b" />
                            <text x="506" y="89" font-size="10" font-weight="700" fill="#b45309">Capex: -Rp 1.18T</text>

                            <!-- Data Points: Operating Cash Flow (CFO) -->
                            <g class="points-goto-cfo">
                              <!-- 2023: -3.9T -->
                              <circle 
                                cx="140" cy="167.75" r="6" fill="#10b981" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Operating Cash Flow', year: '2023', val: '(3,942.1) bn', ref: 'B5', rowIdx: 3, formula: '= 2023 Operating Cash Burn: -(Rp 3,942.1 bn)', sources: ['B5'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="140" y="158" class="point-label emerald-label" text-anchor="middle">-3.9T</text>

                              <!-- 2024: -0.8T -->
                              <circle 
                                cx="310" cy="98.0" r="6" fill="#10b981" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Operating Cash Flow', year: '2024', val: '(762.4) bn', ref: 'C5', rowIdx: 3, formula: '= 2024 Operating Cash Burn narrowed: -(Rp 762.4 bn)', sources: ['C5'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="310" y="88" class="point-label emerald-label" text-anchor="middle">-0.8T</text>

                              <!-- 2025: +0.3T (+Rp 307 bn) -->
                              <circle 
                                cx="480" cy="73.25" r="6.5" fill="#10b981" stroke="#ffffff" stroke-width="2" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Operating Cash Flow', year: '2025', val: '+307.0 bn', ref: 'D5', rowIdx: 3, formula: '= 2025 Operating Cash Flow: +Rp 307.0 bn (Crossed into positive territory!)', sources: ['D5'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="480" y="62" class="point-label emerald-label font-bold" text-anchor="middle">+0.3T (+Rp 307 bn CFO)</text>
                            </g>

                            <!-- Data Points: Free Cash Flow (FCF) -->
                            <g class="points-goto-fcf">
                              <!-- 2023: -4.2T -->
                              <circle 
                                cx="140" cy="174.5" r="5" fill="#ef4444" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Free Cash Flow', year: '2023', val: '(4,159.2) bn', ref: 'B7', rowIdx: 5, formula: '= 2023 Free Cash Flow: -(Rp 4,159.2 bn) (CFO -3.9T less Capex 217bn)', sources: ['B7'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="140" y="190" class="point-label crimson-label" text-anchor="middle">-4.2T</text>

                              <!-- 2024: -1.4T -->
                              <circle 
                                cx="310" cy="111.5" r="5" fill="#ef4444" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Free Cash Flow', year: '2024', val: '(1,414.7) bn', ref: 'C7', rowIdx: 5, formula: '= 2024 Free Cash Flow: -(Rp 1,414.7 bn) (CFO -762bn less Capex 652bn)', sources: ['C7'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="310" y="127" class="point-label crimson-label" text-anchor="middle">-1.4T</text>

                              <!-- 2025: -0.9T -->
                              <circle 
                                cx="480" cy="100.25" r="5.5" fill="#ef4444" stroke="#ffffff" stroke-width="1.5" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Free Cash Flow', year: '2025', val: '(875.3) bn', ref: 'D7', rowIdx: 5, formula: '= 2025 Free Cash Flow: -(Rp 875.3 bn) (CFO +307bn less Capex 1,182.4bn)', sources: ['D7'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="480" y="117" class="point-label crimson-label font-bold" text-anchor="middle">-0.9T (-(Rp 875 bn) FCF)</text>
                            </g>

                            <!-- Data Points: Net Loss -->
                            <g class="points-goto-net-loss">
                              <!-- 2024: -5.5T -->
                              <circle 
                                cx="310" cy="203.75" r="5" fill="#1e3a5f" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Net Loss', year: '2024', val: '(5,471.2) bn', ref: 'C4', rowIdx: 2, formula: '= 2024 Net Loss: -(Rp 5,471.2 bn) (Narrowed 94% post-impairment)', sources: ['C4'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="310" y="217" class="point-label slate-label" text-anchor="middle">-5.5T</text>

                              <!-- 2025: -1.5T -->
                              <circle 
                                cx="480" cy="113.75" r="5" fill="#1e3a5f" class="chart-point"
                                @mouseenter="onHoverChartPoint({ series: 'GoTo Net Loss', year: '2025', val: '(1,501.7) bn', ref: 'D4', rowIdx: 2, formula: '= 2025 Net Loss: -(Rp 1,501.7 bn) (Operating loss narrowed to -Rp 378 bn)', sources: ['D4'] })"
                                @mouseleave="onHoverChartPoint(null)"
                              />
                              <text x="480" y="132" class="point-label slate-label" text-anchor="middle">-1.5T (Net Loss)</text>
                            </g>
                          </svg>

                          <!-- Legend -->
                          <div class="chart-legend-row">
                            <div class="legend-item">
                              <span class="legend-line emerald-line"></span>
                              <span class="legend-dot emerald-dot"></span>
                              <span class="legend-text">Operating Cash Flow (CFO, Rp T)</span>
                            </div>
                            <div class="legend-item">
                              <span class="legend-line crimson-line"></span>
                              <span class="legend-dot crimson-dot"></span>
                              <span class="legend-text">Free Cash Flow (FCF = CFO - Capex)</span>
                            </div>
                            <div class="legend-item">
                              <span class="legend-line slate-line"></span>
                              <span class="legend-dot slate-dot"></span>
                              <span class="legend-text">Net Loss for Year (Rp T)</span>
                            </div>
                          </div>
                        </div>

                        <!-- View 2: Macro Deficit Scale (-100T to +10T) -->
                        <div v-else class="svg-container">
                          <svg viewBox="0 0 580 260" class="trend-svg" preserveAspectRatio="xMidYMid meet">
                            <!-- Horizontal Grid Lines & Y-ticks -->
                            <g class="grid-lines">
                              <!-- Y = 10T -->
                              <line x1="70" y1="40" x2="540" y2="40" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="44" class="axis-tick" text-anchor="end">+10T</text>

                              <!-- Y = 0 (Zero Line Bold) -->
                              <line x1="70" y1="55" x2="540" y2="55" stroke="#059669" stroke-width="1.8" />
                              <text x="60" y="59" class="axis-tick font-bold" text-anchor="end" fill="#059669">0.0</text>

                              <!-- Y = -20T -->
                              <line x1="70" y1="85" x2="540" y2="85" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="89" class="axis-tick" text-anchor="end">-20T</text>

                              <!-- Y = -40T -->
                              <line x1="70" y1="115" x2="540" y2="115" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="119" class="axis-tick" text-anchor="end">-40T</text>

                              <!-- Y = -60T -->
                              <line x1="70" y1="145" x2="540" y2="145" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="149" class="axis-tick" text-anchor="end">-60T</text>

                              <!-- Y = -80T -->
                              <line x1="70" y1="175" x2="540" y2="175" stroke="#e2e8f0" stroke-width="1" />
                              <text x="60" y="179" class="axis-tick" text-anchor="end">-80T</text>

                              <!-- Y = -100T -->
                              <line x1="70" y1="205" x2="540" y2="205" stroke="#cbd5e1" stroke-width="1" />
                              <text x="60" y="209" class="axis-tick" text-anchor="end">-100T</text>
                            </g>

                            <!-- Vertical Ticks & X Labels -->
                            <g class="x-axis">
                              <line x1="140" y1="205" x2="140" y2="211" stroke="#64748b" stroke-width="1" />
                              <text x="140" y="227" class="x-axis-label" text-anchor="middle">2023</text>

                              <line x1="310" y1="205" x2="310" y2="211" stroke="#64748b" stroke-width="1" />
                              <text x="310" y="227" class="x-axis-label" text-anchor="middle">2024</text>

                              <line x1="480" y1="205" x2="480" y2="211" stroke="#64748b" stroke-width="1" />
                              <text x="480" y="227" class="x-axis-label" text-anchor="middle">2025</text>
                            </g>

                            <!-- GoTo Net Loss Polyline: (140, 190.8) -> (310, 63.3) -> (480, 57.3) -->
                            <polyline 
                              points="140,190.8 310,63.3 480,57.3" 
                              fill="none" 
                              stroke="#1e3a5f" 
                              stroke-width="3" 
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            />

                            <!-- GoTo CFO Polyline: (140, 60.9) -> (310, 56.2) -> (480, 54.55) -->
                            <polyline 
                              points="140,60.9 310,56.2 480,54.55" 
                              fill="none" 
                              stroke="#10b981" 
                              stroke-width="3" 
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            />

                            <!-- GoTo FCF Polyline (dashed): (140, 61.3) -> (310, 57.1) -> (480, 56.35) -->
                            <polyline 
                              points="140,61.3 310,57.1 480,56.35" 
                              fill="none" 
                              stroke="#ef4444" 
                              stroke-width="2.5" 
                              stroke-dasharray="6 4"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            />

                            <!-- Points -->
                            <circle cx="140" cy="190.8" r="5.5" fill="#1e3a5f" class="chart-point" />
                            <text x="152" y="195" class="point-label slate-label font-bold">-90.5T (Goodwill Crash)</text>

                            <circle cx="310" cy="63.3" r="5" fill="#1e3a5f" class="chart-point" />
                            <text x="322" y="75" class="point-label slate-label">-5.5T</text>

                            <circle cx="480" cy="57.3" r="5" fill="#1e3a5f" class="chart-point" />
                            <text x="492" y="70" class="point-label slate-label">-1.5T</text>

                            <circle cx="480" cy="54.55" r="5.5" fill="#10b981" class="chart-point" />
                            <text x="492" y="44" class="point-label emerald-label font-bold">+0.3T (CFO Positive)</text>
                          </svg>

                          <!-- Legend -->
                          <div class="chart-legend-row">
                            <div class="legend-item">
                              <span class="legend-line slate-line"></span>
                              <span class="legend-dot slate-dot"></span>
                              <span class="legend-text">Net Loss for Year (Rp T)</span>
                            </div>
                            <div class="legend-item">
                              <span class="legend-line emerald-line"></span>
                              <span class="legend-dot emerald-dot"></span>
                              <span class="legend-text">Operating Cash Flow (CFO, Rp T)</span>
                            </div>
                            <div class="legend-item">
                              <span class="legend-line crimson-line"></span>
                              <span class="legend-dot crimson-dot"></span>
                              <span class="legend-text">Free Cash Flow (FCF = CFO - Capex)</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Right Column: GoTo Cash Flow Reality Callout Card -->
                      <div class="chart-notice-card">
                        <div class="notice-title">
                          GoTo Cash Flow Reality
                        </div>
                        <div class="notice-body">
                          <p class="notice-paragraph">
                            <strong>2024 Recovery:</strong> Net loss fell 94% once goodwill write-downs stopped, but CFO still burned -(Rp 762.4 bn).
                          </p>
                          <p class="notice-paragraph">
                            <strong>2025 CFO Crossing:</strong> Operating cash crossed into positive (+Rp 307.0 bn) for the first time in GoTo's corporate history.
                          </p>
                          <p class="notice-paragraph">
                            <strong>The Capex Trap:</strong> Free Cash Flow remained strictly negative at -(Rp 875.3 bn) because mandatory tech investments (Rp 1,182.4 bn) wiped out operating cash.
                          </p>
                        </div>
                        <div class="notice-punchline">
                          Operating cash turned green, but capital burns on.
                        </div>
                        <div class="notice-footnote">
                          <span>Financial Statement Analysis • GoTo Audited Cash Flow Analysis</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Formula Bar (Inspired by efficient-diversification-react) -->
                  <div class="worksheet-formula-bar" :class="{ 'worksheet-active': activeFormulaCell }">
                    <div class="formula-bar-top">
                      <span class="worksheet-cell-ref">{{ activeFormulaCell ? activeFormulaCell.ref : 'fx' }}</span>
                      <span class="worksheet-fx">fx</span>
                      <code :title="activeFormulaCell ? activeFormulaCell.formula : ''">{{ activeFormulaCell ? activeFormulaCell.formula : 'Hover over any line item or cell to inspect formula' }}</code>
                    </div>
                    <div class="formula-bar-bottom">
                      <span class="formula-val-tag">Value:</span>
                      <span class="formula-val-display">{{ activeFormulaCell ? activeFormulaCell.val : '-' }}</span>
                    </div>
                  </div>

                  <div class="val-table-wrap">
                    <table class="data-table worksheet-grid">
                      <thead>
                        <!-- Top Row: Column Letters A, B, C, D, E -->
                        <tr class="worksheet-letters">
                          <th class="row-num-th" aria-label="Row Numbers"></th>
                          <th v-for="(colLtr, cIdx) in getColLetters(slide.goto_report.table_headers.length)" :key="cIdx">
                            {{ colLtr }}
                          </th>
                        </tr>
                        <!-- Second Row: Header Titles with Row Number 1 -->
                        <tr class="worksheet-headings">
                          <th class="row-num-th">1</th>
                          <th v-for="(th, hIdx) in slide.goto_report.table_headers" :key="hIdx">{{ th }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr 
                          v-for="(rVals, rIdx) in slide.goto_report.table_rows" 
                          :key="rIdx"
                          :id="`table-row-${slide.slide_num}-${rIdx}`"
                          :class="{ 'is-row-lit': hoveredRowIdx === rIdx }"
                        >
                          <!-- Row Number on the Left (2, 3, 4, ...) -->
                          <th class="row-num-th">{{ rIdx + 2 }}</th>

                          <!-- Column A (Line Item Title) -->
                          <td 
                            class="bold-cell"
                            :id="`table-cell-${slide.slide_num}-${rIdx}-0`"
                            :data-cell-ref="`A${rIdx + 2}`"
                            :class="{
                              'worksheet-selected': activeFormulaCell && activeFormulaCell.ref === `A${rIdx + 2}`,
                              'worksheet-used': activeFormulaCell && activeFormulaCell.sources.includes(`A${rIdx + 2}`)
                            }"
                            @mouseenter="onHoverCell(slide.slide_num, rIdx, 0, rVals)"
                            @click="onHoverCell(slide.slide_num, rIdx, 0, rVals)"
                          >
                            {{ rVals[0] }}
                          </td>

                          <!-- Columns B, C, D, ... -->
                          <td 
                            v-for="(val, cIdx) in rVals.slice(1)" 
                            :key="cIdx" 
                            :id="`table-cell-${slide.slide_num}-${rIdx}-${cIdx + 1}`"
                            :data-cell-ref="`${getColLetter(cIdx + 1)}${rIdx + 2}`"
                            class="num-cell"
                            :class="{ 
                              'is-cell-lit': hoveredCellRef === `${rIdx}-${cIdx + 1}`,
                              'worksheet-selected': activeFormulaCell && activeFormulaCell.ref === `${getColLetter(cIdx + 1)}${rIdx + 2}`,
                              'worksheet-used': activeFormulaCell && activeFormulaCell.sources.includes(`${getColLetter(cIdx + 1)}${rIdx + 2}`)
                            }"
                            @mouseenter="onHoverCell(slide.slide_num, rIdx, cIdx + 1, rVals)"
                            @click="onHoverCell(slide.slide_num, rIdx, cIdx + 1, rVals)"
                          >
                            {{ val }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div v-if="slide.goto_report.analytical_note" class="gap-expl-box">
                    <h3>
                      <span class="expl-icon">🔍</span>
                      <span>Empirical Finding & Classroom Defense</span>
                      <span class="expl-hint">(hover highlighted values to link table)</span>
                    </h3>
                    <p>
                      <template v-for="(t, tIdx) in getNoteTokens(slide.goto_report.analytical_note, slide.goto_report.table_rows)" :key="tIdx">
                        <span 
                          v-if="t.type === 'ref'"
                          class="ref-chip"
                          :class="{ 'is-active': hoveredRowIdx === t.row && hoveredCellRef === `${t.row}-${t.col}` }"
                          @mouseenter="setHoveredRef(slide.slide_num, t.row, t.col, slide.goto_report.table_rows)"
                          @mouseleave="clearHoveredRef"
                          :title="`Lights up: ${t.account} (${t.val})`"
                        >
                          {{ t.text }}
                        </span>
                        <span v-else>{{ t.text }}</span>
                      </template>
                    </p>
                  </div>
                </div>

                <!-- Case 2: Cards and Badges Content Type -->
                <div v-else-if="slide.goto_report.content_type === 'cards_and_badges'" class="report-metrics-section">
                  <p v-if="slide.goto_report.description" class="report-desc-text">{{ slide.goto_report.description }}</p>
                  <div v-if="slide.goto_report.key_metrics" class="coc-grid">
                    <div v-for="(m, mIdx) in slide.goto_report.key_metrics" :key="mIdx" class="coc-item highlight-green">
                      <span class="coc-lbl">{{ m.label }}</span>
                      <span class="coc-val">{{ m.val }}</span>
                      <span v-if="m.note" class="coc-sub-text">{{ m.note }}</span>
                    </div>
                  </div>
                </div>

                <!-- Case 3: Text and Profile Cards -->
                <div v-else class="report-text-section">
                  <p class="report-desc-text">{{ slide.goto_report.description }}</p>
                  <div v-if="slide.goto_report.key_metrics" class="coc-grid" style="margin-top: 14px;">
                    <div v-for="(m, mIdx) in slide.goto_report.key_metrics" :key="mIdx" class="coc-item">
                      <span class="coc-lbl">{{ m.label }}</span>
                      <span class="coc-val">{{ m.val }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- ================= AUDITED FINANCIAL STATEMENT SCREENSHOT EVIDENCE ================= -->
              <div v-if="slide.audit_evidence" class="audit-evidence-container">
                <div class="evidence-header-banner">
                  <div class="evidence-badge-group">
                    <span class="evidence-badge">AUDITED FINANCIAL STATEMENT EVIDENCE</span>
                    <h3 class="evidence-title">{{ slide.audit_evidence.title }}</h3>
                  </div>
                  <div v-if="slide.audit_evidence.img" class="evidence-header-actions">
                    <div class="evidence-source-tag">Official IDX Filing: LK GOTO 31 Dec 2025</div>
                    <button 
                      type="button" 
                      class="evidence-zoom-btn" 
                      :class="{ active: isActualSize }"
                      @click="isActualSize = !isActualSize"
                      :title="isActualSize ? 'Fit image to container' : 'View at 100% full resolution'"
                    >
                      <span v-if="!isActualSize">🔍 100% Size</span>
                      <span v-else>↔ Fit</span>
                    </button>
                    <button 
                      type="button" 
                      class="evidence-modal-btn" 
                      @click="openLightbox(slide.audit_evidence.img, slide.audit_evidence.title, slide.audit_evidence.caption)"
                      title="Open full-screen interactive view"
                    >
                      ⛶ Fullscreen
                    </button>
                  </div>
                </div>

                <!-- Key Figures Bar -->
                <div v-if="slide.audit_evidence.key_figures && slide.audit_evidence.key_figures.length" class="evidence-key-figures-bar">
                  <div v-for="(kf, kfIdx) in slide.audit_evidence.key_figures" :key="kfIdx" class="evidence-kf-pill">
                    <span class="kf-label">{{ kf.label }}:</span>
                    <strong class="kf-val">{{ kf.val }}</strong>
                    <span v-if="kf.ref" class="kf-ref">[{{ kf.ref }}]</span>
                  </div>
                </div>

                <div 
                  v-if="slide.audit_evidence.img"
                  class="evidence-image-wrapper" 
                  :class="{ 'actual-size-mode': isActualSize }"
                >
                  <img 
                    :src="slide.audit_evidence.img" 
                    :alt="slide.audit_evidence.title"
                    class="actual-statement-image" 
                    :class="{ 'image-full-width': isActualSize }"
                    @click="openLightbox(slide.audit_evidence.img, slide.audit_evidence.title, slide.audit_evidence.caption)"
                    loading="lazy"
                  />
                </div>
                <div v-if="slide.audit_evidence.caption" class="evidence-caption-box">
                  <span class="caption-icon">🔍</span>
                  <p>{{ slide.audit_evidence.caption }}</p>
                </div>
              </div>

            </div>
          </div>
        </div>

        <!-- ================= TAB 3: GOTO APPLICATION (MODELS) ================= -->
        <div v-if="activeTab === 'goto'" class="tab-pane">
          <div class="hero-banner goto-banner">
            <div class="hero-header-row">
              <span class="hero-tag goto-tag">Empirical Data & Analysis</span>
              <span class="hero-reading">PT GoTo Gojek Tokopedia Tbk (IDX: GOTO)</span>
            </div>
            <h1 class="hero-title">{{ currentLecture.goto_application.title }}</h1>
            <p class="goto-subtitle">Prepared by Group 4: Fagly Ramschie, Anggreini Ruitan, Galatia Rompas</p>
          </div>

          <!-- Week 2: Porter's Five Forces Breakdown -->
          <div v-if="currentLecture.goto_application.type === 'five_forces'" class="content-cards">
            <div class="card">
              <h2 class="card-title">Porter's Five Forces Evaluation for GoTo (Milestone 1)</h2>
              <p class="card-subtitle">Evaluating industry profit barriers, pricing power, and competitive rivalry</p>
              
              <div class="forces-list">
                <div v-for="(f, i) in currentLecture.goto_application.forces" :key="i" class="force-card">
                  <div class="force-header">
                    <span class="force-name">{{ f.force }}</span>
                    <span :class="['rating-badge', f.rating.toLowerCase().includes('high') || f.rating.toLowerCase().includes('cutthroat') ? 'badge-high' : 'badge-med']">
                      {{ f.rating }}
                    </span>
                  </div>
                  <p class="force-text">{{ f.analysis }}</p>
                </div>
              </div>

              <div class="gap-expl-box danger-box" style="margin-top: 20px;">
                <h3>Strategic Verdict</h3>
                <p>{{ currentLecture.goto_application.verdict }}</p>
              </div>
            </div>
          </div>

          <!-- General Fallback for Other Weeks -->
          <div v-else class="content-cards">
            <div class="card">
              <h2 class="card-title">Empirical GoTo Application for {{ currentLecture.week }}</h2>
              <p class="card-subtitle">{{ currentLecture.goto_application.title }}</p>
              <div class="general-bullets">
                <div v-for="(tk, i) in currentLecture.study_takeaways" :key="i" class="bullet-item">
                  <span class="bullet-icon">📌</span>
                  <p>{{ tk }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ================= TAB 4: KEY TAKEAWAYS ================= -->
        <div v-if="activeTab === 'flashcards'" class="tab-pane">
          <div class="hero-banner">
            <span class="hero-tag">Quick Revision</span>
            <h1 class="hero-title">Key Exam & Defense Takeaways: {{ currentLecture.week }}</h1>
            <p class="hero-reading">Master these core insights to ace oral defense and exams</p>
          </div>

          <div class="takeaways-deck">
            <div 
              v-for="(t, i) in currentLecture.study_takeaways" 
              :key="i"
              class="takeaway-card"
            >
              <div class="takeaway-num">0{{ i + 1 }}</div>
              <div class="takeaway-body">
                <h3>Core Concept Insight</h3>
                <p>{{ t }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- ================= TAB 5: 6-STEP ROADMAP ================= -->
        <div v-if="activeTab === 'roadmap'" class="tab-pane">
          <div class="hero-banner">
            <span class="hero-tag">The Big Picture</span>
            <h1 class="hero-title">The 16-Week FSA Curriculum Journey</h1>
            <p class="hero-reading">How all 12 modules link seamlessly into your final decision</p>
          </div>

          <div class="roadmap-timeline">
            <div 
              v-for="(lec, idx) in modules" 
              :key="lec.id"
              :class="['roadmap-node', { current: lec.id === selectedWeekId }]"
              @click="selectWeek(lec.id); activeTab = 'slides'"
            >
              <div class="node-badge">{{ lec.week }}</div>
              <div class="node-content">
                <div class="node-cat">{{ lec.category }}</div>
                <h3>{{ lec.title }}</h3>
                <p>{{ lec.core_question }}</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>

    <!-- ================= BROWSER-VIEWPORT PRESENTATION MODE ================= -->
    <div v-if="isPresentMode" class="present-overlay" @click.self="isPresentMode = false">
      <!-- Slim Top Control Bar -->
      <div class="present-topbar">
        <div class="present-top-left">
          <span class="present-mode-badge">PRESENTATION FOCUS</span>
          <span class="present-slide-counter">Slide {{ currentPresSlide.slide_num }} / {{ presentationSlides.length }}</span>
          <span class="present-section-lbl">{{ currentPresSlide.section_tag }}</span>
        </div>

        <div class="present-top-dots">
          <button
            v-for="ps in presentationSlides"
            :key="ps.slide_num"
            :class="['present-dot', { active: ps.slide_num === selectedPresSlideNum, apx: ps.is_appendix }]"
            @click="selectedPresSlideNum = ps.slide_num"
            :title="ps.title"
          >
            {{ ps.is_appendix ? 'A' + (ps.slide_num - 11) : ps.slide_num }}
          </button>
        </div>

        <button class="present-exit-btn" @click="isPresentMode = false" :title="uiText.exitEsc">
          ✕ {{ uiText.exitEsc }}
        </button>
      </div>

      <!-- Center Stage with Left / Right Arrows -->
      <div class="present-stage">
        <button
          class="present-arrow-btn present-arrow-left"
          :disabled="selectedPresSlideNum <= 1"
          @click="prevPresSlide"
          title="Previous Slide (Left Arrow)"
        >
          &lsaquo;
        </button>

        <section class="pres-canvas present-canvas">
          <div class="pres-slide-header">
            <div class="pres-header-top-row">
              <span class="pres-section-tag">{{ currentPresSlide.section_tag }}</span>
              <span class="pres-slide-index">{{ currentPresSlide.is_appendix ? uiText.appendixWord : uiText.mainDeckWord }} | {{ uiText.slideWord.toUpperCase() }} {{ currentPresSlide.slide_num }} / {{ presentationSlides.length }}</span>
            </div>
            <h1 class="pres-action-title">{{ currentPresSlide.title }}</h1>
            <p class="pres-slide-subtitle">{{ currentPresSlide.subtitle }}</p>
          </div>
          <div class="pres-emerald-bar"></div>

          <div class="pres-slide-body present-slide-body">
            <div v-if="currentPresSlide.kpis && currentPresSlide.kpis.length" class="pres-kpi-grid">
              <div
                v-for="(k, kIdx) in currentPresSlide.kpis"
                :key="kIdx"
                :class="['pres-kpi-card pres-interactive-item', 'tone-' + k.tone]"
                @click.stop="onPresItemClick($event, buildPresItemPayload('kpi', k))"
                @dblclick.stop="onPresItemDblClick(buildPresItemPayload('kpi', k))"
              >
                <div class="pres-kpi-val">{{ k.val }}</div>
                <div class="pres-kpi-lbl">{{ k.label }}</div>
                <div class="pres-kpi-sub">{{ k.sub }}</div>
              </div>
            </div>

            <div class="pres-content-grid">
              <div
                v-if="currentPresSlide.chart_url"
                class="pres-chart-card pres-interactive-item"
                @click.stop="onPresItemClick($event, buildPresItemPayload('chart', currentPresSlide))"
                @dblclick.stop="onPresItemDblClick(buildPresItemPayload('chart', currentPresSlide))"
              >
                <img
                  :src="currentPresSlide.chart_url"
                  :alt="currentPresSlide.title"
                  class="pres-chart-img present-chart-img"
                />
              </div>

              <div v-if="currentPresSlide.table" class="pres-table-card">
                <div class="pres-table-title">{{ currentPresSlide.table.title }}</div>
                <div class="wb-table-wrap">
                  <table class="data-table pres-data-table">
                    <thead>
                      <tr>
                        <th v-for="(th, hIdx) in currentPresSlide.table.headers" :key="hIdx">{{ th }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(rVals, rIdx) in currentPresSlide.table.rows"
                        :key="rIdx"
                        class="pres-interactive-row"
                        @click.stop="onPresItemClick($event, buildPresItemPayload('row', rVals, rIdx))"
                        @dblclick.stop="onPresItemDblClick(buildPresItemPayload('row', rVals, rIdx))"
                      >
                        <td v-for="(val, cIdx) in rVals" :key="cIdx" :class="{ 'bold-cell': cIdx === 0, 'num-cell': cIdx > 0 }">
                          {{ val }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div v-if="currentPresSlide.cards && currentPresSlide.cards.length" class="pres-cards-col">
                <div
                  v-for="(card, cIdx) in currentPresSlide.cards"
                  :key="cIdx"
                  :class="['pres-info-card pres-interactive-item', 'card-tone-' + card.tone]"
                  @click.stop="onPresItemClick($event, buildPresItemPayload('card', card))"
                  @dblclick.stop="onPresItemDblClick(buildPresItemPayload('card', card))"
                >
                  <h3 class="pres-card-title">{{ card.title }}</h3>
                  <ul class="pres-card-bullets">
                    <li v-for="(b, bIdx) in card.bullets" :key="bIdx">
                      <strong>{{ b.bold }}</strong> {{ b.text }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="pres-slide-footer">
            <span>Group 4 (Fagly Ramschie) | IDX: GOTO</span>
            <span>{{ uiText.sourceLabel }} {{ currentPresSlide.source_footer }}</span>
          </div>
        </section>

        <button
          class="present-arrow-btn present-arrow-right"
          :disabled="selectedPresSlideNum >= presentationSlides.length"
          @click="nextPresSlide"
          title="Next Slide (Right Arrow)"
        >
          &rsaquo;
        </button>
      </div>
    </div>

    <!-- ================= CLICK POPOVER ABOVE MOUSE ================= -->
    <div
      v-if="clickPopup"
      class="click-popover-above"
      :style="{ left: clickPopup.x + 'px', top: clickPopup.y + 'px' }"
      @click.stop
    >
      <div class="popover-hdr">
        <span class="popover-title">{{ clickPopup.title }}</span>
        <button class="popover-close" @click="clickPopup = null">&times;</button>
      </div>
      <div v-if="clickPopup.value" class="popover-val">{{ clickPopup.value }}</div>
      <p class="popover-exp">{{ clickPopup.detail_explanation || clickPopup.explanation }}</p>
      <div v-if="clickPopup.formula" class="popover-formula">
        <strong>∑</strong> {{ clickPopup.formula }}
      </div>
      <div class="popover-footer">
        <button class="popover-detail-btn" @click="onPresItemDblClick(clickPopup)">
          {{ uiText.clickHintDbl }}
        </button>
      </div>
    </div>

    <!-- ================= RIGHT-SIDE SLIDE-OVER SOURCE DRAWER ================= -->
    <div v-if="detailDrawerItem" class="drawer-backdrop" @click.self="detailDrawerItem = null">
      <aside class="right-detail-drawer">
        <div class="drawer-top-hdr">
          <div>
            <span class="drawer-badge">{{ uiText.drawerSubtitlePrefix }} {{ detailDrawerItem.slide.slide_num }}</span>
            <h3>{{ detailDrawerItem.title }}</h3>
            <div v-if="detailDrawerItem.value" class="drawer-val-pill">{{ detailDrawerItem.value }}</div>
          </div>
          <button class="drawer-close-btn" @click="detailDrawerItem = null" :title="uiText.closeWord + ' (Esc)'">&times;</button>
        </div>

        <div class="drawer-scroll-body">
          <!-- 1. Detailed Meaning & Explanation -->
          <div class="drawer-summary-box">
            <strong>{{ uiText.drawerWhatMeans }}</strong>
            <p>{{ detailDrawerItem.detail_explanation || detailDrawerItem.explanation }}</p>
          </div>

          <!-- 2. How Was This Calculated? (Formula + Step-by-Step Math + Origin) -->
          <div v-if="detailDrawerItem.formula || (detailDrawerItem.calc_steps && detailDrawerItem.calc_steps.length)" class="drawer-calc-box">
            <div class="drawer-calc-hdr">∑ {{ uiText.drawerHowCalculated }}</div>
            <div v-if="detailDrawerItem.formula" class="drawer-formula-pill">
              <span class="formula-lbl">{{ uiText.drawerFormulaLabel }}</span>
              <code>{{ detailDrawerItem.formula }}</code>
            </div>
            <ul v-if="detailDrawerItem.calc_steps && detailDrawerItem.calc_steps.length" class="drawer-calc-steps">
              <li v-for="(step, sIdx) in detailDrawerItem.calc_steps" :key="'cs-'+sIdx">{{ step }}</li>
            </ul>
            <div v-if="detailDrawerItem.data_origin" class="drawer-origin-line">
              <strong>{{ uiText.drawerOriginLabel }}</strong> {{ detailDrawerItem.data_origin }}
            </div>
          </div>

          <!-- 3. Featured Highlighted Audited LK GOTO Page -->
          <div v-if="detailDrawerItem.evidence_img" class="drawer-featured-ev">
            <div class="drawer-fev-hdr">
              <span>🔍 {{ uiText.drawerLkProofTitle }}</span>
            </div>
            <p v-if="detailDrawerItem.evidence_caption" class="drawer-fev-cap">{{ detailDrawerItem.evidence_caption }}</p>
            <img
              :src="detailDrawerItem.evidence_img"
              :alt="detailDrawerItem.evidence_caption || detailDrawerItem.title"
              class="drawer-thumb drawer-featured-thumb"
              @click="openLightbox(detailDrawerItem.evidence_img, detailDrawerItem.title + ' - ' + detailDrawerItem.value, detailDrawerItem.evidence_caption || detailDrawerItem.data_origin)"
            />
            <div class="drawer-zoom-hint">{{ uiText.drawerClickZoomHint }}</div>
          </div>

          <!-- 4. Matched Assignments & Audited Filings (with Highlighted Workbook Supporting Rows) -->
          <div class="drawer-section">
            <h4 class="drawer-sec-title asg-sec">📊 {{ uiText.drawerAsgTitle }} ({{ detailDrawerItem.matchedAssignments.length }})</h4>
            <div v-for="(at, idx) in detailDrawerItem.matchedAssignments" :key="'da-'+idx" class="drawer-trace-card">
              <div class="trace-item-top">
                <span class="trace-pill asg-pill">{{ at.assignment_code }}</span>
                <button class="trace-jump-btn asg-jump" @click="detailDrawerItem = null; isPresentMode = false; jumpToAssignmentSheet(at.assignment_id, at.sheet_name)">
                  {{ uiText.openWord }} {{ at.sheet_name || at.assignment_code }} &rarr;
                </button>
              </div>
              <div v-if="at.trace_role" class="trace-role-badge asg-role">{{ at.trace_role }}</div>
              <div class="trace-cell-ref"><code>{{ at.cell_or_section_ref }}</code></div>
              <p class="trace-mapping-note">{{ at.mapping_note }}</p>

              <!-- Highlighted Excel Workbook Supporting Table -->
              <div v-if="at.sheet_name && getSupportingWorkbookRows(at.assignment_id, at.sheet_name, detailDrawerItem.highlight_terms, detailDrawerItem.keywords).length" class="trace-mini-table-wrap drawer-support-table-wrap">
                <div class="trace-mini-title drawer-support-tbl-hdr">
                  {{ uiText.drawerSupportTableLabel }} '{{ at.sheet_name }}'
                </div>
                <table class="data-table trace-mini-table">
                  <tbody>
                    <tr
                      v-for="(wbRow, wrIdx) in getSupportingWorkbookRows(at.assignment_id, at.sheet_name, detailDrawerItem.highlight_terms, detailDrawerItem.keywords)"
                      :key="'dwb-'+wrIdx"
                      :class="{ 'highlighted-support-row': wbRow.matched, 'trace-wb-hdr': wbRow.origIdx <= 2 }"
                    >
                      <td
                        v-for="(wbCell, wcIdx) in wbRow.cells"
                        :key="'dwbc-'+wcIdx"
                        :class="{
                          'bold-cell': wcIdx === 0,
                          'highlighted-support-cell': wbRow.matched && isCellHighlighted(wbCell, detailDrawerItem.highlight_terms, detailDrawerItem.keywords)
                        }"
                      >
                        <span v-if="wbRow.matched && wcIdx === 0" class="support-hit-badge">★ {{ uiText.drawerSupportBadge }}</span>
                        {{ wbCell }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <img
                v-if="at.evidence_img && at.evidence_img !== detailDrawerItem.evidence_img"
                :src="at.evidence_img"
                :alt="at.evidence_caption"
                class="drawer-thumb"
                @click="openLightbox(at.evidence_img, at.assignment_code, at.evidence_caption)"
              />
            </div>
          </div>

          <!-- 5. Matched Lecture Slides (with Highlighted Knowledge Base Table Rows) -->
          <div class="drawer-section">
            <h4 class="drawer-sec-title lecture-sec">🖥️ {{ uiText.drawerLectureTitle }} ({{ detailDrawerItem.matchedLectures.length }})</h4>
            <div v-for="(lt, idx) in detailDrawerItem.matchedLectures" :key="'dl-'+idx" class="drawer-trace-card">
              <div class="trace-item-top">
                <span class="trace-pill lecture-pill">{{ lt.week_label }} | {{ uiText.slideWord }} {{ lt.slide_num }}</span>
                <button class="trace-jump-btn lecture-jump" @click="detailDrawerItem = null; isPresentMode = false; jumpToLectureSlide(lt.week_id, lt.slide_num)">
                  {{ uiText.openWord }} {{ uiText.slideWord }} &rarr;
                </button>
              </div>
              <div v-if="lt.trace_role" class="trace-role-badge lecture-role">{{ lt.trace_role }}</div>
              <p class="trace-mapping-note">{{ lt.mapping_note }}</p>
              <img
                v-if="getLectureSlideObj(lt.week_id, lt.slide_num)"
                :src="getLectureSlideObj(lt.week_id, lt.slide_num).image_url"
                :alt="lt.week_label + ' Slide ' + lt.slide_num"
                class="drawer-thumb"
                @click="openLightbox(getLectureSlideObj(lt.week_id, lt.slide_num).image_url, lt.week_label + ' - Slide ' + lt.slide_num, lt.mapping_note)"
              />

              <!-- Highlighted Lecture Slide Supporting Table -->
              <div
                v-if="getLectureReportObj(lt.week_id, lt.slide_num)?.table_rows"
                class="trace-mini-table-wrap drawer-support-table-wrap"
              >
                <div class="trace-mini-title drawer-support-tbl-hdr">
                  {{ uiText.drawerLectureTableLabel }} {{ getLectureReportObj(lt.week_id, lt.slide_num).title }}
                </div>
                <table class="data-table trace-mini-table">
                  <thead>
                    <tr>
                      <th v-for="(th, hIdx) in getLectureReportObj(lt.week_id, lt.slide_num).table_headers" :key="'dlh-'+hIdx">{{ th }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(lRow, lrIdx) in getLectureReportObj(lt.week_id, lt.slide_num).table_rows"
                      :key="'dlr-'+lrIdx"
                      :class="{ 'highlighted-support-row': isRowHighlighted(lRow, detailDrawerItem.highlight_terms, detailDrawerItem.keywords) }"
                    >
                      <td
                        v-for="(lCell, lcIdx) in lRow"
                        :key="'dlc-'+lcIdx"
                        :class="{
                          'bold-cell': lcIdx === 0,
                          'highlighted-support-cell': isCellHighlighted(lCell, detailDrawerItem.highlight_terms, detailDrawerItem.keywords)
                        }"
                      >
                        <span v-if="lcIdx === 0 && isRowHighlighted(lRow, detailDrawerItem.highlight_terms, detailDrawerItem.keywords)" class="support-hit-badge">★ {{ uiText.drawerSupportBadge }}</span>
                        {{ lCell }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- ================= LIGHTBOX / FULLSCREEN MODAL ================= -->
    <div v-if="lightboxImage" class="lightbox-overlay" @click.self="closeLightbox">
      <div class="lightbox-modal">
        <div class="lightbox-header">
          <div class="lightbox-title-box">
            <span class="lightbox-badge">AUDITED FINANCIAL STATEMENT INSPECTOR</span>
            <h3 class="lightbox-title">{{ lightboxImage.title }}</h3>
          </div>
          <div class="lightbox-controls">
            <button @click="zoomOutLightbox" class="lb-btn" title="Zoom out">−</button>
            <span class="lb-zoom-level">{{ Math.round(lightboxZoom * 100) }}%</span>
            <button @click="zoomInLightbox" class="lb-btn" title="Zoom in">+</button>
            <button @click="resetLightboxZoom" class="lb-btn" title="Reset zoom">Reset</button>
            <button @click="closeLightbox" class="lb-btn lb-close" title="Close (Esc)">✕ Close</button>
          </div>
        </div>
        <div class="lightbox-body">
          <img 
            :src="lightboxImage.src" 
            :alt="lightboxImage.title" 
            class="lightbox-img" 
            :style="{ transform: `scale(${lightboxZoom})`, transformOrigin: 'top center' }"
          />
        </div>
        <div class="lightbox-footer">
          <span class="caption-icon">🔍</span>
          <p>{{ lightboxImage.caption }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: var(--bg-main);
}

/* Sidebar Styles */
.sidebar {
  width: 320px;
  background: var(--bg-sidebar);
  color: #fff;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255,255,255,0.08);
  flex-shrink: 0;
}

.brand {
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 14px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.brand-logo {
  height: 32px;
  filter: brightness(0) invert(1);
}

.brand-text h2 {
  font-size: 15px;
  letter-spacing: 1.5px;
  font-weight: 800;
  color: var(--goto-green);
}

.brand-text p {
  font-size: 11px;
  color: #889988;
}

.search-box {
  padding: 14px 20px;
}

.search-box input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  color: #fff;
  font-size: 13px;
  outline: none;
}

.search-box input:focus {
  border-color: var(--goto-green);
}

/* Sidebar Top Switcher Menu */
.sidebar-top-switcher {
  display: flex;
  margin: 0 16px 8px;
  background: rgba(255, 255, 255, 0.05);
  padding: 3px;
  border-radius: 9px;
  border: 1px solid rgba(255, 255, 255, 0.09);
  gap: 3px;
}

.sidebar-switch-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 7px 8px;
  border: none;
  background: transparent;
  border-radius: 6px;
  color: #8fa094;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.sidebar-switch-btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.06);
}

.sidebar-switch-btn.active.asg-switch {
  background: #2563eb;
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.35);
}

.sidebar-switch-btn.active.slides-switch {
  background: var(--goto-green-dark);
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 127, 42, 0.35);
}

.switcher-badge {
  padding: 1px 5px;
  font-size: 9.5px;
  font-weight: 700;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.lecture-nav {
  flex: 1;
  overflow-y: auto;
  padding: 8px 12px;
}

.nav-section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.2px;
  color: #667766;
  padding: 12px 12px 6px;
}

.nav-item {
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 4px;
  transition: all 0.15s ease;
}

.nav-item:hover {
  background: rgba(255,255,255,0.04);
}

.nav-item.active {
  background: rgba(0, 170, 19, 0.2);
  border-left: 3px solid var(--goto-green);
}

.assignment-nav-item.active {
  background: rgba(37, 99, 235, 0.2);
  border-left: 3px solid #3b82f6;
}

.nav-item-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3px;
}

.week-badge {
  font-size: 11px;
  font-weight: 700;
  color: var(--goto-green);
}

.asg-badge {
  color: #60a5fa;
}

.slide-count-badge {
  font-size: 10px;
  font-weight: 600;
  background: rgba(255,255,255,0.1);
  padding: 2px 6px;
  border-radius: 4px;
  color: #a0b8a4;
}

.category-tag {
  font-size: 10px;
  color: #889988;
  margin-top: 3px;
}

.nav-item-title {
  font-size: 12.5px;
  color: #e0e6e0;
  font-weight: 500;
  line-height: 1.3;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.08);
  font-size: 11px;
  color: #889988;
}

.sidebar-footer span {
  color: #fff;
  font-weight: 600;
}

/* Content Area */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Sleek Top Navigation Bar */
.top-nav {
  height: 58px;
  background: #ffffff;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  gap: 16px;
  flex-shrink: 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.breadcrumb-container {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f8faf9;
  padding: 4px 10px 4px 5px;
  border-radius: 7px;
  border: 1px solid #e5e9e6;
}

.context-badge {
  padding: 3px 8px;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.week-badge-pill {
  background: var(--goto-green-light);
  color: var(--goto-green-dark);
  border: 1px solid #c7ecd0;
}

.asg-badge-pill {
  background: #eff6ff;
  color: #2563eb;
  border: 1px solid #bfdbfe;
}

.crumb-separator {
  color: #cbd5e1;
  font-size: 12px;
}

.crumb-topic {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.segmented-control {
  display: inline-flex;
  align-items: center;
  background: #f1f4f2;
  padding: 3px;
  border-radius: 9px;
  border: 1px solid #e2e8e4;
  gap: 2px;
}

.segmented-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 11px;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #55655b;
  transition: all 0.15s ease-in-out;
  cursor: pointer;
  white-space: nowrap;
}

.segmented-btn:hover {
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.6);
}

.segmented-btn.active {
  background: #ffffff;
  color: var(--goto-green-dark);
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 1px rgba(0, 0, 0, 0.04);
}

.segmented-btn.asg-segmented-btn.active {
  color: #2563eb;
}

.tab-icon {
  flex-shrink: 0;
  opacity: 0.8;
}

.segmented-btn.active .tab-icon {
  opacity: 1;
}

.tab-badge-pill {
  padding: 1px 5px;
  font-size: 10px;
  font-weight: 700;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 9999px;
  margin-left: 1px;
}

.header-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-shrink: 0;
}

.ticker-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 11px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  font-family: var(--font-mono, monospace);
  font-size: 11px;
}

.ticker-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.ticker-name {
  font-weight: 700;
  color: #111827;
}

.ticker-divider {
  width: 1px;
  height: 10px;
  background: #d1d5db;
}

.ticker-audit {
  color: #6b7280;
  font-weight: 500;
}

.scroll-container {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* Banner Styles */
.hero-banner {
  background: linear-gradient(135deg, #0e1e13 0%, #173620 100%);
  color: #fff;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-md);
}

.goto-banner {
  background: linear-gradient(135deg, #004d13 0%, #007f2a 100%);
}

.asg-hero-banner {
  background: linear-gradient(135deg, #0f2744 0%, #1e3a8a 100%);
}

.hero-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.hero-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  background: rgba(0, 170, 19, 0.3);
  color: #6ee787;
  padding: 4px 10px;
  border-radius: 6px;
}

.asg-hero-tag {
  background: rgba(59, 130, 246, 0.3);
  color: #93c5fd;
}

.hero-reading {
  font-size: 12px;
  color: #b0cbb5;
}

.asg-hero-banner .hero-reading {
  color: #bfdbfe;
}

.hero-title {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 12px;
  line-height: 1.25;
}

.goto-subtitle {
  font-size: 13.5px;
  color: #e0e7ff;
  line-height: 1.5;
}

.core-question-box {
  display: flex;
  gap: 12px;
  background: rgba(255,255,255,0.08);
  border-left: 3px solid var(--goto-green);
  padding: 14px 18px;
  border-radius: 8px;
  font-size: 14px;
}

.cq-icon {
  font-size: 18px;
}

/* Horizontal Slide Menu on Top (Assignments) */
.asg-top-slide-container {
  margin-bottom: 24px;
}

.asg-slide-track {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 8px;
  scrollbar-width: thin;
}

.asg-slide-card {
  flex: 0 0 auto;
  width: 220px;
  background: #ffffff;
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  padding: 12px 14px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.asg-slide-card:hover {
  border-color: #93c5fd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
}

.asg-slide-card.active {
  background: #eff6ff;
  border-color: #2563eb;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.15);
}

.slide-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slide-card-code {
  font-size: 11px;
  font-weight: 800;
  color: #2563eb;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.slide-card-week {
  font-size: 10.5px;
  font-weight: 600;
  color: var(--text-muted);
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
}

.slide-card-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}



/* Assignments Hero KPI Pills & Quick-Jump Bar */
.asg-kpi-badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.asg-kpi-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 11.5px;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.14);
  color: #f8fafc;
  border: 1px solid rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(4px);
}

.asg-kpi-pill-green {
  background: rgba(16, 185, 129, 0.22);
  color: #a7f3d0;
  border-color: rgba(52, 211, 153, 0.4);
}

.asg-kpi-pill-muted {
  background: rgba(15, 23, 42, 0.45);
  color: #cbd5e1;
  border-color: rgba(148, 163, 184, 0.3);
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 11px;
}

.asg-sec-toc-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin: 4px 0 22px 0;
  padding: 12px 16px;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.asg-toc-label {
  font-size: 11.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #475569;
  margin-right: 4px;
}

.asg-toc-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 11px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #1e293b;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.16s ease;
  max-width: 260px;
}

.asg-toc-btn:hover {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #1d4ed8;
  transform: translateY(-1px);
}

.asg-toc-wb-btn {
  background: #0f172a;
  color: #f8fafc;
  border-color: #0f172a;
}

.asg-toc-wb-btn:hover {
  background: #047857;
  border-color: #047857;
  color: #ffffff;
}

.asg-toc-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1px 5px;
  border-radius: 4px;
  background: #e2e8f0;
  color: #334155;
  font-size: 10px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.asg-toc-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Workbook Card Styles */
.workbook-card {
  margin-bottom: 28px;
  border: 1.5px solid #cbd5e1;
  padding: 0;
  overflow: hidden;
  scroll-margin-top: 20px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
}

.wb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 22px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #ffffff;
  flex-wrap: wrap;
  gap: 14px;
}

.wb-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.wb-icon {
  font-size: 22px;
}

.wb-title-group h3 {
  font-size: 14.5px;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
}

.wb-subtitle {
  font-size: 11.5px;
  color: #94a3b8;
  margin-top: 2px;
}

.sheet-tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.sheet-tab-btn {
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: rgba(255, 255, 255, 0.08);
  font-size: 11.5px;
  font-weight: 700;
  color: #e2e8f0;
  cursor: pointer;
  transition: all 0.15s ease;
}

.sheet-tab-btn:hover {
  background: rgba(255, 255, 255, 0.18);
  color: #ffffff;
}

.sheet-tab-btn.active {
  background: #00aa13;
  color: #ffffff;
  border-color: #00aa13;
  box-shadow: 0 2px 8px rgba(0, 170, 19, 0.35);
}

.wb-table-wrap {
  overflow-x: auto;
  max-height: 520px;
  background: #ffffff;
}

.wb-data-table {
  width: 100%;
  font-size: 12px;
  border-collapse: collapse;
}

.wb-data-table td {
  padding: 8px 13px;
  border-bottom: 1px solid #e2e8f0;
  border-right: 1px solid #f1f5f9;
  color: #1e293b;
  vertical-align: middle;
}

.wb-data-table td.num-cell {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-family: 'SFMono-Regular', Consolas, monospace;
  white-space: nowrap;
}

.wb-data-table td.text-data-cell {
  white-space: normal;
  min-width: 150px;
  max-width: 360px;
  line-height: 1.4;
}

.wb-title-banner-row td {
  background: #f8fafc;
  font-size: 13px;
  font-weight: 800;
  color: #0f172a;
  padding: 11px 14px;
  border-bottom: 2px solid #cbd5e1;
}

.wb-col-header-row {
  position: sticky;
  top: 0;
  z-index: 3;
}

.wb-col-header-row td {
  background: #0f172a;
  color: #f8fafc !important;
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.02em;
  border-bottom: 2px solid #334155;
  border-right-color: #1e293b;
}

.wb-section-divider-row td {
  background: #eff6ff;
  color: #1e40af !important;
  font-weight: 800;
  font-size: 11.5px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 8px 13px;
  border-top: 1.5px solid #bfdbfe;
  border-bottom: 1.5px solid #bfdbfe;
}

.wb-total-row td {
  background: #f0fdf4;
  font-weight: 800;
  color: #064e3b !important;
  border-top: 1.5px solid #86efac;
  border-bottom: 1.5px solid #86efac;
}

/* Assignment Sections Stream */
.asg-sections-stream {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.asg-section-card {
  padding: 24px 28px;
  border: 1.5px solid #cbd5e1;
  border-left: 5px solid #1e3a8a;
  border-radius: 14px;
  scroll-margin-top: 20px;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
}

.sec-card-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1.5px solid #e2e8f0;
}

.sec-heading-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sec-num-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: linear-gradient(135deg, #0f2744 0%, #2563eb 100%);
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  flex-shrink: 0;
}

.sec-card-heading {
  font-size: 17px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  padding: 0;
  border: none;
  line-height: 1.3;
}

.sec-cite-pill {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 6px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  font-size: 11px;
  color: #334155;
  max-width: 100%;
}

.sec-paragraphs {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sec-paragraph-text {
  font-size: 13.5px;
  line-height: 1.65;
  color: #1e293b;
  background: #f8fafc;
  border-left: 3px solid #cbd5e1;
  padding: 10px 14px;
  border-radius: 0 8px 8px 0;
  margin: 0;
}

/* Institutional Section Financial Table */
.asg-fin-table-card {
  margin-top: 18px;
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}

.asg-fin-table-topbar {
  padding: 7px 14px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.asg-fin-table-badge {
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.04em;
  color: #334155;
}

.asg-fin-table-scroll {
  overflow-x: auto;
}

.asg-fin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}

.asg-fin-table thead th {
  background: #0f172a;
  color: #f8fafc;
  padding: 10px 14px;
  font-size: 11.5px;
  font-weight: 800;
  letter-spacing: 0.02em;
  border-right: 1px solid #1e293b;
  white-space: nowrap;
}

.asg-fin-table thead th.th-left {
  text-align: left;
}

.asg-fin-table thead th.th-right {
  text-align: right;
}

.asg-fin-table tbody tr {
  transition: background-color 0.12s ease;
}

.asg-fin-table tbody tr:nth-child(even) {
  background: #fafbfd;
}

.asg-fin-table tbody tr:hover {
  background: #f0f9ff;
}

.asg-fin-table tbody td {
  padding: 9px 14px;
  border-bottom: 1px solid #e2e8f0;
  border-right: 1px solid #f1f5f9;
  color: #1e293b;
  vertical-align: top;
  line-height: 1.45;
}

.asg-fin-table tbody td.bold-cell {
  font-weight: 700;
  color: #0f172a;
  min-width: 190px;
}

.asg-fin-table tbody td.num-cell {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-family: 'SFMono-Regular', Consolas, monospace;
  white-space: nowrap;
}

.asg-fin-table tbody td.text-data-cell {
  text-align: left;
  min-width: 150px;
}

.fin-subheader-row td {
  background: #eff6ff !important;
  color: #1e40af !important;
  font-weight: 800 !important;
  font-size: 11px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 7px 14px !important;
  border-top: 1.5px solid #bfdbfe !important;
  border-bottom: 1.5px solid #bfdbfe !important;
}

.fin-total-row td {
  background: #ecfdf5 !important;
  font-weight: 800 !important;
  color: #064e3b !important;
  border-top: 1.5px solid #6ee7b7 !important;
  border-bottom: 2px solid #10b981 !important;
}

.fin-ratio-row td {
  background: #fffbeb !important;
  font-weight: 700;
  color: #78350f !important;
  border-bottom: 1px solid #fde68a !important;
}

.neg-val-cell {
  color: #be123c !important;
  font-weight: 700;
}

.pos-growth-cell {
  color: #047857 !important;
  font-weight: 700;
}

/* Audited LK Visual Evidence Card inside Assignment Section */
.asg-evidence-card {
  margin-top: 18px;
  border: 1.5px solid #bfdbfe;
  border-radius: 12px;
  overflow: hidden;
  background: #f8fafc;
}

.asg-evidence-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px 14px;
  background: #eff6ff;
  border-bottom: 1px solid #dbeafe;
}

.asg-proof-badge {
  font-size: 11px;
  font-weight: 800;
  color: #1e3a8a;
  letter-spacing: 0.03em;
}

.asg-proof-zoom {
  font-size: 11px;
  font-weight: 600;
  color: #2563eb;
}

.asg-evidence-body {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 12px 14px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.asg-evidence-body:hover {
  background: #f0f9ff;
}

.asg-evidence-thumb {
  width: 190px;
  max-height: 120px;
  object-fit: cover;
  object-position: top center;
  border-radius: 8px;
  border: 1.5px solid #94a3b8;
  background: #ffffff;
  flex-shrink: 0;
}

.asg-evidence-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.asg-evidence-caption {
  font-size: 12.5px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.45;
}

.asg-evidence-cite {
  font-size: 11.5px;
  color: #475569;
  font-family: 'SFMono-Regular', Consolas, monospace;
}

/* Slides Stream */
.slides-stream {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.slide-entry-card {
  background: #fff;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-md);
}

.slide-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-light);
}

.slide-number-pill {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1px;
  color: var(--goto-green-dark);
  background: var(--goto-green-light);
  padding: 3px 8px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 6px;
}

.slide-main-header {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.3;
}

.slide-sub-pill {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  background: #f1f5f2;
  padding: 4px 10px;
  border-radius: 6px;
}

/* Slide Image Wrapper */
.slide-image-wrapper {
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.12);
  margin-bottom: 20px;
  border: 1px solid #e0e6e0;
}

.actual-slide-image {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

/* Dual Explanation Columns */
.slide-dual-explanation {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

@media (max-width: 900px) {
  .slide-dual-explanation {
    grid-template-columns: 1fr;
  }
}

.exp-col {
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

.theory-col {
  background: #f8faf9;
  border-left: 4px solid #2563eb;
}

.goto-col {
  background: #f5fbf6;
  border-left: 4px solid var(--goto-green);
}

.exp-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.exp-icon {
  font-size: 16px;
}

.exp-header h3 {
  font-size: 14px;
  font-weight: 700;
}

.theory-col h3 { color: #1e40af; }
.goto-col h3 { color: var(--goto-green-dark); }

.exp-body {
  font-size: 13.5px;
  line-height: 1.6;
  color: var(--text-main);
}

/* Embedded GoTo Report Container */
.goto-report-container {
  background: #fafffb;
  border: 1.5px solid #a7f3d0;
  border-radius: 14px;
  padding: 24px;
  margin-top: 10px;
}

.report-header-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #a7f3d0;
}

.report-badge {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  color: #047857;
  background: #d1fae5;
  padding: 3px 8px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.report-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--goto-green-dark);
}

.report-org-tag {
  font-size: 11px;
  font-weight: 700;
  color: #065f46;
  background: #ecfdf5;
  padding: 4px 10px;
  border-radius: 6px;
}

.report-desc-text {
  font-size: 13.5px;
  line-height: 1.6;
  color: var(--text-main);
  margin-bottom: 14px;
}

/* Audit Evidence Styles */
.audit-evidence-container {
  background: #fff;
  border: 1.5px solid #93c5fd;
  border-radius: 14px;
  padding: 22px;
  margin-top: 18px;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.06);
}

.evidence-header-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #bfdbfe;
  flex-wrap: wrap;
  gap: 10px;
}

.evidence-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.evidence-badge {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  color: #1d4ed8;
  background: #dbeafe;
  padding: 3px 8px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 4px;
}

.evidence-title {
  font-size: 15px;
  font-weight: 800;
  color: #1e3a8a;
}

.evidence-key-figures-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 16px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.evidence-kf-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 12px;
  color: #334155;
}

.evidence-kf-pill .kf-label {
  color: #64748b;
  font-weight: 500;
}

.evidence-kf-pill .kf-val {
  color: #0f172a;
  font-weight: 700;
}

.evidence-kf-pill .kf-ref {
  color: #2563eb;
  font-size: 11px;
  font-weight: 600;
}

.evidence-source-tag {
  font-size: 11px;
  font-weight: 700;
  color: #1e40af;
  background: #eff6ff;
  padding: 5px 10px;
  border-radius: 6px;
  border: 1px solid #bfdbfe;
}

.evidence-zoom-btn, .evidence-modal-btn {
  font-size: 11px;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid #93c5fd;
  background: #ffffff;
  color: #1d4ed8;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.evidence-zoom-btn:hover, .evidence-modal-btn:hover {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #1e40af;
}

.evidence-zoom-btn.active {
  background: #2563eb;
  color: #ffffff;
  border-color: #1d4ed8;
}

/* Native High-Visibility FSA Key Metric Cards */
.evidence-kpi-summary-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.kpi-callout {
  padding: 14px 16px;
  border-radius: 12px;
  border: 1.5px solid;
  display: flex;
  flex-direction: column;
  gap: 5px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}

.kpi-green {
  background: #f0fdf4;
  border-color: #86efac;
}

.kpi-amber {
  background: #fffbeb;
  border-color: #fcd34d;
}

.kpi-red {
  background: #fef2f2;
  border-color: #fca5a5;
}

.kpi-head {
  display: flex;
  align-items: center;
  gap: 8px;
}

.kpi-tag {
  font-size: 9.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  padding: 2px 7px;
  border-radius: 4px;
  color: #ffffff;
}

.kpi-green .kpi-tag { background: #16a34a; }
.kpi-amber .kpi-tag { background: #d97706; }
.kpi-red .kpi-tag { background: #dc2626; }

.kpi-name {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.6px;
}

.kpi-green .kpi-name { color: #15803d; }
.kpi-amber .kpi-name { color: #b45309; }
.kpi-red .kpi-name { color: #b91c1c; }

.kpi-number {
  font-size: 26px;
  font-weight: 900;
  line-height: 1.15;
  letter-spacing: -0.5px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.kpi-green .kpi-number { color: #15803d; }
.kpi-amber .kpi-number { color: #b45309; }
.kpi-red .kpi-number { color: #b91c1c; }

.kpi-formula {
  font-size: 12px;
  color: #475569;
  line-height: 1.35;
}

.kpi-formula strong {
  color: #0f172a;
}

.evidence-image-wrapper {
  background: #f8fafc;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #cbd5e1;
  max-height: 520px;
  overflow-y: auto;
  position: relative;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.04);
  transition: all 0.2s ease;
}

.evidence-image-wrapper.actual-size-mode {
  max-height: 680px;
  overflow: auto;
}

.image-click-hint {
  position: absolute;
  top: 8px;
  right: 12px;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(4px);
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
  opacity: 0.85;
  transition: opacity 0.2s;
  z-index: 10;
}

.evidence-image-wrapper:hover .image-click-hint {
  opacity: 1;
}

.actual-statement-image {
  width: 100%;
  height: auto;
  display: block;
  cursor: zoom-in;
}

.actual-statement-image.image-full-width {
  width: auto;
  min-width: 1500px;
  max-width: none;
  cursor: zoom-out;
}

/* Fullscreen / Lightbox Modal Styles */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(8px);
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.lightbox-modal {
  background: #ffffff;
  border-radius: 16px;
  width: 96vw;
  max-width: 1500px;
  height: 94vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 25px 60px -15px rgba(0,0,0,0.5);
}

.lightbox-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.lightbox-badge {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  color: #1e40af;
  background: #dbeafe;
  padding: 2px 7px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 2px;
}

.lightbox-title {
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
}

.lightbox-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.lb-btn {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #334155;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.lb-btn:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
}

.lb-zoom-level {
  font-size: 12px;
  font-weight: 800;
  color: #64748b;
  min-width: 44px;
  text-align: center;
}

.lb-btn.lb-close {
  background: #ef4444;
  color: #ffffff;
  border-color: #dc2626;
  margin-left: 6px;
}

.lb-btn.lb-close:hover {
  background: #dc2626;
}

.lightbox-body {
  flex: 1;
  overflow: auto;
  padding: 24px;
  background: #f1f5f9;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.lightbox-img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
  transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: grab;
}

.lightbox-footer {
  padding: 12px 20px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #334155;
}

.evidence-caption-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #eff6ff;
  border-left: 4px solid #2563eb;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 12px;
  font-size: 13px;
  color: #1e3a8a;
}

/* ================= WEEK 4 SLIDE 4 LECTURE TREND CHART ================= */
.lecture-chart-card {
  margin-bottom: 20px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.chart-card-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding: 14px 18px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.chart-heading-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.chart-pill-badge {
  display: inline-block;
  align-self: flex-start;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #c26d58;
  background: #fff1ee;
  border: 1px solid #ffd5cc;
  padding: 2px 8px;
  border-radius: 12px;
}

.chart-main-title {
  margin: 4px 0 0;
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
}

.chart-sub-title {
  margin: 0;
  font-size: 12px;
  color: #64748b;
}

.chart-entity-tabs {
  display: flex;
  gap: 6px;
  background: #e2e8f0;
  padding: 3px;
  border-radius: 6px;
}

.chart-tab-btn {
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  border: none;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.chart-tab-btn:hover {
  color: #0f172a;
}

.chart-tab-btn.active {
  background: #ffffff;
  color: #1e3a5f;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
}

.chart-card-body {
  display: grid;
  grid-template-columns: 1fr 310px;
  gap: 20px;
  padding: 18px 20px;
  background: #ffffff;
}

@media (max-width: 900px) {
  .chart-card-body {
    grid-template-columns: 1fr;
  }
}

.chart-svg-column {
  display: flex;
  flex-direction: column;
}

.chart-y-axis-label {
  font-size: 11px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 4px;
  padding-left: 10px;
}

.svg-container {
  width: 100%;
}

.trend-svg {
  display: block;
  width: 100%;
  height: auto;
  background: #ffffff;
}

.grid-lines line {
  stroke-dasharray: 2 2;
}

.axis-tick {
  font-size: 11px;
  fill: #64748b;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.x-axis-label {
  font-size: 12px;
  font-weight: 600;
  fill: #334155;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.chart-point {
  cursor: pointer;
  transition: r 0.15s ease;
}

.chart-point:hover {
  r: 7.5;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25));
}

.point-label {
  font-size: 12px;
  font-weight: 700;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.slate-label {
  fill: #1e3a5f;
}

.emerald-label {
  fill: #059669;
}

.crimson-label {
  fill: #dc2626;
}

.chart-legend-row {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 18px;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid #f1f5f9;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
}

.legend-line {
  width: 18px;
  height: 3px;
  border-radius: 2px;
}

.slate-line { background: #1e3a5f; }
.emerald-line { background: #10b981; }
.crimson-line { 
  background: #ef4444; 
  background-image: linear-gradient(to right, #ef4444 50%, transparent 50%);
  background-size: 6px 100%;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-left: -10px;
}

.slate-dot { background: #1e3a5f; }
.emerald-dot { background: #10b981; }
.crimson-dot { background: #ef4444; }

/* Right Column "Notice" Card - Exact match to Lecture Slide 4 */
.chart-notice-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  background: #fbfbfc;
  border: 1px solid #e8ecef;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.notice-title {
  font-size: 17px;
  font-weight: 700;
  color: #b45309; /* warm gold / amber */
  margin-bottom: 12px;
}

.notice-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
  font-size: 13.5px;
  line-height: 1.5;
  color: #334155;
}

.notice-paragraph strong {
  color: #0f172a;
}

.notice-punchline {
  margin: 18px 0 10px;
  font-size: 17px;
  font-weight: 800;
  color: #c2410c; /* coral red / terracotta */
  letter-spacing: -0.01em;
}

.notice-footnote {
  font-size: 11px;
  color: #94a3b8;
  border-top: 1px solid #edf2f7;
  padding-top: 8px;
  margin-top: auto;
}

/* ================= EFFICIENT DIVERSIFICATION TABLE & FORMULA BAR DESIGN ================= */
.worksheet-formula-bar { 
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px; 
  background: #f0f4f8; 
  border-radius: 6px; 
  font-size: 0.85rem; 
  margin-bottom: 12px;
  border: 1px solid #d4dfe6;
  min-height: 70px;
  max-height: 70px;
  box-sizing: border-box;
  overflow: hidden;
}

.worksheet-formula-bar.worksheet-active { 
  background: #edf4f8; 
  border-color: #315c74;
}

.formula-bar-top {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.worksheet-cell-ref { 
  background: #fff; 
  border-radius: 4px; 
  padding: 2px 8px; 
  text-align: center; 
  font-weight: 700; 
  color: #254459; 
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  border: 1px solid #d4dfe6;
  font-size: 0.82rem;
  flex-shrink: 0;
  min-width: 38px;
}

.worksheet-formula-bar.worksheet-active .worksheet-cell-ref { 
  color: #315c74; 
  border-color: #315c74;
}

.worksheet-fx { 
  color: #61717d; 
  font-style: italic; 
  font-weight: 700; 
  text-align: center; 
  font-family: Georgia, serif;
  font-size: 0.95rem;
  flex-shrink: 0;
}

.worksheet-formula-bar code { 
  display: block; 
  flex: 1;
  min-width: 0; 
  background: #fff; 
  border-radius: 4px; 
  padding: 4px 8px; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis;
  line-height: 1.4; 
  font-weight: 600; 
  color: #123b57; 
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.84rem;
  border: 1px solid #d4dfe6;
}

.worksheet-formula-bar.worksheet-active code { 
  background: #dceaf1; 
  color: #123b57; 
  border-color: #315c74;
}

.formula-bar-bottom {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  padding-left: 2px;
}

.formula-val-tag {
  color: #61717d;
  font-weight: 600;
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  flex-shrink: 0;
}

.formula-val-display {
  font-weight: 800;
  color: #123b57;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.88rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.val-table-wrap {
  overflow-x: auto;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #d4dfe6;
  background: #ffffff;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 13px;
  color: #24313d;
}

/* Worksheet Table Column Letters Header */
.worksheet-letters th { 
  background: #f4f6f7; 
  color: #6a7883; 
  font-size: 0.72rem; 
  padding: 4px 8px; 
  text-align: center; 
  font-weight: 600;
  border-right: 1px solid #d4dfe6;
  border-bottom: 1px solid #d4dfe6;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

/* Row Number indicator on left */
.row-num-th {
  width: 2.4rem;
  min-width: 2.4rem;
  max-width: 2.4rem;
  text-align: center;
  font-weight: 600;
  background: #f0f3f5 !important;
  color: #61717d !important;
  font-size: 0.75rem;
  padding: 6px 4px !important;
  border-right: 1px solid #d4dfe6 !important;
  border-bottom: 1px solid #d4dfe6 !important;
  user-select: none;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.data-table th {
  background: #edf2f4;
  color: #354b5d;
  font-weight: 700;
  padding: 9px 12px;
  border-right: 1px solid #d4dfe6;
  border-bottom: 1px solid #d4dfe6;
  text-align: left;
}

.data-table th:last-child {
  border-right: none;
}

.data-table td {
  border-right: 1px solid #eef2f5;
  border-bottom: 1px solid #eef2f5;
  padding: 8px 12px;
  vertical-align: middle;
  transition: background 0.12s ease, box-shadow 0.12s ease;
  cursor: pointer;
}

.data-table td:last-child {
  border-right: none;
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.data-table tbody tr:nth-child(even) {
  background: #fafbfc;
}

.data-table tbody tr:hover {
  background: #f0f4f8;
}

.data-table td.bold-cell {
  font-weight: 600;
  color: #254459;
}

.data-table td.num-cell {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

/* Cell Lighting Up on Hover (Efficient Diversification Inspired - Zero Jitter) */
.data-table td.is-cell-lit {
  background: #dceaf1 !important;
  color: #123b57 !important;
  box-shadow: inset 0 0 0 2px #315c74 !important;
}

.data-table tr.is-row-lit td {
  background: #edf4f8;
}

.data-table tr.is-row-lit td.bold-cell {
  color: #123b57;
}

/* Formula Sources & Selected Highlighting */
.data-table td.worksheet-used {
  background: #e6f0f7 !important;
  box-shadow: inset 0 0 0 1.5px #5280a0 !important;
}

.data-table td.worksheet-selected {
  background: #c3dce9 !important;
  color: #123b57 !important;
  box-shadow: inset 0 0 0 2px #315c74 !important;
}


/* Empirical Note Card (Clean Slate Style) */
.gap-expl-box {
  background: #f7f9fa;
  border: 1px solid #d4dfe6;
  border-left: 4px solid #315c74;
  border-radius: 6px;
  padding: 14px 16px;
  font-size: 13px;
  color: #24313d;
  line-height: 1.6;
}

.gap-expl-box h3 {
  font-size: 13px;
  font-weight: 700;
  color: #123b57;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.gap-expl-box .expl-hint {
  font-size: 11px;
  font-weight: 500;
  color: #64748b;
  margin-left: 4px;
}

.gap-expl-box p {
  margin: 0;
  line-height: 1.65;
}

/* Interactive Reference Chips in Note */
.ref-chip {
  display: inline-block;
  padding: 1px 5px;
  margin: 0 1px;
  border-radius: 4px;
  background: #eef2f4;
  color: #254459;
  font-weight: 700;
  border-bottom: 1.5px dashed #5280a0;
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: var(--font-mono);
  font-size: 0.94em;
}

.ref-chip:hover, .ref-chip.is-active {
  background: #ccdde7;
  color: #123b57;
  border-bottom-style: solid;
  border-bottom-color: #123b57;
  box-shadow: 0 2px 6px rgba(37, 68, 89, 0.2);
}


/* Cost of Capital & Metrics Grid */
.coc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.coc-item {
  background: #fff;
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 14px;
  display: flex;
  flex-direction: column;
}

.coc-lbl {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.coc-val {
  font-family: var(--font-mono);
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
}

.coc-sub-text {
  font-size: 10.5px;
  color: var(--text-muted);
  margin-top: 4px;
}

.highlight-green {
  background: #f0fdf4;
  border-color: #86efac;
}

.highlight-green .coc-val {
  color: var(--goto-green-dark);
}

/* GoTo Models Card */
.content-cards {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card {
  background: #fff;
  border-radius: 14px;
  padding: 28px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 4px;
}

.card-subtitle {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.forces-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.force-card {
  padding: 18px 22px;
  background: #f9fbf9;
  border-radius: 10px;
  border: 1px solid var(--border-light);
}

.force-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.force-name {
  font-weight: 700;
  font-size: 15px;
  color: var(--text-main);
}

.rating-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
}

.badge-high {
  background: #fef2f2;
  color: #dc2626;
}

.badge-med {
  background: #fffbeb;
  color: #d97706;
}

.force-text {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* Takeaways Deck */
.takeaways-deck {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.takeaway-card {
  display: flex;
  gap: 20px;
  background: #fff;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.takeaway-num {
  font-size: 32px;
  font-weight: 800;
  color: var(--goto-green);
  line-height: 1;
}

.takeaway-body h3 {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 6px;
}

.takeaway-body p {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* Roadmap Timeline */
.roadmap-timeline {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.roadmap-node {
  display: flex;
  gap: 20px;
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s;
}

.roadmap-node:hover {
  transform: translateX(6px);
  border-color: var(--goto-green);
}

.roadmap-node.current {
  border-left: 5px solid var(--goto-green);
  background: #f6fcf7;
}

.node-badge {
  font-size: 14px;
  font-weight: 800;
  color: var(--goto-green-dark);
  min-width: 70px;
}

.node-cat {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 4px;
}

.node-content h3 {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 6px;
}

.node-content p {
  font-size: 13px;
  color: var(--text-muted);
}

/* ================= WEB PRESENTATION & TRACEABILITY STYLES ================= */
.sidebar-switch-btn.active.pres-switch {
  background: linear-gradient(135deg, #00aa13, #047857);
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 170, 19, 0.35);
}

.pres-badge {
  background: #00aa13 !important;
  color: #ffffff !important;
}

.apx-badge {
  background: #475569 !important;
  color: #ffffff !important;
}

.pres-badge-pill {
  background: #00aa13;
  color: #fff;
}

.pres-segmented-btn.active {
  background: linear-gradient(135deg, #0f172a, #1e293b) !important;
  color: #4ade80 !important;
}

.pres-pill {
  background: #00aa13 !important;
  color: #fff !important;
}

.pres-tab-pane {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.pres-controls-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: #fff;
  padding: 12px 18px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.pres-nav-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pres-nav-btn {
  padding: 7px 14px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #0f172a;
  font-weight: 700;
  font-size: 12.5px;
  cursor: pointer;
}

.pres-nav-btn:hover:not(:disabled) {
  background: #0f172a;
  color: #fff;
  border-color: #0f172a;
}

.pres-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pres-counter-pill {
  font-weight: 800;
  font-size: 12.5px;
  color: #0f172a;
  padding: 0 6px;
}

.pres-slide-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.pres-dot-btn {
  width: 30px;
  height: 28px;
  border-radius: 7px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  font-size: 11px;
  font-weight: 700;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s;
}

.pres-dot-btn.apx {
  background: #f1f5f9;
  color: #64748b;
}

.pres-dot-btn.active {
  background: #00aa13;
  color: #fff;
  border-color: #00aa13;
  box-shadow: 0 2px 6px rgba(0, 170, 19, 0.3);
}

.pres-meta-pills {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pres-time-badge, .pres-pts-badge {
  font-size: 11.5px;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 9999px;
  background: #f1f5f9;
  color: #0f172a;
}

.pres-notes-toggle {
  padding: 5px 12px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #fff;
  font-size: 11.5px;
  font-weight: 700;
  color: #334155;
  cursor: pointer;
}

.pres-notes-toggle:hover {
  background: #f8fafc;
}

/* 16:9 Slide Canvas */
.pres-canvas {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  border: 2px solid #0f172a;
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.14);
  display: flex;
  flex-direction: column;
}

.pres-slide-header {
  background: #0f172a;
  color: #ffffff;
  padding: 22px 28px 18px;
}

.pres-header-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.pres-section-tag {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.9px;
  text-transform: uppercase;
  color: #4ade80;
}

.pres-slide-index {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
}

.pres-action-title {
  font-size: 22px;
  font-weight: 800;
  line-height: 1.28;
  color: #ffffff;
  margin-bottom: 6px;
}

.pres-slide-subtitle {
  font-size: 13px;
  color: #cbd5e1;
}

.pres-emerald-bar {
  height: 5px;
  background: linear-gradient(90deg, #00aa13, #10b981);
}

.pres-slide-body {
  padding: 24px 28px;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.pres-kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}

.pres-kpi-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px 16px;
  text-align: center;
  border-top: 4px solid #0f172a;
}

.pres-kpi-card.tone-emerald { border-top-color: #00aa13; }
.pres-kpi-card.tone-red { border-top-color: #dc2626; }
.pres-kpi-card.tone-blue { border-top-color: #2563eb; }
.pres-kpi-card.tone-amber { border-top-color: #d97706; }

.pres-kpi-val {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 4px;
}

.pres-kpi-card.tone-emerald .pres-kpi-val { color: #047857; }
.pres-kpi-card.tone-red .pres-kpi-val { color: #dc2626; }
.pres-kpi-card.tone-blue .pres-kpi-val { color: #1d4ed8; }
.pres-kpi-card.tone-amber .pres-kpi-val { color: #b45309; }

.pres-kpi-lbl {
  font-size: 12px;
  font-weight: 700;
  color: #0f172a;
}

.pres-kpi-sub {
  font-size: 11px;
  color: #64748b;
  margin-top: 2px;
}

.pres-content-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.pres-chart-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px;
  text-align: center;
}

.pres-chart-toolbar {
  margin-bottom: 8px;
}

.pres-chart-badge {
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.7px;
  color: #047857;
  background: #ecfdf5;
  padding: 4px 10px;
  border-radius: 9999px;
}

.pres-chart-img {
  max-width: 100%;
  max-height: 410px;
  object-fit: contain;
  border-radius: 8px;
  cursor: zoom-in;
}

.pres-table-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
}

.pres-table-title {
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 10px;
}

.pres-cards-col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 14px;
}

.pres-info-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-left: 5px solid #0f172a;
  border-radius: 10px;
  padding: 16px 18px;
}

.pres-info-card.card-tone-emerald { border-left-color: #00aa13; }
.pres-info-card.card-tone-red { border-left-color: #dc2626; }
.pres-info-card.card-tone-amber { border-left-color: #d97706; background: #fffbeb; }

.pres-card-title {
  font-size: 14px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 10px;
}

.pres-card-bullets {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.pres-card-bullets li {
  font-size: 13px;
  line-height: 1.48;
  color: #334155;
}

.pres-slide-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 11px 28px;
  background: #f1f5f9;
  border-top: 1px solid #e2e8f0;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
}

.pres-speaker-box {
  background: #0f172a;
  color: #e2e8f0;
  padding: 14px 20px;
  border-radius: 12px;
  border-left: 5px solid #4ade80;
  font-size: 13px;
  line-height: 1.5;
}

.speaker-tag {
  font-weight: 800;
  color: #4ade80;
  display: block;
  margin-bottom: 4px;
  font-size: 11.5px;
}

/* Dual Traceability Inspector & Visual Separation */
.slide-vs-info-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 14px 0 6px;
}

.divider-line {
  flex: 1;
  height: 0;
  border-top: 2px dashed #94a3b8;
}

.divider-pill {
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.7px;
  color: #475569;
  background: #e2e8f0;
  padding: 5px 14px;
  border-radius: 9999px;
  border: 1px solid #cbd5e1;
  white-space: nowrap;
}

.audit-drawer-wrapper {
  background: #e8edf4;
  border: 2px solid #cbd5e1;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.drawer-scope-tag {
  display: inline-block;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  color: #ffffff;
  background: #334155;
  padding: 3px 10px;
  border-radius: 6px;
  margin-bottom: 6px;
}

.traceability-banner {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-left: 5px solid #334155;
  border-radius: 10px;
  padding: 14px 18px;
}

.trace-banner-title h2 {
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 3px;
}

.trace-banner-title p {
  font-size: 12.5px;
  color: #475569;
}

.traceability-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  align-items: start;
}

@media (max-width: 1100px) {
  .traceability-columns {
    grid-template-columns: 1fr;
  }
}

.trace-col {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.trace-col-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  color: #ffffff;
}

.trace-col-header.lecture-hdr {
  background: linear-gradient(135deg, #047857, #065f46);
}

.trace-col-header.asg-hdr {
  background: linear-gradient(135deg, #1d4ed8, #1e40af);
}

.trace-col-icon {
  font-size: 22px;
}

.trace-col-header h3 {
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.6px;
}

.trace-col-header p {
  font-size: 11.5px;
  opacity: 0.9;
}

.trace-item-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.trace-item-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.trace-pill {
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 9999px;
}

.lecture-pill {
  background: #dcfce7;
  color: #166534;
}

.asg-pill {
  background: #dbeafe;
  color: #1e40af;
}

.trace-jump-btn {
  padding: 6px 12px;
  border-radius: 7px;
  border: none;
  font-size: 11.5px;
  font-weight: 700;
  cursor: pointer;
  color: #ffffff;
}

.lecture-jump {
  background: #059669;
}

.lecture-jump:hover {
  background: #047857;
}

.asg-jump {
  background: #2563eb;
}

.asg-jump:hover {
  background: #1d4ed8;
}

.trace-cell-ref {
  font-size: 12px;
  color: #1e293b;
  background: #f8fafc;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.trace-mapping-note {
  font-size: 12.5px;
  line-height: 1.5;
  color: #334155;
}

.trace-slide-meta {
  font-size: 12px;
  color: #0f172a;
}

.trace-thumb-row, .trace-evidence-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.trace-ev-label {
  font-size: 11px;
  color: #1e293b;
  font-weight: 600;
}

.trace-ev-label span {
  color: #1d4ed8;
  font-weight: 800;
}

.trace-slide-thumb, .trace-ev-thumb {
  width: 100%;
  max-height: 220px;
  object-fit: contain;
  border-radius: 6px;
  cursor: zoom-in;
  background: #ffffff;
}

.trace-mini-table-wrap {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow-x: auto;
  background: #ffffff;
}

.trace-mini-title {
  background: #f1f5f9;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 800;
  color: #0f172a;
  border-bottom: 1px solid #e2e8f0;
}

.trace-mini-table {
  font-size: 11px !important;
}

.trace-mini-table th, .trace-mini-table td {
  padding: 5px 8px !important;
}

.trace-wb-hdr td {
  background: #eff6ff !important;
  font-weight: 700;
  color: #1e3a8a;
}

.mode-context-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #0f172a;
}

.mode-context-pill.pres-context {
  background: #ecfdf5;
  border-color: #a7f3d0;
  color: #065f46;
}

.mode-context-pill.asg-context {
  background: #eff6ff;
  border-color: #bfdbfe;
  color: #1e40af;
}

.mode-dot {
  width: 8px;
  height: 8px;
  border-radius: 9999px;
}

.pres-dot { background: #00aa13; }
.asg-dot { background: #2563eb; }

/* Browser-Viewport Presentation Mode */
.pres-present-btn {
  padding: 6px 14px;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #00aa13, #047857);
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 170, 19, 0.35);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}

.pres-present-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 170, 19, 0.45);
}

.present-overlay {
  position: fixed;
  inset: 0;
  z-index: 900;
  background: #0b1120;
  display: flex;
  flex-direction: column;
  padding: 14px 22px 18px;
  gap: 12px;
}

.present-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.present-top-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.present-mode-badge {
  background: #00aa13;
  color: #ffffff;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  padding: 4px 10px;
  border-radius: 9999px;
}

.present-slide-counter {
  color: #f8fafc;
  font-size: 13px;
  font-weight: 800;
}

.present-section-lbl {
  color: #94a3b8;
  font-size: 12.5px;
  font-weight: 600;
}

.present-top-dots {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.present-dot {
  width: 26px;
  height: 24px;
  border-radius: 6px;
  border: 1px solid #334155;
  background: #1e293b;
  color: #cbd5e1;
  font-size: 10.5px;
  font-weight: 700;
  cursor: pointer;
}

.present-dot.active {
  background: #00aa13;
  border-color: #00aa13;
  color: #ffffff;
}

.present-exit-btn {
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid #475569;
  background: #1e293b;
  color: #f8fafc;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.present-exit-btn:hover {
  background: #dc2626;
  border-color: #dc2626;
}

.present-stage {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.present-arrow-btn {
  width: 48px;
  height: 48px;
  border-radius: 9999px;
  border: 1px solid #334155;
  background: rgba(30, 41, 59, 0.9);
  color: #ffffff;
  font-size: 28px;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s ease;
}

.present-arrow-btn:hover:not(:disabled) {
  background: #00aa13;
  border-color: #00aa13;
  transform: scale(1.06);
}

.present-arrow-btn:disabled {
  opacity: 0.25;
  cursor: not-allowed;
}

.present-canvas {
  width: 100%;
  max-width: 1180px;
  max-height: calc(100vh - 96px);
  overflow-y: auto;
  border: 1px solid #334155;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.55);
}

.present-chart-img {
  max-height: 360px;
}

.pres-bottom-reveal-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 6px 0 2px;
}

.pres-reveal-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #0f172a;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05);
  transition: all 0.15s ease;
}

.pres-reveal-btn:hover {
  border-color: #94a3b8;
  background: #f8fafc;
}

.pres-reveal-btn.speaker-reveal.active {
  background: #0f172a;
  color: #4ade80;
  border-color: #0f172a;
}

.pres-reveal-btn.audit-reveal.active {
  background: #334155;
  color: #ffffff;
  border-color: #334155;
}

.reveal-sub-pill {
  font-size: 11px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 9999px;
  background: rgba(148, 163, 184, 0.22);
}

/* Interactive Click & Double-Click Slide Elements */
.pres-interactive-item, .pres-interactive-row {
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease, background-color 0.12s ease;
}

.pres-interactive-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.1);
}

.pres-interactive-row:hover td {
  background: #ecfdf5 !important;
}

/* Click Popover Above Mouse */
.click-popover-above {
  position: fixed;
  transform: translate(-50%, -100%);
  z-index: 960;
  width: 330px;
  max-width: 90vw;
  background: #0f172a;
  color: #f8fafc;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 12px 14px;
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.35);
}

.click-popover-above::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -7px;
  transform: translateX(-50%);
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-top: 7px solid #0f172a;
}

.popover-hdr {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.popover-title {
  font-size: 12.5px;
  font-weight: 800;
  color: #4ade80;
}

.popover-close {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 16px;
  cursor: pointer;
  line-height: 1;
}

.popover-val {
  font-size: 14px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 5px;
}

.popover-exp {
  font-size: 12px;
  line-height: 1.45;
  color: #cbd5e1;
  margin-bottom: 8px;
}

.popover-footer {
  border-top: 1px solid #1e293b;
  padding-top: 7px;
}

.popover-detail-btn {
  width: 100%;
  padding: 6px 10px;
  border-radius: 7px;
  border: none;
  background: #00aa13;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}

.popover-detail-btn:hover {
  background: #059669;
}

/* Right-Side Slide-Over Source Drawer */
.drawer-backdrop {
  position: fixed;
  inset: 0;
  z-index: 950;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  justify-content: flex-end;
}

.right-detail-drawer {
  width: 540px;
  max-width: 94vw;
  height: 100vh;
  background: #f8fafc;
  border-left: 2px solid #cbd5e1;
  box-shadow: -12px 0 36px rgba(15, 23, 42, 0.25);
  display: flex;
  flex-direction: column;
}

.drawer-top-hdr {
  background: #0f172a;
  color: #ffffff;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.drawer-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.7px;
  color: #4ade80;
  margin-bottom: 4px;
}

.drawer-top-hdr h3 {
  font-size: 16px;
  font-weight: 800;
  line-height: 1.3;
  color: #ffffff;
}

.drawer-val-pill {
  display: inline-block;
  margin-top: 6px;
  padding: 3px 10px;
  border-radius: 9999px;
  background: #1e293b;
  color: #e2e8f0;
  font-size: 12px;
  font-weight: 700;
}

.drawer-close-btn {
  background: #1e293b;
  border: 1px solid #334155;
  color: #ffffff;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  font-size: 20px;
  cursor: pointer;
  flex-shrink: 0;
}

.drawer-close-btn:hover {
  background: #dc2626;
  border-color: #dc2626;
}

.drawer-scroll-body {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.drawer-summary-box {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-left: 4px solid #00aa13;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 12.5px;
  line-height: 1.5;
  color: #334155;
}

.drawer-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.drawer-sec-title {
  font-size: 12.5px;
  font-weight: 800;
  padding: 8px 12px;
  border-radius: 8px;
  color: #ffffff;
}

.drawer-sec-title.lecture-sec { background: #047857; }
.drawer-sec-title.asg-sec { background: #1d4ed8; }

.drawer-trace-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.drawer-thumb {
  width: 100%;
  max-height: 220px;
  object-fit: contain;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  cursor: zoom-in;
  background: #ffffff;
}

.popover-formula {
  margin-bottom: 8px;
  padding: 6px 8px;
  border-radius: 7px;
  background: rgba(16, 185, 129, 0.14);
  border: 1px solid rgba(52, 211, 153, 0.35);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11px;
  line-height: 1.4;
  color: #a7f3d0;
}

.trace-role-badge {
  display: inline-block;
  margin-bottom: 6px;
  padding: 3px 9px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.2px;
}

.trace-role-badge.lecture-role {
  background: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.trace-role-badge.asg-role {
  background: #eff6ff;
  color: #1e40af;
  border: 1px solid #bfdbfe;
}

.drawer-calc-box {
  background: #ffffff;
  border: 1.5px solid #a7f3d0;
  border-radius: 10px;
  padding: 12px 14px;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.08);
}

.drawer-calc-hdr {
  font-size: 12.5px;
  font-weight: 800;
  color: #065f46;
  margin-bottom: 8px;
}

.drawer-formula-pill {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  border-radius: 8px;
  padding: 8px 10px;
  margin-bottom: 10px;
  font-size: 12px;
  line-height: 1.45;
  color: #064e3b;
}

.drawer-formula-pill .formula-lbl {
  font-weight: 800;
  margin-right: 5px;
}

.drawer-formula-pill code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11.5px;
  font-weight: 700;
  word-break: break-word;
}

.drawer-calc-steps {
  margin: 0 0 8px 0;
  padding-left: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.drawer-calc-steps li {
  font-size: 12px;
  line-height: 1.5;
  color: #1e293b;
}

.drawer-origin-line {
  padding-top: 8px;
  border-top: 1px dashed #cbd5e1;
  font-size: 11.5px;
  line-height: 1.45;
  color: #475569;
}

.drawer-featured-ev {
  background: #ffffff;
  border: 2px solid #f59e0b;
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 3px 10px rgba(245, 158, 11, 0.12);
}

.drawer-fev-hdr {
  font-size: 12px;
  font-weight: 800;
  color: #92400e;
  margin-bottom: 4px;
}

.drawer-fev-cap {
  font-size: 11.5px;
  color: #475569;
  margin: 0 0 8px 0;
}

.drawer-featured-thumb {
  max-height: 280px;
  border-color: #fde68a;
}

.drawer-zoom-hint {
  margin-top: 5px;
  font-size: 10.5px;
  font-weight: 600;
  color: #64748b;
  text-align: right;
}

.drawer-support-table-wrap {
  margin-top: 8px;
  overflow-x: auto;
}

.drawer-support-tbl-hdr {
  color: #92400e !important;
  background: #fffbeb;
  padding: 4px 8px;
  border-radius: 6px;
}

.highlighted-support-row {
  background: #fef3c7 !important;
  outline: 1.5px solid #f59e0b;
}

.highlighted-support-row td {
  background: #fef3c7 !important;
  color: #0f172a !important;
  font-weight: 600;
}

.highlighted-support-cell {
  background: #fde68a !important;
  color: #78350f !important;
  font-weight: 800 !important;
  border-radius: 3px;
}

.support-hit-badge {
  display: inline-block;
  margin-right: 6px;
  padding: 1px 5px;
  border-radius: 4px;
  background: #d97706;
  color: #ffffff;
  font-size: 9px;
  font-weight: 800;
  vertical-align: middle;
}

/* Language Switcher above Search Box */
.lang-switcher-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  margin: 0 14px 10px;
  padding: 4px;
  background: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 10px;
}

.lang-btn {
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 0.74rem;
  font-weight: 600;
  padding: 6px 8px;
  border-radius: 7px;
  cursor: pointer;
  transition: all 0.16s ease;
  text-align: center;
}

.lang-btn:hover {
  color: #e2e8f0;
  background: rgba(255, 255, 255, 0.06);
}

.lang-btn.active {
  background: #10b981;
  color: #06281e;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.25);
}
</style>
