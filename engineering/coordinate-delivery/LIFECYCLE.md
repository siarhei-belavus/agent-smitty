# Durable Coordinator Lifecycle

This reference governs prior lifecycle state and every human boundary. Durable Work Tracker, Code Host, Git revision, and authoritative runtime evidence are truth; live memory and local path names are not. Read [artifact contracts](ARTIFACTS.md) before creating or validating a record.

## Reconstruct durable state

Re-read the ticket, dependencies, routing, assignees, coordination notes, Review Proposals and feedback, Published Delivery Heads, evidence bindings, and runtime state. Reconstruct the current Execution Checkpoint; active, completed, and superseded Human Action Requests; one free-form Human Response and its reconciliation; actionable feedback after a completed review round; runtime liveness or termination; local-only work; Resumption Records; and handoff effects.

No prior artifacts means an initial attempt. An unresolved escalation-bearing request takes precedence. Mixed sources, multiple active requests, incomplete chains, contradictory revisions, or missing records require a human boundary.

## Establish a human boundary

Preserve safe work and publish a recoverable changed head when authorized and safe. Record local-only work without treating it as published. Then:

1. Create or refresh one Execution Checkpoint.
2. Reuse the one active Human Action Request when it asks for the required action; otherwise create one only when none is active.
3. When planned verification becomes Validation Indeterminacy, supersede it with one linked escalation request that reuses the checkpoint.
4. Verify exactly one active request, transition the open ticket to unassigned `ready-for-human`, and stop.

An Environment Preparation Blocker follows bounded recovery and preserves every prepared worktree. A Specification Contradiction or Material Design Opportunity records authoritative evidence and pauses affected and dependent work. Planned verification records reproducible steps, pass/fail criteria, prerequisites, expected evidence, and an accountable owner. Indeterminate liveness requests human reconciliation because elapsed time is not termination evidence. Unreconciled local-only work requests provenance while remaining outside automatic recovery.

Report contradictory state as observed. Human authority supplies reconciliation; preserve history instead of repairing it destructively.

## Apply the Resume Gate

The ticket must be open, unassigned, and explicitly returned to exactly `ready-for-agent`. Acquire and verify the Workflow Identity claim, then select exactly one source:

| Resume Gate source | Allowed disposition | Required reconciliation |
| --- | --- | --- |
| Execution Checkpoint plus a completed Human Response | `continue` or `replan` | The response resolves its request; `replan` links an execution-ready human-produced or explicitly delegated Resumption Plan. |
| actionable Review Feedback after a completed review round | `continue` | Feedback is unresolved or enumerated, attributable, and addressable within settled authority. |
| runtime-proven termination plus a reconstructed Execution Checkpoint | `continue` | Runtime evidence proves termination and every recovered artifact resolves durably. |

A free-form response becomes executable through reconciliation, not word matching. A terminal outcome does not resume. Missing plans, incompatible meaning, unresolved escalation, or multiple sources returns to the human boundary.

Publish and re-read one Resumption Record before any new Execution Attempt, agent, validation, review, publication, or handoff action. Start from its exact heads and next step.

## Invalidate evidence by influence

- A changed head invalidates that repository's validation and Standards result.
- Invalidate cross-repository evidence whose influencing set includes that delivery, and Bundle Spec when any bound head changes.
- Preserve evidence whose complete influencing heads remain byte-identical.
- Actionable Review Feedback invalidates the affected delivery evidence and dependent results.
- Reuse each existing Review Proposal and verify its new head.

Record invalidated, preserved, and refreshed evidence IDs. Repeat the calculation after every later head change.

## Recover handoff only

When implementation, exact-head evidence, review, and publication are complete but handoff effects are missing, launch a normal handoff-only attempt after the gate. Start zero Implementation Agents, reuse verified proposals and evidence, and apply handoff idempotently. A matching key produces no duplicate note.

## Replay the contract

The replay normalizes provider observations without replacing provider truth:

```bash
python3 scripts/replay_lifecycle.py tests/fixtures/environment-blocker-continue.json
```

Each stable fixture ID supplies durable input and an independently stated public outcome. Replay emits source, disposition, records, event order, evidence invalidation, proposal reuse, routing/claim result, and boundary reason. Run all cases with `python3 -m unittest discover -s skills/matt/engineering/coordinate-delivery/tests -v`.
