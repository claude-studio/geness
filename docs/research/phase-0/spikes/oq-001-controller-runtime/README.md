# OQ-001 disposable controller-runtime spike

이 디렉터리는 Phase 0 OQ-001의 후보 비교를 위한 폐기 가능한 spike artifact다.
Geness 제품 source, manifest 또는 Controller scaffold가 아니다.

## Probe contract

각 후보는 같은 최소 동작을 제공한다.

- SQLite in-memory FTS5 virtual table 생성·insert·MATCH query
- MCP stdio server 시작
- `echo` tool 노출
- `initialize` → `tools/list` → `tools/call` JSON-RPC round-trip
- 서로 다른 working directory에서 동일 entrypoint를 두 번 실행

`stdio_probe.py`는 서버의 stdout을 MCP JSON-RPC channel로만 취급한다. 서버 로그는
stderr로 수집한다. probe는 제품의 host manifest 또는 실제 Claude/Codex installation을
검증하지 않으며, dual-host 결과는 “동일 entrypoint를 두 개의 독립 process가 실행할 수
있는가”에 대한 최소 proxy다.

## Candidate inputs

| Candidate | MCP SDK | SQLite path | Runtime |
| --- | --- | --- | --- |
| TypeScript/Node | `@modelcontextprotocol/server@2.0.0` | Node `node:sqlite` | Node >=20 (measured 22.23)
| Python | `mcp==2.0.0` | stdlib `sqlite3` | Python >=3.10 (measured 3.14.6)
| Go | `github.com/modelcontextprotocol/go-sdk@v1.7.0` | `mattn/go-sqlite3@v1.14.49`, `sqlite_fts5` tag | Go + CGO
| Rust | `rmcp@3.1.4` | `rusqlite@0.40.1`, `bundled` | Tokio

Exact commands, exit status, measured sizes and source links are recorded in the decision
packet one directory above this spike.

## Reproduction outline

The source files are copied to disposable package-manager workspaces before running. Build
outputs and dependency trees are not committed here.

```text
python3 stdio_probe.py --cwd <isolated-dir> -- <candidate-command>
```

Candidate-specific dependency setup and build commands are recorded in
`../OQ-001-controller-runtime.md` after execution.
