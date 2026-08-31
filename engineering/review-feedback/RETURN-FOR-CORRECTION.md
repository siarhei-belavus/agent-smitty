# Return for correction

Return for correction is the human-authorized end of one review round. It changes Work Tracker routing only after the Review Feedback already exists as durable Code Host state.

Read [lifecycle artifact contracts](../federated-workflow/LIFECYCLE-ARTIFACTS.md), then read the Ticket Origin Repository's instructions, Work Tracker binding, Routing Label binding, and affected repositories' Code Host bindings.

Resolve the delivery ticket through its matching Delivery Bundle handoff and affected Review Proposals. A supplied ticket reference narrows the lookup but does not replace the handoff relationship. Re-read the handoff, ticket, dependencies, routing, assignee, active lifecycle records, proposal heads, and complete affected feedback.

Resolve the Workflow Identity through the Work Tracker binding. Verify that the current provider identity has permission to replace the Routing Label before mutation.

Require all of the following before mutation:

- the current instruction explicitly completes the human review round and returns the delivery for correction;
- one matching completed Delivery Bundle handoff relates the ticket to every affected Review Proposal;
- every affected proposal remains at the exact head recorded by that handoff;
- at least one attributable feedback item is unresolved or explicitly actionable and has a permanent provider ID;
- the ticket is open, unassigned, and carries exactly `ready-for-human` among Routing Labels;
- its dependencies remain resolved and no unresolved lifecycle record or competing recovery source exists.

An existing assignee is a recovery condition, not permission to unassign that identity. Preserve the state and report the conflict. Do the same for a changed proposal head, contradictory handoff, ambiguous feedback attribution, active request, or dependency drift.

Through the Work Tracker binding, replace `ready-for-human` with exactly `ready-for-agent`. Change no other label or field. Re-read the ticket, dependencies, routing, and assignee after mutation. Re-read the affected feedback so the completed round is proven by current state rather than the mutation responses.

Do not write a Resumption Record. The resumed delivery workflow owns the Resume Gate and its lifecycle records. Do not claim the ticket, change a Review Proposal, resolve feedback, or invoke delivery work.

**Complete when:** the ticket is authoritatively verified as open, unassigned, dependency-ready, and exactly `ready-for-agent`, while every qualifying feedback item remains attributable and durable. A failed precondition stops before mutation. A failed post-mutation verification reports the uncertain state and performs no further mutation.
