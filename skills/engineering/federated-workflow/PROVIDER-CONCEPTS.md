# Provider concepts

Read [repository identity](REPOSITORY-IDENTITY.md) before applying these concepts.

A **Code Host** is the configured provider repository that owns Git revisions and review artifacts for one Repository ID.

A **Published Delivery Head** is the exact provider-retrievable commit at the tip of a published delivery branch. A **Review Proposal** is one provider review artifact from that branch to its configured Base Branch. **Review Feedback** is durable actionable provider feedback attached to that proposal. Review Proposals and provider-bound evidence name the Published Delivery Head.

A **Work Tracker** is the configured provider location that owns ticket lifecycle, dependencies, claims, routing, and durable coordination state. The **Ticket Origin Repository** is the human-confirmed repository whose Work Tracker owns a ticket.

A **Routing Label** is one configured Work Tracker label that marks an actionable ticket's current workflow state. The configured Routing Labels are mutually exclusive.

A **Workflow Identity** is the logical actor whose provider identity, permissions, and claim ownership are verified before mutation.

The **Delivery frontier** is the binding-defined ordered set of tickets currently eligible for claim.

Code Host and Work Tracker are independent authorities even when one provider supplies both.
