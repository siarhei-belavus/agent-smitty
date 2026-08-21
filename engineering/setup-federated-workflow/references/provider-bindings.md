# Provider Bindings

Every configured Git repository owns `docs/agents/code-host.md`. Only a human-confirmed Ticket Origin Repository owns `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. `AGENTS.md` or `CLAUDE.md` indexes only the bindings that repository owns.

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

The binding names the explicit host/repository locator, CLI/API and Git interfaces, permanent repository/revision references, exact-revision fetch and publication, one Review Proposal per changed delivery, draft/WIP state, proposal-revision verification, actionable feedback, and non-destructive validation.

For GitLab use `git`, `glab repo view`, `glab api`, and `glab mr`; for GitHub use `git`, `gh repo view`, `gh api`, and `gh pr`. Validate readable repository, Base Branch, proposal, feedback, and draft/revision metadata without creating branches, commits, comments, or proposals.

The least-privilege envelope permits read/fetch, publishing a delivery head, creating/updating its single proposal, reading feedback, and updating proposal description/draft state. It excludes protected-base push, merge/accept/submit, administration, and deletion of human artifacts. Record no account, credential, local path, Work Tracker routing, or ticket scope.

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

The Binding records provider, explicit authoritative locator, CLI/API, and canonical ticket-reference form. Git remotes may inform setup but never select the configured Work Tracker at runtime.

Describe the operational sections as ordinary instructions an agent can read:

- `## Ticket operations` gives provider-native create, read, list, comment, label, assign, transition, and close operations. It requires an authoritative re-read after each mutation.
- `## Routing` points to `docs/agents/triage-labels.md` as the sole mapping for `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. Provider events may narrow a read, but they are hints.
- `## Dependencies` uses native blocking relationships when available and names any provider-required fallback. Decisions use current blocker state.
- `## Claims` resolves the Workflow Identity, acquires a claim for only that identity, verifies authoritative assignee state after acquisition, and releases only that identity's claim at an authorized transition.
- `## Delivery frontier` defines the provider query, eligibility and blocker treatment, ordering, authoritative exact-candidate re-read immediately before claim, race recovery, and successful empty-frontier behavior. It uses the claim procedure from `## Claims`; failed verification restarts selection from current provider state.
- `## Coordination log` uses append-only comments and permanent provider references.
- `## Triage request surfaces` identifies the provider objects triage may use.
- `## Wayfinding operations` defines its planning-only map and child-ticket operations separately from the Delivery frontier.
- `## Workflow Identity permissions` grants least-privilege ticket and dependency reads, coordination comments, Routing Label transitions, and the identity's own claims. It excludes administration and records no credentials.
- `## Binding validation` reads the locator, tickets, comments, labels, assignees, dependencies, exposed Workflow Identity, and provider capability metadata. It creates no probe or other mutation.

Base every provider decision on an authoritative re-read. Keep the binding as prose, without an executable Markdown schema or a project-specific adapter. Validate every mapped Routing Label. Create a missing label only after preview and confirmation; preserve existing labels.
