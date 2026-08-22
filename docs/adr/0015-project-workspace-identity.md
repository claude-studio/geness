# ADR-0015: Explicit project lineage and workspace-scoped identity

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-005는 clone, fork, folder rename, 동명 repository와 Git worktree가
`project_id`와 `workspace_id`에 미치는 관계를 비교했다. disposable fixture는 local Git
clone·rename·worktree 사실과 synthetic explicit detach 관계를 두 번 실행해 각각 30/30
assertions와 equality-equivalent stdout을 반환했다.

Git history·remote·path만으로는 사용자의 project lineage 의도를 완전히 판정할 수 없다.
따라서 관찰된 Git 관계와 durable project/workspace policy를 분리해 채택하고, ID 생성
알고리즘과 registry 구현은 후속 결정·evidence로 남긴다.

## 결정

1. portable `.geness/project.json`의 stable `project_id`는 display name, folder path,
   branch와 host session과 독립적인 project lineage를 나타낸다.
2. `workspace_id`는 한 machine에서 clone/worktree 실행 경계를 구분하고, project-scoped
   memory와 workspace-scoped runtime의 저장 경계를 유지한다.
3. 일반 clone은 project lineage를 공유하지만 별도의 workspace로 취급한다.
4. folder rename은 project metadata를 보존하는 한 같은 project와 workspace를 유지한다.
5. Git worktree는 같은 project의 별도 workspace로 취급한다.
6. fork, detach 또는 동명 repository를 별도 project로 취급하려면 사용자의 명시적
   detach/rekey가 필요하다. display name, path 또는 remote 차이만으로 자동 detach하지
   않는다.
7. 이 ADR은 project ID 생성 알고리즘, fork 자동 감지, workspace registry/reconciliation,
   cross-workspace writer authority와 production schema를 확정하지 않는다.

## 결과

- clone과 worktree의 shared project lineage와 isolated runtime 경계를 표현할 수 있다.
- folder rename이 path-derived identity 때문에 runtime을 orphan시키는 위험을 줄인다.
- fork와 동명 repository의 implicit memory sharing을 방지하고 detach 의도를 audit할 수 있다.
- project metadata 복사·보존, explicit rekey UX, path reconciliation과 cross-workspace lease
  authority는 구현 전 별도 evidence가 필요하다.
- Phase 0의 다른 blocking decision과 production evidence가 남아 있으므로 Implementation은
  계속 `HOLD`다.

## 거절한 대안

- **C-02 Git remote/object-derived identity:** remote 부재·변경, mirror와 duplicate remote,
  fork intent를 일관되게 판정하지 못하므로 기본 identity 권위자로 채택하지 않았다.
- **C-03 path/workspace-derived identity:** clone·rename·worktree에서 portable resume과
  durable lineage가 path 변경에 취약하므로 채택하지 않았다.
- **implicit fork detection:** remote/path heuristic만으로 사용자의 detach 의도를 대체하면
  project memory가 잘못 공유되거나 분리될 수 있어 금지한다.

## 검증 방법

- [OQ-005 packet](../research/phase-0/OQ-005-project-workspace-identity.md)의 candidate
  matrix와 risk/limitation을 확인한다.
- [FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001](../research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md)을
  `PYTHONDONTWRITEBYTECODE=1 python3 runner.py`로 두 번 실행해 local Git relation과
  synthetic project/workspace matrix를 확인한다.
- 보존된 두 result manifest가 각각 30/30 assertions와 `all_assertions_pass=true`이고,
  paired stdout이 equality-equivalent인지 확인한다.
- production ID generation, registry migration, fork-provider metadata와 concurrent
  workspace writer validation은 후속 Phase 0/implementation evidence로 남긴다.

## Decision receipt

- **Decision:** C-01 — explicit project lineage와 workspace-scoped identity를 분리
- **Actor:** `user-delegated-autonomous-delivery` under the explicit AUTOPILOT delegation
- **Recorded at:** `2026-08-22T12:03:46Z`
- **Reference:** [OQ-005 decision receipt](../research/phase-0/evidence/OQ-005/USER-DECISION-RECEIPT-001.md)
