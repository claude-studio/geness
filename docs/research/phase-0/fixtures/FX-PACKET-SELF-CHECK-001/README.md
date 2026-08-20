# FX-PACKET-SELF-CHECK-001

> category: documentation self-check
> disposable: yes
> product code: no

## Purpose

Phase 0 packet 예시가 연결한 `git diff --check --` 실행 record와 artifact 보존 형식을
확인한다. 이 fixture는 문서의 의미나 제품 동작을 검증하지 않는다.

## Inputs and preconditions

- current Geness repository root에서 실행한다.
- 파일을 수정하거나 stage·commit하지 않는다.
- 네트워크, `GENESS_HOME`, target `.geness/`와 외부 write를 사용하지 않는다.

## Exact command

```sh
git diff --check --
```

## Expected observation

- whitespace 오류가 없으면 stdout/stderr가 비어 있고 exit status가 `0`이다.
- 오류가 있으면 실제 줄과 exit status를 packet에 기록하며, 결과를 성공으로 바꾸지
  않는다.

## Cleanup and retention

- 별도 temp 파일을 만들지 않으므로 cleanup 대상이 없다.
- 실행 결과는 packet을 직접 지지하는 작은 redacted record만
  `docs/research/phase-0/evidence/OQ-000-example/FX-PACKET-SELF-CHECK-001/`에 보존한다.
- raw output이 생기면 packet 규칙에 따라 redaction 후 보존하거나 `discarded`로 기록한다.
