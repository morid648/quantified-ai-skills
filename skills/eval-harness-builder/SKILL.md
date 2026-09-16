---
name: eval-harness-builder
description: Assembles golden-set evaluation harnesses (input, expected output, automated grader) with pass rate thresholds and human-review escalation rules.
risk: safe
source: self
tags: [ai-training-eval]
---

# Eval Harness Builder

Constructs reproducible, automated evaluation harnesses for LLM applications and extraction pipelines. Combines structured golden evaluation sets with deterministic or model-based grading rules and defines escalation thresholds for human-in-the-loop review.

## When to Use

Use this skill when you need to:
- Build an automated end-to-end evaluation harness for a new or updated AI pipeline.
- Pair test inputs with ground-truth expected outputs and unambiguous grading criteria.
- Define pass/fail thresholds and human spot-check escalation policies.
- Quantify pipeline pass rates and verify grader agreement against human auditors.

Do NOT use this skill for:
- Tracking historical regressions over multiple iterations (use `regression-benchmark-tracker`).
- Designing domain-specific finance extraction prompts (use `extraction-prompt-library-finance`).

## Architecture of an Evaluation Harness

An evaluation harness consists of four tightly coupled components:

```
[ Golden Test Set ] ──> [ Pipeline Under Test ] ──> [ Extracted Prediction ]
                                                           │
                                                           ▼
[ Golden Target   ] ───────────────────────────────> [ Automated Grader ]
                                                           │
                                          ┌────────────────┴───────────────┐
                                          ▼                                ▼
                                    [ Pass / Fail ]            [ Escalation to Human ]
```

1. **Golden Dataset**: Immutable input examples paired with schema-validated expected output targets.
2. **Execution Runner**: Feeds inputs sequentially or in parallel through the target model/prompt.
3. **Automated Grader**:
   - Deterministic matching for exact types (numbers, dates, enum values).
   - Normalized text matching (case-folding, whitespace trimming).
   - Confidence boundary check: If model confidence $< 0.70$ or text fuzzy match is ambiguous ($0.75 < \text{sim} < 0.90$), flag for human escalation.
4. **Audit & Escalation Protocol**: A stratified subset of graded results is surfaced to human auditors to verify that the automated grader is calibrated and accurate.

## Core Formulations

### Pipeline Pass Rate
$$\text{Pass Rate (\%)} = \left( \frac{N_{\text{passed}}}{N_{\text{total evaluated}}} \right) \times 100$$

### Grader-Auditor Agreement
$$\text{Grader Agreement (\%)} = \left( \frac{N_{\text{samples where automated grader matches human verdict}}}{N_{\text{audited spot-check sample}}} \right) \times 100$$

### Human Escalation Rate
$$\text{Escalation Rate (\%)} = \left( \frac{N_{\text{escalated}}}{N_{\text{total evaluated}}} \right) \times 100$$

## Examples

### Example: Harness Grader Rule for Monetary Fields

```python
def grade_monetary_field(predicted_val, expected_val, tolerance=0.01):
    if predicted_val is None and expected_val is None:
        return {"verdict": "PASS", "error_type": "CORRECT", "escalate": False}
    if predicted_val is None or expected_val is None:
        return {"verdict": "FAIL", "error_type": "MISSED_FIELD", "escalate": False}
    try:
        p = float(str(predicted_val).replace('$', '').replace(',', '').strip())
        e = float(str(expected_val).replace('$', '').replace(',', '').strip())
        if abs(p - e) <= tolerance:
            return {"verdict": "PASS", "error_type": "CORRECT", "escalate": False}
        else:
            return {"verdict": "FAIL", "error_type": "WRONG_VALUE", "escalate": True}
    except ValueError:
        return {"verdict": "FAIL", "error_type": "MALFORMED_OUTPUT", "escalate": True}
```

## Limitations

- **Not a replacement for benchmark regression tracking**: Focuses on structuring and running a single evaluation batch rather than multi-version regression statistics.
- **Grader vulnerability to edge cases**: Automated string matching can produce false failures if regex or normalization rules do not account for domain synonyms without human verification.

## Quantified Output

Every evaluation harness execution must emit a standardized result block:

### Worked Numeric Example (50-Document Evaluation Run)

- Total test documents: 50
- Fully passed documents: 44
- Failed documents: 6
- Pass rate: $(44 / 50) \times 100 = 88.0\%$
- Escalations flagged: 8 cases (escalation rate: $16.0\%$)
- Human spot-check: 10 documents audited.
- Grader vs. Human agreement: 9 out of 10 cases agreed ($90.0\%$). Grader discrepancy resolved on 1 case where date formatting was rejected improperly.

### Machine-Readable Result Block

```json
{
  "skill_name": "eval-harness-builder",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 50,
  "status": "pass",
  "metrics": {
    "pass_rate_pct": 88.0,
    "passed_count": 44,
    "failed_count": 6,
    "escalation_rate_pct": 16.0,
    "escalated_count": 8,
    "spot_check_sample_size": 10,
    "grader_human_agreement_pct": 90.0
  },
  "metadata": {
    "pass_threshold_pct": 85.0,
    "escalation_threshold_confidence": 0.70
  }
}
```
