---
run_id: "RUN-OQ009-001"
fixture_id: "FX-LIFECYCLE-LEASE-COMPLETION-001"
packet_id: "OQ-009"
observation_status: "pass"
---

# OQ-009 execution record

## Command outcomes

The runner source compiled successfully:

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Exit status: 0.

The exact fixture command was run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-LEASE-COMPLETION-001/runner.py

Both runs returned exit status 0 and each reported 7 assertions with
all_assertions_pass=true. Their stdout JSON values parsed and compared equal after
ignoring formatting only.

## Synthetic replay observation

The fixture started with terminal_checkpoint=true, lease_active=true and completed=false.

- First replay yielded completed=true and lease_active=false.
- Second replay yielded an equality-equivalent result: completed=true and lease_active=false.
- The replay was therefore idempotent within this synthetic fixture.

This is a minimal fixture observation. It is not proof of a production SQLite
transaction, crash-point matrix, projection atomicity, or recovery guarantee.

## Pending decisions and evidence gaps

The fixture does not decide:

- terminal checkpoint versus writer lease-release ordering
- runtime transaction versus project-document projection ordering
- lease takeover, heartbeat grace, or two-writer authority
- completion Gate, reconciliation, or user receipt requirements

OQ-009 remains pending user decision. No Runtime/Lifecycle ADR, production schema,
daemon policy, or Implementation CLEAR is claimed.

## Hashes

No fixture or input SHA-256 was known from the repository at record-creation time:

- runner.py: bbdcb46779c33c463e088764a817e55e1c4d32cb237113f1ced7586b970014e5
- input/fixture.json: c1402c463a01ec3c1f4b292664263d267093d0238587254fdf54fdb5f1cc090e
