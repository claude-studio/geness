# ADR-0007: V1 contract schema and verification projections

> 상태: Accepted
> 날짜: 2026-08-20

## 맥락

Geness는 RPI의 사람이 읽는 계획 문서와 Ouroboros의 revision·adoption·bounded
verification 원칙을 함께 사용한다. 기존 Stage Guide의 schema를 그대로 복제하면
Geness의 host profile, acting verification, bounded successor와 setup 정보를 표현하기
어렵다.

## 결정

target task는 기존 문서 역할을 유지하되 Geness v1 contract schema를 새로 정의한다.

~~~text
.geness/tasks/<task>/
├── interview.md
├── spec.md
├── plan.md
├── run.md
└── verification.md
~~~

- interview.md는 brief의 질문·답변·provenance·closure projection이다.
- spec.md는 contract의 machine-readable frontmatter와 사람이 읽는 결정 본문이다.
- plan.md는 approved contract에서 파생된 plan projection이다.
- run.md는 impl attempt·checkpoint·변경 요약 projection이다.
- verification.md는 최종 verify 결과 projection이다.

새 contract schema의 핵심 필드는 다음과 같다.

~~~yaml
schema_version: 1
task_id: ...
contract_revision: 1
status: candidate
source:
  brief_id: ...
  brief_revision: 1
profile: auto
contract_digest: sha256:...
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

Codex는 contract candidate와 구조 QA를 만들고, QA REVISE 후보는 사용자가 adoption한
것만 반영한다. brief restate approval과 contract digest adoption은 서로 다른 artifact를
승인하지만, QA PASS 후에는 compact digest confirmation으로 처리해 중복 장문 승인을
피한다.

runtime DB가 mutable state, AC verdict, evidence freshness, verifier provenance와
completion authority의 정본이다. verification.md는 사람이 읽는 projection이며 stale
또는 수동 수정이 발견되면 Controller가 reconciliation한다.

behavior-bearing AC에는 mechanical와 acting observation을 모두 요구한다. 정적 AC는
mechanical, 자동화할 수 없는 AC는 승인된 manual procedure를 사용한다.

verify REVISE는 같은 contract/AC를 유지하는 successor attempt로 bounded convergence를
수행한다. 기본 상한은 task당 5회이며 contract 완화는 허용하지 않는다.

## 결과

- 문서와 runtime의 권한이 분리된다.
- contract schema가 host profile·verifier·retry policy를 추적할 수 있다.
- RPI 문서의 Git 가독성과 Ouroboros식 adoption/convergence를 함께 유지한다.
- schema validation, projection reconciliation, evidence freshness와 migration test가
  추가로 필요하다.

## 거절한 대안

- 기존 Stage Guide schema를 그대로 사용: Geness v1의 profile/acting/retry 요구를
  명확히 표현하지 못하므로 거절했다.
- 별도 contract.yaml과 spec.md를 동시에 정본으로 사용: 두 파일 drift 위험 때문에
  거절했다.
- Codex QA PASS를 곧바로 approval로 승격: 사용자 adoption과 human authority가
  사라지므로 거절했다.
- verification 결과를 run.md에만 포함: execution summary와 final verdict의 관심사가
  섞이므로 거절했다.

## 검증 방법

- schema parse/serialize/digest golden vector
- brief revision과 contract revision lineage
- QA PASS/REVISE/adoption fixture
- profile/retry policy digest invalidation fixture
- mechanical/acting/manual/semantic evidence fixture
- verification.md projection/reconciliation crash fixture
- five-successor bounded loop와 oscillation/budget stop fixture
