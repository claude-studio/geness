---
run_id: "RUN-OQ003-001"
fixture_id: "FX-LEASE-LIVENESS-TAKEOVER-001"
packet_id: "OQ-003"
observation_status: "pass"
---

# OQ-003 execution record

## Command and result

Fixture working directory:

    docs/research/phase-0/fixtures/FX-LEASE-LIVENESS-TAKEOVER-001

Exact fixture command, run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

Both executions returned exit `0`, reported 17/17 assertions with
`all_assertions_pass=true`, and produced byte-identical stdout and stderr hashes.

Additional source check:

    PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile runner.py

The compile command returned exit `0`.

## Observed result

- Two distinct child processes started as writer-A and observer-B; no daemon process was
  started by the fixture.
- writer-A acquired the lease at logical time `0`, and its heartbeat at time `2` extended
  the grace deadline to `5`.
- observer-B takeover attempts at logical times `3`, `4` and the exact grace deadline `5`
  were `DENIED` with `grace_active`.
- writer-A was alive immediately before an abrupt `SIGKILL` interruption and exited with
  status `-9`.
- observer-B takeover at time `4` and at the exact deadline `5` remained `DENIED` during
  grace, then takeover at time `6`
  was `ALLOWED` with `stale_takeover` and previous owner writer-A.
- observer-B heartbeat at time `7` was `ALLOWED`; final state generation was `2`, owner
  observer-B and event count `7`.

The redacted result manifest preserves the deterministic timeline without child PIDs,
temporary paths or raw process output.

## Run metadata

| run_id | started_at | ended_at | exit_status | stdout SHA-256 | stderr SHA-256 | stderr |
| --- | --- | --- | ---: | --- | --- | --- |
| `RUN-OQ003-001` | 2026-08-22T08:06:41Z | 2026-08-22T08:06:41Z | 0 | `0dcbf11c6df7619e16e9af50856fa281e854f16be6fe8b6082bf49d0d8c1c8ab` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty |
| `RUN-OQ003-002` | 2026-08-22T08:06:41Z | 2026-08-22T08:06:41Z | 0 | `0dcbf11c6df7619e16e9af50856fa281e854f16be6fe8b6082bf49d0d8c1c8ab` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty |

## Artifact and cleanup boundary

- `result.json` is a redacted deterministic manifest retained as packet evidence.
- The retained result manifest SHA-256 is
  `9c53e1155125f44e44812933ffca9a03abfe65e6d4068026fa005046818da0a1`.
- Raw child stdout/stderr, temporary state, lock and atomic-write files were not retained;
  their hashes and empty-stderr observation are recorded above.
- The runner reported `network=disabled` and `external_writes=false`. No target `.geness/`,
  real `GENESS_HOME`, repository state or credential was used.

## Scope limitations

This fixture observes a logical lease protocol with POSIX file locking and two child
processes. It does not implement or select a production daemon, sidecar, SQLite schema,
cross-workspace writer authority, clock source, lease threshold or Runtime ADR. It does not
compare installation or operational cost of C-01/C-02/C-03.
