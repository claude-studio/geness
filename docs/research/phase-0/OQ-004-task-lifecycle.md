---
packet_schema_version: 1
packet_id: "OQ-004"
question_id: "OQ-004"
title: "task lifecycle state transition과 FAILED/CANCELLED 의미"
status: "resolved"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-22T19:08:56+09:00"
---

# OQ-004 — task lifecycle state transition

## 1. Scope and authority

- Question: exact allowed/denied task transitions과 FAILED/CANCELLED recovery 의미는 무엇인가?
- Phase/Gate: Phase 0 / decision packet
- Authority: user
- Allowed scope: current lifecycle proposal을 합성 fixture로 관찰하고 candidate를 비교
- Non-goals: product language, package manager, runtime, production schema, scaffold와
  production enforcement evidence

## 2. Candidate transition policies

| candidate | FAILED | CANCELLED | evidence |
| --- | --- | --- | --- |
| C-01 | explicit user reopen 후 REOPENED | terminal | observed + selected |
| C-02 | explicit user reopen 후 REOPENED | explicit reopen 가능 | inferred |
| C-03 | terminal | terminal | inferred |

C-01 is selected by the [user decision receipt](./evidence/OQ-004/USER-DECISION-RECEIPT-001.md)
and [ADR-0013](../../adr/0013-task-lifecycle-recovery.md). C-02 and C-03 are not selected.

| transition case | observed result | reason |
| --- | --- | --- |
| INITIALIZING → INTERVIEWING | ALLOWED | fixture_rule |
| PLAN_APPROVED → RUNNING with stale digest | DENIED | stale_digest |
| INTERVIEWING → RUNNING | DENIED | edge_not_allowed |
| FAILED → REOPENED | candidate-dependent | initial run did not separately assert this edge |

The follow-up candidate comparison is recorded in
[`RUN-OQ004-002`](./evidence/OQ-004/FX-LIFECYCLE-RECOVERY-002/RUN-OQ004-002/RUN.md).
It independently exercises the recovery cases that the first minimal run only described:

| observation | C-01 | C-02 | C-03 |
| --- | --- | --- | --- |
| `FAILED → REOPENED` with explicit user receipt | ALLOWED | ALLOWED | DENIED, terminal |
| `CANCELLED → REOPENED` with explicit user receipt | DENIED, terminal | ALLOWED | DENIED, terminal |
| reopen without explicit user receipt | DENIED | DENIED | DENIED |

The same follow-up observes attempt-level `FAIL` remaining distinct from task-level
`FAILED`, the synthetic completion order `READY_TO_COMPLETE` → final run projection →
terminal checkpoint → lease release → `COMPLETED` exposure, completion exposure being
denied without a terminal checkpoint or with an active lease, and a failure candidate
remaining unverified and hidden from general memory query before independent evidence. The
fixture compares candidates; the subsequent user receipt selects C-01.

## 3. Commands and evidence

- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- same runner command second run → exit 0
- each run reported 7 assertions and all_assertions_pass=true
- parsed JSON values from both runs compared equal
- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/runner.py → exit 0 twice
- each follow-up run reported 14 assertions and all_assertions_pass=true
- follow-up raw JSON values compared equal with cmp

Hashes:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
- execution record: evidence/OQ-004/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ004-001/RUN.md
- follow-up runner.py: 2410d4744e1db936812edcd12e2647ea0ce833d12b21adfda24ddade42369e5f
- follow-up input/fixture.json: 8afb0ce03084e75802d035ead7d7bf3ce073408fa100db0c803ad7185612121a
- follow-up execution record: evidence/OQ-004/FX-LIFECYCLE-RECOVERY-002/RUN-OQ004-002/RUN.md

## 4. Limitations and pending decisions

The original minimal fixture did not independently assert FAILED recovery or CANCELLED
behavior. The follow-up compares those candidate policies and exercises the completion and
candidate-memory guards, but it does not reproduce the complete canonical state graph,
production persistence, crash replay, lease takeover, verifier authority or Plan Gate actor
policy.

OQ-004 recovery policy is resolved as C-01 by the user receipt and [ADR-0013](../../adr/0013-task-lifecycle-recovery.md).
The full state graph, Plan Gate approval actor, completion transaction and production
enforcement remain separate decisions or evidence. Product Implementation remains HOLD and
no Implementation CLEAR is claimed.
