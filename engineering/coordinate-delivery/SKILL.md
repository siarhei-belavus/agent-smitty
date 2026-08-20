---
name: coordinate-delivery
description: "Coordinate one agent-ready ticket through its complete federated delivery and human handoff."
disable-model-invocation: true
---

Coordinate `/coordinate-delivery <ticket reference>` as one fail-closed Delivery Bundle.

Use repository-owned bindings for every provider operation. Persist no provider commands, credentials, or account identity. Preserve recoverable work. Never merge a Review Proposal, push a protected Base Branch, or close the ticket.

## 1. Establish activation authority

Resolve the ticket only through the configured Ticket Origin Repository. Read its `AGENTS.md`, Work Tracker, Routing Label, Domain Orientation, and Code Host bindings, then the complete ticket, comments, dependencies, coordination notes, Review Feedback, and Code Host state.

Classify the claim before recovery. A claim is current only when activation authority, including a verified dispatcher entry, shows that it was acquired for this Coordinator Activation and a provider re-read shows the ticket assigned solely to the Workflow Identity; retain that claim. An assignment without this proof is foreign or interrupted, so read [runtime termination](RUNTIME-TERMINATION.md) before mutation.

When any prior checkpoint, request, response, Resumption Record, existing Review Proposal, or handoff exists, read [recovery](RECOVERY.md) before mutation. Otherwise require an open, unblocked ticket carrying exactly `ready-for-agent`; retain its current-activation claim or, when unassigned, resolve the Workflow Identity, assign only it, and re-read the claim.

**Complete when:** either recovery has produced and verified its terminal or resumable durable result, or the open ticket is unblocked, exactly `ready-for-agent`, solely assigned to the Workflow Identity, and the claim is verified for this Coordinator Activation.

## 2. Validate the delivery contract

Read [`../PLANNING-ARTIFACT-CONTRACTS.md`](../PLANNING-ARTIFACT-CONTRACTS.md) completely. Require complete Repository References, resolvable Context Scope, non-empty Repository Scope with repository-owned outcomes, every applicable Settled Seam and Validation Obligation, and consistent ticket, dependency, user, canonical-context, ADR, and accepted-decision authority.

For every referenced repository, read its instructions, Code Host binding, canonical context, and ADRs. Validate its remote, Base Branch, and non-destructive provider access against the Repository Reference.

**Complete when:** every required contract field and context pointer is present, consistent, readable, and owned by a validated repository; any material omission or conflict has entered the [human-boundary branch](HUMAN-BOUNDARY.md) before repository mutation.

## 3. Prepare repository deliveries

Create a run-specific persistent root outside existing user checkouts. Fetch every configured Base Branch from its declared remote and pin its fresh exact commit. Prepare one clean isolated Execution Worktree per Repository Scope entry, with a unique delivery branch only when changes are required. Keep validation-only and no-change deliveries at their pins and read-only repositories outside writable scope. Record each Repository ID, Reference, path, branch, and fixed base.

**Complete when:** every Repository Delivery is clean at its fixed base, existing user state is unchanged, and any persistent preparation failure has entered the [human-boundary branch](HUMAN-BOUNDARY.md) with all safe work preserved.

## 4. Execute one flat attempt

Start exactly one direct-child Implementation Agent for each delivery requiring changes. Give it a Coordinator-narrowed `implement` assignment containing its repository identity, worktree, branch, fixed base, authority, outcome, Settled Seams, Validation Obligations, instructions, and validation commands. Require one Repository Delivery result and no child agents or reviewers. Record validation-only and no-change deliveries directly.

Verify every result against its assigned worktree and base; classify an expected change with no diff as unchanged.

**Complete when:** every scope entry has exactly one attributable result, every changed worktree is clean at its exact local head, all repository validation is bound to that head, and any discovered contradiction or material design decision has entered the [human-boundary branch](HUMAN-BOUNDARY.md) with affected and dependent work paused.

## 5. Review exact heads

For each changed delivery, verify its fixed-base diff and exact-head validation, then use the `code-review` skill in **Standards only** mode with its fixed Repository Target, authority, seams, and evidence. Record Advisory findings. The bundle has one correction/recheck round across this step and Step 7; route an attributable in-scope Blocking finding to the affected Implementation Agent and refresh every result made stale by a changed head.

**Complete when:** every changed exact head has current repository validation and a fresh Standards result with no Blocking finding; a persistent or authority-changing finding has entered the [human-boundary branch](HUMAN-BOUNDARY.md).

## 6. Publish Review Proposals

Using each changed repository's Code Host binding, publish its delivery branch and verify its remote exact head. Create exactly one Draft Review Proposal to the configured Base Branch; re-read its source, target, draft state, and head. Publish nothing for unchanged deliveries.

**Complete when:** each changed delivery has one verified Draft Review Proposal at its exact Published Delivery Head and every Base Branch remains unchanged.

## 7. Validate the bundle

Run every Cross-Repository Validation Obligation against the complete Published Delivery Head set through its declared Validation Source, prerequisites, method, scenario, expected result, and evidence format. Use the `code-review` skill in **Spec only** mode once over the complete changed target set with all authority, seams, evidence, and proposals. Record Advisory findings and use the remaining correction/recheck round for attributable in-scope Blocking findings.

**Complete when:** every declared obligation and fresh Bundle Spec result passes against one current exact-head set; all evidence made stale by a changed influencing head has been refreshed while identical-head evidence remains current, or planned human verification has entered the [human-boundary branch](HUMAN-BOUNDARY.md).

## 8. Hand off idempotently

Re-read the ticket and verify the Step 1 claim. Mark every verified proposal ready and re-read it. Build `coordinate-delivery:<canonical ticket reference>:<SHA-256 of sorted Repository ID=exact head lines>`.

Reuse a matching handoff; otherwise append one note recording every base, head, branch, proposal, validation and review result, Advisory finding, human action, merge/rollout order, unchanged delivery, preserved state, and limitation. Apply only missing final effects: release the Workflow Identity claim, replace `ready-for-agent` with exactly `ready-for-human`, and leave the ticket open.

**Complete when:** exactly one matching handoff exists, every proposal is ready at its recorded head, and the ticket is open, unassigned, and carries exactly `ready-for-human` among Routing Labels.

Report the ticket, persistent root, fixed bases and heads, validation, proposals, review outcomes, and final Work Tracker state.
