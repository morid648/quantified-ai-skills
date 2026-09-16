# 🧭 Quantified AI Workflows

> **End-to-end multi-skill execution playbooks for automated financial document processing, context optimization, dataset curation, and statistical evaluation.**

---

## 1. What Is a Workflow?

While a **[Bundle](BUNDLES.md)** represents a curated collection of skills by domain pillar, a **Workflow** is an ordered, step-by-step execution playbook that orchestrates multiple skills to solve a complex production challenge.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          WORKFLOW LIFECYCLE                            │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. Ingest & Chunk │ 2. Extract & Flag │ 3. Grade, Audit & Track CI     │
│   Semantic slices │   Structured JSON │   Cohen's κ & z-test baseline  │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

---

## 2. Core Production Workflows

### 🌟 Workflow 1: Financial Document Extraction & Benchmarking Pipeline (`financial-document-extraction-eval`)

**Objective**: Ingest unformatted financial text, allocate token budgets, extract structured data across 5 document categories, and benchmark performance against gold-standard labels with automated CI regression tracking.

**Related Bundles**: `ai-training-eval`, `context-optimization`, `prompt-engineering`, `ai-annotation`, `quantified-eval-suite`

#### Step 1: Document Chunking & Context Allocation
- **Goal**: Chunk long financial filings into semantic sections and allocate token budget while maintaining 100% factual retention.
- **Skills**: [`document-context-chunking`](../skills/document-context-chunking/), [`context-budget-allocator`](../skills/context-budget-allocator/)
- **Prompt Example**:
  ```
  Apply @document-context-chunking to parse benchmarks/finance-50doc-v1/documents/inc_01.txt into header, balance, and footnote chunks, then use @context-budget-allocator to fit within 2,700 tokens.
  ```

#### Step 2: Extraction Prompt Execution
- **Goal**: Apply zero-shot financial extraction prompts with strict schema validation and confidence flags.
- **Skills**: [`extraction-prompt-library-finance`](../skills/extraction-prompt-library-finance/), [`prompt-scorecard-testing`](../skills/prompt-scorecard-testing/)
- **Prompt Example**:
  ```
  Use @extraction-prompt-library-finance to extract invoice entities from benchmarks/finance-50doc-v1/documents/inv_01.txt with field-level confidence scoring.
  ```

#### Step 3: Annotation QA & Ground-Truth Validation
- **Goal**: Measure inter-annotator agreement (Cohen's Kappa) and validate ground-truth answer keys.
- **Skills**: [`annotation-guideline-writer`](../skills/annotation-guideline-writer/), [`annotation-qa-scoring`](../skills/annotation-qa-scoring/), [`finance-document-annotator`](../skills/finance-document-annotator/)
- **Prompt Example**:
  ```
  Use @annotation-qa-scoring to calculate Cohen's Kappa across the 10 double-annotated subset files and categorize discrepancies into the standard error taxonomy.
  ```

#### Step 4: Evaluation Harness & Regression Tracking
- **Goal**: Score model predictions against gold labels and detect any regression against baseline metrics.
- **Skills**: [`eval-harness-builder`](../skills/eval-harness-builder/), [`regression-benchmark-tracker`](../skills/regression-benchmark-tracker/), [`training-data-quality-scorer`](../skills/training-data-quality-scorer/), [`quantified-eval-orchestrator`](../skills/quantified-eval-orchestrator/)
- **Prompt Example**:
  ```
  Use @quantified-eval-orchestrator to run the complete 50-document evaluation suite and verify regression metrics with @regression-benchmark-tracker.
  ```

---

### 🌟 Workflow 2: Training Data Quality Curation & Audit (`training-eval-pipeline`)

**Objective**: Audit and clean candidate prompt-completion datasets before fine-tuning.

#### Step 1: Quality Scoring
- **Goal**: Score candidate pairs across Relevance, Correctness, Diversity, and Label Consistency on a 1–5 scale.
- **Skill**: [`training-data-quality-scorer`](../skills/training-data-quality-scorer/)
- **Target**: Compute composite score (0–100) and reject pairs with scores $< 70.0$.

#### Step 2: Annotation Guideline Generation
- **Goal**: Generate unambiguous annotation rules for low-scoring edge cases.
- **Skill**: [`annotation-guideline-writer`](../skills/annotation-guideline-writer/)

---

### 🌟 Workflow 3: Prompt Scorecard & A/B Utility Optimization (`prompt-optimization-pipeline`)

**Objective**: Systematically optimize prompt templates across precision, recall, latency, and token cost.

#### Step 1: Candidate A/B Testing
- **Goal**: Run candidate prompt variants against the test corpus.
- **Skill**: [`prompt-scorecard-testing`](../skills/prompt-scorecard-testing/)

#### Step 2: Composite Utility Scoring
- **Goal**: Calculate multi-attribute utility score $U = w_A A + w_L (1 - L_{\text{norm}}) + w_C (1 - C_{\text{norm}})$ to pick the winning prompt.
- **Skill**: [`eval-harness-builder`](../skills/eval-harness-builder/)

---

## 3. Automated Script Execution

To run the complete end-to-end benchmark workflow via command line:

```bash
# Execute the full financial extraction & evaluation workflow
npm run benchmark

# Verify all cross-references across workflows and bundles
python scripts/validate_references.py
```
