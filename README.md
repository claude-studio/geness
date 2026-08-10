# Geness

Geness는 반복 인터뷰로 사용자의 암묵지를 결정으로 바꾸고, 승인된 문서를 실행 계약으로
고정한 뒤 Acceptance Criteria의 evidence가 모일 때까지 실행·검증·재개하는 경량
control-plane 플러그인이다. 하나의 공통 Controller와 얇은 adapter로 Codex와 Claude
Code를 함께 지원하는 것을 목표로 한다.

```text
질문으로 결정한다
→ 문서로 승인한다
→ 계획으로 제한한다
→ 실행한다
→ evidence로 검증한다
→ 필요한 교훈만 남긴다
```

## 현재 상태

문서 foundation은 완료됐고 제품 구현은 시작하지 않았다. 구현 가능 여부와 실제
HOLD/CLEAR는 [Progress](./docs/progress/README.md)에서 확인한다.

- 전체 제품·구현 계획: [docs/PLAN.md](./docs/PLAN.md)
- 문서 지도와 읽는 순서: [docs/README.md](./docs/README.md)
- 불변 원칙: [docs/00_GENESS.md](./docs/00_GENESS.md)
- 구현 전 미결정: [docs/research/OPEN_QUESTIONS.md](./docs/research/OPEN_QUESTIONS.md)
- 에이전트 작업 지침: [AGENTS.md](./AGENTS.md)

Geness가 실제 작업 대상 저장소에 만드는 portable artifact는 그 저장소의
`.geness/project.json`과 `.geness/tasks/**`에 위치한다. 실행 DB, lease, raw evidence와
검증된 memory index는 기본적으로 사용자 홈의 `~/.geness/`에 분리한다.

## 설계 영감과 출처

Geness의 interview → specification → execution 흐름은
[`Q00/ouroboros`](https://github.com/Q00/ouroboros/tree/25f958dd7938d3c383ccfd14d551467bcf6e6bd6)의
specification-first workflow와 Socratic interview 설계에서 영감을 받았다. 특히 질문
전담 역할, 답변 provenance, refine, closure/restate Gate와 승인된 실행 계약이라는
원칙을 참고했다.

Geness는 이를 target repository의 Markdown 계약, Codex·Claude 공용 Controller와
분리된 runtime/memory 구조에 맞게 독립적으로 재설계한다. 현재 Ouroboros의 source
file이나 장문의 코드·프롬프트·문서를 verbatim으로 포함하지 않지만, 출처를 밝힌 짧은
식별자와 인터뷰 구조는 design influence로 유지한다. 구체적인 영향·변형·비채택과 MIT
라이선스 경계는
[Ouroboros Reference Findings](./docs/research/OUROBOROS_REFERENCE_FINDINGS.md)에
기록한다. Geness는 Q00 또는 Ouroboros 프로젝트와 제휴하거나 보증받은 프로젝트가
아니다.

Geness 자체의 docs-first 개발 구조는
[`FRONT-JB/mcx`](https://github.com/FRONT-JB/mcx/tree/c49d2493f94fba6928ed20a46c9db8aecdcd3087/docs)를
참고했으며, 적용 차이는 [MCX Reference Findings](./docs/research/MCX_REFERENCE_FINDINGS.md)에
기록한다.
