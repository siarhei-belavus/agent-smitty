# Durable lifecycle artifact contracts

Read [delivery records](DELIVERY-RECORDS.md) and [provider concepts](PROVIDER-CONCEPTS.md) before applying these records.

Publish delivery lifecycle records through the configured Work Tracker coordination log using permanent provider identifiers, canonical ticket references, exact revisions, and stable record IDs.

An Execution Attempt is one interval of delivery work between activation or resumption and the next durable completion or human boundary.

## Record invariants

- Every record ID is unique and every relationship resolves bidirectionally to the named record.
- One current Execution Checkpoint has at most one active Human Action Request and one linked free-form Human Response.
- Repository evidence names its repository and exact head. Cross-repository evidence names its complete influencing delivery-head set and every repository-backed Validation Source with its recorded exact source commit. Bundle Spec evidence names the complete bundle head set and the cross-repository evidence with those source commits. A mismatch is stale evidence.
- Runtime termination evidence names the provider record, its execution URL or equivalent runtime reference when available, the checkpoint, and the observed termination outcome. The runtime reference supports observability and liveness diagnosis; it establishes neither the claim nor recovery authority. Elapsed time is not evidence.
- Durable records identify preserved Execution Worktrees by Repository Delivery, branch, base, exact Git state, and provenance disposition. Local paths remain execution-host inputs and never enter a checkpoint, request, response, Resumption Record, or handoff.
- A runtime-local Context Pack path remains activation state and never enters a checkpoint, request, response, Resumption Record, or handoff. Apply the shared Context Assembly [private-runtime lifecycle](WORK-TRACKER-CONTEXT-ASSEMBLY.md#private-runtime-lifecycle) before every terminal effect. Durable records identify authority by selected profile, permanent root, result, and provider references, never by retaining the pack or its local path.
- Append-only successors preserve history and identify the current record.

## Execution Checkpoint

An Execution Checkpoint is the current durable snapshot of a Delivery Bundle. Record the checkpoint, ticket, Execution Attempt ID, trigger, provider timestamp, ticket/routing/claim snapshot, resolved dependencies and authority, and the next permissible step with prerequisites. For every Repository Delivery record its base, branch, exact Published Delivery Head, Review Proposal, preserved worktree state, and outcome. Record exact repository-backed Validation Source commits; exact-head repository, Standards, cross-repository, and Bundle Spec evidence; affected and preserved deliveries; invalidated, preserved, and pending evidence; the active request ID or explicit absence; local-only exclusions; an execution URL or equivalent runtime reference when the runtime provides one; and limitations.

## Human Action Request

A Human Action Request is a durable request for one accountable human action. Record the request ID, status (`active`, `completed`, or `superseded`), reason, checkpoint, ticket, accountable owner, required action, response location, completion criteria, and next routing transition. Planned verification also records prerequisites, reproducible steps, pass/fail criteria, and expected evidence. Escalation also records its trigger, observed evidence, affected decisions and deliveries, authoritative pointers, and required reconciliation. A Validation Indeterminacy successor records predecessor and successor IDs.

Complete or supersede the current request before activating its successor.

## Human Response

A Human Response is one durable reply from the accountable human through the request's Work Tracker surface. Its prose has no provider-specific schema. Record its permanent provider ID and exact request relationship, then reconcile it against the requested action and completion criteria. Record whether it completes, supersedes, or leaves the request indeterminate and identify accepted authority and evidence.

## Resumption Plan

A Resumption Plan is a human-produced or explicitly delegated execution-ready plan for `replan`. Record its ID, authority, source response, accepted intent, affected and preserved deliveries, treatment of checkpoint worktrees/heads/proposals/evidence, next executable work, settled boundaries, and completion criteria.

## Resumption Record

A Resumption Record is the durable gate result written before a resumed Execution Attempt. Record its ID, ticket, next Execution Attempt ID, exactly one response/feedback/runtime source, `continue` or `replan`, checkpoint, plan when applicable, affected and preserved deliveries, previous and launch exact delivery heads and repository-backed Validation Source commits, reused proposals, invalidated evidence, preserved unchanged-dependency evidence, required refresh, re-read routing/claim state, next step, and limitations.

Publish and re-read this record after a successful Resume Gate and before the named Execution Attempt. Verify its launch heads against provider truth.
