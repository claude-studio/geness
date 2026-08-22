# OQ-001 — Controller 언어·패키지·runtime 후보 비교

> 상태: Resolved research packet / 사용자 결정 기록됨
> 조사일: 2026-08-20
> 결정 권한: 사용자
> 범위: Phase 0 disposable spike

이 문서는 [OQ-001](../OPEN_QUESTIONS.md)의 조사 관찰과 후보 비교를 기록한다. 조사
시점의 spike와 packet은 제품 Controller source, plugin manifest 또는 Phase 1 scaffold가
아니다. 현재 채택 결정은 [ADR-0010](../../adr/0010-controller-runtime-go.md)과 사용자
decision receipt에 기록한다.

## 질문과 범위

배포 크기, SQLite/FTS5, stdio MCP와 dual-host 설치를 기준으로 Controller 후보를
비교한다.

포함한 후보는 공식 MCP SDK를 붙일 수 있는 네 가지다.

- TypeScript/Node
- Python
- Go
- Rust

이번 packet에서 확인하지 않은 항목은 다음과 같다.

- 실제 Claude Code/Codex plugin manifest 설치·reload
- Linux/Windows 실행과 cross-compilation
- background daemon, lease heartbeat와 takeover 정책
- production schema, migration, security policy와 Controller domain 구현
- 성능·메모리의 대표 workload benchmark

따라서 `dual-host` 결과는 실제 host E2E가 아니라, 동일 entrypoint를 두 개의 독립
working directory/process에서 실행한 최소 설치성 proxy다.

## 평가 방법

모든 후보는 같은 `stdio_probe.py`로 다음 sequence를 수행했다.

```text
initialize (protocolVersion=2025-11-25)
→ notifications/initialized
→ tools/list
→ tools/call(echo, {message: "round-trip"})
→ stdin close / process exit
```

서버 시작 전에 각 후보가 다음 FTS5 동작을 실행한다.

```sql
CREATE VIRTUAL TABLE notes USING fts5(body);
INSERT INTO notes(body) VALUES ('geness controller runtime');
SELECT count(*) FROM notes WHERE notes MATCH 'controller'; -- 1
```

측정값의 의미는 다음과 같다.

- Go/Rust: `release` 단일 실행 파일의 byte size
- Node: `node_modules` dependency tree의 disk usage. Node runtime은 별도다.
- Python: Python 3.14 venv와 `site-packages` disk usage. Python runtime은 별도다.
- startup: 같은 machine에서 probe를 5회 실행한 MCP round-trip elapsed median. 첫 실행
  compile/install 비용은 포함하지 않는다.
- FTS5 PASS: 서버가 위 virtual table을 만들고 MATCH query 결과 1을 확인한 뒤 stdio에
  진입했다는 뜻이다.
- stdio PASS: initialize/list/call 모두 response가 current process에서 관찰되고
  exit status가 0이라는 뜻이다.

## 조사 환경

```text
OS/arch: macOS arm64
Go: go1.26.5
Rust: rustc 1.88.0 / cargo 1.88.0
Python: 3.14.6
Node: v22.23.0 / npm 10.9.8
Bun: 1.3.11 (후보 실행에는 사용하지 않음)
host sqlite3: 3.51.0, ENABLE_FTS5
```

실험 dependency와 build output은 `/tmp`의 disposable workspace에만 생성했으며,
repository에는 source와 이 packet만 보존한다.

## Candidate setup

### TypeScript/Node

사용한 package는 `@modelcontextprotocol/server@2.0.0`과 `zod@4.4.3`이다. SDK는
Node `>=20`을 선언한다.

```text
npm init -y                                      → exit 0
npm install --no-audit --no-fund \
  @modelcontextprotocol/server@2.0.0 zod@4.4.3  → exit 0
node --no-warnings node_server.mjs                → exit 0 (probe 실행 전 smoke)
```

`node:sqlite`로 FTS5를 확인했다. 현재 Node 22.23.0에서 SQLite version은 `3.51.3`으로
관찰됐다.

### Python

Python 3.14 호스트 runtime에서 `mcp==2.0.0`을 `uv`로 설치했다. package metadata의
최소 Python은 `>=3.10`이다.

```text
uv venv --python /opt/homebrew/bin/python3 py314env       → exit 0
uv pip install --python py314env/bin/python 'mcp==2.0.0'   → exit 0
py314env/bin/python --version                              → 3.14.6
```

stdlib `sqlite3`의 SQLite version은 `3.53.3`, `ENABLE_FTS5`는 true였다. 현재 package의
실제 server API인 `mcp.server.mcpserver.MCPServer`를 사용했다.

### Go

MCP SDK는 `github.com/modelcontextprotocol/go-sdk@v1.7.0`, SQLite driver는
`github.com/mattn/go-sqlite3@v1.14.49`다. FTS5는 driver의 `sqlite_fts5` build tag를
명시해야 한다.

```text
go mod init example.com/geness-oq001                    → exit 0
go get github.com/modelcontextprotocol/go-sdk/mcp@v1.7.0 → exit 0
go get github.com/mattn/go-sqlite3@v1.14.49              → exit 0
go mod tidy                                               → exit 0
go build -tags sqlite_fts5 -trimpath -ldflags '-s -w' \
  -o geness-go-probe .                                    → exit 0
```

### Rust

MCP SDK는 `rmcp@3.1.4`, SQLite는 `rusqlite@0.40.2` resolved package에 `bundled`
feature를 사용했다. `rmcp`는 `transport-io`와 `server` feature를 사용하고 Tokio를
async runtime으로 사용한다.

```text
cargo init --bin rust                                  → exit 0
cargo add rmcp@3.1.4 --features server,transport-io   → exit 0
cargo add rusqlite@0.40.1 --features bundled           → exit 0
cargo add serde@1 --features derive                     → exit 0
cargo add tokio@1 --features macros,rt-multi-thread    → exit 0
cargo build --release                                   → exit 0
```

`rusqlite`의 semver range 때문에 Cargo.lock에는 `0.40.2`가 resolved됐다. bundled
SQLite가 FTS5를 포함하는 것을 실제 query로 확인했다.

## 결과

| 후보 | FTS5 | stdio round-trip | 두 working directory | 배포 artifact 관찰값 | median elapsed |
| --- | --- | --- | --- | ---: | ---: |
| TypeScript/Node | PASS (`node:sqlite` 3.51.3) | PASS, exit 0 | PASS, 두 번 모두 exit 0 | `node_modules` 14,104 KB + Node runtime | 66.34 ms |
| Python | PASS (stdlib SQLite 3.53.3) | PASS, exit 0 | PASS, 두 번 모두 exit 0 | `site-packages` 34,328 KB + Python runtime | 304.78 ms |
| Go | PASS with `sqlite_fts5` | PASS, exit 0 | PASS, 두 번 모두 exit 0 | stripped Mach-O arm64 7,643,186 B | 5.66 ms |
| Rust | PASS with `rusqlite bundled` | PASS, exit 0 | PASS, 두 번 모두 exit 0 | release Mach-O arm64 5,168,560 B | 3.41 ms |

크기는 서로 다른 배포 모델을 측정하므로 직접적인 “누가 더 작다” 결론으로만
사용하지 않는다. Node/Python은 host runtime과 package install/cache 정책이 필요하고,
Go/Rust는 release artifact가 필요하다.

### Command evidence

동일한 probe를 `host-a`, `host-b` working directory에서 각각 실행했다. 아래는 두
실행 중 대표 output이며 두 후보별 두 실행 모두 probe exit status `0`이었다.

```text
python3 stdio_probe.py --cwd host-a -- \
  ../py314env/bin/python ../python_server.py
→ exit 0; protocol=2025-11-25; tools=[echo]; echo=round-trip

python3 stdio_probe.py --cwd host-a -- \
  node --no-warnings ../node/node_server.mjs
→ exit 0; protocol=2025-11-25; tools=[echo]; echo=round-trip

python3 stdio_probe.py --cwd host-a -- ../go/geness-go-probe
→ exit 0; protocol=2025-11-25; tools=[echo]; structuredContent.message=round-trip

python3 stdio_probe.py --cwd host-a -- ../rust/target/release/rust
→ exit 0; protocol=2025-11-25; tools=[echo]; echo=round-trip
```

5회 반복의 probe exit codes는 네 후보 모두 `[0, 0, 0, 0, 0]`이었다. 단일 machine의
짧은 smoke 측정이므로 release performance claim으로 승격하지 않는다.

### Negative evidence

Go driver를 FTS5 tag 없이 빌드하면 binary 자체는 build되지만, runtime capability
check가 실패한다.

```text
go build -trimpath -ldflags '-s -w' -o geness-go-probe-nofts . → exit 0
./geness-go-probe-nofts </dev/null
→ server exit 1; 2026/08/20 ... no such module: fts5
```

따라서 Go 후보를 채택하면 `sqlite_fts5`를 build contract와 CI/release matrix에
고정해야 한다. 이것은 단순한 optional optimization이 아니다.

Node 설치에서 SDK가 요구하는 Zod 버전보다 낮은 `zod@4.1.12`를 직접 설치했을 때
`tools/list`가 `[toJSONSchema]: Non-representable type encountered: string`으로
실패했다. `zod@4.4.3`으로 정렬한 뒤 PASS했다. SDK와 direct Zod dependency의
호환성 pin도 Node 후보의 package contract에 포함돼야 한다.

## Candidate trade-offs

### Go — provisional primary recommendation

장점:

- host에 Go/Python/Node를 설치하지 않아도 되는 단일 binary 배포 모델
- 공식 MCP Go SDK와 짧은 stdio 경로
- 네 후보 중 충분히 작은 binary와 낮은 startup elapsed
- Go module과 표준 library 기반 application/service 계층을 분리하기 쉬움

비용과 미결정:

- `go-sqlite3`는 CGO와 C compiler를 요구한다.
- FTS5 build tag 누락이 runtime failure로 이어지므로 release/CI 계약이 필요하다.
- Windows/Linux cross-build와 compiler matrix는 이번 macOS spike에서 검증하지 않았다.
- CGO를 제품에서 허용하지 않으면 이 후보의 SQLite 경로를 그대로 채택할 수 없다.

### Rust — binary/runtime isolation 우선 대안

장점:

- bundled SQLite로 OS SQLite version 및 runtime dependency를 줄일 수 있다.
- 가장 작은 measured binary와 가장 낮은 measured startup elapsed
- 공식 `rmcp`의 stdio transport와 현재 MCP protocol evolution에 대응하는 surface

비용과 미결정:

- Cargo dependency/build graph가 네 후보 중 가장 무겁고 compile iteration cost가 크다.
- Rust SDK와 SQLite binding version을 함께 관리해야 하며 release cross-build 검증이
  필요하다.
- 팀의 Rust 운영 역량과 binary supply-chain/target matrix를 사용자 결정으로 확인해야
  한다.

### TypeScript/Node — SDK/개발 속도 우선 대안

장점:

- 공식 TypeScript SDK의 stdio 문서·예제와 가장 짧은 개발 loop
- Node `>=20`이면 host runtime만으로 실행 가능하고, 이 환경의 `node:sqlite`에서 FTS5
  capability가 확인됐다.
- SDK가 tool schema를 JSON Schema로 변환하고 입력을 검증한다.

비용과 미결정:

- 단일 binary가 아니며 Node runtime과 dependency tree를 함께 설치·보존해야 한다.
- `node:sqlite`의 Node version별 stability/SQLite compile option을 setup에서 probe해야
  한다.
- Zod major/minor alignment를 package lock으로 고정해야 한다.

### Python — prototype/host runtime 우선 대안

장점:

- stdlib SQLite와 FTS5 접근이 단순하고 MCP server API를 빠르게 실험할 수 있다.
- `uv`로 dependency와 Python version을 재현할 수 있다.
- 데이터 처리·검증용 library 생태계가 넓다.

비용과 미결정:

- interpreter, venv/site-packages와 Python version policy가 설치 artifact에 포함된다.
- 이 spike의 site-packages가 34 MB를 넘고, cold-ish process round-trip이 네 후보 중
  가장 느렸다.
- host가 Python을 보유하지 않는 환경에서는 `uv`/embedded Python 또는 별도 packaging
policy가 필요하다.

## 권고안과 사용자 결정

조사 시점의 evidence만으로는 다음 순서를 권고했다.

1. **Go + CGO + 명시적 `sqlite_fts5`** — 단일 binary, 공식 SDK, 배포 크기와 개발
   복잡성의 균형이 가장 좋다.
2. **Rust + `rusqlite bundled`** — CGO와 OS SQLite 차이를 피하는 것이 최우선이고
   Rust build/release 비용을 감수할 때 선택한다.
3. **TypeScript/Node** — 설치 대상 host가 Node `>=20`을 보장하고 binary packaging보다
   SDK/개발 속도가 중요할 때 선택한다.
4. **Python** — Controller 본체보다 research/bootstrap 또는 Python runtime이 이미
   보장되는 배포 환경에 적합하다.

조사 시점의 사용자 결정지는 다음과 같았다.

```text
A. Go + CGO를 허용하고, macOS/Linux/Windows release binary를 별도 검증한다.
B. CGO를 피하고 Rust + bundled SQLite를 채택한다.
C. host-managed Node >=20을 전제로 TypeScript/Node를 채택한다.
D. host-managed Python/uv를 전제로 Python을 채택한다.
```

사용자는 **A. Go + CGO + 명시적 `sqlite_fts5`**를 선택했다. 이 선택은 단일 binary
방향을 채택하지만, cross-platform artifact와 FTS5/release matrix를 후속 검증해야 한다.

### User/authority decision receipt

- **Decision:** candidate A — Go + standard Go modules + CGO + explicit `sqlite_fts5`
- **Actor:** `user`
- **Recorded at:** `2026-08-22T16:05:46+09:00`
- **Receipt:** [USER-DECISION-OQ001-001](./evidence/OQ-001/USER-DECISION-RECEIPT-001.md)
- **Accepted ADR:** [ADR-0010](../../adr/0010-controller-runtime-go.md)

daemon 여부는 이 packet의 결론이 아니다. stdio 단발 process가 lease heartbeat 요구를
충족하는지는 별도 OQ-003에서 두 process trace로 조사한다.

## Artifact inventory and hashes

| Artifact | SHA-256 |
| --- | --- |
| `spikes/oq-001-controller-runtime/README.md` | `30d77dadaadd188b55c9b409c1f9b212654a7c7ffc69fbea71a898d597993beb` |
| `spikes/oq-001-controller-runtime/stdio_probe.py` | `b4fc3f21aaaa0ab61cc3dc811e2c65a1f74a5ba8bb305da818533cc4482d6450` |
| `spikes/oq-001-controller-runtime/python_server.py` | `40d50c8e208d83289bdfb350f0384295a27420ccb108a8827aa2a3ece4c31737` |
| `spikes/oq-001-controller-runtime/node_server.mjs` | `2e99d3318236934d72e151a0d37b04ef0de405acc07dcbaa394aafd54c6bcd1e` |
| `spikes/oq-001-controller-runtime/go_server.go` | `f677876c7fa9f426b4d7842f6762b4da8a18fe8a646c7f0683e26fb1d8531adb` |
| `spikes/oq-001-controller-runtime/rust_server.rs` | `1e67ef3327ab8db67f443e7be5b9cee69e0430f96571b06dcfe8998e29c2a9a1` |

Build binary hash는 host/architecture-specific disposable output이라 repository artifact로
보존하지 않았다. 위 source hash와 exact command가 spike input의 재현 기준이다.

## Sources and reuse record

공식 MCP/SQLite 문서와 package metadata만 조사했다. 외부 source code, prompt, template
또는 문서 문구를 복사해 배포 artifact에 포함하지 않았다.

- [MCP official SDK matrix, pinned repository revision](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/4df2d6b6e3588efb46e7542d98498e5c630a0a86/docs/docs/2026-07-28/sdk.mdx)
- [TypeScript SDK stdio/server guide, pinned revision](https://github.com/modelcontextprotocol/typescript-sdk/blob/3924de99df834302d89f5997a1b64ca268282284/docs/get-started/first-server.md)
- [Python SDK repository, pinned revision](https://github.com/modelcontextprotocol/python-sdk/tree/0d92192765fa7d6a20fbfe7e62e242e44933574f)
- [Go SDK repository, pinned revision](https://github.com/modelcontextprotocol/go-sdk/tree/b0408f2821d7a686b6cccff52c81539a4315b229)
- [Rust SDK stdio/feature documentation, pinned revision](https://github.com/modelcontextprotocol/rust-sdk/blob/4a738b9dd99eaca418b614afa433a0cbdaf8d056/README.md)
- [Go SQLite driver FTS5 build tag, pinned release](https://github.com/mattn/go-sqlite3/tree/cc41b8c87686036ea632cede537ffccef69b370a)
- [rusqlite bundled SQLite behavior, pinned release](https://github.com/rusqlite/rusqlite/tree/e88f112bef7899234a497baed5cc3c3d553deeb8)
- [SQLite FTS5 documentation](https://www.sqlite.org/fts5.html)
- [Node 22.23.0 SQLite documentation](https://nodejs.org/download/release/v22.23.0/docs/api/sqlite.html)
- [Python 3.14 sqlite3 documentation](https://docs.python.org/3.14/library/sqlite3.html)

MCP SDK 저장소의 라이선스와 별개로, 이번 변경은 API 사용을 확인한 disposable source만
추가했다. 실제 제품에 SDK 또는 외부 code를 포함하는 후속 변경에서는 해당 package의
license/notice를 다시 검토한다.

## Next gate

이 packet은 OQ-001의 조사 evidence와 사용자 선택, receipt와 Accepted ADR을 연결한다.
다음 검증 가능한 목표는 **OQ-003의 two-process heartbeat·grace·takeover fixture**다.
OQ-003/OQ-004/OQ-008/OQ-009의 packet-level evidence gap과 나머지 Phase 0 decision이 남아 있으므로
Progress의 product Implementation `HOLD`와 Phase 0 `HOLD`는 유지한다.
