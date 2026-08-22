# FX-LIFECYCLE-RECOVERY-002

## fixture_id

`FX-LIFECYCLE-RECOVERY-002`

## packet_id / question_id

`OQ-004`

## purpose

이 disposable fixture는 OQ-004의 미검증 recovery 경계를 후보별로 비교 관찰한다.
`FAILED`와 `CANCELLED`의 reopen 후보, 명시적 user receipt guard, completion 노출
순서와 failure candidate의 memory 승격 방지를 검증한다.

결과는 Phase 0 research evidence이며 제품 Controller 구현, Lifecycle ADR 또는 사용자
결정이 아니다.

## scope and non-goals

- 포함: C-01/C-02/C-03 후보별 `FAILED`·`CANCELLED` recovery 비교
- 포함: attempt-level `FAIL`과 task-level `FAILED`의 분리 관찰
- 포함: terminal checkpoint·lease release 이후에만 `COMPLETED`를 노출하는 guard
- 포함: failure event → candidate 순서와 independent evidence 없는 승격 차단
- 비목표: 후보 선택, exact state machine 확정, Plan Gate actor/risk policy 결정
- 비목표: production persistence, SQLite transaction, crash replay, lease takeover,
  product scaffold와 Implementation `CLEAR`

## exact command

이 디렉터리에서 다음 명령을 실행한다.

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

## expected observation

- C-01/C-02는 명시적 user receipt가 있을 때 `FAILED → REOPENED`를 허용하고,
  C-03은 terminal 후보로 거부한다.
- C-01/C-03은 `CANCELLED → REOPENED`를 terminal 후보로 거부하고, C-02만 명시적
  user receipt가 있을 때 허용한다.
- receipt 없는 reopen은 후보와 무관하게 거부한다.
- attempt-level `FAIL`은 즉시 task-level `FAILED` 또는 durable lesson이 되지 않는다.
- terminal checkpoint가 없거나 active lease가 남아 있으면 `COMPLETED` 노출을 거부한다.
- synthetic completion 순서는 `READY_TO_COMPLETE` → final run projection → terminal
  checkpoint → lease release → `COMPLETED` 노출이다.
- failure candidate는 independent evidence 전에는 `verified` 또는 일반 memory query에
  노출되지 않는다.

## isolation and network policy

- Python standard library만 사용한다.
- network, credentials, target repository, `.geness/`, 실제 `GENESS_HOME`과 external
  write를 사용하지 않는다.
- 입력과 결과는 deterministic JSON이다.

## retention plan

- tracked: README, runner.py와 input/fixture.json
- packet: 실제 실행 후 redacted RUN record와 source/input hash
- local-only 또는 discarded: raw stdout/stderr
