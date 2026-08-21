# ADR-0008: Host compatibility and canonical `gee` command surface

> 상태: Proposed
> 날짜: 2026-08-21

## 맥락

Codex와 Claude Code는 모두 Skill, plugin, hook과 MCP 확장 지점을 제공하지만 manifest
위치, plugin 설치/검증 명령, hook trust/event, MCP 설정과 non-interactive bridge가
서로 다르다. 따라서 host별 기능을 공통 제품 API로 직접 노출하면 같은 task가 host에
따라 다른 상태·승인·resume 결과를 낼 위험이 있다.

Phase 0 조사에서 현재 machine의 `codex-cli 0.149.0`과 `Claude Code 2.1.238`의
read-only capability probe를 실행했고, fixture-local library/CLI/MCP transport가
setup/status/resume/description routing의 같은 projection을 반환하는지 비교했다.
이 문서는 그 조사 결과를 반영한 ADR 후보이며, 사용자 decision receipt 전에는 규범이
아니다.

## 제안 결정

다음 정책을 Host/CLI ADR 후보로 채택 검토한다.

1. 공통 user-facing surface는 `gee` 하나로 둔다.

   - `gee setup`: task 이전 project/workspace readiness bootstrap
   - `gee status`: read-only compact state/next-action projection
   - `gee resume <task>`: checkpoint/blocker에서 Controller가 검증 후 재개하는 action
   - `gee brief`, `gee contract`, `gee plan`, `gee impl`, `gee verify`, `gee done`:
     public stage alias

2. description router와 command registry는 host-neutral application boundary에 둔다.
   Codex `$`/TUI invocation, Claude slash/Skill invocation과 MCP tool은 alias/transport일
   뿐이며 domain state, Gate, digest, lease, completion을 소유하지 않는다. ambiguous
   description은 사용자 선택이 필요한 typed `HOLD`로 남긴다.

3. profile 정책은 ADR-0006과 동일하게 유지한다.

   - `auto`: Codex capability가 준비되면 `cross-model`, 없으면 새 task에 한해 `claude-only`
   - `cross-model`: Codex가 준비되지 않으면 setup attention
   - `claude-only`: Claude capability만 필수
   - active task profile은 silent switch하지 않고 reopen/reapproval을 요구

4. host package는 두 manifest를 제공한다. Codex는 `.codex-plugin/plugin.json`, Claude는
   `.claude-plugin/plugin.json`을 사용한다. 공통 Skill은 Agent Skills의 `SKILL.md`
   `name`/`description` subset과 host-neutral instructions를 공유하고, host-specific
   metadata·paths·hooks는 adapter에 둔다.

5. 두 host의 MCP capability 중 v1 공통 transport는 local stdio를 우선한다. Codex의
   Streamable HTTP, Claude의 HTTP/SSE/OAuth와 host-specific MCP approval은 optional
   adapter capability로 기록하되 canonical task state transport로 사용하지 않는다.

6. hooks는 status 안내, failure observation과 guardrail만 보강한다. hook은 task state,
   completion 또는 lesson promotion의 권위자가 아니며, host별 trust/event/output
   차이를 흡수한다.

7. 지원 범위는 capability gate와 보수적 OS 교집합을 함께 사용한다.

   - cross-model 제안 범위: macOS 13+, Ubuntu 20.04+/Debian 10+, Windows 11 via WSL2
   - claude-only 제안 범위: Claude 공식 문서의 macOS, native Windows/WSL, Ubuntu/Debian,
     지원 Alpine 범위; setup capability probe와 host-specific dependency가 통과해야 함
   - 초기 검증 floor: Codex `0.149.0`, Claude Code `2.1.238` — vendor minimum이 아닌
     조사 machine의 tested floor
   - Codex native Windows cross-model과 tested floor 미만 version은 installed-host
     E2E와 version matrix가 생길 때까지 지원 선언에서 제외

## 결과

- 사용자 명령과 durable task state의 권위가 host session/namespace에서 분리된다.
- CLI와 MCP parity는 동일 application result의 검증 속성이 되고, transport error와
  domain `HOLD`를 구분할 수 있다.
- host plugin manifest와 adapter가 추가되지만, 공통 Skill·Controller contract의 drift
  위험이 줄어든다.
- `gee` grammar, output envelope, ambiguity policy, version N-1 policy와 installed-host
  E2E는 별도 implementation/Phase 0 decision evidence가 필요하다.
- 현재 제안은 제품 scaffold를 승인하지 않으며, Implementation `HOLD`와 OQ-012/OQ-014
  user decision pending 상태를 유지한다.

## 거절한 대안

- host-native slash/mention command를 제품 API로 사용: Codex와 Claude의 namespace,
  discovery/reload와 resume semantics가 달라 portable contract가 깨지므로 deferred.
- CLI를 canonical state surface로 사용: MCP/Skill/host adapter가 CLI process와 exit
  semantics에 결합되어 domain rule 중복이 생기므로 deferred.
- MCP tool schema를 canonical surface로 사용: CLI와 Skill이 MCP protocol/session/error
  semantics에 결합되므로 deferred.
- Codex native Windows를 즉시 cross-model 지원: 현재 공식 install 문서의 WSL2 기준,
  source/package target과 installed-host behavior 사이 evidence gap을 해소하지 못했으므로
  deferred.
- hook을 completion/status authority로 사용: hook은 host lifecycle과 trust에 종속되고
  side effect 이후 관찰만 가능한 event가 있어 거절.

## 검증 방법

- [OQ-012 host compatibility packet](../research/phase-0/OQ-012-host-os-compatibility.md)
  의 official source matrix와 read-only probe를 재실행한다.
- [OQ-014 command surface packet](../research/phase-0/OQ-014-command-surface.md)의
  `FX-HOST-CAPABILITY-COMMAND-SURFACE-001`을 실행해 26 synthetic cases와
  library/CLI/MCP parity를 확인한다.
- 선택된 version floor의 N-1/probe matrix, local plugin load, stdio MCP handshake와
  양방향 same-machine host handoff를 후속 release gate로 실행한다.
- 사용자의 decision receipt를 받은 뒤에만 이 ADR을 `Accepted`로 변경하고,
  `OPEN_QUESTIONS.md`, Host Integration, PLAN과 Progress를 근거 링크로 동기화한다.

## Decision receipt

- **Decision:** `pending`
- **Actor:** `pending`
- **Recorded at:** `pending`
- **Reference:** `pending`
