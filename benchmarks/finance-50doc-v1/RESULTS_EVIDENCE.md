# Results Evidence: Real LLM Extraction, Not Simulation

This document exists to make the [aggregate numbers in REPORT.md](REPORT.md) independently verifiable, not just asserted. Every claim below links directly to the actual raw files committed in this repo — the source document text, the model's raw JSON response, the gold label, and the grader's field-by-field comparison — so you can check the evidence yourself rather than trust a summary table.

**How to verify any of this yourself, in one command:**

```bash
GROQ_API_KEY=<your-key> python scripts/run_finance_benchmark.py
```

This re-runs all 50 documents against a live Groq API call (`openai/gpt-oss-120b`) and regenerates every file referenced below from scratch. Nothing here is hand-edited or precomputed outside that script.

---

## Raw evidence files (the actual proof)

| What | Where | Count |
|---|---|---|
| Source documents (what the model actually reads) | [`documents/`](documents/) | 50 `.txt` files |
| Ground truth | [`gold_labels/`](gold_labels/) | 50 `.json` files |
| **Raw model output** — every field, every value, every confidence score, real token counts, real latency, tagged `"model": "openai/gpt-oss-120b"` | [`extractions/`](extractions/) | 50 `_extracted.json` files |
| Grader's field-by-field verdict | [`per_doc_eval/`](per_doc_eval/) | 50 `_eval.json` files |
| Aggregated scorecard (computed from the above, not typed by hand) | [`aggregated_scorecard.json`](aggregated_scorecard.json) | 1 file |

Every `extractions/*_extracted.json` file carries the model name, real `in_tokens`/`out_tokens` (straight from the API's own `usage` metadata), and real `latency_ms` (measured wall-clock time of that specific API call, retries excluded). Anyone can open any of the 50 and see this directly.

---

## Example 1 — Clean success

**Source:** [`documents/inv_01.txt`](documents/inv_01.txt)

```
Vendor Name:  Apex Cloud Systems Inc
Invoice No:   INV-2024-1001
Invoice Date: 2024-01-15
Payment Due Date: 2024-02-15
--------------------------------------------------
LINE ITEMS:
Description                      Qty    Unit Price   Amount
Kubernetes Cluster Hosting       1.0    $4500.00     $4500.00
High-Throughput Storage (TB)     10.0   $120.00      $1200.00
24/7 SRE Enterprise SLA          1.0    $1800.00     $1800.00
--------------------------------------------------
Subtotal:                                       $7500.00
Sales / Service Tax:                            $600.00
Total Amount Due:                               $8100.00
```

**Raw model output** ([`extractions/inv_01_extracted.json`](extractions/inv_01_extracted.json)): 823ms latency, 699 input / 295 output tokens, every field extracted with 0.99 confidence, including all 3 line items broken out correctly with the exact `desc`/`qty`/`unit`/`amt` keys the grader expects.

**Grader verdict** ([`per_doc_eval/inv_01_eval.json`](per_doc_eval/inv_01_eval.json)): 8/8 fields correct, `doc_passed: true`.

---

## Example 2 — Noisy input, correctly handled (including appropriate uncertainty)

**Source:** [`documents/inv_09.txt`](documents/inv_09.txt) — this one has two deliberately injected real-world defects (per [`gold_labels/inv_09.json`](gold_labels/inv_09.json)'s `injected_flaws`): a missing due date (`"Payment Due Date: [NOT SPECIFIED / IMMEDIATE]"`) and OCR noise in a line item description (`"Enterprise Core License O1 x (OCR Noise)"`).

**Raw model output** ([`extractions/inv_09_extracted.json`](extractions/inv_09_extracted.json)):
- `due_date` extracted as `null`, correctly matching gold — **and** the model scored this field only **0.50 confidence**, correctly below the 0.70 low-confidence threshold, because the source genuinely doesn't state one.
- The OCR-garbled line item description was copied through verbatim (`"Enterprise Core License O1 x (OCR Noise)"`) rather than "corrected" — matching gold exactly, since gold also preserves the noise as-is.
- Every other field: 0.99 confidence, all correct.

**Grader verdict** ([`per_doc_eval/inv_09_eval.json`](per_doc_eval/inv_09_eval.json)): 8/8 fields correct, including the low-confidence `due_date` — `low_confidence_flagged: true` and `matched: true` simultaneously. This is exactly the behavior the `extraction-prompt-library-finance` skill's confidence protocol is designed to produce: appropriate self-doubt on a genuinely ambiguous field, without that doubt meaning the answer is wrong.

---

## Example 3 & 4 — The two real failures, in full

Both of this benchmark's 2 field-level misses (out of 360) are the same failure mode on the same field: `fiscal_period`.

### `inc_01` (clean document, no injected noise)

**Source:** [`documents/inc_01.txt`](documents/inc_01.txt) — states `Fiscal Period:  Q1 2024` in plain text, nothing ambiguous about it.

| Field | Extracted ([full file](extractions/inc_01_extracted.json)) | Gold ([full file](gold_labels/inc_01.json)) | Match |
|---|---|---|---|
| `company_name` | `"Northstar Logistics Corp"` | `"Northstar Logistics Corp"` | ✅ |
| `fiscal_period` | **`"2024-03-31"`** | **`"Q1 2024"`** | ❌ (confidence: 0.98) |
| `total_revenue` | `1250000.0` | `1250000.0` | ✅ |
| `cost_of_goods_sold` | `650000.0` | `650000.0` | ✅ |
| `gross_profit` | `600000.0` | `600000.0` | ✅ |
| `operating_expenses` | `380000.0` | `380000.0` | ✅ |
| `operating_income` | `220000.0` | `220000.0` | ✅ |
| `net_income` | `176000.0` | `176000.0` | ✅ |

Every dollar figure is exact. The model read the document correctly and did the extraction correctly — it just silently reformatted `"Q1 2024"` into what looks like a calendar date, at **0.98 confidence**, as if that were a normalization rather than a substitution.

### `inc_10` (noisy document — different injected flaw, same fiscal_period bug)

**Source:** [`documents/inc_10.txt`](documents/inc_10.txt) — also states `Fiscal Period:  Q1 2024` plainly. This document's actual injected flaw ([`gold_labels/inc_10.json`](gold_labels/inc_10.json)) is `arithmetic_rounding_discrepancy` on `net_income` — a different trap entirely, which the model **passed** (extracted `371000.0`, exactly matching gold, at 0.99 confidence — see [`extractions/inc_10_extracted.json`](extractions/inc_10_extracted.json)).

`fiscal_period` extracted as **`"2024-Q1"`** (a different wrong reformatting than `inc_01`'s, but the same underlying bug) vs. gold's `"Q1 2024"`, at **0.95 confidence**.

### Why this matters more than "2 fields out of 360"

The root cause is identifiable and fixable: the extraction prompt instructs "Dates in ISO-8601 (YYYY-MM-DD)" as a general rule, and the model over-applies that instinct to a field that isn't a date at all — it's a quarter label. That's a real, specific prompt-engineering gap in `extraction-prompt-library-finance`'s category schema (it doesn't currently carve out `fiscal_period` as an explicitly non-date string).

The more interesting result is the **confidence miscalibration**: both wrong answers came with high confidence (0.98, 0.95) — well above the 0.70 flagging threshold — while two separate, genuinely uncertain fields elsewhere in this same 50-document run (`inv_09`'s `due_date` at 0.50, above) were correctly flagged low-confidence and still right. In other words: this model's confidence score reliably signals "the source is ambiguous," but not "I might be systematically wrong about a formatting convention I'm sure I understand." That's a real finding about this specific model on this specific field type — the kind of thing that only shows up when you actually run a live model against real documents, which is exactly why this benchmark was rebuilt to stop simulating that step.

---

## Full manifest — all 50 documents, pass/fail, with links to raw evidence

| Doc ID | Category | Noisy | Fields | Passed | Raw extraction | Raw eval |
|---|---|---|---|---|---|---|
| `inv_01`–`inv_08`, `inv_10` | invoice | mixed | 8/8 each | ✅ | [`extractions/`](extractions/) | [`per_doc_eval/`](per_doc_eval/) |
| `inv_09` | invoice | yes | 8/8 | ✅ | [inv_09_extracted.json](extractions/inv_09_extracted.json) | [inv_09_eval.json](per_doc_eval/inv_09_eval.json) |
| `bank_01`–`bank_10` | bank_statement | mixed | 7/7 each | ✅ | [`extractions/`](extractions/) | [`per_doc_eval/`](per_doc_eval/) |
| `exp_01`–`exp_10` | expense_report | mixed | 6/6 each | ✅ | [`extractions/`](extractions/) | [`per_doc_eval/`](per_doc_eval/) |
| `loan_01`–`loan_10` | loan_application | mixed | 7/7 each | ✅ | [`extractions/`](extractions/) | [`per_doc_eval/`](per_doc_eval/) |
| `inc_01` | income_statement | no | 7/8 | ❌ `fiscal_period` | [inc_01_extracted.json](extractions/inc_01_extracted.json) | [inc_01_eval.json](per_doc_eval/inc_01_eval.json) |
| `inc_02`–`inc_09` | income_statement | mixed | 8/8 each | ✅ | [`extractions/`](extractions/) | [`per_doc_eval/`](per_doc_eval/) |
| `inc_10` | income_statement | yes | 7/8 | ❌ `fiscal_period` | [inc_10_extracted.json](extractions/inc_10_extracted.json) | [inc_10_eval.json](per_doc_eval/inc_10_eval.json) |

50/50 documents extracted successfully (0 API failures in this run). 48/50 fully passed. The 2 that didn't are documented above in full, not glossed over.

---

## What this document is not

This is evidence for the *extraction step* being real, not a formal re-certification of the benchmark. See [REPORT.md §5](REPORT.md#5-independent-human-verification--certification) and [`run_manifest.json`](run_manifest.json)'s `superseded_by` note for the honest scope of what the original 10-document human spot-check audit does and doesn't cover for this run.
