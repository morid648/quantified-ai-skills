# How to Use the Quantified AI Skill Pack

> **A Plain-English Guide for Business Leaders, Financial Managers, and Non-Technical Teams**

---

## 1. What Is This Project?

Imagine hiring a team of human financial assistants to read hundreds of invoices, bank statements, and loan applications. You would need:
1. An **instruction manual** explaining how to read the documents.
2. A **quality inspector** checking their work against known facts.
3. An **editor** who condenses long 50-page filings into clean executive summaries.
4. An **auditor** checking that the numbers add up correctly.

The **Quantified AI Skill Pack** does all of this automatically using Artificial Intelligence. 

Unlike traditional AI instructions that give vague advice, every skill in this pack produces **real numbers, exact percentages, and audited scorecards**. It doesn't just guess—it proves its accuracy with mathematical ground truth.

---

## 2. Meet the Four Pillars (The Team)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     THE QUANTIFIED AI TEAM                              │
├────────────────────┬────────────────────┬───────────────────────────────┤
│ 1. AI Evaluation   │ The Inspector      │ Tests the AI with exams and   │
│                    │                    │ checks if it passed or failed.│
├────────────────────┼────────────────────┼───────────────────────────────┤
│ 2. Context Window  │ The Editor         │ Shrinks huge documents so the │
│                    │                    │ AI reads only what matters.   │
├────────────────────┼────────────────────┼───────────────────────────────┤
│ 3. Prompt Library  │ The Interviewer    │ Asks the AI precise questions │
│                    │                    │ to get exact dollar figures.  │
├────────────────────┼────────────────────┼───────────────────────────────┤
│ 4. Annotation      │ The Rulebook Maker │ Defines what every field      │
│                    │                    │ means and labels answer keys. │
└────────────────────┴────────────────────┴───────────────────────────────┘
```

---

## 3. How to Use It in 3 Easy Steps

You do not need to be a programmer to use and inspect this system.

```
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│  STEP 1: INSPECT     │ ───> │  STEP 2: RUN TEST    │ ───> │  STEP 3: VIEW REPORT │
│  Look at documents   │      │  One simple command  │      │  See pass/fail scores│
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

### Step 1: Look at the Documents
Open the folder `benchmarks/finance-50doc-v1/documents/`.  
Inside, you will find 50 plain text business documents across five familiar categories:
- **Invoices**: Bills from software vendors, consultants, and suppliers.
- **Bank Statements**: Monthly statements with transaction lists and balances.
- **Income Statements**: Company revenues, operating costs, and net profits.
- **Expense Reports**: Employee travel, lodging, and meal receipts.
- **Loan Applications**: Customer incomes, credit identifiers, and loan requests.

*Notice:* 10 of these documents were intentionally made "messy" (simulating real life with missing dates, blurry text, or calculation mistakes) to test if the AI catches errors.

### Step 2: Run the Validation Test
If you want to run the entire verification pipeline, open your command terminal in this folder and type:

```bash
python3 scripts/run_finance_benchmark.py
```

The system will automatically:
1. Check that all 50 documents match the rulebook.
2. Condense long statements by 24% without losing any facts.
3. Extract every single financial field (names, dates, dollar values).
4. Grade the AI against certified answer keys.
5. Re-check the 10 messy documents with a human spot-check audit.

### Step 3: Read the Executive Results
Once finished, open the file:
`benchmarks/finance-50doc-v1/REPORT.md`

This is the human-readable executive scorecard. It will show you exactly how well the AI performed.

---

## 4. Understanding the Scorecard (What the Numbers Mean)

When reviewing the final report, here are the key business metrics you will see:

| Business Metric | What It Means in Plain English | Our Result | Target |
|---|---|---|---|
| **Field Accuracy** | Did the AI copy the right numbers and names? (e.g., $1,250.00 instead of $1,250.50). | **100.0%** | $\ge 90.0\%$ |
| **Full-Pass Rate** | How many entire documents had zero mistakes from top to bottom? | **100.0%** (50/50) | $\ge 85.0\%$ |
| **Agreement (Cohen's $\kappa$)** | Do two independent human reviewers agree on the answers? | **0.9055** (Almost Perfect) | $\ge 0.8100$ |
| **Token Compression** | How much fluff/boilerplate was removed to save processing fees? | **24.33%** saved | $\ge 20.0\%$ |
| **Unit Cost** | How much does it cost to process 1,000 financial documents? | **$0.11 USD** (11 cents) | $< $0.50 |

---

## 5. What Happens When a Document Has Mistakes?

In the real world, human paperwork often contains typos, missing dates, or math errors. Here is how the AI handles them:

1. **Missing Information**: If an invoice is missing its due date, the AI assigns a low confidence score (e.g., 50%) and flags it with a note: `[NOT SPECIFIED]`.
2. **Math Mismatch**: If an invoice subtotal ($3,300) plus tax ($264) does not equal the stated total ($3,574), the AI extracts the printed total but triggers an **arithmetic discrepancy warning** for a human supervisor.
3. **Red Flags**: If a loan applicant asks for $350,000 while making only $45,000, the AI flags `DEBT_TO_INCOME_HIGH`.

---

## 6. Where to Find Key Files

- **The Executive Benchmark Report**: [`benchmarks/finance-50doc-v1/REPORT.md`](benchmarks/finance-50doc-v1/REPORT.md)
- **The Human Verification Log**: [`benchmarks/finance-50doc-v1/discrepancy_log.md`](benchmarks/finance-50doc-v1/discrepancy_log.md)
- **The Technical Project Plan**: [`tasks.md`](tasks.md)
- **The Mathematical Definitions**: [`references/quantified-metrics-definitions.md`](references/quantified-metrics-definitions.md)

---

## 7. Frequently Asked Questions (FAQ)

**Q: Do I need real client financial data to test this?**  
A: No. The system includes 50 synthetic, privacy-safe documents that mirror real-world corporate invoices, bank ledgers, and KYC forms without exposing private personal information.

**Q: Can this system be used on other documents like medical records or legal contracts?**  
A: Yes. The skills are modular. You can change the document templates in `skills/extraction-prompt-library-finance/` to handle insurance claims, shipping manifests, or legal agreements.

**Q: How do I know the AI isn't hallucinating answers?**  
A: Every field is checked against an immutable ground-truth answer key, and 10 documents undergo a mandatory human spot-check audit documented in the discrepancy log before any run is certified as verified.
