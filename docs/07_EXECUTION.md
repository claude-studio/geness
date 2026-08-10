# Execution Stage Guide

> 상태: Proposed v1 contract

## 1. 목적

승인된 spec/plan을 allowed scope 안에서 실행하고, AC 단위 checkpoint와 evidence를
남겨 중단·재계획·cross-host resume를 가능하게 한다.

Execution은 자신의 결과를 최종 검증하거나 contract를 바꾸는 단계가 아니다.

## 2. Entry contract

- current spec과 필요한 plan approval가 유효하다.
- recomputed digest가 저장된 digest와 일치한다.
- preflight snapshot이 stale하지 않다.
- project/task writer lease를 획득했다.
- 실행 권한과 sandbox가 allowed scope를 만족한다.

## 3. Work derivation

- AC와 dependency를 기본 실행 단위로 사용한다.
- 한 AC가 너무 크면 원래 outcome을 보존하는 bounded child step으로 분해한다.
- 독립적인 research/implementation/verification 준비는 subagent로 병렬화할 수 있다.
- worker마다 input revision, allowed paths, expected output과 금지 capability를 전달한다.
- delegated worker는 Geness Controller를 재귀 호출하거나 DB를 직접 쓰지 않는다.

## 4. Attempt contract

각 attempt는 최소 다음을 기록한다.

```text
run_id / attempt_id
spec_digest / plan_revision
AC와 step refs
host / workspace / worker refs
allowed scope
started/ended timestamps
commands/actions summary
changed paths
result category
evidence refs
failure fingerprint
next action
```

원본 로그는 `~/.geness/runtime/.../logs`, evidence는 `evidence/`에 저장한다.

## 5. Checkpoint

- state transition과 attempt 결과를 transaction으로 저장한다.
- AC 또는 의미 있는 step boundary마다 durable checkpoint를 만든다.
- checkpoint는 resume에 필요한 다음 action과 pending blockers를 포함한다.
- conversation transcript만 checkpoint로 사용하지 않는다.
- checkpoint 후 `run.md` projection을 idempotent하게 갱신한다.

## 6. Retry와 recovery

- transient transport retry와 동일 구현 전략 재시도를 구분한다.
- 같은 fingerprint 반복에는 작은 고정 budget을 적용한다.
- progress evidence가 없으면 전략 변경, plan reopen 또는 `BLOCKED`로 전환한다.
- contract assumption 오류는 specification 단계로 돌려보낸다.
- authority/scope 문제는 사용자에게 요청한다.
- runtime/system failure는 contract failure로 오인하지 않는다.

정확한 retry threshold는 ADR로 확정하기 전까지 TBD다.

## 7. Cross-host resume

Resume 절차:

1. project/task/workspace를 resolve한다.
2. lease와 owner 생존/heartbeat를 확인한다.
3. spec/plan digest를 재계산한다.
4. Git state와 changed paths를 last checkpoint와 비교한다.
5. incomplete external side effect를 확인한다.
6. 안전하면 새 host가 명시적으로 lease를 takeover한다.
7. 기록된 next action에서 재개한다.

상태를 확정할 수 없으면 추측해 재실행하지 않고 `BLOCKED` 또는 reconciliation으로
전환한다.

## 8. Exit

- 모든 planned work item이 terminal attempt를 가졌다.
- required evidence reference가 존재한다.
- 실행 중 contract drift가 없다.
- verification이 읽을 execution lineage가 완전하다.
- 실행 실패는 category/fingerprint/next route를 가진다.

Exit는 `COMPLETED`가 아니라 `VERIFYING` 진입 자격이다.

## 9. 테스트 matrix

- stale digest 실행 거부
- allowed path 밖 write 차단
- two-writer lease race
- attempt/checkpoint crash recovery
- host A → host B resume
- same fingerprint retry budget
- contract error와 implementation error routing
- missing/indeterminate external side effect
- worker result가 evidence 없이 success 주장
- `run.md` idempotent projection
