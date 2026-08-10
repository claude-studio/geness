# Verification Stage Guide

> 상태: Proposed v1 contract

## 1. 목적

승인된 AC와 실제 artifact를 독립적으로 검증하고, evidence가 있는 경우에만 task를
완료한다.

## 2. Entry contract

- 승인된 spec digest와 execution lineage가 있다.
- 각 실행 attempt와 changed path를 식별할 수 있다.
- verification command 또는 manual evidence procedure가 확정돼 있다.
- 검증 주체가 구현 worker의 완료 주장만 재사용하지 않는다.

## 3. 검증 층

### Mechanical

- 승인된 verify command의 exit/output
- artifact 존재와 content/hash
- typecheck, test, lint, build와 schema validation
- path와 scope containment

### Semantic

- AC outcome이 실제 사용자-visible 결과와 일치하는지
- 구현이 non-goal과 constraint를 위반하지 않는지
- evidence가 AC를 직접 지지하는지
- 관찰되지 않은 가정을 pass로 처리하지 않았는지

### Conditional manual

자동 검증이 불가능한 AC는 승인된 수동 절차와 관찰자를 기록한다. 모호한 “확인됨”
문구만으로 pass하지 않는다.

## 4. Evidence hierarchy

강한 순서의 예:

1. 재현 가능한 command와 literal/pattern 결과
2. exact artifact와 content/hash
3. 구조화된 integration/E2E observation
4. 명시적 manual procedure와 기록
5. 에이전트 서술

5번만 존재하면 AC는 통과하지 않는다.

## 5. AC verdict

각 AC는 최소 다음 값을 가진다.

```text
PASS | FAIL | INDETERMINATE | NOT_RUN
evidence_refs[]
verified_at
verifier identity/type
spec_digest
reason
```

- `INDETERMINATE`를 PASS로 축약하지 않는다.
- command 실행 실패와 criterion failure를 구분한다.
- stale digest의 evidence를 current revision에 재사용하지 않는다.

## 6. Completion Gate

`COMPLETED` 조건:

- required AC 전부 `PASS`
- AC별 current digest evidence 존재
- open scope/contract violation 없음
- blocker 없음
- project docs와 runtime state reconciliation 성공
- independent completion audit 통과
- final `run.md` projection 완료
- completion transaction에서 terminal checkpoint와 lease release가 함께 성공

하나라도 충족하지 못하면 `HOLD`이며 failure category에 따라 execution, specification,
user decision 또는 system recovery로 route한다.

Verification은 먼저 `READY_TO_COMPLETE`를 선언한다. final `run.md` projection과
reconciliation 뒤 Controller가 한 runtime transaction에서 terminal checkpoint를
기록하고 lease를 해제한다. active lease가 남아 있으면 `COMPLETED`를 노출하지 않는다.
정확한 순서는 [Lifecycle](./02_TASK_LIFECYCLE.md#9-completion)이 소유한다.

## 7. Verification 후 lesson event

- 잘못된 assumption이 evidence로 확인되면 runtime failure event를 만든다.
- lesson 문구 생성과 memory 승격을 같은 단계에서 하지 않는다.
- 성공한 eligible exposure와 사용된 lesson ID를 learning evaluator 입력으로 기록한다.
- 자동 guard가 실제로 실행됐는지 evidence를 남긴다.

## 8. 테스트 matrix

- all-pass completion
- one required AC fail
- command error vs criterion fail
- stale evidence rejection
- artifact missing/content mismatch
- semantic scope violation
- manual procedure incomplete
- worker self-verification only
- completion audit disagreement
- final projection/lease release failure
