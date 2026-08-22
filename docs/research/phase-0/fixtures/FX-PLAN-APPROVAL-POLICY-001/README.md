# FX-PLAN-APPROVAL-POLICY-001

## fixture_id

FX-PLAN-APPROVAL-POLICY-001

## packet_id / question_id

OQ-008

## purpose

이 disposable fixture는 OQ-015에서 채택한 `user_sensitive` floor를 고정한 뒤,
OQ-008의 C-01/C-02/C-03 approval-actor 후보가 routine read-only, routine local
write, scope expansion, external write, destructive action, security-boundary change와
stale digest를 어떻게 다르게 관찰하는지 비교한다. 후보를 선택하거나 일반 risk
threshold를 확정하지 않는다.

## category

Disposable Phase 0 plan-approval policy evidence fixture.

## inputs and preconditions

- `input/fixture.json`의 합성 scenario와 candidate expectation만 사용한다.
- current digest와 `user_sensitive` 분류는 fixture 입력의 관찰 조건이다.
- C-02의 `routine`은 policy actor 후보를 비교하기 위한 synthetic low-risk class이고,
  제품 risk tier의 채택을 의미하지 않는다.

## exact command

이 디렉터리에서 다음 명령을 실행한다.

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

## expected observation

- C-01은 current digest의 모든 scenario에 `user` actor를 요구한다.
- C-02는 routine scenario에 `policy`, `user_sensitive` scenario에 `user`를 관찰한다.
- C-03은 side effect 또는 sensitive boundary가 있는 scenario에 `user`, routine
  read-only에 `policy`를 관찰한다.
- stale digest는 모든 candidate에서 actor와 무관하게 `DENIED`다.
- `selected_candidate`는 `null`로 남는다.

## expected runner exit status

0 when every candidate/scenario comparison and the stale-digest guard assertion passes.

## isolation and network policy

- Python standard library만 사용한다.
- network, credentials, target repository, target `.geness/`, 실제 `GENESS_HOME`과
  external write를 사용하지 않는다.
- runner는 합성 JSON을 stdout에만 출력한다.

## external-write policy

외부 쓰기와 제품 상태 mutation은 금지된다.

## cleanup boundary

runner가 repository 또는 mutable home 경로를 만들지 않으므로 별도 cleanup이 없다.

## retention plan

- tracked: README, runner.py와 input/fixture.json
- packet: 실행 record와 필요 시 redacted result manifest
- discarded: 비교 후 raw stdout/stderr
