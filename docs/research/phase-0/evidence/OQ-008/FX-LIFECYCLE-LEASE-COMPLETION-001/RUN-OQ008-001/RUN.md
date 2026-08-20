---
run_id: "RUN-OQ008-001"
fixture_id: "FX-LIFECYCLE-LEASE-COMPLETION-001"
packet_id: "OQ-008"
observation_status: "pass"
---

# OQ-008 execution record

## Command outcomes

The runner source compiled successfully:

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Exit status: 0.

The exact fixture command was run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Both runs returned exit status 0, each reported 7 assertions with
all_assertions_pass=true, and their stdout JSON values parsed and compared equal after
ignoring formatting only.

## Fixture observation

The fixture observed:

- PLAN_APPROVED → RUNNING with digest_current=false: DENIED
- denial reason: stale_digest

This is an observation of the fixture's stale-revision guard. It is not a decision about
who may approve a plan.

## Unresolved approval policy

The fixture does not choose or finalize any of the following:

- whether every PLAN_APPROVED action requires a human actor
- whether a policy actor may approve low-risk or ordinary plans
- the risk, scope, external-write, destructive-action, or security thresholds
- the required form of a user approval receipt

The OQ-008 user decision remains pending. No approval policy, Lifecycle/Specification
ADR, production schema, or Implementation CLEAR is claimed.

## Hashes

No fixture or input SHA-256 was known from the repository at record-creation time:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
