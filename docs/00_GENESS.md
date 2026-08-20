# Geness Project Constitution

> 상태: Accepted baseline
> 적용 범위: Geness 플러그인 소스, 문서, 테스트와 배포

## 1. 정체성

Geness는 Codex와 Claude Code에서 작동하는 인터뷰 기반 작업 제어 플러그인이다.
모호한 요청을 곧바로 구현하지 않고, 반복 질문으로 사용자의 암묵지를 드러내며,
승인된 문서를 실행 계약으로 고정한다. 실행은 검증 가능한 AC와 evidence를 기준으로
완료하며, 잘못된 가정은 일단 실패 후보로 보존한 뒤 측정 가능한 규칙을 통과한
경우에만 장기 기억으로 승격한다.

> **Geness turns tacit decisions into verified work.**

Geness는 코딩 모델 자체가 아니다. 모델과 작업 에이전트를 조정하고, 계약과 상태를
보존하며, 승인과 완료 Gate를 강제하는 control plane이다.

사용자에게 노출하는 표준 stage는 `brief → contract → plan → impl → verify → done`이며,
검증 실패를 자동으로 복구할 수 있을 때 `resume`으로 이어진다. 이 이름들은 UX alias이고
상태 전이의 권위는 아래 canonical lifecycle과 Controller에 있다.

## 2. North Star

사용자는 어느 호스트에서 시작하더라도 다음 경험을 가져야 한다.

```text
질문으로 결정한다
→ 문서로 승인한다
→ 계획으로 제한한다
→ 실행한다
→ evidence로 검증한다
→ 필요한 교훈만 남긴다
```

대화가 끊기거나 Codex와 Claude 사이를 이동해도 target repository의 문서와 공통
Controller 상태만으로 작업을 이어갈 수 있어야 한다.

v1의 resume은 같은 컴퓨터, 같은 `GENESS_HOME`, 사용자가 미리 준비한 같은
branch/worktree에서만 보장한다. Geness는 Git branch/worktree를 생성·전환·삭제하지
않는다. task에는 active writer 하나만 두고, 두 번째 host/process는 observer로 제한한다.

## 3. 규범 언어

- `MUST`, `MUST NOT`: 위반하면 제품 계약 위반이다.
- `SHOULD`, `SHOULD NOT`: 특별한 근거가 없으면 따른다.
- `MAY`: 선택 가능한 구현이다.
- `Accepted`: 현재 규범이다.
- `Proposed`, `TBD`: 구현 편의로 임의 확정할 수 없다.

## 4. 역할과 권한

### 사용자

- 목표, 비목표, trade-off, 위험 허용치와 새로운 동작을 결정한다.
- spec과 policy가 사용자 권한으로 분류한 plan revision을 승인한다.
- scope 확대, 외부 쓰기와 파괴적 행동을 승인한다.

### Geness Skill

- 사용자와 대화하고 질문 순서를 조율한다.
- 코드 사실과 사용자 판단을 routing한다.
- 답변 refine, restatement와 명시적 승인을 수행한다.
- Core가 드러낸 상태를 사용자에게 설명한다.

### Geness Controller

- schema, 상태 전이, digest, lease, checkpoint와 memory evaluator를 결정적으로
  처리한다.
- 동일 입력에서 같은 판정을 내려야 하는 규칙의 권위자다.
- 사용자를 대신해 판단하거나 승인하지 않는다.

### 작업 에이전트

- 승인된 allowed scope 안에서 조사·구현·검증한다.
- 자신의 작업을 스스로 최종 승인하지 않는다.
- 요구사항을 조용히 수정하지 않는다.

### Codex·Claude adapter

- 각 호스트의 manifest, MCP, hook과 session 정보를 공통 Controller에 연결한다.
- 도메인 규칙이나 별도의 canonical state를 소유하지 않는다.

## 5. 진실의 원천

우선순위는 [문서 안내](./README.md#진실의-원천-우선순위)를 따른다. 특히 다음을
구분한다.

- `PLAN.md`는 미래 작업과 완료 조건이다. 현재 완료 증거가 아니다.
- `progress/README.md`는 실제 테스트·artifact·관찰로 확인한 현재 사실만 담는다.
- `research/`는 관찰의 출처와 확실성을 담으며 채택 여부를 결정하지 않는다.
- 대상 저장소의 승인된 `spec.md`는 해당 task 실행 계약이다.

## 6. 헌법적 원칙

### Principle 1 — Interview before specification

중요한 미결정이 남아 있으면 문서를 확정하지 않는다. 질문 횟수나 LLM 자신감은
인터뷰 종료 근거가 아니다.

### Principle 2 — Specification before execution

승인된 spec과 실행 가능한 AC 없이 구현하지 않는다. 승인된 계약이 변경되면 digest를
무효화하고 사용자에게 돌아간다.

### Principle 3 — Human judgment remains human

코드에서 관찰한 사실을 사용자의 요구사항으로 자동 승격하지 않는다. 선호와 새로운
동작은 사용자가 결정한다.

### Principle 4 — Evidence over reasoning

에이전트의 완료 주장은 완료 증거가 아니다. 모든 필수 AC에 검증 evidence가 있어야
한다.

### Principle 5 — Durable state over conversation memory

대화 transcript나 host session ID를 canonical task state로 사용하지 않는다.
프로젝트 문서와 Controller checkpoint가 재개의 근거다.

### Principle 6 — Core is host-neutral

Codex와 Claude의 세부사항은 adapter 경계에 둔다. Skill, CLI, MCP가 서로 다른 상태
판정을 구현하지 않는다.

### Principle 7 — Scope is a hard boundary

승인된 allowed scope 밖 개선은 구현하지 않는다. 필요하면 기록하고 사용자에게 scope
변경을 요청한다.

### Principle 8 — One writer, observable readers

동일 project/task에는 한 writer만 허용한다. 다른 host와 session은 observer가 될 수
있으며 명시적인 safe takeover만 허용한다.

### Principle 9 — A failure is not a memory

실패는 runtime candidate다. 재발, 재현 가능한 인과관계 또는 guard 효과가 규칙으로
확인되기 전에는 일반 memory 검색에 노출하지 않는다.

### Principle 10 — Recovery is bounded

같은 fingerprint의 반복 실패를 무한 재시도하지 않는다. 재계획, 사용자 판단 또는
typed `BLOCKED`로 종료한다.

### Principle 11 — Small relevant context

전체 transcript, memory와 evidence를 프롬프트에 넣지 않는다. 필요한 구조화 요약과
선택된 evidence만 지연 로딩한다.

### Principle 12 — Documentation before consequential change

상태, Gate, 데이터 소유권, 의존 방향, 권한 또는 기억 알고리즘을 바꿀 때 문서와 ADR을
코드보다 먼저 갱신한다.

## 7. 데이터 경계

```text
Geness 소스 저장소의 docs/
  = Geness 제품을 개발하기 위한 규범과 계획

대상 저장소의 .geness/
  = 사용자가 검토·커밋하는 project ID와 task 문서

사용자 홈의 ~/.geness/runtime/
  = 실행 상태, lease, 원본 로그·evidence와 실패 후보

사용자 홈의 ~/.geness/memory/
  = 검증된 lesson event와 검색 인덱스

plugin 설치/cache 디렉터리
  = 읽기 전용 코드와 template
```

이 경계를 바꾸는 것은 consequential architecture change다.

## 8. 표준 lifecycle

```text
INITIALIZING
→ INTERVIEWING
→ SPEC_READY
→ SPEC_APPROVED
→ PREFLIGHT
→ PLAN_READY
→ PLAN_APPROVED
→ RUNNING
→ VERIFYING
→ COMPLETED
```

`PAUSED`, `BLOCKED`, `REOPENED`, `FAILED`, `CANCELLED`는 happy path 밖의 상태다.
정확한 terminal/recovery 의미와 전이는 [Task Lifecycle](./02_TASK_LIFECYCLE.md)과
Phase 0 결정이 소유한다.

Public alias와 내부 상태의 관계는 다음과 같다.

| Public alias | Canonical state 또는 의미 |
| --- | --- |
| `brief` | `INTERVIEWING` |
| `contract` | `SPEC_READY → SPEC_APPROVED` |
| `plan` | `PREFLIGHT → PLAN_READY → PLAN_APPROVED` |
| `impl` | `RUNNING` |
| `verify` | `VERIFYING` |
| `done` | Controller가 `COMPLETED`를 닫는 transaction |
| `resume` | `PAUSED`, `BLOCKED`, `REOPENED`에서 재개하는 action |
| `setup` | task 이전 project/workspace readiness |

## 9. 완료의 의미

Geness task가 완료되려면 최소한 다음이 모두 사실이어야 한다.

- 승인된 contract digest와 실제 실행 입력이 일치한다.
- 모든 필수 AC가 통과했다.
- 각 AC에 검증 evidence가 연결됐다.
- 승인되지 않은 scope·요구사항 변경이 없다.
- blocker가 열려 있지 않다.
- `run.md`와 runtime checkpoint가 최종 상태를 반영한다.
- `verification.md`가 최종 verify verdict와 evidence projection을 반영한다.
- writer lease가 해제됐다.

## 10. 변경 거버넌스

### Editorial change

의미를 바꾸지 않는 오탈자, 링크, 표현과 예시 개선이다.

### Design change

헌법 안에서 schema, API, 저장 기술이나 adapter를 선택하는 변경이다. 되돌리기
비싸거나 여러 계층에 영향을 주면 ADR을 작성한다.

### Constitutional change

다음은 사용자의 명시적 승인과 ADR이 필요하다.

- 제품 목적 또는 기본 workflow 변경
- 사용자 판단·승인 권한 완화
- 승인 spec 불변성과 digest 규칙 완화
- evidence 없이 완료할 수 있는 예외
- Core host-neutrality 변경
- 프로젝트 문서와 사용자 로컬 데이터 경계 변경
- candidate를 검증 없이 memory로 승격하는 경로
- scope 또는 one-writer 원칙 완화

## 11. 새 세션 온보딩

새 에이전트는 구현 전에 다음을 수행한다.

1. 이 문서를 끝까지 읽는다.
2. [Progress](./progress/README.md)의 실제 상태와 Implementation HOLD/CLEAR를 확인한다.
3. 관련 Architecture, Lifecycle, Stage Guide와 Accepted ADR을 읽는다.
4. Git 상태와 사용자가 둔 기존 변경을 확인한다.
5. 요청을 현재 Phase/Stage, Goal, Non-goal, authority로 다시 표현한다.
6. 미결정 항목을 구현 편의로 확정하지 않는다.
7. 변경 전에 검증 방법과 필요한 문서 업데이트를 정한다.

다음 질문에 답할 수 없으면 구현 전에 문맥을 더 읽어야 한다.

- Geness는 무엇이며 무엇이 아닌가?
- 사용자 판단과 코드 사실은 어떻게 분리되는가?
- target `.geness/`와 home `~/.geness/`는 무엇이 다른가?
- 승인 digest가 바뀌면 왜 실행할 수 없는가?
- 왜 failure candidate가 곧 memory가 아닌가?
- 누가 task 상태와 completion을 판정하는가?
- 현재 구현 가능한 가장 작은 검증 목표는 무엇인가?
