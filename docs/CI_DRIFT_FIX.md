# 🔄 CI Drift Fix & Registry Synchronization Guide

> **Instructions for synchronizing skills indices, catalogs, and documentation when skills are added or updated.**

---

## 1. Problem Overview

When skills or metadata in `skills/` are modified, generated registry files (`skills_index.json`, `CATALOG.md`, `data/catalog.json`, `data/bundles.json`, `README.md`) must be regenerated to prevent CI drift failures.

### CI Error Example
```
❌ Detected uncommitted changes produced by registry/readme/catalog scripts.
```

---

## 2. Step-by-Step Fix Procedure

Run the complete build chain locally before pushing changes:

```bash
# 1. Run the strict validation and generation build chain
npm run build

# 2. Check git status for modified registry files
git status

# 3. Verify all tests and integrity checks pass
npm test

# 4. Commit and push any updated registry files
git add skills_index.json data/catalog.json data/bundles.json CATALOG.md README.md
git commit -m "chore: sync generated registry and index files"
git push
```

---

## 3. Scripts Executed in Build Chain

`npm run build` executes the following sequence:
1. `npm run validate:strict` (`python3 scripts/validate_skills.py --strict`)
2. `npm run index` (`python3 scripts/generate_index.py`)
3. `npm run readme` (`python3 scripts/update_readme.py`)
4. `npm run catalog` (`node scripts/build-catalog.js`)
