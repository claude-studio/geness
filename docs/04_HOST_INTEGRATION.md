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
├── skills/workflow/SKILL.md
├── adapters/codex/
├── adapters/claude/
├── core/
├── schemas/
├── templates/
└── bin/geness
```

- plugin name은 두 manifest 모두 `geness`다.
- version과 공통 component reference의 불일치를 build/test에서 차단한다.
- 각 host manifest는 자기 MCP/hook config를 가리킬 수 있다.
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

## 4. CLI와 MCP

- 공통 domain/application library가 권위자다.
- CLI와 MCP는 같은 dispatch/application service를 호출한다.
- MCP는 durable state 자체가 아니라 control surface다.
- transport error와 도메인 `HOLD`를 구분한다.
- 긴 operation은 checkpoint/run ID를 먼저 만들고 status/resume할 수 있어야 한다.
- tool 출력은 전체 transcript/log가 아니라 작은 envelope와 resource reference를 사용한다.

초기에는 stdio MCP와 단발 CLI로 시작할 수 있는지 검증한다. background daemon은
cross-session heartbeat가 실제로 필요하고 stdio로 충족하지 못할 때만 추가한다.

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

## 8. Cross-host resume

- Host A에서 생성한 project/task/revision을 Host B가 읽을 수 있어야 한다.
- resume 전 digest, Git state, writer lease와 last checkpoint를 검증한다.
- Host A의 conversation transcript가 없어도 next action을 계산해야 한다.
- host session은 audit metadata이며 canonical lineage가 아니다.
- 양방향 E2E를 release gate로 둔다.

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
| cross-host resume | TBD | TBD |

## 10. 설치와 제거

- private/local marketplace로 먼저 검증한다.
- plugin cache가 version별로 바뀌어도 state가 보존돼야 한다.
- uninstall은 target `.geness/`와 `~/.geness/`를 삭제하지 않는다.
- 별도 `prune`/`cleanup`은 정확한 target과 복구 가능성을 보여주고 사용자 확인을 받는다.
- public 배포가 필요하면 OpenAI와 Anthropic directory 제출을 별도 release task로 다룬다.

## 11. 공식 기준

- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference)
