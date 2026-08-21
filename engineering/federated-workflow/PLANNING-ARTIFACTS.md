# Planning artifact contracts

Every record must be verifiable through the published artifact and resulting Work Tracker state. Prior chat, hidden invocation history, checkout layout, and private prompt structure are not authority.

## Source authority

Read `docs/agents/issue-tracker.md` and `docs/agents/domain.md` when present. They select the Work Tracker, Domain Orientation, canonical sources, and artifact owners; never infer those authorities from Git remotes or checkout layout.

Transform only repositories, contexts, seams, validation methods, and decisions present in supplied conversation, accepted planning Resolutions, canonical context, ADRs, configured bindings, or another authoritative source artifact. A missing material record or unsettled choice returns to discovery, planning, or the user instead of being invented.

## Shared semantic records

### Repository Reference

A Repository Reference makes one repository resolvable without granting write authority or creating a Repository Delivery. It contains:

- Repository ID;
- remote;
- Base Branch.

### Context Scope

Context Scope contains the complete artifact-relevant set of:

- Repository-qualified Context Pointers in the form `<Repository ID>:<repo-relative path>`; and
- accepted [Domain Model Deltas](../domain-modeling/DOMAIN-MODEL-DELTA.md) that govern the artifact.

Every pointer and delta owner resolves through a Repository Reference. Use `None — <reason>` only when no canonical context applies; never use it to bypass unresolved product language.

Effective planning language is the ordered combination of oriented Canonical Context Documents and accepted Domain Model Deltas from the current effort. Promote every relevant delta without semantic reduction.

### Settled Seam

A Settled Seam records:

- owning module and Repository ID;
- providers and consumers by Repository ID;
- caller/test-visible interface;
- location;
- status: `new`, `changed`, or `unchanged`;
- observable behavior;
- selected repository-native test approach;
- nearest prior art; and
- each applicable Validation Obligation.

A cross-repository seam uses the same record with providers or consumers in different repositories. Its Validation Obligations stay with the seam rather than moving to a separate validation section.

### Validation Obligation

A Validation Obligation records the behavior to prove, its single owner, affected Repository Deliveries, Validation Source, prerequisites, method, scenario, expected result, and required evidence. An unchanged repository may be a read-only Validation Source. Creating or changing its validation entrypoint, assertions, or setup requires a Repository Scope entry for that repository.

### Repository Scope entry

A Repository Scope entry authorizes writes to exactly one referenced Repository ID and produces one Repository Delivery. It records:

- required repository-owned outcome;
- applicable repository-local Settled Seams; and
- repository-owned Validation Obligations.

Repository Scope is a non-empty writable subset of Repository References in every executable delivery artifact. Read-only context, validation, and decision sources remain references outside the scope. A required canonical documentation change places its owning repository in scope, including a documentation-only Repository Delivery when no code change belongs there.

### Dependency

A dependency is a durable Work Tracker reference represented through the configured native blocking relationship or fallback. When an artifact requires the field but has no dependency, use its artifact-specific `None — <reason>` form rather than omitting it.

## Composition invariants

- A specification carries the complete confirmed solution-level Repository References, grants no write authority, and has no Repository Scope. Its Testing Decisions are the sole owner of all repository-local and cross-repository Settled Seams.
- An executable ticket or Agent Brief carries the minimal complete Repository References required by its writable scope, Context Scope, repository-backed Validation Sources, and explicit read-only authorities.
- Every executable artifact has a non-empty Repository Scope, and every scope entry resolves through its Repository References.
- Ticket creation narrows Context Scope and Settled Seams from source authority; it does not perform new discovery or design.
- Every relevant Domain Model Delta, architecture decision, Settled Seam, Validation Obligation, and provenance record survives transformation at full fidelity.
- Portable repository descriptors, Repository-qualified Context Pointers, canonical artifact pointers, and Settled Seam locations are durable contract data, not stale implementation-path guidance.
- Real Work Tracker and Local Markdown adapters preserve the same semantic records. Provider differences affect publication and relationship operations, not artifact meaning.
- A Routing Label that asserts execution readiness may be applied only after the complete public executable artifact and dependency state satisfy these invariants.
