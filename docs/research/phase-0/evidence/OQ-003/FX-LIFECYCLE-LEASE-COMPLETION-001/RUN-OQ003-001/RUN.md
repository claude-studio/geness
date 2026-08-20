---
run_id: "RUN-OQ003-001"
fixture_id: "FX-LIFECYCLE-LEASE-COMPLETION-001"
packet_id: "OQ-003"
observation_status: "pass"
---

# OQ-003 execution record

## Command and result

Fixture working directory:

    docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001

Exact fixture command, run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Both executions returned exit 0. Both stdout values parsed as JSON and compared equal
after JSON parsing, so formatting differences were ignored.

Additional validation:

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

The compile command returned exit 0. The two-run validation wrapper returned exit 0.

## Observed result

The fixture reported 7 assertions and all assertions passed:

- INITIALIZING → INTERVIEWING: ALLOWED, reason fixture_rule
- PLAN_APPROVED → RUNNING with digest_current=false: DENIED, reason stale_digest
- INTERVIEWING → RUNNING: DENIED, reason edge_not_allowed
- first writer claim: ALLOWED
- second writer claim: DENIED
- first completion replay: terminal_checkpoint=true, lease_active=false, completed=true
- second completion replay: byte/equality-equivalent JSON result

The fixture output declared network disabled and external_writes false.

## Artifact hashes

The requested SHA-256 values were not computed during this single-action evidence-file
creation, so they are not asserted here:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e

## Scope limitations

This is a minimal evidence-only runner. It does not implement or select a product
language, package manager, runtime, production schema, daemon, or scaffold. The lease
probe is a sequential exclusive-file claim, not a multi-process heartbeat/grace-period
or stale-writer takeover implementation. It therefore cannot decide daemon necessity,
lease authority, takeover timing, or the OQ-003 Runtime ADR.

The transition and replay observations are fixture rules only. They do not finalize
FAILED/CANCELLED semantics, Plan Gate actor policy, completion transaction ordering, or
any user decision receipt.

## Decision status

OQ-003 remains pending user decision. No daemon policy, runtime ADR, or implementation
CLEAR is claimed by this record.
