# Preflight and Validation

## Complete read-only preflight

Resolve every target checkout and record, without writing:

1. repository ID, exact origin remote, configured Base Branch and current HEAD;
2. current branch/worktree state and every user change;
3. applicable root/nested instructions, canonical contexts, maps, and ADRs;
4. each repository's independent Code Host binding; every human-confirmed
   Ticket Origin and its independent Work Tracker and Routing Label bindings;
   Domain Orientation and Home bindings; and conflicting or partial prior setup;
5. each Ticket Origin's ordinary Delivery frontier prose, judged for an
   authoritative locator; query, eligibility, ordering, and blocker treatment;
   authoritative exact-candidate re-read; Workflow Identity claim and
   authoritative verification; race recovery; and successful empty-frontier
   behavior;
6. provider-readable locators, tickets, comments, labels, assignees,
   dependencies, Workflow Identity when exposed, and capability metadata, with
   write scope marked verified or unverified rather than tested by mutation;
7. every intended file, whether create/patch/preserve, and exact overlap with
   user changes;
8. application-agent scopes, proving they do not overlap;
9. the complete final diff and validation commands.

Fail closed on wrong identity/Base Branch, unresolved context ownership,
conflicting instructions, unapproved overlap, missing provider access, a
Home-Transfer request, incomplete/ambiguous/contradictory Delivery frontier
knowledge, or any target whose final content cannot be drafted.
Preflight is one gate across the complete operation; do not partially apply a
target that passed while another remains unresolved.

## Result validation

Validate members before the Home, then validate the whole federation:

- every Git repository has its own explicit Code Host binding matching origin
  and Base Branch;
- only human-confirmed Ticket Origin repositories have their own Work Tracker
  and Routing Label bindings;
- provider locators and required metadata are readable non-destructively;
- every member points to the exact Home identity and the Home map records each
  exact member identity and responsibility;
- canonical pointers resolve to substantive owner documents;
- context ownership is unique; participants and External Systems are correctly
  classified; relationship endpoints exist;
- the Home owns the map/federation decisions and no product language merely
  because it is Home;
- no credential, account binding, machine-local path, registry, probe artifact,
  commit, branch, or Review Proposal was created;
- a second preview produces an empty diff.

Report exact changed files, preserved user changes, validation evidence, and
any capability that remained non-destructively unverified.
