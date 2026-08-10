# ADR-0004: Reframe observed Ouroboros interview principles as Geness contracts

> 상태: Accepted
> 날짜: 2026-08-10

## 맥락

사용자가 가치 있게 본 경험은 질문이 계속 암묵지를 드러내고, 충분하지 않은 계획을
쉽게 완료 처리하지 않는 Ouroboros의 specification-first 흐름이다. Geness는 이
경험을 유지하되 Ouroboros 전체 OS나 호환 구현을 만들지 않는다.

조사 근거와 정확한 범위는
[Ouroboros Reference Findings](../research/OUROBOROS_REFERENCE_FINDINGS.md)가 소유한다.

## 결정

Ouroboros에서 관찰한 다음 원칙을 Geness 인터뷰 계약의 설계 입력으로 사용한다.

- 질문과 구현 역할 분리
- 한 번에 가장 영향이 큰 미결정 하나를 묻는 Socratic loop
- 코드·조사 사실과 사용자 결정의 provenance/authority 분리
- 답변 refine와 사용자 확인
- 독립 ambiguity track을 보존하는 visible ledger
- closer/contrarian/gap-hunter 관점의 closure audit
- one-sentence restatement와 명시적 사용자 승인
- 승인된 결과를 검증 가능한 실행 계약으로 고정
- 너무 이른 종료와 불필요한 과잉 인터뷰를 모두 막는 bounded convergence

이는 아이디어와 동작 원칙 수준의 참고다. Geness 사양과 구현은 독립 작성하며,
Ouroboros의 prompt 문구, 식별자, 데이터 모델, 파일 형식과 수치 threshold를 호환성
계약으로 취급하지 않는다.

## 결과

- 사용자가 기대하는 반복 질문과 타이트한 종료 기준을 구체 계약으로 보존한다.
- 채택·변형·비채택 범위를 고정 원본과 비교할 수 있다.
- Ouroboros 변경과 독립적으로 Geness 계약을 발전시킬 수 있다.
- 실제 코드·문서·프롬프트 차용이 시작되면 별도의 MIT 고지 검사가 필요하다.

## 거절한 대안

- Ouroboros 전체 fork/호환 구현: Geness의 경량 범위를 벗어난다.
- 출처를 남기지 않고 유사 UX만 구현: 설계 계보와 차용 경계를 감사할 수 없다.
- ambiguity 수치 하나로 자동 종료: 사용자 authority와 closure evidence를 대체할 수 없다.

## 검증 방법

- Interview contract test가 highest-impact one-question loop, provenance와 rhythm guard를
  검증한다.
- closure fixture가 세 관점 audit, restatement 수정 시 reopen과 explicit approval을
  검증한다.
- 외부 표현물 재사용 변경이 Reference Policy의 license Gate를 통과하는지 검사한다.
