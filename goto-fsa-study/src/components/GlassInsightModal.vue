<script setup>
import { computed, ref, watch } from 'vue'
import { useReportMode } from '../composables/useReportMode'

const props = defineProps({
  item: { type: Object, required: true },
  lang: { type: String, default: 'en' },
  renderMath: { type: Function, default: null },
})

const emit = defineEmits(['close', 'zoom', 'jump-assignment', 'jump-lecture'])

const { reportViewMode } = useReportMode()

const activeTab = ref('overview') // 'overview' | 'compare' | 'calc' | 'schedules' | 'traces'
const chartBasis = computed({
  get: () => (reportViewMode.value === 'original' ? 'previous' : 'current'),
  set: (val) => {
    reportViewMode.value = val === 'previous' ? 'original' : 'restated'
  },
})
const showMoreAnalysis = ref(false)
const showRightPanel = ref(false)
const showAllCalcRows = ref(false)
const showAllTraces = ref(false)
const openSchedules = ref({ 0: true })

// Slide 9 (Cost of Capital) interactive Source & Math walk-through sub-menu
const isSlide9Walkthrough = computed(() => (props.item.slide?.slide_num || 0) === 9)
const activeSlide9Comp = ref('wacc')

const detectInitialSlide9Comp = (item) => {
  const txt = `${item?.title || ''} ${item?.value || ''} ${item?.keywords || ''} ${item?.detail || ''}`.toLowerCase()
  if (txt.includes('risk-free') || txt.includes('risk free') || txt.includes('4.502') || txt.includes('6.120') || txt.includes('sovereign')) return 'rf'
  if (txt.includes('capm') || txt.includes('cost of equity') || txt.includes('8.452') || txt.includes('beta') || txt.includes('erp')) return 'capm'
  if (txt.includes('cost of debt') || txt.includes('5.390') || txt.includes('6.912') || txt.includes('535.15') || txt.includes('tax shield')) return 'kd'
  if (txt.includes('weight') || txt.includes('77.42') || txt.includes('22.58') || txt.includes('capital structure') || txt.includes('market cap')) return 'weights'
  if (txt.includes('terminal') || txt.includes('growth') || txt.includes('3.00%') || txt.includes('3.41%') || txt.includes('reinvestment') || txt.includes('roic')) return 'growth'
  return 'wacc'
}

const slide9Components = computed(() => {
  const id = isId.value
  return [
    {
      id: 'rf',
      shortLabel: id ? '1. Risk-Free (4,502%)' : '1. Risk-Free Rate (4.502%)',
      title: id ? 'Suku Bunga Bebas Risiko IDR (Risk-Free Rate)' : 'IDR Risk-Free Rate (Spread-Adjusted)',
      result: '4.502%',
      formula: 'Rf = ID 10Y Bond Yield (6.120%) − Sovereign Default Spread (1.618%)',
      summary: id
        ? 'Yield obligasi pemerintah Indonesia 10 tahun (6,120%) masih mengandung risiko gagal bayar negara (peringkat Baa2), sehingga kita kurangi spread gagal bayar agar murni bebas risiko dan tidak dihitung ganda dengan CRP.'
        : 'Indonesia\'s 10-year government bond yield (6.120%) still contains sovereign default risk (Baa2 rating), so we deduct the default spread to get a clean default-free IDR rate and avoid double-counting country risk.',
      usedIn: id ? 'Masuk ke langkah 2: CAPM Cost of Equity (8,452%) dan batas atas Terminal Growth.' : 'Feeds Step 2: CAPM Cost of Equity (8.452%) and caps Terminal Growth (g).',
      sources: [
        {
          label: id ? 'Yield Obligasi RI 10 Tahun' : 'Indonesia 10Y Gov. Bond Yield',
          value: '6.120%',
          source: 'Investing.com • Dec 30, 2025',
          note: id ? 'Suku bunga obligasi pemerintah denominasi Rupiah pada tanggal valuasi.' : 'Local IDR government bond yield on the valuation date.',
        },
        {
          label: id ? 'Sovereign Default Spread (Baa2)' : 'Sovereign Default Spread (Baa2)',
          value: '−1.618%',
          source: 'Damodaran • Jan 1, 2026',
          note: id ? 'Kompensasi risiko gagal bayar untuk peringkat kredit Moody\'s Indonesia (Baa2).' : 'Default risk spread for Indonesia\'s Moody\'s Baa2 sovereign rating.',
        },
      ],
      steps: [
        { step: '1', expr: '6.120% (ID 10Y Bond) − 1.618% (Baa2 Default Spread)', out: '4.502% Clean IDR Rf' },
      ],
    },
    {
      id: 'capm',
      shortLabel: id ? '2. CAPM / Ke (8,452%)' : '2. CAPM / Ke (8.452%)',
      title: id ? 'Biaya Ekuitas (CAPM Cost of Equity)' : 'CAPM Cost of Equity (Ke)',
      result: '8.452%',
      formula: 'Ke = Rf (4.502%) + Beta (0.59) × [Mature ERP (4.230%) + Country Risk Premium (2.465%)]',
      summary: id
        ? 'Imbal hasil minimum yang diminta investor saham untuk memegang saham GoTo dibandingkan obligasi bebas risiko. Digunakan langsung sebagai tingkat diskonto pada model Residual Income.'
        : 'The minimum annual return stock investors demand to hold GoTo shares instead of a risk-free bond. Used directly as the discount rate in our Residual Income model.',
      usedIn: id ? 'Masuk ke langkah 5: WACC (bobot ekuitas 77,42%) & diskonto Residual Income.' : 'Feeds Step 5: WACC (77.42% equity weight) and discounts Residual Income.',
      sources: [
        {
          label: id ? 'Risk-Free Rate IDR (Rf)' : 'Clean IDR Risk-Free Rate (Rf)',
          value: '4.502%',
          source: id ? 'Langkah 1 (Investing.com + Damodaran)' : 'Step 1 (Investing.com − Damodaran)',
          note: id ? 'Dasar imbal hasil bebas risiko dalam Rupiah.' : 'Default-free IDR baseline return.',
        },
        {
          label: id ? 'Levered Beta 5 Tahun' : '5-Year Levered Beta (β)',
          value: '0.59',
          source: 'Investing.com • Dec 30, 2025',
          note: id ? 'Sensitivitas saham GOTO terhadap pasar; juga diuji stres hingga 1,30 di Tabel 17.' : 'GoTo stock sensitivity vs. market; also stress-tested up to 1.30 in Table 17.',
        },
        {
          label: id ? 'Mature-Market ERP' : 'Mature-Market ERP',
          value: '4.230%',
          source: 'Damodaran • Jan 1, 2026',
          note: id ? 'Premi risiko saham pasar maju (US S&P 500) di atas obligasi.' : 'Baseline equity risk premium in a mature market (US S&P 500).',
        },
        {
          label: id ? 'Country Risk Premium (CRP)' : 'Indonesia Country Risk Premium',
          value: '2.465%',
          source: 'Damodaran • Jan 1, 2026',
          note: id ? 'Tambahan premi risiko volatilitas saham pasar berkembang Indonesia.' : 'Extra equity-volatility risk bonus required for Indonesian stocks.',
        },
      ],
      steps: [
        { step: '1', expr: 'Total Indonesia ERP = 4.230% (Mature ERP) + 2.465% (CRP)', out: '6.695%' },
        { step: '2', expr: 'GoTo Equity Risk Charge = 0.59 (Beta) × 6.695%', out: '+3.950%' },
        { step: '3', expr: 'Ke = 4.502% (Rf) + 3.950%', out: '8.452% Cost of Equity' },
      ],
    },
    {
      id: 'kd',
      shortLabel: id ? '3. Biaya Utang (5,390%)' : '3. Cost of Debt (5.390%)',
      title: id ? 'Biaya Utang Setelah Pajak (After-Tax Cost of Debt)' : 'After-Tax Cost of Debt (Kd)',
      result: '5.390%',
      formula: 'After-Tax Kd = (Finance Costs Rp 535.15B ÷ Total Debt Rp 7,742.64B) × (1 − 22% Tax)',
      summary: id
        ? 'Suku bunga efektif GoTo berasal dari beban keuangan aktual 2025 dibagi total pinjaman & liabilitas sewa, lalu dikurangi penghematan pajak (tax shield) 22% karena bunga dapat mengurangi pajak.'
        : 'GoTo\'s effective interest rate comes from actual FY2025 finance costs divided by total borrowings & leases, then adjusted for the 22% Indonesian corporate tax shield because interest is tax-deductible.',
      usedIn: id ? 'Masuk ke langkah 5: WACC (bobot utang 22,58%). Cek nol-tax-shield: Kd = 6,912% → WACC 8,101%.' : 'Feeds Step 5: WACC (22.58% debt weight). Zero-tax-shield check: Kd = 6.912% → WACC 8.101%.',
      sources: [
        {
          label: id ? 'Beban Keuangan FY2025' : 'FY2025 Finance Costs',
          value: 'Rp 535.15B',
          source: 'Audited FS Note 27b • p. 131',
          note: id ? 'Total bunga pinjaman (Rp510,3M), bunga sewa (Rp12,4M), dan biaya bank (Rp12,4M).' : 'Borrowing interest (Rp 510.3B) + lease interest (Rp 12.4B) + bank fees (Rp 12.4B).',
        },
        {
          label: id ? 'Total Utang & Liabilitas Sewa' : 'Total Debt & Lease Liabilities',
          value: 'Rp 7,742.64B',
          source: 'Audited FS Notes 19 & 20 • pp. 105–111',
          note: id ? 'Pinjaman bank jangka pendek/panjang, non-bank, dan seluruh liabilitas sewa.' : 'Short-term & long-term bank/non-bank loans plus all lease liabilities.',
        },
        {
          label: id ? 'Tarif Pajak Badan Indonesia' : 'Indonesia Corporate Tax Rate',
          value: '22.00%',
          source: id ? 'UU HPP / Pajak Badan RI' : 'Statutory ID Corporate Tax',
          note: id ? 'Bunga mengurangi laba kena pajak sebesar 22% (juga diuji 0% tax shield di Tabel 14).' : 'Interest reduces taxable income by 22% (also tested at 0% tax shield in Table 14).',
        },
      ],
      steps: [
        { step: '1', expr: 'Pre-Tax Kd = Rp 535.15B (Note 27b) ÷ Rp 7,742.64B (Notes 19–20)', out: '6.912% Pre-Tax Kd' },
        { step: '2', expr: 'After-Tax Kd = 6.912% × (1 − 22.0%) = 6.912% × 0.78', out: '5.390% After-Tax Kd' },
      ],
    },
    {
      id: 'weights',
      shortLabel: id ? '4. Bobot Modal (77,4% / 22,6%)' : '4. Capital Weights (77.4% / 22.6%)',
      title: id ? 'Struktur & Bobot Modal (Market Value Weights)' : 'Capital Structure Weights (Equity vs. Debt)',
      result: '77.42% E / 22.58% D',
      formula: 'Total Capital = Market Cap (Rp 26,550.3B) + Total Debt (Rp 7,742.6B) = Rp 34,292.9B',
      summary: id
        ? 'Bobot WACC menggunakan nilai pasar ekuitas pada harga Rp25,00 (bukan nilai buku) dibagi total modal bersama utang dan sewa.'
        : 'WACC weights use GoTo\'s market capitalization at the Rp 25.00 share price alongside total borrowings and leases.',
      usedIn: id ? 'Masuk ke langkah 5: Menggabungkan Ke (8,452%) dan Kd (5,390%) menjadi WACC.' : 'Feeds Step 5: Blends Ke (8.452%) and After-Tax Kd (5.390%) into WACC.',
      sources: [
        {
          label: id ? 'Harga Saham Pasar (GOTO)' : 'Market Share Price (IDX: GOTO)',
          value: 'Rp 25.00',
          source: 'Investing.com • Dec 30, 2025',
          note: id ? 'Harga penutupan pasar pada tanggal valuasi.' : 'Market closing share price on valuation date.',
        },
        {
          label: id ? 'Saham Beredar (Excl. Treasuri)' : 'Shares Outstanding (Excl. Treasury)',
          value: '1,062.01B sh',
          source: 'Audited FS Note 31 • p. 16',
          note: id ? '1.062.010,2 juta saham biasa beredar di luar saham treasuri.' : '1,062,010.2 million ordinary shares excluding treasury stock.',
        },
        {
          label: id ? 'Total Utang & Liabilitas Sewa' : 'Total Debt & Leases',
          value: 'Rp 7,742.6B',
          source: 'Audited FS Notes 19 & 20',
          note: id ? 'Konsisten dengan definisi utang pada perhitungan Kd dan Net Cash.' : 'Matches exact debt definition used in Kd and Net Cash.',
        },
      ],
      steps: [
        { step: '1', expr: 'Market Value of Equity (E) = Rp 25.00 × 1,062.01B shares', out: 'Rp 26,550.3B' },
        { step: '2', expr: 'Total Capital (E + D) = Rp 26,550.3B + Rp 7,742.6B', out: 'Rp 34,292.9B' },
        { step: '3', expr: 'wE = 26,550.3 ÷ 34,292.9 | wD = 7,742.6 ÷ 34,292.9', out: '77.42% Equity / 22.58% Debt' },
      ],
    },
    {
      id: 'wacc',
      shortLabel: id ? '5. WACC (7,761%)' : '5. WACC (7.761%)',
      title: id ? 'Weighted Average Cost of Capital (WACC)' : 'Baseline Weighted Average Cost of Capital (WACC)',
      result: '7.761%',
      formula: 'WACC = (77.42% × 8.452%) + (22.58% × 5.390%) = 6.544% + 1.217% = 7.761%',
      summary: id
        ? 'Biaya modal rata-rata tertimbang GoTo lintas pemegang saham dan kreditur. Menjadi batas imbal hasil (hurdle rate) untuk mendiskontokan FCFF di DCF; ROIC 2028F GoTo (+2,70%) tertinggal 506 bps di bawah WACC.'
        : 'GoTo\'s blended financing cost across shareholders and lenders. Used to discount DCF Free Cash Flows; GoTo\'s 2028F ROIC (+2.70%) trails this 7.761% hurdle by 506 bps, which is why operating EV is negative.',
      usedIn: id ? 'Digunakan langsung di Slide 10 (Model DCF -> +Rp 10,38/saham) & uji sensitivitas WACC 6,76%–8,76%.' : 'Directly discounts Slide 10 DCF (+Rp 10.38/sh) and anchors the 6.76%–8.76% WACC sensitivity grid.',
      sources: [
        {
          label: id ? 'Kontribusi Ekuitas (wE × Ke)' : 'Equity Component (wE × Ke)',
          value: '6.544%',
          source: id ? 'Langkah 2 & 4 (77,42% × 8,452%)' : 'Steps 2 & 4 (77.42% × 8.452%)',
          note: id ? 'Porsi biaya modal dari pemegang saham publik.' : 'Weighted return required by equity shareholders.',
        },
        {
          label: id ? 'Kontribusi Utang (wD × Kd after-tax)' : 'Debt Component (wD × After-Tax Kd)',
          value: '1.217%',
          source: id ? 'Langkah 3 & 4 (22,58% × 5,390%)' : 'Steps 3 & 4 (22.58% × 5.390%)',
          note: id ? 'Porsi biaya modal dari pinjaman bank & sewa setelah tax shield 22%.' : 'Weighted after-tax cost of bank loans & leases.',
        },
        {
          label: id ? 'Uji Tanpa Tax Shield (0% Tax)' : 'Zero-Tax-Shield Check (0% Tax)',
          value: '8.101%',
          source: 'Valuation Workbook • Cost of Capital',
          note: id ? 'Jika rugi fiskal menghapus tax shield, WACC naik +34 bps ke 8,101%.' : 'If past tax losses remove the tax shield, WACC rises +34 bps to 8.101%.',
        },
      ],
      steps: [
        { step: '1', expr: 'Equity Weight × Cost of Equity = 77.42% × 8.452%', out: '6.544%' },
        { step: '2', expr: 'Debt Weight × After-Tax Kd = 22.58% × 5.390%', out: '1.217%' },
        { step: '3', expr: 'Baseline WACC = 6.544% + 1.217%', out: '7.761% (Zero-Tax-Shield: 8.101%)' },
      ],
    },
    {
      id: 'growth',
      shortLabel: id ? '6. Terminal g (3,00%)' : '6. Terminal Growth g (3.00%)',
      title: id ? 'Tingkat Pertumbuhan Terminal (g = Reinvestment Rate × ROIC)' : 'Fundamental Terminal Growth Rate (g)',
      result: '3.00% (Fund. +3.41%)',
      formula: 'Fundamental g = Reinvestment Rate (126.42%) × ROIC (+2.70%) = +3.41% → Selected 3.00%',
      summary: id
        ? 'Tidak dipilih sembarangan: kami menghitung pertumbuhan fundamental dari proyeksi 2028F (+3,41%), lalu memakai 3,00% secara konservatif agar berada di bawah batas Rf (4,502%) dan selaras dengan target inflasi Bank Indonesia (2,5% ± 1%).'
        : 'Not an arbitrary guess: we derive GoTo\'s fundamental growth (+3.41%) directly from 2028F Reinvestment Rate × ROIC, then cap steady-state g conservatively at 3.00% — below the 4.502% Rf cap and inside Bank Indonesia\'s 2.5% ± 1% inflation target.',
      usedIn: id ? 'Digunakan konsisten di DCF & Residual Income (juga diuji sensitivitas 1,0%–4,0% di Tabel 17).' : 'Used consistently in both DCF and Residual Income (stress-tested across 1.0%–4.0% in Table 17).',
      sources: [
        {
          label: id ? 'NOPAT 2028F' : '2028F NOPAT',
          value: '+Rp 442.4B',
          source: 'Pro Forma 2028F • Table 12 & 15',
          note: id ? 'EBIT Rp 567,2M × (1 − 22% pajak).' : '2028F EBIT Rp 567.2B × (1 − 22% tax).',
        },
        {
          label: id ? 'Net Reinvestment 2028F' : '2028F Net Reinvestment',
          value: 'Rp 559.3B',
          source: 'Pro Forma 2028F • Table 15',
          note: id ? 'CapEx 1.811,1 − D&A 1.111,1 − arus masuk NWC 140,6.' : 'CapEx 1,811.1 − D&A 1,111.1 − NWC inflow 140.6.',
        },
        {
          label: id ? 'Invested Capital Awal 2028F' : 'Beginning 2028F Invested Capital',
          value: 'Rp 16,380.8B',
          source: 'Valuation Workbook • Terminal Growth',
          note: id ? 'Book Equity + Net Debt yang digulirkan dari 2026F–2027F.' : 'Book Equity + Net Debt rolled forward through 2026F–2027F.',
        },
        {
          label: id ? 'Batas Inflasi BI & Rf Cap' : 'BI Inflation Target & Rf Cap',
          value: '2.5% ± 1% | 4.502%',
          source: 'Bank Indonesia • Investing.com',
          note: id ? '3,00% berada aman di dalam target inflasi BI & di bawah Rf 4,502%.' : '3.00% sits inside BI\'s 1.5%–3.5% inflation band & below 4.502% Rf.',
        },
      ],
      steps: [
        { step: '1', expr: 'Reinvestment Rate = Net Reinvestment (559.3B) ÷ NOPAT (442.4B)', out: '126.42%' },
        { step: '2', expr: 'ROIC = NOPAT (442.4B) ÷ Beg. Invested Capital (16,380.8B)', out: '+2.70%' },
        { step: '3', expr: 'Fundamental g = 126.42% × 2.70%', out: '+3.41% Formula Ceiling' },
        { step: '4', expr: 'Steady-State Cap (< +3.41% & < 4.502% Rf; fits BI 2.5% ± 1%)', out: '3.00% Selected Terminal g' },
      ],
    },
  ]
})

const currentSlide9Comp = computed(() =>
  slide9Components.value.find((c) => c.id === activeSlide9Comp.value) || slide9Components.value[4]
)
const currentSlide9Idx = computed(() =>
  slide9Components.value.findIndex((c) => c.id === activeSlide9Comp.value)
)
const prevSlide9Comp = computed(() =>
  currentSlide9Idx.value > 0 ? slide9Components.value[currentSlide9Idx.value - 1] : null
)
const nextSlide9Comp = computed(() =>
  currentSlide9Idx.value >= 0 && currentSlide9Idx.value < slide9Components.value.length - 1
    ? slide9Components.value[currentSlide9Idx.value + 1]
    : null
)

const toggleSchedule = (idx) => {
  openSchedules.value = {
    ...openSchedules.value,
    [idx]: !openSchedules.value[idx],
  }
}

watch(
  () => props.item,
  (newItem) => {
    activeTab.value = 'overview'
    activeSlide9Comp.value = detectInitialSlide9Comp(newItem)
    showMoreAnalysis.value = false
    showRightPanel.value = false
    showAllCalcRows.value = false
    showAllTraces.value = false
    openSchedules.value = { 0: true }
  },
  { immediate: true }
)

const hasChartBasisSwitch = computed(() => {
  const sn = props.item.slide?.slide_num || 0
  if (sn === 5) {
    const t = `${props.item.title || ''} ${props.item.value || ''} ${props.item.keywords || ''}`.toLowerCase()
    return !(t.includes('z-score') || t.includes('z score') || t.includes('altman') || t.includes('distress'))
  }
  return [7, 8, 10, 13].includes(sn)
})

const isId = computed(() => props.lang === 'id')

const hasAnalysisTab = computed(() => explanationParagraphs.value.length > 0)
const visibleAnalysisParagraphs = computed(() =>
  showMoreAnalysis.value ? explanationParagraphs.value : explanationParagraphs.value.slice(0, 1)
)
const hiddenAnalysisCount = computed(() => Math.max(0, explanationParagraphs.value.length - 1))

const hasFormulaBlock = computed(() =>
  Boolean(props.item.formula || props.item.calc_steps?.length || props.item.data_origin)
)
const calcNotesCount = computed(() => props.item.slide?.calculation_notes?.length || 0)
const visibleCalcNotes = computed(() => {
  const list = props.item.slide?.calculation_notes || []
  return showAllCalcRows.value ? list : list.slice(0, 3)
})
const hiddenCalcCount = computed(() => Math.max(0, calcNotesCount.value - 3))
const hasCalcTab = computed(() => hasFormulaBlock.value || calcNotesCount.value > 0)
const calcTabCount = computed(() => calcNotesCount.value + (hasFormulaBlock.value ? 1 : 0))

const schedulesCount = computed(() => props.item.slide?.supporting_schedules?.length || 0)
const hasSchedulesTab = computed(() => schedulesCount.value > 0 || Boolean(props.item.evidence_img))
const schedulesTabCount = computed(() => schedulesCount.value + (props.item.evidence_img ? 1 : 0))

const allTraces = computed(() => [
  ...(props.item.matchedAssignments || []).map((a) => ({ kind: 'assignment', ...a })),
  ...(props.item.matchedLectures || []).map((l) => ({ kind: 'lecture', ...l })),
])
const tracesTabCount = computed(() => allTraces.value.length)
const visibleTraces = computed(() =>
  showAllTraces.value ? allTraces.value : allTraces.value.slice(0, 2)
)
const hiddenTracesCount = computed(() => Math.max(0, allTraces.value.length - 2))
const hasTracesTab = computed(() => tracesTabCount.value > 0)

// Slide-aware Pre-Exit / Original vs. Post-Exit / Final Report comparison view
const comparisonData = computed(() => {
  const sn = props.item.slide?.slide_num || 0
  const id = isId.value

  if (sn === 2) {
    return {
      tabLabel: id ? 'Pra vs. Pasca Exit' : 'Pre vs. Post Exit',
      title: id ? 'Pergeseran Struktural: 2023 Pra-Exit vs. 2025 Pasca-Exit' : 'Structural Regime Shift: 2023 Pre-Exit vs. 2025 Post-Exit',
      subtitle: id ? 'Dekonsolidasi Tokopedia (Feb 2024) mengubah struktur biaya & profitabilitas secara fundamental' : 'Tokopedia deconsolidation (Feb 2024) fundamentally reset GoTo cost structure and profitability',
      leftLabel: id ? '2023 Pra-Exit (Konsolidasi Tokopedia)' : '2023 Pre-Exit (With Tokopedia)',
      rightLabel: id ? '2025 Pasca-Exit (Berlanjut)' : '2025 Post-Exit (Continuing)',
      rows: [
        { metric: id ? 'Pendapatan Bersih' : 'Net Revenue', before: 'Rp 14.79T', after: 'Rp 18.32T', delta: '+23.9% (23→25)', tone: 'pos', pctA: 81, pctB: 100, note: id ? '+15,27% YoY di 2025 dipimpin GoPay (+74,1%) & Gojek (+13,8%).' : '+15.27% YoY in 2025 led by GoPay (+74.1%) & Gojek (+13.8%).' },
        { metric: id ? 'Cash OpEx (% Pendapatan)' : 'Cash OpEx (% Revenue)', before: '117.01%', after: '55.70%', delta: '−6,131 bps', tone: 'pos', pctA: 100, pctB: 48, note: id ? 'Subsidi e-commerce pra-exit tereliminasi; turun −708 bps lagi di 2025.' : 'Pre-exit e-commerce subsidies removed; fell another −708 bps in 2025.' },
        { metric: id ? 'Laba Operasi (EBIT)' : 'Operating Profit (EBIT)', before: '−Rp 10.28T', after: '−Rp 0.38T', delta: '+96.3% loss cut', tone: 'pos', pctA: 100, pctB: 10, note: id ? 'Rugi operasi menyusut 83,1% YoY dari −Rp2,24T (2024) ke −Rp378M (2025).' : 'Operating loss narrowed 83.1% YoY from −Rp2.24T (2024) to −Rp378B (2025).' },
        { metric: id ? 'Laba Bersih Konsolidasian' : 'Consolidated Net Income', before: '−Rp 90.52T', after: '−Rp 1.50T', delta: 'Ex-Rp78.8T goodwill', tone: 'accent', pctA: 100, pctB: 12, note: id ? '2023 terdistorsi penurunan nilai goodwill Rp78,77T (Catatan 34a).' : '2023 distorted by Rp78.77T goodwill impairment write-off (Note 34a).' },
      ],
    }
  }

  if (sn === 4) {
    return {
      tabLabel: id ? 'Pra vs. Pasca Exit' : 'Pre vs. Post Exit',
      title: id ? 'Profitabilitas & DuPont: 2023 Pra-Exit vs. 2025 Pasca-Exit' : 'Profitability & DuPont: 2023 Pre-Exit vs. 2025 Post-Exit',
      subtitle: id ? 'Pemulihan margin operasi besar-besaran namun ROE masih di bawah biaya ekuitas (8,45%)' : 'Massive operating-margin recovery, though ROE still trails the 8.45% Cost of Equity hurdle',
      leftLabel: id ? '2023 Pra-Exit' : '2023 Pre-Exit',
      rightLabel: id ? '2025 Pasca-Exit' : '2025 Post-Exit',
      rows: [
        { metric: id ? 'Margin Laba Kotor' : 'Gross Profit Margin', before: '65.55%', after: '57.72%', delta: '−783 bps mix', tone: 'accent', pctA: 100, pctB: 88, note: id ? 'Pergeseran bauran segmen pasca-exit, namun naik +436 bps YoY dari 2024.' : 'Post-exit segment mix shift, yet expanded +436 bps YoY vs. 2024 (53.36%).' },
        { metric: id ? 'Margin Operasi (EBIT)' : 'Operating Margin (EBIT)', before: '−69.52%', after: '−2.06%', delta: '+6,746 bps', tone: 'pos', pctA: 100, pctB: 8, note: id ? 'Mendekati titik impas operasi setelah keluar dari Tokopedia & Vietnam.' : 'Approaching operating breakeven after Tokopedia & Vietnam exits.' },
        { metric: id ? 'Perputaran Aset (ATO)' : 'Total Asset Turnover', before: '0.273x', after: '0.400x', delta: '+46.5%', tone: 'pos', pctA: 68, pctB: 100, note: id ? 'Mengungguli Grab (0,28x) dan Bukalapak (0,25x) pada FY2025.' : 'Outperforms regional peer Grab (0.28x) and Bukalapak (0.25x) in FY2025.' },
        { metric: id ? 'ROE Konsolidasian' : 'Consolidated ROE', before: '−253.4%', after: '−5.23%', delta: 'Parent: −3.73%', tone: 'pos', pctA: 100, pctB: 10, note: id ? 'Membaik tajam dari −17,97% (2024), namun masih tertinggal dari Grab (+2,96%).' : 'Improved sharply from −17.97% (2024), still lagging Grab (+2.96%).' },
      ],
    }
  }

  if (sn === 5) {
    return {
      tabLabel: id ? 'Pra vs. Revisi' : 'Prior vs. Restated',
      title: id ? 'Rasio Neraca: Sebelum Koreksi vs. Laporan Akhir (Restated)' : 'Balance-Sheet Ratios: Prior Deck vs. Final Report (Restated)',
      subtitle: id ? 'Dampak koreksi Catatan 7 (piutang pinjaman), Catatan 6 (DSO) & harmonisasi utang Catatan 19–20' : 'Impact of Note 7 lending receivables, Note 6 DSO cleanup & full Notes 19–20 debt',
      leftLabel: id ? 'Dek Awal / Pra-Revisi' : 'Prior Deck (Unadjusted)',
      rightLabel: id ? 'Laporan Akhir (Restated)' : 'Final Report (Restated)',
      rows: [
        { metric: id ? 'Rasio Lancar 2024' : '2024 Current Ratio', before: '2.46x', after: '2.62x', delta: '+0.16x fix', tone: 'pos', pctA: 94, pctB: 100, note: id ? 'Menambahkan Rp1.581,8M piutang pinjaman Catatan 7 (2025: 2,73x).' : 'Restored Rp1,581.8B omitted Note 7 lending receivables (2025: 2.73x).' },
        { metric: id ? 'DSO Piutang Usaha 2024' : '2024 Trade DSO', before: '46.88 days', after: '10.56 days', delta: '−36.3 days', tone: 'pos', pctA: 100, pctB: 23, note: id ? 'Memisahkan piutang usaha Catatan 6 dari kredit konsumen Catatan 7 (2025: 10,90d).' : 'Separated Note 6 trade receivables from Note 7 loans (2025: 10.90d).' },
        { metric: id ? 'Utang / Ekuitas 2024' : '2024 Debt / Equity', before: '12.57%', after: '15.85%', delta: '+328 bps', tone: 'accent', pctA: 79, pctB: 100, note: id ? 'Memasukkan porsi lancar & liabilitas sewa penuh (2025 naik ke 26,97%).' : 'Included current maturities & full leases (rose to 26.97% in 2025).' },
        { metric: id ? 'Interest Coverage (TIE)' : 'Times Interest Earned', before: 'N/M', after: '−0.71x (25)', delta: 'Live Note 27b', tone: 'accent', pctA: 15, pctB: 75, note: id ? 'Menautkan biaya bunga Catatan 27b (Rp535,2M): −27,83x (23) → −4,54x (24) → −0,71x (25).' : 'Linked Note 27b finance costs (Rp535.2B): −27.83x (23) → −4.54x (24) → −0.71x (25).' },
      ],
    }
  }

  if (sn === 6) {
    return {
      tabLabel: id ? 'Pra vs. Pasca Exit' : 'Pre vs. Post Exit',
      title: id ? 'Normalisasi Arus Kas & CapEx: Terdistorsi vs. Berlanjut' : 'Cash Flow & CapEx Normalization: Distorted vs. Continuing',
      subtitle: id ? 'Menghapus Rp5,46T transfer aset takberwujud Tokopedia 2024 (Catatan 12) mengungkap tren kas asli' : 'Stripping Rp5.46T of 2024 Tokopedia intangible transfers (Note 12) reveals true cash run-rate',
      leftLabel: id ? '2024 Tidak Disesuaikan' : '2024 Unadjusted (Distorted)',
      rightLabel: id ? '2025 Berlanjut (Pasca-Exit)' : '2025 Continuing (Post-Exit)',
      rows: [
        { metric: id ? 'CapEx Tunai (% Pendapatan)' : 'Cash CapEx (% Revenue)', before: '41.01%', after: '6.45%', delta: '−3,456 bps', tone: 'pos', pctA: 100, pctB: 16, note: id ? '2024 berlanjut sebenarnya 6,63% setelah mengeluarkan Rp5.464,9M Tokopedia.' : '2024 continuing CapEx was actually 6.63% ex-Rp5,464.9B Tokopedia transfer.' },
        { metric: id ? 'Arus Kas Operasi (CFO)' : 'Operating Cash Flow', before: '−Rp 622.1B', after: '+Rp 307.0B', delta: '+Rp 929.1B YoY', tone: 'pos', pctA: 65, pctB: 100, note: id ? 'Berbalik positif meski ekspansi pinjaman GoPay menyerap −Rp2,02T.' : 'Turned positive despite −Rp2.02T working-capital outflow for GoPay lending.' },
        { metric: id ? 'Arus Kas Bebas (FCF)' : 'Free Cash Flow (FCF)', before: '−Rp 7,141B', after: '−Rp 875.3B', delta: 'Cont. 24: −1,676B', tone: 'accent', pctA: 100, pctB: 14, note: id ? 'CFO 2025 baru menutup 25,97% CapEx tunai (Rp1,18T); kas masih tergerus.' : '2025 CFO covered only 25.97% of cash CapEx (Rp1.18T); FCF remains negative.' },
        { metric: id ? 'Rasio Akrual (Dilaporkan)' : 'Reported Accrual Ratio', before: '−11.21%', after: '−3.95%', delta: '+726 bps YoY', tone: 'pos', pctA: 100, pctB: 35, note: id ? 'Akrual berulang yang disesuaikan juga menyempit dari −3,69% ke −1,94%.' : 'Adjusted recurring accrual ratio also tightened from −3.69% to −1.94%.' },
      ],
    }
  }

  if (sn === 7) {
    return {
      tabLabel: id ? 'Pra vs. Pasca Exit' : 'Pre vs. Post Exit',
      title: id ? 'Asumsi Proyeksi: Dek Lama (3-Thn) vs. Laporan Akhir (Pasca-Exit)' : 'Forecast Drivers: Original Deck (3-Yr Avg) vs. Final Report (Post-Exit)',
      subtitle: id ? 'Mengkarantina 2023 pra-Tokopedia menghilangkan distorsi OpEx dan CapEx dalam proyeksi' : 'Quarantining pre-exit 2023 removes massive OpEx and CapEx distortions from Base Case drivers',
      leftLabel: id ? 'Dek Awal (Rata-rata 2023–25)' : 'Original Deck (2023–25 Avg)',
      rightLabel: id ? 'Laporan Akhir (Pasca-Exit)' : 'Final Report (Post-Exit)',
      rows: [
        { metric: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth Rate', before: '11.40%', after: '15.27%', delta: '+387 bps', tone: 'pos', pctA: 75, pctB: 100, note: id ? 'Mencerminkan pertumbuhan organik 2024→2025 tanpa seretan dekonsolidasi.' : 'Reflects clean 2024→2025 organic growth without deconsolidation drag.' },
        { metric: id ? 'COGS / Pendapatan' : 'COGS / Revenue', before: '41.10%', after: '42.28%', delta: '+118 bps', tone: 'accent', pctA: 97, pctB: 100, note: id ? 'Menggunakan basis aktual FY2025 pasca-exit (1H26 membaik ke 38,10%).' : 'Anchored on actual FY2025 post-exit mix (1H26 improved further to 38.10%).' },
        { metric: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue', before: '78.50%', after: '55.70%', delta: '−2,280 bps', tone: 'pos', pctA: 100, pctB: 71, note: id ? 'Menghapus OpEx 2023 (117,01%) yang menyebabkan pembakaran kas buatan.' : 'Eliminates 2023 OpEx (117.01%) that caused artificial cash depletion.' },
        { metric: id ? 'CapEx / Pendapatan' : 'CapEx / Revenue', before: '16.30%', after: '6.45%', delta: '−985 bps', tone: 'pos', pctA: 100, pctB: 40, note: id ? 'Menghapus anomali 41,0% di 2024 akibat transfer takberwujud Tokopedia.' : 'Removes the 41.0% 2024 distortion from Tokopedia intangible transfers.' },
      ],
    }
  }

  if (sn === 8) {
    return {
      tabLabel: id ? 'Pra vs. Pasca Exit' : 'Pre vs. Post Exit',
      title: id ? 'Dampak Proyeksi 2028F: Dek Lama vs. Laporan Akhir Pasca-Exit' : '2028F Forecast Impact: Old Deck vs. Clean Post-Exit Model',
      subtitle: id ? 'Menghilangkan kontaminasi 2023 membalik EBIT & menjaga kas, namun ROIC (2,70%) tetap < WACC' : 'Removing 2023 contamination flips EBIT positive & preserves cash, yet ROIC (2.70%) trails WACC',
      leftLabel: id ? 'Dek Awal (Terkontaminasi 2023)' : 'Original Deck (2023-Polluted)',
      rightLabel: id ? 'Laporan Akhir (Base Pasca-Exit)' : 'Final Report (Post-Exit Base)',
      rows: [
        { metric: id ? '2028F Laba Operasi (EBIT)' : '2028F Operating Profit (EBIT)', before: '−Rp 4,967B', after: '+Rp 567.2B', delta: '+Rp 5.53T swing', tone: 'pos', pctA: 100, pctB: 22, note: id ? 'Berbalik positif sejak 2026F (+Rp426,9M) karena margin kotor > Cash OpEx.' : 'Turns positive in 2026F (+Rp426.9B) as Gross Margin exceeds Cash OpEx.' },
        { metric: id ? '2028F Laba Bersih (GAAP)' : '2028F GAAP Net Income', before: '−Rp 4,348B', after: '+Rp 25.0B', delta: 'Reaches GAAP +', tone: 'pos', pctA: 100, pctB: 10, note: id ? 'Mencapai laba bersih positif pada Tahun ke-3 meski ROE hanya +0,09%.' : 'Reaches GAAP profitability in Year 3, though ROE is only +0.09%.' },
        { metric: id ? '2028F Saldo Kas Akhir' : '2028F Ending Cash Balance', before: 'Rp 0.97T', after: 'Rp 19.42T', delta: '+Rp 18.45T saved', tone: 'pos', pctA: 8, pctB: 100, note: id ? 'Menghilangkan ilusi kebangkrutan kas akibat asumsi OpEx 78,5%.' : 'Eliminates artificial cash depletion caused by the 78.5% OpEx error.' },
        { metric: id ? '2028F ROIC vs. WACC' : '2028F ROIC vs. WACC', before: 'Negative', after: '+2.70% vs 7.76%', delta: '−506 bps spread', tone: 'warn', pctA: 10, pctB: 35, note: id ? 'Masih menghancurkan nilai ekonomi meski operasional sudah untung.' : 'Still earns below cost of capital despite turning operationally profitable.' },
      ],
    }
  }

  if (sn >= 9 && sn <= 13) {
    return {
      tabLabel: id ? 'Pra vs. Pasca Exit' : 'Pre vs. Post Exit',
      title: id ? 'Dampak Valuasi: Dek Lama vs. Laporan Akhir (Pasca-Exit)' : 'Valuation Impact: Original Deck vs. Final Report (Post-Exit)',
      subtitle: id ? 'Koreksi basis pasca-Tokopedia mengangkat DCF +Rp131/sh, namun rekomendasi tetap SELL / AVOID' : 'Post-Tokopedia cleanup lifts Base DCF by +Rp131/sh, yet SELL / AVOID thesis holds firm',
      leftLabel: id ? 'Dek Awal (3-Thn)' : 'Original Deck (3-Yr Avg)',
      rightLabel: id ? 'Laporan Akhir (Pasca-Exit)' : 'Final Report (Post-Exit)',
      rows: [
        { metric: id ? 'Valuasi Base DCF / Saham' : 'Base DCF Value / Share', before: '−Rp 121.10', after: '+Rp 10.38', delta: '+Rp 131.48/sh', tone: 'pos', pctA: 100, pctB: 20, note: id ? 'Net Cash +Rp13,19/sh dikurangi Enterprise Value negatif −Rp2.989M.' : 'Net Cash +Rp13.19/sh minus negative Enterprise Value of −Rp2,989B.' },
        { metric: id ? 'Residual Income (Perpetual)' : 'Base Residual Income / Share', before: '−Rp 54.40', after: '−Rp 12.23', delta: 'g=0%: +Rp0.24', tone: 'accent', pctA: 100, pctB: 23, note: id ? 'ROE 2028F (+0,09%) jauh di bawah Cost of Equity (8,45%).' : '2028F ROE (+0.09%) remains far below the 8.45% Cost of Equity.' },
        { metric: id ? 'Rentang Nilai Intrinsik' : 'Defensible Intrinsic Range', before: 'Negative', after: 'Rp 10.38–16.75', delta: 'Net Cash: Rp13.19', tone: 'pos', pctA: 12, pctB: 75, note: id ? 'Berpusat pada Net Cash Rp13,19/sh hingga Optimistic RI Rp16,75/sh.' : 'Anchored between Base DCF (Rp10.38) and Optimistic RI (Rp16.75).' },
        { metric: id ? 'Rekomendasi Investasi' : 'Investment Recommendation', before: 'SELL / AVOID', after: 'SELL / AVOID', delta: 'Thesis intact', tone: 'warn', pctA: 100, pctB: 100, note: id ? 'Harga pasar masih jauh di atas rentang nilai intrinsik fundamental.' : 'Market price still trades well above fundamental intrinsic value range.' },
      ],
    }
  }

  return null
})
const hasCompareTab = computed(() => Boolean(comparisonData.value))

const explanationParagraphs = computed(() => {
  const raw = props.item.detail_explanation || props.item.explanation || ''
  const paras = String(raw)
    .split(/\n+/)
    .map((s) => s.trim())
    .filter(Boolean)

  const sn = props.item.slide?.slide_num
  const id = isId.value
  const joinedLen = paras.join(' ').length
  const t = `${props.item.title || ''} ${props.item.keywords || ''}`.toLowerCase()

  if (sn === 7 && joinedLen < 95) {
    if (t.includes('cogs') || t.includes('pokok')) {
      paras.push(
        id
          ? 'Pergerakan YoY: COGS naik dari 34,45% (2023 pra-exit) ke 46,64% (2024 pasca-exit) karena pergeseran bauran segmen, lalu turun −436 bps ke 42,28% di FY2025 berkat efisiensi biaya cloud >50% dan skala Gojek, serta membaik lagi ke 38,10% pada 1H 2026.'
          : 'YoY Driver Story: COGS jumped from 34.45% (2023 pre-exit) to 46.64% (2024 post-exit) on segment mix shift after deconsolidation, then fell −436 bps YoY to 42.28% in FY2025 via >50% cloud cost savings and Gojek scale, reaching 38.10% in 1H 2026.'
      )
    } else if (t.includes('opex') || t.includes('operating')) {
      paras.push(
        id
          ? 'Pergerakan YoY: Cash OpEx turun drastis dari 117,01% (2023) → 62,78% (2024) → 55,70% (2025, −708 bps YoY) melalui pemangkasan insentif (−Rp504,2M di Gojek) dan efisiensi korporasi, hingga menyentuh 51,20% pada 1H 2026.'
          : 'YoY Driver Story: Cash OpEx compressed sharply from 117.01% (2023) → 62.78% (2024) → 55.70% (2025, −708 bps YoY) through incentive cuts (−Rp504.2B at Gojek) and leaner corporate overhead, tightening further to 51.20% in 1H 2026.'
      )
    } else if (t.includes('growth') || t.includes('pertumbuhan') || t.includes('revenue')) {
      paras.push(
        id
          ? 'Pergerakan YoY: Pertumbuhan pendapatan lanjutan berlipat dua dari +7,50% (2024) ke +15,27% (2025) didorong lonjakan FinTech (+74,05% YoY; 90,96% kontribusi pertumbuhan) dan Gojek (+13,81% YoY).'
          : 'YoY Driver Story: Continuing revenue growth more than doubled from +7.50% (2024) to +15.27% (2025), powered by FinTech lending expansion (+74.05% YoY; 90.96% of net group growth) alongside On-Demand Services (+13.81% YoY).'
      )
    } else if (t.includes('capex') || t.includes('modal')) {
      paras.push(
        id
          ? 'Pergerakan YoY: Setelah mengeluarkan transfer aset takberwujud Tokopedia Rp5.464,9M dari 2024 (Catatan 12), CapEx lanjutan stabil dari 6,63% (2024) ke 6,45% (2025, −18 bps YoY), mematahkan ilusi lonjakan 41,0% di dek lama.'
          : 'YoY Driver Story: Once Rp5,464.9B of pre-deconsolidation Tokopedia intangible transfers are stripped out of 2024 (Note 12), continuing CapEx holds steady at 6.63% (2024) → 6.45% (2025, −18 bps YoY), correcting the 41.0% old-deck distortion.'
      )
    } else if (t.includes('debt') || t.includes('borrow') || t.includes('interest') || t.includes('bunga') || t.includes('utang')) {
      paras.push(
        id
          ? 'Pergerakan YoY: Biaya bunga efektif atas total utang dan liabilitas sewa penuh (Catatan 19–20 & 27b) bergerak 8,52% (2023) → 10,25% (2024) → 6,91% (2025, −334 bps YoY) seiring fasilitas pinjaman baru berbiaya lebih rendah.'
          : 'YoY Driver Story: Effective borrowing cost on full debt and lease liabilities (Notes 19–20 & 27b) moved 8.52% (2023) → 10.25% (2024) → 6.91% (2025, −334 bps YoY) as lower-cost bank facilities scaled in FY2025.'
      )
    }
  }
  return paras
})

const formulaHtml = computed(() => {
  if (!props.item.formula || !props.renderMath) return ''
  return props.renderMath(props.item.formula, true) || ''
})

// Build context-aware SVG chart configuration tailored to the clicked slide & item
const chartConfig = computed(() => {
  const sn = props.item.slide?.slide_num || 1
  const textBlob = `${props.item.title || ''} ${props.item.value || ''} ${props.item.keywords || ''}`.toLowerCase()
  const id = isId.value

  // Slide 1 & Slide 2: Gojek EBIT bridge or Segment EBIT breakdown
  if (sn === 1 || sn === 2) {
    if (textBlob.includes('gojek') || textBlob.includes('on-demand') || textBlob.includes('888')) {
      return {
        type: 'diverging',
        title: id ? 'Jembatan Laba Operasi (EBIT) Gojek: FY24 → FY25' : 'Gojek Segment EBIT Bridge: FY24 → FY25',
        subtitle: id ? 'Note 29 (Rp miliar) · Lonjakan +1.180% didorong efisiensi insentif & cloud' : 'Note 29 (Rp billion) · +1,180% surge driven by incentive cuts & cloud savings',
        unit: 'Rp bn',
        items: [
          { label: 'FY2024 EBIT', val: 69.4, display: '+69.4B' },
          { label: id ? 'Pendapatan Bruto 3P' : '3P Gross Revenue', val: 995.8, display: '+995.8B' },
          { label: id ? 'Pangkas Insentif (−15,9%)' : 'Incentive Cut (−15.9%)', val: 504.2, display: '+504.2B' },
          { label: id ? 'Antar-Segmen Bersih' : 'Inter-Segment Net', val: 67.8, display: '+67.8B' },
          { label: id ? 'Alokasi Korporasi' : 'Corp. Alloc. Cut', val: 32.5, display: '+32.5B' },
          { label: id ? 'Kenaikan Biaya 3P' : '3P Cost Growth', val: -781.1, display: '−781.1B' },
          { label: 'FY2025 EBIT', val: 888.6, display: '+888.6B', accent: true },
        ],
      }
    }
    return {
      type: 'diverging',
      title: id ? 'Kontribusi EBIT per Segmen (FY2025, Note 29)' : 'FY2025 Segment Operating Profit / Loss (Note 29)',
      subtitle: id ? 'Dalam Rp miliar · Gojek & Tokopedia Fee positif tertutup biaya korporasi' : 'In Rp billion · Positive Gojek & E-Commerce offset by Fintech & Corporate',
      unit: 'Rp bn',
      items: [
        { label: 'On-Demand (Gojek)', val: 888.6, display: '+888.6B', accent: true },
        { label: 'E-Commerce Fee', val: 572.2, display: '+572.2B' },
        { label: 'Fintech (GoPay)', val: -396.6, display: '−396.6B' },
        { label: id ? 'Biaya Korporasi' : 'Unalloc. Corporate', val: -1442.5, display: '−1,442.5B' },
        { label: id ? 'EBIT Konsolidasian' : 'Consolidated EBIT', val: -378.3, display: '−378.3B', accent: true },
      ],
    }
  }

  // Slide 3: Competition Spending & Provisions
  if (sn === 3) {
    return {
      type: 'horizontal',
      title: id ? 'Tekanan Rivalitas: Belanja Persaingan & Provisi Kredit' : 'Competitive Rivalry Cost & Credit Provision Burden',
      subtitle: id ? 'FY2025 (Rp miliar) · Provisi kredit Catatan 7 melonjak +134,9% YoY' : 'FY2025 (Rp billion) · Note 7 credit-loss provisions surged +134.9% YoY',
      unit: 'Rp bn',
      items: [
        { label: id ? 'Penjualan & Pemasaran' : 'Sales & Marketing', val: 3090.1, display: 'Rp 3,090B' },
        { label: id ? 'Pengembangan Produk' : 'Product Development', val: 2152.3, display: 'Rp 2,152B' },
        { label: id ? 'Insentif Beban S&M' : 'Expensed Incentives', val: 1076.9, display: 'Rp 1,077B' },
        { label: id ? 'Provisi Kredit 2024' : '2024 Loan Provisions', val: 173.6, display: 'Rp 174B' },
        { label: id ? 'Provisi Kredit 2025 (+134,9%)' : '2025 Provisions (+134.9%)', val: 407.7, display: 'Rp 408B', warn: true },
      ],
    }
  }

  // Slide 4: Profitability & DuPont ROE
  if (sn === 4) {
    return {
      type: 'diverging',
      title: id ? 'Lintasan ROE GoTo (2023–2025) vs. Pembanding Grab' : 'DuPont ROE Trajectory (2023–2025) vs. Grab Peer',
      subtitle: id ? 'Margin bersih negatif menahan ROE meski perputaran aset 0,40x' : 'Negative Net Margin keeps GoTo ROE below Grab (+2.96%) despite 0.40x turnover',
      unit: '%',
      clampMin: -30,
      items: [
        { label: id ? '2024 Pasca-Exit' : '2024 Post-Exit ROE', val: -17.97, display: '−17.97%' },
        { label: id ? '2025 Konsolidasian' : '2025 Consol. ROE', val: -5.23, display: '−5.23%', accent: true },
        { label: id ? '2025 Ekuitas Induk' : '2025 Parent ROE', val: -3.73, display: '−3.73%' },
        { label: 'Grab FY2025 Cons.', val: 2.96, display: '+2.96%', accent: true },
        { label: 'Grab FY2025 Parent', val: 3.98, display: '+3.98%' },
        { label: id ? 'Batas Cost of Equity' : 'GoTo Cost of Equity (Ke)', val: 8.45, display: '8.45% Hurdle' },
      ],
    }
  }

  // Slide 5: Liquidity, Solvency & Z-Score
  if (sn === 5) {
    if (textBlob.includes('z-score') || textBlob.includes('z score') || textBlob.includes('altman') || textBlob.includes('distress')) {
      return {
        type: 'diverging',
        title: id ? 'Komponen Tertimbang Altman Z-Score (FY2025)' : 'Altman Z-Score Weighted Factor Breakdown (FY2025)',
        subtitle: id ? 'X2 (rugi historis 2023) mendominasi skor −4,72; likuiditas X1 & X4 tetap positif' : 'X2 (sunk 2023 losses) drives Z = −4.72 while X1 working capital & X4 stay healthy',
        unit: 'Score',
        items: [
          { label: '1.2 × X1 (WC / Assets)', val: 0.483, display: '+0.48' },
          { label: '1.4 × X2 (Ret. Earn.)', val: -6.588, display: '−6.59', warn: true },
          { label: '3.3 × X3 (EBIT / Assets)', val: -0.027, display: '−0.03' },
          { label: '0.6 × X4 (Book Eq / Liab)', val: 1.008, display: '+1.01' },
          { label: '1.0 × X5 (Rev / Assets)', val: 0.400, display: '+0.40' },
          { label: 'Total Z (Book / Market)', val: -4.72, display: '−4.72 / −4.80', accent: true },
        ],
      }
    }
    if (chartBasis.value === 'previous') {
      return {
        type: 'vertical_cards',
        title: id ? 'Laporan Sebelumnya: Rasio Neraca 2023–2025 (Pra-Revisi)' : 'Previous Report: 2023–2025 Balance-Sheet Ratios (Pre-Restatement)',
        subtitle: id ? 'Menyertakan 2023 pra-exit; sorotan merah menandai kekeliruan 2024 sebelum koreksi' : 'Includes pre-exit 2023; rose bars flag unadjusted 2023–2024 errors before restatement',
        unit: id ? 'Pra-Revisi' : 'Prior Deck',
        cards: [
          {
            title: id ? 'Rasio Lancar' : 'Current Ratio',
            delta: id ? '2024 keliru' : '2024 understated',
            tone: 'warn',
            bars: [
              { label: '2023', val: 2.62, display: '2.62x' },
              { label: '2024', val: 2.46, display: '2.46x', warn: true },
              { label: '2025', val: 2.73, display: '2.73x', accent: true },
            ],
          },
          {
            title: id ? 'Utang / Ekuitas' : 'Debt / Equity',
            delta: id ? 'Tanpa sewa' : 'Excl. leases',
            tone: 'warn',
            bars: [
              { label: '2023', val: 9.69, display: '9.69%', warn: true },
              { label: '2024', val: 12.57, display: '12.57%', warn: true },
              { label: '2025', val: 26.97, display: '26.97%', accent: true },
            ],
          },
          {
            title: id ? 'DSO Piutang' : 'Trade DSO',
            delta: id ? 'Campur Cat. 7' : 'Mixed Note 7',
            tone: 'warn',
            note: id ? 'Mencampur piutang usaha Catatan 6 & pinjaman Catatan 7.' : 'Mixed Note 6 trade receivables with Note 7 loans.',
            bars: [
              { label: '2023', val: 14.75, display: '14.8d' },
              { label: '2024', val: 46.88, display: '46.9d', warn: true },
              { label: '2025', val: 10.90, display: '10.9d', accent: true },
            ],
          },
          {
            title: 'Times Interest Earned',
            delta: id ? 'N/M di dek lama' : 'N/M in old deck',
            tone: 'warn',
            note: id ? 'Bunga Catatan 27b belum ditautkan pada model awal.' : 'Note 27b interest expense was unlinked in prior model.',
            bars: [
              { label: '2023', val: 27.83, display: '−27.8x', warn: true },
              { label: '2024', val: 4.54, display: '−4.54x', warn: true },
              { label: '2025', val: 0.71, display: '−0.71x', warn: true },
            ],
          },
        ],
      }
    }
    return {
      type: 'vertical_cards',
      title: id ? 'Laporan Akhir: Rasio Likuiditas & Solvabilitas (Pasca-Exit 2024–2025)' : 'Current Final Report: Post-Exit Balance-Sheet Ratios (2024–2025)',
      subtitle: id ? '2023 pra-Tokopedia dikeluarkan; basis auditan bersih setelah koreksi Catatan 6, 7 & 19–20' : 'Pre-exit 2023 excluded; clean post-Tokopedia audited ratios after Notes 6, 7 & 19–20 fixes',
      unit: id ? 'Pasca-Exit' : 'Post-Exit',
      cards: [
        {
          title: id ? 'Rasio Lancar' : 'Current Ratio',
          delta: '+0.11x YoY',
          tone: 'pos',
          note: id ? 'Restorasi Cat. 7 (+Rp1,58T) & kas Rp21,8T jaga likuiditas.' : 'Note 7 restoration (+Rp1.58T) & Rp21.8T cash back WC buffer.',
          bars: [
            { label: '2024', val: 2.62, display: '2.62x' },
            { label: '2025', val: 2.73, display: '2.73x', accent: true },
          ],
        },
        {
          title: id ? 'Utang / Ekuitas' : 'Debt / Equity',
          delta: '+1,112 bps',
          tone: 'accent',
          note: id ? 'Pinjaman bank baru FY25 (+Rp3,72T) naikkan rasio utang.' : 'New FY25 bank borrowings (+Rp3.72T) lifted full debt+lease ratio.',
          bars: [
            { label: '2024', val: 15.85, display: '15.85%' },
            { label: '2025', val: 26.97, display: '26.97%', accent: true },
          ],
        },
        {
          title: id ? 'DSO Piutang' : 'Trade DSO',
          delta: '+0.34d YoY',
          tone: 'pos',
          note: id ? 'Basis piutang usaha Cat. 6 hapus lonjakan buatan 46,88h.' : 'Note 6 trade-only alignment removes 2024 artificial 46.88d spike.',
          bars: [
            { label: '2024', val: 10.56, display: '10.6d' },
            { label: '2025', val: 10.90, display: '10.9d', accent: true },
          ],
        },
        {
          title: 'Times Interest Earned',
          delta: '+3.83x YoY',
          tone: 'warn',
          note: id ? 'Rugi EBIT menyusut (−Rp2,24T → −Rp378M) vs bunga Rp535M.' : 'Narrowing EBIT loss (−Rp2.24T → −Rp378B) vs Rp535B interest.',
          bars: [
            { label: '2024', val: 4.54, display: '−4.54x', warn: true },
            { label: '2025', val: 0.71, display: '−0.71x', warn: true },
          ],
        },
      ],
    }
  }

  // Slide 6: Cash Flow & Accounting Quality
  if (sn === 6) {
    return {
      type: 'diverging',
      title: id ? 'Arus Kas FY2025 & Normalisasi CapEx 2024' : 'FY2025 Free Cash Flow Bridge & CapEx Normalization',
      subtitle: id ? 'CFO (+Rp307M) hanya menutup 25,97% CapEx; CapEx 2024 turun 41% → 6,63%' : 'CFO (+Rp307B) covers 25.97% of CapEx; 2024 continuing CapEx drops 41.0% → 6.63%',
      unit: 'Rp bn',
      items: [
        { label: id ? 'CFO FY2025' : 'FY2025 Operating CF', val: 307.0, display: '+307.0B', accent: true },
        { label: id ? 'CapEx Tunai FY2025' : 'FY2025 Cash CapEx', val: -1182.4, display: '−1,182.4B' },
        { label: id ? 'Arus Kas Bebas (FCF)' : 'FY2025 Free Cash Flow', val: -875.3, display: '−875.3B', warn: true },
        { label: id ? 'Pencairan Deposito' : 'Time Deposit Maturities', val: 1386.5, display: '+1,386.5B' },
        { label: id ? 'CFI Inti (Ex-Deposito)' : 'Core CFI (Ex-Deposits)', val: -867.4, display: '−867.4B' },
      ],
    }
  }

  // Slide 7: Forecast Assumptions
  if (sn === 7) {
    if (chartBasis.value === 'previous') {
      return {
        type: 'horizontal',
        title: id ? 'Laporan Sebelumnya: Asumsi Base Case (Dengan 2023)' : 'Previous Report: Base Case Drivers (With 2023 Included)',
        subtitle: id ? 'Rata-rata 3 tahun (2023–2025) sebelum 2023 pra-Tokopedia dikeluarkan' : 'Original 3-year averages (2023–2025) before removing pre-exit 2023 distortions',
        unit: '%',
        items: [
          { label: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth', val: 11.4, display: '11.40%' },
          { label: 'COGS / Revenue', val: 41.1, display: '41.10%' },
          { label: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue', val: 78.5, display: '78.50%', warn: true },
          { label: 'CapEx / Revenue', val: 16.3, display: '16.30%', warn: true },
        ],
      }
    }
    return {
      type: 'horizontal',
      title: id ? 'Laporan Akhir: Asumsi Base Case (Pasca-Exit, Tanpa 2023)' : 'Current Final Report: Base Case Drivers (Post-Exit, Ex-2023)',
      subtitle: id ? 'Berbasis murni pada lintasan operasional pasca-Tokopedia 2024–2025' : 'Anchored strictly on clean post-Tokopedia 2024–2025 continuing operations',
      unit: '%',
      items: [
        { label: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth', val: 15.27, display: '15.27%', accent: true },
        { label: 'COGS / Revenue', val: 42.28, display: '42.28%' },
        { label: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue', val: 55.70, display: '55.70%', accent: true },
        { label: 'CapEx / Revenue', val: 6.45, display: '6.45%' },
      ],
    }
  }

  // Slide 8: Three-Year Forecast
  if (sn === 8) {
    if (chartBasis.value === 'previous') {
      return {
        type: 'diverging',
        title: id ? 'Laporan Sebelumnya: Proyeksi 2026F–2028F (Dengan 2023)' : 'Previous Report: 2026F–2028F Outcomes (With 2023 Included)',
        subtitle: id ? 'OpEx 78,5% & CapEx 16,3% menciptakan rugi operasi −Rp4,97T dan menguras kas ke Rp968M' : '78.5% OpEx & 16.3% CapEx produced −Rp4.97T operating loss and artificial cash depletion',
        unit: 'Rp bn',
        items: [
          { label: id ? '2026F EBIT (Dek Lama)' : '2026F EBIT (Old 3-Yr)', val: -3854.0, display: '−3,854B', warn: true },
          { label: id ? '2027F EBIT (Dek Lama)' : '2027F EBIT (Old 3-Yr)', val: -4376.0, display: '−4,376B', warn: true },
          { label: id ? '2028F EBIT (Dek Lama)' : '2028F EBIT (Old 3-Yr)', val: -4967.4, display: '−4,967B', warn: true },
          { label: id ? '2028F Laba Bersih' : '2028F Net Income', val: -4347.9, display: '−4,348B', warn: true },
          { label: id ? '2028F Kas Akhir' : '2028F Ending Cash', val: 968.0, display: '+968B' },
        ],
      }
    }
    return {
      type: 'diverging',
      title: id ? 'Laporan Akhir: Skenario Proyeksi 2026F–2028F (Pasca-Exit)' : 'Current Final Report: 2026F–2028F Scenarios (Post-Exit)',
      subtitle: id ? 'Base Case berbalik EBIT positif (+Rp567M) & menjaga kas Rp19,42T; Optimis 1H26 +Rp3,22T' : 'Base Case turns EBIT-positive (+Rp567B) & preserves Rp19.4T cash; 1H26 Opt hits +Rp3.22T',
      unit: 'Rp bn',
      items: [
        { label: id ? '2028F EBIT Konservatif' : 'Conservative 2028F EBIT', val: -2143.4, display: '−2,143B', warn: true },
        { label: id ? '2026F EBIT Base' : 'Base 2026F EBIT', val: 426.9, display: '+426.9B' },
        { label: id ? '2028F EBIT Base' : 'Base 2028F EBIT', val: 567.2, display: '+567.2B', accent: true },
        { label: id ? '2028F NI Base' : 'Base 2028F Net Income', val: 25.0, display: '+25.0B' },
        { label: id ? '2028F EBIT Optimis 1H26' : 'Optimistic 2028F EBIT', val: 3221.1, display: '+3,221B', accent: true },
      ],
    }
  }

  // Slide 9: Cost of Capital
  if (sn === 9) {
    return {
      type: 'horizontal',
      title: id ? 'Struktur Biaya Modal (CAPM & WACC)' : 'Cost of Capital Build-Up & Hurdle Rates (%)',
      subtitle: id ? 'SUN 10T (30 Des 2025) & Spread Damodaran (1 Jan 2026); bobot 77,4% E / 22,6% D' : 'Dated Dec 30, 2025 bond yield & Jan 1, 2026 Damodaran ERP/CRP (77.4% E / 22.6% D)',
      unit: '%',
      items: [
        { label: id ? 'Imbal Hasil SUN 10Y' : 'ID 10Y Bond Yield', val: 6.12, display: '6.120%' },
        { label: id ? 'IDR Risk-Free (Rf)' : 'IDR Risk-Free (Rf)', val: 4.502, display: '4.502%' },
        { label: id ? 'Biaya Ekuitas (Ke)' : 'Cost of Equity (Ke)', val: 8.452, display: '8.452%', accent: true },
        { label: id ? 'Biaya Utang Setelah Pajak' : 'After-Tax Kd (22% tax)', val: 5.39, display: '5.390%' },
        { label: 'Base WACC', val: 7.761, display: '7.761%', accent: true },
        { label: id ? 'WACC Tanpa Tax Shield' : 'WACC (0% Tax Shield)', val: 8.101, display: '8.101%' },
      ],
    }
  }

  // Slide 10: DCF and Residual Income
  if (sn === 10) {
    if (chartBasis.value === 'previous') {
      return {
        type: 'diverging',
        title: id ? 'Laporan Sebelumnya: Valuasi DCF & RI (Dengan 2023)' : 'Previous Report: DCF & Residual Income (With 2023 Included)',
        subtitle: id ? 'Kontaminasi 2023 menghasilkan DCF −Rp121,10/sh dan RI −Rp75,10/sh' : 'Pre-exit 2023 contamination produced artificial −Rp121.10/sh DCF and −Rp75.10/sh RI',
        unit: 'Rp/sh',
        refLine: { val: 13.19, label: id ? 'Kas Bersih Rp13,19' : 'Net Cash Rp13.19' },
        items: [
          { label: id ? 'DCF Dek Lama (3 Thn)' : 'Previous DCF (3-Yr Avg)', val: -121.1, display: '−Rp121.10', warn: true },
          { label: id ? 'RI Dek Lama (3 Thn)' : 'Previous RI (3-Yr Avg)', val: -75.1, display: '−Rp75.10', warn: true },
          { label: id ? 'Kas Bersih / Saham' : 'Net Cash Floor / sh', val: 13.19, display: '+Rp13.19', accent: true },
        ],
      }
    }
    return {
      type: 'diverging',
      title: id ? 'Laporan Akhir: Valuasi DCF & Residual Income (Pasca-Exit)' : 'Current Final Report: DCF & Residual Income (Post-Exit)',
      subtitle: id ? 'Basis pasca-Tokopedia menghasilkan Base DCF +Rp10,38/sh vs. Kas Bersih Rp13,19/sh' : 'Clean post-Tokopedia basis yields +Rp10.38/sh Base DCF vs. Rp13.19/sh Net Cash floor',
      unit: 'Rp/sh',
      refLine: { val: 13.19, label: id ? 'Kas Bersih Rp13,19' : 'Net Cash Rp13.19' },
      items: [
        { label: id ? 'Base RI (g = 3,0%)' : 'Base RI (g = 3.0%)', val: -12.23, display: '−Rp12.23' },
        { label: id ? 'Base RI (g = 0%)' : 'Base RI (g = 0%)', val: 0.24, display: '+Rp0.24' },
        { label: id ? 'Base DCF (Pasca-Exit)' : 'Base DCF (Post-Exit)', val: 10.38, display: '+Rp10.38', accent: true },
        { label: id ? 'Kas Bersih / Saham' : 'Net Cash / Share', val: 13.19, display: '+Rp13.19' },
        { label: id ? 'RI Konvergensi Thn 4+' : 'RI (Yr4+ Convergence)', val: 21.13, display: '+Rp21.13' },
      ],
    }
  }

  // Slide 11: Grab Comparison & Football Field
  if (sn === 11) {
    return {
      type: 'diverging',
      title: id ? 'Peta Valuasi vs. Harga Pasar Rp25,00 & P/B Grab' : 'Valuation Football Field vs. Rp25.00 Market & Grab P/B',
      subtitle: id ? 'Rentang wajar Rp10,38–Rp16,75/sh jauh di bawah Rp25,00; P/B Grab Rp91,02 tidak setara' : 'Defensible Range (Rp10.38–Rp16.75) trails Rp25.00 market price; Grab P/B (Rp91.02) rejected',
      unit: 'Rp/sh',
      refLine: { val: 25.0, label: id ? 'Pasar Rp25,00' : 'Market Rp25.00' },
      items: [
        { label: id ? 'RI Konservatif' : 'Conservative RI', val: -44.42, display: '−Rp44.42' },
        { label: 'Base RI (g=3.0%)', val: -12.23, display: '−Rp12.23' },
        { label: 'Base DCF (Floor)', val: 10.38, display: '+Rp10.38', accent: true },
        { label: id ? 'Kas Bersih / Saham' : 'Net Cash / Share', val: 13.19, display: '+Rp13.19' },
        { label: 'Opt. RI (Ceiling)', val: 16.75, display: '+Rp16.75', accent: true },
        { label: 'Opt. DCF (1H26)', val: 47.34, display: '+Rp47.34' },
        { label: 'Grab P/B (3.04x)', val: 91.02, display: '+Rp91.02' },
      ],
    }
  }

  // Slide 12 & Slide 14: Recommendation & Reconciliation
  if (sn === 12 || sn === 14) {
    return {
      type: 'diverging',
      title: id ? 'Spread Ekonomi (ROIC vs. WACC) & Gap Harga Pasar' : 'Economic Return Spread (ROIC vs. WACC) & Valuation Gap',
      subtitle: id ? 'ROIC 2028F (+2,70%) tertinggal 506 bps di bawah WACC (7,76%) → SELL / AVOID di Rp25' : '2028F ROIC (+2.70%) trails WACC (7.76%) by 506 bps → SELL / AVOID holds at Rp25.00',
      unit: '%',
      items: [
        { label: '2028F Base ROIC', val: 2.70, display: '+2.70%', accent: true },
        { label: 'Base WACC Hurdle', val: 7.76, display: '7.76%' },
        { label: 'ROIC − WACC Spread', val: -5.06, display: '−5.06%', warn: true },
        { label: '2028F Base ROE', val: 0.09, display: '+0.09%' },
        { label: 'Cost of Equity (Ke)', val: 8.45, display: '8.45%' },
        { label: 'ROE − Ke Spread', val: -8.36, display: '−8.36%', warn: true },
      ],
    }
  }

  // Slide 13: 5 Forensic Fixes
  if (sn === 13) {
    if (chartBasis.value === 'previous') {
      return {
        type: 'horizontal',
        title: id ? 'Laporan Sebelumnya: Angka Sebelum 5 Koreksi (Dengan 2023)' : 'Previous Report: Pre-Restatement Figures (With 2023)',
        subtitle: id ? 'OpEx 78,5%, CapEx 41,0% & DSO 46,9 hari sebelum pembersihan forensik' : '78.5% OpEx, 41.0% CapEx & 46.9d DSO before forensic restatement',
        unit: id ? 'Pra-Revisi' : 'Prior Deck',
        items: [
          { label: 'Base Cash OpEx (%)', val: 78.5, display: '78.50%', warn: true },
          { label: '2024 Raw CapEx (%)', val: 41.0, display: '41.00%', warn: true },
          { label: '2024 Mixed DSO (d)', val: 46.88, display: '46.88d', warn: true },
          { label: '2024 Current Ratio', val: 2.46, display: '2.46x' },
        ],
      }
    }
    return {
      type: 'horizontal',
      title: id ? 'Laporan Akhir: Angka Auditan Setelah 5 Koreksi' : 'Current Final Report: Audited Figures After 5 Fixes',
      subtitle: id ? 'Basis pasca-Tokopedia yang bersih tanpa distorsi 2023 & aset takberwujud' : 'Clean post-Tokopedia audited basis with zero 2023 or intangible distortions',
      unit: id ? 'Laporan Akhir' : 'Final Report',
      items: [
        { label: 'Base Cash OpEx (%)', val: 55.70, display: '55.70%', accent: true },
        { label: '2024 Cont. CapEx (%)', val: 6.63, display: '6.63%' },
        { label: '2024 Trade DSO (d)', val: 10.56, display: '10.56d' },
        { label: '2024 Current Ratio', val: 2.62, display: '2.62x', accent: true },
      ],
    }
  }

  // Fallback for Appendices (15..20): parse numeric metrics from slide table or calculation_notes
  const parsed = []
  const notes = props.item.slide?.calculation_notes || []
  for (const c of notes.slice(0, 6)) {
    const raw = String(c.result || '').replace(/,/g, '')
    const m = raw.match(/([−\-+]?\d+(?:\.\d+)?)/)
    if (m) {
      const v = parseFloat(m[1].replace('−', '-'))
      if (Number.isFinite(v)) {
        parsed.push({ label: c.label, val: v, display: String(c.result) })
      }
    }
  }
  if (parsed.length >= 2) {
    return {
      type: 'diverging',
      title: id ? 'Visualisasi Angka Pendukung Lampiran' : 'Appendix Supporting Metrics Overview',
      subtitle: props.item.slide?.title || '',
      unit: '',
      items: parsed,
    }
  }
  return {
    type: 'diverging',
    title: id ? 'Ringkasan Valuasi Inti GoTo (Rp/saham)' : 'GoTo Core Valuation Benchmarks (Rp/share)',
    subtitle: id ? 'Basis Laporan Akhir pasca-Tokopedia vs. acuan Rp25,00' : 'Final Report post-Tokopedia basis vs. Rp25.00 reference price',
    unit: 'Rp/sh',
    refLine: { val: 25.0, label: 'Market Rp25' },
    items: [
      { label: 'Base RI', val: -12.23, display: '−Rp12.23' },
      { label: 'Base DCF', val: 10.38, display: '+Rp10.38', accent: true },
      { label: 'Net Cash / sh', val: 13.19, display: '+Rp13.19' },
      { label: 'Opt. RI Ceiling', val: 16.75, display: '+Rp16.75', accent: true },
      { label: 'Grab P/B Ref.', val: 91.02, display: '+Rp91.02' },
    ],
  }
})

// Compute SVG geometry for diverging / horizontal / grouped charts
const svgChartData = computed(() => {
  const cfg = chartConfig.value
  if (cfg.type === 'vertical_cards') {
    const cards = (cfg.cards || []).map((card) => {
      const maxVal = Math.max(...card.bars.map((b) => Math.abs(b.val)), 1)
      return {
        ...card,
        bars: card.bars.map((b) => ({
          ...b,
          heightPct: Math.max(16, Math.round((Math.abs(b.val) / maxVal) * 100)),
        })),
      }
    })
    return { mode: 'vertical_cards', cards }
  }
  const W = 780
  const labelW = 205
  const rightPad = 105
  const plotW = W - labelW - rightPad
  const rowH = 38
  const topPad = cfg.refLine ? 30 : 12

  if (cfg.type === 'grouped') {
    const rowHG = 50
    const h = 24 + cfg.items.length * rowHG + 10
    const maxVal = Math.max(...cfg.items.flatMap((it) => [Math.abs(it.a), Math.abs(it.b)]), 1)
    const rows = cfg.items.map((it, idx) => ({
      ...it,
      y: 16 + idx * rowHG,
      wA: Math.max(6, (Math.abs(it.a) / maxVal) * plotW),
      wB: Math.max(6, (Math.abs(it.b) / maxVal) * plotW),
    }))
    return { mode: 'grouped', W, H: h, labelW, plotW, rows }
  }

  if (cfg.type === 'horizontal') {
    const h = topPad + cfg.items.length * rowH + 14
    const maxVal = Math.max(...cfg.items.map((it) => Math.abs(it.val)), 1)
    const rows = cfg.items.map((it, idx) => ({
      ...it,
      y: topPad + idx * rowH,
      w: Math.max(6, (Math.abs(it.val) / maxVal) * plotW),
    }))
    return { mode: 'horizontal', W, H: h, labelW, plotW, rows }
  }

  // diverging
  const h = topPad + cfg.items.length * rowH + 18
  const vals = cfg.items.map((it) => it.val)
  if (cfg.refLine) vals.push(cfg.refLine.val)
  const rawMin = Math.min(0, ...vals)
  const rawMax = Math.max(0, ...vals)
  const span = Math.max(rawMax - rawMin, 1)
  const toX = (v) => labelW + ((v - rawMin) / span) * plotW
  const zeroX = toX(0)
  const refX = cfg.refLine ? toX(cfg.refLine.val) : null
  const rows = cfg.items.map((it, idx) => {
    const xVal = toX(it.val)
    return {
      ...it,
      y: topPad + idx * rowH,
      x: Math.min(zeroX, xVal),
      w: Math.max(3, Math.abs(xVal - zeroX)),
      isNeg: it.val < 0,
    }
  })
  return { mode: 'diverging', W, H: h, labelW, plotW, zeroX, refX, rows }
})

const yoySectionTitle = computed(() => {
  const sn = props.item.slide?.slide_num
  const id = isId.value
  const span = id ? '2023* | 2024–2025 Pasca-Exit' : '2023* | 2024–2025 Post-Exit'
  const span1H = id ? '2023* | 2024–1H26 Pasca-Exit' : '2023* | 2024–1H26 Post-Exit'
  const titles = {
    2: id ? `Perubahan Segmen YoY (${span} · Catatan 29)` : `Segment YoY Trajectory (${span} · Note 29)`,
    3: id ? `Tekanan Biaya & Risiko Kredit YoY (${span})` : `Competitive Cost & Credit Risk YoY (${span})`,
    4: id ? `Perubahan Rasio & DuPont YoY (${span} · Tabel 8–9)` : `Year-over-Year DuPont & Margin Trajectory (${span} · Tables 8–9)`,
    5: id ? `Perubahan Likuiditas & Solvabilitas YoY (${span} · Tabel 8)` : `Year-over-Year Liquidity & Leverage Movement (${span} · Table 8)`,
    6: id ? `Perubahan Kualitas Laba & Arus Kas YoY (${span} · Tabel 5)` : `Year-over-Year Cash Flow & Accrual Quality (${span} · Table 5)`,
    7: id ? `Lintasan Historis YoY di Balik Asumsi Driver (${span1H} · Tabel 11)` : `Historical YoY Driver Trajectory Behind Forecast Inputs (${span1H} · Table 11)`,
    8: id ? 'Lintasan Proyeksi Base Case (2025A → 2028F · Tabel 12)' : 'Restated Base Forecast Trajectory (2025A → 2028F · Table 12)',
  }
  return titles[sn] || ''
})

// Year-over-Year progression cards across Strategy, Ratios, Cash Flow, Assumptions & Forecast slides
const yoyRatioCards = computed(() => {
  const sn = props.item.slide?.slide_num
  const id = isId.value
  const titleText = `${props.item.title || ''} ${props.item.keywords || ''}`.toLowerCase()

  if (sn === 2) {
    return [
      {
        title: id ? 'EBIT On-Demand (Gojek)' : 'On-Demand (Gojek) EBIT',
        delta: '+1,180% YoY',
        tone: 'pos',
        note: id
          ? 'Pangkas insentif (−Rp504M), hemat cloud >50% & keluar Vietnam.'
          : 'Incentive cuts (−Rp504B), >50% cloud savings & Vietnam exit.',
        bars: [
          { yr: '2024', val: '+Rp69.4B', pct: 8 },
          { yr: '2025', val: '+Rp888.6B', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'Pendapatan FinTech (GoPay)' : 'FinTech (GoPay) Revenue',
        delta: '+74.05% YoY',
        tone: 'pos',
        note: id
          ? '90,96% pertumbuhan grup. Rugi segmen menyusut −64,3% (−Rp1,11T → −Rp397B).'
          : '90.96% of group growth. Segment loss narrowed −64.3% (−Rp1.11T → −Rp397B).',
        bars: [
          { yr: '2024', val: 'Rp2.98T', pct: 57 },
          { yr: '2025', val: 'Rp5.19T', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'Pendapatan Bersih Konsolidasi' : 'Consolidated Net Revenue',
        delta: '+15.27% YoY',
        tone: 'pos',
        note: id
          ? 'Pertumbuhan inti pasca-exit berlipat dua dari +7,5% (2024).'
          : 'Post-exit core growth more than doubled from +7.5% (2024).',
        bars: [
          { yr: '2023*', val: 'Rp14.79T', pct: 81 },
          { yr: '2024', val: 'Rp15.89T', pct: 87 },
          { yr: '2025', val: 'Rp18.32T', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'EBIT Konsolidasian' : 'Consolidated EBIT',
        delta: '+83.1% YoY',
        tone: 'warn',
        note: id
          ? 'Segmen inti positif (+Rp1,46T), tertutup biaya korporasi −Rp1,44T.'
          : 'Core segments positive (+Rp1.46T), offset by −Rp1.44T corporate overhead.',
        bars: [
          { yr: '2023*', val: '−Rp10.28T', pct: 100 },
          { yr: '2024', val: '−Rp2.24T', pct: 28 },
          { yr: '2025', val: '−Rp378B', pct: 10, current: true },
        ],
      },
    ]
  }

  if (sn === 3) {
    return [
      {
        title: id ? 'Provisi Kredit (Catatan 7)' : 'Credit-Loss Provisions (Note 7)',
        delta: '+134.9% YoY',
        tone: 'warn',
        note: id
          ? 'Mencapai 12,99% pinjaman bruto seiring ekspansi kredit GoPay.'
          : '12.99% of gross loans as GoPay scales consumer credit.',
        bars: [
          { yr: '2024', val: 'Rp173.6B', pct: 43 },
          { yr: '2025', val: 'Rp407.7B', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue',
        delta: '−708 bps YoY',
        tone: 'pos',
        note: id
          ? 'Disiplin promo memangkas bakar kas, tetapi rivalitas batasi harga.'
          : 'Promo discipline narrowed burn, but rivalry caps pricing power.',
        bars: [
          { yr: '2023*', val: '117.0%', pct: 100 },
          { yr: '2024', val: '62.78%', pct: 54 },
          { yr: '2025', val: '55.70%', pct: 48, current: true },
        ],
      },
    ]
  }

  if (sn === 4) {
    return [
      {
        title: id ? 'Margin Operasi (EBIT %)' : 'Operating Margin (EBIT %)',
        delta: '+1,204 bps YoY',
        tone: 'warn',
        note: id
          ? 'Efisiensi insentif & cloud mengangkat margin inti ke ambang impas.'
          : 'Incentive cuts & cloud savings lifted core margin near breakeven.',
        bars: [
          { yr: '2023*', val: '−69.5%', pct: 100 },
          { yr: '2024', val: '−14.10%', pct: 32 },
          { yr: '2025', val: '−2.06%', pct: 10, current: true },
        ],
      },
      {
        title: id ? 'Margin Laba Bersih' : 'Net Profit Margin',
        delta: '+2,618 bps YoY',
        tone: 'warn',
        note: id
          ? 'Rugi bersih menyusut, namun kompensasi berbasis saham Rp593B & bunga masih membebani.'
          : 'Bottom line improved sharply, yet Rp593B share-based compensation & finance costs weigh.',
        bars: [
          { yr: '2023*', val: '−612.2%', pct: 100 },
          { yr: '2024', val: '−34.38%', pct: 28 },
          { yr: '2025', val: '−8.20%', pct: 11, current: true },
        ],
      },
      {
        title: id ? 'Perputaran Aset (ATO)' : 'Total Asset Turnover',
        delta: '+8.8% YoY',
        tone: 'pos',
        note: id
          ? 'Aset bersih 2024 direvisi (+Rp1,58T Cat. 7) & pertumbuhan +15,3%.'
          : 'Restated 2024 assets (+Rp1.58T Note 7) plus +15.3% revenue scale.',
        bars: [
          { yr: '2023*', val: '0.27x', pct: 68 },
          { yr: '2024', val: '0.37x', pct: 92 },
          { yr: '2025', val: '0.40x', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'ROE Konsolidasian (vs Grab +2,96%)' : 'Cons. ROE (vs Grab +2.96%)',
        delta: '+1,274 bps YoY',
        tone: 'warn',
        note: id
          ? 'Leverage moderat (1,59x) belum membantu saat margin masih negatif.'
          : 'Higher EM (1.59x) still amplifies negative margins below Ke (8.45%).',
        bars: [
          { yr: '2023*', val: '−253.4%', pct: 100 },
          { yr: '2024', val: '−17.97%', pct: 30 },
          { yr: '2025', val: '−5.23%', pct: 12, current: true },
        ],
      },
    ]
  }

  if (sn === 5) {
    return [
      {
        title: id ? 'Rasio Lancar (Current Ratio)' : 'Current Ratio',
        delta: '+0.11x YoY',
        tone: 'pos',
        note: id
          ? 'Pemulihan Catatan 7 (+Rp1,58T) & kas kuat jaga penyangga modal kerja Rp18,41T.'
          : 'Note 7 restoration (+Rp1.58T) & Rp21.8T cash support Rp18.41T WC buffer.',
        bars: [
          { yr: '2023*', val: '2.62x', pct: 87 },
          { yr: '2024', val: '2.62x', pct: 87 },
          { yr: '2025', val: '2.73x', pct: 91, current: true },
        ],
      },
      {
        title: id ? 'Piutang Usaha DSO (Cat. 6)' : 'Trade DSO (Note 6)',
        delta: '+0.34d YoY',
        tone: 'pos',
        note: id
          ? 'Penyelarasan ke Catatan 6 hilangkan anomali 46,88 hari di 2024.'
          : 'Note 6 trade-only alignment removes 2024’s artificial 46.88d spike.',
        bars: [
          { yr: '2023*', val: '14.84d', pct: 92 },
          { yr: '2024', val: '10.56d', pct: 66 },
          { yr: '2025', val: '10.90d', pct: 68, current: true },
        ],
      },
      {
        title: id ? 'Utang / Ekuitas (Cat. 19–20)' : 'Debt-to-Equity (Notes 19–20)',
        delta: '+11.12 pp YoY',
        tone: 'accent',
        note: id
          ? 'Penarikan utang baru (+Rp3,72T) tingkatkan leverage ke 26,97%.'
          : 'New FY2025 bank borrowings (+Rp3.72T) lifted full debt+lease ratio.',
        bars: [
          { yr: '2023*', val: '12.14%', pct: 45 },
          { yr: '2024', val: '15.85%', pct: 59 },
          { yr: '2025', val: '26.97%', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'Cakupan Bunga (TIE, Cat. 27b)' : 'Times Interest Earned (TIE)',
        delta: '+3.83x YoY',
        tone: 'warn',
        note: id
          ? 'EBIT membaik −Rp2,24T → −Rp378B. Bunga Catatan 27b sebesar Rp535,2B.'
          : 'Narrowing EBIT loss (−Rp2.24T → −Rp378B) vs. Rp535.2B Note 27b interest.',
        bars: [
          { yr: '2023*', val: '−27.83x', pct: 100 },
          { yr: '2024', val: '−4.54x', pct: 26 },
          { yr: '2025', val: '−0.71x', pct: 8, current: true },
        ],
      },
    ]
  }

  if (sn === 6) {
    return [
      {
        title: id ? 'Arus Kas Operasi (CFO)' : 'Operating Cash Flow (CFO)',
        delta: '+Rp929B YoY',
        tone: 'pos',
        note: id
          ? 'CFO membaik dari −Rp4,33T (2023*) ke +Rp307B, namun baru menutup 25,97% CapEx FY25.'
          : 'Recovered from −Rp4.33T (2023*) to +Rp307B, but funds only 25.97% of FY25 CapEx.',
        bars: [
          { yr: '2023*', val: '−Rp4.33T', pct: 100 },
          { yr: '2024', val: '−Rp622.1B', pct: 34 },
          { yr: '2025', val: '+Rp307.0B', pct: 22, current: true },
        ],
      },
      {
        title: id ? 'CapEx Lanjutan / Pendapatan' : 'Continuing CapEx / Rev',
        delta: '−18 bps YoY',
        tone: 'pos',
        note: id
          ? 'Tanpa transfer takberwujud Tokopedia Rp5,46T Catatan 12 di 2024.'
          : 'Excludes Rp5.46T Tokopedia Note 12 intangible transfer in 2024.',
        bars: [
          { yr: '2023*', val: '1.49%', pct: 22 },
          { yr: '2024', val: '6.63%', pct: 100 },
          { yr: '2025', val: '6.45%', pct: 97, current: true },
        ],
      },
      {
        title: id ? 'Rasio Akrual Dilaporkan' : 'Reported Accrual Ratio',
        delta: '+726 bps YoY',
        tone: 'warn',
        note: id
          ? '2023* terdistorsi goodwill Rp78,8T. Beban non-tunai menyusut tajam pasca-exit.'
          : '2023* distorted by Rp78.8T goodwill write-off. Non-cash charges shrank post-exit.',
        bars: [
          { yr: '2023*', val: '−159.3%', pct: 100 },
          { yr: '2024', val: '−11.21%', pct: 32 },
          { yr: '2025', val: '−3.95%', pct: 16, current: true },
        ],
      },
      {
        title: id ? 'Akrual Laba Berulang' : 'Adj. Recurring Accrual',
        delta: '+175 bps YoY',
        tone: 'warn',
        note: id
          ? '2023* tanpa goodwill. Tetap menahan kompensasi berbasis saham (Rp593B) & provisi kredit.'
          : '2023* ex-goodwill. Retains share-based compensation (Rp593B) & loan provisions as real costs.',
        bars: [
          { yr: '2023*', val: '−13.73%', pct: 100 },
          { yr: '2024', val: '−3.69%', pct: 36 },
          { yr: '2025', val: '−1.94%', pct: 20, current: true },
        ],
      },
    ]
  }

  if (sn === 7) {
    return [
      {
        title: 'COGS / Revenue',
        delta: id ? '−436 bps YoY 24→25' : '−436 bps YoY 24→25',
        tone: 'pos',
        focused: titleText.includes('cogs') || titleText.includes('pokok'),
        note: id
          ? 'Bauran segmen lonjakkan 2024. Efisiensi cloud >50% pangkas COGS 2025 & 1H26.'
          : 'Mix shift spiked 2024 post-exit. Over 50% cloud savings cut COGS in 2025 & 1H26.',
        bars: [
          { yr: '2023*', val: '34.45%', pct: 74 },
          { yr: '2024', val: '46.64%', pct: 100 },
          { yr: '2025', val: '42.28%', pct: 91, current: true },
          { yr: '1H26', val: '38.10%', pct: 82 },
        ],
      },
      {
        title: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue',
        delta: '−708 bps YoY 24→25',
        tone: 'pos',
        focused: titleText.includes('opex') || titleText.includes('operating') || titleText.includes('operasi'),
        note: id
          ? 'Pemangkasan insentif & korporasi mendorong spread operasi +202 bps.'
          : 'Incentive cuts & leaner headcount drive the +202 bps operating spread.',
        bars: [
          { yr: '2023*', val: '117.01%', pct: 100 },
          { yr: '2024', val: '62.78%', pct: 54 },
          { yr: '2025', val: '55.70%', pct: 48, current: true },
          { yr: '1H26', val: '51.20%', pct: 44 },
        ],
      },
      {
        title: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth Rate',
        delta: '+777 bps YoY',
        tone: 'pos',
        focused: titleText.includes('growth') || titleText.includes('pertumbuhan') || titleText.includes('revenue'),
        note: id
          ? 'Pertumbuhan inti berlipat dua saat pinjaman GoPay (+74%) & Gojek (+14%) melesat.'
          : 'Post-exit core growth doubled as GoPay loans (+74%) & Gojek (+14%) scaled.',
        bars: [
          { yr: '2024', val: '+7.50%', pct: 42 },
          { yr: '2025', val: '+15.27%', pct: 85, current: true },
          { yr: 'Base', val: '+15.27%', pct: 85 },
          { yr: 'Opt', val: '+18.00%', pct: 100 },
        ],
      },
      {
        title: id ? 'CapEx Lanjutan / Pendapatan' : 'Continuing CapEx / Rev',
        delta: '−18 bps YoY 24→25',
        tone: 'accent',
        focused: titleText.includes('capex') || titleText.includes('modal'),
        note: id
          ? 'Stabil ~6,5% setelah transfer Tokopedia Rp5,46T dikeluarkan dari 2024.'
          : 'Stable ~6.5% run-rate once Rp5.46T Tokopedia intangibles are removed.',
        bars: [
          { yr: '2023*', val: '1.49%', pct: 22 },
          { yr: '2024', val: '6.63%', pct: 100 },
          { yr: '2025', val: '6.45%', pct: 97, current: true },
        ],
      },
    ]
  }

  if (sn === 8) {
    return [
      {
        title: id ? 'Proyeksi Pendapatan (Base)' : 'Projected Revenue (Base)',
        delta: '+15.27%/yr',
        tone: 'pos',
        note: id
          ? 'Bertumbuh majemuk pada basis pasca-Tokopedia yang bersih.'
          : 'Compounds on clean post-Tokopedia growth run-rate.',
        bars: [
          { yr: '2025A', val: 'Rp18.32T', pct: 65 },
          { yr: '2026F', val: 'Rp21.12T', pct: 75 },
          { yr: '2027F', val: 'Rp24.35T', pct: 87 },
          { yr: '2028F', val: 'Rp28.07T', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'Proyeksi EBIT (Base)' : 'Projected EBIT (Base)',
        delta: id ? 'Berbalik + di 2026F' : 'Flips + in 2026F',
        tone: 'pos',
        note: id
          ? 'Margin of Safety tipis (+3,50%) & leverage operasi 28,56x tinggi.'
          : 'Tight +3.50% Margin of Safety & high 28.56x DOL.',
        bars: [
          { yr: '2025A', val: '−Rp378B', pct: 48 },
          { yr: '2026F', val: '+Rp427B', pct: 75 },
          { yr: '2027F', val: '+Rp492B', pct: 87 },
          { yr: '2028F', val: '+Rp567B', pct: 100, current: true },
        ],
      },
      {
        title: id ? 'Proyeksi Laba Bersih (Base)' : 'Projected Net Income (Base)',
        delta: id ? 'Positif di 2028F' : 'Turns + in 2028F',
        tone: 'accent',
        note: id
          ? 'ROIC 2028F (+2,70%) masih tertinggal −506 bps di bawah WACC (7,76%).'
          : '2028F ROIC (+2.70%) still trails WACC (7.76%) by −506 bps.',
        bars: [
          { yr: '2025A', val: '−Rp1,502B', pct: 100 },
          { yr: '2026F', val: '−Rp84.5B', pct: 18 },
          { yr: '2027F', val: '−Rp33.6B', pct: 10 },
          { yr: '2028F', val: '+Rp25.0B', pct: 8, current: true },
        ],
      },
      {
        title: id ? 'Proyeksi Kas Akhir (Base)' : 'Projected Ending Cash (Base)',
        delta: '−Rp2.33T / 3 yrs',
        tone: 'pos',
        note: id
          ? 'Menjaga kas Rp19,4T vs. hanya Rp968M pada dek awal.'
          : 'Preserves Rp19.4T liquidity vs. Rp968B in the old 2023-polluted deck.',
        bars: [
          { yr: '2025A', val: 'Rp21.76T', pct: 100 },
          { yr: '2026F', val: 'Rp20.69T', pct: 95 },
          { yr: '2027F', val: 'Rp19.96T', pct: 92 },
          { yr: '2028F', val: 'Rp19.42T', pct: 89, current: true },
        ],
      },
    ]
  }
  return null
})

// Keep all 3 years visible (with a vertical Post-Exit divider after 2023*) so the structural break is clear
const visibleYoyRatioCards = computed(() => yoyRatioCards.value)
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-fade">
      <div class="glass-modal-backdrop">
        <div class="glass-modal-scrim" @click="emit('close')" aria-hidden="true"></div>
        <section
          class="glass-modal-panel"
          role="dialog"
          aria-modal="true"
          aria-labelledby="glass-modal-title"
        >
        <!-- Header -->
        <header class="glass-modal-header">
          <div class="glass-hdr-left">
            <span class="glass-slide-pill">
              {{ isId ? 'SLIDE' : 'SLIDE' }} {{ item.slide?.slide_num }} · {{ item.slide?.section_tag || (isId ? 'Analisis Mendalam' : 'Deep Insight') }}
            </span>
            <h2 id="glass-modal-title">{{ item.title }}</h2>
            <div v-if="item.value" class="glass-value-pill">{{ item.value }}</div>
          </div>
          <div class="glass-hdr-actions">
            <button
              type="button"
              class="glass-close-btn"
              @click="emit('close')"
              :aria-label="isId ? 'Tutup' : 'Close'"
              title="Esc"
            >
              &times;
            </button>
          </div>
        </header>

        <!-- Top Navigation Tab Bar (Clean Icon-Only Tabs with Tooltips) -->
        <nav class="glass-tab-bar" role="tablist" :aria-label="isId ? 'Bagian Analisis' : 'Insight Sections'">
          <div class="glass-tab-group">
            <button
              type="button"
              role="tab"
              class="glass-tab-btn is-icon-only"
              :class="{ 'is-active': activeTab === 'overview' }"
              :aria-selected="activeTab === 'overview'"
              :title="isSlide9Walkthrough ? (isId ? 'Sumber & Perhitungan' : 'Sources & Math') : (isId ? 'Grafik & Data' : 'Charts & Data')"
              :aria-label="isSlide9Walkthrough ? (isId ? 'Sumber & Perhitungan' : 'Sources & Math') : (isId ? 'Grafik & Data' : 'Charts & Data')"
              @click="activeTab = 'overview'"
            >
              <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M3 3v18h18" /><path d="M18 17V9" /><path d="M13 17V5" /><path d="M8 17v-3" />
              </svg>
            </button>

            <button
              v-if="hasCompareTab"
              type="button"
              role="tab"
              class="glass-tab-btn is-icon-only"
              :class="{ 'is-active': activeTab === 'compare' }"
              :aria-selected="activeTab === 'compare'"
              :title="comparisonData.tabLabel"
              :aria-label="comparisonData.tabLabel"
              @click="activeTab = 'compare'"
            >
              <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="m16 3 4 4-4 4" /><path d="M20 7H4" /><path d="m8 21-4-4 4-4" /><path d="M4 17h16" />
              </svg>
            </button>

            <button
              v-if="hasCalcTab"
              type="button"
              role="tab"
              class="glass-tab-btn is-icon-only"
              :class="{ 'is-active': activeTab === 'calc' }"
              :aria-selected="activeTab === 'calc'"
              :title="isId ? 'Perhitungan & Rumus' : 'Calculations & Formula'"
              :aria-label="isId ? 'Perhitungan & Rumus' : 'Calculations & Formula'"
              @click="activeTab = 'calc'"
            >
              <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <rect width="16" height="20" x="4" y="2" rx="2" /><line x1="8" x2="16" y1="6" y2="6" /><line x1="8" x2="10" y1="11" y2="11" /><line x1="14" x2="16" y1="11" y2="11" /><line x1="8" x2="10" y1="15" y2="15" /><line x1="14" x2="16" y1="15" y2="15" /><line x1="8" x2="16" y1="19" y2="19" />
              </svg>
            </button>

            <button
              v-if="hasSchedulesTab"
              type="button"
              role="tab"
              class="glass-tab-btn is-icon-only"
              :class="{ 'is-active': activeTab === 'schedules' }"
              :aria-selected="activeTab === 'schedules'"
              :title="isId ? 'Jadwal & Bukti' : 'Schedules & Proof'"
              :aria-label="isId ? 'Jadwal & Bukti' : 'Schedules & Proof'"
              @click="activeTab = 'schedules'"
            >
              <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" /><path d="M8 13h8" /><path d="M8 17h8" />
              </svg>
            </button>

            <button
              v-if="hasTracesTab"
              type="button"
              role="tab"
              class="glass-tab-btn is-icon-only"
              :class="{ 'is-active': activeTab === 'traces' }"
              :aria-selected="activeTab === 'traces'"
              :title="isId ? 'Jejak Tugas & Materi' : 'Workbook & Lectures'"
              :aria-label="isId ? 'Jejak Tugas & Materi' : 'Workbook & Lectures'"
              @click="activeTab = 'traces'"
            >
              <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" /><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
              </svg>
            </button>
          </div>

          <button
            v-if="activeTab === 'overview' && hasAnalysisTab && !isSlide9Walkthrough"
            type="button"
            class="glass-panel-toggle"
            :class="{ 'is-on': showRightPanel }"
            @click="showRightPanel = !showRightPanel"
          >
            <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M15 3v18" />
            </svg>
            <span>{{ showRightPanel ? (isId ? 'Sembunyikan Analisis' : 'Hide Analysis') : (isId ? 'Tampilkan Analisis' : 'Show Analysis') }}</span>
          </button>
        </nav>

        <!-- Slide 9 Interactive Component Sub-Menu Bar (directly below main top bar) -->
        <div
          v-if="isSlide9Walkthrough && activeTab === 'overview'"
          class="glass-sub-nav"
          role="tablist"
          :aria-label="isId ? 'Komponen Biaya Modal' : 'Cost of Capital Components'"
        >
          <button
            v-for="comp in slide9Components"
            :key="comp.id"
            type="button"
            role="tab"
            class="glass-sub-pill"
            :class="{ 'is-active': activeSlide9Comp === comp.id }"
            :aria-selected="activeSlide9Comp === comp.id"
            @click="activeSlide9Comp = comp.id"
          >
            {{ comp.shortLabel }}
          </button>
        </div>

        <!-- Independent Vertical-Scrolling Tab Panels -->
        <div class="glass-modal-body">
          <!-- SLIDE 9 SPECIAL VIEW: Clean Zero-Scroll Side-by-Side (Left: Big Result, Right: Compact Source Table) -->
          <div
            v-if="activeTab === 'overview' && isSlide9Walkthrough"
            class="glass-s9-split"
            :key="'tab-s9-' + currentSlide9Comp.id"
          >
            <!-- Left: Big Result + Formula + One-Line Meaning -->
            <div class="glass-card glass-s9-left">
              <div class="glass-s9-left-top">
                <span class="glass-s9-eyebrow">{{ currentSlide9Comp.title }}</span>
                <div class="glass-s9-big-val">{{ currentSlide9Comp.result }}</div>
                <div class="glass-s9-formula-bar">
                  <code>{{ currentSlide9Comp.formula }}</code>
                </div>
                <p class="glass-s9-one-liner">{{ currentSlide9Comp.usedIn }}</p>
              </div>
              <div class="glass-s9-nav-btns">
                <button
                  v-if="prevSlide9Comp"
                  type="button"
                  class="glass-s9-nav-btn"
                  @click="activeSlide9Comp = prevSlide9Comp.id"
                >
                  ← {{ prevSlide9Comp.shortLabel }}
                </button>
                <button
                  v-if="nextSlide9Comp"
                  type="button"
                  class="glass-s9-nav-btn is-next"
                  @click="activeSlide9Comp = nextSlide9Comp.id"
                >
                  {{ nextSlide9Comp.shortLabel }} →
                </button>
              </div>
            </div>

            <!-- Right: Clean Compact Table (Inputs, Sources & Math Steps — Zero Cards, Zero Scroll) -->
            <div class="glass-card glass-s9-right">
              <table class="glass-s9-table">
                <thead>
                  <tr>
                    <th>{{ isId ? 'Komponen / Langkah' : 'Input / Step' }}</th>
                    <th class="is-num">{{ isId ? 'Nilai' : 'Value' }}</th>
                    <th>{{ isId ? 'Sumber / Keterangan' : 'Source / Note' }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(src, sIdx) in currentSlide9Comp.sources"
                    :key="currentSlide9Comp.id + '-r-' + sIdx"
                  >
                    <td class="is-lbl">{{ src.label }}</td>
                    <td class="is-num is-val">{{ src.value }}</td>
                    <td class="is-src">{{ src.source }}</td>
                  </tr>
                  <tr
                    v-for="(st, stIdx) in currentSlide9Comp.steps"
                    :key="currentSlide9Comp.id + '-st-' + stIdx"
                    class="is-step-row"
                    :class="{ 'is-final-row': stIdx === currentSlide9Comp.steps.length - 1 }"
                  >
                    <td class="is-lbl">{{ st.expr }}</td>
                    <td class="is-num is-out">{{ st.out }}</td>
                    <td class="is-src">{{ stIdx === currentSlide9Comp.steps.length - 1 ? (isId ? 'Hasil Akhir' : 'Final Result') : (isId ? 'Langkah ' + st.step : 'Step ' + st.step) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- TAB 1: Side-by-Side Independent Vertical Scrollers (Left: Charts & Data, Right: Deep Analysis) -->
          <div
            v-else-if="activeTab === 'overview'"
            class="glass-split-view"
            :class="{ 'is-single': !hasAnalysisTab || !showRightPanel }"
            key="tab-overview"
          >
            <!-- Panel 1 (Left): All Charts & YoY Data as a Vertical Scroller -->
            <div class="glass-pane-scroll">
              <div class="glass-card glass-chart-card">
                <div class="glass-card-hdr">
                  <div>
                    <h3>{{ chartConfig.title }}</h3>
                    <p class="glass-chart-sub">{{ chartConfig.subtitle }}</p>
                  </div>
                  <div class="glass-chart-hdr-right">
                    <div
                      v-if="hasChartBasisSwitch"
                      class="glass-basis-switch"
                      role="group"
                      :aria-label="isId ? 'Pilih versi laporan grafik' : 'Select report version for chart'"
                    >
                      <button
                        type="button"
                        class="glass-basis-btn is-prev"
                        :class="{ 'is-active': chartBasis === 'previous' }"
                        @click="chartBasis = 'previous'"
                      >
                        {{ isId ? 'Laporan Lama (Dengan 2023)' : 'Previous Report (With 2023)' }}
                      </button>
                      <button
                        type="button"
                        class="glass-basis-btn"
                        :class="{ 'is-active': chartBasis === 'current' }"
                        @click="chartBasis = 'current'"
                      >
                        {{ isId ? 'Laporan Akhir (Pasca-Exit)' : 'Current Report (Post-Exit)' }}
                      </button>
                    </div>
                    <span v-if="chartConfig.unit" class="glass-unit-badge">{{ chartConfig.unit }}</span>
                  </div>
                </div>

                <div v-if="chartConfig.type === 'grouped'" class="glass-legend-row">
                  <span class="glass-leg-item"><i class="leg-dot leg-a"></i>{{ chartConfig.legendA }}</span>
                  <span class="glass-leg-item"><i class="leg-dot leg-b"></i>{{ chartConfig.legendB }}</span>
                </div>

                <!-- 3-Per-Row Vertical Column Chart Cards -->
                <div
                  v-if="svgChartData.mode === 'vertical_cards'"
                  :key="`vc-${item.slide?.slide_num}-${chartBasis}`"
                  class="glass-vchart-grid"
                >
                  <div
                    v-for="(vc, vIdx) in svgChartData.cards"
                    :key="vc.title"
                    class="glass-vchart-card"
                    :style="{ animationDelay: `${vIdx * 60}ms` }"
                  >
                    <div class="glass-vchart-hdr">
                      <strong>{{ vc.title }}</strong>
                      <span class="glass-yoy-delta" :class="`tone-${vc.tone}`">{{ vc.delta }}</span>
                    </div>
                    <div class="glass-vchart-plot">
                      <template v-for="(bar, bIdx) in vc.bars" :key="bar.label">
                        <div class="glass-vchart-col">
                          <span
                            class="glass-vchart-val"
                            :class="{ 'is-warn': bar.warn || String(bar.display).startsWith('−'), 'is-accent': bar.accent }"
                          >{{ bar.display }}</span>
                          <div class="glass-vchart-bar-wrap">
                            <span
                              class="glass-vchart-bar"
                              :class="{ 'is-warn': bar.warn || String(bar.display).startsWith('−'), 'is-accent': bar.accent }"
                              :style="{ height: `${bar.heightPct}%`, animationDelay: `${vIdx * 60 + bIdx * 55}ms` }"
                            ></span>
                          </div>
                          <span class="glass-vchart-lbl">{{ bar.label }}</span>
                        </div>
                        <div
                          v-if="String(bar.label).startsWith('2023') && bIdx < vc.bars.length - 1"
                          class="glass-vchart-divider"
                          :title="isId ? 'Dekonsolidasi Tokopedia (Jan 2024)' : 'Tokopedia Deconsolidation (Jan 2024)'"
                        >
                          <span class="glass-vchart-div-tag">{{ isId ? 'Exit' : 'Exit' }}</span>
                          <span class="glass-vchart-div-line" aria-hidden="true"></span>
                        </div>
                      </template>
                    </div>
                    <p v-if="vc.note" class="glass-yoy-note">{{ vc.note }}</p>
                  </div>
                </div>

                <svg
                  v-else
                  :key="`${item.slide?.slide_num}-${chartBasis}`"
                  :viewBox="`0 0 ${svgChartData.W} ${svgChartData.H}`"
                  class="glass-svg-chart"
                  role="img"
                  :aria-label="chartConfig.title"
                >
                  <!-- Horizontal Bars -->
                  <template v-if="svgChartData.mode === 'horizontal'">
                    <g v-for="(r, idx) in svgChartData.rows" :key="r.label">
                      <text x="0" :y="r.y + 18" class="svg-lbl">{{ r.label }}</text>
                      <rect :x="svgChartData.labelW" :y="r.y + 3" :width="svgChartData.plotW" height="22" rx="5" class="svg-track" />
                      <rect
                        :x="svgChartData.labelW"
                        :y="r.y + 3"
                        :width="r.w"
                        height="22"
                        rx="5"
                        class="svg-anim-bar"
                        :class="r.warn ? 'svg-bar-warn' : r.accent ? 'svg-bar-accent' : 'svg-bar-pos'"
                        :style="{ animationDelay: `${idx * 45}ms` }"
                      />
                      <text :x="svgChartData.W - 2" :y="r.y + 18" text-anchor="end" class="svg-val">{{ r.display }}</text>
                    </g>
                  </template>

                  <!-- Diverging Bars -->
                  <template v-else-if="svgChartData.mode === 'diverging'">
                    <line
                      :x1="svgChartData.zeroX"
                      :x2="svgChartData.zeroX"
                      y1="14"
                      :y2="svgChartData.H - 8"
                      class="svg-zero-line"
                    />
                    <template v-if="svgChartData.refX !== null">
                      <line
                        :x1="svgChartData.refX"
                        :x2="svgChartData.refX"
                        y1="18"
                        :y2="svgChartData.H - 8"
                        class="svg-ref-line"
                      />
                      <text :x="svgChartData.refX" y="12" text-anchor="middle" class="svg-ref-lbl">
                        {{ chartConfig.refLine.label }}
                      </text>
                    </template>
                    <g v-for="(r, idx) in svgChartData.rows" :key="r.label">
                      <text x="0" :y="r.y + 18" class="svg-lbl">{{ r.label }}</text>
                      <rect
                        :x="r.x"
                        :y="r.y + 3"
                        :width="r.w"
                        height="22"
                        rx="4.5"
                        class="svg-anim-bar"
                        :class="[{ 'is-neg-bar': r.isNeg }, r.warn ? 'svg-bar-warn' : r.isNeg ? 'svg-bar-neg' : r.accent ? 'svg-bar-accent' : 'svg-bar-pos']"
                        :style="{ animationDelay: `${idx * 45}ms` }"
                      />
                      <text
                        :x="svgChartData.W - 2"
                        :y="r.y + 18"
                        text-anchor="end"
                        :class="['svg-val', r.isNeg ? 'is-neg' : 'is-pos']"
                      >{{ r.display }}</text>
                    </g>
                  </template>

                  <!-- Grouped Comparison Bars -->
                  <template v-else-if="svgChartData.mode === 'grouped'">
                    <g v-for="(r, idx) in svgChartData.rows" :key="r.label">
                      <text x="0" :y="r.y + 21" class="svg-lbl">{{ r.label }}</text>
                      <rect :x="svgChartData.labelW" :y="r.y + 2" :width="r.wA" height="13" rx="3.5" class="svg-bar-old svg-anim-bar" :style="{ animationDelay: `${idx * 55}ms` }" />
                      <text :x="svgChartData.labelW + r.wA + 8" :y="r.y + 13" class="svg-val-sm">{{ r.displayA }}</text>
                      <rect :x="svgChartData.labelW" :y="r.y + 19" :width="r.wB" height="15" rx="3.5" class="svg-bar-accent svg-anim-bar" :style="{ animationDelay: `${idx * 55 + 40}ms` }" />
                      <text :x="svgChartData.labelW + r.wB + 8" :y="r.y + 31" class="svg-val-sm is-pos">{{ r.displayB }}</text>
                    </g>
                  </template>
                </svg>
              </div>

              <!-- Year-over-Year Trajectory Grid (Slides 2–8, hidden when top chart already renders vertical ratio cards) -->
              <div v-if="visibleYoyRatioCards && svgChartData.mode !== 'vertical_cards'" class="glass-card glass-yoy-wrap">
                <div class="glass-sec-label">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" /><polyline points="16 7 22 7 22 13" />
                  </svg>
                  <span>{{ yoySectionTitle }}</span>
                </div>
                <div class="glass-vchart-grid">
                  <div
                    v-for="(card, yIdx) in visibleYoyRatioCards"
                    :key="`${card.title}-${chartBasis}`"
                    class="glass-vchart-card"
                    :class="{ 'is-focused': card.focused }"
                    :style="{ animationDelay: `${yIdx * 55}ms` }"
                  >
                    <div class="glass-vchart-hdr">
                      <strong>{{ card.title }}</strong>
                      <span class="glass-yoy-delta" :class="`tone-${card.tone}`">{{ card.delta }}</span>
                    </div>
                    <div class="glass-vchart-plot">
                      <template v-for="(b, bIdx) in card.bars" :key="b.yr">
                        <div class="glass-vchart-col">
                          <span
                            class="glass-vchart-val"
                            :class="{
                              'is-warn': String(b.val).startsWith('−') || (card.tone === 'warn' && b.current),
                              'is-accent': !String(b.val).startsWith('−') && card.tone !== 'warn' && b.current,
                            }"
                          >{{ b.val }}</span>
                          <div class="glass-vchart-bar-wrap">
                            <span
                              class="glass-vchart-bar"
                              :class="[
                                card.tone === 'warn' || String(b.val).startsWith('−') ? 'is-warn' : '',
                                !String(b.val).startsWith('−') && b.current && card.tone === 'pos' ? 'is-accent' : '',
                                !String(b.val).startsWith('−') && b.current && card.tone === 'accent' ? 'is-amber' : '',
                              ]"
                              :style="{ height: `${Math.max(14, b.pct)}%`, animationDelay: `${yIdx * 55 + bIdx * 50}ms` }"
                            ></span>
                          </div>
                          <span class="glass-vchart-lbl">{{ b.yr }}</span>
                        </div>
                        <div
                          v-if="String(b.yr).startsWith('2023') && bIdx < card.bars.length - 1"
                          class="glass-vchart-divider"
                          :title="isId ? 'Dekonsolidasi Tokopedia (Jan 2024)' : 'Tokopedia Deconsolidation (Jan 2024)'"
                        >
                          <span class="glass-vchart-div-tag">{{ isId ? 'Exit' : 'Exit' }}</span>
                          <span class="glass-vchart-div-line" aria-hidden="true"></span>
                        </div>
                      </template>
                    </div>
                    <p v-if="card.note" class="glass-yoy-note">{{ card.note }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Panel 2 (Right): Executive Takeaway & Deep Analysis (Independent Vertical Scroller + View More) -->
            <div v-if="hasAnalysisTab && showRightPanel" class="glass-pane-scroll glass-pane-right">
              <div class="glass-card glass-explain-card">
                <div class="glass-card-top-row">
                  <div class="glass-sec-label" style="margin-bottom: 0;">
                    <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
                    </svg>
                    <span>{{ isId ? 'Ringkasan & Analisis' : 'Executive Takeaway & Analysis' }}</span>
                  </div>
                  <button
                    type="button"
                    class="glass-toggle-pill"
                    @click="showRightPanel = false"
                    :title="isId ? 'Sembunyikan panel' : 'Hide panel'"
                  >
                    {{ isId ? 'Tutup' : 'Hide' }}
                  </button>
                </div>

                <div class="glass-explain-body">
                  <p v-for="(para, pIdx) in visibleAnalysisParagraphs" :key="'p-' + pIdx" class="glass-explain-p">
                    {{ para }}
                  </p>
                </div>

                <button
                  v-if="hiddenAnalysisCount > 0"
                  type="button"
                  class="glass-view-more-btn"
                  @click="showMoreAnalysis = !showMoreAnalysis"
                >
                  <span>
                    {{
                      showMoreAnalysis
                        ? (isId ? 'Tampilkan lebih sedikit' : 'Show less')
                        : (isId ? `Lihat selengkapnya (+${hiddenAnalysisCount})` : `View more (+${hiddenAnalysisCount})`)
                    }}
                  </span>
                  <svg class="glass-icon" :class="{ 'is-rotated': showMoreAnalysis }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <polyline points="6 9 12 15 18 9" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- TAB 2: Pre vs. Post Exit / Prior vs. Restated Side-by-Side Comparison -->
          <div v-else-if="activeTab === 'compare' && comparisonData" class="glass-tab-panel" key="tab-compare">
            <div class="glass-card">
              <div class="glass-card-hdr">
                <div>
                  <h3>{{ comparisonData.title }}</h3>
                  <p class="glass-chart-sub">{{ comparisonData.subtitle }}</p>
                </div>
              </div>
              <div class="glass-legend-row" style="margin-bottom: 14px;">
                <span class="glass-leg-item"><i class="leg-dot leg-a"></i>{{ comparisonData.leftLabel }}</span>
                <span class="glass-leg-item"><i class="leg-dot leg-b"></i>{{ comparisonData.rightLabel }}</span>
              </div>
              <div class="glass-compare-grid">
                <div
                  v-for="(row, rIdx) in comparisonData.rows"
                  :key="row.metric"
                  class="glass-compare-card"
                  :style="{ animationDelay: `${rIdx * 55}ms` }"
                >
                  <div class="glass-yoy-hdr">
                    <strong>{{ row.metric }}</strong>
                    <span class="glass-yoy-delta" :class="`tone-${row.tone}`">{{ row.delta }}</span>
                  </div>
                  <div class="glass-compare-row">
                    <span class="glass-compare-lbl">{{ isId ? 'Sebelum' : 'Before' }}</span>
                    <div class="glass-yoy-track">
                      <span class="glass-yoy-fill" :style="{ width: `${Math.max(8, row.pctA)}%` }"></span>
                    </div>
                    <span class="glass-compare-val">{{ row.before }}</span>
                  </div>
                  <div class="glass-compare-row">
                    <span class="glass-compare-lbl is-after">{{ isId ? 'Sesudah' : 'After' }}</span>
                    <div class="glass-yoy-track">
                      <span
                        class="glass-yoy-fill is-current"
                        :class="`tone-${row.tone}`"
                        :style="{ width: `${Math.max(8, row.pctB)}%` }"
                      ></span>
                    </div>
                    <span class="glass-compare-val is-after">{{ row.after }}</span>
                  </div>
                  <p class="glass-yoy-note">{{ row.note }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 3: Formula & Slide Calculation Table (Vertical Scroller) -->
          <div v-else-if="activeTab === 'calc'" class="glass-tab-panel" key="tab-calc">
            <div v-if="hasFormulaBlock" class="glass-card glass-formula-card">
              <div class="glass-sec-label">
                <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M18 7V4H6l6 8-6 8h12v-3" />
                </svg>
                <span>{{ isId ? 'Rumus & Langkah Perhitungan' : 'Formula & Step-by-Step Math' }}</span>
              </div>
              <div v-if="item.formula" class="glass-formula-box">
                <div v-if="formulaHtml" class="glass-katex" v-html="formulaHtml"></div>
                <code v-else>{{ item.formula }}</code>
              </div>
              <ul v-if="item.calc_steps?.length" class="glass-steps-list">
                <li v-for="(step, idx) in item.calc_steps" :key="'st-' + idx">{{ step }}</li>
              </ul>
              <div v-if="item.data_origin" class="glass-origin-tag">
                <strong>{{ isId ? 'Sumber:' : 'Origin:' }}</strong> {{ item.data_origin }}
              </div>
            </div>

            <div v-if="calcNotesCount > 0" class="glass-card">
              <div class="glass-sec-label">
                <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M3 9h18" /><path d="M9 21V9" />
                </svg>
                <span>{{ isId ? 'Tabel Perhitungan Slide' : 'Slide Calculation Table' }}</span>
              </div>
              <div class="glass-table-scroll">
                <table class="glass-mini-table">
                  <thead>
                    <tr>
                      <th>{{ isId ? 'Ukuran' : 'Metric' }}</th>
                      <th>{{ isId ? 'Hasil' : 'Result' }}</th>
                      <th>{{ isId ? 'Rumus' : 'Formula' }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(c, cIdx) in visibleCalcNotes"
                      :key="'gc-' + cIdx"
                      class="glass-anim-row"
                      :style="{ animationDelay: `${cIdx * 45}ms` }"
                    >
                      <td>{{ c.label }}</td>
                      <td class="is-hi">{{ c.result }}</td>
                      <td><code>{{ c.formula }}</code></td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <button
                v-if="hiddenCalcCount > 0"
                type="button"
                class="glass-view-more-btn"
                @click="showAllCalcRows = !showAllCalcRows"
              >
                <span>
                  {{
                    showAllCalcRows
                      ? (isId ? 'Tampilkan lebih sedikit' : 'Show less')
                      : (isId ? `Lihat semua baris (+${hiddenCalcCount} lagi)` : `View more (+${hiddenCalcCount} rows)`)
                  }}
                </span>
                <svg class="glass-icon" :class="{ 'is-rotated': showAllCalcRows }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </button>
            </div>
          </div>

          <!-- TAB 3: Audited Statement Proof & Supporting Schedules (Vertical Scroller) -->
          <div v-else-if="activeTab === 'schedules'" class="glass-tab-panel" key="tab-schedules">
            <div v-if="item.evidence_img" class="glass-card glass-evidence-card">
              <div class="glass-sec-label">
                <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" />
                </svg>
                <span>{{ isId ? 'Bukti Laporan Keuangan Auditan' : 'Audited Statement Proof' }}</span>
              </div>
              <button
                type="button"
                class="glass-ev-btn"
                @click="emit('zoom', item.evidence_img, item.title, item.evidence_caption || item.explanation)"
              >
                <img :src="item.evidence_img" :alt="item.evidence_caption || item.title" />
                <span class="glass-ev-zoom-lbl">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /><line x1="11" y1="8" x2="11" y2="14" /><line x1="8" y1="11" x2="14" y2="11" />
                  </svg>
                  <span>{{ isId ? 'Perbesar halaman bukti' : 'Click to enlarge proof page' }}</span>
                </span>
              </button>
              <p v-if="item.evidence_caption" class="glass-ev-cap">{{ item.evidence_caption }}</p>
            </div>

            <div v-if="schedulesCount > 0" class="glass-card">
              <div class="glass-sec-label">
                <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M3 9h18" /><path d="M3 15h18" /><path d="M9 3v18" />
                </svg>
                <span>{{ isId ? 'Jadwal Pendukung' : 'Supporting Schedules' }}</span>
              </div>
              <div v-for="(sched, sIdx) in item.slide.supporting_schedules" :key="'gs-' + sIdx" class="glass-sched-block">
                <div class="glass-card-top-row">
                  <h4>{{ sched.title }}</h4>
                  <button type="button" class="glass-toggle-pill" @click="toggleSchedule(sIdx)">
                    <span>{{ openSchedules[sIdx] ? (isId ? 'Sembunyikan' : 'Hide') : (isId ? 'Lihat jadwal' : 'View more') }}</span>
                    <svg class="glass-icon" :class="{ 'is-rotated': openSchedules[sIdx] }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </button>
                </div>
                <div v-if="openSchedules[sIdx]" class="glass-table-scroll">
                  <table class="glass-mini-table">
                    <thead><tr><th v-for="(h, hIdx) in sched.headers" :key="hIdx">{{ h }}</th></tr></thead>
                    <tbody>
                      <tr
                        v-for="(row, rIdx) in sched.rows"
                        :key="rIdx"
                        class="glass-anim-row"
                        :style="{ animationDelay: `${rIdx * 45}ms` }"
                      >
                        <td v-for="(cell, cIdx) in row" :key="cIdx">{{ cell }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 4: Workbook & Lecture Traces (Progressive Disclosure + Vertical Scroller) -->
          <div v-else-if="activeTab === 'traces'" class="glass-tab-panel" key="tab-traces">
            <div class="glass-card">
              <div class="glass-sec-label">
                <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" /><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
                </svg>
                <span>{{ isId ? 'Jejak Tugas & Materi Kuliah' : 'Workbook & Lecture Traces' }}</span>
              </div>
              <div class="glass-trace-grid">
                <template v-for="(tr, tIdx) in visibleTraces" :key="'gt-' + tIdx">
                  <div v-if="tr.kind === 'assignment'" class="glass-trace-item">
                    <div class="glass-trace-top">
                      <span class="glass-trace-badge">{{ tr.assignment_code }}</span>
                      <button type="button" class="glass-jump-btn" @click="emit('jump-assignment', tr.assignment_id, tr.sheet_name)">
                        {{ isId ? 'Buka' : 'Open' }} &rarr;
                      </button>
                    </div>
                    <code class="glass-trace-ref">{{ tr.cell_or_section_ref }}</code>
                    <p>{{ tr.mapping_note }}</p>
                  </div>
                  <div v-else class="glass-trace-item">
                    <div class="glass-trace-top">
                      <span class="glass-trace-badge is-lec">{{ tr.week_label }} · Slide {{ tr.slide_num }}</span>
                      <button type="button" class="glass-jump-btn" @click="emit('jump-lecture', tr.week_id, tr.slide_num)">
                        {{ isId ? 'Buka' : 'Open' }} &rarr;
                      </button>
                    </div>
                    <p>{{ tr.mapping_note }}</p>
                  </div>
                </template>
              </div>
              <button
                v-if="hiddenTracesCount > 0"
                type="button"
                class="glass-view-more-btn"
                @click="showAllTraces = !showAllTraces"
              >
                <span>
                  {{
                    showAllTraces
                      ? (isId ? 'Tampilkan lebih sedikit' : 'Show less')
                      : (isId ? `Lihat semua jejak (+${hiddenTracesCount} lagi)` : `View more (+${hiddenTracesCount} traces)`)
                  }}
                </span>
                <svg class="glass-icon" :class="{ 'is-rotated': showAllTraces }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.glass-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 10020;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: clamp(14px, 2.5vw, 32px);
}

/* Sibling scrim + .app-layout.is-glass-open filter ensures true frosted blur even when Firefox skips backdrop-filter */
.glass-modal-scrim {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: rgba(3, 12, 8, 0.62);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.glass-modal-panel {
  position: relative;
  z-index: 1;
  width: min(1280px, 96vw);
  height: min(88vh, 840px);
  max-height: 92vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 20px;
  color: #eefaf1;
  background:
    radial-gradient(circle at 12% 0%, rgba(74, 222, 128, 0.09), transparent 44%),
    linear-gradient(145deg, rgba(7, 25, 16, 0.96), rgba(4, 16, 10, 0.97));
  backdrop-filter: blur(24px) saturate(150%);
  -webkit-backdrop-filter: blur(24px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow: 0 28px 72px rgba(0, 0, 0, 0.62), inset 0 1px 0 rgba(255, 255, 255, 0.24);
}

@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass-modal-scrim {
    background: rgba(3, 12, 8, 0.78);
  }
  .glass-modal-panel {
    background: linear-gradient(145deg, rgba(8, 28, 18, 0.98), rgba(5, 19, 12, 0.98));
  }
}

.glass-modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 26px 14px;
  background: rgba(255, 255, 255, 0.04);
  flex-shrink: 0;
}

.glass-tab-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 26px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.09);
  border-bottom: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(0, 0, 0, 0.16);
  overflow-x: auto;
  flex-shrink: 0;
  scrollbar-width: none;
}

.glass-tab-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.glass-icon {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
  transition: transform 0.18s ease;
}

.glass-icon.is-rotated {
  transform: rotate(180deg);
}

.glass-panel-toggle {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 13px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.06);
  color: #d1fae5;
  font: inherit;
  font-size: 12.5px;
  font-weight: 650;
  white-space: nowrap;
  cursor: pointer;
  flex-shrink: 0;
  transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease;
}

.glass-panel-toggle:hover {
  background: rgba(255, 255, 255, 0.14);
  color: #ffffff;
}

.glass-panel-toggle.is-on {
  border-color: rgba(134, 239, 172, 0.42);
  background: rgba(34, 197, 94, 0.14);
}

.glass-tab-bar::-webkit-scrollbar {
  display: none;
}

.glass-tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.05);
  color: #cfe9d7;
  font: inherit;
  font-size: 13px;
  font-weight: 650;
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease, box-shadow 0.16s ease;
}

.glass-tab-btn:hover {
  background: rgba(255, 255, 255, 0.11);
  color: #ffffff;
}

.glass-tab-btn.is-active {
  background: rgba(34, 197, 94, 0.22);
  border-color: rgba(74, 222, 128, 0.58);
  color: #ffffff;
  box-shadow: 0 0 0 1px rgba(74, 222, 128, 0.20), 0 4px 14px rgba(0, 0, 0, 0.22);
}

.glass-tab-count {
  font-size: 11px;
  font-weight: 750;
  color: #86efac;
  background: rgba(34, 197, 94, 0.22);
  padding: 1px 7px;
  border-radius: 999px;
}

.glass-tab-btn.is-active .glass-tab-count {
  color: #062815;
  background: #4ade80;
}

.glass-hdr-left {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.glass-slide-pill {
  display: inline-block;
  width: fit-content;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #86efac;
  background: rgba(34, 197, 94, 0.16);
  border: 1px solid rgba(134, 239, 172, 0.30);
  padding: 3px 9px;
  border-radius: 999px;
}

.glass-modal-header h2 {
  margin: 0;
  font-size: clamp(18px, 2vw, 22px);
  font-weight: 750;
  color: #ffffff;
  line-height: 1.25;
}

.glass-value-pill {
  width: fit-content;
  font-size: 13px;
  font-weight: 700;
  color: #fef3c7;
  background: rgba(251, 191, 36, 0.16);
  border: 1px solid rgba(251, 191, 36, 0.34);
  padding: 3px 10px;
  border-radius: 8px;
}

.glass-hdr-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.glass-close-btn {
  width: 36px;
  height: 36px;
  border-radius: 9px;
  border: 1px solid rgba(255, 255, 255, 0.24);
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.15s ease;
}

.glass-close-btn:hover {
  background: rgba(239, 68, 68, 0.35);
  border-color: rgba(252, 165, 165, 0.5);
}

.glass-modal-body {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  min-height: 0;
  overflow: hidden;
}

.glass-split-view {
  display: grid;
  grid-template-columns: 1.55fr 1fr;
  flex: 1 1 auto;
  min-height: 0;
  height: 100%;
  overflow: hidden;
}

.glass-split-view.is-single {
  grid-template-columns: 1fr;
}

.glass-pane-scroll {
  min-height: 0;
  min-width: 0;
  height: 100%;
  overflow-y: auto;
  padding: 20px 24px 26px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  scrollbar-color: rgba(255, 255, 255, 0.28) transparent;
}

.glass-pane-right {
  border-left: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(0, 0, 0, 0.12);
}

@media (max-width: 920px) {
  .glass-split-view {
    grid-template-columns: 1fr;
    overflow-y: auto;
  }
  .glass-pane-scroll {
    height: auto;
    overflow-y: visible;
  }
  .glass-pane-right {
    border-left: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
  }
}

.glass-tab-panel {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  padding: 20px 26px 26px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-width: 0;
  scrollbar-color: rgba(255, 255, 255, 0.28) transparent;
}

.glass-card-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.glass-explain-body {
  margin-top: 12px;
}

.glass-toggle-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.20);
  background: rgba(255, 255, 255, 0.08);
  color: #d1fae5;
  font: inherit;
  font-size: 12px;
  font-weight: 650;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

.glass-toggle-pill:hover {
  background: rgba(34, 197, 94, 0.24);
  border-color: rgba(134, 239, 172, 0.5);
  color: #ffffff;
}

.glass-view-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 14px;
  align-self: flex-start;
  padding: 8px 15px;
  border-radius: 10px;
  border: 1px solid rgba(134, 239, 172, 0.36);
  background: rgba(34, 197, 94, 0.16);
  color: #bbf7d0;
  font: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.glass-view-more-btn:hover {
  background: rgba(34, 197, 94, 0.30);
  border-color: rgba(134, 239, 172, 0.65);
  color: #ffffff;
}

.glass-ev-zoom-lbl {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.glass-compare-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

@media (max-width: 760px) {
  .glass-compare-grid {
    grid-template-columns: 1fr;
  }
}

.glass-compare-card {
  background: rgba(0, 0, 0, 0.24);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: glassRowUp 0.34s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.glass-compare-row {
  display: grid;
  grid-template-columns: 58px 1fr 112px;
  align-items: center;
  gap: 10px;
  font-size: 12.5px;
}

.glass-compare-lbl {
  color: #a3c4ae;
  font-weight: 600;
}

.glass-compare-lbl.is-after {
  color: #86efac;
  font-weight: 700;
}

.glass-compare-val {
  text-align: right;
  color: #cbd5e1;
  font-variant-numeric: tabular-nums;
  font-weight: 600;
}

.glass-compare-val.is-after {
  color: #ffffff;
  font-weight: 750;
}

.glass-card {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 14px;
  padding: 18px 22px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.10);
}

.glass-card-hdr {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}

.glass-chart-hdr-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.glass-basis-switch {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.28);
  border: 1px solid rgba(255, 255, 255, 0.16);
}

.glass-basis-btn {
  border: 0;
  background: transparent;
  color: #cfe9d7;
  font: inherit;
  font-size: 11.5px;
  font-weight: 700;
  padding: 5px 11px;
  border-radius: 7px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
}

.glass-basis-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.08);
}

.glass-basis-btn.is-active {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.88), rgba(22, 163, 74, 0.88));
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(34, 197, 94, 0.30);
}

.glass-basis-btn.is-prev.is-active {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.85), rgba(217, 119, 6, 0.85));
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(245, 158, 11, 0.28);
}

.glass-chart-card h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 750;
  color: #ffffff;
}

.glass-chart-sub {
  margin: 4px 0 0;
  font-size: 13px;
  color: #b7dfc4;
  line-height: 1.45;
}

.glass-unit-badge {
  font-size: 12px;
  font-weight: 700;
  color: #d1fae5;
  background: rgba(255, 255, 255, 0.10);
  border: 1px solid rgba(255, 255, 255, 0.18);
  padding: 3px 10px;
  border-radius: 7px;
  white-space: nowrap;
}

.glass-legend-row {
  display: flex;
  gap: 20px;
  margin-bottom: 10px;
  font-size: 13px;
  color: #d9f3e0;
}

.glass-leg-item {
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

.leg-dot {
  width: 11px;
  height: 11px;
  border-radius: 3px;
  display: inline-block;
}

.leg-a { background: rgba(148, 163, 184, 0.65); }
.leg-b { background: #34d399; }

.glass-svg-chart {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
}

.glass-vchart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
  margin-top: 6px;
}

@media (max-width: 680px) {
  .glass-vchart-grid {
    grid-template-columns: 1fr;
  }
}

.glass-vchart-card {
  background: rgba(0, 0, 0, 0.24);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
  padding: 14px 16px 13px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: glassRowUp 0.34s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.glass-vchart-hdr {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.glass-vchart-hdr strong {
  font-size: 13px;
  font-weight: 750;
  color: #ffffff;
  line-height: 1.3;
}

.glass-vchart-plot {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
  height: 152px;
  padding-top: 6px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.14);
}

.glass-vchart-col {
  flex: 1;
  min-width: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
}

.glass-vchart-divider {
  flex: 0 0 auto;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 3px;
  padding: 0 2px 18px;
}

.glass-vchart-div-tag {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #fbbf24;
  background: rgba(251, 191, 36, 0.14);
  border: 1px solid rgba(251, 191, 36, 0.34);
  border-radius: 4px;
  padding: 1px 4px;
  line-height: 1.2;
}

.glass-vchart-div-line {
  width: 0;
  flex: 1;
  border-left: 1.5px dashed rgba(251, 191, 36, 0.55);
}

.glass-vchart-val {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #dbece0;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.glass-vchart-val.is-accent {
  color: #86efac;
}

.glass-vchart-val.is-warn {
  color: #fda4af;
}

.glass-vchart-bar-wrap {
  width: 100%;
  max-width: 36px;
  flex: 1;
  display: flex;
  align-items: flex-end;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px 6px 2px 2px;
  overflow: hidden;
}

.glass-vchart-bar {
  display: block;
  width: 100%;
  border-radius: 6px 6px 2px 2px;
  background: linear-gradient(180deg, rgba(148, 163, 184, 0.85), rgba(148, 163, 184, 0.50));
  transform-origin: bottom center;
  animation: glassVBarReveal 0.48s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.glass-vchart-card.is-focused {
  background: rgba(34, 197, 94, 0.12);
  border-color: rgba(74, 222, 128, 0.72);
  box-shadow: 0 0 0 1px rgba(74, 222, 128, 0.28), 0 8px 20px rgba(0, 0, 0, 0.24);
}

.glass-vchart-bar.is-accent {
  background: linear-gradient(180deg, #4ade80, #16a34a);
}

.glass-vchart-bar.is-amber {
  background: linear-gradient(180deg, #fbbf24, #d97706);
}

.glass-vchart-bar.is-warn {
  background: linear-gradient(180deg, #fb7185, #e11d48);
}

.glass-vchart-lbl {
  font-size: 11.5px;
  font-weight: 650;
  color: #b7dfc4;
  padding-bottom: 4px;
  font-variant-numeric: tabular-nums;
}

@keyframes glassVBarReveal {
  from {
    opacity: 0.35;
    transform: scaleY(0);
  }
  to {
    opacity: 1;
    transform: scaleY(1);
  }
}

.svg-lbl {
  fill: #e8f8ed;
  font-size: 13px;
  font-weight: 600;
}

.svg-track {
  fill: rgba(255, 255, 255, 0.08);
}

.svg-bar-pos {
  fill: #22c55e;
}

.svg-bar-accent {
  fill: #4ade80;
}

.svg-bar-neg {
  fill: #f87171;
}

.svg-bar-warn {
  fill: #fb7185;
}

.svg-bar-old {
  fill: rgba(148, 163, 184, 0.58);
}

.svg-zero-line {
  stroke: rgba(255, 255, 255, 0.35);
  stroke-width: 1;
}

.svg-ref-line {
  stroke: #fbbf24;
  stroke-width: 1.4;
  stroke-dasharray: 4 3;
}

.svg-ref-lbl {
  fill: #fde68a;
  font-size: 10px;
  font-weight: 700;
}

.svg-val {
  fill: #ffffff;
  font-size: 13px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.svg-val.is-pos { fill: #86efac; }
.svg-val.is-neg { fill: #fecaca; }

.svg-val-sm {
  fill: #cbd5e1;
  font-size: 12px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.svg-val-sm.is-pos { fill: #86efac; font-weight: 750; }

.glass-sec-label {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  font-weight: 750;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #86efac;
  margin-bottom: 10px;
}

.glass-formula-box {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 10px;
  padding: 10px 12px;
  margin-bottom: 10px;
  overflow-x: auto;
  color: #ffffff;
}

.glass-formula-box code {
  font-size: 12.5px;
  color: #d1fae5;
  white-space: pre-wrap;
  word-break: break-word;
}

.glass-katex :deep(.katex) {
  color: #ffffff;
  font-size: 0.95em;
}

.glass-steps-list {
  margin: 0 0 10px;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 12.5px;
  line-height: 1.5;
  color: #dff5e6;
}

.glass-origin-tag {
  font-size: 11.5px;
  color: #b7dfc4;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  padding-top: 8px;
}

.glass-origin-tag strong {
  color: #ffffff;
}

.glass-explain-p {
  margin: 0;
  font-size: 14.5px;
  line-height: 1.65;
  color: #f0faf3;
}

.glass-explain-p + .glass-explain-p {
  margin-top: 10px;
}

.glass-ev-btn {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  padding: 12px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 10px;
  cursor: zoom-in;
  color: #86efac;
  font: inherit;
  font-size: 13px;
  font-weight: 650;
  text-align: center;
  transition: background-color 0.15s ease;
}

.glass-ev-btn:hover {
  background: rgba(255, 255, 255, 0.16);
}

.glass-ev-btn img {
  width: 100%;
  max-height: 320px;
  object-fit: contain;
  background: #ffffff;
  border-radius: 8px;
}

.glass-ev-cap {
  margin: 8px 0 0;
  font-size: 12.5px;
  color: #b7dfc4;
  line-height: 1.45;
}

.glass-table-scroll {
  overflow-x: auto;
}

.glass-mini-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  line-height: 1.5;
  margin-top: 6px;
}

.glass-mini-table th,
.glass-mini-table td {
  padding: 9px 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.10);
  color: #e4f7ea;
  vertical-align: top;
}

.glass-mini-table th {
  color: #86efac;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.05);
}

.glass-mini-table td.is-hi {
  color: #fde68a;
  font-weight: 700;
}

.glass-mini-table code {
  font-size: 12px;
  color: #b7dfc4;
}

.glass-sched-block + .glass-sched-block {
  margin-top: 18px;
}

.glass-sched-block h4 {
  margin: 10px 0 6px;
  font-size: 14px;
  color: #ffffff;
}

.glass-trace-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding-top: 4px;
}

@media (max-width: 720px) {
  .glass-trace-grid {
    grid-template-columns: 1fr;
  }
}

.glass-trace-item {
  background: rgba(0, 0, 0, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  padding: 10px 12px;
}

.glass-trace-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 5px;
}

.glass-trace-badge {
  font-size: 10.5px;
  font-weight: 700;
  color: #86efac;
  background: rgba(34, 197, 94, 0.18);
  padding: 2px 8px;
  border-radius: 6px;
}

.glass-trace-badge.is-lec {
  color: #bae6fd;
  background: rgba(56, 189, 248, 0.18);
}

.glass-jump-btn {
  border: 1px solid rgba(255, 255, 255, 0.24);
  background: rgba(255, 255, 255, 0.10);
  color: #ffffff;
  font: inherit;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 6px;
  cursor: pointer;
}

.glass-jump-btn:hover {
  background: rgba(34, 197, 94, 0.35);
}

.glass-trace-ref {
  display: inline-block;
  font-size: 11px;
  color: #fde68a;
  margin-bottom: 4px;
}

.glass-trace-item p {
  margin: 0;
  font-size: 12px;
  line-height: 1.45;
  color: #d9f3e0;
}

.glass-fade-enter-active,
.glass-fade-leave-active {
  transition: opacity 0.18s ease;
}

.glass-fade-enter-active .glass-modal-panel,
.glass-fade-leave-active .glass-modal-panel {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.18s ease;
}

.glass-fade-enter-from,
.glass-fade-leave-to {
  opacity: 0;
}

.glass-fade-enter-from .glass-modal-panel,
.glass-fade-leave-to .glass-modal-panel {
  opacity: 0;
  transform: scale(0.96) translateY(8px);
}

/* YoY Ratio Movement Grid + Staggered Glass Animations */
.glass-yoy-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

@media (max-width: 720px) {
  .glass-yoy-grid {
    grid-template-columns: 1fr;
  }
}

.glass-yoy-card {
  background: rgba(0, 0, 0, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.13);
  border-radius: 12px;
  padding: 13px 16px;
  display: flex;
  flex-direction: column;
  gap: 7px;
  animation: glassRowUp 0.34s cubic-bezier(0.22, 1, 0.36, 1) both;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
}

.glass-yoy-card.is-focused {
  background: rgba(34, 197, 94, 0.12);
  border-color: rgba(74, 222, 128, 0.72);
  box-shadow: 0 0 0 1px rgba(74, 222, 128, 0.28), 0 8px 20px rgba(0, 0, 0, 0.24);
}

.glass-yoy-note {
  margin: 4px 0 0;
  font-size: 12px;
  line-height: 1.45;
  color: #b7dfc4;
}

.glass-yoy-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 13.5px;
  margin-bottom: 3px;
}

.glass-yoy-hdr strong {
  color: #ffffff;
  font-weight: 700;
  line-height: 1.25;
}

.glass-yoy-delta {
  font-size: 11.5px;
  font-weight: 750;
  padding: 2px 8px;
  border-radius: 999px;
  white-space: nowrap;
}

.glass-yoy-delta.tone-pos {
  color: #86efac;
  background: rgba(34, 197, 94, 0.20);
}

.glass-yoy-delta.tone-accent {
  color: #fde68a;
  background: rgba(251, 191, 36, 0.18);
}

.glass-yoy-delta.tone-warn {
  color: #fecaca;
  background: rgba(248, 113, 113, 0.20);
}

.glass-yoy-bar-row {
  display: grid;
  grid-template-columns: 52px 1fr 78px;
  align-items: center;
  gap: 10px;
  font-size: 12.5px;
}

.glass-yoy-yr {
  color: #b7dfc4;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.glass-yoy-track {
  height: 9px;
  background: rgba(255, 255, 255, 0.10);
  border-radius: 999px;
  overflow: hidden;
}

.glass-yoy-fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.65);
  transform-origin: left center;
  animation: glassBarReveal 0.48s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.glass-yoy-fill.is-current.tone-pos {
  background: #34d399;
}

.glass-yoy-fill.is-current.tone-accent {
  background: #fbbf24;
}

.glass-yoy-fill.tone-warn {
  background: rgba(248, 113, 113, 0.55);
}

.glass-yoy-fill.is-current.tone-warn {
  background: #fb7185;
}

.glass-yoy-val {
  text-align: right;
  color: #cfe9d7;
  font-variant-numeric: tabular-nums;
  font-weight: 550;
}

.glass-yoy-val.is-current {
  color: #ffffff;
  font-weight: 750;
}

.glass-anim-row {
  animation: glassRowUp 0.32s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.svg-anim-bar {
  transform-box: fill-box;
  transform-origin: left center;
  animation: glassBarReveal 0.46s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.svg-anim-bar.is-neg-bar {
  transform-origin: right center;
}

@keyframes glassRowUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes glassBarReveal {
  from {
    opacity: 0.35;
    transform: scaleX(0);
  }
  to {
    opacity: 1;
    transform: scaleX(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .glass-yoy-card,
  .glass-yoy-fill,
  .glass-anim-row,
  .svg-anim-bar {
    animation: none;
  }
}

/* Slide 9 Interactive Sub-Menu & Source-to-Result Panels */
.glass-tab-btn.is-icon-only {
  padding: 8px 11px;
  min-width: 38px;
  justify-content: center;
}

.glass-tab-btn.is-icon-only .glass-icon {
  width: 17px;
  height: 17px;
}

.glass-sub-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 24px;
  background: rgba(8, 22, 16, 0.72);
  border-bottom: 1px solid rgba(74, 222, 128, 0.16);
}

.glass-sub-pill {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.05);
  color: #cfe9d7;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.18s ease;
  font-variant-numeric: tabular-nums;
}

.glass-sub-pill:hover {
  background: rgba(74, 222, 128, 0.14);
  border-color: rgba(74, 222, 128, 0.45);
  color: #ffffff;
}

.glass-sub-pill.is-active {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.32), rgba(16, 185, 129, 0.24));
  border-color: #4ade80;
  color: #ffffff;
  box-shadow: 0 0 14px rgba(74, 222, 128, 0.22);
}

.glass-s9-split {
  display: grid;
  grid-template-columns: minmax(260px, 0.95fr) minmax(380px, 1.65fr);
  gap: 16px;
  padding: 18px 24px;
  align-items: stretch;
  height: 100%;
  box-sizing: border-box;
}

.glass-s9-left {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 16px;
  border-color: rgba(74, 222, 128, 0.34);
  background: linear-gradient(155deg, rgba(16, 46, 32, 0.78), rgba(9, 22, 16, 0.88));
}

.glass-s9-left-top {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.glass-s9-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #86efac;
}

.glass-s9-big-val {
  font-size: 46px;
  line-height: 1.05;
  font-weight: 850;
  color: #ffffff;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
}

.glass-s9-formula-bar {
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-s9-formula-bar code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 12px;
  color: #e2fbe8;
  font-weight: 600;
  word-break: break-word;
}

.glass-s9-one-liner {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  color: #cfe9d7;
}

.glass-s9-right {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 12px 16px;
}

.glass-s9-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}

.glass-s9-table th {
  text-align: left;
  padding: 8px 10px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #9ed3b4;
  border-bottom: 1px solid rgba(255, 255, 255, 0.18);
}

.glass-s9-table td {
  padding: 9px 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  vertical-align: middle;
}

.glass-s9-table .is-num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.glass-s9-table .is-lbl {
  color: #eef9f2;
  font-weight: 550;
}

.glass-s9-table .is-val {
  color: #4ade80;
  font-weight: 750;
}

.glass-s9-table .is-src {
  color: #a9d5bc;
  font-size: 11.5px;
}

.glass-s9-table tr.is-step-row td {
  background: rgba(255, 255, 255, 0.03);
}

.glass-s9-table tr.is-final-row td {
  background: rgba(34, 197, 94, 0.15);
  border-top: 1px solid rgba(74, 222, 128, 0.45);
  border-bottom: none;
  color: #ffffff;
  font-weight: 750;
}

.glass-s9-table .is-out {
  color: #ffffff;
  font-weight: 800;
}

.glass-s9-nav-btns {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.glass-s9-nav-btn {
  appearance: none;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
  color: #e6f6ec;
  font-size: 12px;
  font-weight: 650;
  padding: 6px 11px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.16s ease;
}

.glass-s9-nav-btn:hover {
  background: rgba(74, 222, 128, 0.18);
  border-color: #4ade80;
  color: #ffffff;
}

.glass-s9-nav-btn.is-next {
  background: rgba(34, 197, 94, 0.22);
  border-color: rgba(74, 222, 128, 0.55);
}

@media (max-width: 820px) {
  .glass-s9-split {
    grid-template-columns: 1fr;
  }
}
</style>
