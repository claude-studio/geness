---
run_id: "RUN-OQ007-002"
fixture_id: "FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001"
packet_id: "OQ-007"
observation_status: "pass"
---

# OQ-007 execution record — current revalidation

## Command and result

Fixture working directory:

    docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001

The exact fixture command was executed twice on 2026-08-22:

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

- both executions returned exit `0`, 30/30 assertions and `all_assertions_pass=true`
- `cmp` of the two JSON stdout values returned exit `0`
- paired stdout SHA-256: `sha256:4adfd380c2f0094803b2b3645a330b5645472418a7ea6ea8953d32398626f051`
- the result declared `network=disabled` and `external_writes=false`

## Observed result

- reordered contract and plan object keys retained their base digest;
- contract semantic goal change and plan semantic step addition produced different digests;
- the raw Markdown editorial variant differed under raw-byte hashing;
- the fixture's invalidation observation was `contract_and_downstream_plan_stale` for a
  semantic contract change and `digest_unchanged_under_semantic_projection` for an editorial
  change.

The fixture also passed the shared identity, frontmatter/SQLite projection, stale-write and
portable/runtime boundary assertions. Those observations remain fixture-local and are not
production schema or serializer evidence.

## Artifact and validation commands

- current result manifest: [result.json](./result.json)
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile runner.py` → exit `0`
- `python3 -m json.tool input/fixture.json >/dev/null` → exit `0`
- `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` twice → exit `0` for both runs
- `cmp` of paired stdout → exit `0`
- `python3 -m json.tool` on paired stdout → exit `0`
- `jq` assertion summary on a current run → exit `0`, `true 30 30 disabled false`
- `sha256sum` on paired stdout → exit `0`, `4adfd380c2f0094803b2b3645a330b5645472418a7ea6ea8953d32398626f051`

## Decision status

The subsequent delegated C-01 decision is recorded in [USER-DECISION-OQ007-001](../../USER-DECISION-RECEIPT-001.md)
and [ADR-0017](../../../../../../adr/0017-versioned-semantic-digest.md). This evidence does
not select a production serializer, schema or implementation `CLEAR`.
