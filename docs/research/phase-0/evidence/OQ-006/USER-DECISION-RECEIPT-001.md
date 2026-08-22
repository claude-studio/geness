---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ006-001"
question_ids:
  - "OQ-006"
authority: "user"
recorded_at: "2026-08-22T14:33:16Z"
source: "Explicit AUTOPILOT delegation in the task prompt"
---

# User decision receipt — OQ-006

## Decision

The delegated autonomous-delivery policy adopts candidate C-01, portable Markdown
frontmatter with runtime SQLite as the mutable-state owner.

- Task Markdown frontmatter and body remain the human-readable, Git-portable
  contract/projection. They do not become a home runtime log or evidence store.
- Runtime SQLite is the canonical owner for mutable task state, revision guards,
  attempts, leases, verdicts and evidence freshness.
- Writes use the current revision/digest precondition; a stale write is denied without
  mutating current state.
- Project document updates use operation IDs and idempotent reconciliation. A document
  projection is not completion authority.

This is a delegated decision record; it does not fabricate an interactive user message.
The adoption is permitted by the task's AUTOPILOT rule because the packet recommendation
is clear, the required fixture assertions passed deterministically twice, no contradictory
schema-owner evidence was found, and the choice remains within the packet's delegated
docs/research scope. The known historical A-001/A-004 envelope mismatch is retained as
evidence projection drift, not treated as a semantic contradiction.

## Rationale and evidence

The `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` fixture passed twice with exit `0`, 30/30
assertions and `all_assertions_pass=true`. The paired stdout comparison returned exit `0`
and the current stdout SHA-256 was
`sha256:4adfd380c2f0094803b2b3645a330b5645472418a7ea6ea8953d32398626f051`.
The observation covered frontmatter/SQLite semantic and body round-trip, accepted revision
write, stale revision denial without mutation and the portable/runtime boundary. C-02 and
C-03 remain deferred because their product alternatives were not exercised and conflict
with the accepted portable/local ownership boundary.

## Unresolved scope

This receipt does not choose exact frontmatter grammar, production table/column/index or
migration details, cross-runtime serializer/hash rules owned by OQ-007, crash recovery
owned by later OQ-009/implementation evidence, project ID generation or workspace registry.
It does not change the current product-level Implementation `HOLD`.

## Linked artifacts

- [OQ-006 schema-lineage packet](../../OQ-006-schema-lineage.md)
- [ADR-0016](../../../../adr/0016-schema-lineage-and-projection-ownership.md)
- [RUN-OQ006-003](./FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ006-003/RUN.md)
- [current result manifest](./FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ006-003/result.json)
