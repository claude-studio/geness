# ADR-0003: A failure candidate is not durable memory

> 상태: Accepted
> 날짜: 2026-08-10

## 맥락

실행 중 잘못된 가정이나 오류를 모두 장기 기억으로 주입하면 일회성 문제까지 이후
작업을 오염시키고 context 비용을 늘린다. 반대로 아무것도 남기지 않으면 동일한
검증 가능한 실수를 반복한다. 이 판단을 매번 LLM의 자유 재량에 맡기면 일관되게
재현할 수도 없다.

## 결정

실패는 우선 runtime event와 `candidate`로만 저장한다. 장기 memory 노출은 versioned
deterministic evaluator가 재발, 독립 evidence, 재현 가능한 root cause와 guard 효과를
검사해 승격한 lesson에만 허용한다.

후보는 eligible exposure와 unassisted success, TTL과 invalidation event로 감쇠·만료할
수 있다. 조회는 exact fingerprint → structured filter → FTS rank → 작은 top-K summary
순이며 evidence는 선택 후 지연 로딩한다. LLM은 후보 요약과 evidence를 제안할 수
있지만 상태 전이를 판정하지 않는다.

## 결과

- 일회성 실수가 영구 prompt 편향으로 남지 않는다.
- 승격·만료 결과를 event replay와 fixture로 설명할 수 있다.
- 좋은 fingerprint와 eligible exposure 정의가 중요해진다.
- evaluator version과 rule change migration을 보존해야 한다.

## 거절한 대안

- 모든 실패를 즉시 memory에 저장: false positive와 context pollution 때문에 거절한다.
- LLM이 매번 기억 필요성을 판단: 비결정적이고 감사할 수 없다.
- 아무 실패도 보존하지 않음: 재발 방지와 root cause 추적이 불가능하다.
- vector DB 우선: v1의 데이터량과 exact/filter 검색 요구에 과도하다.

## 검증 방법

- event 순서를 replay했을 때 evaluator가 같은 transition을 산출한다.
- 단일 실패 뒤 일반 memory query에 나타나지 않는지 확인한다.
- 독립 재발/guard evidence fixture만 verified로 승격되는지 확인한다.
- eligible하지 않은 success가 lesson을 만료시키지 않는지 검사한다.
