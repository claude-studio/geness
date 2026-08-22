#!/usr/bin/env python3
"""Disposable two-process lease liveness and takeover fixture.

This runner is Phase 0 evidence only. It is not a production Controller, daemon,
lease implementation, or schema contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable

try:
    import fcntl
except ImportError:  # pragma: no cover - this fixture is POSIX-scoped
    fcntl = None  # type: ignore[assignment]


FIXTURE_ID = "FX-LEASE-LIVENESS-TAKEOVER-001"
FIXTURE_DIR = Path(__file__).resolve().parent
INPUT_PATH = FIXTURE_DIR / "input" / "fixture.json"
ROLE_OWNER = {"writer": "writer-A", "observer": "observer-B"}


def load_input() -> dict[str, Any]:
    return json.loads(INPUT_PATH.read_text(encoding="utf-8"))


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    fd, temp_name = tempfile.mkstemp(
        prefix=".lease-state-", dir=str(path.parent), text=True
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, sort_keys=True, separators=(",", ":"))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


class LeaseStore:
    def __init__(self, state_path: Path) -> None:
        if fcntl is None:
            raise RuntimeError("POSIX fcntl is required by this disposable fixture")
        self.state_path = state_path
        self.lock_path = state_path.with_suffix(".lock")

    @contextmanager
    def lock(self, shared: bool):
        self.lock_path.touch(mode=0o600, exist_ok=True)
        with self.lock_path.open("r+", encoding="utf-8") as lock_stream:
            mode = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
            fcntl.flock(lock_stream.fileno(), mode)
            try:
                yield
            finally:
                fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)

    def read(self) -> dict[str, Any]:
        with self.lock(shared=True):
            return json.loads(self.state_path.read_text(encoding="utf-8"))

    def mutate(self, operation: Callable[[dict[str, Any]], dict[str, Any]]) -> dict[str, Any]:
        with self.lock(shared=False):
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            result = operation(state)
            atomic_write(self.state_path, state)
            return result


def lease_summary(state: dict[str, Any], logical_time: int) -> dict[str, Any]:
    lease = state["lease"]
    if lease is None:
        return {
            "decision": "OBSERVED",
            "lease_active": False,
            "owner": None,
            "generation": state["generation"],
        }
    heartbeat_age = logical_time - lease["last_heartbeat"]
    return {
        "decision": "OBSERVED",
        "lease_active": logical_time <= lease["grace_deadline"],
        "owner": lease["owner"],
        "generation": lease["generation"],
        "last_heartbeat": lease["last_heartbeat"],
        "heartbeat_age": heartbeat_age,
        "heartbeat_due": heartbeat_age >= state["config"]["heartbeat_interval"],
        "grace_deadline": lease["grace_deadline"],
    }


def append_event(state: dict[str, Any], *, actor: str, operation: str, logical_time: int, result: dict[str, Any]) -> None:
    state["events"].append(
        {
            "actor": actor,
            "logical_time": logical_time,
            "operation": operation,
            "result": result,
        }
    )


def acquire(state: dict[str, Any], actor: str, logical_time: int) -> dict[str, Any]:
    current = state["lease"]
    grace_period = state["config"]["grace_period"]
    if current is None:
        generation = state["generation"] + 1
        state["generation"] = generation
        state["lease"] = {
            "owner": actor,
            "generation": generation,
            "acquired_at": logical_time,
            "last_heartbeat": logical_time,
            "grace_deadline": logical_time + grace_period,
        }
        result = {
            "decision": "ALLOWED",
            "reason": "initial_claim",
            "owner": actor,
            "generation": generation,
            "takeover": False,
        }
    elif current["owner"] == actor:
        result = {
            "decision": "DENIED",
            "reason": "already_owner",
            "owner": actor,
            "generation": current["generation"],
            "takeover": False,
        }
    elif logical_time <= current["grace_deadline"]:
        result = {
            "decision": "DENIED",
            "reason": "grace_active",
            "owner": current["owner"],
            "generation": current["generation"],
            "heartbeat_age": logical_time - current["last_heartbeat"],
            "grace_deadline": current["grace_deadline"],
            "takeover": False,
        }
    else:
        previous_owner = current["owner"]
        generation = state["generation"] + 1
        state["generation"] = generation
        state["lease"] = {
            "owner": actor,
            "generation": generation,
            "acquired_at": logical_time,
            "last_heartbeat": logical_time,
            "grace_deadline": logical_time + grace_period,
            "previous_owner": previous_owner,
        }
        result = {
            "decision": "ALLOWED",
            "reason": "stale_takeover",
            "owner": actor,
            "previous_owner": previous_owner,
            "generation": generation,
            "takeover": True,
        }
    append_event(state, actor=actor, operation="acquire", logical_time=logical_time, result=result)
    return result


def heartbeat(state: dict[str, Any], actor: str, logical_time: int) -> dict[str, Any]:
    current = state["lease"]
    if current is None:
        result = {"decision": "DENIED", "reason": "no_active_lease", "owner": actor}
    elif current["owner"] != actor:
        result = {
            "decision": "DENIED",
            "reason": "not_owner",
            "owner": current["owner"],
            "generation": current["generation"],
        }
    elif logical_time < current["last_heartbeat"]:
        result = {
            "decision": "DENIED",
            "reason": "clock_regression",
            "owner": actor,
            "generation": current["generation"],
        }
    elif logical_time > current["grace_deadline"]:
        result = {
            "decision": "DENIED",
            "reason": "lease_expired",
            "owner": actor,
            "generation": current["generation"],
        }
    else:
        current["last_heartbeat"] = logical_time
        current["grace_deadline"] = logical_time + state["config"]["grace_period"]
        result = {
            "decision": "ALLOWED",
            "reason": "heartbeat_recorded",
            "owner": actor,
            "generation": current["generation"],
            "last_heartbeat": current["last_heartbeat"],
            "grace_deadline": current["grace_deadline"],
        }
    append_event(state, actor=actor, operation="heartbeat", logical_time=logical_time, result=result)
    return result


def child_main(role: str, state_path: Path) -> int:
    store = LeaseStore(state_path)
    actor = ROLE_OWNER[role]
    print(json.dumps({"ready": True, "role": role}, sort_keys=True), flush=True)
    for raw_line in sys.stdin:
        command = json.loads(raw_line)
        operation = command["operation"]
        logical_time = int(command.get("logical_time", 0))
        if operation == "acquire":
            response = store.mutate(lambda state: acquire(state, actor, logical_time))
        elif operation == "heartbeat":
            response = store.mutate(lambda state: heartbeat(state, actor, logical_time))
        elif operation == "observe":
            response = lease_summary(store.read(), logical_time)
        elif operation == "shutdown":
            response = {"decision": "SHUTDOWN", "role": role}
            print(json.dumps(response, sort_keys=True), flush=True)
            return 0
        elif operation == "interrupt":
            os.kill(os.getpid(), signal.SIGKILL)
            return 128 + signal.SIGKILL
        else:
            raise ValueError(f"unsupported operation: {operation}")
        print(json.dumps(response, sort_keys=True), flush=True)
    return 0


def start_child(role: str, state_path: Path):
    return subprocess.Popen(
        [sys.executable, "-u", str(Path(__file__).resolve()), "--role", role, "--state", str(state_path)],
        cwd=str(FIXTURE_DIR),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def read_response(process) -> dict[str, Any]:
    if process.stdout is None:
        raise RuntimeError("child stdout is unavailable")
    line = process.stdout.readline()
    if not line:
        stderr = process.stderr.read() if process.stderr is not None else ""
        raise RuntimeError(f"child exited without response: {stderr}")
    return json.loads(line)


def ask(process, operation: str, logical_time: int) -> dict[str, Any]:
    if process.poll() is not None:
        raise RuntimeError(f"child is not alive before {operation}: {process.returncode}")
    if process.stdin is None:
        raise RuntimeError("child stdin is unavailable")
    process.stdin.write(json.dumps({"operation": operation, "logical_time": logical_time}) + "\n")
    process.stdin.flush()
    return read_response(process)


def close_process(process) -> tuple[int, bool]:
    if process.stdin is not None and not process.stdin.closed:
        process.stdin.close()
    return_code = process.wait(timeout=3)
    stderr = process.stderr.read() if process.stderr is not None else ""
    return return_code, stderr == ""


def parent_main() -> int:
    fixture_input = load_input()
    config = fixture_input["config"]
    with tempfile.TemporaryDirectory(prefix="geness-oq003-") as temp_dir:
        temp_root = Path(temp_dir)
        state_path = temp_root / "lease-state.json"
        atomic_write(
            state_path,
            {
                "schema": "fixture.lease_state.v1",
                "project_id": fixture_input["project_id"],
                "task_id": fixture_input["task_id"],
                "config": config,
                "generation": 0,
                "lease": None,
                "events": [],
            },
        )
        writer = start_child("writer", state_path)
        observer = start_child("observer", state_path)
        writer_ready = read_response(writer)
        observer_ready = read_response(observer)
        timeline: dict[str, Any] = {}
        try:
            timeline["writer_initial_claim"] = ask(writer, "acquire", 0)
            timeline["observer_live_observation"] = ask(observer, "observe", 1)
            timeline["writer_heartbeat"] = ask(writer, "heartbeat", 2)
            timeline["observer_before_grace"] = ask(observer, "acquire", 3)
            timeline["observer_due_observation"] = ask(observer, "observe", 4)
            writer_alive_before_interrupt = writer.poll() is None
            if writer.stdin is None:
                raise RuntimeError("writer stdin is unavailable")
            writer.stdin.write(json.dumps({"operation": "interrupt", "logical_time": 4}) + "\n")
            writer.stdin.flush()
            writer.stdin.close()
            writer_exit = writer.wait(timeout=3)
            writer_stderr = writer.stderr.read() if writer.stderr is not None else ""
            timeline["observer_during_grace_after_interrupt"] = ask(observer, "acquire", 4)
            timeline["observer_at_grace_boundary"] = ask(observer, "acquire", 5)
            observer_alive_during_takeover = observer.poll() is None
            timeline["observer_after_grace_takeover"] = ask(observer, "acquire", 6)
            timeline["observer_new_owner_heartbeat"] = ask(observer, "heartbeat", 7)
            timeline["observer_final_observation"] = ask(observer, "observe", 8)
            observer_shutdown = ask(observer, "shutdown", 8)
            observer_exit, observer_stderr_empty = close_process(observer)
        finally:
            for process in (writer, observer):
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=3)
            if writer.stderr is not None and writer.poll() is not None:
                writer.stderr.close()
            if writer.stdout is not None:
                writer.stdout.close()
            if observer.stderr is not None and observer.poll() is not None:
                observer.stderr.close()
            if observer.stdout is not None:
                observer.stdout.close()

        final_state = LeaseStore(state_path).read()
        expected = fixture_input["expected"]
        checks = [
            ("two-child-processes-started", writer_ready == {"ready": True, "role": "writer"} and observer_ready == {"ready": True, "role": "observer"}),
            ("child-pids-are-distinct", writer.pid != observer.pid),
            ("writer-owns-initial-lease", timeline["writer_initial_claim"]["decision"] == "ALLOWED" and timeline["writer_initial_claim"]["owner"] == expected["writer_owner"]),
            ("observer-sees-fresh-heartbeat", timeline["observer_live_observation"]["owner"] == expected["writer_owner"] and not timeline["observer_live_observation"]["heartbeat_due"]),
            ("heartbeat-extends-grace-deadline", timeline["writer_heartbeat"]["decision"] == "ALLOWED" and timeline["writer_heartbeat"]["grace_deadline"] == expected["grace_deadline_after_writer_heartbeat"]),
            ("takeover-denied-before-grace", timeline["observer_before_grace"]["decision"] == expected["takeover_before_grace"] and timeline["observer_before_grace"]["reason"] == "grace_active"),
            ("writer-is-alive-before-interruption", writer_alive_before_interrupt),
            ("writer-interruption-terminates-child", writer_exit == expected["writer_interrupt_exit_status"] and writer_stderr == ""),
            ("takeover-denied-during-grace-after-interruption", timeline["observer_during_grace_after_interrupt"]["decision"] == expected["takeover_before_grace"] and timeline["observer_during_grace_after_interrupt"]["reason"] == "grace_active"),
            ("takeover-denied-at-grace-boundary", timeline["observer_at_grace_boundary"]["decision"] == expected["takeover_before_grace"] and timeline["observer_at_grace_boundary"]["reason"] == "grace_active" and timeline["observer_at_grace_boundary"]["grace_deadline"] == expected["grace_deadline_after_writer_heartbeat"]),
            ("observer-remains-alive-for-takeover", observer_alive_during_takeover),
            ("takeover-allowed-after-grace", timeline["observer_after_grace_takeover"]["decision"] == expected["takeover_after_grace"] and timeline["observer_after_grace_takeover"]["reason"] == "stale_takeover" and timeline["observer_after_grace_takeover"]["previous_owner"] == expected["writer_owner"]),
            ("new-owner-heartbeat-accepted", timeline["observer_new_owner_heartbeat"]["decision"] == "ALLOWED" and timeline["observer_new_owner_heartbeat"]["owner"] == expected["observer_owner"]),
            ("final-owner-is-observer", timeline["observer_final_observation"]["owner"] == expected["observer_owner"] and timeline["observer_final_observation"]["generation"] == 2),
            ("observer-shutdown-is-clean", observer_shutdown == {"decision": "SHUTDOWN", "role": "observer"} and observer_exit == 0 and observer_stderr_empty),
            ("state-event-count-is-deterministic", len(final_state["events"]) == 7),
            (
                "no-daemon-process-started",
                all(
                    "--role" in process.args and "--daemon" not in process.args
                    for process in (writer, observer)
                ),
            ),
        ]
        assertions = [
            {"name": name, "passed": passed, "detail": "observed" if passed else "unexpected observation"}
            for name, passed in checks
        ]
        result = {
            "fixture_id": FIXTURE_ID,
            "manifest_schema": "fixture.oq003.result.v1",
            "input_sha256": hashlib.sha256(INPUT_PATH.read_bytes()).hexdigest(),
            "runner_python": platform_version(),
            "network": "disabled",
            "external_writes": False,
            "daemon_started": False,
            "configuration": config,
            "processes": {
                "child_roles": ["writer", "observer"],
                "child_process_count": 2,
                "distinct_pids": writer.pid != observer.pid,
            },
            "timeline": {"writer_ready": writer_ready, "observer_ready": observer_ready, **timeline},
            "final_state": {
                "generation": final_state["generation"],
                "owner": final_state["lease"]["owner"],
                "last_heartbeat": final_state["lease"]["last_heartbeat"],
                "grace_deadline": final_state["lease"]["grace_deadline"],
                "event_count": len(final_state["events"]),
            },
            "assertions": assertions,
            "assertions_passed": sum(item["passed"] for item in assertions),
            "all_assertions_pass": all(item["passed"] for item in assertions),
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["all_assertions_pass"] else 1


def platform_version() -> str:
    return sys.version.split()[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", choices=sorted(ROLE_OWNER))
    parser.add_argument("--state", type=Path)
    args = parser.parse_args()
    if args.role is not None:
        if args.state is None:
            parser.error("--state is required with --role")
        return child_main(args.role, args.state)
    return parent_main()


if __name__ == "__main__":
    raise SystemExit(main())
