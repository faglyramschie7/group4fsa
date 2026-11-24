const GLOSSARY = [
  { key: 'BVPS', regex: /\bBVPS\b/, en: 'Book Value Per Share', id: 'Nilai Buku per Saham' },
  { key: 'NOPAT', regex: /\bNOPAT\b/, en: 'Net Operating Profit After Tax', id: 'Laba Operasi Bersih Setelah Pajak' },
  { key: 'EBIAT', regex: /\bEBIAT\b/, en: 'Earnings Before Interest After Tax', id: 'Laba Sebelum Bunga Setelah Pajak' },
  { key: 'EBITDA', regex: /\bEBITDA\b/, en: 'Earnings Before Interest, Taxes, Depreciation & Amortization', id: 'Laba Sebelum Bunga, Pajak, Depresiasi & Amortisasi' },
  { key: 'EBIT', regex: /\bEBIT\b/, en: 'Earnings Before Interest & Taxes (Operating Profit)', id: 'Laba Sebelum Bunga & Pajak (Laba Operasi)' },
  { key: 'WACC', regex: /\bWACC\b/, en: 'Weighted Average Cost of Capital', id: 'Biaya Modal Rata-Rata Tertimbang' },
  { key: 'CAPM', regex: /\bCAPM\b/, en: 'Capital Asset Pricing Model', id: 'Model Penentuan Harga Aset Modal' },
  { key: 'FCFF', regex: /\bFCFF\b/, en: 'Free Cash Flow to Firm', id: 'Arus Kas Bebas untuk Perusahaan' },
  { key: 'FCF', regex: /\bFCF\b/, en: 'Free Cash Flow', id: 'Arus Kas Bebas' },
  { key: 'CFO', regex: /\bCFO\b/, en: 'Cash Flow from Operations', id: 'Arus Kas dari Aktivitas Operasi' },
  { key: 'CFI', regex: /\bCFI\b/, en: 'Cash Flow from Investing', id: 'Arus Kas dari Aktivitas Investasi' },
  { key: 'DCF', regex: /\bDCF\b/, en: 'Discounted Cash Flow', id: 'Arus Kas Terdiskonto' },
  { key: 'RI', regex: /\bRI\b/, en: 'Residual Income (Economic Profit)', id: 'Laba Residual (Laba Ekonomi)' },
  { key: 'ROIC', regex: /\bROIC\b/, en: 'Return on Invested Capital', id: 'Imbal Hasil atas Modal Diinvestasikan' },
  { key: 'ROE', regex: /\bROE\b/, en: 'Return on Equity', id: 'Imbal Hasil atas Ekuitas' },
  { key: 'ROA', regex: /\bROA\b/, en: 'Return on Assets', id: 'Imbal Hasil atas Aset' },
  { key: 'P/B', regex: /\bP\/B\b/, en: 'Price-to-Book Ratio', id: 'Rasio Harga terhadap Nilai Buku' },
  { key: 'P/E', regex: /\bP\/E\b/, en: 'Price-to-Earnings Ratio', id: 'Rasio Harga terhadap Laba' },
  { key: 'EV', regex: /\bEV\b/, en: 'Enterprise Value', id: 'Nilai Perusahaan' },
  { key: 'COGS', regex: /\bCOGS\b/, en: 'Cost of Goods Sold', id: 'Beban Pokok Pendapatan' },
  { key: 'OpEx', regex: /\bOpEx\b/i, en: 'Operating Expenses', id: 'Beban Operasional' },
  { key: 'CapEx', regex: /\bCapEx\b/i, en: 'Capital Expenditures', id: 'Belanja Modal' },
  { key: 'D&A', regex: /\bD&A\b/, en: 'Depreciation & Amortization', id: 'Depresiasi & Amortisasi' },
  { key: 'DSO', regex: /\bDSO\b/, en: 'Days Sales Outstanding', id: 'Hari Penagihan Piutang' },
  { key: 'DPO', regex: /\bDPO\b/, en: 'Days Payable Outstanding', id: 'Hari Pembayaran Utang' },
  { key: 'DIO', regex: /\bDIO\b/, en: 'Days Inventory Outstanding', id: 'Hari Persediaan' },
  { key: 'CCC', regex: /\bCCC\b/, en: 'Cash Conversion Cycle', id: 'Siklus Konversi Kas' },
  { key: 'TIE', regex: /\bTIE\b/, en: 'Times Interest Earned (Interest Coverage)', id: 'Rasio Cakupan Bunga' },
  { key: 'DOL', regex: /\bDOL\b/, en: 'Degree of Operating Leverage', id: 'Derajat Leverage Operasi' },
  { key: 'ATO', regex: /\bATO\b/, en: 'Asset Turnover', id: 'Perputaran Aset' },
  { key: 'EM', regex: /\bEM\b/, en: 'Equity Multiplier', id: 'Pengganda Ekuitas' },
  { key: 'ERP', regex: /\bERP\b/, en: 'Equity Risk Premium', id: 'Premi Risiko Ekuitas' },
  { key: 'CRP', regex: /\bCRP\b/, en: 'Country Risk Premium', id: 'Premi Risiko Negara' },
  { key: 'Ke', regex: /\bKe\b/, en: 'Cost of Equity', id: 'Biaya Ekuitas' },
  { key: 'Kd', regex: /\bKd\b/, en: 'Cost of Debt', id: 'Biaya Utang' },
  { key: 'Rf', regex: /\bRf\b/, en: 'Risk-Free Rate', id: 'Tingkat Bebas Risiko' },
  { key: 'GM', regex: /\bGM\b/, en: 'Gross Margin', id: 'Margin Laba Kotor' },
  { key: 'GTV', regex: /\bGTV\b/, en: 'Gross Transaction Value', id: 'Nilai Transaksi Bruto' },
  { key: 'GMV', regex: /\bGMV\b/, en: 'Gross Merchandise Value', id: 'Nilai Barang Dagangan Bruto' },
  { key: 'NWC', regex: /\bNWC\b/, en: 'Net Working Capital', id: 'Modal Kerja Bersih' },
  { key: 'BVE', regex: /\bBVE\b/, en: 'Book Value of Equity', id: 'Nilai Buku Ekuitas' },
  { key: 'MVE', regex: /\bMVE\b/, en: 'Market Value of Equity', id: 'Nilai Pasar Ekuitas' },
  { key: 'NI', regex: /\bNI\b/, en: 'Net Income', id: 'Laba Bersih' },
  { key: 'EBT', regex: /\bEBT\b/, en: 'Earnings Before Tax', id: 'Laba Sebelum Pajak' },
  { key: 'GAAP', regex: /\bGAAP\b/, en: 'Generally Accepted Accounting Principles', id: 'Standar Akuntansi Berlaku Umum' },
  { key: 'YoY', regex: /\bYoY\b/, en: 'Year-over-Year', id: 'Tahun-ke-Tahun' },
  { key: 'bps', regex: /\bbps\b/, en: 'Basis Points (100 bps = 1%)', id: 'Basis Poin (100 bps = 1%)' },
]

export function findAbbrTerms(text, lang = 'en', maxItems = 8) {
  if (!text) return []
  const str = String(text)
  const found = []
  const seen = new Set()
  for (const item of GLOSSARY) {
    if (seen.has(item.key)) continue
    if (item.regex.test(str)) {
      // Avoid redundant subtitle if the full English term is already written right in the string
      const full = lang === 'id' ? item.id : item.en
      if (str.toLowerCase().includes(full.toLowerCase())) continue
      seen.add(item.key)
      found.push({ key: item.key, full })
      if (found.length >= maxItems) break
    }
  }
  return found
}

export function getInlineAbbrHint(label, lang = 'en') {
  const hits = findAbbrTerms(label, lang, 2)
  if (!hits.length) return ''
  return hits.map((h) => (hits.length === 1 ? h.full : `${h.key}: ${h.full}`)).join(' · ')
}
