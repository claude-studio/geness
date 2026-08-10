# Specification and Planning Stage Guide

> 상태: Proposed v1 contract

## 1. 목적

승인된 interview를 검증 가능한 실행 계약으로 변환하고, 실제 repository를 점검한 뒤
AC와 구현 plan을 확정한다.

## 2. Entry contract

- current interview revision의 closure audit가 통과했다.
- 사용자가 one-sentence restatement를 승인했다.
- blocking open question과 contradiction이 없다.
- source provenance가 저장됐다.

## 3. `spec.md` 최소 계약

```yaml
schema_version: 1
task_id: task-...
status: draft | approved | reopened
source_interview_revision: 1
contract_digest: sha256:...
approval:
  approved_at: null
  approved_by: null
goal: ...
non_goals: []
constraints: []
context:
  cwd: .
  relevant_paths: []
acceptance_criteria: []
open_questions: []
execution:
  allowed_scope: []
  test_policy: ...
completion_policy: all_required_acceptance_criteria_verified
```

본문은 problem, decisions, domain rules, exceptions, assumptions와 source refs를 사람이
읽을 수 있게 설명한다.

## 4. Requirement projection

- user decision만 requirement authority를 가진다.
- code/research observation은 context 또는 evidence로 유지한다.
- observation에서 새로운 요구사항을 추론해 추가하지 않는다.
- unresolved/deferred 항목은 owner, impact와 execution blocker 여부를 명시한다.
- non-goal과 constraint를 누락하거나 확장하지 않는다.

## 5. Acceptance Criteria

각 AC는 다음을 가진다.

```text
id
outcome
verify command 또는 manual check
exact artifact paths
expected observable result
required 여부
source requirement refs
```

규칙:

- AC는 구현 순서가 아니라 완료된 결과 상태다.
- 최소 한 개 이상의 AC가 필요하다.
- 모든 requirement가 하나 이상의 AC로 추적된다.
- 자동 검증이 불가능하면 명확한 수동 evidence 절차가 필요하다.
- repository에 존재하지 않는 명령을 사실처럼 만들지 않는다.
- artifact path는 target root 기준의 정확한 상대 경로다.
- AC identity는 revision 사이에서 추적 가능해야 한다.

## 6. Contract digest와 approval

- digest 대상은 goal, non-goals, constraints, relevant context, AC와 execution policy다.
- status, timestamp와 run result는 digest에서 제외한다.
- canonical serialization과 hash algorithm은 versioned contract다.
- 사용자는 digest가 표현하는 현재 spec을 명시적으로 승인한다.
- 의미 있는 hash 대상 변경은 approval과 downstream plan/run을 무효화한다.
- 에이전트가 approval actor를 사칭하거나 implicit approval로 처리하지 않는다.

## 7. Preflight

Spec 승인 후 plan을 확정하기 전에 다음을 실제로 확인한다.

- Git root, branch, worktree와 dirty state
- `.geness/project.json` identity
- relevant files, symbols, schemas와 existing tests
- build/test/lint command 존재 여부
- dependency, network, permission과 외부 service 제약
- allowed scope와 예상 변경 경로
- 과거 verified/enforced lesson top-K
- code 근거 없이 남은 assumption

잘못된 가정이 contract에 영향을 주면 interview/spec을 reopen한다. AC 문구만 조용히
고치지 않는다.

## 8. `plan.md`

Plan은 다음을 포함한다.

- spec digest와 preflight snapshot
- requirement ↔ AC ↔ step traceability
- step dependencies와 실행 순서
- 변경 예상 파일과 경계
- AC별 verifier와 evidence 산출 방식
- 실패·중단·재계획 조건
- destructive/external action approval point
- 필요할 경우 plan digest와 approval

모든 plan은 `PLAN_APPROVED` Gate를 거치되 approval actor는 `user | policy`다. 일반
plan을 policy가 승인할 수 있는지는 Phase 0에서 확정한다. 결정 전에는 사용자 승인을
생략하지 않는다. scope 확대, 파괴적 행동, 외부 쓰기와 high-risk migration은 항상
별도 사용자 승인 없이는 실행할 수 없다.

## 9. Exit Gate

- spec schema와 contract digest 유효
- explicit spec approval
- 모든 requirement ↔ AC trace 존재
- 모든 AC에 verifier/evidence 방법 존재
- plan dependency와 allowed scope 유효
- blocking open question 0
- stale preflight가 아님
- 필요한 plan approval과 actor receipt 존재

## 10. 테스트 matrix

- observation withholding
- non-goal/constraint exact preservation
- outcome-oriented AC validator
- requirement coverage와 duplicate AC identity
- nonexistent verify command HOLD
- manual evidence contract
- canonical digest determinism
- editorial/semantic change 분류
- approval invalidation cascade
- preflight assumption mismatch reopen
- plan scope escape 차단
