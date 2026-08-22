# ADR-0018: Deterministic learning evaluator thresholds

> 상태: Accepted
> 날짜: 2026-08-23
> Supersedes: none

## 맥락

OQ-010은 failure candidate를 일반 memory에 노출하기 전에 어떤 recurrence와
evidence를 요구하고, 언제 eligible unassisted success와 관찰 기간을 기준으로
만료할지 결정한다. Accepted [ADR-0003](./0003-failure-candidate-is-not-memory.md)은
실패 후보와 durable memory를 구분하지만, evaluator threshold와 retrieval visibility는
미정이었다.

`FX-MEMORY-RETENTION-BOOTSTRAP-001`은 동일한 13개 synthetic event를 두 번 replay해
43/43 assertions와 equality-equivalent projection을 통과했다. 첫 failure 격리, 같은
run 중복 제외, 독립 recurrence와 reproducible guard promotion, eligible-only
unassisted-success expiry를 관찰했다.

## 결정

1. v1은 C-01 deterministic evidence-gated evaluator를 사용한다. evaluator는 구조화된
   fingerprint와 versioned event/evaluator rule을 입력으로 사용하며 model confidence를
   promotion 또는 expiry의 권위 있는 입력으로 사용하지 않는다.
2. fingerprint는 project와 phase, module/file/symbol 또는 domain entity, task type,
   failure category, violated rule/invariant와 normalized trigger/action 축을 우선
   보존한다. 전체 error message나 변동 가능한 stack trace를 fingerprint로 사용하지 않는다.
3. candidate는 다음 중 하나를 충족할 때 `verified` promotion 후보가 된다.
   - 서로 다른 독립 run에서 같은 fingerprint가 2회 재발한다.
   - 동일한 rule/evidence lineage를 가진 deterministic fail-before/pass-after guard
     evidence가 재현된다.
   같은 run의 중복은 독립 recurrence로 세지 않는다.
4. `candidate`와 `probationary`는 eligible exposure에서 lesson 주입 없이 성공한
   `unassisted success` 3회와 최소 7일의 관찰 기간을 모두 충족하고 재발·guard
   prevention evidence가 없을 때 `expired` 후보가 된다. injected, ineligible 또는
   unrelated success는 이 count에서 제외한다.
5. 일반 memory retrieval에는 `verified`와 `enforced`만 노출한다. candidate,
   probationary와 expired lesson은 audit/event history에 남기되 일반 검색 결과에는
   노출하지 않는다. guard가 문제를 예방한 횟수는 unassisted success와 별도 event로
   기록한다.
6. threshold와 evaluator/rule version은 event lineage에 함께 기록한다. 이 ADR의
   `2 / 3 / 7일`은 v1 초기 정책이며 실제 evaluator 구현, calibration, migration과
   concurrent writer/crash recovery evidence는 후속 Phase 5/7 범위다.

## 결과

- 일회성 failure와 unrelated success가 durable memory로 오염되는 것을 막는다.
- 독립 recurrence 또는 재현 가능한 guard가 없으면 lesson이 일반 retrieval에 나타나지
  않는다.
- time-only expiry와 injected success에 의한 잘못된 감쇠를 방지한다.
- exact event/SQLite schema, merge/split implementation, revocation/compiled transition,
  writer arbitration과 production calibration은 아직 구현 권한을 얻지 않는다.

## 거절한 대안

- **C-02 weighted/model-assisted evaluator:** calibration, model/version provenance와
  deterministic replay evidence가 없어 v1 권위자로 채택하지 않았다.
- **C-03 eager promotion/no expiry:** 첫 failure를 memory에 노출하고 만료 경로를 없애
  [ADR-0003](./0003-failure-candidate-is-not-memory.md)의 false-positive 경계를
  훼손하므로 control/deferred candidate로 남긴다.

## 검증 방법

- [OQ-010 packet](../research/phase-0/OQ-010-lesson-evaluator.md)의 candidate/trade-off와
  [decision receipt](../research/phase-0/evidence/OQ-010/USER-DECISION-RECEIPT-001.md)를
  확인한다.
- [FX-MEMORY-RETENTION-BOOTSTRAP-001](../research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/README.md)을
  두 번 실행해 각 43/43 assertions, `all_assertions_pass=true`와 paired output equality를
  확인한다.
- fixture evidence가 production evaluator, event/SQLite schema 또는 Implementation
  `CLEAR`를 의미하지 않는지 확인한다.
