# Failure Learning and Memory Guide

> 상태: Accepted principles and evaluator thresholds / implementation TBD

## 1. 목적

실행 중 발견된 잘못된 가정을 재사용 가능한 guard로 바꾸되, 일회성 실패가 장기
프롬프트 기억으로 남지 않게 한다.

## 2. 핵심 구분

```text
runtime failure event
  → candidate
  → probationary
  → verified
  → enforced
  → compiled
```

종료 상태:

```text
expired | rejected | superseded | deprecated
```

- Candidate는 runtime 단기 상태다.
- Verified/enforced lesson만 일반 memory retrieval 대상이다.
- Compiled는 test/lint/type/schema/code guard로 자동화돼 prompt에서 제외된다.

## 3. Failure event

최소 필드:

```text
event_id / run_id / attempt_id
project/task/workspace
phase / AC / step
trigger context
wrong assumption
observed actual rule
root cause candidate
failure category
structured fingerprint
evidence refs
occurred_at
```

LLM이 root cause나 rule 문구를 제안할 수 있지만 evidence와 구조화 필드는 Controller가
검증한다.

## 4. Candidate

Candidate 최소 필드 예시:

```yaml
id: LESSON-017
status: candidate
scope:
  project: current
  modules: [payment]
  task_types: [retry, failure-counter]
trigger: 결제 실패를 집계하거나 재시도 정책을 계획할 때
wrong_assumption: 동일 결제를 사용자 ID 기준으로 묶는다고 가정했다.
actual_rule: 결제 실패는 주문 ID 기준으로 집계한다.
root_cause: 기존 코드의 aggregate key를 확인하기 전에 AC를 작성했다.
proposed_guard: AC 작성 전 PaymentAttempt aggregate key를 확인한다.
evidence_refs: [EVIDENCE-...]
```

Candidate는 저장되지만 task 시작 시 자동 검색·주입하지 않는다.

## 5. Fingerprint

정확한 event/schema는 TBD지만 다음 축을 v1 fingerprint policy의 필수 축으로 사용한다.

- project와 phase
- module/file/symbol 또는 domain entity
- task type
- failure category
- violated rule 또는 invariant
- normalized trigger/action

메시지 문자열 전체나 stack trace의 변동 값을 fingerprint로 사용하지 않는다. 동일한
원인이 합쳐지고 다른 원인이 분리되는지 fixture로 검증한다. promotion threshold와
event/evaluator version은 [ADR-0018](./adr/0018-learning-evaluator-thresholds.md)이
소유한다.

## 6. Eligible exposure

“다시 실패하지 않았다”를 판단하려면 실제로 같은 문제가 발생할 기회가 있었는지
측정해야 한다.

- scope와 trigger가 현재 task에 일치할 때만 eligible exposure다.
- lesson이 prompt에 주입됐는지 기록한다.
- lesson을 주입하지 않은 exposure가 성공하면 `unassisted success`다.
- 관련 없는 task의 성공은 감쇠 근거가 아니다.
- guard가 실행돼 문제를 막았으면 별도의 prevented count로 기록한다.

## 7. 상태 전이

LLM은 상태를 직접 바꾸지 않는다. Controller evaluator가 versioned rule과 event로
전이한다.

### Verified 후보

- 같은 fingerprint가 독립 run에서 반복됨
- 또는 재현 가능한 fail-before/pass-after guard evidence가 존재함
- scope와 actual rule이 서로 모순되지 않음
- evidence가 current code/project context에 유효함

Accepted v1 policy는 독립 run 2회 재발 또는 deterministic guard evidence다. 같은 run의
중복은 독립 recurrence로 세지 않으며, evaluator와 event lineage의 version을 보존한다.

### Expired 후보

- candidate/probationary 상태이며
- 실제 eligible exposure에서 lesson 주입 없이 여러 번 성공했고
- 최소 관찰 기간을 충족했으며
- 재발 또는 guard prevention evidence가 없음

Accepted v1 policy는 eligible unassisted success 3회와 최소 7일의 관찰 기간이다. injected,
ineligible 또는 unrelated success는 count에서 제외하며, 단순 시간 경과만으로는 충분하지
않다. 자세한 전이는 [ADR-0018](./adr/0018-learning-evaluator-thresholds.md)이 소유한다.

### Compiled

- guard가 자동 test/lint/type/schema/code constraint로 구현됨
- 해당 guard가 release/verification 경로에서 실제로 실행됨
- failure가 guard에 의해 차단된다는 test가 있음

Compiled lesson은 audit history를 유지하지만 일반 prompt 검색에서 제외한다.

## 8. Memory query

```text
exact fingerprint
→ project/module/task/file/symbol filter
→ status = verified|enforced
→ SQLite FTS5 rank
→ top-K compact summary
→ selected evidence lazy-load
```

기본 제안:

- top-K 3
- summary 하나 최대 400자
- 전체 memory context 목표 512 model token
- 반환 필드: lesson ID, actual rule, guard, 짧은 관련성, evidence reference
- full evidence와 historical events는 기본 반환하지 않음

## 9. Audit와 rebuild

- `events.jsonl`에 observed, merged, exposure, transition, pin/reject 등의 event를 append한다.
- event에는 evaluator/rule version을 기록한다.
- SQLite lesson/FTS index는 JSONL에서 재구축 가능해야 한다.
- 수정은 과거 event를 덮지 않고 correction/supersede event로 표현한다.
- memory DB 손상은 runtime task completion을 자동 취소하지 않지만 retrieval을
  `BLOCKED` 또는 degraded mode로 명시한다.

## 10. 사용자 제어

사용자는 lesson을 다음처럼 관리할 수 있어야 한다.

- inspect와 evidence 조회
- pin/enforce
- reject
- scope 수정
- guard 수정
- deprecate/supersede
- project/team export 여부 결정

사용자 edit도 event와 revision을 남긴다.

## 11. 테스트 matrix

- 최초 failure는 candidate로만 저장
- 동일 fingerprint merge와 다른 root cause 분리
- unrelated success는 exposure로 계산하지 않음
- injected success와 unassisted success 구분
- independent recurrence threshold
- guard fail-before/pass-after 승격
- TTL만으로 expire하지 않음
- compiled lesson retrieval 제외
- top-K와 context budget
- JSONL → SQLite/FTS rebuild
- evaluator version migration
- concurrent event/write single-writer enforcement
