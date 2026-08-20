#!/usr/bin/env python3
"""Fixture-local application service; not production Geness code."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


RESULT_SCHEMA = "fixture.command_result.v1"


def _stable_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _empty_state() -> dict[str, Any]:
    return {"applied": {}, "side_effect_count": 0}


def _read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return _empty_state()
    return json.loads(path.read_text(encoding="utf-8"))


def _write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix="fixture-state-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


class ApplicationService:
    """Small deterministic service used by all three fixture entry paths."""

    def __init__(self, state_path: str | Path):
        self.state_path = Path(state_path)

    def handle(self, command: dict[str, Any]) -> dict[str, Any]:
        action = command.get("action")
        operation_id = command.get("idempotency_key")
        state = _read_state(self.state_path)

        if action == "gate.check":
            if command.get("approved") is not True:
                return {
                    "kind": "domain_result",
                    "schema": RESULT_SCHEMA,
                    "status": "HOLD",
                    "code": "APPROVAL_REQUIRED",
                    "operation_id": operation_id,
                    "effect_id": None,
                    "decision": None,
                    "side_effect_count": state["side_effect_count"],
                    "replayed": False,
                }
            return {
                "kind": "domain_result",
                "schema": RESULT_SCHEMA,
                "status": "CLEAR",
                "code": "APPROVAL_PRESENT",
                "operation_id": operation_id,
                "effect_id": None,
                "decision": None,
                "side_effect_count": state["side_effect_count"],
                "replayed": False,
            }

        if action == "record_decision":
            decision = command.get("decision")
            fingerprint = _stable_digest(
                {
                    "action": action,
                    "idempotency_key": operation_id,
                    "decision": decision,
                }
            )
            existing = state["applied"].get(operation_id)
            if existing is not None:
                if existing["fingerprint"] != fingerprint:
                    return {
                        "kind": "domain_result",
                        "schema": RESULT_SCHEMA,
                        "status": "HOLD",
                        "code": "IDEMPOTENCY_KEY_CONFLICT",
                        "operation_id": operation_id,
                        "effect_id": existing["result"]["effect_id"],
                        "decision": existing["result"]["decision"],
                        "side_effect_count": state["side_effect_count"],
                        "replayed": False,
                    }
                replay = dict(existing["result"])
                replay["status"] = "REPLAYED"
                replay["replayed"] = True
                return replay

            effect_id = f"effect-{fingerprint[:12]}"
            state["side_effect_count"] += 1
            result = {
                "kind": "domain_result",
                "schema": RESULT_SCHEMA,
                "status": "APPLIED",
                "code": "DECISION_RECORDED",
                "operation_id": operation_id,
                "effect_id": effect_id,
                "decision": decision,
                "side_effect_count": state["side_effect_count"],
                "replayed": False,
            }
            state["applied"][operation_id] = {
                "fingerprint": fingerprint,
                "result": result,
            }
            _write_state(self.state_path, state)
            return result

        return {
            "kind": "domain_result",
            "schema": RESULT_SCHEMA,
            "status": "HOLD",
            "code": "UNSUPPORTED_ACTION",
            "operation_id": operation_id,
            "effect_id": None,
            "decision": None,
            "side_effect_count": state["side_effect_count"],
            "replayed": False,
        }
