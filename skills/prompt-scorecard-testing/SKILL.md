---
name: prompt-scorecard-testing
description: Runs multi-variant prompt A/B testing against labeled test sets, scoring variants across accuracy/F1, latency (p50/p95), and cost per 1,000 calls.
risk: safe
source: self
tags: [prompt-engineering]
---

# Prompt Scorecard Testing

Systematically evaluates and compares candidate prompt variants (e.g. zero-shot vs few-shot vs chain-of-thought) against a labeled ground-truth dataset. Scores variants across accuracy, latency, and token cost to declare an objective winner based on empirical evidence rather than subjective preference.

## When to Use

Use this skill when you need to:
- A/B test competing prompt templates on the same evaluation dataset.
- Determine whether adding few-shot examples or chain-of-thought justification justifies the extra token cost and latency.
- Measure p50 and p95 latency distributions alongside field extraction accuracy.
- Calculate cost per 1,000 document calls to make production architectural decisions.

Do NOT use this skill for:
- One-off single prompt execution without variant comparison (use `extraction-prompt-library-finance`).
- Tracking regressions over time across git commits (use `regression-benchmark-tracker`).

## Prompt Testing Methodology

Candidate prompt variants ($V_A, V_B, \dots, V_k$) are executed across an identical slice of labeled test instances:

```
                  ┌──> [ Variant A: Zero-Shot Direct ]      ──> Scorecard Metrics
                  │
[ Labeled Test ] ─┼──> [ Variant B: Few-Shot (2 examples) ] ──> Scorecard Metrics
                  │
                  └──> [ Variant C: Structured Reasoning ]  ──> Scorecard Metrics
```

### Composite Utility Score
To rank prompt variants with balanced trade-offs, a composite utility index $U(V)$ is computed:
$$U(V) = 0.50 \cdot \left( \frac{\text{Acc}(V)}{\text{Acc}_{\max}} \right) + 0.25 \cdot \left( \frac{\text{Cost}_{\min}}{\text{Cost}(V)} \right) + 0.25 \cdot \left( \frac{\text{Latency}_{\min}}{\text{Latency}_{p95}(V)} \right)$$

## Scorecard Matrix & Formulas

1. **Field Extraction Accuracy**:
   $$\text{Accuracy}(V) = \left( \frac{N_{\text{correct fields}}}{N_{\text{total expected fields}}} \right) \times 100$$
2. **Cost per 1,000 Documents**:
   $$\text{Cost}_{1000}(V) = \frac{\sum_{i=1}^N \left( T_{\text{in}, i} \times R_{\text{in}} + T_{\text{out}, i} \times R_{\text{out}} \right)}{N} \times 1000$$
3. **Latency Profile**:
   - $\text{p50}$: Median response time in milliseconds.
   - $\text{p95}$: 95th percentile response time in milliseconds.

## Examples

### Example: A/B Prompt Variant Matrix (Finance Extraction)

| Metric | Variant A (Zero-Shot) | Variant B (2-Shot Exemplars) | Variant C (COT Reasoning) |
|---|---|---|---|
| **Field Accuracy (%)** | $84.2\%$ | $93.8\%$ | $94.6\%$ |
| **Full-Pass Rate (%)** | $68.0\%$ | $88.0\%$ | $86.0\%$ |
| **Input Tokens / Doc** | $450$ | $1,250$ | $480$ |
| **Output Tokens / Doc** | $120$ | $130$ | $420$ |
| **Cost / 1,000 Docs** | $\$0.140$ | $\$0.266$ | $\$0.324$ |
| **Latency p50 (ms)** | $820\text{ ms}$ | $1,240\text{ ms}$ | $2,450\text{ ms}$ |
| **Latency p95 (ms)** | $1,450\text{ ms}$ | $1,980\text{ ms}$ | $4,100\text{ ms}$ |
| **Utility Score $U$** | $0.865$ | **$0.924$ [WINNER]** | $0.782$ |

*Decision*: Variant B wins. Although Variant C achieves $+0.8\%$ higher accuracy, Variant B delivers $2\times$ faster p95 latency and $18\%$ lower cost.

## Limitations

- **Model specific**: A prompt scorecard winner on Gemini may not be optimal on Claude or GPT without re-running tests.
- **Eval set representativeness**: Results are only as reliable as the diversity of the underlying labeled test set.

## Quantified Output

Every prompt evaluation must emit a comparative machine-readable scorecard:

### Worked Numeric Example (Variant B vs. Variant A on 50 Docs)

- Variant B vs Variant A:
  - Accuracy: $93.8\%$ vs $84.2\%$ ($\Delta = +9.6\%$).
  - Full-Pass: $88.0\%$ vs $68.0\%$ ($\Delta = +20.0\%$).
  - Latency p50: $1,240\text{ ms}$ vs $820\text{ ms}$ ($\Delta = +420\text{ ms}$).
  - Cost / 1k: $\$0.266$ vs $\$0.140$ ($\Delta = +\$0.126$).
- Winning Variant: `Variant_B_TwoShot`.

### Machine-Readable Result Block

```json
{
  "skill_name": "prompt-scorecard-testing",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 50,
  "status": "pass",
  "metrics": {
    "winning_variant_accuracy_pct": 93.8,
    "winning_variant_pass_rate_pct": 88.0,
    "winning_variant_cost_per_1k_usd": 0.266,
    "winning_variant_latency_p50_ms": 1240.0,
    "winning_variant_latency_p95_ms": 1980.0,
    "delta_accuracy_vs_baseline_pct": 9.6,
    "delta_cost_vs_baseline_usd": 0.126
  },
  "metadata": {
    "winner": "Variant_B_TwoShot",
    "variants_evaluated": ["Variant_A_ZeroShot", "Variant_B_TwoShot", "Variant_C_CoT"]
  }
}
```
