# ADR-0014: Completion checkpoint and writer lease release are atomic

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-009의 disposable crash-point fixture는 terminal checkpoint, project projection과
writer lease release의 후보 순서를 비교했다. C-01은 projection을 준비한 뒤 runtime
transaction에서 terminal checkpoint와 lease release를 함께 기록하고, runtime 확인 뒤
`COMPLETED`를 노출한다. C-02는 lease release 후 terminal checkpoint를 별도 기록하고,
C-03은 runtime commit 전에 완료 projection을 노출한다.

두 번의 결정론적 실행 모두 43/43 assertions와 byte-identical stdout을 반환했다. C-01은
네 crash point 모두에서 안전했고, C-02는 `after_lease_release`에서 terminal checkpoint
전 lease 해제를, C-03은 첫 세 crash point에서 runtime commit 전 완료 노출을 관찰했다.
모든 row는 operation-id replay 후 안전한 상태로 수렴했지만, eventual replay만으로는
crash 순간의 writer/completion 안전성을 보장하지 못한다.

## 결정

1. final `run.md`와 `verification.md` projection은 operation ID로 준비·reconcile할 수
   있지만 completion authority가 아니다.
2. Controller는 하나의 runtime transaction에서 terminal checkpoint, writer lease release와
   terminal completion record를 함께 기록한다.
3. runtime commit 전에는 `COMPLETED`를 외부에 노출하지 않는다. commit 후 current runtime
   read가 terminal checkpoint와 inactive lease를 확인한 때만 projection을 완료로 노출한다.
4. crash 전후 재실행은 operation ID에 묶인 idempotent reconciliation으로 처리한다.
5. 이 결정은 production SQLite schema, fsync/WAL 설정, multi-process takeover 또는
   installed-host crash validation을 확정하지 않는다.

## 결과

- terminal completion과 writer ownership의 중간 불일치를 fail-closed로 제한한다.
- project document가 runtime보다 잠시 앞서 준비될 수 있지만, runtime state가 완료 권위자이며
  recovery가 projection을 다시 맞춘다.
- C-02의 writer-free incomplete window와 C-03의 premature completion exposure를 금지한다.
- Phase 0와 product Implementation은 다른 미결정과 production evidence가 남아 있으므로
  계속 `HOLD`다.

## 거절한 대안

- **C-02:** lease가 terminal checkpoint보다 먼저 해제되면 crash 순간 incomplete task에
  writer가 없어진다.
- **C-03:** project projection을 runtime commit 전에 완료로 노출하면 stale projection이
  실제 completion authority처럼 보인다.
- **eventual replay만 보장:** 최종 상태가 같아도 crash window의 잘못된 관찰을 방지하지 못한다.

## 검증 방법

- [`OQ-009 packet`](../research/phase-0/OQ-009-completion-lease-atomicity.md)의
  [`RUN-OQ009-002-A`](../research/phase-0/evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/RUN-A.md)와
  [`RUN-OQ009-002-B`](../research/phase-0/evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/RUN-B.md)를
  확인한다.
- fixture는 C-01/C-02/C-03 각각의 `after_projection`, `after_lease_release`,
  `after_terminal_checkpoint`, `after_runtime_commit`을 재현해야 한다.
- production 구현 전 SQLite transaction, projection reconciliation, stale-writer takeover와
  crash recovery를 별도 evidence로 검증한다.

## Decision receipt

- **Decision:** C-01 — terminal checkpoint와 writer lease release를 한 runtime transaction으로 기록
- **Actor:** `user-delegated-autonomous-delivery` under the explicit AUTOPILOT delegation
- **Recorded at:** `2026-08-22T11:06:43Z`
- **Reference:** [OQ-009 decision receipt](../research/phase-0/OQ-009-completion-lease-atomicity.md#8-decision)
