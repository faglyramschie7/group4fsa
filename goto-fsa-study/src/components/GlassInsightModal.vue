<script setup>
import { computed, ref, watch } from 'vue'
import { useReportMode } from '../composables/useReportMode'
import { findAbbrTerms, getInlineAbbrHint } from '../composables/useAbbrGlossary'
import postTokopediaBaseForecast from '../data/post_tokopedia_base_forecast.json'

const props = defineProps({
  item: { type: Object, required: true },
  lang: { type: String, default: 'en' },
  renderMath: { type: Function, default: null },
})

const emit = defineEmits(['close', 'zoom', 'jump-assignment', 'jump-lecture', 'jump-slide'])

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
const appendixTarget = computed(() => {
  const s = props.item.slide
  if (!s || s.is_appendix) return null
  return appendixMap[s.slide_num] || null
})

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
const hoveredBar = ref(null)
const tooltipPos = ref({ x: 0, y: 0 })
function updateTooltipPos(evt) {
  if (!evt) return
  const pad = 16
  const maxW = 340
  const vw = typeof window !== 'undefined' ? window.innerWidth : 1280
  const x = Math.min(Math.max(evt.clientX, maxW / 2 + pad), vw - maxW / 2 - pad)
  const y = Math.max(evt.clientY, 110)
  tooltipPos.value = { x, y }
}
function setHoveredBar(label, value, cause, evt) {
  if (!cause) return
  hoveredBar.value = { label, value, cause }
  updateTooltipPos(evt)
}
function moveHoveredBar(evt) {
  if (!hoveredBar.value) return
  updateTooltipPos(evt)
}
function clearHoveredBar() {
  hoveredBar.value = null
}

// Slide 9 (Cost of Capital) interactive Source & Math walk-through sub-menu
const isSlide9Walkthrough = computed(() => (props.item.slide?.slide_num || 0) === 9)
const activeSlide9Comp = ref('wacc')

// Slide 3 (Porter's Five Forces) interactive visual dialogue walk-through sub-menu
const isPorterWalkthrough = computed(() => {
  if (props.item.kind === 'five_force') return true
  if ((props.item.slide?.slide_num || 0) !== 3) return false
  const t = `${props.item.title || ''}`.toLowerCase()
  return /entrant|supplier|buyer|substitut|rivalry|pendatang|pemasok|pembeli|substitusi|rivalitas/.test(t)
})
const activePorterForce = ref('entrants')

const detectInitialPorterForce = (item) => {
  const txt = `${item?.title || ''} ${item?.keywords || ''} ${item?.value || ''}`.toLowerCase()
  if (txt.includes('supplier') || txt.includes('pemasok')) return 'suppliers'
  if (txt.includes('buyer') || txt.includes('pembeli')) return 'buyers'
  if (txt.includes('substitut') || txt.includes('substitusi')) return 'substitutes'
  if (txt.includes('rival') || txt.includes('persaingan')) return 'rivalry'
  return 'entrants'
}

const porterForces = computed(() => {
  const id = isId.value
  return [
    {
      id: 'entrants',
      shortLabel: id ? '1. Pendatang Baru (Rendah–Sedang)' : '1. New Entrants (Low–Mod)',
      title: id ? 'Ancaman Pendatang Baru' : 'Threat of New Entrants',
      rating: id ? 'Rendah–Sedang' : 'Low–Moderate',
      ratingTone: 'pos',
      image: '/visuals/force_entrants.png',
      headline: id
        ? 'Membuat aplikasi mudah, tetapi meniru izin keuangan, teknologi Rp 5,94T, dan jaringan GoTo sangat sulit.'
        : 'Building an app is easy, but replicating GoTo’s licenses, Rp 5.94T tech stack, and nationwide network is hard.',
      evidence: id
        ? [
            'Izin Bank Indonesia (BI): PT Dompet Anak Bangsa (GoPay) & PT Midtrans memegang izin sistem pembayaran & uang elektronik dengan syarat modal minimum berbasis risiko.',
            'Izin OJK & PSE: PT Multifinance Anak Bangsa memegang izin pembiayaan OJK untuk pinjaman konsumen, ditambah wajib daftar PSE Komdigi & aturan Permendag e-commerce.',
            'Skala Teknologi & Jaringan: Rp 5,94T aset perangkat lunak (vs. Rp 114,5M Bukalapak), 66 juta pengguna tahunan, 6,4 juta merchant, dan 3 juta+ pengemudi.',
          ]
        : [
            'Bank Indonesia (BI) Licenses: PT Dompet Anak Bangsa (GoPay) & PT Midtrans hold payment/e-money authorizations with risk-weighted capital rules.',
            'OJK & Komdigi Registrations: PT Multifinance Anak Bangsa holds an OJK financing-company license, plus mandatory Komdigi PSE and Permendag compliance.',
            'Tech & Ecosystem Moat: Rp 5.94T software assets (vs. Bukalapak Rp 114.5B), 66M annual users, 6.4M merchants, and 3M+ driver partners.',
          ],
    },
    {
      id: 'suppliers',
      shortLabel: id ? '2. Pemasok (Rendah)' : '2. Suppliers (Low)',
      title: id ? 'Daya Tawar Pemasok' : 'Bargaining Power of Suppliers',
      rating: id ? 'Rendah' : 'Low',
      ratingTone: 'pos',
      image: '/visuals/force_suppliers.png',
      headline: id
        ? 'Jutaan mitra pengemudi, merchant, dan vendor tersebar luas sehingga tidak ada satu pihak pun yang bisa mendikte harga.'
        : 'Millions of fragmented drivers, merchants, and vendors mean no single supplier can dictate pricing or terms.',
      evidence: id
        ? [
            'Basis Mitra Tersebar: Lebih dari 3 juta pengemudi dan 6,4 juta merchant; tidak ada satu pemasok pun yang melebihi 10% pendapatan bersih.',
            'Ketergantungan Platform: Mitra kecil bergantung pada volume pesanan harian GoTo, sehingga GoTo dapat memangkas insentif Gojek 15,9% di 2025.',
            'Disiplin Pengadaan & Cloud: Renegosiasi infrastruktur cloud memangkas biaya >50% pada 2025 dengan ketergantungan rendah pada barang impor.',
          ]
        : [
            'Fragmented Base: 3M+ drivers and 6.4M merchants; zero single vendor exceeds 10% of net revenue.',
            'Platform Dependency: Small merchants and drivers rely on GoTo’s daily order flow, allowing GoTo to cut Gojek incentives by 15.9% in 2025.',
            'Tech Procurement Discipline: Cloud renegotiations delivered >50% savings in 2025 with minimal exposure to physical imported inputs.',
          ],
    },
    {
      id: 'buyers',
      shortLabel: id ? '3. Pembeli (Sedang)' : '3. Buyers (Medium)',
      title: id ? 'Daya Tawar Pembeli' : 'Bargaining Power of Buyers',
      rating: id ? 'Sedang' : 'Medium',
      ratingTone: 'accent',
      image: '/visuals/force_buyers.png',
      headline: id
        ? 'Pengguna tersebar luas, tetapi biaya pindah aplikasi nyaris nol sehingga konsumen sangat sensitif terhadap promo dan tarif.'
        : 'Individual users are fragmented, yet near-zero switching costs make Indonesian consumers highly price-sensitive.',
      evidence: id
        ? [
            'Biaya Pindah Hampir Nol: Pengguna membandingkan tarif, ongkos kirim, dan transfer gratis GoPay dengan pesaing dalam hitungan detik.',
            'Sensitivitas Harga Tinggi: Laporan Tahunan 2025 (hal. 46 & 168) menegaskan persaingan harga dan promo sangat menentukan retensi pengguna.',
            'Penyeimbang Skala: Basis 66 juta pengguna (+24% YoY) yang tersebar menjaga agar tidak ada pembeli tunggal yang mendominasi.',
          ]
        : [
            'Near-Zero Switching Cost: Users compare fares, delivery promos, and free GoPay transfers across competing apps in seconds.',
            'High Price Sensitivity: GoTo’s 2025 Annual Report (pp. 46, 168) explicitly cites price competition and promo sensitivity as core risks.',
            'Fragmented User Counterweight: 66M annual users (+24% YoY) prevent any single customer from exerting direct pricing leverage.',
          ],
    },
    {
      id: 'substitutes',
      shortLabel: id ? '4. Substitusi (Sedang)' : '4. Substitutes (Medium)',
      title: id ? 'Ancaman Produk Substitusi' : 'Threat of Substitutes',
      rating: id ? 'Sedang' : 'Medium',
      ratingTone: 'accent',
      image: '/visuals/force_substitutes.png',
      headline: id
        ? 'Masyarakat selalu punya alternatif di luar aplikasi: transportasi umum, makan di tempat, atau transfer bank biasa.'
        : 'Consumers always have offline or non-super-app alternatives: public transit, dine-in, or standard bank transfers.',
      evidence: id
        ? [
            'Substitusi Transportasi: MRT, TransJakarta, KRL, angkutan lokal, dan kepemilikan motor/mobil pribadi yang tinggi di Indonesia.',
            'Substitusi Pesan-Antar: Makan di tempat (dine-in), masak sendiri, atau pesan langsung ke restoran sekitar tanpa biaya aplikasi.',
            'Substitusi Pembayaran: Uang tunai, kartu debit/kredit, serta mobile banking BI-FAST dan QRIS bank.',
          ]
        : [
            'Mobility Alternatives: Public transit (MRT, TransJakarta, KRL) and high private motorbike/car ownership across Indonesia.',
            'Food Alternatives: Dining in at restaurants, home cooking, or direct walk-in takeaway avoiding platform fees.',
            'Payment Alternatives: Cash, bank cards, and standard mobile-banking BI-FAST / QRIS transfers.',
          ],
    },
    {
      id: 'rivalry',
      shortLabel: id ? '5. Rivalitas (Tinggi)' : '5. Rivalry (High)',
      title: id ? 'Rivalitas Persaingan (Paling Membatasi)' : 'Competitive Rivalry (Most Binding Force)',
      rating: id ? 'Tinggi' : 'High',
      ratingTone: 'warn',
      image: '/visuals/force_rivalry.png',
      headline: id
        ? 'Persaingan langsung yang ketat di setiap lini bisnis menahan daya harga dan memaksa belanja S&M Rp 3,09T + R&D Rp 2,15T.'
        : 'Fierce head-to-head competition across every vertical caps pricing power and forces Rp 3.09T S&M + Rp 2.15T R&D spend.',
      evidence: id
        ? [
            'Pangsa Pasar Ketat: Food delivery 2025 — GrabFood 46% vs. GoFood 31% vs. ShopeeFood 23%; transportasi bersaing dengan Grab, Maxim & inDrive.',
            'Dampak Langsung ke Laba Rugi: Beban Penjualan & Pemasaran Rp 3,09T (+8% YoY) + Pengembangan Produk Rp 2,15T (+23% YoY) + Insentif Rp 1,08T.',
            'Pergeseran ke Risiko Kredit: Di tengah ketatnya persaingan, pinjaman GoPay naik +72,6% ke Rp 2,73T dan provisi kredit melonjak +134,9% ke Rp 408M.',
          ]
        : [
            'Crowded Market Shares: 2025 food delivery — GrabFood 46% vs. GoFood 31% vs. ShopeeFood 23%; rides pressured by Grab, Maxim & inDrive.',
            'Direct P&L Cost: Forced Rp 3.09T Sales & Marketing (+8% YoY), Rp 2.15T Product Dev (+23% YoY), and Rp 1.08T expensed incentives.',
            'Push Into Credit Risk: Seeking higher-margin growth amid rivalry, GoPay consumer loans jumped +72.6% to Rp 2.73T while credit provisions surged +134.9% to Rp 408B.',
          ],
    },
  ]
})

const currentPorterForce = computed(() =>
  porterForces.value.find((f) => f.id === activePorterForce.value) || porterForces.value[0]
)
const currentPorterIdx = computed(() =>
  porterForces.value.findIndex((f) => f.id === activePorterForce.value)
)
const prevPorterForce = computed(() =>
  currentPorterIdx.value > 0 ? porterForces.value[currentPorterIdx.value - 1] : null
)
const nextPorterForce = computed(() =>
  currentPorterIdx.value >= 0 && currentPorterIdx.value < porterForces.value.length - 1
    ? porterForces.value[currentPorterIdx.value + 1]
    : null
)

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
        ? 'Biaya modal rata-rata tertimbang GoTo lintas pemegang saham dan kreditur. Menjadi batas imbal hasil (hurdle rate) untuk mendiskontokan FCFF di DCF; ROIC 2028F GoTo (+2,70%) tertinggal 5.06% di bawah WACC.'
        : 'GoTo\'s blended financing cost across shareholders and lenders. Used to discount DCF Free Cash Flows; GoTo\'s 2028F ROIC (+2.70%) trails this 7.761% hurdle by 5.06%, which is why operating EV is negative.',
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
          note: id ? 'Jika rugi fiskal menghapus tax shield, WACC naik +0.34% ke 8,101%.' : 'If past tax losses remove the tax shield, WACC rises +0.34% to 8.101%.',
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
    activePorterForce.value = detectInitialPorterForce(newItem)
    showMoreAnalysis.value = false
    showRightPanel.value = false
    showAllCalcRows.value = false
    showAllTraces.value = false
    openSchedules.value = { 0: true }
    hoveredBar.value = null
  },
  { immediate: true }
)

watch([chartBasis, activeTab], () => {
  hoveredBar.value = null
})

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

const displayedSchedules = computed(() => {
  const sNum = props.item.slide?.slide_num
  const id = isId.value
  if ((sNum === 8 || sNum === 19) && chartBasis.value === 'current') {
    const hdr = [id ? 'Pos Laporan (Rp miliar)' : 'Line Item (Rp billion)', '2026F', '2027F', '2028F']
    return [
      {
        title: id
          ? 'Laporan Laba Rugi Pro Forma — Base Case Final Report (Pasca-Tokopedia)'
          : 'Base Projected Income Statement — Final Report (Post-Tokopedia)',
        headers: hdr,
        rows: [
          [id ? 'Pendapatan (+15,27% YoY pasca-Tokopedia)' : 'Revenue (+15.27% post-Tokopedia YoY)', '21,121', '24,346', '28,065'],
          [id ? 'Beban Pokok Pendapatan (42,28% dari Pendapatan)' : 'Cost of Goods Sold (42.28% of Revenue)', '8,929', '10,293', '11,865'],
          [id ? 'Laba Kotor (Margin Kotor 57,72%)' : 'Gross Profit (57.72% Gross Margin)', '12,191', '14,053', '16,200'],
          [id ? 'Beban Operasi (55,70% dari Pendapatan)' : 'Operating Expenses (55.70% of Revenue)', '11,765', '13,561', '15,633'],
          ['EBIT', '+427', '+492', '+567'],
          [id ? 'Beban Bunga (Rp 535,2M tetap, Catatan 27b)' : 'Interest Expense (Rp 535.2B fixed, Note 27b)', '535', '535', '535'],
          [id ? 'Laba / (Rugi) Sebelum Pajak (EBT)' : 'Earnings Before Tax (EBT)', '(108)', '(43)', '+32'],
          [id ? 'Beban / (Manfaat) Pajak (22,0%)' : 'Tax Expense / (Benefit) (22.0%)', '(24)', '(9)', '7'],
          [id ? 'Laba / (Rugi) Bersih' : 'Net Income', '(84)', '(34)', '+25'],
        ],
      },
      {
        title: id
          ? 'Neraca Pro Forma — Base Case Final Report (Pasca-Tokopedia)'
          : 'Base Projected Balance Sheet — Final Report (Post-Tokopedia)',
        headers: hdr,
        rows: [
          [id ? 'Kas & Setara Kas (plug)' : 'Cash & Equivalents (plug)', '20,687', '19,955', '19,421'],
          [id ? 'Piutang Usaha (10,90 hari)' : 'Accounts Receivable (10.90 days)', '631', '727', '838'],
          [id ? 'Persediaan (0,66 hari)' : 'Inventory (0.66 days)', '16', '19', '22'],
          [id ? 'Total Aset Lancar' : 'Total Current Assets', '21,334', '20,701', '20,281'],
          [id ? 'Aset Tetap Bersih (Net PP&E)' : 'Net PP&E', '1,712', '2,532', '3,232'],
          [id ? 'Aset Lainnya (tetap)' : 'Other Assets (held constant)', '22,819', '22,819', '22,819'],
          [id ? 'TOTAL ASET' : 'TOTAL ASSETS', '45,865', '46,052', '46,332'],
          [id ? 'Utang Usaha (59,11 hari)' : 'Accounts Payable (59.11 days)', '1,446', '1,667', '1,921'],
          [id ? 'Utang Jangka Pendek (tetap)' : 'Short-Term Debt (held constant)', '1,524', '1,524', '1,524'],
          [id ? 'Utang Jangka Panjang (tetap)' : 'Long-Term Debt (held constant)', '6,219', '6,219', '6,219'],
          [id ? 'Liabilitas Lainnya (tetap)' : 'Other Liabilities (held constant)', '8,049', '8,049', '8,049'],
          [id ? 'Total Liabilitas' : 'Total Liabilities', '17,238', '17,458', '17,713'],
          [id ? 'Total Ekuitas Pemegang Saham' : "Total Shareholders' Equity", '28,627', '28,594', '28,619'],
          [id ? 'TOTAL LIABILITAS & EKUITAS' : 'TOTAL LIABILITIES & EQUITY', '45,865', '46,052', '46,332'],
        ],
      },
      {
        title: id
          ? 'Laporan Arus Kas Pro Forma — Base Case Final Report (Pasca-Tokopedia)'
          : 'Base Projected Cash Flow Statement — Final Report (Post-Tokopedia)',
        headers: hdr,
        rows: [
          [id ? 'Laba / (Rugi) Bersih' : 'Net Income', '(84)', '(34)', '+25'],
          [id ? 'Tambah: Depresiasi & Amortisasi' : 'Add: Depreciation & Amortization', '+273', '+751', '+1,111'],
          [id ? 'Perubahan Piutang Usaha' : '(Increase)/Decrease in Receivables', '(84)', '(96)', '(111)'],
          [id ? 'Perubahan Persediaan' : '(Increase)/Decrease in Inventory', '(2)', '(2)', '(3)'],
          [id ? 'Perubahan Utang Usaha' : 'Increase/(Decrease) in Payables', '+192', '+221', '+255'],
          [id ? 'Arus Kas Operasi (CFO)' : 'Cash Flow from Operations (CFO)', '+295', '+840', '+1,277'],
          [id ? 'Belanja Modal (CapEx 6,45% Pendapatan)' : 'Capital Expenditures (6.45% of Revenue)', '(1,363)', '(1,571)', '(1,811)'],
          [id ? 'Arus Kas Investasi (CFI)' : 'Cash Flow from Investing (CFI)', '(1,363)', '(1,571)', '(1,811)'],
          [id ? 'Arus Kas Pendanaan (CFF)' : 'Cash Flow from Financing (CFF)', '0', '0', '0'],
          [id ? 'Perubahan Bersih Kas' : 'Net Change in Cash', '(1,068)', '(731)', '(534)'],
          [id ? 'Kas Awal' : 'Beginning Cash', '21,755', '20,687', '19,955'],
          [id ? 'Kas Akhir (cocok dengan Neraca)' : 'Ending Cash (reconciles to Balance Sheet)', '20,687', '19,955', '19,421'],
        ],
      },
      {
        title: id
          ? 'Uji Titik Impas (Breakeven) & Leverage Operasi — Final Report'
          : 'Breakeven Check & Operating Leverage — Final Report',
        headers: hdr,
        rows: [
          [id ? 'Margin Kotor (%)' : 'Gross Margin (%)', '57.72%', '57.72%', '57.72%'],
          [id ? 'Pendapatan Titik Impas (OpEx ÷ Margin Kotor)' : 'Breakeven Revenue (OpEx ÷ Gross Margin)', '20,381', '23,494', '27,082'],
          [id ? 'Surplus Pendapatan di Atas Titik Impas' : 'Revenue Surplus Above Breakeven', '+739', '+852', '+983'],
          [id ? 'Status Titik Impas' : 'Breakeven Status', id ? 'Di Atas Impas' : 'Above Breakeven', id ? 'Di Atas Impas' : 'Above Breakeven', id ? 'Di Atas Impas' : 'Above Breakeven'],
          [id ? 'Margin of Safety (%)' : 'Margin of Safety (%)', '+3.50%', '+3.50%', '+3.50%'],
          [id ? 'Degree of Operating Leverage (DOL = GP ÷ EBIT)' : 'Degree of Operating Leverage (DOL = GP ÷ EBIT)', '28.56x', '28.56x', '28.56x'],
        ],
      },
    ]
  }
  return props.item.slide?.supporting_schedules || []
})

const schedulesCount = computed(() => displayedSchedules.value.length)
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
        { metric: id ? 'Cash OpEx (% Pendapatan)' : 'Cash OpEx (% Revenue)', before: '117.01%', after: '55.70%', delta: '−61.31%', tone: 'pos', pctA: 100, pctB: 48, note: id ? 'Subsidi e-commerce pra-exit tereliminasi; turun −7.08% lagi di 2025.' : 'Pre-exit e-commerce subsidies removed; fell another −7.08% in 2025.' },
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
        { metric: id ? 'Margin Laba Kotor' : 'Gross Profit Margin', before: '65.55%', after: '57.72%', delta: '−7.83% mix', tone: 'accent', pctA: 100, pctB: 88, note: id ? 'Pergeseran bauran segmen pasca-exit, namun naik +4.36% YoY dari 2024.' : 'Post-exit segment mix shift, yet expanded +4.36% YoY vs. 2024 (53.36%).' },
        { metric: id ? 'Margin Operasi (EBIT)' : 'Operating Margin (EBIT)', before: '−69.52%', after: '−2.06%', delta: '+67.46%', tone: 'pos', pctA: 100, pctB: 8, note: id ? 'Mendekati titik impas operasi setelah keluar dari Tokopedia & Vietnam.' : 'Approaching operating breakeven after Tokopedia & Vietnam exits.' },
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
        { metric: id ? 'Utang / Ekuitas 2024' : '2024 Debt / Equity', before: '12.57%', after: '15.85%', delta: '+3.28%', tone: 'accent', pctA: 79, pctB: 100, note: id ? 'Memasukkan porsi lancar & liabilitas sewa penuh (2025 naik ke 26,97%).' : 'Included current maturities & full leases (rose to 26.97% in 2025).' },
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
        { metric: id ? 'CapEx Tunai (% Pendapatan)' : 'Cash CapEx (% Revenue)', before: '41.01%', after: '6.45%', delta: '−34.56%', tone: 'pos', pctA: 100, pctB: 16, note: id ? '2024 berlanjut sebenarnya 6,63% setelah mengeluarkan Rp5.464,9M Tokopedia.' : '2024 continuing CapEx was actually 6.63% ex-Rp5,464.9B Tokopedia transfer.' },
        { metric: id ? 'Arus Kas Operasi (CFO)' : 'Operating Cash Flow', before: '−Rp 622.1B', after: '+Rp 307.0B', delta: '+Rp 929.1B YoY', tone: 'pos', pctA: 65, pctB: 100, note: id ? 'Berbalik positif meski ekspansi pinjaman GoPay menyerap −Rp2,02T.' : 'Turned positive despite −Rp2.02T working-capital outflow for GoPay lending.' },
        { metric: id ? 'Arus Kas Bebas (FCF)' : 'Free Cash Flow (FCF)', before: '−Rp 7,141B', after: '−Rp 875.3B', delta: 'Cont. 24: −1,676B', tone: 'accent', pctA: 100, pctB: 14, note: id ? 'CFO 2025 baru menutup 25,97% CapEx tunai (Rp1,18T); kas masih tergerus.' : '2025 CFO covered only 25.97% of cash CapEx (Rp1.18T); FCF remains negative.' },
        { metric: id ? 'Rasio Akrual (Dilaporkan)' : 'Reported Accrual Ratio', before: '−11.21%', after: '−3.95%', delta: '+7.26% YoY', tone: 'pos', pctA: 100, pctB: 35, note: id ? 'Akrual berulang yang disesuaikan juga menyempit dari −3,69% ke −1,94%.' : 'Adjusted recurring accrual ratio also tightened from −3.69% to −1.94%.' },
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
        { metric: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth Rate', before: '11.40%', after: '15.27%', delta: '+3.87%', tone: 'pos', pctA: 75, pctB: 100, note: id ? 'Mencerminkan pertumbuhan organik 2024→2025 tanpa seretan dekonsolidasi.' : 'Reflects clean 2024→2025 organic growth without deconsolidation drag.' },
        { metric: id ? 'COGS / Pendapatan' : 'COGS / Revenue', before: '41.10%', after: '42.28%', delta: '+1.18%', tone: 'accent', pctA: 97, pctB: 100, note: id ? 'Menggunakan basis aktual FY2025 pasca-exit (1H26 membaik ke 38,10%).' : 'Anchored on actual FY2025 post-exit mix (1H26 improved further to 38.10%).' },
        { metric: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue', before: '78.50%', after: '55.70%', delta: '−22.80%', tone: 'pos', pctA: 100, pctB: 71, note: id ? 'Menghapus OpEx 2023 (117,01%) yang menyebabkan pembakaran kas buatan.' : 'Eliminates 2023 OpEx (117.01%) that caused artificial cash depletion.' },
        { metric: id ? 'CapEx / Pendapatan' : 'CapEx / Revenue', before: '16.30%', after: '6.45%', delta: '−9.85%', tone: 'pos', pctA: 100, pctB: 40, note: id ? 'Menghapus anomali 41,0% di 2024 akibat transfer takberwujud Tokopedia.' : 'Removes the 41.0% 2024 distortion from Tokopedia intangible transfers.' },
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
        { metric: id ? '2028F Laba Bersih' : '2028F Net Income', before: '−Rp 4,348B', after: '+Rp 25.0B', delta: 'Turns Profitable', tone: 'pos', pctA: 100, pctB: 10, note: id ? 'Mencapai laba bersih positif pada Tahun ke-3 meski ROE hanya +0,09%.' : 'Reaches positive net profit in Year 3, though ROE is only +0.09%.' },
        { metric: id ? '2028F Saldo Kas Akhir' : '2028F Ending Cash Balance', before: 'Rp 0.97T', after: 'Rp 19.42T', delta: '+Rp 18.45T saved', tone: 'pos', pctA: 8, pctB: 100, note: id ? 'Menghilangkan ilusi kebangkrutan kas akibat asumsi OpEx 78,5%.' : 'Eliminates artificial cash depletion caused by the 78.5% OpEx error.' },
        { metric: id ? '2028F ROIC vs. WACC' : '2028F ROIC vs. WACC', before: 'Negative', after: '+2.70% vs 7.76%', delta: '−5.06% spread', tone: 'warn', pctA: 10, pctB: 35, note: id ? 'Masih menghancurkan nilai ekonomi meski operasional sudah untung.' : 'Still earns below cost of capital despite turning operationally profitable.' },
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
          ? 'Pergerakan YoY: COGS naik dari 34,45% (2023 pra-exit) ke 46,64% (2024 pasca-exit) karena pergeseran bauran segmen, lalu turun −4.36% ke 42,28% di FY2025 berkat efisiensi biaya cloud >50% dan skala Gojek, serta membaik lagi ke 38,10% pada 1H 2026.'
          : 'YoY Driver Story: COGS jumped from 34.45% (2023 pre-exit) to 46.64% (2024 post-exit) on segment mix shift after deconsolidation, then fell −4.36% YoY to 42.28% in FY2025 via >50% cloud cost savings and Gojek scale, reaching 38.10% in 1H 2026.'
      )
    } else if (t.includes('opex') || t.includes('operating')) {
      paras.push(
        id
          ? 'Pergerakan YoY: Cash OpEx turun drastis dari 117,01% (2023) → 62,78% (2024) → 55,70% (2025, −7.08% YoY) melalui pemangkasan insentif (−Rp504,2M di Gojek) dan efisiensi korporasi, hingga menyentuh 51,20% pada 1H 2026.'
          : 'YoY Driver Story: Cash OpEx compressed sharply from 117.01% (2023) → 62.78% (2024) → 55.70% (2025, −7.08% YoY) through incentive cuts (−Rp504.2B at Gojek) and leaner corporate overhead, tightening further to 51.20% in 1H 2026.'
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
          ? 'Pergerakan YoY: Setelah mengeluarkan transfer aset takberwujud Tokopedia Rp5.464,9M dari 2024 (Catatan 12), CapEx lanjutan stabil dari 6,63% (2024) ke 6,45% (2025, −0.18% YoY), mematahkan ilusi lonjakan 41,0% di dek lama.'
          : 'YoY Driver Story: Once Rp5,464.9B of pre-deconsolidation Tokopedia intangible transfers are stripped out of 2024 (Note 12), continuing CapEx holds steady at 6.63% (2024) → 6.45% (2025, −0.18% YoY), correcting the 41.0% old-deck distortion.'
      )
    } else if (t.includes('debt') || t.includes('borrow') || t.includes('interest') || t.includes('bunga') || t.includes('utang')) {
      paras.push(
        id
          ? 'Pergerakan YoY: Biaya bunga efektif atas total utang dan liabilitas sewa penuh (Catatan 19–20 & 27b) bergerak 8,52% (2023) → 10,25% (2024) → 6,91% (2025, −3.34% YoY) seiring fasilitas pinjaman baru berbiaya lebih rendah.'
          : 'YoY Driver Story: Effective borrowing cost on full debt and lease liabilities (Notes 19–20 & 27b) moved 8.52% (2023) → 10.25% (2024) → 6.91% (2025, −3.34% YoY) as lower-cost bank facilities scaled in FY2025.'
      )
    }
  }
  if (sn === 11) {
    paras.push(
      id
        ? 'Basis Rentang Wajar (Rp10,38–Rp16,75/saham): Lantai Rp10,38 adalah Base DCF (WACC 7,76%, g 3,0%): Kas Bersih +Rp14.012,5M (Rp13,19/sh) dikurangi Enterprise Value negatif −Rp2.988,5M (karena ROIC 2,70% < WACC 7,76%) = +Rp11.024,0M ÷ 1.062,01M saham.'
        : 'Defensible Range Basis (Rp 10.38–Rp 16.75/share): The Rp 10.38 floor is Base Case DCF (WACC 7.76%, g 3.0%): Net Cash (+Rp 14,012.5B, or Rp 13.19/sh center) minus negative Enterprise Value (−Rp 2,988.5B, since 2.70% ROIC < 7.76% WACC) = +Rp 11,024.0B ÷ 1,062.01B shares.'
    )
    paras.push(
      id
        ? 'Plafon Rp16,75 adalah Optimistic Residual Income dengan rasio biaya 1H 2026 (pertumbuhan 18,0%, COGS 38,10%, Cash OpEx 51,20% → EBIT 2028F Rp3.221,1M, ROE 6,18% vs. Ke 8,45%).'
        : 'The Rp 16.75 ceiling is Optimistic Residual Income using 1H 2026 interim cost ratios (18.00% growth, 38.10% COGS, 51.20% Cash OpEx → 2028F EBIT Rp 3,221.1B, ROE 6.18% vs. 8.45% Ke).'
    )
    paras.push(
      id
        ? 'Angka di luar rentang: Conservative RI (−Rp44,42) memproyeksikan kembalinya biaya 2024 (OpEx 62,8%); Base RI (−Rp12,23) mengkapitalisasi kerugian ekonomi selamanya; Opt. DCF (+Rp47,34) menuntut OpEx 51,2% bertahan setahun penuh; dan Grab P/B (+Rp91,02) mencerminkan pembanding yang sudah membukukan ROE +2,96%.'
        : 'Why the other Football Field bars sit outside the range: Conservative RI (−Rp 44.42) reverts to 2024 costs (62.8% OpEx); Base RI (−Rp 12.23) capitalizes negative economic profit in perpetuity; Opt. DCF (+Rp 47.34) assumes 51.2% OpEx holds permanently; and Grab P/B (+Rp 91.02) reflects a peer already earning +2.96% ROE.'
    )
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
          { label: 'FY2024 EBIT', val: 69.4, display: '+69.4B', cause: id ? 'Laba awal segmen On-Demand setelah pemisahan Tokopedia di 2024.' : 'Initial On-Demand profit base right after Tokopedia deconsolidation in 2024.' },
          { label: id ? 'Pendapatan Bruto 3P' : '3P Gross Revenue', val: 995.8, display: '+995.8B', cause: id ? 'Tambahan pendapatan komisi & layanan ekosistem Gojek sepanjang FY2025.' : 'Higher trip volume and take-rate commissions added Rp 995.8B of revenue.' },
          { label: id ? 'Pangkas Insentif (−15,9%)' : 'Incentive Cut (−15.9%)', val: 504.2, display: '+504.2B', cause: id ? 'Pemangkasan promo & subsidi mitra sebesar Rp504M langsung menambah laba.' : 'Cutting promo & driver subsidies by 15.9% flowed straight to operating profit.' },
          { label: id ? 'Antar-Segmen Bersih' : 'Inter-Segment Net', val: 67.8, display: '+67.8B', cause: id ? 'Kontribusi bersih penagihan silang antar unit ekosistem GoTo.' : 'Net benefit from ecosystem cross-segment service billing.' },
          { label: id ? 'Alokasi Korporasi' : 'Corp. Alloc. Cut', val: 32.5, display: '+32.5B', cause: id ? 'Penurunan alokasi biaya overhead pusat yang dibebankan ke segmen Gojek.' : 'Lower corporate overhead allocation charged to Gojek segment.' },
          { label: id ? 'Kenaikan Biaya 3P' : '3P Cost Growth', val: -781.1, display: '−781.1B', cause: id ? 'Kenaikan biaya operasional & teknologi untuk mendukung pertumbuhan pesanan.' : 'Higher direct cost of revenue and server/ops scaling for increased trip volume.' },
          { label: 'FY2025 EBIT', val: 888.6, display: '+888.6B', accent: true, cause: id ? 'Laba operasi Gojek melonjak 12,8x (+1.180% YoY) menjadi penopang utama grup.' : 'Gojek EBIT jumped +1,180% YoY to +Rp 888.6B, becoming GoTo’s core profit pillar.' },
        ],
      }
    }
    return {
      type: 'diverging',
      title: id ? 'Kontribusi EBIT per Segmen (FY2025, Note 29)' : 'FY2025 Segment Operating Profit / Loss (Note 29)',
      subtitle: id ? 'Dalam Rp miliar · Gojek & Tokopedia Fee positif tertutup biaya korporasi' : 'In Rp billion · Positive Gojek & E-Commerce offset by Fintech & Corporate',
      unit: 'Rp bn',
      items: [
        { label: 'On-Demand (Gojek)', val: 888.6, display: '+888.6B', accent: true, cause: id ? 'Mesin laba utama GoTo: pertumbuhan 3P + pemangkasan insentif & biaya cloud.' : 'GoTo’s main profit engine: tighter incentive discipline and cloud/ops savings.' },
        { label: 'E-Commerce Fee', val: 572.2, display: '+572.2B', cause: id ? 'Biaya layanan pasca-exit dari Tokopedia/TikTok (margin tinggi tanpa beban OpEx).' : 'High-margin post-exit service fee from Tokopedia/TikTok with no e-commerce OpEx drag.' },
        { label: 'Fintech (GoPay)', val: -396.6, display: '−396.6B', cause: id ? 'Masih rugi akibat ekspansi agresif pinjaman & lonjakan provisi kredit (+134,9%).' : 'Still loss-making due to GoPay loan expansion and +134.9% surge in bad-debt provisions.' },
        { label: id ? 'Biaya Korporasi' : 'Unalloc. Corporate', val: -1442.5, display: '−1,442.5B', cause: id ? 'Beban kantor pusat, kompensasi saham (SBC), & infrastruktur menghapus laba segmen.' : 'Head-office overhead, share-based comp (SBC), and shared tech wipe out segment profits.' },
        { label: id ? 'EBIT Konsolidasian' : 'Consolidated EBIT', val: -378.3, display: '−378.3B', accent: true, cause: id ? 'Rugi operasi menyempit drastis ke −Rp378M, namun belum menutup biaya korporasi.' : 'Operating loss narrowed sharply to −Rp378B, but corporate costs still keep it negative.' },
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
        { label: id ? 'Penjualan & Pemasaran' : 'Sales & Marketing', val: 3090.1, display: 'Rp 3,090B', cause: id ? '16,9% pendapatan untuk melawan Grab, Maxim, inDriver, & ShopeeFood.' : '16.9% of revenue spent defending market share against Grab, Maxim, inDriver & ShopeeFood.' },
        { label: id ? 'Pengembangan Produk' : 'Product Development', val: 2152.3, display: 'Rp 2,152B', cause: id ? '11,7% pendapatan agar teknologi super-app GoTo tetap bersaing vs pesaing spesialis.' : '11.7% of revenue needed to maintain super-app tech against specialized rivals.' },
        { label: id ? 'Insentif Beban S&M' : 'Expensed Incentives', val: 1076.9, display: 'Rp 1,077B', cause: id ? 'Promo pelanggan & mitra karena biaya pindah sangat rendah sehingga harga sulit dinaikkan.' : 'Promo subsidies GoTo cannot cut deeply because customer switching costs are very low.' },
        { label: id ? 'Provisi Kredit 2024' : '2024 Loan Provisions', val: 173.6, display: 'Rp 174B', cause: id ? 'Cadangan kredit macet awal saat portofolio pinjaman GoPay masih Rp1,58T di 2024.' : 'Baseline bad-debt buffer in 2024 when GoPay’s net consumer loan book was Rp1.58T.' },
        { label: id ? 'Provisi Kredit 2025 (+134,9%)' : '2025 Provisions (+134.9%)', val: 407.7, display: 'Rp 408B', warn: true, cause: id ? 'Naik hampir 2x lebih cepat (+134,9%) dari lonjakan pinjaman GoPay (+72,6% ke Rp2,73T).' : 'Jumped +134.9% — nearly 2x faster than GoPay consumer loan growth (+72.6% to Rp2.73T).' },
      ],
    }
  }

  // Slide 4: Profitability & Three-Step DuPont ROE Decomposition
  if (sn === 4) {
    return {
      type: 'dupont_3step',
      title: id ? 'Dekomposisi DuPont 3-Langkah: GoTo vs. Grab' : 'Three-Step DuPont ROE: GoTo vs. Grab',
      subtitle: id
        ? 'ROE = Margin Bersih × Perputaran Aset × Equity Multiplier'
        : 'ROE = Net Margin × Asset Turnover × Equity Multiplier',
      unit: 'Ke = 8.45%',
      rows: [
        {
          label: id ? 'GoTo 2024 (Konsol.)' : 'GoTo 2024 (Consol.)',
          shortLabel: "GoTo '24\nCons.",
          tone: 'crimson',
          margin: -34.38,
          marginDisp: '−34.38%',
          turnover: 0.37,
          turnoverDisp: '0.37x',
          leverage: 1.42,
          leverageDisp: '1.42x',
          roe: -17.97,
          roeDisp: '−17.97%',
          cause: id ? 'Tahun transisi tepat setelah pemisahan Tokopedia: rugi bersih Rp5,47T menekan ROE ke −17,97%.' : 'First post-Tokopedia transition year: −Rp5.47T net loss pulled ROE down to −17.97%.',
        },
        {
          label: id ? 'GoTo 2025 (Konsol.)' : 'GoTo 2025 (Consol.)',
          shortLabel: "GoTo '25\nCons.",
          tone: 'amber',
          margin: -8.20,
          marginDisp: '−8.20%',
          turnover: 0.40,
          turnoverDisp: '0.40x',
          leverage: 1.59,
          leverageDisp: '1.59x',
          roe: -5.23,
          roeDisp: '−5.23%',
          cause: id ? 'Perputaran aset (0,40x) kalahkan Grab; satu-satunya penghambat ROE adalah margin bersih negatif −8,20%.' : 'Asset turnover (0.40x) beats Grab and leverage (1.59x) is safe; negative Net Margin (−8.20%) is the sole bottleneck.',
        },
        {
          label: id ? 'GoTo 2025 (Induk)' : 'GoTo 2025 (Parent)',
          shortLabel: "GoTo '25\nParent",
          tone: 'blue',
          margin: -6.47,
          marginDisp: '−6.47%',
          turnover: 0.40,
          turnoverDisp: '0.40x',
          leverage: 1.44,
          leverageDisp: '1.44x',
          roe: -3.73,
          roeDisp: '−3.73%',
          cause: id ? 'Tanpa porsi kepentingan non-pengendali (NCI), ROE khusus pemegang saham induk membaik ke −3,73%.' : 'Excluding Non-Controlling Interests (NCI), Parent shareholders’ ROE improves to −3.73%, though still below Ke 8.45%.',
        },
        {
          label: id ? 'Grab 2025 (Konsol.)' : 'Grab 2025 (Consol.)',
          shortLabel: "Grab '25\nCons.",
          tone: 'emerald',
          margin: 5.93,
          marginDisp: '+5.93%',
          turnover: 0.28,
          turnoverDisp: '0.28x',
          leverage: 1.77,
          leverageDisp: '1.77x',
          roe: 2.96,
          roeDisp: '+2.96%',
          cause: id ? 'Meski perputaran aset Grab (0,28x) lebih rendah, margin bersih positif (+5,93%) membuat ROE positif +2,96%.' : 'Even with lower asset turnover (0.28x), Grab’s positive +5.93% net margin gives it positive +2.96% ROE.',
        },
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
          { label: '1.2 × X1 (WC / Assets)', val: 0.483, display: '+0.48', cause: id ? 'Modal kerja bersih Rp18,41T sangat sehat dibanding total aset (X1 positif kuat).' : 'Healthy Rp 18.41T working capital buffer supported by Rp 21.76T cash.' },
          { label: '1.4 × X2 (Ret. Earn.)', val: -6.588, display: '−6.59', warn: true, cause: id ? 'PENYEBAB UTAMA Z negatif: akumulasi rugi historis 2023 (hapus buku goodwill Tokopedia Rp78,8T).' : 'MAIN DRIVER of negative Z-score: sunk 2023 Tokopedia Rp 78.8T goodwill write-off carried in Retained Earnings.' },
          { label: '3.3 × X3 (EBIT / Assets)', val: -0.027, display: '−0.03', cause: id ? 'EBIT hampir impas (−Rp378M), hanya menyumbang sedikit angka negatif pada Z-Score.' : 'Near-breakeven EBIT (−Rp 378B) barely pulls the Z-Score down anymore.' },
          { label: '0.6 × X4 (Book Eq / Liab)', val: 1.008, display: '+1.01', cause: id ? 'Ekuitas Rp28,7T jauh melampaui total liabilitas Rp17,1T (solvabilitas jangka panjang aman).' : 'Strong equity base (Rp 28.7T) vs. total liabilities (Rp 17.1T) keeps solvency healthy.' },
          { label: '1.0 × X5 (Rev / Assets)', val: 0.400, display: '+0.40', cause: id ? 'Perputaran aset 0,40x (lebih tinggi dari Grab 0,28x) menambah +0,40 ke skor.' : 'Asset turnover of 0.40x (above Grab’s 0.28x) adds a solid +0.40 to the score.' },
          { label: 'Total Z (Book / Market)', val: -4.72, display: '−4.72 / −4.80', accent: true, cause: id ? 'Tampak "bangkrut" hanya karena rugi lama X2 (−6,59); empat komponen lain justru positif (+1,86).' : 'Screams "distress" purely from sunk X2 (−6.59); the other 4 components sum to a healthy +1.86.' },
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
            note: id ? 'Aset lancar 2024 belum memasukkan Rp1,58T pinjaman GoPay Catatan 7.' : '2024 Current Assets accidentally omitted Rp 1.58T of Note 7 GoPay loans.',
            bars: [
              { label: '2023', val: 2.62, display: '2.62x', cause: id ? 'Rasio lancar 2023 sebelum dekonsolidasi Tokopedia.' : '2023 Current Ratio prior to Tokopedia deconsolidation.' },
              { label: '2024', val: 2.46, display: '2.46x', warn: true, cause: id ? 'Terlalu rendah karena Rp1,58T piutang GoPay Catatan 7 terlewat (direvisi jadi 2,62x).' : 'Understated because Rp 1.58T Note 7 GoPay loans were left out (restated to 2.62x).' },
              { label: '2025', val: 2.73, display: '2.73x', accent: true, cause: id ? 'Didukung kas Rp21,76T (hampir 3x aset lancar dibanding utang jangka pendek).' : 'Backed by Rp 21.76T cash cushion covering short-term obligations nearly 3x.' },
            ],
          },
          {
            title: id ? 'Utang / Ekuitas' : 'Debt / Equity',
            delta: id ? 'Tanpa sewa' : 'Excl. leases',
            tone: 'warn',
            note: id ? 'Dek lama 2023–2024 belum memasukkan liabilitas sewa (IFRS 16).' : 'Old 2023–2024 figures omitted lease liabilities (IFRS 16).',
            bars: [
              { label: '2023', val: 9.69, display: '9.69%', warn: true, cause: id ? 'Hanya menghitung pinjaman bank tanpa liabilitas sewa.' : 'Counted bank borrowings only without IFRS 16 lease obligations.' },
              { label: '2024', val: 12.57, display: '12.57%', warn: true, cause: id ? 'Belum memasukkan sewa; setelah sewa dimasukkan menjadi 15,85%.' : 'Excludes leases; rises to 15.85% once full lease debt is included.' },
              { label: '2025', val: 26.97, display: '26.97%', accent: true, cause: id ? 'Naik karena pinjaman bank baru FY25 (+Rp3,72T), tetap tergolong rendah.' : 'Lifted by +Rp 3.72T new FY25 bank borrowings, still very conservative overall.' },
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
            { label: '2024', val: 2.62, display: '2.62x', cause: id ? 'Direvisi naik dari 2,46x setelah memulihkan Rp1,58T pinjaman GoPay Catatan 7 ke Aset Lancar.' : 'Restated up from 2.46x after restoring Rp 1.58T of Note 7 GoPay loans into Current Assets.' },
            { label: '2025', val: 2.73, display: '2.73x', accent: true, cause: id ? 'Naik ke 2,73x berkat kas Rp21,76T & modal kerja Rp18,41T (hampir 3x lipat utang lancar).' : 'Rose to 2.73x backed by Rp 21.76T cash & Rp 18.41T working capital (nearly 3x short-term bills).' },
          ],
        },
        {
          title: id ? 'Utang / Ekuitas' : 'Debt / Equity',
          delta: '+11.12% YoY',
          tone: 'accent',
          note: id ? 'Pinjaman bank baru FY25 (+Rp3,72T) naikkan rasio utang.' : 'New FY25 bank borrowings (+Rp3.72T) lifted full debt+lease ratio.',
          bars: [
            { label: '2024', val: 15.85, display: '15.85%', cause: id ? 'Sudah memasukkan liabilitas sewa IFRS 16 (naik dari angka dek lama 12,57% tanpa sewa).' : 'Includes full IFRS 16 lease liabilities (up from old deck’s 12.57% ex-leases).' },
            { label: '2025', val: 26.97, display: '26.97%', amber: true, cause: id ? 'Naik akibat pinjaman bank baru FY25 (+Rp3,72T), tapi rasio 27% masih tergolong rendah.' : 'Increased due to +Rp 3.72T new FY25 bank borrowings, though 27% leverage remains low.' },
          ],
        },
        {
          title: id ? 'DSO Piutang' : 'Trade DSO',
          delta: '+0.34d YoY',
          tone: 'pos',
          note: id ? 'Koreksi salah klasifikasi Cat. 6 vs Cat. 7 (46,9h → 10,6h); di 2025 naik tipis +0,34h.' : 'Fixed our earlier Note 6 vs Note 7 mix-up (46.9d → 10.6d); 2025 edged up +0.34d.',
          bars: [
            { label: '2024', val: 10.56, display: '10.6d', cause: id ? 'Memisahkan piutang usaha Catatan 6 saja (Rp460M) memperbaiki salah hitung lama 46,9h.' : 'Separated Note 6 trade receivables only (Rp 460B), fixing our earlier 46.9d mix-up.' },
            { label: '2025', val: 10.90, display: '10.9d', accent: true, cause: id ? 'Naik tipis +0,34 hari ke 10,9 hari; penagihan dari pelanggan masih sangat cepat.' : 'Edged up slightly (+0.34d) to 10.9 days — customer cash collection remains super fast.' },
          ],
        },
        {
          title: id ? 'Utang Usaha (DPO)' : 'Payables (DPO)',
          delta: '−2.0d YoY',
          tone: 'pos',
          note: id ? 'GoTo membayar pemasok dalam ~59 hari, menjaga kas tetap di dalam.' : 'GoTo pays suppliers in ~59 days, keeping cash inside the business longer.',
          bars: [
            { label: '2024', val: 61.1, display: '61.1d', cause: id ? 'Rata-rata tempo pembayaran GoTo ke pemasok sekitar 61 hari pasca-exit Tokopedia.' : 'GoTo took ~61 days on average to pay suppliers right after Tokopedia exit.' },
            { label: '2025', val: 59.1, display: '59.1d', accent: true, cause: id ? 'Lebih cepat 2 hari ke 59,1 hari, masih memberi kelonggaran kredit ~2 bulan.' : '2 days shorter at 59.1 days, still giving GoTo nearly 2 months of supplier credit.' },
          ],
        },
        {
          title: id ? 'Siklus Kas (CCC)' : 'Cash Conversion (CCC)',
          delta: id ? 'Negatif (Sehat)' : 'Negative (Strong)',
          tone: 'pos',
          note: id ? 'Kas masuk 47,5 hari lebih cepat sebelum GoTo membayar pemasok.' : 'Cash arrives 47.5 days before GoTo has to pay suppliers.',
          bars: [
            { label: '2024', val: 49.2, display: '−49.2d', goodNeg: true, cause: id ? 'Kas pelanggan masuk ~49 hari sebelum tagihan pemasok jatuh tempo.' : 'Customer cash arrived ~49 days before supplier bills came due.' },
            { label: '2025', val: 47.5, display: '−47.5d', accent: true, goodNeg: true, cause: id ? 'Tetap negatif kuat (−47,5h): pemasok ikut membantu membiayai modal kerja GoTo.' : 'Still strongly negative (−47.5d): suppliers effectively help finance GoTo’s working capital.' },
          ],
        },
        {
          title: 'Times Interest Earned',
          delta: '+3.83x YoY',
          tone: 'warn',
          note: id ? 'Rugi EBIT menyusut (−Rp2,24T → −Rp378M) vs bunga Rp535M.' : 'Narrowing EBIT loss (−Rp2.24T → −Rp378B) vs Rp535B interest.',
          bars: [
            { label: '2024', val: 4.54, display: '−4.54x', warn: true, cause: id ? 'Rugi EBIT besar (−Rp2,24T) membuat cakupan bunga sangat negatif (−4,54x).' : 'Large −Rp 2.24T EBIT loss meant operating profit couldn’t cover interest (−4.54x).' },
            { label: '2025', val: 0.71, display: '−0.71x', warn: true, cause: id ? 'Rugi EBIT menyusut tajam ke −Rp378M vs beban bunga Rp535M; hampir menutup bunga.' : 'EBIT loss narrowed to −Rp 378B vs Rp 535B interest — almost breakeven on coverage.' },
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
        { label: id ? 'CFO FY2025' : 'FY2025 Operating CF', val: 307.0, display: '+307.0B', accent: true, cause: id ? 'Akhirnya positif berkat efisiensi biaya pasca-Tokopedia, tapi baru menutup 26% kebutuhan CapEx.' : 'Finally turned positive after post-Tokopedia cost cuts, but still only covers 26% of ongoing CapEx.' },
        { label: id ? 'CapEx Tunai FY2025' : 'FY2025 Cash CapEx', val: -1182.4, display: '−1,182.4B', cause: id ? 'Belanja rutin aplikasi, server & software (6,45% pendapatan) — terpisah dari biaya deal 2024.' : 'Normal ongoing app, server, and software spending (6.45% of revenue), separate from 2024’s deal.' },
        { label: id ? 'Arus Kas Bebas (FCF)' : 'FY2025 Free Cash Flow', val: -875.3, display: '−875.3B', warn: true, cause: id ? 'CFO (+Rp307M) dikurangi CapEx (Rp1.182M) = −Rp875M; bisnis inti masih membakar kas.' : 'Operating CF (+Rp 307B) minus CapEx (Rp 1,182B) = −Rp 875B; GoTo still burns cash overall.' },
        { label: id ? 'Pencairan Deposito' : 'Time Deposit Maturities', val: 1386.5, display: '+1,386.5B', cause: id ? 'Pencairan deposito bank GoTo sendiri — sekadar pindah rekening, BUKAN laba operasional baru.' : 'GoTo’s own bank depositos maturing — moving cash from one pocket to another, NOT new business profit.' },
        { label: id ? 'CFI Inti (Ex-Deposito)' : 'Core CFI (Ex-Deposits)', val: -867.4, display: '−867.4B', cause: id ? 'Arus kas investasi riil setelah deposito bank (+Rp1,39T) dikeluarkan agar kas masuk tidak tampak semu.' : 'True investing cash outflow once maturing bank deposits (+Rp 1,386.5B) are stripped out.' },
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
          { label: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth', val: 11.4, display: '11.40%', cause: id ? 'Rata-rata terdistorsi dekonsolidasi Tokopedia pada 2023–2024.' : '3-year average pulled down by Tokopedia deconsolidation revenue drop.' },
          { label: 'COGS / Revenue', val: 41.1, display: '41.10%', cause: id ? 'Mencampur struktur biaya e-commerce 2023 dengan pasca-exit 2024–2025.' : 'Blends 2023 e-commerce cost structure with post-exit 2024–2025.' },
          { label: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue', val: 78.5, display: '78.50%', warn: true, cause: id ? 'Lonjakan buatan akibat memasukkan OpEx berat Tokopedia 2023 (>100%).' : 'Artificially inflated by including heavy 2023 pre-exit Tokopedia OpEx (>100%).' },
          { label: 'CapEx / Revenue', val: 16.3, display: '16.30%', warn: true, cause: id ? 'Terdongkrak aset takberwujud 1x Tokopedia Rp5,46T pada tahun 2024.' : 'Inflated by 2024’s one-time Rp 5.46T Tokopedia separation intangibles.' },
        ],
      }
    }
    return {
      type: 'horizontal',
      title: id ? 'Laporan Akhir: Asumsi Base Case (Pasca-Exit, Tanpa 2023)' : 'Current Final Report: Base Case Drivers (Post-Exit, Ex-2023)',
      subtitle: id ? 'Berbasis murni pada lintasan operasional pasca-Tokopedia 2024–2025' : 'Anchored strictly on clean post-Tokopedia 2024–2025 continuing operations',
      unit: '%',
      items: [
        { label: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth', val: 15.27, display: '15.27%', accent: true, cause: id ? 'Pertumbuhan organik pasca-exit FY2025 (+15,27%): Gojek + GoPay + Service Fee.' : 'Pure FY2025 post-exit organic revenue growth (+15.27%) without 2023 noise.' },
        { label: 'COGS / Revenue', val: 42.28, display: '42.28%', cause: id ? 'Rasio beban pokok FY2025 yang mencerminkan margin kotor 57,7% pasca-Tokopedia.' : 'Audited FY2025 COGS ratio reflecting GoTo’s cleaner 57.7% post-exit gross margin.' },
        { label: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue', val: 55.70, display: '55.70%', accent: true, cause: id ? 'Turun dari 78,5% karena beban 2023 dikeluarkan (FY25: 55,70%, masih konservatif vs 1H26 51,2%).' : 'Dropped from 78.5% after removing 2023; anchored on FY25 55.70% (1H26 ran even leaner at 51.2%).' },
        { label: 'CapEx / Revenue', val: 6.45, display: '6.45%', cause: id ? 'Belanja modal berkelanjutan riil FY2025 (konsisten dengan 2024 bersih 6,63%).' : 'True ongoing FY2025 CapEx intensity (matching clean continuing 2024 at 6.63%).' },
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
          { label: id ? '2026F EBIT (Dek Lama)' : '2026F EBIT (Old 3-Yr)', val: -3854.0, display: '−3,854B', warn: true, cause: id ? 'Dipicu asumsi OpEx 78,5% yang membawa kerugian 2023 ke dalam proyeksi.' : 'Driven by 78.5% OpEx assumption carrying 2023 pre-exit losses forward.' },
          { label: id ? '2027F EBIT (Dek Lama)' : '2027F EBIT (Old 3-Yr)', val: -4376.0, display: '−4,376B', warn: true, cause: id ? 'Skala pendapatan tumbuh tapi margin tetap negatif karena beban 2023 masih terbawa.' : 'Higher revenue multiplied by negative margin keeps EBIT sinking further.' },
          { label: id ? '2028F EBIT (Dek Lama)' : '2028F EBIT (Old 3-Yr)', val: -4967.4, display: '−4,967B', warn: true, cause: id ? 'Rugi operasi melebar hampir −Rp5T sebelum koreksi pasca-Tokopedia.' : 'Operating loss balloons toward −Rp 5T before removing 2023 distortions.' },
          { label: id ? '2028F Laba Bersih' : '2028F Net Income', val: -4347.9, display: '−4,348B', warn: true, cause: id ? 'Proyeksi rugi bersih terus membengkak dan menggerus ekuitas.' : 'Compounding operating losses pull bottom-line Net Income deeply negative.' },
          { label: id ? '2028F Kas Akhir' : '2028F Ending Cash', val: 968.0, display: '+968B', cause: id ? 'Kas Rp21,8T habis terkuras secara semu akibat asumsi CapEx 16,3% & rugi 78,5% OpEx.' : 'Artificially drains GoTo’s Rp 21.8T cash down to Rp 968B due to 78.5% OpEx & 16.3% CapEx.' },
        ],
      }
    }
    return {
      type: 'diverging',
      title: id ? 'Laporan Akhir: Skenario Proyeksi 2026F–2028F (Pasca-Exit)' : 'Current Final Report: 2026F–2028F Scenarios (Post-Exit)',
      subtitle: id ? 'Base Case berbalik EBIT positif (+Rp567M) & menjaga kas Rp19,42T; Optimis 1H26 +Rp3,22T' : 'Base Case turns EBIT-positive (+Rp567B) & preserves Rp19.4T cash; 1H26 Opt hits +Rp3.22T',
      unit: 'Rp bn',
      items: [
        { label: id ? '2028F EBIT Konservatif' : 'Conservative 2028F EBIT', val: -2143.4, display: '−2,143B', warn: true, cause: id ? 'Skenario stres jika perang promo Grab/Shopee kembali memaksa OpEx naik ke ~60%.' : 'Downside stress test if renewed Grab/Shopee promo wars push Cash OpEx back near 60%.' },
        { label: id ? '2026F EBIT Base' : 'Base 2026F EBIT', val: 426.9, display: '+426.9B', cause: id ? 'Berbalik positif dari −Rp378M (2025) seiring skala pendapatan +15% & OpEx 55,7%.' : 'Flips positive from −Rp 378B (2025) as +15% revenue scale meets 55.7% Cash OpEx.' },
        { label: id ? '2028F EBIT Base' : 'Base 2028F EBIT', val: 567.2, display: '+567.2B', accent: true, cause: id ? 'EBIT berbalik positif +Rp567M, namun ROIC (2,70%) masih jauh di bawah WACC (7,76%).' : 'Turns EBIT-positive (+Rp 567B), but ROIC (2.70%) still trails WACC (7.76%) by 5.06%.' },
        { label: id ? '2028F NI Base' : 'Base 2028F Net Income', val: 25.0, display: '+25.0B', cause: id ? 'Laba bersih hampir impas (+Rp25M) karena beban bunga & pajak masih menggerus EBIT.' : 'Net Income barely breaks even (+Rp 25B) as interest and taxes absorb most of EBIT.' },
        { label: id ? '2028F EBIT Optimis 1H26' : 'Optimistic 2028F EBIT', val: 3221.1, display: '+3,221B', accent: true, cause: id ? 'Jika efisiensi 1H26 (Cash OpEx 51,2%) bertahan penuh 3 tahun, EBIT melonjak ke +Rp3,22T.' : 'Shows upside if 1H26 lean run-rate (51.2% Cash OpEx) sustains across 2026F–2028F.' },
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
        { label: id ? 'Imbal Hasil SUN 10Y' : 'ID 10Y Bond Yield', val: 6.12, display: '6.120%', cause: id ? 'Imbal hasil obligasi pemerintah RI 10 tahun per 30 Des 2025 (masih memuat risiko gagal bayar negara).' : 'Indonesia 10-year government bond yield on Dec 30, 2025 (before stripping default spread).' },
        { label: id ? 'IDR Risk-Free (Rf)' : 'IDR Risk-Free (Rf)', val: 4.502, display: '4.502%', cause: id ? 'SUN 10Y (6,120%) dikurangi Default Spread Indonesia Damodaran (1,618%) = 4,502%.' : 'ID 10Y Bond Yield (6.120%) minus Damodaran Baa2 sovereign default spread (1.618%).' },
        { label: id ? 'Biaya Ekuitas (Ke)' : 'Cost of Equity (Ke)', val: 8.452, display: '8.452%', accent: true, cause: id ? 'CAPM: Rf 4,502% + Beta (0,59) × Total ERP Indonesia (6,70%) = 8,452% batas minimal ROE.' : 'CAPM: Rf (4.502%) + Beta (0.59) × Indonesia Total ERP (6.70%) = 8.452% shareholder hurdle.' },
        { label: id ? 'Biaya Utang Setelah Pajak' : 'After-Tax Kd (22% tax)', val: 5.39, display: '5.390%', cause: id ? 'Bunga utang efektif 6,91% (Catatan 27b/19-20) dikali (1 − tarif pajak 22%).' : 'Effective borrowing rate (6.91% from Notes 19–20/27b) × (1 − 22% statutory tax rate).' },
        { label: 'Base WACC', val: 7.761, display: '7.761%', accent: true, cause: id ? 'Rata-rata tertimbang: 77,4% Ekuitas (8,45%) + 22,6% Utang (5,39%) = batas minimum ROIC.' : 'Weighted hurdle: 77.4% Equity (8.45%) + 22.6% Debt (5.39%); GoTo must beat 7.76% ROIC to create value.' },
        { label: id ? 'WACC Tanpa Tax Shield' : 'WACC (0% Tax Shield)', val: 8.101, display: '8.101%', cause: id ? 'Uji sensitivitas jika rugi pajak membuat GoTo belum menikmati penghematan pajak bunga.' : 'Stress check assuming GoTo’s accumulated tax losses mean zero immediate debt tax shield.' },
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
          { label: id ? 'DCF Dek Lama (3 Thn)' : 'Previous DCF (3-Yr Avg)', val: -121.1, display: '−Rp121.10', warn: true, cause: id ? 'Negatif tajam akibat proyeksi OpEx 78,5% & CapEx 16,3% dari data pra-exit 2023.' : 'Deeply negative due to 78.5% OpEx & 16.3% CapEx distorted by 2023 Tokopedia data.' },
          { label: id ? 'RI Dek Lama (3 Thn)' : 'Previous RI (3-Yr Avg)', val: -75.1, display: '−Rp75.10', warn: true, cause: id ? 'Rugi terus-menerus membuat Residual Income jauh di bawah biaya ekuitas 8,45%.' : 'Projected perpetual losses drag Residual Income far below zero.' },
          { label: id ? 'Kas Bersih / Saham' : 'Net Cash Floor / sh', val: 13.19, display: '+Rp13.19', accent: true, cause: id ? 'Kas Rp21,76T − Utang Rp7,74T = Rp14,01T kas bersih riil (Rp13,19 per lembar).' : 'Cash (Rp 21.76T) minus Debt (Rp 7.74T) = Rp 14.01T net cash floor per share.' },
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
        { label: id ? 'Base RI (g = 3,0%)' : 'Base RI (g = 3.0%)', val: -12.23, display: '−Rp12.23', cause: id ? 'Mengasumsikan defisit laba (ROE 0,09% vs. Ke 8,45%) terus membesar 3% selamanya pasca-2028 (TV = 85,0% PV). Penalti −Rp41,7T ini menggerus habis ekuitas buku Rp28,7T.' : 'Assumes GoTo’s profit shortfall (0.09% ROE vs. 8.45% Ke) keeps growing 3% bigger forever after 2028 (TV = 85.0% of PV). That −Rp 41.7T compounding penalty wipes out Rp 28.7T of book equity.' },
        { label: id ? 'Base RI (g = 0%)' : 'Base RI (g = 0%)', val: 0.24, display: '+Rp0.24', cause: id ? 'Model RI yang sama, tetapi menghentikan pertumbuhan defisit pasca-2028 (g = 0%). Mematikan g = 3% saja menaikkan nilai +Rp12,47/sh—bukti tingginya sensitivitas Terminal Value (85% PV).' : 'Same Residual Income model, but stops growing the post-2028 shortfall (g = 0%). Turning off 3% terminal growth alone swings fair value by +Rp 12.47/sh—showing how sensitive RI is to Terminal Value (85% of PV).' },
        { label: id ? 'Base DCF (Pasca-Exit)' : 'Base DCF (Post-Exit)', val: 10.38, display: '+Rp10.38', accent: true, cause: id ? 'Rp2,81/sh di bawah garis Kas Bersih Rp13,19 karena CapEx membuat FCF operasi tetap negatif (EV −Rp2,99T atau −Rp2,81/sh), menggerus kas bersih +Rp14,01T (+Rp13,19/sh).' : 'Stops Rp 2.81/sh below the Rp 13.19 Net Cash line because ongoing CapEx keeps core Free Cash Flow negative (EV −Rp 2.99T, or −Rp 2.81/sh), eating into GoTo’s +Rp 14.01T (+Rp 13.19/sh) cash pile.' },
        { label: id ? 'Kas Bersih / Saham' : 'Net Cash / Share', val: 13.19, display: '+Rp13.19', cause: id ? 'Batas bawah kas likuidasi (Kas Rp21,76T − Utang & sewa Rp7,74T = Rp14,01T). Jika operasi berhenti hari ini dan kas bersih dibagikan, tiap lembar saham ditopang Rp13,19.' : 'The liquidation cash floor (Rp 21.76T cash minus Rp 7.74T debt & leases = Rp 14.01T). If GoTo shut down operations today and returned net cash to shareholders, each share has Rp 13.19 behind it.' },
        { label: id ? 'RI Konvergensi Thn 4+' : 'RI (Yr4+ Convergence)', val: 21.13, display: '+Rp21.13', cause: id ? 'Skenario terbaik: mengasumsikan ROE GoTo menyamai Ke 8,45% mulai Thn 4 (2029+), sehingga RI pasca-2028 menjadi Rp0. Ekuitas buku Rp28,7T hanya dikurangi defisit 2026–2028 (+Rp21,13/sh—satu-satunya yang melampaui kas Rp13,19, namun masih di bawah Rp25).' : 'Best case: assumes GoTo finally catches up to its 8.45% ROE hurdle from Year 4 (2029+) onward, making post-2028 Residual Income Rp 0. Keeps Rp 28.7T book equity minus only 2026–2028 shortfalls (+Rp 21.13/sh—only scenario beating the Rp 13.19 cash floor, yet still below Rp 25).' },
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
        { label: id ? 'RI Konservatif' : 'Conservative RI', val: -44.42, display: '−Rp44.42', cause: id ? 'Skenario stres perang promo membuat ROE sangat negatif sehingga nilai ekuitas turun −Rp44,42.' : 'Downside stress if promo wars return — deeply negative ROE drags Residual Income to −Rp 44.42.' },
        { label: 'Base RI (g=3.0%)', val: -12.23, display: '−Rp12.23', cause: id ? 'ROE dasar (+0,09%) < Ke (8,45%) menyebabkan ekspansi terminal menggerus nilai buku.' : 'Base ROE (+0.09%) below Ke (8.45%) means growing below cost of equity erodes book value.' },
        { label: 'Base DCF (Floor)', val: 10.38, display: '+Rp10.38', accent: true, cause: id ? 'Batas bawah rentang wajar utama kami (+Rp10,38/sh), ditopang kuat oleh kas bersih Rp13,19/sh.' : 'Lower bound of our Defensible Range (+Rp 10.38/sh), anchored by GoTo’s net cash pile.' },
        { label: id ? 'Kas Bersih / Saham' : 'Net Cash / Share', val: 13.19, display: '+Rp13.19', cause: id ? 'Kas Rp21,76T dikurangi total utang & sewa Rp7,74T dibagi 1,06T lembar saham.' : 'Rp 21.76T cash minus Rp 7.74T debt & leases divided by 1.06T diluted shares.' },
        { label: 'Opt. RI (Ceiling)', val: 16.75, display: '+Rp16.75', accent: true, cause: id ? 'Batas atas rentang wajar (+Rp16,75/sh): jika efisiensi 1H26 bertahan — tetap −33% di bawah Rp25.' : 'Upper bound of our Defensible Range (+Rp 16.75/sh) under 1H26 efficiency — still 33% below Rp 25.' },
        { label: 'Opt. DCF (1H26)', val: 47.34, display: '+Rp47.34', cause: id ? 'Hanya tercapai jika OpEx 1H26 (51,2%) + g=3% bertahan selamanya tanpa perlawanan Grab/Shopee.' : 'Only reached if 1H26 ultra-lean OpEx (51.2%) lasts forever with zero competitive pushback.' },
        { label: 'Grab P/B (3.04x)', val: 91.02, display: '+Rp91.02', cause: id ? 'DITOLAK: Grab layak 3,04x P/B karena sudah untung (+2,96% ROE), sedangkan GoTo masih −5,23% ROE.' : 'REJECTED outlier: Grab earns 3.04x P/B because it is already profitable (+2.96% ROE vs. GoTo −5.23%).' },
      ],
    }
  }

  // Slide 12 & Slide 14: Recommendation & Reconciliation
  if (sn === 12 || sn === 14) {
    return {
      type: 'diverging',
      title: id ? 'Spread Ekonomi (ROIC vs. WACC) & Gap Harga Pasar' : 'Economic Return Spread (ROIC vs. WACC) & Valuation Gap',
      subtitle: id ? 'ROIC 2028F (+2,70%) tertinggal 5.06% di bawah WACC (7,76%) → SELL / AVOID di Rp25' : '2028F ROIC (+2.70%) trails WACC (7.76%) by 5.06% → SELL / AVOID holds at Rp25.00',
      unit: '%',
      items: [
        { label: '2028F Base ROIC', val: 2.70, display: '+2.70%', accent: true, cause: id ? 'Imbal hasil operasi proyeksi tahun 2028 sudah berbalik positif (+2,70%), bukti perbaikan operasional.' : 'Projected 2028F return on invested capital flips positive (+2.70%), proving real turnaround.' },
        { label: 'Base WACC Hurdle', val: 7.76, display: '7.76%', cause: id ? 'Biaya modal rata-rata tertimbang yang wajib dilampaui GoTo agar menciptakan nilai.' : 'Minimum blended cost of capital GoTo must beat to create economic value.' },
        { label: 'ROIC − WACC Spread', val: -5.06, display: '−5.06%', warn: true, cause: id ? 'Spread negatif −5,06% berarti pada 2028F GoTo masih menghancurkan nilai ekonomi → rekomendasi SELL.' : 'Negative −5.06% economic spread explains why SELL/AVOID holds even after Tokopedia exit.' },
        { label: '2028F Base ROE', val: 0.09, display: '+0.09%', cause: id ? 'Laba bersih 2028F (+Rp25M) nyaris nol dibanding ekuitas Rp28,7T.' : 'Base 2028F Net Income (+Rp 25B) yields barely +0.09% ROE on Rp 28.7T equity.' },
        { label: 'Cost of Equity (Ke)', val: 8.45, display: '8.45%', cause: id ? 'Kompensasi risiko minimum yang dituntut pemegang saham GoTo (CAPM).' : 'Minimum return required by equity investors given GoTo’s risk profile.' },
        { label: 'ROE − Ke Spread', val: -8.36, display: '−8.36%', warn: true, cause: id ? 'Spread ekuitas negatif −8,36% mengonfirmasi harga pasar Rp25 masih terlalu mahal vs nilai wajar.' : 'Negative −8.36% equity spread confirms Rp 25.00 market price outruns GoTo’s fundamentals.' },
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
          { label: 'Base Cash OpEx (%)', val: 78.5, display: '78.50%', warn: true, cause: id ? 'Salah memasukkan tahun 2023 sebelum pemisahan Tokopedia ke dalam rata-rata historis.' : 'Erroneously included pre-Tokopedia-exit 2023 in the 3-year historical average.' },
          { label: '2024 Raw CapEx (%)', val: 41.0, display: '41.00%', warn: true, cause: id ? 'Memasukkan Rp5,46T pembelian aset takberwujud 1x Tokopedia (Catatan 12) sebagai CapEx normal.' : 'Included Rp 5.46T one-time Tokopedia intangibles (Note 12) inside recurring CapEx.' },
          { label: '2024 Mixed DSO (d)', val: 46.88, display: '46.88d', warn: true, cause: id ? 'Mencampurkan pinjaman konsumen GoPay (Cat. 7) ke dalam piutang usaha (Cat. 6).' : 'Mixed GoPay consumer loans (Note 7) into trade receivables (Note 6).' },
          { label: '2024 Current Ratio', val: 2.46, display: '2.46x', cause: id ? 'Terlalu rendah karena lupa memasukkan Rp1,58T pinjaman lancar GoPay Catatan 7 ke Aset Lancar.' : 'Understated because Rp 1.58T of current Note 7 GoPay loans was omitted from Current Assets.' },
        ],
      }
    }
    return {
      type: 'horizontal',
      title: id ? 'Laporan Akhir: Angka Auditan Setelah 5 Koreksi' : 'Current Final Report: Audited Figures After 5 Fixes',
      subtitle: id ? 'Basis pasca-Tokopedia yang bersih tanpa distorsi 2023 & aset takberwujud' : 'Clean post-Tokopedia audited basis with zero 2023 or intangible distortions',
      unit: id ? 'Laporan Akhir' : 'Final Report',
      items: [
        { label: 'Base Cash OpEx (%)', val: 55.70, display: '55.70%', accent: true, cause: id ? 'Dibangun ulang dari biaya operasi kas FY2025 murni pasca-exit Tokopedia.' : 'Rebuilt strictly on clean FY2025 post-Tokopedia continuing Cash OpEx.' },
        { label: '2024 Cont. CapEx (%)', val: 6.63, display: '6.63%', cause: id ? 'Rp5,46T aset takberwujud 1x dikeluarkan; CapEx 2024 murni (6,63%) selaras dengan FY2025 (6,45%).' : 'Stripped out Rp 5.46T one-time intangibles; clean 2024 (6.63%) aligns with 2025 (6.45%).' },
        { label: '2024 Trade DSO (d)', val: 10.56, display: '10.56d', cause: id ? 'Memisahkan piutang usaha Catatan 6 saja (10,56h di 2024; 10,90h di 2025).' : 'Aligned strictly to Note 6 trade receivables (10.56d in 2024; 10.90d in 2025).' },
        { label: '2024 Current Ratio', val: 2.62, display: '2.62x', accent: true, cause: id ? 'Mengembalikan Rp1,58T piutang GoPay Catatan 7 ke Aset Lancar sehingga neraca 2024 cocok 100%.' : 'Restored Rp 1.58T of Note 7 GoPay loans to Current Assets, matching audited 2024 totals.' },
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
        parsed.push({ label: c.label, val: v, display: String(c.result), cause: c.formula ? `${c.formula} (${c.data_origin || 'Audited'})` : '' })
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
      { label: 'Base RI', val: -12.23, display: '−Rp12.23', cause: id ? 'ROE 2028F (0,09%) di bawah Ke (8,45%) menekan nilai Residual Income.' : '2028F ROE (0.09%) trailing Ke (8.45%) weighs on Residual Income.' },
      { label: 'Base DCF', val: 10.38, display: '+Rp10.38', accent: true, cause: id ? 'Nilai DCF dasar pasca-Tokopedia (+Rp10,38/sh), ditopang kas bersih.' : 'Post-Tokopedia Base DCF fair value (+Rp 10.38/sh), backed by net cash.' },
      { label: 'Net Cash / sh', val: 13.19, display: '+Rp13.19', cause: id ? 'Kas bersih Rp14,01T dibagi total saham terdilusi.' : 'Rp 14.01T net cash divided by total diluted shares.' },
      { label: 'Opt. RI Ceiling', val: 16.75, display: '+Rp16.75', accent: true, cause: id ? 'Batas atas rentang wajar (+Rp16,75/sh) dengan efisiensi 1H26.' : 'Upper bound of Defensible Range (+Rp 16.75/sh) using 1H26 cost efficiency.' },
      { label: 'Grab P/B Ref.', val: 91.02, display: '+Rp91.02', cause: id ? 'Ditolak karena Grab sudah untung (+2,96% ROE) sedangkan GoTo −5,23% ROE.' : 'Rejected outlier: Grab earns +2.96% ROE vs. GoTo −5.23% ROE.' },
    ],
  }
})

// Compute SVG geometry for diverging / horizontal / grouped charts
const svgChartData = computed(() => {
  const cfg = chartConfig.value
  if (cfg.type === 'dupont_3step') {
    const marginMaxNeg = 40
    const marginMaxPos = 15
    const marginSpan = marginMaxNeg + marginMaxPos
    const marginZeroPct = (marginMaxNeg / marginSpan) * 100

    const roeMaxNeg = 22
    const roeMaxPos = 10
    const roeSpan = roeMaxNeg + roeMaxPos
    const roeZeroPct = (roeMaxNeg / roeSpan) * 100

    const multMax = 2.0

    const rows = (cfg.rows || []).map((r) => {
      const mW = (Math.abs(r.margin) / marginSpan) * 100
      const mLeft = r.margin < 0 ? marginZeroPct - mW : marginZeroPct
      const rW = (Math.abs(r.roe) / roeSpan) * 100
      const rLeft = r.roe < 0 ? roeZeroPct - rW : roeZeroPct
      return {
        ...r,
        marginBarLeft: `${Math.max(0, mLeft).toFixed(2)}%`,
        marginBarWidth: `${Math.max(2, mW).toFixed(2)}%`,
        roeBarLeft: `${Math.max(0, rLeft).toFixed(2)}%`,
        roeBarWidth: `${Math.max(2, rW).toFixed(2)}%`,
        turnoverHeight: `${Math.max(10, Math.round((r.turnover / multMax) * 100))}%`,
        leverageHeight: `${Math.max(10, Math.round((r.leverage / multMax) * 100))}%`,
      }
    })
    return {
      mode: 'dupont_3step',
      marginZeroPct: `${marginZeroPct.toFixed(2)}%`,
      roeZeroPct: `${roeZeroPct.toFixed(2)}%`,
      rows,
    }
  }
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
    2: id ? `Perubahan Segmen YoY (${span} · Appendix A1)` : `Segment YoY Trajectory (${span} · Appendix A1)`,
    3: id ? `Tekanan Biaya & Risiko Kredit YoY (${span} · Appendix A1)` : `Competitive Cost & Credit Risk YoY (${span} · Appendix A1)`,
    4: id ? `Perubahan Rasio & DuPont YoY (${span} · Appendix A2)` : `Year-over-Year DuPont & Margin Trajectory (${span} · Appendix A2)`,
    5: id ? `Perubahan Likuiditas & Solvabilitas YoY (${span} · Appendix A3)` : `Year-over-Year Liquidity & Leverage Movement (${span} · Appendix A3)`,
    6: id ? `Perubahan Kualitas Laba & Arus Kas YoY (${span} · Appendix A3)` : `Year-over-Year Cash Flow & Accrual Quality (${span} · Appendix A3)`,
    7: id ? `Lintasan Historis YoY di Balik Asumsi Driver (${span1H} · Appendix A4)` : `Historical YoY Driver Trajectory Behind Forecast Inputs (${span1H} · Appendix A4)`,
    8: id ? 'Lintasan Proyeksi Base Case (2025A → 2028F · Appendix A5)' : 'Restated Base Forecast Trajectory (2025A → 2028F · Appendix A5)',
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
          { yr: '2024', val: '+Rp69.4B', pct: 8, cause: id ? 'Baru saja menyentuh impas positif pasca-restrukturisasi awal & keluar Vietnam.' : 'Barely reached positive EBIT (+Rp 69.4B) right after early restructuring & Vietnam exit.' },
          { yr: '2025', val: '+Rp888.6B', pct: 100, current: true, cause: id ? 'Lonjakan +1.180% didorong efisiensi insentif (−Rp504M), cloud >50%, & take-rate 3P.' : 'Jumped 12.8x (+1,180%) from −Rp 504B incentive cuts, >50% cloud savings & 3P take-rate growth.' },
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
          { yr: '2024', val: 'Rp2.98T', pct: 57, cause: id ? 'Skala awal kredit konsumen GoPay sebesar Rp1,58T dengan rugi segmen −Rp1,11T.' : 'Early consumer-lending ramp (Rp 1.58T loan book) while segment still lost −Rp 1.11T.' },
          { yr: '2025', val: 'Rp5.19T', pct: 100, current: true, cause: id ? 'Menyumbang 90,96% pertumbuhan pendapatan grup saat pinjaman melonjak +72,6% ke Rp2,73T.' : 'Drove 90.96% of total group revenue growth as loans surged +72.6% to Rp 2.73T.' },
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
          { yr: '2023*', val: 'Rp14.79T', pct: 81, cause: id ? 'Basis pra-exit yang masih mencakup Tokopedia sebelum dekonsolidasi Jan 2024.' : 'Pre-exit reported base still including Tokopedia before Jan 2024 deconsolidation.' },
          { yr: '2024', val: 'Rp15.89T', pct: 87, cause: id ? 'Tahun pertama pasca-Tokopedia: tumbuh moderat +7,5% dengan service fee baru.' : 'First post-Tokopedia year: grew a modest +7.5% with the new e-commerce service fee.' },
          { yr: '2025', val: 'Rp18.32T', pct: 100, current: true, cause: id ? 'Kecepatan tumbuh berlipat dua ke +15,27%, didorong GoPay +74% & Gojek +14%.' : 'Growth more than doubled to +15.27%, led by GoPay (+74%) and Gojek (+14%).' },
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
          { yr: '2023*', val: '−Rp10.28T', pct: 100, cause: id ? 'Rugi operasi raksasa sebelum exit akibat subsidi bakar uang & beban penuh Tokopedia.' : 'Massive pre-exit operating loss from Tokopedia’s heavy subsidies & cash burn.' },
          { yr: '2024', val: '−Rp2.24T', pct: 28, cause: id ? 'Pemangkasan rugi 78% langsung setelah Tokopedia didekonsolidasi pada 2024.' : 'Loss plunged 78% right after deconsolidating Tokopedia’s cash-burning operations.' },
          { yr: '2025', val: '−Rp378B', pct: 10, current: true, cause: id ? 'Laba Gojek (+Rp889M) + Tokopedia Fee (+Rp572M) nyaris menutup biaya korporasi (−Rp1,44T).' : 'Gojek (+Rp 889B) + Tokopedia Fee (+Rp 572B) almost offset corporate overhead (−Rp 1.44T).' },
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
          { yr: '2024', val: 'Rp173.6B', pct: 43, cause: id ? 'Cadangan kredit macet awal saat portofolio pinjaman GoPay masih Rp1,58T.' : '2024 bad-debt buffer when net GoPay consumer loans stood at Rp 1.58T.' },
          { yr: '2025', val: 'Rp407.7B', pct: 100, current: true, cause: id ? 'Melonjak +134,9% — hampir 2x lebih cepat dari kenaikan pinjaman (+72,6%), bukti risiko kredit naik.' : 'Surged +134.9% — nearly 2x faster than loan growth (+72.6%), signaling rising credit risk.' },
        ],
      },
      {
        title: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue',
        delta: '−7.08% YoY',
        tone: 'pos',
        note: id
          ? 'Disiplin promo memangkas bakar kas, tetapi rivalitas batasi harga.'
          : 'Promo discipline narrowed burn, but rivalry caps pricing power.',
        bars: [
          { yr: '2023*', val: '117.0%', pct: 100, cause: id ? 'Beban operasi pra-exit melebihi pendapatan (117%) akibat perang subsidi e-commerce.' : 'Pre-exit OpEx exceeded 100% of revenue due to Tokopedia subsidy battles.' },
          { yr: '2024', val: '62.78%', pct: 54, cause: id ? 'Turun drastis ke 62,8% pasca-exit, meski S&M & promo tetap besar untuk lawan Grab.' : 'Fell sharply to 62.8% post-Tokopedia, though competitive S&M remained heavy.' },
          { yr: '2025', val: '55.70%', pct: 48, current: true, cause: id ? 'Disiplin insentif memangkas rasio −7,08%, tapi rivalitas menjaga S&M tetap Rp3,09T.' : 'Promo & headcount discipline cut −7.08%, yet rivalry keeps S&M at Rp 3.09T.' },
        ],
      },
    ]
  }

  if (sn === 4) {
    return [
      {
        title: id ? 'Margin Operasi (EBIT %)' : 'Operating Margin (EBIT %)',
        delta: '+12.04% YoY',
        tone: 'warn',
        note: id
          ? 'Efisiensi insentif & cloud mengangkat margin inti ke ambang impas.'
          : 'Incentive cuts & cloud savings lifted core margin near breakeven.',
        bars: [
          { yr: '2023*', val: '−69.5%', pct: 100, cause: id ? 'Margin tertekan hebat sebelum pemisahan Tokopedia.' : 'Deeply underwater before separating Tokopedia’s heavy OpEx.' },
          { yr: '2024', val: '−14.10%', pct: 32, cause: id ? 'Lonjakan perbaikan +55 poin setelah keluar dari e-commerce berbiaya tinggi.' : 'Massive +55 pp rebound immediately after exiting high-burn e-commerce.' },
          { yr: '2025', val: '−2.06%', pct: 10, current: true, cause: id ? 'Mendekati impas (−Rp378M EBIT) berkat efisiensi insentif & cloud.' : 'Nearly breakeven (−Rp 378B EBIT) thanks to incentive discipline & cloud savings.' },
        ],
      },
      {
        title: id ? 'Margin Laba Bersih' : 'Net Profit Margin',
        delta: '+26.18% YoY',
        tone: 'warn',
        note: id
          ? 'Rugi bersih menyusut, namun kompensasi berbasis saham Rp593B & bunga masih membebani.'
          : 'Bottom line improved sharply, yet Rp593B share-based compensation & finance costs weigh.',
        bars: [
          { yr: '2023*', val: '−612.2%', pct: 100, cause: id ? 'Terdistorsi penghapusan goodwill Tokopedia Rp78,8T (non-tunai) di bawah EBIT.' : 'Distorted by the non-cash Rp 78.8T Tokopedia goodwill write-off below EBIT.' },
          { yr: '2024', val: '−34.38%', pct: 28, cause: id ? 'Rugi bersih menyempit ke −Rp5,47T di tahun pertama pasca-exit.' : 'Net loss narrowed to −Rp 5.47T in the first full post-exit year.' },
          { yr: '2025', val: '−8.20%', pct: 11, current: true, cause: id ? 'Naik +26,2% ke −8,20%, namun beban SBC (Rp593M) & bunga masih menahan laba.' : 'Improved +26.2% to −8.20%, still weighed down by Rp 593B SBC & finance costs.' },
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
          { yr: '2023*', val: '0.27x', pct: 68, cause: id ? 'Basis aset lama masih terbebani goodwill raksasa sebelum penghapusan buku.' : 'Pre-exit asset base weighed down by bloated goodwill before write-off.' },
          { yr: '2024', val: '0.37x', pct: 92, cause: id ? 'Efisiensi aset langsung naik setelah goodwill Tokopedia keluar (aset Rp43,21T).' : 'Asset efficiency jumped post-exit on audited Rp 43.21T asset base.' },
          { yr: '2025', val: '0.40x', pct: 100, current: true, cause: id ? 'Pendapatan +15,3% mendorong ATO ke 0,40x — kini mengungguli Grab (0,28x).' : '+15.3% revenue scale pushed ATO to 0.40x, beating peer Grab (0.28x).' },
        ],
      },
      {
        title: id ? 'ROE Konsolidasian (vs Grab +2,96%)' : 'Cons. ROE (vs Grab +2.96%)',
        delta: '+12.74% YoY',
        tone: 'warn',
        note: id
          ? 'Leverage moderat (1,59x) belum membantu saat margin masih negatif.'
          : 'Higher EM (1.59x) still amplifies negative margins below Ke (8.45%).',
        bars: [
          { yr: '2023*', val: '−253.4%', pct: 100, cause: id ? 'Hapus buku goodwill Rp78,8T menggerus ekuitas dan menjatuhkan ROE ke −253,4%.' : 'Rp 78.8T goodwill write-off hammered equity and pushed ROE to −253.4%.' },
          { yr: '2024', val: '−17.97%', pct: 30, cause: id ? 'Membaik tajam ke −17,97% begitu distorsi non-tunai 2023 berlalu.' : 'Improved dramatically to −17.97% once non-cash 2023 write-offs cleared.' },
          { yr: '2025', val: '−5.23%', pct: 12, current: true, cause: id ? 'Naik ke −5,23% konsolidasi (−3,73% induk), namun masih kalah dari Grab (+2,96%) & Ke (8,45%).' : 'Reached −5.23% cons. (−3.73% parent), still trailing Grab (+2.96%) and Ke (8.45%).' },
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
          { yr: '2023*', val: '2.62x', pct: 87, cause: id ? 'Posisi likuiditas kas jangka pendek sudah cukup tebal sebelum exit.' : 'Short-term cash buffer was already solid pre-exit.' },
          { yr: '2024', val: '2.62x', pct: 87, cause: id ? 'Direvisi dari 2,46x ke 2,62x setelah memulihkan Rp1,58T pinjaman GoPay Catatan 7.' : 'Restated up from 2.46x to 2.62x after restoring Rp 1.58T Note 7 GoPay loans.' },
          { yr: '2025', val: '2.73x', pct: 91, current: true, cause: id ? 'Naik ke 2,73x didukung kas Rp21,76T dan modal kerja bersih Rp18,41T.' : 'Improved to 2.73x backed by Rp 21.76T cash & Rp 18.41T working capital.' },
        ],
      },
      {
        title: id ? 'Piutang Usaha DSO (Cat. 6)' : 'Trade DSO (Note 6)',
        delta: '+0.34d YoY',
        tone: 'pos',
        note: id
          ? 'Koreksi salah klasifikasi Cat. 6 vs Cat. 7 (46,88h → 10,56h); di 2025 naik tipis +0,34h.'
          : 'Fixed our earlier Note 6 vs Note 7 mix-up (46.88d → 10.56d); 2025 edged up +0.34d.',
        bars: [
          { yr: '2023*', val: '14.84d', pct: 92, cause: id ? 'Tempo tagih pra-exit sedikit lebih panjang (~15 hari) karena bauran e-commerce.' : 'Slightly slower ~15d collection pre-exit due to Tokopedia merchant mix.' },
          { yr: '2024', val: '10.56d', pct: 66, cause: id ? 'Memisahkan piutang usaha Catatan 6 saja (Rp460M) memperbaiki salah hitung 46,88h.' : 'Trade-only Note 6 basis (Rp 460B) corrected our earlier 46.88d mix-up.' },
          { yr: '2025', val: '10.90d', pct: 68, current: true, cause: id ? 'Naik tipis +0,34h ke 10,9h (tetap sangat cepat dibanding DPO pemasok 59,1h).' : 'Edged up +0.34d to 10.9d — still ultra-fast vs. 59.1d supplier DPO.' },
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
          { yr: '2023*', val: '12.14%', pct: 45, cause: id ? 'Rasio utang penuh (termasuk sewa IFRS 16) sangat rendah pada 2023.' : 'Full debt-plus-lease ratio started very low at 12.14% in 2023.' },
          { yr: '2024', val: '15.85%', pct: 59, cause: id ? 'Naik sedikit ke 15,85% seiring berkurangnya ekuitas dari rugi 2024.' : 'Ticked up to 15.85% as 2024 net loss slightly trimmed equity.' },
          { yr: '2025', val: '26.97%', pct: 100, current: true, cause: id ? 'Penarikan pinjaman bank baru FY25 (+Rp3,72T) mengangkat leverage ke 26,97% (0,27x).' : '+Rp 3.72T new FY25 bank borrowings lifted Debt/Equity to 26.97% (0.27x, still low).' },
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
          { yr: '2023*', val: '−27.83x', pct: 100, cause: id ? 'Rugi EBIT raksasa −Rp10,28T menyebabkan rasio cakupan bunga sangat negatif.' : 'Massive −Rp 10.28T EBIT loss produced −27.83x coverage.' },
          { yr: '2024', val: '−4.54x', pct: 26, cause: id ? 'Membaik tajam ke −4,54x seiring mengecilnya rugi operasi menjadi −Rp2,24T.' : 'Improved sharply to −4.54x as EBIT loss shrank to −Rp 2.24T.' },
          { yr: '2025', val: '−0.71x', pct: 8, current: true, cause: id ? 'Rugi EBIT tinggal −Rp378M vs bunga Rp535,2M — selangkah lagi menutup penuh beban bunga.' : 'EBIT loss narrowed to −Rp 378B vs. Rp 535.2B interest — almost back to breakeven.' },
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
          { yr: '2023*', val: '−Rp4.33T', pct: 100, cause: id ? 'Pembakaran kas berat pra-exit akibat subsidi & biaya operasional Tokopedia.' : 'Heavy pre-exit cash burn from Tokopedia subsidies and e-commerce operating overhead.' },
          { yr: '2024', val: '−Rp622.1B', pct: 34, cause: id ? 'Arus kas keluar menyusut −86% pasca-dekonsolidasi Tokopedia, namun masih minus.' : 'Operating cash burn dropped −86% right after Tokopedia exit, though still negative.' },
          { yr: '2025', val: '+Rp307.0B', pct: 22, current: true, cause: id ? 'Pertama kali positif (+Rp307M) berkat pangkas insentif & cloud, tapi baru menutup 26% CapEx.' : 'First positive CFO (+Rp 307B) via incentive & cloud cuts, still covering only 26% of CapEx.' },
        ],
      },
      {
        title: id ? 'CapEx Lanjutan / Pendapatan' : 'Continuing CapEx / Rev',
        delta: '−0.18% YoY',
        tone: 'pos',
        note: id
          ? 'Tanpa transfer takberwujud Tokopedia Rp5,46T Catatan 12 di 2024.'
          : 'Excludes Rp5.46T Tokopedia Note 12 intangible transfer in 2024.',
        bars: [
          { yr: '2023*', val: '1.49%', pct: 22, cause: id ? 'Di 2023, GoTo hanya belanja CapEx Rp 220M (Rp 171M perangkat keras + Rp 49M software) — hampir tidak ada software yang dikapitalisasi.' : 'In 2023, GoTo spent only Rp 220B on CapEx (Rp 171B hardware + Rp 49B software) — almost no software was capitalized.' },
          { yr: '2024', val: '6.63%', pct: 100, cause: id ? 'CapEx mentah 2024 adalah Rp 6,52T (41%), namun setelah mengeluarkan Rp 5,46T aset Tokopedia (Cat. 12), CapEx lanjutan adalah Rp 1,05T (6,63%, terutama Rp 874M software).' : 'Raw 2024 CapEx was Rp 6.52T (41%); after removing Rp 5.46T of Tokopedia intangibles (Note 12), continuing CapEx was Rp 1.05T (6.63%, mostly Rp 874B software).' },
          { yr: '2025', val: '6.45%', pct: 97, current: true, cause: id ? 'Stabil di 6,45% (Rp 1,18T): Rp 302M server/perangkat IT + Rp 880M kapitalisasi software & hubungan pelanggan (Cat. 12).' : 'Steady at 6.45% (Rp 1.18T): Rp 302B IT hardware + Rp 880B capitalized software & customer intangibles (Note 12).' },
        ],
      },
      {
        title: id ? 'Rasio Akrual Dilaporkan' : 'Reported Accrual Ratio',
        delta: id ? 'Makin dekat 0%' : 'Closer to 0%',
        tone: 'pos',
        note: id
          ? 'Semakin dekat 0% semakin bersih. 2023* (−159%) terdistorsi goodwill Rp78,8T; kini membaik ke −3,95%.'
          : 'Closer to 0% = cleaner earnings quality. 2023* (−159%) was distorted by Rp78.8T goodwill write-off; now normalized to −3.95%.',
        bars: [
          { yr: '2023*', val: '−159.3%', pct: 100, cause: id ? 'Meledak ke −159,3% karena hapus buku goodwill Tokopedia Rp78,8T (100% beban non-tunai).' : 'Blown out to −159.3% by the 100% non-cash Rp 78.8T Tokopedia goodwill write-off.' },
          { yr: '2024', val: '−11.21%', pct: 32, cause: id ? 'Turun drastis ke −11,21% pasca-exit, masih memuat penyusutan & biaya non-tunai transisi.' : 'Fell sharply to −11.21% post-exit, still reflecting D&A and post-deal non-cash charges.' },
          { yr: '2025', val: '−3.95%', pct: 16, current: true, cause: id ? 'Kualitas laba jauh membaik (−3,95%): selisih rugi akuntansi & arus kas makin tipis.' : 'Much cleaner earnings quality (−3.95%): accounting losses and cash flow moved closely together.' },
        ],
      },
      {
        title: id ? 'Akrual Laba Berulang' : 'Adj. Recurring Accrual',
        delta: id ? 'Makin dekat 0%' : 'Closer to 0%',
        tone: 'pos',
        note: id
          ? 'Penyesuaian sama di semua tahun (hapus penurunan nilai 1x); tetap menahan SBC (Rp593M) & provisi kredit.'
          : 'Same adjustment across all 3 years (strips one-off write-offs); retains SBC (Rp593B) & loan provisions as real costs.',
        bars: [
          { yr: '2023*', val: '−13.73%', pct: 100, cause: id ? 'Dari −159,3% dilaporkan → setelah mengeluarkan hapus buku goodwill Rp78,8T, akrual berulang 2023* menjadi −13,73%.' : 'From −159.3% reported → stripping out the Rp 78.8T goodwill write-off brings 2023* recurring accruals to −13.73%.' },
          { yr: '2024', val: '−3.69%', pct: 36, cause: id ? 'Dari −11,21% dilaporkan → setelah mengeluarkan penurunan nilai & volatilitas asosiasi 2024, menyusut ke −3,69%.' : 'From −11.21% reported → stripping out 2024 impairments & associate swings brings recurring accruals to −3.69%.' },
          { yr: '2025', val: '−1.94%', pct: 20, current: true, cause: id ? 'Dari −3,95% dilaporkan → setelah mengeluarkan penurunan nilai & rugi nilai wajar 2025, turun ke −1,94% (sangat dekat 0% = kualitas laba bersih).' : 'From −3.95% reported → stripping out 2025 impairments & fair-value losses brings recurring accruals to −1.94% (near 0% = clean earnings).' },
        ],
      },
    ]
  }

  if (sn === 7) {
    return [
      {
        title: 'COGS / Revenue',
        delta: id ? '−4.36% YoY 24→25' : '−4.36% YoY 24→25',
        tone: 'pos',
        focused: titleText.includes('cogs') || titleText.includes('pokok'),
        note: id
          ? 'Bauran segmen lonjakkan 2024. Efisiensi cloud >50% pangkas COGS 2025 & 1H26.'
          : 'Mix shift spiked 2024 post-exit. Over 50% cloud savings cut COGS in 2025 & 1H26.',
        bars: [
          { yr: '2023*', val: '34.45%', pct: 74, cause: id ? 'Rasio lama masih mencampur margin komisi marketplace Tokopedia.' : 'Pre-exit blend reflected Tokopedia’s lower-COGS marketplace revenue mix.' },
          { yr: '2024', val: '46.64%', pct: 100, warn: true, cause: id ? 'Lonjakan COGS pasca-exit akibat bauran bisnis bergeser ke Gojek/GoPay sebelum efisiensi cloud.' : 'Bad post-exit COGS spike as mix shifted to Gojek/GoPay before cloud cost cuts.' },
          { yr: '2025', val: '42.28%', pct: 91, warn: true, cause: id ? 'Membaik −4,36% berkat penghematan cloud >50%, tapi masih lebih tinggi dari 2023* (34,45%).' : 'Improved −4.36% from >50% cloud savings, though still elevated vs. 2023* (34.45%).' },
          { yr: '1H26', val: '38.10%', pct: 82, good: true, cause: id ? 'Akhirnya turun signifikan ke 38,10% di 1H26 seiring efisiensi server & teknologi berlanjut.' : 'Finally trending down cleanly to 38.10% in 1H26 as tech & cloud savings compound.' },
        ],
      },
      {
        title: id ? 'Cash OpEx / Pendapatan' : 'Cash OpEx / Revenue',
        delta: '−7.08% YoY 24→25',
        tone: 'pos',
        focused: titleText.includes('opex') || titleText.includes('operating') || titleText.includes('operasi'),
        note: id
          ? 'Pemangkasan insentif & korporasi mendorong spread operasi +2.02%.'
          : 'Incentive cuts & leaner headcount drive the +2.02% operating spread.',
        bars: [
          { yr: '2023*', val: '117.01%', pct: 100, cause: id ? 'Kontaminasi tahun 2023 pra-exit membuat rata-rata dek lama melonjak ke 78,5%.' : 'Pre-exit Tokopedia burn (117%) caused old deck’s 3-yr average OpEx to blow up to 78.5%.' },
          { yr: '2024', val: '62.78%', pct: 54, cause: id ? 'Anjlok −54 poin di tahun pertama pasca-Tokopedia berkat efisiensi promo.' : 'Plunged −54 pp right after Tokopedia exit on deep subsidy cuts.' },
          { yr: '2025', val: '55.70%', pct: 48, current: true, cause: id ? 'Menyentuh 55,70% di FY2025 — menjadi dasar konservatif Base Case kami (+2,02% margin EBIT).' : 'Reached 55.70% in audited FY25 — our Base Case anchor delivering +2.02% operating spread.' },
          { yr: '1H26', val: '51.20%', pct: 44, cause: id ? 'Lebih ramping di 1H26 (51,20%); menjadi patokan Skenario Optimis kami.' : 'Trimmed further in 1H26 to 51.20% — used as our Optimistic Case driver.' },
        ],
      },
      {
        title: id ? 'Pertumbuhan Pendapatan' : 'Revenue Growth Rate',
        delta: '+7.77% YoY',
        tone: 'pos',
        focused: titleText.includes('growth') || titleText.includes('pertumbuhan') || titleText.includes('revenue'),
        note: id
          ? 'Pertumbuhan inti berlipat dua saat pinjaman GoPay (+74%) & Gojek (+14%) melesat.'
          : 'Post-exit core growth doubled as GoPay loans (+74%) & Gojek (+14%) scaled.',
        bars: [
          { yr: '2024', val: '+7.50%', pct: 42, cause: id ? 'Pertumbuhan tahun transisi pasca-exit masih moderat di +7,50%.' : 'Modest +7.50% growth during the 2024 Tokopedia transition year.' },
          { yr: '2025', val: '+15.27%', pct: 85, current: true, cause: id ? 'Berlipat dua ke +15,27% berkat GoPay (+74%) dan Gojek (+14%).' : 'Doubled to +15.27% powered by GoPay FinTech (+74%) and Gojek (+14%).' },
          { yr: 'Base', val: '+15.27%', pct: 85, cause: id ? 'Kami mengunci proyeksi pertumbuhan Base Case 2026F–2028F di laju aktual FY25 (+15,27%/thn).' : 'Base Case locks 2026F–2028F growth directly to audited FY25 pace (+15.27%/yr).' },
          { yr: 'Opt', val: '+18.00%', pct: 100, cause: id ? 'Asumsi Skenario Optimis jika akselerasi pinjaman GoPay & Gojek melampaui FY25.' : 'Optimistic upside case (+18%/yr) if GoPay & mobility accelerate faster than FY25.' },
        ],
      },
      {
        title: id ? 'CapEx Lanjutan / Pendapatan' : 'Continuing CapEx / Rev',
        delta: '−0.18% YoY 24→25',
        tone: 'accent',
        focused: titleText.includes('capex') || titleText.includes('modal'),
        note: id
          ? 'Stabil ~6,5% setelah transfer Tokopedia Rp5,46T dikeluarkan dari 2024.'
          : 'Stable ~6.5% run-rate once Rp5.46T Tokopedia intangibles are removed.',
        bars: [
          { yr: '2023*', val: '1.49%', pct: 22, cause: id ? 'Di 2023, GoTo hanya belanja CapEx Rp 220M (Rp 171M perangkat keras + Rp 49M software) sebelum kapitalisasi software naik di 2024.' : 'In 2023, GoTo spent only Rp 220B (Rp 171B hardware + Rp 49B software) before ramping up capitalized software in 2024.' },
          { yr: '2024', val: '6.63%', pct: 100, cause: id ? 'CapEx mentah 2024 adalah 41,0%; setelah Rp 5,46T aset Tokopedia dikeluarkan, CapEx lanjutan adalah Rp 1,05T (6,63%, terutama Rp 874M software).' : 'Raw 2024 CapEx was 41.0%; stripping Rp 5.46T Tokopedia intangibles leaves Rp 1.05T (6.63%, mostly Rp 874B software).' },
          { yr: '2025', val: '6.45%', pct: 97, current: true, cause: id ? 'Stabil di 6,45% (Rp 1,18T: Rp 302M hardware + Rp 880M software) — patokan bersih Base Case 2026F–2028F.' : 'Steady at 6.45% (Rp 1.18T: Rp 302B hardware + Rp 880B software) — anchored as our Base Case CapEx rate.' },
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
          { yr: '2025A', val: 'Rp18.32T', pct: 65, cause: id ? 'Pendapatan auditan FY2025 murni pasca-Tokopedia sebagai titik awal proyeksi.' : 'Audited FY2025 post-Tokopedia revenue serves as the clean starting baseline.' },
          { yr: '2026F', val: 'Rp21.12T', pct: 75, cause: id ? 'Tumbuh +15,27% mengikuti momentum GoPay FinTech & Gojek.' : 'Compounds +15.27% on continuing GoPay FinTech and Gojek momentum.' },
          { yr: '2027F', val: 'Rp24.35T', pct: 87, cause: id ? 'Skala pendapatan menembus Rp24,35T dengan asumsi pangsa pasar terjaga.' : 'Scales past Rp 24.35T assuming stable market share and pricing.' },
          { yr: '2028F', val: 'Rp28.07T', pct: 100, current: true, cause: id ? 'Mencapai Rp28,07T di Tahun ke-3 (+53% lebih besar dibanding FY2025).' : 'Reaches Rp 28.07T in Year 3 (+53% larger than FY2025 revenue).' },
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
          { yr: '2025A', val: '−Rp378B', pct: 48, cause: id ? 'Masih sedikit rugi (−Rp378M) karena biaya korporasi Rp1,44T belum tertutup penuh.' : 'Still slightly negative (−Rp 378B) due to Rp 1.44T corporate overhead.' },
          { yr: '2026F', val: '+Rp427B', pct: 75, cause: id ? 'Berbalik untung operasi (+Rp427M) karena margin kotor 57,72% > Cash OpEx 55,70% (+2,02%).' : 'Flips EBIT-positive (+Rp 427B) as 57.72% Gross Margin exceeds 55.70% Cash OpEx (+2.02%).' },
          { yr: '2027F', val: '+Rp492B', pct: 87, cause: id ? 'Laba operasi naik proporsional seiring ekspansi skala pendapatan +15,27%.' : 'Operating profit scales proportionally alongside +15.27% revenue growth.' },
          { yr: '2028F', val: '+Rp567B', pct: 100, current: true, cause: id ? 'Mencapai +Rp567M, tapi ROIC (+2,70%) masih di bawah WACC (7,76%) — nilai belum tercipta.' : 'Hits +Rp 567B, yet ROIC (+2.70%) still trails WACC (7.76%) — no economic profit yet.' },
        ],
      },
      {
        title: id ? 'Proyeksi Laba Bersih (Base)' : 'Projected Net Income (Base)',
        delta: id ? 'Positif di 2028F' : 'Turns + in 2028F',
        tone: 'accent',
        note: id
          ? 'ROIC 2028F (+2,70%) masih tertinggal −5.06% di bawah WACC (7,76%).'
          : '2028F ROIC (+2.70%) still trails WACC (7.76%) by −5.06%.',
        bars: [
          { yr: '2025A', val: '−Rp1,502B', pct: 100, cause: id ? 'EBIT −Rp378M ditambah beban bunga & pajak membuat rugi bersih FY25 −Rp1,50T.' : 'Negative EBIT (−Rp 378B) plus interest & charges led to −Rp 1.50T FY25 net loss.' },
          { yr: '2026F', val: '−Rp84.5B', pct: 18, cause: id ? 'Meski EBIT +Rp427M, beban bunga Rp535M & pajak membuat laba bersih masih tipis minus.' : 'Even with +Rp 427B EBIT, interest expense & taxes keep bottom line slightly negative.' },
          { yr: '2027F', val: '−Rp33.6B', pct: 10, cause: id ? 'Nyaris impas (−Rp33,6M) seiring kenaikan EBIT ke +Rp492M.' : 'Approaching bottom-line breakeven (−Rp 33.6B) as EBIT rises to +Rp 492B.' },
          { yr: '2028F', val: '+Rp25.0B', pct: 8, current: true, cause: id ? 'Akhirnya positif tipis (+Rp25M), tapi ROE cuma +0,09% vs batas Ke 8,45%!' : 'Finally barely positive (+Rp 25B), yet ROE is just +0.09% vs. 8.45% Ke hurdle!' },
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
          { yr: '2025A', val: 'Rp21.76T', pct: 100, cause: id ? 'Saldo kas auditan awal Rp21,76T memberi bantalan likuiditas sangat tebal.' : 'Starting audited Rp 21.76T cash pile provides a huge liquidity runway.' },
          { yr: '2026F', val: 'Rp20.69T', pct: 95, cause: id ? 'Berkurang wajar (~Rp1,07T) karena CapEx rutin 6,45% masih melampaui CFO tahun awal.' : 'Modest −Rp 1.07T drawdown as ongoing 6.45% CapEx slightly exceeds Year 1 CFO.' },
          { yr: '2027F', val: 'Rp19.96T', pct: 92, cause: id ? 'Laju bakar kas melambat saat pendapatan dan laba operasi tumbuh.' : 'Cash burn slows down further as EBIT scales up.' },
          { yr: '2028F', val: 'Rp19.42T', pct: 89, current: true, cause: id ? 'Menjaga Rp19,42T kas akhir (hampir 20x lebih aman daripada dek lama Rp968M).' : 'Preserves Rp 19.42T cash (vs. false Rp 968B cash wipeout in old 2023-based deck).' },
        ],
      },
    ]
  }
  return null
})

// Keep all 3 years visible (with a vertical Post-Exit divider after 2023*) so the structural break is clear
const visibleYoyRatioCards = computed(() => yoyRatioCards.value)

// Slide 7: Pro Forma Key Financial Statement Charts (placed ABOVE historical driver charts)
const slide7ProFormaCards = computed(() => {
  if (props.item.slide?.slide_num !== 7) return null
  const id = isId.value
  const isOld = chartBasis.value === 'previous'
  if (isOld) {
    return [
      {
        title: id ? 'Pendapatan Pro Forma (IS)' : 'Pro Forma Revenue (IS)',
        delta: '+11.40%/yr',
        tone: 'accent',
        note: id ? 'Basis dek lama 2023–2025 (rata-rata 3 tahun).' : 'Old 3-year average growth basis (2023–2025).',
        bars: [
          { yr: '2025A', val: 'Rp18.32T', pct: 72, cause: id ? 'Pendapatan aktual FY2025 sebagai basis awal.' : 'Audited FY2025 actual revenue starting point.' },
          { yr: '2026F', val: 'Rp20.41T', pct: 81, cause: id ? 'Menggunakan rata-rata lama +11,4% yang tertahan angka dekonsolidasi 2023–2024.' : 'Uses old +11.4%/yr average dragged down by 2023–2024 Tokopedia exit.' },
          { yr: '2027F', val: 'Rp22.73T', pct: 90, cause: id ? 'Proyeksi pertumbuhan majemuk 11,4% di Tahun ke-2.' : 'Year 2 compounding at the understated 11.4% legacy growth rate.' },
          { yr: '2028F', val: 'Rp25.32T', pct: 100, current: true, cause: id ? 'Tertinggal Rp2,75T dibanding Base Case pasca-exit (Rp28,07T).' : 'Trails clean post-exit Base Case (Rp 28.07T) by Rp 2.75T.' },
        ],
      },
      {
        title: id ? 'Laba Operasi / EBIT (IS)' : 'Operating Profit / EBIT (IS)',
        delta: '−Rp4.97T (28F)',
        tone: 'warn',
        note: id ? 'OpEx 78,5% memperdalam rugi operasi setiap tahun.' : '78.5% OpEx ratio deepens operating losses every year.',
        bars: [
          { yr: '2025A', val: '−Rp378B', pct: 14, cause: id ? 'Rugi aktual FY2025 yang sudah nyaris impas.' : 'Actual FY2025 loss already near breakeven.' },
          { yr: '2026F', val: '−Rp4.00T', pct: 80, cause: id ? 'Tiba-tiba anjlok 10x lipat karena model lama memakai rata-rata OpEx 78,5% (bawaan 2023).' : 'Jumps back to −Rp 4.00T because legacy 78.5% OpEx assumes 2023 burn returns.' },
          { yr: '2027F', val: '−Rp4.46T', pct: 90, cause: id ? 'Makin besar pendapatan, makin dalam ruginya selama margin tetap negatif.' : 'Higher revenue only widens losses while OpEx is stuck at 78.5%.' },
          { yr: '2028F', val: '−Rp4.97T', pct: 100, current: true, cause: id ? 'Rugi semu −Rp4,97T akibat kontaminasi pra-exit 2023.' : 'Artificial −Rp 4.97T operating loss driven by pre-exit 2023 contamination.' },
        ],
      },
      {
        title: id ? 'Laba Bersih Konsolidasi (IS)' : 'Consolidated Net Income (IS)',
        delta: '−Rp4.35T (28F)',
        tone: 'warn',
        note: id ? 'Rugi bersih melebar akibat beban operasi pra-exit.' : 'Net losses widen due to pre-exit operating cost drag.',
        bars: [
          { yr: '2025A', val: '−Rp1.50T', pct: 35, cause: id ? 'Rugi bersih auditan FY2025.' : 'Audited FY2025 consolidated net loss baseline.' },
          { yr: '2026F', val: '−Rp3.54T', pct: 81, cause: id ? 'Rugi operasi semu −Rp4T langsung menjatuhkan laba bersih ke −Rp3,54T.' : 'Artificial −Rp 4T EBIT loss immediately drags Net Income down to −Rp 3.54T.' },
          { yr: '2027F', val: '−Rp3.92T', pct: 90, cause: id ? 'Akumulasi kerugian makin dalam tiap tahun di dek lama.' : 'Losses keep compounding negatively every year in the legacy model.' },
          { yr: '2028F', val: '−Rp4.35T', pct: 100, current: true, cause: id ? 'Mengakibatkan valuasi dek lama anjlok semu ke −Rp121/saham.' : 'Responsible for legacy deck’s distorted −Rp 121/sh DCF valuation.' },
        ],
      },
      {
        title: id ? 'Saldo Kas Akhir (BS)' : 'Ending Cash Balance (BS)',
        delta: '−Rp20.8T Burn',
        tone: 'warn',
        note: id ? 'Kas terkuras buatan hingga Rp968M pada 2028F.' : 'Artificially drains cash down to Rp968B by 2028F.',
        bars: [
          { yr: '2025A', val: 'Rp21.76T', pct: 100, cause: id ? 'Saldo kas aktual Rp21,76T di akhir FY2025.' : 'Actual Rp 21.76T ending cash at FY2025.' },
          { yr: '2026F', val: 'Rp14.50T', pct: 67, cause: id ? 'Kas Rp7,26T habis terbakar dalam setahun akibat asumsi OpEx 78,5% & CapEx 16,3%.' : 'Assumed −Rp 7.26T cash drain in a single year from 78.5% OpEx & 16.3% CapEx.' },
          { yr: '2027F', val: 'Rp7.40T', pct: 34, cause: id ? 'Tersisa sepertiga saja di Tahun ke-2 akibat asumsi CapEx aset takberwujud 2024.' : 'Drops to Rp 7.40T as 2024 one-time intangibles are wrongly projected every year.' },
          { yr: '2028F', val: 'Rp0.97T', pct: 8, current: true, cause: id ? 'Krisis kas semu (tinggal Rp968M) — kesalahan utama yang diperbaiki Laporan Akhir.' : 'False cash crisis (only Rp 968B left) — the exact distortion our Final Report fixed.' },
        ],
      },
    ]
  }
  return [
    {
      title: id ? 'Pendapatan Pro Forma (IS)' : 'Pro Forma Revenue (IS)',
      delta: '+15.27%/yr',
      tone: 'pos',
      note: id ? 'Bertumbuh majemuk pada basis pasca-Tokopedia yang bersih.' : 'Compounds on clean 2024→2025 post-Tokopedia growth.',
      bars: [
        { yr: '2025A', val: 'Rp18.32T', pct: 65, cause: id ? 'Pendapatan auditan FY2025 bersih pasca-exit Tokopedia.' : 'Audited FY2025 post-Tokopedia continuing revenue.' },
        { yr: '2026F', val: 'Rp21.12T', pct: 75, cause: id ? 'Naik +15,27% dipimpin ekspansi pinjaman GoPay & komisi Gojek.' : 'Grows +15.27% led by GoPay lending & Gojek take-rate.' },
        { yr: '2027F', val: 'Rp24.35T', pct: 87, cause: id ? 'Melanjutkan pertumbuhan organik dua digit tanpa beban Tokopedia.' : 'Continues double-digit post-exit organic compounding.' },
        { yr: '2028F', val: 'Rp28.07T', pct: 100, current: true, cause: id ? 'Tumbuh +53% dalam 3 tahun menuju Rp28,07T.' : 'Expands +53% over 3 years to Rp 28.07T.' },
      ],
    },
    {
      title: id ? 'Laba Operasi / EBIT (IS)' : 'Operating Profit / EBIT (IS)',
      delta: id ? 'Berbalik + di 2026F' : 'Flips + in 2026F',
      tone: 'pos',
      note: id ? 'Margin kotor 57,72% melampaui Cash OpEx 55,70% (+2.02%).' : '57.72% Gross Margin exceeds 55.70% Cash OpEx (+2.02%).',
      bars: [
        { yr: '2025A', val: '−Rp378B', pct: 67, cause: id ? 'Rugi operasi FY25 tinggal −Rp378M setelah pemangkasan biaya.' : 'FY25 EBIT loss already narrowed to −Rp 378B.' },
        { yr: '2026F', val: '+Rp427B', pct: 75, cause: id ? 'Berbalik positif (+Rp427M) saat margin kotor 57,72% mengungguli Cash OpEx 55,70%.' : 'Flips positive (+Rp 427B) once 57.72% Gross Margin beats 55.70% Cash OpEx.' },
        { yr: '2027F', val: '+Rp492B', pct: 87, cause: id ? 'Laba operasi naik ke +Rp492M seiring skala pendapatan.' : 'Operating profit climbs to +Rp 492B on revenue scale.' },
        { yr: '2028F', val: '+Rp567B', pct: 100, current: true, cause: id ? 'Untung +Rp567M, namun ROIC 2,70% masih di bawah WACC 7,76% (tetap SELL).' : 'Reaches +Rp 567B, though 2.70% ROIC still lags 7.76% WACC.' },
      ],
    },
    {
      title: id ? 'Laba Bersih Konsolidasi (IS)' : 'Consolidated Net Income (IS)',
      delta: id ? 'Laba + di 2028F' : 'Profitable in 2028F',
      tone: 'pos',
      note: id ? 'Menutup bunga utang Rp535B dan mencetak laba pada Tahun ke-3.' : 'Covers Rp535B interest expense and turns profitable in Year 3.',
      bars: [
        { yr: '2025A', val: '−Rp1.50T', pct: 100, cause: id ? 'Rugi bersih FY25 masih −Rp1,50T akibat beban bunga, SBC, & pajak.' : 'FY25 Net Loss (−Rp 1.50T) weighed by interest, SBC & taxes.' },
        { yr: '2026F', val: '−Rp84.5B', pct: 18, cause: id ? 'Rugi menyusut drastis ke −Rp84,5M begitu EBIT berbalik positif.' : 'Net loss shrinks −94% to −Rp 84.5B once EBIT turns positive.' },
        { yr: '2027F', val: '−Rp33.6B', pct: 10, cause: id ? 'Nyaris impas (−Rp33,6M) karena EBIT mulai menutupi bunga utang.' : 'Near breakeven (−Rp 33.6B) as growing EBIT covers interest.' },
        { yr: '2028F', val: '+Rp25.0B', pct: 8, current: true, cause: id ? 'Mencetak laba bersih +Rp25M — tapi ROE cuma 0,09% jauh di bawah Ke 8,45%.' : 'First bottom-line profit (+Rp 25B), yet 0.09% ROE far trails 8.45% Ke.' },
      ],
    },
    {
      title: id ? 'Saldo Kas Akhir (BS)' : 'Ending Cash Balance (BS)',
      delta: 'Rp19.4T Kept',
      tone: 'pos',
      note: id ? 'Likuiditas terjaga Rp19,42T di 2028F tanpa pembakaran kas buatan.' : 'Preserves Rp19.42T liquidity in 2028F without artificial burn.',
      bars: [
        { yr: '2025A', val: 'Rp21.76T', pct: 100, cause: id ? 'Kas awal Rp21,76T menjadi penyangga utama valuasi (kas bersih Rp13,19/sh).' : 'Starting Rp 21.76T cash backs our Rp 13.19/sh net-cash valuation floor.' },
        { yr: '2026F', val: 'Rp20.69T', pct: 95, cause: id ? 'Penurunan kas tipis (−Rp1,07T) dari CapEx rutin 6,45%.' : 'Controlled −Rp 1.07T dip as normal 6.45% CapEx slightly exceeds Year 1 CFO.' },
        { yr: '2027F', val: 'Rp19.96T', pct: 92, cause: id ? 'Arus kas keluar melambat tajam ke ~Rp730M seiring membaiknya laba operasi.' : 'Net cash drawdown slows to ~Rp 730B as operating cash flow grows.' },
        { yr: '2028F', val: 'Rp19.42T', pct: 89, current: true, cause: id ? 'Tetap mengantongi Rp19,42T kas — tidak bangkrut, tapi uang menganggur di bawah WACC.' : 'Holds Rp 19.42T cash — GoTo won’t go bankrupt, it simply earns below WACC.' },
      ],
    },
  ]
})

// Slide 7: Focused Financial-Statement Forecast Assumptions Table (placed BELOW charts)
const hoverTip = ref({ visible: false, x: 0, y: 0, title: '', detail: '' })

const showHoverTip = (evt, title, detail) => {
  if (!detail) return
  hoverTip.value = {
    visible: true,
    x: evt.clientX,
    y: evt.clientY,
    title,
    detail,
  }
}

const moveHoverTip = (evt) => {
  if (!hoverTip.value.visible) return
  hoverTip.value.x = evt.clientX
  hoverTip.value.y = evt.clientY
}

const hideHoverTip = () => {
  hoverTip.value.visible = false
}

const slide7AssumptionsTable = computed(() => {
  if (props.item.slide?.slide_num !== 7) return null
  const id = isId.value
  return {
    title: id
      ? 'Tabel Asumsi Kunci Laporan Keuangan (Pasca-Tokopedia · Tabel 11)'
      : 'Key Financial Statement Forecast Assumptions (Post-Tokopedia · Table 11)',
    headers: id
      ? ['Driver Laporan Keuangan', '2024A', '2025A', 'Base (24→25)', 'Optimis (1H26)', 'Konservatif (24)']
      : ['Financial Statement Driver', '2024A', '2025A', 'Base (24→25)', 'Optimistic (1H26)', 'Conservative (24)'],
    rows: [
      [id ? 'Pertumbuhan Pendapatan (IS)' : 'Revenue Growth Rate (IS)', '+7.50%', '+15.27%', '15.27%', '18.00%', '7.50%'],
      [id ? 'Beban Pokok / COGS (% Rev)' : 'Cost of Goods Sold (% Rev)', '46.64%', '42.28%', '42.28%', '38.10%', '46.64%'],
      [id ? 'Cash OpEx di luar D&A (% Rev)' : 'Cash OpEx Excl. D&A (% Rev)', '62.78%', '55.70%', '55.70%', '51.20%', '62.78%'],
      [id ? 'Belanja Modal Lanjutan (% Rev)' : 'Continuing CapEx (% Rev)', '6.63%', '6.45%', '6.45%', '5.50%', '6.63%'],
      [id ? 'Modal Kerja (DSO / DPO)' : 'Working Capital (DSO / DPO)', '10.6d / 61.1d', '10.9d / 59.1d', '10.9d / 59.1d', '10.5d / 65.0d', '10.6d / 61.1d'],
      [id ? 'Suku Bunga Utang Efektif (Kd)' : 'Effective Debt Interest Rate', '10.25%', '6.91%', '6.91%', '6.91%', '10.25%'],
      [id ? 'Tarif Pajak Penghasilan Badan' : 'Corporate Income Tax Rate', '22.00%', '22.00%', '22.00%', '22.00%', '22.00%'],
    ],
    tooltips: id
      ? [
          [
            'Pertumbuhan pendapatan bersih YoY untuk proyeksi 2026F–2028F (Catatan 25).',
            'Audit 2024 vs 2023: Rp 15,89T vs Rp 14,79T.',
            'Audit 2025 vs 2024: Rp 18,32T vs Rp 15,89T (Catatan 25).',
            'Dipertahankan pada laju organik pasca-Tokopedia 2025 (tanpa 2023).',
            'Skenario akselerasi FinTech & On-Demand (+2.73% di atas Base).',
            'Kembali ke lantai transisi pasca-exit 2024.',
          ],
          [
            'Biaya langsung pengiriman & platform dibagi pendapatan bersih (Catatan 26).',
            'Audit 2024: COGS Rp 7.413M ÷ Pendapatan Rp 15.894M.',
            'Audit 2025: COGS Rp 7.746M ÷ Pendapatan Rp 18.322M (Gross Margin 57,72%).',
            'Mengikuti rasio audit FY2025 (Gross Margin 57,72%).',
            'Mengacu laporan interim 1H 2026 GoTo (Gross Margin 61,90%).',
            'Kembali ke rasio COGS pasca-exit FY2024 (Gross Margin 53,36%).',
          ],
          [
            'Beban operasional di luar D&A non-kas (G&A, S&M, Produk, Ops; Catatan 26).',
            'Audit 2024: Cash OpEx Rp 9.978M ÷ Pendapatan Rp 15.894M.',
            'Audit 2025: Cash OpEx Rp 10.206M ÷ Pendapatan Rp 18.322M (−7.08% YoY).',
            'Mengikuti rasio berulang FY2025 (2.02% di bawah Gross Margin).',
            'Mengacu efisiensi biaya laporan interim 1H 2026 (−4.50% vs Base).',
            'Kembali ke belanja FY2024 jika perang promo berulang.',
          ],
          [
            'Belanja modal kas aset tetap & takberwujud di luar aset Tokopedia (Catatan 12).',
            'CapEx kas 2024 Rp 1.054M setelah mengeluarkan Rp 5.465M aset Tokopedia (Catatan 12).',
            'Audit 2025: CapEx kas Rp 1.182M (hal. 21) ÷ Pendapatan Rp 18.322M.',
            'Mengikuti intensitas CapEx lanjutan audit FY2025.',
            'Efisiensi CapEx moderat seiring skala cloud & platform.',
            'Kembali ke rasio CapEx lanjutan FY2024.',
          ],
          [
            'Piutang usaha Catatan 6 (DSO) & utang usaha (DPO); mengecualikan pinjaman Catatan 7.',
            'Audit 2024: Piutang Catatan 6 (Rp 460M) & utang usaha (Rp 1.241M).',
            'Audit 2025: Piutang Catatan 6 (Rp 547M) & utang usaha (Rp 1.254M).',
            'Mengikuti siklus penagihan & pembayaran audit FY2025 (CCC negatif).',
            'Penagihan sedikit lebih cepat & termin pemasok lebih panjang.',
            'Kembali ke hari modal kerja audit FY2024.',
          ],
          [
            'Beban keuangan (Catatan 27b) dibagi total pinjaman & sewa (Catatan 19–20).',
            'Audit 2024: Beban bunga Rp 494M ÷ Total utang & sewa Rp 4.819M.',
            'Audit 2025: Beban bunga Rp 535M (Catatan 27b) ÷ Total utang Rp 7.743M.',
            'Mengikuti suku bunga efektif FY2025 atas utang tetap Rp 7,74T.',
            'Sama dengan suku bunga efektif FY2025.',
            'Uji stres kembali ke suku bunga lebih tinggi FY2024.',
          ],
          [
            'Tarif pajak penghasilan badan statutori Indonesia (UU HPP).',
            'Tarif pajak badan Indonesia statutori (22%).',
            'Tarif pajak badan Indonesia statutori (22%).',
            'Tarif pajak badan statutori 22% diterapkan konsisten.',
            'Tarif pajak badan statutori 22% diterapkan konsisten.',
            'Tarif pajak badan statutori 22% diterapkan konsisten.',
          ],
        ]
      : [
          [
            'YoY net revenue growth driving 2026F–2028F sales (Note 25).',
            'Audited FY2024 vs FY2023: Rp 15.89T vs Rp 14.79T.',
            'Audited FY2025 vs FY2024: Rp 18.32T vs Rp 15.89T (Note 25).',
            'Held at FY2025 post-Tokopedia YoY growth (excludes 2023).',
            'Upside FinTech & On-Demand momentum (+2.73% above Base).',
            'Reverts to GoTo\'s FY2024 post-exit transition growth floor.',
          ],
          [
            'Direct delivery & platform costs as % of net revenue (Note 26).',
            'Audited FY2024: COGS Rp 7,413B ÷ Revenue Rp 15,894B.',
            'Audited FY2025: COGS Rp 7,746B ÷ Revenue Rp 18,322B (57.72% Gross Margin).',
            'Held at FY2025 audited ratio (57.72% gross margin).',
            'From GoTo 1H 2026 interim financial statements (61.90% gross margin).',
            'Reverts to FY2024 post-exit COGS ratio (53.36% gross margin).',
          ],
          [
            'Operating costs excl. non-cash D&A (G&A, S&M, R&D, Ops; Note 26).',
            'Audited FY2024: Cash OpEx Rp 9,978B ÷ Revenue Rp 15,894B.',
            'Audited FY2025: Cash OpEx Rp 10,206B ÷ Revenue Rp 18,322B (−7.08% YoY).',
            'Held at FY2025 recurring ratio (2.02% below Gross Margin).',
            'From GoTo 1H 2026 interim cost ratio (−4.50% vs Base).',
            'Reverts to FY2024 spending if promo intensity returns.',
          ],
          [
            'Cash CapEx for PP&E & intangibles excl. Tokopedia exit (Note 12).',
            '2024 cash CapEx Rp 1,054B after removing Rp 5,465B Tokopedia intangibles (Note 12).',
            'Audited FY2025: Cash CapEx Rp 1,182B (p. 21) ÷ Revenue Rp 18,322B.',
            'Held at FY2025 audited continuing CapEx intensity.',
            'Modest CapEx discipline as cloud & platform scale.',
            'Reverts to FY2024 continuing CapEx ratio.',
          ],
          [
            'Note 6 trade receivables (DSO) & trade payables (DPO); excludes Note 7 loans.',
            'Audited FY2024: Note 6 receivables (Rp 460B) & payables (Rp 1,241B).',
            'Audited FY2025: Note 6 receivables (Rp 547B) & payables (Rp 1,254B).',
            'Held at FY2025 audited collection & payable timing (negative CCC).',
            'Slightly faster collections and extended supplier terms.',
            'Reverts to FY2024 audited working capital days.',
          ],
          [
            'Finance costs (Note 27b) divided by total debt & leases (Notes 19–20).',
            'Audited FY2024: Finance costs Rp 494B ÷ Total debt Rp 4,819B.',
            'Audited FY2025: Finance costs Rp 535B (Note 27b) ÷ Total debt Rp 7,743B.',
            'Held at FY2025 effective rate on fixed Rp 7.74T debt.',
            'Same FY2025 effective borrowing rate.',
            'Stress rate reverting to FY2024 higher borrowing cost.',
          ],
          [
            'Statutory Indonesian corporate income tax rate (UU HPP).',
            'Statutory Indonesian corporate tax rate (22%).',
            'Statutory Indonesian corporate tax rate (22%).',
            '22% statutory corporate tax rate applied consistently.',
            '22% statutory corporate tax rate applied consistently.',
            '22% statutory corporate tax rate applied consistently.',
          ],
        ],
  }
})

// Keep the final-report forecast visible below Slide 8's trajectory charts.
const slide8ForecastTable = computed(() => {
  if (props.item.slide?.slide_num !== 8) return null
  const id = isId.value
  return {
    title: id
      ? 'Proyeksi Tiga Laporan Keuangan · Base Case · Tabel 12'
      : 'Three-Statement Forecast · Base Case · Table 12',
    note: id
      ? 'Rp miliar · A = aktual, F = proyeksi. Angka dalam kurung menunjukkan nilai negatif. Sumber: Laporan Akhir, Tabel 12; Appendix A5.'
      : 'Rp billion · A = actual, F = forecast. Parentheses indicate negative amounts. Source: Final Report, Table 12; Appendix A5.',
    headers: id
      ? ['Pos laporan keuangan', '2025A Auditan', '2026F Base', '2027F Base', '2028F Base']
      : ['Financial statement line', ...postTokopediaBaseForecast.headers.slice(1)],
    rows: postTokopediaBaseForecast.rows.map((row) => ({
      ...row,
      label: id ? row.label_id : row.label,
    })),
  }
})

// Slide 10: Restated Sensitivity Analysis (TV/PV Calculation Bridges + 2D WACC x g Grid + Beta / WACC / RI Boundary Checks, Table 16)
const slide10SensitivityTables = computed(() => {
  if (props.item.slide?.slide_num !== 10) return null
  const id = isId.value
  return {
    dcfBridgeTitle: id
      ? 'Perhitungan Langkah-demi-Langkah DCF: FCFF, PV & Terminal Value (WACC 7,761% · g 3,00%)'
      : 'DCF Step-by-Step Calculation: FCFF, PV & Terminal Value (WACC 7.761% · g 3.00%)',
    dcfBridgeHeaders: id
      ? ['Tahap Perhitungan', 'Rumus & Substitusi', 'Hasil (Rp Miliar)']
      : ['Calculation Step', 'Formula & Substitution', 'Result (Rp Billion)'],
    dcfBridgeRows: [
      [
        id ? '1. FCFF Tahunan (2026F–2028F)' : '1. Annual FCFF (2026F–2028F)',
        'NOPAT + D&A − CapEx + ΔNWC → 2026F: 332.9 + 273.1 − 1,362.9 + 105.8 | 2027F: 383.8 + 751.4 − 1,571.1 + 122.0 | 2028F: 442.4 + 1,111.1 − 1,811.1 + 140.6',
        '−651.0 | −313.9 | −116.9',
      ],
      [
        id ? '2. PV FCFF 3 Tahun (Eksplisit)' : '2. PV of 3-Yr Explicit FCFF',
        '−651.0÷1.07761¹ (−604.1) + −313.9÷1.07761² (−270.3) + −116.9÷1.07761³ (−93.4)',
        '−967.9',
      ],
      [
        id ? '3. Terminal Value (TV di Akhir 2028F)' : '3. Terminal Value (TV at End of 2028F)',
        'FCFF₂₀₂₈ × (1 + g) ÷ (WACC − g) = −116.88 × 1.03 ÷ (7.761% − 3.00%) = −120.38 ÷ 4.761%',
        '−2,528.6',
      ],
      [
        id ? '4. Present Value of TV (PV TV)' : '4. Present Value of TV (PV of TV)',
        'TV ÷ (1 + WACC)³ = −2,528.6 ÷ (1.07761)³ = −2,528.6 × 0.7991  (TV Share = 67.6% of EV)',
        '−2,020.6',
      ],
      [
        id ? '5. Enterprise Value (EV)' : '5. Enterprise Value (EV)',
        'PV FCFF 3 Thn (−967.9) + PV of TV (−2,020.6)',
        '−2,988.5',
      ],
      [
        id ? '6. Nilai Ekuitas & Nilai per Saham' : '6. Equity Value & Value per Share',
        'EV (−2,988.5) + Net Cash (+14,012.5) = +11,024.0B ÷ 1,062.01B shares',
        '+Rp 10.38 / sh',
      ],
    ],
    riBridgeTitle: id
      ? 'Perhitungan Langkah-demi-Langkah Residual Income: RI, PV & Terminal Value (Ke 8,452% · g 3,00%)'
      : 'Residual Income Step-by-Step Calculation: RI, PV & Terminal Value (Ke 8.452% · g 3.00%)',
    riBridgeHeaders: id
      ? ['Tahap Perhitungan', 'Rumus & Substitusi', 'Hasil (Rp Miliar)']
      : ['Calculation Step', 'Formula & Substitution', 'Result (Rp Billion)'],
    riBridgeRows: [
      [
        id ? '1. Residual Income Tahunan (2026F–2028F)' : '1. Annual Residual Income (2026F–2028F)',
        'NI − (Beg. BVE × 8.452%) → 2026F: −84.5 − 2,426.7 | 2027F: −33.6 − 2,419.6 | 2028F: +25.0 − 2,416.7',
        '−2,511.2 | −2,453.2 | −2,391.7',
      ],
      [
        id ? '2. PV RI 3 Tahun (Eksplisit)' : '2. PV of 3-Yr Explicit RI',
        '−2,511.2÷1.08452¹ (−2,315.5) + −2,453.2÷1.08452² (−2,085.7) + −2,391.7÷1.08452³ (−1,875.0)',
        '−6,276.2',
      ],
      [
        id ? '3. Terminal Value RI (TV di Akhir 2028F)' : '3. Terminal Value of RI (TV at End of 2028F)',
        'RI₂₀₂₈ × (1 + g) ÷ (Ke − g) = −2,391.74 × 1.03 ÷ (8.452% − 3.00%) = −2,463.49 ÷ 5.452%',
        '−45,184.7',
      ],
      [
        id ? '4. Present Value of Terminal RI (PV TV)' : '4. Present Value of Terminal RI (PV of TV)',
        'TV ÷ (1 + Ke)³ = −45,184.7 ÷ (1.08452)³ = −45,184.7 × 0.7839  (TV Share = 85.0% of Total PV)',
        '−35,422.4',
      ],
      [
        id ? '5. Total PV Residual Income' : '5. Total PV of Residual Income',
        'PV RI 3 Thn (−6,276.2) + PV Terminal RI (−35,422.4)',
        '−41,698.6',
      ],
      [
        id ? '6. Nilai Ekuitas & Nilai per Saham' : '6. Equity Value & Value per Share',
        'Beg. BVE (+28,711.7) + Total PV(RI) (−41,698.6) = −12,987.0B ÷ 1,062.01B shares',
        '−Rp 12.23 / sh',
      ],
    ],
    gridTitle: id
      ? 'Uji Sensitivitas DCF Base Case: WACC × Pertumbuhan Terminal g (Rp / saham · Tabel 16)'
      : 'Base DCF Sensitivity Matrix: WACC × Terminal Growth g (Rp / share · Table 16)',
    gridHeaders: ['WACC \\ g', '1.0%', '2.0%', '3.0% (Base)', '3.5%', '4.0%'],
    gridRows: [
      ['6.76% (−1.00%)', 'Rp 10.68', 'Rp 10.33', 'Rp 9.79', 'Rp 9.40', 'Rp 8.86'],
      ['7.76% (Baseline)', 'Rp 10.97', 'Rp 10.73', 'Rp 10.38', 'Rp 10.15', 'Rp 9.85'],
      ['8.76% (+1.00%)', 'Rp 11.18', 'Rp 11.00', 'Rp 10.77', 'Rp 10.61', 'Rp 10.43'],
    ],
    gridNote: id
      ? 'Nilai DCF bergerak sempit di Rp 8,86–Rp 11,18/saham. WACC lebih tinggi sedikit menaikkan DCF karena diskonto mengecilkan Enterprise Value negatif (−Rp 2,99T) terhadap Kas Bersih Rp 14,01T.'
      : 'Tightly bounded between Rp 8.86 and Rp 11.18/share. Higher WACC slightly raises Base DCF because discounting shrinks negative Enterprise Value (−Rp 2.99T) relative to fixed Rp 14.01T Net Cash.',
    stressTitle: id
      ? 'Uji Stres Beta, WACC Tanpa Tax Shield & Batas Residual Income (Tabel 14–16)'
      : 'Beta Stress, Zero-Tax-Shield WACC & Residual Income Boundary Checks (Tables 14–16)',
    stressHeaders: id
      ? ['Skenario Uji Stres', 'Ke / WACC', 'DCF / Saham', 'RI / Saham']
      : ['Sensitivity / Boundary Test', 'Ke / WACC', 'DCF / Share', 'RI / Share'],
    stressRows: [
      [id ? 'Beta Dasar Investing.com (0,59)' : 'Base Investing.com Beta (0.59)', '8.45% / 7.76%', '+Rp 10.38', '−Rp 12.23'],
      [id ? 'WACC Tanpa Tax Shield (Pajak 0%)' : 'Zero-Tax-Shield WACC (0% Tax)', '8.45% / 8.10%', '+Rp 10.52', '−Rp 12.23'],
      [id ? 'Beta Teknologi Normal (1,01)' : 'Normalized Tech Beta (1.01)', '11.26% / 9.94%', '+Rp 11.09', '−Rp 8.45'],
      [id ? 'Beta Volatilitas Tinggi (1,30)' : 'High-Volatility Beta (1.30)', '13.21% / 11.45%', '+Rp 11.36', '−Rp 6.00'],
      [id ? 'Batas RI Tanpa Pertumbuhan (g = 0%)' : 'Residual Income Floor (g = 0% forever)', id ? 'Tanpa rugi tumbuh kekal' : 'No perpetual loss growth', '—', '+Rp 0.24'],
      [id ? 'Konvergensi RI Tahun 4+ (ROE = Ke)' : 'Residual Income Yr 4+ Convergence', id ? 'ROE menyamai Ke (8,45%)' : 'ROE converges to Ke (8.45%)', '—', '+Rp 21.13'],
    ],
    stressTooltips: [
      [
        {
          title: id ? 'Sumber Beta Dasar (0,59)' : 'Base Beta Source (0.59)',
          detail: id
            ? 'Beta levered historis 5Y GOTO dari Investing.com (30 Des 2025). Mengukur sensitivitas saham GOTO terhadap IHSG.'
            : 'Historical 5Y levered beta for GOTO from Investing.com (30 Dec 2025). Measures GOTO stock sensitivity vs. the market.',
        },
        {
          title: id ? 'Rumus Ke & WACC Dasar' : 'Base Ke & WACC Math',
          detail: id
            ? 'Ke = 4,502% (Rf) + 0,59 × 6,695% (ERP+CRP) = 8,45%. WACC = (77,42% × 8,45%) + (22,58% × 5,39%) = 7,76%.'
            : 'Ke = 4.502% (Rf) + 0.59 × 6.695% (ERP+CRP) = 8.45%. WACC = (77.42% × 8.45%) + (22.58% × 5.39%) = 7.76%.',
        },
        {
          title: id ? 'DCF Base Case (+Rp 10,38)' : 'Base Case DCF (+Rp 10.38)',
          detail: id
            ? '(PV FCF −Rp 2,99T + Kas Bersih Rp 14,01T) = Ekuitas Rp 11,02T ÷ 1.062,01M saham = +Rp 10,38/saham.'
            : '(PV of FCF −Rp 2.99T + Net Cash Rp 14.01T) = Rp 11.02T Equity ÷ 1,062.01B shares = +Rp 10.38/share.',
        },
        {
          title: id ? 'RI Base Case (−Rp 12,23)' : 'Base Case RI (−Rp 12.23)',
          detail: id
            ? 'BVE Rp 28,71T + PV RI 3 thn (−Rp 6,28T) + PV RI Terminal (−Rp 35,42T) = −Rp 12,99T ÷ 1.062,01M saham = −Rp 12,23/saham.'
            : 'BVE Rp 28.71T + 3-Yr PV RI (−Rp 6.28T) + Terminal PV RI (−Rp 35.42T) = −Rp 12.99T ÷ 1,062.01B shares = −Rp 12.23/share.',
        },
      ],
      [
        {
          title: id ? 'Asal Uji Stres Pajak 0%' : 'Origin of 0% Tax-Shield Check',
          detail: id
            ? 'Menguji skenario jika rugi fiskal (NOL/loss carryforward) GOTO membuat perusahaan tidak mendapat manfaat penghematan pajak bunga (tax shield = 0%).'
            : 'Tests the reality check where GOTO tax loss carryforwards (NOLs) eliminate the near-term interest tax shield (effective tax rate = 0%).',
        },
        {
          title: id ? 'Ke Tetap 8,45% / WACC Naik ke 8,10%' : 'Ke Unchanged 8.45% / WACC Rises to 8.10%',
          detail: id
            ? 'Kd setelah pajak naik dari 5,39% menjadi 6,91% (6,91% × (1 − 0%)). WACC = (77,42% × 8,45%) + (22,58% × 6,91%) = 8,10% (+34 bps).'
            : 'After-tax Kd rises from 5.39% to 6.91% (6.91% × (1 − 0%)). WACC = (77.42% × 8.45%) + (22.58% × 6.91%) = 8.10% (+34 bps).',
        },
        {
          title: id ? 'Dampak DCF (+Rp 10,52)' : 'DCF Impact (+Rp 10.52)',
          detail: id
            ? 'WACC lebih tinggi (8,10% vs 7,76%) mendiskonto PV FCF negatif lebih kecil sehingga Ekuitas sedikit naik ke +Rp 10,52/saham.'
            : 'Higher WACC (8.10% vs 7.76%) shrinks the negative PV of FCF slightly, nudging Equity Value to +Rp 10.52/share.',
        },
        {
          title: id ? 'RI Tetap −Rp 12,23' : 'RI Unchanged (−Rp 12.23)',
          detail: id
            ? 'Residual Income didiskonto memakai Ke (8,45%), bukan WACC, sehingga tarif pajak utang tidak mengubah nilai RI.'
            : 'Residual Income discounts equity cash flows at Ke (8.45%), not WACC, so removing the debt tax shield leaves RI unchanged.',
        },
      ],
      [
        {
          title: id ? 'Asal Beta Teknologi Normal (1,01)' : 'Where Normalized Tech Beta (1.01) Comes From',
          detail: id
            ? 'Tolok ukur beta pasar/peer teknologi yang ternormalisasi (~1,01, sekitar beta pasar = 1,0) untuk menguji jika beta GOTO (0,59) naik ke level normal industri.'
            : 'Normalized peer/market-level tech beta benchmark (~1.01, near market beta 1.0) used to stress-test if GOTO’s low 0.59 beta mean-reverts.',
        },
        {
          title: id
            ? 'Perhitungan Ke 11,26% & WACC 9,94%'
            : 'Ke 11.26% & WACC 9.94% Math',
          detail: id
            ? 'Ke = 4,502% + 1,01 × 6,695% = 11,26%. WACC = (77,42% × 11,26%) + (22,58% × 5,39%) = 9,94%.'
            : 'Ke = 4.502% + 1.01 × 6.695% = 11.26%. WACC = (77.42% × 11.26%) + (22.58% × 5.39%) = 9.94%.',
        },
        {
          title: id ? 'Dampak DCF (+Rp 11,09)' : 'DCF Impact (+Rp 11.09)',
          detail: id
            ? 'WACC 9,94% mengecilkan EV negatif lebih jauh terhadap Kas Bersih Rp 14,01T tetap, sehingga DCF naik tipis ke +Rp 11,09/saham.'
            : '9.94% WACC shrinks negative EV further against fixed Rp 14.01T Net Cash, lifting DCF slightly to +Rp 11.09/share.',
        },
        {
          title: id ? 'Dampak RI (−Rp 8,45)' : 'RI Impact (−Rp 8.45)',
          detail: id
            ? 'Ke lebih tinggi (11,26%) menaikkan beban ekuitas tahunan tetapi sangat menekan faktor diskonto atas rugi RI terminal jangka panjang.'
            : 'Higher Ke (11.26%) raises annual equity charge but heavily discounts long-term negative terminal RI, reducing the negative PV.',
        },
      ],
      [
        {
          title: id ? 'Asal Beta Volatilitas Tinggi (1,30)' : 'Where High-Volatility Beta (1.30) Comes From',
          detail: id
            ? 'Asumsi stres platform teknologi berisiko tinggi (1,30 = +30% di atas beta pasar 1,0) untuk menguji batas atas risiko ekuitas GOTO.'
            : 'High-beta tech platform stress assumption (1.30 = +30% above market beta 1.0) testing an aggressive upper bound for GOTO equity risk.',
        },
        {
          title: id ? 'Perhitungan Ke 13,21% & WACC 11,45%' : 'Ke 13.21% & WACC 11.45% Math',
          detail: id
            ? 'Ke = 4,502% + 1,30 × 6,695% = 13,21%. WACC = (77,42% × 13,21%) + (22,58% × 5,39%) = 11,45%.'
            : 'Ke = 4.502% + 1.30 × 6.695% = 13.21%. WACC = (77.42% × 13.21%) + (22.58% × 5.39%) = 11.45%.',
        },
        {
          title: id ? 'Dampak DCF (+Rp 11,36)' : 'DCF Impact (+Rp 11.36)',
          detail: id
            ? 'WACC 11,45% hampir menghapus nilai kini EV negatif, membuat nilai DCF mendekati lantai Kas Bersih per saham (+Rp 11,36).'
            : '11.45% WACC compresses negative EV even further, leaving DCF anchored near Net Cash per share (+Rp 11.36).',
        },
        {
          title: id ? 'Dampak RI (−Rp 6,00)' : 'RI Impact (−Rp 6.00)',
          detail: id
            ? 'Diskonto Ke 13,21% menekan nilai kini RI terminal negatif, mempersempit nilai RI negatif dari −Rp 12,23 menjadi −Rp 6,00/saham.'
            : '13.21% Ke discount rate compresses the PV of negative terminal RI, narrowing RI from −Rp 12.23 to −Rp 6.00/share.',
        },
      ],
      [
        {
          title: id ? 'Asal Batas RI Tanpa Pertumbuhan (g = 0%)' : 'Origin of RI Floor (g = 0% forever)',
          detail: id
            ? 'Uji batas model agar kerugian residual (−Rp 2,39T di 2028F) tidak dianggap terus membesar 3%/tahun selamanya dalam perpetuitas.'
            : 'Model boundary check ensuring negative residual income (−Rp 2.39T in 2028F) does not compound at +3%/yr forever in perpetuity.',
        },
        {
          title: id ? 'Formula Terminal g = 0%' : 'Terminal g = 0% Formula',
          detail: id
            ? 'PV Terminal RI = (−Rp 2,39T ÷ 8,452%) × 0,7839 = −Rp 22,18T (jauh lebih kecil dari −Rp 35,42T saat g = 3%).'
            : 'Terminal PV RI = (−Rp 2.39T ÷ 8.452%) × 0.7839 = −Rp 22.18T (vs. −Rp 35.42T when negative RI grows at g = 3%).',
        },
        null,
        {
          title: id ? 'Perhitungan RI (+Rp 0,24)' : 'RI Calculation (+Rp 0.24)',
          detail: id
            ? 'BVE Rp 28,71T + PV RI 3 thn (−Rp 6,28T) + PV Terminal (−Rp 22,18T) = +Rp 251,5M ÷ 1.062,01M saham = +Rp 0,24/saham.'
            : 'BVE Rp 28.71T + 3-Yr PV RI (−Rp 6.28T) + Terminal PV (−Rp 22.18T) = +Rp 251.5B ÷ 1,062.01B shares = +Rp 0.24/share.',
        },
      ],
      [
        {
          title: id ? 'Asal Konvergensi Tahun 4+ (ROE = Ke)' : 'Origin of Yr 4+ Convergence (ROE = Ke)',
          detail: id
            ? 'Asumsi ekonomi standar bahwa setelah 2028F persaingan mendorong ROE menyamai Ke (8,45%), sehingga laba residual setelah Tahun ke-3 = 0.'
            : 'Standard economic fade assumption: after 2028F, ROE converges to Ke (8.45%) so post-Year 3 Residual Income equals zero.',
        },
        {
          title: id ? 'Terminal RI = Rp 0' : 'Terminal RI = Rp 0',
          detail: id
            ? 'Jika ROE = Ke (8,45%) mulai 2029F+, maka Ekuitas tidak menciptakan maupun menghancurkan nilai lagi (PV Terminal RI = 0).'
            : 'When ROE = Ke (8.45%) from 2029F+, equity neither creates nor destroys economic value (Terminal PV RI = 0).',
        },
        null,
        {
          title: id ? 'Perhitungan RI (+Rp 21,13)' : 'RI Calculation (+Rp 21.13)',
          detail: id
            ? 'BVE Rp 28,71T + PV RI 3 thn (−Rp 6,28T) + Terminal Rp 0 = +Rp 22,44T ÷ 1.062,01M saham = +Rp 21,13/saham.'
            : 'BVE Rp 28.71T + 3-Yr PV RI (−Rp 6.28T) + Rp 0 Terminal = +Rp 22.44T ÷ 1,062.01B shares = +Rp 21.13/share.',
        },
      ],
    ],
  }
})

// Slide 11: 3-Scenario Valuation Matrix & Defensible Range Reconciliation (Table 16 & Workbook 3)
const slide11ScenarioMatrix = computed(() => {
  if (props.item.slide?.slide_num !== 11) return null
  const id = isId.value
  return {
    title: id
      ? 'Matriks Valuasi 3 Skenario & Rekonsiliasi Rentang Nilai Wajar (Rp / saham · Appendix A6)'
      : '3-Scenario Valuation Matrix & Defensible Range Reconciliation (Rp / share · Appendix A6)',
    headers: id
      ? ['Skenario / Tolok Ukur', 'DCF / Saham', 'RI / Saham', 'Interpretasi Ekonomi']
      : ['Scenario / Benchmark', 'DCF / Share', 'RI / Share', 'Economic Driver & Role'],
    rows: [
      [
        id ? 'Base (2024→2025 YoY)' : 'Base (2024→2025 YoY)',
        '+Rp 10.38',
        '−Rp 12.23',
        id ? 'EBIT positif, namun ROIC 2,70% < WACC 7,76%. Menjadi lantai rentang nilai.' : 'Positive EBIT, but 2.70% ROIC < 7.76% WACC. Anchors intrinsic floor.',
      ],
      [
        id ? 'Optimis (Efisiensi 1H 2026)' : 'Optimistic (1H 2026 OpEx)',
        '+Rp 47.34',
        '+Rp 16.75',
        id ? 'Pertumbuhan 18%, COGS 38,1%, OpEx 51,2% mengangkat ROE 2028F ke 6,18%. Plafon RI.' : '18% growth, 38.1% COGS, 51.2% OpEx lifts 2028F ROE to 6.18%. Anchors RI ceiling.',
      ],
      [
        id ? 'Konservatif (Lantai 2024)' : 'Conservative (2024 Floor)',
        '−Rp 33.95',
        '−Rp 44.42',
        id ? 'OpEx 62,78% & COGS 46,64% mengembalikan rugi EBIT −Rp2,14T. Risiko turun tajam.' : '62.78% OpEx & 46.64% COGS restore −Rp2.14T EBIT losses. Severe downside.',
      ],
      [
        id ? 'Kas Bersih per Saham (FY2025)' : 'Net Cash Backing (FY2025)',
        '+Rp 13.19',
        '—',
        id ? 'Kas bersih Rp14,01T / 1.062M saham. Titik tengah rentang Rp10,38–Rp16,75.' : 'Rp14.01T Net Cash / 1,062B shares. Center of Rp10.38–Rp16.75 range.',
      ],
      [
        id ? 'Pembanding P/B Grab (3,04x)' : 'Grab-Only P/B Peer (3.04x)',
        'Rp 91.02',
        id ? '(Kondisional)' : '(Conditional)',
        id ? 'Grab sudah profit (+2,96% ROE). Plafon aspiratif saja, tidak dirata-rata.' : 'Profitable peer (+2.96% ROE). Aspirational ceiling only, not blended.',
      ],
    ],
  }
})
const titleAbbrHint = computed(() => getInlineAbbrHint(props.item.title || '', props.lang))

const modalAbbrGlossary = computed(() => {
  const cfg = chartConfig.value || {}
  const chartLabels = [
    cfg.title,
    cfg.subtitle,
    ...(cfg.items || []).map((i) => i.label),
    ...(cfg.cards || []).map((c) => c.title),
  ]
  const blob = [
    props.item.title,
    props.item.value,
    ...chartLabels,
    ...(explanationParagraphs.value || []).slice(0, 2),
  ]
    .filter(Boolean)
    .join(' ')
  return findAbbrTerms(blob, props.lang, 8)
})
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
            <h2 id="glass-modal-title">{{ isPorterWalkthrough ? currentPorterForce.title : item.title }}</h2>
            <div v-if="titleAbbrHint && !isPorterWalkthrough" class="glass-abbr-sub">{{ titleAbbrHint }}</div>
            <div v-if="isPorterWalkthrough ? currentPorterForce.rating : item.value" class="glass-value-pill">{{ isPorterWalkthrough ? currentPorterForce.rating : item.value }}</div>
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
              :title="isSlide9Walkthrough ? (isId ? 'Sumber & Perhitungan' : 'Sources & Math') : isPorterWalkthrough ? (isId ? 'Lima Kekuatan Porter' : 'Porter Five Forces') : (isId ? 'Grafik & Data' : 'Charts & Data')"
              :aria-label="isSlide9Walkthrough ? (isId ? 'Sumber & Perhitungan' : 'Sources & Math') : isPorterWalkthrough ? (isId ? 'Lima Kekuatan Porter' : 'Porter Five Forces') : (isId ? 'Grafik & Data' : 'Charts & Data')"
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

          <div class="glass-tab-right-actions">
            <button
              v-if="appendixTarget"
              type="button"
              class="glass-panel-toggle is-apx"
              @click="emit('jump-slide', appendixTarget.slideNum)"
              :title="isId ? `Lompat ke Appendix ${appendixTarget.code}` : `Jump to Appendix ${appendixTarget.code}`"
            >
              <span>Appendix {{ appendixTarget.code }}</span>
              <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M7 17 17 7" /><path d="M7 7h10v10" />
              </svg>
            </button>

            <button
              v-if="activeTab === 'overview' && hasAnalysisTab && !isSlide9Walkthrough && !isPorterWalkthrough"
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
          </div>
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

        <!-- Slide 3 Porter's Five Forces Sub-Menu Bar (directly below main top bar) -->
        <div
          v-if="isPorterWalkthrough && activeTab === 'overview'"
          class="glass-sub-nav"
          role="tablist"
          :aria-label="isId ? 'Lima Kekuatan Porter' : 'Porter Five Forces'"
        >
          <button
            v-for="pf in porterForces"
            :key="pf.id"
            type="button"
            role="tab"
            class="glass-sub-pill"
            :class="{ 'is-active': activePorterForce === pf.id }"
            :aria-selected="activePorterForce === pf.id"
            @click="activePorterForce = pf.id"
          >
            {{ pf.shortLabel }}
          </button>
        </div>

        <!-- Independent Vertical-Scrolling Tab Panels -->
        <div class="glass-modal-body">
          <!-- SLIDE 3 PORTER FIVE FORCES SPECIAL VIEW: Visual Picture + Presenter Dialogue & Evidence -->
          <div
            v-if="activeTab === 'overview' && isPorterWalkthrough"
            class="glass-porter-split"
            :key="'tab-porter-' + currentPorterForce.id"
          >
            <!-- Left: Custom Illustration + Rating Pill + Headline + Prev/Next -->
            <div class="glass-card glass-porter-left">
              <div class="glass-porter-img-wrap">
                <img :src="currentPorterForce.image" :alt="currentPorterForce.title" class="glass-porter-img" />
                <span class="glass-porter-rating" :class="`tone-${currentPorterForce.ratingTone}`">
                  {{ isId ? 'Peringkat:' : 'Rating:' }} {{ currentPorterForce.rating }}
                </span>
              </div>
              <div class="glass-porter-left-copy">
                <span class="glass-s9-eyebrow">{{ currentPorterForce.title }}</span>
                <p class="glass-porter-headline">{{ currentPorterForce.headline }}</p>
              </div>
              <div class="glass-s9-nav-btns">
                <button
                  v-if="prevPorterForce"
                  type="button"
                  class="glass-s9-nav-btn"
                  @click="activePorterForce = prevPorterForce.id"
                >
                  ← {{ prevPorterForce.shortLabel }}
                </button>
                <button
                  v-if="nextPorterForce"
                  type="button"
                  class="glass-s9-nav-btn is-next"
                  @click="activePorterForce = nextPorterForce.id"
                >
                  {{ nextPorterForce.shortLabel }} →
                </button>
              </div>
            </div>

            <!-- Right: Key Points Only -->
            <div class="glass-card glass-porter-right">
              <div class="glass-porter-facts-box">
                <div class="glass-sec-label" style="margin-bottom: 10px;">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <polyline points="9 11 12 14 22 4" /><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
                  </svg>
                  <span>{{ isId ? 'Poin Utama' : 'Key Points' }}</span>
                </div>
                <ul class="glass-porter-facts">
                  <li v-for="(ev, eIdx) in currentPorterForce.evidence" :key="currentPorterForce.id + '-ev-' + eIdx">
                    {{ ev }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- SLIDE 9 SPECIAL VIEW: Clean Zero-Scroll Side-by-Side (Left: Big Result, Right: Compact Source Table) -->
          <div
            v-else-if="activeTab === 'overview' && isSlide9Walkthrough"
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
                        <div
                          class="glass-vchart-col is-hoverable"
                          @mouseenter="setHoveredBar(`${vc.title} (${bar.label})`, bar.display, bar.cause || vc.note, $event)"
                          @mousemove="moveHoveredBar($event)"
                          @mouseleave="clearHoveredBar()"
                        >
                          <span
                            class="glass-vchart-val"
                            :class="{ 'is-warn': bar.warn || (!bar.goodNeg && String(bar.display).startsWith('−')), 'is-accent': bar.accent, 'is-amber': bar.amber }"
                          >{{ bar.display }}</span>
                          <div class="glass-vchart-bar-wrap">
                            <span
                              class="glass-vchart-bar"
                              :class="{ 'is-warn': bar.warn || (!bar.goodNeg && String(bar.display).startsWith('−')), 'is-accent': bar.accent, 'is-amber': bar.amber }"
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

                <!-- Three-Step DuPont ROE 3-Panel Breakdown (Slide 4) -->
                <div
                  v-else-if="svgChartData.mode === 'dupont_3step'"
                  :key="`dupont-${item.slide?.slide_num}-${chartBasis}`"
                  class="glass-dupont-wrap"
                >
                  <div class="glass-dupont-grid">
                    <!-- Panel 1: Profitability (Net Margin %) -->
                    <div class="glass-dupont-panel">
                      <div class="glass-dupont-panel-hdr">
                        <strong>{{ isId ? '1. Profitabilitas (Margin Bersih)' : '1. Profitability (Net Margin)' }}</strong>
                        <span class="glass-dupont-axis-tag">%</span>
                      </div>
                      <div class="glass-dupont-hrows">
                        <div
                          v-for="row in svgChartData.rows"
                          :key="`m-${row.label}`"
                          class="glass-dupont-hrow is-hoverable"
                          @mouseenter="setHoveredBar(row.label, `Margin ${row.marginDisp}`, row.cause, $event)"
                          @mousemove="moveHoveredBar($event)"
                          @mouseleave="clearHoveredBar()"
                        >
                          <span class="glass-dupont-rlbl">{{ row.label }}</span>
                          <div class="glass-dupont-htrack">
                            <span class="glass-dupont-zero" :style="{ left: svgChartData.marginZeroPct }"></span>
                            <span
                              class="glass-dupont-hbar"
                              :class="`tone-${row.tone}`"
                              :style="{ left: row.marginBarLeft, width: row.marginBarWidth }"
                            ></span>
                          </div>
                          <span class="glass-dupont-rval" :class="`tone-${row.tone}`">{{ row.marginDisp }}</span>
                        </div>
                      </div>
                    </div>

                    <!-- Panel 2: Efficiency × Leverage (Multiple x) -->
                    <div class="glass-dupont-panel">
                      <div class="glass-dupont-panel-hdr">
                        <strong>{{ isId ? '2. Efisiensi × Leverage' : '2. Efficiency × Leverage' }}</strong>
                        <div class="glass-dupont-mini-leg">
                          <span><i class="leg-dot is-turn"></i>{{ isId ? 'Perputaran Aset' : 'Asset Turnover' }}</span>
                          <span><i class="leg-dot is-lev"></i>{{ isId ? 'Equity Mult.' : 'Equity Mult.' }}</span>
                        </div>
                      </div>
                      <div class="glass-dupont-vplot">
                        <div
                          v-for="row in svgChartData.rows"
                          :key="`el-${row.label}`"
                          class="glass-dupont-vgroup is-hoverable"
                          @mouseenter="setHoveredBar(row.label, `ATO ${row.turnoverDisp} · EM ${row.leverageDisp}`, row.cause, $event)"
                          @mousemove="moveHoveredBar($event)"
                          @mouseleave="clearHoveredBar()"
                        >
                          <div class="glass-dupont-vpair">
                            <div class="glass-dupont-vcol">
                              <span class="glass-dupont-vval">{{ row.turnoverDisp }}</span>
                              <div class="glass-dupont-vbar-wrap">
                                <span class="glass-dupont-vbar is-turn" :style="{ height: row.turnoverHeight }"></span>
                              </div>
                            </div>
                            <div class="glass-dupont-vcol">
                              <span class="glass-dupont-vval is-lev">{{ row.leverageDisp }}</span>
                              <div class="glass-dupont-vbar-wrap">
                                <span class="glass-dupont-vbar is-lev" :style="{ height: row.leverageHeight }"></span>
                              </div>
                            </div>
                          </div>
                          <span class="glass-dupont-vlbl">{{ row.shortLabel }}</span>
                        </div>
                      </div>
                    </div>

                    <!-- Panel 3: Result: ROE (= 1 × 2) -->
                    <div class="glass-dupont-panel">
                      <div class="glass-dupont-panel-hdr">
                        <strong>{{ isId ? '3. Hasil: ROE (= 1 × 2)' : '3. Result: ROE (= 1 × 2)' }}</strong>
                        <span class="glass-dupont-axis-tag">ROE %</span>
                      </div>
                      <div class="glass-dupont-hrows">
                        <div
                          v-for="row in svgChartData.rows"
                          :key="`r-${row.label}`"
                          class="glass-dupont-hrow is-hoverable"
                          @mouseenter="setHoveredBar(row.label, `ROE ${row.roeDisp}`, row.cause, $event)"
                          @mousemove="moveHoveredBar($event)"
                          @mouseleave="clearHoveredBar()"
                        >
                          <span class="glass-dupont-rlbl">{{ row.label }}</span>
                          <div class="glass-dupont-htrack">
                            <span class="glass-dupont-zero" :style="{ left: svgChartData.roeZeroPct }"></span>
                            <span
                              class="glass-dupont-hbar"
                              :class="`tone-${row.tone}`"
                              :style="{ left: row.roeBarLeft, width: row.roeBarWidth }"
                            ></span>
                          </div>
                          <span class="glass-dupont-rval" :class="`tone-${row.tone}`">{{ row.roeDisp }}</span>
                        </div>
                      </div>
                    </div>
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
                    <g
                      v-for="(r, idx) in svgChartData.rows"
                      :key="r.label"
                      class="svg-hover-row"
                      @mouseenter="setHoveredBar(r.label, r.display, r.cause, $event)"
                      @mousemove="moveHoveredBar($event)"
                      @mouseleave="clearHoveredBar()"
                    >
                      <rect x="0" :y="r.y - 2" :width="svgChartData.W" height="32" rx="6" class="svg-hit-row" />
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
                    <g
                      v-for="(r, idx) in svgChartData.rows"
                      :key="r.label"
                      class="svg-hover-row"
                      @mouseenter="setHoveredBar(r.label, r.display, r.cause, $event)"
                      @mousemove="moveHoveredBar($event)"
                      @mouseleave="clearHoveredBar()"
                    >
                      <rect x="0" :y="r.y - 2" :width="svgChartData.W" height="32" rx="6" class="svg-hit-row" />
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
                    <g
                      v-for="(r, idx) in svgChartData.rows"
                      :key="r.label"
                      class="svg-hover-row"
                      @mouseenter="setHoveredBar(r.label, `${r.displayA} → ${r.displayB}`, r.cause, $event)"
                      @mousemove="moveHoveredBar($event)"
                      @mouseleave="clearHoveredBar()"
                    >
                      <rect x="0" :y="r.y - 2" :width="svgChartData.W" height="38" rx="6" class="svg-hit-row" />
                      <text x="0" :y="r.y + 21" class="svg-lbl">{{ r.label }}</text>
                      <rect :x="svgChartData.labelW" :y="r.y + 2" :width="r.wA" height="13" rx="3.5" class="svg-bar-old svg-anim-bar" :style="{ animationDelay: `${idx * 55}ms` }" />
                      <text :x="svgChartData.labelW + r.wA + 8" :y="r.y + 13" class="svg-val-sm">{{ r.displayA }}</text>
                      <rect :x="svgChartData.labelW" :y="r.y + 19" :width="r.wB" height="15" rx="3.5" class="svg-bar-accent svg-anim-bar" :style="{ animationDelay: `${idx * 55 + 40}ms` }" />
                      <text :x="svgChartData.labelW + r.wB + 8" :y="r.y + 31" class="svg-val-sm is-pos">{{ r.displayB }}</text>
                    </g>
                  </template>
                </svg>
              </div>

              <!-- Slide 7: Pro Forma Key Financial Statement Outcomes (ABOVE driver charts) -->
              <div v-if="slide7ProFormaCards" class="glass-card glass-yoy-wrap">
                <div class="glass-sec-label">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M3 3v18h18" /><path d="M7 16l4-4 4 3 5-7" />
                  </svg>
                  <span>
                    {{
                      chartBasis === 'previous'
                        ? (isId ? 'Hasil Pro Forma Laporan Keuangan — Dek Lama (2025A → 2028F)' : 'Pro Forma Key Financial Statement Outcomes — Old Deck (2025A → 2028F)')
                        : (isId ? 'Hasil Pro Forma Laporan Keuangan — Pasca-Tokopedia (2025A → 2028F · Tabel 12)' : 'Pro Forma Key Financial Statement Outcomes — Post-Tokopedia (2025A → 2028F · Table 12)')
                    }}
                  </span>
                </div>
                <div class="glass-vchart-grid">
                  <div
                    v-for="(card, pIdx) in slide7ProFormaCards"
                    :key="`pf-${card.title}-${chartBasis}`"
                    class="glass-vchart-card"
                    :style="{ animationDelay: `${pIdx * 55}ms` }"
                  >
                    <div class="glass-vchart-hdr">
                      <strong>{{ card.title }}</strong>
                      <span class="glass-yoy-delta" :class="`tone-${card.tone}`">{{ card.delta }}</span>
                    </div>
                    <div class="glass-vchart-plot">
                      <div
                        v-for="(b, bIdx) in card.bars"
                        :key="b.yr"
                        class="glass-vchart-col is-hoverable"
                        @mouseenter="setHoveredBar(`${card.title} (${b.yr})`, b.val, b.cause || card.note || `${card.title}: ${card.delta}`, $event)"
                        @mousemove="moveHoveredBar($event)"
                        @mouseleave="clearHoveredBar()"
                      >
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
                            :style="{ height: `${Math.max(14, b.pct)}%`, animationDelay: `${pIdx * 55 + bIdx * 50}ms` }"
                          ></span>
                        </div>
                        <span class="glass-vchart-lbl">{{ b.yr }}</span>
                      </div>
                    </div>
                    <p v-if="card.note" class="glass-yoy-note">{{ card.note }}</p>
                  </div>
                </div>
              </div>

              <!-- Slide 11: Football Field Benchmarks Breakdown -->
              <div v-if="item.slide?.slide_num === 11" class="glass-card glass-yoy-wrap">
                <div class="glass-sec-label">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M12 3v18" /><path d="M5 7h14" /><path d="M5 17h14" />
                  </svg>
                  <span>{{ isId ? 'Rincian Setiap Bar Valuasi Football Field (Rp / Saham)' : 'What Drives Each Football Field Valuation Bar (Rp / Share)' }}</span>
                </div>
                <div class="glass-vchart-grid">
                  <div class="glass-vchart-card">
                    <div class="glass-vchart-hdr">
                      <strong>{{ isId ? 'Conservative RI' : 'Conservative RI' }}</strong>
                      <span class="glass-yoy-delta tone-warn">−Rp 44.42</span>
                    </div>
                    <p class="glass-yoy-note">
                      {{ isId ? 'Kembali ke lantai biaya 2024 (OpEx 62,78%, COGS 46,64%, pertumbuhan 7,5%) → rugi 2028F −Rp2,29T & menguras kas ke Rp13,52T.' : 'Reverts to 2024 transition costs (62.78% OpEx, 46.64% COGS, 7.5% growth) → −Rp 2.29T 2028F loss & heavy equity charge.' }}
                    </p>
                  </div>
                  <div class="glass-vchart-card">
                    <div class="glass-vchart-hdr">
                      <strong>Base RI (g = 3.0%)</strong>
                      <span class="glass-yoy-delta tone-warn">−Rp 12.23</span>
                    </div>
                    <p class="glass-yoy-note">
                      {{ isId ? 'ROE 2028F (+0,09%) jauh di bawah Ke (8,45%), sehingga rugi residual ~Rp2,4T/thn dikapitalisasi menjadi penalti −Rp35,4T.' : '2028F ROE (+0.09%) trails 8.45% Ke, capitalizing ~Rp 2.4T/yr residual losses in perpetuity (−Rp 35.4T PV penalty; g=0% gives +Rp 0.24).' }}
                    </p>
                  </div>
                  <div class="glass-vchart-card is-focused">
                    <div class="glass-vchart-hdr">
                      <strong>{{ isId ? 'Lantai: Base DCF' : 'Floor: Base DCF' }}</strong>
                      <span class="glass-yoy-delta tone-pos">+Rp 10.38</span>
                    </div>
                    <p class="glass-yoy-note">
                      {{ isId ? 'Kas Bersih +Rp14.012,5M − EV negatif −Rp2.988,5M (ROIC 2,70% < WACC 7,76%) = +Rp11.024,0M ÷ 1.062,01M saham.' : 'Net Cash (+Rp 14,012.5B) minus negative EV (−Rp 2,988.5B, since 2.70% ROIC < 7.76% WACC) = +Rp 11,024.0B ÷ 1,062.01B shares.' }}
                    </p>
                  </div>
                  <div class="glass-vchart-card is-focused">
                    <div class="glass-vchart-hdr">
                      <strong>{{ isId ? 'Pusat: Kas Bersih' : 'Center: Net Cash' }}</strong>
                      <span class="glass-yoy-delta tone-accent">+Rp 13.19</span>
                    </div>
                    <p class="glass-yoy-note">
                      {{ isId ? 'Kas Rp21.755,2M − Total Utang & Sewa Rp7.742,6M = +Rp14.012,5M kas bersih sebagai jangkar lantai likuiditas.' : 'YE25 Cash (Rp 21,755.2B) minus Total Debt & Leases (Rp 7,742.6B) = +Rp 14,012.5B net cash backing the intrinsic range.' }}
                    </p>
                  </div>
                  <div class="glass-vchart-card is-focused">
                    <div class="glass-vchart-hdr">
                      <strong>{{ isId ? 'Plafon: Opt. RI' : 'Ceiling: Opt. RI' }}</strong>
                      <span class="glass-yoy-delta tone-pos">+Rp 16.75</span>
                    </div>
                    <p class="glass-yoy-note">
                      {{ isId ? 'Rasio biaya 1H26 (tumbuh 18%, COGS 38,1%, OpEx 51,2%) angkat EBIT 2028F ke Rp3.221,1M & ROE 6,18% (masih < Ke 8,45%).' : '1H26 cost ratios (18% growth, 38.1% COGS, 51.2% OpEx) lift 2028F EBIT to Rp 3,221.1B & ROE to 6.18% (still < 8.45% Ke).' }}
                    </p>
                  </div>
                  <div class="glass-vchart-card">
                    <div class="glass-vchart-hdr">
                      <strong>Opt. DCF (1H26)</strong>
                      <span class="glass-yoy-delta tone-accent">+Rp 47.34</span>
                    </div>
                    <p class="glass-yoy-note">
                      {{ isId ? 'Mengasumsikan efisiensi OpEx 51,2% & COGS 38,1% bertahan permanen (+Rp1,89T FCFF 2028F); dikecualikan sampai terbukti setahun penuh.' : 'Assumes 51.2% OpEx & 38.1% COGS hold permanently (+Rp 1.89T 2028F FCFF); excluded from base range until full-year execution is proven.' }}
                    </p>
                  </div>
                  <div class="glass-vchart-card">
                    <div class="glass-vchart-hdr">
                      <strong>Grab P/B (3.04×)</strong>
                      <span class="glass-yoy-delta tone-accent">+Rp 91.02</span>
                    </div>
                    <p class="glass-yoy-note">
                      {{ isId ? '3,0391× P/B Grab × BVPS Induk GoTo (Rp29,95); ditolak karena Grab sudah untung (+2,96% ROE) sedangkan GoTo masih −5,23% ROE.' : 'Grab 3.0391× P/B × GoTo Parent BVPS (Rp 29.95); rejected as an actionable target because Grab earns +2.96% ROE vs. GoTo −5.23% ROE.' }}
                    </p>
                  </div>
                </div>
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
                        <div
                          class="glass-vchart-col is-hoverable"
                          @mouseenter="setHoveredBar(`${card.title} (${b.yr})`, b.val, b.cause || card.note || `${card.title}: ${card.delta}`, $event)"
                          @mousemove="moveHoveredBar($event)"
                          @mouseleave="clearHoveredBar()"
                        >
                          <span
                            class="glass-vchart-val"
                            :class="{
                              'is-warn': b.warn || String(b.val).startsWith('−') || (card.tone === 'warn' && b.current),
                              'is-accent': !b.warn && (b.good || (!String(b.val).startsWith('−') && card.tone !== 'warn' && b.current)),
                              'is-amber': b.amber,
                            }"
                          >{{ b.val }}</span>
                          <div class="glass-vchart-bar-wrap">
                            <span
                              class="glass-vchart-bar"
                              :class="[
                                b.warn || card.tone === 'warn' || String(b.val).startsWith('−') ? 'is-warn' : '',
                                !b.warn && (b.good || (!String(b.val).startsWith('−') && b.current && card.tone === 'pos')) ? 'is-accent' : '',
                                b.amber || (!b.warn && !String(b.val).startsWith('−') && b.current && card.tone === 'accent') ? 'is-amber' : '',
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

              <!-- Slide 7: Key Financial Statement Assumptions Table (BELOW charts) -->
              <div v-if="slide7AssumptionsTable" class="glass-card glass-assumptions-card">
                <div class="glass-sec-label">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M3 9h18M3 15h18M9 3v18" />
                  </svg>
                  <span>{{ slide7AssumptionsTable.title }}</span>
                </div>
                <div class="glass-table-scroll">
                  <table class="glass-data-table glass-assumptions-tbl">
                    <thead>
                      <tr>
                        <th v-for="(h, hIdx) in slide7AssumptionsTable.headers" :key="hIdx" :class="{ 'is-base-col': hIdx === 3 }">{{ h }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, rIdx) in slide7AssumptionsTable.rows" :key="rIdx">
                        <td
                          v-for="(cell, cIdx) in row"
                          :key="cIdx"
                          class="is-hoverable-cell"
                          :class="{ 'is-base-col': cIdx === 3 }"
                          @mouseenter="showHoverTip($event, `${row[0]} · ${slide7AssumptionsTable.headers[cIdx]}`, slide7AssumptionsTable.tooltips[rIdx][cIdx])"
                          @mousemove="moveHoverTip($event)"
                          @mouseleave="hideHoverTip"
                        >
                          {{ cell }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Slide 8: Full base forecast stays in the overview below its charts. -->
              <section v-if="slide8ForecastTable" class="glass-card glass-assumptions-card glass-forecast-card" aria-labelledby="slide8-forecast-table-title">
                <div class="glass-sec-label" id="slide8-forecast-table-title">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M3 9h18M3 15h18M9 3v18" />
                  </svg>
                  <span>{{ slide8ForecastTable.title }}</span>
                </div>
                <p class="glass-yoy-note">{{ slide8ForecastTable.note }}</p>
                <div class="glass-table-scroll">
                  <table class="glass-data-table glass-forecast-tbl">
                    <thead>
                      <tr>
                        <th v-for="(header, index) in slide8ForecastTable.headers" :key="index" scope="col">{{ header }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, index) in slide8ForecastTable.rows" :key="index" :class="{ 'is-statement-section': row.is_section }">
                        <th v-if="row.is_section" :colspan="slide8ForecastTable.headers.length" scope="rowgroup">{{ row.label }}</th>
                        <template v-else>
                          <th scope="row">{{ row.label }}</th>
                          <td v-for="(value, yearIndex) in row.values" :key="yearIndex">{{ value }}</td>
                        </template>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>

              <!-- Cursor-Following Hover Card (positioned directly above cursor) -->
              <Teleport to="body">
                <div
                  v-if="hoverTip.visible"
                  class="glass-cursor-tip"
                  :style="{ left: `${hoverTip.x}px`, top: `${hoverTip.y}px` }"
                >
                  <div class="glass-cursor-tip-title">{{ hoverTip.title }}</div>
                  <div class="glass-cursor-tip-body">{{ hoverTip.detail }}</div>
                </div>
              </Teleport>
              <!-- Slide 10: Restated Sensitivity Analysis (TV/PV Calculation Bridges + 2D WACC x g + Beta & RI Checks) -->
              <template v-if="slide10SensitivityTables">
                <div class="glass-card glass-assumptions-card">
                  <div class="glass-sec-label">
                    <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <rect width="16" height="20" x="4" y="2" rx="2" /><line x1="8" x2="16" y1="6" y2="6" /><line x1="8" x2="10" y1="11" y2="11" /><line x1="14" x2="16" y1="11" y2="11" /><line x1="8" x2="10" y1="15" y2="15" /><line x1="14" x2="16" y1="15" y2="15" /><line x1="8" x2="16" y1="19" y2="19" />
                    </svg>
                    <span>{{ slide10SensitivityTables.dcfBridgeTitle }}</span>
                  </div>
                  <div class="glass-table-scroll">
                    <table class="glass-data-table glass-assumptions-tbl">
                      <thead>
                        <tr>
                          <th v-for="(h, hIdx) in slide10SensitivityTables.dcfBridgeHeaders" :key="hIdx">{{ h }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(row, rIdx) in slide10SensitivityTables.dcfBridgeRows"
                          :key="rIdx"
                          :class="{ 'is-base-row': rIdx === 3 || rIdx === 5 }"
                        >
                          <td v-for="(cell, cIdx) in row" :key="cIdx">{{ cell }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div class="glass-card glass-assumptions-card">
                  <div class="glass-sec-label">
                    <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <rect width="16" height="20" x="4" y="2" rx="2" /><line x1="8" x2="16" y1="6" y2="6" /><line x1="8" x2="10" y1="11" y2="11" /><line x1="14" x2="16" y1="11" y2="11" /><line x1="8" x2="10" y1="15" y2="15" /><line x1="14" x2="16" y1="15" y2="15" /><line x1="8" x2="16" y1="19" y2="19" />
                    </svg>
                    <span>{{ slide10SensitivityTables.riBridgeTitle }}</span>
                  </div>
                  <div class="glass-table-scroll">
                    <table class="glass-data-table glass-assumptions-tbl">
                      <thead>
                        <tr>
                          <th v-for="(h, hIdx) in slide10SensitivityTables.riBridgeHeaders" :key="hIdx">{{ h }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(row, rIdx) in slide10SensitivityTables.riBridgeRows"
                          :key="rIdx"
                          :class="{ 'is-base-row': rIdx === 3 || rIdx === 5 }"
                        >
                          <td v-for="(cell, cIdx) in row" :key="cIdx">{{ cell }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div class="glass-card glass-assumptions-card">
                  <div class="glass-sec-label">
                    <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M3 9h18M3 15h18M9 3v18" />
                    </svg>
                    <span>{{ slide10SensitivityTables.gridTitle }}</span>
                  </div>
                  <div class="glass-table-scroll">
                    <table class="glass-data-table glass-assumptions-tbl">
                      <thead>
                        <tr>
                          <th v-for="(h, hIdx) in slide10SensitivityTables.gridHeaders" :key="hIdx" :class="{ 'is-base-col': hIdx === 3 }">{{ h }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(row, rIdx) in slide10SensitivityTables.gridRows" :key="rIdx" :class="{ 'is-base-row': rIdx === 1 }">
                          <td v-for="(cell, cIdx) in row" :key="cIdx" :class="{ 'is-base-col': cIdx === 3 }">{{ cell }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <p class="glass-yoy-note" style="margin-top: 8px;">{{ slide10SensitivityTables.gridNote }}</p>
                </div>

                <div class="glass-card glass-assumptions-card">
                  <div class="glass-sec-label">
                    <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <path d="M12 2v20M2 12h20" />
                    </svg>
                    <span>{{ slide10SensitivityTables.stressTitle }}</span>
                  </div>
                  <div class="glass-table-scroll">
                    <table class="glass-data-table glass-assumptions-tbl">
                      <thead>
                        <tr>
                          <th v-for="(h, hIdx) in slide10SensitivityTables.stressHeaders" :key="hIdx">{{ h }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(row, rIdx) in slide10SensitivityTables.stressRows" :key="rIdx" :class="{ 'is-base-row': rIdx === 0 }">
                          <td
                            v-for="(cell, cIdx) in row"
                            :key="cIdx"
                            :class="{ 'is-hoverable-cell': Boolean(slide10SensitivityTables.stressTooltips?.[rIdx]?.[cIdx]) }"
                            @mouseenter="slide10SensitivityTables.stressTooltips?.[rIdx]?.[cIdx] && showHoverTip($event, slide10SensitivityTables.stressTooltips[rIdx][cIdx].title, slide10SensitivityTables.stressTooltips[rIdx][cIdx].detail)"
                            @mousemove="moveHoverTip($event)"
                            @mouseleave="hideHoverTip"
                          >{{ cell }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </template>

              <!-- Slide 11: 3-Scenario Valuation Matrix & Range Reconciliation -->
              <div v-if="slide11ScenarioMatrix" class="glass-card glass-assumptions-card">
                <div class="glass-sec-label">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M3 9h18M3 15h18M9 3v18" />
                  </svg>
                  <span>{{ slide11ScenarioMatrix.title }}</span>
                </div>
                <div class="glass-table-scroll">
                  <table class="glass-data-table glass-scenario-tbl">
                    <thead>
                      <tr>
                        <th v-for="(h, hIdx) in slide11ScenarioMatrix.headers" :key="hIdx">{{ h }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, rIdx) in slide11ScenarioMatrix.rows" :key="rIdx" :class="{ 'is-base-row': rIdx === 0 }">
                        <td v-for="(cell, cIdx) in row" :key="cIdx">{{ cell }}</td>
                      </tr>
                    </tbody>
                  </table>
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
              <div class="glass-chart-head" style="margin-bottom: 10px;">
                <div class="glass-sec-label" style="margin-bottom: 0;">
                  <svg class="glass-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <rect width="18" height="18" x="3" y="3" rx="2" /><path d="M3 9h18" /><path d="M3 15h18" /><path d="M9 3v18" />
                  </svg>
                  <span>{{ isId ? 'Jadwal Pendukung' : 'Supporting Schedules' }}</span>
                </div>
                <div v-if="item.slide?.slide_num === 8 || item.slide?.slide_num === 19" class="glass-basis-toggle" role="group" :aria-label="isId ? 'Pilih basis laporan' : 'Select report basis'">
                  <button
                    type="button"
                    class="glass-basis-btn is-prev"
                    :class="{ 'is-active': chartBasis === 'previous' }"
                    @click="chartBasis = 'previous'"
                  >
                    {{ isId ? 'Dek Lama (Dengan 2023)' : 'Original Deck (With 2023)' }}
                  </button>
                  <button
                    type="button"
                    class="glass-basis-btn"
                    :class="{ 'is-active': chartBasis === 'current' }"
                    @click="chartBasis = 'current'"
                  >
                    {{ isId ? 'Laporan Akhir (Pasca-Exit)' : 'Final Report (Post-Exit)' }}
                  </button>
                </div>
              </div>
              <div v-for="(sched, sIdx) in displayedSchedules" :key="'gs-' + chartBasis + '-' + sIdx" class="glass-sched-block">
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
          <!-- Compact Abbreviation Glossary Strip -->
        <footer v-if="modalAbbrGlossary.length" class="glass-abbr-footer">
          <span class="glass-abbr-key-lbl">{{ isId ? 'Istilah:' : 'Terms:' }}</span>
          <span v-for="t in modalAbbrGlossary" :key="t.key" class="glass-abbr-chip">
            <strong>{{ t.key }}</strong> {{ t.full }}
          </span>
        </footer>
      </section>
      <div
        v-if="hoveredBar"
        class="glass-float-tooltip"
        :style="{ left: `${tooltipPos.x}px`, top: `${tooltipPos.y}px` }"
        role="tooltip"
      >
        <div class="glass-ft-hdr">
          <strong>{{ hoveredBar.label }}</strong>
          <span class="glass-ft-val">{{ hoveredBar.value }}</span>
        </div>
        <p class="glass-ft-cause">{{ hoveredBar.cause }}</p>
      </div>
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

.glass-tab-right-actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.glass-panel-toggle.is-apx {
  border-color: rgba(134, 239, 172, 0.42);
  background: rgba(34, 197, 94, 0.12);
  color: #bbf7d0;
}

.glass-panel-toggle.is-apx:hover {
  background: rgba(34, 197, 94, 0.28);
  border-color: rgba(134, 239, 172, 0.72);
  color: #ffffff;
}

.glass-abbr-sub {
  font-size: 12px;
  font-weight: 500;
  color: #a7d9b8;
  margin-top: -2px;
  line-height: 1.3;
}

.glass-abbr-footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 12px;
  padding: 8px 24px 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.10);
  background: rgba(0, 0, 0, 0.22);
  font-size: 11px;
  line-height: 1.35;
  color: #a9d5b8;
  flex-shrink: 0;
}

.glass-abbr-key-lbl {
  font-weight: 750;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #86efac;
  font-size: 10px;
}

.glass-abbr-chip strong {
  color: #e8f8ed;
  font-weight: 700;
  margin-right: 3px;
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

.glass-table-scroll {
  width: 100%;
  overflow-x: auto;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(0, 0, 0, 0.22);
}

.glass-data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
  line-height: 1.45;
  color: #e4f5ea;
}

.glass-data-table thead th {
  padding: 10px 14px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;
  color: #a7f3d0;
  background: rgba(255, 255, 255, 0.06);
  border-bottom: 1px solid rgba(255, 255, 255, 0.14);
}

.glass-data-table tbody td {
  padding: 10px 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  vertical-align: middle;
}

.glass-data-table tbody tr:last-child td {
  border-bottom: none;
}

.glass-data-table tbody tr:hover td {
  background: rgba(255, 255, 255, 0.04);
}

.glass-assumptions-tbl th,
.glass-assumptions-tbl td {
  white-space: nowrap;
}

.glass-assumptions-tbl th:not(:first-child),
.glass-assumptions-tbl td:not(:first-child) {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.glass-assumptions-tbl th.is-base-col,
.glass-assumptions-tbl td.is-base-col {
  background: rgba(34, 197, 94, 0.14);
  color: #bbf7d0;
  font-weight: 700;
}

.glass-forecast-card > .glass-yoy-note { margin: 0 0 14px; }
.glass-forecast-tbl { min-width: 720px; }
.glass-forecast-tbl tbody th { padding: 10px 14px; text-align: left; font-weight: 500; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
.glass-forecast-tbl td,
.glass-forecast-tbl thead th:not(:first-child) { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
.glass-forecast-tbl .is-statement-section th { background: rgba(34, 197, 94, 0.14); color: #a7f3d0; font-weight: 750; text-transform: uppercase; letter-spacing: .04em; }

.glass-assumptions-tbl tr.is-base-row td,
.glass-scenario-tbl tr.is-base-row td {
  background: rgba(34, 197, 94, 0.12);
  color: #ffffff;
  font-weight: 700;
}

.glass-scenario-tbl th:nth-child(2),
.glass-scenario-tbl td:nth-child(2),
.glass-scenario-tbl th:nth-child(3),
.glass-scenario-tbl td:nth-child(3) {
  text-align: right;
  white-space: nowrap;
  padding-right: 18px;
  font-variant-numeric: tabular-nums;
}

.glass-scenario-tbl th:nth-child(4),
.glass-scenario-tbl td:nth-child(4) {
  padding-left: 18px;
  color: #c8e7d3;
  line-height: 1.45;
}

.glass-scenario-tbl td:first-child {
  white-space: nowrap;
  font-weight: 600;
  color: #f0fdf4;
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

/* Cursor-Following Hover Card for Slide 7 Assumptions Table */
.glass-assumptions-tbl td.is-hoverable-cell {
  cursor: help;
  transition: background 0.14s ease, color 0.14s ease;
}

.glass-assumptions-tbl td.is-hoverable-cell:hover {
  background: rgba(74, 222, 128, 0.18) !important;
  color: #ffffff;
}

.glass-cursor-tip {
  position: fixed;
  z-index: 99999;
  pointer-events: none;
  transform: translate(-50%, calc(-100% - 14px));
  max-width: 290px;
  padding: 9px 12px;
  border-radius: 10px;
  background: rgba(9, 25, 18, 0.96);
  border: 1px solid rgba(74, 222, 128, 0.55);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(10px);
}

.glass-cursor-tip::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 100%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: rgba(74, 222, 128, 0.55);
}

.glass-cursor-tip-title {
  font-size: 11px;
  font-weight: 750;
  color: #86efac;
  margin-bottom: 3px;
  letter-spacing: 0.02em;
}

.glass-cursor-tip-body {
  font-size: 12px;
  line-height: 1.4;
  color: #eef9f2;
  font-weight: 500;
}

/* Slide 3 Porter's Five Forces Visual Dialogue Walkthrough */
.glass-porter-split {
  display: grid;
  grid-template-columns: minmax(290px, 1.05fr) minmax(380px, 1.45fr);
  gap: 16px;
  padding: 18px 24px;
  align-items: stretch;
  height: 100%;
  box-sizing: border-box;
  overflow-y: auto;
}

.glass-porter-left {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  padding: 16px;
}

.glass-porter-img-wrap {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(74, 222, 128, 0.28);
  background: rgba(5, 18, 11, 0.85);
}

.glass-porter-img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
}

.glass-porter-rating {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 750;
  letter-spacing: 0.03em;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.25);
}

.glass-porter-rating.tone-pos {
  background: rgba(16, 185, 129, 0.85);
  color: #ffffff;
}

.glass-porter-rating.tone-accent {
  background: rgba(245, 158, 11, 0.88);
  color: #0b1610;
}

.glass-porter-rating.tone-warn {
  background: rgba(239, 68, 68, 0.88);
  color: #ffffff;
}

.glass-porter-left-copy {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.glass-porter-headline {
  margin: 0;
  font-size: 14px;
  line-height: 1.45;
  color: #eefaf1;
  font-weight: 600;
}

.glass-porter-right {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px 22px;
  overflow-y: auto;
}

.glass-porter-facts-box {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(74, 222, 128, 0.22);
  border-radius: 12px;
  padding: 18px 20px;
}

.glass-porter-facts {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.glass-porter-facts li {
  font-size: 14px;
  line-height: 1.55;
  color: #e4f5eb;
}

@media (max-width: 820px) {
  .glass-porter-split {
    grid-template-columns: 1fr;
  }
}

/* Three-Step DuPont ROE 3-Panel Breakdown (Slide 4) */
.glass-dupont-wrap {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 6px;
}

.glass-dupont-eq-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.glass-dupont-eq-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 11px;
  border-radius: 999px;
  font-size: 12px;
  background: rgba(251, 191, 36, 0.12);
  border: 1px solid rgba(251, 191, 36, 0.3);
  color: #fde68a;
}

.glass-dupont-eq-pill.is-peer {
  background: rgba(52, 211, 153, 0.12);
  border-color: rgba(52, 211, 153, 0.3);
  color: #a7f3d0;
}

.glass-dupont-eq-pill.is-hurdle {
  background: rgba(148, 163, 184, 0.12);
  border-color: rgba(148, 163, 184, 0.28);
  color: #e2e8f0;
}

.glass-dupont-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.glass-dupont-panel {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(110, 231, 183, 0.14);
  border-radius: 14px;
  padding: 13px 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.glass-dupont-panel-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  flex-wrap: wrap;
}

.glass-dupont-panel-hdr strong {
  font-size: 12.5px;
  color: #ecfdf5;
  letter-spacing: 0.01em;
}

.glass-dupont-axis-tag {
  font-size: 10.5px;
  font-weight: 600;
  color: #a7f3d0;
  background: rgba(16, 185, 129, 0.12);
  padding: 2px 7px;
  border-radius: 999px;
}

.glass-dupont-mini-leg {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 10.5px;
  color: #a7f3d0;
}

.glass-dupont-mini-leg .leg-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 2px;
  margin-right: 4px;
}

.glass-dupont-mini-leg .leg-dot.is-turn {
  background: rgba(167, 243, 208, 0.45);
}

.glass-dupont-mini-leg .leg-dot.is-lev {
  background: #34d399;
}

.glass-dupont-hrows {
  display: flex;
  flex-direction: column;
  gap: 11px;
  justify-content: center;
  flex: 1;
}

.glass-dupont-hrow {
  display: grid;
  grid-template-columns: 92px 1fr 56px;
  align-items: center;
  gap: 7px;
}

.glass-dupont-rlbl {
  font-size: 11px;
  color: #d1fae5;
  line-height: 1.2;
}

.glass-dupont-htrack {
  position: relative;
  height: 18px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 5px;
  overflow: hidden;
}

.glass-dupont-zero {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1.5px;
  background: rgba(236, 253, 245, 0.35);
  z-index: 2;
}

.glass-dupont-hbar {
  position: absolute;
  top: 2px;
  bottom: 2px;
  border-radius: 3px;
  z-index: 1;
}

.glass-dupont-hbar.tone-crimson { background: rgba(244, 63, 94, 0.85); }
.glass-dupont-hbar.tone-amber   { background: rgba(251, 113, 133, 0.72); }
.glass-dupont-hbar.tone-blue    { background: rgba(253, 164, 175, 0.62); }
.glass-dupont-hbar.tone-emerald { background: linear-gradient(90deg, #34d399, #10b981); }

.glass-dupont-rval {
  font-size: 11.5px;
  font-weight: 700;
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.glass-dupont-rval.tone-crimson { color: #fda4af; }
.glass-dupont-rval.tone-amber   { color: #fecdd3; }
.glass-dupont-rval.tone-blue    { color: #ffe4e6; }
.glass-dupont-rval.tone-emerald { color: #6ee7b7; }

.glass-dupont-vplot {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 6px;
  align-items: end;
  flex: 1;
  padding-top: 6px;
}

.glass-dupont-vgroup {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.glass-dupont-vpair {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 118px;
}

.glass-dupont-vcol {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
  gap: 3px;
}

.glass-dupont-vval {
  font-size: 9.5px;
  font-weight: 700;
  color: rgba(209, 250, 229, 0.75);
  font-variant-numeric: tabular-nums;
}

.glass-dupont-vval.is-lev {
  color: #6ee7b7;
}

.glass-dupont-vbar-wrap {
  width: 14px;
  height: 94px;
  display: flex;
  align-items: flex-end;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 4px;
  overflow: hidden;
}

.glass-dupont-vbar {
  width: 100%;
  border-radius: 3px 3px 0 0;
}

.glass-dupont-vbar.is-turn {
  background: rgba(167, 243, 208, 0.42);
}

.glass-dupont-vbar.is-lev {
  background: linear-gradient(180deg, #34d399, #059669);
}

.glass-dupont-vlbl {
  font-size: 10px;
  color: rgba(209, 250, 229, 0.72);
  text-align: center;
  white-space: pre-line;
  line-height: 1.15;
}

@media (max-width: 1080px) {
  .glass-dupont-grid {
    grid-template-columns: 1fr;
  }
}

.glass-vchart-val.is-amber {
  color: #fcd34d;
}

.glass-vchart-bar.is-amber {
  background: linear-gradient(180deg, #fbbf24 0%, #d97706 100%);
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.28);
}

/* Floating Mouse-Following Tooltip */
.glass-float-tooltip {
  position: fixed;
  z-index: 99999;
  pointer-events: none;
  width: max-content;
  max-width: 330px;
  transform: translate(-50%, calc(-100% - 14px));
  background: rgba(6, 28, 18, 0.95);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(52, 211, 153, 0.48);
  border-radius: 11px;
  padding: 9px 12px;
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.58);
}

.glass-float-tooltip::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 100%;
  transform: translateX(-50%);
  border-width: 6px 6px 0 6px;
  border-style: solid;
  border-color: rgba(52, 211, 153, 0.48) transparent transparent transparent;
}

.glass-ft-hdr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 4px;
}

.glass-ft-hdr strong {
  font-size: 11.5px;
  font-weight: 700;
  color: #ecfdf5;
}

.glass-ft-val {
  font-size: 11.5px;
  font-weight: 700;
  color: #6ee7b7;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.glass-ft-cause {
  margin: 0;
  font-size: 12px;
  line-height: 1.4;
  color: #d1fae5;
}

.is-hoverable {
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.15s ease, transform 0.15s ease, filter 0.15s ease;
}

.is-hoverable:hover {
  background: rgba(52, 211, 153, 0.09);
  filter: brightness(1.08);
}

.svg-hover-row {
  cursor: pointer;
}

.svg-hit-row {
  fill: transparent;
  transition: fill 0.15s ease;
}

.svg-hover-row:hover .svg-hit-row {
  fill: rgba(52, 211, 153, 0.1);
}

.svg-hover-row:hover .svg-anim-bar {
  filter: brightness(1.14);
}
</style>
