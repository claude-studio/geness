# FX-COMMAND-API-TYPED-RESULT-001

## fixture_id

`FX-COMMAND-API-TYPED-RESULT-001`

## packet_id / question_id

- packet: `OQ-002`
- question: `OQ-002`

## purpose

Compare one synthetic command through a fixture-local common application service, a
CLI thin transport, and an MCP-like stdio thin transport. The fixture observes typed
domain `HOLD`, transport errors, and idempotent replay without selecting a production
language, package manager, runtime, schema, daemon, or scaffold.

## category

Disposable Phase 0 contract/acting fixture. Python is used only as a dependency-free
runner implementation; it is not a Controller-language recommendation.

## inputs and preconditions

- Synthetic input: `input/fixture.json`.
- Python 3 standard library only.
- The runner is executed from this fixture directory or with its path resolved.
- No target repository, `.geness/`, real `GENESS_HOME`, credentials, or network access
  is needed.

## exact command

From this directory:

```text
PYTHONDONTWRITEBYTECODE=1 python3 runner.py
```

The runner starts the following thin transports in per-run temporary state directories:

```text
python3 cli_transport.py --state <run-temp>/cli-state.json
python3 mcp_transport.py --state <run-temp>/mcp-state.json
```

The library path calls `ApplicationService` directly in the runner process. The CLI and
MCP paths import the same `common_service.py`; the transport files contain no domain
decision constants.

## expected observation

- All three paths return the same domain `HOLD` projection for the unapproved gate
  command.
- All three paths return the same semantic result for the first decision (`APPLIED`)
  and the replay (`REPLAYED`), with one stored side effect and one stable effect ID.
- Invalid CLI JSON is a typed `transport_error` with process exit `2` and does not call
  the application service.
- An unknown MCP method is a JSON-RPC transport error (`-32601`) with process exit `0`
  and does not call the application service.
- A domain `HOLD` is a successful transport exchange (exit `0`) and is not rewritten as
  a transport error.

## expected runner exit status

`0` when every comparison and boundary assertion passes; non-zero when the fixture
cannot establish the expected observation.

## isolation and network policy

- State files and all raw subprocess output are created below one per-run
  `tempfile.TemporaryDirectory` and are removed when the runner exits.
- Network is disabled by procedure: no network command, package install, or external
  service is used.
- The fixture does not use or override the real `GENESS_HOME` because it has no product
  runtime state.

## external-write policy

No external writes. The fixture writes only synthetic state below its run-specific temp
directory and stdout from the runner.

## cleanup boundary

The runner owns and removes only its own temporary directory. There is no repository,
target, home, branch, worktree, or global cache cleanup.

## retention plan

- `tracked`: this README, the runner/transport source, and synthetic input.
- `packet`: a redacted result manifest copied into the OQ-002 evidence directory after
  an actual run.
- `local-only`/`discarded`: raw subprocess stdout/stderr and intermediate JSON state;
  the packet records the run status and artifact hash without retaining raw logs.
