---
run_id: "RUN-OQ009-002-A"
fixture_id: "FX-LIFECYCLE-LEASE-COMPLETION-001"
packet_id: "OQ-009"
started_at: "2026-08-22T11:06:43Z"
ended_at: "2026-08-22T11:06:43Z"
cwd: "docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001"
command: "PYTHONDONTWRITEBYTECODE=1 python3 runner.py"
exit_status: 0
observation_status: "pass"
stdout_ref: "result.json sha256=219b98005ecac98195dbe4c29ba4b8a5b58d9825dfbb84e6e8367d715269e4db"
stderr_ref: "empty; discarded after paired comparison"
artifact_refs:
  - "runner.py sha256=9c3361989c10fd361a67e0432c88a6573ebfe399f639b791f8442623adb1cc54"
  - "input/fixture.json sha256=bc5d871017fd45b8aeed16d2c71a1587992ee4a4e3affaab300c9e319e2b8147"
  - "result.json sha256=219b98005ecac98195dbe4c29ba4b8a5b58d9825dfbb84e6e8367d715269e4db"
redaction: "none required; synthetic output only"
runtime: "Python 3.9.6"
fixture_revision: "fe59953e51fa90a43783716d9147201b1da56086"
---

# OQ-009 execution record — crash-point matrix run A

The fixture returned exit status 0 and reported 43/43 assertions with
`all_assertions_pass=true`. Run B returned the same exit status and its stdout was
byte-identical to this run.

The matrix covered C-01, C-02 and C-03 at `after_projection`, `after_lease_release`,
`after_terminal_checkpoint` and `after_runtime_commit`. C-01 was safe at all four
crash points. C-02 observed `lease_released_before_terminal_checkpoint` after
`after_lease_release`. C-03 observed `completed_exposed_before_runtime_commit` at
the first three points. Every row converged to a safe state after operation-id
replay, and a second replay was equality-equivalent.

Raw stdout was retained as the small synthetic `result.json`; stderr was empty and
discarded after the paired comparison.
