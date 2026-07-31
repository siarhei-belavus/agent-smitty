---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## Orient before modeling

If `docs/agents/domain.md` exists, read it first and perform its Domain Orientation. Treat that configured routing as authoritative:

- terms and definitions belong to their Canonical Context Document;
- bounded-context topology, participants, External Systems, and relationships belong to the owning Context Map;
- context-local and repository-wide architecture decisions belong to their repository owner;
- federation-wide architecture decisions belong to the Domain Federation Home Repository.

Follow Repository-qualified Context Pointers through the configured portable repository identities. Checkout proximity may help resolve an already selected owner; it never selects an owner or grants write authority.

If the canonical owner or its configured artifact is unavailable, report the unavailable owner and preserve the proposed change for routing. Do not create a local substitute, duplicate canonical content, or silently choose another repository.

## Planning and write authority

Domain modeling keeps the same depth in planning as in direct documentation work, but planning results are not repository-wide current truth yet.

- When composed inside `/grill-with-docs` or `/wayfinder`, record each human-confirmed result immediately in the active planning ticket's single complete `## Resolution draft`. Preserve the owning Repository ID and Canonical Context Pointer, operation, exact language, relationships, invariants, boundaries, scenarios and counterexamples, rationale and rejected alternatives, complete ADR rationale when applicable, provenance, canonical documentation obligations, and contradiction conditions. Finalize that same draft as `## Resolution` when shared understanding is confirmed. Follow the configured Work Tracker's update-own-comment or append-only supersession behavior.
- A standalone invocation writes canonical domain artifacts only when the user explicitly authorized an in-place domain-documentation change. Otherwise discuss or return the same full-fidelity Domain Model Delta without writing it.

Effective planning language is the ordered combination of the oriented Canonical Context Documents and the accepted Domain Model Deltas in the current effort. A later accepted delta governs artifacts derived from that effort without becoming canonical current truth before its authorized Repository Delivery is accepted.

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something authorized to write and only in the routed owner. If no `CONTEXT.md` exists, create one when the first term is resolved and the current repository is its confirmed canonical owner. If no `docs/adr/` exists, create it when the first owned ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Capture resolved language immediately

When a term is resolved, capture it right there. Don't batch these up. In explicitly authorized documentation work, update the routed `CONTEXT.md` using [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md). In planning, update the active Resolution draft with the full-fidelity delta instead.

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to record an ADR decision when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. For authorized documentation work, use [ADR-FORMAT.md](./ADR-FORMAT.md) in the routed owner. During planning, preserve the complete decision and documentation obligation in the Resolution draft instead of writing the canonical ADR.
