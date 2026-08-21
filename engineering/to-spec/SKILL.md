---
name: to-spec
description: Synthesize accepted planning authority into a Work Tracker specification.
disable-model-invocation: true
---

Synthesize a specification from accepted planning authority and codebase understanding. Planning authority may be the current conversation, a supplied Wayfinder map reference, or both. Do not interview the user; use only what the selected sources establish.

Read [planning artifact contracts](../federated-workflow/PLANNING-ARTIFACTS.md) before producing the specification.

## Process

1. Select and load the planning source:

   - With no Wayfinder map reference, use the accepted decisions and Domain Model Deltas in the current conversation.
   - With a Wayfinder map reference, load the map through the configured Work Tracker binding, then re-read every final `## Resolution` linked from its Decisions-so-far. The linked Resolutions, not their one-line map gists, carry the durable decisions and deltas. If the destination still has open decision tickets or material fog, return it to Wayfinder instead of guessing.
   - When both sources are supplied, treat the durable map and linked Resolutions as the baseline and add only explicitly accepted decisions from the current conversation. Surface contradictions instead of silently choosing one source.

2. Perform configured Domain Orientation, then explore the referenced repositories only as needed to understand current state. Use the loaded effective planning language and applicable ADRs throughout.

3. Materialize the planning records established by discovery or planning. Use bounded source validation to resolve their pointers. Return unresolved material questions to discovery or planning.

4. Sketch out the complete set of seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

When materially different caller-facing ownership, interface, seam, or contract choices remain possible, use the `codebase-design` skill before proposing the set. For each seam, propose the smallest faithful repository-native test approach and its nearest prior art. Check with the user that the complete seam set and proposed approaches match their expectations; the confirmed records are settled.

5. Assemble Testing Decisions from the confirmed seam set.

6. Write the spec using the template below, then publish it to the Ticket Origin Repository's configured Work Tracker. A specification is planning authority, not an executable delivery ticket; do not apply an execution Routing Label solely because the specification was published.

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

<Repository Reference records>

## Context Scope

The complete relevant Context Scope record. If no canonical context applies, write `None — <reason>`.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be built/modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Identify the owning Repository ID for every repository-owned decision.

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

<Test behavior decisions and Settled Seam records>

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
