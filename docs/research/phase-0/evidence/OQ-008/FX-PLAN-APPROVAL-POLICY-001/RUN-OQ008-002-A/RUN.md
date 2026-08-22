---
run_id: "RUN-OQ008-002-A"
fixture_id: "FX-PLAN-APPROVAL-POLICY-001"
packet_id: "OQ-008"
started_at: "2026-08-22T10:40:37Z"
ended_at: "2026-08-22T10:40:37Z"
cwd: "docs/research/phase-0/fixtures/FX-PLAN-APPROVAL-POLICY-001"
command: "PYTHONDONTWRITEBYTECODE=1 python3 runner.py"
exit_status: 0
observation_status: "pass"
stdout_ref: "discarded after paired byte comparison; sha256=cd964c1db1a12f390301896dd92a89386fcef17e7897f3c7eb70246936513684"
stderr_ref: "discarded after paired byte comparison"
artifact_refs:
  - "runner.py sha256=a8d5b86389230531ddf0afe7c956882c730a67d9844d1b2cdec93c6cd59c5e5f"
  - "input/fixture.json sha256=1b3e1106847ceb3d57119ba82d84f86326723d289b880f1cc3d341f2012f7654"
redaction: "none required; synthetic output only"
---

# OQ-008 execution record — paired run A

The fixture returned exit status 0 and reported 31/31 assertions with
`all_assertions_pass=true`. Its stdout and stderr were byte-identical to paired run B.

Observed matrix:

| scenario | C-01 | C-02 | C-03 |
| --- | --- | --- | --- |
| routine read-only | `ALLOWED/user` | `ALLOWED/policy` | `ALLOWED/policy` |
| routine local write | `ALLOWED/user` | `ALLOWED/policy` | `ALLOWED/user` |
| scope expansion | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| external write | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| destructive action | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| security-boundary change | `ALLOWED/user` | `ALLOWED/user` | `ALLOWED/user` |
| stale digest | `DENIED/none` | `DENIED/none` | `DENIED/none` |

`selected_candidate` remained `null`. Raw stdout/stderr was discarded after the paired
comparison; only the synthetic observation summary and hashes are retained.
