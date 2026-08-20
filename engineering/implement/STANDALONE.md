# Standalone assignments

A Standalone assignment accepts one or more writable Repository Scope entries. The existing single-repository invocation is the one-entry case. When the user supplies only the current repository and no federated ticket contract, treat that repository as the single Repository Delivery and the supplied spec, ticket, or conversation as authority.

Resolve the Fixed Review Base from the unchanged current `HEAD` before editing when the assignment does not supply one. Use the supplied isolated worktree or another isolated writable checkout authorized by the assignment.

Use the complete Settled Seam set and test approaches recorded in the supplied authority. When none exists, identify every existing, changed, and new seam the outcome spans. Propose the smallest faithful repository-native test approach and nearest prior art for each. Use `codebase-design` when materially different caller-facing ownership, interface, seam, or contract choices remain, then ask the user to confirm the complete set once.

After the common implementation and exact-result validation in `SKILL.md`, use the `code-review` skill once with all fixed Repository Targets, both review axes, the authoritative sources, and the same Settled Seam and test-approach records. Fix Blocking findings only in affected Repository Deliveries, then commit, validate, and repeat the required review against the original fixed bases. A finding that changes scope, acceptance behavior, or a Settled Seam is a Material contradiction.

A changed head needs refreshed repository validation and fresh Standards review before the next whole-bundle Spec review. Finish when every latest committed head passes full repository validation and the latest selected review has no Blocking finding.

Standalone implementation changes no Code Host publication, Review Proposal, or Work Tracker state unless the user grants that authority separately.

**Complete when:** every current exact head has fresh repository validation and the selected review has no Blocking finding, with any separately authorized provider effects reported.
