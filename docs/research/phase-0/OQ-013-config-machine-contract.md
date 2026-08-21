---
packet_schema_version: 1
packet_id: "OQ-013"
question_id: "OQ-013"
title: ".geness/config.yaml과 task별 machine JSON 필요성 비교"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T00:38:27Z"
updated_at: "2026-08-21T00:57:55Z"
---

# OQ-013 — .geness/config.yaml과 task별 machine JSON

## 1. Scope and authority

- **Question:** `.geness/config.yaml`과 task별 machine JSON이 필요한가, Markdown frontmatter와
  home runtime boundary만으로 충분한가?
- **Phase/Gate:** Phase 0 / OQ-013 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** portable project/task field와 machine/runtime field boundary, separate
  config/task machine JSON 후보, frontmatter-plus-runtime fixture observation
- **Non-goals:** config key 최종 schema, precedence/merge algorithm, secrets policy의 최종
  threshold, CLI command, target `.geness/` 생성, product implementation과 user decision
  receipt 확정
- **Dependencies:** #14 closed/done; OQ-005 identity, OQ-006 schema와 OQ-007 digest는 user
  decision 전이다.
- **Research owner:** Codex review

이 packet은 현재 Storage/Architecture 경계를 검증하는 research다. config candidate를
채택하거나 `OPEN` 질문을 `Resolved`로 옮기지 않으며 Implementation `HOLD`를 유지한다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | Frontmatter + project.json + home runtime boundary | project identity는 portable `project.json`, task contract는 Markdown frontmatter, machine/runtime state는 `GENESS_HOME` 아래 DB/evidence로 둔다. 별도 project config/task machine JSON은 v1에 추가하지 않는다. | task별 policy가 contract frontmatter와 approved plan으로 표현 가능하고 machine capability는 runtime receipt로 충분하다. | `observed` boundary fixture + `inferred` recommendation |
| C-02 | Optional `.geness/config.yaml` + frontmatter | project-wide allowed scope/test policy 같은 stable policy를 tracked config로 분리하고 task contract는 frontmatter에 둔다. machine-only state는 home runtime에 둔다. | project policy가 task contract와 독립적으로 재사용되고 precedence/merge를 명확히 정의할 수 있다. | `inferred` — 별도 config parser 미실행 |
| C-03 | config.yaml + per-task machine JSON | project config와 task별 machine JSON을 별도 machine contract로 두고 Markdown은 human projection이 된다. | 여러 host/tool이 별도 machine fields를 직접 소비해야 하며 multi-file drift를 감수한다. | `inferred` — 별도 round-trip 미실행 |

## 3. Trade-off matrix

| criterion | C-01 minimal boundary | C-02 project config | C-03 config + task JSON | evidence/source refs |
| --- | --- | --- | --- | --- |
| portable diff / review | fixture에서 portable field와 machine field overlap/forbidden field가 0이었다. `observed` | project policy diff가 명확해질 수 있으나 file count가 늘어난다. `inferred` | human projection과 machine JSON drift가 동시에 생긴다. `inferred` | F-001, A-001, S-001/S-002 |
| machine state leakage | runtime path, host session, evidence path와 secret를 portable set에서 배제했다. `observed` | config에 machine path가 섞이면 leakage 위험이 늘어난다. `inferred` | task JSON에 host/session/evidence metadata가 들어갈 위험이 높다. `inferred` | F-001, A-001, S-004 |
| task contract round-trip | frontmatter/DB round-trip과 stale guard를 같은 fixture에서 관찰했다. `observed` | config↔frontmatter precedence가 추가된다. `inferred` | 두 machine file과 Markdown을 함께 reconcile해야 한다. `inferred` | F-001, A-001, S-003 |
| policy reuse | 별도 config가 없어 project-wide policy 중복이 생길 수 있다. `inferred` | shared policy를 표현하는 장점이 있다. `inferred` | 가장 유연하지만 policy source가 많아진다. `inferred` | S-001, S-005 |
| migration/compatibility | surface가 작고 frontmatter/runtime schema 두 축만 versioning한다. `inferred` | config schema/precedence migration이 추가된다. `inferred` | config, task JSON, frontmatter 세 schema가 drift할 수 있다. `inferred` | S-002, S-006 |
| security / retention | tracked contract와 private runtime을 분리한다. `observed` boundary / full threat test pending | config secret 실수 방지가 필요하다. `inferred` | machine JSON의 host/session/evidence path와 secret redaction이 필요하다. `inferred` | S-002, S-004 |

## 4. Sources

모든 source는 repository-local canonical 문서이며 외부 코드·문구를 복사하지 않았다.
`pinned ref`는 조사 기준 commit `176e9375c0ad51614ce12f4bae7aa00c0130b5dd`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/03_STORAGE.md#2-세-저장-경계` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | target `.geness/`, runtime와 memory의 ownership 및 `config.yaml` 도입 여부 TBD를 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | `docs/04_HOST_INTEGRATION.md#6-shared-data-home` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | `GENESS_HOME`과 vendor data directory의 canonical 경계를 확인했다. | Local project document; no external reuse. |
| S-003 | `local-doc` | `docs/06_SPECIFICATION.md#3-specmd-최소-계약` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | spec frontmatter가 contract/provenance/AC/execution policy를 portable하게 표현하는 현재 제안을 확인했다. | Local project document; no external reuse. |
| S-004 | `local-doc` | `docs/00_GENESS.md#7-데이터-경계` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | source docs, target `.geness/`, home runtime/memory와 plugin cache의 security/data boundary를 확인했다. | Local project document; no external reuse. |
| S-005 | `local-doc` | `docs/adr/0002-project-and-local-state-boundary.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | portable project documents와 local mutable state를 분리하는 Accepted decision을 확인했다. | Accepted local ADR; no external reuse. |
| S-006 | `local-doc` | `docs/PLAN.md#23-구현-전-미결정-사항` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | `.geness/config.yaml`과 task별 machine JSON을 Phase 0 decision으로 두고 frontmatter-only를 먼저 검증한다는 계획을 확인했다. | Local project plan; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | portable project/task fields와 machine/runtime fields의 overlap·forbidden field·separate file 후보 관찰 | deterministic boundary lists와 frontmatter/DB case | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | portable/machine overlap 0, forbidden field 0, fixture profile `frontmatter-plus-runtime-boundary` | temporary state와 raw output만 폐기; target/home은 건드리지 않음 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ013-001` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-21T00:49:56Z / 2026-08-21T00:49:57Z | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — config boundary 4 assertions 포함 30/30 | A-001, A-002, A-003 |
| `RUN-OQ013-002` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-21T00:49:57Z / 2026-08-21T00:49:57Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — parsed JSON output equality confirmed | A-004 |

### 5.3 Observed result

- portable project/task field set과 machine/runtime field set의 overlap은 `[]`였다.
- `host_session_id`, `runtime_db_path`, `evidence_path`, `secret`가 portable set에 없었다.
- fixture-local C-01 profile은 별도 project config와 task machine JSON을 `false`로 두었다.
  이는 C-01 candidate를 실행한 관찰이지 product config policy의 승인 결과가 아니다.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | redacted result manifest | `docs/research/phase-0/evidence/OQ-013/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ013-001/result.json` | `RUN-OQ013-001` | recorded after final validation | `packet` | portable/local config boundary |
| A-002 | fixture runner | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | fixture definition | recorded after final validation | `tracked` | repeatable boundary assertion |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json` | fixture definition | recorded after final validation | `tracked` | portable/machine field sets |
| A-004 | redacted rerun result | `docs/research/phase-0/evidence/OQ-013/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ013-002/result.json` | `RUN-OQ013-002` | same manifest; parsed outputs equal | `packet` | repeatability |
| A-005 | raw stdout/temp state | temporary per-run state | `RUN-OQ013-001/002` | discarded after redaction | `discarded` | raw execution only |

Additional validation commands:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | `0` | runner parses successfully |
| `python3 -m json.tool docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json >/dev/null` | `0` | input is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-013/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ013-001/result.json >/dev/null` | `0` | evidence is valid JSON |
| `git diff --check --` | `0` | no whitespace error after final edit |
| read-only Node Markdown local-link/fence check | `0` | `markdown_files=57`, `local_links=147`, `fence_delimiters=122`, `trailing_whitespace=0`, `errors=[]` |

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | no separate config/task JSON was tested against a real host capability or policy consumer. | `high` | project-wide policy reuse, precedence, profile capability and setup bootstrap fields are 미확인이다. | OQ-012/OQ-014와 selected runtime setup prototype에서 read-only compare를 수행한다. | user / Phase 1 | `open` |
| R-002 | boundary assertion does not prove secrets are redacted in every future field. | `high` | nested evidence/env/config values and threat model coverage are 미확인이다. | OQ-008 threat/permission work and schema validator redaction fixture로 보강한다. | user | `open` |
| R-003 | frontmatter-only candidate can duplicate project-wide policy across tasks. | `medium` | policy reuse/override semantics와 user ergonomics가 미확인이다. | 사용자가 C-01/C-02를 선택하고 config precedence를 ADR로 기록한다. | user | `open` |
| R-004 | task machine JSON absence is a fixture input, not a compatibility promise. | `medium` | host adapter schema와 installed capability snapshot이 아직 없다. | Phase 6 host E2E 전까지 task machine JSON을 제품 API로 만들지 않는다. | user / Phase 6 | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 for v1 bootstrap — portable `project.json`/task frontmatter와 local
  `GENESS_HOME` runtime/memory boundary를 우선하고, 별도 `.geness/config.yaml`과 task machine
  JSON은 실제 project-wide policy reuse 또는 host capability gap이 evidence로 확인될 때만
  추가한다.
- **Rationale:** fixture는 portable projection에서 runtime path, host session, evidence path와
  secret를 분리했고 frontmatter/DB stale guard를 함께 통과시켰다. 이는 plugin cache/vendor
  data를 canonical state로 쓰지 않고 target contract와 home mutable state를 분리하는
  `ADR-0002`/Storage 방향을 유지한다.
- **Rejected/deferred candidates:** C-02는 policy reuse 장점이 있으나 precedence와 threat
  surface를 측정하지 못해 deferred; C-03은 multi-file drift와 secret leakage risk 때문에
  deferred. user decision 전에는 어떤 config file도 제품 artifact로 생성하지 않는다.
- **Unresolved impact:** config inclusion, precedence, task machine JSON 필요성, capability
  snapshot schema가 닫히지 않으면 setup/contract schema를 확정할 수 없다.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

사용자가 C-01/C-02/C-03 config boundary를 결정하고, 선택한 project policy/host capability
evidence에 따라 config precedence와 machine contract 필요성을 별도 ADR 또는 schema packet으로
기록한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] 세 config candidate와 assumption/evidence status가 기록됐다.
- [x] trade-off가 source/fixture evidence에 연결됐다.
- [x] portable/local boundary와 forbidden field 결과가 기록됐다.
- [x] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행 command, exit status, artifact와 raw redaction이 기록됐다.
- [x] config parser/host capability/policy precedence limitation이 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] 제품 config/task JSON/target `.geness/`를 생성하지 않았다.
- [x] 최종 `git diff --check --`와 JSON/Markdown 검증 결과가 기록된다.
