---
packet_schema_version: 1
packet_id: "OQ-015"
question_id: "OQ-015"
title: "threat model과 권한·scope·external write·secret 정책"
status: "resolved"
owner: "Codex research / Phase 0 cross-concern synthesis"
decision_authority: "user"
opened_at: "2026-08-21T06:32:24Z"
updated_at: "2026-08-21T07:18:40Z"
---

# OQ-015 — threat model과 권한 정책

## 1. Scope and authority

- **Question:** Geness v1의 threat model과 permission policy에서 target root, task scope,
  approval, host capability, secret/evidence와 completion 경계를 어떻게 보호할 것인가?
- **Phase/Gate:** Phase 0 / cross-concern decision packet
- **Decision authority:** 사용자
- **Allowed scope:** local same-machine v1의 trust boundary, 위협 시나리오, 권한·scope·external
  write·destructive action·secret·evidence control, 선행 OQ와 canonical 문서의 owner/link 정렬
- **Non-goals:** 제품 구현 언어·package·runtime·DB schema, host sandbox 구현, secret detector의
  최종 pattern set, 조직 IAM/remote service 보안, cloud resume, 실제 target `.geness/` 또는
  `~/.geness/` 상태 생성
- **Dependencies:** OQ-003/OQ-004/OQ-008/OQ-009의 lease·lifecycle·approval·completion
  결정과 OQ-005/OQ-006/OQ-007/OQ-010/OQ-011/OQ-012/OQ-013/OQ-014의 identity·schema·digest·
  memory·retention·host·config·command 결정
- **Research owner:** Codex research; user는 policy 선택과 residual risk 수용 권한을 가진다.

이 packet은 기존 OQ의 결정을 대신하지 않는다. 특히 OQ-008의 일반 `PLAN_APPROVED` actor와
risk threshold, OQ-009의 production atomicity와 secret redaction의 exact implementation은
후속 사용자 결정 또는 구현 evidence가 필요하다. OQ-003의 v1 no-daemon/liveness policy는
[ADR-0012](../../adr/0012-no-background-daemon-v1.md)와 receipt로 별도 기록됐다. 사용자는 C-01의
fail-closed boundary와 `user_sensitive`/`secret_handling` permission class를 선택했으며,
그 receipt와 Accepted ADR-0009가 이 packet의 결정 상태를 소유한다.

## 2. Candidates

| candidate_id | candidate | description | assumptions | evidence status |
| --- | --- | --- | --- | --- |
| C-01 | layered fail-closed Controller policy | Controller가 identity·revision·digest·lease·scope를 결정적으로 검사하고, read-only를 기본으로 하며 scope 확대·external write·destructive action·security boundary 변경은 current digest에 묶인 user receipt 없이는 `HOLD`한다. host/worker/hook은 capability를 축소할 수만 있고 approval을 승격할 수 없다. | Controller가 host capability와 user receipt를 검증 가능한 envelope로 받고, redaction·root containment·independent verification을 공통 policy로 구현한다. | `observed` fixture control + `inferred` recommendation |
| C-02 | host-trust delegation | 각 host의 sandbox·approval·trust model이 실제 권한을 소유하고 Controller는 결과와 metadata만 기록한다. | Codex와 Claude의 approval·hook·MCP semantics가 충분히 동등하고 host가 모든 transport를 우회할 수 없다는 가정이 필요하다. | `observed` host capability facts + `inferred` risk |
| C-03 | policy auto-approval | low-risk/routine plan은 risk classifier가 자동 승인하고 user는 high-risk·scope·external action만 승인한다. | risk 분류가 누락·오탐 없이 결정적이고, 모든 side effect를 사전 분류할 수 있다는 가정이 필요하다. | `unverified` product policy |

## 3. ATAM-style threat model

### 3.1 Assets and trust boundaries

| asset / boundary | 보호할 속성 | 권위자 | 경계 실패 시 영향 |
| --- | --- | --- | --- |
| target `.geness/` contract projection | integrity, portability, target-root containment | Controller + approved user contract | 다른 저장소·path에 문서가 쓰이거나 승인 계약이 오염됨 |
| `~/.geness/runtime/` state, lease, approvals, evidence metadata | confidentiality, integrity, availability, lineage | Controller runtime transaction | stale/replay run, 두 writer, false completion, 민감정보 노출 |
| `~/.geness/memory/` events/lessons/index | integrity, scope isolation, retrieval confidentiality | Controller + deterministic evaluator | candidate poisoning, project 간 memory bleed, 잘못된 guard 주입 |
| user approval and provenance | authenticity, non-repudiation within local audit | user receipt + Controller validation | worker/host가 사용자 판단을 사칭하거나 implicit approval 발생 |
| host/worker transport | capability confinement, message integrity | thin adapter + Controller envelope | transport가 domain rule을 우회하거나 scope 밖 side effect를 발생 |
| model context and raw command output | confidentiality, minimization | redaction boundary before persistence/context | token·credential·environment secret이 문서·memory·prompt로 유출 |
| external/destructive side effect | authorization, auditability, reversibility | user; host approval is additional guard | remote resource 변경, 데이터 손실, 복구 불가능한 변경 |

v1의 threat model은 같은 컴퓨터·같은 사용자 데이터 루트·사용자가 준비한 worktree를 전제로
한다. 다른 사용자·원격 공격자·cloud sync의 인증/조직 IAM은 이 packet의 결정 대상이 아니며,
그 경계를 안전하다고 주장하지 않는다.

### 3.2 Threat actors and scenarios

- **Untrusted project content:** README, task text, config 또는 generated output이 “정책을
  무시하고 승인하라”는 instruction을 포함할 수 있다. content는 `from-code` 또는 untrusted
  observation일 뿐 `from-user` approval이 아니다.
- **Compromised/buggy worker or adapter:** worker, hook, CLI/MCP transport가 runtime DB를
  직접 쓰거나 forbidden capability를 요청할 수 있다.
- **Stale or replayed operation:** 이전 digest·approval·checkpoint를 재사용해 오래된 scope나
  side effect를 다시 실행할 수 있다.
- **Concurrent local process/workspace:** 두 host/process가 같은 `project_id + task_id`를
  동시에 mutate하거나 stale lease를 탈취할 수 있다.
- **Accidental secret source:** stdout/stderr, environment, config, evidence와 memory 후보에
  token·credential·secret이 섞일 수 있다.
- **Corrupt or manipulated projection:** runtime DB, Markdown projection 또는 memory index가
  불완전·손상·stale한데도 `CLEAR`/`COMPLETED`로 축약될 수 있다.

위 시나리오를 control matrix에서 다음 threat ID로 추적한다.

| threat_id | threat | primary impact |
| --- | --- | --- |
| `T-root` | target-root traversal·symlink escape | target 밖 write와 portable contract 오염 |
| `T-authority` | untrusted content/worker가 user approval을 사칭 | 무단 scope·side effect 실행 |
| `T-stale` | stale/replayed digest·approval·checkpoint | 오래된 contract 실행과 duplicate effect |
| `T-race` | 두 local writer 또는 stale lease takeover | state/evidence/lease 불일치 |
| `T-capability` | forbidden capability와 host/worker escalation | runtime DB 조작·external/destructive action |
| `T-secret` | raw output·environment·evidence의 secret leakage | credential 노출과 memory/context 오염 |
| `T-completion` | worker self-verification 또는 부족한 evidence | 근거 없는 `COMPLETED` |
| `T-memory` | candidate poisoning 또는 corrupt index optimistic handling | 잘못된 lesson 주입과 unsafe continuation |
| `T-projection` | Markdown/runtime projection drift | stale verdict·reconciliation 누락 |
| `T-host` | host trust/transport/cache 경계 혼동 | host별 approval·state drift |
| `T-retention` | runtime/evidence prune와 memory cleanup 혼동 | 복구 evidence 삭제 또는 memory loss |

### 3.3 Quality-attribute scenarios

| scenario | stimulus | required response | sensitivity point |
| --- | --- | --- | --- |
| Q-01 root escape | worker가 `../` 또는 symlink를 통해 target 밖 path를 요청 | canonical resolved root containment 검사 후 `HOLD`, no write | path canonicalization와 symlink handling |
| Q-02 authority injection | project text가 external write 승인을 지시 | provenance를 user receipt로 승격하지 않고 `HOLD` | authority classification |
| Q-03 stale approval/run | old digest의 plan/approval을 current task에 제출 | digest/revision mismatch를 `HOLD`, no mutation | versioned digest and idempotency |
| Q-04 writer race | 두 process가 같은 task lease를 획득 | first writer만 mutate, second는 observer/`HOLD` | project-scoped lease authority |
| Q-05 capability escalation | worker가 danger-full-access, runtime DB write 또는 external write를 요청 | capability allowlist와 user-only policy로 차단 | host sandbox와 Controller policy의 결합 |
| Q-06 secret exposure | command output에 synthetic token이 포함 | persistence/context 전에 redaction, 원문 project 문서 저장 금지 | detector coverage와 fail-closed behavior |
| Q-07 false completion | worker가 자기 결과만으로 behavior AC를 PASS 주장 | independent verifier와 current acting evidence 없이는 `HOLD` | verifier independence/evidence freshness |
| Q-08 memory poisoning | first failure 또는 corrupt index가 query에 들어옴 | candidate는 숨기고 corrupt/unavailable은 typed `HOLD` | memory lifecycle and bootstrap result |

### 3.4 Sensitivity and trade-off points

- **Controller policy vs host delegation:** C-01은 host 차이와 worker 오작동을 한 경계에서
  차단하지만 Controller policy/envelope 구현 비용이 커진다. C-02는 초기 구현이 단순해도
  host별 approval/trust 차이로 같은 contract가 다른 side effect를 낼 위험이 높다.
- **Fail-closed vs throughput:** C-01은 redaction 불확실성, missing capability, stale state를
  `HOLD`로 라우팅하므로 자동 진행률이 낮아질 수 있다. 대신 security boundary를 조용히
  완화하지 않는다. C-03은 routine work가 빠르지만 risk classifier 오류가 사용자 승인을
  대체한다.
- **Portable evidence vs confidentiality:** target 문서에는 요약·hash·lineage만 두고 raw
  output/evidence는 local runtime 경계로 제한한다. 이 경계는 Git portability보다 secret
  최소화를 우선하며, 필요한 evidence lazy-load와 owner-only permission 비용을 만든다.
- **One writer vs collaboration:** v1 one-writer/observer는 race를 줄이지만 여러 worktree
  동시 수정과 cloud resume을 지원하지 않는다. 이 범위는 ADR-0006과 기존 lifecycle 방향을
  유지한다.

## 4. Control matrix and ownership

`current direction`은 이미 상위 문서에 있는 baseline이고, `accepted policy`는 이 packet의
user receipt와 ADR-0009가 확정한 C-01 합성 결론이다. OQ-008의 일반 plan approval actor와
정확한 risk tier는 별도 미결정으로 남는다.
표의 `FX-...-001`은 `FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001` fixture의 축약 표기다.

| control_id | threat | accepted control | canonical owner | blocking OQ / authority | fixture/evidence |
| --- | --- | --- | --- | --- | --- |
| C-01 | T-root | resolved target root containment, parent traversal·symlink escape 거부, branch/worktree lifecycle은 user-owned | Storage / Controller boundary | OQ-005/OQ-006/OQ-013 · user | `FX-...-001` `path.*` |
| C-02 | T-authority | `from-user`/`from-code`/`from-research` provenance 분리; untrusted text·worker result는 approval이 아님 | Interview + Specification | OQ-008/OQ-015 · user | `FX-...-001` `authority.untrusted_instruction` |
| C-03 | T-stale | spec/plan/approval digest와 revision precondition, operation ID/idempotent replay | Lifecycle / Specification | OQ-007/OQ-009 · user | `FX-...-001` `execution.stale_digest`, `approval.stale_user_receipt` |
| C-04 | T-race | `project_id + task_id` active writer 하나, observer read-only, grace/takeover는 별도 evidence 후 적용 | Lifecycle / Runtime | ADR-0012/OQ-009 · user | `FX-...-001` `lease.*`; production takeover remains open |
| C-05 | T-capability | setup/preflight read-only, approved in-scope local write만 허용; runtime DB·approval bypass·danger-full-access·external/destructive action은 forbidden 또는 user-only | Host Integration / Execution | OQ-008/OQ-012/OQ-014/OQ-015 · user | `FX-...-001` `approval.*`, `capability.*` |
| C-06 | T-secret | 저장·projection·model context 전 redaction; raw/credential은 project docs와 memory에 저장하지 않고 detector 불확실성은 `HOLD`/local-only로 라우팅 | Storage / Verification | OQ-011/OQ-013/OQ-015 · user | `FX-...-001` `secret.redacted_output`; exact detector open |
| C-07 | T-completion | worker self-verification 금지, behavior-bearing AC는 current mechanical+acting evidence와 independent verifier 필요 | Verification / Controller | OQ-004/OQ-008/OQ-009 · user | `FX-...-001` `verification.*` |
| C-08 | T-memory | candidate는 retrieval에서 숨김, corrupt/unavailable memory는 empty로 축약하지 않고 typed `HOLD`, event/index lineage 보존 | Learning / Storage | OQ-010/OQ-011 · user | `FX-...-001` `memory.*`; OQ-011 fixture |
| C-09 | T-projection | runtime DB가 mutable verdict/lease의 정본, Markdown은 idempotent projection; stale/manual projection은 reconciliation | Architecture / Storage | OQ-006/OQ-009 · user | OQ-006/OQ-009 fixtures |
| C-10 | T-host | thin host adapter, hook non-authoritative, shared `GENESS_HOME`, host cache read-only; capability snapshot 없이는 profile 실행 금지 | Host Integration | OQ-012/OQ-014 · user | OQ-012/OQ-014 fixtures |
| C-11 | T-retention | active/blocked/high-risk runtime evidence 자동 삭제 금지; completed low-risk prune와 memory cleanup 분리 | Storage | OQ-011 · user | OQ-011 `result.json` |

### 4.1 Permission classes

| class | examples | default actor/capability | denial result |
| --- | --- | --- | --- |
| `observe` | repository read, status, setup/preflight probe | Controller/worker read-only | unavailable evidence면 `HOLD` |
| `approved_local_write` | approved target path 안의 contract-scoped implementation | active writer + approved plan + host workspace-write | scope/path/digest/lease mismatch면 `HOLD` |
| `user_sensitive` | scope 확대, external write, destructive action, security boundary/permission escalation | explicit user receipt bound to current digest; host approval may add a guard | absent/stale/non-user receipt면 `HOLD` |
| `forbidden_v1` | runtime DB 직접 write, approval bypass, danger-full-access default, candidate memory promotion | no worker/adapter authority | deterministic deny/`HOLD` |
| `secret_handling` | token/credential/environment secret 출력·저장·context injection | never intentionally accepted; redaction before persistence/context | detector uncertainty or unredacted value면 `HOLD`/local-only |

## 5. Sources

모든 source는 repository-local 문서다. 외부 코드·prompt·template을 복사하지 않았다. 고정
기준 ref는 packet 작성 직전의 `8baaef630a6a725892236f4e72bdcaaa09b05b9d`다.

| source_id | kind | locator | pinned ref | accessed | observation | license/action |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | `local-doc` | [`docs/00_GENESS.md`](../../00_GENESS.md#4-역할과-권한), `#6-헌법적-원칙` | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | user/Controller/worker/adapter authority와 scope/evidence/one-writer 원칙을 확인했다. | Local project document; no external reuse. |
| S-002 | `local-doc` | [`docs/01_ARCHITECTURE.md`](../../01_ARCHITECTURE.md#7-원자성-경계), `#9-architecture-invariants` | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | Controller transaction, thin adapter, projection과 candidate/dual-writer invariant를 확인했다. | Local project document; no external reuse. |
| S-003 | `local-doc` | [`docs/02_TASK_LIFECYCLE.md`](../../02_TASK_LIFECYCLE.md#4-gate-공통-계약), `#8-writer-lease`, `#9-completion` | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | Gate `HOLD`, approval actor, writer lease와 completion 조건의 현재 contract를 확인했다. | Local project document; no external reuse. |
| S-004 | `local-doc` | [`docs/03_STORAGE.md`](../../03_STORAGE.md#5-project-document-contract), `#10-security` | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | root containment, owner-only storage, redaction, runtime/memory boundary를 확인했다. | Local project document; no external reuse. |
| S-005 | `local-doc` | [`docs/04_HOST_INTEGRATION.md`](../../04_HOST_INTEGRATION.md#4-cli와-mcp), `#5-host-adapter-책임`, `#7-hooks` | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | common application authority, host approval non-bypass, hook non-authority를 확인했다. | Local project document; no external reuse. |
| S-006 | `local-doc` | [`docs/06_SPECIFICATION.md`](../../06_SPECIFICATION.md#8-planmd)와 [`docs/07_EXECUTION.md`](../../07_EXECUTION.md#3-work-derivation) | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | allowed/forbidden scope, approval point, handoff envelope와 checkpoint 경계를 확인했다. | Local project document; no external reuse. |
| S-007 | `local-doc` | [`docs/08_VERIFICATION.md`](../../08_VERIFICATION.md#3-검증-층)와 [`docs/09_LEARNING.md`](../../09_LEARNING.md#2-핵심-구분) | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | acting/independent evidence와 candidate/retrieval 분리를 확인했다. | Local project document; no external reuse. |
| S-008 | `local-research` | [`OQ-008`](./OQ-008-plan-approval-policy.md), [`OQ-011`](./OQ-011-runtime-retention.md), [`OQ-012`](./OQ-012-host-os-compatibility.md), [`OQ-013`](./OQ-013-config-machine-contract.md) | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | approval/security threshold, retention/bootstrap, host capability와 portable/local leakage gap이 user-owned임을 확인했다. | Local research; no external reuse. |
| S-009 | `local-research` | [`FIXTURE_RULES.md`](./FIXTURE_RULES.md)와 [`OQ-002`](./OQ-002-canonical-command-api.md) | `8baaef630a6a725892236f4e72bdcaaa09b05b9d` | 2026-08-21 | fixture isolation, network/external-write off, redacted evidence와 typed result 경계를 확인했다. | Local research convention; no external reuse. |

## 6. Fixture catalog and execution

### 6.1 Fixture catalog

| fixture_id | purpose | input/precondition | runner | expected observation | disposable boundary |
| --- | --- | --- | --- | --- | --- |
| `FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001` | path/authority/digest/lease/capability/redaction/verification/memory control의 fail-closed 후보 관찰 | `input/fixture.json`의 synthetic digest, allowed scope, forbidden capability와 redaction probe | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | 17 assertions pass, `all_assertions_pass=true`, two-run projection equality | runner temp target/symlink와 raw output은 폐기; input/runner `tracked`, result `packet` |

### 6.2 Execution records

| run_id | fixture_id | started_at / ended_at | cwd | exact command | exit_status | observation status/result | artifact refs |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `RUN-OQ015-001` | `FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001` | 2026-08-21T06:32:24Z / 2026-08-21T06:32:24Z | `docs/research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001` | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 17/17 assertions; root escape, authority, stale approval/digest, lease, capability, redaction, verification과 memory boundary | A-001, A-002, A-003 |
| `RUN-OQ015-002` | `FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001` | 2026-08-21T06:32:24Z / 2026-08-21T06:32:24Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 17/17 assertions; output byte-identical to RUN-OQ015-001 | A-004 |
| `RUN-OQ015-003` | `FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001` | 2026-08-21T06:41:37Z / 2026-08-21T06:41:38Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — final runner hash 기준 17/17 assertions | A-006 |
| `RUN-OQ015-004` | `FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001` | 2026-08-21T06:41:38Z / 2026-08-21T06:41:38Z | same as above | `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` | `0` | `pass` — 17/17 assertions; output byte-identical to RUN-OQ015-003 | A-007 |

추가 실행 환경:

- **Tool/runtime versions:** Python `3.14.5`, Git `2.53.0`, Darwin `25.4.0 arm64`
- **Environment overrides:** `PYTHONDONTWRITEBYTECODE=1`; 실제 `GENESS_HOME` 미사용
- **Network/external writes:** disabled / false; credentials, login, plugin install, MCP server와
  daemon은 사용하지 않음
- **Redaction:** runner output은 assertion 결과와 hash만 보존하며 raw stdout/stderr와 temporary
  target state는 보존하지 않음

### 6.3 Observed result

- canonical root 안의 허용 파일만 `ALLOW`이고 parent traversal과 symlink escape는 `false`였다.
- user receipt 없는 external write와 untrusted repository instruction, stale user receipt는
  `HOLD`였다. current digest에 묶인 user receipt만 sensitive scope action을 `ALLOW`했다.
- 두 번째 writer, stale digest, danger-full-access/forbidden capability는 `HOLD`이고 observer
  read는 `ALLOW`였다.
- synthetic redaction probe는 `[REDACTED]`로 축약됐고 원문 marker는 redacted output에 남지
  않았다.
- worker self-verification과 behavior-bearing AC의 acting evidence 누락은 `HOLD`였고, candidate
  lesson은 query에서 숨겨졌으며 corrupt memory는 `HOLD/rebuild_or_repair`였다.
- 두 runner output은 byte-identical했고 result input hash는
  `sha256:41dfd917257a4ddc34c3d156afed1a6aa5b6a3c1a81c84888cfb218a6cea06fb`다.

이는 fixture-local policy observation이지 Controller 구현, host sandbox guarantee, secret
detector completeness, production lease/transaction 또는 user decision의 증거는 아니다.

## 7. Artifacts and evidence

| artifact_id | kind | path/URI | produced by | sha256 or reason | retention | supports |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | fixture README | `docs/research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/README.md` | fixture definition | recorded after validation | `tracked` | isolation, exact command, control catalog |
| A-002 | fixture runner | `docs/research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/runner.py` | fixture definition | `sha256:b8f926b12e08ce234e608818598e0fbb81efda25725cb633d7a68f0784b1398a` | `tracked` | deterministic 17-assertion control probe |
| A-003 | synthetic input | `docs/research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/input/fixture.json` | fixture definition | `sha256:41dfd917257a4ddc34c3d156afed1a6aa5b6a3c1a81c84888cfb218a6cea06fb` | `tracked` | current digest, allowed scope, forbidden capability and redaction case |
| A-004 | redacted result manifest | `docs/research/phase-0/evidence/OQ-015/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/RUN-OQ015-001/result.json` | `RUN-OQ015-001/002` | `sha256:e5d7afbd810487fb7847f48a035d329b17e292b2e29695169942e4c4a1a00ce7` | `packet` | 17 assertions and two-run equality |
| A-005 | redacted rerun manifest | `docs/research/phase-0/evidence/OQ-015/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/RUN-OQ015-002/result.json` | `RUN-OQ015-002` | `sha256:e5d7afbd810487fb7847f48a035d329b17e292b2e29695169942e4c4a1a00ce7` | `packet` | rerun equality |
| A-006 | final redacted result manifest | `docs/research/phase-0/evidence/OQ-015/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/RUN-OQ015-003/result.json` | `RUN-OQ015-003` | `sha256:e5d7afbd810487fb7847f48a035d329b17e292b2e29695169942e4c4a1a00ce7` | `packet` | final runner source와 control observation |
| A-007 | final redacted rerun manifest | `docs/research/phase-0/evidence/OQ-015/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/RUN-OQ015-004/result.json` | `RUN-OQ015-004` | `sha256:e5d7afbd810487fb7847f48a035d329b17e292b2e29695169942e4c4a1a00ce7` | `packet` | final rerun equality |
| A-008 | raw stdout/temp target | per-run temp state | `RUN-OQ015-001/002/003/004` | discarded after redaction; no target/home state used | `discarded` | raw execution only |

Additional validation records:

| command | exit status | result |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/runner.py` | `0` | runner parses successfully |
| `python3 -m json.tool docs/research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/input/fixture.json >/dev/null` | `0` | synthetic input is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-015/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/RUN-OQ015-001/result.json >/dev/null` | `0` | redacted evidence is valid JSON |
| `python3 -m json.tool docs/research/phase-0/evidence/OQ-015/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/RUN-OQ015-003/result.json >/dev/null` | `0` | final redacted evidence is valid JSON |
| `git diff --check --` | `0` | no whitespace errors in tracked diff |
| `node /tmp/geness-p0-06-markdown-check.mjs` | `0` | `markdown_files=67`, `local_links=223`, `local_anchor_links=25`, `fence_delimiters=154`, `trailing_whitespace=0`, `errors=[]` |

Receipt-sync revalidation in the current worktree repeated the fixture twice with exit `0`,
17/17 assertions and byte-identical raw output. The Markdown checker then returned exit `0`
with `markdown_files=69`, `local_links=240`, `local_anchor_links=25`,
`fence_delimiters=154`, `trailing_whitespace=0`, `errors=[]`; `git diff --check --` also
returned exit `0`.

## 8. Risks and limitations

| risk_id | risk/limitation | impact | evidence gap | mitigation/next check | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | C-01 is selected, but the general `PLAN_APPROVED` actor and risk threshold remain open. | `high` | OQ-008 still owns ordinary plan approval and exact risk classification. | OQ-008 decision packet and Lifecycle/Specification ADR follow-up. | user | `open` |
| R-002 | fixture is a pure Python synthetic model, not a production Controller or host sandbox. | `high` | official transport, sandbox enforcement, multi-process race와 crash recovery는 미검증이다. | selected runtime/host 이후 Phase 1/4/6 fixture와 E2E를 실행한다. | user / Phase 1/4/6 | `open` |
| R-003 | redaction probe covers only synthetic patterns. | `high` | binary output, Unicode, nested JSON, tool transcripts, unknown secret formats와 detector false negative가 미확인이다. | redaction schema/version, fail-closed behavior와 corpus를 user decision 후 별도 security test로 확장한다. | user / Phase 1/4 | `open` |
| R-004 | lease/approval/transaction observations are not production atomicity. | `high` | cross-workspace arbitration, crash-point matrix와 receipt storage가 미확인이다. | OQ-009의 다중 process/replay fixture와 selected runtime ADR/implementation evidence를 완료한다. OQ-003의 no-daemon policy는 ADR-0012로 결정됐다. | user | `open` |
| R-005 | target-root and project identity policy depends on unresolved OQ-005/OQ-006/OQ-013. | `medium` | fork/rekey, schema migration, config precedence와 symlink policy의 final schema가 미확인이다. | Storage/Schema ADR에서 identity, projection과 config boundary를 함께 확정한다. | user | `open` |
| R-006 | threat actor scope excludes remote/cloud/organization IAM. | `medium` | external service auth, multi-user shared home와 supply-chain provenance는 별도 threat model이 필요하다. | v1 범위 밖으로 기록하고 remote/cloud release 전 별도 security review를 만든다. | user / Phase 6/7 | `open` |

## 9. Decision

- **Packet decision status:** `resolved`
- **Decision:** C-01 — host-neutral Controller가 fail-closed permission boundary를 소유하고,
  read-only를 기본 capability로 두며, approved in-scope local write만 current spec/plan digest와
  active writer lease 아래 허용한다. scope 확대, external write, destructive action, security
  boundary 변경과 permission escalation은 current digest에 묶인 explicit user receipt 없이는
  `HOLD`한다. worker·adapter·hook은 runtime DB/approval/completion/memory promotion 권한을
  갖지 않으며, secret은 persistence/context 전에 redaction하고 불확실하면 `HOLD`/local-only로
  라우팅한다. independent current evidence가 없는 completion과 candidate/corrupt memory의
  optimistic 처리도 허용하지 않는다.
- **Rationale:** C-01은 기존 Constitution, Lifecycle, Storage, Host Integration의 owner/one-writer/
  evidence boundary를 하나의 cross-concern으로 연결하고, fixture에서 root escape·authority
  confusion·stale approval/digest·writer race·capability escalation·redaction·self-verification·
  memory poisoning control의 결정표를 재현했다. C-02는 host trust 차이와 transport bypass를
  Controller 밖에 남기며, C-03은 risk classifier가 user approval을 대체하는 false-negative 경계를
  만든다.
- **Rejected/deferred candidates:** C-02는 host-specific approval/trust drift 때문에 deferred;
  C-03은 risk classification과 policy auto-approval evidence가 없어 deferred. C-01의 exact
  risk tiers, secret detector, receipt schema, retention/backup과 production enforcement는
  OQ-008 및 후속 implementation evidence로 남긴다.
- **Unresolved impact:** OQ-008의 일반 plan approval actor/risk tier와 다른 Phase 0 결정이
  열려 있으므로 Phase 0 전체 `CLEAR`나 Phase 1 scaffold를 주장하지 않는다.

### User/authority decision receipt

- **Decision:** C-01 fail-closed boundary와 `user_sensitive`/`secret_handling` permission class 선택
- **Actor:** `user`
- **Recorded at:** `2026-08-21T07:18:40Z`
- **Reference:** [USER-DECISION-OQ015-001](./evidence/OQ-015/USER-DECISION-RECEIPT-001.md)
- **Supersedes:** `none`

## 10. Next verifiable goal

OQ-008의 일반 `PLAN_APPROVED` actor/risk threshold와 나머지 Phase 0 blocking decision을
사용자 receipt로 닫고, Phase 0 Gate에 필요한 전체 evidence를 감사한다.

## 11. Completeness checklist

- [x] 질문·권한·allowed scope·non-goal과 선행 OQ owner/authority가 명확하다.
- [x] C-01/C-02/C-03의 material trade-off와 보안 품질 속성을 비교했다.
- [x] asset, trust boundary, threat actor, scenario, sensitivity/trade-off와 residual risk가 있다.
- [x] control마다 canonical owner, blocking OQ/authority와 fixture/evidence link가 있다.
- [x] source마다 local locator, pinned ref, accessed date와 license/action이 있다.
- [x] 실행한 fixture command에 exact text, exit status와 실제 observation이 있다.
- [x] 실행하지 않은 production enforcement, host E2E, multi-process race와 detector corpus는 limitation으로 남겼다.
- [x] artifact path, hash와 retention이 있다.
- [x] decision status와 authority receipt가 일치한다.
- [x] secret/raw log/대용량 output/target `.geness/`/실제 `~/.geness/`를 packet에 넣지 않았다.
- [x] fixture runner/input/result가 제품 scaffold와 분리되어 있다.
