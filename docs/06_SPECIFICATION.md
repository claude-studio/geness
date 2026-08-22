# Specification and Planning Stage Guide

> 상태: Proposed v1 contract

## 1. 목적

승인된 interview를 검증 가능한 실행 계약으로 변환하고, 실제 repository를 점검한 뒤
AC와 구현 plan을 확정한다.

## 2. Entry contract

- `setup`이 `SETUP_READY`이며 task의 host profile과 capability snapshot이 저장됐다.
- current interview revision의 closure audit가 통과했다.
- 사용자가 one-sentence restatement를 승인했다.
- blocking open question과 contradiction이 없다.
- source provenance가 저장됐다.

## 3. `spec.md` 최소 계약

~~~yaml
schema_version: 1
task_id: ...
contract_revision: 1
status: candidate | approved | reopened
source:
  brief_id: ...
  brief_revision: 1
profile: auto
digest_profile: geness.semantic-json-v1
contract_digest: sha256:...
approval:
  brief_restate: approved
  contract_adoption: pending | approved
  approved_at: null
  approved_by: null
goal: ...
non_goals: []
constraints: []
decisions: []
context:
  relevant_paths: []
  verified_facts: []
acceptance_criteria:
  - id: AC-001
    outcome: ...
    required: true
    mechanical:
      command: null
      expect: null
    acting:
      required: false
      procedure: null
      timeout_seconds: null
    manual:
      procedure: null
      observer: null
    artifacts: []
    source_refs: []
execution:
  allowed_scope: []
  forbidden_scope: []
  test_policy: ...
  retry:
    max_successors: 5
completion_policy: all_required_acceptance_criteria_verified
~~~

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

~~~text
id
outcome
required
mechanical command/expect
acting required/procedure/timeout_seconds
manual procedure/observer
artifacts
source_refs
~~~

규칙:

- AC는 구현 순서가 아니라 완료된 결과 상태다.
- 최소 한 개 이상의 AC가 필요하다.
- 모든 requirement가 하나 이상의 AC로 추적된다.
- 자동 검증이 불가능하면 명확한 수동 evidence 절차가 필요하다.
- API·CLI·UI·integration처럼 동작을 주장하는 AC는 mechanical 결과와 acting observation을
  모두 요구한다. 정적 artifact는 mechanical로, 자동화할 수 없는 AC는 승인된 manual
  procedure로 검증한다.
- repository에 존재하지 않는 명령을 사실처럼 만들지 않는다.
- artifact path는 target root 기준의 정확한 상대 경로다.
- AC identity는 revision 사이에서 추적 가능해야 한다.

## 6. Contract digest와 approval

- digest는 [ADR-0017](./adr/0017-versioned-semantic-digest.md)의
  `geness.semantic-json-v1` semantic projection profile과 SHA-256을 사용한다.
- contract digest 대상은 profile, goal, non-goals, constraints, decisions, relevant
  context, AC와 execution/retry policy이며, plan digest는 current contract digest와
  plan steps, dependency/order, allowed scope와 test policy처럼 실행 의미를 바꾸는
  field를 포함한다.
- canonical bytes는 profile이 정한 UTF-8 JSON serialization이다. object key order는
  의미가 아니며 array order는 보존한다. number, Unicode, duplicate-key와 escaping
  edge rule은 host serializer 기본값에 맡기지 않고 profile golden vector로 검증한다.
- status, timestamp, run result, checkpoint, lease와 editorial Markdown body는 approval
  digest에서 제외한다.
- semantic projection이 바뀌면 approval과 downstream plan/run을 무효화하고, 같은
  projection의 editorial-only 변경은 digest를 바꾸지 않는다.
- 사용자는 digest가 표현하는 현재 spec을 명시적으로 승인한다.
- 의미 있는 hash 대상 변경은 approval과 downstream plan/run을 무효화한다.
- 에이전트가 approval actor를 사칭하거나 implicit approval로 처리하지 않는다.

### Contract QA와 adoption

public `contract` 단계는 Codex가 candidate와 구조적 QA를 만들고, Claude가 결과를
사용자에게 설명하는 흐름이다.

1. QA `PASS`면 사용자는 compact digest를 확인한다.
2. QA `REVISE`면 제안된 후보별로 adoption/reject를 결정한다.
3. 채택한 후보만 새 contract revision에 반영하고 digest를 다시 계산한다.
4. `CONTRACT_APPROVED` 전에는 plan이나 impl을 시작하지 않는다.

brief restatement 승인과 contract digest adoption은 서로 다른 승인이며, QA PASS 후에는
같은 내용을 장문으로 반복 승인받지 않는다.

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

public `plan` 단계의 모든 plan은 `PLAN_APPROVED` Gate를 거치되 approval actor는 `user | policy`다. 일반
plan을 policy가 승인할 수 있는지는 Phase 0에서 확정한다. 결정 전에는 사용자 승인을
생략하지 않는다. scope 확대, 파괴적 행동, 외부 쓰기와 high-risk migration은 항상
별도 사용자 승인 없이는 실행할 수 없다.

### 8.1 Permission classification alignment

[OQ-015](./research/phase-0/OQ-015-threat-model-permission-policy.md)의 Accepted C-01 matrix와
[ADR-0009](./adr/0009-threat-model-permission-boundaries.md)에 따라 contract/plan은 다음
capability와 approval point를 명시해야 한다. exact risk tier와 policy approval은 OQ-008의
사용자 결정 전까지 `TBD`다.

| class | contract/plan requirement | default result |
| --- | --- | --- |
| `observe` | read-only paths/probes와 evidence reference | capability unavailable이면 `HOLD` |
| `approved_local_write` | target-relative allowed scope, forbidden scope, current digest와 writer lease | containment/scope/digest/lease mismatch면 `HOLD` |
| `user_sensitive` | scope expansion, external/destructive/security-boundary action의 user receipt와 target/intent | non-user 또는 stale receipt면 `HOLD` |
| `forbidden_v1` | runtime DB direct write, approval bypass, default danger-full-access, candidate promotion | 실행하지 않고 typed `HOLD` |
| `secret_handling` | redaction/minimization procedure와 no-project-storage rule | redaction 불확실성은 `HOLD`/local-only |

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
