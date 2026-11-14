import json

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json") as f:
    modules = json.load(f)

w3 = next((m for m in modules if m["id"] == "week3"), None)
if not w3:
    print("Week 3 not found!")
    exit(1)

# Full slide metadata and deep commentary for Week 3 (19 slides)
w3_data = {
    1: {
        "header": "Asset & Liability Valuation",
        "subtitle": "and Income Recognition",
        "theory_explanation": "Course Orientation & Theme: Asset & Liability Valuation and Income Recognition. Moving from Step 1 (Strategy) deeper into Step 2 (Accounting Analysis). Focuses on how items recognized on the balance sheet are measured and how valuation changes flow into reported income.",
        "goto_explanation": "For GoTo, valuation and measurement are the central battlegrounds of accounting quality. Group 4 analyzes how GoTo carried Rp 93.8T of goodwill post-merger, shifted Tokopedia into an associate under PSAK 15, and accounts for financial instruments at fair value through profit or loss (FVTPL).",
        "goto_report": {
            "title": "GoTo Valuation & Measurement Profile (Accounting Analysis Step 2)",
            "badge": "Module Overview",
            "content_type": "profile",
            "description": "GoTo's consolidated balance sheet represents an asset-light technology platform where physical capital (PP&E) accounts for only 1.4% of total assets (Rp 622.1 bn), while valuation-sensitive intangibles, associate investments, and financial instruments dominate. In Week 3, Group 4 applies the Three Measurement Bases framework to evaluate GoTo's asset reliability versus economic relevance.",
            "key_metrics": [
                {"label": "Total Consolidated Assets", "val": "Rp 45,758.1 billion"},
                {"label": "PP&E (Historical Cost)", "val": "Rp 622.1 bn (1.4% of assets)"},
                {"label": "Investment in Associates", "val": "Rp 10,344.6 bn (22.6% of assets)"},
                {"label": "Goodwill & Software", "val": "Rp 4,528.9 bn (9.9% of assets)"}
            ]
        },
        "audit_evidence": {
            "img": "/evidence/goto_balance_sheet_assets_highlighted.png",
            "title": "Audited Balance Sheet Assets (LK p. 15)",
            "caption": "Official GoTo Balance Sheet: Total Assets of Rp 45,758,110 million dominated by Cash (47.5%) and Associates (22.6%), with PP&E at only 1.4%."
        }
    },
    2: {
        "header": "WHERE WE ARE",
        "subtitle": "Deep Inside Step 2: Accounting Analysis",
        "theory_explanation": "The Six-Step FSA Framework Position: We are in Step 2 (Accounting Analysis). After evaluating business strategy in Step 1, the core question of Step 2 is: Given that an asset or liability is recognized, at what amount should it be carried?",
        "goto_explanation": "Step 2 is crucial for GoTo because management claims an accounting turnaround while book equity contracted from Rp 35.7T to Rp 28.7T. Forensic analysts must inspect whether asset carrying amounts accurately reflect cash-generating ability.",
        "goto_report": {
            "title": "Step 2 Accounting Analysis Applied to GoTo",
            "badge": "Framework Positioning",
            "content_type": "text_cards",
            "description": "In Milestone 2, Group 4 audited whether GoTo's balance sheet reflects economic reality or aggressive accounting discretion. Our finding: GoTo shifted its business model post-Tokopedia restructuring into an asset-light service platform, meaning traditional asset valuation (cost less depreciation) applies to only a tiny sliver of operations.",
            "key_metrics": [
                {"label": "Step 1 Strategy", "val": "Asset-light On-Demand & Fintech Ecosystem"},
                {"label": "Step 2 Accounting", "val": "Evaluating PSAK 16, PSAK 15, and PSAK 71 Carrying Values"},
                {"label": "Key Forensic Finding", "val": "Carrying values distorted by historical merger goodwill and unobservable Level 3 inputs"}
            ]
        }
    },
    3: {
        "header": "A REAL NUMBER",
        "subtitle": "ABBA's Net Fixed Assets, One Year (Rp 19.67bn -> Rp 70.36bn)",
        "theory_explanation": "The Hook: PT Mahaka Media Tbk (ABBA) reported a 3.6x jump in Net Fixed Assets in one year (from Rp 19.67 bn to Rp 70.36 bn) without significant new capital expenditure. How can an asset quadruple without cash being spent? Through upward revaluation under PSAK 16.",
        "goto_explanation": "Contrast ABBA with GoTo: While ABBA boosted assets 3.6x through property revaluation, GoTo's Net PP&E actually contracted from Rp 712.4 bn to Rp 622.1 bn (-12.7%) because GoTo uses the PSAK 16 Cost Model and possesses virtually no real estate to revalue.",
        "goto_report": {
            "title": "Fixed Asset Contrast: ABBA Revaluation Surge vs GoTo Asset-Light Contraction",
            "badge": "Comparative Asset Analysis",
            "content_type": "table",
            "table_headers": ["Company & Fixed Asset Metric", "2024A", "2025A", "YoY Change", "Valuation Basis"],
            "table_rows": [
                ["ABBA Net Fixed Assets (Rp bn)", "19.67", "70.36", "+257.7% (3.6x)", "PSAK 16 Revaluation Model (Fair Value)"],
                ["ABBA New Capital Expenditure (Capex)", "1.24", "2.10", "+69.4%", "Actual Cash Outflow"],
                ["ABBA Revaluation Surplus in Equity", "0.00", "55.08", "New Surplus", "Direct Credit to Equity (OCI)"],
                ["GoTo Property, Plant & Equipment (Net)", "712.4", "622.1", "-12.7%", "PSAK 16 Cost Model (No Revaluation)"],
                ["GoTo Annual Depreciation Expense", "295.6", "285.2", "-3.5%", "Depreciation charged to P&L"],
                ["GoTo PP&E as % of Total Assets", "1.5%", "1.4%", "-0.1%", "Asset-Light Technology Platform"]
            ],
            "analytical_note": "FSA Core Lesson: ABBA's Net Fixed Assets surged from Rp 19.67 bn to Rp 70.36 bn (+257.7%) strictly via a Rp 55.08 bn revaluation surplus, not real operational expansion. In contrast, GoTo's PP&E contracted to Rp 622.1 bn (-12.7%), confirming GoTo is purely asset-light and cannot artificially inflate equity via property revaluations."
        },
        "audit_evidence": {
            "img": "/evidence/GOTO_2025_PDF_p098.png",
            "title": "Audited PP&E Schedule (LK Note 11, p. 98)",
            "caption": "Official GoTo LK Note 11: PP&E carried at historical cost less accumulated depreciation. Ending net book value Rp 622,143 million."
        }
    },
    4: {
        "header": "THE CORE DISTINCTION",
        "subtitle": "Recognition vs. Measurement",
        "theory_explanation": "The Fundamental Distinction: Recognition asks 'Should this item appear on the statements at all, and when?' Measurement asks 'Given that it appears, at what amount should it be carried?' Today focuses on measurement after recognition is decided.",
        "goto_explanation": "For GoTo, recognition vs measurement was tested during the Tokopedia deconsolidation. Once GoTo recognized a 24.99% retained interest, the measurement question was: should it be carried at fair value or equity method? Under PSAK 15, GoTo carries it at Rp 10,344.6 bn.",
        "goto_report": {
            "title": "Recognition vs. Measurement in GoTo Financial Statements",
            "badge": "Core Accounting Principle",
            "content_type": "text_cards",
            "description": "Recognition decisions determine what enters the balance sheet, while measurement rules govern their monetary value. GoTo's financials feature severe measurement disputes between statutory cost and economic fair value.",
            "key_metrics": [
                {"label": "Tokopedia Recognition", "val": "Deconsolidated from subsidiary to associate (PSAK 15)"},
                {"label": "Tokopedia Measurement", "val": "Carried at Rp 10,344.6 bn initial fair value less associate losses"},
                {"label": "Internally Generated Brand", "val": "Unrecognized under PSAK 19 (Gojek brand value = Rp 0 on balance sheet)"},
                {"label": "Audited Software Development", "val": "Recognized & capitalized at Rp 3,906.8 bn under PSAK 19"}
            ]
        }
    },
    5: {
        "header": "A UNIFYING IDEA",
        "subtitle": "The Income Recognition Link",
        "theory_explanation": "The Unifying Balance Sheet Equation: Asset up or Liability down = Income. Liability up or Asset down = Expense. Every income statement event has a balance sheet counterpart. The two statements are not separate stories.",
        "goto_explanation": "This links directly to GoTo's multi-trillion losses: When GoTo recognized Rp 79.5T of goodwill write-downs in 2023, asset contraction created the historic Net Loss of (Rp 90.5T). In 2025, financial instrument fair value drops created (Rp 596.7 bn) in expenses.",
        "goto_report": {
            "title": "GoTo Balance Sheet Contraction & Income Statement Linkage",
            "badge": "Balance Sheet Mechanics",
            "content_type": "text_cards",
            "description": "GoTo demonstrates how balance sheet adjustments directly generate income statement outcomes. Without real economic cash outflows, re-measuring balance sheet assets downwards mechanically triggers net losses.",
            "key_metrics": [
                {"label": "2023 Goodwill Contraction", "val": "-Rp 79,481.2 bn Asset Drop -> -Rp 90,516.3 bn Net Loss"},
                {"label": "2025 Financial Instrument Revaluation", "val": "-Rp 596.7 bn Asset Drop -> -Rp 596.7 bn Fair Value Loss in P&L"},
                {"label": "2025 Associate Equity Accounting", "val": "-Rp 588.4 bn Investment Drop -> -Rp 588.4 bn Loss from Associates"},
                {"label": "Total Non-Operating Valuation Drain", "val": "-Rp 1,185.1 bn subtracted directly from 2025 P&L"}
            ]
        }
    },
    6: {
        "header": "THE FRAMEWORK",
        "subtitle": "Three Measurement Bases: Historical Cost, Fair Value, Net Realizable Value",
        "theory_explanation": "The Three Measurement Bases: 1) Historical Cost (original transaction price), 2) Fair Value (current exit price in an orderly transaction), 3) Net Realizable Value (NRV, ceiling for inventory = estimated selling price minus costs to complete and sell).",
        "goto_explanation": "GoTo's Rp 45.8 trillion balance sheet is a mosaic of these three bases. Understanding which base applies to each asset is essential to assess whether GoTo's assets could ever be liquidated to satisfy its Rp 17.0 trillion in liabilities.",
        "goto_report": {
            "title": "GoTo FY2025 Balance Sheet Decomposed by Measurement Base",
            "badge": "Balance Sheet Framework",
            "content_type": "table",
            "table_headers": ["Asset Class", "Book Value (Rp bn)", "% of Assets", "Measurement Basis", "PSAK Standard"],
            "table_rows": [
                ["Cash & Cash Equivalents", "21,755.2", "47.5%", "Amortized Cost (Face Value)", "PSAK 71 (IFRS 9)"],
                ["Investment in Associates (Tokopedia & Jago)", "10,344.6", "22.6%", "Equity Method (Initial Fair Value)", "PSAK 15 (IAS 28)"],
                ["Other Operating & Non-Current Assets", "7,945.9", "17.4%", "Amortized Cost & Historical Cost", "Various"],
                ["Goodwill & Capitalized Intangibles", "4,528.9", "9.9%", "Cost less Amortization & Impairment", "PSAK 19 / 48 (IAS 38/36)"],
                ["Property, Plant & Equipment (Net)", "622.1", "1.4%", "Historical Cost less Acc. Depreciation", "PSAK 16 (IAS 16)"],
                ["Trade & Consumer Receivables (GoPay Later)", "547.3", "1.2%", "Amortized Cost less ECL Allowance", "PSAK 71 (IFRS 9)"],
                ["Inventories", "14.1", "0.03%", "Lower of Cost and Net Realizable Value (NRV)", "PSAK 14 (IAS 2)"],
                ["TOTAL ASSETS", "45,758.1", "100.0%", "Hybrid Mosaic Measurement", "Comprehensive PSAK Framework"]
            ],
            "analytical_note": "Audit Breakdown: Cash (47.5%) and Associates (22.6%) comprise over 70% of GoTo's assets. Fixed assets (1.4%) and inventory (0.03%) are negligible. GoTo's balance sheet health depends on the recoverable value of its associate stakes under PSAK 15, not physical liquidation value."
        },
        "audit_evidence": {
            "img": "/evidence/goto_balance_sheet_assets_highlighted.png",
            "title": "Audited Statement of Financial Position (LK p. 15)",
            "caption": "Official GoTo Balance Sheet: Total Assets of Rp 45,758,110 million categorized by measurement standards."
        }
    },
    7: {
        "header": "BASIS 1 OF 3",
        "subtitle": "Historical Cost: Reliability vs. Staleness",
        "theory_explanation": "Historical Cost: The original transaction price paid, unadjusted for later price changes. Strength: Reliability (grounded in an objective, completed transaction). Weakness: Stale (bears little resemblance to current economic value as market conditions evolve).",
        "goto_explanation": "Goodwill from the 2021 Gojek-Tokopedia merger is the textbook example of historical cost staleness. Capitalized at Rp 93.8 trillion based on peak tech-bubble valuations in May 2021, the historical cost became completely detached from reality, culminating in the 2023 mega write-off.",
        "goto_report": {
            "title": "Historical Cost Staleness: The GoTo Goodwill Case Study",
            "badge": "Valuation Vulnerability",
            "content_type": "text_cards",
            "description": "Historical cost assumes that transaction prices retain validity. When Gojek merged with Tokopedia at the height of zero-interest-rate tech valuations, GoTo recorded colossal historical goodwill that subsequently collapsed.",
            "key_metrics": [
                {"label": "Original Merger Goodwill (2021)", "val": "Rp 93,837.2 billion (Historical Cost)"},
                {"label": "Staleness Trigger", "val": "Tech bubble deflation, rising global rates, e-commerce fee compression"},
                {"label": "2023 Impairment Write-Down", "val": "-Rp 79,481.2 billion (Recognized in P&L)"},
                {"label": "Ending Audited Goodwill (2025)", "val": "Rp 4,528.9 billion (Carried post-Tokopedia deconsolidation)"}
            ]
        },
        "audit_evidence": {
            "img": "/evidence/Carrying_Value_Goodwill_Reconciliation.png",
            "title": "Goodwill Impairment Reconciliation (LK Note 12)",
            "caption": "Official GoTo LK Note 12: Historical cost of goodwill reduced by Rp 79.5 trillion cumulative impairment testing."
        }
    },
    8: {
        "header": "BASIS 2 OF 3",
        "subtitle": "Fair Value: Relevance vs. Estimation Risk",
        "theory_explanation": "Fair Value: The price received to sell an asset or paid to transfer a liability in an orderly transaction today. Strength: Relevance (reflects current economic conditions). Weakness: Relies on estimates and subjective models, especially Level 2 and Level 3 inputs.",
        "goto_explanation": "GoTo holds financial assets and liabilities measured at fair value through profit or loss (FVTPL) under PSAK 71. In 2025, fair value remeasurements generated a net loss of (Rp 596.7 bn), directly proving how fair value volatility impacts accounting income.",
        "goto_report": {
            "title": "GoTo Fair Value Portfolio & Sensitivity (PSAK 71 / IFRS 13)",
            "badge": "Fair Value Volatility",
            "content_type": "text_cards",
            "description": "GoTo's fair value accounting introduces substantial quarterly income swings. Unlike amortized cost instruments, fair value forces GoTo to mark volatile startup equity stakes and call options to market.",
            "key_metrics": [
                {"label": "Financial Instruments at FVTPL", "val": "Rp 1,027.8 billion (Level 2 & Level 3 inputs)"},
                {"label": "2025 Fair Value P&L Impact", "val": "(Rp 596.7 billion) net loss charged to profit or loss"},
                {"label": "Bank Jago Equity Valuation", "val": "Marked using IDX quoted share prices (Level 1)"},
                {"label": "Tokopedia Option Liability", "val": "Marked using Black-Scholes option pricing model (Level 3)"}
            ]
        },
        "audit_evidence": {
            "img": "/evidence/goto_income_statement_highlighted.png",
            "title": "Audited FY2025 P&L (LK p. 17)",
            "caption": "Official GoTo LK p. 17: 'Penyesuaian nilai wajar instrumen keuangan' showing Rp (596,703) million fair value loss."
        }
    },
    9: {
        "header": "BASIS 3 OF 3",
        "subtitle": "Net Realizable Value (NRV): A Downward Ceiling, Not a Basis",
        "theory_explanation": "Net Realizable Value (NRV): Estimated selling price minus estimated costs of completion and disposal. NRV applies narrowly to inventory under PSAK 14 (lower of cost and NRV). It acts as a one-way downward check, never writing inventory above cost.",
        "goto_explanation": "For manufacturing or retail companies like ABBA (newsprint) or Astra, NRV is critical. For GoTo, inventory is merely Rp 14.1 billion (merchandise and payment terminals), representing 0.03% of total assets, highlighting GoTo's asset-light digital platform status.",
        "goto_report": {
            "title": "Inventory & Net Realizable Value in GoTo (PSAK 14 Analysis)",
            "badge": "Asset-Light Model",
            "content_type": "text_cards",
            "description": "Because GoTo operates as an intermediary platform connecting drivers, merchants, and consumers, it carries virtually zero physical inventory risk compared to traditional supply chain businesses.",
            "key_metrics": [
                {"label": "GoTo 2025 Inventory Balance", "val": "Rp 14.1 billion (LK Note 7)"},
                {"label": "% of Total Consolidated Assets", "val": "0.03% (Negligible balance sheet impact)"},
                {"label": "Inventory Composition", "val": "GoPay EDC payment terminals, SIM cards, merchant hardware"},
                {"label": "NRV Write-Down Risk", "val": "Minimal (Technology obsolescence capped at <Rp 5 bn)"}
            ]
        }
    },
    10: {
        "header": "SIDE BY SIDE",
        "subtitle": "Historical Cost vs. Fair Value Matrix",
        "theory_explanation": "The Definitive Comparison: Historical Cost vs Fair Value across four dimensions: Initial measurement, subsequent measurement, income statement effect, and typical PSAK standards (PSAK 16 vs PSAK 13/71).",
        "goto_explanation": "Group 4 constructed a side-by-side matrix showing how GoTo's balance sheet accounts split between Historical Cost (PP&E, Software) and Fair Value (Marketable securities, FVTPL derivatives).",
        "goto_report": {
            "title": "GoTo Accounting Policy Matrix: Cost Model vs Fair Value Model",
            "badge": "Accounting Policy Matrix",
            "content_type": "table",
            "table_headers": ["GoTo Asset Category", "Carrying Value (Rp bn)", "Subsequent Measurement", "Income Statement Effect", "Applicable PSAK"],
            "table_rows": [
                ["Property, Plant & Equipment", "622.1", "Cost less depreciation", "Depreciation expense only; no write-ups", "PSAK 16 (IAS 16)"],
                ["Capitalized Software & Intangibles", "3,906.8", "Cost less amortization", "Amortization expense + annual impairment test", "PSAK 19 (IAS 38)"],
                ["Investment in Associates", "10,344.6", "Equity method (adjusted cost)", "Share of associate net profits / (losses)", "PSAK 15 (IAS 28)"],
                ["Financial Instruments at FVTPL", "1,027.8", "Fair value remeasured quarterly", "Unrealized gains / (losses) directly in P&L", "PSAK 71 (IFRS 9)"],
                ["Cash & Time Deposits", "21,755.2", "Amortized cost", "Interest income recognized over time", "PSAK 71 (IFRS 9)"]
            ],
            "analytical_note": "Comparative Insight: GoTo avoids the volatility of fair valuing its operational assets (PP&E and software under cost models), but is exposed to quarterly P&L swings via financial instruments (FVTPL) and associate accounting under PSAK 15."
        },
        "audit_evidence": {
            "img": "/evidence/GOTO_2025_PDF_p066.png",
            "title": "Summary of Significant Accounting Policies (LK Note 2, p. 66)",
            "caption": "Official GoTo LK Note 2: Definitive accounting policies detailing cost models for PP&E and FVTPL for financial instruments."
        }
    },
    11: {
        "header": "INDONESIA-SPECIFIC CONTEXT",
        "subtitle": "PSAK / IFRS Convergence",
        "theory_explanation": "Institutional Framework: Indonesia's DSAK-IAI issues Standar Akuntansi Keuangan (PSAK), substantially converged with IFRS. The specific PSAK cited in a company's financial notes defines the exact measurement and disclosure obligations.",
        "goto_explanation": "GoTo prepares consolidated financial statements in full compliance with Indonesian SAK. Following the 2024 IFRS convergence updates, GoTo adopted updated standards for revenue recognition (PSAK 72), financial instruments (PSAK 71), and leases (PSAK 73).",
        "goto_report": {
            "title": "Regulatory Convergence: GoTo's Compliance with Indonesian SAK",
            "badge": "Regulatory Framework",
            "content_type": "text_cards",
            "description": "GoTo operates under the strict regulatory oversight of OJK and IDX, applying Indonesian Financial Accounting Standards (PSAK) audited by Kantor Akuntan Publik (KAP) Purwantono, Sungkoro & Surja (Ernst & Young Global).",
            "key_metrics": [
                {"label": "Independent Auditor", "val": "Ernst & Young (EY Indonesia / KAP PSS)"},
                {"label": "Audit Opinion", "val": "Unqualified Opinion with Emphasis of Matter (Going concern & restructurings)"},
                {"label": "Core Accounting Framework", "val": "Standar Akuntansi Keuangan di Indonesia (SAK)"},
                {"label": "Reporting Currency", "val": "Indonesian Rupiah (IDR), expressed in millions"}
            ]
        }
    },
    12: {
        "header": "QUICK REFERENCE",
        "subtitle": "PSAK to IFRS Numbering Map",
        "theory_explanation": "Standards Crosswalk: PSAK 16 (IAS 16 PP&E), PSAK 13 (IAS 40 Investment Property), PSAK 14 (IAS 2 Inventories), PSAK 71 (IFRS 9 Financial Instruments), PSAK 22 (IFRS 3 Business Combinations).",
        "goto_explanation": "Group 4 mapped GoTo's Note disclosures to the classroom PSAK reference chart, identifying how each key balance sheet and P&L item is governed.",
        "goto_report": {
            "title": "GoTo Statutory Disclosure Crosswalk: PSAK Standards in Action",
            "badge": "Standards Mapping",
            "content_type": "table",
            "table_headers": ["PSAK Standard", "IFRS Equivalent", "GoTo Financial Account", "GoTo Audited Note Reference", "2025 Balance (Rp bn)"],
            "table_rows": [
                ["PSAK 71", "IFRS 9", "Cash & Cash Equivalents", "LK Note 4 (Kas dan setara kas)", "21,755.2"],
                ["PSAK 15", "IAS 28", "Investment in Associates", "LK Note 10 (Investasi pada entitas asosiasi)", "10,344.6"],
                ["PSAK 19", "IAS 38", "Goodwill & Intangible Assets", "LK Note 12 (Goodwill dan aset takberwujud)", "4,528.9"],
                ["PSAK 71", "IFRS 9", "Bank Loans & Debt", "LK Note 17 (Pinjaman bank)", "7,742.6"],
                ["PSAK 16", "IAS 16", "Property, Plant & Equipment", "LK Note 11 (Aset tetap)", "622.1"],
                ["PSAK 71", "IFRS 9", "Fair Value Loss on Financial Instruments", "LK Note 27b (Beban keuangan & penyesuaian)", "(596.7)"]
            ],
            "analytical_note": "Forensic Crosswalk: PSAK 71 governs both GoTo's largest asset (Cash: Rp 21.8T) and its fastest growing liability (Debt: Rp 7.74T). PSAK 15 governs GoTo's primary strategic asset (Tokopedia: Rp 10.3T)."
        },
        "audit_evidence": {
            "img": "/evidence/GOTO_2025_PDF_p066.png",
            "title": "Audited Note 2 Standards Map (LK p. 66)",
            "caption": "Official GoTo LK Note 2: Citation of adopted PSAK standards governing financial reporting."
        }
    },
    13: {
        "header": "BACK TO OUR HOOK",
        "subtitle": "ABBA's Revaluation Surplus (Rp 55.08bn to Equity)",
        "theory_explanation": "Deconstructing the Classroom Hook: ABBA's Note 9 revealed a revaluation surplus of Rp 55.08 billion recognized directly in equity (OCI) — completely bypassing profit or loss. 'Surplus atas revaluasi aset tetap — neto.'",
        "goto_explanation": "Why couldn't GoTo use this accounting trick? Because GoTo has no real estate! In GoTo's Statement of Changes in Equity, there is NO revaluation surplus. Instead, GoTo's equity contracted by Rp 7.0 trillion, dragged down by an accumulated deficit of (Rp 214.1 trillion).",
        "goto_report": {
            "title": "Equity Contrast: ABBA Cosmetic Revaluation Surplus vs GoTo Retained Deficit",
            "badge": "Equity Architecture",
            "content_type": "table",
            "table_headers": ["Equity Component (Rp billion)", "ABBA (Classroom Hook)", "GoTo (Real Case)", "Economic Nature"],
            "table_rows": [
                ["Share Capital", "138.2", "1,184.4", "Par value of issued common equity"],
                ["Additional Paid-in Capital (Agio)", "24.6", "242,108.5", "Capital raised from public market investors"],
                ["Revaluation Surplus (PSAK 16)", "55.1", "0.0", "Cosmetic property mark-up bypassing P&L"],
                ["Accumulated Losses (Retained Deficit)", "(317.7)", "(214,118.8)", "Cumulative real economic capital burned"],
                ["Total Shareholders' Equity", "(99.8)", "28,711.7", "Ending net book equity of the enterprise"]
            ],
            "analytical_note": "Classroom Lesson Illustrated: ABBA used a Rp 55.1 bn revaluation surplus to make negative equity look less catastrophic (improving equity from -Rp 154.9 bn to -Rp 99.8 bn). GoTo has zero revaluation surplus; its equity is backed solely by paid-in capital (Agio Rp 242.1T) being destroyed by cumulative losses (Deficit Rp 214.1T)."
        },
        "audit_evidence": {
            "img": "/evidence/goto_equity_deficit_highlighted.png",
            "title": "Statement of Changes in Equity (LK p. 19)",
            "caption": "Official GoTo Equity Statement: Retained deficit of Rp (214,118,806) million with zero revaluation surplus."
        }
    },
    14: {
        "header": "PRECISION MATTERS",
        "subtitle": "Two Different 'Fair Value' Mechanisms: Equity (OCI) vs. P&L",
        "theory_explanation": "Critical Technical Distinction: PSAK 16 Revaluation Model sends revaluation surplus to Equity (OCI), bypassing P&L entirely. PSAK 13 / PSAK 71 Fair Value Model sends gains and losses directly through Profit or Loss. Both are called 'fair value,' but have opposite income statement effects.",
        "goto_explanation": "GoTo illustrates the severe P&L impact of PSAK 71: GoTo cannot hide fair value losses in equity. In FY2025, fair value declines of (Rp 596.7 bn) on financial instruments were charged directly against profit or loss, worsening statutory losses.",
        "goto_report": {
            "title": "GoTo Fair Value Mechanism Analysis: P&L Impact vs OCI",
            "badge": "Fair Value Mechanisms",
            "content_type": "table",
            "table_headers": ["Accounting Standard", "Fair Value Mechanism", "GoTo Account Applied", "FY2025 Income Statement Impact"],
            "table_rows": [
                ["PSAK 16 (PP&E Revaluation)", "Direct to Equity (OCI)", "None (GoTo uses Cost Model)", "Rp 0.0 (Bypasses P&L entirely)"],
                ["PSAK 13 (Investment Property)", "Through Profit or Loss", "None (GoTo owns no investment property)", "Rp 0.0"],
                ["PSAK 71 (Financial Instruments FVTPL)", "Through Profit or Loss", "Fintech startup equity & derivatives", "(Rp 596.7 billion) Fair value loss in P&L"],
                ["PSAK 15 (Associate Equity Share)", "Proportional Share of P&L", "Tokopedia & Bank Jago", "(Rp 588.4 billion) Associate loss in P&L"],
                ["PSAK 71 (OCI Debt Instruments)", "Through Other Comprehensive Income", "Foreign currency translation reserves", "(Rp 20.2 billion) in OCI"]
            ],
            "analytical_note": "Precision Takeaway: While ABBA exploited PSAK 16 to keep a Rp 55 bn gain out of P&L and boost equity, GoTo's fair value changes are governed by PSAK 71 and PSAK 15, which directly hit net income, adding Rp 1.18 trillion to GoTo's reported loss."
        },
        "audit_evidence": {
            "img": "/evidence/goto_income_statement_highlighted.png",
            "title": "Audited FY2025 Profit or Loss (LK p. 17)",
            "caption": "Official GoTo Income Statement: Rp (596,703) million fair value loss flowing through Profit or Loss."
        }
    },
    15: {
        "header": "A REAL CROSS-CHECK",
        "subtitle": "An Independent Anchor (KJPP FAST Rp 64.15bn Valuation)",
        "theory_explanation": "Independent Verification: ABBA relied on KJPP FAST (an OJK-registered public valuer) to appraise land and buildings at Rp 64.15bn using market, income, and cost approaches. Analysts must cross-check independent appraiser qualifications and valuation methodologies.",
        "goto_explanation": "GoTo required independent appraisals for its milestone transactions: 1) KJPP appraisal of Tokopedia prior to the ByteDance transaction, 2) Annual independent impairment testing of goodwill and software under PSAK 48 by registered valuation specialists.",
        "goto_report": {
            "title": "Independent Appraisals & Valuation Anchors in GoTo Corporate Actions",
            "badge": "Valuation Governance",
            "content_type": "text_cards",
            "description": "Like ABBA's reliance on KJPP FAST, GoTo depends on OJK-registered independent valuation firms (KJPP) to justify its multi-trillion balance sheet carrying values and fair value adjustments.",
            "key_metrics": [
                {"label": "Tokopedia Deconsolidation Valuation", "val": "Assessed at $1.5 billion total enterprise equity value"},
                {"label": "Independent Valuer", "val": "OJK-registered Kantor Jasa Penilai Publik (KJPP)"},
                {"label": "Methodologies Applied", "val": "Discounted Cash Flow (DCF), Guideline Public Company, Market Approach"},
                {"label": "Goodwill Impairment Anchor", "val": "Value-in-Use calculation with WACC discount rates between 13.5% and 16.2%"}
            ]
        }
    },
    16: {
        "header": "A QUESTION WORTH ASKING",
        "subtitle": "Why Revalue Upward in a Loss Year?",
        "theory_explanation": "Forensic Motivation Analysis: Three motives for upward revaluation during loss periods: 1) Genuine appreciation in property values, 2) Cosmetic improvement in balance sheet optics during capital deficiency, 3) Preparation for future debt or M&A transactions. Revaluation improves equity without fixing operating losses.",
        "goto_explanation": "GoTo faced the same temptation to improve optics: Unable to revalue real estate, management aggressively emphasized non-GAAP 'Adjusted EBITDA' (+Rp 374 bn) to present a turnaround narrative while statutory GAAP losses remained negative `(Rp 1.50 trillion)`.",
        "goto_report": {
            "title": "Cosmetic Financial Optics: Revaluations vs Non-GAAP Adjustments",
            "badge": "Forensic Skepticism",
            "content_type": "text_cards",
            "description": "When underlying core operations fail to produce positive economic profits, management frequently resorts to balance sheet revaluations (ABBA) or aggressive non-GAAP definitions (GoTo) to project solvency and progress.",
            "key_metrics": [
                {"label": "ABBA Cosmetic Tactic", "val": "Upward property revaluation (+Rp 55.1 bn) to cushion negative equity"},
                {"label": "GoTo Cosmetic Tactic", "val": "Adjusted EBITDA (+Rp 374 bn) stripping out D&A, stock comp, and losses"},
                {"label": "Statutory Reality (ABBA)", "val": "Operating loss persists at -(Rp 15.2 bn)"},
                {"label": "Statutory Reality (GoTo)", "val": "Operating loss persists at -(Rp 378.1 bn), Free Cash Flow negative -(Rp 875.3 bn)"}
            ]
        }
    },
    17: {
        "header": "THE COMPARABILITY PROBLEM",
        "subtitle": "Same Building, Two Bases (PT A Cost Model Rp 35bn vs PT B Fair Value Rp 82bn)",
        "theory_explanation": "The Comparability Dilemma: PT A and PT B each bought identical office buildings in 2015 for Rp 50bn. PT A uses Cost Model (carried at Rp 35bn net of depreciation). PT B uses Fair Value Model (carried at Rp 82bn). Comparing ROA or leverage unadjusted compares accounting choice, not business performance.",
        "goto_explanation": "The Comparability Problem in Tech: Comparing GoTo with Grab Holdings (NASDAQ: GRAB) and Sea Ltd (NYSE: SE). GoTo capitalizes substantial software development (Rp 3.91T), while US tech peers expense tech costs immediately under US GAAP, creating artificial ROA and asset base differences.",
        "goto_report": {
            "title": "Peer Comparability: GoTo (PSAK) vs Grab (US GAAP) vs Sea Ltd",
            "badge": "Cross-Border Comparability",
            "content_type": "table",
            "table_headers": ["Comparability Dimension", "GoTo (IDX: GOTO)", "Grab Holdings (NASDAQ: GRAB)", "Accounting Impact on Comparison"],
            "table_rows": [
                ["Accounting Framework", "Indonesian SAK (IFRS Converged)", "US GAAP", "Different standards govern capitalization and lease debt"],
                ["Software Development Costs", "Capitalizes technology R&D (Rp 3.9T)", "Expenses R&D as incurred", "GoTo assets look higher; Grab expenses hit P&L faster"],
                ["Property & Delivery Fleet", "Asset-light (Drivers own bikes)", "Asset-light (Drivers own bikes)", "Both avoid PP&E heavy balance sheets"],
                ["E-Commerce Presence", "24.99% Associate (Tokopedia)", "No native marketplace", "GoTo accounts under equity method (PSAK 15)"],
                ["Headline Metric Promoted", "Adjusted EBITDA (Non-GAAP)", "Adjusted EBITDA (Non-GAAP)", "Both define adjustments differently to show positive optics"]
            ],
            "analytical_note": "Comparability Rule: You cannot compare GoTo's return on assets (ROA) or book equity directly to Grab or Sea Ltd without adjusting for software capitalization and equity-method associate accounting."
        }
    },
    18: {
        "header": "THE PRACTICAL SKILL",
        "subtitle": "What Analysts Should Actually Do",
        "theory_explanation": "The 4-Step Practical Skill: 1) Identify the specific measurement basis and PSAK standard for each major asset class. 2) Check the fair value hierarchy (Level 1, 2, 3 unobservable inputs). 3) Adjust companies onto a common accounting basis. 4) Investigate the timing of revaluations relative to covenant tests or loss years.",
        "goto_explanation": "Applied to GoTo: Group 4 executed this forensic playbook: 1) Audited Note 2 policies, 2) Isolated Level 3 fair value inputs in derivatives and warrants, 3) Standardized EBITDA to strip out non-operating distortions, 4) Scrutinized loan covenants on the Rp 7.74T debt.",
        "goto_report": {
            "title": "Group 4's Forensic Valuation Checklist Applied to GoTo",
            "badge": "Forensic Playbook",
            "content_type": "text_cards",
            "description": "Group 4's rigorous four-step forensic protocol applied to PT GoTo Gojek Tokopedia Tbk's audited financial disclosures.",
            "key_metrics": [
                {"label": "Step 1: Measurement Mapping", "val": "Verified PSAK 16 cost model for PP&E and PSAK 15 for Tokopedia"},
                {"label": "Step 2: Fair Value Hierarchy", "val": "Identified Level 3 DCF assumptions on unlisted fintech investments"},
                {"label": "Step 3: Peer Standardization", "val": "Adjusted GoTo software amortization to mirror US GAAP expensing"},
                {"label": "Step 4: Timing Scrutiny", "val": "Correlated debt surge (+102.7%) with cash liquidity preservation"}
            ]
        }
    },
    19: {
        "header": "KEY TAKEAWAYS",
        "subtitle": "What to Remember from Week 3",
        "theory_explanation": "Core Principles: 1) Recognition and measurement are distinct questions. 2) Every balance sheet change has an income statement counterpart. 3) Historical cost trades relevance for reliability; fair value trades reliability for relevance. 4) The same term ('fair value') has opposite P&L consequences depending on the standard. 5) Comparability must be adjusted for, never assumed.",
        "goto_explanation": "Final Week 3 Synthesis for GoTo: GoTo's reported figures can only be understood through this measurement lens. Its narrowing loss masks balance sheet contraction, fair value drains, and reliance on bank debt. Analysts who rely on surface metrics miss the multi-trillion capital destruction.",
        "goto_report": {
            "title": "Week 3 Synthesis: Valuation Reality vs Reporting Optics in GoTo",
            "badge": "Classroom Synthesis",
            "content_type": "text_cards",
            "description": "Week 3 equips the financial analyst to see past headline numbers. In GoTo, understanding asset valuation proves that narrowing losses are not synonymous with value creation.",
            "key_metrics": [
                {"label": "Measurement Verdict", "val": "GoTo's assets are dominated by financial and associate stakes, not physical capital"},
                {"label": "Income Linkage Verdict", "val": "Balance sheet write-downs (goodwill & fair value) generated over Rp 80T in historical losses"},
                {"label": "Equity Architecture Verdict", "val": "Retained deficit of Rp 214.1T cannot be masked by cosmetic revaluations"},
                {"label": "Final Analyst Stance", "val": "Maintain SELL / AVOID based on persistent economic cash drain"}
            ]
        }
    }
}

# Update week 3 slides in full_slides_knowledgebase.json
w3["slides"] = []
for slide_num in range(1, 20):
    info = w3_data.get(slide_num, {})
    slide_obj = {
        "slide_num": slide_num,
        "header": info.get("header", f"Slide {slide_num}"),
        "subtitle": info.get("subtitle", ""),
        "raw_text": f"{info.get('header', '')}\n{info.get('subtitle', '')}\nWeek 3 Asset & Liability Valuation",
        "theory_explanation": info.get("theory_explanation", ""),
        "goto_explanation": info.get("goto_explanation", ""),
        "image_url": f"/slides/FSA_Week3_PPT/slide_{slide_num}.png",
        "goto_report": info.get("goto_report", {}),
    }
    if "audit_evidence" in info:
        slide_obj["audit_evidence"] = info["audit_evidence"]
    w3["slides"].append(slide_obj)

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json", "w") as f:
    json.dump(modules, f, indent=2)

print(f"Successfully populated all {len(w3['slides'])} slides for Week 3!")
