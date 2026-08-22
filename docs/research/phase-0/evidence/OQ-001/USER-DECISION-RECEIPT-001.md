---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ001-001"
question_ids:
  - "OQ-001"
authority: "user"
recorded_at: "2026-08-22T16:05:46+09:00"
source: "Explicit user confirmation in Codex session"
---

# User decision receipt — OQ-001

## Decision

The user selected candidate A: Go with standard Go modules, CGO and an explicit
`sqlite_fts5` build contract for the v1 Controller runtime.

- The Controller v1 implementation language is Go.
- Go modules are the package and dependency management boundary.
- The SQLite path must build with CGO and the `sqlite_fts5` capability enabled.
- macOS, Linux and Windows release artifacts require separate validation; this receipt
  does not claim that the support matrix or release pipeline is already verified.

## Unresolved scope

This receipt does not select the background-daemon policy, lease heartbeat/takeover
semantics, production schema or migration tool, exact SDK/driver versions, host support
floor, release CI matrix or product scaffold. Those remain owned by the other Phase 0
questions and later implementation evidence. The selected runtime does not change the
current product-level Implementation `HOLD`.

## Linked artifacts

- [OQ-001 controller runtime packet](../../OQ-001-controller-runtime.md)
- [ADR-0010](../../../../adr/0010-controller-runtime-go.md)
