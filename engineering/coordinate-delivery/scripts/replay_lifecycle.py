#!/usr/bin/env python3
"""Replay normalized durable Coordinator state through the Resume Gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _base_result() -> dict[str, Any]:
    return {
        "result": "human-boundary",
        "source": None,
        "disposition": None,
        "claim": "none",
        "routing": "unassigned-ready-for-human",
        "checkpoint_id": None,
        "active_request_id": None,
        "resumption_record_id": None,
        "attempt_id": None,
        "attempt_kind": None,
        "implementation_repositories": [],
        "event_order": [],
        "evidence": {"invalidate": [], "preserve": []},
        "review_proposals": {"reuse": [], "create": []},
        "boundary_reason": None,
        "request_actions": [],
    }


def _evidence_disposition(state: dict[str, Any]) -> dict[str, list[str]]:
    checkpoint_heads = (state.get("checkpoint") or {}).get("heads", {})
    current_heads = state.get("heads", {})
    affected = {
        repository
        for repository in set(checkpoint_heads) | set(current_heads)
        if checkpoint_heads.get(repository) != current_heads.get(repository)
    }
    for feedback in state.get("feedback", []):
        if feedback.get("status") == "actionable":
            affected.update(feedback.get("repositories", []))

    invalidated: set[str] = set()
    preserved: set[str] = set()
    evidence = state.get("evidence", {})
    for item in evidence.get("repository", []):
        target = invalidated if item["repository"] in affected else preserved
        target.update((item["validation_id"], item["standards_id"]))
    for item in evidence.get("cross_repository", []):
        target = invalidated if affected.intersection(item.get("heads", {})) else preserved
        target.add(item["id"])
    bundle = evidence.get("bundle_spec")
    if bundle:
        target = invalidated if affected.intersection(bundle.get("heads", {})) else preserved
        target.add(bundle["id"])
    return {"invalidate": sorted(invalidated), "preserve": sorted(preserved)}


def _start_attempt(
    result: dict[str, Any],
    state: dict[str, Any],
    *,
    source: str,
    disposition: str,
    token: str,
) -> dict[str, Any]:
    checkpoint = state.get("checkpoint")
    if checkpoint:
        record_id = f"resumption:{checkpoint['id']}:{token}"
        attempt_id = f"attempt:{checkpoint['id']}:{token}"
        event_order = [record_id, attempt_id]
    else:
        record_id = None
        attempt_id = "attempt:initial"
        event_order = [attempt_id]
    result.update(
        {
            "result": "start" if source == "initial" else "resume",
            "source": source,
            "disposition": disposition,
            "claim": "acquire",
            "routing": "claimed-ready-for-agent",
            "resumption_record_id": record_id,
            "attempt_id": attempt_id,
            "attempt_kind": (
                "handoff-only"
                if (state.get("handoff") or {}).get("status") == "incomplete"
                and not state.get("required_changes", [])
                else "normal"
            ),
            "implementation_repositories": sorted(state.get("required_changes", [])),
            "event_order": event_order,
            "evidence": _evidence_disposition(state),
            "review_proposals": {
                "reuse": sorted(
                    proposal["id"] for proposal in state.get("review_proposals", [])
                ),
                "create": [],
            },
            "boundary_reason": None,
        }
    )
    return result


def replay(state: dict[str, Any]) -> dict[str, Any]:
    result = _base_result()
    checkpoint = state.get("checkpoint")
    if checkpoint:
        result["checkpoint_id"] = checkpoint["id"]
    requests = state.get("requests", [])
    responses = {item["id"]: item for item in state.get("responses", [])}
    reconciliations = {
        item["response_id"]: item for item in state.get("reconciliations", [])
    }

    active = [request for request in requests if request.get("status") == "active"]
    if len(active) > 1:
        result["boundary_reason"] = "contradictory-active-requests"
        return result
    if len(active) == 1:
        request = active[0]
        response_id = request.get("response_id")
        reconciliation = reconciliations.get(response_id)
        if (
            request.get("kind") == "planned-verification"
            and response_id in responses
            and reconciliation
            and reconciliation.get("disposition") == "indeterminate"
        ):
            successor_id = f"{request['id']}:indeterminacy"
            result.update(
                {
                    "active_request_id": successor_id,
                    "boundary_reason": "validation-indeterminacy",
                    "request_actions": [
                        f"supersede:{request['id']}",
                        f"create:{successor_id}",
                    ],
                }
            )
            return result
        result.update(
            {
                "active_request_id": request["id"],
                "boundary_reason": "awaiting-human-response",
            }
        )
        return result
    if requests and all(request.get("status") == "superseded" for request in requests):
        result["boundary_reason"] = "incomplete-request-chain"
        return result

    local_only = [
        item
        for item in state.get("local_work", [])
        if item.get("status") == "dirty" and item.get("provenance") != "reconciled"
    ]
    if local_only:
        request_id = f"request:{checkpoint['id']}:local-provenance" if checkpoint else None
        result.update(
            {
                "boundary_reason": "local-only-work-needs-human-reconciliation",
                "active_request_id": request_id,
                "request_actions": [f"create:{request_id}"] if request_id else [],
            }
        )
        return result

    runtime = state.get("runtime")
    if checkpoint and runtime and runtime.get("status") == "indeterminate":
        request_id = f"request:{checkpoint['id']}:liveness"
        result.update(
            {
                "boundary_reason": "runtime-termination-not-proven",
                "active_request_id": request_id,
                "request_actions": [f"create:{request_id}"],
            }
        )
        return result

    completed = [
        request
        for request in requests
        if request.get("status") == "completed"
        and request.get("response_id") in responses
        and request.get("response_id") in reconciliations
        and checkpoint
        and request.get("checkpoint_id") == checkpoint.get("id")
    ]

    feedback = [
        item
        for item in state.get("feedback", [])
        if item.get("status") == "actionable"
        and item.get("review_round") == "completed"
    ]
    runtime_terminated = bool(runtime and runtime.get("status") == "terminated")
    sources = []
    if completed:
        sources.append("checkpoint-response")
    if checkpoint and feedback:
        sources.append("review-feedback")
    if checkpoint and runtime_terminated:
        sources.append("runtime-termination")

    if len(sources) > 1 or len(completed) > 1 or len(feedback) > 1:
        result["boundary_reason"] = "mixed-resume-sources"
        return result

    ticket = state.get("ticket", {})
    ticket_ready = (
        ticket.get("state") == "open"
        and ticket.get("routing") == "ready-for-agent"
        and ticket.get("assignee") is None
    )
    if not ticket_ready:
        result["boundary_reason"] = "ticket-not-unassigned-ready-for-agent"
        return result

    if sources == ["checkpoint-response"]:
        response_id = completed[0]["response_id"]
        reconciliation = reconciliations[response_id]
        disposition = reconciliation.get("disposition")
        if disposition == "replan":
            plan = reconciliation.get("resumption_plan", {})
            if plan.get("status") != "execution-ready":
                result["boundary_reason"] = "missing-execution-ready-resumption-plan"
                return result
        if disposition not in {"continue", "replan"}:
            result["boundary_reason"] = "unsupported-resumption-disposition"
            return result
        return _start_attempt(
            result,
            state,
            source="checkpoint-response",
            disposition=disposition,
            token=response_id,
        )

    if sources == ["review-feedback"]:
        return _start_attempt(
            result,
            state,
            source="review-feedback",
            disposition="continue",
            token=feedback[0]["id"],
        )

    if sources == ["runtime-termination"]:
        return _start_attempt(
            result,
            state,
            source="runtime-termination",
            disposition="continue",
            token=f"runtime:{runtime['activation_id']}",
        )

    lifecycle_artifacts = checkpoint or requests or state.get("feedback") or runtime
    if not lifecycle_artifacts:
        return _start_attempt(
            result,
            state,
            source="initial",
            disposition="new",
            token="initial",
        )

    result["boundary_reason"] = "incomplete-or-unsupported-lifecycle-state"
    return result


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: replay_lifecycle.py <fixture.json>", file=sys.stderr)
        return 2
    fixture = json.loads(Path(argv[1]).read_text())
    print(json.dumps(replay(fixture["state"]), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
