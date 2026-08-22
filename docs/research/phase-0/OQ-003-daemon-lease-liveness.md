---
packet_schema_version: 1
packet_id: "OQ-003"
question_id: "OQ-003"
title: "v1 background daemon과 lease liveness 비교"
status: "blocked"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T00:00:00Z"
---

# OQ-003 — background daemon과 lease liveness

## 1. Scope and authority

- Question: v1 lease heartbeat에 background daemon이 필요한가?
- Phase/Gate: Phase 0 / decision packet
- Authority: user
- Allowed scope: daemon/no-daemon lease liveness trade-off와 disposable fixture 관찰
- Non-goals: 제품 언어, package manager, runtime, production schema, daemon 구현,
  plugin scaffold와 user decision receipt 확정
- Dependencies: #15 merged prerequisite; OQ-001 is resolved by ADR-0010 and OQ-002 remains
  user-decision pending

## 2. Candidates

| candidate | description | evidence |
| --- | --- | --- |
| C-01 | no-daemon stdio/short-lived Controller와 explicit checkpoint/takeover | unverified |
| C-02 | local background daemon이 heartbeat와 lease authority를 유지 | unverified |
| C-03 | host-owned heartbeat sidecar 또는 별도 lease monitor | unverified |

No candidate is selected.

## 3. Trade-off and actual observation

No-daemon은 설치·lifecycle 복잡성이 낮지만 process 중단 뒤 heartbeat, grace period와
safe takeover를 아직 관찰하지 못했다. Daemon/sidecar는 지속 heartbeat를 제공할 수
있지만 process ownership, crash recovery와 installation boundary를 추가한다.

FX-LIFECYCLE-LEASE-COMPLETION-001 observed:

- INITIALIZING → INTERVIEWING: ALLOWED
- stale digest PLAN_APPROVED → RUNNING: DENIED, reason stale_digest
- INTERVIEWING → RUNNING: DENIED, reason edge_not_allowed
- sequential exclusive claim: first ALLOWED, second DENIED
- terminal replay: completed=true, lease_active=false; second replay equality-equivalent
- 7 assertions passed; two runner JSON outputs parsed and compared equal

The fixture did not reproduce heartbeat, grace-period expiry, process crash, daemon
liveness, or safe stale-writer takeover. The exclusive claim is not a two-process race.

## 4. Commands and artifacts

- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py (twice) → exit 0, 7 assertions each, JSON equal
- sha256sum runner.py and input/fixture.json → exit 0
- git diff --check -- → exit 0

Artifact hashes:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
- execution record: evidence/OQ-003/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ003-001/RUN.md

## 5. Risks and limitations

- High: heartbeat/grace/takeover evidence is absent; run a real two-process logical-clock
  fixture before selecting a lease policy.
- High: no production transaction, DB schema, daemon or cross-workspace authority was tested.
- Medium: fixture rules are observations only and cannot establish user requirements.

## 6. Decision

- Packet status: blocked / needs-user-decision
- Recommendation: no selection; execute the missing heartbeat/grace/takeover fixture, then
  ask the user to choose among C-01/C-02/C-03.
- User decision receipt: pending
- No Runtime ADR is created. OQ-003 remains open and Implementation remains HOLD; no
  Implementation CLEAR is claimed.
