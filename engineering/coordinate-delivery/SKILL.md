---
name: coordinate-delivery
description: "Coordinate one agent-ready ticket through its complete federated delivery and human handoff."
disable-model-invocation: true
---

Coordinate `/coordinate-delivery <ticket reference>` as one fail-closed durable lifecycle.

Use repository-owned bindings for every provider operation. Keep provider commands, credentials, and account identity out of skill artifacts. At a gate that needs human authority, follow the [durable lifecycle](LIFECYCLE.md), write records from the [artifact contracts](ARTIFACTS.md), establish one human boundary, and stop. Preserve recoverable work. Never merge a Review Proposal, push a protected Base Branch, or close the ticket.

## 1. Reconstruct and establish authority

Resolve the ticket only through the configured Ticket Origin Repository. Read its applicable `AGENTS.md`, Work Tracker, Routing Label, Domain Orientation, and Code Host bindings, then read the complete ticket, comments, provider-native dependencies, coordination records, Review Feedback, and authoritative runtime state.

Classify the ticket before mutation. When any Execution Checkpoint, Human Action Request, Human Response, Review Feedback, existing Review Proposal, prior handoff, assigned claim, or interrupted activation exists, read `LIFECYCLE.md` completely and reconcile it from durable state. An initial attempt requires an open, unblocked, unassigned ticket carrying exactly the configured `ready-for-agent` Routing Label. A resumed attempt must pass the Resume Gate.

Resolve the authenticated provider user as the **Workflow Identity**. Acquire or reacquire only the eligible ticket, re-read its exact claim, and publish the required Resumption Record before a resumed Execution Attempt. Explicit human direction on an unassigned `ready-for-human` ticket authorizes assistance with the active human request, not an Execution Attempt.

**Complete when:** exactly one initial or resumed path is proven, every blocker is resolved, the ticket's sole assignee is the Workflow Identity, and any resumed path has its durable Resumption Record.

## 2. Validate the delivery contract

Read [`../PLANNING-ARTIFACT-CONTRACTS.md`](../PLANNING-ARTIFACT-CONTRACTS.md) completely and validate the ticket as a public executable artifact. Require complete Repository References, resolvable Context Scope, non-empty Repository Scope with repository-owned outcomes, every applicable Settled Seam and Validation Obligation, and consistent ticket, dependency, user, canonical-context, ADR, and accepted-decision authority.

For every referenced repository, read its instructions, Code Host binding, canonical context, and ADRs. Validate its remote, configured Base Branch, and non-destructive provider access against the Repository Reference.

**Complete when:** every contract record and context pointer is present, consistent, readable, and owned by a validated repository.

## 3. Prepare repository worktrees

Create a run-specific persistent worktree root outside existing user checkouts. Fetch each configured Base Branch from its declared remote, pin its fresh exact commit, and create one clean isolated worktree per Repository Scope entry. Create a unique delivery branch only for an outcome requiring changes; keep validation-only and explicit no-change deliveries at the pin, and read-only repositories outside writable scope. Record Repository ID, Reference, path, branch, and fixed base.

After bounded repository-owned recovery, treat persistent setup failure as an Environment Preparation Blocker and establish the human boundary from the preserved state.

**Complete when:** every Repository Delivery has one clean isolated worktree at its fixed base and existing user checkouts and branches remain unchanged.

## 4. Execute one flat attempt

Start exactly one direct-child implementation agent for each delivery requiring changes. Give it a Coordinator-narrowed `/implement` assignment with its Repository ID, Reference, Execution Worktree, branch, fixed base, authoritative sources, repository outcome, Settled Seams, Validation Obligations, instructions, and validation commands. Require one Repository Delivery result and no children or reviewers. The coordinator owns publication, Review Proposals, Work Tracker changes, bundle validation, and review. Record validation-only and no-change deliveries directly.

Verify every result against its assigned worktree and base; an expected change with no diff is unchanged. A Specification Contradiction or Material Design Opportunity pauses affected and dependent deliveries while preserving unrelated valid work through the human boundary.

**Complete when:** every scope entry has one attributable result, every changed worktree is clean at its exact local head, and repository validation is bound to that head.

## 5. Review exact heads

For every changed delivery, verify its fixed-base diff and exact-head validation, then invoke `/code-review` in **Standards only** mode with its fixed Repository Target, authority, seams, and evidence. Record Advisory findings.

The bundle has one correction/recheck round across Steps 5 and 7. Route an attributable in-scope Blocking finding to the affected Implementation Agent, then refresh validation and Standards for every changed head. A post-boundary attempt launches a fresh affected Implementation Agent. Escalate a persistent Blocking finding or a correction that changes material scope, acceptance, a settled seam, or an accepted decision.

**Complete when:** every changed exact head has current repository validation and a fresh Standards result with no Blocking finding.

## 6. Publish Review Proposals

Using each changed repository's Code Host binding, publish its delivery branch and verify the remote exact head. Create one Draft Review Proposal to the configured Base Branch, or reuse the delivery's existing proposal on a resumed attempt. Keep it Draft until bundle validation and Spec review pass; re-read its source, target, state, and head. Unchanged deliveries receive no publication or proposal.

**Complete when:** each changed delivery has one verified Draft Review Proposal at its exact published head and every protected Base Branch is unchanged.

## 7. Validate the bundle

Run every Cross-Repository Validation Obligation against the complete exact-head set through its declared source, prerequisites, method, scenario, result, and evidence format. For planned human verification, establish a checkpoint and request with reproducible steps, pass/fail criteria, and an accountable owner; stop at that boundary.

Invoke `/code-review` in **Spec only** mode once over the complete changed target set with all authority, seams, evidence, and proposals. Record Advisory findings. Route an attributable in-scope Blocking finding through the one correction/recheck round. After any changed influencing head, refresh repository validation, Standards, publication verification, dependent cross-repository evidence, and Bundle Spec. Escalate when the round is spent or settled authority must change.

**Complete when:** every declared obligation passes against the current exact-head set and a fresh Bundle Spec result has no Blocking finding.

## 8. Hand off idempotently

Re-read the ticket and require the Step 1 claim. Mark every verified proposal ready and re-read it. Build `coordinate-delivery:<canonical ticket reference>:<SHA-256 of sorted Repository ID=exact head lines>`.

Reuse a matching handoff; otherwise append one note recording every base, head, branch, proposal, validation and review result, Advisory finding, human action, merge/rollout order, unchanged delivery, preserved state, and limitation. Apply only missing final effects: release the Workflow Identity claim, replace `ready-for-agent` with exactly `ready-for-human`, and leave the ticket open.

**Complete when:** exactly one matching handoff exists, every proposal is ready at its recorded head, and the ticket is open, unassigned, and carries exactly `ready-for-human` among Routing Labels.

Report the ticket, persistent worktree root, fixed bases and heads, validation, proposals, review outcomes, and final Work Tracker state.
