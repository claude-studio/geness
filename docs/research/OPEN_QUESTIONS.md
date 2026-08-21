# Geness Open Questions

> 상태: Phase 0 decision queue
> 원칙: 이 목록은 구현 편의를 위한 암묵적 기본값이 아니다.

## 사용 방법

각 질문은 조사 → 대안 비교 → 권한 확인 → ADR 또는 규범 문서 반영 순으로 닫는다.
결정이 채택되면 이 파일에서 삭제하지 않고 `Resolved` 표에 근거 링크를 남긴다.

## Blocking questions

| ID | 질문 | 현재 권장 방향 | 결정 권한 | 결과 문서 |
| --- | --- | --- | --- | --- |
| OQ-001 | Controller 언어와 패키지 도구는 무엇인가? | 배포 크기, FTS5, stdio MCP prototype 비교 | 사용자 | Architecture ADR |
| OQ-002 | 공통 library, CLI와 MCP 중 어떤 계층이 canonical command API인가? | library가 규칙, CLI/MCP는 thin transport | 사용자 | Architecture ADR |
| OQ-003 | v1에 background daemon이 필요한가? | 제외 후 lease heartbeat 요구를 측정 | 사용자 | Runtime ADR |
| OQ-004 | exact task state transition과 `FAILED` terminal 의미는 무엇인가? | typed result와 recovery edge를 fixture로 확정 | 사용자 | Lifecycle |
| OQ-005 | clone, fork, worktree, folder rename에서 project/workspace ID는 어떻게 변하는가? | clone 공유, fork explicit detach/rekey 후보 | 사용자 | Storage ADR |
| OQ-006 | task Markdown frontmatter와 SQLite schema v1은 무엇인가? | concern별 canonical owner를 먼저 고정 | 사용자 | Schema/Storage ADR |
| OQ-007 | contract와 plan digest를 어떤 canonicalization으로 계산하는가? | versioned canonical serializer | 사용자 | Specification ADR |
| OQ-008 | 모든 `PLAN_APPROVED`가 human approval인가? | 위험·scope 변경만 별도 승인하는 policy 검토 | 사용자 | Lifecycle/Specification |
| OQ-009 | completion commit과 writer lease release의 원자적 순서는 무엇인가? | terminal record 후 lease release를 한 transaction 경계로 표현 | 사용자 | Lifecycle/Runtime |
| OQ-010 | lesson fingerprint, 승격, 감쇠와 만료 threshold는 무엇인가? | replay fixture로 false positive/negative 비교 | 사용자 | Learning ADR |
| OQ-011 | runtime/evidence 보존 기간과 용량 제한은 무엇인가? | 상태·위험도 기반 TTL | 사용자 | Storage ADR |
| OQ-012 | Codex·Claude 최소 버전과 macOS/Linux/Windows 지원 범위는 무엇인가? | 공식 host contract prototype 후 확정 | 사용자 | Host ADR |
| OQ-013 | `.geness/config.yaml`과 task별 machine JSON이 필요한가? | Markdown frontmatter로 충분한지 먼저 검증 | 사용자 | Storage/Schema ADR |
| OQ-014 | 사용자-facing command set은 무엇인가? | 주 workflow + status/resume 최소 표면 | 사용자 | Host/CLI ADR |
| OQ-015 | Phase 0 threat model과 권한·scope·external write·secret 정책은 무엇인가? | C-01 Controller 중심 layered fail-closed boundary 채택; exact risk tier와 detector는 후속 결정 | 사용자 | Accepted ADR-0009 + Architecture/Lifecycle/Storage/Host |

## Non-blocking research queue

- verified lesson을 팀에 export하는 최소 포맷
- FTS5 미지원 환경의 정확한 fallback
- SQLite backup, schema migration과 disaster recovery UX
- hook에서 허용할 최대 조회 latency와 context byte budget
- install/update/uninstall 시 공통 `GENESS_HOME` 보존 정책

## Resolved

| ID | 결정 | 근거 |
| --- | --- | --- |
| RQ-001 | 플러그인 이름은 `geness`다. | 사용자 결정, [PLAN](../PLAN.md#4-확정된-결정) |
| RQ-002 | Codex·Claude가 공통 Controller를 사용한다. | [ADR-0001](../adr/0001-dual-host-shared-core.md) |
| RQ-003 | target `.geness/`와 home `~/.geness/`를 분리한다. | [ADR-0002](../adr/0002-project-and-local-state-boundary.md) |
| RQ-004 | failure candidate는 자동으로 장기 memory가 되지 않는다. | [ADR-0003](../adr/0003-failure-candidate-is-not-memory.md) |
| RQ-005 | C-01 fail-closed Controller permission boundary, 민감 action의 current-digest user receipt와 secret redaction fail-closed 원칙을 채택한다. | [ADR-0009](../adr/0009-threat-model-permission-boundaries.md), [OQ-015 receipt](./phase-0/evidence/OQ-015/USER-DECISION-RECEIPT-001.md) |

OQ-015는 앞선 packet의 cross-concern synthesis owner이며 RQ-005 receipt로 C-01 boundary를
Resolved로 기록했다. OQ-003/OQ-004/OQ-008/OQ-009 및 OQ-005/OQ-006/OQ-007/OQ-010/OQ-011/
OQ-012/OQ-013/OQ-014의 user decision을 대체하지 않는다. 특히 일반 `PLAN_APPROVED` actor와
risk tier는 OQ-008에 남아 있다.
