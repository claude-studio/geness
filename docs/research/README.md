# Geness Research Index

> 상태: 관찰 기록
> 규범성: 없음. 채택된 결정은 Constitution, Stage Guide 또는 Accepted ADR이 소유한다.

## 목적

이 디렉터리는 외부 프로젝트, 공식 문서와 기술 spike에서 확인한 사실을 출처와 함께
보존한다. Research는 설계 입력이지 구현 권한이 아니다. 관찰을 제품 계약으로
바꾸려면 관련 규범 문서와, 필요한 경우 ADR을 갱신해야 한다.

## 현재 문서

- [Ouroboros Reference Findings](./OUROBOROS_REFERENCE_FINDINGS.md) — 인터뷰,
  closure, 실행 계약에서 참고한 원칙과 독립 설계 경계
- [MCX Reference Findings](./MCX_REFERENCE_FINDINGS.md) — docs-first 작업 체계에서
  채택·변형한 요소
- [Open Questions](./OPEN_QUESTIONS.md) — 구현 전에 닫아야 할 미결정과 결정 권한
- [Reference and Reuse Policy](./REFERENCE_POLICY.md) — 외부 자료의 인용, 차용,
  라이선스 기록 규칙
- [Phase 0 packet and fixture convention](./phase-0/README.md) — 결정 packet의 공통
  필드와 disposable fixture 실행·보존 규칙

## 증거 수준

- `verified observation`: 고정 커밋의 원본 파일이나 공식 문서에서 직접 확인했다.
- `inference`: 여러 관찰을 종합한 해석이며 원본의 명시적 계약은 아니다.
- `proposal`: Geness에 적용할 후보이며 아직 채택되지 않았다.
- `superseded`: 더 최신 조사나 결정으로 대체됐다.

각 문서는 가능하면 저장소, 고정 commit, 파일 permalink, 조사일과 라이선스를
기록한다. 움직이는 `main` 링크만으로 설계 근거를 남기지 않는다.

## Research에서 결정으로 이동하는 절차

```text
관찰과 출처 기록
→ Geness 적용/비적용/변형 비교
→ consequential decision 여부 판단
→ ADR 제안 및 사용자 권한 확인
→ Constitution/Architecture/Stage Guide 반영
→ PLAN과 Progress 정렬
```

Research 파일을 수정해 이미 Accepted된 결정을 우회하지 않는다.
