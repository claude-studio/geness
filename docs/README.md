# Geness 문서 안내

이 디렉터리는 **Geness 자체를 개발하기 위한 문서 시스템**이다. Geness가 실제 작업
대상 저장소에 생성하는 `.geness/tasks/**`와는 역할이 다르다.

## 현재 상태

- 제품과 구현 계획은 [PLAN](./PLAN.md)에 정리돼 있다.
- 구현은 시작하지 않았다.
- 검증된 현재 상태와 구현 가능 여부는 [Progress](./progress/README.md)가 소유한다.
- 아직 확정하지 않은 구현 선택은 [Open Questions](./research/OPEN_QUESTIONS.md)에 둔다.

## 진실의 원천 우선순위

1. 사용자의 현재 명시적 결정
2. [Geness Constitution](./00_GENESS.md)
3. [Accepted ADR](./adr/README.md)
4. Architecture, Lifecycle, Storage, Host Integration과 Stage Guide
5. 승인된 대상 task의 `.geness/tasks/**/spec.md`와 `plan.md`
6. 테스트와 공개 인터페이스 계약
7. 구현
8. Progress와 실행 evidence
9. 채팅 기록과 추론

하위 문서나 구현이 상위 규범과 충돌하면 충돌을 숨기지 않는다. 상위 규범이 잘못된
경우에도 구현에 맞춰 조용히 고치지 않고 변경 절차와 사용자 승인을 거친다.

## 읽는 순서

새 에이전트 세션은 다음 순서로 읽는다.

1. [00_GENESS](./00_GENESS.md) — 목적과 불변 원칙
2. [Progress](./progress/README.md) — 검증된 현재 상태와 HOLD/CLEAR
3. 작업과 관련된 아래 문서
4. 관련 [ADR](./adr/README.md)
5. 필요한 [Research](./research/README.md)
6. [PLAN](./PLAN.md)의 해당 Phase와 완료 조건

## 문서 구조와 소유권

| 문서 | 소유하는 질문 |
| --- | --- |
| [00_GENESS](./00_GENESS.md) | 무엇을 왜 만들며 무엇을 절대 어기지 않는가? |
| [01_ARCHITECTURE](./01_ARCHITECTURE.md) | 구성 요소, 책임과 의존 방향은 무엇인가? |
| [02_TASK_LIFECYCLE](./02_TASK_LIFECYCLE.md) | task 상태, Gate와 되돌아가는 조건은 무엇인가? |
| [03_STORAGE](./03_STORAGE.md) | 프로젝트 문서, runtime, memory와 identity를 어디에 어떻게 보존하는가? |
| [04_HOST_INTEGRATION](./04_HOST_INTEGRATION.md) | Codex·Claude·Skill·CLI·MCP·hook의 경계는 무엇인가? |
| [05_INTERVIEW](./05_INTERVIEW.md) | 질문, 답변 authority와 인터뷰 종료 조건은 무엇인가? |
| [06_SPECIFICATION](./06_SPECIFICATION.md) | spec, AC, digest와 실행 전 점검 계약은 무엇인가? |
| [07_EXECUTION](./07_EXECUTION.md) | 실행, lease, checkpoint와 재개 규칙은 무엇인가? |
| [08_VERIFICATION](./08_VERIFICATION.md) | 어떤 evidence가 있어야 완료할 수 있는가? |
| [09_LEARNING](./09_LEARNING.md) | 실패 후보가 언제 memory가 되고 언제 사라지는가? |
| [PLAN](./PLAN.md) | 무엇을 어떤 순서와 완료 조건으로 구현할 것인가? |
| [ADR](./adr/README.md) | 왜 이 결정을 채택했고 어떤 대안을 거절했는가? |
| [Progress](./progress/README.md) | 실제 evidence 기준으로 지금 어디까지 완료됐는가? |
| [Research](./research/README.md) | 원본과 외부 자료에서 무엇을 관찰했는가? |

## 상태 용어

- `Proposed`: 검토할 설계 후보이며 아직 규범이 아니다.
- `Accepted`: 사용자 결정 또는 Accepted ADR로 현재 규범이 됐다.
- `Verified`: 테스트나 실물 관찰로 구현까지 확인됐다.
- `TBD`: 구현 전에 조사 또는 사용자 결정이 필요하다.
- `Superseded`: 다른 결정으로 대체됐다.
- `HOLD`: 다음 구현 Gate를 통과하지 못했다.
- `CLEAR`: 문서에 적힌 다음 단계 진입 조건을 evidence로 충족했다.

`PLAN`의 checkbox나 에이전트의 완료 보고는 `Verified` evidence가 아니다.

## 문서 기반 작업 흐름

```text
Research
→ consequential decision이면 ADR
→ Constitution/Architecture/Lifecycle/Stage Guide 갱신
→ PLAN의 현재 Phase와 Gate 확인
→ 최소 구현
→ 테스트와 실사용 evidence
→ Progress 갱신
→ 문서와 구현 drift 재검사
```

모든 작은 수정에 ADR을 요구하지는 않는다. 다음 변경은 코드보다 문서와 ADR이
먼저다.

- 상태나 Gate 의미 변경
- 승인 digest와 불변성 변경
- Core와 host adapter 의존 방향 변경
- `.geness/`와 `~/.geness/` 데이터 경계 변경
- memory 승격·만료 알고리즘 변경
- 권한, scope 또는 completion policy 완화
- 사용자-facing 명령과 문서 schema 변경
- Ouroboros 또는 채택한 참고 설계와 의도적으로 다르게 가는 핵심 동작

## 업데이트 규칙

- 계획은 `PLAN.md`, 검증된 현재 사실은 `progress/README.md`에 기록한다.
- 관찰과 설계 결정을 `research/`에 섞지 않는다. 결정은 ADR로 승격한다.
- Accepted ADR의 의미를 바꿀 때 기존 파일을 덮지 않고 새 ADR로 supersede한다.
- 문서에 존재하지 않는 테스트·명령·파일을 완료 evidence처럼 쓰지 않는다.
- 작업 종료 시 관련 문서와 Progress를 실제 결과에 맞춰 갱신한다.
- 링크, code fence, 용어와 상태 전이 일관성을 함께 검증한다.

## 구조의 출처

인터뷰와 실행 계약은
[`Q00/ouroboros`](https://github.com/Q00/ouroboros/tree/25f958dd7938d3c383ccfd14d551467bcf6e6bd6)의
specification-first workflow를 조사해 독립적인 Geness 계약으로 재정의했다. 채택한
원칙, 변경·비채택 범위와 MIT 라이선스 경계는
[Ouroboros Reference Findings](./research/OUROBOROS_REFERENCE_FINDINGS.md)에 기록한다.

문서 소유권 분리는 [`FRONT-JB/mcx`](https://github.com/FRONT-JB/mcx/tree/c49d2493f94fba6928ed20a46c9db8aecdcd3087/docs)의
Constitution, Architecture, Lifecycle, Stage Guide, ADR, Progress, Research 구조를
참고했다. Geness에 적용한 내용과 의도적으로 바꾼 내용은
[MCX Reference Findings](./research/MCX_REFERENCE_FINDINGS.md)에 기록한다.
