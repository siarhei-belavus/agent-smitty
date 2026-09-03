---
name: setup-federated-workflow
description: Configure independent Code Host bindings and human-confirmed Work Tracker, Routing Label, Domain Orientation, and Domain Federation bindings, including Establish and Join operations.
---

# Setup Federated Workflow

Prepare final-state repository-owned workflow configuration. Research and human confirmation establish authority; repository Markdown is the durable interface.

## Process

### 1. Classify the operation

Read the current repository instructions and `docs/agents/`, then read [provider concepts](../federated-workflow/PROVIDER-CONCEPTS.md) and [domain orientation](../federated-workflow/DOMAIN-ORIENTATION.md). When the request or current configuration establishes, joins, or changes a federation, read [domain federation configuration](../federated-workflow/DOMAIN-FEDERATION.md) before classifying the request as:

- configure one repository without federation membership;
- **Establish Domain Federation** with the current or explicitly selected repository as Home and one or more initial members;
- **Join Domain Federation** for exactly one member and its existing Home.

Establish Domain Federation creates the accepted Home, initial reciprocal member bindings, and Federated Context Map. Join Domain Federation adds one Member binding and updates its existing Home map without moving Home authority.

A Map-affecting delivery changes mapped contexts, context ownership or participation, External Systems, relationships, or Home authority. A Domain Federation Home Transfer is a Map-affecting delivery that moves Home authority and the artifacts it owns.

If an existing binding points to another Home, or the requested change would move the map or federation-wide decisions, route a Domain Federation Home Transfer as a normal Map-affecting delivery. Setup stops without changing files. Classification is complete when exactly one supported operation remains.

### 2. Research current truth

For a single repository without federation, research only that repository. For Establish, discover broadly but grant no membership from discovery. Spawn repository research subagents for candidate repositories, then context research subagents across every repository that may own or participate in each candidate context. For Join, research the joining repository and Home only.

Read [provider binding contracts](../federated-workflow/PROVIDER-BINDINGS.md). Inspect repository identity, remote, Base Branch, instructions, existing bindings, maps, canonical contexts, ADRs, CI/deployment evidence, provider capabilities, and user changes.

For every proposed Ticket Origin, inspect provider documentation, capability metadata, and representative existing artifacts against every Work Tracker requirement in the loaded contracts before asking the human about the mapping. Require one binding-directed Context Assembly acquisition and translation procedure for every public profile, with provider-specific commands, pagination, relationship traversal, credential use, diagnostics, and authorized fallbacks owned only by that binding. Prefer native operations and identify a durable body or comment fallback for every missing native mechanism.

Establish **target-format awareness** for every human-facing provider field the workflow may write. Determine the field's actual storage and rendering format from provider documentation, API metadata, and representative existing artifacts. Distinguish formats such as Markdown dialects, provider-native wiki markup, structured document JSON, HTML, and plain text instead of inferring Markdown from a string-valued API field or from a workflow template. Record the native syntax, escaping rules, field-specific differences, and a non-destructive rendering-validation method in the repository-owned provider binding.

Research is complete when the selected branch has evidence for every required artifact and decision: repository-owned provider and Domain Orientation bindings for the single-repository branch; full proposed topology, context ownership, participation, relationships, External Systems, and Ticket Origin roles for Establish or Join. Each Ticket Origin must also have one complete draft Work Tracker mapping that passes the loaded contracts. Missing evidence or ambiguity that prevents a complete proposal stops research. Supported alternatives remain explicit in the complete proposal for human confirmation.

### 3. Obtain branch authority

For a repository without federation, present its portable repository identity, repository-owned Code Host binding, Work Tracker and Routing Label bindings, Domain Orientation, and required files. Present the complete Work Tracker artifact and Context Assembly mapping as one proposal. Confirm the current repository as the Ticket Origin. Do not propose a Home, member role, reciprocal binding, or federated map.

For Establish or Join, present one recommended complete topology: Home, boundary, members, External Systems, the Ticket Origin status of each repository, contexts, owners, participants, responsibilities, relationships, and required domain documents. Include one complete Work Tracker artifact and Context Assembly mapping for every Ticket Origin. Discuss each material ambiguity separately. Unresolved ownership or provider mapping stops setup.

Confirmation is complete when the human has accepted every item required by the selected branch, including material provider ambiguities, and no placeholder, empty canonical document, partial Work Tracker binding, or `TODO` ownership remains.

### 4. Draft and preflight every write

Draft final content against the loaded provider and domain contracts. Preserve compatible files and patch the smallest coherent sections; never regenerate an existing file merely because its layout differs. Treat workflow templates as semantic shapes and render each provider-bound field in its configured native format. Translate headings, lists, links, code, tables, and placeholders before constructing the API payload. The draft is incomplete while it contains unsupported source markup or lacks a way to verify the target rendering.

Run the [complete read-only preflight](references/preflight-and-validation.md#complete-read-only-preflight) against every target. Begin confirmation only after the gate passes.

### 5. Confirm the exact change

Show one complete English plan and the file-level diff for all repositories. State which existing user changes will be preserved or overlapped. Let the human edit the draft. No write begins until this second confirmation accepts the complete change set.

### 6. Apply in branch order

For Establish, assign one application subagent to each initial member, in parallel up to capacity. After every member succeeds, use a separate subagent for the Home. For Join, change only the joining member, validate it, then update the Home. Ordinary single-repository configuration changes only that repository.

Application writes validated checkouts in place and leaves changes uncommitted. It does not switch branches, stash, commit, push, create a probe artifact, or create/update a Review Proposal. On unexpected failure, stop, report actual changes, resolve the blocker, and rerun this idempotent setup. Application is complete only when every intended file matches the confirmed draft.

### 7. Validate current truth

After application, spawn a fresh validation subagent to execute the selected branch under [result validation](references/preflight-and-validation.md#result-validation). Validate representative structured content and Context Assembly invocations without a mutating probe. Confirm that one dedicated assembly subagent returns one new Markdown file and final result, and that downstream consumers receive the accepted path instead of repeating provider reads.
