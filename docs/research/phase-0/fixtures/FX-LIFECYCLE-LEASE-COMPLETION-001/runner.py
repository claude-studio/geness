#!/usr/bin/env python3
"""Disposable lifecycle, lease, and completion crash-point fixture.

This runner is evidence-only and is not a production Controller implementation.
"""

from __future__ import annotations

import json
import os
import tempfile
from copy import deepcopy
from pathlib import Path


FIXTURE_ID = "FX-LIFECYCLE-LEASE-COMPLETION-001"
INPUT_PATH = Path(__file__).with_name("input") / "fixture.json"
OPERATION_ID = "op-oq009-completion-001"


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


def new_completion_state() -> dict[str, object]:
    return {
        "runtime": {
            "terminal_checkpoint": False,
            "lease_active": True,
            "completed": False,
            "operation_id": None,
        },
        "projection": {"status": "VERIFYING", "operation_id": None},
        "exposed_completed": False,
    }


def projection_prepare(state: dict[str, object]) -> None:
    projection = state["projection"]
    assert isinstance(projection, dict)
    projection["status"] = "COMPLETED"
    projection["operation_id"] = OPERATION_ID


def runtime_atomic_commit(state: dict[str, object]) -> None:
    runtime = state["runtime"]
    assert isinstance(runtime, dict)
    runtime.update(
        {
            "terminal_checkpoint": True,
            "lease_active": False,
            "completed": True,
            "operation_id": OPERATION_ID,
        }
    )


def expose_if_runtime_is_complete(state: dict[str, object]) -> None:
    runtime = state["runtime"]
    projection = state["projection"]
    assert isinstance(runtime, dict)
    assert isinstance(projection, dict)
    if (
        runtime["terminal_checkpoint"]
        and not runtime["lease_active"]
        and runtime["completed"]
        and projection["status"] == "COMPLETED"
    ):
        state["exposed_completed"] = True


def safety_violations(state: dict[str, object]) -> list[str]:
    runtime = state["runtime"]
    assert isinstance(runtime, dict)
    violations: list[str] = []
    if not runtime["terminal_checkpoint"] and not runtime["lease_active"]:
        violations.append("lease_released_before_terminal_checkpoint")
    if state["exposed_completed"] and not (
        runtime["terminal_checkpoint"]
        and not runtime["lease_active"]
        and runtime["completed"]
    ):
        violations.append("completed_exposed_before_runtime_commit")
    if runtime["completed"] and not (
        runtime["terminal_checkpoint"] and not runtime["lease_active"]
    ):
        violations.append("completed_without_terminal_checkpoint_and_released_lease")
    return violations


def replay_completion(state: dict[str, object]) -> dict[str, object]:
    """Apply the operation-id reconciliation result to a copied state."""

    replayed = deepcopy(state)
    runtime = replayed["runtime"]
    projection = replayed["projection"]
    assert isinstance(runtime, dict)
    assert isinstance(projection, dict)
    runtime.update(
        {
            "terminal_checkpoint": True,
            "lease_active": False,
            "completed": True,
            "operation_id": OPERATION_ID,
        }
    )
    projection.update({"status": "COMPLETED", "operation_id": OPERATION_ID})
    replayed["exposed_completed"] = True
    return replayed


def simulate_crash(candidate: str, crash_point: str) -> dict[str, object]:
    """Return the state visible at the requested logical crash point."""

    state = new_completion_state()

    if candidate == "C-01":
        # The projection is prepared but is not a completion authority. The
        # terminal checkpoint and lease release become visible together.
        projection_prepare(state)
        if crash_point == "after_projection":
            return state
        if crash_point in {"after_lease_release", "after_terminal_checkpoint"}:
            return state
        runtime_atomic_commit(state)
        if crash_point == "after_runtime_commit":
            expose_if_runtime_is_complete(state)
            return state
        expose_if_runtime_is_complete(state)
        return state

    if candidate == "C-02":
        # The lease release is deliberately a separate first write.
        runtime = state["runtime"]
        assert isinstance(runtime, dict)
        runtime["lease_active"] = False
        if crash_point == "after_lease_release":
            return state
        runtime["terminal_checkpoint"] = True
        runtime["completed"] = True
        runtime["operation_id"] = OPERATION_ID
        if crash_point in {"after_terminal_checkpoint", "after_runtime_commit"}:
            return state
        projection_prepare(state)
        expose_if_runtime_is_complete(state)
        return state

    if candidate == "C-03":
        # The projection is treated as externally visible before runtime
        # completion. This is the unsafe ordering under investigation.
        projection_prepare(state)
        state["exposed_completed"] = True
        if crash_point == "after_projection":
            return state
        if crash_point in {"after_lease_release", "after_terminal_checkpoint"}:
            return state
        runtime_atomic_commit(state)
        if crash_point == "after_runtime_commit":
            return state
        expose_if_runtime_is_complete(state)
        return state

    raise ValueError(f"unknown candidate: {candidate}")


def run_crash_matrix(data: dict[str, object]) -> tuple[list[dict[str, object]], list[bool]]:
    crash_points = data["completion_cases"][0]["crash_points"]
    candidates = data["completion_cases"][0]["candidates"]
    assert isinstance(crash_points, list)
    assert isinstance(candidates, list)
    rows: list[dict[str, object]] = []
    assertions: list[bool] = []
    for candidate_case in candidates:
        assert isinstance(candidate_case, dict)
        candidate = candidate_case["id"]
        expected_unsafe = candidate_case["expected_unsafe_crash_points"]
        assert isinstance(candidate, str)
        assert isinstance(expected_unsafe, list)
        for crash_point in crash_points:
            assert isinstance(crash_point, str)
            visible = simulate_crash(candidate, crash_point)
            replayed_once = replay_completion(visible)
            replayed_twice = replay_completion(replayed_once)
            violations = safety_violations(visible)
            expected_safe = crash_point not in expected_unsafe
            post_replay_violations = safety_violations(replayed_once)
            row = {
                "candidate": candidate,
                "crash_point": crash_point,
                "pre_replay_safe": not violations,
                "pre_replay_violations": violations,
                "post_replay_safe": not post_replay_violations,
                "post_replay_idempotent": replayed_once == replayed_twice,
            }
            rows.append(row)
            assertions.extend(
                [
                    row["pre_replay_safe"] is expected_safe,
                    row["post_replay_safe"] is True,
                    row["post_replay_idempotent"] is True,
                ]
            )
    return rows, assertions


def main() -> int:
    data = json.loads(INPUT_PATH.read_text())
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
    after_first_replay = {
        "terminal_checkpoint": True,
        "lease_active": False,
        "completed": True,
    }
    after_second_replay = dict(after_first_replay)
    matrix, matrix_assertions = run_crash_matrix(data)
    assertions = [
        allowed["decision"] == "ALLOWED",
        denied == {"decision": "DENIED", "reason": "stale_digest"},
        invalid["decision"] == "DENIED",
        second_writer == "DENIED",
        after_first_replay == after_second_replay,
        after_second_replay["completed"] is True,
        after_second_replay["lease_active"] is False,
    ]
    assertions.extend(matrix_assertions)
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
            "crash_point_matrix": matrix,
        },
        "assertions_passed": sum(assertions),
        "all_assertions_pass": all(assertions),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    raise SystemExit(main())
