# Federated Planning Authority

This is the shared contract for carrying configured repository and domain authority through planning, specification, delivery-ticket, and triage artifacts. A skill consumes it when producing or assessing one of those artifacts; it must not depend on prior chat or hidden invocation history.

## Source authority

Read `docs/agents/issue-tracker.md` and `docs/agents/domain.md` when present. The former selects the Work Tracker and its operations; the latter selects canonical domain sources and artifact owners. Do not infer either authority from a Git remote or checkout layout.

Transform only authority present in the supplied conversation, accepted planning Resolution, specification, ticket, canonical context, ADR, or configured binding. Do not introduce a repository, context, seam, validation method, or decision absent from those sources. A missing material descriptor or unsettled choice returns to discovery, planning, or the user instead of being guessed.

Repository References make sources resolvable; they grant neither write authority nor a delivery obligation. Each reference contains:

- Repository ID;
- remote;
- Base Branch.

Context Scope contains Repository-qualified Context Pointers of the form `<Repository ID>:<repo-relative path>`. Every referenced Repository ID must have a Repository Reference. When no canonical context applies, use `None — <reason>`; never leave the section empty or use `None` to bypass unresolved product language.

## Full-fidelity planning decisions

Effective planning language combines the oriented Canonical Context Documents with accepted Domain Model Deltas from the current effort. Promote every relevant accepted delta without semantic reduction. As applicable, retain:

- owning Repository ID and Canonical Context Pointer;
- add, change, or supersede operation;
- exact terms and definitions;
- relationships, invariants, boundaries, scenarios, and counterexamples;
- rationale and rejected alternatives;
- complete architecture-decision rationale when the ADR threshold was met;
- originating decision provenance;
- canonical documentation obligations;
- contradiction conditions that require escalation rather than reinterpretation.

A summary or pointer may index the source, but it cannot replace this payload. Repository Scope must authorize every required canonical documentation change in its owner, including a documentation-only Repository Delivery when no code change belongs there.

## Specification contract

A specification has these top-level sections in order:

1. Problem Statement
2. Solution
3. User Stories
4. Repository References
5. Context Scope
6. Implementation Decisions
7. Testing Decisions
8. Out of Scope
9. Further Notes

Repository References is the complete confirmed solution-level set. A specification has no Repository Scope and grants no write authority. Repository-owned Implementation Decisions identify their Repository IDs.

Testing Decisions is the sole owner of repository-local and cross-repository settled seams; do not add a duplicate top-level Cross-Repository Seams section. Each settled seam records:

- owning module and Repository ID;
- providers and consumers by Repository ID;
- caller/test-visible interface;
- location;
- status: `new`, `changed`, or `unchanged`;
- observable behavior;
- validation obligation owner, Validation Source, prerequisites, method, and required evidence as applicable;
- selected repository-native test approach;
- nearest prior art.

## Executable delivery-ticket contract

Real Work Tracker and Local Markdown tickets use the same semantic contract, with these top-level sections in order:

1. Parent
2. What to build
3. Acceptance criteria
4. Repository References
5. Repository Scope
6. Context Scope
7. Cross-Repository Seams
8. Blocked by

Use `None — <reason>` for an inapplicable Parent, Cross-Repository Seams, or Blocked by section; do not omit the section.

Each ticket is a vertical tracer bullet and receives only the minimal complete Repository References required by its writable scope, Context Scope, repository-backed Validation Sources, and other explicit read-only authorities.

Repository Scope is a non-empty writable subset of Repository References. Each entry identifies its required outcome, relevant repository-local settled seams, and repository-owned validation obligations and produces one Repository Delivery. Read-only context, validation, and decision sources stay in Repository References but outside Repository Scope. There is no separate Repository Outcomes section.

Context Scope is the minimal relevant subset of the source specification's Context Scope and carries every relevant accepted Domain Model Delta with provenance and documentation obligations.

Cross-Repository Seams contains each seam the ticket creates, changes, or materially relies on. Preserve the complete applicable settled-seam fields from Testing Decisions and keep each Cross-Repository Validation Obligation with its owning seam.

Dependencies use the Work Tracker's native blocking relationship when available and its configured fallback otherwise. Apply the configured `ready-for-agent` Routing Label only after the complete executable contract exists and all blockers and labels are represented consistently.

Portable repository descriptors, Repository-qualified Context Pointers, canonical artifact pointers, and settled seam locations are durable contract fields, not stale implementation-path guidance.

## Executable Agent Brief contract

An Agent Brief is a durable Work Tracker comment with these sections in order:

1. What to build
2. Acceptance criteria
3. Repository References
4. Repository Scope
5. Context Scope
6. Cross-Repository Seams
7. Out of scope
8. Blocked by

It follows the same Repository Reference, writable Repository Scope, Context Scope, full-fidelity decision, seam, validation, and dependency rules as an executable delivery ticket. Current behavior, desired behavior, and durable key-interface guidance belong inside What to build rather than becoming duplicate top-level contract sections.

The mapped `ready-for-agent` Routing Label asserts that this complete executable Agent Brief already exists. A direct maintainer state override can skip discovery or grilling, but it cannot skip or weaken the brief. Post and re-read the complete brief before applying the label. If source authority is insufficient to write it without invention, keep the item out of `ready-for-agent` and route the missing decisions or information explicitly.
