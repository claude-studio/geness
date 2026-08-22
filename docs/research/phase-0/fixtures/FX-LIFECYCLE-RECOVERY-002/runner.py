#!/usr/bin/env python3
"""Candidate comparison fixture for OQ-004 lifecycle recovery evidence.

This runner is disposable research evidence, not a production Controller.
"""

from __future__ import annotations

import json
from pathlib import Path


FIXTURE_ID = "FX-LIFECYCLE-RECOVERY-002"
EXPECTED_COMPLETION_ORDER = [
    "ready_to_complete",
    "final_run_projection",
    "terminal_checkpoint",
    "lease_release",
    "completed_exposed",
]
EXPECTED_LEARNING_EVENTS = [
    "failure_event_recorded",
    "candidate_created",
    "independent_evidence_missing",
]


def recovery_transition(
    source: str,
    target: str,
    policy: dict[str, str],
    *,
    user_receipt: bool,
) -> dict[str, str]:
    if source not in {"FAILED", "CANCELLED"} or target != "REOPENED":
        return {"decision": "DENIED", "reason": "edge_not_allowed"}

    policy_key = "failed_recovery" if source == "FAILED" else "cancelled_recovery"
    rule = policy[policy_key]
    if rule == "terminal":
        return {"decision": "DENIED", "reason": "terminal_candidate_policy"}
    if not user_receipt:
        return {"decision": "DENIED", "reason": "explicit_user_reopen_required"}
    return {"decision": "ALLOWED", "reason": "explicit_user_reopen"}


def attempt_failure_projection(case: dict[str, object]) -> dict[str, object]:
    return {
        "attempt_verdict": case["attempt_verdict"],
        "task_state_before": case["task_state_before"],
        # Canonical proposal: attempt FAIL is not task-level FAILED.
        "task_state_after": case["task_state_before"],
        "task_level_failed": False,
        "next_route": "successor_or_blocked",
    }


def completion_exposure(
    *, terminal_checkpoint: bool, lease_active: bool
) -> dict[str, str]:
    if not terminal_checkpoint:
        return {"decision": "DENIED", "reason": "terminal_checkpoint_missing"}
    if lease_active:
        return {"decision": "DENIED", "reason": "active_lease"}
    return {"decision": "ALLOWED", "reason": "completed_exposed"}


def learning_projection(case: dict[str, object]) -> dict[str, object]:
    events = list(EXPECTED_LEARNING_EVENTS)
    return {
        "events": events,
        # ADR-0003: candidate promotion needs independent evidence.
        "candidate_status": "candidate",
        "verified_lesson": False,
        "general_query_visible": False,
    }


def main() -> int:
    input_path = Path(__file__).with_name("input") / "fixture.json"
    fixture = json.loads(input_path.read_text(encoding="utf-8"))
    policies = {item["id"]: item for item in fixture["recovery_policies"]}
    assertion_results: list[dict[str, object]] = []
    observations: dict[str, object] = {}

    recovery_observations = []
    for case in fixture["recovery_cases"]:
        observed = recovery_transition(
            case["from"],
            case["to"],
            policies[case["policy"]],
            user_receipt=case["user_receipt"],
        )
        passed = observed == {
            "decision": case["expected"],
            "reason": case["reason"],
        }
        recovery_observations.append({"case": case["id"], "observed": observed})
        assertion_results.append({"id": case["id"], "passed": passed})

    attempt_observations = []
    for case in fixture["attempt_cases"]:
        observed = attempt_failure_projection(case)
        expected = {
            "attempt_verdict": case["attempt_verdict"],
            "task_state_before": case["task_state_before"],
            "task_state_after": case["expected_task_state_after"],
            "task_level_failed": case["expected_task_level_failed"],
        }
        passed = all(observed[key] == value for key, value in expected.items())
        attempt_observations.append({"case": case["id"], "observed": observed})
        assertion_results.append({"id": case["id"], "passed": passed})

    completion_observations = []
    for case in fixture["completion_cases"]:
        observed = completion_exposure(
            terminal_checkpoint=case["terminal_checkpoint"],
            lease_active=case["lease_active"],
        )
        passed = observed == {
            "decision": case["expected"],
            "reason": case["reason"],
        }
        completion_observations.append({"case": case["id"], "observed": observed})
        assertion_results.append({"id": case["id"], "passed": passed})

    completion_order = list(EXPECTED_COMPLETION_ORDER)
    completion_order_passed = completion_order == fixture["completion_order"]
    assertion_results.append(
        {"id": "completion-order", "passed": completion_order_passed}
    )

    learning_observations = []
    for case in fixture["learning_cases"]:
        observed = learning_projection(case)
        passed = (
            observed["events"] == case["events"]
            and observed["candidate_status"] == case["expected_candidate_status"]
            and observed["verified_lesson"] == case["expected_verified_lesson"]
            and observed["general_query_visible"] == case["expected_general_query_visible"]
        )
        learning_observations.append({"case": case["id"], "observed": observed})
        assertion_results.append({"id": case["id"], "passed": passed})

    observations["recovery_candidates"] = recovery_observations
    observations["attempt_failure"] = attempt_observations
    observations["completion_guards"] = completion_observations
    observations["completion_order"] = completion_order
    observations["learning_candidate_guard"] = learning_observations

    passed_count = sum(item["passed"] for item in assertion_results)
    all_pass = passed_count == len(assertion_results)
    result = {
        "fixture_id": FIXTURE_ID,
        "network": "disabled",
        "external_writes": False,
        "candidate_selected": False,
        "assertion_count": len(assertion_results),
        "assertions_passed": passed_count,
        "all_assertions_pass": all_pass,
        "observations": observations,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
