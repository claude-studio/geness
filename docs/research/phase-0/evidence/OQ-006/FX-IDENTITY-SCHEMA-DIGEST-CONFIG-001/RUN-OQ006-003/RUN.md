---
run_id: "RUN-OQ006-003"
fixture_id: "FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001"
packet_id: "OQ-006"
observation_status: "pass"
---

# OQ-006 execution record — current revalidation

## Command and result

Fixture working directory:

    docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001

The exact fixture command was executed twice on 2026-08-22:

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

- both executions returned exit `0`, 30/30 assertions and `all_assertions_pass=true`
- `cmp` of the two JSON stdout values returned exit `0`
- paired stdout SHA-256: `sha256:4adfd380c2f0094803b2b3645a330b5645472418a7ea6ea8953d32398626f051`
- the current result summary reported `network=disabled` and `external_writes=false`

The current result manifest is retained as [A-006](./result.json). Its normalized observation
envelope records the same semantic observations: frontmatter/SQLite round-trip equality,
accepted revision 2, stale revision denial without mutation, identity relations, digest
invalidation and zero portable/machine field overlap.

## Evidence artifact drift

The historical A-001/A-004 manifests remain retained as records of the earlier run, but a
read-only normalized comparison against the current runner output returned exit `1`: their
observation envelope uses flattened legacy fields while the current runner emits nested
`identity`, `digest`, `frontmatter_db_round_trip` and `stale_write` fields. This is an evidence
projection drift, not a fixture assertion failure. A-006 is the current manifest for this
revalidation; the mismatch is tracked for follow-up before relying on historical hashes.

## Validation commands

- `PYTHONDONTWRITEBYTECODE=1 python3 runner.py` twice → exit `0` for both runs
- `cmp` of paired stdout → exit `0`
- `python3 -m json.tool` on the paired stdout → exit `0`
- `jq` assertion summary on a current run → exit `0`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile runner.py` → exit `0`
- `python3 -m json.tool input/fixture.json >/dev/null` and current result manifest parse → exit `0`
- read-only Ruby YAML frontmatter check → exit `0`, `frontmatter_checked=37`, `errors=0`
- read-only Node Markdown link/anchor/fence check → exit `0`, `markdown_files=91`,
  `local_links=417`, `local_anchor_links=27`, `fence_delimiters=154`,
  `trailing_whitespace=0`, `errors=0`
- `git diff --check --` → exit `0`

## Decision status

OQ-006 remains pending user decision. This revalidation does not create an ADR, select a
production schema, create a product scaffold or change the Implementation `HOLD`.
