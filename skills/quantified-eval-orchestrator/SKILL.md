---
name: quantified-eval-orchestrator
description: Orchestrates end-to-end quantified AI pipelines across data scoring, context optimization, prompt extraction, annotation QA, and regression benchmarking.
risk: safe
source: self
tags: [quantified-eval-suite]
---

# Quantified Eval Orchestrator

The master orchestration skill that coordinates and chains the 10 specialized skills of the Quantified Skill Pack into an automated, dependency-phased evaluation pipeline. Ensures reproducibility, strict quality gating, and empirical verification against certified ground truth.

## When to Use

Use this skill when you need to:
- Run an end-to-end automated validation benchmark on financial, legal, or enterprise document workflows.
- Execute the standardized 8-step pipeline linking annotation guidelines, document chunking, prompt extraction, grading, and regression testing.
- Enforce strict numeric quality thresholds across multiple interconnected AI modules.
- Produce certified baseline records and discrepancy logs for human-in-the-loop audit sign-off.

Do NOT use this skill for:
- Isolated single-task operations like writing a single prompt (use `extraction-prompt-library-finance` directly) or calculating a standalone kappa score (use `annotation-qa-scoring`).

## Architecture & Sequential Execution Workflow

The orchestrator executes an 8-step pipeline, where each phase strictly gates subsequent execution:

```
[ Step 1: Guideline & Schema Definition ] ──> skills/annotation-guideline-writer
                     │
                     ▼
[ Step 2: Ground-Truth Gold Labeling ]   ──> skills/finance-document-annotator
                     │
                     ▼
[ Step 3: Context Chunking & Budgeting ]  ──> skills/document-context-chunking
                                          ──> skills/context-budget-allocator
                     │
                     ▼
[ Step 4: Structured Prompt Extraction ]  ──> skills/extraction-prompt-library-finance
                     │
                     ▼
[ Step 5: Scorecard Grading vs. Gold ]   ──> skills/prompt-scorecard-testing
                     │
                     ▼
[ Step 6: Annotation QA & Kappa Score ]  ──> skills/annotation-qa-scoring
                     │
                     ▼
[ Step 7: Harness Synthesis & Audit ]    ──> skills/eval-harness-builder
                     │
                     ▼
[ Step 8: Baseline Persistence & Alert ] ──> skills/regression-benchmark-tracker
```

### Execution Gates:
1. **Schema Integrity Gate**: 100% of candidate document schemas and gold answer keys must pass deterministic validation before extraction.
2. **Context Retention Gate**: Context optimization must demonstrate $\ge 95\%$ information retention over known probe facts.
3. **Accuracy Gate**: Overall field accuracy must meet or exceed target threshold ($\ge 90\%$).
4. **Audit Sign-off Gate**: A stratified human spot-check (minimum 10 documents or 20% of corpus) must resolve all discrepancies before run is marked `verified`.

## Examples

### Example: Invoking the Full Pipeline Runner

To execute the entire sequence programmatically via CLI:

```bash
# Execute the complete 8-step orchestrated benchmark
python3 scripts/run_finance_benchmark.py
```

The orchestrator coordinates the execution across all 50 financial documents, records field extractions with confidence ratings, computes Cohen's $\kappa$ across independent annotation passes, logs any edge-case discrepancies, and writes the verified scorecard to `benchmarks/finance-50doc-v1/aggregated_scorecard.json`.

## Limitations

- **Requires pre-existing test corpus**: The orchestrator coordinates processing; it does not scrape live web data or provision external cloud infrastructure.
- **Sequential dependency**: If an upstream step fails (e.g. invalid schema specification), subsequent downstream extraction steps are halted to prevent contaminated metrics.

## Quantified Output

Every execution of this master orchestration skill produces an aggregated end-to-end pipeline scorecard:

### Worked Numeric Example (50-Document Finance Benchmark)

- **Total Documents Processed**: 50 / 50 (100% completion rate).
- **Total Discrete Fields Evaluated**: 360 fields.
- **Overall Field Extraction Accuracy**: $99.44\%$ (358/360 correct, via real Groq `openai/gpt-oss-120b` API calls).
- **Document Full-Pass Rate**: $96.0\%$ (48/50 passed).
- **Context Token Compression**: $24.33\%$ reduction with $100.0\%$ factual retention.
- **Inter-Annotator Agreement**: Cohen's $\kappa = 0.9055$ (Almost Perfect).
- **Unit Processing Cost**: $\$0.2367\text{ USD}$ per 1,000 documents (real Groq pricing).
- **Verification Verdict**: grader logic `VERIFIED` (auditor certified on 10 spot-check documents against the prior extraction run); this run's 2 real misses are documented, not audited by that spot-check — see `benchmarks/finance-50doc-v1/REPORT.md` §3.2 and §5.

### Machine-Readable Result Block

```json
{
  "skill_name": "quantified-eval-orchestrator",
  "version": "2.0.0",
  "timestamp": "2026-09-16T12:22:07Z",
  "sample_size": 50,
  "status": "pass",
  "extraction_method": { "provider": "groq", "model": "openai/gpt-oss-120b" },
  "metrics": {
    "field_accuracy_pct": 99.44,
    "doc_pass_rate_pct": 96.0,
    "total_fields_evaluated": 360,
    "correct_fields_count": 358,
    "inter_annotator_cohens_kappa": 0.9055,
    "context_compression_pct": 24.33,
    "factual_retention_pct": 100.0,
    "cost_per_1000_docs_usd": 0.2367,
    "latency_p50_ms": 1049.59,
    "latency_p95_ms": 1654.27
  },
  "metadata": {
    "pipeline_steps_completed": 8,
    "verification_status": "extraction_verified_live_llm_audit_pending",
    "baseline_id": "finance-50doc-v1"
  }
}
```
