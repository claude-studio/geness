---
packet_schema_version: 1
packet_id: "OQ-009"
question_id: "OQ-009"
title: "completion transaction과 writer lease release ordering"
status: "resolved"
owner: "Codex / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-22T11:06:43Z"
---

# OQ-009 — completion and lease atomicity

## 1. Scope and authority

- Question: terminal checkpoint, projection과 writer lease release의 원자적 순서는 무엇인가?
- Phase/Gate: Phase 0 / decision packet
- Authority: user
- Allowed scope: synthetic terminal replay와 transaction-order candidate 비교
- Dependencies: OQ-004 recovery policy와 ADR-0009 fail-closed completion baseline
- Non-goals: production DB/schema, daemon, crash recovery implementation, scaffold와
  Implementation CLEAR

## 2. Candidate orderings

| candidate | ordering | evidence |
| --- | --- | --- |
| C-01 | projection을 준비한 뒤 terminal checkpoint와 lease release를 같은 runtime transaction으로 기록하고, runtime 확인 후 완료를 노출 | observed; selected |
| C-02 | lease release 후 terminal checkpoint를 별도 기록 | observed; unsafe crash window |
| C-03 | runtime commit 전에 COMPLETED project projection을 외부에 노출 | observed; unsafe crash window |

## 3. Trade-off matrix

| criterion | C-01 | C-02 | C-03 | evidence |
| --- | --- | --- | --- | --- |
| terminal 전 lease release 금지 | 네 crash point 모두 충족 | `after_lease_release`에서 위반 | 충족하지만 projection 선노출 | A-003 / RUN-OQ009-002 |
| runtime commit 전 완료 노출 금지 | projection은 준비만 하고 노출하지 않음 | 충족 | `after_projection`, lease/terminal 중간 지점에서 위반 | A-003 / RUN-OQ009-002 |
| operation-id replay | 두 번 모두 안전·동일 | 두 번 모두 안전·동일하나 중간 위험 존재 | 두 번 모두 안전·동일하나 중간 노출 존재 | A-003 / RUN-OQ009-002 |
| 구현 전 계약 적합성 | 기존 lifecycle/architecture proposal과 일치 | writer loss window를 허용 | projection을 runtime authority처럼 취급 | ADR-0009, ADR-0014 |

## 4. Observed crash-point replay

The fixture retained the original lifecycle, stale-digest and two-writer probes and added
the four crash points `after_projection`, `after_lease_release`,
`after_terminal_checkpoint` and `after_runtime_commit` for C-01, C-02 and C-03.

- C-01: 4/4 crash states were safe before replay; no unsafe invariant was observed.
- C-02: `after_lease_release` exposed `lease_released_before_terminal_checkpoint`.
- C-03: `after_projection`, `after_lease_release` and `after_terminal_checkpoint`
  exposed `completed_exposed_before_runtime_commit`.
- All 12 rows converged to a safe terminal state after operation-id replay, and the
  second replay was equality-equivalent.
- Both executions reported 43/43 assertions and `all_assertions_pass=true`; stdout
  was byte-identical.

The projection is intentionally modeled as prepared but non-authoritative for C-01.
`COMPLETED` is exposed only after the runtime state confirms terminal checkpoint,
released lease and completion. This is synthetic evidence, not proof of a production
SQLite transaction or installed-host crash guarantee.

## 5. Sources

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | local-doc | `docs/02_TASK_LIFECYCLE.md#9-completion` | `fe59953e51fa90a43783716d9147201b1da56086` | 2026-08-22 | proposed completion order requires final projection/reconciliation before atomic terminal checkpoint + lease release and guards `COMPLETED` exposure | local project document; no external reuse |
| S-002 | local-doc | `docs/01_ARCHITECTURE.md#7-원자성-경계` | `fe59953e51fa90a43783716d9147201b1da56086` | 2026-08-22 | runtime terminal completion checkpoint and writer lease release are one logical transaction; project write is reconciled by operation ID | local project document; no external reuse |
| S-003 | local-adr | `docs/adr/0009-threat-model-permission-boundaries.md` | `fe59953e51fa90a43783716d9147201b1da56086` | 2026-08-22 | completion authority and fail-closed stale/two-writer baseline remain Controller-owned | local project ADR; no external reuse |

## 6. Commands and evidence

- `python3 -m json.tool input/fixture.json >/dev/null` → exit 0
- `python3 -m py_compile runner.py` → exit 0
- `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` (RUN-OQ009-002-A) → exit 0
- `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` (RUN-OQ009-002-B) → exit 0
- `cmp -s /tmp/geness-oq009-run-a.json /tmp/geness-oq009-run-b.json` → exit 0
- both output JSON values parsed; each reported 43 assertions and `all_assertions_pass=true`

Tool/runtime: Python 3.9.6 in the fixture working directory. Network and external writes
were disabled. Raw stderr was empty and discarded after paired comparison.

### Artifacts

| artifact_id | kind | path | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- |
| A-001 | runner | `fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py` | `9c3361989c10fd361a67e0432c88a6573ebfe399f639b791f8442623adb1cc54` | tracked | crash-point candidate comparison |
| A-002 | input | `fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/input/fixture.json` | `bc5d871017fd45b8aeed16d2c71a1587992ee4a4e3affaab300c9e319e2b8147` | tracked | fixed candidates and expected unsafe points |
| A-003 | result | `evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/result.json` | `219b98005ecac98195dbe4c29ba4b8a5b58d9825dfbb84e6e8367d715269e4db` | packet | 43 assertions, 12-row matrix and replay equality |
| A-004 | execution records | `evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/RUN-A.md`, `RUN-B.md` | tracked Markdown records | packet | exact commands, exit statuses and paired runs |

The prior minimal evidence remains preserved at
`evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-001/RUN.md`.

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | The runner models transaction boundaries in memory, not a production SQLite transaction. | high | rollback, fsync, WAL and multi-process crash behavior are unobserved | implement the selected contract only after Phase 0 CLEAR, then run production crash/reconciliation evidence | Phase 0 / runtime | open |
| R-002 | The fixture does not exercise stale-writer takeover or heartbeat grace. | high | cross-workspace writer arbitration remains open | retain OQ-006/OQ-009 cross-concern follow-up before implementation completion | Phase 0 | open |
| R-003 | The projection model is synthetic and does not prove filesystem atomic replace. | medium | target-document fsync/reconciliation behavior is unobserved | add projection crash fixture during implementation validation | Storage | open |

## 8. Decision

- **Packet decision status:** `resolved`
- **Recommendation:** C-01 — prepare final projections, atomically record terminal checkpoint and lease release in one runtime transaction, then expose `COMPLETED` only after a current runtime read confirms both.
- **Rationale:** C-01 is the only candidate with no unsafe crash state in the fixed matrix. C-02 creates a writer-free incomplete state, while C-03 allows a projection to claim completion before the runtime authority commits. All candidate rows replayed safely, so the distinguishing evidence is the crash-time invariant rather than eventual replay alone.
- **Rejected/deferred candidates:** C-02 rejected for the lease-release window; C-03 rejected for projection-before-runtime completion exposure. Production transaction, schema and multi-process validation remain deferred.
- **Unresolved impact:** Phase 0 remains HOLD because other user decisions and production evidence are open. This packet does not authorize product scaffold or implementation.

### User/authority decision receipt

- **Decision:** C-01 — completion projection is non-authoritative until runtime reconciliation; terminal checkpoint and writer lease release commit atomically; replay is operation-id idempotent.
- **Actor:** `user-delegated-autonomous-delivery` under the explicit AUTOPILOT rule in the task prompt
- **Recorded at:** `2026-08-22T11:06:43Z`
- **Authority basis:** the delegated rule permits adoption only when the packet recommendation is clear, the fixture passes deterministically twice, no contradictory evidence exists, and the choice remains within the packet's docs/research scope. This receipt records that policy basis and does not fabricate an interactive user message.
- **Reference:** [ADR-0014](../../adr/0014-completion-lease-atomicity.md), [RUN-OQ009-002-A](./evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/RUN-A.md), [RUN-OQ009-002-B](./evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/RUN-B.md)
- **Supersedes:** `pending` OQ-009 packet status; no prior decision receipt

## 9. Next verifiable goal

- Revalidate the decision-ready P0-05 identity/schema/digest queue and determine whether OQ-005 can meet the same delegated-decision evidence gate without changing product scope, security policy or external behavior.
