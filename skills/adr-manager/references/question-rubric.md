# Question rubric

Ask a follow-up question only if the answer changes the ADR materially.

## Ask the question when it changes

- whether the decision is new or just an update
- which alternatives should be evaluated
- the scope of affected systems
- migration or backward compatibility requirements
- security, privacy, or reliability implications
- whether the chosen option is actually acceptable

## Do not ask the question when the repository already answers it

Examples of facts that should usually be discovered from the repository first:

- current framework or library in use
- database engine already deployed
- whether feature flags exist
- whether background processing already exists
- names of modules, packages, or entry points

## Good question shapes

- binary distinction with impact
- scope clarification
- migration constraint clarification
- explicit choice among repository-grounded options

## Bad question shapes

- broad brainstorming with no decision impact
- asking the user to restate code facts
- asking for information that can safely remain an open question in the ADR

## Stop rule

If you can write a correct ADR draft with explicit open questions, stop asking and draft it.
