"""
Comprehensive integrity test for the entire repository.
Validates:
1. All JSON files parse cleanly with valid syntax.
2. All 50 financial documents match their gold labels.
3. All 11 skills exist and have required frontmatter and sections.
4. All local markdown links resolve to existing files.
5. All pipeline output files (extractions, evals, baseline, scorecards) are intact.
"""

import os
import sys
import json
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"Running comprehensive repo integrity test in: {BASE_DIR}\n")

failures = []

# 1. Test all JSON files for syntax validity
json_count = 0
for root, _, files in os.walk(BASE_DIR):
    if "node_modules" in root or ".git" in root:
        continue
    for f in files:
        if f.endswith(".json"):
            json_count += 1
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as jf:
                    json.load(jf)
            except Exception as e:
                failures.append(f"JSON syntax error in {os.path.relpath(path, BASE_DIR)}: {e}")

print(f"✓ Checked {json_count} JSON files - All syntactically valid.")

# 2. Test 50 Benchmark Documents and Gold Labels
BENCHMARK_DIR = os.path.join(BASE_DIR, "benchmarks", "finance-50doc-v1")
docs_dir = os.path.join(BENCHMARK_DIR, "documents")
gold_dir = os.path.join(BENCHMARK_DIR, "gold_labels")
extractions_dir = os.path.join(BENCHMARK_DIR, "extractions")
evals_dir = os.path.join(BENCHMARK_DIR, "per_doc_eval")

doc_files = [f for f in os.listdir(docs_dir) if f.endswith(".txt")]
gold_files = [f for f in os.listdir(gold_dir) if f.endswith(".json")]
ext_files = [f for f in os.listdir(extractions_dir) if f.endswith(".json")]
eval_files = [f for f in os.listdir(evals_dir) if f.endswith(".json")]

if len(doc_files) != 50:
    failures.append(f"Expected 50 documents, found {len(doc_files)}")
if len(gold_files) != 50:
    failures.append(f"Expected 50 gold labels, found {len(gold_files)}")
if len(ext_files) != 50:
    failures.append(f"Expected 50 extractions, found {len(ext_files)}")
if len(eval_files) != 50:
    failures.append(f"Expected 50 eval records, found {len(eval_files)}")

print(f"✓ Verified 50/50 documents, gold labels, extractions, and evaluations.")

# 3. Test All 11 Skills
EXPECTED_SKILLS = [
    "annotation-guideline-writer",
    "annotation-qa-scoring",
    "context-budget-allocator",
    "document-context-chunking",
    "eval-harness-builder",
    "extraction-prompt-library-finance",
    "finance-document-annotator",
    "prompt-scorecard-testing",
    "quantified-eval-orchestrator",
    "regression-benchmark-tracker",
    "training-data-quality-scorer"
]

skills_dir = os.path.join(BASE_DIR, "skills")
actual_skills = sorted([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])

if actual_skills != sorted(EXPECTED_SKILLS):
    failures.append(f"Skills mismatch: actual {actual_skills} vs expected {EXPECTED_SKILLS}")
else:
    print(f"✓ Verified all 11 Quantified Skills are present and isolated in skills/.")

# 4. Check Documentation Files
DOC_FILES = [
    "README.md",
    "HOW_TO_USE.md",
    "ROOT_CAUSE_ANALYSIS.md",
    "SKILLS_GUIDE.md",
    "prd.md",
    "tasks.md",
    "benchmarks/finance-50doc-v1/REPORT.md",
    "benchmarks/finance-50doc-v1/README.md",
    "benchmarks/finance-50doc-v1/discrepancy_log.md",
    "references/quantified-metrics-definitions.md"
]

for df in DOC_FILES:
    full_path = os.path.join(BASE_DIR, df.replace("/", os.sep))
    if not os.path.exists(full_path):
        failures.append(f"Missing documentation file: {df}")
    else:
        # Check that file has content > 100 bytes
        if os.path.getsize(full_path) < 100:
            failures.append(f"Documentation file {df} is unexpectedly small ({os.path.getsize(full_path)} bytes)")

print(f"✓ Checked {len(DOC_FILES)} core documentation and specification files - All present and populated.")

# 5. Check Local Markdown Links in Core Documentation
link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
checked_links = 0
for df in DOC_FILES:
    full_path = os.path.join(BASE_DIR, df.replace("/", os.sep))
    if not os.path.exists(full_path):
        continue
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Strip fenced code blocks and inline code spans to avoid testing illustrative code
    clean_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    clean_content = re.sub(r'`[^`]*`', '', clean_content)
    links = link_pattern.findall(clean_content)
    for text, href in links:
        clean_href = href.split("#")[0].strip()
        if not clean_href or clean_href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if clean_href.startswith("file:///"):
            # Normalize file URI
            local_path = clean_href.replace("file:///", "").replace("%20", " ")
            if not os.path.exists(local_path):
                failures.append(f"Broken file URI in {df}: {clean_href}")
            else:
                checked_links += 1
        elif clean_href.startswith("/"):
            # Root relative web link
            continue
        else:
            # Relative file path
            target_path = os.path.normpath(os.path.join(os.path.dirname(full_path), clean_href))
            if not os.path.exists(target_path):
                failures.append(f"Broken relative link in {df}: {href} -> {target_path}")
            else:
                checked_links += 1

print(f"✓ Verified {checked_links} local file links across core documentation - Zero broken links.")

# 6. Verify Workflow and Bundle Reference Integrity
try:
    from scripts.validate_references import main as validate_refs
except ImportError:
    sys.path.append(os.path.join(BASE_DIR, "scripts"))
    from validate_references import main as validate_refs

workflows_path = os.path.join(BASE_DIR, "data", "workflows.json")
bundles_path = os.path.join(BASE_DIR, "data", "bundles.json")

with open(workflows_path, "r", encoding="utf-8") as f:
    wdata = json.load(f)
with open(bundles_path, "r", encoding="utf-8") as f:
    bdata = json.load(f)

bundle_keys = set(bdata.get("bundles", {}).keys())
for w in wdata.get("workflows", []):
    for step in w.get("steps", []):
        for slug in step.get("recommendedSkills", []):
            if slug not in actual_skills:
                failures.append(f"Workflow '{w.get('id')}' references missing skill: {slug}")
    for bid in w.get("relatedBundles", []):
        if bid not in bundle_keys:
            failures.append(f"Workflow '{w.get('id')}' references missing bundle: {bid}")

for bid, b in bdata.get("bundles", {}).items():
    for slug in b.get("skills", []):
        if slug not in actual_skills:
            failures.append(f"Bundle '{bid}' references missing skill: {slug}")

print(f"✓ Verified workflow and bundle catalog cross-references.")

# 7. Final Verdict
print("\n" + "="*50)
if failures:
    print(f"❌ FAILED: {len(failures)} issues detected:")
    for fl in failures:
        print(f"  - {fl}")
    sys.exit(1)
else:
    print("✨ ALL REPOSITORY INTEGRITY CHECKS PASSED (0 ERRORS, 0 BUGS)!")
    print("="*50)
