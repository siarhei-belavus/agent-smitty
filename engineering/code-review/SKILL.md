---
name: code-review
description: Review fixed Repository Targets. Use when the user asks to review a branch, PR, committed delivery, or worktree; asks for a multi-repository Delivery Bundle review; or asks for Standards-only or Spec-only review.
---

Review committed or worktree changes since fixed points without modifying the reviewed repositories or external collaboration state.

## Public input

Accept one or more fixed Repository Targets. Treat the existing single-repository invocation as the one-element case. Each target records:

- **Repository ID**;
- repository or worktree path;
- **Fixed point**;
- **Review head** as an exact commit SHA;
- **Authoritative sources**;
- **Settled seams** and test approaches relevant to that target;
- repository validation evidence bound to the Review head, when supplied.
- for explicit WIP review, a **Worktree snapshot ID** that identifies the captured uncommitted content.

For the existing single-repository form, the user may supply only a fixed point; use the current repository and resolve the current `HEAD` as the exact Review head. When the single-repository worktree is dirty and the user did not select committed or WIP review, disclose the dirty state and ask whether those changes are in scope. Preserve explicit worktree/WIP review by identifying it with both the current exact `HEAD` and an immutable Git tree snapshot of the tracked, staged, and untracked content.

Select one review mode:

- **Standards only**;
- **Spec only**;
- **Both (the standalone default)**.

Do not silently add an unselected axis.

## Process

### 1. Pin every target

Resolve every Fixed point and Review head once in its target repository. For committed review, use `<fixed-point>...<review-head>` and record `git log <fixed-point>..<review-head> --oneline`.

For explicit worktree review, capture one canonical Git tree without changing the real index or worktree. Point `GIT_INDEX_FILE` at a new temporary Git index, run `git read-tree <review-head>`, `git add -A -- .`, and `git write-tree`, then record the returned tree object ID as the **Worktree snapshot ID**. This uses Git's canonical tree serialization and includes tracked, staged, deleted, renamed, symlink, submodule, and non-ignored untracked state as it would be committed. Review the immutable change set with `git diff <merge-base> <worktree-snapshot-id>` and include the tree object ID in reviewer inputs. Repeat the same temporary-index capture before reporting; when the snapshot ID changes, the review is stale and must restart. If the target cannot be represented by that Git tree, require a committed target instead of claiming WIP freshness.

Confirm each target resolves and has a non-empty selected change set before starting reviewers. A bad ref or empty target fails here. Do not substitute a branch tip or later `HEAD` for the captured Review head.

Apply the complete Evidence freshness rule below before starting reviewers and again before reporting results.

### 2. Identify authoritative sources and seams

Use sources supplied with the Repository Targets first. Otherwise find the originating spec in this order:

1. issue references in commit messages, following `docs/agents/issue-tracker.md` when present;
2. a spec, ticket, or resolved decision path supplied by the user;
3. a matching file under `docs/`, `specs/`, or `.scratch/`;
4. ask the user only when the selected Spec axis has no authoritative source.

Start with supplied seam records, then validate every seam against current authoritative sources. Explicit current user direction, specifications, and resolved decisions take precedence over earlier sources and existing public interfaces. Record source conflicts as Spec findings. When no authoritative source settles a seam, mark it unsettled and assess its shape under the `/codebase-design` baseline rather than choosing a design during review.

### 3. Build repository-local Standards baselines

For each target, read that repository's instructions and documented standards. Add the following Fowler smell baseline unless an authoritative source or documented repository standard explicitly overrides it. Every smell is a judgement call, never automatically a violation:

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

Determine per target whether the change introduces or reshapes a module, interface, seam, adapter, logical ownership, physical decomposition, or contract. When it does, the Standards Reviewer reads `/codebase-design` in full and applies its deletion test and proportional-design rules.

Route requirement or settled-decision violations to Spec. Route structural and change-pressure findings to Standards.

### 4. Run the selected fresh reviews

For the Standards axis, start one fresh Standards Reviewer per selected Repository Target. Give each reviewer only its captured target, commit list, repository-local standards, smell baseline, design trigger result, authoritative seam context, and this brief:

> Report all material Standards findings per file and hunk. Cite the violated rule or name the relevant heuristic. Label a finding **Blocking** only for a mandatory-standard violation or a structural flaw with a credible future bug or material change-pressure path; label other material findings **Advisory**. Omit mechanical issues reliably enforced by configured tooling.

For the Spec axis, start one fresh Bundle Spec Reviewer over the complete selected target set. Give it all captured targets and diffs, authoritative sources, settled seams, repository validation evidence, and this brief:

> Report missing or partial requirements, scope creep, incorrect behavior, unauthorized seam changes, acceptance behavior outside a settled seam, and required behavior not verified through that seam. Route each finding to the affected Repository IDs. Label a finding **Blocking** when it demonstrates a requirement or settled-decision violation or a reachable correctness regression; label other material findings **Advisory**.

Run fresh reviewers concurrently where harness capacity permits; freshness and complete inputs matter, not a particular internal agent topology. If the selected Spec axis has no source after the user confirms none exists, skip that reviewer and report `no spec available`.

### 5. Aggregate without merging axes

Report Standards separately for every repository, using one section per target:

`## Standards — <Repository ID>`

Report the whole-bundle result once:

`## Spec — Delivery Bundle`

Do not merge, reclassify, or rerank the axes. End with Blocking and Advisory counts per repository Standards result and for the bundle Spec result, plus the highest-severity finding within each result when present.

This skill does not publish branches, does not create or update Review Proposals, and does not change Work Tracker state. A review reports findings and evidence only.

## Evidence freshness

Every finding and pass result is bound to the captured exact Review heads and, for WIP, the Worktree snapshot ID. Changed heads or snapshot IDs invalidate affected repository validation and Standards results; any Spec result influenced by a changed target is stale. Require refreshed evidence and a new fixed target rather than carrying an earlier pass forward.
