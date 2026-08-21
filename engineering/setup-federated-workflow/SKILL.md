---
name: setup-federated-workflow
description: Configure independent Code Host bindings and human-confirmed Work Tracker, Routing Label, Domain Orientation, and Domain Federation bindings, including Establish and Join operations.
---

# Setup Federated Workflow

Prepare final-state repository-owned workflow configuration. This is a
prompt-driven setup skill: research and confirmation establish authority;
repository Markdown remains the durable interface.

## Process

### 1. Classify the operation

Read the current repository instructions and `docs/agents/`, then classify the
request as:

- configure one repository without federation membership;
- **Establish Domain Federation** with the current or explicitly selected
  repository as Home and one or more initial members;
- **Join Domain Federation** for exactly one member and its existing Home.

If an existing binding points to another Home, or the requested change would
move the map or federation-wide decisions, route a **Domain Federation Home
Transfer** as a normal Map-affecting delivery. Setup stops without changing
files. Classification is complete when exactly one supported operation remains.

### 2. Research current truth

For Establish, discover broadly but grant no membership from discovery. Spawn
repository research subagents for candidate repositories, then context research
subagents across every repository that may own or participate in each candidate
context. For Join, research the joining repository and Home only.

Inspect repository identity, remote, Base Branch, instructions, existing
bindings, maps, canonical contexts, ADRs, CI/deployment evidence, provider
capabilities, and user changes. Treat Ticket Origin as a human-confirmed role,
independent of Home or Member status. Every Git repository owns its own Code
Host binding. Only a confirmed Ticket Origin owns a Work Tracker and Routing
Label binding. Read
[`references/domain-federation.md`](references/domain-federation.md) whenever
federation topology or context ownership is in scope. Research is complete when
every proposed member, context owner, participant, relationship, External
System, Ticket Origin role, and required artifact has evidence or is explicitly
unsettled.

### 3. Obtain topology authority

Present one recommended complete topology: Home, boundary, members, External
Systems, the Ticket Origin status of each repository, contexts, owners,
participants, responsibilities, relationships, and required domain documents.
Discuss each material ambiguity separately. A coordination-only Home never owns
product language for convenience; unresolved ownership stops setup.

This confirmation is complete only when the human has accepted the entire
topology and no placeholder, empty canonical document, or `TODO` ownership
remains.

### 4. Draft and preflight every write

Draft the final content using
[`references/provider-bindings.md`](references/provider-bindings.md) and the
domain reference. Preserve compatible files and patch the smallest coherent
sections; never regenerate an existing file merely because its layout differs.

For every confirmed Ticket Origin, read and judge the Work Tracker binding and
its ordinary `## Delivery frontier` prose. Together they must supply an
authoritative locator; the frontier query, eligibility, ordering, and blocker
treatment; an authoritative exact-candidate re-read; Workflow Identity claim
acquisition and authoritative post-claim verification; race recovery; and
successful empty-frontier behavior. Missing, ambiguous, or contradictory
knowledge stops setup with the specific gap reported. The deterministic
validator checks the section's structure and non-empty content; it does not
replace this model-driven semantic assessment.

Run the single complete read-only preflight in
[`references/preflight-and-validation.md`](references/preflight-and-validation.md)
against every target before the first write. A failed check starts no
application subagent and changes no file. Preflight is complete when every
repository, identity, Base Branch, instruction set, binding, intended artifact,
provider-readable capability, conflicting user change, and non-overlapping
application scope is accounted for.

### 5. Confirm the exact change

Show one complete English plan and the file-level diff for all repositories.
State which existing user changes will be preserved or overlapped. Let the human
edit the draft. No write begins until this second confirmation accepts the
complete change set.

### 6. Apply member-first and Home-last

For Establish, assign one application subagent to each initial member, in
parallel up to capacity. After every member succeeds, use a separate subagent
for the Home. For Join, change only the joining member, validate it, then update
the Home. Ordinary single-repository configuration changes only that repository.

Application writes validated checkouts in place and leaves changes uncommitted.
It does not switch branches, stash, commit, push, create a probe artifact, or
create/update a Review Proposal. On unexpected failure, stop, report actual
changes, resolve the blocker, and rerun this idempotent setup. Application is
complete only when every intended file matches the confirmed draft.

### 7. Validate current truth

Spawn a fresh validation subagent after application. Validate members first and
Home last. Check provider readability, reciprocal identities, context-pointer
resolution, confirmed Ticket Origin ownership, independent Code Host ownership,
absence of credentials and local paths, and idempotence. Run:

```bash
python3 scripts/validate_federation.py \
  --home '<repository-id>=<checkout>' \
  --member '<repository-id>=<checkout>' \
  --ticket-origin '<repository-id>'
```

Add one `--member` per member and one `--ticket-origin` per human-confirmed
Ticket Origin. The paths are runtime inputs and never enter durable
configuration. Completion is `configuration prepared and locally validated`;
it becomes authoritative only after all participating changes are accepted in
their configured Base Branches.
