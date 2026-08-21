#!/usr/bin/env python3
"""Fixture-local command surface and host-profile policy model."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


SCHEMA = "fixture.oq012-oq014.surface-result.v1"
ROUTE_INTENTS = ("setup", "status", "resume", "brief", "contract", "plan", "impl", "verify", "done")


def stable_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def result(status: str, request: dict[str, Any], **fields: Any) -> dict[str, Any]:
    value = {
        "schema": SCHEMA,
        "kind": "domain_result",
        "status": status,
        "request_digest": stable_digest(request),
    }
    value.update(fields)
    return value


def route(request: dict[str, Any]) -> dict[str, Any]:
    raw = str(request.get("input", "")).strip()
    normalized = raw.lower()

    host_aliases = {
        "/geness:status": "status",
        "/geness:resume": "resume",
        "$geness status": "status",
        "$geness resume": "resume",
    }
    if normalized in host_aliases:
        intent = host_aliases[normalized]
        return result(
            "ROUTED",
            request,
            intent=intent,
            canonical_command=f"gee {intent}",
            source="host_alias",
        )

    if normalized.startswith("gee "):
        parts = normalized.split()
        command = parts[1] if len(parts) > 1 else ""
        aliases = {"config": "config", "status": "status", "resume": "resume"}
        if command in aliases or command in ROUTE_INTENTS:
            intent = aliases.get(command, command)
            if intent == "config":
                return result("ROUTED", request, intent="config", canonical_command="gee config", source="explicit")
            return result(
                "ROUTED",
                request,
                intent=intent,
                canonical_command=f"gee {intent}",
                source="explicit",
            )
        return result(
            "HOLD",
            request,
            code="ROUTE_CHOICE_REQUIRED",
            reason="unknown explicit command",
            candidates=list(ROUTE_INTENTS),
        )

    keywords = {
        "setup": ("initialize", "initialise", "setup", "ready"),
        "status": ("status", "progress", "current state", "where are we"),
        "resume": ("resume", "continue", "checkpoint", "blocked"),
        "brief": ("vague", "clarify", "questions", "brief"),
        "contract": ("contract", "acceptance criteria", "specification"),
        "plan": ("plan", "preflight"),
        "impl": ("implement", "implementation", "approved plan"),
        "verify": ("verify", "evidence", "test the implementation"),
        "done": ("finish", "complete", "done", "after verification"),
    }
    scores = {
        intent: sum(1 for keyword in terms if keyword in normalized)
        for intent, terms in keywords.items()
    }
    best_score = max(scores.values(), default=0)
    winners = [intent for intent, score in scores.items() if score == best_score and score > 0]
    if len(winners) != 1:
        return result(
            "HOLD",
            request,
            code="ROUTE_CHOICE_REQUIRED",
            reason="description is ambiguous or does not identify a Geness intent",
            candidates=winners or list(ROUTE_INTENTS),
            source="description",
        )
    intent = winners[0]
    return result(
        "ROUTED",
        request,
        intent=intent,
        canonical_command=f"gee {intent}",
        source="description",
    )


def setup(request: dict[str, Any]) -> dict[str, Any]:
    profile = request.get("profile", "auto")
    codex_ready = bool(request.get("codex_ready"))
    claude_ready = bool(request.get("claude_ready"))
    active_task = bool(request.get("active_task"))

    if not claude_ready:
        return result("SETUP_ATTENTION", request, code="CLAUDE_REQUIRED", required_action="enable_claude_host")
    if profile == "claude-only":
        return result("SETUP_READY", request, selected_profile="claude-only", fallback=False)
    if profile == "cross-model":
        if codex_ready:
            return result("SETUP_READY", request, selected_profile="cross-model", fallback=False)
        return result("SETUP_ATTENTION", request, code="CODEX_REQUIRED", required_action="enable_codex_host")
    if profile == "auto":
        if codex_ready:
            return result("SETUP_READY", request, selected_profile="cross-model", fallback=False)
        if active_task:
            return result(
                "SETUP_ATTENTION",
                request,
                code="PROFILE_CHANGE_REQUIRES_REOPEN",
                required_action="reopen_or_resume_with_user_approval",
            )
        return result(
            "SETUP_READY",
            request,
            selected_profile="claude-only",
            fallback=True,
            fallback_reason="codex_unavailable_new_task",
        )
    return result("SETUP_ATTENTION", request, code="UNKNOWN_PROFILE", required_action="choose_supported_profile")


def status(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("setup_state") != "SETUP_READY":
        return result("HOLD", request, code="SETUP_REQUIRED", required_action="gee setup")
    return result(
        "STATUS_READY",
        request,
        task_state=request.get("task_state", "UNKNOWN"),
        next_action=request.get("next_action", "none"),
        read_only=True,
    )


def resume(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("task_state") not in {"PAUSED", "BLOCKED", "REOPENED"}:
        return result("HOLD", request, code="RESUME_NOT_AVAILABLE", required_action="inspect_task_status")
    if not request.get("digest_current", False):
        return result("HOLD", request, code="STALE_DIGEST", required_action="reopen_contract")
    if request.get("writer_active", False):
        return result("HOLD", request, code="WRITER_ACTIVE", required_action="observe_or_takeover_explicitly")
    return result(
        "RESUME_READY",
        request,
        next_action=request.get("checkpoint", "reconcile_checkpoint"),
        lease_action="takeover_only_after_explicit_validation",
    )


def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    action = request.get("action")
    if action == "route":
        return route(request)
    if action == "setup":
        return setup(request)
    if action == "status":
        return status(request)
    if action == "resume":
        return resume(request)
    return result("HOLD", request, code="UNKNOWN_ACTION", required_action="choose_fixture_action")
