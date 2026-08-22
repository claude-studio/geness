---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ010-001"
question_ids:
  - "OQ-010"
authority: "user"
recorded_at: "2026-08-22T16:04:00Z"
source: "Explicit AUTOPILOT delegation in the task prompt"
---

# User decision receipt — OQ-010

## Decision

The delegated autonomous-delivery policy adopts candidate C-01, the deterministic
evidence-gated lesson evaluator, with the fixture's reviewed threshold values.

- A structured fingerprint is promoted to `verified` after the same fingerprint is
  observed in two independent runs, or after reproducible fail-before/pass-after guard
  evidence. Duplicate observations in one run do not count as independent recurrence.
- A `candidate` or `probationary` lesson may expire only after three eligible
  unassisted successes, a minimum age of seven days, and no recurrence or guard-prevention
  evidence. Injected, ineligible and unrelated successes do not count; age alone does not
  expire a lesson.
- General retrieval exposes only `verified` or `enforced` lessons. Evaluator/rule version
  and the selected threshold profile remain part of the event lineage.

This is a delegated decision record; it does not fabricate an interactive user message.
The adoption is permitted by the task's AUTOPILOT rule because the packet recommendation
is clear, the required fixture assertions passed deterministically twice, no contradictory
lesson-lifecycle policy was found in repository evidence, and the choice remains within the
packet's docs/research scope.

## Rationale and evidence

`FX-MEMORY-RETENTION-BOOTSTRAP-001` returned exit `0` twice with 43/43 assertions and
`all_assertions_pass=true`. The paired current-worktree stdout comparison returned exit `0`
with SHA-256 `sha256:de54f8842b75bd1de711bbf0d309fff83b53010203ecf5b6945033b869565713`.
The retained projection hash is
`sha256:0e3e7e4ef2ae40c0b6e68673774afe7cc2d8b74a122fb38438d7ddf8371b2b07`.

The fixture observed first-failure isolation, independent recurrence and reproducible guard
promotion, eligible-only unassisted-success expiry, and deterministic replay. C-02 has no
fixture evidence and C-03 conflicts with the accepted candidate/memory boundary in ADR-0003.

## Unresolved scope

This receipt does not choose the production fingerprint schema or merge/split normalization,
event/SQLite tables, migration or writer/crash recovery, calibration beyond the selected
research thresholds, verified-lesson revocation, compiled-guard semantics or runtime
retention/bootstrap policy owned by OQ-011. It does not change the product-level
Implementation `HOLD` or authorize product scaffold creation.

## Linked artifacts

- [OQ-010 lesson-evaluator packet](../../OQ-010-lesson-evaluator.md)
- [ADR-0018](../../../../adr/0018-deterministic-lesson-evaluator.md)
- [current result manifest](./FX-MEMORY-RETENTION-BOOTSTRAP-001/RUN-OQ010-001/result.json)
- [fixture README](../../fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/README.md)
