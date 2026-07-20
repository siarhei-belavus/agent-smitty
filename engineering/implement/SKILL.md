---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Before making changes, record the current HEAD as the review base.

Use the complete settled seam set and test approaches recorded in the supplied specification, tickets, or resolved design decisions. Do not ask the user to reconfirm them.

When invoked standalone without a settled seam set, identify the complete set of existing, changed, and new seams the solution spans. For each seam, propose the smallest faithful repository-native test approach and its nearest prior art. If materially different caller-facing ownership, interface, seam, or contract choices remain possible, run `/codebase-design` before proposing the set. Ask the user to confirm the complete set and proposed approaches once; the confirmed seams are settled.

Invoke `/tdd` with the authoritative sources and the complete settled seam records, including each seam's owning module, caller/test-visible interface, location, status, observable behavior, selected test approach, and nearest prior art. Run typechecking and focused tests regularly. After each coherent green iteration, commit the work to the current branch.

Run the full test suite once the implementation is complete.

Invoke `/code-review` against the original review base with the authoritative sources and the same settled seam and test-approach records.

Fix Blocking findings, validate the changes, commit them, and repeat the full review when the reviewed implementation changes. Escalate any finding whose resolution would change scope, acceptance behavior, or a settled seam.

Finish only when the latest committed state passes full repository validation and has no Blocking review findings.
