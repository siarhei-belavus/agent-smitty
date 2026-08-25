---
name: implement
description: "Implement repository deliveries from authoritative specs or tickets. Use for standalone implementation and for one repository delivery narrowed by coordinate-delivery."
---

Implement the work described by the user in the authoritative spec or tickets.

Read [delivery records](../federated-workflow/DELIVERY-RECORDS.md) before resolving the assignment. When authority includes a Work Tracker Delivery Ticket, Task, or Bug, read [Work Tracker context assembly](../federated-workflow/WORK-TRACKER-CONTEXT-ASSEMBLY.md) and assemble Delivery Context before accepting the assignment.

## Resolve the assignment

Classify the assignment before changing a checkout.

- When the user authorizes one or more writable Repository Deliveries directly, read [Standalone assignments](STANDALONE.md).
- When `coordinate-delivery` supplies one complete narrowing assignment for exactly one Repository Scope entry, read [Coordinator narrowing](COORDINATOR-NARROWED.md).

For Work Tracker authority, use the configured artifact mapping rather than provider issue type inference. Require and read a parent only for mapped derived delivery. A standalone Task or Bug may have no parent or Authority Source when its own content passes the contract's self-contained check. Continue only with a `Complete` Delivery Context; report `Incomplete` or `Ambiguous` at the applicable clarification, planning, or human boundary without switching profiles.

Every writable Repository Delivery must supply or resolve:

- Repository ID and Repository Reference;
- writable checkout or Execution Worktree and its branch;
- exact launch commit or Fixed Review Base;
- repository-specific required outcome;
- authoritative sources and repository instructions;
- complete Settled Seam records and their test approaches;
- repository-owned Validation Obligations and validation commands.

A Fixed Review Base is the exact starting commit against which a Repository Delivery is implemented and reviewed.

Read-only context and validation repositories remain outside writable scope. Missing authority, a worktree that disagrees with the assignment, or a required change to approved scope, acceptance behavior, or a Settled Seam is a **Material contradiction**. Preserve safe work and return the conflicting sources. Authority comes from the assignment, not inference.

**Complete when:** the writable scope, authority, every required delivery field, and any requested Delivery Context are complete, or a Material contradiction or explicit Context Assembly stop has been returned without repository mutation.

## Prepare each delivery

Validate that the writable path belongs to the Repository Reference and that its starting revision agrees with the supplied launch commit or Fixed Review Base. After complete Context Assembly stops at canonical pointers, perform configured Domain Orientation and read that repository's instructions, routed canonical context, ADRs, validation commands, and nearest relevant prior art. Do not use one repository's instructions or validation as authority for another.

Record the Repository ID, writable path, Fixed Review Base, authoritative sources, complete Settled Seams, test approaches, Validation Obligations, and validation commands before editing.

Use the authorized isolated writable checkout. Classify existing changes against the assignment. Preserve unrelated content and return a blocker when it cannot be isolated without changing user work.

**Complete when:** every writable path, starting revision, instruction source, seam, test approach, Validation Obligation, and validation command is verified for its own repository, and unrelated content is either isolated or reported as a blocker.

## Implement through TDD

Work in vertical slices. Use the `tdd` skill with the authoritative sources and complete Settled Seam records, including each seam's owning module, caller-visible interface, location, status, observable behavior, test approach, and nearest prior art.

Run focused tests and typechecking during the work. After each coherent green iteration, commit focused changes to that delivery's branch. Each commit contains changes from one repository only.

**Complete when:** every authorized outcome is implemented in committed green slices, classified unchanged, or represented by an exact blocker or Material contradiction.

## Validate the exact result

Establish a **Clean delivery state** before final validation: every assignment-owned change is committed and the worktree is clean. Isolate unrelated or uncommitted content safely, or return a blocker with the exact status. Validation from a dirty worktree is not attributable to `HEAD`.

Run the full repository-owned validation suite after implementation. Record every command, outcome, and relevant limitation against the exact commit it validated. Resolve the Exact local HEAD and clean-worktree status after validation. A changed head or worktree makes prior validation evidence stale and requires a refresh.

Return one **Repository Delivery result** for each writable entry with:

- Repository ID, Repository Reference, writable path, and branch;
- Fixed Review Base and Exact local HEAD;
- changed, unchanged, or blocked outcome;
- Clean delivery state;
- focused commits;
- repository validation commands and outcomes;
- remaining blockers or Material contradiction details.

**Complete when:** every authorized Repository Delivery satisfies its assignment's completion requirements and the requested result has been returned.
