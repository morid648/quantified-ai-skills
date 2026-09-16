# PRD: AI Training/Evaluation, Context Optimization, Prompt Engineering & Annotation Skill Pack — with a 50-Document Finance Validation Run

**Author:** Anshul
**Status:** Draft v1.0
**Target repo:** existing skills framework (880+ existing skills under `skills/<name>/SKILL.md`)

---

## 1. Objective

Build a coherent, **measurable** ("quantified") set of skills covering four pillars — AI training & evaluation, context optimization, prompt engineering, and AI annotation — inside the existing skills framework, then **prove they work** by running them end-to-end against 50 sample finance documents and verifying the output against ground truth.

Two deliverables, in order:
1. **Phase 1:** the skill pack itself (new `SKILL.md` folders, validated against this repo's own quality bar).
2. **Phase 2:** a benchmark run — 50 finance documents processed through the pack, results generated, and independently verified — proving the skills produce correct, measurable output rather than just plausible-sounding guidance.

## 2. Why "Quantified" Skills Specifically

I inspected the repo's existing skills in these four areas first, so this PRD doesn't duplicate what's already there.

**Already present** (generic, qualitative): `evaluation`, `llm-evaluation`, `agent-evaluation`, `context-optimization`, `context-compression`, `context-window-management`, `prompt-engineering`, `prompt-engineer`, `prompt-engineering-patterns`, `prompt-library`, `data-quality-frameworks`.

**What's missing across all of them:** none of the existing skills in these categories define a required numeric output. They tell an agent *how to think about* evaluation, context, or prompts — but nothing forces a scorecard, a metric, or a pass/fail threshold out the other end. There is also **no AI-annotation skill at all** in the current 880+ skill catalog — a genuine gap, not an overlap.

So this pack's differentiator, and the reason it's worth building rather than reusing what exists: **every skill in this pack must emit at least one numeric, reproducible metric**, not just advice. That's the "quantified" requirement, and it's enforced as an extra frontmatter/content field on top of the repo's normal 5-point quality bar (see §4).

## 3. Repo Quality Bar (inherited, not invented)

Every new `SKILL.md` in this pack must pass the repo's existing validator (`npm run validate:strict`, backed by `scripts/validate_skills.py`), which requires:

| Check | Requirement |
|---|---|
| Metadata | `name` (kebab-case, matches folder), `description` (<200 chars, states *when* to trigger), `risk` (`none/safe/critical/offensive`), `source` (URL or `"self"`) |
| Triggers | A `## When to Use` (or equivalent accepted heading) section |
| Safety | Correct risk classification |
| Examples | At least one copy-pasteable example |
| Limitations | An explicit list of what the skill does *not* do |

## 4. The "Quantified" Extension (this pack's addition)

Beyond the standard bar, every skill in this pack adds:

- **`## Quantified Output`** section — names the metric(s) the skill produces (e.g., field-level extraction accuracy %, Cohen's kappa, token-reduction %, cost per 1,000 documents), the formula/method to compute each, and a worked numeric example using dummy data.
- **A machine-readable result block** the skill instructs the agent to emit at the end of a run — a small JSON object (metric name → value) — so results from different runs/documents can be aggregated and compared without re-reading prose.

## 5. Skill Pack Specification

### Pillar A — AI Training & Evaluation

| Skill folder | Purpose | Quantified output |
|---|---|---|
| `training-data-quality-scorer` | Score candidate training/fine-tuning examples on relevance, correctness, diversity, and label consistency using a 1–5 rubric per dimension | Per-example composite score (0–100), rubric breakdown, rejection rate for a batch |
| `eval-harness-builder` | Assemble a reusable golden-set (input → expected output → automated grader) for any task, including a human-review escalation rule | Pass rate %, grader-agreement % vs. a human spot-check sample |
| `regression-benchmark-tracker` | Store a benchmark run's results and statistically compare against the previous run to catch quality regressions | Δ accuracy vs. baseline, statistical significance flag (e.g., a simple z-test on pass rate) |

### Pillar B — Context Optimization

| Skill folder | Purpose | Quantified output |
|---|---|---|
| `document-context-chunking` | Chunk long, structured documents (financial statements, contracts, filings) for LLM processing while preserving cross-references (tables, footnotes) | Token count before/after, % information retained (via a retrieval-recall check against known facts) |
| `context-budget-allocator` | Given a fixed token budget across multiple source documents, decide what to keep, summarize, or drop | Tokens used vs. budget, task-accuracy impact of the trim (before/after) |

### Pillar C — Prompt Engineering

| Skill folder | Purpose | Quantified output |
|---|---|---|
| `prompt-scorecard-testing` | A/B test prompt variants against a labeled eval set and pick a winner on evidence, not taste | Accuracy/F1 per variant, cost per 1,000 calls, latency (p50/p95) |
| `extraction-prompt-library-finance` | Domain-tuned prompt templates for pulling structured fields out of finance documents (invoices, statements, KYC forms), with a required confidence score in every model output | Field-level extraction accuracy %, % of fields returned with low-confidence flags correctly caught |

### Pillar D — AI Annotation

| Skill folder | Purpose | Quantified output |
|---|---|---|
| `annotation-guideline-writer` | Produce an unambiguous labeling schema + taxonomy + edge-case rules + 3–5 worked examples for a given annotation task | Guideline completeness checklist score, count of edge cases explicitly covered |
| `annotation-qa-scoring` | Quantify annotation quality across annotators/passes | Inter-annotator agreement (Cohen's κ / Fleiss' κ), gold-set accuracy %, error-taxonomy breakdown |
| `finance-document-annotator` | Domain application: schema + procedure for tagging finance documents (entities, line items, anomaly/risk flags) to produce gold labels | Labeled-field count per doc, self-consistency check pass rate |

**10 skills total**, each a standalone `skills/<name>/SKILL.md` folder, independently useful, but designed to chain together for Phase 2.

## 6. Build Process (this repo's actual tooling)

1. Scaffold each folder per `docs/SKILL_ANATOMY.md` (`SKILL.md` required; `examples/`, `references/`, `scripts/` optional).
2. Write frontmatter + content per §3–§4 above.
3. Run locally:
   ```bash
   npm ci
   pip install -r requirements.txt
   npm run validate:strict   # must pass before anything else
   npm run index             # regenerate skills_index.json
   npm run catalog           # regenerate data/catalog.json
   npm run readme            # regenerate README skill listing
   ```
4. Register each skill's `id`/`tags`/`triggers` in `data/catalog.json` (handled by `npm run catalog`, but tags should be hand-picked for discoverability: `evaluation`, `annotation`, `finance`, `prompt-engineering`, `context-optimization`).

## 7. Phase 2 — 50-Document Finance Validation Run

This is the proof step: does the pack actually work, measured against ground truth, not just "runs without erroring."

### 7.1 Document Set

No real finance documents were provided, so the run uses **synthetic-but-realistic** sample documents — assumption flagged in §11. 50 documents across 5 categories (10 each), each with a hand-built **gold-label answer key**:

| Category | Example fields to extract |
|---|---|
| Invoices | vendor, invoice #, line items, tax, total, due date |
| Bank statements | account #, period, opening/closing balance, transaction list |
| Income statements | revenue, COGS, operating expenses, net income, period |
| Expense reports | employee, category, amount, date, approval status |
| Loan/KYC applications | applicant name, income, requested amount, ID type, risk flags |

### 7.2 Pipeline

```
1. annotation-guideline-writer     → labeling schema for all 5 doc types
2. finance-document-annotator      → gold labels for all 50 docs (ground truth)
3. document-context-chunking       → chunk longer docs (statements, income statements)
        + context-budget-allocator → apply a token budget, measure retention
4. extraction-prompt-library-finance → run extraction prompts on all 50 docs
5. prompt-scorecard-testing        → score extracted output vs. gold labels
6. annotation-qa-scoring           → if annotation is double-passed on a subset, compute agreement
7. eval-harness-builder            → aggregate everything into one pass/fail report
8. regression-benchmark-tracker    → save this run as the v1.0 baseline benchmark
```

### 7.3 Metrics Captured (per run, per category, and overall)

- Field-level extraction accuracy (%)
- Document-level full-pass rate (%) — every required field correct
- Token count before/after context optimization, and accuracy delta from optimization
- Cost estimate per 1,000 documents (based on token counts × a stated per-token rate)
- Latency (p50/p95) per document
- Error taxonomy: missed field / wrong value / hallucinated field / low-confidence-correctly-flagged

### 7.4 Verification Step (this is the "verify," not just "generate")

Self-reported metrics from an automated grader aren't trustworthy on their own — verify them:
- **Human spot-check:** manually re-check 10 of the 50 documents (2 per category) against the gold labels *and* the automated grader's verdict, to catch cases where the grader itself is wrong.
- **Discrepancy log:** any case where the manual check disagrees with the automated score gets logged and the grader logic is corrected before the number is reported as final.
- Only after this reconciliation does a run get marked `verified` in the benchmark record.

### 7.5 Deliverables of Phase 2

- `benchmarks/finance-50doc-v1/` folder: the 50 synthetic source documents, gold-label answer key, per-document extraction output, aggregated scorecard (JSON + a short written report), and the discrepancy log from the verification step.
- Updated `regression-benchmark-tracker` record so this becomes the reusable baseline for future skill changes.

## 8. Acceptance Criteria

- [ ] All 10 skills pass `npm run validate:strict`.
- [ ] Every skill's `## Quantified Output` section includes a worked numeric example, not just a metric name.
- [ ] All 50 documents processed with no unhandled pipeline failures.
- [ ] Field-level extraction accuracy and document-level pass rate reported per category and overall.
- [ ] Human spot-check completed on 10/50 documents with any grader discrepancies resolved and logged.
- [ ] Benchmark run saved via `regression-benchmark-tracker` as a re-runnable baseline.

## 9. Delivery Plan

| Phase | Scope | Exit criteria |
|---|---|---|
| 1 — Pillar A & D skills | `training-data-quality-scorer`, `eval-harness-builder`, `regression-benchmark-tracker`, `annotation-guideline-writer`, `annotation-qa-scoring` | All pass strict validation |
| 2 — Pillar B & C skills | `document-context-chunking`, `context-budget-allocator`, `prompt-scorecard-testing`, `extraction-prompt-library-finance` | All pass strict validation |
| 3 — Domain skill | `finance-document-annotator` | Passes validation; schema covers all 5 document categories |
| 4 — Synthetic dataset | 50 documents + gold labels built | Reviewed for realism and label completeness |
| 5 — Pipeline run | Full pipeline executed end-to-end | Scorecard generated for all 50 docs |
| 6 — Verification | 10-document human spot-check + discrepancy resolution | Run marked `verified` |
| 7 — Write-up | Final report + README for the benchmark folder | A stranger can read the methodology and results in one pass |

## 10. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Synthetic documents are unrealistically clean, inflating accuracy | Deliberately inject messy cases (ambiguous line items, missing fields, OCR-style noise) into ~20% of the set |
| Automated grader has systematic bias, making "verification" circular | The 10-doc human spot-check specifically targets grader disagreement, not just extraction correctness |
| Skills overlap with existing repo skills, causing confusion about which to use | §2's gap analysis is the answer key; each new skill's description explicitly states how it differs from the existing generic one |
| Metric definitions drift skill-to-skill (e.g., two different "accuracy" formulas) | A single shared metrics-definition reference file is created once and linked from every skill's Quantified Output section |

## 11. Assumptions & Open Questions

- **Document source:** assumed synthetic, since no real finance documents were supplied. If real (de-identified) documents are available, swap them in for a more meaningful benchmark — the pipeline doesn't change either way.
- **Model/provider for the extraction step:** not yet specified — the prompt library should stay provider-agnostic (works with any chat-completions-style API) rather than hardcoding one vendor.
- **Portfolio framing:** built out, this pack and its verified benchmark report double as a concrete, numbers-backed artifact for AI training/evaluation, annotation, and prompt-engineering work — worth keeping the final report readable as a standalone writeup, not just raw JSON.
