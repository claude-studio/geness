# ADR-0002: Project documents and local mutable state are separate

> 상태: Accepted
> 날짜: 2026-08-10

## 맥락

사용자가 검토하고 Git으로 공유할 계약과 실행 중 자주 바뀌는 lease, log, raw evidence,
검색 인덱스는 수명·보안·동시성 요구가 다르다. 모든 것을 target repository나 plugin
cache에 넣으면 민감정보, 큰 diff, update 손실과 host 간 충돌이 생긴다.

## 결정

세 저장 경계를 사용한다.

- target repository의 `.geness/`: `project.json`과 task의 interview/spec/plan/run 문서
- `~/.geness/runtime/`: run, attempt, checkpoint, lease, failure candidate와 원본 evidence
- `~/.geness/memory/`: verified lesson event와 SQLite/FTS 검색 projection

Plugin install/cache는 읽기 전용 code, schema와 template만 보유한다. concern별
canonical owner는 Storage 문서가 정하며 `run.md` 같은 요약 projection을 mutable
runtime state로 오인하지 않는다.

## 결과

- project 계약은 host와 machine을 넘어 검토·공유할 수 있다.
- private log와 mutable state는 Git에서 분리된다.
- project/workspace identity와 reconciliation 규칙이 필요하다.
- home data의 backup, migration, retention과 uninstall 보존 UX가 필요하다.

## 거절한 대안

- 모든 상태를 `.geness/`에 저장: 비밀정보와 noisy diff 때문에 거절한다.
- 모든 상태를 `~/.geness/`에 저장: 팀 공유와 portable contract가 사라진다.
- Claude/Codex plugin data dir를 canonical home으로 사용: 두 host가 공유할 수 없고 update
  수명에 종속된다.
- 저장소 폴더명만 project key로 사용: 동명 repository가 충돌한다.

## 검증 방법

- 생성 문서가 resolved target root 아래에만 쓰이는지 containment test를 실행한다.
- plugin update/uninstall 뒤 `GENESS_HOME`과 target 계약이 보존되는지 확인한다.
- 동명 clone, rename과 Git worktree fixture로 identity 충돌을 검사한다.
