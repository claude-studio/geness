---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ004-001"
question_ids:
  - "OQ-004"
authority: "user"
recorded_at: "2026-08-22T19:08:56+09:00"
source: "Explicit user instruction to proceed with the recommended C-01 candidate in Codex session"
---

# User decision receipt — OQ-004

## Decision

사용자는 앞서 제시된 OQ-004 C-01 권고안을 기준으로 진행하도록 확인했다.

- task-level `FAILED`는 명시적인 user reopen receipt가 있을 때만 `REOPENED`로 전환한다.
- `FAILED`의 자동 reopen은 허용하지 않는다.
- `CANCELLED`는 terminal 상태로 취급하며 `CANCELLED → REOPENED` 전이는 허용하지 않는다.
- attempt-level `FAIL`은 task-level `FAILED`와 구분한다.

이 receipt는 lifecycle recovery policy만 결정한다. 일반 `PLAN_APPROVED` actor/risk policy,
completion transaction atomicity와 production persistence는 각각 OQ-008/OQ-009 및 후속
evidence가 소유한다.

## Rationale and evidence

결정은 [OQ-004 follow-up execution record](./FX-LIFECYCLE-RECOVERY-002/RUN-OQ004-002/RUN.md)의
14/14 assertion 결과와 후보 비교에 근거한다. fixture는 C-01/C-02에서 명시적 receipt가
있는 `FAILED → REOPENED`를 허용하고, C-01/C-03에서 `CANCELLED → REOPENED`를 terminal로
거부하며, receipt 없는 reopen을 모든 후보에서 거부했다.

이 evidence는 deterministic synthetic projection이다. production Controller, SQLite
transaction, crash replay, lease takeover과 receipt 저장·검증 구현을 증명하지 않는다.

## Unresolved scope

정확한 전체 state graph와 `CANCELLED` 진입 전이, current digest에 묶인 receipt envelope의
schema/validation, Plan Gate actor/risk policy, completion crash-point atomicity와 독립
verifier authority는 별도 결정 또는 구현 evidence로 남아 있다. 제품 Implementation `HOLD`와
Phase 0 Gate `HOLD`는 변경하지 않는다.

## Linked artifacts

- [OQ-004 lifecycle packet](../../OQ-004-task-lifecycle.md)
- [ADR-0013](../../../../adr/0013-task-lifecycle-recovery.md)
- [FX-LIFECYCLE-RECOVERY-002](../../fixtures/FX-LIFECYCLE-RECOVERY-002/README.md)
