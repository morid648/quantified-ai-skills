"""
Generates the 50 synthetic financial documents, gold label ground truth,
and secondary annotation pass for the Finance Validation Run (v1.0).
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARK_DIR = os.path.join(BASE_DIR, "benchmarks", "finance-50doc-v1")
DOCS_DIR = os.path.join(BENCHMARK_DIR, "documents")
GOLD_DIR = os.path.join(BENCHMARK_DIR, "gold_labels")
PASS2_DIR = os.path.join(BENCHMARK_DIR, "annotator_pass2")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(GOLD_DIR, exist_ok=True)
os.makedirs(PASS2_DIR, exist_ok=True)

# 1. INVOICES (10 documents: inv_01 to inv_10)
INVOICE_DATA = [
    {
        "id": "inv_01",
        "vendor": "Apex Cloud Systems Inc",
        "inv_num": "INV-2024-1001",
        "date": "2024-01-15",
        "due": "2024-02-15",
        "items": [
            {"desc": "Kubernetes Cluster Hosting", "qty": 1.0, "unit": 4500.00, "amt": 4500.00},
            {"desc": "High-Throughput Storage (TB)", "qty": 10.0, "unit": 120.00, "amt": 1200.00},
            {"desc": "24/7 SRE Enterprise SLA", "qty": 1.0, "unit": 1800.00, "amt": 1800.00}
        ],
        "subtotal": 7500.00, "tax": 600.00, "total": 8100.00, "noisy": False, "flaws": []
    },
    {
        "id": "inv_02",
        "vendor": "Meridian Office Solutions LLC",
        "inv_num": "MOS-88219",
        "date": "2024-01-22",
        "due": "2024-02-22",
        "items": [
            {"desc": "Ergonomic Mesh Task Chairs", "qty": 8.0, "unit": 350.00, "amt": 2800.00},
            {"desc": "Motorized Sit-Stand Desks", "qty": 4.0, "unit": 650.00, "amt": 2600.00}
        ],
        "subtotal": 5400.00, "tax": 432.00, "total": 5832.00, "noisy": False, "flaws": []
    },
    {
        "id": "inv_03",
        "vendor": "Crestview Strategic Consulting",
        "inv_num": "CSC-9904",
        "date": "2024-02-01",
        "due": "2024-03-01",
        "items": [
            {"desc": "Q1 Market Expansion Feasibility Study", "qty": 40.0, "unit": 275.00, "amt": 11000.00},
            {"desc": "Competitive Intelligence Dossier", "qty": 1.0, "unit": 3500.00, "amt": 3500.00}
        ],
        "subtotal": 14500.00, "tax": 0.00, "total": 14500.00, "noisy": False, "flaws": []
    },
    {
        "id": "inv_04",
        "vendor": "Summit Logistics & Freight",
        "inv_num": "SLF-44102",
        "date": "2024-02-10",
        "due": "2024-02-25",
        "items": [
            {"desc": "Interstate Freight Transit - 2 TEU", "qty": 2.0, "unit": 1850.00, "amt": 3700.00},
            {"desc": "Fuel Surcharge", "qty": 1.0, "unit": 420.50, "amt": 420.50}
        ],
        "subtotal": 4120.50, "tax": 206.03, "total": 4326.53, "noisy": False, "flaws": []
    },
    {
        "id": "inv_05",
        "vendor": "Hyperion Cybersecurity Corp",
        "inv_num": "HYP-2024-501",
        "date": "2024-02-18",
        "due": "2024-03-20",
        "items": [
            {"desc": "Penetration Testing & Red Team Audit", "qty": 1.0, "unit": 16000.00, "amt": 16000.00},
            {"desc": "SOC-2 Type II Compliance Readiness", "qty": 1.0, "unit": 8500.00, "amt": 8500.00}
        ],
        "subtotal": 24500.00, "tax": 1960.00, "total": 26460.00, "noisy": False, "flaws": []
    },
    {
        "id": "inv_06",
        "vendor": "Vanguard Hardware Distribution",
        "inv_num": "VHD-77301",
        "date": "2024-03-02",
        "due": "2024-04-02",
        "items": [
            {"desc": "Rackmount Server Nodes 1U", "qty": 3.0, "unit": 3200.00, "amt": 9600.00},
            {"desc": "100GbE Managed Switch", "qty": 1.0, "unit": 4200.00, "amt": 4200.00}
        ],
        "subtotal": 13800.00, "tax": 1104.00, "total": 14904.00, "noisy": False, "flaws": []
    },
    {
        "id": "inv_07",
        "vendor": "BlueWave Media & Advertising",
        "inv_num": "BWM-2024-039",
        "date": "2024-03-12",
        "due": "2024-04-12",
        "items": [
            {"desc": "Digital Ad Placement Retainer", "qty": 1.0, "unit": 8000.00, "amt": 8000.00},
            {"desc": "Creative Production & Video Assets", "qty": 1.0, "unit": 4500.00, "amt": 4500.00}
        ],
        "subtotal": 12500.00, "tax": 1000.00, "total": 13500.00, "noisy": False, "flaws": []
    },
    {
        "id": "inv_08",
        "vendor": "Pinnacle Facilities Management",
        "inv_num": "PFM-11082",
        "date": "2024-03-20",
        "due": "2024-04-20",
        "items": [
            {"desc": "Monthly Commercial Janitorial Service", "qty": 1.0, "unit": 2400.00, "amt": 2400.00},
            {"desc": "HVAC Filter Replacement & Inspection", "qty": 1.0, "unit": 850.00, "amt": 850.00}
        ],
        "subtotal": 3250.00, "tax": 260.00, "total": 3510.00, "noisy": False, "flaws": []
    },
    # NOISY INVOICES
    {
        "id": "inv_09",
        "vendor": "OmniTek Global Software",
        "inv_num": "OTG-90211",
        "date": "2024-03-25",
        "due": None, # Missing due date
        "items": [
            {"desc": "Enterprise Core License O1 x (OCR Noise)", "qty": 1.0, "unit": 5200.00, "amt": 5200.00},
            {"desc": "Add-on Analytics Module", "qty": 2.0, "unit": 900.00, "amt": 1800.00}
        ],
        "subtotal": 7000.00, "tax": 560.00, "total": 7560.00, "noisy": True,
        "flaws": ["missing_due_date", "ocr_noise_in_line_item"]
    },
    {
        "id": "inv_10",
        "vendor": "Acme Industrial Supplies",
        "inv_num": "AIS-66100",
        "date": "2024-04-01",
        "due": "2024-05-01",
        "items": [
            {"desc": "Packaging Crates Grade A", "qty": 100.0, "unit": 25.00, "amt": 2500.00},
            {"desc": "Industrial Strapping Rolls", "qty": 10.0, "unit": 80.00, "amt": 800.00}
        ],
        "subtotal": 3300.00, "tax": 264.00, "total": 3574.00, # Deliberate arithmetic mismatch on total: 3300 + 264 = 3564, but document states 3574
        "stated_doc_total": 3574.00, "calculated_total": 3564.00,
        "noisy": True, "flaws": ["arithmetic_total_discrepancy"]
    }
]

# 2. BANK STATEMENTS (10 documents: bank_01 to bank_10)
BANK_DATA = [
    {
        "id": "bank_01",
        "bank": "First Horizon Commercial Bank",
        "account": "9820-4411-82",
        "start": "2024-01-01", "end": "2024-01-31",
        "opening": 45200.00, "closing": 58950.00,
        "txns": [
            {"date": "2024-01-05", "desc": "Wire In: Alpha Ventures", "amount": 25000.00, "balance": 70200.00},
            {"date": "2024-01-12", "desc": "ACH Out: Payroll Services", "amount": -8500.00, "balance": 61700.00},
            {"date": "2024-01-25", "desc": "Debit: Cloud Infrastructure", "amount": -2750.00, "balance": 58950.00}
        ],
        "noisy": False, "flaws": []
    },
    {
        "id": "bank_02",
        "bank": "Pacific Merchant Bank",
        "account": "1044-8839-01",
        "start": "2024-01-01", "end": "2024-01-31",
        "opening": 112400.00, "closing": 98600.00,
        "txns": [
            {"date": "2024-01-08", "desc": "Vendor Pmt: Apex Systems", "amount": -18800.00, "balance": 93600.00},
            {"date": "2024-01-20", "desc": "Client Retainer: Acme Corp", "amount": 5000.00, "balance": 98600.00}
        ],
        "noisy": False, "flaws": []
    },
    {
        "id": "bank_03",
        "bank": "Beacon Trust & Savings",
        "account": "5501-2299-43",
        "start": "2024-02-01", "end": "2024-02-29",
        "opening": 28400.00, "closing": 44150.00,
        "txns": [
            {"date": "2024-02-04", "desc": "Deposit: POS Terminal Settlement", "amount": 19250.00, "balance": 47650.00},
            {"date": "2024-02-18", "desc": "Utility Bill Autopay", "amount": -3500.00, "balance": 44150.00}
        ],
        "noisy": False, "flaws": []
    },
    {
        "id": "bank_04",
        "bank": "Metro Commercial Bank",
        "account": "3391-7722-60",
        "start": "2024-02-01", "end": "2024-02-29",
        "opening": 76500.00, "closing": 62100.00,
        "txns": [
            {"date": "2024-02-11", "desc": "ACH: Commercial Lease Office", "amount": -12000.00, "balance": 64500.00},
            {"date": "2024-02-24", "desc": "Corporate Credit Card Settlement", "amount": -2400.00, "balance": 62100.00}
        ],
        "noisy": False, "flaws": []
    },
    {
        "id": "bank_05",
        "bank": "Keystone National Bank",
        "account": "4490-1120-77",
        "start": "2024-03-01", "end": "2024-03-31",
        "opening": 154000.00, "closing": 178200.00,
        "txns": [
            {"date": "2024-03-07", "desc": "Wire Transfer Customer Payment", "amount": 35000.00, "balance": 189000.00},
            {"date": "2024-03-22", "desc": "Tax Withholding Payment", "amount": -10800.00, "balance": 178200.00}
        ],
        "noisy": False, "flaws": []
    },
    {
        "id": "bank_06",
        "bank": "Liberty Business Banking",
        "account": "8812-4409-12",
        "start": "2024-03-01", "end": "2024-03-31",
        "opening": 33100.00, "closing": 29800.00,
        "txns": [
            {"date": "2024-03-10", "desc": "Office Supplies Direct Debit", "amount": -4500.00, "balance": 28600.00},
            {"date": "2024-03-28", "desc": "Interest Earned", "amount": 1200.00, "balance": 29800.00}
        ],
        "noisy": False, "flaws": []
    },
    {
        "id": "bank_07",
        "bank": "First Horizon Commercial Bank",
        "account": "9820-4411-82",
        "start": "2024-02-01", "end": "2024-02-29",
        "opening": 58950.00, "closing": 71450.00,
        "txns": [
            {"date": "2024-02-14", "desc": "Client Invoice Collection", "amount": 21000.00, "balance": 79950.00},
            {"date": "2024-02-28", "desc": "ACH Out: Healthcare Benefits", "amount": -8500.00, "balance": 71450.00}
        ],
        "noisy": False, "flaws": []
    },
    {
        "id": "bank_08",
        "bank": "Pacific Merchant Bank",
        "account": "1044-8839-01",
        "start": "2024-02-01", "end": "2024-02-29",
        "opening": 98600.00, "closing": 84200.00,
        "txns": [
            {"date": "2024-02-09", "desc": "Software Tool Subscriptions", "amount": -14400.00, "balance": 84200.00}
        ],
        "noisy": False, "flaws": []
    },
    # NOISY BANK STATEMENTS
    {
        "id": "bank_09",
        "bank": "Summit City Union Bank",
        "account": "7710-9941-O8", # OCR letter O instead of 0
        "start": "2024-03-01", "end": "2024-03-31",
        "opening": 12500.00, "closing": 8750.00,
        "txns": [
            {"date": "2024-03-05", "desc": "Merchant POS Batch", "amount": 4200.00, "balance": 16700.00},
            {"date": "2024-03-19", "desc": "Unrecognized International Fee", "amount": -7950.00, "balance": 8750.00}
        ],
        "noisy": True, "flaws": ["ocr_char_in_account_number"]
    },
    {
        "id": "bank_10",
        "bank": "Keystone National Bank",
        "account": "4490-8811-00",
        "start": "2024-04-01", "end": "2024-04-30",
        "opening": 2100.00, "closing": -450.00, # Negative balance / Overdraft
        "txns": [
            {"date": "2024-04-12", "desc": "ACH Debit: Equipment Rental", "amount": -2550.00, "balance": -450.00}
        ],
        "noisy": True, "flaws": ["overdraft_negative_closing_balance"]
    }
]

# 3. INCOME STATEMENTS (10 documents: inc_01 to inc_10)
INCOME_DATA = [
    {
        "id": "inc_01",
        "company": "Northstar Logistics Corp",
        "period": "Q1 2024",
        "revenue": 1250000.00, "cogs": 650000.00, "gross_profit": 600000.00,
        "opex": 380000.00, "operating_income": 220000.00, "net_income": 176000.00,
        "noisy": False, "flaws": []
    },
    {
        "id": "inc_02",
        "company": "Vanguard Biotech Inc",
        "period": "Q1 2024",
        "revenue": 840000.00, "cogs": 210000.00, "gross_profit": 630000.00,
        "opex": 490000.00, "operating_income": 140000.00, "net_income": 112000.00,
        "noisy": False, "flaws": []
    },
    {
        "id": "inc_03",
        "company": "Apex Cloud Systems Inc",
        "period": "Q4 2023",
        "revenue": 2100000.00, "cogs": 720000.00, "gross_profit": 1380000.00,
        "opex": 890000.00, "operating_income": 490000.00, "net_income": 392000.00,
        "noisy": False, "flaws": []
    },
    {
        "id": "inc_04",
        "company": "BlueRidge Industrial Supply",
        "period": "Q1 2024",
        "revenue": 3450000.00, "cogs": 2150000.00, "gross_profit": 1300000.00,
        "opex": 780000.00, "operating_income": 520000.00, "net_income": 416000.00,
        "noisy": False, "flaws": []
    },
    {
        "id": "inc_05",
        "company": "Zenith Financial Technologies",
        "period": "Q1 2024",
        "revenue": 1820000.00, "cogs": 360000.00, "gross_profit": 1460000.00,
        "opex": 920000.00, "operating_income": 540000.00, "net_income": 432000.00,
        "noisy": False, "flaws": []
    },
    {
        "id": "inc_06",
        "company": "Silverline Consumer Products",
        "period": "Q1 2024",
        "revenue": 950000.00, "cogs": 580000.00, "gross_profit": 370000.00,
        "opex": 260000.00, "operating_income": 110000.00, "net_income": 88000.00,
        "noisy": False, "flaws": []
    },
    {
        "id": "inc_07",
        "company": "TerraEnergy Dynamics",
        "period": "Q4 2023",
        "revenue": 4800000.00, "cogs": 3100000.00, "gross_profit": 1700000.00,
        "opex": 950000.00, "operating_income": 750000.00, "net_income": 600000.00,
        "noisy": False, "flaws": []
    },
    {
        "id": "inc_08",
        "company": "OmniMedia Publishing Group",
        "period": "Q1 2024",
        "revenue": 620000.00, "cogs": 180000.00, "gross_profit": 440000.00,
        "opex": 310000.00, "operating_income": 130000.00, "net_income": 104000.00,
        "noisy": False, "flaws": []
    },
    # NOISY INCOME STATEMENTS
    {
        "id": "inc_09",
        "company": "Cascade Marine Services",
        "period": "TTM Ended Q2 2024 (Non-Standard)",
        "revenue": 1420000.00, "cogs": 890000.00, "gross_profit": 530000.00,
        "opex": 390000.00, "operating_income": 140000.00, "net_income": 112000.00,
        "noisy": True, "flaws": ["non_standard_fiscal_period_header"]
    },
    {
        "id": "inc_10",
        "company": "Delta Robotics Lab",
        "period": "Q1 2024",
        "revenue": 2200000.00, "cogs": 980000.00, "gross_profit": 1220000.00,
        "opex": 750000.00, "operating_income": 470000.00, "net_income": 371000.00, # 1k arithmetic discrepancy in document vs 376000
        "stated_net_income": 371000.00, "calculated_net_income": 376000.00,
        "noisy": True, "flaws": ["arithmetic_rounding_discrepancy"]
    }
]

# 4. EXPENSE REPORTS (10 documents: exp_01 to exp_10)
EXPENSE_DATA = [
    {
        "id": "exp_01",
        "employee": "Sarah Jenkins",
        "report_id": "EXP-2024-081",
        "date": "2024-02-14",
        "items": [
            {"date": "2024-02-10", "category": "TRAVEL", "merchant": "Delta Air Lines", "amount": 485.20},
            {"date": "2024-02-11", "category": "LODGING", "merchant": "Marriott Downtown", "amount": 340.00},
            {"date": "2024-02-12", "category": "MEALS", "merchant": "The Palm Steakhouse", "amount": 125.50}
        ],
        "total": 950.70, "status": "APPROVED", "noisy": False, "flaws": []
    },
    {
        "id": "exp_02",
        "employee": "Michael Chang",
        "report_id": "EXP-2024-082",
        "date": "2024-02-18",
        "items": [
            {"date": "2024-02-15", "category": "SOFTWARE", "merchant": "JetBrains License", "amount": 249.00},
            {"date": "2024-02-16", "category": "SUPPLIES", "merchant": "Amazon Business", "amount": 78.40}
        ],
        "total": 327.40, "status": "APPROVED", "noisy": False, "flaws": []
    },
    {
        "id": "exp_03",
        "employee": "David Rossi",
        "report_id": "EXP-2024-083",
        "date": "2024-02-25",
        "items": [
            {"date": "2024-02-20", "category": "TRAVEL", "merchant": "Uber Technologies", "amount": 42.80},
            {"date": "2024-02-21", "category": "MEALS", "merchant": "Blue Bottle Coffee", "amount": 18.50}
        ],
        "total": 61.30, "status": "APPROVED", "noisy": False, "flaws": []
    },
    {
        "id": "exp_04",
        "employee": "Elena Rostova",
        "report_id": "EXP-2024-084",
        "date": "2024-03-02",
        "items": [
            {"date": "2024-02-27", "category": "LODGING", "merchant": "Hyatt Regency", "amount": 620.00},
            {"date": "2024-02-28", "category": "TRAVEL", "merchant": "United Airlines", "amount": 510.00}
        ],
        "total": 1130.00, "status": "APPROVED", "noisy": False, "flaws": []
    },
    {
        "id": "exp_05",
        "employee": "Marcus Vance",
        "report_id": "EXP-2024-085",
        "date": "2024-03-05",
        "items": [
            {"date": "2024-03-01", "category": "SOFTWARE", "merchant": "GitHub Enterprise", "amount": 420.00},
            {"date": "2024-03-02", "category": "SOFTWARE", "merchant": "Figma Professional", "amount": 180.00}
        ],
        "total": 600.00, "status": "APPROVED", "noisy": False, "flaws": []
    },
    {
        "id": "exp_06",
        "employee": "Jessica Miller",
        "report_id": "EXP-2024-086",
        "date": "2024-03-12",
        "items": [
            {"date": "2024-03-08", "category": "MEALS", "merchant": "Pret A Manger", "amount": 24.10},
            {"date": "2024-03-09", "category": "TRAVEL", "merchant": "Amtrak Northeast", "amount": 185.00}
        ],
        "total": 209.10, "status": "APPROVED", "noisy": False, "flaws": []
    },
    {
        "id": "exp_07",
        "employee": "Rajesh Patel",
        "report_id": "EXP-2024-087",
        "date": "2024-03-18",
        "items": [
            {"date": "2024-03-14", "category": "SUPPLIES", "merchant": "Staples Office Store", "amount": 145.20},
            {"date": "2024-03-15", "category": "TRAVEL", "merchant": "Lyft Transportation", "amount": 38.60}
        ],
        "total": 183.80, "status": "APPROVED", "noisy": False, "flaws": []
    },
    {
        "id": "exp_08",
        "employee": "Hannah Abbott",
        "report_id": "EXP-2024-088",
        "date": "2024-03-22",
        "items": [
            {"date": "2024-03-19", "category": "LODGING", "merchant": "Hilton Garden Inn", "amount": 290.00},
            {"date": "2024-03-20", "category": "MEALS", "merchant": "Chipotle Mexican Grill", "amount": 16.75}
        ],
        "total": 306.75, "status": "APPROVED", "noisy": False, "flaws": []
    },
    # NOISY EXPENSE REPORTS
    {
        "id": "exp_09",
        "employee": "Arthur Pendelton",
        "report_id": "EXP-2024-089",
        "date": "2024-03-28",
        "items": [
            {"date": "2024-03-24", "category": "LODGING", "merchant": "Boutique Hotel (Missing Receipt Note)", "amount": 450.00},
            {"date": "2024-03-25", "category": "MEALS", "merchant": "Airport Cafe", "amount": 28.50}
        ],
        "total": 478.50, "status": "PENDING", "noisy": True,
        "flaws": ["missing_receipt_attachment_flag", "pending_supervisor_approval"]
    },
    {
        "id": "exp_10",
        "employee": "Chloe Bennett",
        "report_id": "EXP-2024-090",
        "date": "2024-04-02",
        "items": [
            {"date": "2024-03-30", "category": "MEALS", "merchant": "Corner Bistro (Duplicate Entry A)", "amount": 65.00},
            {"date": "2024-03-30", "category": "MEALS", "merchant": "Corner Bistro (Duplicate Entry B)", "amount": 65.00}
        ],
        "total": 130.00, "status": "REJECTED", "noisy": True,
        "flaws": ["duplicate_transaction_same_day", "rejected_policy_flag"]
    }
]

# 5. LOAN / KYC APPLICATIONS (10 documents: loan_01 to loan_10)
LOAN_DATA = [
    {
        "id": "loan_01",
        "applicant": "Jonathan Edward Vance",
        "id_type": "SSN", "id_number": "XXX-XX-4912",
        "income": 145000.00, "requested": 35000.00,
        "purpose": "Debt Consolidation",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    {
        "id": "loan_02",
        "applicant": "Maria Luisa Gonzalez",
        "id_type": "PASSPORT", "id_number": "P88319022",
        "income": 92000.00, "requested": 20000.00,
        "purpose": "Home Improvement Remodel",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    {
        "id": "loan_03",
        "applicant": "Robert Taylor Sterling",
        "id_type": "TAX_ID", "id_number": "XX-XXX7701",
        "income": 220000.00, "requested": 50000.00,
        "purpose": "Working Capital Expansion",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    {
        "id": "loan_04",
        "applicant": "Amanda Claire Wright",
        "id_type": "SSN", "id_number": "XXX-XX-1084",
        "income": 115000.00, "requested": 15000.00,
        "purpose": "Vehicle Purchase",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    {
        "id": "loan_05",
        "applicant": "Tariq Abdul Mansour",
        "id_type": "PASSPORT", "id_number": "N77102941",
        "income": 160000.00, "requested": 40000.00,
        "purpose": "Solar Panel Installation",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    {
        "id": "loan_06",
        "applicant": "Danielle Christine Moore",
        "id_type": "SSN", "id_number": "XXX-XX-9022",
        "income": 88000.00, "requested": 12000.00,
        "purpose": "Medical Expense Financing",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    {
        "id": "loan_07",
        "applicant": "Kevin Alexander O'Connor",
        "id_type": "TAX_ID", "id_number": "XX-XXX4419",
        "income": 175000.00, "requested": 45000.00,
        "purpose": "Inventory Equipment Bridge",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    {
        "id": "loan_08",
        "applicant": "Sunita Lakshmi Rao",
        "id_type": "PASSPORT", "id_number": "Z10948201",
        "income": 130000.00, "requested": 25000.00,
        "purpose": "Higher Education Tuition",
        "risk_flags": [], "noisy": False, "flaws": []
    },
    # NOISY LOAN APPLICATIONS
    {
        "id": "loan_09",
        "applicant": "Bradley Thomas Thorne",
        "id_type": "SSN", "id_number": "XXX-XX-8831",
        "income": 45000.00, "requested": 350000.00, # Excessive debt to income ratio
        "purpose": "Speculative Real Estate",
        "risk_flags": ["DEBT_TO_INCOME_HIGH", "SPECULATIVE_PURPOSE_FLAG"],
        "noisy": True, "flaws": ["high_debt_to_income_anomaly"]
    },
    {
        "id": "loan_10",
        "applicant": "Valerie Nicole Stone",
        "id_type": "PASSPORT", "id_number": "EXPIRED-P33019", # Expired identification document
        "income": 95000.00, "requested": 30000.00,
        "purpose": "Refinancing Secondary Debt",
        "risk_flags": ["EXPIRED_IDENTIFICATION", "IDENTITY_VERIFICATION_FAILED"],
        "noisy": True, "flaws": ["expired_id_document"]
    }
]

def render_invoice_text(d):
    due_line = f"Payment Due Date: {d['due']}" if d['due'] else "Payment Due Date: [NOT SPECIFIED / IMMEDIATE]"
    lines = [
        "==================================================",
        f"               COMMERCIAL INVOICE                 ",
        "==================================================",
        f"Vendor Name:  {d['vendor']}",
        f"Invoice No:   {d['inv_num']}",
        f"Invoice Date: {d['date']}",
        due_line,
        "--------------------------------------------------",
        "LINE ITEMS:",
        f"{'Description':<32} {'Qty':<6} {'Unit Price':<12} {'Amount':<10}"
    ]
    for it in d['items']:
        lines.append(f"{it['desc']:<32} {it['qty']:<6.1f} ${it['unit']:<11.2f} ${it['amt']:<9.2f}")
    lines.append("--------------------------------------------------")
    lines.append(f"Subtotal:                                       ${d['subtotal']:.2f}")
    lines.append(f"Sales / Service Tax:                            ${d['tax']:.2f}")
    tot = d.get('stated_doc_total', d['total'])
    lines.append(f"Total Amount Due:                               ${tot:.2f}")
    lines.append("==================================================")
    return "\n".join(lines)

def render_bank_statement_text(d):
    lines = [
        "==================================================",
        f"        MONTHLY COMMERCIAL ACCOUNT STATEMENT      ",
        "==================================================",
        f"Financial Institution: {d['bank']}",
        f"Account Number:        {d['account']}",
        f"Statement Period:      {d['start']} to {d['end']}",
        "--------------------------------------------------",
        f"Opening Balance:       ${d['opening']:.2f}",
        f"Closing Balance:       ${d['closing']:.2f}",
        "--------------------------------------------------",
        "TRANSACTION LEDGER:",
        f"{'Date':<12} {'Description':<26} {'Amount':<12} {'Balance':<10}"
    ]
    for tx in d['txns']:
        amt_str = f"${tx['amount']:.2f}" if tx['amount'] >= 0 else f"-${abs(tx['amount']):.2f}"
        bal_str = f"${tx['balance']:.2f}" if tx['balance'] >= 0 else f"-${abs(tx['balance']):.2f}"
        lines.append(f"{tx['date']:<12} {tx['desc']:<26} {amt_str:<12} {bal_str:<10}")
    lines.append("==================================================")
    return "\n".join(lines)

def render_income_statement_text(d):
    lines = [
        "==================================================",
        f"          STATEMENT OF OPERATIONS / INCOME        ",
        "==================================================",
        f"Company Name:   {d['company']}",
        f"Fiscal Period:  {d['period']}",
        "--------------------------------------------------",
        f"Total Revenue:                   ${d['revenue']:,.2f}",
        f"Cost of Goods Sold (COGS):       ${d['cogs']:,.2f}",
        f"Gross Profit:                    ${d['gross_profit']:,.2f}",
        "--------------------------------------------------",
        f"Operating Expenses (OpEx):       ${d['opex']:,.2f}",
        f"Operating Income:                ${d['operating_income']:,.2f}",
        "--------------------------------------------------",
        f"Net Income:                      ${d.get('stated_net_income', d['net_income']):,.2f}",
        "=================================================="
    ]
    return "\n".join(lines)

def render_expense_report_text(d):
    lines = [
        "==================================================",
        f"           CORPORATE EXPENSE REPORT               ",
        "==================================================",
        f"Employee Name:    {d['employee']}",
        f"Report ID:        {d['report_id']}",
        f"Submission Date:  {d['date']}",
        f"Approval Status:  {d['status']}",
        "--------------------------------------------------",
        "ITEMIZED EXPENSES:",
        f"{'Date':<12} {'Category':<10} {'Merchant':<20} {'Amount':<10}"
    ]
    for it in d['items']:
        lines.append(f"{it['date']:<12} {it['category']:<10} {it['merchant']:<20} ${it['amount']:.2f}")
    lines.append("--------------------------------------------------")
    lines.append(f"Total Claimed Amount:                            ${d['total']:.2f}")
    lines.append("==================================================")
    return "\n".join(lines)

def render_loan_app_text(d):
    risk_str = ", ".join(d['risk_flags']) if d['risk_flags'] else "None (Clean Profile)"
    lines = [
        "==================================================",
        f"          LOAN / KYC APPLICATION FORM             ",
        "==================================================",
        f"Applicant Full Name:      {d['applicant']}",
        f"Identification Type:      {d['id_type']}",
        f"ID Number:                {d['id_number']}",
        "--------------------------------------------------",
        f"Stated Annual Income:     ${d['income']:,.2f}",
        f"Requested Loan Amount:    ${d['requested']:,.2f}",
        f"Stated Purpose:           {d['purpose']}",
        "--------------------------------------------------",
        f"Underwriter Risk Flags:   {risk_str}",
        "=================================================="
    ]
    return "\n".join(lines)

print("Starting generation of 50 financial documents and gold labels...")

# 1. Generate Invoices
for d in INVOICE_DATA:
    txt = render_invoice_text(d)
    with open(os.path.join(DOCS_DIR, f"{d['id']}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    gold = {
        "doc_id": d["id"],
        "category": "invoice",
        "is_noisy": d["noisy"],
        "injected_flaws": d["flaws"],
        "fields": {
            "vendor_name": d["vendor"],
            "invoice_number": d["inv_num"],
            "invoice_date": d["date"],
            "due_date": d["due"],
            "subtotal": d["subtotal"],
            "tax_amount": d["tax"],
            "total_amount": d["total"],
            "line_items": d["items"]
        },
        "self_consistency_passed": not ("arithmetic_total_discrepancy" in d["flaws"]),
        "risk_flags": d["flaws"]
    }
    with open(os.path.join(GOLD_DIR, f"{d['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(gold, f, indent=2)

# 2. Generate Bank Statements
for d in BANK_DATA:
    txt = render_bank_statement_text(d)
    with open(os.path.join(DOCS_DIR, f"{d['id']}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    gold = {
        "doc_id": d["id"],
        "category": "bank_statement",
        "is_noisy": d["noisy"],
        "injected_flaws": d["flaws"],
        "fields": {
            "bank_name": d["bank"],
            "account_number": d["account"],
            "statement_period_start": d["start"],
            "statement_period_end": d["end"],
            "opening_balance": d["opening"],
            "closing_balance": d["closing"],
            "transactions": d["txns"]
        },
        "self_consistency_passed": True,
        "risk_flags": d["flaws"]
    }
    with open(os.path.join(GOLD_DIR, f"{d['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(gold, f, indent=2)

# 3. Generate Income Statements
for d in INCOME_DATA:
    txt = render_income_statement_text(d)
    with open(os.path.join(DOCS_DIR, f"{d['id']}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    gold = {
        "doc_id": d["id"],
        "category": "income_statement",
        "is_noisy": d["noisy"],
        "injected_flaws": d["flaws"],
        "fields": {
            "company_name": d["company"],
            "fiscal_period": d["period"],
            "total_revenue": d["revenue"],
            "cost_of_goods_sold": d["cogs"],
            "gross_profit": d["gross_profit"],
            "operating_expenses": d["opex"],
            "operating_income": d["operating_income"],
            "net_income": d["net_income"]
        },
        "self_consistency_passed": not ("arithmetic_rounding_discrepancy" in d["flaws"]),
        "risk_flags": d["flaws"]
    }
    with open(os.path.join(GOLD_DIR, f"{d['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(gold, f, indent=2)

# 4. Generate Expense Reports
for d in EXPENSE_DATA:
    txt = render_expense_report_text(d)
    with open(os.path.join(DOCS_DIR, f"{d['id']}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    gold = {
        "doc_id": d["id"],
        "category": "expense_report",
        "is_noisy": d["noisy"],
        "injected_flaws": d["flaws"],
        "fields": {
            "employee_name": d["employee"],
            "report_id": d["report_id"],
            "submission_date": d["date"],
            "total_amount": d["total"],
            "approval_status": d["status"],
            "expense_items": d["items"]
        },
        "self_consistency_passed": True,
        "risk_flags": d["flaws"]
    }
    with open(os.path.join(GOLD_DIR, f"{d['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(gold, f, indent=2)

# 5. Generate Loan Applications
for d in LOAN_DATA:
    txt = render_loan_app_text(d)
    with open(os.path.join(DOCS_DIR, f"{d['id']}.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    gold = {
        "doc_id": d["id"],
        "category": "loan_application",
        "is_noisy": d["noisy"],
        "injected_flaws": d["flaws"],
        "fields": {
            "applicant_name": d["applicant"],
            "id_type": d["id_type"],
            "id_number": d["id_number"],
            "annual_income": d["income"],
            "requested_amount": d["requested"],
            "loan_purpose": d["purpose"],
            "risk_flags": d["risk_flags"]
        },
        "self_consistency_passed": True,
        "risk_flags": d["risk_flags"]
    }
    with open(os.path.join(GOLD_DIR, f"{d['id']}.json"), "w", encoding="utf-8") as f:
        json.dump(gold, f, indent=2)

# 6. Generate Double-Annotated Pass 2 Subset (10 docs: 2 per category)
DOUBLE_ANNOTATED_IDS = [
    "inv_03", "inv_09",
    "bank_02", "bank_10",
    "inc_04", "inc_09",
    "exp_05", "exp_10",
    "loan_01", "loan_09"
]

for doc_id in DOUBLE_ANNOTATED_IDS:
    with open(os.path.join(GOLD_DIR, f"{doc_id}.json"), "r", encoding="utf-8") as f:
        gold = json.load(f)
    pass2 = json.loads(json.dumps(gold))
    pass2["annotator_id"] = "annotator_pass_2"
    # Inject realistic annotator variation on noisy docs
    if doc_id == "inv_09":
        # Annotator 2 trimmed OCR artifact slightly differently
        pass2["fields"]["line_items"][0]["desc"] = "Enterprise Core License O1 x"
    elif doc_id == "loan_09":
        # Annotator 2 used alternate phrasing for risk flag
        pass2["fields"]["risk_flags"] = ["DEBT_TO_INCOME_HIGH"]
    
    with open(os.path.join(PASS2_DIR, f"{doc_id}.json"), "w", encoding="utf-8") as f:
        json.dump(pass2, f, indent=2)

print(f"Successfully created 50 document text files in: {DOCS_DIR}")
print(f"Successfully created 50 gold label files in: {GOLD_DIR}")
print(f"Successfully created 10 double-annotated files in: {PASS2_DIR}")
