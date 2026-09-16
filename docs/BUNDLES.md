# 📦 Quantified AI Skill Bundles

> **Curated collections of production-grade AI skills organized across the 4 foundational pillars of Agentic AI Evaluation & Financial Document Extraction.**

---

## 🚀 Available Bundles

### 1. 📊 AI Training & Evaluation Pillar (`ai-training-eval`)
*For training dataset curation, automated evaluation harnesses, and CI/CD regression detection.*

- [`training-data-quality-scorer`](../skills/training-data-quality-scorer/): Automated dataset health scoring across schema conformity, completeness, noise, and balance.
- [`eval-harness-builder`](../skills/eval-harness-builder/): Full evaluation harness for field-level scoring, semantic distance, and confidence thresholding.
- [`regression-benchmark-tracker`](../skills/regression-benchmark-tracker/): Automated CI/CD regression testing against golden baseline datasets.

---

### 2. ⚡ Context Optimization Pillar (`context-optimization`)
*For deterministic chunking, LLM token budget allocation, and context compression.*

- [`document-context-chunking`](../skills/document-context-chunking/): Deterministic chunking algorithms preserving financial tables and markdown formatting.
- [`context-budget-allocator`](../skills/context-budget-allocator/): Token budget management with zero factual degradation.

---

### 3. 🎯 Prompt Engineering Pillar (`prompt-engineering`)
*For systematic scorecard prompt optimization and zero-shot financial extraction.*

- [`prompt-scorecard-testing`](../skills/prompt-scorecard-testing/): Multi-dimensional prompt scoring across precision, recall, schema compliance, latency, and token cost.
- [`extraction-prompt-library-finance`](../skills/extraction-prompt-library-finance/): Production-grade extraction prompt templates for 5 financial document types.

---

### 4. 🏷️ AI Annotation Pillar (`ai-annotation`)
*For ground truth labeling, annotation guidelines, and inter-annotator agreement QA.*

- [`annotation-guideline-writer`](../skills/annotation-guideline-writer/): Comprehensive, unambiguous annotation guidelines with boundary conditions and edge cases.
- [`annotation-qa-scoring`](../skills/annotation-qa-scoring/): Inter-annotator agreement scoring via Cohen's Kappa ($\kappa$) and error taxonomy classification.
- [`finance-document-annotator`](../skills/finance-document-annotator/): High-precision ground-truth annotation for financial records.

---

### 5. 👑 Master Orchestrator Suite (`quantified-eval-suite`)
*The complete 11-skill unified pipeline orchestrator.*

- [`quantified-eval-orchestrator`](../skills/quantified-eval-orchestrator/): Master coordinator orchestrating chunking, extraction, double-annotation QA, scoring, and regression tracking into a unified scorecard.

---

## 🛠️ Usage Example

You can execute skills individually or chain them together using the master orchestrator or npm scripts:

```bash
# Run the full 50-document benchmark suite
npm run benchmark

# Validate all skills against strict schema rules
npm run validate:strict

# Run all test suites
npm test
```
