# ADR-0016: Schema lineage and projection ownership

> 상태: Accepted
> 날짜: 2026-08-22
> Supersedes: none

## 맥락

OQ-006은 task Markdown frontmatter와 runtime SQLite 사이에서 portable contract,
mutable state, revision lineage, stale write와 projection reconciliation의 권위를
구분해야 하는 질문이다. Accepted [ADR-0002](./0002-project-and-local-state-boundary.md)와
[ADR-0007](./0007-v1-contract-and-verification-artifacts.md)는 각각 저장 경계와
contract/projection 방향을 제시하지만, concern-level owner와 stale-write 경계를
별도 결정으로 남겨 두었다.

Phase 0 fixture는 frontmatter와 fixture-local SQLite row를 거친 semantic/body round-trip,
현재 revision write와 stale revision 거부를 두 번 결정론적으로 통과했다. 이 결과는
production table이나 migration을 정하지 않으며, historical evidence envelope drift는
별도 제한사항으로 남아 있다.

## 결정

1. Task Markdown frontmatter와 사람이 읽는 body는 Git으로 공유하는 portable
   contract/projection을 소유한다. raw runtime log, lease, secret와 대용량 evidence는
   이 문서에 저장하지 않는다.
2. Runtime SQLite는 mutable task state, revision guard, attempt, lease, verifier verdict와
   evidence freshness의 canonical owner다. `run.md`와 `verification.md` 같은 문서는
   runtime 결과를 사람이 읽도록 투영한다.
3. 문서와 runtime write는 current revision/digest precondition을 사용한다. stale write는
   거부하고 current state를 변경하지 않는다.
4. DB와 document projection 사이의 비원자 경계는 operation ID와 idempotent
   projection/reconciliation으로 복구한다. Document projection은 `COMPLETED` 또는
   다른 lifecycle Gate의 권위자가 아니다.
5. 이 ADR은 exact frontmatter grammar, production SQLite table/column/index/migration,
   cross-runtime digest serializer, project ID algorithm, workspace registry와 crash-point
   recovery를 확정하지 않는다. 이 항목들은 해당 OQ와 후속 implementation evidence에
   남긴다.

## 결과

- 사람이 검토하고 Git으로 공유하는 계약과 private/mutable runtime state의 경계가
  명확해진다.
- stale editor 또는 stale projection이 current runtime verdict를 조용히 덮어쓸 수 없다.
- projection failure는 runtime completion authority를 바꾸지 않고 operation ID로 재시도·복구할
  수 있다.
- exact schema, migration, serializer, cross-workspace arbitration과 crash recovery는
  여전히 Phase 0/후속 Gate의 blocker다. Implementation `HOLD`는 유지한다.

## 거절한 대안

- **C-02 SQLite canonical, Markdown derived:** Git에서 직접 검토하는 portable contract의
  provenance와 projection drift 처리 비용이 커지므로 기본 owner로 채택하지 않았다.
- **C-03 Markdown canonical with sidecar machine JSON:** mutable lease·attempt·verdict와
  document merge를 하나의 권위로 안전하게 표현하기 어렵고 sidecar drift가 늘어나므로
  채택하지 않았다.

## 검증 방법

- [OQ-006 packet](../research/phase-0/OQ-006-schema-lineage.md)의 candidate/trade-off와
  limitation을 확인한다.
- [FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001](../research/phase-0/fixtures/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/README.md)을
  `PYTHONDONTWRITEBYTECODE=1 python3 runner.py`로 두 번 실행한다.
- 두 실행이 exit `0`, 30/30 assertions, `all_assertions_pass=true`이고 paired stdout이
  byte-identical인지 확인한다.
- [decision receipt](../research/phase-0/evidence/OQ-006/USER-DECISION-RECEIPT-001.md)와
  current [RUN-OQ006-003](../research/phase-0/evidence/OQ-006/FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001/RUN-OQ006-003/RUN.md)을
  함께 확인한다.
