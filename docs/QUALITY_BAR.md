# 🏆 Quality Bar & Strict Validation Standards

> **Every skill in this repository is built to meet strict quality, mathematical precision, and schema conformity standards enforced by automated CI validators.**

---

## 1. The Quantified Validation Standard ✅

To earn certification, every skill in the **Quantified AI Skills Portfolio** must satisfy these **6 automated checks**:

### 1. Metadata Integrity (YAML Frontmatter)
The `SKILL.md` frontmatter must be valid YAML containing:
- `name`: Matches the folder name exactly in kebab-case (e.g. `training-data-quality-scorer`).
- `description`: A clear value proposition under 200 characters.
- `risk`: One of `[none, safe, critical, offensive, unknown]`.
- `source`: URL to original reference, academic paper, or `"self"` for original portfolio implementations.

### 2. Unambiguous Triggers ("When to Use")
The skill MUST contain a clear section defining explicit activation boundaries:
- Accepted headings: `## When to Use`, `## When to Use This Skill`, `## Use this skill when`.
- Must specify both positive use cases and negative boundaries (when NOT to use).

### 3. Quantified Mathematical Formulation
The skill MUST define explicit formulas and variable definitions for all emitted metrics (e.g. Accuracy %, Cohen's Kappa $\kappa$, Compression Ratio %, or $z$-score). Heuristic or purely qualitative advice is not permitted.

### 4. Worked Numerical Examples
The skill MUST provide step-by-step mathematical calculations demonstrating exact arithmetic on realistic sample inputs.

### 5. Machine-Readable JSON Output Schema
Every skill MUST emit structured output blocks conforming to [`references/quantified-output-schema.json`](../references/quantified-output-schema.json).

### 6. Standard Error Taxonomy
Discrepancies and edge cases MUST be classified using the standard error taxonomy:
- `CORRECT`
- `MISSED_FIELD`
- `WRONG_VALUE`
- `HALLUCINATED_FIELD`
- `LOW_CONFIDENCE_CORRECTLY_FLAGGED`

---

## 2. Validation Modes & CI Enforcement

Validation is enforced by `scripts/validate_skills.py` and `scripts/tests/verify_repo_integrity.py`:

```bash
# 1. Strict CI Validation Mode (fails on any missing field, invalid heading, or oversized description)
npm run validate:strict

# 2. Comprehensive Repository Integrity Test (checks all JSON files, links, documents, and cross-references)
npm test
```

### Passing Standard
- **Skill Validation**: 11/11 skills passing 100% strict checks.
- **Reference Integrity**: 0 broken links across all markdown documentation.
- **JSON Syntax**: 100% valid syntax across all data payloads.
