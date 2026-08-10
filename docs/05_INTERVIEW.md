# Interview Stage Guide

> 상태: Proposed v1 contract

## 1. 목적

사용자가 아직 말하지 않은 중요한 판단, 예외, 실패 동작과 검증 기준을 반복 질문으로
드러내고, provenance가 있는 승인 가능한 requirement set을 만든다.

Interview는 spec을 바로 쓰거나 코드를 실행하는 단계가 아니다.

## 2. Entry contract

- target project root와 project ID가 확인됐다.
- task ID와 초기 요청이 저장됐다.
- read-only repository exploration 권한이 정해졌다.
- 이전 interview revision이 있으면 stale write를 막을 revision을 읽었다.

## 3. Actors

- 사용자: 판단과 승인
- Skill/coordinator: 질문 routing, refine와 대화
- Question generator: 가장 영향이 큰 gap 하나를 질문으로 변환
- Code/research resolver: read-only 사실 조사
- Closure reviewers: closer, contrarian, gap-hunter
- Controller: revision, ledger, provenance와 Gate 판정

Closure reviewer가 자신의 발견을 요구사항으로 직접 추가하지 않는다. 발견은 blocker나
질문 후보가 되며 사용자 또는 검증된 code fact 경로로 해소한다.

## 4. 답변 authority

```text
from-user       사용자 판단·선호·승인
from-code       정확한 code/config/test 관찰
from-research   외부 1차 자료 관찰
```

- observation은 자동으로 user requirement가 되지 않는다.
- 질문에 판단이 조금이라도 섞이면 사용자에게 묻는다.
- code fact와 desired behavior가 같은지 별도로 구분한다.
- exact manifest/config literal처럼 해석이 필요 없는 사실만 자동 확인한다. 이름,
  control flow 또는 기존 동작에서 의도를 추론한 내용은 사용자 확인 없이 결정으로
  고정하지 않는다.
- 자유 답변은 Decision/Reasoning/Constraints/Out of scope/Code context로 정제하고
  사용자가 의미 보존을 확인한다.

## 5. 질문 loop

1. repository와 기존 task 문서에서 현재 사실을 읽는다.
2. scope, constraints, outputs, verification ledger를 갱신한다.
3. 열린 gap 중 downstream 영향이 가장 큰 하나를 고른다.
4. fact, judgment, mixed, research 중 route를 결정한다.
5. 사용자가 결정할 질문은 한 번에 하나씩 묻는다.
6. answer와 provenance를 저장하고 revision을 증가시킨다.
7. contradiction, assumption, deferred/open 상태를 다시 계산한다.
8. 종료 후보가 아니면 반복한다.

코드·research 경로의 non-user answer가 세 번 연속되면, 미해결 human judgment가 있는
한 다음 질문은 반드시 사용자에게 보낸다. 이 rhythm guard는 사실 조사로 인터뷰가
끝난 것처럼 보이는 상황을 막는다.

한 종류의 gap을 최대 세 번 닫은 뒤에는 전체 ledger breadth를 다시 점검한다. 수치
ambiguity score를 사용하더라도 질문 우선순위의 보조 신호일 뿐, closure나 승인을
대신하지 않는다.

## 6. Ledger

최소 추적 항목:

- goal
- scope와 non-goals
- constraints
- expected outputs
- failure behavior와 edge cases
- verification/acceptance
- assumptions
- contradictions
- open questions
- deferred decisions와 owner/impact

결정 수정은 이전 내용을 삭제하지 않고 `superseded_by` lineage를 남긴다.

## 7. 종료 후보와 closure audit

다음 조건을 모두 충족해야 closure audit을 시작한다.

- blocking open question 0
- unresolved contradiction 0
- 목표·범위·비목표·예외·실패 동작 존재
- 중요한 가정에 code/research 근거 또는 사용자 확인 존재
- 모든 요구사항을 검증 가능한 결과로 표현 가능

Audit lane:

- `closer`: 명세 생성에 필요한 결정이 충분한가?
- `contrarian`: 반례나 잘못된 기본 가정이 남았는가?
- `gap-hunter`: output, failure, ownership, verification 누락이 있는가?

closer 실패 또는 advisory lane의 HIGH finding은 종료를 차단한다. 발견을 해소한 뒤 현재
revision으로 audit을 다시 수행한다.

반대로 현재 revision이 위 조건과 audit을 통과하면 단순 wording preference나 가능성이
낮은 극단적 edge case만 찾기 위해 인터뷰를 계속하지 않는다. 새 질문은 계약, 위험 또는
검증 결과를 실질적으로 바꿀 수 있는 gap을 가리켜야 한다.

## 8. Restate와 승인

Audit 통과 후 합의 목표를 한 문장으로 restate한다. 사용자는 승인, 문구 수정 또는
누락 scope를 선택할 수 있다.

- 명시적 승인 전 spec을 승인 상태로 만들지 않는다.
- 수정은 refine 확인을 거친 interview correction으로 저장하고 closure 상태를 reopen한
  뒤 audit을 다시 실행한다.
- approval은 현재 interview revision에 묶인다.
- 단순 `done` 표현도 closure Gate를 우회하지 않는다.

여기서의 승인은 “인터뷰가 사용자의 의도를 정확히 담았다”는 승인이다.
[Specification](./06_SPECIFICATION.md)의 contract digest 승인을 대신하지 않는다.

## 9. Output

- `.geness/tasks/<task-slug>--<task-id>/interview.md`
- provenance가 있는 requirement/decision projection
- closure audit record
- 승인된 restatement와 source revision
- spec 생성에 필요한 handoff

## 10. HOLD 예시

- 사용자가 결정해야 할 trade-off가 열려 있음
- code fact와 앞선 답변이 충돌함
- 성공 기준을 검증 가능한 결과로 표현할 수 없음
- reviewer가 HIGH severity gap을 찾음
- answer refine가 아직 사용자 확인을 받지 못함
- current revision에 대한 closure audit가 없음

## 11. 테스트 matrix

- code fact 자동 해소와 user judgment 질문 구분
- mixed question은 사용자에게 route
- provenance 없는 answer 거부
- superseded decision lineage
- starvation guard
- closure 3-lane 병렬 결과의 결정적 합성
- stale revision audit/approval 거부
- restatement 수정 후 재감사
- 최소 질문 수만으로 종료하지 않음
- resume 후 같은 ledger와 next gap 복구
- 세 번의 non-user answer 뒤 human-judgment rhythm guard
- breadth 재점검과 closure 이후 over-interview 차단
- exact literal fact와 inferred intent의 authority 분리

질문 생성이나 reviewer 호출이 실패하면 작은 고정 retry budget 안에서만 같은 operation
ID로 재시도한다. budget이 소진되면 질문을 임의로 생략하거나 승인하지 않고 typed
`HOLD`로 남긴다. 정확한 budget은 Phase 0 policy로 확정한다.

## 12. 참고 기준

- [Ouroboros interview skill](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/skills/interview/SKILL.md)
- [Ouroboros Socratic interviewer](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/src/ouroboros/agents/socratic-interviewer.md)
- [Ouroboros seed closer](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/src/ouroboros/agents/seed-closer.md)
- [Geness의 Ouroboros 조사 및 차용 경계](./research/OUROBOROS_REFERENCE_FINDINGS.md)
