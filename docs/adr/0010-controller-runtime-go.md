# ADR-0010: Go Controller runtime

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-001은 TypeScript/Node, Python, Go와 Rust를 배포 모델, SQLite/FTS5 capability,
stdio MCP round-trip과 두 개의 독립 working directory 실행으로 비교했다. 관찰은
macOS arm64의 disposable spike에 한정되며, installed-host E2E와 Linux/Windows
release는 아직 검증하지 않았다.

사용자는 [OQ-001 decision receipt](../research/phase-0/evidence/OQ-001/USER-DECISION-RECEIPT-001.md)로
Go 후보를 선택했다.

## 결정

1. Geness v1 Controller는 **Go**로 구현한다.
2. Go modules를 package와 dependency management 경계로 사용한다.
3. SQLite FTS5는 CGO와 명시적인 `sqlite_fts5` build tag를 요구하는 build contract로
   고정한다. build tag가 빠진 artifact는 FTS5 capability를 충족한 것으로 취급하지
   않는다.
4. 단일 binary 배포 모델을 기본 방향으로 삼되, macOS·Linux·Windows artifact와
   toolchain/cross-build matrix는 별도 검증한다.
5. 이 ADR은 Controller의 domain/state 권위, CLI/MCP 경계, daemon 정책, schema와
   migration을 결정하지 않는다. 해당 concern은 각 Phase 0 OQ와 후속 ADR이 소유한다.

## 결과

- host에 별도 Node/Python runtime을 요구하지 않는 Controller 배포 방향을 갖는다.
- Go application/service와 CLI/MCP thin transport를 분리하는 Architecture 방향을
  유지할 수 있다.
- CGO compiler availability와 `sqlite_fts5` build tag를 local build, CI와 release
  validation에서 검증해야 한다.
- cross-platform release, SDK/driver version pinning, schema migration과 installed-host
  behavior는 아직 구현 완료나 지원 선언이 아니다.

## 거절한 대안

- **Rust + `rusqlite bundled`**: CGO와 OS SQLite 차이를 줄이는 장점은 있으나, 이번
  선택에서는 Rust build/release 복잡성보다 Go의 단일 binary와 SDK/개발 균형을 우선했다.
- **TypeScript/Node**: SDK와 개발 loop는 유리하지만 Node runtime과 dependency tree를
  함께 배포·검증해야 하므로 v1 Controller 본체 후보에서 제외했다.
- **Python**: prototype과 데이터 처리에는 적합하지만 interpreter/venv와 더 큰
  dependency artifact가 필요하므로 v1 Controller 본체 후보에서 제외했다.

## 검증 방법

- [OQ-001 packet](../research/phase-0/OQ-001-controller-runtime.md)의 동일 fixture 결과와
  source/artifact hash를 보존한다.
- Go build에서 `sqlite_fts5` tag를 포함한 FTS5 query와 stdio MCP round-trip을 재현한다.
- 후속 Phase 0/implementation evidence에서 macOS·Linux·Windows artifact, cross-build,
  CGO toolchain, migration, multi-process lease/crash와 installed-host capability를
  별도로 검증한다.

## Decision receipt

- **Decision:** Go + Go modules + CGO + explicit `sqlite_fts5`
- **Actor:** `user`
- **Recorded at:** `2026-08-22T16:05:46+09:00`
- **Reference:** [USER-DECISION-OQ001-001](../research/phase-0/evidence/OQ-001/USER-DECISION-RECEIPT-001.md)
