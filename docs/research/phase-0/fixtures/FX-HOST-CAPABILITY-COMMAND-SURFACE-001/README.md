# FX-HOST-CAPABILITY-COMMAND-SURFACE-001

## fixture_id

`FX-HOST-CAPABILITY-COMMAND-SURFACE-001`

## packet_id / question_id

- packets: `OQ-012`, `OQ-014`
- questions: `OQ-012`, `OQ-014`

## purpose

Probe the installed Codex and Claude command surfaces without starting an agent run,
then compare a fixture-local `gee` setup/status/resume/description router through a
library path, a CLI thin transport, and an MCP-like stdio transport. The fixture is
research evidence only; it does not create a plugin, select a production runtime, or
write Geness state.

## category

Disposable Phase 0 host capability and command-surface parity fixture.

## inputs and preconditions

- Synthetic expectations and route/profile cases: `input/fixture.json`.
- `codex` and `claude` are expected to be on `PATH` for the local capability probe.
- The probe uses only `--version`, `--help`, `features list`, and other read-only help
  surfaces. It does not start an agent, authenticate, install a plugin, or connect to
  an MCP server.
- Python 3 standard library only.

## exact command

From this directory:

```text
PYTHONDONTWRITEBYTECODE=1 python3 runner.py
```

The runner starts fixture-local CLI and MCP transports in a per-run temporary directory.
Their state is synthetic and unrelated to a target repository or `GENESS_HOME`.

## expected observation

- The installed Codex and Claude binaries return exit `0` for the read-only capability
  probes and expose the required version, plugin, skill, hook, MCP, and non-interactive
  command tokens.
- `auto` selects `cross-model` when Codex is ready and falls back to `claude-only` only
  for a new task when Codex is unavailable.
- Explicit `cross-model` stops at setup attention when Codex is unavailable; explicit
  `claude-only` does not require Codex; an active task never silently changes profile.
- Explicit `gee` commands, host aliases, and natural-language descriptions produce the
  same canonical intent. Ambiguous descriptions return a typed choice-required result.
- The library, CLI, and MCP projections agree for setup, status, resume, and routing;
  malformed CLI input and unknown MCP methods remain transport errors.

## expected runner exit status

`0` when every host probe, profile policy assertion, route assertion, and transport parity
assertion passes. A missing host binary or changed help surface is an observable fixture
failure, not a reason to rewrite the expected result.

## isolation and network policy

- Network is disabled by procedure: no package installation, login, agent prompt, or MCP
  server is started.
- Codex help probes use a per-run temporary `CODEX_HOME`; no real Codex configuration is
  read or modified.
- Surface transports use only a per-run `tempfile.TemporaryDirectory`.
- Raw host stdout/stderr is hashed and discarded; the runner emits only normalized version,
  exit-status, token-match, and result projections.

## external-write policy

No external writes. The fixture does not modify this repository, a target repository,
plugin cache, `~/.geness/`, or host configuration.

## cleanup boundary

The runner owns and removes only its own temporary directory. No repository, home,
branch, worktree, plugin, or global cache cleanup is performed.

## retention plan

- `tracked`: this README, `input/fixture.json`, and fixture-local runner/transports.
- `packet`: redacted result manifests copied to the OQ-012/OQ-014 evidence directories
  after actual runs.
- `discarded`: raw host help output, transport wire lines, and temporary synthetic state;
  only hashes and normalized observations are retained.
