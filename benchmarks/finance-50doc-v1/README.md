# Finance 50-Document Validation Benchmark (v1.0)

This directory contains the complete artifacts, synthetic documents, gold ground-truth labels, evaluation logs, and verified baseline for the **50-Document Finance Validation Run** using the Quantified AI Skill Pack.

---

## Directory Structure

```
benchmarks/finance-50doc-v1/
├── documents/                     # 50 synthetic financial documents (plain text)
│   ├── inv_01.txt ... inv_10.txt  # Commercial Invoices (inv_09, inv_10 noisy)
│   ├── bank_01.txt ... bank_10.txt# Bank Statements (bank_09, bank_10 noisy)
│   ├── inc_01.txt ... inc_10.txt  # Income Statements (inc_09, inc_10 noisy)
│   ├── exp_01.txt ... exp_10.txt  # Expense Reports (exp_09, exp_10 noisy)
│   └── loan_01.txt ... loan_10.txt# Loan / KYC Applications (loan_09, loan_10 noisy)
├── gold_labels/                   # 50 verified ground-truth JSON answer keys
├── annotator_pass2/               # 10 double-annotated JSON files for Cohen's Kappa QA
├── extractions/                   # 50 model-extracted JSON outputs with confidence scores
├── per_doc_eval/                  # 50 field-by-field scoring breakdowns & error tags
├── context_optimized/             # 20 chunked and token-optimized structured filings
├── schema_spec.json               # Canonical category field schemas and validation rules
├── aggregated_scorecard.json      # Machine-readable overall & per-category scorecards
├── baseline_run.json              # Immutable baseline snapshot for regression tracking
├── discrepancy_log.md             # Human verification spot-check audit & reconciliation log
├── run_manifest.json              # Signed certification manifest marking run as verified
├── REPORT.md                      # Comprehensive publication-grade portfolio benchmark report
└── README.md                      # This directory guide
```

---

## Quickstart: Reproducing the Benchmark

To regenerate the synthetic corpus, execute the evaluation pipeline, and verify the baseline:

```bash
# 1. Regenerate the 50 synthetic documents, gold labels, and double-annotated subset
python3 scripts/generate_finance_dataset.py

# 2. Run the end-to-end 8-step benchmark pipeline harness
python3 scripts/run_finance_benchmark.py

# 3. Verify strict compliance of all repository skills
npm run validate:strict
```

---

## Key Benchmark Artifacts

- **Executive Report**: Read [REPORT.md](REPORT.md) for detailed methodology, empirical scorecards, error distributions, and latency/cost profiles.
- **Verification Log**: Review [discrepancy_log.md](discrepancy_log.md) for the 10-document human spot-check audit notes and grader calibration.
- **Baseline Record**: Inspect [baseline_run.json](baseline_run.json) for the formal baseline snapshot used by `regression-benchmark-tracker`.
