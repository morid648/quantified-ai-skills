# ❓ Frequently Asked Questions (FAQ)

> **Common questions and answers regarding the Quantified AI Skills suite, the 50-document financial benchmark, evaluation contracts, and agentic workflows.**

---

## 🎯 General Questions

### What makes a skill "Quantified"?

Unlike conventional AI skills that provide qualitative or heuristic guidance, every skill in this suite is built on a **Quantified Output Contract**:
1. **Deterministic Formulas**: Defines explicit mathematical equations (e.g. Field Accuracy, Cohen's $\kappa$, Token Compression Ratio, Two-Proportion $z$-test).
2. **Standardized Error Taxonomy**: Classifies all outcomes into five discrete states (`CORRECT`, `MISSED_FIELD`, `WRONG_VALUE`, `HALLUCINATED_FIELD`, `LOW_CONFIDENCE_CORRECTLY_FLAGGED`).
3. **Machine-Readable JSON Payloads**: Emits immutable JSON blocks conforming to [`references/quantified-output-schema.json`](../references/quantified-output-schema.json) for automated aggregation.

### How many skills are in this repository?

The repository contains **11 production-grade skills** organized into four functional pillars plus a master orchestrator:
- **Pillar A (AI Training & Evaluation)**: `training-data-quality-scorer`, `eval-harness-builder`, `regression-benchmark-tracker`
- **Pillar B (Context Optimization)**: `document-context-chunking`, `context-budget-allocator`
- **Pillar C (Prompt Engineering)**: `prompt-scorecard-testing`, `extraction-prompt-library-finance`
- **Pillar D (AI Annotation)**: `annotation-guideline-writer`, `annotation-qa-scoring`, `finance-document-annotator`
- **Master Orchestrator**: `quantified-eval-orchestrator`

### What is the 50-Document Financial Benchmark?

The 50-document benchmark is an empirical evaluation suite located in [`benchmarks/finance-50doc-v1/`](../benchmarks/finance-50doc-v1/) spanning five critical financial document types (10 documents each):
1. **Commercial Invoices** (Line items, tax, subtotals, totals)
2. **Bank Statements** (Account details, opening/closing balances, transactions)
3. **Income Statements** (Revenue, COGS, OpEx, operating income, net income)
4. **Corporate Expense Reports** (Employees, categories, receipts, approvals)
5. **Loan / KYC Applications** (Applicant profiles, stated income, loan purposes, risk flags)

The dataset incorporates a **20% stress noise injection** (10 noisy documents with OCR corruptions, arithmetic mismatches, and expired credentials) to test edge-case resilience.

---

## 📊 Benchmark Results & Metrics

### What are the verified performance metrics?

Against the 50-document financial dataset, the suite achieved:
- **Field-Level Extraction Accuracy**: **99.44%** (358/360 fields correct; target $\ge 90.0\%$)
- **Document Full-Pass Rate**: **96.0%** (48/50 documents passed; target $\ge 85.0\%$)
- **Inter-Annotator Agreement**: **$\kappa = 0.9055$** (Cohen's Kappa on double-annotated subset; target $\ge 0.81$)
- **Context Token Compression**: **24.33%** reduction (3,526 raw tokens $\rightarrow$ 2,668 optimized tokens; target $\ge 20.0\%$)
- **Factual Information Retention**: **100.0%** (20/20 anchor probes preserved; target $\ge 95.0\%$)
- **Inference Latency Profile**: Median p50 = **1,050 ms**, p95 = **1,654 ms** — real measured latency against a live model (Groq `openai/gpt-oss-120b`), target $< 3,000\text{ ms}$
- **Measured Unit Cost**: **$0.2367 USD per 1,000 documents** (real Groq pricing; target $< $0.50 USD)
- **Human Spot-Check Verification**: 10-document stratified audit confirmed 0.0% false positives and 0.0% false negatives on the grader logic (see `benchmarks/finance-50doc-v1/REPORT.md` §5 for what this does and doesn't certify about the current run).

The 2 field-level misses (out of 360) are a real, explainable finding, not simulation noise — see `REPORT.md` §3.2.

---

## 🔌 Supported AI Assistants & Environments

### Which tools work with these skills?

All skills use the standard `SKILL.md` format and work across:
- ✅ **Claude Code** (Anthropic CLI)
- ✅ **Gemini CLI** (Google DeepMind)
- ✅ **Cursor** (AI IDE)
- ✅ **Antigravity IDE** (Google DeepMind)
- ✅ **Kiro CLI** (AWS)
- ✅ **Codex CLI** (OpenAI)

### How do I invoke a skill in my assistant?

Simply mention the skill by name with an `@` handle or in plain English:
```bash
# In Claude Code / Cursor / Codex:
Use @extraction-prompt-library-finance to extract data from benchmarks/finance-50doc-v1/documents/inv_01.txt

# In Gemini CLI / Antigravity IDE:
Apply document-context-chunking to parse and chunk this bank statement while preserving markdown tables.
```

---

## 🛠️ Testing, Validation & CI

### How do I run the benchmark and integrity tests locally?

```bash
# Run the complete 50-document benchmark evaluation
npm run benchmark

# Validate all skill schemas in strict mode
npm run validate:strict

# Run full repository integrity and reference checks
npm test
```

### How does statistical regression tracking work?

The skill [`regression-benchmark-tracker`](../skills/regression-benchmark-tracker/) executes a two-proportion $z$-test:
$$z = \frac{p_C - p_B}{\sqrt{p^*(1-p^*)\left(\frac{1}{n_B} + \frac{1}{n_C}\right)}}$$
Comparing candidate run accuracy ($p_C$) against the immutable baseline ($p_B = 1.00$, $n_B = 50$). If a candidate change results in a statistically significant regression ($z < -1.96$, $p < 0.05$), CI immediately fails the build.

---

## 📦 Bundles vs. Workflows

### What is the difference?

- **[Bundles](BUNDLES.md)** are curated groupings of skills by functional pillar (e.g. `ai-training-eval`, `context-optimization`, `prompt-engineering`, `ai-annotation`).
- **[Workflows](WORKFLOWS.md)** are multi-step orchestration playbooks that chain multiple skills in sequence to solve complete end-to-end tasks.
