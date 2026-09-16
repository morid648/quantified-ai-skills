# 🧪 Real-World Examples ("Quantified Skills Cookbook")

> **Step-by-step recipes demonstrating how to chain the 11 Quantified AI Skills to solve complex document extraction, context optimization, and model evaluation challenges.**

---

## 🥘 Recipe 1: Production Financial Invoice & Statement Ingestion

**Scenario**: You need to process incoming enterprise financial invoices and bank statements, extract key line items into strict JSON schemas, and flag arithmetic or OCR anomalies.

**Skills Used**:
1. [`document-context-chunking`](../skills/document-context-chunking/) (Preserve tabular financial data without column degradation)
2. [`extraction-prompt-library-finance`](../skills/extraction-prompt-library-finance/) (Execute zero-shot 5-category extraction with confidence scoring)
3. [`prompt-scorecard-testing`](../skills/prompt-scorecard-testing/) (Grade extraction accuracy against schema requirements)

### Workflow Steps

1. **Chunk & Format**:
   > *"Agent, use `document-context-chunking` on `benchmarks/finance-50doc-v1/documents/bank_09.txt` to isolate the transaction ledger into clean tabular blocks."*

2. **Extract with Confidence Ratings**:
   > *"Apply `extraction-prompt-library-finance` to extract `account_number`, `opening_balance`, `closing_balance`, `total_debits`, `total_credits`, and `transaction_count`. Assign confidence scores to all fields and flag any OCR artifacts."*

3. **Verify Discrepancies**:
   The skill detects character substitutions (e.g. OCR letter `'O'` in account number `"7710-9941-O8"`) and assigns a lower confidence rating ($0.65$), categorizing it as `LOW_CONFIDENCE_CORRECTLY_FLAGGED` for human review.

---

## 🥘 Recipe 2: Context Window Budgeting for Massive Filings

**Scenario**: You have 10-K filings and lengthy income statements (3,500+ tokens) that need to fit into a tight LLM prompt budget (under 2,700 tokens) without losing critical financial facts.

**Skills Used**:
1. [`document-context-chunking`](../skills/document-context-chunking/) (Semantic partitioning with header/footnote isolation)
2. [`context-budget-allocator`](../skills/context-budget-allocator/) (Apply keep/summarize/drop priority budgeting)

### Workflow Steps

1. **Partition Long Filings**:
   > *"Agent, run `document-context-chunking` on `benchmarks/finance-50doc-v1/documents/inc_01.txt` to separate revenue tables, operating expense lines, and narrative management notes."*

2. **Allocate Budget**:
   > *"Use `context-budget-allocator` to compress the document into a 2,700 token budget. Keep core balance tables verbatim, summarize footnotes, and drop boilerplate disclosures."*

3. **Validate Retention**:
   The allocator outputs a **24.33% Token Compression Ratio** (reducing tokens from 3,526 down to 2,668) while achieving **100.0% Factual Retention** (20/20 probe facts preserved).

---

## 🥘 Recipe 3: Model Upgrade & Statistical Regression Certification

**Scenario**: You are evaluating a new fine-tuned model or updated prompt template against your production baseline. You need statistical proof that accuracy has not regressed before deploying to production.

**Skills Used**:
1. [`eval-harness-builder`](../skills/eval-harness-builder/) (Run automated golden-set grading across 50 benchmark documents)
2. [`annotation-qa-scoring`](../skills/annotation-qa-scoring/) (Calculate Cohen's Kappa agreement on double-annotated subset)
3. [`regression-benchmark-tracker`](../skills/regression-benchmark-tracker/) (Run two-proportion $z$-test against baseline)

### Workflow Steps

1. **Execute Golden Set Grading**:
   > *"Agent, use `eval-harness-builder` to score predictions from `candidate_run.json` against `benchmarks/finance-50doc-v1/gold_labels/`."*

2. **Inter-Annotator QA**:
   > *"Run `annotation-qa-scoring` to compute Cohen's Kappa on the 10-document double-annotated validation set."*

3. **Statistical Regression Test**:
   > *"Run `regression-benchmark-tracker` to compare candidate performance against `benchmarks/finance-50doc-v1/baseline_run.json`."*

4. **CI Verdict**:
   If the candidate achieves $z \ge -1.96$ ($p \ge 0.05$), the benchmark passes and updates the baseline. If $z < -1.96$, CI fails and outputs the specific fields that regressed.
