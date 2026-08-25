# Preflight and Validation

## Work Tracker binding check

A Work Tracker binding passes when it satisfies every requirement in the loaded provider-binding and Context Assembly contracts against representative provider artifacts. Record each capability's contract-selected verification state.

## Complete read-only preflight

Resolve every target checkout and record, without writing:

1. repository ID, exact origin remote, configured Base Branch and current HEAD;
2. current branch/worktree state and every user change;
3. applicable root/nested instructions, canonical contexts, maps, and ADRs;
4. each repository's independent Code Host binding; every human-confirmed Ticket Origin and its independent Work Tracker and Routing Label bindings; Domain Orientation and Home bindings; and conflicting or partial prior setup;
5. each Ticket Origin's complete Work Tracker binding under the common check above, including its ordinary Delivery frontier prose;
6. provider-readable locators, representative artifacts, complete bodies and comments, pagination, permanent references, relationships, labels, assignees, dependencies, accepted Resolution records, Workflow Identity when exposed, and capability metadata, with write scope marked verified or unverified rather than tested by mutation;
7. every intended file, whether create/patch/preserve, and exact overlap with user changes;
8. application-agent scopes, proving they do not overlap;
9. the complete final diff and validation commands.

Judge every provider binding against the loaded provider contract. For one repository without federation, record exact marker, Git-identity, and provider-read commands. For Establish or Join, the federation validator adds deterministic marker and topology checks. Neither path replaces semantic judgment.

Fail closed on wrong identity/Base Branch, unresolved context ownership, conflicting instructions, unapproved overlap, missing provider access, a Home-Transfer request, incomplete, ambiguous, or contradictory provider-binding knowledge, a mapping that cannot preserve permanent references or reconstruct complete current authority, or any target whose final content cannot be drafted. Preflight is one gate across the complete operation; do not partially apply a target that passed while another remains unresolved.

## Result validation

For every operation:

- every provider binding satisfies the loaded provider contract and its locators and required metadata are readable non-destructively;
- every Work Tracker binding passes the common check above with its human-confirmed mapping;
- no credential, account binding, machine-local path, registry, probe artifact, commit, branch, or Review Proposal was created;
- a second preview produces an empty diff.

### One repository without federation

Validate only the current repository:

- its Repository ID, origin remote, and Base Branch agree with Git and the repository-owned Code Host binding;
- the Work Tracker locator and its required metadata are readable through its configured non-destructive validation operations;
- representative provider artifacts pass the common Work Tracker binding check;
- every Routing Label maps to a readable provider label;
- `AGENTS.md` or `CLAUDE.md` points directly to the repository-owned Code Host, Work Tracker, Routing Label, and Domain Orientation bindings;
- `docs/agents/domain.md` satisfies the loaded Domain Orientation contract and contains no `## Domain Federation` binding or Repository-qualified federated map.

Execute the exact marker, Git-identity, and provider-read commands recorded by preflight. Do not run `validate_federation.py` or supply a synthetic `--home`: that validator accepts only materialized Home/member topology.

### Establish or Join

Validate members before the Home, then validate the whole federation:

- every member points to the exact Home identity and the Home map records each exact member identity and responsibility;
- canonical pointers resolve to substantive owner documents;
- context ownership is unique; participants and External Systems are correctly classified; relationship endpoints exist.

Run:

```bash
python3 scripts/validate_federation.py \
  --home '<repository-id>=<checkout>' \
  --member '<repository-id>=<checkout>' \
  --ticket-origin '<repository-id>'
```

Add one `--member` per member and one `--ticket-origin` per human-confirmed Ticket Origin. Paths are runtime inputs and never enter durable configuration.

Report the selected branch, exact changed files, preserved user changes, validation evidence, and any capability that remained non-destructively unverified.

**Complete when:** configuration is prepared and locally validated. It becomes authoritative only after every participating change is accepted in its configured Base Branch.
