# Recovery

Read this file when an activation finds any prior checkpoint, request, response, Resumption Record, existing Review Proposal, handoff, assigned claim, or interrupted activation.

Re-read the ticket, dependencies, routing, assignees, coordination notes, Review Proposals and feedback, Published Delivery Heads, evidence bindings, and runtime state. Validate every lifecycle record against [the artifact invariants](ARTIFACTS.md#record-invariants). Durable provider state must suffice in a fresh context; live memory supplies no missing fact. Preserve local-only dirty work but exclude it from authority until a human establishes provenance.

Use exactly one Resume Gate source:

- an Execution Checkpoint plus completed Human Response;
- [actionable Review Feedback](REVIEW-FEEDBACK.md) after a completed review round; read that branch to qualify the source, then continue here;
- [runtime-proven termination](RUNTIME-TERMINATION.md) plus reconstructed Execution Checkpoint; read that branch to qualify the source, then continue here.

An unresolved escalation-bearing request takes precedence. Mixed sources, multiple active requests, incomplete chains, contradictory revisions, missing records, or unreconciled local-only work enter the [human-boundary branch](HUMAN-BOUNDARY.md).

The ticket must be open, unassigned, and explicitly returned to exactly `ready-for-agent`. Acquire and verify the Workflow Identity claim. Select `continue` for Review Feedback or runtime termination. For a completed Human Response, select `continue` or `replan`; `replan` requires an execution-ready human-produced or explicitly delegated Resumption Plan.

Compare every recorded evidence head with current provider revisions. A changed head invalidates its repository validation and Standards result, every cross-repository result influenced by that head, and Bundle Spec; preserve evidence whose complete influencing heads remain byte-identical.

Publish and re-read the [Resumption Record](ARTIFACTS.md#resumption-record) before any new Execution Attempt or downstream mutation. When only final handoff effects remain, continue with [handoff-only recovery](HANDOFF-ONLY.md); otherwise continue the primary skill at Step 2 from the record's exact heads and next step.

**Complete when:** exactly one source and allowed disposition are proven, the claim and launch heads match provider truth, evidence is classified by influence, and the Resumption Record precedes the next attempt.
