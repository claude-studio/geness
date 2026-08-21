# FX-MEMORY-RETENTION-BOOTSTRAP-001

## fixture_id

FX-MEMORY-RETENTION-BOOTSTRAP-001

## packet_id / question_id

OQ-010, OQ-011

## purpose

이 disposable fixture는 failure event replay를 통해 candidate·eligible exposure·승격·감쇠·만료의
관찰 경계를 확인하고, 합성 runtime/evidence 항목의 상태·위험도·용량별 prune 후보와
미생성·empty·available·unavailable memory의 typed result를 비교한다.

결과는 Phase 0 research evidence일 뿐 제품 evaluator, retention worker, bootstrap command,
schema, ADR 또는 사용자 결정 receipt가 아니다.

## scope and non-goals

- 포함: deterministic event replay, independent recurrence와 guard evidence, eligible/unassisted
  exposure 구분, candidate expiry simulation, active/blocked/completed/memory retention cases,
  memory capability result projection
- 입력: `input/fixture.json`의 결정론적 합성 payload
- 비목표: 제품 언어, package manager, runtime schema, SQLite/FTS implementation, daemon,
  scheduler, background prune worker, plugin scaffold, target `.geness/`, 실제 `GENESS_HOME` 또는
  사용자 decision receipt 선택
- Python과 JSON은 fixture 도구일 뿐 Controller 언어·event schema·retention threshold 추천을
  자동으로 채택하지 않는다.
- fixture-local profile의 숫자와 typed result는 비교 가능한 candidate observation이지 제품
  policy의 확정값이 아니다.

## category

Disposable Phase 0 memory, retention and bootstrap evidence fixture.

## exact command

이 디렉터리에서 다음 명령을 실행한다.

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

runner는 Python standard library만 사용하며, 입력 외의 파일·DB·lock을 만들지 않는다.

## expected observation

- 첫 failure는 `candidate`로 남고 verified/enforced retrieval에 나타나지 않는다.
- 독립 run의 반복 또는 재현 가능한 guard evidence가 있는 lesson만 fixture-local profile에서
  `verified`가 된다.
- 같은 run의 중복 failure, ineligible exposure와 lesson-injected success는 독립 재발·unassisted
  success 계산에 중복 반영되지 않는다.
- candidate/probationary 항목은 eligible unassisted success와 최소 관찰 기간을 함께 충족할 때만
  expiry candidate가 된다. verified lesson은 이 fixture profile에서 자동 expire하지 않는다.
- active/blocked runtime은 오래되거나 커도 자동 prune하지 않고, completed low-risk 항목은
  TTL 또는 size candidate에 의해 prune된다. high-risk와 memory event는 별도 보존 경계를 가진다.
- `UNINITIALIZED`, `EMPTY`, `AVAILABLE`, `UNAVAILABLE` memory 결과가 서로 구분되며, missing/empty는
  명시적 no-memory 결과를, unavailable은 rebuild/repair attention을 반환한다.
- 같은 입력을 두 번 replay한 projection은 equality-equivalent하다.

## isolation and network policy

- Python standard library만 사용한다.
- 입력은 합성 lesson/event/retention/bootstrap case만 포함한다.
- network, GitHub, target repository, `.geness/`, 실제 `GENESS_HOME`, credentials와 external writes를
  사용하지 않는다.
- runner는 현재 repository 또는 사용자 로컬 상태를 읽거나 쓰지 않는다.

## cleanup boundary

runner는 temporary directory나 persistent state를 만들지 않으므로 별도 cleanup 대상이 없다.
stdout은 실행 직후 redaction 요약만 evidence로 보존하고 raw output은 폐기한다.

## retention plan

- tracked: README, runner.py와 input/fixture.json
- packet: 실제 실행 후 redacted result manifest와 각 OQ의 RUN record
- local-only 또는 discarded: raw stdout/stderr와 실행 환경의 임시 output
