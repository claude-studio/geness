---
packet_schema_version: 1
packet_id: "OQ-005"
question_id: "OQ-005"
title: "clone·fork·rename·worktree project/workspace identity 비교"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T00:38:27Z"
updated_at: "2026-08-21T00:57:55Z"
---

# OQ-005 — clone·fork·rename·worktree project/workspace identity

## 1. Scope and authority

- **Question:** clone, fork, folder rename과 worktree에서 `project_id`와 `workspace_id`는
  어떻게 변하는가?
- **Phase/Gate:** Phase 0 / OQ-005 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** local Git clone/fork/rename/worktree 관찰, 동명 repository 충돌 사례,
  project/workspace identity relation 후보 비교
- **Non-goals:** project ID 생성 알고리즘의 제품 채택, fork 자동 감지, workspace registry,
  runtime lease, cloud sync, 제품 schema·Controller·plugin scaffold와 user decision receipt
  확정
- **Dependencies:** #14 / OQ-001은 [ADR-0010](../../adr/0010-controller-runtime-go.md)과
  receipt로 resolved됐고 OQ-002는 [ADR-0011](../../adr/0011-canonical-command-api.md)과
  receipt로 resolved됐다. #14는 `closed`·`status:done`으로 확인했으며 이 packet은 command
  API 결정을 대신하지 않는다.
- **Research owner:** Codex review

이 packet은 관찰과 권고를 보존한다. `OQ-005`를 `Resolved`로 옮기거나 Storage ADR을
만들지 않으며 제품 Implementation `HOLD`를 유지한다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | Explicit project lineage + workspace registry | portable `project.json`의 stable `project_id`와 local workspace record의 `workspace_id`를 분리한다. clone은 project를 공유하고, fork는 명시적 detach/rekey 후 새 project가 되며, rename은 metadata를 유지하고 worktree는 새 workspace가 된다. | project metadata가 복사·보존되고 fork 사용자가 detach 의도를 표시한다. rename 뒤 runtime path/registry reconciliation이 가능하다. | `observed` relation fixture + `inferred` policy |
| C-02 | Git remote/object-derived project identity | canonical remote 또는 Git object lineage에서 project ID를 계산한다. clone·rename·worktree는 동일 source로 묶고 다른 fork remote는 분리한다. | remote URL이 존재·정규화 가능하고 local mirror/duplicate remote가 동일 project로 취급돼도 된다. | `observed` Git facts + `inferred` policy |
| C-03 | Path/workspace-derived identity | resolved folder path 또는 workspace path를 project key로 사용한다. 별도 registry 없이 구현할 수 있다. | folder rename, clone과 worktree가 새로운 project로 분리돼도 되고 portable resume이 path에 종속돼도 된다. | `inferred` — 별도 product fixture 미실행 |

## 3. Trade-off matrix

`observed`는 fixture가 직접 확인한 사실이고 `inferred`는 문서 계약과 관찰에서 도출한
설계 영향이다. 표는 사용자 결정을 자동으로 채택하지 않는다.

| criterion | C-01 Explicit lineage | C-02 Git-derived | C-03 Path-derived | evidence/source refs |
| --- | --- | --- | --- | --- |
| clone | project shared, workspace distinct를 명시적으로 표현할 수 있다. `observed` | local clone의 Git history/remote가 유지되면 shared 후보가 된다. `observed` | clone path가 달라져 project가 분리된다. `inferred` | F-001, A-001, S-001/S-002 |
| folder rename | project와 workspace metadata를 유지하면 same workspace로 resume할 수 있다. `observed` relation / registry는 미구현 | Git repository는 rename 뒤에도 같은 HEAD를 읽었다. `observed`; ID 보존은 별도 정책 | path key가 바뀌므로 orphan/new project 위험이 있다. `inferred` | F-001, A-001 |
| worktree | project shared, workspace distinct를 표현하며 runtime을 격리할 수 있다. `observed` relation | Git common dir와 history 공유는 관찰되지만 concurrent workspace 권위는 미검증 | worktree path가 project를 분리한다. `inferred` | F-001, A-001, S-002 |
| fork / detach | implicit sharing을 피하고 명시적 rekey를 audit할 수 있다. `observed` synthetic relation / user policy pending | 다른 remote가 있으면 분리 후보지만 local fork·mirror와 remote 정규화 예외가 남는다. `inferred` | 다른 path만으로 분리되므로 fork 의도와 clone을 구분하지 못한다. `inferred` | F-001, A-001, S-001 |
| 동명 repository 충돌 | display name과 identity를 분리한다. `observed` | remote/object canonicalization 품질에 의존한다. `inferred` | path가 다르면 구분되지만 path 이동 시 안정성이 낮다. `inferred` | F-001, A-001, S-001 |
| 운영·복구 비용 | explicit artifact와 registry reconciliation이 필요하다. `inferred` | remote가 없거나 바뀐 repository의 recovery 정책이 필요하다. `inferred` | 가장 단순하지만 rename·portable resume 오류가 크다. `inferred` | S-001, S-002, S-003 |

## 4. Sources

모든 source는 repository-local canonical 문서이며 외부 코드·문구를 복사하지 않았다.
`pinned ref`는 조사 기준 commit `176e9375c0ad51614ce12f4bae7aa00c0130b5dd`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/00_GENESS.md#7-데이터-경계` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | target `.geness/`, runtime과 memory의 경계, one-writer와 user-prepared worktree 원칙을 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | `docs/03_STORAGE.md#3-project-identity` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | project ID는 folder rename/worktree에 안정적이어야 하고 workspace는 machine 실행 경계를 구분한다는 현재 제안과 clone/fork TBD를 확인했다. | Local project document; no external reuse. |
| S-003 | `local-doc` | `docs/04_HOST_INTEGRATION.md#8-resume와-v1-범위` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | v1은 같은 machine·GENESS_HOME·사용자 준비 worktree를 전제로 하며 host session은 identity가 아님을 확인했다. | Local project document; no external reuse. |
| S-004 | `local-doc` | `docs/adr/0002-project-and-local-state-boundary.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | target project 문서와 home mutable runtime/memory를 분리하는 Accepted boundary를 확인했다. | Accepted local ADR; no external reuse. |
| S-005 | `local-doc` | `docs/PLAN.md#phase-0-핵심-계약과-adr-확정` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | OQ-005의 계획 artifact가 clone/fork/rename/same-name/worktree identity fixture임을 확인했다. | Local project plan; no external reuse. |
| S-006 | `local-doc` | `docs/research/phase-0/FIXTURE_RULES.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | fixture isolation, exact command/exit status, redacted artifact/hash와 `not-run` 규칙을 확인했다. | Local research convention; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 실제 local Git의 clone/fork/rename/worktree facts와 synthetic project/workspace relation 비교 | `input/fixture.json`의 deterministic IDs와 temporary local Git repository | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | 30 assertions pass; local Git facts와 identity relation이 expected matrix와 일치 | runner가 만든 temporary Git state와 SQLite만 폐기; tracked input/runner와 redacted result는 보존 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ005-001` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-21T00:49:56Z / 2026-08-21T00:49:57Z | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 30/30 assertions, local Git probe, relation matrix, output equality | A-001, A-002, A-003 |
| `RUN-OQ005-002` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-21T00:49:57Z / 2026-08-21T00:49:57Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — parsed JSON output equality confirmed against RUN-OQ005-001 | A-004 |

Additional validation commands are recorded after the final packet/fixture edit in the
evidence section below.

### 5.3 Observed result

- local `git init`, local `git clone`, folder rename, `git worktree add`와 synthetic fork
  remote change가 temporary directory에서 모두 exit `0`으로 수행됐다.
- clone과 rename의 HEAD, worktree HEAD가 같고 worktree가 Git common dir를 공유했다.
- fixture relation은 clone/worktree의 `project_id` 공유와 workspace 분리, rename의 project와
  workspace 유지, fork와 동명 repository의 explicit detach를 통과했다.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | redacted result manifest | `docs/research/phase-0/evidence/OQ-005/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ005-001/result.json` | `RUN-OQ005-001` | recorded after final validation | `packet` | identity relation matrix와 local Git observation |
| A-002 | fixture runner | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | fixture definition | recorded after final validation | `tracked` | repeatable local Git/identity probe |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json` | fixture definition | recorded after final validation | `tracked` | deterministic identity cases |
| A-004 | redacted rerun result | `docs/research/phase-0/evidence/OQ-005/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ005-002/result.json` | `RUN-OQ005-002` | same manifest; parsed outputs equal | `packet` | repeatability |
| A-005 | raw stdout/temp Git state | temporary per-run state | `RUN-OQ005-001/002` | discarded after redaction; no secret or external write | `discarded` | raw execution only |

The fixture state, absolute temporary paths and raw stdout/stderr are not preserved. No target
`.geness/` or real `GENESS_HOME` state was used.

Additional validation records:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | `0` | runner parses successfully |
| `python3 -m json.tool docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json >/dev/null` | `0` | deterministic input is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-005/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ005-001/result.json >/dev/null` | `0` | redacted evidence is valid JSON |
| `git diff --check --` | `0` | no whitespace error after packet/fixture/evidence edits |
| read-only Node Markdown local-link/fence check | `0` | `markdown_files=57`, `local_links=147`, `fence_delimiters=122`, `trailing_whitespace=0`, `errors=[]` |

Tool/runtime versions and environment:

- fixture Python path/version and `git --version` are recorded in the final worktree verification.
- network/external writes: disabled / none
- environment override: `PYTHONDONTWRITEBYTECODE=1`; no `GENESS_HOME` override
- redaction: temporary Git paths and raw output removed; only relation booleans, IDs, hashes and
  result categories retained

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | local Git clone/worktree facts do not define Geness project lineage policy. | `high` | fork intent, project.json copy, registry migration과 explicit rekey UX가 관찰되지 않았다. | 사용자에게 C-01/C-02/C-03 중 lineage policy를 선택받고 Storage ADR/fixture를 별도로 확정한다. | user | `open` |
| R-002 | fork is represented by local clone plus synthetic remote/detach marker, not a hosted fork API. | `medium` | GitHub/GitLab fork metadata와 remote normalization이 미관찰이다. | selected host/provider가 생긴 뒤 read-only provider fixture를 승인해 추가한다. | user / Phase 6 | `open` |
| R-003 | workspace registry, path rename reconciliation과 cross-workspace writer arbitration은 실행하지 않았다. | `high` | orphan runtime, lease takeover와 same project의 concurrent worktree가 미관찰이다. | OQ-003/OQ-006/OQ-009 race/recovery fixture로 분리한다. | user | `open` |
| R-004 | C-02/C-03은 독립 product implementation이 아니라 trade-off inference다. | `medium` | remote/object/path identity의 충돌·성능 비교가 없다. | 사용자 결정 전에는 제품 ID algorithm을 구현하지 않는다. | user | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 — explicit stable project lineage와 workspace-scoped runtime을
  분리하고, clone은 shared project, rename은 metadata-preserving same workspace, worktree는
  distinct workspace, fork는 명시적 detach/rekey로 취급한다.
- **Rationale:** local Git probe는 clone/rename/worktree가 동일 history를 보존하고 worktree가
  common dir를 공유함을 확인했지만, 그 사실만으로 project identity를 자동 추론할 수는 없다.
  synthetic relation fixture는 display name/path/Git history와 durable project/workspace
  identity를 분리해야 clone·fork·rename·worktree를 구분할 수 있음을 보였다. 이는
  `docs/03_STORAGE.md`의 project/workspace 경계와 `ADR-0002`의 portable/local boundary에
  맞는다.
- **Rejected/deferred candidates:** C-02는 remote/object 예외와 fork intent 불명확성 때문에
  deferred; C-03은 rename/clone/worktree resume 불안정성 때문에 deferred. 사용자 결정 전
  rejected/accepted로 확정하지 않는다.
- **Unresolved impact:** project ID 생성·rekey algorithm, workspace registry와 cross-workspace
  writer authority가 닫히지 않으면 제품 schema와 runtime 구현을 시작할 수 없다.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

사용자가 C-01/C-02/C-03 중 project/workspace lineage policy를 선택하고, 선택 결과를 Storage
ADR 및 project identity migration/reconciliation fixture의 입력으로 기록한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] 후보가 셋이며 C-02/C-03의 미실행 범위가 기록됐다.
- [x] candidate와 동일 기준의 trade-off가 source/fixture evidence에 연결됐다.
- [x] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행한 fixture command에 exact text, 실제 observation과 exit status가 있다.
- [x] 실행하지 않은 product/provider fixture는 risk와 `deferred`로 분리했다.
- [x] artifact path/URI, hash 또는 raw 폐기 이유와 retention이 있다.
- [x] risk/limitation과 evidence gap, owner와 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] secret/raw log/대용량 output이 packet에 없다.
- [x] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [x] `git diff --check --`와 관련 JSON/Markdown 검증 결과가 최종 변경 뒤 기록된다.
