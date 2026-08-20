#!/usr/bin/env python3
"""Minimal disposable lifecycle, lease, and completion replay fixture.

This runner is evidence-only and is not a production Controller implementation.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


FIXTURE_ID = "FX-LIFECYCLE-LEASE-COMPLETION-001"


def transition(source: str, target: str, *, digest_current: bool = True) -> dict[str, object]:
    allowed = {
        ("INITIALIZING", "INTERVIEWING"),
        ("PLAN_APPROVED", "RUNNING"),
        ("RUNNING", "VERIFYING"),
        ("FAILED", "REOPENED"),
    }
    if (source, target) not in allowed:
        return {"decision": "DENIED", "reason": "edge_not_allowed"}
    if (source, target) == ("PLAN_APPROVED", "RUNNING") and not digest_current:
        return {"decision": "DENIED", "reason": "stale_digest"}
    return {"decision": "ALLOWED", "reason": "fixture_rule"}


def replay_completion(state: dict[str, object]) -> dict[str, object]:
    if state["terminal_checkpoint"]:
        state["lease_active"] = False
        state["completed"] = True
    return dict(state)


def main() -> int:
    allowed = transition("INITIALIZING", "INTERVIEWING")
    denied = transition("PLAN_APPROVED", "RUNNING", digest_current=False)
    invalid = transition("INTERVIEWING", "RUNNING")

    with tempfile.TemporaryDirectory(prefix="geness-lifecycle-") as temp_dir:
        lock_path = Path(temp_dir) / "writer.lock"
        first_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(first_fd)
        try:
            os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            second_writer = "DENIED"
        else:
            second_writer = "ALLOWED"

    before = {"terminal_checkpoint": True, "lease_active": True, "completed": False}
    after_first_replay = replay_completion(before)
    after_second_replay = replay_completion(after_first_replay)
    assertions = [
        allowed["decision"] == "ALLOWED",
        denied == {"decision": "DENIED", "reason": "stale_digest"},
        invalid["decision"] == "DENIED",
        second_writer == "DENIED",
        after_first_replay == after_second_replay,
        after_second_replay["completed"] is True,
        after_second_replay["lease_active"] is False,
    ]
    result = {
        "fixture_id": FIXTURE_ID,
        "network": "disabled",
        "external_writes": False,
        "observations": {
            "allowed_transition": allowed,
            "stale_digest_transition": denied,
            "invalid_transition": invalid,
            "two_writer_probe": {"first_writer": "ALLOWED", "second_writer": second_writer},
            "completion_replay": {
                "first": after_first_replay,
                "second": after_second_replay,
            },
        },
        "assertions_passed": sum(assertions),
        "all_assertions_pass": all(assertions),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    raise SystemExit(main())
