# 🤖 Kiro CLI Integration Guide

> **How to use the Quantified AI Skills suite with AWS Kiro CLI for autonomous financial document processing and model evaluation.**

---

## 1. Overview

**Kiro CLI** is AWS's agentic AI-powered coding assistant. It supports autonomous tool use, context-aware repository analysis, and spec-driven development.

By integrating the **Quantified AI Skills Portfolio** with Kiro, you empower Kiro agents to:
- Perform structured zero-shot financial entity extraction.
- Deterministically chunk and compress long financial statements into token budgets.
- Build golden-set evaluation harnesses and run statistical regression detection against verified baselines.

---

## 2. Installation & Setup for Kiro

### Step 1: Clone the Repository
Clone the repository or link the `skills/` directory into Kiro's skill path (`~/.kiro/skills/`):

```bash
# Clone directly to Kiro skills folder
git clone https://github.com/morid648/quantified-ai-skills.git ~/.kiro/skills

# Or create a symlink / directory link from your existing repo
# Linux/macOS:
ln -s "$(pwd)/skills" ~/.kiro/skills
```

### Step 2: Verification
```bash
test -d ~/.kiro/skills && echo "✓ Quantified Skills available for Kiro"
```

---

## 3. Invoking Quantified Skills in Kiro

Kiro uses natural language prompts to invoke skills:

### Example 1: Extracting Financial Line Items
```
Use @extraction-prompt-library-finance to extract invoice data from benchmarks/finance-50doc-v1/documents/inv_01.txt into structured JSON conforming to the commercial invoice schema.
```

### Example 2: Chunking Bank Statements
```
Use @document-context-chunking to parse benchmarks/finance-50doc-v1/documents/bank_01.txt while preserving all ASCII accounting tables intact.
```

### Example 3: Running Evaluation Harness
```
Use @eval-harness-builder and @regression-benchmark-tracker to score candidate extractions against benchmarks/finance-50doc-v1/gold_labels/ and check for statistical regression against baseline_run.json.
```

---

## 4. Troubleshooting & Best Practices

1. **Explicit File Paths**: Provide exact relative or absolute paths to target documents in your prompt.
2. **Schema Enforcement**: Command Kiro to output responses enclosed in standard JSON blocks matching `references/quantified-output-schema.json`.
3. **Audit Discrepancies**: Refer to `benchmarks/finance-50doc-v1/discrepancy_log.md` for error taxonomy definitions when analyzing noisy inputs.
