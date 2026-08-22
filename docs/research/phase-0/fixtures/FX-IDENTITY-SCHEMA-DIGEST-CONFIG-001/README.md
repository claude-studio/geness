# FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001

## fixture_id

FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001

## packet_id / question_id

OQ-005, OQ-006, OQ-007, OQ-013

## purpose

이 disposable fixture는 project/workspace identity 관계, Markdown frontmatter와 임시
SQLite projection의 의미 보존, stale write 거부, contract/plan digest canonicalization과
portable/local config 경계를 최소 입력으로 관찰한다.

결과는 Phase 0 research evidence이며, 제품 Controller 구현이나 production schema를
대신하지 않는다. OQ-005와 OQ-006의 별도 delegated decision receipt·ADR은 이 fixture의
관찰을 근거로 하지만 fixture 자체가 그 결정을 수행하지 않는다.

## scope and non-goals

- 포함: local Git clone/fork/rename/worktree probe, 합성 project/workspace ID 관계,
  fixture-local frontmatter parser와 SQLite round-trip, revision guard, digest golden
  vector와 config boundary assertion
- 입력: `input/fixture.json`의 결정론적 합성 payload
- 비목표: 제품 언어, package manager, runtime, production schema, migration, daemon,
  plugin scaffold, target `.geness/`, 실제 `GENESS_HOME` 또는 사용자 decision receipt 선택
- Python과 SQLite는 fixture 도구일 뿐 Controller 언어·DB schema 추천이 아니다.
- fork는 Git의 local primitive가 아니므로 local clone과 synthetic explicit detach marker로
  project lineage 정책의 관찰 경계를 표시한다.

## category

Disposable Phase 0 identity/schema/digest/config evidence fixture.

## exact command

이 디렉터리에서 다음 명령을 실행한다.

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

runner는 standard library와 local `git` executable만 사용하며, Git repository와 SQLite는
per-run temporary directory 또는 in-memory DB에만 만든다.

## expected observation

- clone과 worktree는 synthetic project ID를 공유하고 workspace ID는 구분한다.
- folder rename은 project/workspace ID를 유지하는 explicit metadata 경로를 관찰한다.
- fork와 같은 이름의 별도 repository는 explicit detach/rekey 없이는 동일 project로 취급하지
  않는다.
- frontmatter를 임시 SQLite projection으로 round-trip해도 semantic field가 보존된다.
- current revision에 대한 accepted write 뒤 stale revision write는 DENIED되고 state를
  바꾸지 않는다.
- canonical semantic JSON payload의 key ordering과 editorial body 변경은 digest를 바꾸지
  않지만, contract/plan semantic 변경은 digest를 바꾼다.
- portable project/task projection에는 runtime path, host session과 secret field가 없다.

## isolation and network policy

- Python standard library와 local `git`만 사용한다.
- Git probe는 `tempfile.TemporaryDirectory` 아래에서만 `git init`, local `git clone`,
  `git worktree add`와 remote metadata 변경을 수행한다.
- network, GitHub remote, target repository, `.geness/`, 실제 `GENESS_HOME`, credentials와
  external writes를 사용하지 않는다.

## cleanup boundary

runner가 만든 temporary Git repositories, renamed folder, worktree와 in-memory SQLite만
process 종료 시 정리한다. repository, target, home, branch와 worktree를 정리하거나
변경하지 않는다.

## retention plan

- tracked: README, runner.py와 input/fixture.json
- packet: 실제 실행 후 redacted result manifest와 RUN record
- local-only 또는 discarded: raw stdout/stderr, temporary Git state와 DB

## parser limitation

frontmatter parser는 이 fixture가 고정한 `key: JSON scalar/object/array` subset만 읽는다.
full YAML compatibility나 product serialization grammar를 주장하지 않으며, 그 한계는
OQ-006/007 packet의 risk로 기록한다.
