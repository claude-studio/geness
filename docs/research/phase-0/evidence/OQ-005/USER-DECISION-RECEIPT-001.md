---
receipt_schema_version: 1
receipt_id: "USER-DECISION-OQ005-001"
question_ids:
  - "OQ-005"
authority: "user"
recorded_at: "2026-08-22T12:03:46Z"
source: "Explicit AUTOPILOT delegation in the task prompt"
---

# User decision receipt — OQ-005

## Decision

The delegated autonomous-delivery policy adopts candidate C-01, explicit project lineage
with workspace-scoped runtime identity.

- A normal clone shares `project_id` but receives a distinct `workspace_id`.
- A folder rename preserves project and workspace identity when project metadata is preserved.
- A Git worktree is a distinct workspace of the same project.
- A fork, detach or same-name repository becomes a new project only after explicit detach/rekey;
  path, display name or remote heuristics do not silently make that decision.

This receipt is a delegated decision record. It does not fabricate an interactive user message.
The adoption is permitted by the task's AUTOPILOT rule because the packet recommendation is clear,
the required fixture assertions passed deterministically twice, no contradictory identity policy
was found in the repository evidence, and the choice remains within the packet's docs/research
scope.

## Rationale and evidence

The OQ-005 fixture executed twice with exit `0`, 30/30 assertions and equality-equivalent stdout.
The local Git probe observed clone/rename/worktree history and common-dir relations; the synthetic
matrix distinguished shared project lineage from distinct workspace execution and explicit fork
detach. C-02 and C-03 remain deferred because their remote/object and path-derived policies do not
reliably preserve user intent across the observed cases.

This evidence does not select a project ID generation algorithm, fork auto-detection, workspace
registry, cross-workspace writer authority, production schema or Implementation `CLEAR`.

## Linked artifacts

- [OQ-005 packet](../../OQ-005-project-workspace-identity.md)
- [ADR-0015](../../../../adr/0015-project-workspace-identity.md)
- [RUN-OQ005-001 result](./FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ005-001/result.json)
- [RUN-OQ005-002 result](./FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ005-002/result.json)
