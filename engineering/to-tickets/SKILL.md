---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in one file per ticket locally, or native blocking links on a real tracker.
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets** — tracer-bullet vertical slices, each declaring the tickets that **block** it.

Read the shared [planning artifact contracts](../PLANNING-ARTIFACT-CONTRACTS.md) first. This skill owns the delivery-ticket section order and template; the shared contract owns the semantic records and cross-artifact invariants. Use the configured Work Tracker, Routing Label mapping, and Domain Orientation when their bindings exist; preserve standalone Local Markdown behavior when they do not.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, Work Tracker item, or URL) as an argument, fetch it and read its full body and comments. Accepted planning Resolutions, Domain Model Deltas, and architecture decisions are authoritative source payloads, not background summaries.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change." Keep exploration bounded to understanding the current state needed for transformation.

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Carry every source Implementation Decision and architecture decision relevant to the slice inside What to build
- Carry every source Testing Decision relevant to the slice, including its settled seams, selected test approaches, and nearest prior art
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges** — the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

For each proposed slice, derive the complete executable contract from its source:

- narrow Repository References to the minimal complete set;
- give Repository Scope a non-empty writable subset of Repository References;
- narrow Context Scope without reducing any relevant Domain Model Delta; and
- copy every created, changed, or materially relied-on cross-repository Settled Seam from Testing Decisions.

Run the shared Source authority and Composition invariants as a preflight. If either fails, return to clarification or planning instead of publishing the ticket.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so no independently green vertical slice can contain it. Sequence the migration as a coordinated cutover: divide mechanical work into batches sized by blast radius (per package, per directory) on an integration branch, then block one final integrate-and-verify ticket on every batch. Individual batches may be temporarily red; the final ticket establishes the single new form and restores green CI. Carry an old and new form together only when the source specification explicitly records approved external compatibility and its removal condition.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work
- **Executable scope**: writable Repository IDs, relevant contexts, and cross-repository seams

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct — does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker `/setup-matt-pocock-skills` configured — the ticket body below is the same either way, only its provider envelope and the shape of the blocking edges change:

- **Local Markdown** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Prepend `# <NN> — <Ticket title>` and `**Status:** ready-for-agent` to the body. Its Blocked by section names the numbers/titles it depends on.
- **Configured Work Tracker** → publish one item per ticket in dependency order (blockers first) so each ticket's blocking edges can reference durable identifiers. Use the configured native blocking/sub-item relationship where available and its documented fallback otherwise. Apply the mapped `ready-for-agent` Routing Label only after re-reading the resulting item and verifying its complete executable contract and state.

Do NOT close or modify any parent issue.

<ticket-body-template>

## Parent

<durable source specification or planning-artifact reference, or `None — <reason>`>

## What to build

<the end-to-end behaviour this ticket makes work, plus complete relevant source-authorized implementation and architecture decisions — not a layer-by-layer edit list>

## Acceptance criteria

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

## Repository References

<minimal complete set of Repository Reference records>

## Repository Scope

<one Repository Scope entry per writable repository>

## Context Scope

<minimal relevant Context Scope record>

## Cross-Repository Seams

<complete applicable cross-repository Settled Seam records, or `None — <reason>`>

## Blocked by

<durable references to blocking tickets, or `None — can start immediately`>

</ticket-body-template>

Avoid additional implementation file paths or code snippets. If a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

Publishing the validated tickets completes this planning skill. Each eligible ticket may proceed in a fresh `/implement` context across its complete authorized Repository Scope without reconstructing planning history.
