# Preflight and Validation

## Complete read-only preflight

Resolve every target checkout and record, without writing:

1. repository ID, exact origin remote, configured Base Branch and current HEAD;
2. current branch/worktree state and every user change;
3. applicable root/nested instructions, canonical contexts, maps, and ADRs;
4. every configured provider and domain binding, plus conflicting or partial prior setup;
5. each Ticket Origin's complete Work Tracker binding, judged against the provider-binding contract, including its ordinary Delivery frontier prose;
6. provider-readable locators, tickets, comments, labels, assignees, dependencies, Workflow Identity when exposed, and capability metadata, with write scope marked verified or unverified rather than tested by mutation;
7. every intended file, whether create/patch/preserve, and exact overlap with user changes;
8. application-agent scopes, proving they do not overlap;
9. the complete final diff and validation commands.

Fail closed on wrong identity/Base Branch, unresolved context ownership, conflicting instructions, unapproved overlap, missing provider access, a Home-Transfer request, incomplete, ambiguous, or contradictory provider-binding knowledge, or any target whose final content cannot be drafted. Preflight is one gate across the complete operation; do not partially apply a target that passed while another remains unresolved.

## Result validation

Validate members before the Home, then validate the whole federation:

- every provider binding satisfies the loaded provider contract and its locators and required metadata are readable non-destructively;
- every member points to the exact Home identity and the Home map records each exact member identity and responsibility;
- canonical pointers resolve to substantive owner documents;
- context ownership is unique; participants and External Systems are correctly classified; relationship endpoints exist;
- the Home owns the map/federation decisions and no product language merely because it is Home;
- no credential, account binding, machine-local path, registry, probe artifact, commit, branch, or Review Proposal was created;
- a second preview produces an empty diff.

Report exact changed files, preserved user changes, validation evidence, and any capability that remained non-destructively unverified.
