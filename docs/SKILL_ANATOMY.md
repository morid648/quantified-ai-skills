# 🧬 Anatomy of a Quantified AI Skill

> **A detailed technical breakdown of how a production-grade Quantified Skill is structured, from YAML frontmatter and mathematical formulations to JSON output schemas.**

---

## 1. Directory & File Structure

Each skill resides in its own isolated directory under `skills/<skill-name>/`:

```
skills/
└── document-context-chunking/
    ├── SKILL.md              ← Mandatory: Primary instruction & contract definition
    ├── examples/             ← Optional: Input/output reference files
    ├── scripts/              ← Optional: Helper utilities
    └── references/           ← Optional: Formal mathematical definitions
```

---

## 2. Structure of `SKILL.md`

Every `SKILL.md` file contains two distinct parts:
1. **YAML Frontmatter** (Machine-readable metadata)
2. **Contract Body** (Human and LLM operational instructions)

---

## 3. Part 1: YAML Frontmatter

```yaml
---
name: document-context-chunking
description: "Deterministic chunking algorithms preserving financial tables, footnotes, and key-value pairs with quantitative retention tracking."
risk: "safe"
source: "self"
tags: ["context-optimization", "financial-documents", "chunking", "token-compression"]
---
```

### Required Frontmatter Fields

| Field | Type | Rules |
|---|---|---|
| `name` | string | Kebab-case, must match the folder name exactly. |
| `description` | string | Concise summary strictly under 200 characters. |
| `risk` | string | One of `none`, `safe`, `critical`, `offensive`, `unknown`. |
| `source` | string | URL or `"self"` for internal portfolio skills. |
| `tags` | list | Keyword array for index and catalog generation. |

---

## 4. Part 2: Contract Body & Standard Headings

A compliant Quantified Skill includes these standard sections:

### 1. Title & Overview (H1 & H2)
```markdown
# Document Context Chunking & Retention Skill

## Overview
Provides deterministic algorithms for partitioning complex financial filings into semantic chunks while maintaining 100% factual retention across accounting tables.
```

### 2. When to Use (H2)
```markdown
## When to Use This Skill
- Use when long financial documents exceed LLM context window limits.
- Use when structured markdown or ASCII accounting tables must be preserved without column breaks.
- Do NOT use for unstructured single-paragraph conversational queries.
```

### 3. Mathematical Formula & Rubric (H2)
```markdown
## Mathematical Formulations

### 1. Token Compression Ratio
$$\text{Compression Ratio} = 1 - \frac{\text{Optimized Tokens}}{\text{Raw Tokens}}$$

### 2. Factual Retention Rate
$$\text{Retention Rate} = \frac{\text{Verified Anchor Probes Preserved}}{\text{Total Anchor Probes}} \times 100\%$$
```

### 4. Step-by-Step Execution Procedure (H2)
```markdown
## Operational Procedure
1. Scan input text for markdown tables and demarcate start/end boundaries.
2. Isolate document header metadata (Invoice #, Date, Account #).
3. Split narrative body text at semantic paragraph boundaries.
4. Verify all anchor probes are accounted for across generated chunk payloads.
```

### 5. Worked Numerical Example (H2)
```markdown
## Worked Numerical Example
- **Raw Document Tokens**: 3,526 tokens
- **Optimized Chunk Tokens**: 2,668 tokens
- **Calculation**:
  $$\text{Compression Ratio} = 1 - \frac{2668}{3526} = 1 - 0.7567 = 24.33\%$$
- **Probe Check**: 20 out of 20 anchor facts found $\rightarrow 100.0\%$ retention.
```

### 6. Machine-Readable JSON Output Block (H2)
```markdown
## Standard Output JSON Schema
```json
{
  "skill": "document-context-chunking",
  "document_id": "bank_01.txt",
  "raw_tokens": 3526,
  "optimized_tokens": 2668,
  "compression_ratio_pct": 24.33,
  "anchor_probes_total": 20,
  "anchor_probes_retained": 20,
  "retention_rate_pct": 100.0,
  "status": "PASS"
}
```
```

---

## 5. Quality Checklist Before Publishing

- [x] Folder name matches `name` field in YAML frontmatter.
- [x] Description is $\le 200$ characters.
- [x] Includes explicit `## When to Use` section.
- [x] Contains mathematical equations with variable definitions.
- [x] Contains a step-by-step worked arithmetic example.
- [x] Emits valid JSON conforming to [`references/quantified-output-schema.json`](../references/quantified-output-schema.json).
- [x] Passes `npm run validate:strict` with 0 errors.
