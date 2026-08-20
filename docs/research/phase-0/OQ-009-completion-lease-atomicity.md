---
packet_schema_version: 1
packet_id: "OQ-009"
question_id: "OQ-009"
title: "completion transaction과 writer lease release ordering"
status: "blocked"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T00:00:00Z"
---

# OQ-009 — completion and lease atomicity

## 1. Scope and authority

- Question: terminal checkpoint, projection과 writer lease release의 원자적 순서는 무엇인가?
- Phase/Gate: Phase 0 / decision packet
- Authority: user
- Allowed scope: synthetic terminal replay와 transaction-order candidate 비교
- Non-goals: production DB/schema, daemon, crash recovery implementation, ADR,
  scaffold와 user receipt 확정

## 2. Candidate orderings

| candidate | ordering | evidence |
| --- | --- | --- |
| C-01 | terminal checkpoint와 lease release를 같은 runtime transaction으로 기록 | unverified |
| C-02 | lease release 후 terminal checkpoint를 기록 | unverified |
| C-03 | project projection 후 runtime terminal/lease commit을 기록 | unverified |

No candidate is selected.

## 3. Observed replay

The fixture started with terminal_checkpoint=true, lease_active=true and completed=false.
The first replay yielded completed=true and lease_active=false. The second replay was
equality-equivalent, also completed=true and lease_active=false. Both runner executions
reported 7 assertions and all_assertions_pass=true.

This is a synthetic fixture observation of replay idempotency only. It is not proof of
any production transaction order or atomicity guarantee.

## 4. Commands and evidence

- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py (twice) → each exit 0
- both stdout JSON values parsed and compared equal

Hashes:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
- execution record: evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-001/RUN.md

## 5. Gaps and decision

The fixture does not reproduce a crash-point matrix, project-document projection
ordering, stale-writer takeover, heartbeat grace, or a production transaction. It does
not compare rollback/reconciliation behavior across candidate orderings.

OQ-009 remains pending user decision. No Runtime/Lifecycle ADR is created; product
Implementation remains HOLD and no Implementation CLEAR is claimed.
