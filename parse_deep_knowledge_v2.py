import json

modules = [
    {
        "id": "week1",
        "week": "Week 1",
        "title": "The FSA Mindset & Six-Step Framework",
        "reading": "Wahlen Ch. 1 • Subramanyam Ch. 1",
        "category": "Foundations",
        "core_question": "Who is reading the financial statements, and what specific decision question are they trying to answer?",
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
            "title": "Group 4 Stakeholder Persona for GoTo",
            "type": "cards_and_badges",
            "persona": "Long-Term Public Equity Investor (IDX: GOTO)",
            "context": "Evaluating GoTo at Rp 25.00 following the Tokopedia deconsolidation and BEI price floor reform.",
            "decision": "SELL / AVOID. GoTo destroys shareholder value under historical cost structures and burns through its cash cushion.",
            "metrics": [
                {"label": "Target User", "val": "Public Equity Investor", "note": "Primary lens throughout Weeks 1-16"},
                {"label": "Current Market Price", "val": "Rp 25.00", "note": "Down 93% from Rp 338 IPO"},
                {"label": "Group 4 Decision", "val": "SELL / AVOID", "note": "Cash burn and negative economic value"},
                {"label": "Net Cash Floor", "val": "Rp 13.20", "note": "Rp 14.01T net cash / 1.06T shares"}
            ],
            "key_takeaways": [
                "Financial statement analysis is never a mechanical calculation: the user determines the critical question.",
                "Steps 1 to 3 look backward into the firm; Steps 4 to 6 look forward to act.",
                "Never skip steps: valuation without accounting analysis is pure fiction."
            ]
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
            "title": "GoTo Strategy & Industry Economics (Milestone 1)",
            "type": "five_forces",
            "strategy": "Hybrid / Differentiation via Hyper-Local Ecosystem, but lacks Cost Leadership.",
            "verdict": "Unfavorable industry economics prevent GoTo from achieving sustainable operating profits without continuous incentive cuts.",
            "forces": [
                {"force": "1. Threat of New Entrants", "rating": "Moderate", "analysis": "High capital barrier to build an ecosystem, but low switching costs allow niche fintechs or foreign giants (Bytedance/TikTok) to enter through partnerships."},
                {"force": "2. Bargaining Power of Suppliers", "rating": "Moderate to High", "analysis": "Gig-economy drivers and merchants have multi-apping flexibility. Attempts to increase take-rates or cut driver incentives trigger strikes or churn."},
                {"force": "3. Bargaining Power of Buyers", "rating": "Extremely High", "analysis": "Consumers experience near-zero switching costs between Grab, Gojek, Maxim, ShopeeFood, and InDrive. Habitual promo-seeking erodes pricing power."},
                {"force": "4. Threat of Substitutes", "rating": "Moderate to High", "analysis": "Public transit (MRT, LRT, TransJakarta), offline dining, direct bank transfers (BI-FAST), and cash alternatives."},
                {"force": "5. Competitive Rivalry", "rating": "Cutthroat / Unfavorable", "analysis": "Duopoly competition against Grab in On-Demand Services (ODS) and against Sea Ltd (Shopee) / TikTok in e-commerce and fintech creates perpetual margin suppression."}
            ]
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
            "title": "GoTo Balance Sheet Accounting Reality (2025 Audited Balance Sheet)",
            "type": "accounting_items",
            "items": [
                {
                    "name": "Investment in Associates (Tokopedia & Bank Jago)",
                    "standard": "PSAK 15 (Equity Method)",
                    "amount": "Rp 10,344.6 billion (22.6% of Total Assets)",
                    "finding": "GoTo owns 24.99% of PT Tokopedia and 21.4% of PT Bank Jago Tbk. Under equity method, only GoTo's net share of profits/losses appears on the income statement, obscuring Tokopedia's actual underlying cash burn from GoTo's top-line revenue."
                },
                {
                    "name": "Intangibles & Historical Goodwill",
                    "standard": "PSAK 48 / PSAK 22 (Impairment & Combinations)",
                    "amount": "Rp 4,528.9 billion carrying value",
                    "finding": "Goodwill is never amortized: tested annually for impairment. GoTo previously took over Rp 70 trillion in goodwill impairments post-2021 merger, proving historical overpayment and balance sheet inflation."
                },
                {
                    "name": "Cash, Cash Equivalents & Time Deposits",
                    "standard": "PSAK 50 / 55 / 71 (Financial Instruments)",
                    "amount": "Rp 21,755.2 billion (47.5% of Total Assets)",
                    "finding": "The single largest asset on GoTo's balance sheet. However, cash rose in 2025 not from operations (+Rp 307 bn), but from cashing in Rp 1.39T of time deposits and borrowing Rp 3.72T of new third-party bank debt."
                }
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
            "title": "The 2025 Audited Cash Flow Reality (LK GOTO pp. 21-22)",
            "type": "cash_flow",
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
            "type": "dupont_table",
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
            "title": "GoTo Altman Z''-Score Calculation (2025 Audited Balance Sheet)",
            "type": "altman_breakdown",
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
            "type": "red_flags",
            "flags": [
                {
                    "flag": "Tokopedia Deconsolidation Accounting Gain",
                    "severity": "High Impact",
                    "analysis": "GoTo recognized large one-off non-cash accounting adjustments when transferring majority control of Tokopedia to ByteDance in early 2024, creating an artificial boost to reported 2024 earnings that does not repeat in 2025."
                },
                {
                    "flag": "Consumer Lending Credit Loss Provisions Doubling",
                    "severity": "Rising Risk",
                    "analysis": "Fintech loan impairment provisions more than doubled in 2025 to over Rp 1.4 trillion as GoTo aggressively grew GoPay Later buy-now-pay-later (BNPL) loans. Credit costs threaten to wipe out fintech revenue gains."
                },
                {
                    "flag": "Aggressive Software Capitalization vs Operating Expense",
                    "severity": "Medium Concern",
                    "analysis": "GoTo capitalized Rp 880.3 billion in intangible technology assets in 2025 instead of expensing it directly as R&D in opex, flattering operating income at the expense of heavy future amortization."
                }
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
            "title": "GoTo Capital & Financing Structure (2025 Audited Notes 18 & 19)",
            "type": "financing_structure",
            "metrics": [
                {"label": "Total Debt Outstanding", "val": "Rp 7,742.6 billion", "sub": "Doubled (+102.7%) from Rp 3,820.0 billion in 2024"},
                {"label": "Short-Term Debt Portion", "val": "Rp 1,523.8 billion", "sub": "Working capital bank facilities"},
                {"label": "Long-Term Debt Portion", "val": "Rp 6,218.9 billion", "sub": "Term loans and fintech warehouse lines"},
                {"label": "Pre-Tax Effective Cost of Debt", "val": "6.91%", "sub": "Rp 535.2 bn interest expense / Rp 7,742.6 bn debt"},
                {"label": "After-Tax Cost of Debt", "val": "5.39%", "sub": "6.91% x (1 - 22% statutory corporate tax rate)"},
                {"label": "Capital Structure Weight (Wd)", "val": "22.6% Debt / 77.4% Equity", "sub": "Market equity of Rp 26,550 bn at Rp 25 share price"}
            ],
            "analysis": "GoTo transitioned from a purely equity-funded startup to borrowing heavily from commercial banks in 2025. With operating income negative, debt service adds Rp 535 bn to Rp 788 bn of annual cash drain."
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
            "title": "GoTo Intercorporate Holdings & Associate Valuation",
            "type": "investing_activities",
            "holdings": [
                {
                    "entity": "PT Tokopedia (E-Commerce Associate)",
                    "ownership": "24.99% Non-Controlling Interest",
                    "accounting": "PSAK 15 Equity Method",
                    "carrying_value": "~Rp 9.5 Trillion",
                    "details": "Controlled by ByteDance (TikTok Shop). GoTo does not consolidate Tokopedia's gross revenue or operating costs; instead, GoTo receives an e-commerce service fee (~Rp 150-200 bn/quarter) and records its 24.99% share of Tokopedia's net profit/loss."
                },
                {
                    "entity": "PT Bank Jago Tbk (Digital Banking Partner)",
                    "ownership": "21.4% Associate Stake",
                    "accounting": "PSAK 15 Equity Method",
                    "carrying_value": "~Rp 800+ Billion",
                    "details": "Strategic digital bank providing direct integration for GoPay savings accounts, term deposits, and consumer lending balance sheet funding."
                },
                {
                    "entity": "Capital Expenditures (Capex Breakdown)",
                    "ownership": "Consolidated Technology Core",
                    "accounting": "Cash Flow Investing (CFI)",
                    "carrying_value": "Rp 1,182.4 Billion (2025)",
                    "details": "Consists of Rp 302.1 bn physical fixed assets plus Rp 880.3 bn capitalized software and intangible development, consuming 3.8x GoTo's operating cash flow."
                }
            ]
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
            "title": "GoTo Segment Breakdown & Operating Leverage (Milestone 4 Baseline)",
            "type": "segments_and_dol",
            "segments": [
                {
                    "name": "On-Demand Services (ODS - Gojek)",
                    "nature": "Ride-Hailing & Food Delivery",
                    "margin": "Thin Variable Gross Margin",
                    "desc": "Primary volume driver. Faces fierce price competition from Grab and Maxim, requiring ongoing driver and consumer incentives to protect market share."
                },
                {
                    "name": "Financial Technology (Fintech - GoPay)",
                    "nature": "Payments, Lending & BNPL",
                    "margin": "High Take-Rate & Interest Spread",
                    "desc": "Highest growth potential in the group. Consumer loan book expansion provides lucrative interest margins, but requires heavy provisions for credit impairment."
                },
                {
                    "name": "E-Commerce Service Fee (Tokopedia)",
                    "nature": "Ecosystem Revenue Share",
                    "margin": "~100% Flow-Through Margin",
                    "desc": "Contractual service fee paid by ByteDance for maintaining Tokopedia ecosystem integration, providing ~Rp 600-800 bn of annual pure cash margin."
                }
            ],
            "dol_analysis": "Under GoTo's Base Case (where operating expenses scale at 78.5% of sales based on 3-year historical averages), Operating Income (EBIT) is negative in all forecast years (-Rp 4.0T in 2026F to -Rp 5.0T in 2028F). Because EBIT is negative, standard DOL is not reported / not meaningful. GoTo operates Below Breakeven, requiring Rp 27.2 trillion of revenue just to cover costs (vs forecast revenue of Rp 20.4 trillion)."
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
            "type": "proforma_table",
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
            "type": "valuation_complete",
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

print("Updated structured_lectures.json with rich typed structures for every single week!")
