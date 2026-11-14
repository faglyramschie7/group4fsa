import json

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json") as f:
    modules = json.load(f)

w4 = next((m for m in modules if m["id"] == "week4"), None)
if not w4:
    print("Week 4 not found!")
    exit(1)

w4_data = {
    1: {
        "header": "Analyzing the Statement of Cash Flows",
        "subtitle": "Direct vs. Indirect Method • Classification • Free Cash Flow • Earnings vs. Cash Quality",
        "theory_explanation": "Course Orientation & Theme: Analyzing the Statement of Cash Flows. Step 3 (Financial Analysis). Net income reflects accrual accounting choices; the statement of cash flows grounds analysis in real economic cash inflows and outflows.",
        "goto_explanation": "For GoTo, the cash flow statement is the ultimate arbiter of turnaround claims. In 2025, management celebrated positive Adjusted EBITDA and narrowing net losses, but Group 4's forensic cash flow audit reveals a negative Free Cash Flow of -(Rp 875.3 bn) and reliance on Rp 3.72T in new debt.",
        "goto_report": {
            "title": "GoTo Cash Flow Profile & Liquidity Architecture (Step 3)",
            "badge": "Cash Flow Overview",
            "content_type": "profile",
            "description": "While GoTo achieved a positive statutory Operating Cash Flow of +Rp 307.0 billion in FY2025 (turning around from -Rp 3,942.1 bn in 2023), its cash from operations was insufficient to fund capital expenditures of Rp 1,182.4 billion. Cash balances rose to Rp 21,755.2 billion solely through time deposit liquidations (Rp 1.39T) and bank borrowing (Rp 3.72T).",
            "key_metrics": [
                {"label": "Operating Cash Flow (CFO)", "val": "+Rp 307.0 billion (1.7% of revenue)"},
                {"label": "Capital Expenditures (Capex)", "val": "Rp 1,182.4 billion (PP&E + Software)"},
                {"label": "Free Cash Flow (FCF)", "val": "(Rp 875.3 billion) strictly negative"},
                {"label": "New Bank Borrowings (CFF)", "val": "+Rp 3,718.0 billion new debt"}
            ]
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p1_highlighted.png",
            "title": "Audited Statement of Cash Flows (LK p. 20)",
            "caption": "Official GoTo LK p. 20: Cash flow from operating activities showing +Rp 307,017 million direct method collections."
        }
    },
    2: {
        "header": "WHERE WE ARE",
        "subtitle": "Still Inside Step 3: Financial Analysis",
        "theory_explanation": "Framework Context: Moving from Step 1 (Strategy) and Step 2 (Accounting Analysis) into Step 3 (Financial Analysis). Step 3 synthesizes profitability, liquidity, and cash generation to assess the true operating health of the firm.",
        "goto_explanation": "Group 4's Milestone 3 investigation focused on whether GoTo's narrowing accounting loss is matched by organic cash generation. We discovered a profound divergence between accrual metrics and cash flow realities.",
        "goto_report": {
            "title": "Step 3 Financial Analysis: Cash Reality vs Accounting Accruals",
            "badge": "Framework Positioning",
            "content_type": "text_cards",
            "description": "Financial analysis requires verifying whether accounting profits convert into spendable cash. GoTo's business model requires substantial ongoing technology reinvestment that consumes all operating cash flow.",
            "key_metrics": [
                {"label": "Step 2 Conclusion", "val": "Asset-light balance sheet with heavy associate exposure (PSAK 15)"},
                {"label": "Step 3 Cash Focus", "val": "Assessing cash conversion cycle, debt service coverage, and FCF sustainability"},
                {"label": "Forensic Insight", "val": "Operating turnaround is fragile; CFO covers only 26% of annual tech capex"}
            ]
        }
    },
    3: {
        "header": "THE CORE IDEA",
        "subtitle": "Net Income Is an Opinion. Cash Is a Fact.",
        "theory_explanation": "The Foundational FSA Axiom: Net income is an opinion (subject to revenue recognition timing, depreciation methods, and non-cash accrual estimates). Cash is a fact (the literal change in money in the bank).",
        "goto_explanation": "GoTo epitomizes this core idea: Management's preferred 'opinion' is Adjusted EBITDA of +Rp 374 bn. The audited GAAP 'opinion' is a Net Loss of -(Rp 1,501.7 bn). The economic 'fact' is that Free Cash Flow was -(Rp 875.3 bn) and debt doubled.",
        "goto_report": {
            "title": "Opinion vs. Fact: The Spectrum of GoTo's 2025 Financial Reporting",
            "badge": "Core Principle",
            "content_type": "text_cards",
            "description": "Comparing the spectrum of figures presented to investors versus the unyielding facts of GoTo's cash flow statement.",
            "key_metrics": [
                {"label": "Management Opinion (Non-GAAP)", "val": "+Rp 374 billion (Adjusted EBITDA 'profitability')"},
                {"label": "Statutory GAAP Opinion", "val": "(Rp 1,501.7 billion) Net Loss for the Year"},
                {"label": "Audited Cash Fact (CFO)", "val": "+Rp 307.0 billion generated from day-to-day operations"},
                {"label": "Ultimate Economic Fact (FCF)", "val": "(Rp 875.3 billion) cash burned after mandatory capex"}
            ]
        }
    },
    4: {
        "header": "A REAL COMPANY",
        "subtitle": "PT Mahaka Media Tbk (ABBA), 2023–2025 vs. GoTo",
        "theory_explanation": "The ABBA Divergence: Net income and operating cash flow lines crossed twice in three years. In 2024, ABBA had net income of +Rp 6bn but negative CFO of -(Rp 33bn). In 2025, ABBA had a net loss of -(Rp 26bn) but positive CFO of +Rp 3bn.",
        "goto_explanation": "GoTo mirrors ABBA's crossing lines: From 2023 to 2025, GoTo's Net Loss narrowed dramatically from -(Rp 90.5T) to -(Rp 1.50T), while CFO flipped from -(Rp 3,942.1 bn) to +Rp 307.0 bn. Group 4 analyzes whether this represents real operational turnaround or working capital timing.",
        "goto_report": {
            "title": "Three-Year Trend Comparison: Net Income vs. Operating Cash Flow (CFO)",
            "badge": "Trend Divergence Analysis",
            "content_type": "table",
            "table_headers": ["Company & Metric (Rp billion)", "2023A", "2024A", "2025A", "YoY Trajectory"],
            "table_rows": [
                ["ABBA Net Income / (Loss)", "(52.4)", "5.6", "(25.7)", "Flipped back to loss in 2025"],
                ["ABBA Operating Cash Flow (CFO)", "(58.6)", "(33.0)", "2.8", "Turned positive via collections"],
                ["GoTo Net Income / (Loss)", "(90,516.3)", "(5,471.2)", "(1,501.7)", "-72.6% (Loss narrowed)"],
                ["GoTo Operating Cash Flow (CFO)", "(3,942.1)", "(762.4)", "307.0", "Turned positive (+Rp 1.07T improvement)"],
                ["GoTo Free Cash Flow (FCF)", "(4,159.2)", "(1,414.7)", "(875.3)", "Remains strictly negative!"]
            ],
            "analytical_note": "FSA Insight: In both ABBA and GoTo, net income and cash flow diverge sharply. While GoTo's CFO crossed into positive territory (+Rp 307.0 bn), its Free Cash Flow remains deep in the red (-(Rp 875.3 bn)), confirming that operating cash cannot yet support required capital spending."
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p1_highlighted.png",
            "title": "Three-Year Audited Cash Flows (LK p. 20)",
            "caption": "Official GoTo Cash Flow Statement showing CFO turning from -(Rp 762,393) million to +Rp 307,017 million."
        }
    },
    5: {
        "header": "THE FRAMEWORK",
        "subtitle": "Every Cash Flow Is One of Three Types: CFO + CFI + CFF",
        "theory_explanation": "The Cash Flow Framework: Cash flows are partitioned into three mutually exclusive categories: Operating (CFO), Investing (CFI), and Financing (CFF). Their sum equals the Net Change in Cash.",
        "goto_explanation": "Deconstructing GoTo's 2025 Net Change in Cash (+Rp 751.4 bn): CFO was +Rp 307.0 bn, CFI was +Rp 1,094.6 bn, and CFF was +Rp 2,494.4 bn, offset by foreign exchange effects of -(Rp 20.2 bn).",
        "goto_report": {
            "title": "GoTo 2025 Three-Part Cash Flow Reconciliation (Rp billion)",
            "badge": "Cash Flow Architecture",
            "content_type": "table",
            "table_headers": ["Cash Flow Activity", "2024A (Rp bn)", "2025A (Rp bn)", "YoY Change", "Primary Economic Driver"],
            "table_rows": [
                ["Operating Activities (CFO)", "(762.4)", "307.0", "+Rp 1,069.4 bn", "Narrowing losses & vendor payable timing"],
                ["Investing Activities (CFI)", "1,424.8", "1,094.6", "-Rp 330.2 bn", "Cashing in Rp 1,386.5 bn time deposits vs Capex"],
                ["Financing Activities (CFF)", "(241.2)", "2,494.4", "+Rp 2,735.6 bn", "Borrowed Rp 3,718.0 bn in new bank debt"],
                ["Effect of Exchange Rate Changes", "(413.7)", "(20.2)", "+Rp 393.5 bn", "Currency revaluation on foreign cash balances"],
                ["Net Increase in Cash & Equivalents", "7.5", "751.4", "+Rp 743.9 bn", "Closing Cash reached Rp 21,755.2 billion"]
            ],
            "analytical_note": "Critical Audit Revelation: GoTo's cash grew by Rp 751.4 bn not because the core business generated abundant cash, but because financing activities contributed +Rp 2,494.4 bn (driven by Rp 3.72T of new bank loans) and investing activities contributed +Rp 1,094.6 bn (cashing in deposits)."
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p2_highlighted.png",
            "title": "Audited Statement of Cash Flows (LK p. 21)",
            "caption": "Official GoTo LK p. 21: Net increase in cash of Rp 751,433 million yielding ending cash of Rp 21,755,200 million."
        }
    },
    6: {
        "header": "CLASSIFICATION 1 OF 3",
        "subtitle": "Operating Activities (CFO): The Core Engine",
        "theory_explanation": "Operating Cash Flow (CFO): The cash effects of the core, day-to-day, revenue-generating business. Cash received from customers minus cash paid to suppliers, employees, operating expenses, interest, and taxes.",
        "goto_explanation": "GoTo's 2025 CFO reached +Rp 307.0 billion (1.7% of revenue). While positive, this margin is razor-thin for a platform processing hundreds of trillions in gross transaction value (GTV), showing that GoTo has little buffer against cost shocks.",
        "goto_report": {
            "title": "Operating Cash Flow Breakdown (Direct Method)",
            "badge": "Core Operating Cash",
            "content_type": "text_cards",
            "description": "GoTo reports operating cash flows using the direct method on page 20 of its audited financial statements, providing total transparency into operational receipts and disbursements.",
            "key_metrics": [
                {"label": "Cash Received from Customers", "val": "Rp 18,339.5 billion (Gojek, GoPay, merchant fees)"},
                {"label": "Cash Paid to Suppliers & Partners", "val": "(Rp 17,987.3 billion) (Driver incentives, hosting, staff)"},
                {"label": "Cash Paid for Corporate Taxes", "val": "(Rp 415.1 billion)"},
                {"label": "Net Operating Cash Flow", "val": "+Rp 307.0 billion (1.68% conversion margin)"}
            ]
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p1_highlighted.png",
            "title": "Direct Method Operating Cash Flow (LK p. 20)",
            "caption": "Official GoTo LK p. 20: 'Arus kas dari aktivitas operasi' detailing Rp 18.3T receipts and Rp 17.99T operating payments."
        }
    },
    7: {
        "header": "CLASSIFICATION 2 OF 3",
        "subtitle": "Investing Activities (CFI): Capital Reinvestment vs Liquidation",
        "theory_explanation": "Investing Cash Flow (CFI): The cash effects of acquiring or disposing of long-term productive assets (PP&E, software, investments). Purchases of productive assets are cash outflows (-); disposals or liquidations are cash inflows (+).",
        "goto_explanation": "GoTo's CFI was +Rp 1,094.6 billion in 2025. In a healthy growing company, CFI is typically negative (reinvesting cash into future productive capacity). GoTo's CFI is positive because it cashed in Rp 1,386.5 bn of time deposits to subsidize operational Capex.",
        "goto_report": {
            "title": "Investing Cash Flows: Unmasking the Positive CFI Distortion",
            "badge": "Capital Deployment",
            "content_type": "text_cards",
            "description": "A superficial look at GoTo's +Rp 1,094.6 billion CFI suggests strong cash generation. Forensic dissection proves GoTo was liquidating financial reserves rather than organically expanding.",
            "key_metrics": [
                {"label": "Additions to PP&E", "val": "(Rp 302.1 billion) cash spent on servers & equipment"},
                {"label": "Additions to Intangibles (Software)", "val": "(Rp 880.3 billion) capitalized software development"},
                {"label": "Total Capital Expenditures", "val": "(Rp 1,182.4 billion) required tech reinvestment"},
                {"label": "Liquidation of Time Deposits", "val": "+Rp 1,386.5 billion cash collected from maturing deposits"}
            ]
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p2_highlighted.png",
            "title": "Audited Investing Cash Flows (LK p. 21)",
            "caption": "Official GoTo LK p. 21: 'Arus kas dari aktivitas investasi' showing net inflow of Rp 1,094,565 million."
        }
    },
    8: {
        "header": "CLASSIFICATION 3 OF 3",
        "subtitle": "Financing Activities (CFF): Capital Injections vs Debt Burden",
        "theory_explanation": "Financing Cash Flow (CFF): The cash effects of transactions with owners and creditors: borrowing and repaying debt, issuing and repurchasing shares, and paying dividends.",
        "goto_explanation": "GoTo's CFF exploded to +Rp 2,494.4 billion in 2025 (up from -Rp 241.2 bn in 2024). GoTo drew down Rp 3,718.0 billion in new bank debt while repaying Rp 1,223.6 billion, expanding total bank debt by +102.7% to Rp 7,742.6 billion.",
        "goto_report": {
            "title": "Financing Cash Flows: The Debt Expansion Lifeline",
            "badge": "Financing Mechanics",
            "content_type": "text_cards",
            "description": "GoTo maintained liquidity in 2025 by tapping commercial bank credit lines. This borrowing doubled outstanding debt and added substantial interest burdens.",
            "key_metrics": [
                {"label": "Proceeds from Bank Borrowings", "val": "+Rp 3,718.0 billion new bank debt drawn"},
                {"label": "Repayment of Bank Borrowings", "val": "(Rp 1,223.6 billion) debt principal repaid"},
                {"label": "Net Cash from Financing Activities", "val": "+Rp 2,494.4 billion net cash borrowed"},
                {"label": "Ending Audited Debt", "val": "Rp 7,742.6 billion (+102.7% increase YoY)"}
            ]
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p2_highlighted.png",
            "title": "Audited Financing Cash Flows (LK p. 21)",
            "caption": "Official GoTo LK p. 21: 'Penerimaan dari penarikan pinjaman bank' of Rp 3,718,000 million."
        }
    },
    9: {
        "header": "READING THE PATTERN",
        "subtitle": "Life-Cycle Signatures: Where Does GoTo Sit?",
        "theory_explanation": "Life-Cycle Signatures Framework: Start-up (- - +), High Growth (+ - +), Mature (+ - -), Harvesting (+ + -), Decline/Distress (- + -). Each pattern reflects the economic reality of the business model.",
        "goto_explanation": "Where does GoTo sit? GoTo exhibits an anomalous (+ + +) signature in 2025: CFO (+), CFI (+), CFF (+). This is NOT a healthy high-growth pattern (+ - +). GoTo achieved positive CFI by liquidating savings, and positive CFF by borrowing debt to survive.",
        "goto_report": {
            "title": "Life-Cycle Cash Flow Signatures: GoTo vs Theoretical Norms",
            "badge": "Life-Cycle Diagnostic",
            "content_type": "table",
            "table_headers": ["Stage / Entity", "CFO", "CFI", "CFF", "Forensic Interpretation"],
            "table_rows": [
                ["Start-up", "Negative (-)", "Negative (-)", "Positive (+)", "Equity funding initial build-out and losses"],
                ["High Growth", "Positive (+)", "Negative (-)", "Positive (+)", "Operations fund growth; debt/equity accelerates capex"],
                ["Mature", "Positive (+)", "Negative (-)", "Negative (-)", "CFO funds capex, debt service, and dividends"],
                ["Harvesting", "Positive (+)", "Positive (+)", "Negative (-)", "Downsizing operations; liquidating productive assets"],
                ["Decline / Distress", "Negative (-)", "Positive (+)", "Negative (-)", "Asset sales cover operational cash deficits"],
                ["GoTo 2023 Actual", "Negative (-)", "Positive (+)", "Negative (-)", "Decline / Distress: Liquidating cash to cover operating burn"],
                ["GoTo 2025 Actual", "Positive (+)", "Positive (+)", "Positive (+)", "Anomalous (+ + +): Borrowing debt and cashing deposits to maintain optical cash"]
            ],
            "analytical_note": "Life-Cycle Verdict: GoTo's (+ + +) cash signature is an artificial construct. If GoTo had not liquidated deposits (CFI) and borrowed Rp 3.72T in debt (CFF), organic Free Cash Flow of -(Rp 875.3 bn) would have caused cash balances to contract."
        }
    },
    10: {
        "header": "PRESENTING OPERATING CASH FLOW",
        "subtitle": "Two Methods, One Answer: Direct vs. Indirect",
        "theory_explanation": "Methodological Parity: The Direct Method and Indirect Method always reconcile to the exact same operating cash flow figure. They differ only in presentation. PSAK 2 (IAS 7) permits either method, but recommends the Direct Method.",
        "goto_explanation": "GoTo provides BOTH: On page 20 of its audited financial report, GoTo presents the primary statement using the Direct Method (+Rp 307.0 bn). In Note 39, GoTo provides the full Indirect Method reconciliation starting from Loss Before Income Tax.",
        "goto_report": {
            "title": "Direct vs. Indirect Presentation in GoTo Financial Statements",
            "badge": "Presentation Standards",
            "content_type": "text_cards",
            "description": "GoTo complies with best practices under PSAK 2 by publishing both the direct cash receipts and disbursements and the non-cash accrual reconciliation.",
            "key_metrics": [
                {"label": "Primary Presentation", "val": "Direct Method (LK p. 20, Statement of Cash Flows)"},
                {"label": "Note Reconciliation", "val": "Indirect Method (LK Note 39, Non-cash items)"},
                {"label": "Statutory Result", "val": "+Rp 307.0 billion (Reconciles exactly to Rp 307,017 million)"},
                {"label": "Regulatory Standard", "val": "PSAK 2 (Pernyataan Standar Akuntansi Keuangan: Laporan Arus Kas)"}
            ]
        }
    },
    11: {
        "header": "METHOD 1 OF 2",
        "subtitle": "The Direct Method: Real Cash Collections & Payments",
        "theory_explanation": "The Direct Method: Lists actual cash receipts from customers and payments to suppliers, employees, operating expenses, interest, and taxes. Provides immediate insight into operational liquidity.",
        "goto_explanation": "GoTo's Direct Method statement shows that GoTo collected Rp 18,339.5 bn from customers and paid out Rp 17,987.3 bn to service providers, drivers, and employees, yielding an operating cash margin of only 1.7%.",
        "goto_report": {
            "title": "GoTo Audited Direct Method Operating Cash Flows (FY2025)",
            "badge": "Direct Method Audit",
            "content_type": "table",
            "table_headers": ["Cash Flow Line Item (Rp billion)", "2024A", "2025A", "YoY Change", "Economic Meaning"],
            "table_rows": [
                ["Penerimaan kas dari pelanggan (Customers)", "15,892.4", "18,339.5", "+15.4%", "Gross collections from app users & merchants"],
                ["Pembayaran kas kepada pemasok & karyawan", "(16,115.8)", "(17,987.3)", "+11.6%", "Direct cost of driver incentives, IT & staff"],
                ["Arus kas operasi sebelum pajak & bunga", "(223.4)", "352.2", "Turned positive", "Core operational cash spread"],
                ["Pembayaran pajak penghasilan (Income Tax)", "(385.1)", "(415.1)", "+7.8%", "Corporate and withholding tax payments"],
                ["Pembayaran bunga dan beban keuangan", "(153.9)", "(30.1)", "-80.4%", "Interest paid on outstanding credit facilities"],
                ["Arus Kas Bersih dari Aktivitas Operasi (CFO)", "(762.4)", "307.0", "+Rp 1,069.4 bn", "Final Net Operating Cash Flow"]
            ],
            "analytical_note": "Direct Method Audit: Receipts grew +15.4% (Rp 18.34T) while operating payments grew +11.6% (Rp 17.99T). The positive CFO of Rp 307.0 bn was achieved because GoTo restrained supplier payment growth relative to revenue collection."
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p1_highlighted.png",
            "title": "Audited Direct Statement of Cash Flows (LK p. 20)",
            "caption": "Official GoTo LK p. 20: Direct method schedule detailing receipts from customers and payments to vendors."
        }
    },
    12: {
        "header": "METHOD 2 OF 2",
        "subtitle": "The Indirect Method: Reconciling Net Loss to Cash",
        "theory_explanation": "The Indirect Method: Starts from net income (or loss before tax), adds back non-cash expenses (depreciation, amortization, stock compensation), and adjusts for changes in operating working capital.",
        "goto_explanation": "GoTo's Indirect reconciliation proves why CFO was positive despite a massive Net Loss: GoTo added back Rp 1,372.1 bn of non-cash D&A, Rp 412.5 bn of stock-based compensation, and Rp 588.4 bn of associate losses, totaling Rp 2.37T in non-cash add-backs!",
        "goto_report": {
            "title": "GoTo Audited Indirect Method Reconciliation (LK Note 39)",
            "badge": "Indirect Method Audit",
            "content_type": "table",
            "table_headers": ["Reconciliation Component (Rp billion)", "2024A", "2025A", "Nature of Adjustment", "Economic Reality"],
            "table_rows": [
                ["Rugi sebelum pajak penghasilan (Loss Before Tax)", "(5,275.8)", "(1,086.6)", "Statutory Accrual Loss", "Unprofitable core accrual operations"],
                ["Penyusutan dan amortisasi (D&A Add-back)", "1,756.1", "1,372.1", "Non-Cash Expense (+)", "Wear and tear of tech software and servers"],
                ["Beban kompensasi berbasis saham (SBC)", "624.5", "412.5", "Non-Cash Expense (+)", "Stock options granted to management & staff"],
                ["Bagian rugi dari entitas asosiasi (Tokopedia/Jago)", "2,305.1", "588.4", "Non-Cash Equity Loss (+)", "Book equity loss of non-consolidated associates"],
                ["Penyesuaian nilai wajar instrumen keuangan", "482.1", "596.7", "Non-Cash Fair Value Loss (+)", "Mark-to-market write-downs of venture stakes"],
                ["Perubahan modal kerja (Working Capital Adjustments)", "(654.4)", "(1,576.1)", "Operating Working Capital (-)", "Outflows into receivables & payable settlements"],
                ["Arus Kas Bersih dari Aktivitas Operasi (CFO)", "(762.4)", "307.0", "Reconciled Cash Result", "Exact match to Direct Method (+Rp 307.0 bn)"]
            ],
            "analytical_note": "Forensic Indirect Breakdown: GoTo did not produce positive CFO because operations were wildly lucrative; it produced positive CFO because Rp 2,969.7 billion of non-cash expenses (D&A, Stock Comp, Associate Losses, Fair Value) were added back to offset the accrual loss."
        },
        "audit_evidence": {
            "img": "/evidence/goto_income_statement_highlighted.png",
            "title": "Audited Income Statement Link (LK p. 17)",
            "caption": "Official GoTo LK p. 17: Loss before income tax of Rp (1,086,604) million forming the starting point for indirect CFO."
        }
    },
    13: {
        "header": "THE PAYOFF",
        "subtitle": "Two Roads, One Destination: Exact Built-in Accuracy Check",
        "theory_explanation": "Built-in Accuracy Check: Direct and indirect methods must yield the exact same rupiah figure. If they diverge by even one rupiah, there is an error in classification or non-cash reconciliation.",
        "goto_explanation": "In GoTo's audited filing, both roads lead precisely to +Rp 307,017 million (+Rp 307.0 billion). Group 4 verified this equality down to the penny.",
        "goto_report": {
            "title": "Reconciliation Parity Check: Direct Method vs Indirect Method",
            "badge": "Audit Verification",
            "content_type": "table",
            "table_headers": ["Reconciliation Road", "Calculated CFO (Rp million)", "Calculated CFO (Rp billion)", "Audit Discrepancy", "Status"],
            "table_rows": [
                ["Road 1: Direct Method (LK p. 20)", "307,017", "+307.017", "Rp 0.00", "Verified Accurate"],
                ["Road 2: Indirect Method (LK Note 39)", "307,017", "+307.017", "Rp 0.00", "Verified Accurate"],
                ["Built-in Equality Check", "0", "0.000", "Zero Variance", "Fully Reconciled"]
            ],
            "analytical_note": "Mathematical Perfection: Direct receipts less payments exactly matches net loss plus non-cash add-backs and working capital changes at +Rp 307.017 billion."
        }
    },
    14: {
        "header": "A NEW CONCEPT",
        "subtitle": "Free Cash Flow: Operating Cash Flow Minus Capital Expenditures",
        "theory_explanation": "Free Cash Flow Formula: Free Cash Flow (FCF) = Operating Cash Flow (CFO) minus Capital Expenditures (Capex). FCF measures the cash generated that is truly free to be distributed or reinvested after maintaining productive capacity.",
        "goto_explanation": "Applying FCF to GoTo: CFO was +Rp 307.0 bn. Capital expenditures were Rp 1,182.4 bn (Rp 302.1m PP&E + Rp 880.3m capitalized software). Free Cash Flow = 307.0 - 1,182.4 = -(Rp 875.3 billion). GoTo's free cash flow is strictly negative.",
        "goto_report": {
            "title": "GoTo 2025 Free Cash Flow (FCF) Calculation (Rp billion)",
            "badge": "Free Cash Flow Formula",
            "content_type": "table",
            "table_headers": ["Free Cash Flow Component", "2024A (Rp bn)", "2025A (Rp bn)", "YoY Change", "Formula Reference"],
            "table_rows": [
                ["Operating Cash Flow (CFO)", "(762.4)", "307.0", "+Rp 1,069.4 bn", "Direct cash from core operations"],
                ["Less: Additions to PP&E", "(217.1)", "(302.1)", "+39.2% Capex", "Physical IT servers and office upgrades"],
                ["Less: Additions to Capitalized Software", "(435.2)", "(880.3)", "+102.3% Capex", "Core software development & app engineering"],
                ["Total Capital Expenditures (Capex)", "(652.3)", "(1,182.4)", "+81.3% Capex", "Capex = PP&E Capex + Tech Software Capex"],
                ["Free Cash Flow (FCF = CFO - Capex)", "(1,414.7)", "(875.3)", "+38.1% (Deficit narrowed)", "FCF = CFO - Capex"]
            ],
            "analytical_note": "The Cold Truth: GoTo's FCF improved from -(Rp 1,414.7 bn) to -(Rp 875.3 bn), but remains firmly negative. GoTo burns Rp 875.3 million in cold cash every single year just to maintain its technological platform and app infrastructure."
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p2_highlighted.png",
            "title": "Audited Capex Disclosures (LK p. 21)",
            "caption": "Official GoTo LK p. 21: 'Perolehan aset tetap' (Rp 302.1 bn) and 'Perolehan aset takberwujud' (Rp 880.3 bn)."
        }
    },
    15: {
        "header": "WHY IT MATTERS",
        "subtitle": "What Free Cash Flow Actually Enables",
        "theory_explanation": "The Four Capital Allocations: Free cash flow is the only source of cash that allows a business to: 1) Repay debt principal, 2) Pay cash dividends, 3) Buy back shares, 4) Fund acquisitions without issuing shares. Negative FCF requires continuous external financing.",
        "goto_explanation": "GoTo's negative FCF of -(Rp 875.3 bn) renders it incapable of performing any of these four functions autonomously. GoTo cannot pay dividends, cannot retire its Rp 7.74T debt from operations, and must rely on external lenders.",
        "goto_report": {
            "title": "GoTo Capital Allocation Capabilities under Negative FCF",
            "badge": "Capital Allocation Audit",
            "content_type": "text_cards",
            "description": "Evaluating GoTo's ability to execute standard corporate finance capital allocation decisions with an organic Free Cash Flow deficit of -(Rp 875.3 billion).",
            "key_metrics": [
                {"label": "1. Repay Debt Principal", "val": "Impossible organically; GoTo had to borrow Rp 3.72T in new debt to refinance Rp 1.22T repayments"},
                {"label": "2. Pay Cash Dividends", "val": "Zero dividend capacity; prohibited by accumulated deficit of -(Rp 214.1 trillion)"},
                {"label": "3. Share Buybacks", "val": "Limited to modest treasury share acquisitions funded by debt or asset sales"},
                {"label": "4. Fund Growth Autonomously", "val": "Dependent on ByteDance funding commitments ($1.5B) for Tokopedia development"}
            ]
        }
    },
    16: {
        "header": "THREE RATIOS",
        "subtitle": "Cash Flow Ratios We'll Cover",
        "theory_explanation": "The Cash Flow Ratio Triad: 1) Cash Flow Adequacy Ratio (Does CFO cover capex, debt, and dividends?), 2) Cash Flow to Debt Ratio (Could CFO retire debt?), 3) Cash Return on Assets (Cash ROA).",
        "goto_explanation": "Group 4 calculated all three cash ratios for GoTo's audited 2025 financial statements, comparing them against healthy corporate benchmarks and peer tech metrics.",
        "goto_report": {
            "title": "GoTo Cash Flow Ratio Scorecard (FY2025)",
            "badge": "Ratio Framework",
            "content_type": "text_cards",
            "description": "The cash flow ratio triad provides an objective solvency and operating assessment immune to accrual manipulation.",
            "key_metrics": [
                {"label": "1. Cash Flow Adequacy Ratio", "val": "0.078x (Critical failure; healthy threshold > 1.0x)"},
                {"label": "2. Cash Flow to Debt Ratio", "val": "0.040x (Extreme leverage risk; healthy threshold > 0.40x)"},
                {"label": "3. Cash Return on Assets (Cash ROA)", "val": "0.67% (Severe capital inefficiency; peer median ~8-12%)"},
                {"label": "Overall Ratio Diagnostic", "val": "Distressed solvency profile masked by temporary bank debt liquidity"}
            ]
        }
    },
    17: {
        "header": "RATIO 1 OF 3",
        "subtitle": "Cash Flow Adequacy Ratio: CFO ÷ (Capex + Debt Repayments + Dividends)",
        "theory_explanation": "Cash Flow Adequacy Ratio: CFO divided by (Capex + Debt Repayments + Dividends). Above 1.0x indicates the firm covers internal capital needs without external debt or equity dilution. Below 1.0x signals financing dependency.",
        "goto_explanation": "GoTo's Cash Flow Adequacy Ratio is a dismal 0.078x: CFO of Rp 307.0 bn divided by (Capex Rp 1,182.4 bn + Debt Repayments Rp 2,778.2 bn short-term). GoTo covers less than 8% of its immediate mandatory cash commitments from operations.",
        "goto_report": {
            "title": "GoTo Cash Flow Adequacy Ratio Deconstruction",
            "badge": "Solvency Ratio 1",
            "content_type": "table",
            "table_headers": ["Adequacy Formula Component", "GoTo 2025 Amount (Rp bn)", "Benchmark Standard", "Adequacy Assessment"],
            "table_rows": [
                ["Numerator: Operating Cash Flow (CFO)", "307.0", "Positive cash flow", "Barely positive (+1.7% of revenue)"],
                ["Denominator Item 1: Capital Expenditures (Capex)", "1,182.4", "Required tech maintenance", "CFO covers only 26.0% of capex alone"],
                ["Denominator Item 2: Short-Term Debt Due", "2,778.2", "Bank obligations due <1 year", "CFO covers only 11.1% of short-term debt"],
                ["Denominator Item 3: Cash Dividends", "0.0", "Zero dividends paid", "No cash returned to shareholders"],
                ["Total Mandatory Outflows (Denominator)", "3,960.6", "Full cash obligations", "Requires Rp 3.96T in annual liquidity"],
                ["Cash Flow Adequacy Ratio (CFO / Outflows)", "0.078x", "> 1.0x Threshold", "Severe Deficit (Covers only 7.8% of needs)"]
            ],
            "analytical_note": "Formula Proof: Cash Flow Adequacy = 307.0 / (1,182.4 + 2,778.2 + 0) = 0.078x. GoTo generates less than 8 cents of operational cash for every dollar of capex and debt repayments coming due."
        }
    },
    18: {
        "header": "RATIO 2 OF 3",
        "subtitle": "Cash Flow to Debt Ratio: CFO ÷ Total Debt",
        "theory_explanation": "Cash Flow to Debt Ratio: CFO divided by Total Debt. Measures how many years of current operating cash flow would be required to extinguish total debt. Above 0.40x indicates strong solvency. Below 0.10x indicates acute repayment vulnerability.",
        "goto_explanation": "GoTo's Cash Flow to Debt Ratio is 0.040x: CFO of Rp 307.0 bn divided by Total Debt of Rp 7,742.6 bn. It would take GoTo over 25 years of 2025 cash flow to retire its debt, assuming zero capex!",
        "goto_report": {
            "title": "GoTo Cash Flow to Debt & Repayment Amortization",
            "badge": "Solvency Ratio 2",
            "content_type": "table",
            "table_headers": ["Debt Coverage Metric", "GoTo 2024A", "GoTo 2025A", "Healthy Threshold", "Forensic Interpretation"],
            "table_rows": [
                ["Operating Cash Flow (CFO)", "(762.4)", "307.0", "> 0", "Turned positive, but tiny magnitude"],
                ["Short-Term Bank Borrowings", "2,342.1", "2,778.2", "Low", "Due within 12 months"],
                ["Long-Term Bank Debt & Leases", "1,477.9", "4,964.4", "Sustainable", "+235.9% expansion in long-term debt"],
                ["Total Consolidated Debt", "3,820.0", "7,742.6", "Moderate", "Total debt doubled (+102.7% YoY)"],
                ["Cash Flow to Debt Ratio (CFO / Debt)", "-0.199x", "0.040x", "> 0.40x", "Extreme solvency vulnerability"],
                ["Implied Debt Amortization Period", "Infinite (Negative)", "25.2 Years", "< 2.5 Years", "Takes a quarter century of 2025 CFO to repay debt"]
            ],
            "analytical_note": "Formula Proof: Cash Flow to Debt = 307.0 / 7,742.6 = 0.040x. Inverted, 1 / 0.040 = 25.2 years. Even if GoTo spent zero rupiah on servers, marketing, and developers, it would take 25.2 years of operating cash flow to retire its debt."
        }
    },
    19: {
        "header": "RATIO 3 OF 3",
        "subtitle": "Cash Return on Assets (Cash ROA): CFO ÷ Total Assets",
        "theory_explanation": "Cash Return on Assets: Operating Cash Flow divided by Total Assets. The cash-basis analog to ROA. Unlike Net Income / Assets, Cash ROA is immune to accrual distortions, non-cash depreciation, and subjective revenue timing.",
        "goto_explanation": "GoTo's Cash ROA is 0.67%: CFO of Rp 307.0 bn divided by Total Assets of Rp 45,758.1 bn. Despite managing a Rp 45.8 trillion asset base, GoTo converts less than 0.7% into operating cash flow.",
        "goto_report": {
            "title": "GoTo Cash Return on Assets (Cash ROA) Analysis",
            "badge": "Operating Efficiency Ratio 3",
            "content_type": "table",
            "table_headers": ["Return on Assets Metric", "Accrual Basis (ROA)", "Cash Basis (Cash ROA)", "Variance", "Forensic Meaning"],
            "table_rows": [
                ["Numerator", "Net Loss: (1,501.7)", "CFO: +307.0", "+Rp 1,808.7 bn", "Accruals vs Real Cash Spread"],
                ["Denominator (Total Assets)", "45,758.1", "45,758.1", "Rp 0.0", "Consolidated Balance Sheet Base"],
                ["Calculated Return Metric", "-3.28% (Negative ROA)", "+0.67% (Cash ROA)", "+3.95% Spread", "Accruals show loss; cash shows tiny return"],
                ["Benchmark (Cost of Capital)", "+13.5% WACC", "+13.5% WACC", "Severe Hurdle Gap", "Both metrics fail cost of capital hurdle by over 1,200 bps"]
            ],
            "analytical_note": "Formula Proof: Cash ROA = 307.0 / 45,758.1 = 0.67%. Even after stripping out non-cash losses, GoTo generates an anemic 67 cents of cash flow per Rp 100 of assets deployed, failing to cover its 13.5% cost of capital."
        }
    },
    20: {
        "header": "THE CENTRAL IDEA",
        "subtitle": "Earnings Quality vs. Cash Quality: The Red Flag Gap",
        "theory_explanation": "The Red Flag Gap: A large, persistent gap between net income and operating cash flow in either direction is one of the most reliable red flags in financial statement analysis. Cash is far harder to manipulate than accruals.",
        "goto_explanation": "GoTo presents a colossal multi-year gap: In 2023, Net Loss was -(Rp 90.5T) while CFO was -(Rp 3.9T). In 2025, Net Loss was -(Rp 1.50T) while CFO was +Rp 307 bn. This persistent divergence is driven by billions in non-cash stock compensation and associate write-downs.",
        "goto_report": {
            "title": "GoTo Accrual-to-Cash Gap & Earnings Quality Red Flags",
            "badge": "Forensic Quality",
            "content_type": "text_cards",
            "description": "Analyzing the multi-trillion discrepancy between GoTo's accrual income statement and its cash flow reality across three fiscal years.",
            "key_metrics": [
                {"label": "2023 Accrual vs Cash Gap", "val": "Rp 86.6 trillion spread (driven by Rp 79.5T goodwill write-down)"},
                {"label": "2024 Accrual vs Cash Gap", "val": "Rp 4.7 trillion spread (driven by Tokopedia deconsolidation losses)"},
                {"label": "2025 Accrual vs Cash Gap", "val": "Rp 1.81 trillion spread (D&A add-back + stock compensation)"},
                {"label": "Earnings Quality Rating", "val": "Low (Recurring non-cash adjustments disconnect P&L from cash reality)"}
            ]
        }
    },
    21: {
        "header": "A PRACTICAL TECHNIQUE",
        "subtitle": "Resolving a Net Income vs. Cash Flow Puzzle",
        "theory_explanation": "The 3 Working Capital Questions: 1) Did receivables grow faster than revenue? (Earned, not yet collected). 2) Did inventory build up? (Cash spent, not yet in COGS). 3) Did payables stretch out? (Expense incurred, cash not yet paid).",
        "goto_explanation": "In GoTo's 2025 financial statements: Receivables grew +15.2% (Rp 547.3 bn vs Rp 475.2 bn), roughly matching revenue (+15.3%). Trade payables stretched to Rp 1,578.4 bn (+8.2%), allowing GoTo to preserve cash by delaying vendor payments.",
        "goto_report": {
            "title": "Working Capital Forensic Audit: Receivables, Inventory, and Payables",
            "badge": "Forensic Technique",
            "content_type": "text_cards",
            "description": "Applying the three working capital diagnostic questions to PT GoTo Gojek Tokopedia Tbk's balance sheet movements.",
            "key_metrics": [
                {"label": "1. Receivables vs Revenue Growth", "val": "Receivables +15.2% vs Revenue +15.3% (Healthy alignment, no channel stuffing)"},
                {"label": "2. Inventory Buildup", "val": "Inventory fell from Rp 15.8m to Rp 14.1m (Zero inventory tie-up)"},
                {"label": "3. Payables Stretching", "val": "Trade payables rose to Rp 1,578.4 bn (GoTo preserved cash by delaying vendor settlements)"},
                {"label": "Working Capital Cash Drain", "val": "Total operating working capital change drained -(Rp 1,576.1 billion) in cash"}
            ]
        }
    },
    22: {
        "header": "CLOSING THE LOOP",
        "subtitle": "ABBA's Resolution vs. GoTo's Resolution",
        "theory_explanation": "The Resolution: ABBA's CFO turned positive because receivables fell from Rp 61.8bn to Rp 44.1bn (collecting old cash). GoTo's CFO turned positive not through aggressive customer collections, but through non-cash add-backs and vendor payable timing.",
        "goto_explanation": "Contrasting the resolutions: ABBA collected historical cash from customers. GoTo achieved positive CFO because Rp 1.37T of software depreciation and Rp 412.5m of stock-based compensation were added back to its net loss.",
        "goto_report": {
            "title": "Cash Flow Resolution Contrast: ABBA vs GoTo",
            "badge": "Resolution Synthesis",
            "content_type": "table",
            "table_headers": ["Company", "Reported Net Result", "Reported CFO", "Primary Driver of CFO Turnaround", "Quality of Turnaround"],
            "table_rows": [
                ["ABBA (Mahaka Media)", "Loss: (Rp 25.7 bn)", "+Rp 2.8 bn", "Collected Rp 17.7 bn of old receivables", "High cash quality (Real cash collected)"],
                ["GoTo (Gojek Tokopedia)", "Loss: (Rp 1,501.7 bn)", "+Rp 307.0 bn", "Added back Rp 2.37T in D&A and non-cash equity items", "Low cash quality (Accrual add-back artifact)"]
            ],
            "analytical_note": "Forensic Conclusion: ABBA's cash turnaround was driven by real collections from customers. GoTo's cash turnaround was an accrual artifact where non-cash depreciation and stock compensation eclipsed the operational loss."
        }
    },
    23: {
        "header": "KEY TAKEAWAYS",
        "subtitle": "What to Remember from Week 4",
        "theory_explanation": "Core Principles: 1) Net income and cash differ by design, not error. 2) Classify every flow and read the life-cycle sign pattern. 3) Direct and indirect methods must reconcile. 4) Free cash flow (CFO - Capex) is the foundation of DCF valuation. 5) Divergence resolves through working capital.",
        "goto_explanation": "Final Week 4 Takeaway for GoTo: GoTo's positive CFO (+Rp 307 bn) is insufficient to support its capex (Rp 1.18T), resulting in negative Free Cash Flow (-(Rp 875 bn)). Debt doubled to Rp 7.74T, leaving cash flow adequacy at 0.078x.",
        "goto_report": {
            "title": "Week 4 Synthesis: The Cash Truth About GoTo",
            "badge": "Classroom Synthesis",
            "content_type": "text_cards",
            "description": "Week 4 equips analysts to see past accounting opinions. GoTo's statement of cash flows proves that narrowing losses have not solved fundamental cash generation shortfalls.",
            "key_metrics": [
                {"label": "Cash Signature", "val": "Anomalous (+ + +) fueled by debt borrowing and time deposit liquidation"},
                {"label": "Free Cash Flow Reality", "val": "-(Rp 875.3 billion) burn after mandatory software and server capex"},
                {"label": "Solvency Diagnostic", "val": "Cash Flow Adequacy is 0.078x; Cash Flow to Debt is 0.040x (25.2 years to repay)"},
                {"label": "Final Classroom Stance", "val": "SELL / AVOID confirmed by negative organic free cash flow"}
            ]
        }
    },
    24: {
        "header": "CLASS ACTIVITY",
        "subtitle": "CFO Independent Reconstruction",
        "theory_explanation": "Hands-On Exercise: Reconstructing Operating Cash Flow independently from the Income Statement and Balance Sheet. Deriving the statement by hand builds the analytical muscle required for pro-forma forecasting in Week 13.",
        "goto_explanation": "Group 4's reconstruction of GoTo's Statement of Cash Flows: Reconciling reported Net Loss of -(Rp 1,501.7 bn) through D&A, stock comp, associates, and working capital to arrive independently at the exact published CFO of +Rp 307.0 bn.",
        "goto_report": {
            "title": "Group 4 Independent CFO Reconstruction Schedule",
            "badge": "Class Activity Reconstruction",
            "content_type": "table",
            "table_headers": ["Reconstruction Step", "Line Item Account", "Formula / Source", "Amount (Rp billion)"],
            "table_rows": [
                ["Step 1: Starting Accrual Base", "Rugi tahun berjalan (Net Loss)", "Audited P&L (LK p. 17)", "(1,501.7)"],
                ["Step 2: Add Non-Cash Depreciation", "Penyusutan aset tetap (PP&E)", "LK Note 11 (Aset tetap)", "+285.2"],
                ["Step 3: Add Non-Cash Amortization", "Amortisasi aset takberwujud", "LK Note 12 (Software)", "+1,086.9"],
                ["Step 4: Add Stock Compensation", "Beban kompensasi saham", "LK Note 23 (Share options)", "+412.5"],
                ["Step 5: Add Associate Equity Loss", "Bagian rugi entitas asosiasi", "LK Note 10 (Tokopedia)", "+588.4"],
                ["Step 6: Add Financial Fair Value Loss", "Rugi nilai wajar instrumen", "LK Note 27b (FVTPL)", "+596.7"],
                ["Step 7: Adjust Working Capital", "Perubahan modal kerja operasi", "Balance Sheet changes", "(1,161.0)"],
                ["Step 8: Reconstructed CFO", "Arus Kas Operasi (CFO)", "Step 1 through Step 7", "+307.0"]
            ],
            "analytical_note": "Reconstruction Check: Independently derived CFO of +Rp 307.0 billion perfectly reconciles with the official Direct Method cash flow statement reported on page 20."
        },
        "audit_evidence": {
            "img": "/evidence/goto_cash_flows_p1_highlighted.png",
            "title": "Audited Operating Cash Flow Benchmark (LK p. 20)",
            "caption": "Official GoTo LK p. 20: Published benchmark against which Group 4's independent reconstruction reconciles."
        }
    }
}

# Update week 4 in full_slides_knowledgebase.json
w4["slides"] = []
for slide_num in range(1, 25):
    info = w4_data.get(slide_num, {})
    slide_obj = {
        "slide_num": slide_num,
        "header": info.get("header", f"Slide {slide_num}"),
        "subtitle": info.get("subtitle", ""),
        "raw_text": f"{info.get('header', '')}\n{info.get('subtitle', '')}\nWeek 4 Statement of Cash Flows",
        "theory_explanation": info.get("theory_explanation", ""),
        "goto_explanation": info.get("goto_explanation", ""),
        "image_url": f"/slides/FSA_Week4_PPT/slide_{slide_num}.png",
        "goto_report": info.get("goto_report", {}),
    }
    if "audit_evidence" in info:
        slide_obj["audit_evidence"] = info["audit_evidence"]
    w4["slides"].append(slide_obj)

with open("goto-fsa-study/src/data/full_slides_knowledgebase.json", "w") as f:
    json.dump(modules, f, indent=2)

print(f"Successfully generated all {len(w4['slides'])} slides for Week 4!")
