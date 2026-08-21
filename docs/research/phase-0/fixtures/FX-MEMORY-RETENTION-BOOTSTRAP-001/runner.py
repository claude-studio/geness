#!/usr/bin/env python3
"""Evidence-only memory evaluator, retention, and bootstrap fixture.

This runner deliberately does not implement a Geness product schema or controller.
All thresholds and typed results are fixture-local candidate observations.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any


FIXTURE_ID = "FX-MEMORY-RETENTION-BOOTSTRAP-001"
ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "fixture.json"
RETRIEVAL_STATUSES = {"verified", "enforced"}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def parse_day(value: str) -> date:
    return date.fromisoformat(value)


def visible_lesson_ids(lessons: dict[str, dict[str, Any]]) -> list[str]:
    return sorted(
        lesson_id
        for lesson_id, lesson in lessons.items()
        if lesson["status"] in RETRIEVAL_STATUSES
    )


def new_lesson(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "lesson_id": event["lesson_id"],
        "fingerprint": event["fingerprint"],
        "status": "candidate",
        "opened_at": event["occurred_at"],
        "failure_event_ids": [],
        "independent_failure_runs": [],
        "evidence_refs": [],
        "eligible_exposure_ids": [],
        "ignored_exposure_ids": [],
        "unassisted_successes": 0,
        "decay_signal_count": 0,
        "transitions": [],
    }


def record_transition(
    lesson: dict[str, Any],
    *,
    event_id: str,
    to_status: str,
    reason: str,
) -> None:
    before = lesson["status"]
    if before == to_status:
        return
    lesson["status"] = to_status
    lesson["transitions"].append(
        {
            "event_id": event_id,
            "from": before,
            "to": to_status,
            "reason": reason,
        }
    )


def maybe_expire(
    lesson: dict[str, Any],
    event: dict[str, Any],
    policy: dict[str, Any],
) -> None:
    if lesson["status"] not in {"candidate", "probationary"}:
        return
    age_days = (parse_day(event["occurred_at"]) - parse_day(lesson["opened_at"])).days
    if (
        lesson["unassisted_successes"] >= policy["unassisted_successes_to_expire"]
        and age_days >= policy["minimum_observation_age_days"]
    ):
        record_transition(
            lesson,
            event_id=event["event_id"],
            to_status="expired",
            reason="eligible_unassisted_success_and_minimum_age",
        )


def replay_events(
    events: list[dict[str, Any]],
    policy: dict[str, Any],
) -> dict[str, Any]:
    lessons: dict[str, dict[str, Any]] = {}
    ignored_exposures: list[str] = []
    checkpoints: list[dict[str, Any]] = []
    evaluator_inputs: list[str] = []

    for event in events:
        event_type = event["type"]
        lesson_id = event.get("lesson_id")
        if event_type == "failure_observed":
            lesson = lessons.setdefault(lesson_id, new_lesson(event))
            lesson["failure_event_ids"].append(event["event_id"])
            lesson["evidence_refs"] = sorted(
                set(lesson["evidence_refs"]) | set(event.get("evidence_refs", []))
            )
            if event["run_id"] not in lesson["independent_failure_runs"]:
                lesson["independent_failure_runs"].append(event["run_id"])
            if (
                len(lesson["independent_failure_runs"])
                >= policy["independent_failure_runs_required"]
                and lesson["evidence_refs"]
                and lesson["status"] in {"candidate", "probationary"}
            ):
                record_transition(
                    lesson,
                    event_id=event["event_id"],
                    to_status="verified",
                    reason="independent_failure_recurrence_with_evidence",
                )
        elif event_type == "guard_evidence":
            lesson = lessons[lesson_id]
            if (
                event["fail_before"]
                and event["pass_after"]
                and event["reproducible"]
                and event.get("evidence_refs")
                and lesson["status"] in {"candidate", "probationary"}
            ):
                record_transition(
                    lesson,
                    event_id=event["event_id"],
                    to_status="verified",
                    reason="reproducible_guard_evidence",
                )
        elif event_type == "exposure":
            lesson = lessons[lesson_id]
            if not event["eligible"]:
                ignored_exposures.append(event["event_id"])
                lesson["ignored_exposure_ids"].append(event["event_id"])
            else:
                evaluator_inputs.append(event["event_id"])
                lesson["eligible_exposure_ids"].append(event["event_id"])
                if event["outcome"] == "success" and not event["lesson_injected"]:
                    lesson["unassisted_successes"] += 1
                    lesson["decay_signal_count"] += 1
                    maybe_expire(lesson, event, policy)
        else:
            raise AssertionError(f"unsupported event type: {event_type}")

        checkpoint = event.get("checkpoint")
        if checkpoint:
            checkpoints.append(
                {
                    "checkpoint": checkpoint,
                    "visible_lesson_ids": visible_lesson_ids(lessons),
                    "lesson_statuses": {
                        key: lessons[key]["status"] for key in sorted(lessons)
                    },
                }
            )

    normalized_lessons: dict[str, dict[str, Any]] = {}
    for lesson_id in sorted(lessons):
        lesson = lessons[lesson_id]
        normalized_lessons[lesson_id] = {
            **lesson,
            "independent_failure_runs": sorted(lesson["independent_failure_runs"]),
            "evidence_refs": sorted(lesson["evidence_refs"]),
            "eligible_exposure_ids": sorted(lesson["eligible_exposure_ids"]),
            "ignored_exposure_ids": sorted(lesson["ignored_exposure_ids"]),
        }

    return {
        "evaluator_version": policy["version"],
        "events_replayed": len(events),
        "lessons": normalized_lessons,
        "ignored_exposure_ids": sorted(ignored_exposures),
        "evaluator_input_exposure_ids": sorted(evaluator_inputs),
        "retrieval_checkpoints": checkpoints,
        "final_visible_lesson_ids": visible_lesson_ids(normalized_lessons),
    }


def replay_probe(
    events: list[dict[str, Any]],
    policy: dict[str, Any],
) -> tuple[dict[str, Any], list[bool]]:
    first = replay_events(events, policy)
    second = replay_events(events, policy)
    repeat = first["lessons"]["LESSON-REPEAT"]
    oneoff = first["lessons"]["LESSON-ONEOFF"]
    guard = first["lessons"]["LESSON-GUARD"]
    checkpoints = {item["checkpoint"]: item for item in first["retrieval_checkpoints"]}
    assertions = [
        first == second,
        first["final_visible_lesson_ids"] == ["LESSON-GUARD", "LESSON-REPEAT"],
        repeat["status"] == "verified",
        repeat["independent_failure_runs"] == ["RUN-001", "RUN-002"],
        oneoff["status"] == "expired",
        oneoff["eligible_exposure_ids"]
        == [
            "EXPOSURE-ONEOFF-INJECTED",
            "EXPOSURE-ONEOFF-UNASSISTED-001",
            "EXPOSURE-ONEOFF-UNASSISTED-002",
            "EXPOSURE-ONEOFF-UNASSISTED-003",
        ],
        oneoff["unassisted_successes"] == 3,
        oneoff["ignored_exposure_ids"] == ["EXPOSURE-ONEOFF-INELIGIBLE"],
        guard["status"] == "verified",
        checkpoints["after-first-failure"]["visible_lesson_ids"] == [],
        checkpoints["after-independent-recurrence"]["visible_lesson_ids"]
        == ["LESSON-REPEAT"],
        checkpoints["oneoff-expired"]["visible_lesson_ids"]
        == ["LESSON-REPEAT"],
        "EXPOSURE-UNRELATED-SUCCESS" in first["ignored_exposure_ids"],
    ]
    observation = {
        "replay_equal": first == second,
        "first_projection_sha256": sha256(first),
        "second_projection_sha256": sha256(second),
        "projection": first,
    }
    return observation, assertions


def retention_decision(
    item: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    if item["store"] == "memory":
        return {
            "case_id": item["case_id"],
            "action": "KEEP",
            "reason": "memory_store_separate",
        }
    if item["state"] == "active":
        return {
            "case_id": item["case_id"],
            "action": "KEEP",
            "reason": "active_runtime_protected",
        }
    if item["state"] == "blocked":
        return {
            "case_id": item["case_id"],
            "action": "KEEP",
            "reason": "blocked_runtime_protected",
        }
    if item["risk"] == "high" and item["explicit_disposition"] is None:
        return {
            "case_id": item["case_id"],
            "action": "KEEP",
            "reason": "high_risk_requires_disposition",
        }
    if item["age_days"] > policy["completed_low_risk_ttl_days"]:
        return {
            "case_id": item["case_id"],
            "action": "PRUNE",
            "reason": "completed_low_risk_ttl",
        }
    if item["size_bytes"] > policy["completed_item_size_limit_bytes"]:
        return {
            "case_id": item["case_id"],
            "action": "PRUNE",
            "reason": "completed_size_limit",
        }
    return {
        "case_id": item["case_id"],
        "action": "KEEP",
        "reason": "completed_within_candidate_limits",
    }


def retention_probe(
    cases: list[dict[str, Any]],
    policy: dict[str, Any],
) -> tuple[dict[str, Any], list[bool]]:
    decisions = [retention_decision(case, policy) for case in cases]
    expected_by_id = {case["case_id"]: case for case in cases}
    assertions = [
        decision["action"] == expected_by_id[decision["case_id"]]["expected_action"]
        and decision["reason"] == expected_by_id[decision["case_id"]]["expected_reason"]
        for decision in decisions
    ]
    by_id = {decision["case_id"]: decision for decision in decisions}
    assertions.extend(
        [
            by_id["RUNTIME-ACTIVE-OLD-LARGE"]["action"] == "KEEP",
            by_id["RUNTIME-BLOCKED-OLD-LARGE"]["action"] == "KEEP",
            by_id["MEMORY-VERIFIED-LESSON-OLD"]["action"] == "KEEP",
            by_id["RUNTIME-COMPLETED-LOW-TTL"]["action"] == "PRUNE",
            by_id["RUNTIME-COMPLETED-LOW-SIZE"]["action"] == "PRUNE",
        ]
    )
    return {
        "policy_version": policy["version"],
        "decisions": decisions,
        "kept_case_ids": sorted(
            decision["case_id"]
            for decision in decisions
            if decision["action"] == "KEEP"
        ),
        "pruned_case_ids": sorted(
            decision["case_id"]
            for decision in decisions
            if decision["action"] == "PRUNE"
        ),
    }, assertions


def bootstrap_result(case: dict[str, Any]) -> dict[str, Any]:
    state = case["storage_state"]
    if state == "missing":
        return {
            "result_type": "MEMORY_CAPABILITY_RESULT",
            "schema_version": 1,
            "status": "UNINITIALIZED",
            "gate": "CLEAR",
            "can_continue": True,
            "query_status": "NO_DATA",
            "lesson_ids": [],
            "attention": "bootstrap_pending",
            "required_action": "bootstrap_on_first_write",
        }
    if state == "empty":
        return {
            "result_type": "MEMORY_CAPABILITY_RESULT",
            "schema_version": 1,
            "status": "EMPTY",
            "gate": "CLEAR",
            "can_continue": True,
            "query_status": "EMPTY",
            "lesson_ids": [],
            "attention": "none",
            "required_action": "none",
        }
    if state == "ready":
        return {
            "result_type": "MEMORY_CAPABILITY_RESULT",
            "schema_version": 1,
            "status": "AVAILABLE",
            "gate": "CLEAR",
            "can_continue": True,
            "query_status": "READY",
            "lesson_ids": ["LESSON-READY"],
            "attention": "none",
            "required_action": "none",
        }
    if state == "corrupt":
        return {
            "result_type": "MEMORY_CAPABILITY_RESULT",
            "schema_version": 1,
            "status": "UNAVAILABLE",
            "gate": "HOLD",
            "can_continue": False,
            "query_status": "NOT_RUN",
            "lesson_ids": [],
            "attention": "memory_unavailable",
            "required_action": "rebuild_or_repair",
        }
    raise AssertionError(f"unsupported bootstrap state: {state}")


def bootstrap_probe(
    cases: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[bool]]:
    results = [bootstrap_result(case) for case in cases]
    expected_by_id = {case["case_id"]: case for case in cases}
    assertions = []
    for case, result in zip(cases, results):
        expected = expected_by_id[case["case_id"]]
        assertions.extend(
            [
                result["status"] == expected["expected_status"],
                result["gate"] == expected["expected_gate"],
                result["can_continue"] == expected["expected_can_continue"],
                result["required_action"] == expected["expected_action"],
            ]
        )
    by_id = {case["case_id"]: result for case, result in zip(cases, results)}
    assertions.extend(
        [
            by_id["MEMORY-MISSING"]["status"] != by_id["MEMORY-EMPTY"]["status"],
            by_id["MEMORY-CORRUPT"]["status"] != by_id["MEMORY-EMPTY"]["status"],
            by_id["MEMORY-CORRUPT"]["query_status"] == "NOT_RUN",
        ]
    )
    return {
        "result_contract": "fixture.memory-capability-result-v1",
        "results": [
            {"case_id": case["case_id"], **result}
            for case, result in zip(cases, results)
        ],
    }, assertions


def main() -> int:
    fixture_input = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    if fixture_input["fixture_schema"] != "fixture.memory-retention-bootstrap.input.v1":
        raise AssertionError("unexpected fixture schema")

    replay_observation, replay_assertions = replay_probe(
        fixture_input["events"], fixture_input["evaluator_policy"]
    )
    retention_observation, retention_assertions = retention_probe(
        fixture_input["retention_cases"], fixture_input["retention_policy_candidate"]
    )
    bootstrap_observation, bootstrap_assertions = bootstrap_probe(
        fixture_input["bootstrap_cases"]
    )
    assertions = replay_assertions + retention_assertions + bootstrap_assertions
    result = {
        "fixture_id": FIXTURE_ID,
        "fixture_schema": fixture_input["fixture_schema"],
        "network": "disabled",
        "external_writes": False,
        "assertions_passed": sum(assertions),
        "assertions_total": len(assertions),
        "all_assertions_pass": all(assertions),
        "observations": {
            "replay": replay_observation,
            "retention": retention_observation,
            "bootstrap": bootstrap_observation,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    raise SystemExit(main())
