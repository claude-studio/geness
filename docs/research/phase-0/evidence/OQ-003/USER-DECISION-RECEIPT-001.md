---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ003-001"
question_ids:
  - "OQ-003"
authority: "user"
recorded_at: "2026-08-22T18:21:07+09:00"
source: "Explicit user confirmation in Codex session"
---

# User decision receipt — OQ-003

## Decision

The user confirmed candidate C-01: Geness v1 does not require a background daemon or a
host-owned heartbeat sidecar. The Controller is invoked through stdio MCP or a short-lived
CLI/application-service process and uses an explicit lease heartbeat, checkpoint and safe
takeover protocol.

- v1 does not install, start or require a background daemon or sidecar for lease liveness.
- An active writer sends explicit heartbeat/checkpoint updates. Heartbeat absence alone does
  not immediately authorize takeover; grace, the last checkpoint and explicit lease
  verification are required first.
- Exact heartbeat interval, clock source, SQLite transaction boundary, crash-point behavior
  and cross-workspace writer authority remain implementation evidence or separate Phase 0
  decisions.

## Rationale and evidence

The decision follows the existing host integration direction to validate stdio MCP and a
short-lived CLI first, adding a daemon only if cross-session heartbeat cannot be satisfied by
that model. `FX-LEASE-LIVENESS-TAKEOVER-001` observed two actual child processes, heartbeat
extension, grace-boundary denial, writer interruption, safe takeover and new-owner heartbeat
with 17/17 assertions on two byte-identical runs. The fixture is logical-clock and
fixture-local evidence, not production daemon, clock or SQLite evidence.

The local background daemon (C-02) and host-owned sidecar (C-03) were not selected. Their
installation, lifecycle, ownership and recovery costs were not independently benchmarked;
the decision is a v1 policy choice grounded in the existing stdio-first contract and the
available no-daemon liveness observation.

## Unresolved scope

This receipt does not create daemon code or a product scaffold. It does not select exact
lease thresholds, production clock/SQLite behavior, cross-workspace arbitration,
completion/lease transaction ordering, public command names or host support guarantees. The
decision does not change the product-level Implementation `HOLD` or Phase 0 `HOLD`.

## Linked artifacts

- [OQ-003 daemon and lease liveness packet](../../OQ-003-daemon-lease-liveness.md)
- [ADR-0012](../../../../adr/0012-no-background-daemon-v1.md)
