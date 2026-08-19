---
name: coordinate-delivery
description: "Coordinate one agent-ready ticket through its complete federated delivery and human handoff."
disable-model-invocation: true
---

Coordinate `/coordinate-delivery <ticket reference>` as one fail-closed happy path.

Use repository-owned bindings for every provider operation. Keep provider commands, credentials, and account identity out of this skill. At any gate, report the exact observed obstacle and perform no later mutation when required authority or evidence is missing. Never merge a Review Proposal, push a protected Base Branch, or close the ticket.

## 1. Establish authority

Resolve the ticket only through the configured Ticket Origin Repository and read its applicable `AGENTS.md`, Work Tracker, Routing Label, Domain Orientation, and Code Host bindings. Read the complete ticket, comments, and provider-native dependencies.

Proceed only when the ticket is open, unblocked, unassigned, and has exactly the configured `ready-for-agent` Routing Label. Resolve the authenticated provider user as the **Workflow Identity**, assign only that identity, then re-read the ticket and verify the exact claim.

**Complete when:** the ticket remains open and ready for an agent, every blocker is resolved, and its sole assignee is the Workflow Identity.

## 2. Validate the delivery contract

Read [`../PLANNING-ARTIFACT-CONTRACTS.md`](../PLANNING-ARTIFACT-CONTRACTS.md) completely and validate the ticket as a public executable artifact. Require:

- a complete minimal set of Repository References;
- Context Scope whose pointers resolve through those references;
- a non-empty Repository Scope whose entries each resolve to one Repository Reference and state a repository-owned outcome;
- every applicable Settled Seam, repository-local Validation Obligation, and Cross-Repository Validation Obligation with its required fields;
- no material conflict among the ticket, its dependencies, current user direction, canonical context, or accepted decisions.

For every referenced repository, read the applicable repository instructions, Code Host binding, canonical context, and ADRs. Validate the remote, configured Base Branch, and non-destructive provider access against the Repository Reference.

**Complete when:** every contract record and context pointer is present, consistent, readable, and owned by a validated repository.

## 3. Prepare repository worktrees

Create a new run-specific persistent worktree root outside existing user checkouts. Fetch each configured Base Branch from its declared remote and pin its fresh exact commit. Never derive the delivery base from a pre-existing local branch.

For every Repository Scope entry, create one clean isolated worktree at that pinned base. Create a new uniquely named delivery branch only when the entry's required outcome requires changes; keep validation-only or explicit no-change entries at the pinned commit. Keep read-only repositories outside writable scope. Record Repository ID, Repository Reference, persistent worktree path, branch when applicable, and fixed base.

**Complete when:** every Repository Delivery has one clean isolated worktree whose `HEAD` equals its recorded fixed base, and no existing user checkout or branch was changed.

## 4. Execute flat deliveries

Classify every Repository Scope entry by its required outcome. Start exactly one direct-child implementation agent only for each Repository Delivery that requires changes. Give it a Coordinator-narrowed `/implement` assignment containing only:

- its Repository ID, Reference, Execution Worktree, delivery branch, and fixed base;
- the ticket and other authoritative sources;
- its repository-owned outcome, complete applicable Settled Seams, and Validation Obligations;
- the repository instructions and validation commands discovered for that repository.

Require the child to follow `/implement`'s public Coordinator-narrowed contract, start no child agents or reviewers, and return exactly one Repository Delivery result. The coordinator alone owns publication, Review Proposals, Work Tracker changes, and bundle review.

For every validation-only or explicit no-change entry, record its exact stable base and head and satisfy its applicable Validation Obligations without an implementation agent. Wait for every implementation result and verify it against its assigned worktree and fixed base. A delivery expected to change but returning no diff is unchanged; record it and exclude it from publication and proposals.

**Complete when:** every scope entry is attributable to either one implementation result or one coordinator-owned validation record, every changed worktree is clean at its reported exact local head, and every repository validation result is bound to that head.

## 5. Review exact heads

For every changed Repository Delivery, verify the fixed-base diff and repository validation evidence at the reported exact head. Invoke `/code-review` in **Standards only** mode with one fixed Repository Target per changed repository, its authoritative sources, settled seams, and exact-head validation evidence.

Record Advisory findings for handoff. The bundle has one correction/recheck round across Steps 5 and 7. When Standards has an attributable Blocking finding within authorized implementation, route it to the affected existing Implementation Agent, then refresh repository validation and Standards for every changed head. Any changed head makes its prior validation, review, and downstream evidence stale. Continue only when the fresh Standards result has no Blocking finding. If a Blocking persists or its correction requires a material scope, acceptance, seam, or decision change, report the exact obstacle and stop further mutation.

**Complete when:** every changed exact head has current repository validation evidence and a fresh passing Standards result.

## 6. Publish Review Proposals

Using each changed repository's Code Host binding, publish only its delivery branch and verify the remote branch resolves to the intended exact head. Create exactly one Draft Review Proposal from that branch to the configured Base Branch and keep it Draft until bundle validation and Spec review pass. Re-read its source, target, draft state, and head revision. Unchanged repositories receive neither a published delivery branch nor a Review Proposal.

**Complete when:** each changed Repository Delivery has one published exact head and exactly one verified Draft Review Proposal at that head, with no protected Base Branch changed.

## 7. Validate the bundle

Run every declared Cross-Repository Validation Obligation against the published exact heads, using its named Validation Source, prerequisites, method, scenario, expected result, and evidence format. Record commands, outcomes, and limitations against the complete head set.

Then invoke `/code-review` in **Spec only** mode once over the complete changed Repository Target set. Supply the ticket and other authoritative sources, all settled seams, repository and cross-repository validation evidence, and verified Review Proposals. Record Advisory findings for handoff.

When Bundle Spec has an attributable Blocking finding and the correction/recheck round remains, route it to each affected existing Implementation Agent. Every changed head requires fresh repository validation and Standards, exact-head republication and Review Proposal verification, complete cross-repository validation, and a fresh Bundle Spec review. Continue only when the fresh Bundle Spec result has no Blocking finding. If the round is already spent, a Blocking persists, or correction requires a material scope, acceptance, seam, or decision change, report the exact obstacle and stop further mutation.

**Complete when:** the published exact-head bundle satisfies every declared validation obligation and has a fresh passing Bundle Spec result.

## 8. Hand off idempotently

Re-read the ticket immediately before handoff and require the claim established in Step 1 to remain exact. Mark every verified Review Proposal ready for human review through its Code Host binding and re-read its state. Build the deterministic handoff key `coordinate-delivery:<canonical ticket reference>:<SHA-256 of the sorted Repository ID=exact head lines>`.

Search existing ticket notes for that key. When absent, append one handoff note containing:

- every fixed base, exact published head, branch, and Review Proposal;
- repository-local and cross-repository validation evidence;
- Standards and Bundle Spec outcomes, including Advisory findings;
- required human actions and the explicit Review Proposal merge and rollout order;
- unchanged Repository Scope entries and material limitations.

When the key is already present, verify its recorded bundle matches instead of adding another note. Apply only missing final-state mutations: remove the Workflow Identity assignment, replace `ready-for-agent` with exactly the configured `ready-for-human` Routing Label, and leave the ticket open. Re-read ticket and note state.

**Complete when:** exactly one matching handoff note exists and the ticket is open, unassigned, and carries exactly `ready-for-human` among Routing Labels.

Report the ticket, persistent worktree root, every fixed base and exact head, validation evidence, Review Proposal links, review outcomes, and final Work Tracker state.
