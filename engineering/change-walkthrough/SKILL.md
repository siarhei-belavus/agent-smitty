---
name: change-walkthrough
description: Walk through a change set one end-to-end flow at a time.
disable-model-invocation: true
---

# Change Walkthrough

Guide the human through a change set as a **semantic zoom** over a map. Reconstruct the whole change before presenting it, then reveal one end-to-end scenario and one logical step at a time. This is a walkthrough for understanding, not a review or approval gate.

Operate read-only: inspect and explain the repository, history, supplied sources, tests, and existing review findings while leaving code, repository state, merge requests, and external systems unchanged.

Before the first user-visible walkthrough response, read [FORMAT.md](FORMAT.md) in full and follow its rendering contract throughout the session.

## 1. Pin the change set

Resolve one fixed point and one target:

- For a merge request, use its base and head.
- For a supplied branch or commit, compare it with the supplied fixed point; when none was supplied, use its merge base with the repository's default branch.
- For an explicitly current or WIP walkthrough, compare the worktree with the merge base of the fixed point and `HEAD`; include tracked, untracked, and staged changes.

Record the resolved SHAs, commit list, changed files, and full diff once. When the intended bounds remain ambiguous after inspecting the available context, show the candidate bounds and ask the human to confirm them.

This step is complete when both bounds resolve, the captured change set is non-empty, and every in-scope untracked file is captured.

## 2. Build the atlas

Do the legwork before narrating. Read relevant repository instructions, authoritative specs and decisions, issue context, commit messages, interfaces, callers, tests, and enough unchanged code to trace each change from an entry to an observable result.

Organise the diff by observable behaviour, never by file order or commit order. Order the atlas as:

1. External or user-visible scenarios
2. Domain-rule changes
3. Internal supporting flows
4. Behaviour-preserving refactoring
5. Tests, documentation, and configuration as evidence for the preceding flows

Assign every changed hunk to exactly one home:

- an end-to-end scenario;
- a shared change used by several scenarios;
- behaviour-preserving refactoring;
- tests, documentation, or configuration;
- a derived artifact such as generated code, a snapshot, fixture, or lockfile;
- a **detour** whose purpose cannot be explained by the available evidence.

Connect each changed node to the minimum unchanged entry and exit context needed to explain its role. Mark changed and unchanged nodes distinctly. Group maps larger than seven nodes into nested regions according to logical ownership, then map each region separately.

Use an authoritative source to explain intent when available. Otherwise infer intent from interfaces, callers, tests, history, and the diff, and label it **Inferred intent**. Existing code-review findings may appear as attention flags on the relevant nodes; do not perform a new code review.

Collapse derived artifacts into a derived region connected to the change that produced them. Record why each artifact changed, how it is generated, its scale, and its file location; reveal its contents only when the human zooms into it.

This step is complete when every hunk has exactly one home and every changed node either participates in a traced scenario, supports one, or is an explicit detour.

## 3. Present the atlas

Orient the human with the `What this change set is about` view from [FORMAT.md](FORMAT.md), then show the compact atlas.

Synthesize the shared purpose of the whole atlas in domain language. When the change set has several independent goals, show them separately instead of inventing one umbrella goal, and associate every top-level scenario with one of them. Include a material non-goal only when an authoritative source states it or it is needed to prevent a likely scope misunderstanding.

Name scenarios by behaviour. Show their entry, observable result, changed regions, and any attention flags. Keep the first view at no more than seven nodes, recommend the first route, and let the human reroute. Use a top-to-bottom Markdown flow by default: place the route in one compact blockquote, with one node per quoted line and explicit visual markers for unchanged context, changed behaviour, the current position, and the observable result. Do not prefix the nodes with bullets or numbers. Bold the complete current-node line. The line order communicates flow; do not add connector arrows between items or compress a multi-step route into a single parenthesized arrow expression. Do not render a linear route as a code block or add decorative box-drawing frames. Use a small Mermaid diagram only when branching or convergence is materially clearer as a diagram.

This step is complete when every top-level scenario is accounted for by the summary and the human can see the whole atlas, the current position, and the available routes without opening code.

## 4. Walk one scenario

Before its first step, show the whole scenario map with minimal unchanged context. Then show exactly one logical step per response. Keep the full route only in the first response for that scenario; on later responses use a compact position breadcrumb and restore the full route only when the human asks to return to the map.

Make navigation language friendly:

- localize structural labels such as `Scenario`, `Step`, `Outcome`, `Where we are`, and `Navigate` into the language used by the human;
- render progress as natural language, for example `Step 3 of 4` or its localized equivalent, never the terse `Hop 3/4`;
- name each step in plain domain language that describes what happens; put an unavoidable technical term second, not as the whole title;
- do not repeat the legend after the first scenario-map response unless the human asks for it.

For the current step, provide:

- its role in the scenario;
- where control or data arrives from and where it goes next;
- one clickable reference to the exact file and line;
- the smallest self-contained code excerpt that explains the step, normally 5–20 lines;
- links without excerpts for supporting locations;
- a link to the test that demonstrates the observable behaviour, or an explicit note that no direct test was found.

Use the host's clickable file-and-line syntax and label links with repository-relative paths. Show `before → after` only when the current code alone cannot explain the change. Render the scenario, step, deeper, and detour views exactly as [FORMAT.md](FORMAT.md) specifies.

End each step with one navigation choice: **deeper**, **next**, or **back to the map**. Treat ordinary-language equivalents as the same commands.

- **Deeper** zooms into the current step through its callers, implementation, tests, history, or supporting diff.
- **Next** moves to the next step while retaining the breadcrumb.
- **Back to the map** restores the scenario or atlas view.

The walkthrough is a guide, not an examination: navigation never requires the human to approve the design or prove understanding.

Questions and discussion may expose a concrete problem that was not visible from the diff alone. When that happens:

- distinguish an actionable mismatch, unnecessary mechanism, missing proof, or maintainability problem from a request for explanation or a reasonable design preference;
- trace the concern back to exact code, an authoritative source, or observable behaviour before presenting it;
- label it a **Follow-up candidate**, not a review finding, because the walkthrough does not perform a new code review;
- draft a concise MR comment that states the problem, its impact, and the desired final state without prescribing incidental implementation details;
- draft and post MR comments in English by default, regardless of the walkthrough language; use another language only when the user explicitly requests it;
- explicitly offer to add that comment to the merge request;
- do not post it during the read-only walkthrough. Posting requires a separate explicit user instruction and is performed as a follow-up action outside the walkthrough.

Use the follow-up rendering from [FORMAT.md](FORMAT.md). Keep navigation available so the human can continue the walkthrough without resolving the candidate immediately.

When a detour is reached, pause and show its exact hunk, why it does not fit the current map, and any plausible connection labelled as inference. Offer to inspect it now or leave it marked for the end.

A scenario is complete when every step has been visited or the human explicitly skips the remainder.

## 5. Finish or checkpoint

After each scenario, update the compact tour map and recommend the next route.

The walkthrough is complete only when:

- every changed hunk remains accounted for;
- every scenario has been walked or explicitly skipped;
- every detour has been visited or remains explicitly marked;
- every follow-up candidate raised during the walkthrough is recorded as posted, declined, or outstanding;
- a final atlas shows the route actually taken, skipped regions, and remaining detours.

If the human stops earlier, provide a compact checkpoint containing the fixed point, target, current scenario and step, completed and skipped routes, outstanding detours, and outstanding follow-up candidates. Continue from that checkpoint when the same walkthrough resumes.
