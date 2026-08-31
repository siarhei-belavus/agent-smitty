# Publish feedback

Publication turns approved human judgement into durable Code Host state. It does not complete the review round.

Read the affected repository's instructions and Code Host binding. Require the binding and current provider identity to permit publication of human-approved Review Feedback. Resolve and re-read the Review Proposal's permanent reference, source, target, base, exact head, and existing discussions before writing.

For each approved draft:

1. Bind code-specific feedback to the exact head and diff position supported by the provider. Prefer a resolvable discussion.
2. Publish general feedback only when its text makes the required action explicit.
3. Before retrying an uncertain request, re-read existing feedback and match the intended body and position so the retry cannot create a duplicate.
4. Re-read the created note or discussion through the provider. Record its permanent proposal, discussion, and note identifiers, exact head, location, body, author-visible state, and resolved state.

Treat a provider response without a permanent re-readable item as an incomplete publication. Preserve the approved draft and report the failure without creating a substitute comment elsewhere.

Leave the delivery ticket, Review Proposal draft state, source branch, and target branch unchanged. Publication authority does not grant approval, merge, code mutation, or Work Tracker routing authority.

**Complete when:** every approved draft exists exactly once on the intended Review Proposal, is unresolved or explicitly actionable, and has a permanent provider reference verified by re-read; otherwise the exact unverified item and preserved draft have been returned without further mutation.
