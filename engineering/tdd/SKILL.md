---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure. A regression test earns its place by catching the failure again, but name and assert it as the intended behavior or domain invariant, not the historical bug or implementation mistake.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams — where tests go

A seam is where a module's interface lives. Tests exercise observable behavior through that interface, never the module's implementation.

Use the settled seams recorded in the supplied specification, ticket, resolved design decision, or by the invoking skill. Do not ask the user to reconfirm them.

When invoked standalone without a settled seam set, identify the complete set of existing, changed, and new seams the requested behavior spans. If materially different caller-facing seams remain possible, use the `codebase-design` skill before proposing the set. For each seam, also propose its test approach using the repository's test architecture. Ask the user to confirm the complete set and proposed approaches once; the confirmed seams are settled.

Treat the repository's existing test suites, commands, harnesses, fixtures, and naming as its **test architecture**. For each settled seam, use its recorded test approach; if none is recorded, find the nearest prior art and choose the smallest repository-native approach that **faithfully** exercises the behavior through that seam. Extend the existing approach; a new one earns its place only when the test architecture cannot exercise the behavior, with the gap stated explicitly.

Before writing tests, record which settled seams and test approaches are under test. Test only through those seams.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
