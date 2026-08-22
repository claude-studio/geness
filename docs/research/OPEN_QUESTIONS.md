# Geness Open Questions

> 상태: Phase 0 decision queue
> 원칙: 이 목록은 구현 편의를 위한 암묵적 기본값이 아니다.

## 사용 방법

각 질문은 조사 → 대안 비교 → 권한 확인 → ADR 또는 규범 문서 반영 순으로 닫는다.
결정이 채택되면 이 파일에서 삭제하지 않고 `Resolved` 표에 근거 링크를 남긴다.

## Blocking questions

| ID | 질문 | 현재 권장 방향 | 결정 권한 | 결과 문서 |
| --- | --- | --- | --- | --- |
| OQ-001 | Controller 언어와 패키지 도구는 무엇인가? | Go + Go modules + CGO + 명시적 `sqlite_fts5` | 사용자 | Accepted ADR-0010 |
| OQ-002 | 공통 library, CLI와 MCP 중 어떤 계층이 canonical command API인가? | library/application service가 규칙, CLI/MCP는 thin transport | 사용자 | Accepted ADR-0011 |
| OQ-003 | v1에 background daemon이 필요한가? | v1 daemon/sidecar 제외, stdio·단발 호출과 explicit lease liveness | 사용자 | Accepted ADR-0012 |
| OQ-004 | exact task state transition과 `FAILED` terminal 의미는 무엇인가? | C-01: explicit user receipt가 있는 `FAILED`만 reopen, `CANCELLED`는 terminal | 사용자 | Accepted ADR-0013 |
| OQ-005 | clone, fork, worktree, folder rename에서 project/workspace ID는 어떻게 변하는가? | C-01: explicit project lineage, clone shared project/distinct workspace, fork explicit detach/rekey | delegated user authority | [ADR-0015](../adr/0015-project-workspace-identity.md) |
| OQ-006 | task Markdown frontmatter와 SQLite schema v1은 무엇인가? | portable Markdown contract/projection과 runtime SQLite mutable-state owner를 분리 | delegated user authority | [ADR-0016](../adr/0016-schema-lineage-and-projection-ownership.md) |
| OQ-007 | contract와 plan digest를 어떤 canonicalization으로 계산하는가? | versioned canonical serializer | 사용자 | Specification ADR |
| OQ-008 | 모든 `PLAN_APPROVED`가 human approval인가? | 위험·scope 변경만 별도 승인하는 policy 검토 | 사용자 | Lifecycle/Specification |
| OQ-009 | completion commit과 writer lease release의 원자적 순서는 무엇인가? | C-01: projection은 비권위로 준비하고 terminal record·completion·lease release를 한 runtime transaction에 기록 | 사용자 / delegated autonomous delivery | [ADR-0014](../adr/0014-completion-lease-atomicity.md) |
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
| RQ-006 | v1 Controller는 Go + Go modules + CGO와 명시적 `sqlite_fts5` build contract를 사용한다. | [ADR-0010](../adr/0010-controller-runtime-go.md), [OQ-001 receipt](./phase-0/evidence/OQ-001/USER-DECISION-RECEIPT-001.md) |
| RQ-007 | 공통 application service가 canonical command API이며 CLI/MCP는 thin transport다. | [ADR-0011](../adr/0011-canonical-command-api.md), [OQ-002 receipt](./phase-0/evidence/OQ-002/USER-DECISION-RECEIPT-001.md) |
| RQ-008 | v1은 required background daemon/host-owned sidecar 없이 explicit lease heartbeat·checkpoint·grace·takeover를 사용한다. | [ADR-0012](../adr/0012-no-background-daemon-v1.md), [OQ-003 receipt](./phase-0/evidence/OQ-003/USER-DECISION-RECEIPT-001.md) |
| RQ-009 | C-01: 명시적 user receipt가 있는 task-level `FAILED`만 `REOPENED`로 복구하고 `CANCELLED`는 terminal로 유지한다. | [ADR-0013](../adr/0013-task-lifecycle-recovery.md), [OQ-004 receipt](./phase-0/evidence/OQ-004/USER-DECISION-RECEIPT-001.md) |
| RQ-010 | C-01: terminal checkpoint·completion record·writer lease release는 한 runtime transaction에 기록하고, current runtime read 뒤에만 `COMPLETED`를 노출한다. | [ADR-0014](../adr/0014-completion-lease-atomicity.md), [OQ-009 delegated receipt](./phase-0/OQ-009-completion-lease-atomicity.md#8-decision) |
| RQ-011 | C-01: project lineage와 workspace-scoped runtime identity를 분리하고, fork/detach와 동명 repository는 explicit detach/rekey 뒤 새 project로 취급한다. | [ADR-0015](../adr/0015-project-workspace-identity.md), [OQ-005 receipt](./phase-0/evidence/OQ-005/USER-DECISION-RECEIPT-001.md) |
| RQ-012 | C-01: portable task Markdown은 contract/projection을 보유하고 runtime SQLite는 mutable state·revision guard·attempt·lease·verdict의 canonical owner가 되며, stale write는 거부하고 projection은 operation ID로 reconcile한다. | [ADR-0016](../adr/0016-schema-lineage-and-projection-ownership.md), [OQ-006 receipt](./phase-0/evidence/OQ-006/USER-DECISION-RECEIPT-001.md) |

OQ-001은 RQ-006 receipt와 Accepted ADR-0010으로, OQ-002는 RQ-007 receipt와 Accepted
ADR-0011으로, OQ-003은 RQ-008 receipt와 Accepted ADR-0012로, OQ-004는 RQ-009 receipt와
Accepted ADR-0013으로, OQ-005는 RQ-011 delegated receipt와 Accepted ADR-0015로, OQ-006은
RQ-012 delegated receipt와 Accepted ADR-0016으로 Resolved로 기록했다. OQ-015는 앞선
packet의 cross-concern synthesis owner이며 RQ-005 receipt로 C-01 boundary를 Resolved로
기록했다. 이 결정들은 OQ-007/OQ-008 및 OQ-010/
OQ-011/OQ-012/OQ-013/OQ-014의 user decision을 대체하지 않는다. 특히 일반
`PLAN_APPROVED` actor와 risk tier는 OQ-008에 남아 있으며, OQ-004의 전체 state graph와
production receipt validation은 ADR-0013의 제한 범위 밖이다. OQ-009의 production
SQLite/WAL/multi-process validation은 ADR-0014의 후속 evidence 범위다.
