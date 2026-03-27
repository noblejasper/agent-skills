# Turning a design doc into ADRs

Use this process when the user gives you a spec, design doc, or notes and wants ADRs.

## Step 1: Extract candidate decisions

Look for statements that imply long-lived choices such as:

- architecture or topology changes
- storage model decisions
- library or framework standardization
- protocol or API contract choices
- security, privacy, tenancy, or compliance posture
- rollout, migration, or compatibility strategy

Ignore sections that are only task breakdowns, timelines, or local implementation notes.

## Step 2: Split by decision boundary

Create separate ADR candidates when the document mixes distinct choices.

Typical split signals:

- one section changes data model, another changes runtime execution
- one section is accepted, another is still exploratory
- one section affects external contracts, another only affects internal implementation

## Step 3: Reconcile with repository evidence

Check whether each candidate decision is already covered by:

- existing ADRs
- current implementation
- configuration or infrastructure code
- repository docs

Mark each candidate as one of:

- new ADR needed
- update existing ADR
- not ADR-worthy
- blocked by missing information

## Step 4: Ask only the missing questions

For each blocked candidate, ask the minimum set of questions needed to determine:

- the actual decision
- the rejected alternatives
- the consequences and rollout impact

## Step 5: Draft with explicit traceability

For each ADR draft, include the source document path and any related ADR or code paths.

## Recommended response format for doc-ingest

For each candidate:

- Candidate title
- Why it appears ADR-worthy
- Related files and ADRs
- Missing information
- Recommended action: create / update / skip
