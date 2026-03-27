# Default ADR template

Use this template only when the repository does not provide one.

```md
# ADR NNNN: [Decision title]

- Status: proposed
- Date: YYYY-MM-DD
- Related: [ADR-0007], [PR-123], [doc path if relevant]
- Supersedes: [ADR-0003] 

## Context

Describe the problem, constraints, existing implementation, and why this decision matters now.

## Decision

State the decision in clear, implementation-relevant terms.

## Options considered

### Option A: [Name]

- Pros:
- Cons:
- Why not chosen:

### Option B: [Name]

- Pros:
- Cons:
- Why not chosen:

## Consequences

Describe expected benefits, trade-offs, and new constraints.

## Rollout / migration

Describe adoption plan, compatibility concerns, and sequencing.

## Validation

Describe how the team will know the decision worked.

## Rollback / escape hatch

Describe how to revert or limit blast radius if needed.

## Open questions

List only the questions that are intentionally unresolved.
```

## Guidance

- Keep `Context` grounded in repository evidence.
- Keep `Decision` specific enough that future implementation choices can follow it.
- Record rejected alternatives briefly but concretely.
- Use `Open questions` for unresolved items instead of hiding ambiguity.
- Omit sections only if the repository has a stricter template.
- **Language**: Write the ADR in the language the user is using in this session, or match the language of existing ADRs in the repository for consistency (see the main skill’s §7 Language).
