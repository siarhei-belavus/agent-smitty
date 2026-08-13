# Engineering

Skills I use daily for code work.

## Shared contracts

- **[Planning Artifact Contracts](./PLANNING-ARTIFACT-CONTRACTS.md)** — Normalized repository, context, decision, seam, validation, scope, and dependency records shared by specification, ticket, and triage artifacts.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[ask-matt](./ask-matt/SKILL.md)** — Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[change-walkthrough](./change-walkthrough/SKILL.md)** — Explore a change set as a semantic zoom through end-to-end scenarios, one logical hop at a time.
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — One-session grilling with domain modeling that carries complete deltas in conversation to specification synthesis.
- **[triage](./triage/SKILL.md)** — Move configured Work Tracker requests through triage and require a complete executable Agent Brief before `ready-for-agent`.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** — Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **[setup-matt-pocock-skills](./setup-matt-pocock-skills/SKILL.md)** — Configure this repo for the engineering skills (issue tracker, triage labels, domain doc layout). Run once per repo.
- **[to-spec](./to-spec/SKILL.md)** — Synthesize a solution-level specification with Repository References, Context Scope, and complete Testing Decisions, then publish it to the configured Work Tracker.
- **[to-tickets](./to-tickets/SKILL.md)** — Transform settled source authority into self-contained tracer-bullet delivery tickets, one file per ticket locally or provider-native items on the configured Work Tracker.
- **[implement](./implement/SKILL.md)** — Build the work described by a spec or set of tickets, driving `/tdd` at pre-agreed seams and closing out with `/code-review` before committing.
- **[wayfinder](./wayfinder/SKILL.md)** — Plan a huge, foggy effort as a configured Work Tracker map of decision tickets while preserving its planning-only frontier.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)** — Build a throwaway prototype to answer a design question: a runnable terminal app for state/logic, or several toggleable UI variations.

- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./research/SKILL.md)** — Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./tdd/SKILL.md)** — Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./domain-modeling/SKILL.md)** — Sharpen domain language and return complete Domain Model Deltas, with default canonical capture for explicit standalone use.
- **[codebase-design](./codebase-design/SKILL.md)** — Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.
- **[code-review](./code-review/SKILL.md)** — Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/PRD?), run as parallel sub-agents.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation — never `--abort`.
