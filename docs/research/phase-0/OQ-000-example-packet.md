---
packet_schema_version: 1
packet_id: "OQ-000-example"
question_id: "OQ-000-example"
title: "Packet 표준 self-check 예시"
status: "example"
owner: "docs"
decision_authority: "none (format example)"
opened_at: "2026-08-20T00:00:00Z"
updated_at: "2026-08-20T00:00:00Z"
---

# OQ-000-example — Packet 표준 self-check 예시

> 이 파일은 실제 blocking OQ가 아니다. template의 모든 필드와 fixture 실행 기록을
> 검토하기 위한 예시이며 Open Questions의 `Resolved` 표를 변경하지 않는다.

## 1. Scope and authority

- **Question:** packet이 후보 비교와 fixture evidence를 같은 구조로 기록하는가?
- **Phase/Gate:** Phase 0 / packet format self-check
- **Decision authority:** none; example only
- **Allowed scope:** 이 문서와 연결된 작은 read-only fixture의 구조 확인
- **Non-goals:** Controller 언어, 제품 schema, runtime과 host 계약 결정
- **Dependencies:** `none`
- **Research owner:** docs

## 2. Candidates [required]

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | prose-only note | 섹션 구분 없이 조사 결론만 기록 | 작성자가 필요한 사실을 기억한다고 가정 | `observed` (형식상 한계) |
| C-02 | structured packet | 후보·trade-off·source·fixture·artifact·risk·decision을 고정 섹션으로 기록 | 작성자가 실행 결과를 실제로 채운다고 가정 | `observed` (이 예시로 확인) |

## 3. Trade-off matrix [required]

| criterion | C-01 | C-02 | evidence/source refs |
| --- | --- | --- | --- |
| 필수 field 누락 탐지 | 어렵다 | checklist로 확인 가능 | S-001, A-001 |
| 후보 비교 재현성 | 낮다 | 동일 table 구조로 비교 가능 | S-001, F-001 |
| 결정과 관찰 분리 | 결론에 섞이기 쉽다 | decision receipt를 별도 기록 | S-002 |

## 4. Sources [required]

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | `docs/PLAN.md#phase-0-핵심-계약과-adr-확정` | `2eea353` | 2026-08-20 | Phase 0 packet은 candidate, trade-off, source, command, exit status, artifact, risk와 결정 근거를 가져야 한다. | repository-internal; no reuse |
| S-002 | `local-doc` | `docs/research/REFERENCE_POLICY.md` | `2eea353` | 2026-08-20 | 관찰·설계 영향·표현물 재사용을 구분하고 고정 source를 기록한다. | repository-internal; no reuse |

## 5. Fixture catalog and execution [required]

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| FX-PACKET-SELF-CHECK-001 | tracked Markdown의 whitespace 오류를 찾는 read-only check | current repository, no input file | `git` | command가 오류 없이 끝나고 exit `0` | command result만 기록; Git 상태 변경 없음 |

### 5.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-OQ000-001 | FX-PACKET-SELF-CHECK-001 | 2026-08-20T11:42:45Z / 2026-08-20T11:42:45Z | repository root | `git diff --check --` | `0` | `pass` — stdout/stderr empty; whitespace error 없음 | A-001 |

추가 실행 환경:

- **Tool/runtime versions:** `git version 2.49.0`
- **Environment overrides:** none
- **Network/external writes:** disabled; read-only Git check
- **Redaction:** output empty; redaction not required

## 6. Artifacts and evidence [required]

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | redacted result | `docs/research/phase-0/evidence/OQ-000-example/FX-PACKET-SELF-CHECK-001/RUN-OQ000-001.md` | RUN-OQ000-001 | `sha256:31b9050dcfb34911868687831d80f4794d21350b670692e7c1b95f51c85c5b51` | `packet` | `git diff --check --`가 오류 없이 종료했다는 관찰 |

raw stdout/stderr는 비어 있어 보존하지 않는다. 위 evidence file은 exit status와 관찰을
작게 요약한 redacted record다.

## 7. Risks and limitations [required]

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | self-check는 문서 field 존재와 whitespace만 검사하며 semantic packet 품질을 보장하지 않는다. | `medium` | 실제 OQ packet 작성 시 누락·오해 가능성 | 첫 실제 OQ packet에서 checklist와 source/fixture 연결을 재검토 | docs | `open` |
| R-002 | 이 예시는 사용자 결정 receipt를 포함하지 않는다. | `low` | normative decision 없음 | 실제 OQ packet은 authority receipt가 없으면 `needs-user-decision` 유지 | docs | `mitigated` |

## 8. Decision [required]

- **Packet decision status:** `recommendation`
- **Recommendation:** C-02를 packet 표준의 예시 구조로 사용한다.
- **Rationale:** required field, fixture execution, exit status, artifact와 risk를 별도
  row로 연결해 관찰과 권고를 분리할 수 있다.
- **Rejected/deferred candidates:** C-01은 field와 evidence 연결을 안정적으로 검사할
  수 없어 예시 표준으로 선택하지 않는다. 이 판단은 제품 계약을 결정하지 않는다.
- **Unresolved impact:** 실제 OQ의 authority와 trade-off 기준은 각 질문별로 채워야 한다.

### User/authority decision receipt

- **Decision:** `not-applicable — example only`
- **Actor:** `none`
- **Recorded at:** `not-applicable`
- **Reference:** `P0-01 format example`
- **Supersedes:** `none`

## 9. Next verifiable goal

- 실제 첫 OQ packet을 이 구조로 작성하고, 해당 OQ의 authority가 recommendation을
  채택·거절했는지 별도 receipt로 확인한다.

## 10. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal이 명확하다.
- [x] candidate와 동일 기준의 trade-off가 source/fixture evidence에 연결됐다.
- [x] source locator, pinned ref, accessed date와 license/action이 있다.
- [x] exact command와 실제 exit status를 execution record에 적었다.
- [x] artifact locator와 retention이 있다.
- [x] risk/limitation과 evidence gap, next check가 있다.
- [x] decision status가 example-only authority와 일치한다.
- [x] 제품 scaffold와 target/home state를 변경하지 않는 fixture다.
