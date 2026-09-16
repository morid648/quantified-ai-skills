# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-09-16

### Changed

- **Rebuilt the 50-document finance benchmark to call a real, live LLM** (Groq API, `openai/gpt-oss-120b`) instead of the deterministic/simulated harness used in 1.0.0. Every accuracy, latency, confidence, token-count, and cost figure in `benchmarks/finance-50doc-v1/REPORT.md` is now a genuine measurement from that run, not a fixed constant. Result: 99.44% field-level accuracy (358/360 fields), 96% document full-pass rate (48/50 docs) — a real, non-perfect, well-explained result (see `RESULTS_EVIDENCE.md` and `ROOT_CAUSE_ANALYSIS.md` for the `fiscal_period` formatting bug this run surfaced).
- Added `benchmarks/finance-50doc-v1/RESULTS_EVIDENCE.md` linking every headline claim to the raw per-document source text, gold label, model output, and grader verdict, so the benchmark is independently checkable rather than only summarized.

---

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

### Notes

This project builds on top of a larger community skills scaffold (repo tooling conventions, validation scripts, CI structure) that this repo was originally seeded from — see [prd.md](prd.md) for full context. The 11 skills and the finance benchmark above are this project's own work.
