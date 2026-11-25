<script setup>
import { computed, ref } from 'vue'
import { useReportMode } from './composables/useReportMode'
import { getInlineAbbrHint } from './composables/useAbbrGlossary'

const { reportViewMode } = useReportMode()

const props = defineProps({
  slide: { type: Object, required: true },
  lang: { type: String, default: 'en' },
  total: { type: Number, default: 12 },
  backSlideNum: { type: Number, default: 12 },
})
const emit = defineEmits(['explain', 'evidence', 'zoom', 'jump-slide'])

const appendixMap = {
  2: { code: 'A1', slideNum: 15 },
  3: { code: 'A1', slideNum: 15 },
  4: { code: 'A2', slideNum: 16 },
  5: { code: 'A3', slideNum: 17 },
  6: { code: 'A3', slideNum: 17 },
  7: { code: 'A4', slideNum: 18 },
  8: { code: 'A5', slideNum: 19 },
  9: { code: 'A6', slideNum: 20 },
  10: { code: 'A6', slideNum: 20 },
  11: { code: 'A6', slideNum: 20 },
  12: { code: 'A6', slideNum: 20 },
  13: { code: 'A6', slideNum: 20 },
  14: { code: 'A6', slideNum: 20 },
}
const appendixTarget = computed(() => (!props.slide.is_appendix ? appendixMap[props.slide.slide_num] || null : null))
const appendixList = [
  { code: 'A1', slideNum: 15 },
  { code: 'A2', slideNum: 16 },
  { code: 'A3', slideNum: 17 },
  { code: 'A4', slideNum: 18 },
  { code: 'A5', slideNum: 19 },
  { code: 'A6', slideNum: 20 },
]
const restatableSlides = new Set([4, 5, 6, 7, 8, 10, 11, 12])
const hasRestatement = computed(() => !props.slide.is_appendix && restatableSlides.has(props.slide.slide_num))
const isRestated = computed(() => hasRestatement.value && reportViewMode.value === 'restated')
const restatementSummary = computed(() => {
  const id = props.lang === 'id'
  const sn = props.slide.slide_num
  const map = {
    4: id
      ? 'Restatement: Aset 2024 +Rp1.582M (Catatan 7); AT 0,3679x, EM 1,421x; EBIT Gojek +Rp888,6M'
      : 'Restatement: 2024 Assets +Rp1,582B (Note 7); AT 0.3679x, EM 1.421x; Gojek EBIT +Rp888.6B',
    5: id
      ? 'Restatement: CR 2024 2,46x→2,62x; DSO 46,9h→10,56h (Cat. 6); utang+sewa penuh (TIE −4,54x→−0,71x)'
      : 'Restatement: 2024 CR 2.46x→2.62x; DSO 46.9d→10.56d (Note 6); full debt+leases (TIE −4.54x→−0.71x)',
    6: id
      ? 'Restatement: CapEx lanjutan 2024 turun 41,0%→6,63% (Rp1.054M) setelah keluarkan transfer Tokopedia'
      : 'Restatement: 2024 continuing CapEx drops 41.0%→6.63% (Rp1,054B) ex-Tokopedia intangibles',
    7: id
      ? 'Restatement: Keluarkan 2023 (OpEx 117%); Base murni 2024–2025 (OpEx 55,70%, CapEx 6,45%)'
      : 'Restatement: 2023 excluded (117% OpEx); Base anchored on 2024–2025 (55.70% OpEx, 6.45% CapEx)',
    8: id
      ? 'Restatement: EBIT 2028F −Rp4.967M→+Rp567,2M; Laba Bersih +Rp25,0M; Kas Akhir Rp19,42T'
      : 'Restatement: 2028F EBIT −Rp4,967B→+Rp567.2B; Net Income +Rp25.0B; Ending Cash Rp19.42T',
    10: id
      ? 'Restatement: Basis pasca-Tokopedia angkat DCF Dasar −Rp121,1→+Rp10,38 & RI −Rp75,1→−Rp12,23'
      : 'Restatement: Clean post-Tokopedia FCF lifts Base DCF −Rp121.1→+Rp10.38 & RI −Rp75.1→−Rp12.23',
    11: id
      ? 'Restatement: Rentang Nilai Wajar Rp10,38–Rp16,75/sh vs harga pasar Rp25,00 (P/B Grab Rp91,02 ditolak)'
      : 'Restatement: Defensible Range Rp10.38–Rp16.75/sh vs Rp25.00 market (Grab P/B Rp91.02 rejected)',
    12: id
      ? 'Restatement: SELL / AVOID tetap berlaku — ROIC 2028F (+2,70%) tertinggal 506 bps di bawah WACC (7,76%)'
      : 'Restatement: SELL / AVOID holds — 2028F ROIC (+2.70%) trails WACC (7.76%) by 506 bps',
  }
  return map[sn] || ''
})
const titles = {
  en: [
    'GoTo equity analysis',
    'Two operating businesses after the Tokopedia exit',
    'Competition limits pricing power',
    'Margins improved. Returns remain below the hurdle.',
    'Operating cash flow still falls short of capex',
    'The base case consumes the cash buffer',
    'A 7.76% cost of capital',
    'Both intrinsic models produce negative values',
    'Grab is our sole operating comparable',
    'Cash burn explains the valuation gap',
    'SELL / AVOID at Rp 25.00',
    'Historical results and base-case projections',
    'Sensitivity and operating breakeven',
  ],
  id: [
    'Analisis ekuitas GoTo',
    'Dua bisnis utama setelah pelepasan Tokopedia',
    'Persaingan membatasi kekuatan harga',
    'Margin membaik. Imbal hasil masih di bawah target.',
    'Arus kas operasi belum menutup belanja modal',
    'Skenario dasar menguras cadangan kas',
    'Biaya modal sebesar 7,76%',
    'Kedua model intrinsik menghasilkan nilai negatif',
    'Grab menjadi satu-satunya pembanding operasional',
    'Pembakaran kas menjelaskan perbedaan valuasi',
    'JUAL / HINDARI pada Rp 25,00',
    'Hasil historis dan proyeksi skenario dasar',
    'Sensitivitas dan titik impas operasional',
  ],
}
const takeaways = {
  en: [
    'Low switching costs constrain pricing. Cash flow has yet to fund investment.',
    'Gojek generates most revenue. Financial technology supplies the fastest growth.',
    'Price-sensitive users sustain promotion costs while lending adds credit risk.',
    'ROE of −5.2% remains below the 8.45% cost of equity.',
    'Positive operating cash flow leaves a Rp 875 bn shortfall after capex.',
    '2028F ending cash falls to Rp 968 bn under historical cost assumptions.',
    'Equity carries 77.4% of the capital weight. Debt carries 22.6%.',
    'Both models use the same operating forecast and 3.0% terminal growth.',
    'The Grab P/B benchmark assumes comparable earning power and remains conditional.',
    'Intrinsic models reflect future losses. Market multiples reflect asset value.',
    'An upgrade requires sustained profit, capex coverage, and disciplined operating costs.',
  ],
  id: [
    'Biaya perpindahan yang rendah membatasi harga. Arus kas belum mendanai investasi.',
    'Gojek menyumbang pendapatan terbesar. Teknologi finansial tumbuh paling cepat.',
    'Pengguna sensitif terhadap harga. Pinjaman menambah eksposur risiko kredit.',
    'ROE −5,2% masih di bawah biaya ekuitas sebesar 8,45%.',
    'Arus kas operasi positif masih menyisakan kekurangan Rp 875 miliar setelah capex.',
    'Saldo kas akhir 2028F turun menjadi Rp 968 miliar dengan asumsi biaya historis.',
    'Bobot ekuitas sebesar 77,4% dan utang sebesar 22,6%.',
    'Kedua model memakai proyeksi operasi yang sama dan pertumbuhan terminal 3,0%.',
    'Pembanding P/B Grab mengasumsikan daya laba sebanding dan tetap bersyarat.',
    'Model intrinsik mencerminkan kerugian mendatang. Kelipatan pasar menilai aset.',
    'Peningkatan rekomendasi membutuhkan laba berkelanjutan, cakupan capex, dan disiplin biaya.',
  ],
}
const layoutSlide = computed(() => props.slide.layout_slide || props.slide.slide_num)
const title = computed(() => props.slide.display_title || titles[props.lang]?.[layoutSlide.value - 1] || props.slide.title)
const takeaway = computed(() => props.slide.display_takeaway || props.slide.analysis_points?.[1]?.text || takeaways[props.lang]?.[layoutSlide.value - 1] || '')
const table = computed(() => props.slide.table)
const forecastScenario = ref('base')
const valuationBasis = ref('3yr') // '3yr' | '2yr'
const tableAnimKey = computed(() => `${props.slide.slide_num}-${reportViewMode.value}-${forecastScenario.value}-${valuationBasis.value}`)
const isForecastSlide = computed(() => !props.slide.is_appendix && props.slide.slide_num === 8)
const isDcfRiSlide = computed(() => !props.slide.is_appendix && props.slide.slide_num === 10)
const isGrabSlide = computed(() => !props.slide.is_appendix && props.slide.slide_num === 11)
const isValuationSlide = computed(() => isDcfRiSlide.value || isGrabSlide.value)
const visibleValuationRange = computed(() => {
  const baseRange = props.slide.valuation_range || []
  if (isRestated.value && isGrabSlide.value) {
    return [
      { label: 'DCF', value: 10.38 },
      { label: 'RI', value: -12.23 },
      { label: 'Grab P/B', value: 91.02 },
    ]
  }
  if (!isValuationSlide.value || valuationBasis.value !== '2yr') return baseRange
  return baseRange.map((row) => {
    if (row.label === 'DCF') return { ...row, value: -72.5 }
    if (row.label === 'RI') return { ...row, value: -31.3 }
    return row
  })
})
const restatedForecastData = computed(() => {
  const id = props.lang === 'id'
  return {
    base: {
      headers: [id ? 'Pos Utama (Rp miliar)' : 'Key Line Item (Rp bn)', '2025A', '2026F Base', '2027F Base', '2028F Base'],
      rows: [
        [id ? 'Pendapatan Bersih (+15,27%)' : 'Net Revenue (+15.27%)', '18,322.1', '21,120.6', '24,346.4', '28,065.0'],
        [id ? 'Laba Operasi (EBIT)' : 'Operating Profit (EBIT)', '(378.3)', '+426.9', '+492.1', '+567.2'],
        [id ? 'Laba / (Rugi) Bersih' : 'Consolidated Net Income', '(1,501.7)', '(84.5)', '(33.6)', '+25.0'],
        [id ? 'Kas Akhir Tahun' : 'Ending Cash Balance', '21,755.2', '20,686.7', '19,955.4', '19,421.1'],
      ],
    },
    optimistic: {
      headers: [id ? 'Pos Utama (Rp miliar)' : 'Key Line Item (Rp bn)', '2025A', '2026F Opt', '2027F Opt', '2028F Opt'],
      rows: [
        [id ? 'Pendapatan Bersih (+18,00%)' : 'Net Revenue (+18.00%)', '18,322.1', '21,620.1', '25,511.7', '30,103.8'],
        [id ? 'Laba Operasi (EBIT)' : 'Operating Profit (EBIT)', '(378.3)', '+2,313.4', '+2,729.8', '+3,221.1'],
        [id ? 'Laba Bersih Konsolidasian' : 'Consolidated Net Income', '(1,501.7)', '+1,387.1', '+1,711.8', '+2,095.0'],
        [id ? 'Kas Akhir Tahun' : 'Ending Cash Balance', '21,755.2', '22,570.6', '23,604.2', '24,795.0'],
      ],
    },
    conservative: {
      headers: [id ? 'Pos Utama (Rp miliar)' : 'Key Line Item (Rp bn)', '2025A', '2026F Cons', '2027F Cons', '2028F Cons'],
      rows: [
        [id ? 'Pendapatan Bersih (+7,50%)' : 'Net Revenue (+7.50%)', '18,322.1', '19,696.3', '21,173.5', '22,761.8'],
        [id ? 'Rugi Operasi (EBIT)' : 'Operating Loss (EBIT)', '(378.3)', '(1,854.7)', '(1,993.8)', '(2,143.4)'],
        [id ? 'Rugi Bersih Konsolidasian' : 'Consolidated Net Loss', '(1,501.7)', '(2,071.5)', '(2,177.2)', '(2,291.0)'],
        [id ? 'Kas Akhir Tahun' : 'Ending Cash Balance', '21,755.2', '18,754.2', '16,133.1', '13,516.5'],
      ],
    },
  }
})
const restatedSlideTables = computed(() => {
  const id = props.lang === 'id'
  const scenKey = forecastScenario.value === 'base_2yr' ? 'base' : forecastScenario.value
  return {
    4: {
      headers: id
        ? ['Rasio / DuPont (Appendix A2)', '2023*', '2024', '2025', 'YoY 24→25']
        : ['Ratio / DuPont (Appendix A2)', '2023*', '2024', '2025', 'YoY 24→25'],
      rows: [
        [id ? 'Margin Operasi (EBIT %)' : 'Operating Margin (EBIT %)', '−69.5%', '−14.10%', '−2.06%', '+12.04%'],
        [id ? 'Margin Laba Bersih' : 'Net Profit Margin', '−612.2%', '−34.38%', '−8.20%', '+26.18%'],
        [id ? 'Perputaran Aset (ATO)' : 'Asset Turnover (Rev / Assets)', '0.27x', '0.37x', '0.40x', '+8.8%'],
        [id ? 'Multiplier Ekuitas (EM)' : 'Equity Multiplier (Assets / Eq)', '1.51x', '1.42x', '1.59x', '+0.17x'],
        ['ROA (Cons.)', '−167.3%', '−12.65%', '−3.28%', '+9.37%'],
        [id ? 'ROE (Kons. / Induk)' : 'ROE (Cons. / Parent)', '−253.4%', '−17.97%', '−5.23% / −3.73%', '+12.74%'],
      ],
    },
    7: {
      headers: id
        ? ['Asumsi Utama', 'Optimistis (1H26)', 'Base (Pasca-Exit)', 'Konservatif (2024)']
        : ['Assumption', 'Optimistic (1H26)', 'Base (Post-Exit)', 'Conservative (2024)'],
      rows: [
        [id ? 'Pertumbuhan pendapatan' : 'Revenue growth', '18.00%', '15.27%', '7.50%'],
        [id ? 'Beban pokok / pendapatan' : 'COGS / revenue', '38.10%', '42.28%', '46.64%'],
        [id ? 'Beban operasi tunai / pend.' : 'Cash OpEx / revenue', '51.20%', '55.70%', '62.78%'],
        [id ? 'CapEx / pendapatan' : 'CapEx / revenue', '6.45%', '6.45%', '6.63%'],
        [id ? 'Suku bunga utang (pra-pajak)' : 'Borrowing rate (pre-tax)', '6.91%', '6.91%', '10.25%'],
      ],
    },
    8: restatedForecastData.value[scenKey] || restatedForecastData.value.base,
    10: {
      headers: id ? ['Tahap Model', 'DCF', 'Residual Income'] : ['Model Step', 'DCF', 'Residual Income'],
      rows: [
        [id ? 'Tingkat diskonto' : 'Discount rate', 'WACC: 7.76%', 'Ke: 8.45%'],
        [id ? 'Pertumbuhan terminal (g_fund +3,41%)' : 'Terminal growth (g_fund +3.41%)', '3.00% (TV 67.6% EV)', '3.00% (TV 85.0% PV)'],
        [id ? 'Jembatan nilai ekuitas' : 'Equity bridge', 'EV −2,988.5B + NetCash 14,012.5B', 'BVE 28,711.7B − PV(RI) 41,698.6B'],
        [id ? 'Hasil per saham' : 'Model output / share', '+Rp10.38', '−Rp12.23 (+Rp0.24 g=0%)'],
      ],
    },
    11: {
      headers: id ? ['Input / Hasil Valuasi', 'Nilai Laporan Akhir'] : ['Input / Result', 'Final Report Value'],
      rows: [
        ['Grab P/B (31 Dec 2025)', '3.0391x'],
        [id ? 'BVPS Induk GoTo' : 'GoTo parent BVPS', 'Rp29.95 / share'],
        [id ? 'Pembanding P/B bersyarat' : 'Conditional P/B benchmark', id ? 'Rp91.02 / sh (Ditolak)' : 'Rp91.02 / sh (Rejected)'],
        [id ? 'Rentang Nilai Intrinsik Wajar' : 'Defensible Intrinsic Range', 'Rp10.38 – Rp16.75 / sh'],
      ],
    },
  }
})
const restatedRowDetail = (row) => {
  const id = props.lang === 'id'
  return {
    heading: row[0],
    text: `${row.slice(1).join('  |  ')} — ${restatementSummary.value}`,
    detail_explanation: id
      ? `Nilai restated dari Laporan Akhir Final (Group4_FinalReport_GOTO.docx): ${row[0]} = ${row.slice(1).join(' | ')}. ${restatementSummary.value}`
      : `Restated value from the Final Report (Group4_FinalReport_GOTO.docx): ${row[0]} = ${row.slice(1).join(' | ')}. ${restatementSummary.value}`,
    formula: restatementSummary.value,
    calc_steps: row.map((c, idx) => `${visibleHeaders.value[idx] || 'Col ' + (idx + 1)}: ${c}`),
    data_origin: 'Group4_FinalReport_GOTO.docx (Restated Post-Tokopedia Model) & LK GOTO FY2025',
    evidence_img: null,
  }
}
const forecastScenarioData = computed(() => {
  const id = props.lang === 'id'
  return {
    base_2yr: {
      headers: [id ? 'Pos Utama (Rp miliar)' : 'Key Line Item (Rp bn)', '2025A', '2026F (2-Yr)', '2027F (2-Yr)', '2028F (2-Yr)'],
      rows: [
        ['Revenue', '18,322', '20,408', '22,732', '25,321'],
        [id ? 'Rugi operasi (Rata-rata 2 Thn)' : '2-Yr Avg operating loss', '(378)', '(754.6)', '(840.5)', '(936.2)'],
        [id ? 'Rugi bersih (Rata-rata 2 Thn)' : '2-Yr Avg net loss', '(1,502)', '(1,202.9)', '(1,269.9)', '(1,344.6)'],
        [id ? 'Kas akhir (Rata-rata 2 Thn)' : '2-Yr Avg ending cash', '21,755', '15,300', '9,966', '5,071'],
      ],
    },
    optimistic: {
      headers: [id ? 'Pos Utama (Rp miliar)' : 'Key Line Item (Rp bn)', '2025A', '2026F Opt', '2027F Opt', '2028F Opt'],
      rows: [
        ['Revenue', '18,322', '21,125', '24,358', '28,084'],
        [id ? 'Optimistic operating profit' : 'Optimistic operating profit', '(378)', '+1,309.8', '+1,510.2', '+1,741.2'],
        [id ? 'Optimistic net income' : 'Optimistic net income', '(1,502)', '+604.9', '+761.2', '+941.4'],
        [id ? 'Optimistic ending cash' : 'Optimistic ending cash', '21,755', '21,457', '21,249', '21,284'],
      ],
    },
    conservative: {
      headers: [id ? 'Pos Utama (Rp miliar)' : 'Key Line Item (Rp bn)', '2025A', '2026F Cons', '2027F Cons', '2028F Cons'],
      rows: [
        ['Revenue', '18,322', '19,696', '21,174', '22,762'],
        [id ? 'Conservative operating loss' : 'Conservative operating loss', '(378)', '(6,224.0)', '(6,690.8)', '(7,192.6)'],
        [id ? 'Conservative net loss' : 'Conservative net loss', '(1,502)', '(5,633.8)', '(5,997.9)', '(6,389.3)'],
        [id ? 'Conservative ending cash' : 'Conservative ending cash', '21,755', '11,428', '3,053', '(5,000)'],
      ],
    },
  }
})
// Detailed source columns remain in the study notes, outside the projected slide.
const visibleHeaders = computed(() => {
  if (isRestated.value && restatedSlideTables.value[props.slide.slide_num]) {
    return restatedSlideTables.value[props.slide.slide_num].headers
  }
  if (isForecastSlide.value && forecastScenario.value !== 'base') {
    return forecastScenarioData.value[forecastScenario.value]?.headers || table.value?.headers || []
  }
  return table.value?.headers || []
})
const datedWaccSources = [
  'SUN: 30 Dec 2025. Default spread: Damodaran, 1 Jan 2026.',
  'Beta: Investing.com, Dec 2025. ERP: Damodaran, 1 Jan 2026.',
  'Damodaran country-risk data, 1 Jan 2026.',
  'CAPM using the dated inputs above.',
  'FY2025 interest / year-end debt. Statutory tax assumption: 22%.',
  'Rp 25 case reference × shares. Debt: FY2025. Weights: 77.4% / 22.6%.',
]
const visibleRows = computed(() => {
  if (isRestated.value && restatedSlideTables.value[props.slide.slide_num]) {
    return restatedSlideTables.value[props.slide.slide_num].rows
  }
  if (isForecastSlide.value && forecastScenario.value !== 'base') {
    return forecastScenarioData.value[forecastScenario.value]?.rows || table.value?.rows || []
  }
  if (isDcfRiSlide.value && valuationBasis.value === '2yr') {
    const baseRows = table.value?.rows || []
    return baseRows.map((row, idx) => (idx === baseRows.length - 1 ? [row[0], '−Rp72.5', '−Rp31.3'] : row))
  }
  return props.slide.story_rebuilt ? table.value?.rows || [] : (table.value?.rows || []).map((row, i) => layoutSlide.value === 7 ? [row[0], row[1], datedWaccSources[i]] : row)
})
const restatedPointsMap = computed(() => {
  const id = props.lang === 'id'
  const scenKey = forecastScenario.value === 'base_2yr' ? 'base' : forecastScenario.value
  const s8ByScenario = {
    base: [
      {
        heading: id ? 'Laba Operasi Positif (2026F–2028F)' : 'Operating Profit Turns Positive',
        text: id
          ? 'Tanpa angka 2023, pendapatan tumbuh ke Rp28,07T di 2028F. Laba operasi (EBIT) jadi positif (+Rp426,9M ke +Rp567,2M), dan laba bersih mencapai +Rp25,0M.'
          : 'Without 2023 noise, revenue reaches Rp28.07T by 2028F. Operating profit turns positive (+Rp426.9B to +Rp567.2B), and net income reaches +Rp25.0B.',
        formula: '2026F EBIT = Rp21,120.6bn × (57.72% GM − 55.70% Cash OpEx) = +Rp426.9bn',
        data_origin: 'Final Report §4.2 (Table 12)',
      },
      {
        heading: id ? 'Titik Impas Sangat Tipis' : 'Very Thin Profit Cushion',
        text: id
          ? 'GoTo butuh pendapatan Rp20,38T untuk impas di 2026F, jadi bantalan aman hanya 3,5%. Karena itu, perubahan kecil di penjualan menggeser laba 28,6x (DOL).'
          : 'GoTo needs Rp20.38T in sales just to break even in 2026F, leaving only a 3.5% safety cushion. A small dip in sales swings profit by 28.6x (DOL).',
        formula: 'Breakeven = Rp11,764.6bn / 57.723% = Rp20,381.1bn (+3.50% Margin of Safety)',
        data_origin: 'Final Report §4.3',
      },
      {
        heading: id ? 'Hasil Modal Masih Kalah dari Biaya Modal' : 'Returns Still Below Cost of Capital',
        text: id
          ? 'Kas tetap aman di Rp19,42T pada 2028F. Namun hasil modal (ROIC +2,70%) masih jauh di bawah biaya modal GoTo (WACC 7,76%).'
          : 'Cash stays strong at Rp19.42T by 2028F. Still, GoTo only earns +2.70% on its capital (ROIC), well below its 7.76% cost of capital (WACC).',
        formula: '2028F ROIC = NOPAT Rp442.42bn / Beginning IC Rp16,380.8bn = +2.70% vs 7.76% WACC',
        data_origin: 'Final Report §5.1 (Tables 14–15)',
      },
    ],
    optimistic: [
      {
        heading: id ? 'Skenario Optimistis (Biaya 1H 2026)' : 'Optimistic Case (1H 2026 Costs)',
        text: id
          ? 'Jika efisiensi biaya 1H 2026 bertahan (COGS 38,1%, OpEx 51,2%) dengan pertumbuhan 18%, laba operasi 2028F naik hampir 6x menjadi +Rp3,22T.'
          : 'If GoTo keeps its lower 1H 2026 costs (38.1% COGS, 51.2% OpEx) and grows 18% a year, 2028F operating profit jumps to +Rp3.22T.',
        formula: '2028F Opt EBIT = Rp30,103.8bn × (61.90% GM − 51.20% OpEx) = +Rp3,221.1bn',
        data_origin: 'Final Report §4.1 & Table 13',
      },
      {
        heading: id ? 'Laba & Arus Kas Jadi Kuat' : 'Strong Profit & Positive Cash Flow',
        text: id
          ? 'Laba bersih naik ke +Rp2,10T, arus kas bebas (FCFF) positif +Rp1,89T, dan kas akhir bertambah menjadi Rp24,80T di 2028F.'
          : 'Net income reaches +Rp2.10T, free cash flow turns positive (+Rp1.89T), and cash grows to Rp24.80T by 2028F.',
        formula: '2028F Opt NI = +Rp2,095.0bn | 2028F Opt FCFF = +Rp1,887.0bn',
        data_origin: 'Final Report Table 13',
      },
      {
        heading: id ? 'Batas Atas Nilai Saham' : 'Upside Fair Value',
        text: id
          ? 'Jika efisiensi 1H 2026 benar-benar bertahan penuh setahun, nilai saham naik ke Rp16,75 (RI) hingga Rp47,34 per saham (DCF).'
          : 'Only if GoTo sustains 1H 2026 cost cuts all year does fair value rise to Rp16.75 (RI) or Rp47.34 per share (DCF).',
        formula: 'Optimistic RI = Rp16.75/sh | Optimistic DCF = Rp47.34/sh',
        data_origin: 'Final Report Table 17',
      },
    ],
    conservative: [
      {
        heading: id ? 'Skenario Konservatif (Pola 2024)' : 'Conservative Case (2024 Costs)',
        text: id
          ? 'Jika biaya naik lagi ke level 2024 (COGS 46,6%, OpEx 62,8%, bunga 10,3%), GoTo kembali rugi operasi −Rp2,14T di 2028F.'
          : 'If costs slip back to 2024 levels (46.6% COGS, 62.8% OpEx, 10.3% interest), GoTo returns to a −Rp2.14T operating loss in 2028F.',
        formula: '2028F Cons EBIT = Rp22,761.8bn × (53.36% GM − 62.78% OpEx) = −Rp2,143.4bn',
        data_origin: 'Final Report Table 11 & Table 13',
      },
      {
        heading: id ? 'Kas Berkurang, Tapi Tidak Habis' : 'Cash Drops, But No Bankruptcy',
        text: id
          ? 'Kas turun karena rugi, tapi masih tersisa Rp13,52T di 2028F. Jadi GoTo tidak langsung kehabisan kas seperti perkiraan lama.'
          : 'Losses drain cash, but GoTo still ends 2028F with Rp13.52T in the bank, so it does not run out of cash like our old model showed.',
        formula: '2028F Cons Ending Cash = Rp13,516.5bn (vs −Rp5,000bn old deck)',
        data_origin: 'Final Report Table 13 & Appendix B',
      },
      {
        heading: id ? 'Risiko Penurunan Nilai Saham' : 'Downside Value Risk',
        text: id
          ? 'Jika perang promo kembali seperti 2024, nilai saham turun jauh menjadi negatif (−Rp33,95 DCF dan −Rp44,42 RI).'
          : 'If promo spending returns to 2024 levels, fair value drops sharply into negative territory (−Rp33.95 DCF and −Rp44.42 RI).',
        formula: 'Conservative DCF = −Rp33.95/sh | Conservative RI = −Rp44.42/sh',
        data_origin: 'Final Report Table 17',
      },
    ],
  }
  return {
    4: [
      {
        heading: id ? 'Laba Gojek Melonjak di 2025' : 'Gojek Profit Jumped 13x in 2025',
        text: id
          ? 'Angka 2023 masih tercampur Tokopedia. Di 2025, laba Gojek melonjak ke +Rp888,6M berkat pangkas promo, hemat biaya cloud, dan keluar dari Vietnam.'
          : '2023 still included Tokopedia. In 2025, Gojek operating profit jumped to +Rp888.6B thanks to lower promos, cloud savings, and exiting Vietnam.',
        formula: 'Gojek 2025 EBIT: +Rp69.4bn → +Rp888.6bn (+1,180% YoY)',
        data_origin: 'Final Report §1.1 & Note 29 pp. 133–134',
      },
      {
        heading: id ? 'Perbaikan Data Aset 2024' : 'Fixed 2024 Assets (+Rp1.58T)',
        text: id
          ? 'Kami menambahkan kembali Rp1,58T piutang pinjaman 2024 yang terlewat, memulihkan Total Aset 2024 dari Rp41,63T menjadi Rp43,21T (ROE 2024 tetap −17,97%).'
          : 'We added back Rp1.58T of 2024 consumer loans that were missed earlier, restoring 2024 Total Assets from Rp41.63T to the audited Rp43.21T (2024 ROE unchanged at −17.97%).',
        formula: '2024 Assets = Rp43,207,884m (Check = 0); 2024 ROE = −17.97%',
        data_origin: 'Final Report Appendix B & §3.1',
      },
      {
        heading: id ? 'ROE GoTo Masih Kalah dari Grab' : 'GoTo ROE Still Trails Grab',
        text: id
          ? 'GoTo memakai aset lebih efisien dari Grab (0,40x vs 0,28x), tapi margin GoTo masih minus (−8,20%) sehingga ROE tetap negatif (−5,23% vs Grab +2,96%).'
          : 'GoTo uses its assets more efficiently than Grab (0.40x vs 0.28x), but negative profit margins (−8.20%) keep GoTo ROE negative (−5.23% vs Grab +2.96%).',
        formula: 'Cons. ROE = −8.20% × 0.4004x × 1.5937x = −5.23%',
        data_origin: 'Final Report §3.3 (Table 9)',
      },
    ],
    5: [
      {
        heading: id ? 'Kas Kuat & Tagihan Lancar' : 'Strong Liquidity & Fast Collections',
        text: id
          ? 'Current Ratio tetap sehat di 2,73x (2025). Setelah memisahkan piutang usaha Catatan 6, waktu tagih (DSO) sangat cepat di 10,9 hari.'
          : 'Short-term liquidity is strong (2.73x Current Ratio in 2025). Using Note 6 trade receivables shows fast collections at 10.9 days (DSO).',
        formula: '2024 Current Ratio = 2.62x | DSO = 10.56d (2024) → 10.90d (2025)',
        data_origin: 'Final Report Appendix B & §3.2',
      },
      {
        heading: id ? 'Utang Naik & Bunga Belum Tertutup' : 'Higher Debt & Negative Interest Coverage',
        text: id
          ? 'Total utang dan sewa naik dari Rp4,82T ke Rp7,74T di 2025 (D/E 27,0%). Karena EBIT masih minus, laba operasi belum cukup menutup bunga (TIE −0,71x).'
          : 'Total debt and leases rose from Rp4.82T to Rp7.74T in 2025 (27.0% D/E). Because EBIT is still negative, operations do not yet cover interest (−0.71x TIE).',
        formula: '2024 D/E = 15.85%; 2025 D/E = 26.97%; TIE = −0.71x',
        data_origin: 'Final Report Table 8',
      },
      {
        heading: id ? 'Z-Score Rendah Karena Rugi Lama' : 'Low Z-Score Driven by Past Losses',
        text: id
          ? 'Z-Score memang negatif (−4,72 buku / −4,80 pasar), tapi itu karena akumulasi rugi lama dari 2023. Kas GoTo masih kuat sehingga tidak ada risiko gagal bayar jangka pendek.'
          : 'The Z-Score is negative (−4.72 book / −4.80 market), mostly due to past 2023 losses. Strong cash reserves mean there is no immediate default risk.',
        formula: 'Z (Book) = −4.72 | Z (Market Rp25.00) = −4.80 (< 1.81 cutoff)',
        data_origin: 'Final Report §3.4 (Table 10)',
      },
    ],
    6: [
      {
        heading: id ? 'Risiko 1: Nilai Investasi Tokopedia & Jago' : 'Risk 1: Heavy Tokopedia & Bank Jago Stakes',
        text: id
          ? 'Saham Tokopedia (Rp7,43T) dan Bank Jago (Rp2,89T) mencapai 22,6% total aset. Jika nilai Tokopedia & aset privat turun 20%, ekuitas GoTo terpotong 6,3%.'
          : 'Tokopedia (Rp7.43T) and Bank Jago (Rp2.89T) make up 22.6% of total assets. A 20% write-down on Tokopedia and private stakes cuts equity by 6.3%.',
        formula: '20% Stress on Rp9,100.9bn (Tokopedia + L3) = −Rp1,820.2bn (−6.34% equity)',
        data_origin: 'Final Report §2.1 (Table 4; Notes 14 & 15)',
      },
      {
        heading: id ? 'Risiko 2: Biaya Promo & Pihak Berelasi' : 'Risk 2: Promo Costs & Related-Party Fees',
        text: id
          ? 'Promo berlebih Rp1,08T dicatat di biaya pemasaran (Catatan 26), dan pendapatan dari pihak berelasi (terutama Tokopedia) naik menjadi 7,13% dari total pendapatan.'
          : 'Rp1.08T of customer promos sit inside marketing expenses (Note 26), and related-party revenue (mostly Tokopedia fees) rose to 7.13% of total revenue.',
        formula: 'Related-Party Rev = Rp1,306.1bn (7.13% of Rev) | Expensed Incentives = Rp1,076.9bn',
        data_origin: 'Final Report §2.1 (Notes 2s, 25 & 26)',
      },
      {
        heading: id ? 'Risiko 3: Kredit Macet GoPay Naik Cepat' : 'Risk 3: Rising GoPay Loan Losses',
        text: id
          ? 'Pinjaman konsumen GoPay naik 72,6% ke Rp2,73T (memakai kas Rp2,02T), sementara cadangan kredit macet melonjak lebih dari 2x (+134,9%) ke Rp407,7M.'
          : 'GoPay consumer loans grew 72.6% to Rp2.73T (using Rp2.02T of cash), while bad-loan provisions more than doubled (+134.9%) to Rp407.7B.',
        formula: 'ECL Allowance: Rp173.6bn → Rp407.7bn (+134.9%) | +500 bps loss = −Rp136.5bn',
        data_origin: 'Final Report §2.1 (Note 7 & Cash Flow p. 21)',
      },
    ],
    7: [
      {
        heading: id ? 'Dasar Proyeksi 2024–2025' : 'Clean 2024–2025 Base Case',
        text: id
          ? 'Proyeksi Base memakai tren pasca-Tokopedia: pendapatan tumbuh 15,27%, COGS 42,28%, Cash OpEx 55,70%, dan CapEx 6,45%.'
          : 'Our Base Case uses GoTo’s actual post-Tokopedia track record: 15.27% sales growth, 42.28% COGS, 55.70% Cash OpEx, and 6.45% CapEx.',
        formula: '2025 Margin Spread = 57.72% Gross Margin − 55.70% Cash OpEx = +202 bps',
        data_origin: 'Final Report §4.1 (Table 11)',
      },
      {
        heading: id ? 'Kenapa Data 2023 Dibuang' : 'Why We Dropped 2023 Data',
        text: id
          ? 'Model lama merata-ratakan biaya tinggi 2023 (OpEx 117%) dan aset Tokopedia 2024, sehingga proyeksi dulu terlihat membakar kas jauh berlebihan.'
          : 'Our earlier draft averaged in 2023 pre-exit costs (117% OpEx) and Tokopedia intangibles, which exaggerated cash burn in the old forecast.',
        formula: 'Cash OpEx Restated: 78.5% (3-yr old) → 55.70% (FY2025 clean)',
        data_origin: 'Final Report §1.3 & Appendix B',
      },
      {
        heading: id ? 'Tiga Skenario yang Jelas' : 'Three Clear Scenarios',
        text: id
          ? 'Optimistis memakai efisiensi biaya 1H 2026 (OpEx 51,2%); Konservatif memakai pola biaya 2024 (OpEx 62,8%) jika promo kembali tinggi.'
          : 'Optimistic uses GoTo’s lower 1H 2026 costs (51.2% OpEx); Conservative returns to 2024 costs (62.8% OpEx) if heavy promos come back.',
        formula: 'Scenarios: Opt (51.2% OpEx) | Base (55.7% OpEx) | Cons (62.8% OpEx)',
        data_origin: 'Final Report §4.1 (Table 11)',
      },
    ],
    8: s8ByScenario[scenKey] || s8ByScenario.base,
    10: [
      {
        heading: id ? 'DCF Jadi Positif (+Rp10,38/saham)' : 'DCF Turns Positive (+Rp10.38/share)',
        text: id
          ? 'Setelah membuang data 2023, nilai DCF naik dari −Rp121,1 menjadi +Rp10,38 per saham (Kas Bersih +Rp14,01T dikurangi nilai operasi −Rp2,99T).'
          : 'Removing 2023 noise lifts Base DCF from −Rp121.1 to +Rp10.38 per share (+Rp14.01T Net Cash minus −Rp2.99T operating value).',
        formula: 'Equity Value = −Rp2,988.5bn EV + Rp14,012.5bn Net Cash = +Rp11,024.0bn (+Rp10.38/sh)',
        data_origin: 'Final Report §5.2 (Table 16)',
      },
      {
        heading: id ? 'Kenapa Nilai Operasi Masih Negatif' : 'Why Operating Value Is Still Negative',
        text: id
          ? 'Meski EBIT positif, biaya CapEx (Rp1,36T–1,81T/thn) masih lebih besar sehingga arus kas bebas tetap minus. Nilai +Rp10,38 datang dari kas GoTo (Rp13,19/saham).'
          : 'Even with positive EBIT, annual CapEx (Rp1.36T–1.81T) keeps free cash flow negative. The +Rp10.38 value comes from GoTo’s Rp13.19/share net cash.',
        formula: 'PV Explicit FCFF (−Rp967.9bn) + PV Terminal Value (−Rp2,020.6bn) = −Rp2,988.5bn EV',
        data_origin: 'Final Report §5.2',
      },
      {
        heading: id ? 'Residual Income Tetap Negatif (−Rp12,23)' : 'Residual Income Is Still Negative (−Rp12.23)',
        text: id
          ? 'ROE 2028F hanya +0,09%, jauh di bawah target investor 8,45%. Hasilnya −Rp12,23/saham (atau +Rp0,24 jika g = 0%; +Rp21,13 jika ROE = Ke di Tahun 4+).'
          : '2028F ROE (+0.09%) is far below the 8.45% return investors require. That gives −Rp12.23/share (+Rp0.24 at 0% growth; +Rp21.13 if ROE hits 8.45% in Yr 4+).',
        formula: 'Fundamental g = 126.42% × 2.70% ROIC = +3.41% (selected 3.00%)',
        data_origin: 'Final Report §5.1–5.2 (Tables 15–16)',
      },
    ],
    11: [
      {
        heading: id ? 'Rentang Nilai Wajar: Rp10,38–Rp16,75' : 'Fair Value Range: Rp10.38–Rp16.75',
        text: id
          ? 'Nilai wajar GoTo berada di Rp10,38 (DCF Base) hingga Rp16,75 (RI Optimistis), di sekitar Kas Bersih Rp13,19. Harga pasar Rp25,00 jauh terlalu tinggi.'
          : 'GoTo’s fair value sits between Rp10.38 (Base DCF) and Rp16.75 (Optimistic RI), centered around Rp13.19 Net Cash. The Rp25.00 market price is too high.',
        formula: 'Value Range: Rp10.38 (Base DCF) to Rp16.75 (Opt. RI) vs Rp25.00 Market',
        data_origin: 'Final Report §5.3 (Table 17)',
      },
      {
        heading: id ? 'Kenapa Kelipatan Grab (Rp91,02) Tidak Dipakai' : 'Why We Do Not Use Grab’s Multiple (Rp91.02)',
        text: id
          ? 'Grab sudah untung (ROE +2,96%), sehingga wajar dihargai 3,04x P/B. GoTo belum menutup biaya modalnya, jadi tidak adil memakai kelipatan Grab.'
          : 'Grab is already profitable (+2.96% ROE), which justifies its 3.04x P/B multiple. GoTo still earns below its cost of capital, so Grab’s multiple does not fit.',
        formula: 'Grab P/B = US$4.99 / US$1.6419 = 3.0391x × Rp29.95 BVPS = Rp91.02/sh',
        data_origin: 'Final Report §5.3 & Grab FY2025 20-F',
      },
      {
        heading: id ? 'Catatan Tanggal Data' : 'Pricing Date vs. Audited Results',
        text: id
          ? 'Harga Rp25,00 (30 Des 2025) kami bandingkan dengan laporan audit FY2025 (terbit Maret 2026), serta data biaya 1H 2026 khusus untuk skenario Optimistis.'
          : 'We compare the Dec 30, 2025 Rp25.00 share price against audited FY2025 statements (published March 2026), using 1H 2026 costs only in the Optimistic case.',
        formula: 'Market Quote: Dec 30, 2025 | FY2025 Audited Filing: March 2026',
        data_origin: 'Final Report §5.3',
      },
    ],
    12: [
      {
        heading: id ? 'Kesimpulan: Tetap SELL / AVOID di Rp25' : 'Verdict: SELL / AVOID at Rp25.00',
        text: id
          ? 'Walau Base Case mulai untung kecil di 2028F (+Rp25M), harga Rp25,00 (2,4x nilai DCF dan 1,9x kas bersih) terlalu mahal untuk investor jangka pendek.'
          : 'Even though the Base Case turns slightly profitable in 2028F (+Rp25B), paying Rp25.00 (2.4x DCF and 1.9x Net Cash) is too expensive for a short-term investor.',
        formula: 'Market Rp25.00 vs Fair Value Rp10.38–Rp16.75 (−33% to −58% downside)',
        data_origin: 'Final Report §6.1',
      },
      {
        heading: id ? 'Kapan Rekomendasi Berubah?' : 'When Would We Change Our Rating?',
        text: id
          ? 'Naik ke BUY jika Cash OpEx ≤ 51,2% & GM ≥ 61,9% dua kuartal beruntun. HOLD jika harga turun ≤ Rp13,20 dengan arus kas positif. Tetap SELL jika OpEx ≥ 60%.'
          : 'Move to BUY if Cash OpEx stays ≤ 51.2% and Gross Margin ≥ 61.9% for two quarters. Move to HOLD if price drops ≤ Rp13.20 with positive FCF. Stay SELL if OpEx ≥ 60%.',
        formula: 'BUY: OpEx ≤ 51.2% & GM ≥ 61.9% | HOLD: Price ≤ Rp13.20 & FCF > 0',
        data_origin: 'Final Report §6.2 (Table 18)',
      },
      {
        heading: id ? 'Risiko Utama yang Perlu Dipantau' : 'Key Risks to Watch',
        text: id
          ? 'Risiko naik: efisiensi biaya 1H 2026 bertahan penuh atau ada merger/akuisisi. Risiko turun: kredit macet GoPay makin naik atau penurunan nilai Tokopedia.'
          : 'Upside risks: faster cost cuts matching 1H 2026 or an M&A buyout. Downside risks: rising GoPay loan losses or a write-down on Tokopedia.',
        formula: '2028F ROIC (+2.70%) − WACC (7.76%) = −506 bps gap',
        data_origin: 'Final Report §6.3',
      },
    ],
  }
})
const visibleAnalysisPoints = computed(() => {
  if (isRestated.value && restatedPointsMap.value[props.slide.slide_num]) {
    return restatedPointsMap.value[props.slide.slide_num]
  }
  if (isDcfRiSlide.value && valuationBasis.value === '2yr') {
    const id = props.lang === 'id'
    const basePts = props.slide.analysis_points || []
    return basePts.map((pt, idx) => {
      if (idx === 1) {
        return {
          ...pt,
          text: id
            ? 'Kedua model memakai rata-rata 2 tahun (2024–2025: OpEx 59,2%, COGS 44,5%, CapEx 23,8%) tanpa 2023, dan nilai terminal melanjutkan rugi 2028F dengan pertumbuhan 3,0%.'
            : 'Both models use the 2-year average (2024–2025: 59.2% OpEx, 44.5% COGS, 23.8% CapEx), dropping 2023, with terminal value extending 2028F losses at 3.0% growth.',
        }
      }
      if (idx === 2) {
        return {
          ...pt,
          text: id
            ? 'Rugi menyusut tajam dibanding basis 3 tahun, namun arus kas bebas tetap negatif sehingga DCF menjadi −Rp72,5/saham dan Residual Income −Rp31,3/saham.'
            : 'Losses shrink sharply versus the 3-year base, yet free cash flow and net income stay negative—putting DCF at −Rp72.5/share and Residual Income at −Rp31.3/share.',
        }
      }
      return pt
    })
  }
  if (props.slide.slide_num === 6 && !isRestated.value) {
    const pts = props.slide.analysis_points || []
    if (pts.length >= 3) return [pts[0], pts[2], pts[1]]
    return pts
  }
  if (!isForecastSlide.value) return props.slide.analysis_points || []
  const id = props.lang === 'id'
  const byScenario = {
    base: [
      {
        heading: id ? 'Kasus Dasar (Base)' : 'Base Case',
        text: id
          ? 'Model memproyeksikan pendapatan Rp25.321M pada 2028F, tetapi rugi operasi berlanjut (-Rp4.967M) dan kas akhir turun dari Rp21.755M menjadi Rp968M.'
          : 'The model projects revenue of Rp25,321bn in 2028F, but operating losses continue (-Rp4,967bn) and ending cash falls from Rp21,755bn to Rp968bn.',
      },
      {
        heading: id ? 'Rasio Biaya Operasi' : 'Operating Cost Ratio',
        text: id
          ? 'Untuk setiap Rp100 penjualan, Kasus Dasar menghasilkan laba kotor Rp58,90 tetapi membelanjakan Rp78,50 untuk biaya operasi, mengunci defisit Rp19,60 per Rp100 pendapatan.'
          : 'For every Rp100 of sales, the Base Case earns Rp58.90 in gross profit but spends Rp78.50 on operating costs, locking in a Rp19.60 loss per Rp100 of revenue that grows as sales scale.',
      },
      {
        heading: id ? 'Penurunan Cadangan Kas' : 'Cash Cushion Drain',
        text: id
          ? 'Kerugian operasi dan CapEx 16,3% menguras kas Rp20.787M selama tiga tahun, menyisakan hanya Rp968M pada 2028F.'
          : 'Operating losses and 16.3% CapEx consume Rp20,787bn of cash over three years, leaving only Rp968bn by 2028F.',
      },
    ],
    base_2yr: [
      {
        heading: id ? 'Kasus Rata-rata 2 Tahun (2024–2025)' : '2-Year Avg Case (2024–2025)',
        text: id
          ? 'Mengeluarkan pembakaran biaya 2023 (117%) menurunkan OpEx dari 78,5% menjadi 59,2% (COGS 44,5%), sehingga rugi operasi 2026F menyusut 81% menjadi -Rp754,6M (vs -Rp4.003,4M).'
          : 'Dropping 2023’s 117% burn lowers OpEx from 78.5% to 59.2% (COGS 44.5%), shrinking 2026F operating loss by 81% to -Rp754.6bn (vs -Rp4,003.4bn in 3-yr Base).',
      },
      {
        heading: id ? 'Rasio Biaya Operasi (2 Tahun)' : 'Operating Cost Ratio (2-Yr Avg)',
        text: id
          ? 'Untuk setiap Rp100 penjualan, laba kotor Rp55,50 berbanding biaya operasi Rp59,20, menyisakan defisit operasi tipis -Rp3,70 per Rp100 penjualan (jauh lebih baik dari -Rp19,60).'
          : 'For every Rp100 of sales, gross profit is Rp55.50 vs Rp59.20 in cash OpEx—a small -Rp3.70 operating shortfall per Rp100 of sales (vs -Rp19.60 under 3-yr Base).',
      },
      {
        heading: id ? 'Kas Akhir & CapEx (2 Tahun)' : 'Cash Buffer & CapEx (2-Yr Avg)',
        text: id
          ? 'Dengan CapEx rata-rata 2 tahun sebesar 23,8% (terpengaruh lonjakan CapEx 2024 sebesar 41,0%), kas akhir 2028F tetap terjaga di Rp5.071M (vs Rp968M pada Base 3 tahun).'
          : 'With 2-year avg CapEx at 23.8% (pulled up by 2024’s 41.0% CapEx), 2028F ending cash stays at Rp5,071bn (vs Rp968bn in the 3-yr Base).',
      },
    ],
    optimistic: [
      {
        heading: id ? 'Kasus Optimistis' : 'Optimistic Case',
        text: id
          ? 'Pendapatan mencapai Rp28.084M pada 2028F (+15,3%/thn), laba operasi berbalik positif (+Rp1.741M), dan kas akhir terjaga di Rp21.284M.'
          : 'Revenue reaches Rp28,084bn in 2028F (+15.3%/yr), operating profit turns positive (+Rp1,741bn), and ending cash stays healthy at Rp21,284bn.',
      },
      {
        heading: id ? 'Rasio Biaya Operasi' : 'Operating Cost Ratio',
        text: id
          ? 'Untuk setiap Rp100 penjualan, Kasus Optimistis menghasilkan laba kotor Rp61,90 dengan biaya operasi Rp55,70, mencetak margin operasi +Rp6,20 per Rp100 pendapatan.'
          : 'For every Rp100 of sales, the Optimistic Case earns Rp61.90 in gross profit and spends Rp55.70 on operating costs, generating a +Rp6.20 operating margin per Rp100 of sales.',
      },
      {
        heading: id ? 'Pertumbuhan Didanai Sendiri' : 'Self-Funded Growth',
        text: id
          ? 'Laba bersih positif (+Rp605M hingga +Rp941M) dan CapEx efisien 6,5% menjaga kas tetap stabil di sekitar Rp21,3T hingga 2028F.'
          : 'Positive net income (+Rp605bn to +Rp941bn) and lean 6.5% CapEx keep cash roughly flat around Rp21.3T through 2028F without external funding.',
      },
    ],
    conservative: [
      {
        heading: id ? 'Kasus Konservatif' : 'Conservative Case',
        text: id
          ? 'Pendapatan tumbuh lambat ke Rp22.762M pada 2028F (+7,5%/thn), rugi operasi melebar ke -Rp7.193M, dan kas akhir berbalik negatif menjadi -Rp5.000M.'
          : 'Revenue grows slowly to Rp22,762bn in 2028F (+7.5%/yr), operating losses widen to -Rp7,193bn, and ending cash turns negative at -Rp5,000bn.',
      },
      {
        heading: id ? 'Rasio Biaya Operasi' : 'Operating Cost Ratio',
        text: id
          ? 'Untuk setiap Rp100 penjualan, Kasus Konservatif menghasilkan laba kotor Rp53,40 tetapi membelanjakan Rp85,00 untuk biaya operasi, menciptakan defisit -Rp31,60 per Rp100 penjualan.'
          : 'For every Rp100 of sales, the Conservative Case earns Rp53.40 in gross profit but spends Rp85.00 on operating costs, creating a -Rp31.60 operating shortfall per Rp100 of sales.',
      },
      {
        heading: id ? 'Defisit Likuiditas' : 'Liquidity Deficit',
        text: id
          ? 'Pembakaran kas yang besar dan CapEx 20,0% menghabiskan cadangan kas Rp21.755M pada 2028F (defisit -Rp5.000M), sehingga membutuhkan pendanaan atau pemangkasan biaya.'
          : 'Heavy burn and 20.0% CapEx exhaust the Rp21,755bn cash buffer by 2028F (-Rp5,000bn deficit), requiring financing or sharp cost cuts.',
      },
    ],
  }
  const basePoints = props.slide.analysis_points || []
  return (byScenario[forecastScenario.value] || byScenario.base).map((pt, idx) => ({
    ...basePoints[idx],
    ...pt,
    detail_explanation: pt.text,
  }))
})
const label = computed(() => props.slide.section_name || (props.lang === 'id' ? 'ANALISIS LAPORAN KEUANGAN' : 'FINANCIAL STATEMENT ANALYSIS'))
const editorialRows = computed(() => {
  const id = props.lang === 'id'
  if (isRestated.value && props.slide.slide_num === 5) {
    const base = props.slide.visual_rows || []
    return [
      {
        ...base[0],
        name: id ? 'Likuiditas & Siklus Modal Kerja' : 'Liquidity & Working Capital Cycle',
        value: '2.73x (+0.11x)',
        text: id
          ? 'Current Ratio: 2,62x (23) → 2,62x (24) → 2,73x (25)\nDSO 10,56h → 10,90h | DPO 61,1h → 59,1h | CCC −49,2h → −47,5h'
          : 'Current Ratio: 2.62x (23) → 2.62x (24) → 2.73x (25)\nDSO 10.56d → 10.90d | DPO 61.1d → 59.1d | CCC −49.2d → −47.5d',
        detail_explanation: id
          ? 'Menambahkan piutang pinjaman Catatan 7 (+Rp1.581,8M) memulihkan Current Ratio 2024 ke 2,62x dan 2025 meningkat +0,11x ke 2,73x (Modal Kerja naik Rp16,29T → Rp18,41T). Memisahkan piutang usaha Catatan 6 memperbaiki DSO YoY menjadi 14,84h (2023) → 10,56h (2024) → 10,90h (2025), dengan DPO 59,11h menjaga siklus kas negatif −47,54 hari.'
          : 'Restoring Rp1,581.8bn of omitted Note 7 lending receivables adjusts 2024 Current Ratio to 2.62x before rising +0.11x YoY to 2.73x in 2025 (Working Capital Rp16.29T → Rp18.41T). Aligning AR to Note 6 sets Trade DSO at 14.84d (2023) → 10.56d (2024) → 10.90d (2025), while 59.11d DPO keeps CCC negative at −47.54d.',
      },
      {
        ...base[1],
        name: id ? 'Solvabilitas & Cakupan Bunga' : 'Leverage & Interest Coverage',
        value: '26.97% / −0.71x',
        text: id
          ? 'Debt/Equity: 12,14% → 15,85% → 26,97% (+11,12 pp YoY)\nTIE: −27,83x → −4,54x → −0,71x (+3,83x YoY, Cat. 27b)'
          : 'Debt/Equity: 12.14% → 15.85% → 26.97% (+11.12 pp YoY)\nTIE: −27.83x → −4.54x → −0.71x (+3.83x YoY, Note 27b)',
        detail_explanation: id
          ? 'Memasukkan porsi utang jangka pendek dan semua liabilitas sewa (Catatan 19–20: Rp4,34T di 2023 → Rp4,82T di 2024 → Rp7,74T di 2025) mencatat D/E YoY 12,14% → 15,85% → 26,97% (+11,12 pp YoY), serta menautkan bunga Catatan 27b sehingga TIE membaik YoY dari −27,83x → −4,54x → −0,71x (+3,83x YoY).'
          : 'Harmonizing all short/long-term borrowings and leases (Notes 19–20: Rp4.34T → Rp4.82T → Rp7.74T) tracks Debt/Equity YoY at 12.14% → 15.85% → 26.97% (+11.12 pp YoY) and links Note 27b finance costs for live TIE improvement from −27.83x (2023) → −4.54x (2024) → −0.71x (2025, +3.83x YoY).',
      },
      {
        ...base[2],
        name: id ? 'Altman Z-Score (Buku / Pasar)' : 'Altman Z-Score (Book / Mkt)',
        value: '−4.72 / −4.80',
        text: id
          ? 'Sensitivitas X4: Buku 1,68x (−4,72) vs Pasar Rp25 1,56x (−4,80)\nX2 (−6,59 rugi historis 2023) mendominasi; X1 (+0,40) sehat'
          : 'X4 Sensitivity: Book 1.68x (−4.72) vs Mkt Rp25 1.56x (−4.80)\nX2 (−6.59 sunk 2023 losses) dominates; X1 (+0.40) healthy',
        detail_explanation: id
          ? 'Uji sensitivitas X4 antara Ekuitas Buku (1,6844x → Z = −4,72) dan Nilai Pasar Rp25,00 (1,5576x → Z = −4,80) membuktikan zona distress (< 1,81) berasal dari X2 (−6,59 akibat akumulasi rugi historis 2023) alih-alih krisis kas jangka pendek (X1 tetap kuat +0,40).'
          : 'Testing X4 sensitivity between Book Equity (1.6844x → Z = −4.72) and Market Cap at Rp25.00 (1.5576x → Z = −4.80) confirms the distress score (< 1.81) stems from sunk 2023 accumulated losses (X2 = −6.59) rather than 12-month liquidity risk (X1 stays healthy at +0.40).',
      },
    ]
  }
  if (isRestated.value && props.slide.slide_num === 12) {
    const base = props.slide.visual_rows || []
    return [
      {
        ...base[0],
        name: id ? 'Rekomendasi final (12 bulan)' : 'Final verdict (12-month horizon)',
        value: 'SELL / AVOID',
        text: id
          ? 'Harga pasar Rp25,00 jauh di atas rentang Rp10,38–Rp16,75\n(2,41x Base DCF Rp10,38 & 1,90x Kas Bersih Rp13,19)'
          : 'Rp25.00 market price exceeds Rp10.38–Rp16.75 range\n(2.41x Base DCF Rp10.38 & 1.90x Net Cash Rp13.19)',
        detail_explanation: id
          ? 'Berdasarkan Laporan Akhir yang direvisi, rekomendasi SELL / AVOID pada Rp25,00 tetap dipertahankan bagi investor ekuitas jangka pendek karena harga pasar mencerminkan premi 50%–141% di atas nilai intrinsik fundamental.'
          : 'Under the restated Final Report, SELL / AVOID at Rp25.00 holds for a short-term public equity investor: market pricing stands well above our Rp10.38–Rp16.75/share intrinsic range.',
      },
      {
        ...base[1],
        name: id ? 'Spread nilai ekonomi (ROIC vs WACC)' : 'Economic spread (ROIC vs WACC)',
        value: '−506 bps',
        text: id
          ? '2028F ROIC (+2,70%) tertinggal di bawah WACC (7,76%)\nLaba akuntansi positif (+Rp25M) belum ciptakan nilai'
          : '2028F Base ROIC (+2.70%) trails WACC (7.76%)\nNet profit (+Rp25bn) still destroys economic value',
        detail_explanation: id
          ? 'Meskipun perbaikan pasca-Tokopedia membalik EBIT 2026F (+Rp426,9M) dan Laba Bersih 2028F (+Rp25,0M) menjadi positif, ROIC 2028F (+2,70%) tetap jauh di bawah WACC (7,76%) dan ROE (+0,09%) di bawah Ke (8,45%).'
          : 'Although removing 2023 distortions turns Base EBIT (+Rp426.9bn in 2026F) and Net Income (+Rp25.0bn in 2028F) positive, 2028F ROIC (+2.70%) still trails WACC (7.76%) by 506 bps.',
      },
      {
        ...base[2],
        name: id ? 'Pemicu re-rating terukur (Appendix A6)' : 'Upgrade triggers (Appendix A6)',
        value: '≤ Rp13.20 / ≤ 51.2%',
        text: id
          ? 'HOLD: harga ≤ Rp13,20 (1,0x Kas Bersih) & FCF > 0\nBUY: Cash OpEx ≤ 51,2% & Margin Kotor ≥ 61,9% (2Q)'
          : 'HOLD: price ≤ Rp13.20 (1.0x Net Cash) w/ FCF > 0\nBUY: Cash OpEx ≤ 51.2% & Gross Margin ≥ 61.9% (2Q)',
        detail_explanation: id
          ? 'Ambang re-rating kuantitatif (Appendix A6): naikkan ke HOLD bila harga turun ≤ Rp13,20 dengan FCF positif, naikkan ke BUY bila efisiensi 1H 2026 (Cash OpEx ≤ 51,2%, GM ≥ 61,9%) bertahan dua kuartal berturut-turut.'
          : 'Quantitative re-rating thresholds (Appendix A6): upgrade to HOLD if IDX price pulls back to ≤ Rp13.20 with positive FCF; upgrade to BUY if Cash OpEx ≤ 51.2% and Gross Margin ≥ 61.9% hold for two consecutive quarters.',
      },
    ]
  }
  if (props.slide.visual_rows) return props.slide.visual_rows
  if (props.slide.story_rebuilt) return null
  if (props.slide.slide_num === 2) return [
    {
      name: 'Gojek',
      value: 'Rp 12,361 bn',
      img: '/visuals/row_gojek.png',
      text: id ? 'Mobilitas, pengantaran makanan, dan logistik' : 'Mobility, food delivery, and logistics',
      detail_explanation: id
        ? 'Berasal dari Catatan 29 (Segmen Operasi) pada Laporan Tahunan 2025 hal. 468 / LK Auditan FY2025 hal. 133. Gojek (On-Demand Services) adalah mesin pendapatan terbesar GoTo (67,5% dari total pendapatan bersih konsolidasian) dan mencetak laba segmen +Rp 888,6 M sebelum biaya korporasi.'
        : 'From Note 29 (Segment Operations) in the 2025 Annual Report p. 468 / Audited LK GOTO FY2025 p. 133. Gojek (On-Demand Services) is GoTo’s largest revenue engine (67.5% of consolidated net revenue) and generated +Rp 888.6 bn in segment operating profit before corporate overhead.',
      formula: id ? 'Pendapatan Bersih ODS = Rp 15.030,99 M (Bruto) − Rp 2.669,74 M (Insentif) = Rp 12.361,26 M' : 'ODS Net Revenue = Rp 15,030.99 bn (Gross) − Rp 2,669.74 bn (Incentives) = Rp 12,361.26 bn',
      calc_steps: [
        id ? 'Pendapatan bruto pihak ketiga ODS: Rp 15.030.994 juta' : 'Gross third-party ODS revenue: Rp 15,030,994 million',
        id ? 'Dikurangi insentif kepada pelanggan: (Rp 2.669.735 juta)' : 'Less customer incentives & promos: (Rp 2,669,735 million)',
        id ? 'Pendapatan bersih pihak ketiga Gojek: Rp 12.361.259 juta (dibulatkan Rp 12.361 M)' : 'Net third-party Gojek revenue: Rp 12,361,259 million (rounded Rp 12,361 bn)',
        id ? 'Ditambah antar-segmen Rp 234.884 juta → Laba operasi segmen: +Rp 888.619 juta' : 'Plus inter-segment Rp 234,884m → Segment operating profit: +Rp 888,619m',
        id ? 'Rekonsiliasi konsolidasi: 12.361,26 + 5.190,62 + 819,72 − 49,48 (eliminasi promo) = Rp 18.322,12 M' : 'Consolidated tie-out: 12,361.26 + 5,190.62 + 819.72 − 49.48 (promo elimination) = Rp 18,322.12 bn',
      ],
      data_origin: '2025 Annual Report p. 468 & LK GOTO FY2025 p. 133 (Note 29: Segment Operations)',
      highlight_terms: ['12,361', '12,361,259', 'On-Demand', 'Gojek'],
      evidence_img: '/evidence/annual_report_p468_segment_note29.png',
      evidence_caption: '2025 Annual Report p. 468 (Note 29: Segment Operations): On-Demand Services Net Third-Party Revenue = Rp 12,361,259m',
    },
    {
      name: 'GoTo Financial',
      value: 'Rp 5,191 bn',
      img: '/visuals/row_gofinancial.png',
      text: id ? 'Pembayaran digital dan pinjaman konsumen' : 'Digital payments and consumer lending',
      detail_explanation: id
        ? 'Angka ini juga berasal dari Catatan 29 (Segmen Operasi) di Laporan Tahunan 2025 hal. 468 / LK Auditan FY2025 hal. 133 (Rp 5.190.617 juta, dibulatkan menjadi Rp 5.191 M). Segmen FinTech (GoPay & pinjaman konsumen) adalah mesin pertumbuhan tercepat GoTo, tetapi masih membukukan rugi operasi segmen sebesar −Rp 396,6 M karena ekspansi kredit dan pencadangan kerugian pinjaman.'
        : 'This figure also comes from Note 29 (Segment Operations) in the 2025 Annual Report p. 468 / Audited LK GOTO FY2025 p. 133 (Rp 5,190,617 million, rounded to Rp 5,191 bn). Financial Technology (GoPay payments & consumer lending) is GoTo’s fastest-growing segment, though it still posted a segment operating loss of −Rp 396.6 bn due to credit provisions and scaling.',
      formula: id ? 'Pendapatan Bersih FinTech = Rp 5.460,84 M (Bruto) − Rp 270,23 M (Insentif) = Rp 5.190,62 M' : 'FinTech Net Revenue = Rp 5,460.84 bn (Gross) − Rp 270.23 bn (Incentives) = Rp 5,190.62 bn',
      calc_steps: [
        id ? 'Pendapatan bruto pihak ketiga FinTech: Rp 5.460.844 juta' : 'Gross third-party FinTech revenue: Rp 5,460,844 million',
        id ? 'Dikurangi insentif kepada pelanggan: (Rp 270.227 juta)' : 'Less customer incentives: (Rp 270,227 million)',
        id ? 'Pendapatan bersih pihak ketiga FinTech: Rp 5.190.617 juta (dibulatkan Rp 5.191 M)' : 'Net third-party FinTech revenue: Rp 5,190,617 million (rounded Rp 5,191 bn)',
        id ? 'Rugi operasi segmen FinTech: −Rp 396.607 juta (pinjaman konsumen bersih Rp 2.731 M)' : 'FinTech segment operating loss: −Rp 396,607m (net consumer loans Rp 2,731 bn)',
      ],
      data_origin: '2025 Annual Report p. 468 & LK GOTO FY2025 p. 133 (Note 29: Segment Operations)',
      highlight_terms: ['5,191', '5,190,617', 'Financial technology', 'GoPay'],
      evidence_img: '/evidence/annual_report_p468_segment_note29.png',
      evidence_caption: '2025 Annual Report p. 468 (Note 29: Segment Operations): Financial Technology Net Third-Party Revenue = Rp 5,190,617m',
    },
    {
      name: 'Tokopedia',
      value: 'Rp 820 bn',
      img: '/visuals/row_tokopedia.png',
      text: id ? 'Kepemilikan tersisa. Rp 820 miliar pendapatan jasa.' : 'Retained stake. Rp 820 bn in service fee revenue.',
      detail_explanation: id
        ? 'Setelah GoTo mengalihkan 75,01% kendali Tokopedia kepada TikTok pada Januari 2024, GoTo tidak lagi mengonsolidasi pendapatan GMV Tokopedia. Sebaliknya, porsi tersisa 24,99% dicatat sebagai entitas asosiasi (Catatan 14 LK GOTO 2025), dan GoTo menerima imbalan jasa e-commerce sebesar Rp 819,72 M (~Rp 820 M) per tahun berdasarkan persentase GMV Inti Tokopedia (Catatan 29 & 25).'
        : 'After GoTo transferred 75.01% control of Tokopedia to TikTok in January 2024, GoTo stopped consolidating Tokopedia’s operating revenue. Instead, the remaining 24.99% is accounted for as an equity-method associate (Note 14), and GoTo collects an e-commerce service fee of Rp 819.72 bn (~Rp 820 bn) based on Tokopedia’s Core GMV (Note 29 & Note 25).',
      formula: id ? 'Kepemilikan Tersisa = 100% − 75,01% = 24,99% | Imbalan Jasa = Rp 819,72 M' : 'Retained Stake = 100% − 75.01% = 24.99% | Service Fee = Rp 819.72 bn',
      calc_steps: [
        id ? 'Porsi saham tersisa di PT Tokopedia (Catatan 14): 24,99%' : 'Retained ownership in PT Tokopedia (Note 14): 24.99%',
        id ? 'Pendapatan jasa e-commerce FY2025 (Catatan 29): Rp 819.724 juta (~Rp 820 M)' : 'FY2025 e-commerce service fee revenue (Note 29): Rp 819,724m (~Rp 820 bn)',
        id ? 'Total aset entitas asosiasi (Tokopedia + Bank Jago): 22,57% dari total aset GoTo' : 'Total investments in associates (Tokopedia + Bank Jago): 22.57% of GoTo total assets',
      ],
      data_origin: 'LK GOTO FY2025 Note 14 (Associates) & Annual Report p. 468 (Note 29)',
      highlight_terms: ['24.99%', '819,724', 'Tokopedia'],
      evidence_img: '/evidence/goto_note14_associates_tokopedia_jago.png',
      evidence_caption: 'LK GOTO FY2025 Note 14: Investments in Associates (PT Tokopedia 24.99% & Bank Jago)',
    },
  ]
  if (props.slide.slide_num === 5) return [
    {
      name: id ? 'Arus kas operasi' : 'Operating cash flow',
      value: '+Rp 307 bn',
      img: '/visuals/row_cfo.png',
      text: id ? 'Kas yang dihasilkan dari operasi pada 2025' : 'Cash generated from operations in 2025',
      detail_explanation: id
        ? 'Arus kas bersih dari aktivitas operasi pada Laporan Arus Kas Konsolidasian FY2025 sebesar +Rp 307.183 juta. Meski positif secara headline setelah defisit tahun-tahun sebelumnya, jumlah ini belum cukup menutup belanja modal dan sebagian terbantu oleh pergerakan modal kerja.'
        : 'FY2025 Consolidated Net Cash Provided by Operating Activities was +Rp 307,183 million. While headline positive after prior-year burns, it remains insufficient to cover capital expenditure and was partly supported by working-capital timing.',
      formula: id ? 'CFO FY2025 = +Rp 307.183 juta (+Rp 307 M) | Akrual M3 = (Laba Bersih − CFO) / Aset Akhir = −3,95%' : 'FY2025 CFO = +Rp 307,183m (+Rp 307 bn) | M3 Accrual = (Net Income − CFO) / Closing Assets = −3.95%',
      calc_steps: [
        id ? 'Arus kas bersih dari aktivitas operasi (LK Arus Kas): +Rp 307.183 juta' : 'Net cash from operating activities (Cash Flow Statement): +Rp 307,183m',
        id ? 'Bandingkan dengan Rugi Bersih FY2025: −Rp 1.441,7 M → selisih non-kas/modal kerja = akrual −3,95%' : 'Compare vs FY2025 Net Loss −Rp 1,441.7 bn → non-cash/WC bridge = −3.95% accrual ratio',
      ],
      data_origin: 'LK GOTO FY2025 Consolidated Statement of Cash Flows & Milestone 3!Calculations D12',
      highlight_terms: ['307', '307,183', 'Operating'],
      evidence_img: '/evidence/goto_cash_flows_p1_highlighted.png',
      evidence_caption: 'LK GOTO FY2025 Consolidated Statement of Cash Flows (Part 1): Operating Cash Flow = +Rp 307,183m',
    },
    {
      name: id ? 'Belanja modal' : 'Capital expenditure',
      value: 'Rp 1,182 bn',
      img: '/visuals/row_capex.png',
      text: id ? 'Cakupan arus kas operasi hanya 26%' : 'Only 26% covered by operating cash flow',
      detail_explanation: id
        ? 'Mengukur kas yang keluar untuk membeli aset tetap, perangkat lunak, dan infrastruktur platform pada FY2025 (Rp 1.182.518 juta). Karena CFO hanya +Rp 307 M, operasi inti baru mampu membiayai 25,97% dari kebutuhan capex tahunan.'
        : 'Measures cash spent on property, equipment, software, and platform infrastructure in FY2025 (Rp 1,182,518 million). Because CFO was only +Rp 307 bn, core operations funded just 25.97% of annual capital expenditure.',
      formula: id ? 'Cakupan Capex = CFO / Capex = Rp 307,18 M / Rp 1.182,52 M = 25,97%' : 'Capex Coverage = CFO / Capex = Rp 307.18 bn / Rp 1,182.52 bn = 25.97%',
      calc_steps: [
        id ? 'Arus kas operasi (CFO): Rp 307.183 juta' : 'Operating cash flow (CFO): Rp 307,183m',
        id ? 'Belanja modal (Capex): Rp 1.182.518 juta' : 'Capital expenditure (Capex): Rp 1,182,518m',
        id ? 'Rasio cakupan = 307.183 / 1.182.518 = 25,97% (~26%)' : 'Coverage ratio = 307,183 / 1,182,518 = 25.97% (~26%)',
      ],
      data_origin: 'LK GOTO FY2025 Cash Flows (Investing) & Milestone 3!Calculations D36',
      highlight_terms: ['1,182', '25.97%', '26%'],
      evidence_img: '/evidence/goto_cash_flows_p2_highlighted.png',
      evidence_caption: 'LK GOTO FY2025 Consolidated Statement of Cash Flows (Part 2): Investing Capex & Cash Bridge',
    },
    {
      name: id ? 'Arus kas bebas' : 'Free cash flow',
      value: '−Rp 875 bn',
      img: '/visuals/row_fcf.png',
      text: id ? 'Kekurangan setelah belanja modal' : 'Funding shortfall after capital expenditure',
      detail_explanation: id
        ? 'Arus kas bebas (FCF) menunjukkan sisa kas untuk pemegang saham dan kreditur setelah investasi pemeliharaan/pertumbuhan aset. Nilai −Rp 875 M (−Rp 875.335 juta) membuktikan GoTo masih mengalami defisit kas operasional bersih setiap tahunnya.'
        : 'Free cash flow (FCF) measures cash left over for debt and equity holders after funding capital investments. At −Rp 875 bn (−Rp 875,335 million), GoTo still faces an annual operating-plus-investment cash shortfall.',
      formula: id ? 'FCF = CFO − Capex = Rp 307,18 M − Rp 1.182,52 M = −Rp 875,34 M' : 'FCF = CFO − Capex = Rp 307.18 bn − Rp 1,182.52 bn = −Rp 875.34 bn',
      calc_steps: [
        id ? 'CFO (+Rp 307.183 juta) − Capex (Rp 1.182.518 juta) = −Rp 875.335 juta (~−Rp 875 M)' : 'CFO (+Rp 307,183m) − Capex (Rp 1,182,518m) = −Rp 875,335m (~−Rp 875 bn)',
      ],
      data_origin: 'Milestone 3!Calculations D37 (−875,335)',
      highlight_terms: ['875', 'Free cash flow'],
      evidence_img: '/evidence/goto_cash_flows_p2_highlighted.png',
      evidence_caption: 'LK GOTO FY2025 Consolidated Statement of Cash Flows: CFO vs. Investing Capex Shortfall',
    },
  ]
  if (props.slide.slide_num === 11) return [
    {
      name: id ? '01  Arus kas mandiri' : '01  Self-funding cash flow',
      value: '> Rp 1.2T',
      img: '/visuals/row_hurdle_cfo.png',
      text: id ? 'Arus kas operasi tahunan menutup capex tanpa utang baru' : 'Annual operating cash flow covers capex without new borrowing',
      detail_explanation: id
        ? 'Syarat pertama untuk mengubah rekomendasi dari SELL/AVOID: arus kas operasi tahunan harus naik dari +Rp 307 M menjadi di atas ~Rp 1,2T agar belanja modal tahunan (Rp 1,18T) tertutup secara organik tanpa menguras cadangan kas atau menambah utang.'
        : 'First hurdle to upgrade from SELL/AVOID: annual operating cash flow must rise from +Rp 307 bn to > Rp 1.2T so annual capex (Rp 1.18T) is funded organically without draining cash or raising debt.',
      formula: id ? 'Syarat 1: CFO Tahunan ≥ Capex (~Rp 1,2T) → FCF ≥ 0' : 'Hurdle 1: Annual CFO ≥ Capex (~Rp 1.2T) → FCF ≥ 0',
      calc_steps: [
        id ? 'Baseline FY2025: CFO Rp 307 M vs Capex Rp 1.182 M (defisit FCF −Rp 875 M)' : 'FY2025 baseline: CFO Rp 307 bn vs Capex Rp 1,182 bn (FCF shortfall −Rp 875 bn)',
      ],
      data_origin: 'Final Report Section 7 & Milestone 3!Calculations D36:D37',
      highlight_terms: ['1.2T', 'capex', 'CFO'],
      evidence_img: '/evidence/goto_cash_flows_p1_highlighted.png',
      evidence_caption: 'LK GOTO FY2025 Cash Flows: Baseline CFO (+Rp 307 bn) vs. > Rp 1.2T Self-Funding Hurdle',
    },
    {
      name: id ? '02  Disiplin biaya' : '02  Operating cost discipline',
      value: '< 56%',
      img: '/visuals/row_hurdle_opex.png',
      text: id ? 'Beban operasi sebagai persentase pendapatan' : 'Operating expenses as a percentage of revenue',
      detail_explanation: id
        ? 'Syarat kedua: rasio beban operasi (OpEx / Pendapatan) harus turun di bawah 56% secara berkelanjutan. Dalam skenario dasar Tugas 14 yang memakai rata-rata historis 78,5%, GoTo terus membakar kas Rp 6,6T–7,5T/tahun dan nilai intrinsik menjadi negatif.'
        : 'Second hurdle: operating expenses as a share of revenue must stay below 56%. Under Assignment 14’s historical mean-reverting assumption (78.5% OpEx/Revenue), GoTo burns Rp 6.6T–7.5T/yr and intrinsic equity value turns negative.',
      formula: id ? 'Syarat 2: OpEx / Pendapatan < 56% (vs asumsi historis 78,5%)' : 'Hurdle 2: OpEx / Revenue < 56% (vs. 78.5% historical assumption)',
      calc_steps: [
        id ? 'Analisis titik impas fixed-OpEx (Tugas 14): impas terjadi pada pendapatan Rp 18.604 M' : 'Assignment 14 fixed-OpEx breakeven: operating breakeven requires Rp 18,604 bn revenue',
      ],
      data_origin: 'Milestone 4 & Assignment 14 Sensitivity/Breakeven',
      highlight_terms: ['56%', '78.5%', 'OpEx'],
      evidence_img: '/evidence/goto_gross_profit_opex_highlighted.png',
      evidence_caption: 'LK GOTO FY2025 Income Statement: Gross Profit vs. Operating Expenses Structure',
    },
    {
      name: id ? '03  Laba berkelanjutan' : '03  Sustained profitability',
      value: '> Rp 2.43T',
      img: '/visuals/row_hurdle_profit.png',
      text: id ? 'Laba bersih selama dua tahun berturut-turut' : 'Annual net income for two consecutive years',
      detail_explanation: id
        ? 'Syarat ketiga: laba bersih harus melampaui beban biaya ekuitas tahunan (Rp 28.711,66 M × Ke 8,45% = Rp 2,43T/tahun) selama dua tahun berturut-turut. Tanpa melewati Rp 2,43T, Residual Income tetap negatif dan perusahaan belum menciptakan nilai ekonomi bagi pemegang saham.'
        : 'Third hurdle: annual net income must exceed the equity capital charge (Rp 28,711.66 bn × 8.45% Ke = Rp 2.43T/yr) for two consecutive years. Below Rp 2.43T, Residual Income remains negative and destroys shareholder value.',
      formula: id ? 'Beban Ekuitas = BVE Awal (Rp 28.711,66 M) × Ke (8,45%) = Rp 2,43T / tahun' : 'Equity Charge = Beginning BVE (Rp 28,711.66 bn) × Ke (8.45%) = Rp 2.43T / yr',
      calc_steps: [
        id ? 'Residual Income = Laba Bersih − (BVE Awal × 8,45%)' : 'Residual Income = Net Income − (Beginning BVE × 8.45%)',
        id ? 'RI > 0 hanya tercapai jika Laba Bersih > Rp 2,43T/tahun' : 'RI > 0 only when Net Income > Rp 2.43T/yr',
      ],
      data_origin: 'Residual Income Valuation!B5:D10 (Assignment 14 Workbook)',
      highlight_terms: ['2.43T', '8.45%', 'Residual Income'],
      evidence_img: '/evidence/goto_balance_sheet_liabilities_equity_highlighted.png',
      evidence_caption: 'LK GOTO FY2025 Equity Base & Assignment 14 Residual Income Equity Charge Hurdle',
    },
  ]
  return null
})
const bannerMap = {
  6: '/visuals/banner_slide6_forecast.png',
  7: '/visuals/banner_slide7_wacc.png',
  8: '/visuals/banner_slide8_intrinsic.png',
}
const slideBannerUrl = computed(() => props.slide.hide_banner ? '' : bannerMap[layoutSlide.value] || '')
const lossScale = computed(() => Math.max(...(props.slide.loss_chart?.series || []).map(row => Math.abs(row.value)), 1))
const rangeX = value => 145 + (value + 140) / 260 * 345

const pointIcons = {
  '2-2': {
    risk: false,
    svg: '<path d="M22 26V11a15 15 0 1 0 15 15H22z" fill="#86efac" stroke="#008c2c" stroke-width="2.2" stroke-linejoin="round"/><path d="M26 9a15 15 0 0 1 13 13H26V9z" fill="#008c2c" stroke="#008c2c" stroke-width="2" stroke-linejoin="round"/><circle cx="35" cy="13" r="3" fill="#efc96c"/>',
  },
  '3-0': {
    risk: true,
    svg: '<path d="M12 34L33 13M33 13h-7M33 13v7" stroke="#dc2626" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M36 34L15 13M15 13h7M15 13v7" stroke="#ef4444" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="24" r="4.5" fill="#fecaca" stroke="#dc2626" stroke-width="2"/>',
  },
  '3-1': {
    risk: false,
    svg: '<circle cx="17" cy="16" r="5" fill="#86efac" stroke="#008c2c" stroke-width="2.2"/><circle cx="31" cy="16" r="5" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M9 33c0-4.4 3.6-8 8-8s8 3.6 8 8" fill="#86efac" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round"/><path d="M23 33c0-4.4 3.6-8 8-8s8 3.6 8 8" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round"/><path d="M19 38h10M26 35l3 3-3 3" stroke="#008c2c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  },
  '3-2': {
    risk: true,
    svg: '<rect x="8" y="15" width="26" height="18" rx="3" fill="#fecaca" stroke="#dc2626" stroke-width="2.2"/><path d="M8 21h26" stroke="#dc2626" stroke-width="2.5"/><path d="M33 21l8 14H25l8-14z" fill="#fca5a5" stroke="#b91c1c" stroke-width="2" stroke-linejoin="round"/><path d="M33 26v4M33 32.5v.5" stroke="#7f1d1d" stroke-width="2" stroke-linecap="round"/>',
  },
  '4-0': {
    risk: true,
    svg: '<path d="M10 15l10 10 7-5 11 11" stroke="#dc2626" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M31 31h7v-7" stroke="#dc2626" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="9" y="34" width="30" height="4" rx="2" fill="#fecaca"/>',
  },
  '4-1': {
    risk: false,
    svg: '<path d="M24 10v26M15 36h18" stroke="#008c2c" stroke-width="2.4" stroke-linecap="round"/><path d="M11 17h26" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round"/><path d="M11 17l-4 10h8l-4-10zM37 17l-4 10h8l-4-10z" fill="#bbf7d0" stroke="#008c2c" stroke-width="2" stroke-linejoin="round"/>',
  },
  '4-2': {
    risk: true,
    svg: '<path d="M24 9l15 27H9L24 9z" fill="#fecaca" stroke="#dc2626" stroke-width="2.3" stroke-linejoin="round"/><path d="M24 19v8M24 31v1" stroke="#991b1b" stroke-width="2.6" stroke-linecap="round"/>',
  },
  '5-0': {
    risk: true,
    svg: '<rect x="12" y="10" width="24" height="28" rx="4" fill="#fff" stroke="#dc2626" stroke-width="2.2"/><rect x="15" y="29" width="18" height="6" rx="1.5" fill="#fca5a5"/><path d="M15 22h18" stroke="#fecaca" stroke-width="2" stroke-dasharray="3 2"/>',
  },
  '5-1': {
    risk: false,
    svg: '<rect x="9" y="11" width="30" height="26" rx="3" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M15 20h18M15 27h10M29 25l3 3 5-6" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
  },
  '5-2': {
    risk: false,
    svg: '<rect x="10" y="9" width="20" height="28" rx="3" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M15 16h10M15 22h8" stroke="#008c2c" stroke-width="2" stroke-linecap="round"/><circle cx="31" cy="29" r="6" fill="#edf6ef" stroke="#008c2c" stroke-width="2.2"/><path d="M35.5 33.5L40 38" stroke="#008c2c" stroke-width="2.5" stroke-linecap="round"/>',
  },
  '6-0': {
    risk: false,
    svg: '<rect x="10" y="25" width="6" height="12" rx="1.5" fill="#86efac" stroke="#008c2c" stroke-width="1.8"/><rect x="21" y="19" width="6" height="18" rx="1.5" fill="#86efac" stroke="#008c2c" stroke-width="1.8"/><rect x="32" y="12" width="6" height="25" rx="1.5" fill="#008c2c"/>',
  },
  '6-1': {
    risk: true,
    svg: '<path d="M10 33c7-2 12-10 17-16l11-4" stroke="#dc2626" stroke-width="2.6" stroke-linecap="round"/><circle cx="38" cy="13" r="3.5" fill="#fecaca" stroke="#dc2626" stroke-width="2"/><path d="M10 37h28" stroke="#fca5a5" stroke-width="2" stroke-linecap="round"/>',
  },
  '6-2': {
    risk: false,
    svg: '<circle cx="12" cy="24" r="3.5" fill="#008c2c"/><path d="M15.5 24H24M24 24l8-10h6M24 24h14M24 24l8 10h6" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="38" cy="14" r="2.5" fill="#86efac" stroke="#008c2c" stroke-width="1.8"/><circle cx="38" cy="24" r="2.5" fill="#86efac" stroke="#008c2c" stroke-width="1.8"/><circle cx="38" cy="34" r="2.5" fill="#86efac" stroke="#008c2c" stroke-width="1.8"/>',
  },
  '7-0': {
    risk: false,
    svg: '<circle cx="24" cy="24" r="14" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><ellipse cx="24" cy="24" rx="6.5" ry="14" stroke="#008c2c" stroke-width="1.8"/><path d="M10 24h28" stroke="#008c2c" stroke-width="1.8"/>',
  },
  '7-1': {
    risk: false,
    svg: '<rect x="8" y="17" width="32" height="14" rx="3" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><rect x="8" y="17" width="23" height="14" rx="3" fill="#008c2c"/><path d="M14 24h11" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>',
  },
  '7-2': {
    risk: false,
    svg: '<rect x="10" y="12" width="28" height="26" rx="3" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M10 20h28M18 9v6M30 9v6" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round"/><circle cx="24" cy="29" r="3.5" fill="#008c2c"/>',
  },
  '8-0': {
    risk: true,
    svg: '<path d="M12 20h24M12 28h16" stroke="#dc2626" stroke-width="2.4" stroke-linecap="round"/><rect x="8" y="11" width="32" height="26" rx="4" fill="#fecaca" fill-opacity="0.45" stroke="#dc2626" stroke-width="2.2"/><path d="M31 28h6" stroke="#991b1b" stroke-width="2.6" stroke-linecap="round"/>',
  },
  '8-1': {
    risk: true,
    svg: '<circle cx="24" cy="24" r="14" fill="#fecaca" stroke="#dc2626" stroke-width="2.2"/><path d="M17 24h14" stroke="#991b1b" stroke-width="3" stroke-linecap="round"/>',
  },
  '8-2': {
    risk: false,
    svg: '<path d="M17 29c-3.5 0-6-2.5-6-5.5S13.5 18 17 18c4 0 6 5.5 7 5.5s3-5.5 7-5.5c3.5 0 6 2.5 6 5.5S34.5 29 31 29c-4 0-6-5.5-7-5.5S21 29 17 29z" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.3"/>',
  },
  '9-0': {
    risk: false,
    svg: '<rect x="10" y="15" width="12" height="22" rx="2" fill="#86efac" stroke="#008c2c" stroke-width="2"/><rect x="26" y="11" width="12" height="26" rx="2" fill="#bbf7d0" stroke="#008c2c" stroke-width="2"/><path d="M19 24h10" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round"/>',
  },
  '9-1': {
    risk: false,
    svg: '<path d="M11 33L33 11l4 4L15 37H11v-4z" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2" stroke-linejoin="round"/><circle cx="31" cy="17" r="2" fill="#008c2c"/>',
  },
  '9-2': {
    risk: true,
    svg: '<path d="M10 12h28l-10 13v11l-8-3v-8L10 12z" fill="#fecaca" stroke="#dc2626" stroke-width="2.2" stroke-linejoin="round"/>',
  },
  '10-0': {
    risk: false,
    svg: '<path d="M11 16h18M11 24h26M11 32h12" stroke="#008c2c" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="16" r="3" fill="#efc96c"/><circle cx="26" cy="32" r="3" fill="#86efac" stroke="#008c2c" stroke-width="1.8"/>',
  },
  '10-1': {
    risk: true,
    svg: '<circle cx="24" cy="24" r="13" fill="#fecaca" stroke="#dc2626" stroke-width="2.2"/><path d="M16 16l16 16" stroke="#991b1b" stroke-width="2.6" stroke-linecap="round"/>',
  },
  '10-2': {
    risk: false,
    svg: '<rect x="10" y="10" width="28" height="28" rx="4" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M16 19l3 3 6-6M16 29l3 3 6-6M28 19h5M28 29h5" stroke="#008c2c" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
  },
  '11-0': {
    risk: true,
    svg: '<path d="M24 8l13 5v11c0 8.5-5.6 15.6-13 18-7.4-2.4-13-9.5-13-18V13l13-5z" fill="#fecaca" stroke="#dc2626" stroke-width="2.2" stroke-linejoin="round"/><path d="M19 19l10 10M29 19L19 29" stroke="#991b1b" stroke-width="2.5" stroke-linecap="round"/>',
  },
  '11-1': {
    risk: false,
    svg: '<circle cx="24" cy="24" r="14" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M24 31V17M18 23l6-6 6 6" stroke="#008c2c" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
  },
  '11-2': {
    risk: true,
    svg: '<path d="M17 12v24M17 12l-5 5M17 12l5 5" stroke="#008c2c" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M31 36V12M31 36l-5-5M31 36l5-5" stroke="#dc2626" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
  },
  '13-0': {
    risk: true,
    svg: '<path d="M14 14l20 20M34 14L14 34" stroke="#dc2626" stroke-width="2.4" stroke-linecap="round"/><circle cx="24" cy="24" r="14" fill="#fecaca" fill-opacity="0.35" stroke="#dc2626" stroke-width="2"/>',
  },
  '13-1': {
    risk: false,
    svg: '<rect x="10" y="10" width="28" height="28" rx="4" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M16 24l5 5 11-11" stroke="#008c2c" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
  },
  '13-2': {
    risk: false,
    svg: '<path d="M12 16h24M12 24h24M12 32h16" stroke="#008c2c" stroke-width="2.4" stroke-linecap="round"/><circle cx="34" cy="32" r="4" fill="#86efac" stroke="#008c2c" stroke-width="2"/>',
  },
  '14-0': {
    risk: false,
    svg: '<rect x="10" y="24" width="6" height="13" rx="1.5" fill="#9ecbaa" stroke="#008c2c" stroke-width="1.8"/><rect x="21" y="17" width="6" height="20" rx="1.5" fill="#86efac" stroke="#008c2c" stroke-width="1.8"/><rect x="32" y="11" width="6" height="26" rx="1.5" fill="#008c2c"/>',
  },
  '14-1': {
    risk: true,
    svg: '<path d="M24 9l15 27H9L24 9z" fill="#fecaca" stroke="#dc2626" stroke-width="2.2" stroke-linejoin="round"/><path d="M24 19v7M24 30v1" stroke="#991b1b" stroke-width="2.5" stroke-linecap="round"/>',
  },
  '14-2': {
    risk: false,
    svg: '<circle cx="24" cy="24" r="14" fill="#bbf7d0" stroke="#008c2c" stroke-width="2.2"/><path d="M18 24l4 4 8-8" stroke="#008c2c" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
  },
}
const slide6RedFlagIcon = {
  risk: true,
  svg: '<path d="M13 10v28" stroke="#dc2626" stroke-width="2.6" stroke-linecap="round"/><path d="M13 12h22l-4.5 7 4.5 7H13V12z" fill="#fca5a5" stroke="#dc2626" stroke-width="2.2" stroke-linejoin="round"/>',
}
const slide6AssetRedIcon = {
  risk: true,
  svg: '<rect x="10" y="9" width="20" height="28" rx="3" fill="#fecaca" stroke="#dc2626" stroke-width="2.2"/><path d="M15 16h10M15 22h8" stroke="#dc2626" stroke-width="2" stroke-linecap="round"/><circle cx="31" cy="29" r="6" fill="#fef2f2" stroke="#dc2626" stroke-width="2.2"/><path d="M35.5 33.5L40 38" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round"/>',
}
const getPointIcon = (slideNum, index) => {
  if (props.slide.slide_num === 6) {
    if (isRestated.value) return slide6RedFlagIcon
    if (index === 0) return pointIcons['5-0']
    if (index === 1) return slide6AssetRedIcon
    if (index === 2) return pointIcons['5-1']
  }
  return pointIcons[`${slideNum}-${index}`] || null
}
const competitionChart = computed(() => props.slide.competition_chart)
const spendingChart = computed(() => props.slide.competitive_spending_chart)
const spendingScale = computed(() => Math.max(...(spendingChart.value?.series || []).map(row => row.value), 1) * 1.1)
const provisionScale = computed(() => Math.max(...(competitionChart.value?.series || []).map(row => row.value), 1) * 1.1)
const provisionGrowth = computed(() => {
  const rows = competitionChart.value?.series || []
  return rows.length === 2 && rows[0].value > 0 ? Math.round((rows[1].value / rows[0].value - 1) * 100) : null
})
</script>

<template>
  <div class="financial-slide" :aria-label="`${slide.slide_num}. ${title}`">
    <article class="slide-sheet" :class="{ 'slide-cover': slide.slide_num === 1, 'slide-appendix': slide.is_appendix, 'slide-has-table': table }">
      <template v-if="slide.slide_num === 1">
        <div class="slide-cover-top">
          <img class="slide-brand" src="/goto_logo.png" alt="GoTo" />
          <span>{{ label }}</span>
        </div>
        <div class="slide-cover-title">
          <p>PT GoTo Gojek Tokopedia Tbk</p>
          <h1>GoTo<span>{{ lang === 'id' ? 'Analisis ekuitas' : 'Equity analysis' }}</span></h1>
          <div class="slide-cover-business is-clickable-claim" role="button" tabindex="0" @click="emit('explain', $event, 'claim', slide.analysis_points?.[0] || { heading: 'Business Scope', text: lang === 'id' ? 'Gojek · GoTo Financial · 24,99% Tokopedia' : 'Gojek · GoTo Financial · 24.99% Tokopedia' })" @keydown.enter="emit('explain', $event, 'claim', slide.analysis_points?.[0] || { heading: 'Business Scope', text: lang === 'id' ? 'Gojek · GoTo Financial · 24,99% Tokopedia' : 'Gojek · GoTo Financial · 24.99% Tokopedia' })">{{ lang === 'id' ? 'Gojek · GoTo Financial · 24,99% Tokopedia' : 'Gojek · GoTo Financial · 24.99% Tokopedia' }}</div>
          <p class="slide-cover-question">{{ lang === 'id' ? 'Dari model bisnis hingga arus kas, valuasi, dan keputusan.' : 'From the business model to cash flow, value, and a decision.' }}</p>
        </div>
        <aside class="slide-cover-summary">
        <div class="slide-cover-user">
          <span>{{ lang === 'id' ? 'UNTUK SIAPA' : 'OUR USER' }}</span>
          <p>{{ lang === 'id' ? 'Investor saham publik jangka pendek' : 'Short-term public equity investor' }}</p>
        </div>
        <div
          class="slide-cover-verdict is-clickable-claim"
          role="button"
          tabindex="0"
          @click="emit('explain', $event, 'claim', slide.analysis_points?.[1])"
          @keydown.enter="emit('explain', $event, 'claim', slide.analysis_points?.[1])"
        >
          <span>{{ lang === 'id' ? 'HARGA ACUAN TUGAS' : 'ASSIGNMENT REFERENCE PRICE' }}</span>
          <strong class="slide-cover-investor-question">{{ lang === 'id' ? 'Rp 25 per saham' : 'Rp 25 per share' }}</strong>
          <p>{{ lang === 'id' ? 'Harga acuan tugas per saham' : 'Assignment reference price per share' }}</p>
        </div>
        <div class="slide-cover-reason">
          <span>{{ lang === 'id' ? 'CAKUPAN ANALISIS' : 'ANALYSIS SCOPE' }}</span>
          <p>{{ lang === 'id' ? 'Model bisnis, industri, hasil keuangan, kualitas akuntansi, proyeksi dan valuasi.' : 'Business model, industry, financial results, accounting quality, forecasts and valuation.' }}</p>
          <small>{{ lang === 'id' ? 'Aktual 2023–2025 · Proyeksi 2026–2028' : '2023–2025 actuals · 2026–2028 forecasts' }}</small>
        </div>
        </aside>
        <div class="slide-cover-team">
          <strong>GROUP 4</strong>
          <span>Fagly Ramschie · Anggreini Ruitan · Galatia Rompas</span>
          <span>Magister Manajemen, Universitas Klabat</span>
        </div>
      </template>

      <template v-else>
        <header class="slide-heading">
          <div class="slide-heading-copy">
            <p>{{ label }} <span v-if="slide.is_appendix"> / {{ lang === 'id' ? 'LAMPIRAN' : 'APPENDIX' }}</span></p>
            <h1>{{ title }}</h1>
          </div>
          <img class="slide-brand" src="/goto_logo.png" alt="GoTo" />
        </header>

        <div v-if="hasRestatement" class="slide-restatement-bar" :class="{ 'is-restated': isRestated }" @click.stop>
          <div class="restatement-pills" role="tablist" :aria-label="lang === 'id' ? 'Pilih versi data laporan' : 'Select report data version'">
            <button
              type="button"
              class="restatement-pill"
              :class="{ active: !isRestated }"
              @click="reportViewMode = 'original'"
            >
              {{ lang === 'id' ? 'Dek Awal (Tersubmit)' : 'Original Deck' }}
            </button>
            <button
              type="button"
              class="restatement-pill"
              :class="{ active: isRestated }"
              @click="reportViewMode = 'restated'; if (forecastScenario === 'base_2yr') forecastScenario = 'base'"
            >
              {{ lang === 'id' ? 'Laporan Akhir (Restated)' : 'Final Report (Restated)' }}
            </button>
          </div>
          <span class="restatement-delta">
            <strong>{{ isRestated ? (lang === 'id' ? 'Apa yang Direvisi:' : 'Final Report Fix:') : (lang === 'id' ? 'Catatan Revisi:' : 'Paper Update:') }}</strong>
            {{ restatementSummary }}
          </span>
        </div>

        <main class="slide-evidence-layout" :class="{ 'slide-table-only': slide.is_appendix, 'slide-business-layout': layoutSlide === 2, 'has-restatement-bar': hasRestatement }">
          <div class="slide-evidence" :class="{ 'slide-evidence-stacked': slideBannerUrl, 'slide-evidence-peer': slide.peer_exclusions, 'slide-evidence-competition': competitionChart, 'slide-evidence-explained': slide.loss_chart || slide.valuation_range }">
            <button
              v-if="slideBannerUrl"
              class="slide-evidence-banner"
              @click="emit('zoom', slideBannerUrl, title)"
              :aria-label="lang === 'id' ? 'Perbesar visual' : 'Enlarge visual'"
            >
              <img :src="slideBannerUrl" :alt="title" />
            </button>
            <template v-if="slide.five_forces">
            <table class="slide-forces-table">
              <thead><tr><th>{{ lang === 'id' ? 'Kekuatan' : 'Force' }}</th><th>{{ lang === 'id' ? 'Penilaian' : 'Rating' }}</th><th>{{ lang === 'id' ? 'Dasar penilaian' : 'Basis for assessment' }}</th></tr></thead>
              <tbody :key="tableAnimKey">
                <tr
                  v-for="(row, index) in slide.five_forces"
                  :key="index"
                  class="is-clickable-row"
                  :style="{ animationDelay: `${index * 55}ms` }"
                  tabindex="0"
                  @click="emit('explain', $event, 'five_force', row)"
                  @keydown.enter="emit('explain', $event, 'five_force', row)"
                >
                  <td
                    v-for="(cell, c) in row"
                    :key="c"
                    :class="c === 1 ? (/high|tinggi/i.test(cell) ? 'rating-bad' : /medium|sedang/i.test(cell) ? 'rating-mid' : '') : ''"
                  >{{ cell }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="competitionChart" class="slide-competition-charts">
            <figure
              v-if="spendingChart"
              class="slide-provision-chart slide-spending-chart"
              role="button"
              tabindex="0"
              :aria-label="lang === 'id' ? 'Belanja 2025: pemasaran Rp 3,09 triliun dan pengembangan produk Rp 2,15 triliun.' : '2025 spending: marketing Rp 3.09 trillion and product development Rp 2.15 trillion.'"
              @click="emit('explain', $event, 'claim', slide.analysis_points?.[0])"
              @keydown.enter="emit('explain', $event, 'claim', slide.analysis_points?.[0])"
              @keydown.space.prevent="emit('explain', $event, 'claim', slide.analysis_points?.[0])"
            >
              <figcaption><div><strong>{{ lang === 'id' ? 'Belanja untuk bersaing' : 'Spending to compete' }}</strong><span>{{ lang === 'id' ? '2025 · Rp triliun' : '2025 · Rp trillion' }}</span></div></figcaption>
              <dl>
                <div v-for="(row, i) in spendingChart.series" :key="row.key" class="slide-spending-row">
                  <dt>{{ lang === 'id' ? row.label_id : row.label }}</dt>
                  <dd class="slide-provision-value">{{ row.value.toLocaleString(lang === 'id' ? 'id-ID' : 'en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</dd>
                  <dd class="slide-provision-track"><span :class="{ 'slide-spending-product': i === 1, 'slide-provision-current': i === 0 }" :style="{ width: `${row.value / spendingScale * 100}%` }"></span></dd>
                </div>
              </dl>
            </figure>
            <figure
              v-if="competitionChart"
              class="slide-provision-chart"
              role="button"
              tabindex="0"
              :aria-label="`${lang === 'id' ? 'Provisi kerugian kredit' : 'Credit-loss provisions'}: ${competitionChart.series.map(row => `${row.period}: Rp ${row.value} ${lang === 'id' ? 'miliar' : 'billion'}`).join('; ')}`"
              @click="emit('explain', $event, 'claim', slide.analysis_points?.[2])"
              @keydown.enter="emit('explain', $event, 'claim', slide.analysis_points?.[2])"
              @keydown.space.prevent="emit('explain', $event, 'claim', slide.analysis_points?.[2])"
            >
              <figcaption>
                <div><strong>{{ lang === 'id' ? 'Provisi kerugian kredit' : 'Credit-loss provisions' }}</strong><span>{{ lang === 'id' ? 'Rp miliar' : 'Rp billion' }}</span></div>
                <span class="slide-provision-growth">+{{ provisionGrowth }}% {{ lang === 'id' ? 'tahunan' : 'YoY' }}</span>
              </figcaption>
              <dl>
                <div v-for="(row, i) in competitionChart.series" :key="row.period" class="slide-provision-row">
                  <dt>{{ row.period }}</dt>
                  <dd class="slide-provision-track"><span :class="{ 'slide-provision-current': i === competitionChart.series.length - 1 }" :style="{ width: `${row.value / provisionScale * 100}%` }"></span></dd>
                  <dd class="slide-provision-value">{{ row.value }}</dd>
                </div>
              </dl>
              <p v-if="competitionChart.consumer_loans_bn" class="slide-provision-note">{{ lang === 'id' ? 'Pinjaman konsumen 2025:' : '2025 consumer loans:' }} Rp {{ (competitionChart.consumer_loans_bn / 1000).toLocaleString(lang === 'id' ? 'id-ID' : 'en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}T</p>
              <p v-if="competitionChart.formula" class="slide-chart-formula">{{ competitionChart.formula }}</p>
            </figure>
            </div>
            </template>
            <div v-else-if="editorialRows" :key="tableAnimKey" class="slide-editorial-rows">
              <div
                v-for="(row, index) in editorialRows"
                :key="index"
                class="slide-editorial-row is-clickable-row"
                :style="{ animationDelay: `${index * 60}ms` }"
                role="button"
                tabindex="0"
                @click="emit('explain', $event, 'editorial', row)"
                @keydown.enter="emit('explain', $event, 'editorial', row)"
              >
                <div class="slide-editorial-left">
                  <img
                    v-if="row.img"
                    :src="row.img"
                    :alt="row.name"
                    class="slide-editorial-thumb"
                    @click.stop="emit('zoom', row.img, row.name)"
                  />
                  <div>
                    <h2>{{ row.name }}</h2>
                    <small v-if="getInlineAbbrHint(row.name, lang)" class="slide-abbr-sub">{{ getInlineAbbrHint(row.name, lang) }}</small>
                    <p v-if="row.text && row.text.includes('\n')">
                      <em class="slide-editorial-formula">{{ row.text.split('\n')[0] }}</em>
                      <span class="slide-editorial-calc">{{ row.text.split('\n').slice(1).join('\n') }}</span>
                    </p>
                    <p v-else>{{ row.text }}</p>
                  </div>
                </div>
                <strong>{{ row.value }}</strong>
              </div>
            </div>
            <template v-else-if="table">
              <div class="slide-table-stack">
                <div v-if="isForecastSlide" class="slide-scenario-bar" @click.stop>
                  <span class="slide-scenario-label">{{ lang === 'id' ? 'Skenario:' : 'Scenario:' }}</span>
                  <select v-model="forecastScenario" class="slide-scenario-select" aria-label="Select forecast scenario">
                    <option value="base">{{ isRestated ? (lang === 'id' ? 'Base (Pasca-Tokopedia 2024–2025)' : 'Base (Post-Tokopedia 2024–2025)') : (lang === 'id' ? 'Base (Rata-rata 3 Thn)' : 'Base (3-Yr Avg)') }}</option>
                    <option v-if="!isRestated" value="base_2yr">{{ lang === 'id' ? 'Base (Rata-rata 2 Thn: 2024–2025)' : 'Base (2-Yr Avg: 2024–2025)' }}</option>
                    <option value="optimistic">{{ isRestated ? (lang === 'id' ? 'Optimistis (OpEx 1H 2026: 51,2%)' : 'Optimistic (1H 2026 OpEx: 51.2%)') : 'Optimistic' }}</option>
                    <option value="conservative">{{ isRestated ? (lang === 'id' ? 'Konservatif (Lantai 2024: 62,8%)' : 'Conservative (2024 Floor: 62.8%)') : 'Conservative' }}</option>
                  </select>
                </div>
                <div v-if="isDcfRiSlide && !isRestated" class="slide-scenario-bar" @click.stop>
                  <span class="slide-scenario-label">{{ lang === 'id' ? 'Basis Proyeksi:' : 'Base Basis:' }}</span>
                  <select v-model="valuationBasis" class="slide-scenario-select" aria-label="Select valuation base basis">
                    <option value="3yr">{{ lang === 'id' ? 'Rata-rata 3 Tahun (2023–2025)' : '3-Yr Avg (2023–2025)' }}</option>
                    <option value="2yr">{{ lang === 'id' ? 'Rata-rata 2 Tahun (2024–2025)' : '2-Yr Avg (2024–2025)' }}</option>
                  </select>
                </div>
                <div v-if="slide.is_appendix && table.title" class="slide-appendix-schedule">
                  <h3>{{ table.title }}</h3>
                </div>
                <table
                  class="slide-financial-table"
                  :class="{
                    'slide-table-dense': slide.is_appendix,
                    'slide-table-ratios': isRestated && slide.slide_num === 4,
                    'slide-table-wacc': !slide.is_appendix && layoutSlide === 7,
                    'slide-table-multiples': !slide.is_appendix && layoutSlide === 9,
                    'slide-table-restatement': !slide.is_appendix && (layoutSlide === 13 || layoutSlide === 14),
                  }"
                >
                  <thead><tr><th v-for="(cell, i) in visibleHeaders" :key="i">{{ cell }}</th></tr></thead>
                  <tbody :key="tableAnimKey">
                    <tr
                      v-for="(row, r) in visibleRows"
                      :key="r"
                      :style="{ animationDelay: `${r * 55}ms` }"
                      @click="isRestated ? emit('explain', $event, 'claim', restatedRowDetail(row)) : emit('explain', $event, 'row', table.rows[r])"
                      @dblclick="isRestated ? emit('evidence', 'claim', restatedRowDetail(row)) : emit('evidence', 'row', table.rows[r])"
                      tabindex="0"
                      @keydown.enter="isRestated ? emit('explain', $event, 'claim', restatedRowDetail(row)) : emit('explain', $event, 'row', table.rows[r])"
                    >
                      <td
                        v-for="(cell, c) in row"
                        :key="c"
                        :class="c === 1 ? (/high|tinggi/i.test(cell) ? 'rating-bad' : /medium|sedang/i.test(cell) ? 'rating-mid' : '') : ''"
                      >
                        <span>{{ cell }}</span>
                        <small v-if="c === 0 && !slide.is_appendix && getInlineAbbrHint(cell, lang)" class="slide-abbr-sub">{{ getInlineAbbrHint(cell, lang) }}</small>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p v-if="slide.is_appendix && table.note" class="slide-appendix-note">{{ table.note }}</p>
              <template v-if="slide.is_appendix && slide.supporting_schedules?.length">
                <div v-for="(sched, sIdx) in slide.supporting_schedules" :key="'apx-sched-'+sIdx" class="slide-appendix-schedule">
                  <h3>{{ sched.title }}</h3>
                  <table class="slide-financial-table slide-table-dense">
                    <thead><tr><th v-for="(cell, i) in sched.headers" :key="i">{{ cell }}</th></tr></thead>
                    <tbody :key="tableAnimKey + '-' + sIdx">
                      <tr
                        v-for="(row, r) in sched.rows"
                        :key="r"
                        :style="{ animationDelay: `${r * 55}ms` }"
                        @click="emit('explain', $event, 'claim', slide.analysis_points?.[0] || { heading: sched.title, text: row.join(' | ') })"
                        tabindex="0"
                        @keydown.enter="emit('explain', $event, 'claim', slide.analysis_points?.[0] || { heading: sched.title, text: row.join(' | ') })"
                      >
                        <td v-for="(cell, c) in row" :key="c">{{ cell }}</td>
                      </tr>
                    </tbody>
                  </table>
                  <p v-if="sched.note" class="slide-appendix-note">{{ sched.note }}</p>
                </div>
              </template>
            </template>
            <button v-else-if="slide.chart_url" class="slide-chart" @click="emit('zoom', slide.chart_url, title)" :aria-label="lang === 'id' ? 'Perbesar grafik' : 'Enlarge chart'">
              <img :src="slide.chart_url" :alt="slide.title" />
            </button>
            <div v-if="slide.loss_chart" :class="{ 'slide-loss-grid': Boolean(slide.chart_url) }">
              <figure class="slide-story-chart" role="button" tabindex="0" :aria-label="slide.loss_chart.title" @click="emit('explain', $event, 'claim', visibleAnalysisPoints[0])" @keydown.enter="emit('explain', $event, 'claim', visibleAnalysisPoints[0])" @keydown.space.prevent="emit('explain', $event, 'claim', visibleAnalysisPoints[0])">
                <figcaption>{{ slide.loss_chart.title }}</figcaption>
                <div v-for="row in slide.loss_chart.series" :key="row.label" class="slide-loss-row">
                  <span>{{ row.label }}</span>
                  <div class="slide-provision-track"><span class="slide-provision-current" :style="{ width: `${Math.abs(row.value) / lossScale * 100}%` }"></span></div>
                  <strong>−{{ Math.abs(row.value).toLocaleString(lang === 'id' ? 'id-ID' : 'en-US') }}</strong>
                </div>
                <p v-if="slide.chart_formula" class="slide-chart-formula">{{ slide.chart_formula }}</p>
              </figure>
              <button v-if="slide.chart_url" class="slide-chart slide-loss-chart-btn" @click="emit('zoom', slide.chart_url, title)" :aria-label="lang === 'id' ? 'Perbesar grafik' : 'Enlarge chart'">
                <img :src="slide.chart_url" :alt="slide.title" />
              </button>
            </div>
            <figure v-if="slide.valuation_range" class="slide-story-chart slide-range-chart">
              <figcaption class="slide-range-hdr">
                <span>{{ lang === 'id' ? 'Hasil Valuasi (Rp/saham)' : 'Valuation Results (Rp/share)' }}</span>
                <select v-if="isGrabSlide && !isRestated" v-model="valuationBasis" class="slide-scenario-select" aria-label="Select valuation base basis" @click.stop>
                  <option value="3yr">{{ lang === 'id' ? '3-Thn (2023–2025)' : '3-Yr Avg (2023–2025)' }}</option>
                  <option value="2yr">{{ lang === 'id' ? '2-Thn (2024–2025)' : '2-Yr Avg (2024–2025)' }}</option>
                </select>
              </figcaption>
              <svg viewBox="0 0 560 176" role="img" :aria-label="isRestated ? (lang === 'id' ? 'DCF plus 10,4; RI minus 12,2; P/B Grab 91,0; acuan 25 rupiah per saham.' : 'DCF plus 10.4; RI minus 12.2; Grab P/B 91.0; reference price 25 rupiah per share.') : (lang === 'id' ? 'DCF minus 121,1; RI minus 75,1; P/B Grab 91,0; acuan 25 rupiah per saham.' : 'DCF minus 121.1; RI minus 75.1; Grab P/B 91.0; reference price 25 rupiah per share.')">
                <line :x1="rangeX(0)" :x2="rangeX(0)" y1="20" y2="148" stroke="#a4bfae" />
                <line :x1="rangeX(25)" :x2="rangeX(25)" y1="20" y2="148" stroke="#173d25" stroke-dasharray="4 4" />
                <text :x="rangeX(25)" y="13" text-anchor="middle" fill="#526a59" font-size="12">{{ lang === 'id' ? 'Acuan Rp25' : 'Ref. Rp25' }}</text>
                <g v-for="(row,i) in visibleValuationRange" :key="row.label">
                  <text x="0" :y="40+i*40" fill="#173d25" font-size="14.5" font-weight="650">{{ row.label }}</text>
                  <text v-if="getInlineAbbrHint(row.label, lang)" x="0" :y="53+i*40" fill="#5a7363" font-size="10">{{ getInlineAbbrHint(row.label, lang).replace(' (Economic Profit)', '').replace(' (Laba Ekonomi)', '') }}</text>
                  <rect :x="Math.min(rangeX(row.value),rangeX(0))" :y="28+i*40" :width="Math.abs(rangeX(row.value)-rangeX(0))" height="22" :fill="row.value < 0 ? '#a8cdb3' : '#008c2c'" />
                  <text x="554" :y="44+i*40" text-anchor="end" fill="#173d25" font-size="15" font-weight="650">{{ row.value > 0 ? '+' : '−' }}{{ Math.abs(row.value).toFixed(1) }}</text>
                </g>
                <text :x="rangeX(-140)" y="166" fill="#63786a" font-size="12">−140</text>
                <text :x="rangeX(0)" y="166" text-anchor="middle" fill="#63786a" font-size="12">0</text>
                <text :x="rangeX(120)" y="166" text-anchor="end" fill="#63786a" font-size="12">+120 Rp/share</text>
              </svg>
              <p v-if="isRestated && isGrabSlide" class="slide-chart-formula">{{ lang === 'id' ? 'Rentang Nilai Wajar: Base DCF (+Rp10,38) – Opt. RI (+Rp16,75) · Kas Bersih Rp13,19/sh vs Harga Pasar Rp25,00' : 'Defensible Range: Base DCF (+Rp10.38) – Opt. RI (+Rp16.75) · Net Cash Rp13.19/sh vs Market Rp25.00' }}</p>
              <p v-else-if="slide.chart_formula" class="slide-chart-formula">{{ slide.chart_formula }}</p>
            </figure>
            <section v-if="slide.peer_exclusions" class="slide-peer-exclusions">
              <h2>{{ lang === 'id' ? 'Mengapa pembanding lain dikeluarkan?' : 'Why the other companies are excluded' }}</h2>
              <div
                v-for="peer in slide.peer_exclusions"
                :key="peer.company"
                class="slide-peer-exclusion is-clickable-row"
                role="button"
                tabindex="0"
                @click="emit('explain', $event, 'peer_exclusion', peer)"
                @keydown.enter="emit('explain', $event, 'peer_exclusion', peer)"
              >
                <strong>{{ peer.company }}</strong><p>{{ peer.reason }}</p>
              </div>
            </section>
          </div>

          <aside v-if="!slide.is_appendix" class="slide-key-figures" :class="{ 'slide-analysis-panel': slide.analysis_points?.length }">
            <template v-if="visibleAnalysisPoints.length">
              <div
                v-for="(point, i) in visibleAnalysisPoints"
                :key="i"
                class="slide-analysis-point is-clickable-claim"
                :class="{ 'has-point-icon': layoutSlide === 2 || Boolean(getPointIcon(layoutSlide, i)) }"
                role="button"
                tabindex="0"
                @click="emit('explain', $event, 'claim', point)"
                @keydown.enter="emit('explain', $event, 'claim', point)"
              >
                <div v-if="layoutSlide === 2 && i < 2" class="slide-point-icon" aria-hidden="true">
                  <img v-if="i === 0" src="/visuals/point_revenue.png" alt="" />
                  <img v-else src="/visuals/point_competition.png" alt="" />
                </div>
                <div
                  v-else-if="getPointIcon(layoutSlide, i)"
                  class="slide-point-icon"
                  :class="{ 'is-risk-icon': getPointIcon(layoutSlide, i).risk }"
                  aria-hidden="true"
                >
                  <svg viewBox="0 0 48 48" fill="none" class="slide-point-svg" v-html="getPointIcon(layoutSlide, i).svg"></svg>
                </div>
                <div class="slide-point-copy">
                  <h2>{{ point.heading }}</h2>
                  <p>{{ point.text }}</p>
                </div>
              </div>
            </template>
            <template v-else>
              <button v-for="(k, i) in slide.kpis" :key="i" class="slide-key-figure" @click="emit('explain', $event, 'kpi', k)" @dblclick="emit('evidence', 'kpi', k)">
                <span>{{ k.label }}</span><strong>{{ k.val }}</strong><small>{{ k.sub }}</small>
              </button>
              <p
                class="slide-takeaway is-clickable-claim"
                role="button"
                tabindex="0"
                @click="emit('explain', $event, 'verdict', { title: title, text: takeaway })"
                @keydown.enter="emit('explain', $event, 'verdict', { title: title, text: takeaway })"
              >{{ takeaway }}</p>
            </template>
          </aside>
        </main>
      </template>

      <footer class="slide-footline">
        <span>{{ slide.slide_num === 1 ? 'IDX: GOTO' : 'GROUP 4   /   IDX: GOTO' }}</span>
        <span class="slide-source">{{ slide.source_footer }}</span>
        <div class="slide-foot-right" @click.stop>
          <button
            v-if="appendixTarget"
            type="button"
            class="slide-apx-jump"
            @click="emit('jump-slide', appendixTarget.slideNum)"
            :title="lang === 'id' ? `Lompat ke Appendix ${appendixTarget.code}` : `Jump to Appendix ${appendixTarget.code}`"
          >
            <span>Appendix {{ appendixTarget.code }}</span>
            <svg class="slide-apx-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M7 17 17 7" /><path d="M7 7h10v10" />
            </svg>
          </button>
          <template v-else-if="slide.is_appendix">
            <button
              type="button"
              class="slide-apx-jump is-back"
              @click="emit('jump-slide', backSlideNum || 12)"
            >
              <svg class="slide-apx-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="m15 18-6-6 6-6" />
              </svg>
              <span>{{ lang === 'id' ? `Kembali ke Slide ${backSlideNum || 12}` : `Back to Slide ${backSlideNum || 12}` }}</span>
            </button>
            <div class="slide-apx-mini-nav" role="navigation" aria-label="Appendix quick jump">
              <button
                v-for="apx in appendixList"
                :key="apx.code"
                type="button"
                class="slide-apx-dot"
                :class="{ active: slide.slide_num === apx.slideNum }"
                @click="emit('jump-slide', apx.slideNum)"
              >
                {{ apx.code }}
              </button>
            </div>
          </template>
          <span class="slide-folio">{{ String(slide.slide_num).padStart(2, '0') }} / {{ total }}</span>
        </div>
      </footer>
    </article>
  </div>
</template>

<style scoped>
.financial-slide { width: 100%; min-width: 0; container-type: inline-size; flex: 1; }
.slide-sheet { position: relative; width: 100%; aspect-ratio: 16 / 9; overflow: hidden; background: linear-gradient(135deg, #007222 0%, #005419 100%); color: white; font-family: 'Plus Jakarta Sans', sans-serif; box-shadow: 0 16px 48px #0002; }
.slide-sheet *, .slide-sheet *::before, .slide-sheet *::after { box-sizing: border-box; }
.slide-brand { display: block; width: 8cqw; height: 4.6cqw; object-fit: contain; background: white; padding: .75cqw 1cqw; border-radius: 0; flex-shrink: 0; }
.slide-heading { position: absolute; top: 4.4%; left: 4%; right: 4%; display: flex; justify-content: space-between; gap: 3cqw; align-items: flex-start; }
.slide-heading-copy { max-width: 76cqw; }
.slide-heading p { margin: 0 0 .9cqw; font-size: .85cqw; letter-spacing: .16cqw; color: #c5f1cb; font-weight: 600; }
.slide-heading h1 { margin: 0; color: white; font-size: 2.75cqw; line-height: 1.2; letter-spacing: -.09cqw; font-weight: 750; }
.slide-restatement-bar { position: absolute; top: 16.5%; left: 4%; right: 4%; display: flex; align-items: center; justify-content: space-between; gap: 1.3cqw; background: linear-gradient(135deg, rgba(48, 32, 8, 0.46), rgba(28, 20, 6, 0.36)); backdrop-filter: blur(18px) saturate(165%); -webkit-backdrop-filter: blur(18px) saturate(165%); border: 1px solid rgba(251, 191, 36, 0.44); border-radius: .75cqw; padding: .52cqw .85cqw; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.24); z-index: 2; }
.slide-restatement-bar.is-restated { background: linear-gradient(135deg, rgba(12, 54, 28, 0.56), rgba(8, 36, 19, 0.44)); border-color: rgba(134, 239, 172, 0.48); color: #eefaf2; box-shadow: 0 10px 28px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.26); }
.restatement-pills { display: inline-flex; align-items: center; gap: .35cqw; background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(255, 255, 255, 0.16); padding: .28cqw; border-radius: .55cqw; flex-shrink: 0; }
.slide-restatement-bar.is-restated .restatement-pills { background: rgba(0, 0, 0, 0.28); border-color: rgba(134, 239, 172, 0.22); }
.restatement-pill { border: 0; background: transparent; color: rgba(235, 250, 240, 0.86); font: inherit; font-size: 1.02cqw; font-weight: 700; padding: .46cqw 1.05cqw; border-radius: .42cqw; cursor: pointer; white-space: nowrap; transition: background-color .16s ease, color .16s ease, box-shadow .16s ease; }
.restatement-pill:hover { background: rgba(255, 255, 255, 0.12); color: #ffffff; }
.slide-restatement-bar.is-restated .restatement-pill { color: rgba(224, 247, 232, 0.86); }
.restatement-pill.active { background: linear-gradient(135deg, rgba(245, 158, 11, 0.92), rgba(217, 119, 6, 0.92)); color: #ffffff; box-shadow: 0 3px 12px rgba(245, 158, 11, 0.34), inset 0 1px 0 rgba(255, 255, 255, 0.34); }
.slide-restatement-bar.is-restated .restatement-pill.active { background: linear-gradient(135deg, rgba(34, 197, 94, 0.92), rgba(22, 163, 74, 0.92)); color: #ffffff; box-shadow: 0 3px 12px rgba(34, 197, 94, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.35); }
.restatement-delta { flex: 1; min-width: 0; font-size: .96cqw; line-height: 1.35; color: #eefaf2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.restatement-delta strong { color: #fde68a; margin-right: .4cqw; font-weight: 750; }
.slide-restatement-bar.is-restated .restatement-delta { color: #eefaf2; }
.slide-restatement-bar.is-restated .restatement-delta strong { color: #fde68a; }
.slide-evidence-layout { position: absolute; top: 25%; left: 4%; right: 4%; bottom: 10%; display: grid; grid-template-columns: 1.65fr 1fr; gap: 3cqw; align-items: stretch; }
.slide-evidence-layout.has-restatement-bar { top: 27.6%; bottom: 9.6%; }
.slide-evidence-layout.has-restatement-bar .slide-evidence.slide-evidence-peer { padding: .85cqw 1.1cqw; gap: .55cqw; }
.slide-evidence-layout.has-restatement-bar .slide-evidence-peer .slide-financial-table th,
.slide-evidence-layout.has-restatement-bar .slide-evidence-peer .slide-financial-table td { padding: .42cqw .55cqw; }
.slide-evidence-layout.has-restatement-bar .slide-peer-exclusion { padding: .38cqw 0; font-size: .86cqw; }
.slide-evidence-layout.has-restatement-bar .slide-editorial-row h2 { font-size: 1.35cqw; margin-bottom: .35cqw; }
.slide-evidence-layout.has-restatement-bar .slide-editorial-row p { font-size: .96cqw; line-height: 1.38; max-width: 30cqw; }
.slide-evidence-layout.has-restatement-bar .slide-analysis-panel .slide-analysis-point p { font-size: 1.04cqw; line-height: 1.44; }
.slide-evidence { background: #fff; color: #172e21; overflow: hidden; min-width: 0; display: flex; align-items: center; padding: 1cqw; }
.slide-evidence.slide-evidence-explained { flex-direction: column; align-items: stretch; justify-content: space-between; padding: .75cqw 1.2cqw; gap: .4cqw; }
.slide-evidence.slide-evidence-explained .slide-financial-table th { padding: .52cqw .65cqw; }
.slide-evidence.slide-evidence-explained .slide-financial-table td { padding: .48cqw .65cqw; line-height: 1.28; }
.slide-evidence.slide-evidence-explained .slide-abbr-sub { font-size: .62cqw; line-height: 1.15; margin-top: .04cqw; }
.slide-story-chart { margin: 0; padding-top: .75cqw; border-top: 1px solid #dce8df; }
.slide-story-chart figcaption { font-size: .94cqw; color: #173d25; font-weight: 650; margin-bottom: .65cqw; line-height: 1.35; }
.slide-chart-formula { color: #526a59; font-size: .76cqw; line-height: 1.45; margin: .35cqw 0 0; overflow-wrap: anywhere; }
.slide-loss-row { display: grid; grid-template-columns: 3.2cqw 1fr 5cqw; align-items: center; gap: .8cqw; margin-top: .8cqw; font-size: .95cqw; }
.slide-loss-row strong { text-align: right; font-variant-numeric: tabular-nums; }
.slide-loss-row .slide-provision-track { height: 1cqw; }
.slide-range-chart figcaption.slide-range-hdr { display: flex; align-items: center; justify-content: space-between; gap: .8cqw; }
.slide-range-hdr .slide-scenario-select { padding: .15cqw .5cqw; font-size: .78cqw; }
.slide-range-chart svg { display: block; width: 100%; height: auto; }
.slide-evidence.slide-evidence-peer { display: flex; flex-direction: column; align-items: stretch; justify-content: space-between; gap: 1cqw; padding: 1.2cqw; }
.slide-evidence-peer .slide-financial-table { font-size: .86cqw; line-height: 1.3; }
.slide-evidence-peer .slide-financial-table th { font-size: .8cqw; padding: .6cqw; }
.slide-evidence-peer .slide-financial-table td { padding: .55cqw .6cqw; }
.slide-peer-exclusions { border-top: 2px solid #008c2c; padding-top: .7cqw; }
.slide-peer-exclusions h2 { color: #008c2c; font-size: 1.05cqw; margin: 0 0 .5cqw; }
.slide-peer-exclusion { display: grid; grid-template-columns: 8cqw 1fr; gap: .8cqw; border-top: 1px solid #e3ece6; padding: .55cqw 0; font-size: .91cqw; line-height: 1.4; }
.slide-peer-exclusion strong { color: #173d25; }
.slide-peer-exclusion p { margin: 0; color: #526a59; }
.slide-evidence-stacked { flex-direction: column; justify-content: flex-start; align-items: stretch; padding: .65cqw .95cqw; gap: .28cqw; }
.slide-evidence-banner { display: block; width: 100%; height: 9.4cqw; padding: 0 0 .3cqw; border: 0; border-bottom: 1px solid #dce8df; background: #fff; cursor: zoom-in; flex-shrink: 0; }
.slide-evidence-banner img { width: 100%; height: 100%; display: block; object-fit: contain; }
.slide-evidence.slide-evidence-competition { flex-direction: column; align-items: stretch; justify-content: space-between; padding: 1.4cqw; gap: 1.7cqw; }
.slide-evidence-competition .slide-forces-table { flex-shrink: 0; }
.slide-competition-charts { display: grid; grid-template-columns: 1fr 1fr; gap: 1.8cqw; padding: 1.3cqw .3cqw .3cqw; border-top: 1px solid #dce8df; }
.slide-provision-chart { min-width: 0; margin: 0; padding: 0; cursor: pointer; }
.slide-competition-charts > figure + figure { border-left: 1px solid #dce8df; padding-left: 1.5cqw; }
.slide-provision-chart figcaption { display: flex; justify-content: space-between; align-items: baseline; gap: 1cqw; margin-bottom: 1.2cqw; }
.slide-provision-chart figcaption strong { display: block; font-size: .95cqw; line-height: 1.35; font-weight: 650; color: #173d25; }
.slide-provision-chart figcaption div > span { display: block; margin-top: .25cqw; color: #63786a; font-size: .79cqw; }
.slide-provision-growth { white-space: nowrap; color: #008c2c; font-size: .83cqw; font-weight: 750; }
.slide-provision-chart dl { margin: 0; display: grid; gap: 1cqw; }
.slide-provision-row { display: grid; grid-template-columns: 2.8cqw 1fr 2.5cqw; align-items: center; gap: .6cqw; }
.slide-provision-row dt { color: #526a59; font-size: .96cqw; }
.slide-provision-row dd { margin: 0; }
.slide-provision-track { height: 1.25cqw; background: #edf6ef; }
.slide-provision-track > span { display: block; height: 100%; background: #9ecbaa; }
.slide-provision-track > span.slide-provision-current { background: #008c2c; }
.slide-provision-track > span.slide-spending-product { background: #173d25; }
.slide-provision-value { text-align: right; color: #173d25; font-size: 1.15cqw; font-weight: 700; font-variant-numeric: tabular-nums; }
.slide-spending-row { display: grid; grid-template-columns: 1fr auto; column-gap: .7cqw; row-gap: .35cqw; align-items: baseline; }
.slide-spending-row dt { font-size: .88cqw; line-height: 1.4; color: #526a59; }
.slide-spending-row .slide-provision-track { grid-column: 1 / -1; height: .85cqw; }
.slide-provision-note { font-size: .76cqw; line-height: 1.4; margin: 1cqw 0 0; color: #63786a; }
.slide-provision-chart:hover { background: #f7faf7; }
.slide-provision-chart:focus-visible { outline: 2px solid #008c2c; outline-offset: 4px; }
.slide-editorial-rows { width: 100%; height: 100%; display: grid; grid-template-rows: repeat(3, 1fr); padding: 0 1.2cqw; }
.slide-editorial-row { display: flex; align-items: center; justify-content: space-between; gap: 1.4cqw; border-bottom: 1px solid #dce8df; }
.slide-editorial-left { display: flex; align-items: center; gap: 1.3cqw; min-width: 0; }
.slide-editorial-thumb { width: 8.2cqw; height: 6.4cqw; object-fit: cover; border-radius: .5cqw; border: 1px solid #dce8df; flex-shrink: 0; cursor: zoom-in; background: #edf6ef; }
.slide-editorial-row:last-child { border: 0; }
.slide-editorial-row h2 { font-size: 1.45cqw; color: #173d25; line-height: 1.3; margin: 0 0 .5cqw; }
.slide-editorial-row p { font-size: 1.05cqw; line-height: 1.45; color: #63786a; margin: 0; max-width: 28cqw; white-space: pre-line; }
.slide-editorial-formula { display: block; font-style: italic; }
.slide-editorial-calc { display: block; font-style: normal; }
.slide-editorial-row strong { flex-shrink: 0; font-size: 1.75cqw; font-weight: 750; color: #008c2c; letter-spacing: -.07cqw; }
.slide-chart { display: block; width: 100%; height: 100%; padding: 0; border: 0; background: white; cursor: zoom-in; }
.slide-chart img { width: 100%; height: 100%; display: block; object-fit: contain; }
.slide-loss-grid { display: grid; grid-template-columns: 1fr 1.15fr; gap: 1cqw; align-items: center; margin-top: .8cqw; }
.slide-loss-grid .slide-story-chart { margin-top: 0; }
.slide-loss-chart-btn { height: auto; max-height: 11.5cqw; border-radius: .5cqw; border: 1px solid #dce8df; overflow: hidden; padding: .2cqw; }
.slide-loss-chart-btn img { max-height: 11cqw; width: 100%; object-fit: contain; }
.slide-key-figures { min-height: 0; display: flex; flex-direction: column; justify-content: space-between; }
.slide-analysis-point + .slide-analysis-point { border-top: 1px solid #ffffff40; padding-top: 1.15cqw; }
.slide-analysis-point.has-point-icon { display: flex; align-items: flex-start; gap: 1cqw; }
.slide-point-icon { width: 4.2cqw; height: 4.2cqw; flex-shrink: 0; border-radius: .55cqw; background: #edf6ef; border: 1px solid #ffffff85; overflow: hidden; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.14); }
.slide-point-icon.is-risk-icon { background: #fef2f2; border-color: #fecaca; }
.slide-forces-table td.rating-bad { color: #dc2626; }
.slide-forces-table td.rating-mid { color: #b45309; }
.slide-point-icon img { width: 100%; height: 100%; object-fit: cover; display: block; }
.slide-point-icon .slide-point-svg { width: 80%; height: 80%; display: block; }
.slide-point-copy { min-width: 0; flex: 1; }
.slide-analysis-point h2 { color: #fff; font-size: 1.18cqw; line-height: 1.35; margin: 0 0 .6cqw; font-weight: 750; }
.slide-analysis-point p { color: #e7f5ea; font-size: 1.02cqw; line-height: 1.55; margin: 0; }
.slide-business-layout { grid-template-columns: 1.35fr 1fr; gap: 2cqw; }
.slide-analysis-panel { background: transparent; color: #ffffff; padding: .35cqw 1.3cqw .8cqw; gap: .6cqw; }
.slide-analysis-panel .slide-analysis-point { min-width: 0; border-radius: 0; }
.slide-analysis-panel .slide-analysis-point + .slide-analysis-point { border-color: #ffffff35; padding-top: .65cqw; }
.slide-analysis-panel .slide-analysis-point.has-point-icon { display: grid; grid-template-columns: 2.4cqw minmax(0, 1fr); column-gap: .75cqw; row-gap: .5cqw; align-items: center; }
.slide-analysis-panel .has-point-icon .slide-point-copy { display: contents; }
.slide-analysis-panel .slide-point-icon { grid-column: 1; grid-row: 1; width: 2.4cqw; height: 2.4cqw; box-shadow: none; border-color: #d5e3d9; border-radius: .3cqw; }
.slide-analysis-panel .has-point-icon h2 { grid-column: 2; grid-row: 1; margin: 0; }
.slide-analysis-panel .has-point-icon p { grid-column: 1 / -1; }
.slide-analysis-panel .slide-analysis-point h2 { color: #ffffff; font-size: 1.2cqw; font-weight: 750; }
.slide-analysis-panel .slide-analysis-point p { color: #f1f8f3; font-size: 1.1cqw; line-height: 1.5; font-weight: 450; }
.slide-analysis-panel .slide-analysis-point.is-clickable-claim:hover { background: #ffffff0a; padding-left: 0; padding-right: 0; margin-left: 0; margin-right: 0; }
.slide-analysis-panel .slide-analysis-point:focus-visible { outline-color: #b9efca; }
.slide-forces-table { width: 100%; border-collapse: collapse; font-size: .96cqw; line-height: 1.36; }
.slide-forces-table th { text-align: left; color: #008c2c; padding: .55cqw .75cqw; border-bottom: 2px solid #008c2c; font-size: .88cqw; }
.slide-forces-table td { padding: .68cqw .75cqw; border-bottom: 1px solid #dce8df; }
.slide-forces-table td:nth-child(2) { color: #008c2c; font-weight: 750; white-space: nowrap; }
.slide-forces-table td:first-child { font-weight: 650; }
.slide-forces-table tr:last-child td { border-bottom: 0; }
.slide-key-figure { display: block; background: transparent; color: #fff; text-align: left; border: 0; padding: 0 0 1.1cqw; margin: 0; border-bottom: 1px solid #ffffff40; cursor: pointer; font: inherit; }
.slide-key-figure span { display: block; color: #c5f1cb; font-size: .9cqw; font-weight: 500; line-height: 1.4; }
.slide-key-figure strong { display: block; font-size: 2.45cqw; font-weight: 750; letter-spacing: -.08cqw; line-height: 1.2; margin: .35cqw 0; }
.slide-key-figure small { display: block; font-size: .78cqw; line-height: 1.45; color: #def7e1; }
.slide-takeaway { margin: 1cqw 0 0; font-size: 1.05cqw; line-height: 1.55; color: #fff; font-weight: 500; }
.slide-footline { position: absolute; left: 4%; right: 4%; bottom: 3.2%; display: flex; align-items: start; gap: 2cqw; border-top: 1px solid #ffffff40; padding-top: .9cqw; font-size: .65cqw; line-height: 1.4; color: #d9f0df; }
.slide-footline > span:first-child { white-space: nowrap; font-weight: 700; }
.slide-source { flex: 1; }
.slide-folio { font-variant-numeric: tabular-nums; white-space: nowrap; }
.slide-table-only { grid-template-columns: 1fr; }
.slide-table-stack { width: 100%; display: flex; flex-direction: column; }
.slide-scenario-bar { display: flex; align-items: center; justify-content: space-between; gap: .8cqw; margin-bottom: .9cqw; }
.slide-scenario-label { font-size: .85cqw; font-weight: 700; color: #153b22; }
.slide-scenario-select { font-size: .85cqw; font-weight: 650; color: #153b22; background: #edf6ef; border: 1px solid #a7cdb1; border-radius: .45cqw; padding: .35cqw .7cqw; cursor: pointer; font-family: inherit; }
.slide-financial-table { width: 100%; border-collapse: collapse; font-size: 1cqw; line-height: 1.45; table-layout: fixed; }
.slide-financial-table th { color: #007b2b; text-align: right; background: #edf6ef; padding: 1cqw .7cqw; font-size: .85cqw; font-weight: 750; }
.slide-financial-table td { padding: 1.1cqw .7cqw; text-align: right; border-bottom: 1px solid #dce8df; color: #253d2d; overflow-wrap: anywhere; }
.slide-evidence-stacked .slide-financial-table { font-size: .78cqw; line-height: 1.24; }
.slide-evidence-stacked .slide-financial-table th { padding: .38cqw .48cqw; font-size: .74cqw; }
.slide-evidence-stacked .slide-financial-table td { padding: .36cqw .48cqw; }
.slide-financial-table th:first-child, .slide-financial-table td:first-child { width: 34%; text-align: left; font-weight: 650; }
.slide-table-ratios { font-size: .84cqw; line-height: 1.28; }
.slide-table-ratios th { padding: .56cqw .48cqw; font-size: .75cqw; }
.slide-table-ratios td { padding: .60cqw .48cqw; }
.slide-table-ratios th:first-child, .slide-table-ratios td:first-child { width: 31%; }
.slide-table-ratios th:nth-child(5), .slide-table-ratios td:nth-child(5) { color: #007b2b; font-weight: 700; }
@keyframes slideRowUp {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.slide-financial-table tbody tr,
.slide-forces-table tbody tr,
.slide-editorial-row {
  animation: slideRowUp 0.36s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@media (prefers-reduced-motion: reduce) {
  .slide-financial-table tbody tr,
  .slide-forces-table tbody tr,
  .slide-editorial-row {
    animation: none;
  }
}
.slide-table-wacc th:first-child, .slide-table-wacc td:first-child { width: 33%; }
.slide-table-wacc th:nth-child(2), .slide-table-wacc td:nth-child(2) { width: 16%; }
.slide-table-wacc th:nth-child(3), .slide-table-wacc td:nth-child(3) { width: 51%; text-align: left; }
.slide-table-multiples { font-size: .86cqw; }
.slide-table-multiples th:first-child, .slide-table-multiples td:first-child { width: 28%; }
.slide-table-restatement { font-size: 1.02cqw; line-height: 1.38; }
.slide-table-restatement th, .slide-table-restatement td { text-align: left; padding: .72cqw .68cqw; vertical-align: top; }
.slide-table-restatement th:first-child, .slide-table-restatement td:first-child { width: 22%; }
.slide-table-restatement th:nth-child(2), .slide-table-restatement td:nth-child(2) { width: 26%; }
.slide-table-restatement th:nth-child(3), .slide-table-restatement td:nth-child(3) { width: 26%; }
.slide-table-restatement th:nth-child(4), .slide-table-restatement td:nth-child(4) { width: 26%; }
.slide-financial-table tbody tr:last-child td { border: 0; }
.slide-financial-table tbody tr:hover td { background: #edf6ef; cursor: pointer; }
.slide-table-dense { font-size: .92cqw; }
.slide-table-dense td { padding: .55cqw .7cqw; }
.slide-table-dense th { padding: .65cqw .7cqw; }
.slide-table-dense td:first-child, .slide-table-dense th:first-child { width: 30%; }
.slide-appendix .slide-evidence { padding: 1.2cqw; flex-direction: column; align-items: stretch; justify-content: flex-start; gap: 1.2cqw; overflow-y: auto; }
.slide-appendix-schedule { display: flex; flex-direction: column; gap: .45cqw; }
.slide-appendix-schedule h3 { margin: .2cqw 0 0; font-size: .95cqw; color: #006b23; font-weight: 700; }
.slide-appendix-note { margin: 0; font-size: .78cqw; color: #526a59; }
.slide-appendix .slide-financial-table:not(.slide-table-dense) { font-size: 1.05cqw; }
.slide-cover { background: linear-gradient(135deg, #007222 0%, #005419 100%); }
.slide-cover-top { position: absolute; left: 5%; right: 5%; top: 7%; display: flex; justify-content: space-between; align-items: center; }
.slide-cover-top .slide-brand { width: 11cqw; height: 6cqw; padding: 1cqw 1.4cqw; }
.slide-cover-top > span { font-size: .9cqw; letter-spacing: .18cqw; font-weight: 700; }
.slide-cover-title { position: absolute; left: 5%; top: 22%; width: 55%; }
.slide-cover-title > p { font-size: 1.15cqw; margin: 0 0 .9cqw; color: #edffeb; }
.slide-cover-title h1 { font-size: 7.2cqw; font-weight: 800; letter-spacing: -.36cqw; line-height: 1; margin: 0; color: white; }
.slide-cover-title h1 span { display: block; margin-top: .9cqw; font-size: 3.3cqw; letter-spacing: -.12cqw; font-weight: 650; }
.slide-cover-business { font-size: 1.02cqw; margin-top: 1.2cqw; font-weight: 650; }
.slide-cover-question { font-size: 1.35cqw; line-height: 1.5; margin: 1.8cqw 0 0; max-width: 43cqw; color: #e7f5ea; }
.slide-cover-summary { position: absolute; left: 63%; right: 5%; top: 22%; bottom: 11.5%; padding-left: 2.1cqw; border-left: 1px solid rgba(255, 255, 255, .28); display: flex; flex-direction: column; justify-content: flex-start; gap: 1.65cqw; }
.slide-cover-user > span, .slide-cover-verdict > span, .slide-cover-reason > span { display: block; font-size: .76cqw; letter-spacing: .14cqw; font-weight: 700; color: #c5e8ce; }
.slide-cover-user > p { font-size: 1.18cqw; line-height: 1.5; margin: .6cqw 0 0; max-width: 27cqw; }
.slide-cover-verdict { padding: 1.4cqw 0 0; border: 0; border-top: 1px solid rgba(255, 255, 255, .28); border-radius: 0; background: transparent; }
.slide-cover-verdict > strong { display: block; font-size: 2.55cqw; line-height: 1.18; margin-top: .85cqw; letter-spacing: -.08cqw; color: #ffffff; }
.slide-cover-verdict > strong.slide-cover-investor-question { font-size: 2.05cqw; line-height: 1.25; }
.slide-cover-verdict p { font-size: 1.05cqw; line-height: 1.5; margin: .6cqw 0 0; color: #e7f5ea; max-width: 27cqw; }
.slide-cover-reason { border-top: 1px solid rgba(255, 255, 255, .28); padding-top: 1.4cqw; }
.slide-cover-reason p { font-size: 1.05cqw; line-height: 1.6; margin: .6cqw 0 .65cqw; }
.slide-cover-reason small { font-size: .73cqw; line-height: 1.4; color: #c5e8ce; }
.slide-cover-team { position: absolute; left: 5%; bottom: 11.5%; display: flex; flex-direction: column; gap: .35cqw; font-size: .88cqw; line-height: 1.45; }
.slide-cover-team strong { font-size: .75cqw; letter-spacing: .15cqw; margin-bottom: .25cqw; }
button:focus-visible, tr:focus-visible, [role="button"]:focus-visible { outline: 2px solid #efc96c; outline-offset: 3px; }
.is-clickable-row { cursor: pointer; transition: background-color .16s ease; }
.slide-forces-table tbody tr.is-clickable-row:hover td { background: #edf6ef; }
.slide-editorial-row.is-clickable-row:hover { background: #edf6ef; border-radius: .45cqw; padding-left: .6cqw; padding-right: .6cqw; margin-left: -.6cqw; margin-right: -.6cqw; }
.slide-peer-exclusion.is-clickable-row:hover { background: #edf6ef; border-radius: .35cqw; padding-left: .5cqw; padding-right: .5cqw; margin-left: -.5cqw; margin-right: -.5cqw; }
.is-clickable-claim { cursor: pointer; transition: background-color .16s ease, border-color .16s ease; border-radius: .45cqw; }
.slide-analysis-point.is-clickable-claim:hover,
.slide-takeaway.is-clickable-claim:hover,
.slide-cover-business.is-clickable-claim:hover,
.slide-cover-thesis.is-clickable-claim:hover { background: rgba(255, 255, 255, 0.12); padding-left: .6cqw; padding-right: .6cqw; margin-left: -.6cqw; margin-right: -.6cqw; }
.slide-cover-verdict.is-clickable-claim:hover { background: transparent; }
.slide-cover-verdict:focus-visible { outline-color: #ffffff; }
.slide-foot-right { display: inline-flex; align-items: center; gap: .75cqw; flex-shrink: 0; }
.slide-apx-jump { display: inline-flex; align-items: center; gap: .32cqw; padding: .24cqw .68cqw; border-radius: .38cqw; border: 1px solid rgba(134, 239, 172, 0.48); background: rgba(255, 255, 255, 0.14); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); color: #eaffef; font: inherit; font-size: .74cqw; font-weight: 750; letter-spacing: .03em; cursor: pointer; white-space: nowrap; transition: background-color .15s ease, border-color .15s ease, transform .15s ease; }
.slide-apx-jump:hover { background: rgba(34, 197, 94, 0.42); border-color: rgba(134, 239, 172, 0.85); color: #ffffff; transform: translateY(-1px); }
.slide-apx-jump.is-back { border-color: rgba(251, 191, 36, 0.55); background: rgba(245, 158, 11, 0.24); color: #fef3c7; }
.slide-apx-jump.is-back:hover { background: rgba(245, 158, 11, 0.46); color: #ffffff; }
.slide-apx-ico { width: .82cqw; height: .82cqw; flex-shrink: 0; }
.slide-apx-mini-nav { display: inline-flex; align-items: center; gap: .22cqw; }
.slide-apx-dot { border: 1px solid rgba(255, 255, 255, 0.26); background: rgba(0, 0, 0, 0.22); color: #d1fae5; font: inherit; font-size: .68cqw; font-weight: 700; padding: .18cqw .42cqw; border-radius: .26cqw; cursor: pointer; transition: background-color .14s ease, color .14s ease; }
.slide-apx-dot:hover { background: rgba(255, 255, 255, 0.20); color: #ffffff; }
.slide-apx-dot.active { background: #4ade80; border-color: #4ade80; color: #052e16; }
.slide-abbr-sub { display: block; font-size: .68cqw; font-weight: 500; color: #547560; line-height: 1.25; margin-top: .1cqw; letter-spacing: 0; }
</style>
