#!/usr/bin/env python3
"""Fixture-local CLI wire adapter; domain decisions stay in common_service."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common_service import ApplicationService


TRANSPORT_SCHEMA = "fixture.transport_error.v1"


def transport_error(code: str, message: str) -> dict[str, str]:
    return {
        "kind": "transport_error",
        "schema": TRANSPORT_SCHEMA,
        "code": code,
        "message": message,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    args = parser.parse_args()

    wire = sys.stdin.read()
    try:
        command = json.loads(wire)
    except json.JSONDecodeError:
        print(json.dumps(transport_error("INVALID_JSON", "wire input is not valid JSON"), sort_keys=True))
        return 2

    if not isinstance(command, dict):
        print(json.dumps(transport_error("INVALID_COMMAND_SHAPE", "wire input must be a JSON object"), sort_keys=True))
        return 2

    result = ApplicationService(Path(args.state)).handle(command)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
