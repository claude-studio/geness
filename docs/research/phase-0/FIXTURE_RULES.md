# Disposable Fixture Rules

> 상태: Proposed research convention
> 적용 범위: `docs/research/phase-0/`의 조사 fixture

## 1. 정의

Disposable fixture는 하나의 Phase 0 가설이나 trade-off를 최소 입력으로 재현하고, 결과를
packet의 evidence로 남긴 뒤 안전하게 폐기할 수 있는 격리된 조사 장치다. fixture는 제품
구현이 아니며, 결과가 성공이든 실패든 decision packet에 관찰로 기록한다.

fixture는 다음을 만족해야 한다.

- 목적과 expected observation이 하나의 질문으로 좁혀져 있다.
- 입력·runner·version·환경·명령이 재현 가능하게 고정되어 있다.
- 현재 repository, target `.geness/`, 실제 `GENESS_HOME`과 credentials를 건드리지 않는다.
- network와 external write는 기본적으로 꺼져 있고, 예외는 packet에서 명시적으로 승인·기록한다.
- 동일 입력의 재실행이 가능하며, 실패를 숨기거나 성공으로 바꾸지 않는다.
- 결과가 제품 scaffold, manifest, package, Controller source 또는 배포 artifact로
  재사용되지 않는다.

## 2. 디렉터리와 보존 경계

```text
docs/research/phase-0/
├── fixtures/
│   └── <fixture-id>/
│       ├── README.md          # 목적·입력·명령·기대값·cleanup
│       └── input/             # 작고 합성된 입력만
├── evidence/
│   └── <packet-id>/<fixture-id>/<run-id>/
│       └── <redacted-artifact>
└── OQ-<번호>-<slug>.md        # packet과 실행 record
```

각 경계의 규칙은 다음과 같다.

| 영역 | 보존 대상 | 금지 대상 |
| --- | --- | --- |
| `fixtures/` | fixture 설명, 합성 입력, 재실행 가능한 작은 runner | 제품 코드·실제 secret·사용자 데이터 |
| `evidence/` | packet을 직접 지지하는 작고 redacted된 manifest/result | raw log, credential, 대용량 DB·binary |
| OS temp 또는 명시한 외부 경로 | raw stdout/stderr, 중간 DB, 대용량 결과 | packet에서 locator/hash 없이 사라지는 필수 evidence |
| packet | 요약 observation, exact command, exit status, artifact locator/hash, 위험 | 원본 secret·대용량 output·검증하지 않은 주장 |

raw output을 보존하지 않기로 했다면 packet의 artifact record에 `discarded`와 폐기 이유를
적는다. 보존한 artifact는 redaction 후에만 repository에 복사한다.

## 3. Fixture definition contract

각 fixture의 `README.md`는 최소 다음을 가진다.

```text
fixture_id
packet_id / question_id
purpose
category
inputs and preconditions
exact command
expected observation
expected runner exit status (if applicable)
isolation and network policy
external-write policy
cleanup boundary
retention plan
```

`expected observation`은 candidate 선택과 분리한다. fixture는 사실을 관찰할 뿐, 사용자
권한의 decision을 자동으로 채택하지 않는다.

## 4. 실행 절차

1. packet과 fixture ID를 정하고 run ID를 새로 만든다. 같은 run을 덮어쓰지 않는다.
2. fixture의 입력, 현재 commit, runner/tool version과 resolved working directory를
   기록한다.
3. 필요하면 OS temp 아래에 run 전용 디렉터리를 만들고, `GENESS_HOME` 같은 mutable
   경로는 반드시 그 디렉터리로 override한다. 실제 `~/.geness/`를 사용하지 않는다.
4. fixture README에 적힌 exact command를 실행한다. 실행 전 명령을 바꾸면 새 fixture
   revision 또는 새 run으로 기록한다.
5. 실제 stdout/stderr, observation, runner 오류와 process exit status를 각각 기록한다.
   명령이 non-zero를 반환해도 expected failure일 수 있으므로 exit status와 observation
   status를 합치지 않는다.
6. 결과를 redaction하고, packet에 필요한 작은 manifest/result만 `evidence/`로 보존한다.
   파일·blob은 SHA-256을 계산하고 실행 record의 artifact ID와 연결한다.
7. raw 중간 파일을 정리한다. 정리 범위는 해당 run 전용 temp 디렉터리로 제한하며, 다른
   프로젝트·worktree·home 경로를 지우지 않는다.
8. packet의 `Commands/results`, `Artifacts and evidence`, `Risks and limitations`를
   실제 결과에 맞춰 갱신한다.

### 실행 record 최소 형식

```yaml
run_id: "RUN-<unique>"
fixture_id: "FX-<...>"
started_at: "<RFC3339>"
ended_at: "<RFC3339>"
cwd: "<resolved path>"
command: "<exact command>"
exit_status: 0
observation_status: "pass | fail | indeterminate | not-run"
observation: "<actual result>"
stdout_ref: "<redacted artifact or discarded reason>"
stderr_ref: "<redacted artifact or discarded reason>"
artifact_refs: ["A-<...>"]
redaction: "<rule/version or none>"
```

`not-run`은 실행하지 않았다는 사실과 이유를 표시하는 값이다. `not-run` record는
evidence를 충족하지 않으며, 계획된 명령을 실행한 것으로 보고하지 않는다.

## 5. 격리·안전 규칙

- fixture는 합성 입력과 최소 파일만 사용한다. 실제 repository secret, token, 개인 경로,
  사용자 prompt 원문과 환경변수 전체를 복사하지 않는다.
- target repository를 조사해야 하면 현재 worktree를 수정하지 말고 disposable temp
  target을 준비한다. `.geness/` 생성·migration을 시험할 때도 per-run temp root를
  사용하고 원래 target root를 사용하지 않는다.
- Git branch checkout, branch/worktree 생성·삭제·전환을 fixture가 수행하지 않는다.
  필요한 상태는 fixture 입력으로 표현하고, 작업공간 lifecycle은 사용자 책임이다.
- network는 `disabled`가 기본이다. 켜야 한다면 host, URL, pinned commit/version, 목적,
  credential 부재와 결과의 변동 가능성을 packet에 적는다.
- 외부 write, package install, daemon 시작과 destructive command는 기본 금지다. 필요하면
  별도 authority 승인을 받고, 대상·범위·복구 방법을 실행 전 packet에 적는다.
- `GENESS_HOME`을 다루는 fixture는 실제 home이 아닌 per-run temp를 사용한다. runtime,
  memory, lock과 evidence의 경계를 섞지 않는다.
- fixture가 실패해도 원인을 추측해 expected result를 바꾸지 않는다. candidate·risk·next
  check로 라우팅한다.

## 6. 보존 등급

각 artifact는 다음 중 하나의 retention을 가진다.

| 등급 | 의미 | 예 |
| --- | --- | --- |
| `tracked` | 재실행에 필요한 작은 정의·합성 입력을 Git에 보존 | fixture README, input JSON |
| `packet` | 해당 OQ 판단을 직접 지지하는 redacted 결과를 Git에 보존 | 결과 요약, manifest, hash |
| `local-only` | Git에 넣지 않고 외부 경로에 남김. locator·hash·권한을 packet에 기록 | 큰 log, DB snapshot |
| `discarded` | hash/요약을 남긴 후 안전한 temp에서 폐기 | 중간 파일, 비결정적 raw output |

`tracked`나 `packet` artifact에는 secret·credential·민감한 개인 정보가 없어야 한다.
redaction 여부를 확인할 수 없으면 `local-only`로 낮추고 packet에 blocker를 남긴다.

## 7. 재실행과 결과 합성

- 재실행은 새 `run_id`를 사용하고 동일한 fixture revision과 입력 hash를 기록한다.
- 같은 fixture의 결과가 다르면 어느 run이 실패했는지 숨기지 말고 환경·version·network
  차이를 risk로 올린다.
- 여러 candidate가 같은 fixture를 사용하면 candidate별 observation을 별도 row로
  기록한다. 한 candidate의 결과를 다른 candidate의 성공 근거로 재사용하지 않는다.
- fixture 결과는 `PASS`, `FAIL`, `INDETERMINATE`, `NOT_RUN` 중 하나로 남길 수 있지만,
  이것이 Geness task lifecycle의 `COMPLETED`나 Phase 0 `CLEAR`를 의미하지는 않는다.
- command exit code와 expected observation이 다르면 `runner error`, `criterion failure`,
  `environment blocker` 중 관찰 가능한 범주를 고르고, 모르는 경우 `indeterminate`로
  남긴다.

## 8. Packet 연결 checklist

- [ ] fixture ID와 packet/OQ ID가 서로 연결된다.
- [ ] 정의 README의 exact command와 packet execution record가 일치한다.
- [ ] 실행 시각, cwd, tool version, input/environment와 run ID가 있다.
- [ ] 실제 exit status와 observation status가 분리돼 있다.
- [ ] artifact마다 locator, hash 또는 hash 불가/폐기 이유와 retention이 있다.
- [ ] raw output과 redacted evidence의 경계가 기록돼 있다.
- [ ] fixture가 current target/home, product scaffold와 외부 상태를 변경하지 않았다.
- [ ] 재실행·불일치·cleanup 결과가 packet의 risk/limitation에 반영됐다.
