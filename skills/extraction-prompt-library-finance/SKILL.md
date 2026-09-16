---
name: extraction-prompt-library-finance
description: Production prompt templates and JSON schemas for extracting structured fields from 5 financial document categories with mandatory field-level confidence scores.
risk: safe
source: self
tags: [prompt-engineering]
---

# Extraction Prompt Library (Finance)

A production-tuned library of structured extraction prompt templates covering five core financial document categories: Invoices, Bank Statements, Income Statements, Expense Reports, and Loan/KYC Applications. Enforces strict JSON output schemas with mandatory field-level confidence scores and low-confidence anomaly flags.

## When to Use

Use this skill when you need to:
- Extract structured entities and numeric tables from financial documents.
- Require the model to emit a calibrated confidence score ($0.0 \dots 1.0$) for every extracted field.
- Automatically flag low-confidence or ambiguous fields for human auditor triage.
- Standardize output schemas across different document vendors and formats.

Do NOT use this skill for:
- Splitting long documents before extraction (use `document-context-chunking`).
- Comparing multiple prompt variations to choose a winner (use `prompt-scorecard-testing`).

## Supported Financial Document Categories

The prompt library specifies standardized schemas for five document types:

1. **Invoices**: `vendor_name`, `invoice_number`, `invoice_date`, `due_date`, `line_items` (`description`, `quantity`, `unit_price`, `amount`), `subtotal`, `tax_amount`, `total_amount`.
2. **Bank Statements**: `bank_name`, `account_number`, `statement_period_start`, `statement_period_end`, `opening_balance`, `closing_balance`, `transactions` (`date`, `description`, `amount`, `balance`).
3. **Income Statements**: `company_name`, `fiscal_period`, `total_revenue`, `cost_of_goods_sold`, `gross_profit`, `operating_expenses`, `operating_income`, `net_income`.
4. **Expense Reports**: `employee_name`, `report_id`, `submission_date`, `expense_items` (`date`, `category`, `merchant`, `amount`), `total_amount`, `approval_status`.
5. **Loan / KYC Applications**: `applicant_name`, `id_type`, `id_number`, `annual_income`, `requested_amount`, `loan_purpose`, `risk_flags`.

## Prompt Architecture & Confidence Protocol

Every prompt template adheres to a standardized instruction pattern:
- **Strict Role & Domain Definition**: Explicit instruction to act as a certified financial data auditor.
- **Normalization Mandate**: ISO-8601 for dates (`YYYY-MM-DD`), numeric floats without currency symbols or commas.
- **Field-Level Confidence Score**: Every extracted property must be returned as an object containing `value` and `confidence` ($0.0 \dots 1.0$).
- **Low-Confidence Tripping**: Any field where text is smudged, ambiguous, or missing must be assigned confidence $< 0.70$ and annotated with an explanation in `extraction_notes`.

## Examples

### Example: Invoice Extraction Prompt Template

```markdown
You are an expert financial document extraction engine. Extract the structured invoice fields from the text below.
Format your output strictly as a JSON object adhering to this schema:
{
  "vendor_name": { "value": string, "confidence": float },
  "invoice_number": { "value": string, "confidence": float },
  "invoice_date": { "value": "YYYY-MM-DD", "confidence": float },
  "due_date": { "value": "YYYY-MM-DD", "confidence": float },
  "subtotal": { "value": float, "confidence": float },
  "tax_amount": { "value": float, "confidence": float },
  "total_amount": { "value": float, "confidence": float },
  "line_items": [
    {
      "description": { "value": string, "confidence": float },
      "quantity": { "value": float, "confidence": float },
      "unit_price": { "value": float, "confidence": float },
      "amount": { "value": float, "confidence": float }
    }
  ]
}

Document Content:
{{DOCUMENT_TEXT}}
```

## Limitations

- **Does not execute OCR**: Assumes text or clean markdown is provided as input; cannot process raw scanned image pixels without prior OCR.
- **Provider agnostic**: Designed for chat-completion JSON mode, but actual model adherence to schema depends on the underlying LLM's instruction following ability.

## Quantified Output

Every extraction batch executed using this library must emit a quantified extraction scorecard:

### Worked Numeric Example (50 Finance Documents - 400 Total Fields)

- Total expected fields: $400$.
- Correctly extracted fields: $376$.
- Field-level accuracy: $(376 / 400) \times 100 = 94.0\%$.
- Ambiguous / messy fields in input: $24$ fields.
- Correctly flagged with confidence $< 0.70$: $22$ fields.
- Low-confidence flag precision: $(22 / 24) \times 100 = 91.67\%$.
- Document full-pass count: $43 / 50$ ($86.0\%$).

### Machine-Readable Result Block

```json
{
  "skill_name": "extraction-prompt-library-finance",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 50,
  "status": "pass",
  "metrics": {
    "field_accuracy_pct": 94.0,
    "doc_pass_rate_pct": 86.0,
    "total_fields_evaluated": 400,
    "correct_fields_count": 376,
    "low_confidence_flag_precision_pct": 91.67,
    "low_confidence_flags_raised": 24
  },
  "metadata": {
    "categories_covered": ["invoices", "bank_statements", "income_statements", "expense_reports", "loan_applications"],
    "confidence_threshold": 0.70
  }
}
```
