# 📜 Sources, References & Attributions

> **Formal academic citations, industry standards, and architectural attributions underpinning the Quantified AI Skills portfolio and evaluation framework.**

---

## 1. Mathematical & Statistical Foundations

The evaluation harnesses and statistical tracking skills implement established peer-reviewed mathematical methodologies:

| Concept / Metric | Academic Source | Application in Repository |
|---|---|---|
| **Inter-Annotator Agreement (Cohen's Kappa $\kappa$)** | Cohen, Jacob. (1960). *"A Coefficient of Agreement for Nominal Scales."* Educational and Psychological Measurement, 20(1), 37–46. | Implemented in [`skills/annotation-qa-scoring`](../skills/annotation-qa-scoring/) for double-annotated QA verification. |
| **Multi-Rater Agreement (Fleiss' Kappa)** | Fleiss, Joseph L. (1971). *"Measuring nominal scale agreement among many raters."* Psychological Bulletin, 76(5), 378–382. | Formula reference for multi-agent consensus grading. |
| **Two-Proportion Hypothesis Testing ($z$-score)** | Snedecor, G. W., & Cochran, W. G. (1989). *Statistical Methods* (8th ed.). Iowa State University Press. | Implemented in [`skills/regression-benchmark-tracker`](../skills/regression-benchmark-tracker/) for CI/CD regression detection. |
| **Context Compression & Probe Retention** | Liu, N. F., et al. (2023). *"Lost in the Middle: How Language Models Use Long Contexts."* Transactions of the Association for Computational Linguistics. | Context chunking and factual probe verification in [`skills/document-context-chunking`](../skills/document-context-chunking/). |

---

## 2. Financial & Industry Standards

The 5 financial document categories and extraction schemas are modeled after standard accounting practices:

| Document Type | Standard / Reference Format | Extracted Fields |
|---|---|---|
| **Commercial Invoices** | UN/CEFACT Cross-Industry Invoice (CII) & UBL 2.1 | Vendor Name, Invoice Number, Invoice Date, Due Date, Line Items (Qty, Unit Price, Amount), Subtotal, Tax, Total |
| **Bank Statements** | OFX / CAMT.053 ISO 20022 Financial Services Standard | Account Number, Statement Period, Opening Balance, Closing Balance, Total Debits, Total Credits, Transactions |
| **Income Statements** | GAAP / IFRS Standard Multi-Step Income Statement | Revenue, Cost of Goods Sold (COGS), Gross Profit, Operating Expenses (R&D, SG&A), Operating Income, Tax, Net Income |
| **Corporate Expense Reports** | Standard Corporate Travel & Expense (T&E) Policy | Employee Name, Report ID, Submission Date, Expense Items (Category, Amount, Date), Total Amount, Approval Status |
| **Loan / KYC Applications** | Fannie Mae Form 1003 / Uniform Residential Loan Application | Applicant Name, Government ID Type/Number, Stated Annual Income, Requested Loan Amount, Loan Purpose, Risk Flags |

---

## 3. Evaluation & Governance Standards

- **NIST AI Risk Management Framework (AI RMF 1.0)**: Guidelines for measuring AI model validity, reliability, safety, and accountability.
- **ISO/IEC 25010**: Software engineering product quality measurement standards.

---

## 4. Authorship & Project Attribution

The **Quantified AI Skills Portfolio** was designed and implemented by **Anshul** as an independent production-grade demonstration of agentic evaluation systems, context optimization, prompt scorecards, and financial document extraction.
