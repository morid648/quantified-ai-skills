# 🤝 Contributing Guide

Thanks for taking a look at this repo. This guide covers how to add a new skill, run the local tooling, and what the quality bar checks for.

---

## 🧐 The Quality Bar

**Critical for new skills:** every skill must pass the **5-Point Quality Check** (see `docs/QUALITY_BAR.md` for details), enforced by `scripts/validate_skills.py`:

1.  **Metadata**: Correct Frontmatter (`name`, `description`).
    - The `name` MUST exactly match the folder name.
    - The `description` MUST be concise (under 200 characters) and focus on WHEN to trigger the skill.
2.  **Safety**: No harmful commands without "Risk" labels.
3.  **Clarity**: Clear "When to use" section.
4.  **Examples**: At least one copy-paste usage example.
5.  **Actions**: Must define concrete steps, not just "thoughts".

On top of the standard bar, every skill in this pack also adds a `## Quantified Output` section with a worked numeric example and a machine-readable result block — see `prd.md` §4.

---

## Local development setup

To run validation, index generation, and README updates locally:

1. **Node.js** (for catalog and installer): `npm ci`
2. **Python 3** (for validate, index, readme scripts): install dependencies with
   ```bash
   pip install -r requirements.txt
   ```
   Then you can run `npm run chain` (validate → index → readme) and `npm run catalog`.

**Validation:** The canonical validator is **Python** (`scripts/validate_skills.py`). Use `npm run validate` (or `npm run validate:strict` for CI-style checks). The JavaScript validator (`scripts/validate-skills.js`) is legacy/optional and uses a different schema; CI and PR checks rely on the Python validator only.

**npm audit:** CI runs `npm audit --audit-level=high`. To fix issues locally: run `npm audit`, then `npm update` or `npm audit fix` as appropriate; for breaking changes, update dependencies manually and run tests.

---

## How to Add a New Skill

### Step 1: Choose Your Skill Topic

It should fit one of the four pillars (AI training & evaluation, context optimization, prompt engineering, AI annotation) and, per this pack's own quantified-output requirement, produce at least one numeric, reproducible metric — not just advice.

### Step 2: Create the Folder Structure

Skills live in the `skills/` directory. Use `kebab-case` for folder names.

```bash
cd skills/
mkdir my-new-skill
cd my-new-skill
touch SKILL.md
```

### Step 3: Write Your SKILL.md

```markdown
---
name: my-new-skill
description: "Brief one-line description of what this skill does"
risk: safe
source: self
---

# Skill Title

## When to Use

- Use when [scenario 1]
- Use when [scenario 2]

## How It Works

Detailed step-by-step instructions for the AI...

## Examples

### Example 1

\`\`\`
code example here
\`\`\`

## Quantified Output

Name the metric(s) this skill produces, the formula, and a worked numeric example.

## Limitations

- What this skill does *not* do
```

### Step 4: Validate

```bash
npm run validate        # soft mode (warnings only)
npm run validate:strict # strict mode (what CI runs)
```

This checks: `SKILL.md` exists, frontmatter is correct, name matches folder name, and every quality-bar item above passes.

### Step 5: Regenerate the index/catalog

```bash
npm run index    # regenerate skills_index.json
npm run catalog  # regenerate data/catalog.json
npm run readme   # regenerate the README skill listing
```

---

## Commit Message Guidelines

- `feat:` - New skill or major feature
- `docs:` - Documentation improvements
- `fix:` - Bug fixes
- `refactor:` - Code improvements without changing functionality
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

```
feat: add my-new-skill
docs: improve getting started guide
fix: correct typo in extraction-prompt-library-finance
```

---

## Code of Conduct

- Be respectful and constructive.
- **No harmful content**: see `docs/SECURITY_GUARDRAILS.md`.

See [docs/COMMUNITY_GUIDELINES.md](docs/COMMUNITY_GUIDELINES.md) for the full code of conduct.
