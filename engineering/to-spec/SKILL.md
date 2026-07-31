---
name: to-spec
description: Turn the current conversation into a spec and publish it to the configured Work Tracker — no interview, just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec (you may know this document as a PRD). Do NOT interview the user — just synthesize what you already know.

Read the shared [federated planning authority contract](../FEDERATED-AUTHORITY.md) before producing the specification. Use the configured Work Tracker and Domain Orientation when their bindings exist; preserve standalone behavior when they do not.

## Process

1. Perform configured Domain Orientation, then explore the referenced repositories only as needed to understand current state. Use the effective planning language throughout: oriented Canonical Context Documents followed by relevant accepted Domain Model Deltas. Respect applicable ADRs.

2. Materialize the complete solution-level Repository References and Context Scope already established by discovery or planning. Bounded source validation is allowed; do not begin new open-ended discovery. Return unresolved material questions to discovery or planning.

3. Sketch out the complete set of seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

When materially different caller-facing ownership, interface, seam, or contract choices remain possible, run `/codebase-design` before proposing the set. For each seam, propose the smallest faithful repository-native test approach and its nearest prior art. Check with the user that the complete seam set and proposed approaches match their expectations; the confirmed records are settled.

4. Record every confirmed repository-local and cross-repository seam only in Testing Decisions, using the complete fields from the shared contract. Preserve full-fidelity Domain Model Deltas, architecture rationale, provenance, and canonical documentation obligations in Context Scope and the applicable decisions.

5. Write the spec using the template below, then publish it to the Ticket Origin Repository's configured Work Tracker. A specification is planning authority, not an executable delivery ticket; do not apply an execution Routing Label solely because the specification was published.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Repository References

The complete confirmed solution-level repository set. For each repository include Repository ID, remote, and Base Branch. References grant no write authority.

## Context Scope

The complete relevant set of Repository-qualified Context Pointers, plus every accepted Domain Model Delta and its provenance and canonical documentation obligations. If no canonical context applies, write `None — <reason>`.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be built/modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Identify the owning Repository ID for every repository-owned decision. Preserve applicable accepted architecture rationale and rejected alternatives in full.

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Every repository-local and cross-repository settled seam, including its owning module and Repository ID, providers and consumers, caller/test-visible interface, location, status, observable behavior, validation obligations and evidence, selected repository-native approach, and nearest prior art

This is the sole specification section that owns settled seams. Do not add Repository Scope or a separate Cross-Repository Seams section to a specification.

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
