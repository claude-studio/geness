# Geness Progress

> 마지막 검증: 2026-08-21
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

### Phase 0 P0-05 #17 identity·schema·digest·config research — VERIFIED OBSERVATION

2026-08-21에 [OQ-005](../research/phase-0/OQ-005-project-workspace-identity.md),
[OQ-006](../research/phase-0/OQ-006-schema-lineage.md),
[OQ-007](../research/phase-0/OQ-007-digest-canonicalization.md),
[OQ-013](../research/phase-0/OQ-013-config-machine-contract.md) packet과 공통 disposable
fixture를 추가했다. 네 packet은 decision-ready recommendation이지만 사용자 decision
receipt가 없으므로 `Resolved` 또는 ADR로 승격하지 않았다.

정확한 fixture command를 두 번 실행했다.

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py

두 실행 모두 exit `0`, 30/30 assertions와 `all_assertions_pass=true`를 보고했고 parsed
JSON output이 equality-equivalent였다. local Git temporary probe에서 clone/rename/worktree
와 synthetic explicit fork relation을 확인했으며, frontmatter/SQLite semantic·body
round-trip, accepted revision 2 write와 stale revision DENIED/no mutation, contract/plan
golden vector와 portable/local config boundary도 통과했다.

보존한 artifact hash는 다음과 같다.

- `runner.py`: `42475a16c6e8136000eb5ee03297bef289a795e50af69855499ce4694c5e2a61`
- `input/fixture.json`: `06a74865a1852918d61e5cec7138dc521beee6084234bfee9d585b32de98fc4e`
- redacted result manifest: `c3dbbbf7a77605a2c195f3721178611c55e30bc79ef9c4a15fa262bc940e1c8c`

추가 검증은 `python3 -m py_compile` exit `0`, input/result JSON validation exit `0`,
`git diff --check --` exit `0`, read-only Markdown 검사 `markdown_files=57`,
`local_links=147`, `fence_delimiters=122`, `trailing_whitespace=0`, `errors=[]`였다.
이 결과는 identity/schema/digest/config 후보의 조사 evidence이지 production schema,
serializer, config policy, ADR 또는 Implementation `CLEAR`가 아니다.

### Phase 0 P0-06 #18 host·command surface research — VERIFIED OBSERVATION

2026-08-21에 [OQ-012 host compatibility packet](../research/phase-0/OQ-012-host-os-compatibility.md),
[OQ-014 command surface packet](../research/phase-0/OQ-014-command-surface.md), Proposed
[ADR-0008](../adr/0008-host-command-surface.md)와 폐기 가능한
`FX-HOST-CAPABILITY-COMMAND-SURFACE-001`을 추가했다. 두 packet은 decision-ready
recommendation이지만 사용자 decision receipt가 없으므로 `Resolved` 또는 Accepted ADR로
승격하지 않았다.

fixture의 read-only host probe는 Darwin 25.4.0 arm64에서 Codex `codex-cli 0.149.0`과
Claude Code `2.1.238`의 version/help/plugin/MCP/feature surface를 확인했다. 네트워크,
로그인, plugin install, agent 실행과 MCP server startup은 수행하지 않았다. 동일한
synthetic input을 fixture-local library, CLI thin transport와 MCP-like stdio transport로
보내 setup/profile, explicit/alias/description routing, status, resume와 transport error
경계를 비교했다.

실행한 주요 검증은 다음과 같다.

- `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` → `RUN-OQ012-001`, exit `0`, 83/83 assertions, 26 cases, `all_assertions_pass=true`
- `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` → `RUN-OQ014-001`, exit `0`, 동일한 83/83 assertions와 byte-identical raw result
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile surface_service.py cli_transport.py mcp_transport.py runner.py` → exit `0`
- `python3 -m json.tool input/fixture.json >/dev/null` → exit `0`
- `git diff --check --` → exit `0`
- `node /tmp/geness-p0-06-markdown-check.mjs` → exit `0`, `markdown_files=61`, `local_links=159`, `local_anchor_links=8`, `fence_delimiters=152`, `trailing_whitespace=0`, `errors=[]`

보존한 artifact hash는 OQ-012 result `25ff01711cc2a9aaf063fd117822f39d76f3b801fdec4dd8ea5dea49170d0511`,
OQ-014 result `ef1a6be9c0c302a0907403c4b1cab73185803abe28147cbe631fdabc62e41271`, fixture
input `8ffefbcbd76b4e8dcb3830196770e0713bdafcbe739bab5e8805a3f507b4e920`이다.
현재 관찰은 host capability와 command/profile 후보의 조사 evidence이지 installed-host
E2E, historical-version support floor, 제품 command schema, plugin scaffold 또는
Implementation `CLEAR`가 아니다. OQ-012/OQ-014와 ADR-0008의 user decision은 pending이다.

### Phase 0 P0-07 #19 memory·retention·bootstrap research — VERIFIED OBSERVATION

2026-08-21에 [OQ-010 lesson evaluator](../research/phase-0/OQ-010-lesson-evaluator.md),
[OQ-011 runtime retention](../research/phase-0/OQ-011-runtime-retention.md) packet과
폐기 가능한 `FX-MEMORY-RETENTION-BOOTSTRAP-001`을 추가했다. 두 packet은
decision-ready recommendation이지만 user decision receipt가 없으므로 `Resolved` 또는
ADR로 승격하지 않았고 Implementation `HOLD`를 유지한다.

정확한 fixture command를 두 번 실행했다.

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

두 실행 모두 exit `0`, 43/43 assertions와 `all_assertions_pass=true`를 보고했고 parsed
JSON output이 equality-equivalent였다. 관찰된 projection hash는
`sha256:0e3e7e4ef2ae40c0b6e68673774afe7cc2d8b74a122fb38438d7ddf8371b2b07`다.

관찰된 사실은 다음과 같다.

- 첫 failure는 `candidate`로 남고 retrieval에 노출되지 않았다. 동일 run의 중복은 독립
  recurrence로 세지 않았고, 독립 run 2회 또는 재현 가능한 guard evidence가 있는
  candidate만 fixture-local profile에서 `verified`가 됐다.
- `LESSON-ONEOFF`는 ineligible success를 제외하고 injected success를 unassisted로 세지
  않았으며, eligible unassisted success 3회와 최소 관찰 기간 뒤 `expired`가 됐다.
- 오래된 active/blocked runtime은 `KEEP`, completed low-risk는 TTL/size candidate에서
  `PRUNE`, high-risk no-disposition와 memory store item은 `KEEP`로 관찰됐다.
- bootstrap result contract는 `UNINITIALIZED`/`EMPTY`/`AVAILABLE`/`UNAVAILABLE`을
  구분하며, fixture-local recommendation에서 missing/empty/available은 explicit
  `CLEAR`/continue, corrupt는 `HOLD`/`rebuild_or_repair`였다.

보존한 artifact hash는 다음과 같다.

- fixture runner: `9706fbe1615baab6c184c84ff8b826f282b8cf17bc624ced8d6846eea5552c86`
- fixture input: `a8f292a84d629b342b7ec3d2e1cf21520788a7c81cef6cf4e46ad12e013ae4cb`
- OQ-010/OQ-011 redacted result manifest: `7f67e265b5f813b566c8f04c53d75b7b48fd33d54622662b74f4b4b81779a267`

추가 검증은 `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile .../runner.py`, 세 JSON
artifact에 대한 `python3 -m json.tool ... >/dev/null`, `git diff --check --`가 모두
exit `0`이었다. read-only Markdown 검사는
`node /tmp/geness-p0-06-markdown-check.mjs` → exit `0`,
`markdown_files=64`, `local_links=185`, `local_anchor_links=15`, `fence_delimiters=152`,
`trailing_whitespace=0`, `errors=[]`를 반환했다.

현재 관찰은 deterministic evaluator, runtime retention과 memory capability result 후보의
research evidence이지 production threshold, retention worker, bootstrap command, event/SQLite
schema, Learning/Storage ADR 또는 Implementation `CLEAR`가 아니다.

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

사용자가 Phase 0 blocking packet의 후보를 검토하고 decision receipt를 기록한다. 특히
[OQ-001](../research/OPEN_QUESTIONS.md)의 runtime 후보, P0-05의 OQ-005/006/007/013
identity·schema·digest·config recommendation, P0-06의 OQ-012/014 host·command
recommendation과 P0-07의 OQ-010/011 memory·retention·bootstrap recommendation을
선택하기 전에는 Architecture/Storage/Host/Specification/Learning ADR을 Accepted로
바꾸거나 제품 scaffold를 만들지 않는다.

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
