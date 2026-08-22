# ADR-0017: Versioned semantic contract and plan digests

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-007은 contract와 plan digest가 사람이 편집하는 Markdown bytes를 그대로
해시할지, semantic projection을 안정적으로 해시할지를 비교했다. OQ-006과
ADR-0016은 portable Markdown과 runtime mutable state의 owner를 분리했으므로,
digest도 document formatting이 아니라 승인 가능한 semantic contract의 revision을
식별해야 한다.

`FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001`은 같은 입력을 두 번 실행해 30/30 assertion을
통과했다. object key reorder는 같은 digest를 냈고, contract/plan semantic change는
서로 다른 digest를 냈으며, raw Markdown editorial change는 raw-byte candidate에서만
digest를 바꿨다.

## 결정

1. contract와 plan digest는 raw Markdown/frontmatter bytes가 아니라 명시적인
   **versioned semantic projection**에서 계산한다.
2. 현재 v1 profile identifier는 `geness.semantic-json-v1`이며 hash algorithm은
   SHA-256이다. artifact와 runtime receipt는 digest와 함께 profile/version을
   기록해야 한다.
3. contract projection은 profile, goal, non-goals, constraints, decisions, relevant
   context, acceptance criteria와 execution/retry policy처럼 계약·실행 의미를 바꾸는
   field를 포함한다. plan projection은 current contract digest와 plan steps,
   dependency/order, allowed scope와 test policy처럼 실행 의미를 바꾸는 field를
   포함한다.
4. `status`, timestamp, run result, checkpoint, lease와 raw editorial body처럼
   mutable 또는 presentation-only인 값은 해당 approval digest에서 제외한다. object
   key ordering은 의미가 아니며 array order는 의미가 있는 순서로 보존한다.
5. canonical bytes는 UTF-8 JSON serialization으로 만들고, profile이 정한 key,
   number, Unicode, duplicate-key와 escaping 규칙을 따른다. 구현체의 기본 serializer
   동작을 profile 대신 암묵적으로 사용하지 않는다. 이 edge-case 규칙의
   cross-runtime golden vector와 migration evaluator는 Phase 1 evidence로 검증한다.
6. semantic projection의 변경은 approval과 downstream plan/run을 stale로 만든다.
   editorial-only Markdown 변경은 semantic projection이 같다면 approval을
   무효화하지 않는다.
7. 승인 receipt와 digest/profile metadata는 target `spec.md` projection과 runtime
   canonical state에 함께 기록하되, 문서 projection은 completion authority가 아니다.

이 결정은 RFC/JCS compatibility, production serializer package, schema/migration,
Unicode/number edge-case의 구현 세부 또는 Implementation `CLEAR`를 확정하지 않는다.

## 결과

- 의미 없는 Markdown formatting 때문에 승인과 plan이 재실행되는 false invalidation을
  줄인다.
- semantic change가 current digest와 downstream freshness를 무효화하는 기준이
  명확해진다.
- profile/version과 golden vector를 통해 cross-host serializer drift를 발견할 수 있다.
- exact cross-language serializer profile, migration/old digest handling과 production
  transaction enforcement는 Phase 1 및 후속 implementation evidence가 필요하다.

## 거절한 대안

- **C-02 canonical YAML/frontmatter:** parser, scalar, duplicate-key와 serializer
  ordering semantics를 host 간 동일하게 고정할 근거가 부족하다.
- **C-03 raw Markdown/frontmatter bytes:** editorial whitespace와 key ordering까지
  semantic invalidation으로 취급해 false invalidation을 만든다.

## 검증 방법

- [OQ-007 packet](../research/phase-0/OQ-007-digest-canonicalization.md)의 candidate
  matrix와 현재 [RUN-OQ007-002](../research/phase-0/evidence/OQ-007/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-002/RUN.md)를 확인한다.
- fixture를 `PYTHONDONTWRITEBYTECODE=1 python3 runner.py`로 두 번 실행한다.
- 두 실행이 exit `0`, 30/30 assertions, `all_assertions_pass=true`이고 paired stdout이
  byte-identical인지 확인한다.
- production Go serializer, cross-language edge vector, migration과 stale transaction
  enforcement는 Implementation 전 별도 evidence로 검증한다.
