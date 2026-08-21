---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ015-001"
question_ids:
  - "OQ-015"
authority: "user"
recorded_at: "2026-08-21T07:18:40Z"
source: "Explicit user confirmation in Codex session"
---

# User decision receipt — OQ-015

## Decision

The user approved candidate C-01, the layered fail-closed Controller permission
boundary, as the v1 threat-model baseline.

- The Controller owns identity, target-root containment, revision/digest, writer
  lease, allowed/forbidden scope and completion policy.
- Read-only observation is the default. Approved local writes require the current
  contract/plan digest, active writer lease, target containment and allowed scope.
- Scope expansion, external write, destructive action, security-boundary change and
  permission escalation require an explicit user receipt bound to the current digest;
  missing or stale receipts produce `HOLD`.
- Worker, adapter and hook capabilities cannot write runtime state, bypass approval,
  promote candidate memory or self-verify completion.
- Secrets are redacted before persistence or model context. Redaction uncertainty is
  routed to `HOLD` or local-only handling.

## Unresolved scope

This receipt does not select the general `PLAN_APPROVED` actor/risk-tier policy,
receipt storage schema, exact secret detector, retention threshold, lease liveness or
production transaction design. Those remain owned by OQ-008 and the other referenced
Phase 0 questions.

## Linked artifacts

- [OQ-015 packet](../../OQ-015-threat-model-permission-policy.md)
- [ADR-0009](../../../../adr/0009-threat-model-permission-boundaries.md)
