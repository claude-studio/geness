---
packet_schema_version: 1
packet_id: "OQ-007"
question_id: "OQ-007"
title: "contract·plan digest canonicalization과 invalidation 비교"
status: "resolved"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T00:38:27Z"
updated_at: "2026-08-22T15:02:35Z"
---

# OQ-007 — contract·plan digest canonicalization과 invalidation

## 1. Scope and authority

- **Question:** contract와 plan digest를 어떤 canonicalization으로 계산하고 editorial/semantic
  변경을 어떻게 구분하는가?
- **Phase/Gate:** Phase 0 / OQ-007 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** versioned semantic projection 후보, contract/plan golden vector, key-order와
  editorial/semantic 변경, downstream invalidation 관계의 fixture 관찰
- **Non-goals:** SHA-256 이외 hash 선택, RFC/JCS compatibility 채택, production serializer,
  schema/migration, cross-runtime edge-case validation과 Implementation `CLEAR`
- **Dependencies:** #14 closed/done; OQ-005 identity boundary는 [ADR-0015](../../adr/0015-project-workspace-identity.md)로
  resolved됐고 OQ-006 schema lineage는 [ADR-0016](../../adr/0016-schema-lineage-and-projection-ownership.md)로
  resolved됐다. OQ-001 runtime follow-up은 아직 pending이다.
- **Research owner:** Codex review

이 packet은 fixture-local canonical JSON profile을 관찰하고, 명시적인 AUTOPILOT delegated
decision gate를 통과한 뒤 C-01의 제품 방향을 ADR-0017로 채택한다. cross-runtime edge
규칙과 production serializer 구현은 여전히 후속 evidence 범위다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | Versioned semantic projection + canonical JSON | digest 대상 field를 명시적으로 projection하고 UTF-8 canonical JSON bytes를 SHA-256한다. object key order와 editorial Markdown body는 제외하고 array order는 보존한다. | cross-language serializer profile, number/Unicode rules와 version migration을 별도로 고정한다. | `observed` fixture-local vector; exact product profile `unverified` |
| C-02 | Canonicalized YAML/frontmatter | Markdown frontmatter를 normalized YAML로 serialize한 뒤 hash한다. 사람이 읽는 표현과 가깝다. | YAML parser, scalar/anchor/duplicate-key/ordering semantics가 모든 host에서 동일하다. | `inferred` — 별도 runner 미실행 |
| C-03 | Raw Markdown/frontmatter bytes | 파일의 canonical byte stream을 그대로 hash한다. 구현은 단순하고 artifact integrity를 직접 나타낸다. | editorial whitespace, key order와 formatting 변경도 semantic invalidation으로 허용한다. | `observed` negative control — raw hashes differ on editorial change |

## 3. Trade-off matrix

| criterion | C-01 semantic canonical JSON | C-02 canonical YAML | C-03 raw bytes | evidence/source refs |
| --- | --- | --- | --- | --- |
| key ordering | reordered contract/plan payload가 같은 digest를 냈다. `observed` | parser/serializer의 key order policy를 추가로 고정해야 한다. `inferred` | byte order가 달라져 digest가 달라진다. `observed` | F-001, A-001 |
| editorial change | body를 semantic payload 밖에 두면 digest unchanged 관찰이 가능하다. `observed` fixture profile | YAML comments/quotes/line breaks와 body 경계를 정해야 한다. `inferred` | editorial variant raw digest가 달라졌다. `observed` | F-001, A-001, S-001 |
| semantic invalidation | contract/plan semantic change가 각각 다른 digest를 냈다. downstream stale rule을 표현할 수 있다. `observed` | semantics와 serialization ambiguity를 함께 관리해야 한다. `inferred` | 모든 byte change를 invalidation으로 처리해 false invalidation 위험이 있다. `inferred` | F-001, A-001, S-002 |
| cross-runtime stability | explicit version/profile과 golden vectors가 필요하다. `inferred` | YAML implementation/version drift 위험이 높다. `inferred` | 모든 host에서 bytes만 같으면 된다. `inferred` | S-003/S-004 |
| auditability / migration | digest 대상 projection, serializer version, old/new digest를 event에 남길 수 있다. `inferred` | YAML schema migration과 parser behavior를 함께 기록해야 한다. `inferred` | 의미 없는 editorial history도 semantic change처럼 보인다. `inferred` | S-001, S-005 |
| implementation risk | restricted JSON vector는 작지만 numeric/Unicode edge가 아직 미검증이다. `observed limitation` | full YAML canonicalization이 복잡하다. `inferred` | 가장 낮지만 contract authoring UX와 stale plan 비용이 크다. `inferred` | S-002, S-006 |

## 4. Sources

모든 source는 repository-local canonical 문서이며 외부 코드·문구를 복사하지 않았다.
`pinned ref`는 조사 기준 commit `176e9375c0ad51614ce12f4bae7aa00c0130b5dd`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/06_SPECIFICATION.md#6-contract-digest와-approval` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | digest 대상이 goal/non-goals/constraints/context/AC/execution policy이고 status/timestamp/run result는 제외된다는 current proposal을 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | `docs/02_TASK_LIFECYCLE.md#6-invalidation` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | semantic contract change가 approval/plan/run을 stale로 만든다는 invalidation 방향과 editorial canonicalization TBD를 확인했다. | Local project document; no external reuse. |
| S-003 | `local-doc` | `docs/adr/0007-v1-contract-and-verification-artifacts.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | contract schema와 profile/retry policy digest invalidation, schema parse/serialize golden test 필요성을 확인했다. | Accepted local ADR; no external reuse. |
| S-004 | `local-doc` | `docs/PLAN.md#12-1-승인-digest` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | semantic projection SHA-256과 approval/downstream invalidation의 계획 방향을 확인했다. | Local project plan; no external reuse. |
| S-005 | `local-doc` | `docs/01_ARCHITECTURE.md#6-canonical-state와-projection` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | digest/revision과 document/DB reconciliation이 canonical state 경계의 일부임을 확인했다. | Local project document; no external reuse. |
| S-006 | `local-doc` | `docs/research/phase-0/DECISION_PACKET_TEMPLATE.md` | `176e9375c0ad51614ce12f4bae7aa00c0130b5dd` | 2026-08-21 | golden vector, exact command, artifact hash와 user decision receipt를 분리 기록하는 packet 규칙을 확인했다. | Local research convention; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | contract/plan semantic projection과 raw Markdown negative control의 digest vector 비교 | deterministic base/reordered/semantic-changed payload와 editorial Markdown variants | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | contract/plan key reorder same, semantic change different, raw editorial change different, golden hashes match | temporary Git/SQLite와 raw stdout만 폐기; vector/result는 packet에 보존 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ007-001` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-21T00:49:56Z / 2026-08-21T00:49:57Z | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 30/30 assertions와 contract/plan golden vector | A-001, A-002, A-003 |
| `RUN-OQ007-002` | `FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` | 2026-08-22T15:02:35Z / 2026-08-22T15:02:35Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — current revalidation, paired stdout byte-identical | A-004 |

### 5.3 Golden vector and observed invalidation

Fixture-local algorithm is `fixture.canonical-json-v1`: semantic payload를 UTF-8 JSON으로
`sort_keys=true`, compact separators와 `allow_nan=false`로 serialize하고 SHA-256한다. 이는
제품 serializer 또는 RFC/JCS compatibility 선택이 아니다.

| vector | digest | expected relation |
| --- | --- | --- |
| contract base | `sha256:e33553ac8e334a18186c49a081e9abddd26b77409ded3949cad3072b5a541128` | golden |
| contract reordered object keys | `sha256:e33553ac8e334a18186c49a081e9abddd26b77409ded3949cad3072b5a541128` | equal to base |
| contract semantic goal change | `sha256:7d308ef3c880e5b8602aafa7d64f95f34d19869c219c76765b9542c3a445a269` | different; contract/plan stale candidate |
| plan base | `sha256:e729ee145de2d0df63d1b28f7c6a53b8b4da43538684198ff41f70111b9fcd4a` | golden |
| plan reordered object keys | `sha256:e729ee145de2d0df63d1b28f7c6a53b8b4da43538684198ff41f70111b9fcd4a` | equal to base |
| plan semantic step addition | `sha256:c568f7bcd04147c2311251477f158cda4a5dcc7a2100426a764ff481d5079dab` | different |
| raw Markdown editorial variant | `sha256:1776b4a9ba9c9819b84dc79d981320f029da6908658d145a39756678ea2c6a47` | differs from raw base `sha256:8220efeb9e505d5d0e7501ec1808bec545ed7bd8f2f341ac1337239b8c58af99` |

The fixture observed the candidate policy `editorial_change → digest unchanged under semantic
projection` and `contract semantic change → contract and downstream plan stale`. These
observations support the adopted C-01 direction; the exact cross-runtime edge profile remains
an implementation evidence gate.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | redacted result manifest | `docs/research/phase-0/evidence/OQ-007/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-001/result.json` | `RUN-OQ007-001` | recorded after final validation | `packet` | golden vector and invalidation observation |
| A-002 | fixture runner | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | fixture definition | recorded after final validation | `tracked` | deterministic serializer probe |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json` | fixture definition | recorded after final validation | `tracked` | base/reordered/semantic payloads |
| A-004 | redacted rerun result | `docs/research/phase-0/evidence/OQ-007/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-002/result.json` | `RUN-OQ007-002` | same manifest; parsed outputs equal | `packet` | repeatability |
| A-005 | raw stdout/temp state | temporary per-run state | `RUN-OQ007-001/002` | discarded after redaction | `discarded` | raw execution only |

Additional validation commands:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` | `0` | runner parses successfully |
| `python3 -m json.tool docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json >/dev/null` | `0` | input is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-007/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-001/result.json >/dev/null` | `0` | historical evidence is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-007/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-002/result.json >/dev/null` | `0` | current evidence is valid JSON |
| `cmp` of paired current fixture stdout | `0` | deterministic replay output is byte-identical |
| `jq` assertion summary on current fixture output | `0` | `true`, `30`, `30`, `disabled`, `false` |
| `git diff --check --` | `0` | no whitespace error after final edit |
| read-only Node Markdown local-link/fence check | `0` | `markdown_files=57`, `local_links=147`, `fence_delimiters=122`, `trailing_whitespace=0`, `errors=[]` |

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | fixture serializer is a restricted Python JSON profile, not a cross-language canonicalization contract. | `high` | number representation, Unicode normalization, escaping, duplicate keys, NaN/Infinity, large values와 other runtime parity가 미확인이다. | user-selected runtime에서 language-independent golden vector와 versioned serializer test를 실행한다. | user / Phase 1 | `open` |
| R-002 | editorial/semantic classification was exercised on a small synthetic payload. | `medium` | all frontmatter/body fields와 nested schema changes의 classification이 미확인이다. | OQ-006 schema decision 뒤 field-level canonical projection matrix를 추가한다. | user | `open` |
| R-003 | downstream stale observation is a fixture label, not a production state transaction. | `high` | plan/run/approval invalidation ordering과 crash reconciliation이 미관찰이다. | selected runtime + OQ-009 completion/recovery fixture로 검증한다. | user | `open` |
| R-004 | profile version migration and old digest handling remain unimplemented. | `medium` | hash agility, old digest migration과 backward compatibility가 미결정이다. | ADR-0017 records the profile boundary; Phase 1 defines upgrade/invalid-digest behavior and evidence. | user / Phase 1 | `open` |

## 8. Decision

- **Packet decision status:** `resolved`
- **Recommendation:** C-01 — digest는 raw Markdown이 아니라 versioned semantic projection에
  적용하고, canonical serializer와 hash algorithm/version을 명시한 golden vector를 계약으로
  둔다. fixture 결과는 key ordering과 editorial body를 semantic payload에서 분리할 때 stable
  digest와 semantic invalidation을 얻는다는 관찰을 제공한다.
- **Rationale:** contract/plan payload의 object key reordering은 각각 같은 digest를 냈고,
  semantic goal/step change는 서로 다른 digest를 냈다. raw Markdown negative control은
  editorial line 하나에도 hash가 달라졌다. 이는 `docs/06_SPECIFICATION.md`, Lifecycle
  invalidation과 ADR-0007의 current direction을 지지한다.
- **Rejected/deferred candidates:** C-02는 YAML parser/serialization ambiguity, C-03은
  editorial false invalidation 때문에 deferred. C-01의 exact cross-runtime serializer profile,
  numeric/Unicode rules와 migration behavior는 후속 implementation evidence로 남긴다.
- **Unresolved impact:** production serializer, edge-case vector, migration과 stale evidence
  freshness enforcement는 제품 schema와 implementation 전에 별도 검증해야 한다.

### User/authority decision receipt

- **Decision:** C-01 — versioned semantic projection + canonical JSON profile, SHA-256
- **Actor:** `user-delegated-autonomous-delivery` under the explicit AUTOPILOT delegation
- **Recorded at:** `2026-08-22T15:02:35Z`
- **Reference:** [USER-DECISION-OQ007-001](./evidence/OQ-007/USER-DECISION-RECEIPT-001.md), [ADR-0017](../../adr/0017-versioned-semantic-digest.md)
- **Supersedes:** `none`

## 9. Next verifiable goal

다음 목표는 OQ-010 lesson evaluator recommendation을 같은 delegated-decision evidence gate로
재검증하는 것이다. OQ-008은 fixture가 `selected_candidate=null`을 반환한 별도 user-decision
blocker로 유지한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] 세 canonicalization 후보와 미실행 범위가 기록됐다.
- [x] trade-off가 source/fixture evidence에 연결됐다.
- [x] golden vector와 editorial/semantic invalidation observation이 기록됐다.
- [x] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행 command, exit status, artifact와 raw redaction이 기록됐다.
- [x] cross-runtime/edge-case limitation과 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] 제품 serializer의 미검증 edge case와 implementation 범위를 명시적으로 남겼다.
- [x] 최종 `git diff --check --`와 JSON/Markdown 검증 결과가 기록된다.
