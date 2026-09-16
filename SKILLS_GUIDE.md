# Complete Guide to the Quantified AI Skill Pack

> **A Comprehensive Technical Manual Explaining Architecture, Mathematical Contracts, Chaining Workflows, and Usage for All 11 Skills**

---

## 1. Architectural Philosophy: Why "Quantified" Skills?

Conventional AI skills and agent prompts are overwhelmingly **qualitative**: they instruct an agent on *how to think about* an evaluation or prompt, but nothing requires a measurable score, a reproducible metric, or a pass/fail threshold out the other end.

The **Quantified AI Skill Pack** introduces an engineering standard:
1. **Mandatory Numerical Output**: Every skill must compute and emit at least one reproducible mathematical metric (e.g. Field Extraction Accuracy %, Cohen's $\kappa$, Token Compression %, or Regression $z$-score).
2. **Standardized Error Taxonomy**: Discrepancies must be classified into uniform categories (`CORRECT`, `MISSED_FIELD`, `WRONG_VALUE`, `HALLUCINATED_FIELD`, `LOW_CONFIDENCE_CORRECTLY_FLAGGED`).
3. **Machine-Readable JSON Block**: Every skill outputs an immutable JSON payload conforming to `references/quantified-output-schema.json`, enabling programmatic aggregation, dashboarding, and regression tracking.

---

## 2. Catalog of Skills by Pillar

The pack spans four functional pillars plus a master pipeline orchestrator (11 skills total):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       QUANTIFIED SKILL CATALOG                              │
├───────────────────┬──────────────────────────────────┬──────────────────────┤
│ Pillar            │ Skill Identifier                 │ Primary Metric       │
├───────────────────┼──────────────────────────────────┼──────────────────────┤
│ Pillar A: Train & │ training-data-quality-scorer     │ Composite Score 0-100│
│ Evaluation        │ eval-harness-builder             │ Pass Rate %          │
│                   │ regression-benchmark-tracker     │ z-score (p < 0.05)   │
├───────────────────┼──────────────────────────────────┼──────────────────────┤
│ Pillar B: Context │ document-context-chunking        │ Retention Rate %     │
│ Optimization      │ context-budget-allocator         │ Budget Utilization % │
├───────────────────┼──────────────────────────────────┼──────────────────────┤
│ Pillar C: Prompt  │ prompt-scorecard-testing         │ Composite Utility U  │
│ Engineering       │ extraction-prompt-library-finance│ Field Accuracy %     │
├───────────────────┼──────────────────────────────────┼──────────────────────┤
│ Pillar D: AI      │ annotation-guideline-writer      │ Completeness Score % │
│ Annotation        │ annotation-qa-scoring            │ Cohen's Kappa (κ)    │
│                   │ finance-document-annotator       │ Arithmetic Pass %    │
├───────────────────┼──────────────────────────────────┼──────────────────────┤
│ Master Pipeline   │ quantified-eval-orchestrator     │ End-to-End Scorecard │
└───────────────────┴──────────────────────────────────┴──────────────────────┘
```

---

## 3. Detailed Skill Breakdowns

### Pillar A — AI Training & Evaluation

#### 1. `skills/training-data-quality-scorer`
- **Purpose**: Audits and scores candidate prompt-completion pairs before fine-tuning.
- **Rubric**: Evaluates four orthogonal dimensions on a 1–5 scale:
  - *Relevance* ($w=0.30$): Alignment with target domain instruction.
  - *Correctness* ($w=0.35$): Factual alignment with ground truth.
  - *Diversity* ($w=0.15$): Syntactic, lexical, and structural uniqueness.
  - *Label Consistency* ($w=0.20$): Adherence to schema formatting standards.
- **Formula**:
  $$\text{Composite Score} = \left( 0.30 S_R + 0.35 S_C + 0.15 S_D + 0.20 S_L \right) \times 100$$
- **When to Trigger**: When auditing a dataset before training, filtering noisy candidate pairs, or setting batch rejection gates.

#### 2. `skills/eval-harness-builder`
- **Purpose**: Assembles reproducible automated evaluation harnesses pairing test inputs with ground truth and deterministic or LLM graders.
- **Key Features**:
  - Exact monetary tolerance ($0.01 tolerance).
  - ISO-8601 date normalization.
  - Confidence boundary check (escalate to human review if confidence $< 0.70$).
- **Formula**:
  $$\text{Pass Rate (\%)} = \left( \frac{N_{\text{passed}}}{N_{\text{total evaluated}}} \right) \times 100$$
- **When to Trigger**: When launching an automated evaluation run for an extraction pipeline.

#### 3. `skills/regression-benchmark-tracker`
- **Purpose**: Stores immutable baseline evaluation runs and uses statistical hypothesis testing to detect regressions between versions.
- **Statistical Model**: Two-proportion $z$-test:
  $$z = \frac{p_C - p_B}{\sqrt{p^*(1-p^*)\left(\frac{1}{n_B} + \frac{1}{n_C}\right)}}$$
- **Decision Boundary**:
  - $z < -1.96$: Statistically significant regression ($p < 0.05$) $\rightarrow$ **CI Build Fails**.
  - $-1.96 \le z \le +1.96$: Expected sampling variation.
- **When to Trigger**: When evaluating a candidate model/prompt version against an established production baseline.

---

### Pillar B — Context Optimization

#### 4. `skills/document-context-chunking`
- **Purpose**: Chunks long structured documents (10-Ks, statements, filings) without cleaving tables or stranding footnotes.
- **Invariants**:
  - *Table Row Atomicity*: Never splits a row across chunks; duplicates headers across table continuations.
  - *Hierarchical Breadcrumbs*: Prepends parent section headers to every child chunk.
  - *Footnote Binding*: Keeps superscript footnotes co-located with their tables.
- **Metrics**: Token Compression Ratio (%) and Factual Information Retention Rate (%) over probe facts.
- **When to Trigger**: When preparing multi-page tabular filings for LLM context ingestion.

#### 5. `skills/context-budget-allocator`
- **Purpose**: Manages rigid multi-document token budgets using a priority density algorithm:
  $$p_i = \frac{w_i}{c_i} \quad (\text{Relevance Weight} / \text{Token Cost})$$
- **Actions**:
  - `KEEP` (100% tokens): Core schema target sections.
  - `SUMMARIZE` (60–80% compression): Supporting context and background.
  - `DROP` (0 tokens): Legal boilerplate, disclaimers.
- **When to Trigger**: When fitting multiple long documents (e.g. tax returns + bank statements + credit reports) into a fixed token window.

---

### Pillar C — Prompt Engineering

#### 6. `skills/prompt-scorecard-testing`
- **Purpose**: Systematically A/B tests competing prompt variations on the same labeled test set.
- **Composite Utility Index**:
  $$U(V) = 0.50 \cdot \left( \frac{\text{Acc}(V)}{\text{Acc}_{\max}} \right) + 0.25 \cdot \left( \frac{\text{Cost}_{\min}}{\text{Cost}(V)} \right) + 0.25 \cdot \left( \frac{\text{Latency}_{\min}}{\text{Latency}_{p95}(V)} \right)$$
- **When to Trigger**: When choosing between Zero-Shot, Few-Shot, and Chain-of-Thought prompt variations.

#### 7. `skills/extraction-prompt-library-finance`
- **Purpose**: Production-tuned prompt templates for 5 financial document categories:
  - *Invoices*: Vendor, invoice #, line items, tax, subtotal, total.
  - *Bank Statements*: Bank, account #, period dates, opening/closing balance, transactions.
  - *Income Statements*: Revenue, COGS, Gross Profit, OpEx, Operating Income, Net Income.
  - *Expense Reports*: Employee, report ID, submission date, expense items, total, status.
  - *Loan Applications*: Applicant name, ID type/number, income, loan request, risk flags.
- **Confidence Protocol**: Mandatory field-level confidence rating ($0.0 \dots 1.0$) with low-confidence tripping ($< 0.70$).
- **When to Trigger**: When executing live structured data extraction from financial texts.

---

### Pillar D — AI Annotation

#### 8. `skills/annotation-guideline-writer`
- **Purpose**: Authors unambiguous labeling guidelines, schemas, and edge-case resolution rules.
- **Quality Scorecard**: 10-point completeness checklist ($C_1 \dots C_{10}$) covering task scope, taxonomy, boundary rules, normalization, edge-case catalog, and worked examples.
- **When to Trigger**: Before launching an annotation campaign or when auditing instruction clarity.

#### 9. `skills/annotation-qa-scoring`
- **Purpose**: Computes inter-annotator agreement across multiple labeling passes.
- **Formulation (Cohen's Kappa)**:
  $$\kappa = \frac{P_o - P_e}{1 - P_e}$$
- **Interpretation (Landis & Koch)**:
  - $\ge 0.81$: Almost Perfect Agreement (Our benchmark achieved **0.9055**).
- **When to Trigger**: When auditing label consistency across human annotators or comparing AI passes.

#### 10. `skills/finance-document-annotator`
- **Purpose**: Domain application skill establishing schemas and arithmetic self-consistency checks for financial tagging:
  - Invoice balance check: $\text{Subtotal} + \text{Tax} = \text{Total}$.
  - Statement balance check: $\text{Opening} + \sum \text{Txns} = \text{Closing}$.
  - Income check: $\text{Revenue} - \text{COGS} = \text{Gross Profit}$.
- **When to Trigger**: When generating gold-standard ground truth labels for financial datasets.

---

### Master Orchestration

#### 11. `skills/quantified-eval-orchestrator`
- **Purpose**: Chains the 10 skills together in an automated 8-step pipeline:
  ```
  Step 1: Guideline & Schema Check  ──> annotation-guideline-writer
  Step 2: Ground Truth Verification ──> finance-document-annotator
  Step 3: Chunking & Budgeting      ──> document-context-chunking + context-budget-allocator
  Step 4: Prompt Extraction Engine  ──> extraction-prompt-library-finance
  Step 5: Scorecard Grading         ──> prompt-scorecard-testing
  Step 6: Annotation QA Pass        ──> annotation-qa-scoring
  Step 7: Harness Synthesis & Audit ──> eval-harness-builder
  Step 8: Baseline Persistence      ──> regression-benchmark-tracker
  ```
- **When to Trigger**: When running an end-to-end benchmark run.

---

## 4. How to Run the System

```bash
# 1. Run strict validation on all 900 repository skills
npm run validate:strict

# 2. Run the end-to-end 50-document benchmark
python3 scripts/run_finance_benchmark.py

# 3. View the generated reports
# - Executive report: benchmarks/finance-50doc-v1/REPORT.md
# - Spot-check audit: benchmarks/finance-50doc-v1/discrepancy_log.md
# - Baseline snapshot: benchmarks/finance-50doc-v1/baseline_run.json
# - Non-tech guide: HOW_TO_USE.md
```
