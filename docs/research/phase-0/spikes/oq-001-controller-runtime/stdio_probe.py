#!/usr/bin/env python3
"""Small newline-delimited JSON-RPC probe for the disposable OQ-001 servers."""

from __future__ import annotations

import argparse
import json
import selectors
import subprocess
import sys
import time
from pathlib import Path


def read_response(process: subprocess.Popen[str], expected_id: int, timeout: float) -> dict:
    selector = selectors.DefaultSelector()
    assert process.stdout is not None
    selector.register(process.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        remaining = max(0.01, deadline - time.monotonic())
        events = selector.select(remaining)
        if not events:
            continue
        line = process.stdout.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        if message.get("id") == expected_id:
            return message
    raise RuntimeError(f"timed out waiting for JSON-RPC response id={expected_id}")


def send(process: subprocess.Popen[str], message: dict) -> None:
    assert process.stdin is not None
    process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
    process.stdin.flush()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.command or args.command[0] != "--":
        parser.error("use -- before the candidate command")
    command = args.command[1:]

    started = time.monotonic()
    process = subprocess.Popen(
        command,
        cwd=args.cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    result: dict[str, object] = {"command": command, "cwd": str(args.cwd)}
    try:
        initialize = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "geness-oq001-probe", "version": "0.1.0"},
            },
        }
        send(process, initialize)
        initialized = read_response(process, 1, args.timeout)
        send(process, {"jsonrpc": "2.0", "method": "notifications/initialized"})

        send(process, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        tools = read_response(process, 2, args.timeout)
        result["tools_response"] = tools
        tool_names = [tool.get("name") for tool in tools.get("result", {}).get("tools", [])]
        if "echo" not in tool_names:
            raise RuntimeError(f"echo tool missing: {tool_names}")

        send(
            process,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "echo", "arguments": {"message": "round-trip"}},
            },
        )
        call = read_response(process, 3, args.timeout)
        content = call.get("result", {}).get("content", [])
        text_values = [item.get("text") for item in content if item.get("type") == "text"]
        structured = call.get("result", {}).get("structuredContent", {})
        if "round-trip" not in text_values and structured.get("message") != "round-trip":
            raise RuntimeError(f"unexpected echo result: {call}")

        result.update(
            {
                "protocol_version": initialized.get("result", {}).get("protocolVersion"),
                "server_info": initialized.get("result", {}).get("serverInfo"),
                "tool_names": tool_names,
                "echo": text_values or [structured.get("message")],
                "elapsed_ms": round((time.monotonic() - started) * 1000, 2),
            }
        )
    except Exception as exc:  # pragma: no cover - exercised by failed candidate runs
        result.update({"error": str(exc), "elapsed_ms": round((time.monotonic() - started) * 1000, 2)})
        print(json.dumps(result, sort_keys=True), file=sys.stderr)
        process.kill()
        process.wait()
        return 1
    finally:
        if process.stdin is not None:
            process.stdin.close()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        stderr = process.stderr.read() if process.stderr is not None else ""
        result["exit_status"] = process.returncode
        result["stderr"] = stderr[-2000:]

    print(json.dumps(result, sort_keys=True))
    return 0 if result["exit_status"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
