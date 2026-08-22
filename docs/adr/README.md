# Geness Architecture Decision Records

ADR은 되돌리기 어렵거나 여러 계층의 계약을 바꾸는 결정을 기록한다. Research가
관찰을 소유하고 PLAN이 구현 순서를 소유한다면, ADR은 무엇을 왜 채택했는지를
소유한다.

## 상태

- `Proposed`: 검토 중이며 구현 권한이 아니다.
- `Accepted`: 현재 규범이다.
- `Superseded`: 새 ADR이 대체했다. 기존 기록은 삭제하지 않는다.
- `Rejected`: 검토했지만 채택하지 않았다.

## 목록

| ADR | 상태 | 결정 |
| --- | --- | --- |
| [0001](./0001-dual-host-shared-core.md) | Accepted | Codex·Claude가 하나의 host-neutral Controller를 공유한다. |
| [0002](./0002-project-and-local-state-boundary.md) | Accepted | target project 문서와 home runtime/memory를 분리한다. |
| [0003](./0003-failure-candidate-is-not-memory.md) | Accepted | 실패 후보는 검증 없이 장기 memory가 되지 않는다. |
| [0004](./0004-ouroboros-interview-principles.md) | Accepted | Ouroboros에서 관찰한 인터뷰 원칙을 독립적인 Geness 계약으로 재정의한다. |
| [0005](./0005-docs-driven-development.md) | Accepted | Geness 자체 개발을 docs-first Gate로 운영한다. |
| [0006](./0006-v1-stage-and-host-profile.md) | Accepted | V1 public stage alias, host profile, user-owned worktree와 one-writer 범위를 정의한다. |
| [0007](./0007-v1-contract-and-verification-artifacts.md) | Accepted | V1 contract schema, artifact projection, acting verification과 bounded successor를 정의한다. |
| [0008](./0008-host-command-surface.md) | Proposed | Host compatibility matrix와 canonical `gee` command surface 후보를 정의한다. |
| [0009](./0009-threat-model-permission-boundaries.md) | Accepted | Threat model과 Controller 중심 fail-closed permission boundary를 정의한다. |
| [0010](./0010-controller-runtime-go.md) | Accepted | v1 Controller는 Go + Go modules + CGO + 명시적 `sqlite_fts5`를 사용한다. |

## ADR이 필요한 변경

- lifecycle state, Gate와 completion 의미
- canonical state owner, storage boundary와 identity
- Core와 adapter 의존 방향
- 승인 digest 또는 evidence 계약
- memory 승격·만료 알고리즘
- 공개 CLI/MCP/schema의 호환성을 깨는 변경
- 보안·권한·scope를 완화하는 변경
- 외부 설계와의 독립성 또는 실제 저작물 재사용 경계 변경

표현 정리나 이미 Accepted된 계약 안의 국소 구현 선택에는 ADR을 강제하지 않는다.

## 작성 형식

새 ADR에는 최소한 `상태`, `날짜`, `맥락`, `결정`, `결과`, `거절한 대안`,
`검증 방법`을 둔다. 기존 Accepted ADR의 의미를 바꿀 때는 새 ADR에서
`Supersedes`를 선언한다.
