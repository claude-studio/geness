# ADR-0009: Threat model and permission boundaries

> 상태: Proposed
> 날짜: 2026-08-21
> Supersedes: none

## 맥락

Phase 0의 lifecycle, identity/schema/digest, host/command, memory/retention packet은 각각
lease·approval·scope·external write·secret·evidence 문제를 관찰했지만, cross-concern의
권위와 fail behavior가 하나의 문서에 모여 있지 않았다. 이 상태에서는 host adapter나 worker가
서로 다른 approval 의미를 만들거나, stale digest·untrusted project content·secret output을
정상 결과로 처리할 위험이 있다.

위협 모델과 decision-ready evidence는
[`OQ-015`](../research/phase-0/OQ-015-threat-model-permission-policy.md)에 보존한다.
이 ADR은 그 packet의 권고를 기록하지만 user decision receipt 전에는 제품 권한이나
Implementation `CLEAR`가 아니다.

## 제안 결정

사용자 승인 전의 v1 보안 baseline으로 다음 layered fail-closed 경계를 채택 검토한다.

1. Controller가 project/task identity, target-root containment, revision/digest, writer
   lease, allowed/forbidden scope와 completion Gate의 공통 권위자가 된다. host adapter,
   CLI/MCP, Skill, hook과 worker는 별도 상태·approval·completion 권위자가 아니다.
2. `observe`와 approved in-scope local write를 기본 capability로 구분한다. setup/preflight는
   read-only를 사용하고, implementation write는 current approved contract/plan digest,
   active writer lease, resolved target containment와 allowed scope를 모두 만족해야 한다.
3. scope 확대, external write, destructive action, security boundary 변경과 permission
   escalation은 current digest에 묶인 explicit user receipt 없이는 실행하지 않고 `HOLD`한다.
   host approval은 추가 guard이지 Controller의 user authority를 대체하지 않는다.
4. runtime DB 직접 쓰기, approval bypass, 기본 `danger-full-access`, candidate lesson
   promotion과 worker self-verification은 v1 worker/adapter capability에서 금지한다.
5. command output·environment·evidence·memory projection은 persistence 또는 model context
   경계 전에 redaction/minimization을 거친다. 원문이 redacted됐음을 보장할 수 없으면
   project document/memory에 저장하지 않고 `HOLD` 또는 local-only로 라우팅한다.
6. behavior-bearing completion은 current digest에 연결된 mechanical evidence와 acting
   evidence, 독립 verifier를 요구한다. candidate memory는 일반 query에 노출하지 않으며,
   corrupt/unavailable memory는 empty로 축약하지 않고 typed `HOLD`로 반환한다.

이 제안은 exact risk tier, secret detector pattern/version, approval receipt schema, retention
threshold, lease heartbeat/takeover와 production transaction을 확정하지 않는다. 해당 결정은
OQ-003/OQ-004/OQ-008/OQ-009/OQ-010/OQ-011 및 관련 ADR/fixture의 user receipt가 소유한다.

## 대안 검토

### Host-trust delegation

host sandbox와 approval 시스템에 권한을 위임하는 방식이다. 초기 Controller가 단순해질 수
있지만 Codex와 Claude의 manifest·hook·MCP·trust semantics 차이가 동일 task의 권한 결과를
바꿀 수 있어 거절하고 후속 capability adapter 후보로 둔다.

### Policy auto-approval

low-risk 작업은 risk classifier가 자동 승인하고 고위험 작업만 사용자에게 묻는 방식이다.
routine workflow는 빨라질 수 있지만 classifier false negative가 user approval을 대체하며,
현재 risk calibration과 side-effect 분류 evidence가 없으므로 채택하지 않는다.

## 결과

### 긍정적 결과

- authority, scope, side effect와 evidence의 단일 fail-closed 경계가 생긴다.
- host/worker가 transport 또는 untrusted project content를 통해 승인을 사칭하기 어렵다.
- stale/replay, two-writer, secret leakage와 false completion을 typed `HOLD`로 관찰할 수 있다.
- portable project 문서와 private runtime/evidence의 기존 storage boundary를 유지한다.

### 비용과 잔여 위험

- Controller envelope, receipt validation, path canonicalization, redaction과 capability test가
  필요해 구현·운영 비용이 늘어난다.
- 보수적인 `HOLD`가 routine automation을 중단할 수 있고, 사용자의 attention 비용이 생긴다.
- redaction detector 완전성, host sandbox 실제 enforcement, multi-process lease/crash recovery,
  remote/cloud threat와 조직 IAM은 이 ADR로 해결되지 않는다.
- user receipt 전에는 이 문서를 Accepted로 올리거나 보안 baseline을 구현할 수 없다.

## 검증 방법

- [`FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001`](../research/phase-0/fixtures/FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001/README.md)
  를 두 번 실행해 17/17 assertion과 byte-identical projection을 확인한다.
- path traversal/symlink escape, untrusted authority, stale digest/approval, two-writer,
  forbidden capability, redaction, self-verification, acting evidence와 memory poisoning
  control이 각각 OQ-015 matrix와 result manifest에 연결되는지 확인한다.
- user receipt 후 selected runtime의 multi-process lease/crash, schema/digest migration,
  installed-host sandbox/MCP, secret corpus와 dual-host E2E를 실행한다.
- Accepted 승격 전 `OPEN_QUESTIONS.md`, Architecture/Lifecycle/Storage/Host Integration,
  PLAN과 Progress의 상태·링크가 동일 결론을 가리키는지 read-only drift 검사를 수행한다.

## Decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
