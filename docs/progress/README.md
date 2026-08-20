# Geness Progress

> 마지막 검증: 2026-08-20
> Documentation foundation: CLEAR
> Implementation: HOLD

## 1. 이 문서가 소유하는 것

이 문서는 PLAN의 희망 상태가 아니라 현재 repository에서 artifact와 command로 확인한
사실만 기록한다. 개별 target task의 Gate가 아니라 **Geness 제품 자체 구현**의
HOLD/CLEAR를 소유한다.

## 2. 현재 판정

### Documentation foundation — CLEAR

Constitution, architecture/lifecycle/storage/host 문서, stage guides, PLAN, ADR, Research,
Progress와 root agent instruction이 존재한다. 로컬 link·anchor, Markdown integrity와
`CLAUDE.md → AGENTS.md` symlink 검사를 통과했다. 자세한 evidence는
[Documentation Foundation](./0000_DOCUMENTATION_FOUNDATION.md)에 있다.

이번 검증에서는 public stage alias, Geness v1 contract schema, `verification.md` final
projection, target setup과 Claude–Codex Controller bridge까지 canonical 문서에 정렬했다.

### Implementation — HOLD

Controller나 plugin scaffold 구현을 시작할 수 없다. 다음 이유가 확인됐다.

- repository에는 아직 구현 source, package manifest와 test harness가 없다.
- [Open Questions](../research/OPEN_QUESTIONS.md)의 Phase 0 blocking decision이 열려 있다.
- Controller 언어, canonical API 경계와 schema v1이 확정되지 않았다.
- 두 host의 최소 prototype과 threat model evidence가 없다.

HOLD 중 허용되는 작업은 문서 정렬, 공식 계약 조사, 읽기 전용 prototype/spike 설계와
사용자가 명시적으로 지시한 foundation 작업이다. 구현 언어를 임의로 선택해 scaffold를
생성하거나 `CLEAR`로 간주하지 않는다.

## 3. 검증된 repository 사실

- Git repository root는 이 프로젝트 디렉터리다.
- 기존 제품 구현은 없고 root `README.md`만 있던 상태에서 문서 foundation을 시작했다.
- Geness의 제품 이름, dual-host 방향, target `.geness/`와 home `~/.geness/` 경계는
  사용자 결정과 Accepted ADR로 기록됐다.
- Root `AGENTS.md`가 docs-first 세션 절차와 Implementation HOLD를 연결하고,
  `CLAUDE.md`는 그 파일의 symlink다.
- 실제 target repository initializer, Controller, SQLite schema, Skill, manifest와 tests는
  아직 존재하지 않는다.
- 실행할 제품 test command는 아직 정의되지 않았다.

## 4. 문서 상태

| 영역 | 상태 | 근거 |
| --- | --- | --- |
| Constitution | Accepted baseline | [00_GENESS](../00_GENESS.md) |
| Architecture | Proposed | [01_ARCHITECTURE](../01_ARCHITECTURE.md) |
| Lifecycle | Proposed, Phase 0 decisions open | [02_TASK_LIFECYCLE](../02_TASK_LIFECYCLE.md) |
| Storage boundary | Accepted, schema TBD | [ADR-0002](../adr/0002-project-and-local-state-boundary.md) |
| Dual-host boundary | Accepted, manifest prototype TBD | [ADR-0001](../adr/0001-dual-host-shared-core.md) |
| Interview principles | Accepted, implementation TBD | [ADR-0004](../adr/0004-ouroboros-interview-principles.md) |
| Failure learning | Accepted principle, thresholds TBD | [ADR-0003](../adr/0003-failure-candidate-is-not-memory.md) |
| Implementation plan | Draft | [PLAN](../PLAN.md) |

## 5. Phase roadmap

| Phase | 상태 | 다음 Gate |
| --- | --- | --- |
| Documentation Foundation | CLEAR | 완료 evidence 보존 및 drift 검사 |
| Phase 0: 계약과 ADR | HOLD | blocking decisions와 prototype evidence |
| Phase 1: plugin/project init | NOT STARTED | Phase 0 CLEAR |
| Phase 2: interview/spec | NOT STARTED | Phase 1 exit criteria |
| Phase 3: preflight/plan | NOT STARTED | Phase 2 exit criteria |
| Phase 4: run/verify/resume | NOT STARTED | Phase 3 exit criteria |
| Phase 5: failure learning | NOT STARTED | Phase 4 event evidence |
| Phase 6: host adapters/hooks | NOT STARTED | shared-core contract evidence |
| Phase 7: quality/release | NOT STARTED | 앞선 Phase integration evidence |

## 6. 다음 하나의 검증 가능한 목표

[OQ-001](../research/OPEN_QUESTIONS.md)의 Controller 언어·패키징 후보를 배포 크기,
SQLite FTS5, stdio MCP와 dual-host 설치 기준으로 비교하는 Phase 0 decision packet을
만든다. 이 목표는 구현 scaffold를 생성하지 않는다.

## 7. 갱신 규칙

- 실제로 실행한 command, exit status와 확인한 artifact만 evidence로 쓴다.
- 계획한 테스트를 통과한 테스트처럼 적지 않는다.
- HOLD 해제 조건을 만족한 evidence가 없으면 `CLEAR`로 바꾸지 않는다.
- 문서 작업과 구현 Phase를 같은 CLEAR로 합치지 않는다.
- 새 검증 결과가 이전 기록과 다르면 현재 판정을 갱신하고 milestone 기록은 보존한다.
- 작업 종료 때 다음 하나의 검증 가능한 목표를 남긴다.
