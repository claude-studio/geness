# OQ-<번호> — <질문 제목>

아래 template을 복사해 `OQ-<번호>-<짧은-kebab-case>.md`로 저장한다. 대괄호 placeholder는
작성 전에 실제 값으로 바꾼다. 이 문서는 Research 기록이며, packet 자체가 제품 결정이나
사용자 승인을 의미하지 않는다.

~~~yaml
---
packet_schema_version: 1
packet_id: "OQ-<번호>"
question_id: "OQ-<번호>"
title: "<질문 제목>"
status: "draft | investigating | decision-ready | blocked | resolved"
owner: "<조사 owner>"
decision_authority: "user | named authority"
opened_at: "<RFC3339>"
updated_at: "<RFC3339>"
---
~~~

## 1. Scope and authority

- **Question:** [정확한 OQ 질문]
- **Phase/Gate:** [예: Phase 0 / decision packet]
- **Decision authority:** [누가 결정하는가]
- **Allowed scope:** [이 packet이 조사할 범위]
- **Non-goals:** [이번 packet에서 결정하지 않는 것]
- **Dependencies:** [선행 packet/issue 또는 `none`]
- **Research owner:** [담당자]

## 2. Candidates [required]

모든 현실적인 후보를 같은 기준으로 기록한다. 구현 편의로 후보 하나만 남기지 않는다.

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | [후보 이름] | [무엇을 선택하는가] | [필요한 가정] | `observed` / `inferred` / `unverified` |
| C-02 | [후보 이름] | [무엇을 선택하는가] | [필요한 가정] | `observed` / `inferred` / `unverified` |

## 3. Trade-off matrix [required]

비교 기준은 질문의 위험과 성공 조건에 연결한다. 숫자를 만들 수 없으면 정성 비교임을
명시하고 근거를 source·fixture로 연결한다.

| criterion | C-01 | C-02 | evidence/source refs |
| --- | --- | --- | --- |
| [기준 1] | [관찰] | [관찰] | [S-### / F-### / A-###] |
| [기준 2] | [관찰] | [관찰] | [S-### / F-### / A-###] |
| [위험·운영 비용] | [관찰] | [관찰] | [S-### / F-### / A-###] |

## 4. Sources [required]

외부 source는 [`REFERENCE_POLICY.md`](../REFERENCE_POLICY.md)에 따라 고정 commit·파일
permalink·조사일·라이선스를 남긴다. 로컬 문서는 repository와 commit을 적는다. source는
관찰의 근거이지 자동으로 Geness requirement가 아니다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` / `official` / `external` | [URL 또는 repository-relative path] | [commit/tag 또는 `not-applicable`] | [YYYY-MM-DD] | [확인한 사실] | [라이선스/고지 조치] |

## 5. Fixture catalog and execution [required]

fixture 정의와 실제 실행을 구분한다. 정의만 있고 실행하지 않았다면 evidence가 아니다.
자세한 격리·보존 규칙은 [`FIXTURE_RULES.md`](./FIXTURE_RULES.md)를 따른다.

### 5.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| FX-<...> | [검사 목적] | [최소 입력·사전 조건] | [runner path/command] | [판정 가능한 기대 결과] | [무엇이 폐기되는가] |

### 5.2 Execution records

각 실행 record는 한 run의 exact command와 실제 결과를 보존한다. `exit_status`는 실행한
프로세스의 실제 정수 code이며, command를 실행하지 않은 경우에만 `not-run`을 사용한다.
runner가 비정상 종료됐는지와 candidate 관찰이 실패했는지는 별도 필드로 기록한다.

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-<...> | FX-<...> | [RFC3339 / RFC3339] | [resolved path] | `[복사 가능한 명령]` | [0 또는 실제 code] | `pass` / `fail` / `indeterminate` / `not-run` + [실제 관찰] | [A-###, 또는 `none`] |

추가 실행 환경:

- **Tool/runtime versions:** [실제 확인한 버전 또는 `not-recorded`와 이유]
- **Environment overrides:** [예: per-run `GENESS_HOME`, locale, timezone]
- **Network/external writes:** [disabled 또는 명시된 host·목적·승인]
- **Redaction:** [적용한 규칙과 원문 보존 여부]

## 6. Artifacts and evidence [required]

artifact는 command·fixture 또는 source 관찰을 직접 지지해야 한다. repository 안에 보존한
파일은 상대 경로, 외부·임시 파일은 명시적인 locator를 적는다. 파일·blob에는 SHA-256을
기록하고, 빈 command output처럼 hash가 적용되지 않는 artifact는 그 이유를 적는다.

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | [redacted log / manifest / result / screenshot / source note] | [path 또는 URI] | [RUN-<...> 또는 S-###] | [hash 또는 `not-applicable: ...`] | `tracked` / `packet` / `local-only` / `discarded` | [직접 지지하는 claim/AC/OQ] |

보존하지 않은 raw output도 실행 record의 exit status와 redaction 결과를 남긴다. secret,
credential, 원본 환경변수와 대용량 evidence를 packet에 붙이지 않는다.

## 7. Risks and limitations [required]

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | [미확인 가정 또는 한계] | `low` / `medium` / `high` | [무엇을 아직 모르는가] | [다음 fixture·질문·완화] | [owner] | `open` / `mitigated` / `accepted` |

`accepted`는 사용자 또는 명시된 authority가 위험을 수용했다는 receipt가 있을 때만 사용한다.

## 8. Decision [required]

Research packet은 관찰과 권고를 제공하지만 규범을 스스로 채택하지 않는다.

- **Packet decision status:** `recommendation` / `needs-user-decision` / `resolved` /
  `blocked` / `superseded`
- **Recommendation:** [선호 candidate 또는 `no recommendation`]
- **Rationale:** [trade-off·source·fixture·artifact를 연결한 이유]
- **Rejected/deferred candidates:** [후보와 이유]
- **Unresolved impact:** [결정되지 않은 채 다음 단계에 미치는 영향]

### User/authority decision receipt

- **Decision:** [사용자/권한자가 실제로 선택한 내용 또는 `pending`]
- **Actor:** [identity 또는 `pending`]
- **Recorded at:** [RFC3339 또는 `pending`]
- **Reference:** [issue/comment/ADR/문서 경로 또는 `pending`]
- **Supersedes:** [이전 packet/decision 또는 `none`]

`resolved`를 쓰려면 위 receipt가 있어야 한다. receipt가 없으면 packet은
`needs-user-decision` 또는 `blocked`로 남기고, 관련 canonical 문서를 조용히 고치지 않는다.

## 9. Next verifiable goal

- [이 packet에서 남은 blocker 또는 다음에 실행할 검증 가능한 목표 하나]

## 10. Completeness checklist

- [ ] 질문·권한·allowed scope·non-goal이 명확하다.
- [ ] 후보가 둘 이상이거나, 하나뿐인 이유와 대안을 조사하지 않은 이유가 기록됐다.
- [ ] candidate와 동일 기준의 trade-off가 source/fixture evidence에 연결됐다.
- [ ] source마다 locator, pinned ref, accessed date와 license/action이 있다.
- [ ] 실행한 모든 command에 exact text, 실제 observation과 exit status가 있다.
- [ ] 실행하지 않은 command는 `not-run`과 이유로 분리돼 있다.
- [ ] artifact path/URI, hash 또는 hash 불가 이유와 retention이 있다.
- [ ] risk/limitation과 evidence gap, owner와 next check가 있다.
- [ ] decision status와 authority receipt가 일치한다.
- [ ] secret/raw log/대용량 output이 packet에 없다.
- [ ] 제품 scaffold, manifest, package와 target `.geness/` 변경이 없다.
- [ ] `git diff --check`와 관련 Markdown 검증 결과가 별도 execution record로 남아 있다.
