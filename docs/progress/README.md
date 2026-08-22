# Geness Progress

> 마지막 검증: 2026-08-22
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
- production schema v1이 확정되지 않았고, Go runtime의 cross-platform/release validation도
  남아 있다.
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
OQ-001은 사용자 후보 선택 전까지 `OPEN`으로 유지했으며, 현재는 별도 decision receipt와
Accepted [ADR-0010](../adr/0010-controller-runtime-go.md)로 `Resolved` 상태다.

### Phase 0 OQ-001 — VERIFIED DECISION

2026-08-22에 사용자는 OQ-001 후보 A인 Go + standard Go modules + CGO + 명시적
`sqlite_fts5` build contract를 선택했다. 결정은
[USER-DECISION-OQ001-001](../research/phase-0/evidence/OQ-001/USER-DECISION-RECEIPT-001.md)와
[ADR-0010](../adr/0010-controller-runtime-go.md)에 기록했다.

이 결정은 runtime 방향을 고정하지만 macOS·Linux·Windows release artifact, cross-build,
exact dependency/toolchain matrix, installed-host E2E와 제품 scaffold를 검증하거나
Implementation `CLEAR`로 바꾸지 않는다.

현재 decision sync 검증은 다음과 같다.

- `git diff --check --` → exit `0`
- OQ-001 receipt YAML parse (`ruby`/Psych) → exit `0`
- OQ-003 packet/receipt frontmatter, evidence JSON and current-run evidence checks → exit `0`
- OQ-003 liveness fixture current smoke run → exit `0`, `17/17 assertions`,
  `all_assertions_pass=true`
- read-only Node Markdown integrity check → exit `0`, `markdown_files=78`,
  `local_links=326`, `local_anchor_links=25`, `fence_delimiters=126`,
  `trailing_whitespace=0`, `errors=[]`

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
검사는 당시 39개 파일·119개 local link·8개 local anchor link·errors `[]`를 반환했다. 이
fixture evidence는 제품 schema/runtime 선택 또는 Implementation `CLEAR`를 의미하지 않는다.

### Phase 0 OQ-002 — VERIFIED DECISION

2026-08-22 사용자가 C-01을 선택했다. 공통 application service가 domain policy, typed
result와 idempotency를 소유하는 canonical command API이고, CLI/MCP는 동일 service를
호출하는 thin transport로 유지한다. Transport-specific error와 domain `HOLD`는
분리하며, 유효한 `HOLD`는 성공한 transport exchange로 보존한다.

결정은 [OQ-002 user receipt](../research/phase-0/evidence/OQ-002/USER-DECISION-RECEIPT-001.md)와
[ADR-0011](../adr/0011-canonical-command-api.md)에 기록됐다. 이 결정은 최종 command/tool
schema·protocol, production schema/digest, daemon/lease, installed-host behavior와
scaffold를 확정하지 않으며, Implementation `HOLD`를 해제하지 않는다.

### Phase 0 P0-04 #16 lifecycle·lease·completion research — VERIFIED OBSERVATION

On 2026-08-20, the disposable fixture and four observed research packets for OQ-003,
OQ-004, OQ-008 and OQ-009 were added under docs/research/phase-0/. At that observation
point the packets were not Resolved decisions and all decision receipts were pending;
later decisions are recorded in the dedicated sections below.

The exact fixture runner command was run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Both runs exited 0, reported 7 assertions with all_assertions_pass=true, and their
parsed JSON outputs compared equal. The source check also exited 0:

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

The recorded SHA-256 values are:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e

In that original run, observed facts were limited to ALLOWED INITIALIZING → INTERVIEWING,
DENIED stale-digest PLAN_APPROVED → RUNNING, DENIED invalid INTERVIEWING → RUNNING, a
sequential first-writer ALLOWED/second-writer DENIED probe, and equality-equivalent terminal
replay with completed=true and lease_active=false. The separate heartbeat/grace/takeover
observation is recorded below. Complete lifecycle and CANCELLED semantics, Plan Gate actor
policy, crash-point matrix and production transaction atomicity remained unobserved at that
original observation point. No language, package, runtime, schema, daemon, lease policy,
approval actor or completion transaction was selected; the later decisions are recorded in
the dedicated decision sections below.

### Phase 0 OQ-003 liveness fixture — VERIFIED OBSERVATION

2026-08-22에 [OQ-003 liveness packet](../research/phase-0/OQ-003-daemon-lease-liveness.md)의
누락된 heartbeat·grace·takeover evidence를 위해
[`FX-LEASE-LIVENESS-TAKEOVER-001`](../research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001/README.md)을
추가하고 두 번 실행했다. 각 실행은 실제 writer/observer child process 두 개를 시작했고,
logical time `0` lease 획득, time `2` heartbeat와 grace deadline `5` 갱신, time `3`·`4`와
정확한 deadline `5` grace 중 takeover 거부, writer의 `SIGKILL` interruption, time `6`
stale takeover 허용, time `7` 새 owner heartbeat 허용을 관찰했다.

정확한 command는 다음과 같다.

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001/runner.py

두 실행 모두 exit `0`, 17/17 assertions와 `all_assertions_pass=true`였고 stdout/stderr
hash가 byte-identical이었다. redacted evidence는
[`result.json`](../research/phase-0/evidence/OQ-003/FX-LEASE-LIVENESS-TAKEOVER-001/RUN-OQ003-001/result.json)에
보존했으며 runner SHA-256은
`af6cafaaf7d24625b133eedf530aa3c70e3c1261951597827b53032c5d027268`, input은
`446dc5f6e01da55c3941cabc8ca491e36c75774853e3ae9680e73c126204dc6d`, result manifest는
`9c53e1155125f44e44812933ffca9a03abfe65e6d4068026fa005046818da0a1`다. 이 관찰은
fixture-local logical lease protocol에 한정되며 daemon/sidecar 선택, production clock·DB
transaction, cross-workspace authority와 Implementation `CLEAR`를 의미하지 않는다. OQ-003
liveness evidence는 아래의 user decision과 Runtime ADR로 후속 반영됐다.

### Phase 0 OQ-003 — VERIFIED DECISION

2026-08-22에 사용자는 OQ-003 C-01인 v1 required background daemon/host-owned sidecar
제외를 확정했다. stdio MCP 또는 단발 CLI/application-service 호출을 기본으로 하고,
explicit heartbeat·checkpoint·grace·safe takeover protocol을 사용한다. 결정은
[USER-DECISION-OQ003-001](../research/phase-0/evidence/OQ-003/USER-DECISION-RECEIPT-001.md)과
Accepted [ADR-0012](../adr/0012-no-background-daemon-v1.md)에 기록했다.

이 결정은 fixture-local logical-clock liveness evidence를 production clock, SQLite
transaction, cross-workspace authority, exact threshold 또는 installed-host E2E로
승격하지 않는다. At that observation point OQ-008/OQ-009와 나머지 Phase 0 decision,
product Implementation `HOLD`는 유지했다.

### Phase 0 OQ-004 lifecycle recovery fixture — VERIFIED OBSERVATION

2026-08-22에 당시 기준으로 기존 OQ-003/OQ-008/OQ-009 evidence runner를 변경하지 않고,
[`FX-LIFECYCLE-RECOVERY-002`](../research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/README.md)를
OQ-004 follow-up fixture로 추가했다. 이 fixture는 C-01/C-02/C-03 후보별
`FAILED`·`CANCELLED` recovery, explicit user receipt guard, completion exposure guard와
failure candidate 승격 차단을 비교 관찰한다.

정확한 command는 다음과 같다.

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/runner.py
    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/runner.py

compile은 exit `0`이었다. fixture를 두 번 실행해 각각 exit `0`, 14/14 assertions와
`all_assertions_pass=true`를 확인했고, 두 raw JSON output을 `cmp`로 비교해 동일성을
확인했다. C-01/C-02의 explicit-receipt `FAILED → REOPENED`, C-02의
`CANCELLED → REOPENED`, receipt 없는 reopen 거부, checkpoint/lease guard와
independent evidence 없는 candidate 비승격과
`READY_TO_COMPLETE` → final run projection → terminal checkpoint → lease release →
`COMPLETED` 노출의 synthetic 순서를 관찰했다. 결과는
[`RUN-OQ004-002`](../research/phase-0/evidence/OQ-004/FX-LIFECYCLE-RECOVERY-002/RUN-OQ004-002/RUN.md)에
보존했다.

이 fixture output 자체는 후보 비교 evidence이며 user decision을 대신하지 않는다. C-01
선택과 Lifecycle ADR 반영은 아래의 별도 decision section에 기록한다. Plan Gate actor
policy, production transaction과 Implementation `CLEAR`는 이 observation으로 확정하지
않는다.

### Phase 0 OQ-004 — VERIFIED DECISION

2026-08-22에 사용자는 앞서 제시된 OQ-004 C-01 권고안을 기준으로 진행하도록 확인했다.
task-level `FAILED`는 명시적인 user reopen receipt가 있을 때만 `REOPENED`로 전환하고,
자동 reopen은 허용하지 않는다. `CANCELLED`는 terminal이며 `CANCELLED → REOPENED`는
허용하지 않는다. attempt-level `FAIL`은 task-level `FAILED`와 구분한다.

결정은 [USER-DECISION-OQ004-001](../research/phase-0/evidence/OQ-004/USER-DECISION-RECEIPT-001.md)과
Accepted [ADR-0013](../adr/0013-task-lifecycle-recovery.md)에 기록했다. OQ-004 packet은
`resolved`로 동기화했으며, C-02/C-03은 선택하지 않았다.

이 결정은 follow-up fixture의 14/14 deterministic assertion과 두 raw JSON output의
`cmp` 동일성에 근거하지만, production persistence, receipt validation, crash replay,
lease takeover과 전체 state graph를 증명하지 않는다. At that observation point OQ-008 Plan
Gate actor/risk policy, OQ-009 completion atomicity와 제품 Implementation `HOLD`는 유지했다.

이번 decision sync에서 `python3 -m json.tool docs/research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/input/fixture.json >/dev/null`,
YAML frontmatter parse, read-only Markdown local-link check와 `git diff --check --`를
실행했다. JSON/frontmatter parse와 diff check는 exit `0`이었고, Markdown check는
`markdown_files=79`, `local_links=327`, `errors=0`을 반환했다.

### Phase 0 OQ-008 approval-policy fixture — VERIFIED OBSERVATION

2026-08-22에 기존 shared lifecycle fixture와 별도로
[`FX-PLAN-APPROVAL-POLICY-001`](../research/phase-0/fixtures/FX-PLAN-APPROVAL-POLICY-001/README.md)을
추가해 OQ-008의 세 candidate를 같은 합성 scenario에 대입했다. C-01은 current digest의
모든 scenario에서 `user`, C-02는 routine에서 `policy`·`user_sensitive`에서 `user`,
C-03은 routine read-only에서 `policy`·side effect와 sensitive boundary에서 `user`를
관찰하도록 비교했다. stale digest는 세 candidate 모두 `DENIED/none`이었다.

정확한 fixture command는 다음과 같다.

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-PLAN-APPROVAL-POLICY-001/runner.py

입력 JSON parse와 runner compile은 각각 exit `0`이었다. fixture를 두 번 실행한 paired
검사는 exit `0`, 각 실행 31/31 assertions와 `all_assertions_pass=true`, stdout/stderr
byte-identical을 확인했다. `selected_candidate`는 `null`이었다. runner SHA-256은
`a8d5b86389230531ddf0afe7c956882c730a67d9844d1b2cdec93c6cd59c5e5f`, input은
`1b3e1106847ceb3d57119ba82d84f86326723d289b880f1cc3d341f2012f7654`, paired stdout는
`cd964c1db1a12f390301896dd92a89386fcef17e7897f3c7eb70246936513684`이다. redacted
execution records는 [RUN-OQ008-002-A](../research/phase-0/evidence/OQ-008/FX-PLAN-APPROVAL-POLICY-001/RUN-OQ008-002-A/RUN.md)와
[RUN-OQ008-002-B](../research/phase-0/evidence/OQ-008/FX-PLAN-APPROVAL-POLICY-001/RUN-OQ008-002-B/RUN.md)에
보존했다.

이 결과는 candidate comparison evidence일 뿐 OQ-008 policy 선택, 일반 risk threshold,
receipt schema, production enforcement 또는 Implementation `CLEAR`를 의미하지 않는다.
OQ-008은 `blocked / user decision pending`으로 유지했다. At that observation point의
다음 목표는 OQ-009 completion/lease atomicity crash-point replay evidence 작성이었고,
그 결과는 아래의 OQ-009 VERIFIED DECISION section에 기록돼 있다.

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

### Phase 0 P0-08 #20 threat model·권한 정책 — VERIFIED DECISION

2026-08-21에 [OQ-015 threat model packet](../research/phase-0/OQ-015-threat-model-permission-policy.md),
Accepted [ADR-0009](../adr/0009-threat-model-permission-boundaries.md)와 durable user decision receipt
([USER-DECISION-OQ015-001](../research/phase-0/evidence/OQ-015/USER-DECISION-RECEIPT-001.md))와 disposable
`FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001`을 추가했다. OQ-015는 앞선 packet의
cross-concern owner/authority와 control-to-fixture 연결을 기록하며, 사용자 결정으로 C-01
fail-closed boundary, sensitive-action receipt와 secret fail-closed handling을 채택했다.
일반 `PLAN_APPROVED` actor/risk tier와 production enforcement는 OQ-008 및 후속 단계에 남아
있고 Implementation `HOLD`를 유지한다.

정확한 fixture command를 최종 runner source hash 기준으로 두 번 실행했다.

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/runner.py

RUN-OQ015-003은 2026-08-21T06:41:37Z–06:41:38Z, RUN-OQ015-004는
2026-08-21T06:41:38Z에 실행했다. 두 실행 모두 exit `0`, 17/17 assertions와
`all_assertions_pass=true`를 보고했고 raw JSON output은 byte-identical이었다. 관찰된 control은 target-root parent/symlink escape 거부,
user receipt 없는 authority/scope·external write 및 stale digest/approval 거부, two-writer
차단과 observer read, forbidden capability 차단, synthetic secret redaction, worker
self-verification/acting evidence 누락 차단, candidate memory 비노출과 corrupt memory
`HOLD`다.

보존한 artifact hash는 다음과 같다.

- fixture runner: `b8f926b12e08ce234e608818598e0fbb81efda25725cb633d7a68f0784b1398a`
- fixture input: `41dfd917257a4ddc34c3d156afed1a6aa5b6a3c1a81c84888cfb218a6cea06fb`
- OQ-015 redacted result manifest: `e5d7afbd810487fb7847f48a035d329b17e292b2e29695169942e4c4a1a00ce7`

추가 검증은 `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile .../runner.py`와
`python3 -m json.tool .../input/fixture.json >/dev/null`로 각각 exit `0`이었다. fixture는
network/external write, credentials, plugin install, daemon, target `.geness/`와 실제
`GENESS_HOME`을 사용하지 않았다. multi-process lease/crash, installed-host sandbox,
secret corpus, exact risk/receipt schema와 user decision은 여전히 open이다.
최종 `git diff --check --`도 exit `0`이었다. `node /tmp/geness-p0-06-markdown-check.mjs`는
exit `0`, `markdown_files=67`, `local_links=223`, `local_anchor_links=25`,
`fence_delimiters=154`, `trailing_whitespace=0`, `errors=[]`를 반환했다.

사용자 decision receipt와 정본 sync 이후 current worktree에서도 같은 fixture를 두 번 재실행했다.
두 실행 모두 exit `0`, 17/17 assertions와 `all_assertions_pass=true`였고 raw output은
byte-identical이었다. `node /tmp/geness-p0-06-markdown-check.mjs`는 exit `0`,
`markdown_files=69`, `local_links=240`, `local_anchor_links=25`, `fence_delimiters=154`,
`trailing_whitespace=0`, `errors=[]`를 반환했으며 `git diff --check --`도 exit `0`이었다.

### Phase 0 OQ-009 — VERIFIED DECISION

2026-08-22에 OQ-009 disposable fixture를 crash-point matrix로 확장했다. C-01/C-02/C-03의
`after_projection`, `after_lease_release`, `after_terminal_checkpoint`,
`after_runtime_commit`을 모두 재현했으며, 두 실행 모두 exit `0`, 43/43 assertions,
`all_assertions_pass=true`와 byte-identical stdout을 반환했다. C-01은 4/4 crash state에서
unsafe invariant가 없었고, C-02는 terminal checkpoint 전 lease release, C-03은 runtime
commit 전 completion exposure를 관찰했다. 12개 row 모두 operation-id replay 뒤 안전한
상태로 수렴했고 두 번째 replay도 동일했다.

decision-ready recommendation과 고정된 fixture 결과가 delegated AUTOPILOT 조건을 모두
충족해 C-01을 채택했다. [ADR-0014](../adr/0014-completion-lease-atomicity.md)와 OQ-009
packet에 결정 receipt·trade-off·risk를 기록했으며, final projection은 runtime completion
authority가 아니고 terminal checkpoint·completion record·lease release는 한 runtime
transaction에 기록한다. 이 결정은 production SQLite/WAL/multi-process crash 검증이나
Implementation `CLEAR`를 의미하지 않는다.

증거는 [RUN-OQ009-002-A](../research/phase-0/evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/RUN-A.md),
[RUN-OQ009-002-B](../research/phase-0/evidence/OQ-009/FX-LIFECYCLE-LEASE-COMPLETION-001/RUN-OQ009-002/RUN-B.md)와
`result.json`에 보존했다. runner SHA-256은
`9c3361989c10fd361a67e0432c88a6573ebfe399f639b791f8442623adb1cc54`, input은
`bc5d871017fd45b8aeed16d2c71a1587992ee4a4e3affaab300c9e319e2b8147`, result는
`219b98005ecac98195dbe4c29ba4b8a5b58d9825dfbb84e6e8367d715269e4db`다. 최종 검사에서
fixture/result JSON parse, `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile runner.py`,
fixture 두 번 실행과 `cmp`, `git diff --check --`가 모두 exit `0`이었다. Read-only inline
Markdown 검사는 `markdown_files=89`, `frontmatter_files=35`, `local_links=396`,
`local_anchor_links=29`, `fence_delimiters=156`, `errors=[]`를 반환했다.

### Phase 0 P0-GATE #21 — HOLD audit

2026-08-21에 [Phase 0 Gate audit](../research/phase-0/PHASE-0-GATE-AUDIT-001.md)을
merged main `23a6e75` 기준으로 수행했다. OQ-002 command API 14 assertions, lifecycle/lease
7, identity/schema/digest/config 30, memory/retention/bootstrap 43, host/command surface 83,
OQ-015 threat model 17 assertions를 각각 재실행해 모두 exit `0`과
`all_assertions_pass=true`를 확인했다.

현재 Gate 판정은 `HOLD`다. OQ-005~OQ-014 중 남은 user decision receipt가 있고,
OQ-004/OQ-008은 packet-level blocker이며, OQ-009는 ADR-0014까지 정렬됐지만 production
evidence와 다른 Phase 0 결정이 남아 있다. Implementation `HOLD`를 해제할 근거는 없다.

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
| Controller runtime | Accepted — Go + Go modules + CGO + `sqlite_fts5` | [ADR-0010](../adr/0010-controller-runtime-go.md) |
| Canonical command API | Accepted — shared application service + thin CLI/MCP transports | [ADR-0011](../adr/0011-canonical-command-api.md) |
| Lease liveness / daemon policy | Accepted — v1 required daemon/host-owned sidecar 제외, explicit heartbeat/checkpoint/grace/takeover | [ADR-0012](../adr/0012-no-background-daemon-v1.md) |
| Lifecycle | Proposed, OQ-004 C-01 recovery policy Accepted; other Phase 0 decisions open | [ADR-0013](../adr/0013-task-lifecycle-recovery.md), [02_TASK_LIFECYCLE](../02_TASK_LIFECYCLE.md) |
| Storage boundary | Accepted, schema TBD | [ADR-0002](../adr/0002-project-and-local-state-boundary.md) |
| Dual-host boundary | Accepted, manifest prototype TBD | [ADR-0001](../adr/0001-dual-host-shared-core.md) |
| Interview principles | Accepted, implementation TBD | [ADR-0004](../adr/0004-ouroboros-interview-principles.md) |
| Failure learning | Accepted principle, thresholds TBD | [ADR-0003](../adr/0003-failure-candidate-is-not-memory.md) |
| Threat model / permission boundary | Accepted baseline, exact risk/detector/production enforcement TBD | [ADR-0009](../adr/0009-threat-model-permission-boundaries.md) |
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

OQ-009가 정렬됐으므로, 다음 하나의 검증 가능한 목표는 P0-05 identity/schema/digest
queue의 OQ-005 recommendation을 같은 delegated-decision evidence gate로 재검증하는
것이다. 제품 scaffold와 Implementation `CLEAR`는 남은 blocking decision과 production
evidence 전까지 시작하지 않는다.

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
