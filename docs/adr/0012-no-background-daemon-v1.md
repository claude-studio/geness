# ADR-0012: No background daemon in v1

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-003 compared a no-daemon stdio/short-lived Controller with a local background daemon and
a host-owned heartbeat sidecar. The existing host contract says to validate stdio MCP and a
short-lived CLI first, adding a daemon only when cross-session heartbeat is required and
cannot be satisfied by those surfaces.

The `FX-LEASE-LIVENESS-TAKEOVER-001` fixture supplied the missing no-daemon liveness
observation: two actual child processes exercised heartbeat extension, grace-boundary denial,
writer interruption, safe takeover and new-owner heartbeat. It passed 17/17 assertions on two
byte-identical runs. This is fixture-local logical-clock evidence, not production clock,
SQLite transaction, cross-workspace authority or installation evidence.

The user selected C-01 in the [OQ-003 decision receipt](../research/phase-0/evidence/OQ-003/USER-DECISION-RECEIPT-001.md).

## 결정

1. Geness v1 does not require, install or start a background daemon or host-owned heartbeat
   sidecar for lease liveness.
2. The default invocation model is stdio MCP or a short-lived CLI/application-service
   process. This ADR does not finalize public command names or MCP schemas.
3. Lease liveness is explicit: the active writer emits heartbeat/checkpoint updates, an
   observer remains read-only while the writer is valid, and heartbeat absence alone does not
   authorize immediate takeover. Grace, the last checkpoint and explicit lease verification
   precede safe stale-writer takeover.
4. Exact heartbeat intervals, clock source, SQLite transaction boundaries, crash-point
   recovery, cross-workspace writer authority and completion ordering remain separate
   implementation evidence or Phase 0 decisions, especially OQ-009.
5. A future requirement for persistent cross-session heartbeat must be supported by new
   evidence and a superseding ADR. A daemon or sidecar must not be introduced implicitly by
   an implementation convenience.

## 결과

- v1 has no daemon installation, supervision, update or cleanup lifecycle to define.
- Controller and host adapters retain one canonical lease/liveness policy while CLI and MCP
  remain transports around the shared application service.
- Long-running work must preserve explicit checkpoints and expose a safe resume/takeover
  path; this decision is not permission to treat a missing heartbeat as an immediate crash.
- Production multi-process lease behavior, transaction atomicity, cross-workspace arbitration
  and installed-host E2E remain verification gates. Implementation `HOLD` is unchanged.

## 거절한 대안

- **C-02 local background daemon:** not selected for v1 because it adds process ownership,
  installation, lifecycle and crash-recovery boundaries without an independent production
  observation in this packet.
- **C-03 host-owned heartbeat sidecar:** not selected for v1 because it multiplies
  host-specific lifecycle and parity behavior without independent operational evidence.
- **Implicit daemon by implementation convenience:** rejected because liveness ownership is a
  consequential runtime policy and requires a new decision if the v1 contract changes.

## 검증 방법

- Preserve the [OQ-003 packet](../research/phase-0/OQ-003-daemon-lease-liveness.md), its two
  liveness runs and redacted result/hash artifacts.
- Before implementation `CLEAR`, add production-runtime evidence for the selected Go/SQLite
  path, crash points, cross-workspace authority and installed stdio host behavior.
- Reopen this ADR with a superseding decision if a product requirement demonstrates that
  short-lived invocation cannot satisfy cross-session heartbeat.

## Decision receipt

- **Decision:** C-01 — no required background daemon or host-owned sidecar in v1; explicit
  heartbeat/checkpoint/grace/takeover protocol
- **Actor:** `user`
- **Recorded at:** `2026-08-22T18:21:07+09:00`
- **Reference:** [USER-DECISION-OQ003-001](../research/phase-0/evidence/OQ-003/USER-DECISION-RECEIPT-001.md)
