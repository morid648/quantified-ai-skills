# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-09-16

### Changed

- **Rebuilt the finance benchmark's extraction step to call a real LLM** (Groq, `openai/gpt-oss-120b`) instead of a deterministic harness that copied gold-label values back out with hand-coded confidence scores and a fixed latency constant. Every accuracy, latency, token-count, and cost figure is now a genuine measurement. See [REPORT.md](benchmarks/finance-50doc-v1/REPORT.md) §3.1 and [RESULTS_EVIDENCE.md](benchmarks/finance-50doc-v1/RESULTS_EVIDENCE.md) for the full methodology and raw evidence.

### Added

- [`RESULTS_EVIDENCE.md`](benchmarks/finance-50doc-v1/RESULTS_EVIDENCE.md) — raw source documents, raw model output, and gold labels linked side by side for every headline claim, including the 2 real extraction failures in full.

## [1.0.0] - 2026

### Added

- **11 quantified agentic skills** across four pillars (see [SKILLS_GUIDE.md](SKILLS_GUIDE.md)):
  - *Training & evaluation*: `training-data-quality-scorer`, `eval-harness-builder`, `regression-benchmark-tracker`, `quantified-eval-orchestrator`
  - *Context optimization*: `document-context-chunking`, `context-budget-allocator`
  - *Prompt engineering*: `prompt-scorecard-testing`, `extraction-prompt-library-finance`
  - *AI annotation*: `annotation-guideline-writer`, `annotation-qa-scoring`, `finance-document-annotator`
- **50-document synthetic financial benchmark** (`benchmarks/finance-50doc-v1/`) — gold labels, per-document evaluation, inter-annotator agreement, and an aggregated scorecard, generated and scored via `scripts/generate_finance_dataset.py` and `scripts/run_finance_benchmark.py`.
- **Validation and CI tooling**: `scripts/validate_skills.py` (strict quality-bar checks), `scripts/generate_index.py`, `scripts/build-catalog.js`, `scripts/tests/verify_repo_integrity.py`.
- **Documentation set**: [HOW_TO_USE.md](HOW_TO_USE.md), [SKILLS_GUIDE.md](SKILLS_GUIDE.md), [ROOT_CAUSE_ANALYSIS.md](ROOT_CAUSE_ANALYSIS.md), and the full `docs/` reference (getting started, bundles, workflows, examples, quality bar, security guardrails).
