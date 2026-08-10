# ADR-0005: Develop Geness through docs-first evidence Gates

> 상태: Accepted
> 날짜: 2026-08-10

## 맥락

Geness 자체가 승인된 문서와 evidence를 강조하는데, 제품 개발을 채팅과 PLAN 하나에만
의존하면 새 Codex·Claude 세션이 현재 규범과 실제 상태를 구분하기 어렵다.
`FRONT-JB/mcx`에서 Constitution, Architecture, Lifecycle, Stage Guide, ADR, Progress와
Research의 소유권 분리를 조사했다.

## 결정

Geness 소스 저장소의 `docs/`를 다음처럼 운영한다.

- `00_GENESS.md`: 목적과 불변 원칙
- `01`~`04`: architecture, lifecycle, storage와 host 경계
- `05`~`09`: 단계별 entry/output/exit/evidence 계약
- `PLAN.md`: 구현 순서와 미래 완료 조건
- `adr/`: 채택 결정과 거절한 대안
- `progress/`: 실제 evidence 기준 현재 상태와 HOLD/CLEAR
- `research/`: 출처가 있는 관찰과 미결정

Root `AGENTS.md`는 상세 규칙을 복제하지 않고 읽기 순서와 필수 금지만 연결한다.
`CLAUDE.md`는 같은 규칙을 읽도록 `AGENTS.md` symlink로 둔다.

## 결과

- 새 호스트 세션이 같은 규범과 상태에서 시작한다.
- 계획, 관찰, 결정과 실제 완료 evidence가 섞이지 않는다.
- 여러 문서를 함께 유지해야 하며 link/drift 검증이 필요하다.

## 거절한 대안

- `PLAN.md` 하나만 사용: 규범, 계획과 현재 상태가 섞인다.
- root instruction에 모든 계약 복사: 상세 문서와 drift한다.
- Progress를 자동 진행 일지로 사용: 검증된 현재 사실을 찾기 어려워진다.

## 검증 방법

- 로컬 Markdown link와 문서 index 누락을 자동 검사한다.
- session-start checklist가 Constitution과 Progress를 먼저 읽도록 한다.
- Progress에는 실행하지 않은 테스트나 계획 checkbox가 evidence로 기록되지 않는다.
