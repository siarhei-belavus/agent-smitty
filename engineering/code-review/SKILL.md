---
name: code-review
description: Review fixed Repository Targets. Use when the user asks to review a branch, PR, committed delivery, or worktree; asks for a multi-repository Delivery Bundle review; or asks for Standards-only or Spec-only review.
---

Review committed or worktree changes since fixed points without modifying the reviewed repositories or external collaboration state.

Read [delivery records](../federated-workflow/DELIVERY-RECORDS.md) before resolving targets or review authority. When review authority is Work Tracker-backed, read [Work Tracker context assembly](../federated-workflow/WORK-TRACKER-CONTEXT-ASSEMBLY.md) before accepting a target.

## Public input

A Fixed point is the caller-selected revision used to anchor review bounds. A Repository Target is one repository's immutable review input, pinned to a Fixed point and exact Review head or WIP snapshot.

Accept one or more fixed Repository Targets. A single repository is the one-element case. Each target records:

- **Repository ID**;
- repository or worktree path;
- **Fixed point**;
- **Review head** as an exact commit SHA;
- **Authoritative sources**;
- an **Authority input** record for the authority under review;
- **Settled seams** and test approaches relevant to that target;
- repository validation evidence bound to the Review head for a committed target or bound to both the Review head and Worktree snapshot ID for WIP, when supplied.
- for explicit WIP review, a **Worktree snapshot ID** that identifies the captured uncommitted content.

For Work Tracker-backed authority, Authority input contains the exact selected profile, permanent root, explicit `Complete` result, and complete lossless Context Pack. Select Decision Context for a Decision Ticket or Specification, Delivery Context for delivered work rooted in a Delivery Ticket, Task, or Bug, and Map Context only when the Map itself is under review. A caller that already assembled this record supplies it unchanged. Retain it for every selected review axis and reviewer. Do not rebuild provider authority, infer another root, switch profiles, or let a reviewer rediscover the provider.

When the user directly supplies a Work Tracker reference without an assembled Authority input, assemble the matching profile for that exact permanent root before accepting the target. Only `Complete` continues. `Incomplete` or `Ambiguous` stops at clarification or the applicable human boundary. A Work Tracker reference inferred only from commits is not authority and does not authorize provider lookup.

For authority that is not Work Tracker-backed, Authority input contains the supplied local specification, current user direction, or other non-provider authority. It has no invented Context Pack, profile, or result.

For the existing single-repository form, the user may supply only a fixed point; use the current repository and resolve the current `HEAD` as the exact Review head. When the single-repository worktree is dirty and the user did not select committed or WIP review, disclose the dirty state and ask whether those changes are in scope. Preserve explicit worktree/WIP review by identifying it with both the current exact `HEAD` and an immutable Git tree snapshot of the tracked, staged, and untracked content.

Select one review mode:

- **Standards only**;
- **Spec only**;
- **Both (the standalone default)**.

Do not silently add an unselected axis.

**Complete when:** every target has one Authority input; every Work Tracker-backed record has one exact compatible profile and permanent root, explicit `Complete`, and a lossless Context Pack; every non-Work-Tracker record retains its supplied authority without invented Context Assembly fields; and the selected axes are explicit.

## Process

### 1. Pin every target

Resolve every Fixed point and Review head once in its target repository. Compute `git merge-base <fixed-point> <review-head>` once and record the returned commit SHA as the exact **Comparison base** for that target. For committed review, use `<fixed-point>...<review-head>` and record `git log <comparison-base>..<review-head> --oneline`. Do not recompute the Comparison base from moving refs during freshness checks.

For explicit worktree review, capture one canonical Git tree without changing the reviewed repository's index, worktree, or object database. Create a temporary object store and a new temporary Git index outside the repository. Set `GIT_OBJECT_DIRECTORY` to the temporary object store, set `GIT_ALTERNATE_OBJECT_DIRECTORIES` to the reviewed repository's object directory plus its configured alternates, and set `GIT_INDEX_FILE` to the temporary Git index for every snapshot and diff command. Resolve and use the target repository root as the working directory for every capture command. With those variables set, run `git read-tree <review-head>`, `git add -A -- :/` using the top-anchored pathspec `:/`, and `git write-tree`, then record the returned tree object ID as the **Worktree snapshot ID**. Git's canonical tree serialization includes tracked, staged, deleted, renamed, symlink, submodule, and non-ignored untracked state as it would be committed, regardless of the original working directory. Materialize `git diff --binary <comparison-base> <worktree-snapshot-id>` into a read-only temporary file outside the repository and record its SHA-256 digest; this is the **immutable materialized diff** supplied to every selected reviewer so they do not need access to the temporary object store. Include the Comparison base, tree object ID, and diff digest in validation and reviewer inputs. Repeat the same temporary-store capture and materialization against the same exact Comparison base before reporting; when the snapshot ID changes or the diff digest changes, the review is stale and must restart. Keep the materialized diff available through aggregation, then remove all temporary evidence. If the target cannot be represented by that Git tree, require a committed target instead of claiming WIP freshness.

Confirm each target resolves and has a non-empty selected change set before starting reviewers. A bad ref or empty target fails here. Do not substitute a branch tip or later `HEAD` for the captured Review head.

Apply the complete Evidence freshness rule below before starting reviewers and again before reporting results.

### 2. Identify authoritative sources and seams

Use the Authority input and sources supplied with the Repository Targets first. Otherwise find non-Work-Tracker authority in this order:

1. a local specification or resolved decision path supplied by the user;
2. a matching file under `docs/`, `specs/`, or `.scratch/`;
3. ask the user only when the selected Spec axis has no authoritative source.

An issue reference found in a commit message is a provenance clue only. Do not follow it into a Work Tracker or treat it as authority without an explicit root and a `Complete` Authority input. For supplied Work Tracker Authority input, use its full pack as the authoritative source set. Do not replace it with individual ticket reads, summaries, or a newly discovered provider source.

Start with supplied seam records, then validate every seam against current authoritative sources. Explicit current user direction, specifications, and resolved decisions take precedence over earlier sources and existing public interfaces. Record source conflicts as Spec findings. When no authoritative source settles a seam, mark it unsettled and assess its shape using the `codebase-design` baseline rather than choosing a design during review.

**Complete when:** every Work Tracker-backed target still uses its supplied exact profile, permanent root, `Complete` result, and lossless Context Pack; every other target has the best available non-provider authority; and every seam is settled, explicitly conflicting, or marked unsettled.

### 3. Build repository-local Standards baselines

For each target, read that repository's instructions and documented standards. Add the following Fowler smell baseline from *Refactoring*, ch. 3, unless an authoritative source or documented repository standard explicitly overrides it. Every smell is a judgement call, never automatically a violation:

- **Mysterious Name** — a name does not reveal what it does or holds.
- **Duplicated Code** — the same logic shape appears in more than one changed place.
- **Feature Envy** — behavior reaches into another object's data more than its own.
- **Data Clumps** — the same fields or parameters repeatedly travel together.
- **Primitive Obsession** — a primitive stands in for a domain concept.
- **Repeated Switches** — repeated conditional dispatch uses the same discriminator.
- **Shotgun Surgery** — one logical change requires scattered edits.
- **Divergent Change** — one module changes for unrelated reasons.
- **Speculative Generality** — unused abstraction or compatibility machinery has no required behavior.
- **Message Chains** — callers navigate through a long object chain.
- **Middle Man** — a module mostly delegates without adding depth.
- **Refused Bequest** — an inheritor ignores most of its inherited contract.

Determine per target whether the change introduces or reshapes a module, interface, seam, adapter, logical ownership, physical decomposition, or contract. When it does, require the Standards Reviewer to read the `codebase-design` skill in full and apply its deletion test and proportional-design rules.

Route requirement or settled-decision violations to Spec. Route structural and change-pressure findings to Standards.

### 4. Run the selected fresh reviews

A full pass continues after every finding and finishes the complete selected axis before the reviewer returns. Give every reviewer this shared completion brief:

> Audit every member of the finite input sets applicable to the selected axis: changed files; repository rules and heuristics for Standards or authoritative requirements and decisions for Spec; Settled Seams and their named providers and consumers; and supplied validation claims. Return all material findings from the full pass together. Include a **Coverage receipt** with audited/total counts for each applicable set. State why a set is not applicable. Coverage is incomplete while any item remains unaccounted for.

For the Standards axis, start one fresh Standards Reviewer per selected Repository Target. Give each reviewer only its captured target, commit list, repository-local standards, smell baseline, design trigger result, authoritative seam context, complete Authority input, and this brief. For a Work Tracker-backed target, pass the exact selected profile, permanent root, `Complete` result, and lossless Context Pack unchanged, and forbid provider lookup or profile switching. For a WIP target, the captured target includes the Worktree snapshot ID and immutable materialized diff with its recorded digest; require the reviewer to inspect that diff rather than the mutable worktree.

> Report all material Standards findings per file and hunk. Cite the violated rule or name the relevant heuristic. Label a finding **Blocking** only for a mandatory-standard violation or a structural flaw with a credible future bug or material change-pressure path; label other material findings **Advisory**. Omit mechanical issues reliably enforced by configured tooling.

For the Spec axis, start one fresh Bundle Spec Reviewer over the complete selected target set. Give it all captured targets and diffs, complete Authority input records, authoritative sources, settled seams, repository validation evidence, and this brief. Pass every Work Tracker-backed profile, permanent root, `Complete` result, and lossless Context Pack unchanged, and forbid provider lookup or profile switching:

> Report missing or partial requirements, scope creep, incorrect behavior, unauthorized seam changes, acceptance behavior outside a settled seam, and required behavior not verified through that seam. Route each finding to the affected Repository IDs. Label a finding **Blocking** when it demonstrates a requirement or settled-decision violation or a reachable correctness regression; label other material findings **Advisory**.

Run fresh reviewers concurrently where harness capacity permits; freshness and complete inputs matter, not a particular internal agent topology. If the selected Spec axis has no source after the user confirms none exists, skip that reviewer and report `no spec available`.

**Complete when:** every reviewer has returned one full-pass result whose Coverage receipt accounts for every changed file, applicable axis input, Settled Seam, named provider and consumer, and supplied validation claim.

### 5. Aggregate without merging axes

For each selected axis only, emit its result and counts. When Standards is selected, report it separately for every repository, using one section per target:

`## Standards — <Repository ID>`

When Spec is selected, report the whole-bundle result once:

`## Spec — selected targets`

Omit the unselected axis entirely. When both are selected, do not merge, reclassify, or rerank the axes. Include the Coverage receipt with each result. End with Blocking and Advisory counts and the highest-severity finding within each selected result when present.

Publish no branch, create or update no Review Proposal, and change no Work Tracker state. Report findings and evidence only.

## Evidence freshness

Every finding and pass result is bound to the captured exact Review heads, each target's Authority input, and, for WIP, the Worktree snapshot ID. Report the selected profile, permanent root, and `Complete` result with every Work Tracker-backed review result. Changed heads, snapshot IDs, or caller-supplied Authority input invalidate affected repository validation and Standards results; any Spec result influenced by a changed target or Authority input is stale. Require refreshed evidence and a new fixed target rather than carrying an earlier pass forward.
