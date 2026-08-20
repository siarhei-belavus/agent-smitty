# Coordinator-narrowed assignments

A Coordinator-narrowed assignment accepts exactly one named Repository Scope entry and one supplied Execution Worktree. The Coordinator must supply every delivery field required by `SKILL.md`.

Change only that Execution Worktree. Start no child agent or reviewer. Change no Code Host or Work Tracker state. The Coordinator owns all other scope entries, validation-only deliveries, publication, Review Proposals, Work Tracker state, and bundle review.

After the common implementation and exact-result validation in `SKILL.md`, return exactly one Repository Delivery result. Confirm that no child agent or reviewer was started and no Code Host publication or Work Tracker change was performed. Then stop.

**Complete when:** exactly one clean Repository Delivery result has been returned with current exact-head validation and the required ownership confirmations, or the exact blocker or Material contradiction has been returned.
