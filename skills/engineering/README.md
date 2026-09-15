# Engineering

Skills I use daily for code work.

## Shared contracts

- **[Federated workflow contracts](./federated-workflow/)** — Delivery and planning records, provider concepts and bindings, domain orientation and federation configuration, and durable lifecycle records loaded directly by the skills that need them.

## User-invoked

Reachable only when you invoke them explicitly.

- [closeout](./closeout/SKILL.md). Close a completed delivery, record acceptance, and remove its worktrees and branches.
- **[ask-matt](./ask-matt/SKILL.md)** — Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[change-walkthrough](./change-walkthrough/SKILL.md)** — Explore a change set as a semantic zoom through end-to-end scenarios, one logical hop at a time.
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — One-session grilling with output-only domain modeling that returns a sharpened plan or design with complete Domain Model Deltas.
- **[triage](./triage/SKILL.md)** — Move configured Work Tracker requests through triage and require a complete executable Agent Brief before `ready-for-agent`.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** — Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **[to-spec](./to-spec/SKILL.md)** — Synthesize a solution-level specification with Repository References, Context Scope, and complete Testing Decisions, then publish it to the configured Work Tracker.
- **[to-tickets](./to-tickets/SKILL.md)** — Transform settled source authority into self-contained tracer-bullet delivery tickets, one file per ticket locally or provider-native items on the configured Work Tracker.
- **[coordinate-delivery](./coordinate-delivery/SKILL.md)** — Coordinate one named or next agent-ready ticket through its complete federated delivery and human handoff.
- **[wayfinder](./wayfinder/SKILL.md)** — Plan a huge, foggy effort as a configured Work Tracker map of decision tickets while preserving its planning-only frontier.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[setup-federated-workflow](./setup-federated-workflow/SKILL.md)** — Configure one repository or establish or join a Domain Federation through repository-owned bindings.
- **[prototype](./prototype/SKILL.md)** — Build a throwaway prototype to answer a design question: a terminal app or shareable HTML file for state/logic, or several toggleable UI variations.
- **[review-feedback](./review-feedback/SKILL.md)** — Draft and publish human review feedback, then return a completed review round's delivery ticket for correction when explicitly requested.

- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./research/SKILL.md)** — Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./tdd/SKILL.md)** — Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./domain-modeling/SKILL.md)** — Sharpen domain language and return complete Domain Model Deltas, with default canonical capture for explicit standalone use.
- **[codebase-design](./codebase-design/SKILL.md)** — Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.
- **[implement](./implement/SKILL.md)** — Build one or more authorized Repository Deliveries with `tdd`, exact-head validation evidence, and standalone bundle review or one complete Coordinator narrowing assignment.
- **[code-review](./code-review/SKILL.md)** — Selectable Standards and Spec review for one or more fixed Repository Targets: repository-local Standards results and one whole-bundle Spec result.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation — never `--abort`.
- **[wizard](./wizard/SKILL.md)**: Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.
