# 📖 Usage Guide: Quantified AI Skills Suite

> **The practical guide to invoking, chaining, and automating the 11 production-grade Quantified AI Skills for financial document extraction, context optimization, and evaluation.**

---

## 1. Quick Orientation

You are working with the **Quantified AI Skills Portfolio**—an independent suite of **11 production-grade agentic skills** engineered across four foundational pillars plus a master orchestrator:

1. **Pillar A: AI Training & Evaluation** (`training-data-quality-scorer`, `eval-harness-builder`, `regression-benchmark-tracker`)
2. **Pillar B: Context Optimization** (`document-context-chunking`, `context-budget-allocator`)
3. **Pillar C: Prompt Engineering** (`prompt-scorecard-testing`, `extraction-prompt-library-finance`)
4. **Pillar D: AI Annotation** (`annotation-guideline-writer`, `annotation-qa-scoring`, `finance-document-annotator`)
5. **Master Pipeline Orchestrator** (`quantified-eval-orchestrator`)

### The Quantified Contract
Unlike conventional qualitative skills that merely offer heuristic advice, every skill in this suite is strictly bound to a **Quantified Output Contract**:
- **Mathematical Formulations**: Every evaluation computes deterministic numerical metrics (e.g. Field Extraction Accuracy %, Cohen's $\kappa$, Token Compression Ratio %, or Regression $z$-scores).
- **Standardized Error Taxonomy**: Failures are classified into standard categories (`CORRECT`, `MISSED_FIELD`, `WRONG_VALUE`, `HALLUCINATED_FIELD`, `LOW_CONFIDENCE_CORRECTLY_FLAGGED`).
- **Machine-Readable Payloads**: All skills emit valid JSON blocks conforming to [`references/quantified-output-schema.json`](../references/quantified-output-schema.json).

---

## 2. Invoking Skills Across AI Assistants

All skills are stored as self-contained directories under [`skills/<skill-name>/`](../skills/) with a mandatory `SKILL.md` instruction file. You can load and invoke them seamlessly across all major AI agent runtimes:

### Claude Code (CLI)
```bash
# In your Claude Code chat:
Use @extraction-prompt-library-finance to extract invoice data from benchmarks/finance-50doc-v1/documents/inv_01.txt
```

### Cursor (AI IDE)
```bash
# In the Cursor composer or chat panel:
@document-context-chunking chunk benchmarks/finance-50doc-v1/documents/bank_01.txt preserving all transaction tables
```

### Gemini CLI / Antigravity IDE
```bash
# In your Antigravity / Gemini prompt:
Apply the training-data-quality-scorer skill to evaluate data/finance_samples.json with rejection threshold 70
```

### Kiro CLI (AWS)
```bash
# In your Kiro prompt:
Use @eval-harness-builder to generate a golden-set evaluation schema for corporate expense reports
```

### OpenAI Codex CLI
```bash
# In your Codex session:
Apply @regression-benchmark-tracker to compare candidate_run.json against benchmarks/finance-50doc-v1/baseline_run.json
```

---

## 3. Hands-On Step-by-Step Scenarios

### Scenario 1: Production Financial Document Extraction

**Objective**: Extract structured financial data from a commercial invoice or bank statement with confidence ratings and schema validation.

1. **Select the document**: `benchmarks/finance-50doc-v1/documents/inv_01.txt`
2. **Invoke the skill**:
   ```
   Apply @extraction-prompt-library-finance to extract all line items, tax, vendor details, and totals from benchmarks/finance-50doc-v1/documents/inv_01.txt into structured JSON conforming to the commercial invoice schema.
   ```
3. **What happens**:
   - The skill applies the 5-category financial extraction template.
   - It performs arithmetic cross-checks (`subtotal + tax == total_amount`).
   - It assigns field-level confidence scores ($0.00$ to $1.00$).
   - It flags any OCR discrepancies or calculation errors for human review.

---

### Scenario 2: Context Window Optimization & Token Budgeting

**Objective**: Compress a multi-page financial filing by 20%+ while maintaining 100% factual accuracy.

1. **Select the filing**: `benchmarks/finance-50doc-v1/documents/inc_01.txt`
2. **Invoke the skills in sequence**:
   ```
   First, use @document-context-chunking to partition inc_01.txt into semantic chunks while keeping tabular financial statements intact.
   Then, use @context-budget-allocator to fit the content into a 2,000 token budget using the keep/summarize/drop priority rule.
   ```
3. **What happens**:
   - Tabular accounting blocks are preserved without breaking row associations.
   - Narrative footnotes and disclaimers are safely condensed.
   - The system computes the **Token Compression Ratio** ($\Delta \text{Tokens} / \text{Raw Tokens}$) and verifies the **Information Retention Rate** against anchor probes.

---

### Scenario 3: Automated Dataset Quality Scoring

**Objective**: Score candidate prompt-completion pairs before fine-tuning or evaluation.

1. **Invoke the skill**:
   ```
   Use @training-data-quality-scorer to evaluate my dataset pairs against the 4-dimension rubric (Relevance, Correctness, Diversity, Label Consistency).
   ```
2. **What happens**:
   - Each sample is scored on a 1–5 scale across the four dimensions.
   - The skill calculates the weighted **Composite Quality Score** (0–100):
     $$\text{Composite Score} = (0.30 S_R + 0.35 S_C + 0.15 S_D + 0.20 S_L) \times 100$$
   - Items scoring below 70.0 are automatically flagged for rejection or re-annotation.

---

### Scenario 4: Inter-Annotator Agreement QA

**Objective**: Validate ground-truth consistency across independent annotators before establishing a baseline.

1. **Invoke the skill**:
   ```
   Use @annotation-qa-scoring to calculate Cohen's Kappa between annotator_a.json and annotator_b.json across the 10 double-annotated financial documents.
   ```
2. **What happens**:
   - The skill builds the confusion matrix and calculates observed agreement ($P_o$) and chance agreement ($P_e$).
   - It outputs Cohen's $\kappa$ (our benchmark measured $\kappa = 0.9055$, exceeding the $\ge 0.81$ "Almost Perfect" threshold).
   - Any boundary discrepancies are categorized by error taxonomy.

---

### Scenario 5: CI/CD Statistical Regression Tracking

**Objective**: Verify whether a new prompt version or model checkpoint causes statistically significant regression.

1. **Invoke the skill**:
   ```
   Use @regression-benchmark-tracker to execute a two-proportion z-test comparing candidate_run.json against benchmarks/finance-50doc-v1/baseline_run.json.
   ```
2. **What happens**:
   - The skill calculates the standard score:
     $$z = \frac{p_C - p_B}{\sqrt{p^*(1-p^*)\left(\frac{1}{n_B} + \frac{1}{n_C}\right)}}$$
   - If $z < -1.96$ ($p < 0.05$), the skill flags a critical regression and triggers a build failure.

---

## 4. Standard Error Taxonomy

Every extraction and evaluation failure must be classified using this taxonomy:

| Code | Severity | Description | Action Required |
|---|---|---|---|
| `CORRECT` | Info | Field value and type match ground truth exactly. | None |
| `MISSED_FIELD` | Critical | Expected field present in source but missing in extraction. | Prompt rule refinement |
| `WRONG_VALUE` | Critical | Field extracted with inaccurate, corrupted, or incorrect value. | Schema constraint check |
| `HALLUCINATED_FIELD` | Critical | Field generated that does not exist in the source document. | Anti-hallucination constraint |
| `LOW_CONFIDENCE_CORRECTLY_FLAGGED` | Warning | Value extracted correctly but flagged due to source ambiguity or noise. | Auditor human review |

---

## 5. Automation Scripts & CLI Commands

This repository includes turnkey npm and Python commands for validating, indexing, and benchmarking the entire suite:

```bash
# 1. Run the full 50-document financial benchmark pipeline
npm run benchmark

# 2. Execute strict repository validation against all skill schemas
npm run validate:strict

# 3. Run the comprehensive integrity test suite (JSON, links, workflows, documents)
npm test

# 4. Regenerate skills index, catalog, and documentation registry
npm run build
```

---

## 6. Pro Tips for Maximum Impact

1. **Anchor with Schemas**: Always specify the target JSON schema when extracting data so the AI produces deterministic types.
2. **Preserve Tables in Context**: Use `document-context-chunking` before feeding long accounting sheets into an LLM to prevent broken column alignments.
3. **Audit Messy Documents**: Review `benchmarks/finance-50doc-v1/discrepancy_log.md` to see how the system handles OCR noise and arithmetic errors.
4. **Never Accept Prose for Metrics**: Ensure your agent emits the structured JSON result block for automated logging.
