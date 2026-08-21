#!/usr/bin/env python3
"""Run the OQ-012/OQ-014 host and command-surface comparison."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from surface_service import dispatch


FIXTURE_ID = "FX-HOST-CAPABILITY-COMMAND-SURFACE-001"
PACKETS = ["OQ-012", "OQ-014"]
ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "fixture.json"


def stable_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_host_probe(host: str, specs: list[dict[str, Any]], temp_root: Path) -> dict[str, Any]:
    binary = shutil.which(host)
    if binary is None:
        return {
            "host": host,
            "available": False,
            "executable": "not-found",
            "commands": [
                {"id": spec["id"], "command": " ".join([host, *spec["args"]]), "status": "not_found"}
                for spec in specs
            ],
            "all_pass": False,
        }

    codex_home = temp_root / "codex-home"
    codex_home.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "NO_COLOR": "1", "CODEX_HOME": str(codex_home)}
    if host == "claude":
        env["CLAUDE_CODE_SIMPLE"] = "1"
    commands: list[dict[str, Any]] = []
    for spec in specs:
        display_command = " ".join([host, *spec["args"]])
        try:
            completed = subprocess.run(
                [binary, *spec["args"]],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            combined = f"{completed.stdout}\n{completed.stderr}"
            lowered = combined.lower()
            token_checks = {token: token.lower() in lowered for token in spec["tokens"]}
            version = completed.stdout.strip().splitlines()[0] if spec["id"] == "version" and completed.stdout.strip() else None
            commands.append(
                {
                    "id": spec["id"],
                    "command": display_command,
                    "exit_status": completed.returncode,
                    "status": "pass" if completed.returncode == 0 and all(token_checks.values()) else "fail",
                    "token_checks": token_checks,
                    "stdout_stderr_sha256": hashlib.sha256(combined.encode("utf-8")).hexdigest(),
                    "observed_version": version,
                }
            )
        except subprocess.TimeoutExpired:
            commands.append({"id": spec["id"], "command": display_command, "status": "timeout"})
    return {
        "host": host,
        "available": True,
        "executable": "resolved-on-PATH",
        "commands": commands,
        "all_pass": all(command.get("status") == "pass" for command in commands),
    }


def invoke_cli(request: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    completed = subprocess.run(
        [sys.executable, "cli_transport.py"],
        cwd=ROOT,
        input=json.dumps(request),
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f"CLI returned {len(lines)} JSON lines")
    return completed.returncode, json.loads(lines[0])


def invoke_mcp(request: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "gee", "arguments": request}},
    ]
    completed = subprocess.run(
        [sys.executable, "mcp_transport.py"],
        cwd=ROOT,
        input="".join(json.dumps(message, sort_keys=True) + "\n" for message in messages),
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
    )
    responses = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    result = next(response["result"]["structuredContent"] for response in responses if response.get("id") == 2)
    return completed.returncode, result


def projection(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != "request_digest"}


def main() -> int:
    fixture_input = read_json(INPUT_PATH)
    input_sha256 = hashlib.sha256(INPUT_PATH.read_bytes()).hexdigest()
    assertions: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        assertions.append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            raise RuntimeError(f"assertion failed: {name}: {detail}")

    with tempfile.TemporaryDirectory(prefix="geness-oq012-oq014-") as temp_dir:
        temp_root = Path(temp_dir)
        host_probe = {
            host: run_host_probe(host, specs, temp_root)
            for host, specs in fixture_input["host_probes"].items()
        }
        check("codex-read-only-probe", host_probe["codex"]["all_pass"], "Codex version/help/plugin/MCP/feature probes passed")
        check("claude-read-only-probe", host_probe["claude"]["all_pass"], "Claude version/help/plugin/MCP probes passed")

        surface_cases: list[dict[str, Any]] = []
        all_cases = [
            *fixture_input["route_cases"],
            *fixture_input["setup_cases"],
            *fixture_input["status_cases"],
            *fixture_input["resume_cases"],
        ]
        for case in all_cases:
            request = case["request"]
            library_result = dispatch(request)
            cli_exit, cli_result = invoke_cli(request)
            mcp_exit, mcp_result = invoke_mcp(request)
            expected = case["expected"]
            expected_match = all(library_result.get(key) == value for key, value in expected.items())
            parity = projection(library_result) == projection(cli_result) == projection(mcp_result)
            check(f"expected-{case['id']}", expected_match, f"library result satisfies expected observation for {case['id']}")
            check(f"cli-parity-{case['id']}", parity and cli_exit == 0, f"library and CLI projections match for {case['id']}")
            check(f"mcp-parity-{case['id']}", parity and mcp_exit == 0, f"library and MCP projections match for {case['id']}")
            surface_cases.append(
                {
                    "id": case["id"],
                    "expected": expected,
                    "library": projection(library_result),
                    "cli": {"exit_status": cli_exit, "result": projection(cli_result)},
                    "mcp": {"exit_status": mcp_exit, "result": projection(mcp_result)},
                }
            )

        invalid_cli_exit, invalid_cli_result = invoke_cli({"invalid": "not-a-request"})
        # An unknown action is a domain HOLD, not a transport error.
        check("unknown-action-is-domain-result", invalid_cli_exit == 0 and invalid_cli_result["kind"] == "domain_result", "valid JSON remains a domain response")

        malformed = subprocess.run(
            [sys.executable, "cli_transport.py"],
            cwd=ROOT,
            input="{not-json",
            text=True,
            capture_output=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
        )
        malformed_result = json.loads(malformed.stdout)
        check("malformed-cli-is-transport-error", malformed.returncode == 2 and malformed_result["kind"] == "transport_error", "malformed CLI wire is not a domain HOLD")

        unknown_mcp = subprocess.run(
            [sys.executable, "mcp_transport.py"],
            cwd=ROOT,
            input=json.dumps({"jsonrpc": "2.0", "id": 9, "method": "unknown/method"}) + "\n",
            text=True,
            capture_output=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
        )
        unknown_mcp_result = json.loads(unknown_mcp.stdout)
        check("unknown-mcp-is-transport-error", unknown_mcp.returncode == 0 and unknown_mcp_result["error"]["data"]["kind"] == "transport_error", "unknown MCP method is a protocol error")

        manifest = {
            "manifest_schema": "fixture.oq012-oq014.result.v1",
            "fixture_id": FIXTURE_ID,
            "packet_ids": PACKETS,
            "input_sha256": input_sha256,
            "runner_python": platform.python_version(),
            "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
            "network": "disabled",
            "external_writes": False,
            "host_probe": host_probe,
            "surface_cases": surface_cases,
            "assertions": assertions,
            "all_assertions_pass": True,
        }
        print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"manifest_schema": "fixture.oq012-oq014.runner-error.v1", "error": str(error)}, sort_keys=True))
        raise
