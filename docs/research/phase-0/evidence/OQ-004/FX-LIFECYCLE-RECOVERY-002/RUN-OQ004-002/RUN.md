---
run_id: "RUN-OQ004-002"
fixture_id: "FX-LIFECYCLE-RECOVERY-002"
packet_id: "OQ-004"
observation_status: "pass"
candidate_selected: false
---

# OQ-004 lifecycle recovery follow-up

## Command and result

The source validation command returned exit `0`:

    python3 -m py_compile docs/research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/runner.py

The exact fixture command was run twice:

    PYTHONDONTWRITEBYTECODE=1 python3 docs/research/phase-0/fixtures/FX-LIFECYCLE-RECOVERY-002/runner.py

Both executions returned exit `0`, reported `14/14` assertions with
`all_assertions_pass=true`, and their raw JSON output compared equal with `cmp`.
The output declared `network=disabled`, `external_writes=false` and
`candidate_selected=false`.

## Observed candidate comparison

- C-01 and C-02 allow `FAILED → REOPENED` only with an explicit user receipt;
  C-03 returns `DENIED` as a terminal candidate.
- C-01 and C-03 return `DENIED` for `CANCELLED → REOPENED`; C-02 allows it only
  with an explicit user receipt.
- Reopen without a user receipt returns `DENIED` with
  `explicit_user_reopen_required`.
- An attempt-level `FAIL` remains distinct from task-level `FAILED` and routes to
  `successor_or_blocked` in this synthetic projection.
- Completion exposure returns `DENIED` when the terminal checkpoint is missing or
  an active lease remains, and returns `ALLOWED` only after checkpoint and lease
  release conditions are present.
- The synthetic completion order is `READY_TO_COMPLETE` → final run projection →
  terminal checkpoint → lease release → `COMPLETED` exposure.
- Failure event → candidate creation → missing independent evidence leaves the
  candidate unverified and hidden from the general memory query projection.

These observations compare all three packet candidates. The fixture output itself does not
select a candidate; the later user decision receipt and ADR record C-01.

## Pending decisions and limitations

The fixture does not decide the exact lifecycle contract, Plan Gate actor/risk policy,
completion transaction ordering, or receipt validation implementation. It is a deterministic
synthetic projection and does not
reproduce production persistence, SQLite atomicity, crash replay, lease takeover,
independent verifier authority or user decision receipt validation.

At execution time OQ-004 was `blocked`; it is now resolved as C-01 by the subsequent
[user decision receipt](../../USER-DECISION-RECEIPT-001.md) and [ADR-0013](../../../../../../adr/0013-task-lifecycle-recovery.md).
No production schema or Implementation `CLEAR` is claimed.

## Hashes

- commit under test: `a5e363cb120f92b46496e49a9a55bff21315240b`
- runner.py: `2410d4744e1db936812edcd12e2647ea0ce833d12b21adfda24ddade42369e5f`
- input/fixture.json: `8afb0ce03084e75802d035ead7d7bf3ce073408fa100db0c803ad7185612121a`
