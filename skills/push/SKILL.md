---
name: push
description: Push the current branch to origin safely (lint, test, resolve non-fast-forward via pull skill, then push). Use when the user asks to push or publish commits to the remote. Does not create or edit PRs—use the create-pr-jp skill for that.
metadata:
  author: noblejasper
  version: "1.0.0"
compatibility:
  - codex
  - cursor
---

# Push

## Purpose

- Push the current branch to `origin` safely.
- Keep branch history clean when the remote has moved forward (coordinate with **pull** as needed).

## Prerequisites

- Git remote `origin` is configured and reachable.
- Credentials for `git push` work for this host (HTTPS or SSH).

## When to Use

- "pushして", "リモートに出して", "origin に push", or similar—when the user asks to push commits to the remote.

## Do Not Use When

- Only syncing or updating the local branch is needed (use the **pull** skill).
- The user wants a PR opened or updated (use the **create-pr-jp** skill—out of scope for this skill).

## Related Skills

- **pull**: When push is rejected or the branch is not cleanly synced (non-fast-forward, merge conflicts, branch behind remote).
- **create-pr-jp**: When the user wants to create or update a GitHub PR (Japanese title/body per repo rules).

## Procedure

1. Identify the current branch and inspect remote state (`git status`, `git remote -v`, `git fetch` as needed).
2. Run local checks before pushing: `pnpm lint` then `pnpm test` (or `pnpm lint && pnpm test`), unless the repo documents different pre-push checks.
3. Push to `origin`, setting upstream tracking if needed (`git push -u origin HEAD`).
4. If push fails or is non-fast-forward:
   - For non-fast-forward or sync issues: use the **pull** skill to merge or rebase per repo rules (`origin/main` or the appropriate base), resolve conflicts, re-run `pnpm lint && pnpm test`, then push again. Use `--force-with-lease` only when history was rewritten intentionally.
   - For auth, permissions, or host policy: do not rewrite the remote or change protocols; show the exact error and stop.

## Output

- A successful `git push` to `origin` for the current branch (and upstream set when first pushing the branch).

## Usage

Reference flow (adapt branch names and commands to the repo):

```sh
branch=$(git branch --show-current)

# Validation gate (lint then test; use repo-specific scripts if documented)
pnpm lint && pnpm test

# Push (with upstream tracking on first push)
git push -u origin HEAD

# If the remote moved: resolve via the pull skill, re-run `pnpm lint && pnpm test`, then:
# git push -u origin HEAD

# Auth/permission failures: show the error and stop—do not force-push to fix.

# Only after intentional history rewrite:
# git push --force-with-lease origin HEAD
```

## Present Results to User

- Confirm the branch name and that the push to `origin` succeeded.
- If push failed, report the exact error and what was tried (e.g. pull/rebase)—do not imply a PR was created or updated (that is **create-pr-jp**’s job).

## Notes

- Never use `--force`. Use `--force-with-lease` only as a last resort when history was intentionally rewritten.
- Distinguish sync issues from auth/permission issues: resolve the former with **pull**; for the latter, surface errors without changing remotes or protocols.

## Troubleshooting

| Situation | Action |
|-----------|--------|
| `non-fast-forward` / behind remote | **pull** skill → merge/rebase per repo rules → `pnpm lint && pnpm test` → push again |
| Credential / permission denied | Report verbatim; user fixes credentials or repo access—do not bypass with force push |
| Wrong remote or branch | Verify `git branch --show-current` and `origin` URL before pushing |
