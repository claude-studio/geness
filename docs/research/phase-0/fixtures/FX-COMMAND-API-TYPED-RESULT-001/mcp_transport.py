#!/usr/bin/env python3
"""Fixture-local MCP-like stdio adapter; it does not implement domain policy."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from common_service import ApplicationService


TRANSPORT_SCHEMA = "fixture.transport_error.v1"


def rpc_error(request_id: Any, code: int, message: str, transport_code: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
            "data": {
                "kind": "transport_error",
                "schema": TRANSPORT_SCHEMA,
                "code": transport_code,
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    args = parser.parse_args()
    service: ApplicationService | None = None

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            print(json.dumps(rpc_error(None, -32700, "parse error", "PARSE_ERROR"), sort_keys=True), flush=True)
            continue

        request_id = message.get("id") if isinstance(message, dict) else None
        method = message.get("method") if isinstance(message, dict) else None
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "fixture-mcp/1",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "oq-002-fixture", "version": "1"},
                },
            }
            print(json.dumps(response, sort_keys=True), flush=True)
            continue
        if method == "notifications/initialized":
            continue
        if method == "tools/call":
            params = message.get("params") if isinstance(message, dict) else None
            if not isinstance(params, dict) or params.get("name") != "command":
                response = rpc_error(request_id, -32602, "invalid tool call", "INVALID_TOOL_CALL")
                print(json.dumps(response, sort_keys=True), flush=True)
                continue
            command = params.get("arguments")
            if not isinstance(command, dict):
                response = rpc_error(request_id, -32602, "tool arguments must be an object", "INVALID_ARGUMENTS")
                print(json.dumps(response, sort_keys=True), flush=True)
                continue
            if service is None:
                service = ApplicationService(Path(args.state))
            domain_result = service.handle(command)
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "structuredContent": domain_result,
                    "content": [{"type": "text", "text": json.dumps(domain_result, sort_keys=True)}],
                },
            }
            print(json.dumps(response, sort_keys=True), flush=True)
            continue

        response = rpc_error(request_id, -32601, "method not found", "METHOD_NOT_FOUND")
        print(json.dumps(response, sort_keys=True), flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
