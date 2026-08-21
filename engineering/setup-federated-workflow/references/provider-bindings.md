# Provider Bindings

Every configured Git repository owns `docs/agents/code-host.md`. Only a
human-confirmed Ticket Origin Repository owns
`docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`.
`AGENTS.md` or `CLAUDE.md` indexes only the bindings that repository owns.

## Code Host

Use this semantic structure:

```markdown
# Code Host: <provider>

## Binding
- Repository ID: `<portable-id>`
- Remote: `<git-remote>`
- Base Branch: `<branch>`

## Repository operations
## Published Delivery Heads
## Review Proposals
## Review Feedback
## Workflow Identity permissions
## Binding validation
```

The binding names the explicit host/repository locator, CLI/API and Git
interfaces, permanent repository/revision references, exact-revision fetch and
publication, one Review Proposal per changed delivery, draft/WIP state,
proposal-revision verification, actionable feedback, and non-destructive
validation.

For GitLab use `git`, `glab repo view`, `glab api`, and `glab mr`; for GitHub
use `git`, `gh repo view`, `gh api`, and `gh pr`. Validate readable repository,
Base Branch, proposal, feedback, and draft/revision metadata without creating
branches, commits, comments, or proposals.

The least-privilege envelope permits read/fetch, publishing a delivery head,
creating/updating its single proposal, reading feedback, and updating proposal
description/draft state. It excludes protected-base push, merge/accept/submit,
administration, and deletion of human artifacts. Record no account, credential,
local path, Work Tracker routing, or ticket scope.

## Work Tracker

Use this semantic structure:

```markdown
# Work Tracker: <provider>

## Binding
## Ticket operations
## Routing
## Dependencies
## Claims
## Delivery frontier
## Coordination log
## Triage request surfaces
## Wayfinding operations
## Workflow Identity permissions
## Binding validation
```

The Binding records provider, explicit authoritative locator, CLI/API, and
canonical ticket-reference form. Git remotes may inform setup but never select
the configured Work Tracker at runtime.

Document provider-native create/read/list/comment/label/assign/transition/close;
native blocking relationships; claim acquire/re-read/release; append-only
coordination comments and permanent references; and Wayfinding separately from
the Delivery frontier. Write `## Delivery frontier` as ordinary instructions an
agent can read. Define candidate queries, eligibility, ordering, provider
re-reads, and race recovery without an executable Markdown schema or a
project-specific adapter. Events may narrow a query, but they are hints. Re-read
every candidate before claiming it.

`docs/agents/triage-labels.md` is the sole mapping for `needs-triage`,
`needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. Validate every
mapped label. Missing labels may be created only after preview and confirmation;
existing labels are not renamed or deleted.

The least-privilege envelope permits ticket/dependency reads, coordination
comments, Routing Label transitions, and acquisition/release of the Workflow
Identity's own claim. It excludes administration and contains no credentials.
Validation reads the locator, tickets, comments, labels, assignees,
dependencies, Workflow Identity when the provider exposes it, and provider
capability metadata. It creates no probe ticket, comment, label, assignment, or
other mutation.
