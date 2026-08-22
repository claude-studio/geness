# FX-LEASE-LIVENESS-TAKEOVER-001

## fixture_id

`FX-LEASE-LIVENESS-TAKEOVER-001`

## packet_id / question_id

OQ-003

## purpose

이 disposable fixture는 실제 두 child process가 하나의 합성 lease state를 공유하는
상황에서 heartbeat, grace period, writer interruption과 stale-writer takeover를
관찰한다. 결과는 daemon/no-daemon 후보의 운영 비용을 자동 선택하지 않으며, 제품
Controller나 lease policy의 구현이 아니다.

## scope and non-goals

- 포함: 두 process, logical clock, heartbeat 갱신, grace 전 takeover 거부, process
  interruption, grace 이후 takeover, 새 owner heartbeat
- 비목표: background daemon/sidecar 설치·선택, production SQLite schema, cross-workspace
  authority, 실제 `GENESS_HOME`, plugin scaffold와 user decision receipt
- Python은 fixture runner와 child process 도구일 뿐 Controller 언어를 재선택하지 않는다.
- POSIX `fcntl` file lock은 fixture-local serialization을 위한 도구이며 production
  locking contract가 아니다.

## category

Disposable Phase 0 runtime/liveness evidence fixture.

## inputs and preconditions

- `input/fixture.json`의 synthetic project/task, heartbeat interval `2`와 grace period `3`
- runner가 생성한 per-run temporary state file과 lock file
- runner parent가 두 child process를 시작하고 logical time을 명시적으로 전달

## exact command

repository root에서 다음 명령을 실행한다.

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001/runner.py

## expected observation

- writer-A가 logical time `0`에 lease를 획득한다.
- writer-A가 time `2`에 heartbeat를 갱신하고 grace deadline을 `5`로 연장한다.
- observer-B는 time `3`, `4`와 grace deadline인 `5`에 takeover를 시도해도 `DENIED`다.
- writer-A process가 abrupt interruption으로 종료된 뒤에도 time `4`에는 takeover가
  `DENIED`다.
- time `6`에 observer-B의 stale takeover가 `ALLOWED`가 되고, B의 time `7` heartbeat가
  새 lease owner로 허용된다.
- runner는 daemon process를 시작하지 않으며, 두 child process의 PID가 서로 다르다.

## expected runner exit status

`0` when all expected observations pass. The runner exits non-zero for a fixture or
environment error; it does not convert an unexpected observation into success.

## isolation and network policy

- Python standard library만 사용한다.
- state와 lock은 OS temporary directory 아래에만 생성한다.
- target repository, target `.geness/`, 실제 `GENESS_HOME`, credentials와 network를
  사용하지 않는다.
- 외부 write와 product state mutation은 없다.

## cleanup boundary

runner가 만든 child process, temporary state, lock과 atomic-write 임시 파일만 정리한다.
repository, target, home, branch와 worktree는 정리하지 않는다.

## retention plan

- tracked: README, runner.py와 input/fixture.json
- packet: redacted deterministic result manifest와 execution record
- discarded: raw child stdout/stderr와 temporary state/lock
