# Skill root — only when `scripts/...` fails

Read this **after** trying [Agent Skills](https://agentskills.io/skill-creation/using-scripts.md) defaults: CWD = skill directory, **`python3 scripts/<name>.py`**.

## Quick tries

1. **`cd`** to the folder that contains this file’s parent `SKILL.md` and `scripts/`, then `python3 scripts/fetch_review_threads.py --format markdown`.
2. From a **git repo root** (e.g. this monorepo):  
   `python3 skills/gh-pr-review-responder/scripts/fetch_review_threads.py --format markdown`
3. If the client sets **`SKILL_ROOT`** or **`AGENT_SKILL_DIR`**, use `"$SKILL_ROOT/scripts/..."`.

## Absolute path search (first match wins)

1. `$SKILL_ROOT` / `$AGENT_SKILL_DIR`
2. `$(git rev-parse --show-toplevel)/skills/gh-pr-review-responder`
3. `$(git rev-parse --show-toplevel)/.agents/skills/gh-pr-review-responder`
4. `$(git rev-parse --show-toplevel)/.cursor/skills/gh-pr-review-responder`
5. `$HOME/.codex/skills/gh-pr-review-responder`
6. `$HOME/.cursor/skills/gh-pr-review-responder`
7. Mount-style paths (e.g. `/mnt/skills/user/gh-pr-review-responder`)

Do **not** use **`CODEX_HOME`** (or similar) as the primary locator—not all agents define it.

```bash
python3 "$SKILL_ROOT/scripts/fetch_review_threads.py" --format markdown
```
