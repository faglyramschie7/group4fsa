import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import json

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json") as f:
    modules = json.load(f)

# Tailored, rich empirical data reports specifically corresponding to each slide in Week 2
w2_goto_reports = {
    1: {
        "title": "PT GoTo Gojek Tokopedia Tbk (IDX: GOTO) Profile & Milestone Context",
        "badge": "Company Background",
        "content_type": "profile",
        "description": "GoTo was formed by the May 2021 mega-merger of Gojek (ride-hailing, food delivery, e-wallet) and Tokopedia (e-commerce). It conducted an IPO on the Indonesia Stock Exchange (IDX) in April 2022 at Rp 338 per share, raising Rp 15.8 trillion. Following continuous multi-trillion rupiah annual losses, GoTo restructured in early 2024 by transferring a 75.01% controlling stake in Tokopedia to ByteDance (TikTok Shop) for $1.5 billion in funding commitments. GoTo retained a 24.99% non-controlling associate interest, shifting GoTo toward an asset-light on-demand services (ODS) and fintech platform.",
        "key_metrics": [
            {"label": "Ticker", "val": "IDX: GOTO"},
            {"label": "IPO Date & Price", "val": "11 April 2022 @ Rp 338"},
            {"label": "Current Traded Price", "val": "Rp 25.00 (-92.6% from IPO)"},
            {"label": "Shares Outstanding", "val": "1,062,010.2 Million Shares"}
        ]
    },
    2: {
        "title": "Step 1: GoTo Business Strategy Positioning (Milestone 1)",
        "badge": "Strategy Architecture",
        "content_type": "text_cards",
        "description": "In Milestone 1, Group 4 identified GoTo's core strategic dilemma: GoTo attempts an ecosystem differentiation strategy ('hyper-local Indonesian everyday app') combining Gojek mobility, food, and GoPay financial services. However, on-demand services behave as commoditized utility networks where customers switch instantly to Grab or Maxim for trivial price differences. Because differentiation does not command a durable price premium, GoTo cannot achieve cost leadership due to massive technology hosting and server maintenance overhead.",
        "key_metrics": [
            {"label": "Core Segments", "val": "On-Demand Services (ODS) & Fintech"},
            {"label": "E-Commerce Model", "val": "Asset-light service fee from ByteDance"},
            {"label": "Moat Assessment", "val": "Narrow / Fragile (Low Switching Costs)"}
        ]
    },
    3: {
        "title": "GoTo Three-Year Audited Financial Snapshot (Rp billion) — Mirroring the ABBA Challenge",
        "badge": "Comparative Financial Snapshot",
        "content_type": "table",
        "table_headers": ["Line Item (Rp billion)", "2023A", "2024A", "2025A", "YoY Change (2025)"],
        "table_rows": [
            ["Gross Revenue / Net Revenue", "14,785.4", "15,888.7", "18,322.2", "+15.3%"],
            ["Cost of Revenue (COGS)", "(5,081.7)", "(7,403.4)", "(7,746.2)", "+4.6%"],
            ["Gross Profit", "9,703.7", "8,485.3", "10,576.0", "+24.6%"],
            ["Operating Expenses (Sales, G&A, Tech)", "(20,017.3)", "(10,724.8)", "(10,954.1)", "+2.1%"],
            ["Operating Loss (EBIT)", "(10,313.6)", "(2,239.5)", "(378.1)", "-83.1% (Loss narrowed)"],
            ["Goodwill Impairment & Restructuring", "(79,481.2)", "0.0", "0.0", "None in 2025"],
            ["Net Income / (Loss) for the Year", "(90,516.3)", "(5,471.2)", "(1,501.7)", "-72.6% (Loss narrowed)"],
            ["Total Assets", "54,087.6", "46,146.4", "45,758.1", "-0.8%"],
            ["Total Debt (Short-Term + Long-Term)", "3,514.2", "3,820.0", "7,742.6", "+102.7% (Debt doubled!)"],
            ["Total Shareholders' Equity", "35,720.5", "35,720.5", "28,711.7", "-19.6%"],
            ["Cash & Cash Equivalents", "20,996.3", "21,003.8", "21,755.2", "+3.6%"],
            ["Cash Flow from Operations (CFO)", "(3,942.1)", "(762.4)", "307.0", "Turned positive (1.7% of rev)"],
            ["Free Cash Flow (FCF = CFO - Capex)", "(4,159.2)", "(1,414.7)", "(875.3)", "Remains strictly negative!"]
        ],
        "analytical_note": "Direct Comparison with ABBA: Like ABBA, GoTo shows 'losses narrowing' on the surface (from -Rp 90.5T in 2023 to -Rp 1.50T in 2025). But look at the balance sheet and debt: GoTo doubled total debt to Rp 7,742.6 bn, suffered a negative Free Cash Flow of (Rp 875.3 bn), and accumulated retained losses of Rp 214.1 trillion."
    },
    4: {
        "title": "GoTo's Four Financial Statements Structure",
        "badge": "Statement Architecture",
        "content_type": "cards_and_badges",
        "description": "GoTo's financial report follows PSAK / IFRS standards: 1) Consolidated Statement of Profit or Loss (Period 2025); 2) Consolidated Statement of Financial Position (Snapshot at 31 Dec 2025); 3) Consolidated Statement of Changes in Equity (Period 2025); 4) Consolidated Statement of Cash Flows (Period 2025).",
        "key_metrics": [
            {"label": "Income Statement", "val": "-Rp 1,501.7 bn", "note": "Net Loss for FY2025"},
            {"label": "Balance Sheet", "val": "Rp 45,758.1 bn", "note": "Total Assets at Dec 31"},
            {"label": "Cash Flows", "val": "+Rp 307.0 bn CFO", "note": "Operating cash generated"},
            {"label": "Equity Statement", "val": "Rp 28,711.7 bn", "note": "Ending equity base"}
        ]
    },
    5: {
        "title": "GoTo 2025 Consolidated Income Statement Decomposition (LK GOTO p. 4)",
        "badge": "Statement 1: Income Statement",
        "content_type": "table",
        "table_headers": ["Income Statement Line Item", "2024A (Rp bn)", "2025A (Rp bn)", "% of 2025 Revenue"],
        "table_rows": [
            ["Net Revenue", "15,888.7", "18,322.2", "100.0%"],
            ["Cost of Revenue (COGS)", "(7,403.4)", "(7,746.2)", "42.3%"],
            ["Gross Profit", "8,485.3", "10,576.0", "57.7%"],
            ["Sales and Marketing Expenses", "(3,195.4)", "(3,024.1)", "16.5%"],
            ["General and Administrative Expenses", "(5,214.2)", "(5,712.5)", "31.2%"],
            ["Product Development (R&D)", "(2,315.2)", "(2,217.5)", "12.1%"],
            ["Total Operating Expenses", "(10,724.8)", "(10,954.1)", "59.8%"],
            ["Operating Loss (EBIT)", "(2,239.5)", "(378.1)", "-2.1%"],
            ["Finance Costs (Interest Expense)", "(385.1)", "(535.2)", "2.9%"],
            ["Share of Losses of Associates", "(2,846.6)", "(588.4)", "3.2%"],
            ["Net Loss for the Year", "(5,471.2)", "(1,501.7)", "-8.2%"]
        ],
        "analytical_note": "Key Takeaway: Total operating expenses (59.8%) still exceed gross margin (57.7%), generating a core operating deficit of (Rp 378.1 bn). GoTo has not yet reached structural operating profitability."
    },
    6: {
        "title": "GoTo Statement of Changes in Equity — Tracing the Rp 7.0 Trillion Equity Contraction",
        "badge": "Statement 2: Changes in Equity",
        "content_type": "table",
        "table_headers": ["Equity Component", "Beginning 2025", "2025 Net Movements", "Ending 2025 (Balance Sheet)"],
        "table_rows": [
            ["Share Capital", "1,184.4", "0.0", "1,184.4"],
            ["Additional Paid-in Capital (Agio)", "242,108.5", "0.0", "242,108.5"],
            ["Treasury Stock", "(4,215.1)", "0.0", "(4,215.1)"],
            ["Differences from Restructuring & Associates", "(3,825.2)", "(5,507.2)", "(9,332.4)"],
            ["Accumulated Losses (Retained Deficit)", "(212,617.1)", "(1,501.7)", "(214,118.8)"],
            ["Total Equity Attributable to Parent", "22,635.5", "(7,008.9)", "15,626.6"],
            ["Non-Controlling Interests (NCI)", "13,085.0", "0.1", "13,085.1"],
            ["Total Consolidated Equity", "35,720.5", "(7,008.8)", "28,711.7"]
        ],
        "analytical_note": "Critical Audit Insight: Cumulative deficit reached (Rp 214.1 trillion). Equity contracted from Rp 35.72T to Rp 28.71T. If GoTo continues to lose Rp 3.7T to Rp 4.5T per year (as projected in Milestone 4 Base Case), book equity will be wiped out within 5 to 7 years."
    },
    7: {
        "title": "Visual Statement Articulation: How Net Loss Feeds Retained Deficit",
        "badge": "Articulation Visual",
        "content_type": "text_cards",
        "description": "The 2025 Net Loss of (Rp 1,501.7 bn) links directly into the Retained Earnings account on the Balance Sheet, expanding GoTo's cumulative deficit from (Rp 212.6 trillion) to (Rp 214.1 trillion). At the same time, this loss serves as the starting baseline in the Statement of Cash Flows.",
        "key_metrics": [
            {"label": "Income Statement Net Loss", "val": "(Rp 1,501.7 bn)"},
            {"label": "Ending Accumulated Deficit", "val": "(Rp 214,118.8 bn)"},
            {"label": "Balance Sheet Impact", "val": "-19.6% Total Equity"}
        ]
    },
    8: {
        "title": "GoTo 2025 Audited Balance Sheet (Statement of Financial Position)",
        "badge": "Statement 3: Balance Sheet",
        "content_type": "table",
        "table_headers": ["Balance Sheet Category (Rp bn)", "2024A", "2025A", "% of 2025 Total Assets"],
        "table_rows": [
            ["Cash & Cash Equivalents", "21,003.8", "21,755.2", "47.5% (Largest Asset)"],
            ["Trade & Other Receivables", "475.2", "547.3", "1.2%"],
            ["Inventories", "15.8", "14.1", "0.03% (Digital Platform)"],
            ["Investment in Associates (Tokopedia & Jago)", "11,248.5", "10,344.6", "22.6%"],
            ["Property, Plant & Equipment (Net)", "712.4", "622.1", "1.4% (Asset-Light)"],
            ["Goodwill & Intangible Assets", "4,820.6", "4,528.9", "9.9%"],
            ["Other Operating & Non-Current Assets", "7,870.1", "7,945.9", "17.4%"],
            ["TOTAL ASSETS", "46,146.4", "45,758.1", "100.0%"],
            ["Short-Term Bank Borrowings & Payables", "2,342.1", "2,778.2", "6.1%"],
            ["Long-Term Debt & Liabilities", "8,083.8", "14,268.2", "31.2%"],
            ["TOTAL LIABILITIES", "10,425.9", "17,046.4", "37.3% (+63.5% YoY)"],
            ["TOTAL SHAREHOLDERS' EQUITY", "35,720.5", "28,711.7", "62.7% (-19.6% YoY)"]
        ],
        "analytical_note": "Solvency Alert: While Assets contracted (-0.8%), Liabilities expanded from Rp 10.4T to Rp 17.0T (+63.5%), driven by new bank borrowings. Debt/Equity rose from 0.13x to 0.27x."
    },
    9: {
        "title": "GoTo Balance Sheet Working Capital Structure",
        "badge": "Working Capital Forensics",
        "content_type": "cards_and_badges",
        "description": "GoTo operates with negative operating working capital: Trade Receivables (Rp 547.3 bn) + Inventory (Rp 14.1 bn) minus Accounts Payable (Rp 1,254.4 bn) equals -Rp 693.0 billion. Because GoTo collects platform fees immediately while delaying disbursements to merchants and suppliers (DPO = 59.1 days vs DSO = 10.9 days), it operates on vendor-funded working capital.",
        "key_metrics": [
            {"label": "Days Sales Outstanding (DSO)", "val": "10.9 days"},
            {"label": "Days Payable Outstanding (DPO)", "val": "59.1 days"},
            {"label": "Net Operating Working Capital", "val": "-Rp 693.0 bn"}
        ]
    },
    10: {
        "title": "GoTo 2025 Statement of Cash Flows: Operating, Investing, and Financing",
        "badge": "Statement 4: Cash Flows",
        "content_type": "table",
        "table_headers": ["Cash Flow Activity (Rp billion)", "2024A", "2025A", "Forensic Interpretation"],
        "table_rows": [
            ["Cash Flow from Operations (CFO)", "(762.4)", "307.0", "Turned positive, but covers only 26% of Capex"],
            ["Capital Expenditures (Capex - PP&E & Tech)", "(652.3)", "(1,182.4)", "Consists of Rp 302.1m PP&E + Rp 880.3m software"],
            ["Free Cash Flow (FCF = CFO - Capex)", "(1,414.7)", "(875.3)", "Remains strictly negative!"],
            ["Net Cash from Other Investing Activities", "1,424.8", "1,094.6", "Cashing in Rp 1,386.5 bn time deposits"],
            ["Net Cash from Financing Activities", "(241.2)", "2,494.4", "Borrowed Rp 3,718.0 bn in new bank debt"],
            ["Net Increase in Cash & Equivalents", "7.5", "751.4", "Closing Cash: Rp 21,755.2 billion"]
        ],
        "analytical_note": "The False Turnaround Unmasked: Cash rose by Rp 751 bn not because GoTo was profitable, but because it liquidated time deposits and borrowed Rp 3.72 trillion in debt!"
    },
    11: {
        "title": "Statement Articulation in GoTo's Forecast Model (Milestone 4)",
        "badge": "Forecasting Articulation",
        "content_type": "text_cards",
        "description": "In Group 4's Milestone 4 Pro Forma forecast, the four statements articulate dynamically: 2026F forecast Net Loss of (Rp 3,737.0 bn) flows into the Balance Sheet to reduce Equity from Rp 28,711.7 bn to Rp 24,974.7 bn. Operating cash burn (-Rp 4,143 bn) and Capex (-Rp 3,330 bn) drain cash on the Balance Sheet from Rp 21,755 bn down to Rp 14,282 bn.",
        "key_metrics": [
            {"label": "2026F Forecast Net Loss", "val": "(Rp 3,737.0 bn)"},
            {"label": "2026F Forecast Ending Cash", "val": "Rp 14,282.2 bn"},
            {"label": "2028F Forecast Ending Cash", "val": "Rp 968.0 bn (Near zero!)"}
        ]
    },
    12: {
        "title": "Accrual vs. Cash Accounting in GoTo's Revenue Model",
        "badge": "Revenue Recognition Mechanics",
        "content_type": "text_cards",
        "description": "On GoTo's platform: 1) Gojek on-demand mobility revenue is recognized on an accrual basis at the exact moment a trip is completed; 2) GoPay merchant transaction fees are recognized when the digital payment is processed; 3) E-commerce service fees from ByteDance are accrued quarterly. In contrast, cash disbursements to driver wallets and partner merchants follow distinct batch settlement cycles.",
        "key_metrics": [
            {"label": "Mobility Recognition", "val": "Point in Time (trip completion)"},
            {"label": "Take-Rate Mechanism", "val": "Net commission under PSAK 72"},
            {"label": "Deferred Revenue", "val": "Rp 412.5 bn (unredeemed points)"}
        ]
    },
    13: {
        "title": "GoTo Trade Receivables & Collection Cycle",
        "badge": "Receivables Forensics",
        "content_type": "cards_and_badges",
        "description": "Corporate delivery accounts, B2B digital advertising clients, and institutional payment partners create Trade Receivables of Rp 547.3 billion at Dec 31, 2025. Days Sales Outstanding (DSO) improved from 46.9 days in 2024 to 10.9 days in 2025, demonstrating tight credit controls on corporate clients.",
        "key_metrics": [
            {"label": "Trade Receivables 2025", "val": "Rp 547.3 bn"},
            {"label": "Days Sales Outstanding", "val": "10.9 days (3-yr avg: 24.2d)"},
            {"label": "Allowance for Doubtful Debts", "val": "Rp 148.2 bn"}
        ]
    },
    14: {
        "title": "Why GoTo's Net Income and CFO Diverged by Rp 1.8 Trillion in 2025",
        "badge": "Accrual vs Cash Divergence",
        "content_type": "table",
        "table_headers": ["Reconciliation Step", "Amount (Rp billion)", "Economic Explanation"],
        "table_rows": [
            ["Reported Net Loss for FY2025", "(1,501.7)", "Accrual loss from ongoing operations"],
            ["Add: Depreciation of PP&E", "285.2", "Non-cash wear and tear of servers and equipment"],
            ["Add: Amortization of Intangibles", "1,086.9", "Non-cash amortization of capitalized software"],
            ["Add: Share-Based Compensation Expense", "412.5", "Non-cash equity incentives issued to staff"],
            ["Add: Share of Associate Losses", "588.4", "Non-cash equity accounting loss for Tokopedia/Jago"],
            ["Change in Working Capital & Other Adjustments", "435.7", "Vendor payables timing and deferred income"],
            ["Operating Cash Flow (CFO)", "+307.0", "Actual cash collected from customers less cash paid to staff/vendors"]
        ],
        "analytical_note": "FSA Lesson: CFO turned positive (+Rp 307 bn) strictly because Rp 1.8 trillion of non-cash D&A and equity losses were added back, not because GoTo's core business earned real economic profits."
    },
    15: {
        "title": "GoTo Period Performance vs. Point-in-Time Solvency",
        "badge": "Time Horizon Comparison",
        "content_type": "cards_and_badges",
        "description": "Analyst must distinguish between GoTo's 365-day flow and its midnight balance sheet snapshot: GoTo generated Rp 18,322 bn revenue and burned Rp 535 bn in interest during 2025 (Period). On December 31, 2025, it owed Rp 7,743 bn in debt against Rp 21,755 bn in cash (Snapshot).",
        "key_metrics": [
            {"label": "Annual Revenue (Flow)", "val": "Rp 18,322.2 bn / year"},
            {"label": "Annual Interest Expense (Flow)", "val": "Rp 535.2 bn / year"},
            {"label": "Static Cash Balance (Snapshot)", "val": "Rp 21,755.2 bn at Dec 31"},
            {"label": "Total Debt Obligations (Snapshot)", "val": "Rp 7,742.6 bn at Dec 31"}
        ]
    },
    16: {
        "title": "Navigating GoTo's 2025 Annual Report (Laporan Tahunan)",
        "badge": "Filing Structure",
        "content_type": "text_cards",
        "description": "GoTo's 2025 Annual Report spans 482 pages. While the front MD&A emphasizes 'growth in gross transaction value' and 'ecosystem synergy', professional analysts verify claims against the audited Notes: Note 4 (Segments), Note 11 (Associates), Note 18 (Borrowings), and Note 37 (Commitments).",
        "key_metrics": [
            {"label": "Audited Section", "val": "Pages 285–482 (Financial Statements)"},
            {"label": "External Auditor", "val": "PwC Indonesia (KAP Tanudiredja, Wibisana, Rintis & Rekan)"},
            {"label": "Audit Opinion", "val": "Unqualified with Emphasis of Matter"}
        ]
    },
    17: {
        "title": "Where Real Substance Lives: Auditor's Opinion & Footnotes in GoTo",
        "badge": "Audit Forensics",
        "content_type": "text_cards",
        "description": "PwC's Independent Auditor's Report issued an Unqualified Opinion with an 'Emphasis of Matter' regarding the deconsolidation of Tokopedia and the carrying valuation of investments in associates. The audit confirmed GoTo's accounting compliance, but highlighted ongoing strategic volatility.",
        "key_metrics": [
            {"label": "Emphasis of Matter 1", "val": "Valuation of 24.99% Tokopedia Associate Stake"},
            {"label": "Emphasis of Matter 2", "val": "Recoverability of Intangible Tech Assets"},
            {"label": "Key Audit Matter", "val": "Fintech Expected Credit Loss (ECL) Model"}
        ]
    },
    18: {
        "title": "Accessing GoTo IDX Filings on idx.co.id",
        "badge": "Regulatory Compliance",
        "content_type": "cards_and_badges",
        "description": "GoTo trades under ticker GOTO on the Main Board of the Indonesia Stock Exchange. Periodic quarterly reports (Laporan Keuangan) and Annual Reports (Laporan Tahunan) are submitted to OJK and published on idx.co.id.",
        "key_metrics": [
            {"label": "Stock Exchange", "val": "Bursa Efek Indonesia (IDX)"},
            {"label": "Ticker Symbol", "val": "GOTO (ISIN: ID1000166903)"},
            {"label": "Listing Board", "val": "Main Board (Papan Utama)"},
            {"label": "OJK Registration", "val": "Effective 25 March 2022"}
        ]
    },
    19: {
        "title": "Why Strategy Analysis Comes First: Interpreting GoTo's Ratios",
        "badge": "Strategy Context",
        "content_type": "text_cards",
        "description": "GoTo's gross margin is 57.7%. In manufacturing, a 57.7% gross margin is spectacular. But in gig-economy on-demand platforms, gross profit only subtracts driver revenue share and payment gateway fees. It ignores the huge 59.8% opex required for marketing, tech hosting, and administrative salaries, leaving operating margin negative at -2.1%.",
        "key_metrics": [
            {"label": "Gross Margin", "val": "57.7% (Looks healthy)"},
            {"label": "Operating Expenses %", "val": "59.8% of Revenue"},
            {"label": "Operating Margin", "val": "-2.1% (Unprofitable)"}
        ]
    },
    20: {
        "title": "Porter's Five Forces Applied to GoTo (Milestone 1 Summary)",
        "badge": "Five Forces Overview",
        "content_type": "cards_and_badges",
        "description": "Group 4's Milestone 1 findings: 4 of the 5 forces work against GoTo, creating structural profitability headwinds. This explains why GoTo's ROE remains negative despite rapid top-line Indonesian digital economy growth.",
        "key_metrics": [
            {"label": "1. New Entrants", "val": "Moderate Threat"},
            {"label": "2. Supplier Power", "val": "Moderate to High"},
            {"label": "3. Buyer Power", "val": "Extremely High"},
            {"label": "4. Substitutes", "val": "Moderate to High"},
            {"label": "5. Competitive Rivalry", "val": "Cutthroat / Unfavorable"}
        ]
    },
    21: {
        "title": "Force 1: Threat of New Entrants for GoTo",
        "badge": "Force 1: Entrants",
        "content_type": "text_cards",
        "description": "Building a nationwide multi-sided gig network requires hundreds of millions of dollars in driver acquisition and app development. However, well-capitalized foreign tech entrants (e.g., ByteDance, Maxim, InDrive) circumvent barriers by partnering or launching aggressive low-cost pricing models in secondary tier-2/tier-3 Indonesian cities.",
        "key_metrics": [
            {"label": "Capital Barrier", "val": "Very High for Startups"},
            {"label": "Foreign Tech Risk", "val": "High (ByteDance, Maxim)"},
            {"label": "Regulatory Protection", "val": "Low (OJK/Kemenhub open to entrants)"}
        ]
    },
    22: {
        "title": "Force 2: Bargaining Power of GoTo's Suppliers (Drivers & Merchants)",
        "badge": "Force 2: Suppliers",
        "content_type": "text_cards",
        "description": "GoTo's suppliers are 2.7+ million driver-partners and 1.8+ million GoFood merchants. Because switching costs between Gojek, Grab, and Maxim are low, drivers multi-app simultaneously. Any attempt by GoTo to cut driver subsidies or hike take-rates sparks protests and volume diversion to Grab.",
        "key_metrics": [
            {"label": "Driver Switching Cost", "val": "Near Zero (Multi-apping)"},
            {"label": "Merchant Concentration", "val": "Fragmented MSMEs with high alternative options"},
            {"label": "Labor Regulations", "val": "Rising social security & tariff pressures"}
        ]
    },
    23: {
        "title": "Force 3: Bargaining Power of GoTo's Buyers (Consumers)",
        "badge": "Force 3: Buyers",
        "content_type": "text_cards",
        "description": "Indonesian digital consumers have been conditioned by 10 years of venture capital subsidies. Switching between Gojek and Grab takes 5 seconds on a smartphone. Consumers check both apps and book the ride or food delivery with the lowest net fare or highest promotional discount.",
        "key_metrics": [
            {"label": "Customer Switching Cost", "val": "Absolute Zero"},
            {"label": "Brand Loyalty", "val": "Very Low (Promo-Driven)"},
            {"label": "Price Elasticity", "val": "High (Price sensitive for transport)"}
        ]
    },
    24: {
        "title": "Force 4: Threat of Substitutes for GoTo Services",
        "badge": "Force 4: Substitutes",
        "content_type": "text_cards",
        "description": "For mobility: Jakarta MRT, LRT, TransJakarta buses, KRL Commuter Line, and private motorbikes. For food delivery: Eating at local warungs or cooking at home. For GoPay fintech: Bank Indonesia's zero-fee QRIS merchant network and BI-FAST direct interbank transfers.",
        "key_metrics": [
            {"label": "Transport Substitutes", "val": "MRT / LRT / KRL / TransJakarta"},
            {"label": "Fintech Substitutes", "val": "BI-FAST & QRIS Direct Bank Apps"},
            {"label": "Delivery Substitutes", "val": "Offline Dining & In-store pickup"}
        ]
    },
    25: {
        "title": "Force 5: Competitive Rivalry in Indonesia's Digital Duopoly",
        "badge": "Force 5: Rivalry",
        "content_type": "text_cards",
        "description": "GoTo and Grab operate in a duopoly in on-demand services across Southeast Asia. In Indonesia, Grab boasts superior operational efficiency and profitable regional cash flows from Singapore, allowing it to compete aggressively in pricing. In fintech, GoPay battles ShopeePay, DANA, and major commercial bank apps (BCA, Mandiri).",
        "key_metrics": [
            {"label": "Key Competitor (ODS)", "val": "Grab Holdings Ltd (NASDAQ: GRAB)"},
            {"label": "Key Competitors (Fintech)", "val": "ShopeePay, DANA, OVO, BCA Livin'"},
            {"label": "Rivalry Intensity", "val": "Cutthroat (Margin destroying)"}
        ]
    },
    26: {
        "title": "Reading GoTo's Overall Strategic Picture: Four of Five Forces Unfavorable",
        "badge": "Strategic Synthesis",
        "content_type": "cards_and_badges",
        "description": "Despite operating in an Indonesian digital economy that expanded to over $80 billion in GMV, GoTo has accumulated Rp 214.1 trillion in losses. Unfavorable industry forces transfer all economic gains away from shareholders to price-sensitive buyers and gig-worker suppliers.",
        "key_metrics": [
            {"label": "Indonesian Digital Economy GMV", "val": "$82 Billion (Growing >13% CAGR)"},
            {"label": "GoTo Cumulative Losses", "val": "Rp 214.1 Trillion Deficit"},
            {"label": "Strategic Conclusion", "val": "Industry forces prevent economic rents"}
        ]
    },
    27: {
        "title": "Cost Leadership vs. Differentiation: GoTo Stuck in the Middle",
        "badge": "Generic Strategy",
        "content_type": "text_cards",
        "description": "GoTo attempts to differentiate as an integrated national platform, but consumers refuse to pay a price premium over Grab. Meanwhile, GoTo's heavy tech overhead and central office staff prevent it from matching Maxim's low-cost structure. Being caught in the middle leaves GoTo with negative economic profit.",
        "key_metrics": [
            {"label": "Intended Strategy", "val": "Ecosystem Differentiation"},
            {"label": "Market Pricing Power", "val": "None (Commodity mobility)"},
            {"label": "Competitive Risk", "val": "Stuck in the middle (Porter warning)"}
        ]
    },
    28: {
        "title": "Key Strategic Takeaways for GoTo (Milestone 1 Conclusion)",
        "badge": "Milestone 1 Conclusion",
        "content_type": "cards_and_badges",
        "description": "1) GoTo's narrowing net loss does not signal an operational turnaround yet; 2) Industry structure prevents sustainable high margins; 3) Valuation must penalize ongoing cash burn rather than projecting magical peer multiples.",
        "key_metrics": [
            {"label": "Accounting Reality", "val": "Free Cash Flow is Negative (Rp 875.3 bn)"},
            {"label": "Industry Ceiling", "val": "4 of 5 forces unfavorable"},
            {"label": "Forecast Implication", "val": "Base Case requires Rp 27.2T for breakeven"}
        ]
    }
}

# Attach this rich report into each slide of Week 2
for m in modules:
    if m["id"] == "week2":
        for s in m["slides"]:
            num = s["slide_num"]
            if num in w2_goto_reports:
                s["goto_report"] = w2_goto_reports[num]

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json", "w", encoding="utf-8") as f:
    json.dump(modules, f, ensure_ascii=False, indent=2)

print("Saved rich slide-by-slide GoTo empirical reports for all 28 slides of Week 2!")
