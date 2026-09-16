---
name: context-budget-allocator
description: Allocates fixed token budgets across multi-document sources via keep/summarize/drop rules, quantifying budget utilization and downstream task accuracy impact.
risk: safe
source: self
tags: [context-optimization]
---

# Context Budget Allocator

Distributes a constrained token budget across multiple source documents or sections. Systematically determines which sections to retain in full fidelity (`KEEP`), which to condense (`SUMMARIZE`), and which to omit (`DROP`), while measuring budget utilization and downstream task accuracy impact.

## When to Use

Use this skill when you need to:
- Fit multiple long documents (e.g. 3 years of statements + loan application + credit report) within a strict LLM token window.
- Prioritize high-value quantitative tables over boilerplate prose when tokens are constrained.
- Measure the trade-off between aggressive token reduction and downstream extraction/reasoning accuracy.
- Enforce predictable cost and latency caps in multi-document processing pipelines.

Do NOT use this skill for:
- Splitting a single document into sequential chunks (use `document-context-chunking`).
- Testing prompt wording variations (use `prompt-scorecard-testing`).

## Token Allocation Algorithm

Given a global token budget $B$ and a set of candidate document sections $\{S_1, S_2, \dots, S_m\}$ with estimated relevance weights $w_i \in [0, 1]$ and token costs $c_i$:

```
Rank Sections by Priority Density:  p_i = w_i / c_i
       │
       ├── Priority 1 (High density, core facts)   ──> KEEP (100% tokens)
       ├── Priority 2 (Medium density, background) ──> SUMMARIZE (compress by 60–80%)
       └── Priority 3 (Low density, boilerplate)   ──> DROP (0 tokens)
```

### Allocation Rules:
1. **Direct Extract Targets**: Any section holding mandatory fields specified in the schema is marked `PROTECTED` and cannot be dropped.
2. **Tabular Priority**: Tabular financial data is summarized only via deterministic column pruning, never via lossy prose paraphrasing.
3. **Budget Buffer**: Reserve $10–15\%$ of total budget for model instruction overhead and expected JSON completion tokens.

## Quantified Formulas

### 1. Budget Utilization Percentage
$$\text{Budget Utilization (\%)} = \left( \frac{\text{Tokens}_{\text{allocated}}}{B_{\text{target}}} \right) \times 100$$

### 2. Token Reduction / Trim Percentage
$$\text{Token Trim (\%)} = \left( 1 - \frac{\text{Tokens}_{\text{allocated}}}{\text{Tokens}_{\text{raw candidate}}} \right) \times 100$$

### 3. Downstream Accuracy Impact Delta
$$\Delta \text{Accuracy} = \text{Accuracy}_{\text{budgeted}} - \text{Accuracy}_{\text{unconstrained}}$$

## Examples

### Example: Multi-Document Loan Application Allocation

- **Total Context Budget**: $4,000$ tokens.
- **Candidate Inputs**:
  - $S_1$: Loan Application Form ($800$ tokens, mandatory) $\rightarrow$ `KEEP` ($800$ tokens).
  - $S_2$: 12-Month Bank Statement ($3,200$ tokens) $\rightarrow$ `SUMMARIZE` (retain monthly summary lines only: $650$ tokens).
  - $S_3$: 2-Year Tax Returns ($4,500$ tokens) $\rightarrow$ `SUMMARIZE` (extract AGI, total income: $400$ tokens).
  - $S_4$: Credit Bureau Report Terms & Disclosures ($1,800$ tokens) $\rightarrow$ `DROP` ($0$ tokens).
  - Prompt instructions & completion reserve: $800$ tokens.
- **Total Allocated**: $800 + 650 + 400 + 800 = 2,650$ tokens.
- **Budget Utilization**: $(2650 / 4000) \times 100 = 66.25\%$.

## Limitations

- **Risk of information loss**: Aggressive summarization of financial context can strip footnote caveats that change risk assessments.
- **Requires prior task knowledge**: Allocation cannot function effectively without knowing in advance which fields the downstream prompt requires.

## Quantified Output

Every allocation plan execution must emit a standardized result block:

### Worked Numeric Example (Multi-Source Finance Ingestion)

- Candidate raw tokens across 4 files: $10,300$ tokens.
- Target context budget: $4,000$ tokens.
- Total allocated tokens: $3,450$ tokens (including $600$ token completion reserve).
- Budget Utilization: $(3450 / 4000) \times 100 = 86.25\%$.
- Token Trim: $(1 - 3450 / 10300) \times 100 = 66.5\%$.
- Downstream task extraction accuracy on 20 test fields:
  - Unconstrained context: $95.0\%$ (19/20).
  - Budgeted context: $90.0\%$ (18/20).
  - $\Delta \text{Accuracy} = 90.0\% - 95.0\% = -5.0\%$.
- Status: `pass` ($\Delta \text{Accuracy} \ge -5.0\%$).

### Machine-Readable Result Block

```json
{
  "skill_name": "context-budget-allocator",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 1,
  "status": "pass",
  "metrics": {
    "target_budget_tokens": 4000,
    "raw_candidate_tokens": 10300,
    "allocated_tokens": 3450,
    "budget_utilization_pct": 86.25,
    "token_trim_pct": 66.5,
    "unconstrained_accuracy_pct": 95.0,
    "budgeted_accuracy_pct": 90.0,
    "delta_accuracy_pct": -5.0
  },
  "metadata": {
    "actions": {
      "keep_count": 2,
      "summarize_count": 2,
      "drop_count": 1
    }
  }
}
```
