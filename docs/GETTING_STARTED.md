# 🚀 Getting Started with Quantified AI Skills

> **Get up and running with the 11 production-grade Quantified AI Skills, benchmark datasets, and evaluation harnesses in under 5 minutes.**

---

## 1. What Are Quantified AI Skills?

Traditional AI skills offer qualitative guidance—prompt suggestions and heuristic tips that sound good but provide no measurable proof of accuracy.

The **Quantified AI Skills Portfolio** establishes an engineering baseline where every skill:
1. **Enforces Explicit Mathematical Formulas**: Metrics like Field Extraction Accuracy, Cohen's Kappa ($\kappa$), Token Compression Ratio, and Two-Proportion $z$-tests are calculated rigorously.
2. **Classifies Discrepancies**: Uses a standardized 5-state Error Taxonomy (`CORRECT`, `MISSED_FIELD`, `WRONG_VALUE`, `HALLUCINATED_FIELD`, `LOW_CONFIDENCE_CORRECTLY_FLAGGED`).
3. **Emits Machine-Readable JSON**: Conforms to [`references/quantified-output-schema.json`](../references/quantified-output-schema.json) for automated pipeline logging.
4. **Is Empirically Proven**: Validated against an audited **50-document financial benchmark** spanning Commercial Invoices, Bank Statements, Income Statements, Expense Reports, and Loan Applications.

---

## 2. Quickstart: 3-Step Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/morid648/quantified-ai-skills.git ai-skills
cd ai-skills
```

### Step 2: Install Dependencies & Verify Environment
Make sure Node.js (>= 18) and Python (>= 3.9) are available:
```bash
# Install Node dependencies
npm install

# Verify strict skill schema compliance
npm run validate:strict
```

### Step 3: Run the 50-Document Financial Benchmark
Execute the automated evaluation pipeline to run chunking, extraction, double-annotation QA, and scorecard generation:
```bash
npm run benchmark
```
Output:
```
============================================================
  QUANTIFIED SKILLS EVALUATION PIPELINE
  50-Document Synthetic Financial Benchmark Run
============================================================
Step 1: Schema Specification Check  ──> Verified 50/50 documents conform to schema
Step 2: Gold-Standard Integrity     ──> 100% arithmetic self-consistency pass on clean sets
Step 3: Chunking & Budgeting        ──> 24.33% token compression on long statements
Step 4: Extraction Engine           ──> 50/50 extractions completed with confidence ratings
Step 5: Scorecard Grading           ──> Field match and error taxonomy classification
Step 6: Annotation QA Pass          ──> Secondary pass comparison; Cohen's kappa = 0.9055
Step 7: Aggregated Reporting        ──> Multi-category synthesis & unit cost calculation
Step 8: Baseline Persistence        ──> Saved immutable snapshot (baseline_run.json)
```

---

## 3. The 4 Functional Pillars & 11 Skills

The 11 skills are organized into four core pillars plus a master orchestrator:

| Pillar | Skill Name | Primary Metric | Target | Measured |
|---|---|---|---|---|
| **Pillar A: AI Training & Evaluation** | [`training-data-quality-scorer`](../skills/training-data-quality-scorer/) | Composite Score (0–100) | $\ge 70.0$ | Calibrated |
| | [`eval-harness-builder`](../skills/eval-harness-builder/) | Full-Pass Rate % | $\ge 85.0\%$ | **100.0%** |
| | [`regression-benchmark-tracker`](../skills/regression-benchmark-tracker/) | Two-Proportion $z$-test | $z \ge -1.96$ | **Verified Baseline** |
| **Pillar B: Context Optimization** | [`document-context-chunking`](../skills/document-context-chunking/) | Factual Retention Rate % | $\ge 95.0\%$ | **100.0%** |
| | [`context-budget-allocator`](../skills/context-budget-allocator/) | Token Compression Ratio | $\ge 20.0\%$ | **24.33%** |
| **Pillar C: Prompt Engineering** | [`prompt-scorecard-testing`](../skills/prompt-scorecard-testing/) | Composite Utility Score | $\ge 80.0$ | Calibrated |
| | [`extraction-prompt-library-finance`](../skills/extraction-prompt-library-finance/) | Field Extraction Accuracy % | $\ge 90.0\%$ | **100.0%** |
| **Pillar D: AI Annotation** | [`annotation-guideline-writer`](../skills/annotation-guideline-writer/) | Guideline Completeness % | $\ge 80.0\%$ | Calibrated |
| | [`annotation-qa-scoring`](../skills/annotation-qa-scoring/) | Cohen's Kappa ($\kappa$) | $\ge 0.81$ | **0.9055** |
| | [`finance-document-annotator`](../skills/finance-document-annotator/) | Arithmetic Balance Pass % | $100.0\%$ | **100.0%** |
| **Master Orchestrator** | [`quantified-eval-orchestrator`](../skills/quantified-eval-orchestrator/) | End-to-End Pipeline Scorecard | Full Pass | **Verified** |

---

## 4. Using Skills in Your AI Assistant

To use any skill in your favorite agentic IDE or CLI tool:

### In Claude Code
```bash
Use @extraction-prompt-library-finance to extract invoice data from benchmarks/finance-50doc-v1/documents/inv_01.txt
```

### In Cursor
```bash
@document-context-chunking chunk benchmarks/finance-50doc-v1/documents/bank_01.txt keeping all table columns aligned
```

### In Gemini CLI / Antigravity IDE
```bash
Apply the training-data-quality-scorer skill to evaluate my candidate fine-tuning pairs
```

### In Kiro CLI
```bash
Use @eval-harness-builder to build an evaluation harness for loan applications
```

---

## 5. Next Steps

- 📖 Read the [**Usage Guide**](USAGE.md) for in-depth prompt templates and multi-step chaining patterns.
- 📦 Explore [**Skill Bundles**](BUNDLES.md) to inspect curated collections by pillar.
- 🔄 Review [**Workflows**](WORKFLOWS.md) for end-to-end multi-agent orchestration playbooks.
- 📊 Inspect the [**50-Document Benchmark Report**](../benchmarks/finance-50doc-v1/REPORT.md) for empirical accuracy, latency, and cost telemetry.
- 🛠️ Read [**SKILLS_GUIDE.md**](../SKILLS_GUIDE.md) for the complete architectural manual and mathematical proofs.
