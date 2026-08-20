---
packet_schema_version: 1
packet_id: "OQ-004"
question_id: "OQ-004"
title: "task lifecycle state transition과 FAILED/CANCELLED 의미"
status: "blocked"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T00:00:00Z"
---

# OQ-004 — task lifecycle state transition

## 1. Scope and authority

- Question: exact allowed/denied task transitions과 FAILED/CANCELLED recovery 의미는 무엇인가?
- Phase/Gate: Phase 0 / decision packet
- Authority: user
- Allowed scope: current lifecycle proposal을 합성 fixture로 관찰하고 candidate를 비교
- Non-goals: product language, package manager, runtime, production schema, Lifecycle ADR,
  scaffold와 user decision receipt 확정

## 2. Candidate transition policies

| candidate | FAILED | CANCELLED | evidence |
| --- | --- | --- | --- |
| C-01 | explicit user reopen 후 REOPENED | terminal | inferred |
| C-02 | explicit user reopen 후 REOPENED | explicit reopen 가능 | inferred |
| C-03 | terminal | terminal | inferred |

No candidate is selected.

| transition case | observed result | reason |
| --- | --- | --- |
| INITIALIZING → INTERVIEWING | ALLOWED | fixture_rule |
| PLAN_APPROVED → RUNNING with stale digest | DENIED | stale_digest |
| INTERVIEWING → RUNNING | DENIED | edge_not_allowed |
| FAILED → REOPENED | rule defined as allowed | not separately asserted in this run |

## 3. Commands and evidence

- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- same runner command second run → exit 0
- each run reported 7 assertions and all_assertions_pass=true
- parsed JSON values from both runs compared equal

Hashes:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
- execution record: evidence/OQ-004/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ004-001/RUN.md

## 4. Limitations and pending decisions

The minimal fixture does not independently assert FAILED recovery, CANCELLED behavior,
the complete canonical state graph, completion ordering, or Plan Gate actor policy.
It does not reproduce production persistence, crash replay, lease takeover, or verifier
authority.

OQ-004 remains pending user decision. CANCELLED meaning, Plan Gate approval actor,
completion semantics and exact lifecycle contract are unresolved. No Lifecycle ADR is
created; product Implementation remains HOLD and no Implementation CLEAR is claimed.
