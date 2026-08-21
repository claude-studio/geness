---
packet_schema_version: 1
packet_id: "OQ-014"
question_id: "OQ-014"
title: "gee 사용자-facing command surface와 description routing"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T04:10:00Z"
updated_at: "2026-08-21T05:08:00Z"
---

# OQ-014 — gee 사용자-facing command surface와 description routing

## 1. Scope and authority

- **Question:** 사용자-facing command set은 무엇인가?
- **Phase/Gate:** Phase 0 / OQ-014 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** `setup`, `status`, `resume`, public stage alias와 description-based
  routing 후보를 비교하고, 같은 입력을 library/CLI/MCP thin transport로 보내 user-flow
  projection parity를 관찰한다. `auto`, `cross-model`, `claude-only`의 setup route와
  active-task profile 보호도 함께 확인한다.
- **Non-goals:** 제품 CLI, MCP schema, router implementation, plugin/Skill scaffold,
  host slash-command namespace, Controller language/runtime와 최종 명령 이름을 이
  packet에서 채택하지 않는다.
- **Dependencies:** P0-03 / #15가 `CLOSED`·`status:done`이며 typed result/transport
  boundary evidence가 있다. OQ-012의 host capability matrix와 shared fixture를 함께
  사용하지만, OQ-012 또는 OQ-014를 사용자 결정 없이 `Resolved`로 만들지 않는다.
- **Research owner:** Codex

이 packet은 command surface recommendation과 fixture evidence를 보존한다. `gee`는
현재 문서의 proposed/canonical-surface 후보이며 제품 구현 권한이나 user approval을
대체하지 않는다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | 공통 `gee` router + thin CLI/MCP | `gee setup`, `gee status`, `gee resume <task>`와 `brief → contract → plan → impl → verify → done`을 공통 intent/command registry가 소유하고, host aliases와 CLI/MCP는 같은 application service를 호출한다. | description router는 ambiguous input을 사용자 선택으로 멈추고 transport가 domain result를 재해석하지 않는다. | `observed` fixture + local docs |
| C-02 | host-native command surface | Claude slash command와 Codex `$`/TUI command를 각 host의 주 API로 노출하고, host adapter가 state/result를 매핑한다. | host-specific namespace와 lifecycle이 장기 호환성을 유지한다. | `inferred`; not implemented |
| C-03 | transport-specific API | CLI subcommand와 MCP tool names를 각각 canonical command로 정의하고 shared parity를 compatibility test로 사후 보장한다. | 두 transport의 schema/error/retry 차이를 각 adapter가 독립적으로 관리해도 drift를 감당할 수 있다. | `inferred`; not implemented |

## 3. Trade-off matrix

| criterion | C-01 common `gee` | C-02 host-native | C-03 transport-specific | evidence/source refs |
| --- | --- | --- | --- | --- |
| 사용자 학습·이식성 | 하나의 `setup/status/resume`와 public stage description을 두 host에서 재사용한다. | host마다 slash/mention syntax와 namespace를 배워야 한다. | CLI와 MCP client마다 다른 command/tool contract가 된다. | S-001, S-002, S-003, F-001 |
| state authority | Controller/application service가 route와 domain HOLD를 소유한다. | adapter가 state/approval rule을 중복할 위험이 있다. | transport code가 domain semantics를 소유하기 쉬워진다. | S-004, S-005, S-006, F-001 |
| ambiguous description | `ROUTE_CHOICE_REQUIRED` typed HOLD로 자동 종료를 막는다. | host classifier 차이가 선택 결과를 바꿀 수 있다. | description routing이 각 transport에 중복된다. | S-001, S-002, F-001 |
| setup/profile policy | `auto`는 Codex ready면 cross-model, 새 task에서만 Codex absent면 claude-only; explicit cross-model은 attention; active task는 reopen 요구로 동일하다. | host가 profile fallback이나 active-task switch를 조용히 구현할 위험이 있다. | profile policy가 command/transport별로 분산된다. | S-002, S-007, F-001 |
| status/resume semantics | status는 read-only projection, resume은 checkpoint/digest/lease 검증 후 action으로 고정할 수 있다. | host session resume을 durable task state로 오인할 수 있다. | CLI/MCP별 resume/error envelope가 분기된다. | S-001, S-004, F-001 |
| future host compatibility | `/geness:status`와 `$geness status`는 alias일 뿐 canonical `gee status`를 가리킨다. | host command rename이 제품 API breaking change가 된다. | transport migration이 public API migration이 된다. | S-003, S-008, F-001 |

권고 command surface 후보는 다음과 같다. 이름은 아직 사용자 decision receipt 전의
recommendation이다.

| surface | role | route/authority |
| --- | --- | --- |
| `gee setup` | task 이전 project/workspace readiness bootstrap | Controller setup gate; `SETUP_READY` 전 stage 차단 |
| `gee status` | compact current state/next action 조회 | read-only Controller projection; mutation·completion 권한 없음 |
| `gee resume <task>` | checkpoint/blocker에서 재개 | Controller action; digest/Git/lease 확인 후 worker 선택 |
| `gee brief` | interview/closure/restatement | Claude 기본 host |
| `gee contract` | contract candidate/QA/adoption | Codex candidate + Claude/user adoption |
| `gee plan` | preflight/plan gate | Claude 기본 host |
| `gee impl` | approved plan 실행 | Codex 기본 host, claude-only에서는 Claude |
| `gee verify` | 독립 evidence 검증 | Claude 기본 host |
| `gee done` | final completion transaction | Controller 권위 |
| `gee config` | profile/capability 조회·선택 | project/task contract policy; `gee:config`는 host input alias 후보 |

## 4. Sources

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/PLAN.md#182-description-based-gee-router` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | host slash command를 제품 API로 노출하지 않고 공통 `gee` description registry가 intent를 선택하며 audit을 남기도록 현재 계획돼 있다. | Local plan; no external reuse. |
| S-002 | `local-doc` | `docs/04_HOST_INTEGRATION.md#31-public-stage와-host-profile` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | public stage, host profile, auto fallback, setup readiness와 resume boundary를 확인했다. | Local project document; no external reuse. |
| S-003 | `local-doc` | `docs/README.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | `brief → contract → plan → impl → verify → done`, `setup/status/resume`의 문서 소유권과 public alias를 확인했다. | Local project document; no external reuse. |
| S-004 | `local-doc` | `docs/01_ARCHITECTURE.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | Host adapters/CLI/MCP가 application service를 호출하고 domain rule을 중복하지 않아야 한다. | Local project document; no external reuse. |
| S-005 | `local-doc` | `docs/02_TASK_LIFECYCLE.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | `HOLD`는 transport error가 아닌 domain result이며, `resume`은 PAUSED/BLOCKED/REOPENED action이다. | Local project document; no external reuse. |
| S-006 | `local-doc` | `docs/adr/0001-dual-host-shared-core.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | Codex·Claude thin adapter가 하나의 host-neutral Controller를 공유하는 Accepted 방향이다. | Accepted local ADR; no external reuse. |
| S-007 | `local-doc` | `docs/adr/0006-v1-stage-and-host-profile.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | auto/cross-model/claude-only profile과 Codex 부재 새 task fallback, active task silent switch 금지를 확인했다. | Accepted local ADR; no external reuse. |
| S-008 | `local-doc` | `docs/adr/0007-v1-contract-and-verification-artifacts.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | contract profile/revision/digest와 behavior-bearing result의 structured evidence 원칙을 확인했다. | Accepted local ADR; no external reuse. |
| S-009 | `local-research` | `docs/research/phase-0/OQ-002-canonical-command-api.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | 공통 application service와 CLI/MCP thin transport의 typed domain result, transport error와 idempotency 비교 방향을 확인했다. | Local research; no external reuse. |
| S-010 | `official` | `https://developers.openai.com/codex/skills` | rolling vendor docs; no immutable ref | 2026-08-21 | Codex는 Skill description을 통한 implicit routing과 `$`/`/skills` explicit invocation을 제공한다. | Official OpenAI documentation; paraphrase only. |
| S-011 | `official` | `https://code.claude.com/docs/en/slash-commands` | rolling vendor docs; no immutable ref | 2026-08-21 | Claude의 Skill/command는 slash invocation과 description-based model invocation을 제공하지만 plugin namespace가 host-owned다. | Official Anthropic documentation; paraphrase only. |
| S-012 | `official` | `https://developers.openai.com/codex/mcp` | rolling vendor docs; no immutable ref | 2026-08-21 | Codex CLI는 `codex mcp`와 stdio/HTTP MCP를 제공한다. | Official OpenAI documentation; paraphrase only. |
| S-013 | `official` | `https://code.claude.com/docs/en/mcp` | rolling vendor docs; no immutable ref | 2026-08-21 | Claude는 `.mcp.json`, plugin MCP와 `claude mcp`를 제공하며 project-scoped approval은 host가 소유한다. | Official Anthropic documentation; paraphrase only. |
| S-014 | `local-fixture` | `docs/research/phase-0/fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/README.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | setup/status/resume/profile/routing synthetic cases와 library/CLI/MCP parity procedure를 정의한다. | Local research convention; no external reuse. |
| S-015 | `local-observation` | `docs/research/phase-0/evidence/OQ-014/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/RUN-OQ014-001/result.json` | fixture result hash below | 2026-08-21 | 26 cases, 83 assertions, profile policy와 description/alias/status/resume parity가 통과했다. | Generated local evidence; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-HOST-CAPABILITY-COMMAND-SURFACE-001` | `gee` setup/status/resume/description routing과 CLI/MCP parity 비교 | `input/fixture.json`; fixture-local service/transports; host read-only probe available | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | 26 cases와 83 assertions pass; common projection parity; ambiguous route is typed HOLD | fixture source/input tracked; subprocess wire/temp state discarded after each run |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ014-001` | `FX-HOST-CAPABILITY-COMMAND-SURFACE-001` | 2026-08-21T05:07:58Z / 2026-08-21T05:07:59Z | `docs/research/phase-0/fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — setup profile matrix, explicit/alias/description routing, status/resume guard, library/CLI/MCP parity와 transport error separation이 83/83 assertions로 통과 | A-001, A-002, A-003 |

Additional execution and source checks:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile surface_service.py cli_transport.py mcp_transport.py runner.py` | `0` | fixture sources parse successfully. |
| `python3 -m json.tool input/fixture.json >/dev/null` | `0` | synthetic command/profile input is valid JSON. |
| `git diff --check --` | `0` | no whitespace errors in the repository diff after the packet, ADR, index and progress edits. |
| `node /tmp/geness-p0-06-markdown-check.mjs` | `0` | read-only Markdown integrity check: `markdown_files=61`, `local_links=159`, `local_anchor_links=8`, `fence_delimiters=152`, `trailing_whitespace=0`, `errors=[]`. |

Additional execution environment:

- **Tool/runtime versions:** fixture runner `/usr/bin/python3`, Python `3.9.6`; local host probe observed Codex `0.149.0` and Claude `2.1.238`; Darwin `25.4.0` arm64.
- **Environment overrides:** per-run temporary `CODEX_HOME`; `CLAUDE_CODE_SIMPLE=1`; `NO_COLOR=1`; fixture subprocesses use `PYTHONDONTWRITEBYTECODE=1`.
- **Network/external writes:** disabled / none.
- **Redaction:** raw help and transport output is discarded; evidence keeps only normalized projections and hashes.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | synthetic input | `docs/research/phase-0/fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/input/fixture.json` | fixture definition | `sha256:8ffefbcbd76b4e8dcb3830196770e0713bdafcbe739bab5e8805a3f507b4e920` | `tracked` | fixed route/setup/status/resume expectations and host token probes |
| A-002 | redacted result manifest | `docs/research/phase-0/evidence/OQ-014/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/RUN-OQ014-001/result.json` | `RUN-OQ014-001` | `sha256:ef1a6be9c0c302a0907403c4b1cab73185803abe28147cbe631fdabc62e41271` | `packet` | 26 cases, 83 assertions, profile/routing/status/resume parity |
| A-003 | raw runner stdout | `/tmp/<fixture-run>/run.json` | `RUN-OQ014-001` | `sha256:79ea167189cd5216e1528c569d03be9d7849544f76926bd7bd2c6e442beb5064`; discarded after redaction | `discarded` | actual full result before reduction |

No product command, target `.geness/`, real `~/.geness/`, plugin cache, credential or
external MCP service was used.

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | Fixture router is a deterministic synthetic model, not the Geness Controller or final intent classifier. | `high` | Natural-language recall, conflict policy and production schema are untested. | Keep fixture as contract observation only; implement after OQ-014 user decision and Phase 0 CLEAR. | user / Phase 1 | `open` |
| R-002 | Only a small representative description set was exercised. | `medium` | Multilingual, typo, long-form and multi-intent requests are unobserved. | Add approved routing corpus and ambiguity policy in product QA. | Phase 1/7 | `open` |
| R-003 | Host aliases are fixture inputs, not claims that either host currently registers a Geness namespace. | `medium` | Plugin discovery/invocation installed-host E2E is not run. | Keep host aliases non-canonical and validate through plugin E2E later. | Phase 6 | `open` |
| R-004 | `status`/`resume` projections use simplified task state and checkpoint fields. | `high` | Runtime DB, digest, Git, lease and crash reconciliation remain OQ-003/OQ-004/OQ-009 work. | Require Controller-owned typed envelopes and lifecycle fixtures before implementation. | user / Phase 0 | `open` |
| R-005 | CLI/MCP parity was tested with fixture-local transports, not official Codex/Claude clients. | `high` | Installed host transport startup, auth and plugin bridge remain unobserved. | Repeat with selected runtime and installed host adapters in Phase 6. | Phase 6 | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 — make `gee` the single canonical user-facing surface. Keep
  `gee setup` as an idempotent task-precondition bootstrap, `gee status` as a read-only
  compact projection, `gee resume <task>` as a Controller action, and expose the public
  stage aliases `brief`, `contract`, `plan`, `impl`, `verify`, and `done`. Keep description
  routing in the shared registry/application service; host slash/mention forms are
  compatibility aliases only. Valid domain `HOLD` must remain a successful transport result,
  while malformed CLI/unknown MCP methods remain transport errors.
- **Rationale:** The fixture produced identical library/CLI/MCP projections for 26 cases,
  including explicit commands, host aliases, descriptions, ambiguous input, setup profile
  fallback, setup gating, status and resume blockers. This preserves ADR-0001/0006's
  host-neutral Controller and avoids treating host conversation resume as durable task state.
- **Rejected/deferred candidates:** C-02 is deferred because host command namespaces and
  invocation semantics differ and would make public compatibility host-owned. C-03 is
  deferred because it duplicates domain/error/idempotency semantics at transport boundaries;
  its parity should remain a verification property, not an authority model.
- **Unresolved impact:** Final command grammar, output schema, config alias, description
  scoring/ambiguity policy, transport exit codes and installed-host command registration
  remain open. No `gee` executable or production router should be scaffolded from this
  packet alone.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

사용자가 C-01의 canonical `gee` surface와 host alias/description routing 범위를 선택한
뒤, selected host versions에서 local plugin load와 Controller stdio MCP를 포함한
installed-host parity probe를 실행한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] candidate가 셋이며 host-native/transport-specific의 drift 위험을 기록했다.
- [x] candidate와 동일 기준의 trade-off가 source/fixture evidence에 연결됐다.
- [x] source마다 locator, pinned ref 또는 rolling-doc 한계, accessed date와 license/action이 있다.
- [x] 실행한 fixture command에 exact text, 실제 observation과 exit status가 있다.
- [x] 실행하지 않은 production router/installed-host E2E는 limitation으로 분리했다.
- [x] artifact path/URI, hash 또는 raw 폐기 이유와 retention이 있다.
- [x] risk/limitation과 evidence gap, owner와 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] secret/raw log/대용량 output이 packet에 없다.
- [x] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [x] `git diff --check --`와 관련 Markdown 검증 결과를 최종 packet/fixture/ADR/progress 변경 이후 추가했다.
