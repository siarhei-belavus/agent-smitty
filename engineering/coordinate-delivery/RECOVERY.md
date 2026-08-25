# Recovery

Read [planning artifact contracts](../federated-workflow/PLANNING-ARTIFACTS.md) and [lifecycle artifact contracts](../federated-workflow/LIFECYCLE-ARTIFACTS.md) before classifying recovery.

The Resume Gate proves that exactly one durable source authorizes the next Execution Attempt and determines whether work continues under existing intent or follows a Resumption Plan.

Re-read the ticket, dependencies, routing, assignees, coordination notes, Review Proposals and feedback, Published Delivery Heads, and evidence bindings. Validate every lifecycle record against [the artifact invariants](../federated-workflow/LIFECYCLE-ARTIFACTS.md#record-invariants). Durable provider state must suffice in a fresh context; live memory supplies no missing fact. Preserve local-only dirty work but exclude it from authority until a human establishes provenance.

Treat an accessible Execution Worktree as reusable host state, not recovery authority. Verify its Repository Reference, intended delivery branch, fixed base, current head, and provenance from current context, Execution Checkpoint, handoff, completed Human Response, or Resumption Record. Preserve an identity mismatch or unknown dirty state and enter the [human-boundary branch](HUMAN-BOUNDARY.md). When the worktree is absent or unavailable, reconstruct the delivery from its latest Published Delivery Head or recorded Base Branch launch commit without treating the old local path as required state.

Classify a matching handoff before the Resume Gate. When its ticket, deterministic bundle key, exact heads, proposals, and evidence match current provider truth, the Delivery Bundle handoff is complete, and no unresolved lifecycle record remains, treat the delivery as terminal: report the existing handoff and return without a new request, claim, Resume Gate, or mutation. When delivery results are complete but the handoff note or final effects are incomplete, continue through the Resume Gate and then read [handoff-only recovery](HANDOFF-ONLY.md). A contradictory handoff enters the [human-boundary branch](HUMAN-BOUNDARY.md).

Use exactly one Resume Gate source:

- an Execution Checkpoint plus completed Human Response;
- [actionable Review Feedback](REVIEW-FEEDBACK.md) after a completed review round; read that branch to qualify the source, then continue here;
- [runtime-proven termination](RUNTIME-TERMINATION.md) plus reconstructed Execution Checkpoint; read that branch to qualify the source, then continue here.

An unresolved escalation-bearing request takes precedence. Mixed sources, multiple active requests, incomplete chains, contradictory revisions, missing records, or unreconciled local-only work enter the [human-boundary branch](HUMAN-BOUNDARY.md).

The ticket must be open and explicitly returned to exactly `ready-for-agent`. Retain an activation-authority claim already acquired and verified for this Coordinator Activation; otherwise require the ticket to be unassigned, then acquire and verify the Workflow Identity claim. A foreign or interrupted claim qualifies only through [runtime termination](RUNTIME-TERMINATION.md). Select `continue` for Review Feedback or runtime termination. For a completed Human Response, select `continue` or `replan`; `replan` requires an execution-ready human-produced or explicitly delegated Resumption Plan.

Compare every recorded evidence dependency with current provider revisions. A changed delivery head invalidates its repository validation and Standards result, every cross-repository result it influences, and Bundle Spec. A changed influencing Validation Source commit invalidates only dependent cross-repository evidence and Bundle Spec.

Whenever Recovery or Review Feedback reassembles Work Tracker authority, treat the accepted output as a new Authority input. Invalidate every prior Standards and Bundle Spec result that depended on the previous input and require fresh reviews. This conservative invalidation does not by itself invalidate repository validation or cross-repository evidence; preserve those when their complete delivery-head and Validation Source commit dependency sets remain unchanged. This paragraph is the sole owner of recovery evidence classification for reassembled Authority input.

Publish and re-read the [Resumption Record](../federated-workflow/LIFECYCLE-ARTIFACTS.md#resumption-record) before any new Execution Attempt or downstream mutation. Always revalidate the complete delivery contract and Repository Resolution, including instructions, bindings, canonical context, and ADRs, against provider truth. When that authority remains valid, jump exactly to the record's next permissible step, which must name the earliest invalidated prerequisite; reuse already-complete preparation only after worktree identity and provenance validation, and reuse implementation, publication, and evidence whose prerequisites, influencing delivery heads, and Validation Source commits remain unchanged and which the conservative Authority input rule above did not invalidate.

**Complete when:** either the completed matching handoff is proven terminal, or exactly one source and allowed disposition are proven, the claim and launch heads match provider truth, reassembled authority has invalidated its dependent review evidence, evidence is otherwise classified by influence, and the Resumption Record precedes the next attempt.
