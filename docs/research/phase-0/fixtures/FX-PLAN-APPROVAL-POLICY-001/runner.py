#!/usr/bin/env python3
"""Synthetic OQ-008 approval-actor candidate comparison fixture."""

from __future__ import annotations

import json
from pathlib import Path


FIXTURE_ID = "FX-PLAN-APPROVAL-POLICY-001"
EXPECTED_CANDIDATES = ("C-01", "C-02", "C-03")


def scenario_has_user_sensitive_boundary(scenario: dict[str, object]) -> bool:
    return any(
        (
            scenario["approval_class"] == "user_sensitive",
            scenario["scope_changed"],
            scenario["external_write"],
            scenario["destructive_action"],
            scenario["security_boundary_change"],
        )
    )


def evaluate(candidate_id: str, scenario: dict[str, object]) -> dict[str, str]:
    if not scenario["digest_current"]:
        return {
            "decision": "DENIED",
            "approval_actor": "none",
            "reason": "stale_digest",
        }

    if candidate_id == "C-01":
        actor = "user"
    elif candidate_id == "C-02":
        actor = "user" if scenario["approval_class"] == "user_sensitive" else "policy"
    elif candidate_id == "C-03":
        actor = "user" if scenario_has_user_sensitive_boundary(scenario) or scenario["side_effect"] != "none" else "policy"
    else:
        raise ValueError(f"unknown candidate: {candidate_id}")

    return {
        "decision": "ALLOWED",
        "approval_actor": actor,
        "reason": "fixture_candidate_rule",
    }


def main() -> int:
    input_path = Path(__file__).parent / "input" / "fixture.json"
    fixture = json.loads(input_path.read_text())
    candidates = [candidate["id"] for candidate in fixture["candidates"]]
    scenarios = fixture["scenarios"]
    expected = fixture["expected"]
    assertions: list[bool] = [
        fixture["fixture_id"] == FIXTURE_ID,
        fixture["deterministic"] is True,
        tuple(candidates) == EXPECTED_CANDIDATES,
        len(scenarios) == 7,
        set(expected) == set(EXPECTED_CANDIDATES),
    ]
    matrix: dict[str, dict[str, dict[str, str]]] = {}

    for candidate_id in candidates:
        matrix[candidate_id] = {}
        for scenario in scenarios:
            scenario_id = scenario["id"]
            observed = evaluate(candidate_id, scenario)
            matrix[candidate_id][scenario_id] = observed
            assertions.append(observed == expected[candidate_id][scenario_id])

    sensitive_scenarios = [
        scenario for scenario in scenarios if scenario["approval_class"] == "user_sensitive"
    ]
    for scenario in sensitive_scenarios:
        scenario_id = scenario["id"]
        assertions.append(
            all(
                matrix[candidate_id][scenario_id]["approval_actor"] == "user"
                for candidate_id in candidates
            )
        )

    stale_scenario_id = "stale_digest_routine"
    assertions.append(
        all(
            matrix[candidate_id][stale_scenario_id]
            == {"decision": "DENIED", "approval_actor": "none", "reason": "stale_digest"}
            for candidate_id in candidates
        )
    )
    result = {
        "fixture_id": FIXTURE_ID,
        "network": "disabled",
        "external_writes": False,
        "selected_candidate": None,
        "observations": {
            "candidate_matrix": matrix,
            "sensitive_floor": "user_sensitive scenarios require user across all candidates",
            "stale_digest_guard": "DENIED across all candidates",
        },
        "assertions_passed": sum(assertions),
        "all_assertions_pass": all(assertions),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    raise SystemExit(main())
