---
name: domain-modeling
description: Build and sharpen a project's domain model, returning complete Domain Model Deltas and applying them to canonical documentation when the invocation grants that authority. Use when discussing a codebase's ubiquitous language, writing or editing a CONTEXT.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenge terms, invent edge-case scenarios, and write the glossary and decisions down the moment they crystallise. Merely reading `CONTEXT.md` for vocabulary does not invoke domain modeling.

## Orient before modeling

Load [DOMAIN-ORIENTATION.md](../federated-workflow/DOMAIN-ORIENTATION.md). If `docs/agents/domain.md` exists, read it and perform the configured Domain Orientation.

Follow Repository-qualified Context Pointers through the configured portable repository identities. Checkout proximity may help resolve an already selected owner; it never selects an owner or grants write authority.

## Output and capture authority

Every human-confirmed domain-language or architecture change produces a complete [Domain Model Delta](DOMAIN-MODEL-DELTA.md) immediately. Resolve its owner and route during Domain Orientation. Do not batch confirmed results or reduce them to reminders.

- An explicit standalone invocation grants canonical capture by default: apply each confirmed delta immediately to its routed `CONTEXT.md`, `CONTEXT-MAP.md`, or ADR owner unless the user asks for discussion only.
- A composed or model-invoked use returns each delta as output without writing canonical artifacts or selecting a planning persistence destination. It may apply a delta only when explicitly granted canonical capture.

Capture authority changes only the destination, never the modeling depth or delta contents.

## Create routed artifacts lazily

Under canonical capture, create the configured Canonical Context Document, Context Map, or ADR only when the first owned change requires it. Do not pre-create empty canonical documents.

Use [CONTEXT-MAP-FORMAT.md](./CONTEXT-MAP-FORMAT.md) for the configured Context Map of one repository. Preserve a compatible existing layout. A Federated Context Map follows the Domain Federation contract selected during orientation.

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

Emit each resolved term's complete Domain Model Delta immediately. Apply [Output and capture authority](#output-and-capture-authority), and format a routed glossary update with [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

### Offer ADRs sparingly

Only offer to record an ADR decision when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Under canonical capture, use [ADR-FORMAT.md](./ADR-FORMAT.md) in the routed owner. Otherwise return the decision's Delta.
