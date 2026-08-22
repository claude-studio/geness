---
packet_schema_version: 1
packet_id: "OQ-003"
question_id: "OQ-003"
title: "v1 background daemon과 lease liveness 비교"
status: "decision-ready"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-22T17:01:51+09:00"
---

# OQ-003 — background daemon과 lease liveness

## 1. Scope and authority

- Question: v1 lease heartbeat에 background daemon이 필요한가?
- Phase/Gate: Phase 0 / decision packet
- Authority: user
- Allowed scope: daemon/no-daemon lease liveness trade-off와 disposable fixture 관찰
- Non-goals: 제품 언어, package manager, runtime, production schema, daemon 구현,
  plugin scaffold와 user decision receipt 확정
- Dependencies: #15 merged prerequisite; OQ-001 is resolved by ADR-0010 and OQ-002 is
  resolved by ADR-0011 and its user receipt

## 2. Candidates

| candidate | description | evidence |
| --- | --- | --- |
| C-01 | no-daemon stdio/short-lived Controller와 explicit checkpoint/takeover | observed — FX-LEASE-LIVENESS-TAKEOVER-001; not selected |
| C-02 | local background daemon이 heartbeat와 lease authority를 유지 | unverified |
| C-03 | host-owned heartbeat sidecar 또는 별도 lease monitor | unverified |

No candidate is selected. The fixture evidence closes the missing liveness observation but does
not automatically choose a daemon policy.

## 3. Trade-off and actual observation

No-daemon은 설치·lifecycle 복잡성이 낮을 수 있지만 process 중단 뒤 heartbeat, grace
period와 safe takeover의 실제 경계가 필요하다. Daemon/sidecar는 지속 heartbeat를 제공할
수 있지만 process ownership, crash recovery와 installation boundary를 추가한다. 이
trade-off 자체는 사용자 결정 대상이며 fixture가 자동으로 확정하지 않는다.

FX-LIFECYCLE-LEASE-COMPLETION-001 observed:

- INITIALIZING → INTERVIEWING: ALLOWED
- stale digest PLAN_APPROVED → RUNNING: DENIED, reason stale_digest
- INTERVIEWING → RUNNING: DENIED, reason edge_not_allowed
- sequential exclusive claim: first ALLOWED, second DENIED
- terminal replay: completed=true, lease_active=false; second replay equality-equivalent
- 7 assertions passed; two runner JSON outputs parsed and compared equal

The fixture did not reproduce heartbeat, grace-period expiry, process crash, daemon
liveness, or safe stale-writer takeover. The exclusive claim is not a two-process race.

FX-LEASE-LIVENESS-TAKEOVER-001 then ran a POSIX-isolated logical-clock fixture with two
actual child processes. writer-A acquired at time `0`, heartbeated at `2` and extended the
grace deadline to `5`. observer-B was denied at `3`, `4` and the exact deadline `5` while
grace was active. writer-A was interrupted with exit status `-9`; observer-B was still denied
at `4` and `5`, then was allowed to take over at `6` and heartbeated as the new owner at `7`.
The fixture passed 17/17
assertions twice with byte-identical stdout/stderr hashes. It started no daemon or sidecar.

This is a logical-clock observation of a fixture-local lease protocol, not production daemon,
clock, SQLite transaction, cross-workspace authority or installation evidence.

## 4. Commands and artifacts

- python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py (twice) → exit 0, 7 assertions each, JSON equal
- sha256sum runner.py and input/fixture.json → exit 0
- In the fixture cwd, `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` (twice) → exit 0, 17 assertions each, byte-identical stdout/stderr
- From repository root, `PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001/runner.py` (smoke run) → exit 0
- PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001/runner.py → exit 0
- python3 -m json.tool docs/research/phase-0/evidence/OQ-003/FX-LEASE-LIVENESS-TAKEOVER-001/RUN-OQ003-001/result.json → exit 0
- sha256sum runner.py, input/fixture.json and redacted result.json → exit 0
- git diff --check -- → exit 0

Artifact hashes:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
- execution record: evidence/OQ-003/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ003-001/RUN.md
- liveness runner.py: af6cafaaf7d24625b133eedf530aa3c70e3c1261951597827b53032c5d027268
- liveness input/fixture.json: 446dc5f6e01da55c3941cabc8ca491e36c75774853e3ae9680e73c126204dc6d
- liveness redacted result.json: 9c53e1155125f44e44812933ffca9a03abfe65e6d4068026fa005046818da0a1
- liveness execution record: evidence/OQ-003/FX-LEASE-LIVENESS-TAKEOVER-001/RUN-OQ003-001/RUN.md

### Liveness execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `RUN-OQ003-001` | `FX-LEASE-LIVENESS-TAKEOVER-001` | 2026-08-22T08:06:41Z / 2026-08-22T08:06:41Z | `docs/research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | 0 | `pass` — 17/17 assertions, two child processes, interruption, grace-boundary denial and stale takeover | [result.json](./evidence/OQ-003/FX-LEASE-LIVENESS-TAKEOVER-001/RUN-OQ003-001/result.json) |
| `RUN-OQ003-002` | `FX-LEASE-LIVENESS-TAKEOVER-001` | 2026-08-22T08:06:41Z / 2026-08-22T08:06:41Z | `docs/research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | 0 | `pass` — same result and stdout/stderr hashes as RUN-OQ003-001 | [RUN.md](./evidence/OQ-003/FX-LEASE-LIVENESS-TAKEOVER-001/RUN-OQ003-001/RUN.md) |

Additional execution environment:

- runner Python: `3.14.6`
- environment override: `PYTHONDONTWRITEBYTECODE=1`; logical clock supplied by parent runner
- network/external writes: `disabled` / `false`
- redaction: child PIDs, temporary paths and raw process output were omitted from the packet;
  raw stdout/stderr were discarded after hashing

### Liveness artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-006 | redacted result manifest | `evidence/OQ-003/FX-LEASE-LIVENESS-TAKEOVER-001/RUN-OQ003-001/result.json` | `RUN-OQ003-001` | `9c53e1155125f44e44812933ffca9a03abfe65e6d4068026fa005046818da0a1` | `packet` | deterministic 17-assertion liveness/takeover result |
| A-007 | raw stdout, discarded | wrapper memory capture; no file retained | `RUN-OQ003-001/002` | `sha256:0dcbf11c6df7619e16e9af50856fa281e854f16be6fe8b6082bf49d0d8c1c8ab`; discarded after redaction | `discarded` | full runner observation before redaction |
| A-008 | raw stderr, discarded | `/tmp` run-local output | `RUN-OQ003-001/002` | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; empty and discarded | `discarded` | no child error output |

## 5. Risks and limitations

- High: the new fixture uses a logical clock and POSIX file lock; production clock source,
  SQLite transaction, crash points and cross-workspace writer authority remain unobserved.
- High: daemon/sidecar installation, process ownership, host lifecycle and operational cost
  were not compared; C-01/C-02/C-03 still require user judgment.
- Medium: fixture rules are observations only and cannot establish user requirements or a
  Runtime ADR.

## 6. Decision

- Packet status: decision-ready / needs-user-decision
- Recommendation: no automatic selection; the two-process fixture now supplies the missing
  heartbeat/grace/takeover observation. Ask the user to choose among C-01/C-02/C-03 after
  reviewing the remaining production and operational evidence gaps.
- User decision receipt: pending
- No Runtime ADR is created. OQ-003 remains open and Implementation remains HOLD; no
  Implementation CLEAR is claimed.
