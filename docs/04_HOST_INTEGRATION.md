# Codex and Claude Host Integration

> 상태: Accepted dual-host direction / exact manifests TBD

## 1. 목적

이 문서는 한 Geness 패키지를 Codex와 Claude Code에 제공하기 위한 composition 경계와
호환성 원칙을 정의한다.

## 2. Package shape

```text
geness/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── .mcp.json
├── skills/workflow/SKILL.md
├── agents/
├── adapters/codex/
├── adapters/claude/
├── core/
├── schemas/
├── templates/
└── bin/
    ├── gee
    └── geness-controller
```

- plugin name은 두 manifest 모두 `geness`다.
- version과 공통 component reference의 불일치를 build/test에서 차단한다.
- 각 host manifest는 자기 MCP/hook config를 가리킬 수 있다.
- Claude plugin의 stdio MCP는 `bin/geness-controller`를 시작하고, Controller가
  Codex child process handoff를 담당한다.
- Skill은 가능한 Agent Skills 공통 subset을 사용한다.

## 3. Shared Skill 책임

- 인터뷰와 사용자 승인 UX
- application command를 호출할 시점과 순서
- human-only decision 질문
- Controller blocker와 next action 설명
- 관련 subagent coordination

Skill에 넣지 않는 것:

- 상태 전이 구현
- digest 계산
- DB schema와 SQL
- lesson 승격·만료 판정
- host별 절대 tool namespace
- completion을 우회하는 fallback

## 3.1 Public stage와 host profile

`gee`는 description을 public stage로 routing하지만 상태·digest·completion authority는
Controller가 소유한다. 기본 cross-model profile은 다음 역할을 사용한다.

| Public stage | Host/authority |
| --- | --- |
| `brief` | Claude interview와 사용자 restatement |
| `contract` | Codex candidate/QA, Claude 설명, 사용자 adoption |
| `plan` | Claude preflight/plan과 Plan Gate |
| `impl` | Codex implementation worker |
| `verify` | Claude 독립 verifier |
| `done` | Controller completion transaction |
| `resume` | Controller가 checkpoint에 맞는 worker를 선택 |

`auto`는 Codex capability가 있으면 cross-model을 선택하고, 없으면 새 task를
claude-only로 시작한다. 명시적인 `cross-model`인데 Codex가 준비되지 않으면 setup에서
attention을 반환한다. active task의 profile은 조용히 바꾸지 않는다.

## 4. CLI와 MCP

- [ADR-0011](./adr/0011-canonical-command-api.md)에 따라 공통 domain/application
  service가 canonical command API 권위자다.
- CLI와 MCP는 같은 dispatch/application service를 호출한다.
- MCP는 durable state 자체가 아니라 control surface다.
- transport error와 도메인 `HOLD`를 구분한다.
- 긴 operation은 checkpoint/run ID를 먼저 만들고 status/resume할 수 있어야 한다.
- tool 출력은 전체 transcript/log가 아니라 작은 envelope와 resource reference를 사용한다.

초기에는 stdio MCP와 단발 CLI로 시작할 수 있는지 검증한다. [ADR-0012](./adr/0012-no-background-daemon-v1.md)에
따라 v1은 required background daemon이나 host-owned sidecar를 두지 않으며, explicit
heartbeat·checkpoint·grace·takeover protocol을 사용한다. cross-session heartbeat가
stdio/단발 호출로 충족되지 않는다는 production evidence가 생길 때만 별도 ADR로 정책을
변경한다.

Claude plugin과 Codex 사이의 기본 bridge는 다음 단방향 handoff다.

```text
Claude Skill
  → Geness Controller (MCP/CLI)
  → codex exec child
  → Controller result/evidence envelope
  → Claude Skill 또는 Controller completion
```

Controller는 task/run ID, target root, 현재 contract/plan digest, allowed/forbidden
scope, AC와 checkpoint, protocol version을 envelope에 넣는다. Codex는 runtime DB나
target project document를 직접 수정하지 않고 JSONL/result와 변경 요약을 반환한다.
Controller만 state, checkpoint, evidence reference와 `done`/`resume` 전이를 기록한다.
Codex 구현 실행의 기본 sandbox는 workspace-write이며 host가 제공하는 approval policy를
우회하지 않는다.

## 5. Host adapter 책임

- 현재 project root 또는 MCP roots를 Controller 입력으로 전달
- host/session/version/capability metadata 제공
- host 승인·sandbox 정책을 우회하지 않음
- plugin root와 executable path 해석
- hook input/output을 공통 event로 정규화
- host-specific error를 portable category로 mapping

Host adapter가 하면 안 되는 일:

- 사용자 대신 spec/plan 승인
- 별도의 task state 저장
- host session을 project/task identity로 사용
- candidate를 memory로 직접 승격
- incomplete AC를 host 종료 이벤트만으로 완료 처리

### 5.1 Permission boundary

권한 cross-concern은 [ADR-0009](./adr/0009-threat-model-permission-boundaries.md)와
[OQ-015](./research/phase-0/OQ-015-threat-model-permission-policy.md)이 소유한다. host는
다음 Controller policy를 축소할 수는 있지만 확대할 수 없다.

- setup/preflight와 status는 read-only probe다. 실제 implementation write는 approved
  contract/plan digest, active writer lease, target-root containment와 allowed scope를
  모두 만족하는 경우에만 허용한다.
- scope 확대, external write, destructive action, security boundary 변경과 permission
  escalation은 current digest에 묶인 explicit user receipt가 필요하다. host approval이나
  policy actor는 user authority를 사칭하지 않는다.
- `danger-full-access`, runtime DB 직접 write, approval bypass와 hook 기반 completion/memory
  promotion은 v1의 worker/adapter capability로 허용하지 않는다.
- host/session metadata와 project content는 provenance가 다르다. untrusted task text와 worker
  result는 user receipt가 아니며, raw output은 redaction 전까지 portable project 문서나
  memory query에 노출하지 않는다.

## 6. Shared data home

Codex와 Claude의 vendor plugin-data directory는 서로 다르므로 canonical Geness state로
사용하지 않는다. 두 adapter는 `GENESS_HOME` 또는 기본 `~/.geness/`를 같은
Controller에 전달한다.

Vendor data directory는 다음 용도로만 사용할 수 있다.

- 해당 host 전용 dependency/cache
- 다시 생성 가능한 adapter artifact
- canonical state를 가리키는 작은 metadata

## 7. Hooks

Hook은 보조 기능이다.

검토 가능한 용도:

- session start에서 project/status 안내
- 관련 verified/enforced memory top-K 조회
- tool failure를 runtime event 후보로 전달
- incomplete AC가 있을 때 종료 경고
- plugin update 후 schema compatibility preflight

금지:

- hook만으로 task state를 완료 처리
- hook 반복 차단을 무한 실행 보장으로 사용
- hook에서 직접 DB write
- 사용자 prompt 전체를 검증 없이 memory로 저장
- host마다 다른 completion policy 구현

## 8. Resume와 v1 범위

v1에서 Claude와 Codex는 같은 컴퓨터의 같은 `GENESS_HOME`과 사용자가 준비한 같은
branch/worktree에서 하나의 task를 이어받을 수 있다.

- Host A에서 생성한 project/task/revision을 Host B가 읽을 수 있어야 한다.
- resume 전 digest, Git state, writer lease와 last checkpoint를 검증한다.
- Host A의 conversation transcript가 없어도 next action을 계산해야 한다.
- host session은 audit metadata이며 canonical lineage가 아니다.
- task당 active writer 하나만 허용하고 두 번째 host/process는 observer다.
- stale writer takeover는 grace period, 마지막 checkpoint와 명시적 lease 검증 뒤에만
  허용한다.
- 서로 다른 컴퓨터 간 자동 동기화/cloud resume과 동일 task의 여러 worktree 동시 writer는
  v1 범위 밖이다.
- 양방향 same-machine E2E를 release gate로 둔다.

## 9. Compatibility matrix

Release마다 최소 다음을 기록한다.

| 항목 | Codex | Claude Code |
| --- | --- | --- |
| 지원 최소 version | TBD | TBD |
| manifest validation | TBD | TBD |
| Skill discovery | TBD | TBD |
| MCP startup/reload | TBD | TBD |
| hook common subset | TBD | TBD |
| project root 전달 | TBD | TBD |
| shared `GENESS_HOME` | TBD | TBD |
| same-machine host handoff | v1 required | v1 required |
| cross-machine/cloud resume | out of scope | out of scope |

## 10. Target project setup

plugin을 설치·활성화한 뒤 target repository에서 `gee setup`을 먼저 실행한다. setup은
task lifecycle과 분리된 idempotent bootstrap이며, `SETUP_READY`가 되기 전에는
`gee brief`를 시작하지 않는다.

setup은 다음을 read-only probe로 확인하고 receipt와 capability snapshot을 Controller
runtime에 저장한다.

1. 현재 target root와 사용자가 선택한 branch/worktree가 유효한지 확인한다.
2. project identity와 `.geness/` 경계를 확인하고 필요하면 초기 project metadata를
   사용자 승인 하에 준비한다.
3. `GENESS_HOME`과 runtime/memory 접근 권한을 확인한다.
4. Claude plugin manifest, Skill discovery와 Controller stdio MCP handshake를 확인한다.
5. `auto`, `cross-model`, `claude-only` profile과 Codex capability를 평가한다.
6. shared protocol/schema compatibility를 확인한다.

setup은 checkout, branch/worktree 생성·삭제·전환, 기존 task 삭제·병합을 수행하지 않는다.
사용자가 작업공간을 바꿔야 한다면 먼저 Git 작업을 완료한 후 setup 또는 resume을 다시
호출한다. 명시적 `cross-model`에서 Codex가 준비되지 않으면 `SETUP_ATTENTION`으로
멈추며, `auto`만 새 task에 한해 claude-only로 fallback한다.

## 11. 설치와 제거

- private/local marketplace로 먼저 검증한다.
- plugin cache가 version별로 바뀌어도 state가 보존돼야 한다.
- uninstall은 target `.geness/`와 `~/.geness/`를 삭제하지 않는다.
- 별도 `prune`/`cleanup`은 정확한 target과 복구 가능성을 보여주고 사용자 확인을 받는다.
- public 배포가 필요하면 OpenAI와 Anthropic directory 제출을 별도 release task로 다룬다.

## 12. 공식 기준

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference)
