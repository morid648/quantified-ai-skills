---
name: finance-document-annotator
description: Annotation schemas and procedures for tagging financial documents to produce gold labels, enforcing arithmetic self-consistency and anomaly flag verification.
risk: safe
source: self
tags: [ai-annotation]
---

# Finance Document Annotator

A specialized domain annotation skill defining schemas, tagging protocols, and mathematical validation rules for generating gold-standard labels across five financial document categories: Invoices, Bank Statements, Income Statements, Expense Reports, and Loan/KYC Applications.

## When to Use

Use this skill when you need to:
- Create authoritative gold-standard ground truth labels for financial document datasets.
- Tag tabular line items, entities, financial metrics, and transaction ledgers.
- Enforce arithmetic self-consistency validation (e.g. line items sum to subtotal, subtotal + tax = total).
- Tag financial risk flags and document anomalies (e.g. negative balances, OCR artifacts, missing required metadata).

Do NOT use this skill for:
- Authoring high-level annotation guidelines for generic text (use `annotation-guideline-writer`).
- Computing statistical kappa across multiple human annotators (use `annotation-qa-scoring`).

## Annotation Schemas Across 5 Categories

### 1. Invoices (`category: "invoice"`)
- `vendor_name` (string, required): Legal issuing business name.
- `invoice_number` (string, required): Unique identifier code.
- `invoice_date` (string `YYYY-MM-DD`, required): Issuance date.
- `due_date` (string `YYYY-MM-DD`, optional): Payment deadline.
- `line_items` (array of objects, required):
  - `description` (string), `quantity` (float), `unit_price` (float), `amount` (float).
- `subtotal` (float, required): Pre-tax line item sum.
- `tax_amount` (float, required): Explicit tax amount.
- `total_amount` (float, required): Final payable balance.

### 2. Bank Statements (`category: "bank_statement"`)
- `bank_name` (string, required), `account_number` (string, required).
- `statement_period_start` (string `YYYY-MM-DD`), `statement_period_end` (string `YYYY-MM-DD`).
- `opening_balance` (float, required), `closing_balance` (float, required).
- `transactions` (array of objects, required):
  - `date` (`YYYY-MM-DD`), `description` (string), `amount` (float, signed: negative for debits, positive for credits), `balance` (float).

### 3. Income Statements (`category: "income_statement"`)
- `company_name` (string, required), `fiscal_period` (string, required).
- `total_revenue` (float, required), `cost_of_goods_sold` (float, required).
- `gross_profit` (float, required).
- `operating_expenses` (float, required), `operating_income` (float, required).
- `net_income` (float, required).

### 4. Expense Reports (`category: "expense_report"`)
- `employee_name` (string, required), `report_id` (string, required), `submission_date` (`YYYY-MM-DD`).
- `expense_items` (array of objects, required):
  - `date` (`YYYY-MM-DD`), `category` (enum: `MEALS`, `TRAVEL`, `LODGING`, `SOFTWARE`, `SUPPLIES`), `merchant` (string), `amount` (float).
- `total_amount` (float, required), `approval_status` (enum: `APPROVED`, `PENDING`, `REJECTED`).

### 5. Loan / KYC Applications (`category: "loan_application"`)
- `applicant_name` (string, required), `id_type` (enum: `SSN`, `PASSPORT`, `TAX_ID`), `id_number` (string, required).
- `annual_income` (float, required), `requested_amount` (float, required), `loan_purpose` (string).
- `risk_flags` (array of strings): Tags such as `DEBT_TO_INCOME_HIGH`, `MISSING_PROOF_OF_INCOME`, `INCONSISTENT_ADDRESS`.

## Mathematical Self-Consistency Verification

Every generated gold label must pass deterministic arithmetic validation before acceptance:

1. **Invoice Balance Check**:
   $$|\text{Subtotal} - \sum \text{LineItem amounts}| \le 0.01$$
   $$|(\text{Subtotal} + \text{Tax}) - \text{Total Amount}| \le 0.01$$
2. **Statement Balance Check**:
   $$|\text{Opening Balance} + \sum \text{Transactions} - \text{Closing Balance}| \le 0.01$$
3. **Income Statement Check**:
   $$|\text{Total Revenue} - \text{COGS} - \text{Gross Profit}| \le 0.01$$
   $$|\text{Operating Income} - (\text{Gross Profit} - \text{OpEx})| \le 0.01$$

$$\text{Self-Consistency Pass Rate (\%)} = \left( \frac{N_{\text{passed arithmetic checks}}}{N_{\text{total arithmetic checks}}} \right) \times 100$$

## Examples

### Example: Labeled Gold-Standard Invoice Entry

```json
{
  "doc_id": "inv_01",
  "category": "invoice",
  "is_noisy": false,
  "fields": {
    "vendor_name": "Apex Cloud Systems Inc",
    "invoice_number": "INV-2024-8831",
    "invoice_date": "2024-03-15",
    "due_date": "2024-04-15",
    "subtotal": 12500.00,
    "tax_amount": 1000.00,
    "total_amount": 13500.00,
    "line_items": [
      { "description": "Cloud Hosting Enterprise", "quantity": 1.0, "unit_price": 10000.00, "amount": 10000.00 },
      { "description": "Dedicated Support SLA", "quantity": 1.0, "unit_price": 2500.00, "amount": 2500.00 }
    ]
  },
  "self_consistency_passed": true,
  "risk_flags": []
}
```

## Limitations

- **Not an OCR reader**: Tags digital representation of documents; image-based OCR pre-processing is required upstream.
- **Jurisdiction differences**: Tax calculation formulas (VAT vs Sales Tax vs GST) differ; annotator records the document's explicit stated figures rather than re-computing municipal tax rates.

## Quantified Output

Every dataset annotation pass must emit a quantified quality audit:

### Worked Numeric Example (50 Finance Documents Labeling Run)

- Total documents labeled: $50$ (10 per category).
- Total discrete fields tagged: $412$ fields across all documents.
- Mathematical self-consistency equations tested: $90$ balance equations (invoices, statements, income statements, expense reports).
- Equations passed: $88$. ($2$ failed due to deliberate noisy document injections having arithmetic errors in the source document).
- Consistency Pass Rate: $(88 / 90) \times 100 = 97.78\%$.
- Injected anomalies and risk flags correctly labeled: $14$ flags across $10$ noisy docs.

### Machine-Readable Result Block

```json
{
  "skill_name": "finance-document-annotator",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 50,
  "status": "pass",
  "metrics": {
    "documents_annotated_count": 50,
    "total_fields_tagged": 412,
    "self_consistency_pass_rate_pct": 97.78,
    "consistency_checks_passed": 88,
    "consistency_checks_total": 90,
    "anomalies_flagged_count": 14
  },
  "metadata": {
    "categories": ["invoice", "bank_statement", "income_statement", "expense_report", "loan_application"],
    "clean_doc_count": 40,
    "noisy_doc_count": 10
  }
}
```
