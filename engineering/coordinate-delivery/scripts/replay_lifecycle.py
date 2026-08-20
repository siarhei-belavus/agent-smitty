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


def _record_structure_error(state: dict[str, Any]) -> str | None:
    checkpoint = state.get("checkpoint")
    requests = state.get("requests", [])
    responses = state.get("responses", [])
    feedback = state.get("feedback", [])
    proposals = state.get("review_proposals", [])
    evidence = state.get("evidence", {})
    runtime_evidence = (state.get("runtime") or {}).get("evidence")

    ticket = state.get("ticket", {})
    if not {"state", "routing", "assignee"}.issubset(ticket):
        return "invalid-durable-record-structure"
    if checkpoint and (
        not checkpoint.get("id")
        or not checkpoint.get("next_step")
        or not isinstance(checkpoint.get("heads"), dict)
    ):
        return "invalid-durable-record-structure"
    if any(
        not request.get("id")
        or not request.get("checkpoint_id")
        or not request.get("kind")
        or request.get("status") not in {"active", "completed", "superseded"}
        or (request.get("status") == "completed" and not request.get("response_id"))
        for request in requests
    ):
        return "invalid-durable-record-structure"
    if any(
        not response.get("id")
        or not response.get("request_id")
        or not isinstance(response.get("body"), str)
        or not response["body"].strip()
        for response in responses
    ):
        return "invalid-durable-record-structure"
    if any(
        not item.get("id")
        or not item.get("status")
        or (
            item.get("status") == "actionable"
            and (
                item.get("review_round") != "completed"
                or not isinstance(item.get("repositories"), list)
                or not item["repositories"]
            )
        )
        for item in feedback
    ):
        return "invalid-durable-record-structure"
    if any(
        not proposal.get("id")
        or not proposal.get("repository")
        or not proposal.get("head")
        for proposal in proposals
    ):
        return "invalid-durable-record-structure"
    if any(
        not item.get("repository")
        or not item.get("head")
        or not item.get("validation_id")
        or not item.get("standards_id")
        for item in evidence.get("repository", [])
    ):
        return "invalid-durable-record-structure"
    if any(
        not item.get("id")
        or not isinstance(item.get("heads"), dict)
        or not item["heads"]
        for item in evidence.get("cross_repository", [])
    ):
        return "invalid-durable-record-structure"
    bundle = evidence.get("bundle_spec")
    if bundle and (
        not bundle.get("id") or not isinstance(bundle.get("heads"), dict)
    ):
        return "invalid-durable-record-structure"
    if any(
        not reconciliation.get("response_id")
        or not reconciliation.get("disposition")
        for reconciliation in state.get("reconciliations", [])
    ):
        return "invalid-durable-record-structure"

    record_ids: list[str] = []
    if checkpoint and checkpoint.get("id"):
        record_ids.append(checkpoint["id"])
    for records in (requests, responses, feedback, proposals):
        record_ids.extend(item["id"] for item in records if item.get("id"))
    for item in evidence.get("repository", []):
        record_ids.extend((item.get("validation_id"), item.get("standards_id")))
    record_ids.extend(
        item["id"] for item in evidence.get("cross_repository", []) if item.get("id")
    )
    if bundle and bundle.get("id"):
        record_ids.append(bundle["id"])
    if runtime_evidence and runtime_evidence.get("id"):
        record_ids.append(runtime_evidence["id"])
    record_ids = [record_id for record_id in record_ids if record_id]
    if len(record_ids) != len(set(record_ids)):
        return "duplicate-durable-record-id"

    response_ids = {response["id"] for response in responses}
    reconciliations = state.get("reconciliations", [])
    reconciliation_ids = [item.get("response_id") for item in reconciliations]
    if len(reconciliation_ids) != len(set(reconciliation_ids)):
        return "invalid-response-request-chain"
    requests_by_id = {request["id"]: request for request in requests}
    responses_by_id = {response["id"]: response for response in responses}

    for response in responses:
        request = requests_by_id.get(response.get("request_id"))
        if not request or request.get("response_id") != response.get("id"):
            return "invalid-response-request-chain"
    for request in requests:
        response_id = request.get("response_id")
        if response_id:
            response = responses_by_id.get(response_id)
            if not response or response.get("request_id") != request.get("id"):
                return "invalid-response-request-chain"
        if checkpoint and request.get("checkpoint_id") != checkpoint.get("id"):
            return "invalid-response-request-chain"
    if response_ids - set(reconciliation_ids):
        return "invalid-response-request-chain"
    if set(reconciliation_ids) - response_ids:
        return "invalid-response-request-chain"
    return None


def _runtime_termination_proven(
    runtime: dict[str, Any] | None, checkpoint: dict[str, Any] | None
) -> bool:
    if not runtime or runtime.get("status") != "terminated" or not checkpoint:
        return False
    evidence = runtime.get("evidence")
    return bool(
        isinstance(evidence, dict)
        and evidence.get("id")
        and evidence.get("provider_ref")
        and evidence.get("outcome") == "terminated"
        and evidence.get("activation_id") == runtime.get("activation_id")
        and evidence.get("checkpoint_id") == checkpoint.get("id")
    )


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
        stale = (
            item["repository"] in affected
            or current_heads.get(item["repository"]) != item.get("head")
        )
        target = invalidated if stale else preserved
        target.update((item["validation_id"], item["standards_id"]))
    for item in evidence.get("cross_repository", []):
        bound_heads = item.get("heads", {})
        stale = affected.intersection(bound_heads) or any(
            current_heads.get(repository) != head
            for repository, head in bound_heads.items()
        )
        target = invalidated if stale else preserved
        target.add(item["id"])
    bundle = evidence.get("bundle_spec")
    if bundle:
        bound_heads = bundle.get("heads", {})
        stale = bool(affected.intersection(bound_heads)) or bound_heads != current_heads
        target = invalidated if stale else preserved
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
    structure_error = _record_structure_error(state)
    if structure_error:
        result["boundary_reason"] = structure_error
        return result
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
    if (
        checkpoint
        and runtime
        and runtime.get("status") == "terminated"
        and not _runtime_termination_proven(runtime, checkpoint)
    ):
        result["boundary_reason"] = "runtime-termination-evidence-invalid"
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
    runtime_terminated = _runtime_termination_proven(runtime, checkpoint)
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
