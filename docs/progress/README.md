# Geness Progress

> 마지막 검증: 2026-08-20
> Documentation foundation: CLEAR
> Implementation: HOLD

## 1. 이 문서가 소유하는 것

이 문서는 PLAN의 희망 상태가 아니라 현재 repository에서 artifact와 command로 확인한
사실만 기록한다. 개별 target task의 Gate가 아니라 **Geness 제품 자체 구현**의
HOLD/CLEAR를 소유한다.

## 2. 현재 판정

### Documentation foundation — CLEAR

Constitution, architecture/lifecycle/storage/host 문서, stage guides, PLAN, ADR, Research,
Progress와 root agent instruction이 존재한다. 로컬 link·anchor, Markdown integrity와
`CLAUDE.md → AGENTS.md` symlink 검사를 통과했다. 자세한 evidence는
[Documentation Foundation](./0000_DOCUMENTATION_FOUNDATION.md)에 있다.

이번 검증에서는 public stage alias, Geness v1 contract schema, `verification.md` final
projection, target setup과 Claude–Codex Controller bridge까지 canonical 문서에 정렬했다.
또한 DOC-01의 GitHub task handoff contract를 `AGENTS.md`와 `PLAN.md`에 정렬해 issue body,
checkpoint, session start/end checklist의 portable 기록 형식을 추가했다.

### Implementation — HOLD

Controller나 plugin scaffold 구현을 시작할 수 없다. 다음 이유가 확인됐다.

- repository에는 아직 구현 source, package manifest와 test harness가 없다.
- [Open Questions](../research/OPEN_QUESTIONS.md)의 Phase 0 blocking decision이 열려 있다.
- Controller 언어, canonical API 경계와 schema v1이 확정되지 않았다.
- 두 host의 최소 prototype과 threat model evidence가 없다.

HOLD 중 허용되는 작업은 문서 정렬, 공식 계약 조사, 읽기 전용 prototype/spike 설계와
사용자가 명시적으로 지시한 foundation 작업이다. 구현 언어를 임의로 선택해 scaffold를
생성하거나 `CLEAR`로 간주하지 않는다.

### Phase 0 OQ-001 disposable spike — VERIFIED OBSERVATION

2026-08-20에 [OQ-001 decision packet](../research/phase-0/OQ-001-controller-runtime.md)과
폐기 가능한 최소 runtime spike를 작성했다. macOS arm64에서 TypeScript/Node, Python,
Go, Rust 후보 모두 FTS5 table/query와 `initialize → tools/list → tools/call` stdio
round-trip을 exit `0`으로 통과했고, 두 개의 독립 working directory에서 같은 entrypoint를
재실행했다. 관찰된 release artifact는 Go 7,643,186 B, Rust 5,168,560 B이며 Node와
Python은 각각 dependency tree/site-packages disk usage를 측정했다.

실행한 주요 검증은 다음과 같다.

- `npm install @modelcontextprotocol/server@2.0.0 zod@4.4.3` → exit `0`
- `uv pip install --python py314env/bin/python 'mcp==2.0.0'` → exit `0`
- `go build -tags sqlite_fts5 ...` → exit `0`; stdio probe 두 working directory exit `0`
- `cargo build --release` → exit `0`; stdio probe 두 working directory exit `0`
- Go `sqlite_fts5` tag를 생략한 runtime probe → server exit `1`, `no such module: fts5`
- `git diff --check` → exit `0`; Markdown 31개·local link 108개 integrity 검사 `errors=[]`

이 결과는 후보 비교 evidence이지 구현 `CLEAR`, host 설치 E2E 또는 사용자 결정이 아니다.
OQ-001은 사용자 후보 선택 전까지 `OPEN`으로 유지한다.

### Phase 0 OQ-002 disposable fixture — VERIFIED OBSERVATION

2026-08-20에 [OQ-002 decision packet](../research/phase-0/OQ-002-canonical-command-api.md)과
폐기 가능한 typed-result/idempotency fixture를 실행했다. 같은 합성 입력을 fixture-local
common application service, CLI thin transport와 MCP-like stdio thin transport로 보냈고,
세 경로의 domain `HOLD`, `APPLIED`, `REPLAYED` projection이 일치했다. malformed CLI JSON와
unknown MCP method는 typed transport error로 분리됐고, valid domain `HOLD`는 transport
성공으로 유지됐다. 동일 idempotency key replay는 effect ID와 side-effect count `1`을
유지했다.

실제 evidence는
[`result.json`](../research/phase-0/evidence/OQ-002/FX-COMMAND-API-TYPED-RESULT-001/RUN-OQ002-001/result.json)에
보존했으며 SHA-256은
`502cf76ff555770e45dce6a3945a8f1eb30403de04ef2b94b6cefe0aa3f175aa`다. fixture runner는
14 assertions를 exit `0`으로 통과했고, `git diff --check --`는 exit `0`, read-only Markdown
검사는 39개 파일·119개 local link·8개 local anchor link·errors `[]`를 반환했다. 이 결과는
공통 service 경계의 조사 관찰이지 OQ-002 `Resolved`, Architecture ADR, 제품 schema/runtime
선택 또는 Implementation `CLEAR`가 아니다. OQ-001 사용자 결정과 OQ-002 사용자 decision
receipt는 모두 pending/open으로 유지한다.

### Phase 0 P0-04 #16 lifecycle·lease·completion research — VERIFIED OBSERVATION

On 2026-08-20, the disposable fixture and four observed research packets for OQ-003,
OQ-004, OQ-008 and OQ-009 were added under docs/research/phase-0/. The packets are
not Resolved decisions and all user decision receipts remain pending.

The exact fixture runner command was run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Both runs exited 0, reported 7 assertions with all_assertions_pass=true, and their
parsed JSON outputs compared equal. The source check also exited 0:

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

The recorded SHA-256 values are:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e

Observed facts are limited to ALLOWED INITIALIZING → INTERVIEWING, DENIED stale-digest
PLAN_APPROVED → RUNNING, DENIED invalid INTERVIEWING → RUNNING, a sequential first-writer
ALLOWED/second-writer DENIED probe, and equality-equivalent terminal replay with
completed=true and lease_active=false. Heartbeat/grace/takeover, complete lifecycle and
CANCELLED semantics, Plan Gate actor policy, crash-point matrix and production transaction
atomicity remain unobserved. No language, package, runtime, schema, daemon, lease policy,
approval actor or completion transaction was selected; no ADR was created.

## 3. 검증된 repository 사실

- Git repository root는 이 프로젝트 디렉터리다.
- 기존 제품 구현은 없고 root `README.md`만 있던 상태에서 문서 foundation을 시작했다.
- Geness의 제품 이름, dual-host 방향, target `.geness/`와 home `~/.geness/` 경계는
  사용자 결정과 Accepted ADR로 기록됐다.
- Root `AGENTS.md`가 docs-first 세션 절차와 Implementation HOLD를 연결하고,
  `CLAUDE.md`는 그 파일의 symlink다.
- 실제 target repository initializer, Controller, SQLite schema, Skill, manifest와 tests는
  아직 존재하지 않는다.
- 실행할 제품 test command는 아직 정의되지 않았다.
- GitHub task handoff contract는 `AGENTS.md`와 `docs/PLAN.md`에 존재하며, 제품 runtime
  state·Gate·completion authority를 대체하지 않는다.

## 4. 문서 상태

| 영역 | 상태 | 근거 |
| --- | --- | --- |
| Constitution | Accepted baseline | [00_GENESS](../00_GENESS.md) |
| Architecture | Proposed | [01_ARCHITECTURE](../01_ARCHITECTURE.md) |
| Lifecycle | Proposed, Phase 0 decisions open | [02_TASK_LIFECYCLE](../02_TASK_LIFECYCLE.md) |
| Storage boundary | Accepted, schema TBD | [ADR-0002](../adr/0002-project-and-local-state-boundary.md) |
| Dual-host boundary | Accepted, manifest prototype TBD | [ADR-0001](../adr/0001-dual-host-shared-core.md) |
| Interview principles | Accepted, implementation TBD | [ADR-0004](../adr/0004-ouroboros-interview-principles.md) |
| Failure learning | Accepted principle, thresholds TBD | [ADR-0003](../adr/0003-failure-candidate-is-not-memory.md) |
| Implementation plan | Draft | [PLAN](../PLAN.md) |

## 5. Phase roadmap

| Phase | 상태 | 다음 Gate |
| --- | --- | --- |
| Documentation Foundation | CLEAR | 완료 evidence 보존 및 drift 검사 |
| Phase 0: 계약과 ADR | HOLD | blocking decisions와 prototype evidence |
| Phase 1: plugin/project init | NOT STARTED | Phase 0 CLEAR |
| Phase 2: interview/spec | NOT STARTED | Phase 1 exit criteria |
| Phase 3: preflight/plan | NOT STARTED | Phase 2 exit criteria |
| Phase 4: run/verify/resume | NOT STARTED | Phase 3 exit criteria |
| Phase 5: failure learning | NOT STARTED | Phase 4 event evidence |
| Phase 6: host adapters/hooks | NOT STARTED | shared-core contract evidence |
| Phase 7: quality/release | NOT STARTED | 앞선 Phase integration evidence |

## 6. 다음 하나의 검증 가능한 목표

[OQ-001](../research/OPEN_QUESTIONS.md)의 후보 비교 evidence를 읽고 사용자가 Go+CGO,
Rust+bundled SQLite, TypeScript/Node 또는 Python 중 하나를 선택한다. 선택 전에는
Architecture ADR과 제품 scaffold를 만들지 않는다.

이번 DOC-01 문서 변경 뒤 다음을 검증했다.

- `git diff --check` → exit `0`
- read-only Node Markdown integrity 검사 → tracked Markdown 30개, local link/anchor,
  fenced code block과 trailing whitespace 검사 `errors=0`
- `AGENTS.md`와 `docs/PLAN.md`의 handoff contract, checkpoint heading과 session
  start/end checklist가 서로 정렬돼 있음을 diff로 확인

## 7. 갱신 규칙

- 실제로 실행한 command, exit status와 확인한 artifact만 evidence로 쓴다.
- 계획한 테스트를 통과한 테스트처럼 적지 않는다.
- HOLD 해제 조건을 만족한 evidence가 없으면 `CLEAR`로 바꾸지 않는다.
- 문서 작업과 구현 Phase를 같은 CLEAR로 합치지 않는다.
- 새 검증 결과가 이전 기록과 다르면 현재 판정을 갱신하고 milestone 기록은 보존한다.
- 작업 종료 때 다음 하나의 검증 가능한 목표를 남긴다.
