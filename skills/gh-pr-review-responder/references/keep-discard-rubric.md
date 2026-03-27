# KEEP vs DISCARD rubric

Use this **before** writing code or spending deep analysis on a thread. Goal: **only KEEP items** get implementation work; **DISCARD** items get a **respectful reply** that states the decision and criteria, then **resolve the thread** when appropriate.

## Evaluation criteria

### 1. Factual accuracy

Does the problem **actually exist** in the code? Check for:

- Context misunderstanding by the reviewer
- Missed type narrowing or guards
- Incorrect framework/API assumptions

### 2. Severity

- **CRITICAL**: Bugs, security issues, data loss, race conditions
- **IMPORTANT**: Correctness issues, substantial performance problems, insufficient error handling at system boundaries
- **LOW**: Style preferences, naming nits, overly cautious warnings, hypothetical edge cases unlikely in practice

### 3. Diff relevance

Does the comment address **code changed in this PR’s diff**? Evaluate **this branch’s changes**, not pre-existing code unless the review explicitly ties them to the change.

### 4. Actionability

Is there a **concrete, specific** fix? Reject driving work from vague notes (“consider refactoring”, “might be good to add”).

## Decision rules

### KEEP (may implement code and/or reply with assessment)

**All** of the following should hold:

- Severity is **CRITICAL** or **IMPORTANT**
- Factually **accurate** after checking source
- **Relevant** to the PR diff (or clearly tied to the change under review)
- **Actionable** with a clear fix or test

→ Then triage into **`needs_code_change`** or **`keep_no_code`** (accurate but already addressed / explanation suffices).

### DISCARD (reply + criteria only; no code for this feedback)

Reply with judgment when **any** of these apply:

- **LOW** severity
- **Factually incorrect** after source verification
- Style/formatting that **linters/formatters** should own
- Targets **code not in this PR’s diff** (unless reviewer explicitly scopes it to your change and it still fails relevance)
- Generic asks (“add tests”, “add docs”, “add comments”) **without** a concrete gap tied to this change
- **Vague or unactionable** suggestion
- Would **oscillate** with prior iterations on the same point

→ Post a **DISCARD reply** (see [reply-templates.md](reply-templates.md)), optionally **resolve** the thread. **Do not** change product code solely to satisfy DISCARD feedback.

## Reply shape (for both KEEP and DISCARD)

For each thread, the GitHub reply should include:

1. **Decision**: `KEEP` or `DISCARD`
2. **Short reasoning** (which criteria passed/failed)
3. **KEEP**: Factual assessment + concrete next step if implementing
4. **DISCARD**: Which rule applied (e.g. “LOW severity”, “outside this PR’s diff”)

Stay **respectful and decisive**; the goal is to filter noise without being dismissive.
