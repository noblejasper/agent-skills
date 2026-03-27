---
name: pull
description: Merge the latest default branch (e.g. origin/main) into the current branch, resolve merge conflicts, and verify with pnpm lint && pnpm test. Merge-based sync (not rebase) unless the repo specifies otherwise. Use when syncing a feature branch with origin, after a non-fast-forward push, or when the branch is behind. Does not push or manage PRs—use push and create-pr-jp for those.
metadata:
  author: noblejasper
  version: "1.0.0"
compatibility:
  - codex
  - cursor
---

# Pull

## Purpose

- Bring the current branch up to date with the remote default branch (typically `origin/main`) using a **merge** (not rebase, unless AGENTS.md or team policy says otherwise).
- Resolve merge conflicts safely and verify with **`pnpm lint && pnpm test`** (or the repo’s documented checks).
- Prefer **rerere** and clear conflict styles so repeated conflicts are easier to handle.

## Prerequisites

- Git remote `origin` exists and points at the expected host.
- You know which branch is the integration base (usually `main`; use the repo’s default if different).

## When to Use

- "pullして", "main を取り込んで", "同期して", or similar—when the feature branch must match `origin/main` (or the team base branch).
- After **`git push` is rejected** with non-fast-forward, or when the local branch is **behind** the remote tracking branch.
- When preparing to push and the branch needs the latest upstream changes first (often chained before **push**).

## Do Not Use When

- The user only wants to **push** without merging the base (use **push**; if push fails, then use **pull**).
- The user wants to **create or update a GitHub PR** (use **create-pr-jp**).
- The goal is **merging or landing an approved PR** on the default branch (use a **land** or merge workflow skill if the workspace defines one—not this skill).

## Related Skills

- **push**: After sync and green checks, publish commits to `origin`.
- **create-pr-jp**: Open or update a PR; out of scope for **pull**.

## Procedure

1. Ensure the working tree is safe to merge: **commit or stash** uncommitted work before merging.
2. Enable **rerere** locally (recommended):
   - `git config rerere.enabled true`
   - `git config rerere.autoupdate true`
3. Confirm **remotes and branch**: `origin` exists; the current branch is the one that should receive the merge.
4. **Fetch**: `git fetch origin`
5. **Fast-forward the current branch** from its remote counterpart if it exists (picks up remote-only commits before merging main):
   - `git pull --ff-only origin "$(git branch --show-current)"`
6. **Merge the base branch** (replace `main` if the repo uses another default):
   - Prefer `git -c merge.conflictstyle=zdiff3 merge origin/main` for clearer conflict context.
7. If conflicts appear, resolve them (see **Conflict Resolution** below), then:
   - `git add <files>`
   - `git commit` or `git merge --continue` as appropriate.
8. Verify: run **`pnpm lint && pnpm test`**, or follow `AGENTS.md` / project scripts if they differ.
9. Summarize for the user: hardest conflicts, how they were resolved, and any follow-ups.

## Output

- Current branch contains the merged base; conflicts resolved; **`pnpm lint && pnpm test`** (or repo equivalent) passed.
- A clear narrative of what was merged and any notable resolution decisions.

## Usage

Reference flow (adapt `main` / branch names to the repo):

```sh
git config rerere.enabled true
git config rerere.autoupdate true

git fetch origin

# Optional: sync remote feature branch commits first
git pull --ff-only origin "$(git branch --show-current)"

# Merge default branch (zdiff3 for conflict readability)
git -c merge.conflictstyle=zdiff3 merge origin/main

# After resolving conflicts:
# git add … && git commit   # or git merge --continue

pnpm lint && pnpm test
```

## Conflict Resolution

- Inspect before editing:
  - `git status` for conflicted files; `git diff` / `git diff --merge` for hunks.
  - Optional: `git diff :1:path :2:path` and `:1:` vs `:3:` for base vs ours/theirs.
  - With `merge.conflictstyle=zdiff3`, markers are `<<<<<<<` ours, `|||||||` base, `=======`, `>>>>>>>` theirs.
  - Infer intent on both sides; choose semantics first, then edit code.
- Prefer **minimal, intention-preserving** edits aligned with the branch’s purpose.
- Resolve in batches; **rerun `pnpm lint && pnpm test`** after a logical batch of files when helpful.
- Use **ours/theirs** only when one side should win entirely.
- **Generated files**: fix sources first, then regenerate with the project’s command; stage regenerated output.
- **Import conflicts**: if unclear, temporarily keep both imports, finish the merge, then let lint/typecheck trim unused imports.
- After resolution: `git diff --check` (no conflict markers left).

## When to Ask the User

Ask only when there is no safe default. Prefer a documented decision and proceed otherwise.

Ask when:

- Product behavior cannot be inferred from code, tests, or docs.
- The conflict affects a public API, migration, or contract with no clear safe choice.
- Two designs are equally plausible with no local signal.
- The change risks data loss, schema damage, or irreversible effects without a safe default.
- The branch or remote names cannot be determined locally.

Otherwise complete the merge, note assumptions briefly, and leave reviewable history.

## Present Results to User

- State the base branch merged (e.g. `origin/main`) and the current branch name.
- List major conflict areas and how they were fixed.
- Report **`pnpm lint && pnpm test`** (or what ran) and pass/fail.
- Do **not** claim a PR was updated or that commits were pushed—those are **create-pr-jp** and **push**.

## Notes

- Default integration strategy here is **merge**; do not rebase unless the repository explicitly requires it.
- If `git pull --ff-only origin <branch>` fails, diagnose (diverged history) before merging `origin/main`.

## Troubleshooting

| Situation | Action |
|-----------|--------|
| Dirty working tree | Commit or stash before merge |
| `merge` conflicts | Follow **Conflict Resolution**, then `pnpm lint && pnpm test` |
| Wrong default branch name | Use `git symbolic-ref refs/remotes/origin/HEAD` or repo docs for `main` vs `master` |
| Lint/test fails after merge | Fix or revert; do not push broken state—coordinate with **push** only after green checks |
