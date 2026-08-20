# FX-LIFECYCLE-LEASE-COMPLETION-001

## fixture_id

FX-LIFECYCLE-LEASE-COMPLETION-001

## packet_id / question_id

OQ-003, OQ-004, OQ-008, OQ-009

## purpose

이 disposable fixture는 lifecycle transition 허용·거부, stale digest 차단,
두 writer exclusive claim과 completion replay의 최소 관찰을 제공한다.
결과는 Phase 0 research evidence일 뿐 제품 Controller 구현이나 규범 채택이 아니다.

## scope and non-goals

- 포함: 합성 state transition, lease claim, terminal replay 관찰
- 입력: input/fixture.json의 결정론적 합성 사례
- 비목표: 제품 언어, package manager, runtime, production schema, daemon,
  plugin scaffold 또는 사용자 decision receipt 선택
- Python은 fixture runner 도구일 뿐 Controller 언어 추천이 아니다.

## category

Disposable Phase 0 lifecycle/runtime evidence fixture.

## exact command

이 디렉터리에서 다음 명령을 실행한다.

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

## expected observation

- INITIALIZING → INTERVIEWING은 ALLOWED로 관찰된다.
- stale digest를 가진 PLAN_APPROVED → RUNNING은 DENIED로 관찰된다.
- 금지된 INTERVIEWING → RUNNING은 DENIED로 관찰된다.
- exclusive claim을 시도한 두 writer 중 첫 번째만 ALLOWED이고 두 번째는 DENIED다.
- terminal checkpoint replay는 lease를 해제하고 COMPLETED를 만든 뒤 재실행해도
  같은 결과를 유지한다.

## isolation and network policy

- Python standard library만 사용한다.
- lease probe는 per-run tempfile 아래에만 lock file을 만든다.
- target repository, .geness/, 실제 GENESS_HOME, credentials와 network를 사용하지 않는다.
- 외부 write와 product state mutation은 없다.

## cleanup boundary

runner가 만든 tempfile과 synthetic lock file만 process 종료 시 제거한다.
repository, target, home, branch와 worktree를 정리하지 않는다.

## retention plan

- tracked: README, runner.py와 input/fixture.json
- packet: 실제 실행 후 redacted result manifest
- local-only 또는 discarded: raw stdout/stderr와 임시 lock state
