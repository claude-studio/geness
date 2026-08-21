#!/usr/bin/env python3
"""Fixture-local JSON-RPC stdio transport for OQ-014."""

from __future__ import annotations

import json
import sys

from surface_service import dispatch


def response(message_id: object, value: dict[str, object]) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": message_id, "result": {"structuredContent": value}}


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "data": {"kind": "transport_error", "code": "INVALID_JSON"}}}))
            continue
        method = message.get("method")
        message_id = message.get("id")
        if method == "initialize":
            print(json.dumps(response(message_id, {"schema": "fixture.oq012-oq014.mcp.v1", "status": "READY"}), sort_keys=True))
        elif method == "notifications/initialized":
            continue
        elif method == "tools/call":
            params = message.get("params", {})
            if params.get("name") != "gee":
                print(json.dumps({"jsonrpc": "2.0", "id": message_id, "error": {"code": -32602, "data": {"kind": "transport_error", "code": "UNKNOWN_TOOL"}}}, sort_keys=True))
                continue
            print(json.dumps(response(message_id, dispatch(params.get("arguments", {}))), sort_keys=True))
        else:
            print(json.dumps({"jsonrpc": "2.0", "id": message_id, "error": {"code": -32601, "data": {"kind": "transport_error", "code": "METHOD_NOT_FOUND"}}}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
