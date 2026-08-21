---
packet_schema_version: 1
packet_id: "OQ-012"
question_id: "OQ-012"
title: "Codex·Claude host OS·version·capability compatibility"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T04:10:00Z"
updated_at: "2026-08-21T05:08:00Z"
---

# OQ-012 — Codex·Claude host OS·version·capability compatibility

## 1. Scope and authority

- **Question:** Codex·Claude 최소 버전과 macOS/Linux/Windows 지원 범위는 무엇인가?
- **Phase/Gate:** Phase 0 / OQ-012 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** 공식 Codex·Claude host 문서, 현재 설치된 CLI의 read-only help/version
  surface, plugin·Skill·hook·MCP capability와 cross-model/claude-only setup policy를
  비교한다.
- **Non-goals:** 제품 manifest, Controller, package/runtime, installed-host E2E, plugin
  scaffold, final release policy와 사용자 결정을 대신하지 않는다. 실제 host에 plugin을
  설치하거나 MCP server를 시작하지 않는다.
- **Dependencies:** P0-03 / #15가 `CLOSED`·`status:done`이며 command API fixture evidence가
  `origin/main`에 있다. Existing host direction은 ADR-0001·ADR-0006이 소유한다.
- **Research owner:** Codex

이 packet은 관찰과 권고를 보존한다. vendor의 공식 최소 버전과 Geness의 지원 floor를
동일시하지 않으며, 사용자 decision receipt 없이 `Resolved`나 Accepted Host ADR로
승격하지 않는다. 제품 Implementation `HOLD`도 유지한다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | 보수적 dual-host 교집합 + capability gate | cross-model은 두 host의 문서화된 공통 OS와 초기 검증 release floor만 지원하고, setup read-only probe가 모든 required capability를 확인한다. claude-only는 Claude 단독 지원 범위를 추가한다. | Codex의 Windows 문서가 WSL2를 기준으로 유지되고, native Windows는 별도 E2E 전까지 cross-model에 포함하지 않는다. | `observed` OS/docs + local probe; policy is `inferred` |
| C-02 | capability-only rolling support | vendor-supported OS/version에서 required command·plugin·MCP·exec capability가 통과하면 version floor 없이 지원한다. | host가 capability를 semver보다 안정적으로 유지하고, 재현 가능한 release matrix를 별도 유지한다. | `inferred`; no historical-version probe |
| C-03 | broad host-native support | Codex native Windows target과 Claude native Windows/Alpine까지 하나의 cross-model matrix에 포함한다. | Codex native Windows installer target과 current CLI help만으로 installed-host parity를 추론할 수 있다. | `inferred` / unverified for Geness |

초기 release floor는 vendor minimum이 아니라 이번 machine에서 실제로 확인한 기준으로만
제안한다: `codex-cli 0.149.0`, `Claude Code 2.1.238`. 이보다 낮은 버전은 조사하지
않았으므로 지원 또는 비지원이라고 주장하지 않는다.

## 3. Trade-off matrix

| criterion | C-01 교집합 + gate | C-02 capability-only | C-03 broad native | evidence/source refs |
| --- | --- | --- | --- | --- |
| cross-model OS 재현성 | macOS 13+, Ubuntu 20.04+/Debian 10+, Windows 11 WSL2로 좁혀 문서 교집합을 명시한다. | vendor 범위를 따라 넓지만 release별 결과가 흔들릴 수 있다. | native Windows까지 넓지만 Codex 문서와 release asset 설명이 일치하지 않아 현재 근거가 약하다. | S-003, S-009, S-015 |
| claude-only 범위 | Claude 문서의 native Windows, WSL, Linux와 macOS를 별도로 허용할 수 있다. | probe가 Claude만 통과하면 넓은 범위를 허용한다. | cross-model과 동일한 broad 범위를 주장한다. | S-009, S-010, S-015 |
| 최소 version policy | 초기 검증 floor를 `Codex 0.149.0` / `Claude 2.1.238`로 기록하고, setup은 capability를 재확인한다. | semver 분기 부담이 낮지만 지원 재현성이 떨어진다. | 최신 설치만으로 충분하다고 가정한다. | S-003, S-009, S-015 |
| plugin/Skill compatibility | host별 manifest를 분리하고 공통 Skill body·stdio MCP·보조 hook subset만 공유한다. | 공통 subset을 계속 유지해야 한다. | host-specific capability를 공통 contract로 누출할 위험이 크다. | S-004~S-013 |
| hook 안전성 | hook은 optional guard/telemetry로 두고 trust와 event 차이를 adapter에 격리한다. | host별 hook semantics를 매 release 다시 확인해야 한다. | hook을 workflow authority로 사용하기 쉽다. | S-008, S-012, S-015 |
| 운영·지원 비용 | 지원 범위가 작고 실패 route가 명확하다. | runtime probe와 compatibility telemetry 비용이 증가한다. | 설치·E2E·문서 matrix 비용이 가장 크다. | S-001, S-002, S-015 |

### 3.1 Host capability matrix

`observed`는 현재 설치된 binary의 read-only probe, `official`은 vendor 문서 관찰이다.
`not-observed`는 지원하지 않는다는 뜻이 아니라 이번 Phase 0에서 실행하지 않았다는
뜻이다.

| capability | Codex | Claude Code | Geness compatibility boundary |
| --- | --- | --- | --- |
| OS baseline | `official`: macOS 12+, Ubuntu 20.04+/Debian 10+, Windows 11 via WSL2. Current source also contains native Windows targets, but that path is not aligned with the install doc. | `official`: macOS 13+, Windows 10 1809+/Server 2019+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+; native Windows and WSL modes. | cross-model은 보수적으로 macOS 13+, Ubuntu/Debian 공통 범위와 Windows 11 WSL2만 제안; native Windows/Alpine은 claude-only 또는 후속 E2E. |
| version | `observed`: `codex-cli 0.149.0`; vendor Geness minimum is not published. | `observed`: `2.1.238 (Claude Code)`; vendor Geness minimum is not published. Claude MCP v2 behavior is documented as version-sensitive. | 초기 tested floor 후보만 기록하고 setup capability gate를 함께 요구; older versions는 미확인. |
| plugin package | `official` `.codex-plugin/plugin.json`; `observed` `codex plugin` add/list/marketplace/remove. Local `--plugin-dir`/validator command was not observed. | `official` `.claude-plugin/plugin.json`; `observed` `--plugin-dir` and `claude plugin` validate/install/list surfaces. | 두 manifest/설치 adapter를 분리하고 공통 component path를 추측하지 않는다. |
| Skill | `official`: `SKILL.md` name/description, repo/user/admin/system discovery, `$` or `/skills` explicit and description implicit invocation. | `official`: plugin `skills/<name>/SKILL.md`, slash namespace and model-invoked descriptions. | common `SKILL.md` body와 minimal metadata만 공유; invocation/namespace는 adapter alias. |
| hooks | `official`: config/plugin `hooks.json`, trust review, command hooks and Codex event/matcher/output semantics. | `official`: plugin `hooks/hooks.json`, skill/agent frontmatter hooks, command/http/prompt/agent/mcp_tool types. | hook은 optional observation/guardrail; state/completion authority 금지. |
| MCP client | `observed` `codex mcp`, `codex mcp-server --help` stdio surface; `official` STDIO and Streamable HTTP, TOML config. | `observed` `claude mcp` add/list/serve/login; `official` project/user/plugin JSON config and stdio/HTTP-family transports. | v1 common transport는 local stdio; host-specific HTTP/OAuth는 optional capability. |
| non-interactive bridge | `observed` `codex exec --json --output-schema --ephemeral`; `official` JSONL/non-interactive execution. | `observed` `--print`, `--output-format json|stream-json`; `official` non-interactive `-p` path. | Controller가 host-specific envelope를 normalize; worker stdout만으로 completion하지 않는다. |
| root/session | `observed` `-C/--cd`, `resume`; `official` project config and local session behavior. | `observed` cwd/`--add-dir`, `--resume`; `official` plugin project-root variables and session behavior. | root/workspace/host session을 분리하고 host resume을 canonical task state로 사용하지 않는다. |
| status/command UX | `official` TUI `/status`, `$` Skill mention과 plugin browser. | `official` slash/Skill and `/mcp`/plugin menus. | `gee status`와 `gee resume`가 canonical; host-native forms는 aliases/read-only bridges. |
| trust/approval | `official` sandbox/approval/hook trust is host-owned. | `official` plugin/MCP project approval, permissions and hook trust are host-owned. | setup은 read-only probe; approval/sandbox 우회 금지. |

## 4. Sources

외부 source는 관찰만 사용했으며 코드·prompt·template 문구를 복사하지 않았다. OpenAI
GitHub source는 조사 시점의 immutable commit으로 고정했고, vendor docs 페이지는
versioned commit을 제공하지 않아 rolling page와 접근일을 명시했다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/04_HOST_INTEGRATION.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | host manifest·Skill·hook·MCP의 책임, shared `GENESS_HOME`, setup handshake와 v1 same-machine 범위를 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | `docs/adr/0006-v1-stage-and-host-profile.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | `auto`, `cross-model`, `claude-only` profile과 auto의 새 task fallback, active task silent switch 금지를 확인했다. | Accepted local ADR; no external reuse. |
| S-003 | `official` | `https://github.com/openai/codex/blob/2151d3a5b78ca93128496b26333bc30187385a5f/docs/install.md` | `2151d3a5b78ca93128496b26333bc30187385a5f` | 2026-08-21 | Codex install document lists macOS 12+, Ubuntu 20.04+/Debian 10+, and Windows 11 via WSL2; RAM and Git guidance are also listed. | OpenAI Codex repository is Apache-2.0; no source copied. |
| S-004 | `official` | `https://github.com/openai/codex/blob/2151d3a5b78ca93128496b26333bc30187385a5f/codex-rs/skills/src/assets/samples/plugin-creator/references/plugin-json-spec.md` | `2151d3a5b78ca93128496b26333bc30187385a5f` | 2026-08-21 | Codex plugin manifest sample uses `.codex-plugin/plugin.json` and declares skills, hooks, MCP servers and interface metadata. | OpenAI Codex repository is Apache-2.0; observation only. |
| S-005 | `official` | `https://developers.openai.com/codex/plugins` | rolling vendor docs; no immutable ref | 2026-08-21 | Codex CLI has a plugin browser; plugins can bundle skills, connectors, MCP servers and hooks; IDE extension does not expose the plugin browser. | Official OpenAI documentation; paraphrase only. |
| S-006 | `official` | `https://developers.openai.com/codex/skills` | rolling vendor docs; no immutable ref | 2026-08-21 | Codex skills use `SKILL.md` with `name` and `description`, support progressive disclosure, explicit `$`/`/skills` invocation and implicit description matching. | Official OpenAI documentation; paraphrase only. |
| S-007 | `official` | `https://developers.openai.com/codex/mcp` | rolling vendor docs; no immutable ref | 2026-08-21 | Codex supports local STDIO and Streamable HTTP MCP, stores CLI configuration in `config.toml`, and exposes `codex mcp`. | Official OpenAI documentation; paraphrase only. |
| S-008 | `official` | `https://developers.openai.com/codex/hooks` | rolling vendor docs; no immutable ref | 2026-08-21 | Codex hooks can be configured per layer or plugin, require trust review for non-managed hooks, and have host-specific event/matcher/output semantics. | Official OpenAI documentation; paraphrase only. |
| S-009 | `official` | `https://code.claude.com/docs/en/installation` | rolling vendor docs; no immutable ref | 2026-08-21 | Claude Code documents macOS 13+, Windows 10 1809+/Server 2019+, Ubuntu 20.04+, Debian 10+, Alpine 3.19+, x64/ARM64 and native/WSL Windows modes. | Official Anthropic documentation; paraphrase only. |
| S-010 | `official` | `https://code.claude.com/docs/en/plugins` | rolling vendor docs; no immutable ref | 2026-08-21 | Claude plugins support `.claude-plugin/plugin.json`, root-level skills/agents/hooks/MCP, local `--plugin-dir`, reload and component checks. | Official Anthropic documentation; paraphrase only. |
| S-011 | `official` | `https://code.claude.com/docs/en/plugins-reference` | rolling vendor docs; no immutable ref | 2026-08-21 | Claude plugin CLI exposes init/install/uninstall/enable/disable/list/validate; plugin component paths and scopes are defined. | Official Anthropic documentation; paraphrase only. |
| S-012 | `official` | `https://code.claude.com/docs/en/hooks` | rolling vendor docs; no immutable ref | 2026-08-21 | Claude hook types include command/http/prompt/agent/mcp_tool; plugin and skill hook lifecycle differs from Codex. | Official Anthropic documentation; paraphrase only. |
| S-013 | `official` | `https://code.claude.com/docs/en/mcp` | rolling vendor docs; no immutable ref | 2026-08-21 | Claude supports project/user/plugin MCP configuration and stdio/HTTP-family transports; project-scoped approval and runtime version behavior are host-owned. | Official Anthropic documentation; paraphrase only. |
| S-014 | `local-fixture` | `docs/research/phase-0/fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/README.md` | `5ab614d3016fe85ec2a22bdfadea7649150580aa` | 2026-08-21 | Fixture isolation, read-only probes, synthetic profile cases and transport parity boundary. | Local project research convention; no external reuse. |
| S-015 | `local-observation` | `docs/research/phase-0/evidence/OQ-012/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/RUN-OQ012-001/result.json` | fixture result hash below | 2026-08-21 | Current macOS arm64 probe observed Codex 0.149.0 and Claude 2.1.238; all required help/probe assertions passed. | Generated local evidence; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-HOST-CAPABILITY-COMMAND-SURFACE-001` | Codex/Claude read-only capability and profile/command parity comparison | `input/fixture.json`; both host binaries on `PATH`; no authentication or MCP server required | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | host probes pass; 26 synthetic cases produce 83 assertions; library/CLI/MCP projections agree | runner, transports and input are tracked; host output/temp state is hashed or discarded |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ012-001` | `FX-HOST-CAPABILITY-COMMAND-SURFACE-001` | 2026-08-21T05:07:56Z / 2026-08-21T05:07:58Z | `docs/research/phase-0/fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — Codex 0.149.0 and Claude 2.1.238 read-only probes passed; profile, route, status, resume and transport assertions passed (`83/83`). | A-001, A-002, A-003 |

Additional execution and source checks:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile surface_service.py cli_transport.py mcp_transport.py runner.py` | `0` | four fixture sources parse successfully under the fixture-local Python 3 interpreter. |
| `python3 -m json.tool input/fixture.json >/dev/null` | `0` | synthetic input is valid JSON. |
| `git diff --check --` | `0` | no whitespace errors in the repository diff after the packet, ADR, index and progress edits. |
| `node /tmp/geness-p0-06-markdown-check.mjs` | `0` | read-only Markdown integrity check: `markdown_files=61`, `local_links=159`, `local_anchor_links=8`, `fence_delimiters=152`, `trailing_whitespace=0`, `errors=[]`. |

Additional execution environment:

- **Tool/runtime versions:** fixture runner `/usr/bin/python3`, Python `3.9.6`; Codex `codex-cli 0.149.0`; Claude `2.1.238 (Claude Code)`; Darwin `25.4.0` arm64.
- **Environment overrides:** per-run temporary `CODEX_HOME`; `CLAUDE_CODE_SIMPLE=1`; `NO_COLOR=1`; `PYTHONDONTWRITEBYTECODE=1` for fixture subprocesses.
- **Network/external writes:** disabled / none; no login, install, plugin activation or MCP server startup.
- **Redaction:** help/stdout/stderr content is not retained; only version, command IDs, exit status, token checks and SHA-256 hashes are in the evidence manifest.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | synthetic input | `docs/research/phase-0/fixtures/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/input/fixture.json` | fixture definition | `sha256:8ffefbcbd76b4e8dcb3830196770e0713bdafcbe739bab5e8805a3f507b4e920` | `tracked` | fixed host token checks, setup/profile cases and route cases |
| A-002 | redacted result manifest | `docs/research/phase-0/evidence/OQ-012/FX-HOST-CAPABILITY-COMMAND-SURFACE-001/RUN-OQ012-001/result.json` | `RUN-OQ012-001` | `sha256:25ff01711cc2a9aaf063fd117822f39d76f3b801fdec4dd8ea5dea49170d0511` | `packet` | current host versions, required capability probes and setup profile policy |
| A-003 | raw runner stdout | `/tmp/<fixture-run>/run.json` | `RUN-OQ012-001` | `sha256:79ea167189cd5216e1528c569d03be9d7849544f76926bd7bd2c6e442beb5064`; discarded after redaction | `discarded` | actual 83-assertion runner output before reduction |

No credentials, environment dump, target `.geness/` state, real `~/.geness/` state, plugin
cache or MCP transcript was retained.

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | Only the installed Codex 0.149.0 and Claude 2.1.238 were probed. | `high` | No N-1, minimum-version or upgrade/rollback probe exists. | Treat these as the initial tested floor only; run a version matrix before accepting a release support policy. | user / Phase 0 | `open` |
| R-002 | Codex install documentation says Windows 11 via WSL2, while the current source contains native Windows installer/target material. | `high` | Native Windows plugin/Skill/MCP and cross-host E2E are not observed. | Keep native Windows Codex out of cross-model support until the official docs and installed-host E2E converge. | user / Phase 6 | `open` |
| R-003 | The local probe checks CLI help/version/features only; it does not install or enable a plugin, load a Skill, start MCP, or run `codex exec`/`claude -p`. | `high` | Installed plugin lifecycle and authenticated host bridge remain unobserved. | Require disposable plugin validation and both installed-host handoff E2Es after Phase 0 decisions. | Phase 1/6 | `open` |
| R-004 | Codex and Claude expose different manifest paths, hook events, trust rules, and MCP configuration models. | `medium` | Common component subset and schema translation are not production-tested. | Keep two adapter manifests; constrain shared Skill body to common Agent Skills metadata and use stdio MCP first. | user / Phase 1 | `open` |
| R-005 | Claude MCP v2 behavior is version-sensitive and the packet does not select a protocol revision. | `medium` | Geness Controller protocol and MCP negotiation are undecided. | Record host capability snapshots and defer protocol selection to the canonical API/host ADR. | user / Phase 0 | `open` |
| R-006 | Host help output and rolling vendor docs can change without an immutable docs ref. | `medium` | Long-term source reproducibility is weaker for vendor docs. | Keep accessed date, installed version, output hashes and repeat the probe in release CI. | Phase 7 | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 — conservative dual-host intersection plus a capability gate.
  Publish the initial tested floors as Codex `0.149.0` and Claude Code `2.1.238`, but label
  them as Geness evidence floors rather than vendor minimums. For cross-model, support the
  documented common range of macOS 13+, Ubuntu 20.04+/Debian 10+, and Windows 11 via WSL2;
  allow Claude-only to use Claude's documented native Windows and additional Linux range
  after a Claude-only host check. Keep plugin manifests separate, share only the common
  Skill/MCP contract, and keep hooks optional and non-authoritative.
- **Rationale:** Official sources show both hosts can provide Skills, plugin packaging,
  hooks and MCP, but their manifest paths, invocation, trust and lifecycle details differ.
  The local probe observed the required Codex `exec`/plugin/MCP/stdio surfaces and Claude
  print/resume/plugin/MCP surfaces. The fixture verified profile fallback, active-task
  protection and 26 setup/status/resume/description cases with identical library/CLI/MCP
  projections.
- **Rejected/deferred candidates:** C-02 remains a possible long-term capability contract
  but is too weak as the first support promise without historical-version evidence. C-03 is
  deferred because native Windows Codex behavior is not aligned across the current official
  install document and source material, and no installed-host E2E was run.
- **Unresolved impact:** The exact Geness minimum version, N-1 policy, native Windows
  cross-model status, plugin validation contract, and supported MCP protocol remain open.
  No product manifest or implementation scaffold may be created from this packet alone.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

사용자가 C-01의 cross-model 교집합·초기 tested floor와 C-02의 capability-gate 여부를
선택한 뒤, native Windows Codex 및 N-1 version probe를 승인된 compatibility matrix로
실행한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] OS/version/capability 후보가 셋이며 C-02/C-03의 미확인 범위가 기록됐다.
- [x] candidate와 동일 기준의 trade-off가 source/fixture evidence에 연결됐다.
- [x] source마다 locator, pinned ref 또는 rolling-doc 한계, accessed date와 license/action이 있다.
- [x] 실행한 fixture command에 exact text, 실제 observation과 exit status가 있다.
- [x] 실행하지 않은 installed-host/plugin E2E는 limitation으로 분리했다.
- [x] artifact path/URI, hash 또는 raw 폐기 이유와 retention이 있다.
- [x] risk/limitation과 evidence gap, owner와 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] secret/raw log/대용량 output이 packet에 없다.
- [x] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [x] `git diff --check --`와 관련 Markdown 검증 결과를 최종 packet/fixture/ADR/progress 변경 이후 추가했다.
