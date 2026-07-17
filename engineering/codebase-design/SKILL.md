---
name: codebase-design
description: Design deep modules proportionally. Use when the user wants to design or improve a module's interface, decide where a seam goes, deepen or privately decompose a module without widening its interface, make it testable through that interface, judge whether a design is overengineered, or when another skill needs the deep-module vocabulary.
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

## Glossary

Use these terms exactly — don't substitute "component," "service," "API," or "boundary." Consistent language is the whole point.

**Module** — anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice. _Avoid_: unit, component, service.

**Interface** — everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API, signature (too narrow — they refer only to the type-level surface).

**Implementation** — what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth** — leverage at the interface: the amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_ — a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it. _Avoid_: boundary (overloaded with DDD's bounded context).

**Adapter** — a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

**Leverage** — what callers get from depth: more capability per unit of interface they learn. One implementation pays back across N call sites and M tests.

**Locality** — what maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. Fix once, fixed everywhere.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of cohesive private parts — they just aren't part of the interface. A module can have **internal seams** where its implementation genuinely varies, but physical file boundaries do not create seams.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

## Proportional design

Choose the **least-complex coherent design** that protects current acceptance criteria, established repository invariants and ADRs, and **credible failures** while preserving depth and locality. Fewer constructs are not simpler when ownership, invariant knowledge, or boundary policy leaks through the interface into callers.

A failure is credible only when its state is reachable through a named external boundary, supported persisted data, an allowed lifecycle transition, or a realistic concurrency or failure interleaving. Untyped or external data earns the trusted domain type only after validation or translation at its boundary; a cast or unchecked deserialization does not establish that trust. Handle invalid input at the boundary, then make invalid internal states unrepresentable so internal modules can rely on their declared typed contracts.

Every added mechanism must name the acceptance criterion or established invariant it protects, the credible failure and material impact, and why a simpler coherent design is insufficient. A simplification must leave those protections and the intended module shape intact. A deferral names the accepted residual risk and its next owner.

### Final state

Leave every touched current-truth artifact in **final-state** form: code, tests, configuration, schemas, examples, plans, skills, and durable design docs describe the intended system directly, using its current names, owners, statuses, contracts, layout, validation expectations, and vocabulary. Prefer one clear model over artifacts that teach superseded and current shapes together.

Artifact role decides whether chronology belongs. A current-truth artifact answers what is intended now; an intentional history artifact answers how decisions or understanding evolved. Change logs, review findings, issue history, commits, Git history, and explicitly superseded ADRs or learning records may preserve chronology. A file does not become a history artifact merely because notes were appended to it.

Tests are current truth: express stable expected behavior, domain invariants, and observable outcomes through the module's interface. A past bug can motivate a regression test, but the test presents the behavior that must hold, not the accidental implementation mistake that exposed it.

### Clean breaks

An internal contract change is a **clean break**: establish one current contract, update every producer and consumer under the same change authority, and remove the superseded form in the completed change. Aliases, shims, dual reads or writes, legacy payload handling, compatibility wrappers, and deprecated fallbacks are added mechanisms; internal migration convenience is not an acceptance criterion.

A contract crosses a real external boundary when existing consumers outside the service's change authority depend on it, including public HTTP, RPC, webhook, CLI, UI, event, file, protocol, integration, persisted, or published contracts. At that boundary, stop and ask whether backward compatibility is required. Only explicit human approval makes compatibility an acceptance criterion; otherwise make the clean break. When approved, define the supported transition and the condition that removes the old contract.

## Logical ownership and physical decomposition

A module is a logical owner, not a file. Its implementation may span cohesive private files hidden behind one public interface at one seam. **Physical decomposition** splits independently changing internal responsibilities while preserving that interface, the module's invariants and vocabulary, and every boundary translation. Treat each new file as a private implementation detail; promote it to an owner, adapter, public seam, or test surface only when separate responsibility or variation passes proportional design.

Before adding behavior to a module whose implementation contains independently changing responsibilities, either decompose those responsibilities privately behind the existing seam or state the concrete locality reason they are clearer and safer together. A behavior-preserving private split is tidy-first refactoring within the current implementation authority. Every split should improve locality by concentrating understanding and change.

## Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow — interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

## Going deeper

- **Deepening a cluster given its dependencies** — see [DEEPENING.md](DEEPENING.md): dependency categories, seam discipline, and replace-don't-layer testing.
- **Exploring alternative interfaces** — see [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md): spin up parallel sub-agents to design the interface several radically different ways, then compare on depth, locality, and seam placement.
