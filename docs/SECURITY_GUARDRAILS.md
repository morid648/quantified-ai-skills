# 🛡️ Security Guardrails & Data Governance Policy

> **Security standards, privacy controls, and safe execution guardrails governing the processing of financial records, evaluation datasets, and agentic workflows.**

---

## 1. Core Principles

Financial data processing and autonomous AI evaluations require stringent security controls to prevent unintended data exposure, model manipulation, or destructive runtime execution.

```
┌────────────────────────────────────────────────────────────────────────┐
│                     SECURITY & GOVERNANCE PILLARS                      │
├───────────────────┬───────────────────┬────────────────────────────────┤
│ 1. Data Privacy   │ 2. Read-Only Ops  │ 3. Injection Defense           │
│ Synthetic corpus, │ Deterministic &   │ Anti-prompt injection checks   │
│ no real PII       │ zero file delete  │ in untrusted financial text    │
└───────────────────┴───────────────────┴────────────────────────────────┘
```

---

## 2. Data Privacy & Synthetic Benchmark Corpus

1. **Synthetic Data Policy**: All documents contained within `benchmarks/finance-50doc-v1/documents/` are 100% synthetically generated. No real corporate records, customer PII, or confidential banking credentials are included.
2. **PII Redaction Guidelines**: When applying these skills to live enterprise documents, agents must invoke redaction patterns to mask taxpayer IDs, bank account routing numbers, and personal contact info before context transmission.
3. **No External Telemetry Exfiltration**: All evaluation harnesses execute locally in offline-compatible environments without transmitting payload data to third-party endpoints.

---

## 3. Safe, Read-Only Execution Standard

1. **Non-Destructive Operations**: Skills in this repository are strictly analytical and evaluation-focused. They do not execute file deletions, database modifications, or network port scans.
2. **Deterministic Outputs**: Chunking, evaluation grading, and regression calculations are idempotent and produce reproducible JSON outputs for auditing.
3. **Safe Evaluation Sandboxing**: When executing eval harnesses across unvetted model predictions, scripts run within sandboxed Python/Node subprocesses with resource limits.

---

## 4. Prompt Injection & Adversarial Document Defenses

Financial documents ingested from external vendors can occasionally contain malicious adversarial prompt injections (e.g., hidden instructions attempting to override output schemas).

All extraction templates in [`skills/extraction-prompt-library-finance/`](../skills/extraction-prompt-library-finance/) implement:
- **XML/JSON Tag Fencing**: Document content is strictly enclosed within `<document_content>` tags.
- **System Instruction Isolation**: Extraction instructions explicitly command the model to ignore any instructions found within the document text.
- **Strict Schema Filtering**: Outputs that deviate from the expected JSON schema or attempt to return non-conforming keys are rejected automatically.

---

## 5. Reporting Security Vulnerabilities

If you identify a security issue or unexpected execution behavior, please open a private GitHub Advisory or report it directly to the repository maintainer.
