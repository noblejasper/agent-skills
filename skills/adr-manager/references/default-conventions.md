# Default ADR conventions

Use these defaults only when the repository does not define its own ADR conventions.

## Language

- Prefer the **user’s session language** for new ADR prose, or the **language already used in existing ADRs** in this repo for consistency.
- If the repo has no ADRs yet, follow the language of the request or design doc being ingested.

## Default search order for ADR directories

Check these directories in order:

1. `docs/adr/`
2. `adr/`
3. `docs/architecture/adr/`
4. `docs/decisions/`
5. `architecture/decisions/`

Use the first directory that already contains ADRs. If none exist, default to `docs/adr/`.

## Default numbering

Use four-digit, zero-padded sequential numbers.

Examples:

- `0001-use-postgresql-for-primary-storage.md`
- `0002-adopt-queue-based-email-delivery.md`

Determine the next number from existing ADR filenames in the active ADR directory.

## Default filename format

`NNNN-kebab-case-title.md`

Use concise, decision-oriented titles.

Prefer:

- `0017-adopt-event-outbox-pattern.md`
- `0018-standardize-background-jobs-on-sidekiq.md`

Avoid vague titles like:

- `0017-notes.md`
- `0018-about-background-jobs.md`

## Default status values

Use one of:

- `proposed`
- `accepted`
- `superseded`
- `rejected`
- `deprecated`

Reuse repository-native status values if they already exist.

## Default index file

If no index exists, create or update `docs/adr/index.md` with a simple table:

| ADR | Status | Title | Summary |
| --- | --- | --- | --- |
| 0001 | accepted | Use PostgreSQL for primary storage | Standardize transactional data on PostgreSQL. |

## Repository override file

Preferred override file names:

- `.adr-manager.yaml`
- `.adr-manager.yml`
- `.ai/adr-manager.yaml`
- `.ai/adr-manager.yml`

Suggested schema:

```yaml
adr:
  directory: docs/adr
  index_file: docs/adr/index.md
  numbering:
    width: 4
    strategy: sequential
  filename:
    pattern: "{number}-{slug}.md"
  status_values:
    - proposed
    - accepted
    - superseded
    - rejected
    - deprecated
  template_file: docs/adr/template.md
  read_paths:
    - docs/adr
    - docs/architecture
    - README.md
  update_index: true
```

Treat this schema as guidance, not a hard contract. If the repository uses a different but clear structure, follow the repository.
