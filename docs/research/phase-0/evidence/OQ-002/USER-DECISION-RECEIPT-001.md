---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ002-001"
question_ids:
  - "OQ-002"
authority: "user"
recorded_at: "2026-08-22T16:44:59+09:00"
source: "Explicit user confirmation in Codex session"
---

# User decision receipt — OQ-002

## Decision

The user selected candidate C-01: the shared application service is the canonical
command API boundary, while CLI and MCP are thin transports.

- The shared application service owns domain policy, typed domain results and idempotency.
- CLI and MCP call the same application service and preserve its domain result envelope.
- Transports may add only transport-specific errors, such as malformed CLI input or an
  unknown MCP method.
- A valid domain `HOLD` remains a successful transport exchange; transport failure is not
  inferred from the domain result.

## Unresolved scope

This receipt does not select final public command names, MCP tool schemas or protocol
versions, production schema/digest formats, daemon/lease policy, installed-host behavior,
or product scaffold. Those remain owned by OQ-003, OQ-006/OQ-007, OQ-012/OQ-014 and later
implementation evidence. The selected boundary does not change the product-level
Implementation `HOLD`.

## Linked artifacts

- [OQ-002 canonical command API packet](../../OQ-002-canonical-command-api.md)
- [ADR-0011](../../../../adr/0011-canonical-command-api.md)
