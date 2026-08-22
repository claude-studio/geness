# ADR-0013: OQ-004 C-01 task lifecycle recovery policy

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-004의 `FX-LIFECYCLE-RECOVERY-002` disposable fixture는 `FAILED`와 `CANCELLED`의
reopen 후보, 명시적 user receipt guard, attempt/task failure 구분, completion exposure
guard와 failure candidate memory guard를 비교했다. 두 번의 실행 모두 14/14 assertions와
동일한 raw JSON output을 반환했다. 이 결과는 후보 비교 evidence이며 production
Controller나 persistence의 동작을 증명하지 않는다.

사용자는 [OQ-004 decision receipt](../research/phase-0/evidence/OQ-004/USER-DECISION-RECEIPT-001.md)를
통해 C-01을 선택했다.

## 결정

1. task-level `FAILED`는 현재 run lineage를 안전하게 복구할 수 없는 system outcome으로
   기록하며, 명시적인 user reopen receipt가 있을 때만 `REOPENED`로 전환한다.
2. `FAILED`의 자동 reopen은 허용하지 않는다. receipt가 없거나 stale이면 전이를 거부한다.
3. `CANCELLED`는 terminal 상태다. `CANCELLED → REOPENED` 전이는 허용하지 않으며, 다시
   실행하려면 별도의 user-authorized task/revision 경로를 사용한다.
4. attempt-level `FAIL`은 task-level `FAILED`가 아니다. attempt 결과는 successor 또는
   `BLOCKED` 판단의 입력으로 남고 task state를 자동으로 `FAILED`로 바꾸지 않는다.
5. 이 ADR의 recovery decision은 기존 completion·learning guard와 결합한다. terminal
   checkpoint와 lease release 전에는 `COMPLETED`를 외부에 노출하지 않으며, independent
   evidence 없는 failure candidate를 verified lesson이나 일반 memory query로 노출하지
   않는다.

## 결과

- lifecycle contract는 system failure의 제한적 사용자 복구와 user cancellation의 terminal
  의미를 구분한다.
- reopen은 user authority와 current lifecycle context 검증을 통과해야 하며, worker,
  host session 또는 project content가 user receipt를 대신할 수 없다.
- 전체 state graph의 진입 edge, receipt envelope의 저장·검증 schema, Plan Gate actor/risk
  policy와 completion transaction atomicity는 이 ADR이 확정하지 않는다.
- 제품 구현 `HOLD`와 Phase 0 Gate `HOLD`는 유지한다. production persistence, crash replay,
  lease takeover과 installed-host E2E evidence가 추가로 필요하다.

## 거절한 대안

- **C-02:** `CANCELLED`도 명시적 receipt로 reopen하는 정책은 user cancellation의 terminal
  의미와 복구 책임을 혼합하므로 v1에서 채택하지 않았다.
- **C-03:** `FAILED`까지 terminal로 고정하면 안전하지 않은 자동 복구는 막지만, 명시적
  사용자 판단으로 복구 가능한 system failure의 bounded recovery 경로를 잃으므로 채택하지
  않았다.
- **자동 reopen:** 사용자 의도와 current contract 확인 없이 lineage를 재개하므로 채택하지
  않았다.

## 검증 방법

- [OQ-004 packet](../research/phase-0/OQ-004-task-lifecycle.md)의 두 lifecycle fixture
  실행과 14/14 assertion 결과를 보존한다.
- `FAILED` reopen receipt의 authority/current-context validation, `CANCELLED` terminal
  replay, production transaction/crash point와 lease interaction을 구현 전 별도 evidence로
  검증한다.
- OQ-008 또는 OQ-009가 이 recovery policy와 충돌하는 결정을 내리면 superseding ADR로
  lifecycle contract를 갱신한다.

## Decision receipt

- **Decision:** C-01 — explicit user receipt가 있는 `FAILED`만 `REOPENED`; `CANCELLED`는 terminal
- **Actor:** `user`
- **Recorded at:** `2026-08-22T19:08:56+09:00`
- **Reference:** [USER-DECISION-OQ004-001](../research/phase-0/evidence/OQ-004/USER-DECISION-RECEIPT-001.md)
