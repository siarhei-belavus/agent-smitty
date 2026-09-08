# Handoff-Only Recovery

After [recovery](RECOVERY.md) has published the Resumption Record for this branch, start a normal Execution Attempt with zero Implementation Agents. Re-read exact heads, evidence, proposals, ticket claim, routing, and the deterministic handoff key. Apply only the missing effects through [Hand off idempotently](SKILL.md#9-hand-off-idempotently), including the final checkpoint and comment presentation requirements, and reuse any matching note or proposal.

**Complete when:** the Delivery Bundle handoff is complete and no implementation, duplicate handoff, duplicate proposal, or unrelated mutation occurred.
