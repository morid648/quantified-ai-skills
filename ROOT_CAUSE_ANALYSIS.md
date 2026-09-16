# Root Cause Analysis (RCA): Technical Defects, Investigations & Resolutions

**Document Version:** 1.0  
**Project:** Quantified AI Skill Pack & 50-Document Finance Benchmark  
**Author:** Anshul  
**Scope:** Chronological analysis of all technical bugs, environment discrepancies, algorithmic defects, and systemic fixes implemented during project execution.

---

## Executive Summary of Resolved Defects

| Bug ID | Title / Subsystem | Severity | Root Cause Summary | Resolution Status |
|---|---|---|---|---|
| **RCA-01** | PowerShell npm Script Execution Policy Restriction | Medium | Windows execution policy blocking `.ps1` execution wrapper | **RESOLVED** (`npm.cmd` invocation) |
| **RCA-02** | Python Windows Console Encoding (`cp1252` crash on Emojis) | Critical | Default Windows ANSI stdout stream failing on UTF-8 emojis | **RESOLVED** (`sys.stdout.reconfigure`) |
| **RCA-03** | Windows Path Validator False Positives on Root Web URLs | Critical | `os.path.isabs` returning `False` on `/path` on Windows | **RESOLVED** (Cross-platform URL filter) |
| **RCA-04** | Cohen's Kappa Marginal Inbalance / Zero Kappa Defect | High | Unincremented disagree marginals forcing $P_e = P_o$ | **RESOLVED** (Categorical contingency matrix) |
| **RCA-05** | Noisy Source Document Arithmetic Ambiguity in Extraction | Medium | Real-world document math errors conflicting with exact match | **RESOLVED** (Dual-tracking literal vs flag) |

---

## Detailed Root Cause Analysis Reports

### RCA-01: PowerShell Execution Policy Blocking `npm.ps1`

#### 1. Symptom & Error Output
When executing standard package manager commands like `npm run validate:strict` in the PowerShell terminal, the command failed immediately with:
```
npm : File C:\Program Files\nodejs\npm.ps1 cannot be loaded because running scripts is disabled on this system.
For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
+ npm -v
+ ~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

#### 2. Root Cause
On Windows systems, Node.js installs both an `npm.cmd` batch script and an `npm.ps1` PowerShell script in `C:\Program Files\nodejs\`. When `npm` is typed directly in PowerShell, PowerShell prioritizes the `.ps1` file. However, Windows PowerShell defaults to the `Restricted` execution policy, which prohibits executing unsigned scripts, triggering a fatal `PSSecurityException`.

#### 3. Corrective Action & Code Fix
Instead of relying on PowerShell's `.ps1` resolution, all npm tool invocations across automation scripts and terminal commands were explicitly redirected to `npm.cmd`:
```powershell
npm.cmd run validate:strict
npm.cmd run index
npm.cmd run catalog
npm.cmd run readme
```
This cleanly invokes the batch file directly, bypassing PowerShell script execution restrictions safely without requiring administrator privileges to alter system-wide security policies.

---

### RCA-02: Windows Console `cp1252` Character Encoding Crash on Emojis

#### 1. Symptom & Error Output
Executing repository validation or indexing scripts (`scripts/validate_skills.py`, `scripts/generate_index.py`, `scripts/update_readme.py`) crashed with:
```
Traceback (most recent call last):
  File "scripts\validate_skills.py", line 150, in <module>
    success = validate_skills(skills_path, strict_mode=args.strict)
  File "scripts\validate_skills.py", line 33, in validate_skills
    print(f"\U0001f50d Validating skills in: {skills_dir}")
  File "Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f50d' in position 0: character maps to <undefined>
```

#### 2. Root Cause
On Windows, Python 3 defaults standard output (`sys.stdout`) to the legacy Windows ANSI code page (`cp1252` / `charmap`) when running in certain non-UTF-8 console environments or when stdout is piped to an agent tool. When the scripts attempted to print terminal emojis (e.g. `🔍` `\U0001f50d`, `🏗️` `\U0001f3d7`, `✨`, `📖`, `🔢`), the `cp1252` character map threw a fatal `UnicodeEncodeError`.

#### 3. Corrective Action & Code Fix
Injected runtime stream reconfiguration at the entry point of all Python utility scripts (`scripts/validate_skills.py`, `scripts/generate_index.py`, `scripts/update_readme.py`, `scripts/run_finance_benchmark.py`):

```python
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
```

This dynamically switches stdout and stderr to native UTF-8 encoding on Windows, allowing all emojis and Unicode characters to output smoothly.

---

### RCA-03: Windows Path Validator False Positives on Root Web URLs

#### 1. Symptom & Error Output
Running `scripts/validate_skills.py` failed validation with 9 Critical Errors on the upstream skill `skills/competitor-alternatives/SKILL.md`:
```
❌ competitor-alternatives\SKILL.md: Dangling link detected. Path '/alternatives/notion' does not exist locally.
❌ competitor-alternatives\SKILL.md: Dangling link detected. Path '/alternatives/airtable' does not exist locally.
❌ competitor-alternatives\SKILL.md: Dangling link detected. Path '/alternatives/monday' does not exist locally.
...
```

#### 2. Root Cause
The link validation check in scripts/validate_skills.py was designed to find broken local file links (e.g., a relative file link like examples/sample.json). To avoid testing external links, it skipped absolute paths using:
```python
if os.path.isabs(link_clean):
    continue
```
On POSIX/Linux, web root URLs such as `[Notion Alternatives](/alternatives/notion)` start with `/`, so `os.path.isabs('/alternatives/notion')` evaluates to `True`.  
However, on Windows, `os.path.isabs('/alternatives/notion')` evaluates to `False` because Windows requires a drive letter (e.g., `C:\`) or UNC prefix (`\\`).  
Consequently, on Windows, the validator assumed `/alternatives/notion` was a relative local filesystem path, joined it with the local folder path, and reported a dangling link error when the file did not exist on disk.

#### 3. Corrective Action & Code Fix
Updated line 115 of `scripts/validate_skills.py` to explicitly treat root-relative URL paths starting with `'/'` as web URLs rather than local file paths:

```python
# Skip empty anchors, external links, root URLs, and edge cases
if not link_clean or link_clean.startswith(('http://', 'https://', 'mailto:', '<', '>', '/')):
    continue
if os.path.isabs(link_clean):
    continue
```

Immediately following this change, `python scripts/validate_skills.py --strict` passed with 0 errors across all skills.

---

### RCA-04: Cohen's Kappa Marginal Imbalance & Zero Kappa Defect

#### 1. Symptom & Error Output
In the initial execution of Step 6 in `scripts/run_finance_benchmark.py`, the double-annotated subset of 10 documents returned:
```
Double-annotated subset (10 docs): Observed Agreement = 97.2%, Cohen's Kappa = 0.0 (Substantial).
```
While observed agreement was $97.2\%$ (70 out of 72 fields matching), Cohen's $\kappa$ collapsed to $0.0000$.

#### 2. Root Cause
Cohen's Kappa is formulated as:
$$\kappa = \frac{P_o - P_e}{1 - P_e}$$
In the initial code, the calculation tracked agreements as:
```python
if matched:
    r1_agree += 1
    r2_agree += 1
else:
    r1_agree += 1  # BUG: Always incrementing r1_agree!
    r2_disagree += 1
```
Because `r1_agree` was incremented regardless of whether the fields matched or disagreed, Annotator 1 was assigned a positive marginal probability of $p_1 = 1.0$ ($100\%$).  
Under independent marginal probability multiplication:
$$P_e = (p_1 \times p_2) + ((1 - p_1) \times (1 - p_2)) = (1.0 \times P_o) + (0.0 \times \dots) = P_o$$
Because $P_e$ was forced to equal $P_o$, the numerator $P_o - P_e = P_o - P_o = 0.0$. This caused $\kappa$ to mathematically evaluate to 0.0 despite near-perfect agreement.

#### 3. Corrective Action & Code Fix
Re-architected `run_annotation_qa()` in `scripts/run_finance_benchmark.py` to evaluate categorical classification choices across four distinct label taxonomies:
1. `STANDARD_SCALAR`: Clean atomic values (dates, simple strings).
2. `COMPLEX_LINE_ITEMS`: Nested table arrays and transactions.
3. `ANOMALY_OR_FLAG`: Risk flags and known noisy stress fields.
4. `DISCREPANCY_VARIANT`: Valid annotator boundary divergences.

Marginal distributions were computed across all contingency matrix categories:
```python
total_items = len(items)
agreed = sum(1 for c1, c2 in items if c1 == c2)
po = agreed / total_items

categories = list(set([c1 for c1, _ in items] + [c2 for _, c2 in items]))
pe = 0.0
for cat in categories:
    p1 = sum(1 for c1, _ in items if c1 == cat) / total_items
    p2 = sum(1 for _, c2 in items if c2 == cat) / total_items
    pe += (p1 * p2)

kappa = round((po - pe) / (1 - pe), 4)
```
**Result After Fix**:
- Observed Agreement: $97.22\%$ ($P_o = 0.9722$)
- Expected Chance Agreement: $70.61\%$ ($P_e = 0.7061$)
- Calibrated Cohen's $\kappa = \mathbf{0.9055}$ (Categorized as **"Almost Perfect Agreement"** under the Landis & Koch standard).

---

### RCA-05: Source Document Arithmetic Discrepancies in Injected Noisy Datasets

#### 1. Symptom & Error Output
During extraction grading of `inv_10` and `inc_10`:
- In `inv_10`, subtotal ($3,300) + tax ($264) equaled $3,564, but the printed document explicitly stated total as `$3,574.00`.
- In `inc_10`, Operating Income ($470,000) minus effective taxes diverged by $1,000 from stated Net Income ($371,000).

An automated grader testing strict arithmetic equality would fail the extraction model if it extracted what was literally printed, or fail it if it computed the corrected sum.

#### 2. Root Cause
In real-world business paperwork, human errors exist inside the source documents. Per PRD §10, 20% of the benchmark documents were intentionally injected with stress conditions. Without a dual-tracking standard, the grader could not distinguish between a model hallucination and a model faithfully extracting a flawed document.

#### 3. Corrective Action & Code Fix
Standardized dual-tracking in `skills/finance-document-annotator/SKILL.md` and `scripts/run_finance_benchmark.py`:
1. **Extraction Contract**: The model must extract the literal printed token (`3574.00`), preserving document ground reality.
2. **Confidence Flagging**: The model lowers its confidence rating below $0.70$ (e.g. $0.65$) on fields that fail arithmetic balance equations.
3. **Audit Classification**: The discrepancy log classifies these as `CONF_CAUGHT` rather than extraction errors.

---

## Preventative Engineering & Quality Gates

To permanently prevent these classes of errors:
1. **Platform Independence**: All future scripts must include Windows UTF-8 reconfigure blocks and normalize web paths before invoking filesystem checks.
2. **Pre-flight CI Validation**: Running `npm.cmd run validate:strict` ensures zero metadata, link, or schema regressions before any pull request or merge.
3. **Statistical Invariant Testing**: Cohen's $\kappa$ calculations are guarded with sanity assertions ($0 \le P_e < P_o \le 1.0$).
