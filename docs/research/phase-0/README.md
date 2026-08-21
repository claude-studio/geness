# Phase 0 Decision Packets and Fixtures

> 상태: Proposed research convention
> 권위: Research 기록 형식. 제품 계약이나 ADR을 대체하지 않는다.

## 목적

Phase 0의 Open Question 조사를 서로 비교할 수 있는 evidence로 남긴다. 모든 packet은
후보를 비교하고, 실제로 실행한 fixture의 결과를 기록하며, 미해결 위험과 사용자 결정
필요 여부를 드러낸다.

이 디렉터리의 문서는 조사 관찰을 보존할 뿐이다. packet을 작성하거나 `decision`에
권고안을 적는 것만으로 Open Question이 `Resolved`가 되지 않는다. 사용자가 결정해야
하는 항목은 권한을 가진 사용자의 결정을 받은 뒤 관련 ADR·규범 문서와
[`OPEN_QUESTIONS.md`](../OPEN_QUESTIONS.md)의 `Resolved` 표에 별도로 반영한다.

## 범위와 비목표

포함하는 것:

- OQ 하나를 조사하는 decision packet의 공통 구조
- candidate와 trade-off 비교
- 고정된 source와 조사일 기록
- exact command, 실행 결과와 exit status
- fixture가 생성한 artifact의 locator·hash·보존 등급
- 위험, 한계, recommendation과 사용자 결정 receipt
- 폐기 가능한 조사 fixture의 격리·재실행·정리·보존 규칙

포함하지 않는 것:

- Geness Controller, plugin manifest, package 또는 제품 scaffold
- 아직 결정되지 않은 언어·schema·runtime·threshold의 암묵적 확정
- 조사 결과만으로 `CLEAR`, `Resolved` 또는 제품 구현 권한을 선언하는 것
- target repository의 `.geness/`나 사용자의 실제 `~/.geness/`에 상태를 생성하는 것

## 파일 규칙

- 실제 packet은 `OQ-<번호>-<짧은-kebab-case>.md`로 만들고, 하나의 blocking OQ만
  소유한다.
- fixture 정의는 `fixtures/<fixture-id>/` 아래에 둔다. fixture ID는
  `FX-<concern>-<short-name>` 형식으로 고정한다.
- 보존하기로 한 작은 redacted evidence는
  `evidence/<packet-id>/<fixture-id>/<run-id>/` 아래에 둔다.
- raw stdout/stderr, secret, credential, 대용량 DB·binary와 임시 실행 디렉터리는
  repository 밖에만 둔다. packet에는 locator와 hash 또는 폐기 사실만 남긴다.
- [`OQ-000-example-packet.md`](./OQ-000-example-packet.md)는 형식 예시일 뿐 실제
  blocking OQ가 아니며 `Resolved` 표에 포함하지 않는다.

## 표준 문서

| 문서 | 역할 |
| --- | --- |
| [`DECISION_PACKET_TEMPLATE.md`](./DECISION_PACKET_TEMPLATE.md) | OQ packet을 복사해 작성하는 필드·섹션 정본 |
| [`FIXTURE_RULES.md`](./FIXTURE_RULES.md) | fixture 정의, 실행 기록, 격리와 보존 규칙 |
| [`OQ-000-example-packet.md`](./OQ-000-example-packet.md) | 모든 필드와 실행 evidence를 채운 비규범 예시 |
| [`fixtures/FX-PACKET-SELF-CHECK-001/README.md`](./fixtures/FX-PACKET-SELF-CHECK-001/README.md) | 표준 문서 자체를 검사하는 최소 disposable fixture |

## Issue #16 research index

The following are observed Phase 0 research packets for lifecycle, lease and completion.
They are not Resolved decisions and contain no user decision receipts:

| OQ | packet | fixture | RUN evidence | status |
| --- | --- | --- | --- | --- |
| OQ-003 | [OQ-003-daemon-lease-liveness.md](./OQ-003-daemon-lease-liveness.md) | [FX-LIFECYCLE-LEASE-COMPLETION-001/README.md](./fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/README.md) | [RUN-OQ003-001/RUN.md](./evidence/OQ-003/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ003-001/RUN.md) | blocked / user decision pending |
| OQ-004 | [OQ-004-task-lifecycle.md](./OQ-004-task-lifecycle.md) | [FX-LIFECYCLE-LEASE-COMPLETION-001/README.md](./fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/README.md) | [RUN-OQ004-001/RUN.md](./evidence/OQ-004/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ004-001/RUN.md) | blocked / user decision pending |
| OQ-008 | [OQ-008-plan-approval-policy.md](./OQ-008-plan-approval-policy.md) | [FX-LIFECYCLE-LEASE-COMPLETION-001/README.md](./fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/README.md) | [RUN-OQ008-001/RUN.md](./evidence/OQ-008/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ008-001/RUN.md) | blocked / user decision pending |
| OQ-009 | [OQ-009-completion-lease-atomicity.md](./OQ-009-completion-lease-atomicity.md) | [FX-LIFECYCLE-LEASE-COMPLETION-001/README.md](./fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/README.md) | [RUN-OQ009-001/RUN.md](./evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-001/RUN.md) | blocked / user decision pending |

The shared fixture is an evidence-only Python runner. It does not select product language,
package manager, runtime, schema, daemon, lease policy, approval actor, or completion
transaction. Its observed two-run result is 7 assertions per run with equality-equivalent
JSON output. Heartbeat/grace/takeover, complete lifecycle and CANCELLED semantics, Plan Gate
actor policy, crash-point matrix and production atomicity remain unobserved.

## Issue #17 research index

The following are observed Phase 0 research packets for identity, schema, digest and config.
They are decision-ready recommendations, not Resolved decisions, and contain no user decision
receipts:

| OQ | packet | shared fixture | RUN evidence | status |
| --- | --- | --- | --- | --- |
| OQ-005 | [OQ-005-project-workspace-identity.md](./OQ-005-project-workspace-identity.md) | [FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md](./fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md) | [RUN-OQ005-001/RUN.md](./evidence/OQ-005/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ005-001/RUN.md) | decision-ready / user decision pending |
| OQ-006 | [OQ-006-schema-lineage.md](./OQ-006-schema-lineage.md) | [FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md](./fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md) | [RUN-OQ006-001/RUN.md](./evidence/OQ-006/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ006-001/RUN.md) | decision-ready / user decision pending |
| OQ-007 | [OQ-007-digest-canonicalization.md](./OQ-007-digest-canonicalization.md) | [FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md](./fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md) | [RUN-OQ007-001/RUN.md](./evidence/OQ-007/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-001/RUN.md) | decision-ready / user decision pending |
| OQ-013 | [OQ-013-config-machine-contract.md](./OQ-013-config-machine-contract.md) | [FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md](./fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md) | [RUN-OQ013-001/RUN.md](./evidence/OQ-013/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ013-001/RUN.md) | decision-ready / user decision pending |

The shared fixture executed local Git clone/rename/worktree probes, a synthetic explicit fork
relation, frontmatter/SQLite round-trip, stale revision rejection, contract/plan golden digest
vectors and a portable/local config boundary assertion. It reported 30/30 assertions and
equality-equivalent JSON on two runs. The fixture does not choose project ID generation,
production SQLite schema, a cross-language serializer, `.geness/config.yaml`, task machine JSON
or any product implementation.

## Issue #18 research index

The following are decision-ready host and command-surface packets. They are not Resolved
decisions and contain no user decision receipts:

| OQ | packet | shared fixture | RUN evidence | status |
| --- | --- | --- | --- | --- |
| OQ-012 | [OQ-012-host-os-compatibility.md](./OQ-012-host-os-compatibility.md) | [FX-HOST-CAPABILITY-COMMAND-SURFACE-001/README.md](./fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/README.md) | [RUN-OQ012-001/result.json](./evidence/OQ-012/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/RUN-OQ012-001/result.json) | decision-ready / user decision pending |
| OQ-014 | [OQ-014-command-surface.md](./OQ-014-command-surface.md) | [FX-HOST-CAPABILITY-COMMAND-SURFACE-001/README.md](./fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/README.md) | [RUN-OQ014-001/result.json](./evidence/OQ-014/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/RUN-OQ014-001/result.json) | decision-ready / user decision pending |

The shared fixture observed Codex `0.149.0` and Claude Code `2.1.238` on Darwin arm64 using
read-only version/help/feature probes. Its synthetic surface comparison passed 26 cases and
83 assertions across library, CLI and MCP-like stdio paths. It does not install plugins,
start an agent or MCP server, select a production command schema, or establish a release
minimum for older host versions.

## Packet 작성 순서

1. 해당 OQ의 질문, 결정 권한, allowed scope와 non-goal을 먼저 적는다.
2. 조사할 candidate를 모두 열거하고 동일한 기준으로 trade-off를 비교한다.
3. source마다 고정 ref, 조사일, 관찰과 라이선스 조치를 기록한다.
4. fixture를 격리 실행하고 exact command, 실제 observation, exit status를 기록한다.
5. 산출 artifact를 redaction·hash한 뒤 packet과 보존 위치를 연결한다.
6. 위험·한계와 evidence gap을 남기고 recommendation을 적는다.
7. 사용자 결정이 없으면 `needs-user-decision` 또는 `blocked`로 남긴다. 결정이
   반영된 뒤에만 ADR과 Open Questions를 갱신한다.

## 완료 판정

이 표준의 완료는 다음을 모두 확인한 경우다.

- candidate, trade-off, source, command, exit status, artifact, risk/limitation과
  decision 섹션이 존재한다.
- 실행했다고 적은 모든 command에 실제 exit status가 있다. 실행하지 않은 command는
  `not-run`과 이유를 적으며 evidence로 세지 않는다.
- fixture 입력·runner와 generated evidence의 보존 등급이 구분된다.
- packet과 fixture가 제품 scaffold와 분리되어 있고 current target/home state를
  건드리지 않는다.
- `git diff --check`와 repository의 해당 Markdown 검사를 실제로 실행해 결과를
  기록한다.

이 조건은 packet 형식의 evidence Gate이며 Phase 0 전체 `CLEAR`가 아니다.
