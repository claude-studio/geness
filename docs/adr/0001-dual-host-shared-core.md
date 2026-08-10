# ADR-0001: Dual-host adapters share one Controller

> 상태: Accepted
> 날짜: 2026-08-10

## 맥락

Geness는 Codex와 Claude Code에서 같은 인터뷰, 승인, 실행과 재개 경험을 제공해야
한다. 호스트별 Skill, hook과 plugin manifest는 서로 다르지만 상태 전이와 완료
판정까지 각각 구현하면 같은 task가 호스트에 따라 다른 결과를 갖게 된다.

## 결정

상태 머신, schema, digest, lease, checkpoint, verification verdict와 memory evaluator는
하나의 host-neutral Controller가 소유한다. Codex·Claude adapter, Skill, CLI와 MCP는
Controller 기능을 연결하는 thin interface이며 별도의 canonical state나 도메인 규칙을
갖지 않는다.

하나의 소스 저장소에서 두 host manifest를 배포하되 manifest 형식은 억지로 합치지
않는다. 두 호스트는 공통 `GENESS_HOME`과 target `.geness/`를 사용한다.

## 결과

- 호스트 간 resume와 판정 일관성을 중앙에서 검증할 수 있다.
- 호스트 API 변화는 adapter에 격리된다.
- Controller 배포와 transport 호환성 검증이 추가로 필요하다.
- hook은 편의와 관찰을 보강하지만 workflow completion의 권위자가 아니다.

## 거절한 대안

- 호스트별 완전 독립 plugin: 상태와 규칙 drift 위험 때문에 거절한다.
- 하나의 공통 manifest: Codex와 Claude의 패키징 계약이 다르므로 거절한다.
- 대화 transcript를 공통 상태로 사용: durable resume와 동시성 제어가 불가능하다.

## 검증 방법

- 동일 fixture를 Codex/Claude transport로 호출했을 때 같은 transition과 digest가 나온다.
- 한 호스트에서 중단한 run을 다른 호스트가 같은 checkpoint에서 재개한다.
- adapter source에 상태 전이와 memory threshold가 중복되지 않는지 검사한다.
