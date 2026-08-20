---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask Matt

You don't remember every skill, so ask.

A **flow** is a path through the skills. Most paths run along one **main flow**, and two **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **`grill-with-docs`** — sharpen the idea by interview. Start here when you **have a codebase**: it applies the project's domain language and returns complete Domain Model Deltas with the sharpened result. In this flow, the current conversation retains that result as planning authority for `to-spec`. (No codebase? Use `grill-me` — see Standalone. Both run the same `grilling` primitive; `grill-with-docs` adds domain modeling.)
2. **Branch — can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`handoff`** in both directions (see Phase boundaries):
   - **`handoff`** out, then open a separate task against that file,
   - **`prototype`** to answer the question with throwaway code,
   - **`handoff`** back what you learned, and reference it from the original planning task.
3. **Branch — is this a multi-task build?**
   - **Yes** → **`to-spec`** (turn the conversation into a spec), then **`to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. On a local tracker that's one file per ticket under `.scratch/<feature>/issues/`; on a real tracker the edges become native blocking links. Run each eligible agent-ready ticket through **`coordinate-delivery`** for its complete federated delivery and human handoff.
   - **No** → **`implement`** right here, in the same task.

   **`coordinate-delivery`** claims one agent-ready Work Tracker ticket, prepares isolated Repository Deliveries, then invokes **`implement`** in Coordinator-narrowed mode for each changed delivery. It owns publication, bundle review, and the ready-for-human handoff. Use **`implement`** directly for an already-authorized standalone assignment; it drives **`tdd`** internally and closes with **`code-review`**. Reach for **`tdd`** on its own when you just want to build a concrete behaviour test-first, and **`code-review`** on its own whenever you want to review one branch or a complete multi-repository bundle.

### Context hygiene

Keep steps 1–3 in **one task** so the grilling, spec, and tickets build on the same reasoning. Automatic compaction may summarize earlier turns as the task grows. That is continuation within the same task, not a handoff. Before leaving a phase, capture decisions that the next phase cannot safely reconstruct in the flow's durable artifacts.

Implementation starts from complete ticket authority, whether the ticket contains one or multiple Repository Deliveries. It does not need the planning task's full conversation.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **`triage`**. It moves issues through triage roles and produces agent-ready issues for a separately invoked `coordinate-delivery` run.

  Triage is only for issues **you didn't create** — bug reports, incoming feature requests, anything that arrives raw. Tickets that `to-tickets` produced are already agent-ready, so **don't triage them**.

- **Something's broken** → **`diagnosing-bugs`**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** — one command that already goes red on _this_ bug — then fixes with a regression test. Its post-mortem hands off to **`improve-codebase-architecture`** when the real finding is that there's no good seam to lock the bug down.

- **A huge, foggy effort — a greenfield project or a huge feature build, too big for one session** → **`wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker. Each ticket has one claimant; independent ready research may proceed in parallel, while dependent decisions wait for their blockers — producing **decisions, not deliverables** — until the fog is pushed back and the way is clear. Where **`grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't — and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`to-spec`**, which collapses the map's linked decisions into a buildable plan, then `to-tickets`. Each resulting ticket can use `implement` across its complete Repository Scope. Looping the map straight into `implement` skips the collapse and throws linked detail away — do that only when the effort turned out genuinely small and receives explicit execution authority.

## Codebase health

Not feature work — upkeep.

- **`improve-codebase-architecture`** — run whenever you have a spare moment to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one _generates an idea_ you can take into the main flow at `grill-with-docs`. It's the survey that finds the candidates; **`codebase-design`** (below) is the bench you design the chosen one on.

## Vocabulary underneath

Two model-invoked references that run _beneath_ the other skills — each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the skills above pull them in.

- **`domain-modeling`** — sharpen the project's _domain_ language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), and test whether a hard-to-reverse decision merits an ADR. It returns complete Domain Model Deltas to invoking workflows. An explicit standalone invocation captures them in the routed canonical `CONTEXT.md`, `CONTEXT-MAP.md`, or ADR owner by default.
- **`codebase-design`** — the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. `to-spec`, `implement`, and standalone `tdd` invoke it when design decisions are unsettled; `improve-codebase-architecture` invokes it directly.

## Phase boundaries

A phase is a coherent stretch of work such as grilling, specification, implementation, or review. At the boundary between phases, choose by ownership and destination:

1. **Continue in the current task** when the next phase advances the same objective in the same working context and benefits from the reasoning already here. This is the normal path through grilling, `to-spec`, and `to-tickets`.
2. **Let automatic compaction continue the task** when earlier turns are summarized automatically. Compaction does not create a new task or transfer ownership. Continue from the summary, checking durable artifacts when exact decisions matter.
3. **Use `handoff` for another task or repository** when the work needs a new owner, a separate task history, or a different repository context. The handoff file carries the relevant decisions and evidence across that boundary. A prototype in its own task or repository is the standard case.
4. **Delegate a concrete, bounded subtask to a subagent** when it can run independently and report back without taking ownership of the parent task. Give it an explicit deliverable and exclusive scope. Keep integration and phase decisions in the parent task.

Do not create a handoff merely because automatic compaction occurred. Do not delegate an open-ended phase whose result needs ongoing steering or whose authority belongs in the parent task.

## Standalone

Off the main flow entirely.

- **`grill-me`** — the same relentless interview as `grill-with-docs`, but for when you have **no codebase**. Stateless: it saves nothing locally, builds no `CONTEXT.md`. Reach for it to sharpen any plan or design that doesn't live in a repo.
- **`integrate-matt-concept`** — research a proposed doctrine's overlap and behavioral value, then reject, merge, rewrite, or introduce it through one canonical home.
- **`prototype`** — a small, throwaway program that answers one design question: does this state model feel right, or what should this UI look like. Throwaway from day one — keep the answer, delete the code. It's the detour in step 2 of the main flow, but reach for it any time a design question is hard to settle on paper.
- **`research`** — delegate reading legwork to a **background agent**: it investigates a question against **primary sources**, then leaves a cited Markdown file in the repo. Keep working while it reads. The file it produces is something to take _into_ the main flow at `grill-with-docs` — research feeds the thinking, it doesn't replace it.
- **`wait-what`** — re-pitch the last answer when it did not land: add the missing context, use Simplified Technical English, and preserve the applicable canonical domain vocabulary.
- **`teach`** — learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`writing-for-agents`** — reference for writing documents agents consume, including skills and agent instructions.

## Precondition

**`setup-matt-pocock-skills`** — run before your first engineering flow to configure the issue tracker, triage labels, and doc layout the other skills assume. Custom issue trackers also work.
