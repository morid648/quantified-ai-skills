# Quantified Skills Directory

Welcome to the **Quantified AI Skill Pack** directory. This folder contains the 11 production-grade, mathematically verified skills covering the four pillars of modern agentic AI engineering: **AI Training & Evaluation**, **Context Optimization**, **Prompt Engineering**, and **AI Annotation**, coordinated by a **Master Pipeline Orchestrator**.

---

## 📂 Architecture & Directory Layout

Each skill is self-contained in its own directory adhering to the strict repository quality bar:

```
skills/
├── annotation-guideline-writer/       # Guideline schema authoring & completeness score %
├── annotation-qa-scoring/             # Inter-annotator agreement (Cohen's κ) & error taxonomy
├── context-budget-allocator/          # Rigid multi-document token budgeting & keep/summarize/drop
├── document-context-chunking/         # Tabular row preservation, footnotes, and retention %
├── eval-harness-builder/              # Golden sets, automated grading rules, escalation logic
├── extraction-prompt-library-finance/ # Production schemas for 5 finance categories with confidence
├── finance-document-annotator/        # Financial entity tagging & arithmetic self-consistency
├── prompt-scorecard-testing/          # A/B variant testing matrix, utility score, latency & cost
├── quantified-eval-orchestrator/      # Master 8-step pipeline orchestrator
├── regression-benchmark-tracker/      # Baseline storage & two-proportion z-test regression alerts
└── training-data-quality-scorer/      # 4-dimension 1-5 rubric, composite score & batch rejection
```

---

## 🎯 The 11 Quantified Skills

### Pillar A: AI Training & Evaluation
1. **[`training-data-quality-scorer`](training-data-quality-scorer/SKILL.md)**: Scores candidate prompt-completion pairs across 4 rubric dimensions (Relevance, Correctness, Diversity, Label Consistency) on a 1–5 scale, computing a 0–100 weighted composite quality score.
2. **[`eval-harness-builder`](eval-harness-builder/SKILL.md)**: Constructs golden evaluation sets with deterministic tolerances ($0.01 for monetary fields, ISO-8601 for dates) and automated escalation rules.
3. **[`regression-benchmark-tracker`](regression-benchmark-tracker/SKILL.md)**: Stores immutable baseline evaluation snapshots and applies two-proportion $z$-tests ($p < 0.05$) to alert on statistically significant regressions.

### Pillar B: Context Optimization
4. **[`document-context-chunking`](document-context-chunking/SKILL.md)**: Chunks complex financial filings while preserving table row atomicity, footnote markers, and hierarchical breadcrumbs, verifying factual retention.
5. **[`context-budget-allocator`](context-budget-allocator/SKILL.md)**: Distributes a fixed token budget across competing documents using a priority density algorithm (`KEEP`, `SUMMARIZE`, `DROP`).

### Pillar C: Prompt Engineering
6. **[`prompt-scorecard-testing`](prompt-scorecard-testing/SKILL.md)**: Compares prompt variants (Zero-Shot vs Few-Shot vs Chain-of-Thought) across accuracy, p50/p95 latency, and cost per 1,000 calls.
7. **[`extraction-prompt-library-finance`](extraction-prompt-library-finance/SKILL.md)**: Production JSON extraction templates for Invoices, Bank Statements, Income Statements, Expense Reports, and Loan/KYC Applications with mandatory field confidence ratings.

### Pillar D: AI Annotation
8. **[`annotation-guideline-writer`](annotation-guideline-writer/SKILL.md)**: Authors comprehensive labeling instructions evaluated against a 10-point completeness checklist score.
9. **[`annotation-qa-scoring`](annotation-qa-scoring/SKILL.md)**: Measures inter-annotator agreement (Cohen's $\kappa$ and Fleiss' $\kappa$) and breaks down discrepancies by standard error taxonomy.
10. **[`finance-document-annotator`](finance-document-annotator/SKILL.md)**: Tags financial line items and verifies arithmetic balance equations (e.g., Subtotal + Tax = Total).

### Master Orchestration
11. **[`quantified-eval-orchestrator`](quantified-eval-orchestrator/SKILL.md)**: Chains all 10 skills together in an automated 8-step pipeline with strict execution gates.

---

## 🚀 How to Validate and Run

```bash
# Verify all 11 skills against strict quality bar
npm run validate:strict

# Run the 50-document end-to-end benchmark
python3 scripts/run_finance_benchmark.py
```
