---
run_id: "RUN-OQ004-001"
fixture_id: "FX-LIFECYCLE-LEASE-COMPLETION-001"
packet_id: "OQ-004"
observation_status: "pass"
---

# OQ-004 execution record

## Command and result

Exact fixture command, run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Both executions returned exit 0. Each output reported 7 assertions with
all_assertions_pass=true. Both stdout values parsed as JSON and compared equal after
JSON parsing, ignoring formatting only.

The source validation command also returned exit 0:

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

## Observed transition edges

The run directly observed:

- INITIALIZING → INTERVIEWING: ALLOWED, reason fixture_rule
- PLAN_APPROVED → RUNNING with digest_current=false: DENIED, reason stale_digest
- INTERVIEWING → RUNNING: DENIED, reason edge_not_allowed

The runner defines FAILED → REOPENED as an allowed recovery edge. It was not separately
invoked by the 7 assertion cases in this minimal run, so this record does not claim an
independent execution observation for that edge. A follow-up lifecycle fixture must
exercise explicit user-reopen authority and the full FAILED trace.

The run also observed an exclusive writer probe with first writer ALLOWED and second
writer DENIED, and completion replay with terminal_checkpoint=true, lease_active=false
and completed=true on both replay projections. Those are supporting concurrency/replay
observations, not a finalized lifecycle contract.

## User decisions still pending

This evidence does not decide:

- whether CANCELLED is terminal, explicitly reopenable, or has another recovery route
- whether PLAN_APPROVED requires a user actor for every plan or permits policy approval
- the exact lifecycle state machine, FAILED recovery semantics, or completion Gate

Those remain user decisions. No Lifecycle ADR, production state schema, or
Implementation CLEAR is claimed.

## Hashes

No fixture or input SHA-256 was known from the repository at record-creation time:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
