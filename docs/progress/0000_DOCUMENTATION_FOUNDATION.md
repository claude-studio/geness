# Progress 0000 — Documentation Foundation

> 상태: COMPLETED
> 시작일: 2026-08-10
> 완료일: 2026-08-10

## Goal

새 Codex 또는 Claude 세션이 채팅 기록 없이 Geness의 목적, 현재 HOLD, 설계 경계,
단계 계약, 출처와 구현 계획을 찾을 수 있는 문서 기반을 만든다.

## Non-goal

- Controller, Skill, CLI, MCP와 host manifest 구현
- 언어, schema와 evaluator threshold의 임의 확정
- target repository의 `.geness/` artifact 생성
- 제품 테스트 통과 주장

## 산출물

- `docs/README.md`와 `00_GENESS.md`
- Architecture, Lifecycle, Storage, Host Integration
- Interview, Specification, Execution, Verification, Learning Stage Guide
- `docs/PLAN.md`
- 초기 Accepted ADR
- Ouroboros·MCX research, reference policy와 open questions
- Progress index와 이 milestone record
- root `AGENTS.md`와 `CLAUDE.md` symlink
- root `README.md`의 프로젝트 및 문서 진입점

## 완료 조건

- [x] 위 산출물이 실제로 존재한다.
- [x] `CLAUDE.md`는 파일 복사본이 아니라 `AGENTS.md`를 가리키는 symlink다.
- [x] repository-local Markdown 링크가 모두 해석된다.
- [x] `git diff --check`가 통과한다.
- [x] PLAN과 문서 index가 실제 docs 구조를 반영한다.
- [x] Ouroboros의 원본, 고정 commit, 채택·변형·비채택 및 라이선스 경계가 기록됐다.
- [x] MCX에서 채택·변형한 docs-first 요소가 기록됐다.
- [x] 구현이 시작되지 않았다는 사실과 Phase 0 HOLD가 보존됐다.

## Evidence

2026-08-10에 repository root에서 다음을 확인했다.

- `git diff --check` → exit `0`
- `test -L CLAUDE.md`, `readlink` target 비교, `cmp -s AGENTS.md CLAUDE.md` → 모두 exit `0`;
  target은 `AGENTS.md`
- read-only Markdown integrity 검사 → `markdown_files=27 local_links=93 errors=0`
- local Markdown anchor 검사 → `local_anchor_links=4 errors=0`
- integrity 검사는 trailing whitespace, fenced code block 짝, 숨은 Unicode format character와
  local target 존재를 함께 확인했다.
- 독립 subagent 재감사 → P0 문제 없음; 지적된 Progress stale 상태, FAILED 표현과
  Ouroboros 영향 원장 표현을 수정한 뒤 위 검사를 재실행했다.

2026-08-20에 v1 workflow 문서 정렬 후 다음을 추가 확인했다.

- `git diff --check origin/main...HEAD` → exit `0`
- read-only Node Markdown integrity 검사 → tracked Markdown 30개, local link/anchor
  해석 성공, fenced code block 짝 검사 성공
- `test -L CLAUDE.md`, `readlink`, `cmp` → 모두 exit `0`; target은 `AGENTS.md`
- conflict marker 검사 → 발견 없음
- 제품 manifest/package/test harness → 아직 없음; Implementation HOLD 유지

## 남은 blocker

Documentation Foundation 자체 blocker는 없다. 제품 구현은 별도 Gate이며,
[Progress](./README.md)의 Implementation HOLD와
[Open Questions](../research/OPEN_QUESTIONS.md)를 따른다.
