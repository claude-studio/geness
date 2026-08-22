# Geness Storage and Identity

> 상태: Accepted boundary, identity lineage and schema ownership / implementation technology TBD

## 1. 목적

이 문서는 Geness 소스 문서, 대상 저장소 artifact, 사용자 로컬 runtime과 memory의
소유권을 정의한다. SQLite table과 migration의 정확한 schema는 Phase 0에서 확정한다.
OQ-006과 [ADR-0016](./adr/0016-schema-lineage-and-projection-ownership.md)은 portable
task frontmatter/projection과 runtime SQLite mutable-state owner, stale-write와
reconciliation 경계를 먼저 확정한다.

## 2. 세 저장 경계

### Geness 소스 저장소

```text
docs/       Geness 제품 규범·계획·결정·진행·연구
skills/     배포할 workflow
schemas/    배포할 machine contract
templates/  대상 저장소 artifact template
```

### 대상 저장소

```text
<target>/.geness/
├── project.json
├── config.yaml                 # 도입 여부 TBD
└── tasks/
    └── <slug>--<task-id>/
        ├── interview.md
        ├── spec.md
        ├── plan.md
        ├── run.md
        └── verification.md
```

이 영역은 사람이 읽고 Git으로 공유할 portable contract와 summary다.
`spec.md`는 승인된 contract projection, `plan.md`는 plan projection, `run.md`는 impl
summary, `verification.md`는 final verify projection이다. mutable state와 verdict의
정본은 사용자 로컬 runtime DB다.

### 사용자 로컬 데이터

```text
~/.geness/
├── memory/
│   └── <repo-slug>--<project-id>/
│       ├── events.jsonl
│       └── memory.sqlite3
└── runtime/
    └── <repo-slug>--<project-id>/
        └── <workspace-id>/
            ├── runtime.sqlite3
            ├── locks/
            ├── logs/
            └── evidence/
```

`GENESS_HOME`으로 사용자 로컬 루트를 재정의할 수 있게 하는 방향을 채택한다.

## 3. Project identity

Project/workspace lineage policy is defined by [ADR-0015](./adr/0015-project-workspace-identity.md).

`project.json` 최소 필드:

```json
{
  "schema_version": 1,
  "project_id": "<stable-id>",
  "display_name": "<repository-name>",
  "created_at": "<RFC3339>"
}
```

- 폴더명은 display slug일 뿐 identity가 아니다.
- `project_id`는 folder rename과 worktree에 안정적이어야 한다.
- 일반 clone은 `project_id`를 공유하지만 distinct `workspace_id`를 사용한다.
- folder rename은 project metadata를 보존하는 한 같은 project와 workspace로 유지한다.
- Git worktree는 같은 project의 distinct workspace다.
- fork, detach와 동명 repository는 사용자의 명시적 detach/rekey 뒤 새 project lineage가 된다.
- display name, folder path, branch, remote와 host session만으로 project identity를 자동
  detach하거나 공유하지 않는다.

## 4. Workspace identity

- `workspace_id`는 한 machine의 clone/worktree 실행 경계를 구분한다.
- memory는 project 단위로 공유하고 runtime은 workspace 단위로 격리한다.
- clone과 Git worktree는 project가 같아도 workspace가 distinct하며, metadata-preserving
  folder rename은 기존 workspace를 유지한다.
- workspace path가 바뀌어 orphan runtime이 생길 수 있으므로 registry 또는 cleanup 정책이
  필요하다.
- host session ID나 branch 이름만으로 workspace identity를 만들지 않는다.
- ID 생성 algorithm, explicit rekey UX, registry/reconciliation과 cross-workspace writer
  authority는 후속 Phase 0/implementation evidence가 필요하다.

## 5. Project document contract

- Markdown은 사람이 읽는 본문과 machine-readable frontmatter를 함께 가진다.
- write는 temp file + fsync + atomic replace를 우선한다.
- revision, digest와 `geness.semantic-json-v1` digest profile을 기록한다.
- raw log, credential과 대용량 evidence를 포함하지 않는다.
- `run.md`는 runtime DB의 projection이며 직접 임의 수정된 경우 reconciliation이
  필요하다.
- `verification.md`는 runtime의 AC verdict와 evidence freshness를 사람이 읽도록
  투영한 문서다. 직접 수정되거나 stale하면 Controller가 runtime 정본과 reconciliation
  해야 하며, 문서만으로 `COMPLETED`를 선언할 수 없다.
- Markdown frontmatter와 body는 portable contract/projection이고, runtime SQLite는
  mutable task state·revision guard·attempt·lease·verdict·evidence freshness의
  canonical owner다. current revision/digest precondition과 operation ID 기반 idempotent
  projection/reconciliation을 적용한다.
- canonical target root 밖 path와 symlink escape를 거부한다.
- semantic digest는 [ADR-0017](./adr/0017-versioned-semantic-digest.md)에 따라 계산하며,
  editorial body는 approval digest의 입력이 아니다.

## 6. Runtime SQLite 역할

`runtime.sqlite3`는 “현재 task가 어디까지 진행됐고 다음에 무엇을 할 수 있는가?”에
답한다.

필요한 logical tables:

- task/run state와 revisions
- steps, attempts와 AC results
- approvals와 contract digests
- leases와 heartbeats
- host/workspace session references
- evidence metadata와 content hash
- verifier identity/type, evidence freshness와 final verdict
- failure events와 lesson candidates
- transition/audit events
- schema migrations

원본 stdout/stderr와 evidence blob은 파일로 두고 DB에는 path, hash, mime/type, redaction
상태와 lineage만 저장한다.

## 7. Memory SQLite 역할

`memory.sqlite3`는 “이번 작업과 관련해 재사용할 검증된 규칙은 무엇인가?”에 답한다.

필요한 logical tables:

- lessons와 lifecycle status
- scopes와 tags
- fingerprint와 trigger
- rules, root causes와 guards
- occurrence/exposure/success counters
- evidence references
- evaluator/rule version, threshold profile과 transition history
- FTS5 index와 synchronization trigger

memory SQLite는 빠른 검색 index다. lesson event의 append-only 감사 원본은
`events.jsonl`이며 index는 재구축할 수 있어야 한다.

## 8. Concurrency

- Controller 한 process가 DB write authority를 가진다.
- subagent와 host hook은 직접 SQLite를 쓰지 않는다.
- WAL 사용 여부는 filesystem·backup·multi-process 시험 후 결정한다.
- transaction은 짧게 유지하고 무한 busy retry를 하지 않는다.
- stale revision write를 거부한다.
- [ADR-0014](./adr/0014-completion-lease-atomicity.md)에 따라 runtime terminal checkpoint와
  writer lease release를 한 transaction으로 기록한다. project document projection 실패와
  DB commit 성공 또는 그 반대는 completion authority를 바꾸지 않고 operation ID로 복구한다.

## 9. Retention

- project documents는 Git history 정책을 따른다.
- active/blocked runtime은 자동 삭제하지 않는다.
- completed runtime log/evidence는 설정 가능한 TTL과 용량 제한을 적용한다.
- memory event와 verified lesson은 runtime cleanup과 분리한다.
- compiled/deprecated lesson의 보존·export 정책은 Phase 5에서 결정한다.
- uninstall은 `~/.geness/`를 자동 삭제하지 않는다.

## 10. Security

- 가능한 플랫폼에서 local directory는 owner-only 권한을 기본으로 한다.
- 저장 전에 token, credential, secret과 민감한 environment 값을 redaction한다.
- credential과 동일한 등급의 원문은 저장 거부할 수 있어야 한다.
- SQLite query parameterization과 FTS query sanitization을 적용한다.
- evidence를 모델 context에 넣기 전에 별도의 출력 redaction을 적용한다.
- backup과 migration artifact에도 같은 권한·redaction 정책을 적용한다.

### 10.1 Threat model alignment

[ADR-0009](./adr/0009-threat-model-permission-boundaries.md)의 Accepted C-01 baseline과
[OQ-015](./research/phase-0/OQ-015-threat-model-permission-policy.md)에 따라 다음 경계를
유지한다. exact secret detector의 완전성이나 production enforcement는 후속 evidence가
필요하다.

- target 문서에는 contract/projection과 필요한 hash·lineage만 두고 raw command output,
  credential, environment secret과 대용량 evidence를 넣지 않는다.
- 모든 project-local write는 canonical root containment와 symlink escape 검사를 통과해야
  하며, runtime/memory/plugin cache를 target root로 추론하지 않는다.
- redaction을 확인할 수 없는 output은 project document나 memory로 승격하지 않고
  `HOLD` 또는 local-only로 보존한다. candidate lesson과 corrupt memory를 empty/verified로
  축약하지 않는다.
- active/blocked/high-risk runtime evidence와 memory event는 자동 삭제 경계를 서로 공유하지
  않는다. retention/prune decision은 disposition과 audit lineage를 남긴다.

## 11. Migration

- project document, runtime DB, memory DB와 evaluator rule version을 각각 기록한다.
- destructive migration 전에 backup 또는 재구축 가능성을 확인한다.
- memory index가 손상되면 JSONL에서 재구축한다.
- runtime migration 실패는 task를 `BLOCKED`로 유지하고 이전 DB를 보존한다.
- schema 변경은 fixture와 upgrade/rollback test를 요구한다. exact frontmatter grammar,
  production table/column/index/migration과 cross-runtime serializer edge rules는
  ADR-0017 profile의 후속 OQ/evidence로 확정한다.
