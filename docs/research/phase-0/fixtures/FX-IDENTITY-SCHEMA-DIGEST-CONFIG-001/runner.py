#!/usr/bin/env python3
"""Evidence-only identity, projection, stale-write, and digest fixture.

This runner deliberately does not implement a Geness product schema or controller.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sqlite3
import subprocess
import tempfile
from pathlib import Path
from typing import Any


FIXTURE_ID = "FX-IDENTITY-SCHEMA-DIGEST-CONFIG-001"
ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input" / "fixture.json"
SAFE_FRONTMATTER_STRING = re.compile(r"^[A-Za-z0-9_.\-/]+$")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def raw_digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.startswith(("[", "{")) or value.startswith('"'):
        return json.loads(value)
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    lines = markdown.split("\n")
    if not lines or lines[0] != "---":
        raise ValueError("frontmatter must start with ---")
    try:
        closing = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("frontmatter closing delimiter is missing") from error

    frontmatter: dict[str, Any] = {}
    for line in lines[1:closing]:
        if not line.strip():
            continue
        key, separator, raw = line.partition(":")
        if not separator or not key.strip():
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        frontmatter[key.strip()] = parse_scalar(raw)
    return frontmatter, "\n".join(lines[closing + 1 :])


def render_frontmatter(frontmatter: dict[str, Any], body: str) -> str:
    lines = ["---"]
    for key in sorted(frontmatter):
        value = json.dumps(
            frontmatter[key],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append(body)
    return "\n".join(lines)


def run_git(arguments: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def git_identity_probe() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="geness-identity-") as temporary:
        root = Path(temporary)
        source = root / "source"
        clone = root / "clone"
        renamed = root / "renamed"
        fork = root / "fork"
        worktree = root / "worktree"

        source.mkdir()
        commands: list[tuple[list[str], Path]] = [
            (["init", "--quiet"], source),
            (["config", "user.name", "Geness Fixture"], source),
            (["config", "user.email", "fixture@example.invalid"], source),
        ]
        for arguments, cwd in commands:
            result = run_git(arguments, cwd)
            if result.returncode != 0:
                raise AssertionError(f"git command failed: {arguments}: {result.stderr}")
        (source / "README.md").write_text("fixture\n", encoding="utf-8")
        for arguments in (["add", "README.md"], ["commit", "--quiet", "-m", "fixture"]):
            result = run_git(arguments, source)
            if result.returncode != 0:
                raise AssertionError(f"git command failed: {arguments}: {result.stderr}")

        result = run_git(["clone", "--quiet", str(source), str(clone)], root)
        if result.returncode != 0:
            raise AssertionError(f"git clone failed: {result.stderr}")
        clone_head = run_git(["rev-parse", "HEAD"], clone)
        if clone_head.returncode != 0:
            raise AssertionError(f"clone HEAD probe failed: {clone_head.stderr}")

        clone.rename(renamed)
        renamed_head = run_git(["rev-parse", "HEAD"], renamed)
        if renamed_head.returncode != 0:
            raise AssertionError(f"renamed repository probe failed: {renamed_head.stderr}")

        result = run_git(
            ["worktree", "add", "--quiet", "-b", "fixture-worktree", str(worktree)],
            renamed,
        )
        if result.returncode != 0:
            raise AssertionError(f"git worktree failed: {result.stderr}")
        worktree_head = run_git(["rev-parse", "HEAD"], worktree)
        if worktree_head.returncode != 0:
            raise AssertionError(f"worktree HEAD probe failed: {worktree_head.stderr}")
        common_source = run_git(["rev-parse", "--path-format=absolute", "--git-common-dir"], renamed)
        common_worktree = run_git(["rev-parse", "--path-format=absolute", "--git-common-dir"], worktree)
        if common_source.returncode != 0 or common_worktree.returncode != 0:
            raise AssertionError("git common-dir probe failed")

        result = run_git(["clone", "--quiet", str(source), str(fork)], root)
        if result.returncode != 0:
            raise AssertionError(f"local fork clone failed: {result.stderr}")
        result = run_git(
            ["remote", "set-url", "origin", "https://example.invalid/geness/fork.git"],
            fork,
        )
        if result.returncode != 0:
            raise AssertionError(f"fork remote update failed: {result.stderr}")
        clone_remote = run_git(["remote", "get-url", "origin"], renamed)
        fork_remote = run_git(["remote", "get-url", "origin"], fork)
        if clone_remote.returncode != 0 or fork_remote.returncode != 0:
            raise AssertionError("remote URL probe failed")

        return {
            "local_git_commands_passed": True,
            "clone_and_renamed_head_equal": clone_head.stdout.strip() == renamed_head.stdout.strip(),
            "worktree_head_equal": clone_head.stdout.strip() == worktree_head.stdout.strip(),
            "worktree_shares_git_common_dir": common_source.stdout.strip() == common_worktree.stdout.strip(),
            "fork_remote_is_distinct": clone_remote.stdout.strip() != fork_remote.stdout.strip(),
            "network": "disabled",
        }


def identity_probe(cases: dict[str, Any]) -> tuple[dict[str, Any], list[bool]]:
    source = cases["source"]
    observations: list[dict[str, Any]] = []
    assertions: list[bool] = []
    for case in cases["variants"]:
        project_relation = "SHARED" if case["project_id"] == source["project_id"] else "DETACHED"
        workspace_relation = "SHARED" if case["workspace_id"] == source["workspace_id"] else "DISTINCT"
        assertions.extend(
            [
                project_relation == case["expected_project_relation"],
                workspace_relation == case["expected_workspace_relation"],
            ]
        )
        if case["id"] in {"fork", "same-name-repository"}:
            assertions.append(case["explicit_detach"] is True)
        observations.append(
            {
                "id": case["id"],
                "project_relation": project_relation,
                "workspace_relation": workspace_relation,
                "explicit_detach": case["explicit_detach"],
            }
        )
    return {"relations": observations, "git_probe": git_identity_probe()}, assertions


def projection_round_trip(markdown: str) -> tuple[dict[str, Any], list[bool]]:
    frontmatter, body = parse_frontmatter(markdown)
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE task_projection (
            task_id TEXT PRIMARY KEY,
            contract_revision INTEGER NOT NULL,
            contract_digest TEXT NOT NULL,
            frontmatter_json TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )
    connection.execute(
        "INSERT INTO task_projection VALUES (?, ?, ?, ?, ?)",
        (
            frontmatter["task_id"],
            frontmatter["contract_revision"],
            frontmatter["contract_digest"],
            json.dumps(frontmatter, ensure_ascii=False, sort_keys=True),
            body,
        ),
    )
    row = connection.execute(
        "SELECT task_id, contract_revision, contract_digest, frontmatter_json, body "
        "FROM task_projection"
    ).fetchone()
    if row is None:
        raise AssertionError("projection row was not stored")
    restored_frontmatter = json.loads(row[3])
    restored_markdown = render_frontmatter(restored_frontmatter, row[4])
    reparsed_frontmatter, reparsed_body = parse_frontmatter(restored_markdown)
    connection.close()
    assertions = [
        reparsed_frontmatter == frontmatter,
        reparsed_body == body,
        row[0] == frontmatter["task_id"] and row[1] == frontmatter["contract_revision"],
    ]
    return {
        "semantic_fields_equal": reparsed_frontmatter == frontmatter,
        "body_equal": reparsed_body == body,
        "row_identity": {"task_id": row[0], "contract_revision": row[1]},
        "projection_rows": 1,
    }, assertions


def stale_write_probe(case: dict[str, Any]) -> tuple[dict[str, Any], list[bool]]:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE revision_state (task_id TEXT PRIMARY KEY, revision INTEGER, digest TEXT)"
    )
    connection.execute(
        "INSERT INTO revision_state VALUES (?, ?, ?)",
        (case["task_id"], case["initial_revision"], case["initial_digest"]),
    )

    def write(expected_revision: int, expected_digest: str, next_revision: int, next_digest: str) -> dict[str, Any]:
        current = connection.execute(
            "SELECT revision, digest FROM revision_state WHERE task_id = ?",
            (case["task_id"],),
        ).fetchone()
        if current is None:
            raise AssertionError("revision state is missing")
        if current[0] != expected_revision or current[1] != expected_digest:
            return {"decision": "DENIED", "reason": "stale_revision", "current_revision": current[0]}
        connection.execute(
            "UPDATE revision_state SET revision = ?, digest = ? WHERE task_id = ?",
            (next_revision, next_digest, case["task_id"]),
        )
        connection.commit()
        return {"decision": "ALLOWED", "revision": next_revision}

    accepted = write(
        case["initial_revision"],
        case["initial_digest"],
        case["accepted_revision"],
        case["accepted_digest"],
    )
    before_stale = connection.execute(
        "SELECT revision, digest FROM revision_state WHERE task_id = ?",
        (case["task_id"],),
    ).fetchone()
    stale = write(
        case["stale_expected_revision"],
        case["stale_expected_digest"],
        case["stale_attempt_revision"],
        case["stale_attempt_digest"],
    )
    after_stale = connection.execute(
        "SELECT revision, digest FROM revision_state WHERE task_id = ?",
        (case["task_id"],),
    ).fetchone()
    connection.close()
    unchanged = before_stale == after_stale
    assertions = [
        accepted["decision"] == "ALLOWED",
        stale == {"decision": "DENIED", "reason": "stale_revision", "current_revision": case["accepted_revision"]},
        unchanged,
    ]
    return {
        "accepted_write": accepted,
        "stale_write": stale,
        "state_unchanged_after_stale_write": unchanged,
        "current_state": {"revision": after_stale[0], "digest": after_stale[1]},
    }, assertions


def digest_probe(cases: dict[str, Any]) -> tuple[dict[str, Any], list[bool]]:
    contract = cases["contract"]
    plan = cases["plan"]
    contract_base = digest(contract["base"])
    contract_reordered = digest(contract["reordered"])
    contract_changed = digest(contract["semantic_changed"])
    plan_base = digest(plan["base"])
    plan_reordered = digest(plan["reordered"])
    plan_changed = digest(plan["semantic_changed"])
    raw_base = raw_digest(contract["editorial_markdown"]["base"])
    raw_editorial = raw_digest(contract["editorial_markdown"]["variant"])
    assertions = [
        contract_base == contract_reordered,
        contract_base != contract_changed,
        plan_base == plan_reordered,
        plan_base != plan_changed,
        raw_base != raw_editorial,
        contract_base == contract["expected_base_digest"],
        plan_base == plan["expected_base_digest"],
        contract_base != contract_changed and plan_base != plan_changed,
    ]
    return {
        "algorithm": "fixture.canonical-json-v1",
        "contract": {
            "base": contract_base,
            "reordered": contract_reordered,
            "semantic_changed": contract_changed,
            "editorial_body_not_in_payload": contract_base,
        },
        "plan": {
            "base": plan_base,
            "reordered": plan_reordered,
            "semantic_changed": plan_changed,
        },
        "raw_markdown_candidate": {
            "base": raw_base,
            "editorial_variant": raw_editorial,
            "editorial_change_would_invalidate": raw_base != raw_editorial,
        },
        "invalidation_observation": {
            "editorial_change": "digest_unchanged_under_semantic_projection",
            "contract_semantic_change": "contract_and_downstream_plan_stale",
        },
    }, assertions


def config_probe(boundary: dict[str, Any]) -> tuple[dict[str, Any], list[bool]]:
    portable = set(boundary["portable_project_fields"]) | set(boundary["portable_task_fields"])
    machine = set(boundary["machine_state_fields"])
    forbidden = set(boundary["forbidden_portable_fields"])
    assertions = [
        portable.isdisjoint(machine),
        forbidden.isdisjoint(portable),
        boundary["separate_project_config"] is False,
        boundary["task_machine_json"] is False,
    ]
    return {
        "profile": boundary["expected_profile"],
        "portable_machine_field_overlap": sorted(portable & machine),
        "forbidden_portable_fields_present": sorted(portable & forbidden),
        "separate_project_config": boundary["separate_project_config"],
        "task_machine_json": boundary["task_machine_json"],
    }, assertions


def main() -> int:
    fixture_input = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    if fixture_input["fixture_schema"] != "fixture.identity-schema-digest-config.input.v1":
        raise AssertionError("unexpected fixture schema")

    observations: dict[str, Any] = {}
    assertions: list[bool] = []

    identity_observation, identity_assertions = identity_probe(fixture_input["identity_cases"])
    observations["identity"] = identity_observation
    assertions.extend(identity_assertions)

    projection_observation, projection_assertions = projection_round_trip(
        fixture_input["frontmatter_case"]["markdown"]
    )
    observations["frontmatter_db_round_trip"] = projection_observation
    assertions.extend(projection_assertions)

    stale_observation, stale_assertions = stale_write_probe(fixture_input["stale_write_case"])
    observations["stale_write"] = stale_observation
    assertions.extend(stale_assertions)

    digest_observation, digest_assertions = digest_probe(fixture_input["digest_cases"])
    observations["digest"] = digest_observation
    assertions.extend(digest_assertions)

    config_observation, config_assertions = config_probe(fixture_input["config_boundary"])
    observations["config_boundary"] = config_observation
    assertions.extend(config_assertions)

    result = {
        "fixture_id": FIXTURE_ID,
        "fixture_schema": fixture_input["fixture_schema"],
        "network": "disabled",
        "external_writes": False,
        "assertions_passed": sum(assertions),
        "assertions_total": len(assertions),
        "all_assertions_pass": all(assertions),
        "observations": observations,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    raise SystemExit(main())
