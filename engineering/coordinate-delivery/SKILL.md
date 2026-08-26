---
name: coordinate-delivery
description: "Coordinate one agent-ready ticket through its complete federated delivery and human handoff."
disable-model-invocation: true
---

Read [Work Tracker context assembly](../federated-workflow/WORK-TRACKER-CONTEXT-ASSEMBLY.md) before accepting ticket authority or preparing a repository delivery.

A Coordinator Activation is one invocation that selects or resumes at most one ticket and owns only a claim it acquires and verifies.

Coordinate `/coordinate-delivery [<ticket reference>]` fail closed. A supplied reference selects that ticket only. Without a reference, select and claim at most one ticket from the configured Delivery frontier. An empty frontier is a successful no-op.

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

Select Delivery Context for the exact permanent reference of the claimed activation ticket and assemble it through the Ticket Origin Repository's Work Tracker binding after the claim is verified. Retain the accepted output unchanged as the activation's **Authority input**. When assembly stops, enter the [human-boundary branch](HUMAN-BOUNDARY.md) with the claim and safe state preserved.

Read [`../federated-workflow/PLANNING-ARTIFACTS.md`](../federated-workflow/PLANNING-ARTIFACTS.md) completely. Validate the assembled Delivery Context against the planning contracts. Require complete Repository References, resolvable Context Scope, non-empty Repository Scope with repository-owned outcomes, every applicable Settled Seam and Validation Obligation, and consistent ticket, dependency, user, canonical-context, ADR, and accepted-decision authority.

A Delivery Bundle is one ticket's complete delivery state: its Repository Deliveries; any Published Delivery Heads, Review Proposals, and lifecycle records; current validation and review evidence; and handoff state.

**Complete when:** the claimed ticket's Delivery Context gate passes, its Authority input is retained, and the planning contract validates; otherwise the delivery has entered the [human-boundary branch](HUMAN-BOUNDARY.md) before repository mutation.

## 3. Resolve repository references

Read [execution preparation](EXECUTION-PREPARATION.md) completely before binding repositories or mutating local Git state.

Repository Resolution binds each Repository Reference to one validated Repository Store.

Resolve every Repository Reference before fetching a Base Branch or creating an Execution Worktree. Validate and reuse a matching current checkout, explicitly supplied checkout, known worktree, execution-host checkout, or bounded nearby Repository Store. Otherwise prepare a checkout from the reference's declared remote at an execution-host location. Folder proximity neither grants relevance nor proves repository identity. Use no repository registry or broad filesystem scan.

Validate each candidate against its Repository ID, remote, Base Branch, Git and worktree identity, and repository-local Code Host binding. Record a material inferred or prepared binding by its portable repository identity and validation evidence, without its local path. After binding, read the repository's instructions, canonical context, ADRs, Context Scope targets, and repository-backed Validation Sources. Preserve each Repository Store's checkout state and use it only as a Git source for worktree creation, never as a delivery workspace.

**Complete when:** every Repository Reference resolves to one validated Repository Store and every referenced instruction, context, ADR, binding, and Validation Source is readable; a missing or contradictory authority has entered the [human-boundary branch](HUMAN-BOUNDARY.md) as a Specification Contradiction, or a bounded access or host-capability failure has entered it as an Environment Preparation Blocker, before preparation.

## 4. Prepare repository deliveries

Apply the loaded execution-preparation rules. Fetch every configured Base Branch without switching its Repository Store and pin its fresh exact commit. Prepare or reuse one clean isolated Execution Worktree and unique delivery branch per Repository Scope entry. Keep deliveries later classified as no-change at their pins and read-only repositories outside writable scope. Keep the Repository ID-to-worktree mapping in execution-host state; portable records identify the delivery, branch, base, and exact head without a local path.

**Complete when:** every Repository Delivery has a provenance-verified persistent worktree at its intended branch and fixed base, its immediate mandatory bootstrap has succeeded, existing user checkout state is unchanged, and any persistent preparation failure has entered the [human-boundary branch](HUMAN-BOUNDARY.md) with all safe work preserved.

## 5. Execute one flat attempt

Start exactly one direct-child Implementation Agent for each delivery requiring changes. Give it one complete textual narrowing assignment for its Repository Scope entry and run `implement`. Include the Repository ID and Reference, Execution Worktree, branch, fixed base, the unchanged Authority input, repository-specific outcome, Settled Seams and test approaches, Validation Obligations, repository instructions, and validation commands. Require its one Repository Delivery result. Record validation-only and no-change deliveries directly.

Verify every result against its assigned worktree and base; classify an expected change with no diff as unchanged.

**Complete when:** every changed assignment preserves the Authority input from step 2, every scope entry has exactly one attributable result, every changed worktree is clean at its exact local head, all repository validation is bound to that head, and any discovered contradiction or material design decision has entered the [human-boundary branch](HUMAN-BOUNDARY.md) with affected and dependent work paused.

## 6. Review exact heads

For each changed delivery, verify its fixed-base diff and exact-head validation, then use the `code-review` skill in **Standards only** mode. Its fixed Repository Target includes the unchanged Authority input from step 2, together with seams and evidence. Record Advisory findings. Route each attributable in-scope Blocking finding to the affected Implementation Agent. After a correction, refresh repository validation and launch another fresh Standards review against the new exact head with the same Authority input. Repeat until the result has no Blocking finding or a Specification Contradiction, Material Design Opportunity, or another genuine authority boundary applies.

**Complete when:** every changed exact head has current repository validation and a fresh Standards result bound to the Authority input from step 2, with no Blocking finding; a persistent or authority-changing finding has entered the [human-boundary branch](HUMAN-BOUNDARY.md).

## 7. Publish Review Proposals

Using each changed repository's Code Host binding, publish its delivery branch and verify its remote exact head. Create exactly one Draft Review Proposal to the configured Base Branch; re-read its source, target, draft state, and head. Publish nothing for unchanged deliveries.

**Complete when:** each changed delivery has one verified Draft Review Proposal at its exact Published Delivery Head and every Base Branch remains unchanged.

## 8. Validate the bundle

Resolve every repository-backed Validation Source to one exact commit and record it before dispatch. Prepare or reuse isolated working state at that commit for each unchanged repository-backed Validation Source outside Repository Scope. Run validation there so mutable outputs cannot pollute the configured Repository Store. Launch fresh direct-child Validation Agents against the stable exact Published Delivery Head set and declared Validation Sources. Each assignment and its resulting cross-repository evidence bind every repository-backed Validation Source it uses to that recorded exact commit. Assign every mandatory cross-repository Validation Obligation to exactly one agent. Compatible obligations may share one Validation Agent only when they execute through the same compatible Validation Source, with one recorded exact source commit and coherent setup and evidence ownership. Each agent follows the declared prerequisites, method, scenario, expected result, and evidence format. It produces evidence, changes no product code, and makes no whole-ticket Spec judgment.

After every mandatory obligation has current passing evidence, use the `code-review` skill in **Spec only** mode over the complete changed target set. Every Repository Target carries the unchanged Authority input from step 2, together with all seams, evidence, and proposals. Record Advisory findings. Route attributable in-scope Blocking findings to the affected Implementation Agents. After a changed influencing delivery head, refresh its repository validation and fresh Standards review using that same Authority input. A changed influencing delivery head or exact Validation Source commit invalidates only dependent cross-repository evidence and the Bundle Spec result. Rerun every invalidated obligation with fresh Validation Agents before another fresh full-bundle Spec review. Repeat until the result has no Blocking finding or a Specification Contradiction, Material Design Opportunity, or another genuine authority boundary applies.

**Complete when:** every declared obligation and fresh Bundle Spec result passes against one current exact delivery-head and Validation Source commit set and the Authority input from step 2; all evidence made stale by a changed influencing delivery head, Validation Source commit, or Authority input has been refreshed while evidence with an unchanged dependency set remains current, or planned human verification has entered the [human-boundary branch](HUMAN-BOUNDARY.md).

## 9. Hand off idempotently

Re-read the ticket, claim, Published Delivery Heads, proposals, feedback, and current evidence. Return any drift to its earliest invalidated prerequisite. Mark every verified proposal ready and re-read it. Build `coordinate-delivery:<canonical ticket reference>:<SHA-256 of sorted Repository ID=exact head lines>`.

Reuse a matching handoff; otherwise append one note recording every base, head, branch, proposal, validation and review result, Advisory finding, human action, merge/rollout order, unchanged delivery, preserved state, and limitation. Include no local path, credential, or secret. The complete handoff is the final Execution Checkpoint, so create no duplicate checkpoint note. Apply only missing final effects in order: replace `ready-for-agent` with exactly `ready-for-human`, release the Workflow Identity claim, re-read both effects, and leave the ticket open.

**Complete when:** exactly one matching handoff exists, every proposal is ready at its recorded head, and the ticket is open, unassigned, and carries exactly `ready-for-human` among Routing Labels.

Report the ticket, host-local worktree disposition, fixed bases and heads, validation, proposals, review outcomes, and final Work Tracker state.
