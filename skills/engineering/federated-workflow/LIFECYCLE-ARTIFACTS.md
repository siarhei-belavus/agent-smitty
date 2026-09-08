# Durable lifecycle artifact contracts

Read [delivery records](DELIVERY-RECORDS.md) and [provider concepts](PROVIDER-CONCEPTS.md) before applying these records.

Publish delivery lifecycle records through the configured Work Tracker coordination log using permanent provider identifiers, canonical ticket references, exact revisions, and stable record IDs.

An Execution Attempt is one interval of delivery work between activation or resumption and the next durable completion or human boundary.

## Comment presentation

Apply this presentation to every agent-authored lifecycle record, including reconstructed checkpoints, successor requests, delegated Resumption Plans, and final handoffs. Presentation changes neither record identity nor lifecycle authority; reuse an existing valid record regardless of its formatting.

Write each record as one comment with a human-readable opening followed by recovery details. These are parts of the same record, not separate summary and technical comments.

- Lead with a short title stating the result, reason for stopping, or next action. Keep record types and IDs in the recovery details.
- Write the opening in short paragraphs using the record-specific emphasis below. Use descriptive links to proposals, requests, and evidence. Use a compact table when several repositories or results need comparison.
- Keep blockers, material limitations, and required human actions visible in the opening. When action is required, include the owner, response instructions, completion criteria, and what the response enables as defined by the Human Action Request contract. State when no human action is currently needed.
- Follow with a `Recovery details` section containing the remaining contract data, grouped by delivery, evidence, and lifecycle relationships as applicable. Use labeled fields or tables for exact commits, branches, record IDs, routing and claim snapshots, and provenance. Use the provider's supported disclosure format to collapse only this section when its full contents remain readable through the configured coordination-log operation. Otherwise use an ordinary Markdown section.

Every required contract fact must remain explicit in the comment. Keep full exact revisions and evidence dependency sets wherever the contract requires them. A readable link label or shortened hash never replaces that data.

Before publishing, verify that the opening agrees with the recorded evidence and distinguishes observed state from pending transitions. After publication, re-read the entire comment, including recovery details, through the provider. Verify required fields and relationships, and that the opening exposes every required human action and material limitation. Recovery readers consume the whole record regardless of its visual presentation.

## Record invariants

- Every record ID is unique and every relationship resolves bidirectionally to the named record.
- One current Execution Checkpoint has at most one active Human Action Request and one linked free-form Human Response.
- Repository evidence names its repository and exact head. Cross-repository evidence names its complete influencing delivery-head set and every repository-backed Validation Source with its recorded exact source commit. Bundle Spec evidence names the complete bundle head set and the cross-repository evidence with those source commits. A mismatch is stale evidence.
- Runtime termination evidence names the provider record, its execution URL or equivalent runtime reference when available, the checkpoint, and the observed termination outcome. The runtime reference supports observability and liveness diagnosis; it establishes neither the claim nor recovery authority. Elapsed time is not evidence.
- Durable records identify preserved Execution Worktrees by Repository Delivery, branch, base, exact Git state, and provenance disposition. Local paths remain execution-host inputs and never enter a checkpoint, request, response, Resumption Record, or handoff.
- A runtime-local Context Pack path remains activation state and never enters a checkpoint, request, response, Resumption Record, or handoff. Durable records identify authority by selected profile, permanent root, result, and provider references, never by retaining the pack or its local path.
- Append-only successors preserve history and identify the current record.

## Execution Checkpoint

Open with where work stopped, why, what was verified and preserved, and what permits the next step. For a final handoff, explain what is ready for review, link the proposals, summarize verification results, and state the human review, merge, or rollout actions in their required order.

The opening may focus on changes since the previous record; the complete checkpoint, including a final handoff, carries a current snapshot rather than a delta requiring reconstruction from earlier comments.

An Execution Checkpoint is the current durable snapshot of a Delivery Bundle. Record the checkpoint, ticket, Execution Attempt ID, trigger, provider timestamp, ticket/routing/claim snapshot, resolved dependencies and authority, and the next permissible step with prerequisites. For every Repository Delivery record its base, branch, exact Published Delivery Head, Review Proposal, preserved worktree state, and outcome. Record exact repository-backed Validation Source commits; exact-head repository, Standards, cross-repository, and Bundle Spec evidence; affected and preserved deliveries; invalidated, preserved, and pending evidence; the active request ID or explicit absence; local-only exclusions; an execution URL or equivalent runtime reference when the runtime provides one; and limitations.

## Human Action Request

Open with the action and response instructions. For planned verification, keep the complete verification procedure defined below visible too. A successor explains what the previous response left unresolved.

A Human Action Request is a durable request for one accountable human action. Record the request ID, status (`active`, `completed`, or `superseded`), reason, checkpoint, ticket, accountable owner, required action, response location, completion criteria, and next routing transition. Planned verification also records prerequisites, reproducible steps, pass/fail criteria, and expected evidence. Escalation also records its trigger, observed evidence, affected decisions and deliveries, authoritative pointers, and required reconciliation. A Validation Indeterminacy successor records predecessor and successor IDs.

For planned verification, read the [acceptance criteria contract](PLANNING-ARTIFACTS.md#acceptance-criteria). Derive the request from the applicable criteria and settled Validation Obligations, retaining source references and criterion identifiers where assigned. Carry the declared manual procedure and expected results into the request, then supply verified build and environment details where the declared method requires them. Link existing QA cases when supplied. Missing prerequisites remain visible limitations, not invented setup or changed acceptance behavior.

Complete or supersede the current request before activating its successor.

## Human Response

A Human Response is one durable reply from the accountable human through the request's Work Tracker surface. Its prose has no provider-specific schema. Record its permanent provider ID and exact request relationship, then reconcile it against the requested action and completion criteria. Record whether it completes, supersedes, or leaves the request indeterminate and identify accepted authority and evidence.

## Resumption Plan

Open with the accepted plan, how it changes the remaining work, and what existing work and evidence it retains or replaces.

A Resumption Plan is a human-produced or explicitly delegated execution-ready plan for `replan`. Record its ID, authority, source response, accepted intent, affected and preserved deliveries, treatment of checkpoint worktrees/heads/proposals/evidence, next executable work, settled boundaries, and completion criteria.

## Resumption Record

Open with the source authorizing resumption, where work will restart, what is reused, and which checks must run again and why.

A Resumption Record is the durable gate result written before a resumed Execution Attempt. Record its ID, ticket, next Execution Attempt ID, exactly one response/feedback/runtime source, `continue` or `replan`, checkpoint, plan when applicable, affected and preserved deliveries, previous and launch exact delivery heads and repository-backed Validation Source commits, reused proposals, invalidated evidence, preserved unchanged-dependency evidence, required refresh, re-read routing/claim state, next step, and limitations.

Publish and re-read this record after a successful Resume Gate and before the named Execution Attempt. Verify its launch heads against provider truth.
