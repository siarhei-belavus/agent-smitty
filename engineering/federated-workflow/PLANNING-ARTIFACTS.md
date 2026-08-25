# Planning artifact contracts

Read [delivery records](DELIVERY-RECORDS.md), [provider concepts](PROVIDER-CONCEPTS.md), and [domain orientation](DOMAIN-ORIENTATION.md) before applying these contracts.

Every record must be verifiable through the published artifact and resulting Work Tracker state. Prior chat, hidden invocation history, checkout layout, and private prompt structure are not authority.

## Source authority

Read `docs/agents/issue-tracker.md` and `docs/agents/domain.md` when present. They select the Work Tracker, Domain Orientation, canonical sources, and artifact owners; never infer those authorities from Git remotes or checkout layout.

Transform only repositories, contexts, seams, validation methods, and decisions present in supplied conversation, accepted planning Resolutions, canonical context, ADRs, configured bindings, or another authoritative source artifact. A missing material record or unsettled choice returns to discovery, planning, or the user instead of being invented.

## Planning records

### Context Scope

Context Scope contains the complete artifact-relevant set of:

- Repository-qualified Context Pointers; and
- accepted [Domain Model Deltas](../domain-modeling/DOMAIN-MODEL-DELTA.md) that govern the artifact.

Every pointer and delta owner resolves through a Repository Reference. Use `None — <reason>` only when no canonical context applies; never use it to bypass unresolved product language.

Effective planning language is the ordered combination of oriented Canonical Context Documents and accepted Domain Model Deltas from the current effort. Promote every relevant delta without semantic reduction.

### Dependency

A dependency is a durable Work Tracker reference represented through the configured native blocking relationship or fallback. When an artifact requires the field but has no dependency, use its artifact-specific `None — <reason>` form rather than omitting it.

## Composition invariants

- A specification carries the complete confirmed solution-level Repository References, grants no write authority, and has no Repository Scope. Its Testing Decisions are the sole owner of all repository-local and cross-repository Settled Seams.
- An executable ticket or Agent Brief carries the minimal complete Repository References required by its writable scope, Context Scope, repository-backed Validation Sources, and explicit read-only authorities.
- Ticket creation narrows Context Scope and Settled Seams from source authority; it does not perform new discovery or design.
- Every relevant Domain Model Delta, architecture decision, Settled Seam, Validation Obligation, and provenance record survives transformation at full fidelity.
- Portable repository descriptors, Repository-qualified Context Pointers, canonical artifact pointers, and Settled Seam locations are durable contract data, not stale implementation-path guidance.
- A Routing Label that asserts execution readiness may be applied only after the complete public executable artifact and dependency state satisfy these invariants.
