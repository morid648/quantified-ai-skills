---
name: annotation-qa-scoring
description: Calculates inter-annotator agreement (Cohen's/Fleiss' kappa), gold-set accuracy, and error taxonomy breakdowns to quantify annotation quality and consistency.
risk: safe
source: self
tags: [ai-annotation]
---

# Annotation QA Scoring

Calculates statistical agreement metrics across annotators, evaluators, and automated tagging models. Quantifies label quality against curated gold standards and classifies discrepancies using a standardized error taxonomy.

## When to Use

Use this skill when you need to:
- Measure inter-annotator agreement (IAA) between two or more human or AI annotators.
- Evaluate annotation accuracy against an authoritative gold-standard ground truth dataset.
- Quantify drift, disagreement, or bias in multi-pass labeling workflows.
- Break down label errors into actionable categories (e.g. boundary errors, missing labels, value confusion).

Do NOT use this skill for:
- Writing the labeling guidelines themselves (use `annotation-guideline-writer`).
- Running live extraction prompts on finance documents (use `extraction-prompt-library-finance`).

## Mathematical Formulations

### 1. Cohen's Kappa ($\kappa$) for Two Annotators
Measures agreement between two independent raters on categorical classifications, correcting for chance agreement:

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$ is observed relative agreement:
  $$P_o = \frac{\sum_{i=1}^k C_{ii}}{N}$$
- $P_e$ is hypothetical probability of chance agreement:
  $$P_e = \sum_{i=1}^k \left( \frac{R_{1, i}}{N} \times \frac{R_{2, i}}{N} \right)$$
- $N$ is the total number of annotated items or fields.
- $k$ is the number of categorical choices.

**Standard Agreement Interpretation Scale:**
- $< 0.00$: Poor
- $0.00 - 0.20$: Slight
- $0.21 - 0.40$: Fair
- $0.41 - 0.60$: Moderate
- $0.61 - 0.80$: Substantial
- $0.81 - 1.00$: Almost Perfect

### 2. Gold-Standard Accuracy Percentage
When comparing candidate annotations against verified gold labels:

$$\text{Accuracy}_{\text{gold}} = \left( \frac{N_{\text{matching fields}}}{N_{\text{total gold fields}}} \right) \times 100$$

## Error Taxonomy Breakdown

Discrepancies are categorized into four standardized error classes:
1. `MISSED_LABEL`: Entity/field was present in gold standard but omitted by annotator.
2. `INCORRECT_VALUE`: Entity/field was captured, but the annotated value disagrees with ground truth.
3. `SPURIOUS_LABEL`: Entity/field was annotated where none exists in gold standard (hallucination).
4. `BOUNDARY_ERROR`: Entity text was identified but span boundaries were clipped or oversized.

## Examples

### Example: Double-Annotation Confusion Matrix on Risk Flags

Two annotators reviewed 100 loan documents for high-risk flags (`Flagged` vs `Not Flagged`):

| Annotator 1 \ Annotator 2 | Flagged | Not Flagged | Total |
|---|---|---|---|
| **Flagged** | 22 ($C_{11}$) | 4 ($C_{12}$) | 26 ($R_1$) |
| **Not Flagged** | 6 ($C_{21}$) | 68 ($C_{22}$) | 74 ($R_2$) |
| **Total** | 28 ($C_1$) | 72 ($C_2$) | 100 ($N$) |

- $P_o = (22 + 68) / 100 = 0.90$
- $P_e = (26/100 \times 28/100) + (74/100 \times 72/100) = (0.26 \times 0.28) + (0.74 \times 0.72) = 0.0728 + 0.5328 = 0.6056$
- $\kappa = (0.90 - 0.6056) / (1 - 0.6056) = 0.2944 / 0.3944 = 0.746$
- **Result**: $\kappa = 0.746$ (Substantial Agreement).

## Limitations

- **Requires categorical alignment**: Unstructured free-text differences must first be mapped to structured equivalence classes before calculating kappa.
- **Prevalence sensitivity**: Cohen's kappa is sensitive to extreme class imbalance (the "prevalence paradox"), which can produce low kappa despite high observed agreement.

## Quantified Output

Every evaluation of annotation QA must produce a standardized machine-readable summary:

### Worked Numeric Example (100 Field Evaluations)

- Evaluated items: 100 fields across 10 double-annotated documents.
- Agreed fields: 91. Disagreed fields: 9.
- Observed Agreement: $91.0\%$.
- Expected Agreement by Chance: $42.5\%$.
- Cohen's $\kappa = (0.910 - 0.425) / (1.0 - 0.425) = 0.485 / 0.575 = 0.843$ (Almost Perfect).
- Gold accuracy: $92.0\%$ (92/100 matching gold).
- Error counts: 4 `INCORRECT_VALUE`, 3 `MISSED_LABEL`, 1 `SPURIOUS_LABEL`, 0 `BOUNDARY_ERROR`.

### Machine-Readable Result Block

```json
{
  "skill_name": "annotation-qa-scoring",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 100,
  "status": "pass",
  "metrics": {
    "cohens_kappa": 0.843,
    "observed_agreement_pct": 91.0,
    "expected_agreement_pct": 42.5,
    "gold_accuracy_pct": 92.0
  },
  "error_taxonomy": {
    "correct": 92,
    "missed_field": 3,
    "wrong_value": 4,
    "hallucinated_field": 1,
    "low_confidence_correctly_flagged": 2
  },
  "metadata": {
    "agreement_tier": "Almost Perfect",
    "target_field_count": 100
  }
}
```
