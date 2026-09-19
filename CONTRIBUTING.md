# 🤝 Contributing Guide

This repo is an 11-skill personal portfolio project (built on top of a reused community skills scaffold — see [CHANGELOG.md](CHANGELOG.md) for the full origin note), not an actively-maintained multi-contributor project. It's MIT-licensed, so pull requests are welcome, but don't expect an active review queue.

---

## Quality Bar for New Skills

Every skill submitted should pass the **5-point check** (see `docs/QUALITY_BAR.md` for details):

1. **Metadata**: Correct frontmatter (`name`, `description`).
   - The `name` MUST exactly match the folder name.
   - The `description` MUST be concise (under 200 characters) and focus on WHEN to trigger the skill.
2. **Safety**: No harmful commands without "Risk" labels.
3. **Clarity**: Clear "When to use" section.
4. **Examples**: At least one copy-paste usage example.
5. **Actions**: Must define concrete steps, not just "thoughts".

---

## Local development setup

To run validation, index generation, and README updates locally:

1. **Node.js** (for catalog and installer): `npm ci`
2. **Python 3** (for validate, index, readme scripts): install dependencies with
   ```bash
   pip install -r requirements.txt
   ```
   Then you can run `npm run chain` (validate → index → readme) and `npm run catalog`.

**Validation:** The canonical validator is **Python** (`scripts/validate_skills.py`). Use `npm run validate` (or `npm run validate:strict` for CI-style checks). CI and PR checks rely on the Python validator only.

**npm audit:** CI runs `npm audit --audit-level=high`. To fix issues locally: run `npm audit`, then `npm update` or `npm audit fix` as appropriate; for breaking changes, update dependencies manually and run tests.

---

## How to Add a Skill

### Step 1: Choose Your Skill Topic

Ask yourself: "What do I wish my AI assistant knew better?"

### Step 2: Create the Folder Structure

Skills live in the `skills/` directory. Use `kebab-case` for folder names.

```bash
cd skills/
mkdir my-awesome-skill
cd my-awesome-skill
touch SKILL.md
```

### Step 3: Write Your SKILL.md

```markdown
---
name: my-awesome-skill
description: "Brief one-line description of what this skill does"
---

# Skill Title

## Overview

Explain what this skill does and when to use it.

## When to Use This Skill

- Use when [scenario 1]
- Use when [scenario 2]

## How It Works

Detailed step-by-step instructions for the AI...

## Examples

### Example 1

\`\`\`
code example here
\`\`\`

## Best Practices

- ✅ Do this
- ❌ Don't do this
```

### Step 4: Validate

```bash
npm run validate        # soft mode (warnings only)
npm run validate:strict # strict mode (what CI runs)
```

This checks:
- `SKILL.md` exists
- Frontmatter is correct
- Name matches folder name
- Quality bar checks passed

### Step 5: Submit

```bash
git add skills/my-awesome-skill/
git commit -m "feat: add my-awesome-skill"
git push origin my-branch
```

---

## Commit Message Guidelines

Use these prefixes:

- `feat:` - New skill or major feature
- `docs:` - Documentation improvements
- `fix:` - Bug fixes
- `refactor:` - Code improvements without changing functionality
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**

```
feat: add kubernetes-deployment skill
docs: improve getting started guide
fix: correct typo in stripe-integration skill
```

---

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- **No harmful content**: See `docs/SECURITY_GUARDRAILS.md`.
