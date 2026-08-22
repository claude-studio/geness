# ADR-0011: Shared application service is the canonical command API

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-002 compared a shared application service, a CLI-canonical boundary and an
MCP-canonical boundary with the same disposable fixture. The fixture passed 14 assertions:
the three paths produced the same domain projections, a valid `HOLD` remained a successful
transport exchange, malformed CLI input and an unknown MCP method remained typed transport
errors, and idempotent replay kept one side effect. This is fixture evidence, not an
installed-host end-to-end or production API guarantee. The user selected C-01 through the
OQ-002 decision receipt.

## 결정

1. The shared application service is the canonical command API boundary.
2. The application service owns domain policy, typed domain results and idempotency.
3. CLI and MCP are thin wire transports that call the same application service, preserve its
   domain result envelope and add only transport-specific errors.
4. A valid domain `HOLD` is not a transport failure. Malformed CLI input and unknown MCP
   methods are separate typed transport errors.
5. CLI, MCP, Skill and host adapters do not duplicate domain state, Gate, digest, lease,
   completion or memory policy.
6. Final command names, MCP tool schemas/protocol versions, daemon/lease policy, production
   schema/digest formats, installed-host compatibility and product scaffold remain separate
   decisions or implementation evidence.

## 결과

- Domain behavior can be tested without importing a host or transport.
- CLI/MCP parity means reuse of one application service, not duplicated state machines.
- Transport adapters can evolve their wire-specific input/output and error mapping without
  becoming owners of domain policy.
- Official SDK behavior, schema/versioning, installed-host compatibility and cross-host E2E
  still require later evidence.

## 거절한 대안

- **C-02 CLI canonical:** deferred because MCP would depend on CLI process/shape and its
  lifecycle, error and installation semantics.
- **C-03 MCP canonical:** deferred because CLI and other hosts would depend on JSON-RPC/MCP
  lifecycle and error semantics.

These alternatives were not independently implemented production candidates; the deferral is
limited to the boundary decision and does not claim comparative operational measurements.

## 검증 방법

- Preserve the OQ-002 fixture, its 14 assertions and redacted evidence/hash.
- Rerun the fixture after any shared command/result contract change.
- Add official SDK, schema/versioning, installed-host and cross-host parity evidence before
  treating those concerns as resolved.

## Decision receipt

- **Decision:** C-01 — shared application service with thin CLI/MCP transports
- **Actor:** user
- **Recorded at:** 2026-08-22T16:44:59+09:00
- **Reference:** `docs/research/phase-0/evidence/OQ-002/USER-DECISION-RECEIPT-001.md`
