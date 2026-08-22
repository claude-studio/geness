---
run_id: "RUN-OQ007-001"
fixture_id: "FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001"
packet_id: "OQ-007"
observation_status: "pass"
---

# OQ-007 execution record

## Command and result

Fixture working directory:

    docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001

The exact fixture command was executed twice:

    PYTHONDONTWRITEBYTECODE=1 python3 runner.py

- 2026-08-21T00:49:56Z / 2026-08-21T00:49:57Z: exit `0`, 30/30 assertions, `all_assertions_pass=true`
- 2026-08-21T00:49:57Z / 2026-08-21T00:49:57Z: exit `0`, 30/30 assertions, `all_assertions_pass=true`

The two stdout values were parsed as JSON and compared equal. The fixture declared
`network=disabled` and `external_writes=false`.

## Observed result

- local Git clone, rename, worktree and synthetic explicit fork probe passed.
- clone/worktree share the synthetic project relation while workspace relations are distinct;
  folder rename preserves both relations; fork and same-name repository are detached.
- frontmatter/SQLite semantic and body round-trip passed.
- accepted revision 2 write was ALLOWED; stale revision 1 write was DENIED with
  `reason=stale_revision`, and state remained unchanged.
- contract and plan golden vectors passed; reordered object keys were equal, semantic changes
  differed, and the raw Markdown editorial negative control differed.
- portable/local config boundary had zero field overlap and zero forbidden portable fields.

## Artifact hashes

- runner.py: `sha256:42475a16c6e8136000eb5ee03297bef289a795e50af69855499ce4694c5e2a61`
- input/fixture.json: `sha256:06a74865a1852918d61e5cec7138dc521beee6084234bfee9d585b32de98fc4e`
- fixture README: `sha256:7be95ce69ec566482f376ab5542d615f5fc40456dede8f480eedb2a68bb2315a`
- result manifest (both runs): `sha256:5bd6d0ecc1d0871a697a323292b7fe83703229eebadaba2f3a02f613c37fa075`

## Validation commands

- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/runner.py` → exit `0`
- `python3 -m json.tool docs/research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/input/fixture.json >/dev/null` → exit `0`
- `python3 -m json.tool docs/research/phase-0/evidence/OQ-007/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-001/result.json >/dev/null` → exit `0`
- `git diff --check --` → exit `0`
- read-only Markdown local-link/fence check → exit `0`, `markdown_files=57`, `local_links=147`, `fence_delimiters=122`, `trailing_whitespace=0`, `errors=[]`
- tool versions: Python `3.14.5`, Git `2.53.0`

## Scope limitations

This is a minimal evidence-only fixture. It does not implement or select a product language,
package manager, runtime, production schema, migration, daemon, config file, task machine JSON,
cross-language serializer or scaffold. The temporary Git probe does not decide hosted fork
semantics; the parser and SQLite table are fixture-local.

## Decision status

OQ-007 remains pending user decision. No ADR, product schema, config policy or
Implementation CLEAR is claimed by this record.
