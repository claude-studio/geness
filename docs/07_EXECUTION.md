# Execution Stage Guide

> 상태: Proposed v1 contract

## 1. 목적

승인된 spec/plan을 allowed scope 안에서 실행하고, AC 단위 checkpoint와 evidence를
남겨 중단·재계획·v1 same-machine host handoff를 가능하게 한다.

Execution은 public `impl` 단계이며, 자신의 결과를 최종 검증하거나 contract를 바꾸는
단계가 아니다. 기본 cross-model profile에서는 Codex worker가 구현을 담당하고, Claude
verify가 독립적으로 결과를 판정한다.

## 2. Entry contract

- current spec과 필요한 plan approval가 유효하다.
- recomputed digest가 저장된 digest와 일치한다.
- preflight snapshot이 stale하지 않다.
- project/task writer lease를 획득했다.
- 실행 권한과 sandbox가 allowed scope를 만족한다.
- 현재 task의 profile과 capability snapshot이 contract digest와 일치한다.

## 3. Work derivation

- AC와 dependency를 기본 실행 단위로 사용한다.
- 한 AC가 너무 크면 원래 outcome을 보존하는 bounded child step으로 분해한다.
- 독립적인 research/implementation/verification 준비는 subagent로 병렬화할 수 있다.
- worker마다 input revision, allowed paths, expected output과 금지 capability를 전달한다.
- delegated worker는 Geness Controller를 재귀 호출하거나 DB를 직접 쓰지 않는다.
- Claude plugin이 Codex를 호출하는 경우 Controller가 task/run ID, worktree, digest,
  allowed scope, AC, checkpoint와 protocol version을 포함한 handoff envelope를 만든다.
  Codex 결과는 Controller로 돌아오며 runtime DB와 project 문서는 Controller만 갱신한다.

### 3.1 Capability and permission precondition

실행 envelope에는 `allowed_scope`, `forbidden_scope`, capability snapshot, approval receipt
reference와 current spec/plan digest를 함께 묶는다. [ADR-0009](./adr/0009-threat-model-permission-boundaries.md)의
Proposed baseline에 따라 다음 요청은 Controller에서 fail-closed로 라우팅한다.

- target root 밖 path, parent traversal 또는 symlink escape
- current digest와 일치하지 않는 plan/approval, active writer lease 없는 mutation
- scope 확대, external write, destructive action, security-boundary 변경과 permission
  escalation의 non-user 또는 stale receipt
- runtime DB 직접 write, approval bypass, 기본 `danger-full-access`
- redaction이 완료되지 않은 raw output의 project document/memory/context 저장

이 경우 worker가 성공을 주장해도 attempt는 `HOLD`/attention이며 `RUNNING` 또는 `COMPLETED`로
승격하지 않는다. exact approval actor/risk policy는 OQ-008, takeover/atomicity는 OQ-003/OQ-009의
user decision과 후속 fixture가 소유한다.

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

## 7. Resume와 workspace 경계

v1 resume은 같은 컴퓨터·같은 `GENESS_HOME`·사용자가 준비한 같은 branch/worktree에서만
지원한다. Geness는 Git checkout, branch 전환, worktree 생성·삭제·정리를 수행하지 않는다.
사용자가 원하는 작업공간을 먼저 준비하고 `gee resume`을 호출한다.

Resume 절차:

1. project/task/workspace를 resolve한다.
2. lease와 owner 생존/heartbeat를 확인한다.
3. spec/plan digest를 재계산한다.
4. Git state와 changed paths를 last checkpoint와 비교한다.
5. incomplete external side effect를 확인한다.
6. 안전하면 새 host가 명시적으로 lease를 takeover한다. 두 번째 process/host는 기존
   writer가 살아 있는 동안 observer로 제한한다.
7. 기록된 next action에서 재개한다.

상태를 확정할 수 없으면 추측해 재실행하지 않고 `BLOCKED` 또는 reconciliation으로
전환한다.

verify가 수정 가능한 실패를 반환하면 동일한 contract/AC를 유지하는 successor impl을
자동으로 만들 수 있다. task당 최대 5회이며, 반복 fingerprint·진전 없음·예산 소진은
`BLOCKED`와 사용자 attention으로 종료한다. contract, scope, 권한 또는 안전 경계 변경은
brief/contract Gate로 되돌린다.

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
- Codex handoff envelope의 digest/scope 검증
- five-successor bounded resume과 oscillation stop
- 사용자가 준비하지 않은 branch/worktree 변경 시도 차단
