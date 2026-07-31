---
name: implement
description: "Implement one or more Repository Deliveries from a spec or tickets, or one Coordinator-narrowed Repository Delivery in its supplied Execution Worktree."
disable-model-invocation: true
---

Implement the work described by the user in the authoritative spec or tickets.

## Invocation modes

Classify the invocation before changing files.

### Standalone assignment

A Standalone assignment accepts one or more Repository Deliveries. Treat the existing single-repository invocation as the one-element case.

Use the supplied Repository References and non-empty Repository Scope as the authorized assignment. Each writable entry must identify its Repository ID, Repository Reference, required outcome, repository-local validation obligations, settled seams, and writable checkout or worktree. Read-only context and validation repositories are not writable scope.

When the user supplies only the current repository and no federated ticket contract, preserve the existing behavior: use that repository as the single Repository Delivery and the supplied spec, ticket, or conversation as authority.

### Coordinator-narrowed assignment

A Coordinator-narrowed assignment must explicitly name exactly one named Repository Scope entry and one supplied Execution Worktree. It must also provide the Repository ID and Reference, exact launch commit or fixed review base, repository-specific outcome, authoritative sources, settled seams, and validation obligations.

Validate that the supplied Execution Worktree belongs to that Repository Reference and starts from the supplied commit. Change only that Execution Worktree. Do not resolve, prepare, or modify another Repository Scope entry.

Do not start reviewers or any other child agent. Do not publish a branch. Do not create or update a Review Proposal. Do not change Work Tracker state. The Coordinator owns those actions.

If the assignment is missing required authority, disagrees with the supplied worktree, or would require changing approved scope, acceptance behavior, or a settled seam, stop affected work and return a **Material contradiction** with the conflicting sources. Do not invent or expand authority.

## Prepare every Repository Delivery

Before making changes, create one delivery record per writable Repository Scope entry and capture:

- **Repository ID** and validated writable path;
- **Fixed review base** as an exact commit SHA, resolving the current `HEAD` before changes when no exact launch commit was supplied;
- authoritative sources and the complete settled seam records;
- repository-owned validation commands and their nearest prior art.

Do not use one repository's instructions, tests, or validation as authority for another. Preserve existing user work by using the supplied worktree or another isolated writable checkout within the assignment.

Do not mix assignment-owned changes with unrelated worktree content. If the supplied worktree already contains changes, classify them against the assignment before editing. Preserve unrelated content and report a blocker when it cannot be isolated without changing user work.

Use the complete settled seam set and test approaches recorded in the supplied specification, tickets, or resolved design decisions. Do not ask the user to reconfirm them.

When invoked standalone without a settled seam set, identify the complete set of existing, changed, and new seams the solution spans. For each seam, propose the smallest faithful repository-native test approach and its nearest prior art. If materially different caller-facing ownership, interface, seam, or contract choices remain possible, run `/codebase-design` before proposing the set. Ask the user to confirm the complete set and proposed approaches once; the confirmed seams are settled.

## Implement and validate

Work in vertical slices within each Repository Delivery. Invoke `/tdd` with the authoritative sources and complete settled seam records, including each seam's owning module, caller/test-visible interface, location, status, observable behavior, selected test approach, and nearest prior art.

Run typechecking and focused tests regularly. After each coherent green iteration, commit focused work to that delivery's current branch. Never commit changes from another repository in the same commit.

Before final validation, establish a **Clean delivery state**: every assignment-owned change is committed and the worktree is clean. If unrelated or uncommitted content remains, do not attribute validation to `HEAD`; isolate it safely or return a blocker with the exact status. Run the full repository-owned validation suite once implementation is complete in each changed repository. Record every command, outcome, and relevant limitation against the exact commit it validated. Resolve and record the **Exact local HEAD** and clean-worktree status after validation; if the HEAD or worktree state changes, the prior validation evidence is stale and must be refreshed.

## Finish the selected mode

For a Coordinator-narrowed assignment, return exactly one Repository Delivery result and stop. The result contains:

- Repository ID;
- Execution Worktree;
- Fixed review base;
- Exact local HEAD;
- Clean delivery state;
- focused commits;
- Repository validation commands and outcomes;
- remaining blockers or Material contradiction details;
- confirmation that no Code Host publication or Work Tracker change was performed.

For a Standalone assignment, invoke `/code-review` once with all fixed Repository Targets, both axes selected, the authoritative sources, and the same settled seam and test-approach records. Fix Blocking findings only in affected Repository Deliveries, validate and commit those changes, and repeat the required review against the original fixed bases. Escalate any finding whose resolution would change scope, acceptance behavior, or a settled seam.

Changed heads require refreshed repository validation and fresh Standards review before the next whole-bundle Spec review. Finish only when every latest committed head passes full repository validation and the latest selected review has no Blocking findings.

Standalone `/implement` does not publish branches, create or update Review Proposals, or change Work Tracker state unless the user gives that explicit authority separately.
