---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

Load the shared [test-surface contract](../codebase-design/TEST-SURFACE.md), then run the red → green loop below.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

Use [tests.md](tests.md) as examples. Load [mocking.md](mocking.md) only when choosing or designing a test double.

## Seams — where tests go

Use the settled seams recorded in the supplied specification, ticket, resolved design decision, or composed authority. Do not ask the user to reconfirm them.

For standalone TDD without a settled seam set, identify the complete set of existing, changed, and new seams the requested behavior spans. If materially different caller-facing seams remain possible, use `codebase-design` before proposing the set. For each seam, also propose its test approach using the repository's test architecture. Ask the user to confirm the complete set and proposed approaches once; the confirmed seams are settled.

Treat the repository's existing test suites, commands, harnesses, fixtures, and naming as its **test architecture**. For each settled seam, use its recorded test approach; if none is recorded, find the nearest prior art and choose the smallest repository-native approach. Extend the existing approach; a new one earns its place only when the test architecture cannot exercise the behavior, with the gap stated explicitly.

Before writing tests, record which settled seams and test approaches are under test. Test only through those seams.

## Anti-patterns

- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
