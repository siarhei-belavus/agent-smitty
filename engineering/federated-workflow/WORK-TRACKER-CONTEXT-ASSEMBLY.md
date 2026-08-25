# Work Tracker context assembly

Read [provider concepts](PROVIDER-CONCEPTS.md) and [domain orientation](DOMAIN-ORIENTATION.md) before applying this contract.

Work Tracker Context Assembly is the provider-neutral read contract for planning and delivery artifacts. It creates one ephemeral, read-only Context Pack for one workflow session. The requesting workflow selects one profile and continues only when assembly returns `Complete`.

Provider bindings own representation and operations. This contract owns artifact meaning, Authority Sources, profile contents, Resolution succession, reconciliation semantics, result classification, and the handoff to Domain Orientation. Real Work Trackers and Local Markdown preserve the same meaning.

## Artifact roles and provenance

Artifact roles are independent of provider types. A binding may distinguish them with native types, labels, relationships, or durable body conventions.

- A **Map** is the durable index for one planning effort. It may also contain the complete Specification.
- A **Decision Ticket** resolves one decision and belongs to one Map through the configured relationship or fallback.
- A **Specification** is durable solution-level planning authority. It may use zero or more Maps as sources.
- A **Delivery Ticket** is executable work derived from planning authority. A binding may require a parent for this role.
- A **Task** or **Bug** may be standalone executable work. It needs no parent or planning source when its own authoritative content is self-contained.

An **Authority Source** is an explicit permanent reference from actionable Work Tracker work to a Specification, Map, other planning artifact, or canonical repository document that governs it. The configured native relationship may carry that reference. Titles, timestamps, authors, and textual similarity establish neither role nor provenance.

A Decision Ticket's configured owning Map relationship is a required Authority Source. It must resolve to exactly one permanent Map reference. No owning Map or an unreadable permanent reference is `Incomplete`; more than one owning Map is `Ambiguous`.

An **Effective Resolution** is the recognized accepted Resolution content that remains after following explicit `Supersedes` and `Supplements` references.

Every artifact records zero or more Authority Sources. An artifact that has sources preserves every one as a permanent reference. Two source-free forms are valid:

- A Specification may have no upstream Map or planning artifact when its own durable body completely materializes the settled problem, solution, accepted implementation and testing decisions, Repository References, Context Scope, and out-of-scope boundaries. Its permanent identity becomes the provenance root.
- A standalone Task or Bug may have no planning source when its own durable body contains complete expected behavior, scope, acceptance criteria, and validation expectations.

Missing required content makes either form `Incomplete`. A `None` Authority Sources record never excuses an omitted source that the artifact relies on.

These shapes are equivalent inputs to the model:

```text
Map = Specification
`-- Delivery Tickets

Map --> Specification
          `-- Delivery Tickets

Self-contained Task or Bug
`-- no Specification or Map
```

A Specification may reference multiple Maps. Assembly retains the permanent provenance of every visited artifact and accepted Resolution.

Wayfinder is optional. Supported planning paths include `grill-me` to `to-spec` to `to-tickets`, `to-spec` to `to-tickets`, and direct `to-tickets` from settled authority. No path invents a Map merely to continue.

## Assembly rules

Use the repository-owned Work Tracker binding's manual read recipe or its optional helper. The helper is an optimization. Its absence never changes the result or makes the manual recipe incomplete.

For the requested profile:

1. Resolve exactly one compatible active root through the binding's artifact mapping and permanent references. No compatible root returns `Incomplete`; more than one returns `Ambiguous`. Never switch to another profile.
2. Read every required authoritative body and every human-visible comment. Follow every provider pagination mechanism to completion, including pagination on relationships, children, search results, and comments.
3. Follow explicit Authority Sources and configured role relationships. Treat a Decision Ticket's configured owning Map relationship as an Authority Source. Retain each permanent reference and the full Work Tracker or Local Markdown payload it proves. For a canonical repository document, retain and validate its Repository-qualified Context Pointer under the Domain Orientation boundary below; loading that document is not part of Context Assembly.
4. Resolve accepted Resolution succession, then include every effective decision required by the selected profile in full. Context limits never permit omission, filtering, or lossy summary.
5. Remove only provider transport metadata. Keep artifact identity, role, status, routing, claim and blocker state when the profile requires them, permanent references, authoritative bodies, comments, and Resolution text.
6. Classify the result. Return the requested Context Pack only with its explicit result.

The Context Pack is read-only. Do not persist it as authority, use it as a cache, or mutate Work Tracker state while assembling it. If the complete payload cannot fit safely, return `Incomplete` and stop for a planning split or lossless handoff.

## Public profiles

The complete public profile set is exactly Map Context, Decision Context, and Delivery Context. Profile selection follows workflow intent rather than provider issue type. Review reuses the profile of the authority under review. There are no separate spec, task, bug, review, full, context, or auto profiles.

### Map Context

Use Map Context for initiative-wide orientation, planning, and Wayfinder navigation. It contains:

- the complete Map body and human-visible comments;
- every effective Resolution from the Map in full, with permanent provenance;
- open children at low resolution, including permanent identity, role, status, claim, and blocker state;
- dependency state; and
- the current Wayfinder frontier.

### Decision Context

Use Decision Context to create, revise, or review a Decision Ticket or Specification. It contains:

- the complete active Decision Ticket or Specification body and human-visible comments;
- its permanent identity, role, blocker state, and Authority Sources; and
- every complete Map Context reachable through those explicit Authority Sources.

For a Decision Ticket, Decision Context always contains the Map Context of its one configured owning Map. A source-free Specification can produce `Complete` Decision Context without Map Context only when it passes the complete settled-authority check above. A Map that is also the Specification remains one artifact. Its Map role supplies Map Context without a self-reference. Include its body and comments once while retaining both roles.

### Delivery Context

Use Delivery Context for implementation and delivery review of a Delivery Ticket, Task, or Bug. It contains:

- the complete active artifact body and human-visible comments;
- its permanent identity, role, claim, routing, blocker state, and Authority Sources;
- every explicit Specification and other planning source, including their human-visible comments;
- every source Map and all effective decisions from every source Map in full;
- resolved blocker authority; and
- the Context Scope's canonical repository pointers.

Require a parent only when the binding maps the active artifact to derived delivery. A standalone Task or Bug with no parent or Authority Source may still produce a complete Delivery Context when its own content passes the self-contained authority check.

#### Resolved blocker authority

Resolved blocker authority is the complete blocker closure that governs whether the active delivery can proceed. Here, resolved means that every authority record and reference in the closure has been resolved, not that every blocker has provider state resolved. Starting at the active artifact, follow every configured `blocked by` relationship to its blocker, then repeat from each blocker. Include only edges directed into the active artifact through that closure, not artifacts that the active artifact blocks.

The Work Tracker binding normalizes provider-native dependency direction to `blocker -> blocked`. Follow every relationship and comment page to completion. Record each blocker once by permanent reference with:

- every normalized edge through which it participates in the closure;
- its complete authoritative body and human-visible comments;
- its provider-mapped open or resolved state and permanent resolution reference when the provider exposes one; and
- every explicit Authority Source reachable from it.

Assemble reachable governing Specifications, Maps, and effective decisions through the ordinary Authority Source rules. Merge them into the Delivery Context by permanent reference rather than nesting a second planning-source assembly under each blocker. An empty blocker closure is valid.

The result is `Incomplete` when any blocker edge, page, permanent reference, body, comment set, or resolution state is missing or unreadable, or when a declared Authority Source cannot be resolved. A fully read blocker with valid open state remains part of a `Complete` Delivery Context. The configured frontier and eligibility rules use that state to prevent execution until the dependency resolves. The result is `Ambiguous` when direction cannot be normalized, the blocker graph is cyclic, records disagree for one permanent blocker reference, resolution state conflicts, or reachable governing authority conflicts.

## Results

Assembly returns exactly one result. Classify recognized Resolution succession before general missing-material checks, so the variants remain disjoint:

- `Complete` means the requested root is unique; every required Work Tracker or Local Markdown body, comment page, relationship, permanent reference, effective Resolution, and profile field is present; every canonical repository Authority Source has one valid Repository-qualified Context Pointer; and the assembled records are internally consistent.
- `Incomplete` means required material is missing, unreadable, unresolved, only partly paginated, or too large to carry without loss. It also covers an absent compatible root. A recognized succession reference is excluded from this variant.
- `Ambiguous` means more than one root fits, authority conflicts, a recognized `Supersedes` or `Supplements` reference is broken or cyclic, succession has competing effective interpretations, or a claimed supplement conflicts with effective authority.

Only `Complete` permits the requesting workflow to continue. `Incomplete` and `Ambiguous` name the missing or competing permanent references and stop visibly at the workflow's clarification, planning, setup, or human boundary.

## Local Markdown read recipe

Local Markdown is a provider representation of the same contract. Use this complete manual recipe when no real Work Tracker binding applies:

1. Resolve the requested file to one permanent reference made from the portable Repository ID, repository-relative path, and heading anchor when the referenced record is a section. Recognize its role only from the explicit document contract, role field, headings, and relationships written by the producing workflow. A missing compatible role is `Incomplete`; conflicting roles or roots are `Ambiguous`.
2. Read the entire root file and every linked artifact file. Human-visible comments are the complete append-only comment sections or linked comment records declared by an artifact. If it declares none, the comment set is empty. Do not treat an excerpt, cached copy, rendered preview, or search snippet as a body or comment record.
3. Follow every explicit Parent, Authority Sources, Blocked by, owning Map, child, Map-index, and canonical Context Pointer reference. Enumerate every entry in a declared directory, index, or search result used as a relationship set. Local files have no page token, but an incomplete enumeration is the pagination-equivalent failure and returns `Incomplete`.
4. Recognize accepted local Resolution content only in a final `## Resolution` record written by the producing workflow. A `## Resolution draft` is not accepted authority. Give each Resolution a permanent file-and-anchor reference. Apply the same explicit `Supersedes` and `Supplements` forward links, reverse comment, Map history, effective-content, ambiguity, and reconciliation rules as a real Work Tracker.
5. Assemble exactly the selected Map Context, Decision Context, or Delivery Context from those permanent records. Apply the same profile fields and blocker closure, then return exactly `Complete`, `Incomplete`, or `Ambiguous` under the shared result rules. Never switch profiles to compensate for a missing local record.

The recipe adds no second artifact model. Producer-specific layout instructions decide where files and fields are written; this contract decides what a complete read means.

## Resolution succession

Only a Resolution recognized by the configured Work Tracker binding or the Local Markdown recipe above is accepted authority. Ordinary comments never change accepted authority.

A later recognized Resolution may carry one of these explicit permanent forward references, including a reference to a Resolution in another Decision Ticket from the same Map:

- `Supersedes` names an earlier recognized Resolution and replaces it completely. The later Resolution must contain the complete current answer.
- `Supplements` names an earlier recognized Resolution and adds non-conflicting material. Both remain effective.

The forward reference on the later Resolution establishes succession. Append a reverse comment to the earlier ticket. Keep the historical Map index entry, mark it superseded when applicable, and store permanent references to both the earlier and effective Resolutions. Re-read the written artifacts through the provider binding before treating succession as valid.

Broken references, contradictory supplements, cycles, or incompatible effective interpretations return `Ambiguous`. Do not select by timestamp, title, author, or matching prose. Resolution succession adds no Decision ID, revision number, or special concurrency protocol.

## Reconciliation

Context Assembly reports authority and performs no reconciliation mutation. The workflow that accepts a changed Resolution owns this sequence:

1. Publish and re-read the recognized Resolution, its forward reference, the earlier ticket's reverse comment, and the Map index with historical and effective permanent references.
2. Find every open Specification and delivery artifact with explicit provenance from the affected Map.
3. Reconcile open unclaimed artifacts and their routing so stale work is not eligible. Stop claimed or actively implemented work at the configured human boundary.
4. Leave completed delivery history unchanged. Represent a required behavior change as follow-up delivery work.
5. Rebuild every affected Context Pack from permanent sources after authorized updates. Reconciliation completes only when each required rebuild returns `Complete`.

If the binding has no real succession example, Setup records that capability as non-destructively unverified. The first real succession operation performs the full post-write re-read and rebuild before the capability becomes verified.

## Domain Orientation boundary

Context Assembly stops at canonical repository pointers. For each canonical document used as an Authority Source or named by Context Scope, validate and retain exactly one permanent Repository-qualified Context Pointer in the form `<Repository ID>:<repo-relative path>`. The Repository ID must resolve uniquely through the supplied Repository References and configured portable repository identity. A missing or malformed pointer or unresolved Repository ID is `Incomplete`; competing identities or pointers for one claimed source are `Ambiguous`.

This validation does not read, copy, summarize, or test the availability of the canonical repository document or ADR. After a `Complete` Work Tracker or Local Markdown result, the consumer performs configured Domain Orientation, resolves the retained pointer against repository state, and loads the routed canonical source. Failure at that later boundary stops the consumer without changing the completed Context Assembly result.
