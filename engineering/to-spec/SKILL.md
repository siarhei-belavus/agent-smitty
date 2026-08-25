---
name: to-spec
description: Synthesize accepted planning authority into a Work Tracker specification.
disable-model-invocation: true
---

Synthesize a specification from accepted planning authority and codebase understanding. Planning authority may be the current conversation, a supplied Wayfinder map reference, or both. Do not interview the user; use only what the selected sources establish.

Read [planning artifact contracts](../federated-workflow/PLANNING-ARTIFACTS.md) and [Work Tracker context assembly](../federated-workflow/WORK-TRACKER-CONTEXT-ASSEMBLY.md) before producing the specification.
Use the configured Work Tracker and Domain Orientation when their bindings exist; preserve standalone behavior when they do not.

## Process

1. Select and load the planning source:

   - With no Work Tracker reference, use the accepted decisions and Domain Model Deltas in the current conversation. This path needs no Wayfinder Map.
   - With a Wayfinder Map reference, assemble Map Context through the configured binding. Continue only with `Complete`. If the destination still has open decision tickets or material fog, return it to Wayfinder instead of guessing.
   - When revising or reviewing an existing Specification, assemble Decision Context for that exact artifact. Continue only with `Complete` and never switch to another profile.
   - When conversation and durable sources are both supplied, use the durable Context Pack as the baseline and add only explicitly accepted decisions from the current conversation. Return `Ambiguous` contradictions to planning instead of choosing silently.

   Source selection is complete when every selected authority has permanent provenance and every required Work Tracker profile is `Complete`.

2. Perform configured Domain Orientation, then explore the referenced repositories only as needed to understand current state. Use the loaded effective planning language and applicable ADRs throughout.

3. Materialize the complete solution-level Repository References and exhaustive Context Scope established by discovery or planning. Use bounded source validation to resolve their pointers; do not begin new open-ended discovery. Return unresolved material questions to discovery or planning.

4. Sketch out the complete set of seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

When materially different caller-facing ownership, interface, seam, or contract choices remain possible, use the `codebase-design` skill before proposing the set. For each seam, propose the smallest faithful repository-native test approach and its nearest prior art. Check with the user that the complete seam set and proposed approaches match their expectations; the confirmed records are settled.

5. Record every confirmed repository-local and cross-repository Settled Seam only in Testing Decisions. Preserve full-fidelity Domain Model Deltas, architecture rationale, provenance, and canonical documentation obligations in Context Scope and the applicable decisions.

6. Write the spec using the template below, then publish it to the Ticket Origin Repository's configured Work Tracker. When the selected Map is also the Specification under the confirmed artifact mapping, retain one artifact with both roles. Otherwise publish a separate Specification with explicit Map Authority Sources. A specification is planning authority, not an executable delivery ticket; do not apply an execution Routing Label solely because the specification was published.

7. Re-read the durable artifact and assemble Decision Context for the exact published Specification. Publication completes only with `Complete`; `Incomplete` or `Ambiguous` returns to the source or publication step that caused it.

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

The complete confirmed solution-level set of Repository Reference records. References grant no write authority.

## Authority Sources

Permanent references to every governing Map or other planning artifact, or `None — direct accepted authority is fully materialized in this Specification`.

## Context Scope

The complete relevant Context Scope record. If no canonical context applies, write `None — <reason>`.

## Implementation Decisions

Record the accepted implementation decisions. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be built/modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Identify the owning Repository ID for every repository-owned decision.
Preserve applicable accepted architecture rationale and rejected alternatives in full.

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Every repository-local and cross-repository Settled Seam record

This is the sole specification section that owns settled seams. Do not add Repository Scope or a separate Cross-Repository Seams section to a specification.

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
