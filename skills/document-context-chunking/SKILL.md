---
name: document-context-chunking
description: Chunks complex financial documents preserving cross-references and tables, quantifying token reduction and information retention via factual probes.
risk: safe
source: self
tags: [context-optimization]
---

# Document Context Chunking

Partitions long, semi-structured financial documents (earnings reports, financial statements, regulatory filings) into model-ingestible context chunks. Preserves tabular structures, hierarchical section headers, and footnote cross-references while quantifying token compression and factual retention.

## When to Use

Use this skill when you need to:
- Segment multi-page financial statements, SEC filings, or loan packages for LLM extraction.
- Prevent chunk-boundary truncation of tables, line items, and footnotes.
- Measure token reduction achieved by removing boilerplate while verifying that key financial facts remain intact.
- Attach hierarchical parent breadcrumbs (e.g. `[Income Statement > Operating Expenses]`) to segmented text chunks.

Do NOT use this skill for:
- Allocating a rigid multi-document token budget across competing sources (use `context-budget-allocator`).
- Running information extraction prompts (use `extraction-prompt-library-finance`).

## Structural Chunking Protocol

To avoid catastrophic context fragmentation in financial documents, chunking follows three structural invariants:

```
[ Section Header Breadcrumbs ] ──> Prepend to Every Child Chunk
              │
              ├── [ Prose Paragraphs ] ──> Split along natural sentence/paragraph boundaries
              │
              ├── [ Tabular Data ]    ──> Atomic: NEVER split a row across chunks; retain table header
              │
              └── [ Footnotes / Disclosures ] ──> Bind directly to source table or reference marker
```

1. **Table Atomicity**: Tables are never cleaved arbitrarily mid-row. If a table exceeds max chunk capacity, table headers are duplicated across subsequent chunk splits.
2. **Contextual Breadcrumbs**: Every child chunk is prepended with its structural ancestry path (e.g. `# Document > Section 2 > Balance Sheet`).
3. **Footnote Binding**: Superscript footnote markers (e.g. `[1]`, `[*]`) are preserved with their corresponding reference texts co-located in the same chunk.

## Quantified Metrics & Formulas

### 1. Token Compression Ratio
$$\text{Compression Ratio (\%)} = \left( 1 - \frac{\text{Tokens}_{\text{chunked}}}{\text{Tokens}_{\text{original}}} \right) \times 100$$

### 2. Information Retention Rate
Evaluated by checking whether a set of $K$ pre-defined ground-truth factual probes (e.g. specific line-item figures, dates, entity names) can still be successfully retrieved and resolved from the chunked corpus:

$$\text{Retention Rate (\%)} = \left( \frac{K_{\text{retrieved}}}{K_{\text{total probes}}} \right) \times 100$$

## Examples

### Example: Financial Table Preservation Chunking

**Raw Unoptimized Source (650 tokens):**
Contains repetitive legal disclosures, page watermarks, and an income statement table.

**Optimized Chunk Output:**
```markdown
[PATH: Acme Corp > Q4 2024 > Consolidated Statements of Operations]
[TABLE: Unaudited in Thousands USD]
| Metric | Q4 2024 | Q4 2023 |
|---|---|---|
| Total Revenue | $145,200 | $128,400 |
| Cost of Goods Sold | $78,100 | $69,500 |
| Gross Profit | $67,100 | $58,900 |
| Operating Expenses [1] | $42,300 | $38,100 |
| Net Income | $24,800 | $20,800 |

Footnote [1]: Includes $3.2M non-cash stock compensation expense.
```

## Limitations

- **Complex Multi-Page Spanning Tables**: Very wide tables with dozens of columns require column-pruning or transposition rather than pure row chunking.
- **OCR Artifacts**: Poorly scanned documents with unaligned ASCII whitespace tables may require structural normalization before chunking can succeed.

## Quantified Output

Every execution of this skill must emit a standardized result block:

### Worked Numeric Example (10-Page Financial Filing)

- Original raw token count: $12,450$ tokens.
- Optimized chunked corpus token count: $7,220$ tokens.
- Token Compression: $(1 - 7220 / 12450) \times 100 = 42.0\%$.
- Known factual probes: 20 specific financial data points tested across the document.
- Retained probe facts: 19 successfully resolved. 1 omitted from an excluded boilerplate disclaimer appendix.
- Retention Rate: $(19 / 20) \times 100 = 95.0\%$.
- Status: `pass`.

### Machine-Readable Result Block

```json
{
  "skill_name": "document-context-chunking",
  "version": "1.0.0",
  "timestamp": "2026-09-15T12:00:00Z",
  "sample_size": 1,
  "status": "pass",
  "metrics": {
    "original_tokens": 12450,
    "optimized_tokens": 7220,
    "compression_ratio_pct": 42.0,
    "probes_total": 20,
    "probes_retained": 19,
    "information_retention_pct": 95.0,
    "chunks_generated": 6
  },
  "metadata": {
    "document_type": "10-Q_quarterly_report",
    "table_preservation_mode": "atomic_with_headers"
  }
}
```
