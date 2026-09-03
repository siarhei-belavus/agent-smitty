---
name: integrate-matt-concept
description: Research and integrate a useful concept into Matt's skills through one canonical home and minimal approved edits.
disable-model-invocation: true
---

# Integrate a Matt Concept

Research one user-supplied concept, decide whether it earns a place in the local Matt skill collection, then integrate it without scattering doctrine across the workflow.

Before starting, read [`../writing-for-agents/SKILL.md`](../writing-for-agents/SKILL.md) and every reference it requires. Resolve paths from this skill's directory; the Matt collection is `../..`.

Treat the current collection and its Git history as a customized local fork. Preserve existing local changes and intent. Upstream synchronization is a separate future task: this skill neither imports upstream changes nor rewrites local doctrine to resemble upstream.

## 1. Research the current behavior

Capture the worktree baseline. Before interviewing or proposing placement, research whether the collection already produces the intended behavior.

Search the full plausible surface, not only the concept's exact phrase:

- synonyms, avoided terms, examples, and descriptions of the same failure or desired behavior
- broader parent doctrines and narrower sub-rules
- routers, skill bodies, disclosed references, templates, metadata, and generated subagent prompts
- Git history for earlier, renamed, removed, or superseded versions of the idea
- actual invocation paths: whether a matching rule is loaded where the behavior occurs

Read every plausible match and its fired context pointers completely. Establish external facts from primary sources only when the concept depends on them; upstream synchronization stays out of scope.

Produce an **overlap map**. For each match, record its location, current behavior, effective invocation path, and relation to the proposed concept:

- **Equivalent** — already produces the same behavior.
- **Partial** — covers only part of it.
- **Parent** — broader doctrine already owns it.
- **Conflict** — steers the opposite behavior or assigns another owner.
- **Adjacent** — similar words, materially different behavior.
- **Absent** — no effective rule exists after conceptual and historical search.

**Complete when:** every plausible existing home and invocation path has been examined, and every match is classified with evidence rather than keyword similarity.

## 2. Pass the admissibility gate

A concept earns integration by changing behavior, not by sounding sensible. Establish with the user:

- the failure it prevents
- the positive behavior it should produce
- the invariant at its center
- examples that should and should not trigger it
- its intended scope
- the behavior expected today without the concept
- the observable process difference expected with it

Run the **no-op test** against both the current skills and the model's likely default. The concept is admissible only when evidence supports at least one material gain:

- it prevents a concrete recurring failure the current collection permits
- it resolves a live contradiction or ownership ambiguity
- it completes a partial rule whose missing behavior matters
- it collapses several live meanings into one stronger canonical concept or leading word

Being relevant, prudent, or generally true is insufficient. Weigh the gain against context load, cognitive load, maintenance cost, and increased prominence in the workflow.

When the behavioral delta is uncertain, run blind fresh-context probes against representative scenarios: current skills versus a draft rule, same task and evidence. Compare process, not prose. A draft that does not materially change behavior is a no-op.

Choose and recommend one disposition:

- **Reject** — duplicate, no-op, unsupported, or harmful.
- **Merge** — fold useful residue into an existing canonical rule.
- **Rewrite** — reconcile partial or conflicting rules into one coherent source of truth.
- **Introduce** — create a genuinely new concept because no existing rule owns the behavior.

For an admissible concept, propose two or three candidate **leading words** and explain the behavior each recruits. Present the research, behavioral evidence, recommended disposition, and your restatement of the concept. Wait for confirmation. A rejected concept stops here with an explicit no-op report.

**Complete when:** the user has confirmed that the concept is useful, its disposition, intent, scope, and leading language—or has accepted the no-op rejection.

## 3. Map the skill system

For an admissible concept, trace every independent execution path that could own, consume, or merely carry it. Classify each candidate location as one of:

- **Canonical home** — owns the complete definition.
- **Consumer** — needs a context pointer or phase-specific action because it executes independently and cannot rely on an artifact carrying the decision.
- **Carrier** — transports a task-specific decision, not the doctrine itself.
- **Index** — advertises a changed invocation branch.
- **Non-target** — remains unchanged; state why.

Resolve the overlap map structurally:

- equivalent rules remain untouched or consolidate into the chosen canonical home
- partial rules merge without leaving two competing definitions
- conflicts resolve through explicit scope or replacement rather than coexistence
- parent doctrine retains ownership of its sub-rules

Check that the concept strengthens rather than bypasses the collection's software-design discipline.

**Complete when:** every plausible workflow branch is classified and every equivalent, partial, parent, or conflicting rule has a proposed disposition.

## 4. Design the placement

Default to one canonical edit. Before proposing any consumer pointer, run a **composition symmetry test**: inspect how sibling principles from the same canonical home reach the candidate target. Treat the collection's established composition style as architecture, not an omission to repair. A model-facing canonical description may already provide discovery, artifacts may carry task-specific decisions, and a direct conflict may need local replacement without importing the doctrine that resolved it.

An additional consumer pointer earns its place only when all are true:

1. the target runs in an independent context
2. it needs the doctrine itself rather than a task-specific outcome
3. neither the established composition style nor an existing parent-discipline pointer or invocation branch supplies it
4. omission creates a concrete observed behavior variance, not a hypothetical one
5. sibling principles receive equivalent cross-skill treatment

Keep phase outputs beside the phase, but keep definitions and caveats in the canonical home. A sub-rule should not become more prominent across the workflow than its parent discipline. Do not fan a concept across skills merely because each could execute without it.

Choose the smallest correct form using the `writing-for-agents` information hierarchy: existing step, in-skill reference, disclosed reference, or a new skill. Create a new skill only for a distinct invocation branch or a sequence that genuinely needs a context boundary. Treat a concept integrated beneath an existing doctrine as reference, not as a new invocation branch: do not enumerate its sub-rules, examples, or caveats in the model-facing description. Change a description only when users with a genuinely distinct top-level need would not reliably reach the skill through its existing triggers. When it does change, rebalance the whole description as an invocation map rather than a content summary: keep one trigger per genuine branch, remove triggers for behavior the skill does not execute, and give the new concept no extra prominence merely because it is new. Update a router or index only when discoverability changes.

Present the user with:

- the recommended canonical home and form
- text to retain, merge, rewrite, replace, or remove
- every additional file proposed, with its independent reason
- leading word and trigger wording
- conflicts and how the proposal resolves them
- explicit non-targets

Wait for approval of this exact placement. Editing starts only after approval.

**Complete when:** the user has approved the file list, form, conflict resolution, and invocation language.

## 5. Edit the approved surface

Read each approved file and its relevant references completely before editing. Make the smallest cohesive edits.

Keep one meaning in one authoritative place. Additional sites point or record phase-local outcomes instead of restating doctrine. Prefer positive steering, preserve the target skill's vocabulary and information hierarchy, and remove superseded wording approved in Step 4.

Stay inside the approved file list and preserve unrelated worktree state. If implementation reveals another required location or changes the overlap analysis, return to Step 4 for approval.

**Complete when:** every approved edit is present, no unapproved file changed, and unrelated worktree state is preserved.

## 6. Review the integration

Review the diff against `writing-for-agents`:

- predictable invocation and execution
- one single source of truth
- strong context pointers
- checkable completion criteria
- co-location and progressive disclosure
- no duplication, sediment, sprawl, no-ops, or avoidable negation

Repeat the no-op test against the final wording. If utility was uncertain before editing, rerun the same fresh-context probes with the final rule.

Review against the target workflow too: sibling principles receive consistent treatment, and the concept has not been promoted into phases that only carry its outcomes. Repeat the composition symmetry test against the final diff: cross-skill wiring must match the collection's existing style and the treatment of peer doctrines. For engineering concepts, verify that ownership, invariant encoding, boundary policy, module depth/locality, and public test seams remain at least as strong.

For every changed file beyond the canonical home, repeat the placement test from Step 4. Remove any edit that no longer earns its place.

**Complete when:** behavioral evidence still supports the addition, every remaining line changes behavior intentionally, and every changed file passes its placement test.

## 7. Validate and report

Run `git diff --check`, validate Markdown links and skill frontmatter, and compare the final changed-file set with the captured baseline and approved list. Run any collection-specific validation available for edited metadata.

Report:

- overlap-map findings
- admissibility evidence and final disposition
- canonical home
- leading word and invocation decision
- changed files and why each changed
- important non-targets
- conflicts resolved and residual risks
- validation results
- local customizations future upstream synchronization must preserve

Leave changes uncommitted unless the user asks for a commit.

**Complete when:** validation passes, the final report accounts for every changed file, and the concept has exactly one canonical definition.
