---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ010-001"
question_ids:
  - "OQ-010"
authority: "user-delegated-autonomous-delivery"
recorded_at: "2026-08-22T16:07:07Z"
source: "Explicit AUTOPILOT delegation in the task prompt"
---

# User decision receipt — OQ-010

## Decision

The delegated autonomous-delivery policy adopts candidate C-01: lesson evaluation is
deterministic and evidence-gated. A structured fingerprint remains a runtime candidate
until either independent recurrence is observed in two distinct runs or reproducible
fail-before/pass-after guard evidence exists. General retrieval exposes only
`verified|enforced` lessons.

The initial threshold profile observed by the fixture is also adopted for the v1 policy
candidate: candidate/probationary expiry requires three eligible unassisted successes and
a minimum observation age of seven days, with no recurrence or guard-prevention evidence.
Same-run duplicate failures, ineligible exposures and lesson-injected successes do not
count as independent recurrence or unassisted success.

This is a delegated decision record; it does not fabricate an interactive user message.
The adoption is permitted by the task's AUTOPILOT rule because the packet recommendation
is clear, the required fixture assertions passed deterministically twice, no contradictory
evaluator policy was found in repository evidence, and the choice remains within the
packet's docs/research scope.

## Rationale and evidence

`FX-MEMORY-RETENTION-BOOTSTRAP-001` returned exit `0` twice with 43/43 assertions and
`all_assertions_pass=true`. Paired stdout comparison returned equality and the SHA-256
including the command's trailing newline was
`sha256:de54f8842b75bd1de711bbf0d309fff83b53010203ecf5b6945033b869565713`.
The projection hash was
`sha256:0e3e7e4ef2ae40c0b6e68673774afe7cc2d8b74a122fb38438d7ddf8371b2b07`.

The fixture kept the first failure out of retrieval, counted only independent recurrence,
excluded injected and ineligible success from expiry, and observed expiry after three
eligible unassisted successes plus the minimum age. It used synthetic input, no network
and no external writes.

## Unresolved scope

This receipt does not finalize fingerprint normalization or merge/split rules, production
event/SQLite schema, evaluator migration, calibration beyond the initial profile,
revocation/decay semantics for verified lessons, compiled/enforced transitions, or
Implementation `CLEAR`. Those remain later evidence and decision scope.

## Linked artifacts

- [OQ-010 packet](../../OQ-010-lesson-evaluator.md)
- [ADR-0018](../../../../adr/0018-deterministic-lesson-evaluator.md)
- [current execution record](../../OQ-010-lesson-evaluator.md#5-fixture-catalog-and-execution)
- [current result manifest](./FX-MEMORY-RETENTION-BOOTSTRAP-001/RUN-OQ010-001/result.json)
