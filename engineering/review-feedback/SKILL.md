---
name: review-feedback
description: Draft and publish human review feedback on an existing MR or PR, or finish that review round and return its delivery ticket for correction. Use when the user wants a review comment made actionable without running a new review.
---

# Review feedback

Turn a concern raised by the human into durable Review Feedback that a fresh delivery workflow can recover from. This skill records human judgement. It does not inspect a whole change set for new findings, approve a Review Proposal, merge it, or change product code.

Read [provider concepts](../federated-workflow/PROVIDER-CONCEPTS.md) before resolving the operation. Use only repository-owned Code Host and Work Tracker bindings for provider reads and mutations.

## Resolve the operation

Select the operations explicitly authorized by the human:

- **Draft** formulates one or more supplied concerns without changing provider state.
- **Publish** records approved drafts on one existing Review Proposal. Read [publish feedback](PUBLISH.md) before any mutation.
- **Return for correction** completes the human review round and routes its delivery ticket back to agent work. Read [return for correction](RETURN-FOR-CORRECTION.md) before any Work Tracker mutation.

A single instruction may authorize Publish followed by Return for correction only when it explicitly says both to publish the named feedback and to finish the review round. Otherwise publication leaves the review round open and the ticket unchanged.

Resolve one Review Proposal from the supplied permanent reference or the repository context and its Code Host binding. When several proposals or tickets remain plausible, show them and ask the human to select one before mutation.

**Complete when:** the authorized operations, Review Proposal, supplied concerns, and any requested delivery ticket are unambiguous, or the skill has stopped without mutation at the unresolved choice.

## Draft actionable feedback

Ground each supplied concern in exact code, authority, test evidence, or observable behaviour. A preference without a concrete consequence remains discussion and is not Review Feedback.

Write the draft in English by default. Use another language only when the human asks. Make four facts clear without forcing a rigid template:

- the problem;
- its concrete impact;
- the required final state;
- the evidence that locates or proves it.

Preserve design freedom. State the required result, not incidental implementation steps. Keep separate problems in separate drafts so each item can be attributed and resolved independently. When a draft will become a general note rather than a resolvable code discussion, begin it with `Action required:` so its disposition is explicit.

Show every draft before publication unless the human's current instruction already supplies or approves its exact meaning and explicitly asks to post it.

**Complete when:** every draft represents one evidence-backed problem, names its impact and required final state, and is either approved for publication or returned to the human without provider mutation.

## Report the result

For Draft, report the text and evidence location. For Publish, report the permanent Review Proposal and feedback references and whether each item is unresolved or explicitly actionable. For Return for correction, report the canonical ticket reference and the verified open, unassigned `ready-for-agent` state.

Never claim that delivery recovery is ready from a comment alone. It requires both durable actionable feedback and a completed Return for correction operation.
