---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ007-001"
question_ids:
  - "OQ-007"
authority: "user"
recorded_at: "2026-08-22T15:02:35Z"
source: "Explicit AUTOPILOT delegation in the task prompt"
---

# User decision receipt — OQ-007

## Decision

The delegated autonomous-delivery policy adopts candidate C-01: contract and plan
digests use a versioned semantic projection and canonical JSON profile rather than raw
Markdown bytes. The v1 contract identifier is `geness.semantic-json-v1` and the hash
algorithm is SHA-256.

- Contract and plan semantic fields are projected explicitly before hashing.
- Object key ordering and editorial Markdown body are excluded from semantic identity;
  meaningful array order is preserved.
- Semantic contract changes invalidate approval and downstream plan/run state.
- Profile/version metadata is stored with the digest in the portable projection and
  runtime canonical state.

This is a delegated decision record; it does not fabricate an interactive user message.
The adoption is permitted by the task's AUTOPILOT rule because the packet recommendation
is clear, the required fixture assertions passed deterministically twice, no contradictory
digest policy was found in repository evidence, and the choice remains within the packet's
docs/research scope.

## Rationale and evidence

`FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001` returned exit `0` twice with 30/30 assertions and
`all_assertions_pass=true`. Paired stdout comparison returned exit `0` and the SHA-256 was
`sha256:4adfd380c2f0094803b2b3645a330b5645472418a7ea6ea8953d32398626f051`.

The fixture observed equal digests for reordered contract/plan object keys, distinct
digests for semantic changes, and a raw Markdown editorial negative control that changed
under byte hashing. The result was network-disabled and performed no external writes.

## Unresolved scope

This receipt does not select RFC/JCS compatibility, production serializer code, exact
cross-runtime number/Unicode/duplicate-key/escaping rules, schema migration behavior or
Implementation `CLEAR`. Those remain required evidence before product implementation.

## Linked artifacts

- [OQ-007 packet](../../OQ-007-digest-canonicalization.md)
- [ADR-0017](../../../../adr/0017-versioned-semantic-digest.md)
- [current execution record](./FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-002/RUN.md)
- [current result manifest](./FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ007-002/result.json)
