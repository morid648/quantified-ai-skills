# Canonical Specification: Quantified Metrics Definitions

This document establishes the canonical mathematical formulations, edge-case rules, and evaluation conventions for all skills in the Quantified Skill Pack. All skills must adhere to these definitions to eliminate metric drift.

---

## 1. Field-Level Extraction Accuracy

### Definition & Formula
Field-level accuracy evaluates the model's extraction accuracy on individual atomic and compound fields against the ground-truth gold label.

$$\text{Accuracy}_{\text{field}} = \left( \frac{N_{\text{correct fields}}}{N_{\text{total expected fields}}} \right) \times 100$$

Where:
- $N_{\text{total expected fields}}$ is the total count of non-null fields defined in the gold label across evaluated documents.
- $N_{\text{correct fields}}$ is the count of model-extracted fields that match the gold label according to the field comparison criteria.

### Matching Rules by Data Type
1. **Monetary / Numeric Values**:
   - Stripped of currency symbols (`$`, `€`, `£`), thousands separators (`,`), and trailing whitespace.
   - Numeric tolerance: $|V_{\text{extracted}} - V_{\text{gold}}| \le 0.01$ (handles minor float rounding and cents).
2. **Dates**:
   - Normalized to ISO-8601 (`YYYY-MM-DD`).
   - Equivalent dates in different formats (e.g., `"2024-03-31"`, `"March 31, 2024"`, `"03/31/2024"`) evaluate as matching.
3. **Strings / Categorical**:
   - Lowercased, stripped of leading/trailing whitespace, and consecutive whitespace normalized to single spaces.
   - Punctuation-insensitive for non-alphanumeric trailing characters.
4. **Lists / Tabular Line Items**:
   - Evaluated as an unordered set or key-matched array.
   - A line item matches if key identification fields (`description`, `amount`) match within individual field rules.

### Edge Cases & Handling
- **Missing Field in Gold**: If the gold label is `null` / omitted and model extracts `null` / omitted, it is considered correct. If model hallucinates a value, it is counted as an error (`hallucinated_field`).
- **Division by Zero**: If an empty document has 0 expected fields, accuracy is defined as $100\%$ if 0 fields were extracted, else $0\%$.

---

## 2. Document-Level Full-Pass Rate

### Definition & Formula
A strict document-level success metric verifying that an entire document was extracted with 100% field completeness and zero errors on required fields.

$$\text{Pass Rate}_{\text{doc}} = \left( \frac{N_{\text{fully passed documents}}}{N_{\text{total documents}}} \right) \times 100$$

Where a document is considered `passed` if and only if:
$$\text{Document Accuracy}_{\text{field}} = 100\% \quad \text{and} \quad N_{\text{hallucinated fields}} = 0$$

---

## 3. Inter-Annotator Agreement (Cohen's Kappa & Fleiss' Kappa)

### Cohen's Kappa ($\kappa$)
Measures agreement between two independent raters or passes on categorical items (e.g., entity classes, presence/absence of fields, risk flag assignments), correcting for chance agreement.

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$: Observed proportionate agreement:
  $$P_o = \frac{\sum_{i=1}^k C_{ii}}{N}$$
- $P_e$: Expected agreement by chance under independent ratings:
  $$P_e = \sum_{i=1}^k \left( \frac{R_{1, i}}{N} \times \frac{R_{2, i}}{N} \right)$$
- $N$: Total number of items evaluated.
- $k$: Total number of categories.

### Interpretation Standard (Landis & Koch):
- $< 0.00$: Poor agreement
- $0.00 - 0.20$: Slight agreement
- $0.21 - 0.40$: Fair agreement
- $0.41 - 0.60$: Moderate agreement
- $0.61 - 0.80$: Substantial agreement
- $0.81 - 1.00$: Almost perfect / Perfect agreement

---

## 4. Context Optimization: Compression & Retention Metrics

### Token Compression Ratio
Measures the percentage reduction in token consumption achieved by chunking, filtering, or budget allocation.

$$\text{Compression Ratio (\%)} = \left( 1 - \frac{\text{Tokens}_{\text{optimized}}}{\text{Tokens}_{\text{original}}} \right) \times 100$$

### Information Retention Rate
Quantifies whether necessary factual information was preserved after context optimization using targeted fact-retrieval probes.

$$\text{Retention Rate (\%)} = \left( \frac{N_{\text{facts retained and correctly answered}}}{N_{\text{ground-truth probe facts}}} \right) \times 100$$

---

## 5. Training Data Quality Composite Score

### Rubric Dimensions (1 to 5 scale)
1. **Relevance ($R$)** [Weight: $0.30$]: Alignment with the target financial task and schema domain.
2. **Correctness ($C$)** [Weight: $0.35$]: Accuracy of ground truth labels and factual alignment with source text.
3. **Diversity ($D$)** [Weight: $0.15$]: Uniqueness of vocabulary, template variety, and structural layout.
4. **Label Consistency ($L$)** [Weight: $0.20$]: Adherence to standardized normalization and taxonomy rules.

### Formula
Normalized from 1–5 scale to 0–100 scale:

$$\text{Composite Score} = \left( 0.30 \cdot \frac{R - 1}{4} + 0.35 \cdot \frac{C - 1}{4} + 0.15 \cdot \frac{D - 1}{4} + 0.20 \cdot \frac{L - 1}{4} \right) \times 100$$

### Batch Rejection Rate
$$\text{Rejection Rate (\%)} = \left( \frac{N_{\text{examples with Composite Score } < 70}}{N_{\text{total batch examples}}} \right) \times 100$$

---

## 6. Statistical Significance for Regression Detection (Two-Proportion z-test)

To verify whether a performance delta between baseline run ($1$) and candidate run ($2$) is statistically significant or within expected sampling variance:

$$z = \frac{p_2 - p_1}{\sqrt{p^* (1 - p^*) \left( \frac{1}{n_1} + \frac{1}{n_2} \right)}}$$

Where:
- $p_1 = x_1 / n_1$ (Baseline pass rate)
- $p_2 = x_2 / n_2$ (Candidate pass rate)
- $p^* = \frac{x_1 + x_2}{n_1 + n_2}$ (Pooled proportion)

### Decision Boundary:
- If $z < -1.96$ ($p < 0.05$, two-tailed), the drop is **statistically significant** $\rightarrow$ **Regression Alert Triggered**.
- If $-1.96 \le z \le 1.96$, difference is within expected sampling noise.
- If $z > 1.96$, candidate shows statistically significant improvement.

---

## 7. Cost & Latency Modeling

### Cost per 1,000 Documents
Calculated based on standard token pricing:

$$\text{Cost}_{1000} = \frac{\sum_{i=1}^N \left( \text{InputTokens}_i \times \text{Rate}_{\text{in}} + \text{OutputTokens}_i \times \text{Rate}_{\text{out}} \right)}{N} \times 1000$$

*Benchmark Reference Rates:*
- Input Rate: $\$0.150$ per $1,000,000$ tokens ($\$0.00000015$ / token)
- Output Rate: $\$0.600$ per $1,000,000$ tokens ($\$0.00000060$ / token)

### Latency Metrics
- **p50 (Median)**: 50th percentile execution latency in milliseconds.
- **p95**: 95th percentile execution latency in milliseconds.

---

## 8. Standard Error Taxonomy

Every field discrepancy must be categorized into one of five mutually exclusive classes:

| Class Code | Name | Description | Example |
|---|---|---|---|
| `CORRECT` | Correct Extraction | Field matched gold label within specified tolerances. | Gold: `1250.00`, Extracted: `1250` |
| `MISSED_FIELD` | Missed / False Negative | Field present in gold label, omitted or returned null. | Gold: `2024-05-01`, Extracted: `null` |
| `WRONG_VALUE` | Incorrect Value | Field extracted, but value disagrees with gold label. | Gold: `Acme Corp`, Extracted: `Apex Corp` |
| `HALLUCINATED` | Hallucination / False Positive | Field extracted when absent or null in source/gold. | Gold: `null`, Extracted: `500.00` |
| `CONF_CAUGHT` | Low Confidence Correctly Flagged | Extraction was difficult/ambiguous, flagged with confidence $< 0.70$. | Flagged OCR artifact correctly |
