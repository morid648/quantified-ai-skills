---
name: regression-benchmark-tracker
description: Tracks benchmark run histories, statistically evaluates metric deltas vs baselines via z-tests, and alerts on performance regressions.
risk: safe
source: self
tags: [ai-training-eval]
---

# Regression Benchmark Tracker

Records benchmark evaluation runs over time, establishes verified baselines, and statistically tests whether performance changes across model or prompt versions represent significant regressions or expected sampling variance.

## When to Use

Use this skill when you need to:
- Establish and persist an immutable performance baseline for an AI pipeline.
- Compare candidate prompt, model, or chunking changes against an established baseline.
- Perform hypothesis testing (two-proportion z-tests) to verify if an accuracy drop is statistically significant ($p < 0.05$).
- Track longitudinal latency, cost, and accuracy trends across software releases.

Do NOT use this skill for:
- Initial prompt variant discovery or A/B tuning (use `prompt-scorecard-testing`).
- Building the underlying golden dataset (use `eval-harness-builder`).

## Benchmark Storage & Baseline Schema

Benchmark records are stored as structured JSON snapshots in a dedicated benchmark directory (e.g. `benchmarks/<run-id>/baseline_run.json`).

```json
{
  "benchmark_id": "finance-50doc-v1",
  "version": "1.0.0",
  "baseline_timestamp": "2026-09-15T12:00:00Z",
  "verification_status": "verified",
  "sample_size": 50,
  "metrics": {
    "field_accuracy_pct": 94.2,
    "doc_pass_rate_pct": 88.0,
    "latency_p50_ms": 1420,
    "latency_p95_ms": 2850,
    "cost_per_1k_docs_usd": 0.42
  }
}
```

## Statistical Regression Testing (Two-Proportion z-test)

To determine whether an observed difference in pass rate between baseline ($B$) and candidate ($C$) is a genuine regression rather than random fluctuation:

$$z = \frac{p_C - p_B}{\sqrt{p^* (1 - p^*) \left( \frac{1}{n_B} + \frac{1}{n_C} \right)}}$$

Where:
- $p_B = x_B / n_B$: Baseline pass rate ($x_B$ passes out of $n_B$ samples).
- $p_C = x_C / n_C$: Candidate pass rate ($x_C$ passes out of $n_C$ samples).
- $p^* = \frac{x_B + x_C}{n_B + n_C}$: Pooled sample proportion.

### Decision Boundaries (Two-Tailed $\alpha = 0.05$):
- **Statistically Significant Regression**: $z < -1.96$ ($p < 0.05$). Flag **REGRESSION CRITICAL**.
- **Neutral / Noise Margin**: $-1.96 \le z \le +1.96$. Performance is statistically comparable.
- **Statistically Significant Improvement**: $z > +1.96$ ($p < 0.05$). Update baseline candidate.

## Examples

### Example: Comparing Candidate Model to Baseline on 50 Docs

- Baseline ($B$): $n_B = 50$, $x_B = 44$ passes ($p_B = 0.88$).
- Candidate ($C$): $n_C = 50$, $x_C = 37$ passes ($p_C = 0.74$).
- Pooled proportion: $p^* = (44 + 37) / 100 = 81 / 100 = 0.81$.
- Standard Error ($SE$):
  $$SE = \sqrt{0.81 \times 0.19 \times \left( \frac{1}{50} + \frac{1}{50} \right)} = \sqrt{0.1539 \times 0.04} = \sqrt{0.006156} \approx 0.07846$$
- $z$-score:
  $$z = \frac{0.74 - 0.88}{0.07846} = \frac{-0.14}{0.07846} \approx -1.784$$
- Interpretation: Since $-1.784 > -1.96$, the delta is not yet statistically significant at $p < 0.05$ with $N=50$, but represents a substantial practical degradation ($\Delta = -14.0\%$) triggering a warning.

## Limitations

- **Sample size constraints**: With small test sets ($N < 30$), statistical power is limited, and large percentage drops may fail to achieve $p < 0.05$.
- **Does not diagnose root cause**: Flags that a regression has occurred, but requires error taxonomy logs to identify which fields failed.

## Quantified Output

Every regression check execution must emit a standardized result block:

### Worked Numeric Example (Candidate Evaluation vs. Baseline)

- Baseline: $n=50$, pass rate $88.0\%$, mean latency $1420\text{ ms}$, cost $\$0.42 / 1\text{k}$.
- Candidate: $n=50$, pass rate $72.0\%$, mean latency $1100\text{ ms}$, cost $\$0.35 / 1\text{k}$.
- $\Delta \text{ Pass Rate} = 72.0\% - 88.0\% = -16.0\%$.
- Pooled $p^* = (44 + 36) / 100 = 0.80$.
- $SE = \sqrt{0.80 \times 0.20 \times 0.04} = \sqrt{0.0064} = 0.080$.
- $z = (-0.16) / 0.080 = -2.000$.
- Since $z = -2.000 < -1.96$, regression is **statistically significant** ($p = 0.0455$).
- Status: `fail`.

### Machine-Readable Result Block

```json
{
  "skill_name": "regression-benchmark-tracker",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 50,
  "status": "fail",
  "metrics": {
    "delta_pass_rate_pct": -16.0,
    "z_score": -2.000,
    "p_value": 0.0455,
    "is_statistically_significant_regression": 1.0,
    "candidate_pass_rate_pct": 72.0,
    "baseline_pass_rate_pct": 88.0,
    "delta_latency_ms": -320.0,
    "delta_cost_per_1k_usd": -0.07
  },
  "metadata": {
    "baseline_id": "finance-50doc-v1",
    "regression_threshold_z": -1.96
  }
}
```
