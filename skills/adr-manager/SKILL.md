---
name: adr-manager
description: Create, update, review, and reference architecture decision records (ADRs) in the current git repository. Use when the user asks messy design questions, wants a design doc turned into ADR draft(s), needs existing decisions checked before implementation, wants gaps surfaced before writing an ADR, or wants future sessions to reuse decisions consistently. Inspect repository code and docs first, ask only for missing decision-critical information, then produce or update ADR files using the repo’s ADR conventions or the defaults in references/.
metadata:
  author: noblejasper
  version: "1.0.0"
compatibility:
  - codex
  - cursor
---

# ADR Manager

## Purpose

- Turn vague design discussions into **durable ADRs** that future agents can reuse.
- Start from **repository evidence** (existing ADRs, code, config, tests, docs)—not assumptions.
- Ask follow-up questions only for information that **cannot** be recovered from the repo and that **materially** affects the decision.
- Write ADR prose in the **language of the current request** (the language the user is using in session), **or** match the **language of existing ADRs** in this repository when that is clearly established—prefer consistency across the ADR set over mixing languages without reason.

## When to Use

- "create an ADR", "ADR を書いて", "architecture decision", "design doc を ADR に"
- The user wants to **ingest** a spec/design doc into one or more ADRs (`doc-ingest`).
- The user wants to **query** what is already decided before coding (`adr-query`).
- The user wants to **update**, supersede, or clarify an existing ADR (`adr-update`).
- The user is **exploring** a technical choice and needs help shaping it (`decision-intake`).

## Do Not Use When

- The work is a **routine bugfix, refactor, or local implementation detail** with no durable architectural stake—prefer a ticket/PR description, not an ADR.
- The user only needs **git operations** (commit, push, PR)—use **commit-jp**, **push**, **create-pr-jp**, etc.
- The question is **purely factual** about existing code with no decision to record—answer from the repo without drafting an ADR unless the user asks for one.

## Overview

If multiple workflow modes apply, begin with the earliest prerequisite (e.g. `doc-ingest` before `adr-create` when a design doc maps to new ADRs).

## Workflow

Follow this sequence:

1. Detect the request type.
2. Discover repository ADR conventions and overrides.
3. Gather repository evidence.
4. Decide whether this should create a new ADR, update an existing ADR, or remain a non-ADR note.
5. Identify missing decision-critical information.
6. Ask focused questions if needed.
7. Draft or update ADR content.
8. Update supporting files when appropriate.
9. Return a concise summary of what changed, what remains open, and what future agents should read first.

## 1. Detect the request type

Classify the request into one primary mode:

- **decision-intake**: the user is talking loosely about a technical choice and wants help shaping the decision.
- **adr-create**: the user wants a new ADR.
- **adr-update**: the user wants an existing ADR revised, superseded, or clarified.
- **doc-ingest**: the user provides a design doc, spec, or notes and wants it turned into one or more ADRs.
- **adr-query**: the user wants to know what has already been decided and how that should affect current implementation.

If multiple modes apply, begin with the earliest prerequisite mode. Example: for a design doc that likely maps to new ADRs, do `doc-ingest` before `adr-create`.

## 2. Discover repository ADR conventions and overrides

Before drafting anything, search the repository in this order:

1. `.adr-manager.yaml`
2. `.adr-manager.yml`
3. `.ai/adr-manager.yaml`
4. `.ai/adr-manager.yml`
5. `docs/adr/README.md`
6. `docs/adr/index.md`
7. any existing ADR directory listed in [references/default-conventions.md](references/default-conventions.md)

If an override file exists, follow it. If multiple override files exist, prefer the first one in the list above unless one explicitly points to another source of truth.

If no override file exists, infer conventions from existing ADR files. If there are no ADR files, use the default conventions in [references/default-conventions.md](references/default-conventions.md).

## 3. Gather repository evidence

Inspect the repository before asking questions.

Prioritize these sources:

- existing ADRs on the same theme
- superseded or rejected ADRs
- code paths that will change
- interfaces, schemas, migrations, and feature flags
- tests that reveal intended behavior
- design docs, RFCs, or issue notes stored in the repository
- README, architecture docs, and module-level docs

Build a compact evidence summary for yourself with:

- current state
- constraints already encoded in code
- alternatives already discussed
- related decisions and conflicts
- unresolved questions

## 4. Decide whether this should be a new ADR, an update, or not an ADR

Create a **new ADR** when the decision changes architecture, system boundaries, data contracts, deployment/runtime model, major library/framework selection, security/privacy posture, or an important trade-off likely to matter later.

Prefer **updating an existing ADR** when the repository already has an ADR covering the same decision and the user is refining scope, changing status, or recording consequences.

Prefer a **non-ADR note** when the request is just a local implementation detail, routine refactor, bug fix, or one-off task that has little long-term architectural significance.

When the decision is borderline, say so explicitly and explain the recommendation.

## 5. Identify missing decision-critical information

Check whether the repository evidence answers these fields:

- context
- problem or tension
- decision
- options considered
- why rejected options were rejected
- consequences and trade-offs
- rollout or migration impact
- validation plan
- rollback or escape hatch
- status
- owners or stakeholders when relevant
- open questions that should remain open

Ask follow-up questions only for missing items that materially change the ADR.

## 6. Ask focused questions

When questions are needed:

- ask 3 to 7 questions maximum in one round
- ask only repository-grounded questions
- separate **must answer before drafting** from **can remain open in the ADR**
- offer provisional assumptions when possible

Good examples:

- "I found an existing PostgreSQL-first direction in ADR-0012, but this new proposal adds Elasticsearch. Is the goal full replacement, or search-only augmentation?"
- "The current code supports both sync and async job execution. Should this decision standardize on one path or preserve both behind a feature flag?"
- "I found no rollout notes. Should the ADR include a staged migration plan, or is this intended for greenfield only?"

Use [references/question-rubric.md](references/question-rubric.md) to decide whether a question is worth asking.

## 7. Draft or update ADR content

Use the repository's template if one exists. Otherwise use the template in [references/adr-template.md](references/adr-template.md).

### Language

- **Default**: Write the ADR body in the **same language as the user’s messages** in this session (e.g. Japanese if the user writes Japanese, English if they write English).
- **Repository alignment**: If the repo already has ADRs in a **consistent language**, match that language for new or updated ADRs so the corpus stays uniform—even when the current request is in another language, unless the user explicitly asks otherwise.
- If existing ADRs **mix languages**, follow the **dominant** language in the ADR directory you are editing, or the language of the **most relevant** ADR on the same theme; if unclear, ask once or state the assumption in the handoff.

Always preserve concrete why/why-not reasoning. Future coding agents need the rationale, not just the conclusion.

When drafting from a design doc, first split the document into separate decision units. Do not force unrelated choices into one ADR. Use the guidance in [references/doc-to-adr.md](references/doc-to-adr.md).

When information is still missing, write explicit placeholders only when they are decision-safe, such as:

- `Open question:`
- `Assumption:`
- `Needs confirmation:`

Do not invent rejected alternatives, rollout plans, or validation evidence.

## 8. Update supporting files when appropriate

When the repository uses an ADR index, catalog, or README, update it to include:

- ADR number and title
- current status
- supersedes/superseded-by links when relevant
- one-line summary

If the repository has no index and the default conventions are in use, create or update the index format described in [references/default-conventions.md](references/default-conventions.md).

If a decision supersedes another, preserve history instead of deleting old ADRs.

## 9. Return a concise implementation handoff

At the end, provide:

- what evidence you used
- whether you created a new ADR or updated an existing one
- what remains open
- which ADR(s) future coding agents should read first
- any implementation guardrails implied by the decision

## Output expectations by mode

### decision-intake

Return:

1. current understanding
2. related repository evidence
3. missing decision-critical questions
4. recommendation on whether this should become a new ADR, update an ADR, or stay a note

### adr-create

Return:

1. related ADRs and code evidence
2. any necessary clarification questions
3. a complete ADR draft or repository edit
4. index updates if applicable

### adr-update

Return:

1. the ADR being updated
2. what changed since the prior decision
3. updated status and rationale
4. cross-links to superseded or related ADRs

### doc-ingest

Return:

1. candidate ADR list extracted from the document
2. missing information per candidate
3. recommended split or merge of decision units
4. drafted ADRs for the candidates with enough confirmed information

### adr-query

Return:

1. the most relevant ADRs
2. how they constrain the current request
3. contradictions or stale decisions
4. whether a follow-up ADR is needed

## Present Results to User

- Lead with **what changed** (files created/updated) and **where** ADRs live in the repo.
- Give **one short handoff block**: evidence used, open questions, which ADR to read first, implementation guardrails.
- For multi-mode work, state the **mode** you used (`decision-intake`, `adr-create`, etc.).

## Quality bar

A good ADR produced by this skill should let a future coding agent answer all of these without rereading the whole repository:

- what problem were we solving
- what did we choose
- what alternatives were considered
- why did we reject them
- what consequences and trade-offs did we accept
- what code areas are expected to follow this decision
- what is still intentionally unresolved

## Constraints

- stay within the current git repository unless the user explicitly expands scope
- write ADR text in the **session language** or **aligned with existing ADRs** (see §7 Language); do not default to English when the repo or user context is elsewhere
- prefer repository evidence over user memory when they conflict; surface the conflict clearly
- do not silently overwrite an existing ADR when a superseding ADR would preserve history better
- do not collapse multiple major decisions into one ADR just because they came from one design doc
- do not ask questions already answered by code, docs, or existing ADRs

## Troubleshooting

| Situation | Action |
|-----------|--------|
| No ADR directory / conventions found | Apply [references/default-conventions.md](references/default-conventions.md); prefer creating `docs/adr/` if nothing exists |
| Override and existing ADRs disagree | Prefer explicit **override file** if present; otherwise document conflict and ask user |
| Design doc mixes many decisions | Split per [references/doc-to-adr.md](references/doc-to-adr.md); one major decision per ADR |
| User wants an answer without writing files | Use `adr-query` mode; still cite paths to ADRs in the repo |

## Resources

- [references/default-conventions.md](references/default-conventions.md) — fallback layout, numbering, naming, config overrides.
- [references/adr-template.md](references/adr-template.md) — default ADR structure.
- [references/doc-to-adr.md](references/doc-to-adr.md) — design docs → ADRs.
- [references/question-rubric.md](references/question-rubric.md) — which follow-up questions are worth asking.

There is **no required shell script** for this skill; the workflow is agent-driven. If the repository adds automation later, document it in the repo’s own README or `.adr-manager.yaml`.
