---
name: training-data-quality-scorer
description: Evaluates candidate training or fine-tuning examples using a 4-dimension rubric (1-5), emitting a 0-100 composite quality score and batch rejection rate.
risk: safe
source: self
tags: [ai-training-eval]
---

# Training Data Quality Scorer

Scores candidate training and fine-tuning examples against a quantitative four-dimensional rubric (Relevance, Correctness, Diversity, Label Consistency). Designed to filter low-quality, noisy, or redundant examples before fine-tuning runs.

## When to Use

Use this skill when you need to:
- Curate, audit, or filter prompt-completion pairs before fine-tuning an LLM.
- Systematically reject noisy, hallucinatory, or ambiguous training candidates.
- Measure batch-level rejection rates and establish data quality gates for training pipelines.
- Quantify training dataset readiness with a reproducible numeric quality score.

Do NOT use this skill for:
- Evaluating general model test outputs (use `eval-harness-builder` instead).
- Comparing prompt variants against benchmark test sets (use `prompt-scorecard-testing`).

## Four-Dimensional Evaluation Rubric

Each candidate training example $(x_i, y_i)$ is evaluated on a 1–5 integer scale across four orthogonal dimensions:

| Dimension | Weight ($w$) | 1 (Unacceptable) | 3 (Adequate) | 5 (Exemplary) |
|---|---|---|---|---|
| **Relevance ($R$)** | 0.30 | Completely off-topic or irrelevant to target task domain. | Broadly related to domain, but includes extraneous context. | Precisely focused on target task instruction and domain inputs. |
| **Correctness ($C$)** | 0.35 | Contains factual errors, severe hallucination, or syntax errors. | Mostly factual; minor rounding discrepancy or formatting drift. | Factual, mathematically verified, 100% compliant with ground truth. |
| **Diversity ($D$)** | 0.15 | Exact duplicate or trivial syntactic variant of another example. | Standard phrasing, typical structural pattern in training set. | Unique edge-case, novel phrasing, rare table/layout variation. |
| **Label Consistency ($L$)** | 0.20 | Violates schema taxonomy, missing mandatory keys or types. | Minor casing or formatting divergence from guideline standard. | 100% compliant with target schema types and normalization rules. |

## Scoring Formula

### Normalized Composite Score (0–100)
Each 1–5 rating is normalized to a $[0, 1]$ interval:
$$S_d = \frac{\text{Rating}_d - 1}{4}$$

The weighted composite score is computed as:
$$\text{Composite Score} = \left( 0.30 \cdot S_R + 0.35 \cdot S_C + 0.15 \cdot S_D + 0.20 \cdot S_L \right) \times 100$$

### Decision Thresholds
- **Tier 1 (Accepted - High Quality)**: $\text{Composite Score} \ge 85$
- **Tier 2 (Accepted with Warning)**: $70 \le \text{Composite Score} < 85$
- **Tier 3 (Rejected)**: $\text{Composite Score} < 70$

### Batch Rejection Rate
$$\text{Batch Rejection Rate (\%)} = \left( \frac{N_{\text{Rejected}}}{N_{\text{Total Candidates}}} \right) \times 100$$

## Examples

### Example: Financial Extraction Candidate Evaluation

**Input Candidate Example:**
```json
{
  "instruction": "Extract the vendor name, invoice date, and total amount due from the invoice text.",
  "input": "INVOICE #94821\nVendor: Northwind Logistics LLC\nDate: 2024-04-15\nBalance Due: $4,850.20",
  "completion": "{\"vendor\": \"Northwind Logistics LLC\", \"invoice_date\": \"2024-04-15\", \"total_due\": 4850.20}"
}
```

**Rubric Assessment:**
- **Relevance ($R$)**: 5/5 — Direct extraction task matching prompt and document.
- **Correctness ($C$)**: 5/5 — All extracted fields match input text exactly.
- **Diversity ($D$)**: 3/5 — Standard invoice layout, common phrasing.
- **Label Consistency ($L$)**: 5/5 — Clean JSON conforming to schema types.

**Calculation:**
- $S_R = (5-1)/4 = 1.0$
- $S_C = (5-1)/4 = 1.0$
- $S_D = (3-1)/4 = 0.5$
- $S_L = (5-1)/4 = 1.0$
- $\text{Score} = (0.30 \times 1.0 + 0.35 \times 1.0 + 0.15 \times 0.5 + 0.20 \times 1.0) \times 100 = (0.30 + 0.35 + 0.075 + 0.20) \times 100 = 92.5$
- **Verdict**: Accepted (Tier 1).

## Limitations

- **Not a dynamic annotator**: This skill scores candidate pairs; it does not generate new annotations from scratch.
- **Subjectivity in Diversity**: Diversity scoring requires visibility into the surrounding batch distribution to detect true lexical duplicates.
- **Token length blind**: Does not evaluate whether context length exceeds specific hardware limits during training.

## Quantified Output

Every execution of this skill must emit a standardized machine-readable JSON block containing the computed scores:

### Worked Numeric Example (Batch of 5 Examples)

| Candidate ID | $R$ | $C$ | $D$ | $L$ | Composite Score | Status |
|---|---|---|---|---|---|---|
| `cand_01` | 5 | 5 | 4 | 5 | 96.25 | Accepted |
| `cand_02` | 4 | 4 | 3 | 4 | 76.25 | Accepted |
| `cand_03` | 2 | 2 | 2 | 3 | 31.25 | Rejected |
| `cand_04` | 5 | 5 | 3 | 5 | 92.50 | Accepted |
| `cand_05` | 3 | 3 | 3 | 2 | 48.75 | Rejected |

**Batch Aggregates:**
- Total candidates: 5
- Accepted: 3
- Rejected: 2
- Batch Rejection Rate: $(2 / 5) \times 100 = 40.0\%$
- Mean Composite Score: $(96.25 + 76.25 + 31.25 + 92.50 + 48.75) / 5 = 69.0$

### Machine-Readable Result Block

```json
{
  "skill_name": "training-data-quality-scorer",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 5,
  "status": "warn",
  "metrics": {
    "mean_composite_score": 69.0,
    "batch_rejection_rate_pct": 40.0,
    "accepted_count": 3,
    "rejected_count": 2,
    "relevance_mean": 3.8,
    "correctness_mean": 3.8,
    "diversity_mean": 3.0,
    "label_consistency_mean": 3.8
  },
  "metadata": {
    "rejection_threshold": 70.0
  }
}
```
