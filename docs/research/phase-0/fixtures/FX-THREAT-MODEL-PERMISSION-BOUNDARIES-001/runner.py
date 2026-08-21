#!/usr/bin/env python3
"""Disposable, product-independent threat/control boundary fixture."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path


FIXTURE_ID = "FX-THREAT-MODEL-PERMISSION-BOUNDARIES-001"
ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "fixture.json"


def is_within(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return False
    return True


def scope_allows(root: Path, allowed_scope: list[str], candidate: Path) -> bool:
    if not is_within(root, candidate):
        return False
    relative = candidate.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()
    return relative in allowed_scope


def permission_decision(action: str, actor: str, receipt_digest: str | None, current_digest: str) -> dict[str, str]:
    user_only = {
        "scope_expand",
        "external_write",
        "destructive_action",
        "security_boundary",
        "permission_escalation",
    }
    if action not in user_only:
        return {"decision": "ALLOW", "reason": "policy_allowed"}
    if actor != "user":
        return {"decision": "HOLD", "reason": "user_approval_required"}
    if receipt_digest != current_digest:
        return {"decision": "HOLD", "reason": "approval_digest_mismatch"}
    return {"decision": "ALLOW", "reason": "user_receipt"}


def execution_decision(submitted_digest: str, current_digest: str) -> dict[str, str]:
    if submitted_digest != current_digest:
        return {"decision": "HOLD", "reason": "stale_digest"}
    return {"decision": "ALLOW", "reason": "current_digest"}


def lease_decision(current_owner: str | None, requester: str, mode: str) -> dict[str, str]:
    if mode == "read":
        return {"decision": "ALLOW", "reason": "observer_read_only"}
    if current_owner is not None and current_owner != requester:
        return {"decision": "HOLD", "reason": "writer_lease_owned"}
    return {"decision": "ALLOW", "reason": "writer_lease_acquired"}


def capability_decision(capability: str, forbidden: list[str], scope_allowed: bool) -> dict[str, str]:
    if capability in forbidden:
        return {"decision": "HOLD", "reason": "capability_forbidden"}
    if capability == "approved_local_write" and not scope_allowed:
        return {"decision": "HOLD", "reason": "scope_not_allowed"}
    return {"decision": "ALLOW", "reason": "policy_allowed"}


def redact(text: str) -> str:
    patterns = (
        r"TEST_SECRET_REDACT_ME_[A-Z0-9_]+",
        r"(?i)(?:TOKEN|PASSWORD|API_KEY)=[^\s,;]+",
        r"(?i)Bearer\s+[A-Za-z0-9._-]+",
    )
    result = text
    for pattern in patterns:
        result = re.sub(pattern, "[REDACTED]", result)
    return result


def completion_decision(
    *,
    behavior_bearing: bool,
    evidence_current: bool,
    acting_pass: bool,
    verifier: str,
    worker: str,
) -> dict[str, str]:
    if verifier == worker:
        return {"decision": "HOLD", "reason": "worker_self_verification"}
    if not evidence_current:
        return {"decision": "HOLD", "reason": "current_evidence_required"}
    if behavior_bearing and not acting_pass:
        return {"decision": "HOLD", "reason": "acting_evidence_required"}
    return {"decision": "ALLOW", "reason": "independent_current_evidence"}


def memory_query(status: str) -> list[str]:
    return ["LESSON-VERIFIED"] if status in {"verified", "enforced"} else []


def bootstrap_decision(status: str) -> dict[str, str]:
    if status == "corrupt":
        return {"decision": "HOLD", "reason": "rebuild_or_repair"}
    return {"decision": "CLEAR", "reason": "typed_memory_capability"}


def main() -> int:
    input_bytes = INPUT_PATH.read_bytes()
    data = json.loads(input_bytes)
    current_digest = data["current_digest"]
    allowed_scope = data["allowed_scope"]
    assertions: list[dict[str, object]] = []

    def check(assertion_id: str, expected: object, actual: object) -> None:
        assertions.append(
            {
                "id": assertion_id,
                "expected": expected,
                "actual": actual,
                "pass": expected == actual,
            }
        )

    with tempfile.TemporaryDirectory(prefix="geness-oq015-") as temp_dir:
        temp_root = Path(temp_dir)
        target_root = temp_root / "target"
        outside_root = temp_root / "outside"
        (target_root / "docs").mkdir(parents=True)
        outside_root.mkdir()
        (outside_root / "escape.txt").write_text("outside", encoding="utf-8")
        (target_root / "link").symlink_to(outside_root, target_is_directory=True)

        check("path.in_scope_file", True, scope_allows(target_root, allowed_scope, target_root / "docs/contract.md"))
        check("path.parent_escape", False, is_within(target_root, target_root / "../outside.txt"))
        check("path.symlink_escape", False, is_within(target_root, target_root / "link/escape.txt"))

    check(
        "approval.external_without_user",
        {"decision": "HOLD", "reason": "user_approval_required"},
        permission_decision("external_write", "worker", None, current_digest),
    )
    check(
        "approval.scope_with_matching_user_receipt",
        {"decision": "ALLOW", "reason": "user_receipt"},
        permission_decision("scope_expand", "user", current_digest, current_digest),
    )
    check(
        "approval.stale_user_receipt",
        {"decision": "HOLD", "reason": "approval_digest_mismatch"},
        permission_decision("destructive_action", "user", "sha256:old", current_digest),
    )
    check(
        "execution.stale_digest",
        {"decision": "HOLD", "reason": "stale_digest"},
        execution_decision("sha256:old", current_digest),
    )
    check(
        "lease.second_writer",
        {"decision": "HOLD", "reason": "writer_lease_owned"},
        lease_decision("worker-1", "worker-2", "write"),
    )
    check(
        "lease.observer_read",
        {"decision": "ALLOW", "reason": "observer_read_only"},
        lease_decision("worker-1", "worker-2", "read"),
    )
    check(
        "capability.danger_full_access",
        {"decision": "HOLD", "reason": "capability_forbidden"},
        capability_decision("danger_full_access", data["forbidden_capabilities"], False),
    )
    check(
        "capability.approved_in_scope_local_write",
        {"decision": "ALLOW", "reason": "policy_allowed"},
        capability_decision("approved_local_write", data["forbidden_capabilities"], True),
    )
    check(
        "authority.untrusted_instruction",
        {"decision": "HOLD", "reason": "user_approval_required"},
        permission_decision("external_write", "repository_text", None, current_digest),
    )

    probe = "stdout TEST_SECRET_REDACT_ME_123 TOKEN=synthetic-token"
    redacted = redact(probe)
    check("secret.redacted_output", True, "[REDACTED]" in redacted and "TEST_SECRET_REDACT_ME_123" not in redacted)
    check(
        "verification.worker_self_check",
        {"decision": "HOLD", "reason": "worker_self_verification"},
        completion_decision(
            behavior_bearing=True,
            evidence_current=True,
            acting_pass=True,
            verifier="worker-1",
            worker="worker-1",
        ),
    )
    check(
        "verification.behavior_without_acting",
        {"decision": "HOLD", "reason": "acting_evidence_required"},
        completion_decision(
            behavior_bearing=True,
            evidence_current=True,
            acting_pass=False,
            verifier="verifier-1",
            worker="worker-1",
        ),
    )
    check("memory.candidate_hidden", [], memory_query("candidate"))
    check(
        "memory.corrupt_is_hold",
        {"decision": "HOLD", "reason": "rebuild_or_repair"},
        bootstrap_decision("corrupt"),
    )

    result = {
        "fixture_id": FIXTURE_ID,
        "fixture_schema_version": 1,
        "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "assertion_count": len(assertions),
        "passed": sum(1 for item in assertions if item["pass"]),
        "all_assertions_pass": all(item["pass"] for item in assertions),
        "assertions": assertions,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if result["all_assertions_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
