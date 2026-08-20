# Recovery

Read this file when an activation finds any prior checkpoint, request, response, Resumption Record, existing Review Proposal, or handoff.

Re-read the ticket, dependencies, routing, assignees, coordination notes, Review Proposals and feedback, Published Delivery Heads, and evidence bindings. Validate every lifecycle record against [the artifact invariants](ARTIFACTS.md#record-invariants). Durable provider state must suffice in a fresh context; live memory supplies no missing fact. Preserve local-only dirty work but exclude it from authority until a human establishes provenance.

Classify a matching handoff before the Resume Gate. When its ticket, deterministic bundle key, exact heads, proposals, and evidence match current provider truth, Step 8's completion criterion already holds, and no unresolved lifecycle record remains, treat the delivery as terminal: report the existing handoff and return without a new request, claim, Resume Gate, or mutation. When delivery results are complete but the handoff note or final effects are incomplete, continue through the Resume Gate and then read [handoff-only recovery](HANDOFF-ONLY.md). A contradictory handoff enters the [human-boundary branch](HUMAN-BOUNDARY.md).

Use exactly one Resume Gate source:

- an Execution Checkpoint plus completed Human Response;
- [actionable Review Feedback](REVIEW-FEEDBACK.md) after a completed review round; read that branch to qualify the source, then continue here;
- [runtime-proven termination](RUNTIME-TERMINATION.md) plus reconstructed Execution Checkpoint; read that branch to qualify the source, then continue here.

An unresolved escalation-bearing request takes precedence. Mixed sources, multiple active requests, incomplete chains, contradictory revisions, missing records, or unreconciled local-only work enter the [human-boundary branch](HUMAN-BOUNDARY.md).

The ticket must be open and explicitly returned to exactly `ready-for-agent`. Retain a Step 1 claim already acquired and verified for this Coordinator Activation; otherwise require the ticket to be unassigned, then acquire and verify the Workflow Identity claim. A foreign or interrupted claim qualifies only through [runtime termination](RUNTIME-TERMINATION.md). Select `continue` for Review Feedback or runtime termination. For a completed Human Response, select `continue` or `replan`; `replan` requires an execution-ready human-produced or explicitly delegated Resumption Plan.

Compare every recorded evidence head with current provider revisions. A changed head invalidates its repository validation and Standards result, every cross-repository result influenced by that head, and Bundle Spec; preserve evidence whose complete influencing heads remain byte-identical.

Publish and re-read the [Resumption Record](ARTIFACTS.md#resumption-record) before any new Execution Attempt or downstream mutation. Always revalidate Step 2's complete delivery contract, repository authority, instructions, bindings, canonical context, and ADRs against provider truth. When that authority remains valid, jump exactly to the record's next permissible step, which must name the earliest invalidated prerequisite; reuse already-complete preparation, implementation, publication, and evidence whose prerequisites and influencing heads remain unchanged.

**Complete when:** either the completed matching handoff is proven terminal, or exactly one source and allowed disposition are proven, the claim and launch heads match provider truth, evidence is classified by influence, and the Resumption Record precedes the next attempt.
