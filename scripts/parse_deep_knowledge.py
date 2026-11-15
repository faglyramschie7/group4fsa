import os as _os, pathlib as _pathlib
_os.chdir(_pathlib.Path(__file__).resolve().parent.parent)

import json

with open("goto-fsa-study/src/data/fsa_knowledgebase.json") as f:
    raw = json.load(f)

# Structure structured lecture modules with:
# 1. Theoretical Concept & Framework (from PPT)
# 2. Key Formulas / Methodologies
# 3. Reading the Hook / Real Classroom Cases (Garuda, ABBA, Bukalapak)
# 4. GoTo Empirical Data Application (How Group 4 applied this to GOTO)
# 5. Study Cards / Q&A for Exam & Defense Preparation

modules = [
    {
        "id": "week1",
        "week": "Week 1",
        "title": "The FSA Mindset & Six-Step Framework",
        "reading": "Wahlen Ch. 1 • Subramanyam Ch. 1",
        "category": "Foundations",
        "core_question": "Who is reading the financial statements, and what question are they trying to answer?",
        "framework": [
            {"step": "Step 1: Business Strategy Analysis", "desc": "Identify industry profit drivers, competitive advantages (Cost Leadership vs Differentiation), and key risks.", "inward": True},
            {"step": "Step 2: Accounting Analysis", "desc": "Evaluate accounting flexibility, red flags, distortions, and restate where necessary.", "inward": True},
            {"step": "Step 3: Financial Analysis", "desc": "Evaluate profitability (DuPont), liquidity, solvency, efficiency, and cash flows.", "inward": True},
            {"step": "Step 4: Forecasting", "desc": "Translate Steps 1-3 into explicit assumptions; build linked 3-statement pro forma model.", "inward": False},
            {"step": "Step 5: Valuation", "desc": "Convert forecast into intrinsic value: DCF, Residual Income, and Multiples. Read the gap.", "inward": False},
            {"step": "Step 6: Decision", "desc": "Translate valuation into a concrete recommendation for a specific stakeholder.", "inward": False}
        ],
        "six_readers": [
            {"reader": "Equity Investor", "question": "Buy, hold, or sell? Is intrinsic value higher than the market price?"},
            {"reader": "Banker / Creditor", "question": "Will they repay? What is cash coverage, solvency, and collateral value?"},
            {"reader": "Regulator (OJK / BEI)", "question": "Are they solvent, orderly, and compliant with accounting standards?"},
            {"reader": "Non-Profit Board", "question": "Is the mission financially sustainable over the long term?"},
            {"reader": "Church / Foundation Treasurer", "question": "Are resources being stewarded faithfully with minimal risk?"},
            {"reader": "Government Auditor (BPK / BPKP)", "question": "Were public funds used as appropriated according to law?"}
        ],
        "goto_application": {
            "title": "Group 4's Stakeholder Persona for GoTo",
            "persona": "Long-Term Public Equity Investor (IDX: GOTO)",
            "context": "Evaluating GoTo at Rp 25.00 following the Tokopedia deconsolidation and BEI price floor reform.",
            "decision": "SELL / AVOID. GoTo destroys shareholder value under historical cost structures and burns through its cash cushion."
        },
        "study_takeaways": [
            "FSA is not a mechanical calculation: the user determines which metric matters.",
            "Steps 1 to 3 look backward into the firm; Steps 4 to 6 look forward to act.",
            "Never skip steps: valuation without accounting analysis is fiction."
        ]
    },
    {
        "id": "week2",
        "week": "Week 2",
        "title": "Refresher & Industry Strategy Analysis (Porter's Five Forces)",
        "reading": "Wahlen Ch. 1 • Subramanyam Ch. 2",
        "category": "Step 1: Strategy",
        "core_question": "What is the source of competitive advantage, and can the industry sustain excess economic rents?",
        "framework_details": "Porter's Five Forces determines industry structure and profitability ceilings. Generic strategies: Cost Leadership vs Differentiation.",
        "goto_five_forces": [
            {"force": "1. Threat of New Entrants", "rating": "Moderate", "analysis": "High capital barrier to build an ecosystem, but low switching costs allow niche fintechs or foreign giants (Bytedance/TikTok) to enter through partnerships."},
            {"force": "2. Bargaining Power of Suppliers", "rating": "Moderate to High", "analysis": "Gig-economy drivers and merchants have multi-apping flexibility. Attempts to increase take-rates or cut driver incentives trigger strikes or churn."},
            {"force": "3. Bargaining Power of Buyers", "rating": "Extremely High", "analysis": "Consumers experience near-zero switching costs between Grab, Gojek, Maxim, ShopeeFood, and InDrive. Habitual promo-seeking erodes pricing power."},
            {"force": "4. Threat of Substitutes", "rating": "Moderate to High", "analysis": "Public transit (MRT, LRT, TransJakarta), offline dining, direct bank transfers (BI-FAST), and cash alternatives."},
            {"force": "5. Competitive Rivalry", "rating": "Cutthroat / Unfavorable", "analysis": "Duopoly competition against Grab in On-Demand Services (ODS) and against Sea Ltd (Shopee) / TikTok in e-commerce and fintech creates perpetual margin suppression."}
        ],
        "goto_application": {
            "title": "GoTo's Strategic Position",
            "strategy": "Hybrid / Differentiation via Hyper-Local Ecosystem, but lacks Cost Leadership.",
            "verdict": "Unfavorable industry economics prevent GoTo from achieving sustainable operating profits without continuous incentive cuts."
        },
        "study_takeaways": [
            "Four of five forces lean unfavorable for GoTo, capping long-run return on invested capital.",
            "Deconsolidating Tokopedia into ByteDance in 2024 stopped catastrophic e-commerce losses, shifting GoTo to an asset-light e-commerce service fee model."
        ]
    },
    {
        "id": "week3",
        "week": "Week 3",
        "title": "Asset/Liability Valuation & Income Recognition (PSAK/IFRS)",
        "reading": "Wahlen Ch. 2 • Subramanyam Ch. 3",
        "category": "Step 2: Accounting",
        "core_question": "Recognition vs Measurement: How do accounting standards capture economic reality on the balance sheet?",
        "framework_details": "Three measurement bases: Historical Cost, Fair Value, and Net Realizable Value (ceiling). PSAK convergence with IFRS.",
        "goto_application": {
            "title": "GoTo's Balance Sheet Measurement Reality",
            "key_issues": [
                {"item": "Investment in Associates (Tokopedia & Bank Jago)", "amount": "Rp 10,344.6 bn (22.6% of Assets)", "treatment": "Equity method accounting under PSAK 15. The balance sheet reflects GoTo's share of net assets, but obscures underlying Tokopedia cash burn."},
                {"item": "Intangible Assets & Goodwill", "amount": "Rp 4,528.9 bn", "treatment": "Tested annually for impairment under PSAK 48. GoTo took massive goodwill write-downs in 2023 following the merger, proving prior overpayment."},
                {"item": "Cash & Time Deposits", "amount": "Rp 21,755.2 bn", "treatment": "Fair value / amortized cost. Represents GoTo's primary remaining asset after multi-year venture capital burn."}
            ]
        },
        "study_takeaways": [
            "Recognition decides IF an asset appears on the balance sheet; Measurement decides AT WHAT NUMBER.",
            "Historical cost provides verifiable conservatism; Fair value provides market relevance but introduces volatile mark-to-market swings."
        ]
    },
    {
        "id": "week4",
        "week": "Week 4",
        "title": "Analyzing the Statement of Cash Flows",
        "reading": "Wahlen Ch. 3 • Subramanyam Ch. 7",
        "category": "Step 2 & 3: Accounting & Financial",
        "core_question": "Direct vs Indirect Method: Is the business generating real cash from operations or living on external debt and asset liquidations?",
        "framework_details": "CFO + CFI + CFF = Net Change in Cash. Free Cash Flow = CFO - Capex. Free Cash Flow to Firm (FCFF) vs Free Cash Flow to Equity (FCFE).",
        "goto_application": {
            "title": "The 2025 Audited Cash Flow Reality (LK GOTO 31 Dec 2025)",
            "cfo": "Rp 307.0 billion (only 1.7% of revenue)",
            "capex": "Rp 1,182.4 billion (Rp 302.1 bn fixed assets + Rp 880.3 bn intangible software)",
            "fcf": "-Rp 875.3 billion (Negative Free Cash Flow)",
            "financing_mask": "Cash rose from Rp 21.00T to Rp 21.76T only because GoTo cashed in Rp 1,386.5 bn time deposits and borrowed Rp 3,718.0 bn of new debt (doubling debt to Rp 7,743 bn)."
        },
        "study_takeaways": [
            "CFO covered only 26.0% of Capex in 2025: core operations do not self-fund capital investment.",
            "Operating cash flow was positive only due to working capital swings and deferred expenses, not underlying operating profitability."
        ]
    },
    {
        "id": "week5",
        "week": "Week 5",
        "title": "Profitability Analysis I: Common-Size & DuPont ROE Framework",
        "reading": "Wahlen Ch. 4 • Subramanyam Ch. 8",
        "category": "Step 3: Financial",
        "core_question": "What is driving Return on Equity: Profit Margins, Asset Efficiency, or Financial Leverage?",
        "framework_details": "Vertical common-size (% of Revenue/Assets), Horizontal trend (% YoY), and 3-Step DuPont ROE = Net Margin x Asset Turnover x Equity Multiplier.",
        "goto_application": {
            "title": "GoTo 3-Step DuPont ROE Breakdown (2023 - 2025)",
            "table": [
                {"metric": "Net Profit Margin", "y2023": "-612.2%", "y2024": "-34.4%", "y2025": "-8.2%", "note": "Huge operating expenses and restructuring costs; loss narrowed in 2025 to -Rp 1.50T."},
                {"metric": "Total Asset Turnover", "y2023": "0.27x", "y2024": "0.37x", "y2025": "0.40x", "note": "Asset turnover improved as balance sheet contracted post-Tokopedia deconsolidation."},
                {"metric": "Equity Multiplier", "y2023": "1.51x", "y2024": "1.42x", "y2025": "1.59x", "note": "Leverage rose in 2025 as equity shrank (-19.6%) and total debt doubled."},
                {"metric": "3-Step DuPont ROE", "y2023": "-253.4%", "y2024": "-18.0%", "y2025": "-5.2%", "note": "Negative in every single year (vs Bukalapak +12.4% fueled by investment gains)."}
            ]
        },
        "study_takeaways": [
            "ROE was negative across all 3 historical years due entirely to negative net profit margins.",
            "Higher equity multiplier in 2025 indicates worsening financial leverage, not healthy capital expansion."
        ]
    },
    {
        "id": "week6",
        "week": "Week 6",
        "title": "Profitability II & Solvency: Altman Z-Score Distress Analysis",
        "reading": "Wahlen Ch. 4-5 • Subramanyam Ch. 9",
        "category": "Step 3: Financial",
        "core_question": "Can the firm meet short-term obligations and survive long-term solvency distress?",
        "framework_details": "Current/Quick ratios, DSO/DIO/DPO cash conversion cycle, Debt/Equity, Interest Coverage, and Altman Z''-Score for Emerging Markets / Non-Manufacturers.",
        "altman_formula": "Z'' = 6.56 X1 + 3.26 X2 + 6.72 X3 + 1.05 X4 (Safe > 2.60, Gray 1.10 - 2.60, Distress < 1.10)",
        "goto_application": {
            "title": "GoTo's Altman Z''-Score Calculation (2025 Audited Balance Sheet)",
            "components": [
                {"x": "X1 (Working Capital / Assets = +0.402)", "score": "+2.64", "expl": "Working capital is Rp 18,412 bn due to large remaining IPO cash."},
                {"x": "X2 (Retained Earnings / Assets = -4.679)", "score": "-15.25", "expl": "Crushed by Rp 214.1 trillion of cumulative historical retained losses."},
                {"x": "X3 (EBIT / Assets = -0.008)", "score": "-0.06", "expl": "Operating loss of -Rp 378 bn in 2025."},
                {"x": "X4 (Book Equity / Total Liabilities = +1.684)", "score": "+1.77", "expl": "Book equity of Rp 28,712 bn vs liabilities of Rp 17,046 bn."}
            ],
            "total_z": "-10.90 (Deep Distress Zone, threshold < 1.10)",
            "takeaway": "GoTo avoids immediate bankruptcy only because X1 (cash cushion) is positive, but continuous burn will exhaust it."
        },
        "study_takeaways": [
            "Interest coverage is -0.71x: operating income cannot cover Rp 535 bn annual interest expense.",
            "Total debt doubled to Rp 7,743 bn in 2025, raising default risk if cash burn does not stop."
        ]
    },
    {
        "id": "week7",
        "week": "Week 7",
        "title": "Accounting Quality & Earnings Management (Red Flags)",
        "reading": "Wahlen Ch. 6 • Subramanyam Ch. 2 & 4",
        "category": "Step 2: Accounting",
        "core_question": "Are profits real economic earnings or accrual distortions, cookie-jar reserves, and aggressive capitalizations?",
        "framework_details": "Red flags: Divergence between Net Income and CFO, rising Days Sales Outstanding (DSO), sudden goodwill impairments, and related party disclosures.",
        "goto_application": {
            "title": "GoTo Accounting Quality Assessment (Milestone 3 Findings)",
            "red_flags": [
                {"flag": "Tokopedia Deconsolidation Gain", "analysis": "Booked massive one-off non-cash accounting adjustments when transferring majority control to ByteDance in 2024."},
                {"flag": "Consumer Lending Credit Losses", "analysis": "Fintech loan impairment provisions more than doubled in 2025 to Rp 1.4+ trillion as GoTo expands buy-now-pay-later (GoPay Later)."},
                {"flag": "Software Capitalization vs Expensing", "analysis": "GoTo capitalized Rp 880.3 bn in intangible technology assets in 2025 instead of expensing it directly in opex."}
            ]
        },
        "study_takeaways": [
            "Accrual quality is medium-low: reported Adjusted EBITDA excludes heavy stock-based compensation and depreciation costs.",
            "Auditors placed Emphasis of Matter on ongoing restructuring and associate carrying values."
        ]
    },
    {
        "id": "week9",
        "week": "Week 9",
        "title": "Analyzing Financing Activities (Debt vs Equity, Bonds & Leases)",
        "reading": "Wahlen Ch. 7 • Subramanyam Ch. 5",
        "category": "Step 2: Accounting",
        "core_question": "How does the firm fund its asset base: Bank debt, corporate bonds, leases (PSAK 73/IFRS 16), or share issuances?",
        "framework_details": "Operating vs Finance Leases under PSAK 73, effective interest method for debt, off-balance-sheet commitments, and hybrid instruments.",
        "goto_application": {
            "title": "GoTo's Financing Structure (2025 Audited Notes 18 & 19)",
            "total_debt": "Rp 7,742.6 billion (doubled from Rp 3,820.0 billion in 2024)",
            "breakdown": "Short-Term Debt: Rp 1,523.8 bn | Long-Term Debt: Rp 6,218.9 bn",
            "effective_cost": "6.91% pre-tax (Rp 535.2 bn interest expense / Rp 7,742.6 bn debt)",
            "capital_structure": "Market Value Equity (Rp 26,550 bn, 77.4%) vs Debt (Rp 7,743 bn, 22.6%)."
        },
        "study_takeaways": [
            "GoTo began taking on substantial commercial bank loans in 2025 to fund working capital and fintech loan book expansion.",
            "Debt doubling in a loss-making company drastically limits borrowing capacity and increases debt service burden."
        ]
    },
    {
        "id": "week10",
        "week": "Week 10",
        "title": "Analyzing Investing Activities & Intercorporate Investments",
        "reading": "Wahlen Ch. 8 • Subramanyam Ch. 5",
        "category": "Step 2: Accounting",
        "core_question": "How are long-term assets and investments accounted for: PP&E, Goodwill, PSAK 15 (Equity Method) vs PSAK 65 (Consolidation)?",
        "framework_details": "Equity method (20-50% ownership) hides investee debt on a single line; Consolidation (>50%) includes 100% assets/debt with Non-Controlling Interest (NCI).",
        "goto_application": {
            "title": "GoTo's Massive Intercorporate Investments",
            "tokopedia": "Retains a 24.99% non-controlling associate stake accounted for via Equity Method under PSAK 15 (carrying value ~Rp 9.5T). Receives quarterly e-commerce service fees from ByteDance.",
            "bank_jago": "Holds ~21.4% associate stake in PT Bank Jago Tbk, driving digital banking integration.",
            "goodwill_risk": "Impairments in past years wiped out over Rp 70 trillion in goodwill following the original 2021 Gojek-Tokopedia merger."
        },
        "study_takeaways": [
            "Equity method keeps Tokopedia's ongoing operational volatility off GoTo's consolidated revenue and gross profit lines.",
            "Carrying value of associates is vulnerable to future impairments if ByteDance/TikTok e-commerce growth slows."
        ]
    },
    {
        "id": "week12",
        "week": "Week 12",
        "title": "Operating Activities: Revenue, Operating Leverage (DOL) & Segments",
        "reading": "Wahlen Ch. 9 • Subramanyam Ch. 6",
        "category": "Step 2: Accounting & Forecasting Bridge",
        "core_question": "How do fixed vs variable costs determine operating leverage and segment profit contributions?",
        "framework_details": "Degree of Operating Leverage (DOL) = % Change in EBIT / % Change in Sales = Contribution Margin / EBIT. Point-in-time vs Over-time revenue recognition.",
        "goto_application": {
            "title": "GoTo's Segment Breakdown & Operating Leverage (Milestone 4 Baseline)",
            "segments": [
                {"name": "On-Demand Services (Gojek)", "role": "Core cash generator; ride-hailing and food delivery. High volume, thin margin."},
                {"name": "Financial Technology (GoPay)", "role": "Fastest growing segment; lending margins are high but offset by credit loan losses."},
                {"name": "E-Commerce Service Fee (Tokopedia)", "role": "High margin revenue stream (~Rp 150-200 bn/quarter) received from ByteDance."}
            ],
            "dol_puzzle": "Under the Base Case historical cost structure, DOL is not reported / not meaningful because EBIT is negative (-Rp 4.0T to -Rp 5.0T). GoTo operates Below Breakeven in all forecast years."
        },
        "study_takeaways": [
            "High fixed technology overhead creates extreme negative operating leverage when revenue growth decelerates.",
            "Breakeven revenue required under Base Case costs is Rp 27.2 trillion (far above forecast revenue of Rp 20.4 trillion)."
        ]
    },
    {
        "id": "week13",
        "week": "Week 13",
        "title": "Forecasting Financial Statements (Sales-Driven Pro Forma Model)",
        "reading": "Wahlen Ch. 10 • Subramanyam Ch. 9",
        "category": "Step 4: Forecasting",
        "core_question": "How do we build linked 3-statement pro forma forecasts with explicit, defensible assumptions?",
        "framework_details": "Sales-driven forecasting: Income statement scales operating costs; Balance sheet scales working capital & PP&E; Cash & Equivalents serves as the Plug.",
        "goto_application": {
            "title": "GoTo 3-Year Base Case Pro Forma Forecast (2026F - 2028F)",
            "assumptions": "Revenue Growth: 11.4% (3-yr avg) | COGS: 41.1% | Cash Opex: 78.5% | Capex: 16.3% | Tax Rate: 22.0%",
            "forecast_table": [
                {"item": "Revenue", "y2025A": "18,322", "y2026F": "20,408", "y2027F": "22,732", "y2028F": "25,321"},
                {"item": "Gross Profit (58.9% margin)", "y2025A": "10,576", "y2026F": "12,016", "y2027F": "13,384", "y2028F": "14,908"},
                {"item": "Operating Expenses (78.5%)", "y2025A": "10,954", "y2026F": "16,020", "y2027F": "17,844", "y2028F": "19,876"},
                {"item": "EBIT (Operating Loss)", "y2025A": "(378)", "y2026F": "(4,003)", "y2027F": "(4,459)", "y2028F": "(4,967)"},
                {"item": "Net Loss", "y2025A": "(1,502)", "y2026F": "(3,737)", "y2027F": "(4,093)", "y2028F": "(4,489)"},
                {"item": "Cash Balance (Balance Sheet Plug)", "y2025A": "21,755", "y2026F": "14,282", "y2027F": "7,642", "y2028F": "968"},
                {"item": "Shareholders' Equity", "y2025A": "28,712", "y2026F": "24,975", "y2027F": "20,882", "y2028F": "16,393"}
            ]
        },
        "study_takeaways": [
            "Cash Plug Sanity Check: Cash drains from Rp 21.8 trillion down to just Rp 968 billion by 2028F.",
            "Shows why historical average costs are unsustainable without aggressive restructuring and cost freezes."
        ]
    },
    {
        "id": "week14",
        "week": "Week 14",
        "title": "Cost of Capital & Valuation Applications (WACC, DCF, RI, Multiples)",
        "reading": "Wahlen Ch. 11-14 • Subramanyam Ch. 11",
        "category": "Step 5: Valuation",
        "core_question": "How do we triangulate intrinsic value across DCF, Residual Income, and Multiples — and Read the Gap?",
        "framework_details": "Emerging Market CAPM: Ke = Rf + Beta x (Mature ERP + CRP). WACC weights based on Market Value of Equity. Gordon Growth Terminal Value. Reading the Gap (Slide 20).",
        "goto_application": {
            "title": "GoTo Complete Valuation Synthesis & Reconciliation",
            "cost_of_capital": {
                "rf": "4.502% (Indo 10y bond 6.12% - 1.618% Baa2 default spread)",
                "beta": "0.59 (from Investing.com)",
                "erp": "6.695% (Mature 4.23% + Indo CRP 2.465%)",
                "ke": "8.45%",
                "kd_after_tax": "5.39% (6.91% pre-tax x (1 - 22%))",
                "market_equity": "Rp 26,550.3 bn (77.4% weight at Rp 25.00 share price)",
                "debt": "Rp 7,742.6 bn (22.6% weight)",
                "wacc": "7.76%"
            },
            "valuation_summary": [
                {"method": "1. DCF Valuation (FCFF)", "implied_share": "Rp (100.9)", "expl": "FCFF burns -Rp 6.0T to -Rp 6.9T/yr. Enterprise Value = -Rp 121.2T. Adding Rp 14.0T net cash yields -Rp 107.2T equity value."},
                {"method": "2. Residual Income", "implied_share": "Rp (75.1)", "expl": "Net losses plus 8.45% equity charge destroy -Rp 6.2T of economic profit per year, completely erasing Rp 28.7T starting book equity."},
                {"method": "3. Market Multiples", "implied_share": "Rp 39.7", "expl": "Peer median P/B (2.10x) implies Rp 56.8; peer median P/E (32.0x) implies Rp 22.7 (based on peers GRAB, SE, BUKA, BELI, UBER)."},
                {"method": "Current Market Price", "implied_share": "Rp 25.00", "expl": "Trades at 0.8x book value (a 20% discount to book equity) on IDX."},
                {"method": "Net Cash Liquidation Floor", "implied_share": "Rp 13.20", "expl": "Rp 14,012.5 bn net cash divided by 1,062.16 billion shares."}
            ],
            "reading_the_gap": "Why does the stock trade at Rp 25.00 when DCF/RI are negative? 1) Shares have limited liability (cannot drop below zero). 2) Net cash provides a hard floor at Rp 13.20. 3) BEI Regulation: Stock was artificially stuck at Rp 50 under the old 'gocap' floor; on Sept 28, 2026, IDX abolished the Rp 50 floor (lowered to Rp 1), triggering ARB and plunging the stock to Rp 25.00."
        },
        "study_takeaways": [
            "DCF and Residual Income converge on the exact same conclusion: GoTo destroys value under historical cost trends.",
            "The market refuses to pay the peer multiple (2.10x P/B = Rp 56.8), treating GoTo as a distressed asset trading at 0.8x book value."
        ]
    }
]

with open("goto-fsa-study/src/data/structured_lectures.json", "w", encoding="utf-8") as f:
    json.dump(modules, f, ensure_ascii=False, indent=2)

print("Created structured_lectures.json with 12 comprehensive lecture modules!")
