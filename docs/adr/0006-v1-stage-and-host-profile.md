# ADR-0006: V1 public stages and configurable host profile

> 상태: Accepted
> 날짜: 2026-08-20

## 맥락

Geness는 기존 RPI의 단계형 개발 흐름과 Ouroboros에서 관찰한 질문·계약·검증 원칙을
결합한다. 그러나 기존 내부 lifecycle 상태와 새 사용자-facing stage 이름을 동시에
사용해야 하며, Codex가 없는 환경에서도 Claude 단독 실행을 지원해야 한다.

## 결정

사용자-facing stage는 다음으로 고정한다.

~~~text
brief → contract → plan → impl → verify → done
                                      ↘ resume
~~~

새 이름은 기존 canonical internal state의 public alias로 사용한다.

| Public stage | Internal state 또는 의미 |
| --- | --- |
| brief | INTERVIEWING |
| contract | SPEC_READY → SPEC_APPROVED |
| plan | PREFLIGHT → PLAN_READY → PLAN_APPROVED |
| impl | RUNNING |
| verify | VERIFYING |
| done | COMPLETED를 닫는 Controller transition |
| resume | PAUSED/BLOCKED/REOPENED에서 재개하는 action |

기본 host profile은 다음과 같다.

~~~text
Claude: brief / plan / verify
Codex:  contract candidate·QA / impl
Controller: done / resume
~~~

profile은 auto, cross-model, claude-only 중 하나다. auto는 Codex capability를 먼저
확인해 cross-model을 선택하고, Codex가 없을 때 새 task에 한해 claude-only로
fallback한다. active task의 profile은 조용히 변경하지 않는다.

branch checkout, worktree 생성·삭제·전환은 사용자의 책임이다. Geness는 현재 작업공간을
검증할 뿐 Git 작업공간 lifecycle을 관리하지 않는다.

V1은 같은 컴퓨터·같은 사용자 데이터 루트·사용자가 준비한 같은 작업공간을 지원한다.
task당 active writer 하나만 허용하고 두 번째 host/process는 observer로 제한한다.

## 결과

- Claude-only와 cross-model을 같은 Controller contract로 지원할 수 있다.
- public UX와 내부 lifecycle 문서를 독립적으로 진화시킬 수 있다.
- Codex 부재가 새 task의 시작을 막지 않는다.
- active task의 host 변경은 contract digest invalidation과 reapproval이 필요하다.
- 서로 다른 컴퓨터와 여러 worktree 동시 writer는 V1 범위 밖이다.

## 거절한 대안

- public stage 이름을 곧바로 internal state로 교체: 기존 lifecycle/ADR과의 migration
  범위가 커지고 상태 의미가 섞이므로 거절했다.
- Codex가 없을 때 진행 중인 task를 자동으로 Claude로 전환: 승인된 contract와
  provenance가 바뀌므로 거절했다.
- Geness가 branch/worktree를 자동 관리: 사용자 Git 작업공간 권한과 충돌하므로 거절했다.
- 여러 worktree의 동일 task 동시 writer: V1 lease 범위를 복잡하게 만들므로 후순위로 뒀다.

## 검증 방법

- public stage와 internal state 매핑 fixture
- auto/cross-model/claude-only capability matrix
- Codex 부재 새 task fallback fixture
- active task profile change rejection fixture
- one-writer/observer/stale takeover race fixture
- current user-prepared worktree 외부 write 차단 fixture
