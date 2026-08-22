---
packet_schema_version: 1
packet_id: "OQ-002"
question_id: "OQ-002"
title: "Canonical command API와 CLI/MCP 경계 비교"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-20T12:36:59Z"
updated_at: "2026-08-20T12:58:39Z"
---

# OQ-002 — Canonical command API와 CLI/MCP 경계 비교

## 1. Scope and authority

- **Question:** 공통 library/application service, CLI와 MCP 중 어떤 계층이 canonical
  command API인가?
- **Phase/Gate:** Phase 0 / OQ-002 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** 동일한 합성 fixture를 fixture-local common
  application service, CLI thin transport와 MCP-like stdio thin transport로 실행하고,
  typed domain result, transport error와 idempotent replay를 비교한다.
- **Non-goals:** 제품 언어, package manager, runtime, production schema, daemon,
  plugin/manifest, 설치된 host E2E, production scaffold와 최종 API 이름을 선택하거나
  생성하지 않는다. OQ-001 사용자 결정을 대신하지 않는다.
- **Dependencies:** #14 / OQ-001 packet merged evidence. #14는 PR #64가
  `MERGED`이고 issue가 `CLOSED`이며 `origin/main`에 `Closes #14` commit이 반영됐다.
  OQ-001은 [ADR-0010](../../adr/0010-controller-runtime-go.md)과 user receipt로
  `Resolved`됐으며, 이 fixture의 Python stdlib는 runner 선택일 뿐 제품 runtime 선택이
  아니다.
- **Research owner:** Codex

이 packet은 관찰과 권고를 보존한다. `OQ-002`를 `Resolved`로 옮기거나 ADR을 만들지
않으며, 제품 Implementation `HOLD`를 유지한다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | Shared application service | domain policy와 typed result/idempotency를 공통 library/application service가 소유하고 CLI/MCP는 wire adapter가 된다. | transport가 service를 재사용하고 transport-specific error를 별도 envelope로 유지한다. | `observed` — FX-COMMAND-API-TYPED-RESULT-001 |
| C-02 | CLI canonical surface | CLI command/result가 canonical surface가 되고 MCP가 CLI 또는 CLI-owned mapping을 호출한다. | MCP가 CLI process/shape와 lifecycle에 결합돼도 허용한다. | `inferred` — 별도 구현·실행하지 않음 |
| C-03 | MCP canonical surface | MCP tool/schema가 canonical surface가 되고 CLI가 MCP client/adapter가 된다. | CLI가 JSON-RPC lifecycle과 MCP error semantics에 결합돼도 허용한다. | `inferred` — 별도 구현·실행하지 않음 |

## 3. Trade-off matrix

`observed`는 fixture가 직접 확인한 사실이고, `inferred`는 canonical 문서와 fixture
경계에서 도출한 설계 영향이다. 이 표는 사용자 결정을 자동으로 채택하지 않는다.

| criterion | C-01 Shared service | C-02 CLI canonical | C-03 MCP canonical | evidence/source refs |
| --- | --- | --- | --- | --- |
| domain rule ownership | 한 service에 `HOLD`, `APPLIED`, `REPLAYED`와 side-effect count가 모인다. `observed` | CLI adapter 또는 CLI process가 policy owner가 되기 쉬워 MCP parity가 간접화된다. `inferred` | MCP tool handler가 policy owner가 되기 쉬워 CLI가 JSON-RPC semantics에 결합된다. `inferred` | S-001, S-002, S-005, F-001 |
| same-input typed-result parity | library/CLI/MCP의 HOLD와 replay semantic projection이 모두 일치했다. `observed` | MCP가 CLI 결과를 재해석하는 추가 parity boundary가 필요하다. `inferred` | CLI가 MCP result/content/error를 재해석하는 추가 parity boundary가 필요하다. `inferred` | F-001, A-001 |
| transport error vs domain HOLD | CLI malformed JSON는 exit `2` transport error, valid HOLD는 exit `0`; MCP unknown method는 JSON-RPC `-32601` transport error, valid HOLD는 structured result. `observed` | CLI error semantics가 다른 transport의 canonical error contract가 된다. `inferred` | JSON-RPC error semantics가 CLI와 library에 누출될 수 있다. `inferred` | S-003, S-004, F-001, A-001 |
| idempotent replay | 동일 idempotency key replay가 stable effect ID와 side effect count `1`을 유지했다. `observed` | CLI invocation/process boundary에 저장·replay policy를 별도 연결해야 한다. `inferred` | MCP session/request lifecycle에 저장·replay policy를 별도 연결해야 한다. `inferred` | S-001, S-003, F-001, A-001 |
| host neutrality | thin adapter가 shared service를 import하고 domain code를 중복하지 않는 정적 assertion이 통과했다. `observed` | MCP가 CLI contract에 종속될 수 있다. `inferred` | CLI가 MCP SDK/protocol에 종속될 수 있다. `inferred` | S-001, S-002, S-005, A-001 |
| implementation impact | product language/runtime를 선택하지 않고도 boundary를 먼저 시험할 수 있다. `observed` | CLI-specific process/schema/installation을 먼저 canonicalize해야 한다. `inferred` | MCP SDK/version/schema/stdio lifecycle을 먼저 canonicalize해야 한다. `inferred` | S-001, S-006, F-001 |

## 4. Sources

모든 source는 repository-local canonical 문서이며 외부 코드·문구를 복사하지 않았다.
`pinned ref`는 조사 당시의 base commit `744ca6a826037bcdf0385175a2699a40f325bdde`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/01_ARCHITECTURE.md` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | Host adapters/CLI/MCP → application services → domain 방향과 CLI/MCP 공통 application service 원칙을 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | `docs/04_HOST_INTEGRATION.md` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | CLI와 MCP는 같은 dispatch/application service를 호출하고 transport error와 domain HOLD를 구분해야 한다. | Local project document; no external reuse. |
| S-003 | `local-doc` | `docs/02_TASK_LIFECYCLE.md` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | `HOLD`는 transport error가 아닌 정상 domain result이며 Gate는 typed fields를 가져야 한다. | Local project document; no external reuse. |
| S-004 | `local-doc` | `docs/08_VERIFICATION.md` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | command error와 criterion failure를 구분하고 실제 acting observation을 추정하지 말아야 한다. | Local project document; no external reuse. |
| S-005 | `local-doc` | `docs/adr/0001-dual-host-shared-core.md` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | 하나의 host-neutral Controller와 thin CLI/MCP interface를 Accepted 방향으로 확인했다. | Accepted local ADR; no external reuse. |
| S-006 | `local-doc` | `docs/adr/0007-v1-contract-and-verification-artifacts.md` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | behavior-bearing 결과는 structured evidence가 필요하고 schema/digest는 Phase 0에서 확정 전임을 확인했다. | Accepted local ADR; no external reuse. |
| S-007 | `local-doc` | `docs/research/phase-0/FIXTURE_RULES.md` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | fixture 격리, exact command/exit status, redacted artifact/hash와 `not-run` 규칙을 확인했다. | Local research convention; no external reuse. |
| S-008 | `local-doc` | `docs/PLAN.md#17-공통-controller와-mcpcli-경계` | `744ca6a826037bcdf0385175a2699a40f325bdde` | 2026-08-20 | Phase 0 OQ-002 artifact와 shared API/thin transport의 현재 권장 방향을 확인했다. | Local plan; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-COMMAND-API-TYPED-RESULT-001` | common service/library, CLI와 MCP-like stdio의 domain result/error/replay parity 비교 | `input/fixture.json`의 합성 HOLD·decision replay·invalid wire 입력 | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | 14 assertions pass; HOLD parity, transport error 분리와 one-side-effect replay | fixture directory의 runner와 input은 tracked; state/raw output은 per-run temp에서 폐기 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ002-001` | `FX-COMMAND-API-TYPED-RESULT-001` | 2026-08-20T12:49:20Z / 2026-08-20T12:49:27Z | `docs/research/phase-0/fixtures/FX-COMMAND-API-TYPED-RESULT-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — library/CLI/MCP domain projection parity, typed HOLD, CLI/MCP transport error, replay effect stability와 14 assertions 통과 | A-001, A-002, A-003 |
| `RUN-OQ002-002` | `FX-COMMAND-API-TYPED-RESULT-001` | 2026-08-20T12:55:35Z / 2026-08-20T12:55:43Z | `docs/research/phase-0/fixtures/FX-COMMAND-API-TYPED-RESULT-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 동일 fixture revision/input의 재실행이 같은 14 assertions와 raw manifest hash를 산출 | A-004 |
| `RUN-OQ002-003` | `FX-COMMAND-API-TYPED-RESULT-001` | 2026-08-20T12:58:14Z / 2026-08-20T12:58:28Z | `docs/research/phase-0/fixtures/FX-COMMAND-API-TYPED-RESULT-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — EOF-only fixture revision 이후에도 같은 14 assertions와 raw manifest hash를 산출 | A-005 |

Additional commands executed for the fixture and evidence validation:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile common_service.py cli_transport.py mcp_transport.py runner.py` | `0` | four fixture sources parse successfully under fixture-local `python3` (`/usr/bin/python3`, 3.9.6) |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-002/FX-COMMAND-API-TYPED-RESULT-001/RUN-OQ002-001/result.json >/dev/null` | `0` | redacted evidence is valid JSON |
| `cmp -s /tmp/geness-oq002-RUN-OQ002-001.json /tmp/geness-oq002-RUN-OQ002-002.json` | `0` | two fixture runs produced byte-identical raw manifests |
| `cmp -s /tmp/geness-oq002-RUN-OQ002-001.json /tmp/geness-oq002-RUN-OQ002-003.json` | `0` | current staged fixture source produced the same raw manifest after the EOF-only revision |
| `git diff --check --` | `0` | no whitespace error after packet/fixture edits |
| `python3 /tmp/geness-oq002-markdown-check.py` | `0` | read-only Markdown local-link/document integrity check; `markdown_files=39`, `local_links=119`, `local_anchor_links=8`, `errors=[]` |

Tool/runtime versions and environment:

- fixture cwd `python3`: `/usr/bin/python3`, Python `3.9.6` (system interpreter)
- repository-root `python3`: `/opt/homebrew/opt/python@3.14/bin/python3.14`, Python `3.14.6`
- Node: `v22.23.0`; Git: `2.49.0`
- input SHA-256: `29060dc89322dfe5227631b42f3852eb7ec06233b4b0fa5be9cdd0046b379cf2`
- environment override: `PYTHONDONTWRITEBYTECODE=1`; no `GENESS_HOME` override needed
- network/external writes: disabled / none
- redaction: raw runner JSON retained only temporarily; packet evidence keeps a small
  result summary without temp state or raw subprocess output

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | redacted result manifest | `docs/research/phase-0/evidence/OQ-002/FX-COMMAND-API-TYPED-RESULT-001/RUN-OQ002-001/result.json` | `RUN-OQ002-001` | `sha256:502cf76ff555770e45dce6a3945a8f1eb30403de04ef2b94b6cefe0aa3f175aa` | `packet` | same domain result, HOLD/error separation, idempotent replay, thin boundary |
| A-002 | raw runner stdout | `/tmp/geness-oq002-RUN-OQ002-001.json` | `RUN-OQ002-001` | `sha256:ce18e6d622fc639da5964ebbf5a4ca375e8fb8ba1c5ac7446ac2b2e939a7f3e0` | `discarded` | actual full runner observation before redaction; discarded after A-001 creation |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-COMMAND-API-TYPED-RESULT-001/input/fixture.json` | fixture definition | `sha256:29060dc89322dfe5227631b42f3852eb7ec06233b4b0fa5be9cdd0046b379cf2` | `tracked` | stable same-input comparison and replay key |
| A-004 | raw runner stdout, rerun | `/tmp/geness-oq002-RUN-OQ002-002.json` | `RUN-OQ002-002` | `sha256:ce18e6d622fc639da5964ebbf5a4ca375e8fb8ba1c5ac7446ac2b2e939a7f3e0` | `discarded` | byte-identical rerun confirms fixture repeatability |
| A-005 | raw runner stdout, current source rerun | `/tmp/geness-oq002-RUN-OQ002-003.json` | `RUN-OQ002-003` | `sha256:ce18e6d622fc639da5964ebbf5a4ca375e8fb8ba1c5ac7446ac2b2e939a7f3e0` | `discarded` | current staged fixture source still produces the same result |

The fixture state files, intermediate JSON-RPC lines and subprocess stdout/stderr are not
preserved in Git. The packet retains only the redacted result and hash of the discarded raw
runner output. No secret, credential, environment dump, target `.geness/` state or real
`~/.geness/` state was used.

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | MCP path is a fixture-local JSON-RPC/stdin proxy, not an official SDK or installed Claude/Codex MCP server. | `medium` | SDK/version/startup and installed-host behavior remain unobserved. | Keep OQ-001 and Phase 6 host E2E open; repeat with the user-selected runtime/official transport after product decisions. | user / Phase 6 | `open` |
| R-002 | Replay uses one fixture process family and a temp JSON state file; no concurrent writer, crash point or lease race is tested. | `high` | cross-process arbitration and crash recovery remain unobserved. | Route to OQ-003/OQ-006/OQ-009; do not infer production transaction or daemon semantics from this run. | user | `open` |
| R-003 | C-02 and C-03 are trade-off inferences, not independently implemented candidate fixtures. | `medium` | comparative performance/operational costs are not measured. | User decision remains pending; a follow-up candidate spike may be authorized without changing this packet's observation. | user | `open` |
| R-004 | Fixture-local result fields are an evidence vector, not a production schema or compatibility promise. | `high` | canonical serialization, schema versioning and digest policy remain OQ-006/OQ-007. | Preserve `fixture.command_result.v1` as local evidence only; require a later ADR before product adoption. | user | `open` |
| R-005 | Only synthetic commands and one machine/interpreter were exercised. | `low` | real task state, large payload, timeout and cross-platform behavior remain unobserved. | Repeat in a later approved contract harness and host matrix. | user / Phase 6 | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 — shared library/application service owns domain policy and
  typed result; CLI and MCP remain thin transports that preserve the domain envelope and
  add only transport-specific errors.
- **Rationale:** The same synthetic input produced identical domain HOLD/APPLIED/REPLAYED
  projections through all three paths. A valid domain HOLD returned as a successful
  transport exchange, while malformed CLI JSON and unknown MCP methods stayed typed
  transport errors. Replaying the same key preserved effect ID and side-effect count `1`.
  The fixture also observed that both transports import the common service and do not
  duplicate domain result codes. This aligns with S-001/S-002/S-005 and A-001.
- **Rejected/deferred candidates:** C-02 and C-03 remain deferred; they were not selected
  or rejected as product policy because their production cost and official host behavior
  were not measured.
- **Unresolved impact:** Until the user chooses, no OQ-002 command API ADR, production
  schema, daemon policy or scaffold may be created. The product runtime is already fixed by
  ADR-0010; Implementation remains `HOLD`.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

User reviews C-01/C-02/C-03 and decides whether the shared library/application-service
boundary should become an Architecture ADR candidate. The Go runtime is already fixed by
OQ-001/ADR-0010; schema and transport details remain separate Phase 0 decisions.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] candidate가 셋이며 C-02/C-03을 실제 실행하지 않은 이유와 inference 상태가 기록됐다.
- [x] candidate와 동일 기준의 trade-off가 source/fixture evidence에 연결됐다.
- [x] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행한 fixture command에 exact text, 실제 observation과 exit status가 있다.
- [x] 실행하지 않은 candidate fixture는 `inferred`/unverified로 분리했다.
- [x] artifact path/URI, hash 또는 raw 폐기 이유와 retention이 있다.
- [x] risk/limitation과 evidence gap, owner와 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] secret/raw log/대용량 output이 packet에 없다.
- [x] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [x] `git diff --check --`와 `python3 /tmp/geness-oq002-markdown-check.py`를 최종 packet/fixture/evidence 변경 이후 실행했고 exit status와 결과를 기록했다.
