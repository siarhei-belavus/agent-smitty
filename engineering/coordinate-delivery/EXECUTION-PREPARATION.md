# Execution preparation

A provenance-verified existing Execution Worktree remains assigned to its Repository Delivery regardless of its location. Apply root resolution only when creating a new worktree.

For each new Execution Worktree, use an absolute destination explicitly supplied by the execution host. Otherwise resolve one persistent root in this order:

1. Use absolute `AGENT_WORKTREES_ROOT` when non-empty. A relative value is an [Environment Preparation Blocker](HUMAN-BOUNDARY.md).
2. When `AGENT_WORKTREES_ROOT` is unset or empty, use `$XDG_STATE_HOME/agent-worktrees` if `XDG_STATE_HOME` is non-empty and absolute. A non-empty relative `XDG_STATE_HOME` is an Environment Preparation Blocker.
3. When both variables are unset or empty, use `$HOME/.local/state/agent-worktrees`. A missing, empty, or non-absolute `HOME` is an Environment Preparation Blocker.

Create new destinations as `<root>/<ticket-origin-key>/<ticket-key>/<repository-key>`. Derive each key from its portable identity or canonical reference as `<slug>-<digest>`: lowercase the source, replace each run outside `a-z0-9` with `-`, trim leading and trailing `-`, cap the slug at 48 characters, use `item` when empty, and append the first 12 hexadecimal characters of the source's SHA-256 digest. Reuse this path across Execution Attempts; an Execution Attempt ID never enters it.

Before mutation, inspect the complete scope together:

- validate Repository Stores, remotes, Base Branches, remote access, destination availability, known branch conflicts, worktree provenance, and immediate bootstrap requirements;
- preserve a destination containing unrelated content, an accidental branch collision, or unknown dirty or untracked state and enter the human boundary instead of choosing a random replacement;
- allow concurrent preparation to rely on Git locking, retry lock contention within the bounded recovery rule below, and leave every foreign lock, worktree registration, and checkout intact.

Fetch and worktree registration may update a Repository Store's shared Git metadata, but preparation preserves its checked-out branch, index, tracked and untracked content, remotes, hooks, Git identity, and local or global Git configuration. It never switches, resets, cleans, prunes, repairs, or uses the Store as a delivery workspace.

For a new Repository Delivery, fetch without switching the Store, resolve and record the exact Base Branch launch commit, create its unique delivery branch, and create one persistent Execution Worktree at the host-provided destination. Reuse an existing worktree only when it belongs to the intended Repository Reference and delivery branch and its provenance follows from the current context, Execution Checkpoint, handoff, completed Human Response, or Resumption Record. Preserve unknown state for human reconciliation.

Bootstrap from the Execution Worktree through applicable `AGENTS.md`, then referenced repository scripts and documents, then checked-in README, devcontainer, or CI guidance. Materialize an ignored or untracked input only when repository instructions require it and define the safe method. Use host facilities for secrets. Durable artifacts contain no secret value. External package caches may be shared; repository-local mutable outputs remain in their worktree.

Diagnose a preparation failure and apply documented remediation before retrying. An unchanged command receives at most two additional attempts. A documented remediation that materially changes the environment starts one new bounded attempt series. When recovery still requires a human, preserve every safe prepared delivery and enter the human boundary with an Execution Checkpoint and one Environment Preparation Blocker request. Cleanup, disk-pressure reclamation, destructive repair, worktree pruning, and lock deletion remain execution-host or human responsibilities outside this workflow.
