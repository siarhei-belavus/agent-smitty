---
name: coordinate-delivery
description: "Coordinate one agent-ready ticket through its complete federated delivery and human handoff."
disable-model-invocation: true
---

Coordinate `/coordinate-delivery [<ticket reference>]` as one fail-closed Delivery Bundle. A supplied reference selects that ticket only. Without a reference, select and claim at most one ticket from the configured Delivery frontier. An empty frontier is a successful no-op.

Use repository-owned bindings for every provider operation. Persist no provider commands, credentials, or account identity. Preserve recoverable work. Never merge a Review Proposal, push a protected Base Branch, or close the ticket.

## 1. Establish activation authority

Resolve tickets only through the configured Ticket Origin Repository. Read its `AGENTS.md`, Work Tracker, Routing Label, Domain Orientation, and Code Host bindings before selecting a ticket.

Choose one activation ticket. With a supplied reference, resolve exactly that ticket and never substitute another. Without a reference, read the Work Tracker's ordinary Markdown `## Delivery frontier` instructions and query the configured tracker. Authoritatively re-read every candidate's ticket, Routing Labels, assignees, and dependencies before deciding eligibility. Keep open, unblocked, unassigned tickets carrying exactly `ready-for-agent`, then order them as the binding says. If no eligible ticket remains, finish successfully without creating a bundle or changing provider state.

Read the selected ticket's complete body, comments, dependencies, coordination notes, Review Feedback, and Code Host state. A ticketless candidate that becomes ineligible before mutation returns to selection against current provider state. A named ticket that is ineligible or assigned elsewhere stops at the applicable runtime-termination or human boundary and never falls back to frontier selection.

Classify the claim before recovery. Only a claim acquired and provider-verified during this activation is current. Any assignment already present on a named ticket is foreign or interrupted, including an assignment to the Workflow Identity, so read [runtime termination](RUNTIME-TERMINATION.md) before mutation.

When any prior checkpoint, request, response, Resumption Record, existing Review Proposal, or handoff exists, read [recovery](RECOVERY.md) before mutation. Otherwise resolve the Workflow Identity and re-read the selected ticket's Routing Labels, assignees, and dependencies immediately before claiming it. Require it to remain open, unblocked, unassigned, and exactly `ready-for-agent`. Assign only the Workflow Identity, then authoritatively re-read the same state and proceed only when that identity is the sole assignee and every eligibility condition still holds.

For a ticketless activation, any pre-claim change or failed post-claim verification recomputes the ordered frontier from current provider state. Repeat the selection and recovery checks, then attempt another claim. Stop after the first verified claim, so the activation claims at most one ticket. For a named ticket, the same race enters the applicable human boundary instead of selecting another ticket.

**Complete when:** the ticketless frontier is empty; recovery has produced and verified its terminal or resumable durable result; or one open, unblocked, exactly `ready-for-agent` ticket is solely assigned to the Workflow Identity through a claim verified in this Coordinator Activation.

## 2. Validate the delivery contract

Read [`../federated-workflow/PLANNING-ARTIFACTS.md`](../federated-workflow/PLANNING-ARTIFACTS.md) completely. Require complete Repository References, resolvable Context Scope, non-empty Repository Scope with repository-owned outcomes, every applicable Settled Seam and Validation Obligation, and consistent ticket, dependency, user, canonical-context, ADR, and accepted-decision authority.

**Complete when:** every required contract field and context pointer is present and internally consistent; any material omission or conflict has entered the [human-boundary branch](HUMAN-BOUNDARY.md) before repository mutation.

## 3. Resolve repository references

Resolve every Repository Reference before fetching a Base Branch or creating an Execution Worktree. Validate and reuse a matching current checkout, explicitly supplied checkout, known worktree, execution-host checkout, or bounded nearby Repository Store. Otherwise prepare a checkout from the reference's declared remote at an execution-host location. Folder proximity neither grants relevance nor proves repository identity. Use no repository registry or broad filesystem scan.

Validate each candidate against its Repository ID, remote, Base Branch, Git and worktree identity, and repository-local Code Host binding. After binding, read the repository's instructions, canonical context, ADRs, Context Scope targets, and repository-backed Validation Sources. Treat Repository Stores as read-only sources for worktree creation, never as delivery workspaces.

**Complete when:** every Repository Reference resolves to one validated Repository Store and every referenced instruction, context, ADR, binding, and Validation Source is readable; a contradiction or bounded access failure has entered the [human-boundary branch](HUMAN-BOUNDARY.md) before preparation.

## 4. Prepare repository deliveries

Create a run-specific persistent root outside existing user checkouts. Fetch every configured Base Branch from its declared remote and pin its fresh exact commit. Prepare one clean isolated Execution Worktree per Repository Scope entry, with a unique delivery branch only when changes are required. Keep validation-only and no-change deliveries at their pins and read-only repositories outside writable scope. Record each Repository ID, Reference, path, branch, and fixed base.

**Complete when:** every Repository Delivery is clean at its fixed base, existing user state is unchanged, and any persistent preparation failure has entered the [human-boundary branch](HUMAN-BOUNDARY.md) with all safe work preserved.

## 5. Execute one flat attempt

Start exactly one direct-child Implementation Agent for each delivery requiring changes. Give it one complete textual narrowing assignment for its Repository Scope entry and run `implement`. Include the Repository ID and Reference, Execution Worktree, branch, fixed base, authoritative sources, repository-specific outcome, Settled Seams and test approaches, Validation Obligations, repository instructions, and validation commands. Require its one Repository Delivery result. Record validation-only and no-change deliveries directly.

Verify every result against its assigned worktree and base; classify an expected change with no diff as unchanged.

**Complete when:** every scope entry has exactly one attributable result, every changed worktree is clean at its exact local head, all repository validation is bound to that head, and any discovered contradiction or material design decision has entered the [human-boundary branch](HUMAN-BOUNDARY.md) with affected and dependent work paused.

## 6. Review exact heads

For each changed delivery, verify its fixed-base diff and exact-head validation, then use the `code-review` skill in **Standards only** mode with its fixed Repository Target, authority, seams, and evidence. Record Advisory findings. Route each attributable in-scope Blocking finding to the affected Implementation Agent. After a correction, refresh repository validation and launch another fresh Standards review against the new exact head. Repeat until the result has no Blocking finding or a Specification Contradiction, Material Design Opportunity, or another genuine authority boundary applies.

**Complete when:** every changed exact head has current repository validation and a fresh Standards result with no Blocking finding; a persistent or authority-changing finding has entered the [human-boundary branch](HUMAN-BOUNDARY.md).

## 7. Publish Review Proposals

Using each changed repository's Code Host binding, publish its delivery branch and verify its remote exact head. Create exactly one Draft Review Proposal to the configured Base Branch; re-read its source, target, draft state, and head. Publish nothing for unchanged deliveries.

**Complete when:** each changed delivery has one verified Draft Review Proposal at its exact Published Delivery Head and every Base Branch remains unchanged.

## 8. Validate the bundle

Resolve every repository-backed Validation Source to one exact commit and record it before dispatch. Prepare or reuse isolated working state at that commit for each unchanged repository-backed Validation Source outside Repository Scope. Run validation there so mutable outputs cannot pollute the configured Repository Store. Launch fresh direct-child Validation Agents against the stable exact Published Delivery Head set and declared Validation Sources. Each assignment and its resulting cross-repository evidence bind every repository-backed Validation Source it uses to that recorded exact commit. Assign every mandatory Cross-Repository Validation Obligation to exactly one agent. Compatible obligations may share one Validation Agent only when they execute through the same compatible Validation Source, with one recorded exact source commit and coherent setup and evidence ownership. Each agent follows the declared prerequisites, method, scenario, expected result, and evidence format. It produces evidence, changes no product code, and makes no whole-ticket Spec judgment.

After every mandatory obligation has current passing evidence, use the `code-review` skill in **Spec only** mode over the complete changed target set with all authority, seams, evidence, and proposals. Record Advisory findings. Route attributable in-scope Blocking findings to the affected Implementation Agents. After a changed influencing delivery head, refresh its repository validation and fresh Standards review. A changed influencing delivery head or exact Validation Source commit invalidates only dependent cross-repository evidence and the Bundle Spec result. Rerun every invalidated obligation with fresh Validation Agents before another fresh full-bundle Spec review. Repeat until the result has no Blocking finding or a Specification Contradiction, Material Design Opportunity, or another genuine authority boundary applies.

**Complete when:** every declared obligation and fresh Bundle Spec result passes against one current exact delivery-head and Validation Source commit set; all evidence made stale by a changed influencing delivery head or Validation Source commit has been refreshed while evidence with an unchanged dependency set remains current, or planned human verification has entered the [human-boundary branch](HUMAN-BOUNDARY.md).

## 9. Hand off idempotently

Re-read the ticket and verify the activation-authority claim. Mark every verified proposal ready and re-read it. Build `coordinate-delivery:<canonical ticket reference>:<SHA-256 of sorted Repository ID=exact head lines>`.

Reuse a matching handoff; otherwise append one note recording every base, head, branch, proposal, validation and review result, Advisory finding, human action, merge/rollout order, unchanged delivery, preserved state, and limitation. Apply only missing final effects: release the Workflow Identity claim, replace `ready-for-agent` with exactly `ready-for-human`, and leave the ticket open.

**Complete when:** exactly one matching handoff exists, every proposal is ready at its recorded head, and the ticket is open, unassigned, and carries exactly `ready-for-human` among Routing Labels.

Report the ticket, persistent root, fixed bases and heads, validation, proposals, review outcomes, and final Work Tracker state.
