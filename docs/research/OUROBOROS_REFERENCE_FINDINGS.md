# Ouroboros Reference Findings

> 조사 상태: verified observation
> 조사일: 2026-08-10
> 원본: [`Q00/ouroboros`](https://github.com/Q00/ouroboros)
> 상세 분석 기준: `25f958dd7938d3c383ccfd14d551467bcf6e6bd6`
> 최신성 확인: `main`의 `76a16fb66466aadee39e5f8c7ece296b7c78b1e3`
> 라이선스: MIT, Copyright (c) 2025 Q00
> 현재 재사용 상태: 독립 설계, source file·장문 verbatim 복사 없음, 짧은 식별자와
> 구조적 용어는 출처를 밝힌 design influence로 유지

## 1. 조사 범위와 기준점

Geness는 Ouroboros 전체를 포팅하려는 프로젝트가 아니다. 다음 경험을 어떻게
구성하는지 확인하기 위해 interview skill, Socratic interviewer, closure audit,
Seed 계약과 실행 handoff를 조사했다.

- [고정 저장소 스냅샷](https://github.com/Q00/ouroboros/tree/25f958dd7938d3c383ccfd14d551467bcf6e6bd6)
- [Interview Skill](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/skills/interview/SKILL.md)
- [Socratic Interviewer](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/src/ouroboros/agents/socratic-interviewer.md)
- [Seed Closer](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/src/ouroboros/agents/seed-closer.md)
- [Seed Architect](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/src/ouroboros/agents/seed-architect.md)
- [MIT License](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/LICENSE)

2026-08-10에 `main`의 `76a16fb...`까지 다시 확인했고, 위 네 핵심 설계 파일과
LICENSE는 상세 분석 기준 commit 이후 변경되지 않았다. 상세한 행 단위 근거의
재현성을 위해 이 문서는 분석 기준 commit에 링크한다.

## 2. 관찰한 인터뷰 구조

### 질문 역할과 답변 역할을 분리한다

질문 엔진은 구현하지 않고 가장 큰 미결정을 겨냥한 질문을 만든다. 메인 세션은
질문을 `code fact`, `human judgment`, `code + judgment`, `research`로 분류한다.
정확히 확인 가능한 사실은 저장소에서 조사하지만, 선호·새 동작·trade-off는
사용자에게 되돌린다.

### 한 번에 가장 영향이 큰 질문 하나를 다룬다

질문 수를 채우는 것이 목적이 아니다. scope, non-goal, success, ownership, risk,
verification 중 현재 계약을 가장 크게 바꾸는 빈틈을 먼저 닫고, 답변마다 다음
질문을 다시 선택한다.

### 답변을 출처와 함께 정제한다

자유 답변은 decision, reasoning, constraints, out-of-scope, codebase context로
재진술하고 사용자가 누락이나 왜곡이 없는지 확인한다. 코드와 조사에서 얻은
관찰은 사용자 결정과 구분한다.

### 종료를 여러 Gate로 압박 검증한다

단순히 모델이 충분하다고 느끼거나 ambiguity score가 낮아졌다는 이유로 끝내지
않는다. visible ledger를 유지하고, `closer`, `contrarian`, `gap_hunter` 관점으로
누락·모순·검증 불가능성을 확인한 뒤 목표를 한 문장으로 다시 진술해 명시적 승인을
받는다.

타이트한 종료에는 양쪽 방향의 제한이 모두 있다.

- 중요한 미결정이 있으면 너무 일찍 종료하지 않는다.
- closure가 통과하면 단순 wording이나 극단적인 edge case만 더 파고들지 않는다.
- code/research 답변만 세 번 연속 처리했다면 다음에는 반드시 사용자 판단을 묻는다.
- restatement가 수정되면 interview를 reopen하고 refine과 closure audit를 다시 한다.
- non-human fact가 인터뷰 종료 의도를 대신하지 않는다.

### 승인된 결과를 실행 계약으로 결정화한다

Ouroboros의 일반 개발 경로는 interview state에서 immutable Seed를 만든다. Seed의
Acceptance Criteria는 완료 결과, 검증 command, artifact와 기대 output을 표현한다.
반면 project-local `.ouroboros/pm.md`는 다음 인터뷰의 입력이지 runnable 계약은 아니다.

## 3. Geness가 채택한 원칙

| Ouroboros에서 관찰한 원칙 | Geness 적용 |
| --- | --- |
| 질문 전담 역할 | Interview와 Execution 책임을 분리한다. |
| 가장 큰 불확실성 우선 | ledger의 highest-impact open item을 한 번에 하나 묻는다. |
| 사실과 판단의 routing | `from-user`, `from-code`, `from-research` provenance와 authority를 보존한다. |
| 답변 refine | 구조화한 답변을 사용자에게 확인한 뒤 decision으로 고정한다. |
| breadth ledger | scope/non-goal, constraint/context, output, verification track을 계속 점검한다. |
| closure pressure test | closer/contrarian/gap-hunter에 해당하는 독립 검토를 실행한다. |
| restate와 명시 승인 | 문서 생성 직전 한 문장 목표와 남은 deferred item을 확인한다. |
| 실행 가능한 AC | outcome, verify, artifacts, expect를 task 계약에 포함한다. |
| bounded convergence | 인터뷰·재계획·재시도에 명시적 상한과 HOLD/BLOCKED 결과를 둔다. |

이 채택 결정은 [ADR-0004](../adr/0004-ouroboros-interview-principles.md)가 소유한다.

## 4. Geness가 변경한 부분

- Ouroboros Seed YAML 대신 대상 저장소의 `.geness/tasks/**` Markdown 계약을 사용한다.
- 수치 ambiguity score는 자동 승인자가 아니라 질문 우선순위의 보조 신호로만 본다.
- PM 인터뷰와 개발 인터뷰를 나누지 않고 한 task ledger에서 product와 engineering
  결정을 닫는다.
- Ouroboros 전체 Agent OS가 아니라 Codex와 Claude가 공유하는 경량 controller로
  범위를 제한한다.
- target repository의 검토 가능한 문서와 home directory의 mutable runtime/memory를
  분리한다.
- 실패 후보의 장기 기억 승격·감쇠·만료를 deterministic evaluator가 판정한다.

## 5. 채택하지 않은 부분

- ontology schema와 evolution 전체
- 전체 EventStore와 Ouroboros 데이터 모델 호환성
- PAL/model routing과 Double Diamond 실행 엔진 전체
- PM → development 이중 인터뷰
- Ouroboros command, MCP tool name, 파일 형식과 수치 threshold 호환성
- Seed evolution/Ralph를 포함한 전체 자율 실행 OS

## 6. 라이선스와 출처 처리

Ouroboros는 MIT 라이선스다. 그 라이선스는 소프트웨어의 복제물 또는 상당 부분을
배포할 때 원 저작권 표시와 허가문 보존을 요구한다. 현재 Geness는 source file이나
장문의 코드·프롬프트·문서를 verbatim으로 복사하지 않았다. 다만 `from-user`,
`from-code`, `from-research`, refine section shape, closure lane 이름과 세 번의 rhythm
threshold처럼 짧은 식별자와 구조는 원본에서 관찰한 design influence로 명시적으로
유지한다.

향후 실제 차용이 생기면 같은 변경에서 다음을 수행한다.

1. 원본 파일과 고정 commit permalink를 이 문서의 재사용 원장에 추가한다.
2. 로컬 적용 파일, copied/adapted 여부와 수정 범위를 기록한다.
3. Q00 저작권 표시와 MIT 전문을 `THIRD_PARTY_NOTICES.md` 또는
   `LICENSES/Ouroboros-MIT.txt`에 보존한다.
4. 배포 artifact에도 필요한 라이선스 파일이 들어가는지 검증한다.
5. 원본 프로젝트의 보증이나 제휴로 오해될 표현을 사용하지 않는다.

이 기록은 법률 자문을 대신하지 않는다. 실제 코드나 표현물의 상당한 차용이
시작되면 배포 전에 다시 검토한다.

### 재사용·영향 원장

| 로컬 파일 | 원본 파일과 permalink | 유형 | 수정 | 라이선스 조치 |
| --- | --- | --- | --- | --- |
| `docs/05_INTERVIEW.md` | [Interview Skill](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/skills/interview/SKILL.md) | 짧은 provenance 식별자, refine/closure 구조와 rhythm rule의 design influence | Geness 계약으로 재구성 | 이 문서와 ADR에 attribution; source/상당 부분 포팅 시 MIT 전문 추가 |
| `docs/PLAN.md`, `docs/adr/0004-ouroboros-interview-principles.md` | [Interview Skill](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/skills/interview/SKILL.md), [Seed Architect](https://github.com/Q00/ouroboros/blob/25f958dd7938d3c383ccfd14d551467bcf6e6bd6/src/ouroboros/agents/seed-architect.md) | workflow와 실행 계약의 design influence | Geness 저장·승인 모델로 재설계 | 고정 링크와 MIT 원본 표시; 실제 표현물 포팅 때 재검토 |
