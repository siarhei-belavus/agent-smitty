---
name: code-review
description: Review committed or worktree changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

Two-axis review of changes since a supplied fixed point:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

## Process

### 1. Pin the fixed point

Use the fixed point supplied by the user or invoking skill — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If neither supplied one, ask for it.

Resolve and record the current `HEAD` SHA, then capture the review target once:

- For committed changes, diff `<fixed-point>...<head-sha>`.
- When worktree changes are in scope, diff the worktree against `git merge-base <fixed-point> <head-sha>` and include the contents of untracked files.

Use the committed target for an explicitly branch, PR, or committed review; use the worktree target for a WIP, current, or uncommitted review. Otherwise, if the worktree is dirty, disclose it and ask whether those changes are in scope.

Also note the commits via `git log <fixed-point>..<head-sha> --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the selected review target is non-empty. A bad ref or empty target should fail here — not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Spec, ticket, or resolved decision sources supplied by the user or invoking skill.
2. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.). Follow `docs/agents/issue-tracker.md` when present; otherwise use available project tooling.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

Start with seam context supplied by the user or invoking skill, then validate every seam against current authoritative sources. Explicit current user direction, specifications, and resolved decisions take precedence over earlier sources and existing public interfaces. Record each settled seam with its source. Treat existing public interfaces as current-state evidence, not authority. Report source conflicts as **Spec** findings; when no authoritative source settles a seam, mark it unsettled and assess its shape under the `/codebase-design` baseline rather than choosing one during review.

### 3. Build the review baselines

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **Authoritative sources override.** An explicit specification, resolved design decision, or documented repo standard wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation.

Each smell reads _what it is_ → _how to fix_; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, hooks, compatibility machinery, transitional old/new forms, migration-diary residue, or tests centered on an accidental implementation mistake rather than required behavior. → delete it; leave one intended form and express tests as stable behavior.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

Determine whether the review target introduces or reshapes a module, interface, seam, or adapter, or changes logical ownership, physical decomposition, or a contract. Record whether this design-review trigger applies.

Route requirement or settled-decision violations to **Spec**; route structural and change-pressure findings to **Standards**.

### 4. Spawn both sub-agents in parallel

Send a single message with two `Agent` tool calls. Use the `general-purpose` subagent for both.

**Standards sub-agent prompt** — include:

- The captured review target and commit list.
- The standards-source files, smell baseline, routing rule, and design-review trigger result from step 3.
- The seam context, including authoritative sources and any unsettled seams.
- The brief: "When the design-review trigger applies, read `/codebase-design` in full, apply its glossary and policies, and perform a structural simplification scan using its deletion test and proportional-design rules. Do not run a design workflow or choose an unsettled design; if the skill is unavailable, report this review as incomplete. Report all material Standards findings per file/hunk, citing each violated rule or naming the relevant heuristic and quoting the hunk. Label a finding **Blocking** only for a mandatory-standard violation or a structural flaw with a credible future bug or change-pressure path and material impact; label other material findings **Advisory**. Treat proportional-design findings as judgement calls unless an authoritative source makes them mandatory. Omit purely mechanical issues reliably enforced by configured tooling. Keep the report under 400 words when possible."

**Spec sub-agent prompt** — include:

- The captured review target and commit list.
- The paths or fetched contents of the spec and decision sources.
- The seam context, including authoritative sources and any unsettled seams.
- The routing rule from step 3.
- The brief: "Report all material Spec findings: missing or partial requirements, scope creep, incorrect implementation, acceptance behavior outside a settled seam, unauthorized seam changes, and acceptance behavior not verified through that seam. Label a finding **Blocking** when it demonstrates a requirement or settled-decision violation, or a reachable correctness/regression against intended behavior; label other material findings **Advisory**. Cite the authoritative source for each finding. Keep the report under 400 words when possible."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge, reclassify, or rerank findings — the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary of Blocking and Advisory counts per axis and the highest-severity finding reported by each reviewer, if any. Do not pick a single winner across axes.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
