---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ010-001"
question_ids:
  - "OQ-010"
authority: "user"
recorded_at: "2026-08-22T16:06:44Z"
source: "Explicit user instruction in the current conversation: 진행해"
---

# User decision receipt — OQ-010

## Decision

The user instruction `진행해` adopts candidate C-01, the deterministic
evidence-gated lesson evaluator, with the fixture's initial threshold values:

- independent recurrence: 2 distinct runs, or reproducible deterministic guard evidence;
- expiry: 3 eligible unassisted successes plus a minimum observation age of 7 days;
- general retrieval: expose only `verified` or `enforced` lessons;
- injected, ineligible and unrelated successes do not count as unassisted success, and
  same-run duplicates do not count as independent recurrence.

This receipt records the exact user instruction and does not fabricate an interactive user
message. The instruction followed the blocker explanation that OQ-010 had a clear C-01
recommendation, deterministic fixture evidence and a pending user authority receipt.

## Rationale and evidence

`FX-MEMORY-RETENTION-BOOTSTRAP-001` passed twice with exit `0`, 43/43 assertions and
`all_assertions_pass=true`. The paired replay was equality-equivalent; the current
revalidation recorded `cmp=0`, raw stdout SHA-256
`sha256:de54f8842b75bd1de711bbf0d309fff83b53010203ecf5b6945033b869565713` and projection
hash `sha256:0e3e7e4ef2ae40c0b6e68673774afe7cc2d8b74a122fb38438d7ddf8371b2b07`.
The fixture directly observed candidate isolation, independent recurrence, reproducible
guard promotion and eligible-only expiry. C-02 was not executed and C-03 is a negative
control; neither is selected.

## Unresolved scope

This receipt does not choose production event/SQLite schema, merge/split normalization,
evaluator implementation or migration, revocation/compiled semantics, concurrent writer
arbitration, calibration dataset, runtime retention or memory bootstrap policy. It does not
change the product-level Implementation `HOLD`.

## Linked artifacts

- [OQ-010 lesson-evaluator packet](../../OQ-010-lesson-evaluator.md)
- [ADR-0018](../../../../adr/0018-learning-evaluator-thresholds.md)
- [RUN-OQ010-001 result manifest](./FX-MEMORY-RETENTION-BOOTSTRAP-001/RUN-OQ010-001/result.json)
