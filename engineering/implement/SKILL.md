---
name: implement
description: "Implement one or more Repository Deliveries from a spec or tickets, or one Coordinator-narrowed Repository Delivery in its supplied Execution Worktree."
disable-model-invocation: true
---

Implement the work described by the user in the authoritative spec or tickets.

Read the [Repository delivery implementation contract](../../../../docs/agents/repository-delivery-implementation.md) completely before changing a checkout. It owns the Standalone and Coordinator-narrowed assignment modes, preparation, TDD, validation, exact result, mutation limits, and contradiction handling.

Apply its Standalone mode unless the user supplies one explicitly Coordinator-narrowed Repository Delivery. Apply its Coordinator-narrowed mode only to that supplied delivery.

**Complete when:** every authorized Repository Delivery satisfies the selected mode's completion requirements and the requested result has been returned.
