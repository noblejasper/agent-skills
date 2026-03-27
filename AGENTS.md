# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, Copilot, etc.) when working with code in this repository.

## Repository Overview

This repository is a collection of **Agent Skills** for AI coding assistants. Skills follow the [Agent Skills](https://agentskills.io/) format: packaged instructions (and optional scripts) that extend what agents can do in a project.

End users install skills from this repo (for example via `npx skills add` as documented in `README.md`). When editing here, keep `SKILL.md`, scripts, and `README.md` in sync.

Formal architecture decisions for this repository are recorded as **ADRs** under [docs/adr/](docs/adr/index.md). **When investigating** those decisions, **drafting or updating ADRs**, or **turning design questions into ADRs**, prefer the **`adr-manager`** skill (`skills/adr-manager/SKILL.md`) so you follow repo conventions, gather evidence from the tree, and keep ADRs consistent—rather than only opening Markdown files ad hoc. For a quick list of decisions, see [docs/adr/index.md](docs/adr/index.md). Keep `AGENTS.md` for lightweight, day-to-day pointers; **details and rationale live in ADRs.**

## Creating a New Skill

### Directory Structure

Each skill lives in its **own top-level directory** (kebab-case), alongside `README.md` and `SKILL_TEMPLATE.md`:

```
agent-skills/
  {skill-name}/           # kebab-case directory name
    SKILL.md              # Required: skill definition
    scripts/              # Optional: executable helpers
      {script-name}.sh    # Bash scripts (preferred when you need CLI automation)
    references/           # Optional: extra docs loaded on demand
```

There is no required `{skill-name}.zip` in-tree; zipping is optional if you need a distributable archive (see [Creating the Zip Package](#creating-the-zip-package)).

### Naming Conventions

- **Skill directory**: `kebab-case` (e.g., `gh-pr-review-responder`, `deploy-helper`)
- **SKILL.md**: Always uppercase, always this exact filename
- **Scripts**: `kebab-case.sh` (e.g., `fetch-logs.sh`, `deploy.sh`)

### SKILL.md Format

Use YAML front matter plus Markdown body. Start from `SKILL_TEMPLATE.md` in this repository.

### Best Practices for Context Efficiency

Skills are loaded on demand — typically only the skill **name** and **description** are visible until the agent decides the skill is relevant. To save context:

- **Keep SKILL.md under ~500 lines** — move long reference material to `references/` or separate files
- **Write a specific `description`** — include trigger phrases so activation is reliable
- **Use progressive disclosure** — link to supporting files that are read only when needed
- **Prefer scripts over huge inline shell blocks** — execution cost is mostly output, not the script body
- **Deep linking** — keep references one level deep from `SKILL.md` where possible

### Script Requirements

When you add or change Bash scripts:

- Use `#!/bin/bash` and `set -e` for fail-fast behavior
- Send human-oriented status lines to **stderr**: `echo "Message" >&2`
- Send machine-readable output (e.g. JSON) to **stdout** when the agent must parse results
- Use a cleanup `trap` for temporary files when you create any
- In docs, show both **repo-relative** paths (`bash scripts/foo.sh` from the skill dir) and **mounted** paths (`/mnt/skills/user/...`) where users might see either

### After Adding or Changing a Skill

1. Update `README.md` → **利用可能なスキル** (or the English section if you add one) with the new skill name and a short description.
2. If your workflow uses a lockfile for `npx skills` (e.g. `skills-lock.json` in this repo), update it according to your tooling.

### End-User Installation

Document these patterns (also reflected in `README.md`):

**From GitHub (skills CLI):**

```bash
npx skills add https://github.com/noblejasper/agent-skills --skill {skill-name}
```

**manual copy:**

```bash
cp -r {skill-name}/ ~/.claude/skills/
```

Adjust the destination if the user’s environment expects another folder (for example project-local `.agents/skills/`).

If a skill needs network access to specific domains, tell users to allow those domains in their product settings (e.g. Claude capability / allowlist settings).

## Learned User Preferences

## Learned Workspace Facts

Short reminders only—**full rationale, options considered, and consequences** are in the linked ADRs (use **`adr-manager`** when you need to explore or extend them).

- **Skill authoring (language & layout)**: Prefer English in `SKILL.md` for agent ergonomics; put Japanese user-facing rules in dedicated `*-jp` skills; split long detail into `references/`. See [ADR 0001](docs/adr/0001-skill-authoring-language-and-structure.md).
- **Git workflow skills**: Keep roles separate—`push` does not open/update PRs (`create-pr-jp` does); use `pull` to sync with the base branch; before push, run `pnpm lint && pnpm test` when those scripts exist. See [ADR 0002](docs/adr/0002-git-workflow-skills-composition.md).
