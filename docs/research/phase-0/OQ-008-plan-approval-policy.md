---
packet_schema_version: 1
packet_id: "OQ-008"
question_id: "OQ-008"
title: "PLAN_APPROVED actor와 plan approval policy"
status: "blocked"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-22T10:40:37Z"
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

No general `PLAN_APPROVED` candidate is selected.

## 3. Observed guard and candidate comparison

The original shared lifecycle fixture observed:

- PLAN_APPROVED → RUNNING with digest_current=false: DENIED
- reason: stale_digest

이것은 stale revision을 실행하지 않는 fixture guard 관찰이다. 누가 PLAN_APPROVED를
승인할 수 있는지, 즉 user actor와 policy actor의 권한 문제를 결정하지 않는다.

The follow-up [`FX-PLAN-APPROVAL-POLICY-001`](./fixtures/FX-PLAN-APPROVAL-POLICY-001/README.md)
compared all three candidates across synthetic scenarios. The observed actor projection
was:

| scenario | C-01 | C-02 | C-03 |
| --- | --- | --- | --- |
| routine read-only | `ALLOWED/user` | `ALLOWED/policy` | `ALLOWED/policy` |
| routine local write | `ALLOWED/user` | `ALLOWED/policy` | `ALLOWED/user` |
| scope expansion | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| external write | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| destructive action | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| security-boundary change | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| stale digest | `DENIED/none` | `DENIED/none` | `DENIED/none` |

The runner reported 31/31 assertions and left `selected_candidate` as `null`. The
comparison is a synthetic candidate observation: it does not select C-01/C-02/C-03 or
define a product risk tier.

The OQ-015 user receipt establishes the minimum security floor: scope expansion,
external write, destructive action, security-boundary change and permission escalation
require a current-digest-bound user receipt. It does not decide whether an ordinary
low-risk `PLAN_APPROVED` may use a policy actor.

## 4. Commands and evidence

- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py (twice) → each exit 0
- each run reported 7 assertions and all_assertions_pass=true
- both stdout JSON values parsed and compared equal
- python3 -m json.tool docs/research/phase-0/fixtures/FX-PLAN-APPROVAL-POLICY-001/input/fixture.json >/dev/null → exit 0
- python3 -m py_compile docs/research/phase-0/fixtures/FX-PLAN-APPROVAL-POLICY-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-PLAN-APPROVAL-POLICY-001/runner.py (twice) → each exit 0
- paired stdout/stderr comparison and JSON parse → exit 0; byte-identical stdout
- each follow-up run reported 31 assertions and all_assertions_pass=true

Hashes:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
- execution record: evidence/OQ-008/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ008-001/RUN.md
- follow-up runner.py: a8d5b86389230531ddf0afe7c956882c730a67d9844d1b2cdec93c6cd59c5e5f
- follow-up input/fixture.json: 1b3e1106847ceb3d57119ba82d84f86326723d289b880f1cc3d341f2012f7654
- paired stdout: cd964c1db1a12f390301896dd92a89386fcef17e7897f3c7eb70246936513684
- follow-up execution records: [RUN-OQ008-002-A](./evidence/OQ-008/FX-PLAN-APPROVAL-POLICY-001/RUN-OQ008-002-A/RUN.md), [RUN-OQ008-002-B](./evidence/OQ-008/FX-PLAN-APPROVAL-POLICY-001/RUN-OQ008-002-B/RUN.md)

## 5. Unresolved policy

User must decide the approval actor, risk threshold, scope-expansion threshold,
external-write and destructive-action threshold, security boundary treatment, and
the required approval-receipt identity, timestamp, digest and storage format.

OQ-008 remains pending for the general `PLAN_APPROVED` actor, risk tiers and receipt
schema. The sensitive-action floor is accepted through [OQ-015](./OQ-015-threat-model-permission-policy.md)
and [ADR-0009](../../adr/0009-threat-model-permission-boundaries.md). The follow-up
fixture does not observe receipt identity/timestamp/digest storage, production enforcement,
or false-negative/false-positive risk calibration. No product Implementation CLEAR is
claimed, and a user decision is still required.
