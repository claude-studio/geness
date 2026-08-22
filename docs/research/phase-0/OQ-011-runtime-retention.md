---
packet_schema_version: 1
packet_id: "OQ-011"
question_id: "OQ-011"
title: "runtime/evidence 보존 기간과 용량 제한"
status: "decision-ready"
owner: "Codex review / Phase 0 research"
decision_authority: "user"
opened_at: "2026-08-21T05:41:00Z"
updated_at: "2026-08-21T05:41:00Z"
---

# OQ-011 — runtime/evidence 보존 기간과 용량 제한

## 1. Scope and authority

- **Question:** runtime state와 evidence를 task 상태·위험도·용량에 따라 언제 보존·prune하고,
  memory event와 미초기화/손상 memory를 어떤 typed result로 노출할 것인가?
- **Phase/Gate:** Phase 0 / OQ-011 decision packet
- **Decision authority:** 사용자
- **Allowed scope:** active/blocked/completed runtime와 evidence의 retention candidate, risk/size
  guard, memory store 분리, missing/empty/available/unavailable bootstrap result와 Phase 3 Gate 후보
- **Non-goals:** production scheduler/cleanup worker, exact SQLite schema, backup/restore implementation,
  secret redaction implementation, user-facing prune command, product bootstrap 구현과 user decision receipt
  확정
- **Dependencies:** P0-05 #17 `closed/status:done`; [ADR-0002](../../adr/0002-project-and-local-state-boundary.md),
  [ADR-0003](../../adr/0003-failure-candidate-is-not-memory.md), OQ-006 schema owner는
  [ADR-0016](../../adr/0016-schema-lineage-and-projection-ownership.md)로 resolved됐고
  OQ-010은 [ADR-0018](../../adr/0018-deterministic-lesson-evaluator.md)과
  [delegated decision receipt](./evidence/OQ-010/USER-DECISION-RECEIPT-001.md)로 resolved됐다.
- **Research owner:** Codex review

이 packet은 `~/.geness/runtime/`과 `~/.geness/memory/`의 accepted boundary를 관찰 가능한
retention/bootstrap 후보로 구체화한다. fixture의 TTL·size·Gate mapping은 비교용 candidate이며,
사용자 선택 전 Storage ADR·Phase 3 contract·Implementation `CLEAR`를 만들지 않는다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | state/risk/capacity tiered retention + typed capability result | active/blocked runtime은 자동 삭제하지 않고, completed low-risk는 TTL/size candidate로 prune하며, high-risk는 explicit disposition 전 보존한다. memory event/lesson은 runtime prune과 분리한다. missing/empty는 명시적 no-memory `CLEAR`, corrupt/unavailable은 `HOLD`와 rebuild/repair action을 반환한다. | risk classification, evidence lineage, explicit disposition actor와 rebuild path가 저장된다. | `observed` fixture profile + `inferred` recommendation |
| C-02 | fixed TTL / missing-as-empty | 모든 runtime/evidence에 동일 TTL을 적용하고 missing·empty·corrupt를 모두 empty로 취급해 계속 진행한다. | task 상태·위험도·memory integrity가 retention decision에 영향을 주지 않는다. | `unverified` — negative behavior는 inference |
| C-03 | no automatic prune / bootstrap hard precondition | runtime/evidence를 자동 prune하지 않고 memory가 ready가 될 때까지 Phase 3를 HOLD한다. | 디스크 증가를 사용자가 항상 직접 관리하고 Phase 5가 Phase 3보다 먼저 준비된다. | `unverified` — negative behavior는 inference |

## 3. Trade-off matrix

| criterion | C-01 tiered | C-02 fixed TTL/collapse | C-03 no prune/hard precondition | evidence/source refs |
| --- | --- | --- | --- | --- |
| active/blocked 안전성 | 365일·500KB 합성 항목도 `KEEP`로 관찰됐다. | 오래 실행 중인 작업과 blocker evidence를 TTL이 삭제할 수 있다. | 보존은 되지만 용량 증가가 무제한이다. | F-001, A-004, S-001 |
| completed retention | low-risk 항목은 30일 초과 또는 100KB 초과에서 `PRUNE` 후보가 되고 high-risk no-disposition은 `KEEP`였다. | 상태·위험도·size가 무시되어 중요한 evidence와 저위험 기록을 구분하지 못한다. | user cleanup 없이는 runtime/evidence가 계속 누적된다. | F-001, A-004, S-001/S-002 |
| memory와 runtime 경계 | 오래되고 큰 verified memory item은 `KEEP`이며 runtime prune 대상이 아니었다. | runtime cleanup이 memory history까지 건드릴 위험이 있다. | 분리는 가능하지만 rebuild/index 비용을 별도 관리해야 한다. | F-001, A-004, S-003 |
| missing/empty bootstrap | `UNINITIALIZED`와 `EMPTY`를 구분하고 둘 다 명시적 `CLEAR`/continue 결과를 반환한다. | corrupt까지 empty로 합쳐 memory loss를 숨길 수 있다. | 초기 memory가 없으면 Phase 3가 Phase 5에 강하게 결합된다. | F-001, A-004, S-004 |
| corrupt/unavailable safety | `UNAVAILABLE`/`HOLD`/`rebuild_or_repair`로 query를 실행하지 않았다. | 손상 index를 empty로 처리해 관련 lesson이 없는 것처럼 오판할 수 있다. | 안전하지만 정상적인 empty repository도 막을 수 있다. | F-001, A-004, S-005 |
| 운영·복구 비용 | risk/size classification, disposition audit와 prune/rebuild path가 필요하다. | 구현은 단순하지만 false deletion과 hidden degradation 위험이 크다. | cleanup·bootstrap 모두 사용자 수동 부담이 크다. | S-001–S-006 |

수치(30일, 100KB)와 `CLEAR`/`HOLD` mapping은 이 fixture의 C-01 candidate 값이다. 이는
retention 또는 Phase 3 contract를 확정하지 않는다.

## 4. Sources

모든 source는 repository-local canonical 문서이며 외부 코드·문구를 복사하지 않았다. local
source의 pinned ref는 조사 기준 commit `45d9829abed62a4213962485bf616bc4402624e9`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | [`docs/03_STORAGE.md`](../../03_STORAGE.md#9-retention) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | active/blocked runtime 자동 삭제 금지, completed runtime TTL/용량 제한, memory/runtime 분리 방향을 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | [`docs/03_STORAGE.md`](../../03_STORAGE.md#6-runtime-sqlite-역할) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | runtime에 evidence metadata·failure event·lesson candidate가 있고 원본 evidence는 파일 경계에 있다는 사실을 확인했다. | Local project document; no external reuse. |
| S-003 | `local-doc` | [`ADR-0002`](../../adr/0002-project-and-local-state-boundary.md) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | target portable documents와 home runtime/memory의 ownership 분리를 확인했다. | Accepted local ADR; no external reuse. |
| S-004 | `local-doc` | [`docs/PLAN.md`](../../PLAN.md#phase-3-plan) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | Phase 3가 Phase 5 memory 구현을 숨은 entry condition으로 요구하지 않고 explicit bootstrap Gate를 사용해야 함을 확인했다. | Local project plan; no external reuse. |
| S-005 | `local-doc` | [`docs/01_ARCHITECTURE.md`](../../01_ARCHITECTURE.md#9-architecture-invariants) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | memory index 손상 시 retrieval을 `BLOCKED` 또는 degraded mode로 명시해야 하며 runtime cleanup이 memory를 삭제하면 안 된다는 invariant를 확인했다. | Local project document; no external reuse. |
| S-006 | `local-doc` | [`FIXTURE_RULES.md`](./FIXTURE_RULES.md) | `45d9829abed62a4213962485bf616bc4402624e9` | 2026-08-21 | retention fixture는 합성 입력, per-run 격리, raw output redaction과 artifact hash를 가져야 함을 확인했다. | Research convention; no external reuse. |

## 5. Fixture catalog and execution

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-MEMORY-RETENTION-BOOTSTRAP-001` | state/risk/size prune와 memory bootstrap capability를 event replay와 함께 관찰 | `input/fixture.json`의 synthetic retention/bootstrap cases와 same-run replay events | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | active/blocked/memory 보존, completed TTL/size prune, typed missing/empty/ready/corrupt result, 2-run equality | input/runner만 tracked; raw output과 temporary execution state는 보존하지 않음 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RUN-OQ011-001` | `FX-MEMORY-RETENTION-BOOTSTRAP-001` | 2026-08-21T05:40:30Z / 2026-08-21T05:40:37Z | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 43/43 assertions, retention/bootstrap observations 생성 | A-001, A-002, A-003, A-004 |
| `RUN-OQ011-002` | `FX-MEMORY-RETENTION-BOOTSTRAP-001` | 2026-08-21T05:40:41Z / 2026-08-21T05:40:48Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 43/43 assertions, parsed output equality-equivalent | A-004 |

추가 실행 환경:

- **Tool/runtime versions:** Python `3.14.5`, Git `2.53.0`, Darwin `25.4.0 arm64`
- **Environment overrides:** `PYTHONDONTWRITEBYTECODE=1`; `GENESS_HOME` override 없음, 실제 home 미사용
- **Network/external writes:** network `disabled`, external writes `false`
- **Redaction:** stdout 전체는 packet에 보존하지 않고 합성 case ID·action·typed result·hash만 redacted manifest로 보존

### 5.3 Observed result

- active/blocked runtime은 365일·500KB 합성 case에서도 각각 `KEEP`였다.
- completed low-risk case는 age `31 > 30`일에서 TTL prune, age 1일·size `120000 > 100000`에서
  size prune으로 관찰됐다. completed high-risk no-disposition case는 `KEEP`였다.
- memory의 오래되고 큰 verified lesson은 `memory_store_separate` 이유로 `KEEP`였고 runtime
  prune 목록에 들어가지 않았다.
- bootstrap result contract는 `fixture.memory-capability-result-v1`이며, missing=`UNINITIALIZED`,
  empty=`EMPTY`, ready=`AVAILABLE`, corrupt=`UNAVAILABLE`을 구분했다. missing/empty/ready는
  fixture-local `CLEAR`/continue, corrupt는 `HOLD`/`rebuild_or_repair`를 반환했다.
- 위 Gate mapping과 숫자는 C-01 candidate observation이며 Storage ADR 또는 Phase 3 contract가 아니다.

## 6. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | fixture README | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/README.md` | fixture definition | `14f8097945d11a57638cc0074e426bbb9f46007eb259e3f05d7fe85fc130f817` | `tracked` | isolation, expected retention/bootstrap observations |
| A-002 | fixture runner | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/runner.py` | fixture definition | `9706fbe1615baab6c184c84ff8b826f282b8cf17bc624ced8d6846eea5552c86` | `tracked` | prune simulation, typed result and replay assertions |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/input/fixture.json` | fixture definition | `a8f292a84d629b342b7ec3d2e1cf21520788a7c81cef6cf4e46ad12e013ae4cb` | `tracked` | state/risk/size/bootstrap cases |
| A-004 | redacted result manifest | `docs/research/phase-0/evidence/OQ-011/FX-MEMORY-RETENTION-BOOTSTRAP-001/RUN-OQ011-001/result.json` | `RUN-OQ011-001/002` | `7f67e265b5f813b566c8f04c53d75b7b48fd33d54622662b74f4b4b81779a267` | `packet` | 43 assertions, retention and bootstrap observations |
| A-005 | raw stdout/temp state | per-run process output | `RUN-OQ011-001/002` | discarded after summary; fixture creates no persistent state | `discarded` | raw execution only |

Additional validation records:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/runner.py` | `0` | runner parses successfully |
| `python3 -m json.tool docs/research/phase-0/fixtures/FX-MEMORY-RETENTION-BOOTSTRAP-001/input/fixture.json >/dev/null` | `0` | deterministic input is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-011/FX-MEMORY-RETENTION-BOOTSTRAP-001/RUN-OQ011-001/result.json >/dev/null` | `0` | redacted evidence is valid JSON |
| `git diff --check --` | `0` | no whitespace error after final packet/fixture/evidence edits |
| `node /tmp/geness-p0-06-markdown-check.mjs` | `0` | `markdown_files=64`, `local_links=185`, `local_anchor_links=15`, `fence_delimiters=152`, `trailing_whitespace=0`, `errors=[]` |

## 7. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | active/blocked 보존은 안전하지만 장기 실행·대용량 evidence가 용량을 무제한으로 늘릴 수 있다. | `high` | global/project budget, operator alert와 explicit cleanup UX가 미관찰이다. | 사용자에게 state/risk/size policy와 manual prune authority를 선택받고 capacity fixture를 확장한다. | user | `open` |
| R-002 | 30일/100KB와 high-risk disposition rule은 synthetic candidate 값이다. | `high` | 실제 보존 의무, 감사·복구 요구와 task별 위험 분류가 미확인이다. | Storage ADR에서 retention class, backup/restore와 policy version을 결정한다. | user | `open` |
| R-003 | evidence blob 자체의 lineage/freshness와 runtime cleanup 후 verifier 동작을 replay하지 않았다. | `high` | AC evidence가 prune된 뒤 verdict를 재구성하는 경로가 미관찰이다. | OQ-006/OQ-009 및 Phase 4 crash/reconciliation fixture로 검증한다. | user / Phase 4 | `open` |
| R-004 | memory index corruption은 typed HOLD로만 관찰했고 rebuild 성공·degraded retrieval을 실행하지 않았다. | `high` | JSONL rebuild, FTS capability fallback과 recovery cost가 미확인이다. | Phase 5/6 rebuild fixture와 user choice(`HOLD` vs degraded)를 추가한다. | user / Phase 5 | `open` |
| R-005 | missing/empty를 `CLEAR`로 두는 mapping은 fixture-local candidate라 Phase 3 UX 영향이 미결정이다. | `high` | memory 없는 task에서 사용자 기대와 plan Gate wording이 미확인이다. | 사용자 결정 후 bootstrap contract와 Phase 3 Gate 문서에 반영한다. | user | `open` |
| R-006 | fixture는 single-process이며 concurrent prune/memory writer race를 다루지 않는다. | `medium` | one-writer, crash 중복 prune와 event/index atomicity가 미관찰이다. | OQ-003/OQ-009와 Phase 5 race/crash fixture로 보강한다. | user / Phase 5 | `open` |

## 8. Decision

- **Packet decision status:** `needs-user-decision`
- **Recommendation:** C-01 — runtime retention은 state·risk·capacity를 분리해 평가하고, active/blocked
  작업은 자동 삭제하지 않으며 completed low-risk만 versioned TTL/size candidate로 prune한다.
  high-risk evidence는 explicit disposition 전 보존하고, memory event/lesson은 runtime cleanup과
  분리한다. bootstrap은 missing/empty/available/unavailable을 typed result로 구분하며, fixture의
  추천 mapping은 missing/empty/available=`CLEAR`/continue, unavailable=`HOLD`/rebuild_or_repair다.
- **Rationale:** 동일 replay에서 active/blocked와 memory store가 prune되지 않고 low-risk completed만
  TTL/size 조건을 만족했으며, corrupt memory를 empty로 숨기지 않는 typed result가 관찰됐다. 이는
  [ADR-0002](../../adr/0002-project-and-local-state-boundary.md)의 storage boundary와
  [docs/03_STORAGE.md](../../03_STORAGE.md)의 runtime/memory 분리를 유지한다.
- **Rejected/deferred candidates:** C-02는 active/blocker evidence 삭제와 corrupt-as-empty 위험으로
  deferred한다. C-03은 용량 무한 증가와 Phase 3→Phase 5 강결합 때문에 deferred한다. 사용자 결정
  전에는 어느 retention/bootstrapping mapping도 채택하지 않는다.
- **Unresolved impact:** exact retention classes, TTL/size limits, high-risk authority, backup/restore,
  prune audit, evidence freshness와 unavailable degraded-mode가 닫히지 않으면 Storage ADR 및
  Phase 3/5 implementation contract를 확정할 수 없다.

### User/authority decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
- **Supersedes:** `none`

## 9. Next verifiable goal

사용자가 C-01/C-02/C-03 retention 및 bootstrap mapping을 선택하고, 선택 결과를 Storage ADR와
Phase 3 memory capability Gate에 기록한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] 세 candidate와 assumptions/evidence status가 기록됐다.
- [x] retention/bootstrap trade-off가 source/fixture evidence에 연결됐다.
- [x] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행 command, exit status, artifact와 raw redaction이 기록됐다.
- [x] 실행하지 않은 scheduler/rebuild/race fixture는 risk와 deferred로 분리했다.
- [x] artifact path, hash와 retention이 있다.
- [x] risk/limitation과 evidence gap, owner와 next check가 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] secret/raw log/대용량 output이 packet에 없다.
- [x] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [x] 최종 `git diff --check --`와 Markdown 검증 결과가 기록됐다.
