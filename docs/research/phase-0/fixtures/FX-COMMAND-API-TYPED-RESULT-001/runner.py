#!/usr/bin/env python3
"""Run the OQ-002 transport comparison with only Python's standard library."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from common_service import ApplicationService


FIXTURE_ID = "FX-COMMAND-API-TYPED-RESULT-001"
PACKET_ID = "OQ-002"
ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "fixture.json"


def stable_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def invoke(script: str, state_path: Path, wire: str) -> tuple[int, str, str, str]:
    command = [sys.executable, script, "--state", str(state_path)]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        input=wire,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
    )
    display = f"python3 {script} --state <run-temp>/{state_path.name}"
    return completed.returncode, completed.stdout, completed.stderr, display


def cli_call(request: dict[str, Any], state_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    exit_status, stdout, stderr, display = invoke("cli_transport.py", state_path, json.dumps(request))
    return read_result(stdout), {
        "command": display,
        "exit_status": exit_status,
        "stderr_empty": stderr == "",
    }


def read_result(stdout: str) -> dict[str, Any]:
    lines = [line for line in stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f"expected one JSON result line, got {len(lines)}")
    return json.loads(lines[0])


def cli_invalid_wire(wire: str, state_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    exit_status, stdout, stderr, display = invoke("cli_transport.py", state_path, wire)
    return read_result(stdout), {
        "command": display + " <invalid-json-wire>",
        "exit_status": exit_status,
        "stderr_empty": stderr == "",
        "state_created": state_path.exists(),
    }


def mcp_sequence(
    hold_request: dict[str, Any], replay_request: dict[str, Any], invalid_message: dict[str, Any], state_path: Path
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    command = [sys.executable, "mcp_transport.py", "--state", str(state_path)]
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "command", "arguments": hold_request}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "command", "arguments": replay_request}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "command", "arguments": replay_request}},
        invalid_message,
    ]
    wire = "".join(json.dumps(message, sort_keys=True) + "\n" for message in messages)
    completed = subprocess.run(
        command,
        cwd=ROOT,
        input=wire,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
    )
    responses = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    by_id = {response.get("id"): response for response in responses}
    hold = by_id[2]["result"]["structuredContent"]
    first = by_id[3]["result"]["structuredContent"]
    replay = by_id[4]["result"]["structuredContent"]
    error = by_id[99]
    commands = {
        "command": "python3 mcp_transport.py --state <run-temp>/mcp-state.json",
        "exit_status": completed.returncode,
        "stderr_empty": completed.stderr == "",
        "response_count": len(responses),
    }
    return hold, first, replay, {"response": error, "commands": commands}


def hold_projection(result: dict[str, Any]) -> dict[str, Any]:
    keys = ["kind", "schema", "status", "code", "operation_id", "effect_id", "decision", "side_effect_count"]
    return {key: result.get(key) for key in keys}


def replay_projection(result: dict[str, Any]) -> dict[str, Any]:
    keys = ["kind", "schema", "status", "code", "operation_id", "effect_id", "decision", "side_effect_count"]
    return {key: result.get(key) for key in keys}


def main() -> int:
    fixture_input = read_json(INPUT_PATH)
    input_sha256 = hashlib.sha256(INPUT_PATH.read_bytes()).hexdigest()

    with tempfile.TemporaryDirectory(prefix="geness-oq002-") as temp_dir:
        temp = Path(temp_dir)
        library_service = ApplicationService(temp / "library-state.json")
        library_hold = library_service.handle(fixture_input["hold_request"])
        library_first = library_service.handle(fixture_input["replay_request"])
        library_replay = library_service.handle(fixture_input["replay_request"])

        cli_state = temp / "cli-state.json"
        cli_hold, cli_hold_command = cli_call(fixture_input["hold_request"], cli_state)
        cli_first, cli_first_command = cli_call(fixture_input["replay_request"], cli_state)
        cli_replay, cli_replay_command = cli_call(fixture_input["replay_request"], cli_state)
        cli_error, cli_error_command = cli_invalid_wire(fixture_input["invalid_cli_wire"], temp / "cli-error-state.json")

        mcp_hold, mcp_first, mcp_replay, mcp_error = mcp_sequence(
            fixture_input["hold_request"],
            fixture_input["replay_request"],
            fixture_input["invalid_mcp_message"],
            temp / "mcp-state.json",
        )

        domains = {
            "library": {"hold": library_hold, "first": library_first, "replay": library_replay},
            "cli": {"hold": cli_hold, "first": cli_first, "replay": cli_replay},
            "mcp": {"hold": mcp_hold, "first": mcp_first, "replay": mcp_replay},
        }
        assertions: list[dict[str, Any]] = []

        def check(name: str, passed: bool, detail: str) -> None:
            assertions.append({"name": name, "passed": passed, "detail": detail})
            if not passed:
                raise RuntimeError(f"assertion failed: {name}: {detail}")

        hold_values = [hold_projection(item["hold"]) for item in domains.values()]
        check("same-domain-HOLD", len({json.dumps(value, sort_keys=True) for value in hold_values}) == 1, "library/CLI/MCP HOLD projections match")
        check("HOLD-is-domain-result", library_hold["kind"] == "domain_result" and library_hold["status"] == "HOLD", "unapproved gate is typed domain HOLD")
        check("HOLD-does-not-fail-transport", cli_hold["status"] == "HOLD" and cli_hold_command["exit_status"] == 0, "CLI carries HOLD with exit 0")

        first_values = [replay_projection(item["first"]) for item in domains.values()]
        replay_values = [replay_projection(item["replay"]) for item in domains.values()]
        check("same-domain-APPLIED", len({json.dumps(value, sort_keys=True) for value in first_values}) == 1, "first decision projections match")
        check("same-domain-REPLAYED", len({json.dumps(value, sort_keys=True) for value in replay_values}) == 1, "replay projections match")
        check("replay-status", all(item["replay"]["status"] == "REPLAYED" for item in domains.values()), "replay is explicitly typed")
        check("replay-effect-stable", all(item["first"]["effect_id"] == item["replay"]["effect_id"] for item in domains.values()), "replay preserves effect ID")
        check("replay-side-effect-once", all(item["replay"]["side_effect_count"] == 1 for item in domains.values()), "replay does not apply a second side effect")

        check("CLI-transport-error", cli_error["kind"] == "transport_error" and cli_error["code"] == "INVALID_JSON", "malformed CLI wire is transport_error")
        check("CLI-transport-exit", cli_error_command["exit_status"] == 2 and not cli_error_command["state_created"], "CLI parse error exits 2 without service state")
        check("MCP-transport-error", mcp_error["response"]["error"]["data"]["kind"] == "transport_error" and mcp_error["response"]["error"]["code"] == -32601, "unknown MCP method is JSON-RPC transport error")
        check("MCP-transport-exit", mcp_error["commands"]["exit_status"] == 0, "MCP reports protocol error in-band and exits 0")

        cli_source = (ROOT / "cli_transport.py").read_text(encoding="utf-8")
        mcp_source = (ROOT / "mcp_transport.py").read_text(encoding="utf-8")
        check("thin-adapter-import", "from common_service import ApplicationService" in cli_source and "from common_service import ApplicationService" in mcp_source, "both transports call shared service")
        check("no-domain-duplication", all(code not in cli_source + mcp_source for code in ["APPROVAL_REQUIRED", "DECISION_RECORDED", "IDEMPOTENCY_KEY_CONFLICT"]), "domain codes are absent from transport adapters")

        manifest = {
            "manifest_schema": "fixture.oq002.result.v1",
            "fixture_id": FIXTURE_ID,
            "packet_id": PACKET_ID,
            "input_sha256": input_sha256,
            "runner_python": platform.python_version(),
            "network": "disabled",
            "external_writes": False,
            "domain_results": domains,
            "transport_errors": {
                "library": {"status": "not_applicable", "reason": "direct library call has no wire transport"},
                "cli": {"result": cli_error, "command": cli_error_command},
                "mcp": mcp_error,
            },
            "commands": {
                "cli_hold": cli_hold_command,
                "cli_first": cli_first_command,
                "cli_replay": cli_replay_command,
                "mcp_sequence": mcp_error["commands"],
            },
            "assertions": assertions,
            "all_assertions_pass": True,
        }
        print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:  # pragma: no cover - failure path is intentionally visible to the runner
        print(json.dumps({"manifest_schema": "fixture.oq002.runner-error.v1", "error": str(error)}, sort_keys=True))
        raise
