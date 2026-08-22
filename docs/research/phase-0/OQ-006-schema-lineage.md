---
packet_schema_version: 1
packet_id: "OQ-006"
question_id: "OQ-006"
title: "task Markdown frontmatter·SQLite schema v1과 lineage 비교"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T00:38:27Z"
updated_at: "2026-08-21T00:57:55Z"
---

# OQ-006 — task Markdown frontmatter·SQLite schema v1과 lineage

## 1. Scope and authority

- **Question:** task Markdown frontmatter와 runtime SQLite schema v1의 canonical owner,
  stable ID/revision lineage, projection과 stale write 경계는 무엇인가?
- **Phase/Gate:** Phase 0 / OQ-006 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** fixture-local Markdown frontmatter↔SQLite round-trip, revision/digest stale
  write guard, portable document과 mutable runtime의 후보 비교
- **Non-goals:** production table/column/migration 선택, transaction crash atomicity, daemon,
  memory DB, product language/runtime, target `.geness/` 생성과 user decision receipt 확정
- **Dependencies:** #14 / OQ-001 runtime은 [ADR-0010](../../adr/0010-controller-runtime-go.md)으로
  resolved됐고 OQ-002는 [ADR-0011](../../adr/0011-canonical-command-api.md)과 receipt로
  resolved됐다. OQ-005의 identity boundary는 [ADR-0015](../../adr/0015-project-workspace-identity.md)로
  확정됐지만 exact ID algorithm/reconciliation과 OQ-007 digest profile이 아직 열려 있으므로
  결과는 boundary recommendation으로만 남긴다.
- **Research owner:** Codex review

이 packet은 관찰과 권고를 보존한다. OQ-006을 `Resolved`로 옮기거나 Schema/Storage ADR을
만들지 않으며 Implementation `HOLD`를 유지한다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | Portable frontmatter + runtime SQLite owner | 사람이 읽고 Git으로 공유하는 task Markdown은 contract/projection을 보유하고, mutable state·attempt·lease·verdict는 runtime SQLite가 보유한다. revision/digest와 operation ID로 reconciliation한다. | 문서와 DB write를 idempotent projection으로 연결하고 stale revision을 거부한다. | `observed` round-trip/stale fixture + Accepted boundary |
| C-02 | SQLite canonical, Markdown derived | SQLite가 contract와 모든 mutable state의 정본이고 Markdown은 export projection만 제공한다. | Git에서 직접 검토·merge하는 문서의 provenance와 stale projection을 별도 UX로 수용한다. | `inferred` — product fixture 미실행 |
| C-03 | Markdown canonical + sidecar machine JSON | Markdown이 task state 정본이고 JSON/SQLite는 보조 index 또는 cache가 된다. | multi-writer, lease와 attempt transaction을 document write로 안전하게 표현할 수 있다. | `inferred` — product fixture 미실행 |

## 3. Trade-off matrix

| criterion | C-01 frontmatter + runtime SQLite | C-02 SQLite canonical | C-03 Markdown canonical | evidence/source refs |
| --- | --- | --- | --- | --- |
| human review / Git portability | frontmatter와 body를 tracked artifact로 유지하고 raw runtime을 분리한다. `inferred` from current boundary | export diff가 canonical state와 한 단계 떨어진다. `inferred` | 가장 직접적이지만 mutable lease/log가 문서 diff로 섞일 위험이 있다. `inferred` | S-001/S-002/S-004 |
| round-trip | fixture-local parser가 semantic frontmatter와 body를 SQLite row를 거쳐 동일하게 복원했다. `observed` | DB-native round-trip은 쉽지만 Markdown projection reconciliation은 별도다. `inferred` | DB projection drift가 sidecar로 늘어난다. `inferred` | F-001, A-001 |
| stale write | revision+digest precondition을 검사해 second stale write를 DENIED하고 state를 보존했다. `observed` | DB transaction으로 가능하나 Markdown editor conflict UX가 필요하다. `inferred` | document merge와 revision guard를 동시에 보장해야 한다. `inferred` | F-001, A-001, S-003 |
| crash/recovery boundary | DB commit과 document projection을 operation ID/reconciliation으로 분리할 수 있다. `inferred` | DB는 단순하지만 portable projection recovery를 별도 구현한다. `inferred` | 문서 atomic replace와 runtime mutation의 두 권위가 충돌한다. `inferred` | S-002/S-003 |
| schema evolution | frontmatter schema와 runtime migration을 각각 versioning할 수 있다. `inferred` | 하나의 DB migration은 명확하지만 portable schema 변화가 hidden 될 수 있다. `inferred` | 여러 sidecar/parser 버전 drift 위험이 높다. `inferred` | S-002, S-005 |
| security / retention | raw log/evidence와 문서를 분리하고 runtime retention을 적용할 수 있다. `inferred` | export 시 private state 누출 방지가 필요하다. `inferred` | secret·대용량 state가 Git으로 새어 나갈 위험이 있다. `inferred` | S-002, S-004 |

## 4. Sources

모든 source는 repository-local canonical 문서이며 외부 코드·문구를 복사하지 않았다.
`pinned ref`는 조사 기준 commit `176e9375c0ad51614ce12f4bae7aa00c0130b5dd`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/01_ARCHITECTURE.md#6-canonical-state와-projection` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | spec.md와 runtime DB의 canonical owner, run/verification projection과 reconciliation 원칙을 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | `docs/03_STORAGE.md#5-project-document-contract` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | frontmatter, atomic document write, revision/digest, runtime SQLite logical tables와 stale revision 거부 원칙을 확인했다. | Local project document; no external reuse. |
| S-003 | `local-doc` | `docs/06_SPECIFICATION.md#3-specmd-최소-계약` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | v1 spec frontmatter 필드와 contract revision/digest·AC projection이 아직 schema 후보임을 확인했다. | Local project document; no external reuse. |
| S-004 | `local-doc` | `docs/adr/0002-project-and-local-state-boundary.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | target `.geness/`와 home runtime/memory를 분리하는 Accepted boundary를 확인했다. | Accepted local ADR; no external reuse. |
| S-005 | `local-doc` | `docs/adr/0007-v1-contract-and-verification-artifacts.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | target task artifact와 runtime DB authority, schema validation/migration test 필요성을 확인했다. | Accepted local ADR; no external reuse. |
| S-006 | `local-doc` | `docs/research/phase-0/DECISION_PACKET_TEMPLATE.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | packet은 observation과 user decision을 분리하고 실제 command/evidence를 기록해야 함을 확인했다. | Local research convention; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | frontmatter↔SQLite semantic round-trip과 revision/digest stale write guard 관찰 | deterministic frontmatter, in-memory SQLite row와 revision case | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | semantic/body equal, accepted revision 2, stale revision DENIED/no mutation | in-memory SQLite와 temporary Git state만 process 종료 시 폐기 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ006-001` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-21T00:49:56Z / 2026-08-21T00:49:57Z | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — frontmatter/DB semantic equality, body equality와 3 stale-write assertions 포함 30/30 | A-001, A-002, A-003 |
| `RUN-OQ006-002` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-21T00:49:57Z / 2026-08-21T00:49:57Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — parsed JSON output equality confirmed | A-004 |

### 5.3 Observed result

- `frontmatter_db_round_trip.semantic_fields_equal=true`, `body_equal=true`, one projection row,
  `task-p005-001`/revision `3`이 관찰됐다.
- accepted revision `2` write는 ALLOWED이고, revision `1`을 기대한 stale write는
  `DENIED / stale_revision`이며 current state는 revision `2`와 accepted digest로 유지됐다.
- 이 row/table은 fixture-local in-memory schema이며 production SQLite schema의 선택이나
  crash atomicity evidence가 아니다.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | redacted result manifest | `docs/research/phase-0/evidence/OQ-006/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ006-001/result.json` | `RUN-OQ006-001` | recorded after final validation | `packet` | round-trip/stale write observation |
| A-002 | fixture runner | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | fixture definition | recorded after final validation | `tracked` | repeatable SQLite/revision probe |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json` | fixture definition | recorded after final validation | `tracked` | stable frontmatter and revision input |
| A-004 | redacted rerun result | `docs/research/phase-0/evidence/OQ-006/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ006-002/result.json` | `RUN-OQ006-002` | same manifest; parsed outputs equal | `packet` | repeatability |
| A-005 | raw stdout/temp DB | temporary per-run state | `RUN-OQ006-001/002` | discarded after redaction; no secret or external write | `discarded` | raw execution only |

The fixture parser intentionally supports only a restricted frontmatter subset; full YAML
parser behavior, DB migration, concurrent writer race, crash-point recovery와 projection
reconciliation은 관찰하지 않았다.

Additional validation commands:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | `0` | runner parses successfully |
| `python3 -m json.tool docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json >/dev/null` | `0` | input is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-006/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ006-001/result.json >/dev/null` | `0` | evidence is valid JSON |
| `git diff --check --` | `0` | no whitespace error after final edit |
| read-only Node Markdown local-link/fence check | `0` | `markdown_files=57`, `local_links=147`, `fence_delimiters=122`, `trailing_whitespace=0`, `errors=[]` |

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | fixture parser is not a full YAML implementation and its one-line JSON subset is not a product compatibility promise. | `high` | YAML scalar/anchor/multiline/duplicate-key semantics와 cross-language parser parity가 미확인이다. | selected runtime 뒤 official parser/schema fixture와 schema version/migration test를 추가한다. | user / Phase 1 | `open` |
| R-002 | SQLite table is in-memory and fixture-local. | `high` | WAL/locking, transaction crash points, migration/rollback과 multi-process writer arbitration이 미관찰이다. | OQ-003/OQ-009 and selected runtime schema spike로 분리한다. | user | `open` |
| R-003 | one round-trip does not prove all v1 artifact fields or projection recovery. | `medium` | nested frontmatter, AC lineage, evidence freshness, manual edit reconciliation이 미확인이다. | OQ-007 digest vector와 Phase 1 schema validation/round-trip matrix를 추가한다. | user / Phase 1 | `open` |
| R-004 | stable ID/revision behavior was synthetic and depends on unresolved schema/digest details. | `high` | project/workspace ID algorithm, cross-file lineage와 OQ-007 digest profile are not selected. | C-01 identity boundary를 전제로 Schema/Storage ADR과 후속 fixture에서 exact algorithm/reconciliation을 promote한다. | user | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 — portable Markdown frontmatter는 사람이 읽고 Git으로 공유하는
  contract/projection으로 두고, runtime SQLite는 mutable state·revision guard·attempt·lease·
  verdict의 canonical owner로 둔다. 문서와 DB 사이에는 revision/digest/operation ID 기반
  idempotent projection/reconciliation을 둔다.
- **Rationale:** fixture가 frontmatter semantic fields와 body를 SQLite row를 거쳐 equality-
  equivalent하게 복원했고, accepted revision 이후 stale revision write를 거부하면서 current
  state를 보존했다. 이는 `ADR-0002`, `ADR-0007`, Storage/Architecture 문서의 owner 분리와
  일치한다. 단, fixture-local parser/table이 production schema를 결정하지는 않는다.
- **Rejected/deferred candidates:** C-02와 C-03은 portable review·projection drift·mutable
  concurrency trade-off 때문에 deferred이며 사용자 결정 전 product owner로 확정하지 않는다.
- **Unresolved impact:** exact frontmatter grammar, DB columns/indexes/migrations, projection
  crash recovery와 ID lineage가 닫히지 않으면 제품 schema를 만들 수 없다.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

사용자가 C-01 boundary recommendation을 채택할지 결정하고, OQ-005/007 결과와 함께
frontmatter grammar·runtime migration·projection recovery의 Schema/Storage ADR 범위를
정한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] 후보가 셋이며 미실행 product alternatives가 구분됐다.
- [x] trade-off가 source/fixture evidence에 연결됐다.
- [x] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행한 command에 exact text, 실제 observation과 exit status가 있다.
- [x] parser/SQLite의 미관찰 범위와 limitation이 기록됐다.
- [x] artifact path/URI, hash 또는 raw 폐기 이유와 retention이 있다.
- [x] risk/limitation과 evidence gap, owner와 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [x] 최종 `git diff --check --`와 JSON/Markdown 검증 결과가 기록된다.
