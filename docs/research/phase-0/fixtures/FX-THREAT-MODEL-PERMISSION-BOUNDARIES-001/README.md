# FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001

## Fixture metadata

- **Packet:** OQ-015
- **Purpose:** threat model의 핵심 control이 권한·scope·digest·lease·secret·검증 경계를
  fail-closed로 다루는지 합성 입력으로 관찰한다.
- **Category:** security / permission / cross-concern contract
- **Input:** `input/fixture.json`의 고정 digest, 허용 상대 경로, 금지 capability와 합성
  redaction probe
- **Runner:** `runner.py`

## Exact command

```text
PYTHONDONTWRITEBYTECODE=1 python3 runner.py
```

기대 결과는 exit `0`, 17개 assertion 통과와 `all_assertions_pass=true`다. 두 번 실행한
projection은 equality-equivalent여야 한다.

## Observations

runner는 다음 control을 합성 입력으로 확인한다.

- canonical target root containment와 parent/symlink escape 거부
- scope 확대·external write의 user receipt 및 current digest 요구
- stale digest와 두 번째 writer 거부, observer read 허용
- approved in-scope local write만 허용하고 danger-full-access/approval bypass 거부
- untrusted repository instruction을 authority로 승격하지 않음
- synthetic secret redaction 후 원문 비보존
- worker self-verification 및 acting evidence 없는 behavior-bearing completion 거부
- candidate memory 비노출과 corrupt memory의 `HOLD` 분리

## Isolation and retention

- network: disabled
- external writes: false
- credentials/login/plugin install/daemon: not used
- temporary target root와 symlink는 runner의 per-process temp directory 안에서만 생성한다.
- 실제 target `.geness/`, 실제 `~/.geness/`, plugin cache와 현재 worktree는 변경하지 않는다.
- raw stdout/stderr와 temporary state는 packet에 보존하지 않는다. runner source/input은
  `tracked`, redacted result는 `packet` retention으로 둔다.
