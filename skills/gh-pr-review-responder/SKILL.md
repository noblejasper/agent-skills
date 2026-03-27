---
name: gh-pr-review-responder
description: GitHub PR review threads—KEEP/DISCARD triage, replies, KEEP-only code changes, lint/test/push. Open PRs only; not for creating PRs (create-pr-jp).
metadata:
  author: noblejasper
  version: "1.2.1"
compatibility:
  - codex
  - cursor
---

# GitHub PR Review Responder

## Purpose

- **Evaluate** each review thread with **KEEP vs DISCARD** first ([references/keep-discard-rubric.md](references/keep-discard-rubric.md)) so **low-value or out-of-scope feedback** gets a **clear, respectful reply** without unnecessary code churn.
- **Only KEEP** items may lead to **implementation work**; **DISCARD** threads get a **reply that states the decision and criteria**, then **resolve** when appropriate.
- After **KEEP** code changes, **verify** and **push** per [ADR 0002](../../docs/adr/0002-git-workflow-skills-composition.md) (`pnpm lint && pnpm test` when defined).
- **SKILL.md stays in English**; **GitHub replies** match **reviewer language** ([references/reply-templates.md](references/reply-templates.md)).

## When to Use

- "PR レビュー対応", "review comments", "address feedback", `gh-pr-review-responder`, triage with KEEP/DISCARD.

## Do Not Use When

- **Opening or editing PR metadata only**—use **create-pr-jp**.
- **Commit/push only** without review—use **commit-jp** / **push**.
- Branch **behind base**—use **pull** first.

## Related Skills

- **push**: Publish commits after KEEP fixes.
- **pull**: Sync before push when needed.
- **commit-jp**: Japanese commits for fix commits if required.
- **create-pr-jp**: Does not apply to review threads; PR must already exist.

## Prerequisites

- **`gh`** authenticated; **Python 3** for scripts; **open PR** for current branch.

## Workflow

Run bundled scripts from the **skill root** (directory containing this `SKILL.md`): `python3 scripts/fetch_review_threads.py …` and `python3 scripts/reply_review_thread.py …`. From **this repo’s git root**, prefix with `skills/gh-pr-review-responder/`. If commands are not found, see [references/skill-root-resolution.md](references/skill-root-resolution.md).

1. **Auth**: `gh auth status`; stop if unauthenticated.

2. **Collect threads**:  
   `python3 scripts/fetch_review_threads.py --format markdown`  
   (Optional: `--include-resolved`, `--include-outdated`, `--pr NUMBER`.)

3. **KEEP vs DISCARD** (mandatory for each pending thread):  
   Use [references/keep-discard-rubric.md](references/keep-discard-rubric.md). For each comment:
   - **Factual accuracy** — read the actual code; note misunderstandings.
   - **Severity** — CRITICAL / IMPORTANT / LOW.
   - **Diff relevance** — does it target **this PR’s changed lines** (use `git diff <base>...HEAD` or equivalent; align with repo base branch).
   - **Actionability** — specific fix vs vague “consider…”.

4. **Decision**:
   - **DISCARD** if the rubric says so (LOW, wrong fact, out-of-diff, linter-only, vague, oscillation risk, etc.).  
     → **Reply only** using the **DISCARD** templates in [references/reply-templates.md](references/reply-templates.md); **do not** change product code **for this thread**. Resolve thread when suitable.
   - **KEEP** if CRITICAL/IMPORTANT, accurate, diff-relevant, and actionable (or KEEP with explanation if already fixed).  
     → Sub-triage:
     - **`needs_code_change`** — implement fix, then step 6.
     - **`keep_replied`** — explanation or “already in this PR”; no further code (templates §1–2).
     - **`needs_clarification`** — KEEP but cannot act without reviewer input (template §3).

5. **Post replies**:  
   `python3 scripts/reply_review_thread.py --thread-id <ID> --body-file ...`  
   Include **`Decision: KEEP`** or **`Decision: DISCARD`** and reasoning in the body (see the **§0** structure blocks in [references/reply-templates.md](references/reply-templates.md)). Top-level comments: `gh pr comment`. `--resolve` when the thread is complete.

6. **Checks + push** — run **only if** at least one **KEEP** thread required **`needs_code_change`**:
   1. **`pnpm lint && pnpm test`** when defined; else AGENTS.md / README / `package.json`.
   2. Fix until green; **commit** (commit-jp if required); **`git push`**.

7. **Post failures**: report command, stderr, draft text.

8. **Final report**: Counts **KEEP** / **DISCARD**; per thread `implemented` / `discard-replied` / `keep-replied-no-code` / `clarification` / `blocked`; files changed; checks; push result.

## Present Results to User

- **KEEP vs DISCARD** summary table or counts.
- Explicit statement: **no code was written solely for DISCARD threads**.

## Reply Quality Rules

- **DISCARD** replies must name **which criterion** failed (severity, fact, diff, actionability)—see rubric.
- **KEEP** replies tie to evidence: paths, commits, tests.
- Match **reviewer language**.

## Troubleshooting

| Situation | Action |
|-----------|--------|
| Scripts not found | [skill-root-resolution.md](references/skill-root-resolution.md) |
| Unsure KEEP vs DISCARD | Re-read rubric; if still ambiguous, **needs_clarification** (not DISCARD by default) |
| `gh` / GraphQL errors | See stderr; retry once |

## Resources

- [references/keep-discard-rubric.md](references/keep-discard-rubric.md) — **KEEP/DISCARD** criteria (source of truth).
- [references/reply-templates.md](references/reply-templates.md) — structures + EN/JP templates including **DISCARD**.
- [references/skill-root-resolution.md](references/skill-root-resolution.md) — path resolution if `scripts/...` fails.
- [scripts/fetch_review_threads.py](scripts/fetch_review_threads.py)
- [scripts/reply_review_thread.py](scripts/reply_review_thread.py)
