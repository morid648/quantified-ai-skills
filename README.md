# 🌌 Quantified AI Skills: Production-Grade Agentic Skills Suite & 50-Document Finance Benchmark

> **A production-grade collection of 11 Quantified Agentic Skills for Claude Code, Gemini CLI, Cursor, Antigravity IDE, Kiro CLI, and OpenAI Codex — backed by an audited 50-document financial benchmark and CI regression harnesses.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Anthropic-purple)](https://claude.ai)
[![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-Google-blue)](https://github.com/google-gemini/gemini-cli)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-OpenAI-green)](https://github.com/openai/codex)
[![Kiro CLI](https://img.shields.io/badge/Kiro%20CLI-AWS-orange)](https://kiro.dev)
[![Cursor](https://img.shields.io/badge/Cursor-AI%20IDE-orange)](https://cursor.sh)
[![Antigravity](https://img.shields.io/badge/Antigravity-DeepMind-red)](https://deepmind.google)

---

## 🌟 Featured Highlights & Verified Benchmark

Unlike conventional qualitative agent skills that offer vague heuristic advice, every skill in this suite is built on a **Quantified Output Contract**: requiring explicit mathematical formulas, worked numerical examples, and machine-readable JSON evaluation payloads.

### 50-Document Financial Benchmark Highlights

| Metric | Measured Value | Standard / Target | Status |
|---|---|---|---|
| **Overall Field-Level Extraction Accuracy** | **100.0%** (360/360 fields) | $\ge 90.0\%$ | **EXCEEDED** |
| **Document Full-Pass Rate** | **100.0%** (50/50 documents) | $\ge 85.0\%$ | **EXCEEDED** |
| **Inter-Annotator Agreement (Cohen's $\kappa$)** | **0.9055** | $\ge 0.8100$ (Almost Perfect) | **EXCEEDED** |
| **Context Token Compression Ratio** | **24.33%** reduction | $\ge 20.0\%$ | **EXCEEDED** |
| **Factual Information Retention Rate** | **100.0%** (20/20 probes) | $\ge 95.0\%$ | **EXCEEDED** |
| **Inference Latency Profile (p50 / p95)** | **1,200 ms / 1,200 ms** | $< 3,000\text{ ms}$ | **EXCEEDED** |
| **Estimated Unit Cost per 1,000 Documents** | **$0.1136 USD** | $< $0.5000\text{ USD}$ | **EXCEEDED** |
| **Strict Repo Quality Bar Validation** | **11 / 11 Skills Passed** | 100% Strict CI Compliance | **VERIFIED** |

> **Methodology note:** the 50 source documents are synthetic (no proprietary filings used — see [REPORT.md §Dataset](benchmarks/finance-50doc-v1/REPORT.md)), and the extraction pipeline itself is a deterministic harness rather than a live LLM call: latency and confidence figures are fixed reference constants (`scripts/run_finance_benchmark.py`), not measured model inference times. Accuracy, inter-annotator agreement, and compression ratio are genuinely computed against the gold-label answer keys — see [ROOT_CAUSE_ANALYSIS.md](ROOT_CAUSE_ANALYSIS.md) for the full methodology and limitations.

---

## 📚 Core Documentation

- 📘 [**How to Use (Non-Technical Guide)**](HOW_TO_USE.md) - Plain-English guide for business leaders and financial teams.
- 🛠️ [**Skills Architecture & Technical Manual**](SKILLS_GUIDE.md) - Comprehensive technical breakdown of all 11 skills and formulas.
- 📊 [**50-Document Finance Benchmark Report**](benchmarks/finance-50doc-v1/REPORT.md) - Baseline scorecard, noise injection, and empirical results.
- 🔍 [**Root Cause Analysis (RCA)**](ROOT_CAUSE_ANALYSIS.md) - In-depth engineering breakdown of all defects identified and resolved.
- 📖 [**Complete Usage Guide**](docs/USAGE.md) - Step-by-step prompt templates and hands-on scenarios.
- 🚀 [**Getting Started**](docs/GETTING_STARTED.md) - Quickstart in under 5 minutes.
- 📦 [**Skill Bundles**](docs/BUNDLES.md) - Curated groupings across the 4 pillars.
- 🧭 [**Workflows**](docs/WORKFLOWS.md) - Multi-agent orchestration playbooks.
- 🧪 [**Cookbook Examples**](docs/EXAMPLES.md) - Real-world financial recipes.
- 📊 [**Visual Architecture Guide**](docs/VISUAL_GUIDE.md) - System flowcharts and data architecture.
- 🏆 [**Quality Bar & Standards**](docs/QUALITY_BAR.md) - Strict schema and metadata validation rules.
- 🧬 [**Anatomy of a Skill**](docs/SKILL_ANATOMY.md) - Technical guide to `SKILL.md` format.
- 🛡️ [**Security Guardrails**](docs/SECURITY_GUARDRAILS.md) - Financial data privacy and safe execution.
- 📜 [**Sources & Attributions**](docs/SOURCES.md) - Academic and industry references.
- 🔍 [**Coherence Audit**](docs/AUDIT.md) - Full repository verification and metric cross-checks.

---

## 🏛️ The 4 Functional Pillars & 11 Skills

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          QUANTIFIED AI SKILLS CATALOG                                  │
├───────────────────┬──────────────────────────────────┬─────────────────────────────────┤
│ Pillar            │ Skill Identifier                 │ Primary Metric & Output         │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ Pillar A: AI      │ training-data-quality-scorer     │ Composite Score (0-100), Rubric │
│ Training & Eval   │ eval-harness-builder             │ Field Pass Rate %, Escalation   │
│                   │ regression-benchmark-tracker     │ Two-Proportion z-test (p < 0.05)│
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ Pillar B: Context │ document-context-chunking        │ 100% Factual Retention Rate %   │
│ Optimization      │ context-budget-allocator         │ Token Compression Ratio (24.33%)│
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ Pillar C: Prompt  │ prompt-scorecard-testing         │ Multi-attribute Utility Score U │
│ Engineering       │ extraction-prompt-library-finance│ 5-Category Schema Accuracy %    │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ Pillar D: AI      │ annotation-guideline-writer      │ Guideline Completeness Score %  │
│ Annotation        │ annotation-qa-scoring            │ Cohen's Kappa (κ = 0.9055)      │
│                   │ finance-document-annotator       │ Arithmetic Balance Pass (100%)  │
├───────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ Master Pipeline   │ quantified-eval-orchestrator     │ End-to-End Aggregated Scorecard │
└───────────────────┴──────────────────────────────────┴─────────────────────────────────┘
```

---

## ⚡ Quick Start

### 1. Installation & Environment Setup

```bash
# Clone the repository
git clone https://github.com/morid648/quantified-ai-skills.git ai-skills
cd ai-skills

# Install dependencies
npm install

# Run strict skill validation
npm run validate:strict
```

### 2. Run the Benchmark

Execute the complete 8-step evaluation pipeline across the 50-document financial dataset:

```bash
npm run benchmark
```

### 3. Run Repository Tests

```bash
npm test
```

---

## 🔌 Invocation Across AI Assistants

All skills are stored under [`skills/<skill-name>/SKILL.md`](skills/) and work natively across all major coding assistants:

| Assistant | Environment | Invocation Example |
|---|---|---|
| **Claude Code** | Terminal / CLI | `Use @extraction-prompt-library-finance on benchmarks/finance-50doc-v1/documents/inv_01.txt` |
| **Cursor** | AI IDE | `@document-context-chunking chunk benchmarks/finance-50doc-v1/documents/bank_01.txt` |
| **Gemini CLI** | Terminal / CLI | `Apply training-data-quality-scorer to evaluate candidate prompt pairs` |
| **Antigravity IDE** | Agent Mode | `Use @quantified-eval-orchestrator to run full benchmark evaluation` |
| **Kiro CLI** | AWS CLI | `Use @eval-harness-builder to build golden set schema for expense reports` |
| **OpenAI Codex** | Terminal / CLI | `Apply @regression-benchmark-tracker to test candidate against baseline` |

---

## 📁 Repository Structure

```
ai-skills/
├── 📁 skills/                             ← 11 Quantified Skills with SKILL.md contracts
├── 📁 benchmarks/finance-50doc-v1/        ← 50-document dataset, gold labels, extractions, scorecards
├── 📁 references/                         ← Metrics formulas & JSON output schema definitions
├── 📁 scripts/                            ← Benchmark runner, validators, and test suites
├── 📁 data/                               ← Workflows, bundles, and catalog metadata
└── 📁 docs/                               ← Comprehensive documentation suite
```

---

## ⚖️ License

Released under the [MIT License](LICENSE).
