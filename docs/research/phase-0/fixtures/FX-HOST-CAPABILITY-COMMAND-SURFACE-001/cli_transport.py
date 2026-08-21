#!/usr/bin/env python3
"""Fixture-local CLI thin transport for OQ-014."""

from __future__ import annotations

import json
import sys

from surface_service import dispatch


def main() -> int:
    wire = sys.stdin.read()
    try:
        request = json.loads(wire)
    except json.JSONDecodeError:
        print(json.dumps({"schema": "fixture.oq012-oq014.transport-error.v1", "kind": "transport_error", "code": "INVALID_JSON"}))
        return 2
    print(json.dumps(dispatch(request), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
