# MCX Reference Findings

> 조사 상태: verified observation
> 조사일: 2026-08-10
> 원본: [`FRONT-JB/mcx`](https://github.com/FRONT-JB/mcx)
> 고정 커밋: `c49d2493f94fba6928ed20a46c9db8aecdcd3087`

## 1. 조사 목적

Geness 자체 개발을 대화나 단일 PLAN에만 의존하지 않고, 새 에이전트가 문서를 읽고
현재 Gate에서 안전하게 이어갈 수 있게 하는 구조를 확인했다.

[고정 commit의 docs](https://github.com/FRONT-JB/mcx/tree/c49d2493f94fba6928ed20a46c9db8aecdcd3087/docs)와
root `AGENTS.md`, `CLAUDE.md` symlink를 직접 조사했다.

## 2. MCX에서 관찰한 소유권 분리

| 문서 유형 | 소유하는 내용 |
| --- | --- |
| Constitution | 목적, 제품 정체성과 절대 불변 조건 |
| Architecture | 구성 요소, 경계와 의존 방향 |
| Lifecycle | 단계, Gate와 상태 전이 |
| Stage Guide | 단계별 entry, output, verification과 exit |
| ADR | 채택 결정, 근거와 거절한 대안 |
| Progress | 계획이 아닌 evidence로 확인된 현재 상태 |
| Research | 관찰, 출처와 아직 채택하지 않은 해석 |

Root agent instruction은 이 상세 내용을 복제하지 않고 읽는 순서, HOLD/CLEAR, 작업
시작·종료 절차를 연결하는 짧은 포인터 역할을 한다.

## 3. Geness가 채택한 부분

- Constitution → Progress → 관련 설계·ADR 순의 세션 시작 절차
- 미래 계획과 검증된 현재 사실의 분리
- consequential decision을 ADR로 먼저 기록하는 docs-first workflow
- Research와 Accepted decision의 분리
- Stage Guide별 entry/output/exit/evidence 계약
- root `AGENTS.md`를 공통 지침으로 두고 `CLAUDE.md`를 symlink로 연결하는 방식
- `type(scope): 한국어 설명`, 한국어 본문, AI attribution trailer 금지를 명시하는
  [Git 규칙](https://github.com/FRONT-JB/mcx/blob/c49d2493f94fba6928ed20a46c9db8aecdcd3087/AGENTS.md#git-%EA%B7%9C%EC%B9%99)
- 사용자가 커밋을 요청하면 diff·자격증명을 확인한 뒤 현재 브랜치를 같은 작업에서
  `origin`에 push하는 권한 경계
- 한 번에 하나의 다음 검증 가능한 목표를 Progress에 남기는 규칙

## 4. Geness에 맞게 바꾼 부분

- MCX의 mission 용어 대신 Interview, Specification, Execution, Verification,
  Learning을 사용한다.
- 제품 개발 문서 `docs/`와 Geness가 대상 저장소에 만드는 `.geness/` task 문서를
  명시적으로 구분한다.
- Progress의 Implementation HOLD/CLEAR와 개별 task lifecycle Gate를 분리한다.
- Codex·Claude 공용 core, target `.geness/`, home `~/.geness/{runtime,memory}` 경계를
  Geness Architecture와 Storage 계약으로 정의한다.
- MCX의 구체 구현·명령·schema는 가져오지 않는다.

## 5. 운영상의 결론

`docs/README.md`가 문서 지도와 진실의 원천을 소유한다. `AGENTS.md`는 그 내용을
복제하지 않고 반드시 읽어야 할 문서와 금지 규칙만 제공한다. PLAN checkbox는 완료
evidence가 아니며, `docs/progress/README.md`만 Geness 자체 구현의 현재
Implementation HOLD/CLEAR를 소유한다.
