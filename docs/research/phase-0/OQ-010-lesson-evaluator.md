---
packet_schema_version: 1
packet_id: "OQ-010"
question_id: "OQ-010"
title: "lesson fingerprint, 승격, 감쇠와 만료 threshold"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T05:41:00Z"
updated_at: "2026-08-21T05:41:00Z"
---

# OQ-010 — lesson fingerprint, 승격, 감쇠와 만료 threshold

## 1. Scope and authority

- **Question:** failure candidate를 어떤 fingerprint와 evidence 규칙으로 승격하고, 어떤
  eligible exposure·unassisted success·관찰 기간으로 감쇠·만료할 것인가?
- **Phase/Gate:** Phase 0 / OQ-010 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** deterministic lesson lifecycle candidate 비교, event replay, eligible exposure와
  unassisted success 구분, promotion/decay/expiry 후보 threshold, 일반 retrieval visibility
- **Non-goals:** production event/SQLite schema, FTS query algorithm, project writer arbitration,
  team export format, LLM prompt wording, 제품 evaluator 구현과 user decision receipt 확정
- **Dependencies:** P0-05 #17 `closed/status:done`; [ADR-0003](../../adr/0003-failure-candidate-is-not-memory.md),
  OQ-006/OQ-007의 schema·digest user decision은 pending
- **Research owner:** Codex review

이 packet은 [ADR-0003](../../adr/0003-failure-candidate-is-not-memory.md)의 accepted 원칙을
검증 가능한 후보로 좁히는 research다. fixture의 threshold와 transition은 candidate observation이며,
사용자 선택 전에는 Learning ADR·canonical evaluator·Implementation `CLEAR`를 만들지 않는다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | deterministic evidence-gated evaluator | 구조화 fingerprint를 병합하고, 독립 run 2회 evidence 또는 재현 가능한 guard evidence에서 `verified`, 실제 eligible unassisted success 3회와 최소 관찰 기간에서 candidate/probationary를 `expired`로 전환한다. 일반 retrieval은 `verified\|enforced`만 노출한다. | fingerprint와 independent run identity가 안정적으로 기록되고 evaluator/rule version을 함께 보존한다. | `observed` fixture profile + `inferred` recommendation |
| C-02 | weighted confidence / model-assisted evaluator | recurrence, similarity와 모델 confidence를 가중해 확률적으로 승격·감쇠한다. | 모델 version·confidence calibration과 동일 입력 결정성이 별도 보장된다. | `unverified` — fixture 미실행 |
| C-03 | eager promotion / no expiry | 첫 failure를 곧바로 memory로 주입하고 시간 또는 exposure에 따른 만료를 두지 않는다. | false positive와 context pollution을 허용한다. | `observed` negative control — accepted 원칙과 불일치 |

## 3. Trade-off matrix

| criterion | C-01 deterministic | C-02 weighted/model-assisted | C-03 eager/no expiry | evidence/source refs |
| --- | --- | --- | --- | --- |
| false positive 통제 | 첫 failure는 candidate로만 남고, one-off lesson은 retrieval에 노출되지 않았다. | calibration이 없으면 confidence drift를 설명하기 어렵다. | 모든 일회성 failure가 durable context가 된다. | F-001, A-004, S-001/S-002 |
| false negative와 승격 지연 | 독립 재발 2회 또는 guard evidence가 필요해 첫 재발 전에는 보수적이다. | 낮은 confidence가 반복 문제를 늦출 수 있고 모델 변경으로 결과가 달라질 수 있다. | 가장 빠르지만 잘못된 lesson을 제거할 경로가 없다. | F-001, A-004 |
| exposure·감쇠 auditability | eligible exposure만 evaluator 입력으로 남기고 injected/ineligible success를 분리했다. | feature와 model input lineage가 추가로 필요하다. | 감쇠 근거와 expiry event가 없다. | F-001, A-004, S-001 |
| 결정성·migration | fixture replay 두 결과가 equality-equivalent이고 evaluator version을 기록했다. | model/version/threshold migration이 추가된다. | 규칙은 단순하지만 잘못된 memory가 오래 남는다. | F-001, A-004, S-001 |
| 운영·검색 경계 | `verified\|enforced`만 query projection에 노출하고 candidate/expired는 숨겼다. | 모델 latency와 설명 가능성 비용이 있다. | memory pollution과 사용자 정리 비용이 높다. | F-001, A-004, S-002 |

수치(2회, 3회, 7일)는 이 fixture가 비교한 C-01 candidate의 입력값이다. 이 표와 결과는
사용자 승인 전의 recommendation이며 제품 threshold가 아니다.

## 4. Sources

모든 source는 repository-local canonical 문서이며 외부 코드·문구를 복사하지 않았다. local
source의 pinned ref는 조사 기준 commit `45d9829abed62a4213962485bf616bc4402624e9`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | [`docs/09_LEARNING.md`](../../09_LEARNING.md) sections 4–7 | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | candidate는 자동 주입하지 않고, eligible exposure·unassisted success·independent recurrence·guard evidence로 상태를 평가하며 초기 threshold를 제안한다. | Local project document; no external reuse. |
| S-002 | `local-doc` | [`ADR-0003`](../../adr/0003-failure-candidate-is-not-memory.md) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | failure candidate는 deterministic evaluator와 evidence 없이 durable memory가 되지 않으며 replay fixture가 검증 방법이다. | Accepted local ADR; no external reuse. |
| S-003 | `local-doc` | [`docs/08_VERIFICATION.md`](../../08_VERIFICATION.md#7-verification-후-lesson-event) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | verifier는 failure event와 lesson injection/eligible success를 별도로 기록해야 한다. | Local project document; no external reuse. |
| S-004 | `local-doc` | [`docs/03_STORAGE.md`](../../03_STORAGE.md#7-memory-sqlite-역할) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | memory index와 append-only event history, lifecycle counters와 evaluator version의 저장 경계를 확인했다. | Local project document; no external reuse. |
| S-005 | `local-doc` | [`docs/PLAN.md`](../../PLAN.md#phase-0-핵심-계약과-adr-확정) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | OQ-010의 최소 evidence가 event replay 기반 false-positive/negative와 promotion/decay/expiry 비교임을 확인했다. | Local project plan; no external reuse. |
| S-006 | `local-doc` | [`FIXTURE_RULES.md`](./FIXTURE_RULES.md) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | fixture가 제품 구현과 분리되고 current target/home·network·external write를 사용하지 않아야 함을 확인했다. | Research convention; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-MEMORY-RETENTION-BOOTSTRAP-001` | failure lifecycle, eligible exposure, retention와 bootstrap result를 한 deterministic replay에서 비교 | `input/fixture.json`의 synthetic events, retention cases와 bootstrap cases | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | 2-run projection equality, first failure hidden, recurrence/guard promotion, one-off expiry, eligible-only count, typed memory result | input/runner만 tracked; raw output과 temporary execution state는 보존하지 않음 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ010-001` | `FX-MEMORY-RETENTION-BOOTSTRAP-001` | 2026-08-21T05:40:30Z / 2026-08-21T05:40:37Z | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 43/43 assertions, replay projection과 bootstrap/retention observations 생성 | A-001, A-002, A-003, A-004 |
| `RUN-OQ010-002` | `FX-MEMORY-RETENTION-BOOTSTRAP-001` | 2026-08-21T05:40:41Z / 2026-08-21T05:40:48Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 43/43 assertions, parsed output equality-equivalent | A-004 |

추가 실행 환경:

- **Tool/runtime versions:** Python `3.14.5`, Git `2.53.0`, Darwin `25.4.0 arm64`
- **Environment overrides:** `PYTHONDONTWRITEBYTECODE=1`; `GENESS_HOME` override 없음, 실제 home 미사용
- **Network/external writes:** network `disabled`, external writes `false`
- **Redaction:** stdout 전체는 packet에 보존하지 않고 합성 ID·상태·hash만 redacted manifest로 보존

### 5.3 Observed result

- 13 synthetic events의 두 replay가 equality-equivalent했고 projection hash는
  `sha256:0e3e7e4ef2ae40c0b6e68673774afe7cc2d8b74a122fb38438d7ddf8371b2b07`였다.
- 첫 failure checkpoint의 visible lesson은 `[]`였다. `LESSON-REPEAT`는 동일 run 중복을 한 번으로
  세고 독립 `RUN-001`/`RUN-002`에서만 `verified`가 됐으며, `LESSON-GUARD`는 재현 가능한
  fail-before/pass-after evidence에서 `verified`가 됐다.
- `LESSON-ONEOFF`는 eligible exposure 4건 중 injected success 1건을 unassisted로 세지 않고,
  ineligible success 1건을 evaluator input에서 제외했으며, unassisted success 3건과 최소
  관찰 기간 뒤 `expired`가 됐다.
- final retrieval projection에는 `LESSON-GUARD`, `LESSON-REPEAT`만 남았다. 이는 C-01 fixture
  profile의 관찰이지 Learning ADR 채택 결과가 아니다.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | fixture README | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/README.md` | fixture definition | `14f8097945d11a57638cc0074e426bbb9f46007eb259e3f05d7fe85fc130f817` | `tracked` | isolation, expected observation, command |
| A-002 | fixture runner | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/runner.py` | fixture definition | `9706fbe1615baab6c184c84ff8b826f282b8cf17bc624ced8d6846eea5552c86` | `tracked` | replay, prune simulation, typed result assertions |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/input/fixture.json` | fixture definition | `a8f292a84d629b342b7ec3d2e1cf21520788a7c81cef6cf4e46ad12e013ae4cb` | `tracked` | deterministic events, policy candidate and cases |
| A-004 | redacted result manifest | `docs/research/phase-0/evidence/OQ-010/FX-MEMORY-RETENTION-BOOTSTRAP-001/RUN-OQ010-001/result.json` | `RUN-OQ010-001/002` | `7f67e265b5f813b566c8f04c53d75b7b48fd33d54622662b74f4b4b81779a267` | `packet` | 43 assertions, lifecycle/retention/bootstrap observations |
| A-005 | raw stdout/temp state | per-run process output | `RUN-OQ010-001/002` | discarded after summary; fixture creates no persistent state | `discarded` | raw execution only |

Additional validation records:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/runner.py` | `0` | runner parses successfully |
| `python3 -m json.tool docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/input/fixture.json >/dev/null` | `0` | deterministic input is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-010/FX-MEMORY-RETENTION-BOOTSTRAP-001/RUN-OQ010-001/result.json >/dev/null` | `0` | redacted evidence is valid JSON |
| `git diff --check --` | `0` | no whitespace error after final packet/fixture/evidence edits |
| `node /tmp/geness-p0-06-markdown-check.mjs` | `0` | `markdown_files=64`, `local_links=185`, `local_anchor_links=15`, `fence_delimiters=152`, `trailing_whitespace=0`, `errors=[]` |

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | C-01 threshold numbers are synthetic candidate inputs, not calibrated production values. | `high` | real task volume, false-positive/negative rates와 user tolerance가 관찰되지 않았다. | 사용자가 recurrence/guard/expiry policy를 선택하고 Learning ADR 및 production calibration plan을 기록한다. | user | `open` |
| R-002 | fixture fingerprint is pre-labeled and does not implement merge/split normalization. | `high` | project/module/symbol normalization, conflict resolution과 schema lineage가 미확인이다. | OQ-006/OQ-007 결정 후 fingerprint schema·digest fixture를 별도로 확장한다. | user / Phase 5 | `open` |
| R-003 | replay is single-process and does not test append/index crash recovery or concurrent memory writers. | `high` | JSONL→SQLite/FTS projection, writer arbitration과 evaluator migration이 미관찰이다. | OQ-011 및 Phase 5/7의 crash/rebuild/race fixture로 보강한다. | user / Phase 5 | `open` |
| R-004 | verified lesson의 decay/revocation과 compiled/enforced transition은 이 fixture 범위 밖이다. | `medium` | pin/reject/deprecate/supersede와 guard compilation semantics가 미확인이다. | 별도 Learning lifecycle fixture와 user management decision을 추가한다. | user / Phase 5 | `open` |
| R-005 | bootstrap result의 `CLEAR`/`HOLD` mapping은 fixture-local candidate다. | `high` | Phase 3 user experience와 corrupt index recovery cost가 미확인이다. | OQ-010/OQ-011 선택 결과를 bootstrap contract와 Phase 3 Gate에 반영한다. | user | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 — candidate는 일반 retrieval에서 격리하고, 구조화 fingerprint·independent
  recurrence 또는 reproducible guard evidence를 통해서만 promotion candidate가 되며, eligible
  unassisted success와 관찰 기간만 decay/expiry 입력으로 사용한다. fixture의 `2 / 3 / 7일`은
  사용자가 검토할 초기 후보값이다.
- **Rationale:** replay는 첫 failure가 노출되지 않고, 같은 run 중복과 unrelated/ineligible success가
  evaluator 입력에서 제외되며, injected success가 unassisted success로 오인되지 않음을 직접
  관찰했다. 또한 replay 결과가 동일해 deterministic evaluator와 versioned event lineage 후보를
  비교할 수 있다. 이는 ADR-0003의 candidate/memory 경계와 일치한다.
- **Rejected/deferred candidates:** C-03은 첫 failure를 memory로 만드는 accepted principle 위반
  위험 때문에 deferred/rejected control로 둔다. C-02는 calibration, model/version provenance와
  deterministic replay evidence가 없어 deferred한다. 사용자 결정 전 어느 후보도 채택하지 않는다.
- **Unresolved impact:** fingerprint schema, merge/split rule, exact thresholds, evaluator migration,
  verified lesson revocation과 project-scoped writer policy가 닫히지 않으면 Phase 5 구현을 시작할
  수 없다.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

사용자가 C-01/C-02와 fixture의 recurrence·unassisted-success·minimum-age 후보를 선택하고,
선택 결과를 Learning ADR 및 OQ-010 `Resolved` receipt로 기록한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] 세 candidate와 C-02의 미실행 범위가 기록됐다.
- [x] candidate와 동일 기준의 trade-off가 source/fixture evidence에 연결됐다.
- [x] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행 command, exit status, artifact와 raw redaction이 기록됐다.
- [x] 실행하지 않은 product evaluator/merge fixture는 risk와 deferred로 분리했다.
- [x] artifact path, hash와 retention이 있다.
- [x] risk/limitation과 evidence gap, owner와 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] secret/raw log/대용량 output이 packet에 없다.
- [x] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [x] 최종 `git diff --check --`와 Markdown 검증 결과가 기록됐다.
