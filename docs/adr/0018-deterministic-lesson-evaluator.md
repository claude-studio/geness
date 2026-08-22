# ADR-0018: Deterministic lesson evaluator thresholds

> 상태: Accepted
> 날짜: 2026-08-23
> Supersedes: none

## 맥락

ADR-0003은 failure candidate를 deterministic evidence 없이 durable memory로 승격하지
않도록 정한다. OQ-010은 이 원칙을 structured fingerprint, independent recurrence,
reproducible guard evidence, eligible exposure와 unassisted success의 후보 규칙으로
비교했다.

`FX-MEMORY-RETENTION-BOOTSTRAP-001`은 current worktree에서 두 번 실행되어 각각 43/43
assertions와 `all_assertions_pass=true`를 반환했고, paired stdout은 byte-identical했다.
첫 failure는 retrieval에서 격리됐고, independent recurrence와 reproducible guard evidence만
promotion을 만들었으며, injected/ineligible/unrelated success는 expiry 입력에서 제외됐다.

## 결정

1. C-01 deterministic evidence-gated evaluator를 채택한다. LLM이나 host adapter는 lesson
   상태를 직접 변경하지 않는다.
2. 구조화 fingerprint가 같은 `run_id` 중복이 아닌 두 개의 독립 run에서 재발하거나,
   재현 가능한 `fail-before/pass-after` guard evidence가 있으면 `verified` 후보가 된다.
3. `candidate` 또는 `probationary` lesson은 다음을 모두 만족할 때만 `expired` 후보가 된다.
   - eligible exposure에서 lesson을 주입하지 않은 성공이 3회 이상이다.
   - 최초 관찰 후 최소 7일이 지났다.
   - 재발 또는 guard-prevention evidence가 없다.
   Injected, ineligible 또는 unrelated success는 세지 않으며 시간 경과만으로 만료하지 않는다.
4. 일반 memory retrieval은 `verified|enforced` lesson만 노출한다. `candidate`와 `expired`는
   일반 query에서 격리하고 `compiled` lesson은 실행 가능한 guard가 정본이므로 prompt 검색에서
   제외한다.
5. evaluator/rule version과 이 threshold profile을 transition event lineage에 기록한다.
   이 ADR은 연구 범위에서 threshold direction을 채택하지만 production schema, serializer,
   migration, writer arbitration과 evaluator implementation을 만들지 않는다.

## 결과

- 일회성 failure와 같은 run의 중복이 durable memory를 오염시키지 않는다.
- recurrence와 guard promotion, eligible-only expiry를 deterministic replay로 감사할 수 있다.
- 실제 task volume, false-positive/negative rate와 user tolerance를 통한 calibration은 후속
  evidence가 필요하다.
- fingerprint schema/merge-split normalization, verified lesson revocation, event/SQLite
  persistence와 crash/rebuild behavior는 별도 구현·결정 범위로 남는다.
- 제품-level Implementation `HOLD`는 유지한다. OQ-011 runtime retention/bootstrap policy도
  이 결정에 포함되지 않는다.

## 거절한 대안

- **C-02 weighted/model-assisted evaluator:** calibration, model/version provenance와
  deterministic replay evidence가 없어 채택하지 않았다.
- **C-03 eager promotion/no expiry:** first failure를 일반 memory에 노출해 false positive와
  context pollution을 만들고 ADR-0003의 경계를 위반하므로 채택하지 않았다.

## 검증 방법

- [OQ-010 packet](../research/phase-0/OQ-010-lesson-evaluator.md)의 candidate matrix와
  [FX-MEMORY-RETENTION-BOOTSTRAP-001](../research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/README.md)을
  `PYTHONDONTWRITEBYTECODE=1 python3 runner.py`로 두 번 실행한다.
- 두 실행이 exit `0`, 43/43 assertions, `all_assertions_pass=true`이고 paired stdout이
  byte-identical인지 확인한다.
- 현재 paired stdout SHA-256은
  `sha256:de54f8842b75bd1de711bbf0d309fff83b53010203ecf5b6945033b869565713`이며, retained
  projection hash는 `sha256:0e3e7e4ef2ae40c0b6e68673774afe7cc2d8b74a122fb38438d7ddf8371b2b07`다.
- production event/SQLite schema, migration, concurrent writer/crash replay와 calibration은
  Phase 5/7 및 후속 evidence에서 별도로 검증한다.

## 후속 미결정

- production fingerprint schema와 merge/split conflict policy
- event/SQLite schema, evaluator migration과 project-scoped memory writer authority
- verified/enforced lesson의 revocation, pin/reject/deprecate/supersede와 compiled transition
- OQ-011 runtime/evidence retention 및 memory bootstrap/repair policy

## Decision receipt

- **Decision:** C-01 deterministic evidence-gated lesson evaluator; recurrence `2`, eligible
  unassisted success `3`, minimum age `7 days`
- **Actor:** `user-delegated-autonomous-delivery` under the explicit AUTOPILOT delegation
- **Recorded at:** `2026-08-22T16:04:00Z`
- **Reference:** [USER-DECISION-OQ010-001](../research/phase-0/evidence/OQ-010/USER-DECISION-RECEIPT-001.md)
