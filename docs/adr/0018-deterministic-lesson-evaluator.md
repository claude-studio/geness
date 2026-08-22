# ADR-0018: Deterministic evidence-gated lesson evaluator policy

> 상태: Accepted
> 날짜: 2026-08-23
> Supersedes: none

## 맥락

OQ-010은 failure candidate를 durable memory로 승격하거나 감쇠·만료하는 규칙을
[ADR-0003](./0003-failure-candidate-is-not-memory.md)의 accepted boundary 안에서
비교했다. `FX-MEMORY-RETENTION-BOOTSTRAP-001`은 동일 입력을 두 번 replay해 43/43
assertions를 통과했고, 독립 recurrence·guard evidence·eligible exposure와
unassisted success를 구분했다.

Fixture의 수치와 transition은 사용자 결정 전에는 candidate observation이었다. 제품
evaluator, event schema와 fingerprint normalization은 이 결정의 구현 범위가 아니다.

## 결정

1. v1 lesson lifecycle은 deterministic, evidence-gated evaluator policy를 사용한다.
2. 첫 failure는 candidate로만 보존하고 일반 retrieval에 노출하지 않는다.
3. 같은 structured fingerprint가 서로 다른 두 독립 run에서 재발하거나, 재현 가능한
   fail-before/pass-after guard evidence가 있으면 `verified` 승격을 허용한다.
4. candidate/probationary expiry는 eligible exposure에서 lesson을 주입하지 않은
   `unassisted success` 3회와 최소 관찰 기간 7일을 모두 요구한다. 같은 run 중복,
   ineligible exposure와 injected success는 해당 count에서 제외한다.
5. 일반 retrieval은 `verified|enforced` lesson만 대상으로 한다. evaluator/rule version과
   event lineage는 transition audit에 보존한다.
6. C-02 weighted/model-assisted evaluator와 C-03 eager promotion/no expiry는 v1 policy로
   채택하지 않는다.

## 결과

- 일회성 failure와 모델 confidence가 durable memory를 직접 오염시키지 않는다.
- recurrence, guard, exposure와 expiry 판정이 replay 가능한 규칙으로 남는다.
- 초기 `2 / 3 / 7일` threshold profile은 채택됐지만 실제 운영 calibration의 대체물이 아니다.
- fingerprint schema, merge/split normalization, verified lesson revocation, compiled/enforced
  transition, production event/SQLite persistence와 evaluator migration은 후속 evidence가
  필요하다.

## 거절한 대안

- **C-02 weighted/model-assisted evaluator:** calibration, model/version provenance와
  deterministic replay evidence가 없어 v1 policy로 채택하지 않았다.
- **C-03 eager promotion/no expiry:** 첫 failure를 일반 memory에 노출하고 context pollution을
  허용하므로 [ADR-0003](./0003-failure-candidate-is-not-memory.md)와 충돌한다.

## 검증 방법

- [OQ-010 packet](../research/phase-0/OQ-010-lesson-evaluator.md)의 candidate matrix와
  current fixture evidence를 확인한다.
- `FX-MEMORY-RETENTION-BOOTSTRAP-001`을 같은 입력으로 두 번 실행해 exit `0`, 43/43
  assertions, `all_assertions_pass=true`와 paired stdout equality를 확인한다.
- production evaluator, fingerprint normalization, migration, concurrent writer와
  calibration은 제품 구현 전 별도 evidence로 검증한다.

## Decision receipt

- **Decision:** C-01 — deterministic evidence-gated evaluator with `2 / 3 / 7일` initial profile
- **Actor:** `user-delegated-autonomous-delivery` under the explicit AUTOPILOT delegation
- **Recorded at:** `2026-08-22T16:07:07Z`
- **Reference:** [OQ-010 decision receipt](../research/phase-0/evidence/OQ-010/USER-DECISION-RECEIPT-001.md)
