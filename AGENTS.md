# AGENTS.md — Geness 에이전트 작업 지침

이 파일은 Codex와 Claude Code의 새 세션이 같은 출발점에서 일하기 위한 최소 지침이다.
상세 계약은 `docs/`가 소유한다. 충돌하면
[`docs/README.md`](./docs/README.md)의 진실의 원천 우선순위를 따른다.

## 프로젝트 정체

Geness는 반복 질문으로 사용자의 암묵지를 드러내고, 승인된 문서를 실행 계약으로
고정하며, AC evidence가 충족될 때까지 실행·검증·재개하는 dual-host control plane이다.
Ouroboros에서 관찰한 인터뷰 원칙을 참고해 독립 설계하지만 Ouroboros 전체를 복제하거나
호환 구현하지 않는다.

> Geness turns tacit decisions into verified work.

사용자-facing workflow는 `gee setup → brief → contract → plan → impl → verify → done`이며,
수정 가능한 검증 실패는 bounded `resume`으로 이어진다. `brief/plan/verify`는 Claude,
`contract/impl`은 기본 cross-model profile에서 Codex가 담당한다. `auto`는 Codex가
없을 때 새 task에 한해 claude-only로 fallback한다.

## 세션 시작 절차

작업 전 다음을 순서대로 수행한다.

1. [`docs/00_GENESS.md`](./docs/00_GENESS.md)를 끝까지 읽는다.
2. [`docs/progress/README.md`](./docs/progress/README.md)의 검증된 현재 상태와
   Documentation/Implementation HOLD 또는 CLEAR를 확인한다.
3. 요청과 관련된 Architecture, Lifecycle, Storage, Host Integration과 Stage Guide를
   읽는다.
4. 관련 [Accepted ADR](./docs/adr/README.md),
   [Open Questions](./docs/research/OPEN_QUESTIONS.md)와
   [`PLAN.md`](./docs/PLAN.md)의 현재 Phase/Gate를 확인한다.
5. Git status와 사용자가 남긴 기존 변경을 확인한다.
6. 시작 전에 현재 Phase/Stage, Goal, Non-goal, authority, allowed scope와 verification
   방법을 다시 표현한다.

이 질문에 답할 수 없으면 구현 전에 문맥을 더 읽는다.

- 지금 구현하려는가, 조사·계획·문서화하려는가?
- 현재 Progress가 그 작업을 CLEAR했는가?
- 사용자 판단과 코드에서 확인할 사실은 각각 무엇인가?
- 어느 artifact가 해당 concern의 canonical owner인가?
- 무엇을 실제 evidence로 확인해야 완료인가?

## 현재 HOLD

`docs/progress/README.md`가 바뀌기 전까지 **제품 구현은 HOLD**다. 문서 foundation,
공식 계약 조사와 사용자가 명시한 범위의 spike 외에 Controller 언어, package manager,
schema, daemon과 plugin scaffold를 임의로 선택하거나 생성하지 않는다.

- Progress의 project-level Implementation HOLD/CLEAR와
  [`docs/02_TASK_LIFECYCLE.md`](./docs/02_TASK_LIFECYCLE.md)의 개별 task Gate를 구분한다.
- `CLEAR`는 entry condition을 실제 evidence로 충족한 경우에만 선언한다.
- PLAN checkbox, agent confidence와 완료 보고는 evidence가 아니다.
- `HOLD`와 `BLOCKED`는 transport failure가 아니라 정상적인 domain result일 수 있다.

## 어기면 안 되는 원칙

- consequential change는 코드보다 관련 문서와 ADR을 먼저 갱신한다.
- 중요한 미결정이 남아 있으면 interview나 specification을 자동 종료하지 않는다.
- highest-impact gap 하나를 질문하되 ledger breadth와 human-judgment rhythm을 지킨다.
- 정확한 코드 사실을 사용자 requirement로 자동 승격하지 않는다.
- interview restatement 승인과 spec contract digest 승인을 서로 대신하지 않는다.
- 승인된 spec, 실행 가능한 AC와 유효한 digest 없이 실행하지 않는다.
- 사용자 승인 없이 requirement, AC, allowed scope 또는 completion policy를 바꾸지 않는다.
- 모든 필수 AC에 current evidence가 연결되기 전에는 완료하지 않는다.
- 승인된 scope 밖 개선, destructive action과 external write를 추론해 수행하지 않는다.
- 같은 failure fingerprint를 무한 재시도하지 않는다.
- failure candidate를 곧바로 durable memory로 승격하지 않는다.
- 대화 transcript, host session과 agent의 기억을 canonical task state로 사용하지 않는다.

## 데이터와 정본 경계

- 이 저장소의 `docs/`: Geness 제품을 개발하는 규범·계획·결정·진행·연구
- 실제 target repository의 `.geness/`: `project.json`과 portable task 계약·projection
- `~/.geness/runtime/`: mutable run, attempt, checkpoint, lease, raw evidence와 candidate
- `~/.geness/memory/`: verified lesson events와 재구축 가능한 SQLite/FTS projection
- plugin install/cache: 읽기 전용 code, Skill, schema와 template

Target `.geness/`를 Geness plugin source의 `docs/`와 혼동하지 않는다. 사용자가 대상
저장소에서 workflow를 시작하라고 하지 않은 한 이 저장소에 task artifact를 시험 삼아
생성하지 않는다. path write 전 resolved Git root와 containment를 확인하고 symlink escape,
secret log와 민감정보를 차단한다.

Geness는 사용자가 준비한 current branch/worktree를 검증하지만 checkout, branch/worktree
생성·삭제·전환을 수행하지 않는다. v1 resume은 같은 컴퓨터·같은 `GENESS_HOME`·같은
사용자 준비 worktree를 전제로 한다.

## Host-neutral Core와 subagent

- 상태 전이, digest, Gate, lease와 memory lifecycle의 권위자는 공통 Controller다.
- Codex·Claude adapter, Skill, hook, CLI와 MCP transport는 별도 canonical state나 중복
  domain rule을 소유하지 않는다.
- host hook은 workflow를 보강할 수 있지만 completion 권위자가 아니다.
- 독립적인 조사·구현·검증은 승인 범위 안에서 subagent로 병렬화할 수 있다.
- subagent와 hook은 SQLite를 직접 쓰거나 Gate를 승인하거나 task를 완료 처리하지 않는다.
- 작업 worker는 자신의 결과를 유일한 최종 verification으로 사용하지 않는다.
- subagent 결과에는 provenance, 조사/변경 범위, evidence와 미해결 blocker가 있어야 한다.

## 미확정 결정과 문서 변경

`Proposed`와 `TBD`는 규범이 아니다. 언어, schema, threshold, identity, daemon, host
계약과 일반 plan approval policy를 구현 편의로 조용히 확정하지 않는다. 안전한 조사와
prototype으로 대안을 비교한 뒤 필요한 authority가 사용자라면 결정을 요청하고,
consequential decision은 ADR로 기록한다.

작업 흐름은 다음을 기본으로 한다.

```text
Research
→ consequential decision이면 ADR
→ Constitution/Architecture/Lifecycle/Stage Guide 정렬
→ PLAN의 Phase/Gate 확인
→ CLEAR된 최소 구현
→ 실제 테스트와 사용 evidence
→ Progress 갱신
→ 문서·구현 drift 검사
```

계획은 `docs/PLAN.md`, 검증된 현재 사실은 `docs/progress/README.md`, 외부 관찰은
`docs/research/`, 채택 결정은 `docs/adr/`에 둔다.

## 외부 출처와 라이선스

Ouroboros에서 참고한 범위는
[`docs/research/OUROBOROS_REFERENCE_FINDINGS.md`](./docs/research/OUROBOROS_REFERENCE_FINDINGS.md)에
기록한다. 현재는 아이디어와 동작 원칙의 독립 재설계 단계다. 외부 코드, prompt,
template 또는 문서 문구를 복사·번안하면 같은 변경에서 원본 고정 permalink, 로컬 파일,
수정 여부와 라이선스 조치를 기록하고 필요한 저작권·허가문을 배포 artifact에 보존한다.
세부 규칙은 [Reference Policy](./docs/research/REFERENCE_POLICY.md)를 따른다.

## 구현·검증 규칙

- 관련 파일을 먼저 읽고 사용자의 기존 변경을 보존한다.
- 실제 repository에 존재하는 test/build/lint command만 실행·기록한다.
- 테스트가 없거나 실행하지 못했으면 그 사실을 명시하며 통과했다고 표현하지 않는다.
- 문서 local link, code fence, schema example과 상태 전이 drift를 함께 확인한다.
- Controller state write는 one-writer, transaction, idempotency와 migration 계약을 지킨다.
- 파괴적 Git 명령으로 사용자의 작업을 지우지 않는다.

## Git 규칙

- 커밋 제목은 `type(scope): 한국어 설명` 형식으로 작성한다.
- `type`은 `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf` 중 변경의
  성격에 맞는 값을 사용한다. `scope`는 `agents`, `research`, `core`처럼 변경을 소유하는
  가장 좁은 영역을 쓴다.
- 제목은 변경 결과를 간결하게 표현하고 마침표를 붙이지 않는다. 본문이 필요하면 변경
  이유와 영향을 한국어로 작성한다.
- `Co-Authored-By:` 등 AI attribution 목적의 trailer를 붙이지 않는다.
- 예: `docs(agents): 문서 기반 작업 지침에 Git 규칙 추가`
- 커밋 전 staged·unstaged diff와 자격증명 포함 여부를 확인하고 관련 파일만 명시적으로
  stage한다.
- 사용자가 커밋을 요청하면 별도 금지 지시가 없는 한 같은 작업에서 현재 브랜치를
  `origin`에 push한다. 커밋 요청 전에는 commit이나 push하지 않는다.
- tag, release, PR과 외부 메시지는 각각 사용자 승인 없이 만들지 않는다.

## 작업 종료 절차

1. 관련 테스트와 실제 사용 경로를 실행하고 evidence를 확인한다.
2. 변경한 계약과 구현이 관련 문서·ADR과 일치하는지 검사한다.
3. `progress/README.md`에는 계획이 아니라 검증된 사실과 실제 command만 갱신한다.
4. 열린 HOLD, blocker, 미실행 검증과 사용자의 남은 결정을 명시한다.
5. 다음 하나의 검증 가능한 목표를 남긴다.
