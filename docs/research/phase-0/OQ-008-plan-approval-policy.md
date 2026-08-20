---
packet_schema_version: 1
packet_id: "OQ-008"
question_id: "OQ-008"
title: "PLAN_APPROVED actor와 plan approval policy"
status: "blocked"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T00:00:00Z"
---

# OQ-008 — plan approval policy

## 1. Scope and authority

- Question: 모든 PLAN_APPROVED가 human approval인가, policy approval이 가능한가?
- Phase/Gate: Phase 0 / decision packet
- Authority: user
- Allowed scope: synthetic stale-digest guard와 approval-actor candidate 비교
- Non-goals: policy 채택, risk threshold 확정, production schema, ADR, scaffold와
  user receipt 생성

## 2. Candidates

| candidate | policy | evidence |
| --- | --- | --- |
| C-01 | 모든 PLAN_APPROVED에 user actor 요구 | unverified |
| C-02 | 일반 low-risk plan은 policy, 고위험/범위·외부 write는 user | unverified |
| C-03 | user가 scope/side effect만 승인하고 나머지는 policy | unverified |

No candidate is selected.

## 3. Observed guard versus unresolved policy

The fixture observed:

- PLAN_APPROVED → RUNNING with digest_current=false: DENIED
- reason: stale_digest

이것은 stale revision을 실행하지 않는 fixture guard 관찰이다. 누가 PLAN_APPROVED를
승인할 수 있는지, 즉 user actor와 policy actor의 권한 문제를 결정하지 않는다.

## 4. Commands and evidence

- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py (twice) → each exit 0
- each run reported 7 assertions and all_assertions_pass=true
- both stdout JSON values parsed and compared equal

Hashes:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
- execution record: evidence/OQ-008/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ008-001/RUN.md

## 5. Unresolved policy

User must decide the approval actor, risk threshold, scope-expansion threshold,
external-write and destructive-action threshold, security boundary treatment, and
the required approval-receipt identity, timestamp, digest and storage format.

OQ-008 remains pending user decision. No policy or Lifecycle/Specification ADR is
created; product Implementation remains HOLD and no Implementation CLEAR is claimed.
