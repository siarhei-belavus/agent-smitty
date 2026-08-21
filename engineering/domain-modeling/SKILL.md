---
name: domain-modeling
description: Build and sharpen a project's domain model, returning complete Domain Model Deltas and applying them to canonical documentation when the invocation grants that authority. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.
---

# Domain Modeling

Actively sharpen the project's domain model by challenging terms, probing edge cases, and recording confirmed glossary and architecture changes. Merely reading `CONTEXT.md` for vocabulary does not invoke domain modeling.

## Orient before modeling

If `docs/agents/domain.md` exists, read it first and perform its Domain Orientation. Treat that configured routing as authoritative:

- terms and definitions belong to their Canonical Context Document;
- bounded-context topology, participants, External Systems, and relationships belong to the owning Context Map;
- context-local and repository-wide architecture decisions belong to their repository owner;
- federation-wide architecture decisions belong to the Domain Federation Home Repository.

Follow Repository-qualified Context Pointers through the configured portable repository identities. Checkout proximity may help resolve an already selected owner; it never selects an owner or grants write authority.

If the canonical owner or its configured artifact is unavailable, report the unavailable owner and preserve the proposed change for routing. Do not create a local substitute, duplicate canonical content, or silently choose another repository.

## Output and capture authority

Every human-confirmed change produces a complete [Domain Model Delta](DOMAIN-MODEL-DELTA.md) immediately. Do not batch confirmed results or reduce them to reminders.

- An explicit standalone invocation grants canonical capture by default: apply each confirmed delta immediately to its routed `CONTEXT.md`, `CONTEXT-MAP.md`, or ADR owner unless the user asks for discussion only.
- A composed or model-invoked use returns each delta to the invoking workflow without writing canonical artifacts or selecting a planning persistence destination. It may apply a delta only when that invocation explicitly grants canonical capture.

Capture authority changes only the destination, never the modeling depth or delta contents.

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

Under canonical capture, create files lazily and only in the routed owner. If no `CONTEXT.md` exists, create one when the first term is resolved and the current repository is its confirmed canonical owner. If no `docs/adr/` exists, create it when the first owned ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Capture resolved language

Apply [Output and capture authority](#output-and-capture-authority) to each resolved term. Format a routed glossary update with [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

### Offer ADRs sparingly

Only offer to record an ADR decision when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Under canonical capture, use [ADR-FORMAT.md](./ADR-FORMAT.md) in the routed owner. Otherwise include the complete decision rationale and canonical documentation obligation in the returned delta.
