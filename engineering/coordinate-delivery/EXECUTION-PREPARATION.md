# Execution preparation

The execution host supplies each exact worktree destination or one persistent worktree root plus a deterministic path mapping. The workflow defines no execution-root setting. When the host supplies a root, use `<root>/<ticket-origin-key>/<ticket-key>/<repository-key>`, with host-derived filesystem-safe keys for the Ticket Origin Repository ID, canonical ticket reference, and Repository ID. Reuse that mapping across Execution Attempts; an Execution Attempt ID never enters the path.

An authorized preserved worktree may remain in a legacy location. Reuse it after identity and provenance validation rather than moving or duplicating it. When neither exact destinations nor a root and mapping are available, bounded host inspection ends in an [Environment Preparation Blocker](HUMAN-BOUNDARY.md) before local mutation.

Before mutation, inspect the complete scope together:

- validate Repository Stores, remotes, Base Branches, remote access, destination availability, known branch conflicts, worktree provenance, and immediate bootstrap requirements;
- preserve a destination containing unrelated content, an accidental branch collision, or unknown dirty or untracked state and enter the human boundary instead of choosing a random replacement;
- allow concurrent preparation to rely on Git locking, retry lock contention within the bounded recovery rule below, and leave every foreign lock, worktree registration, and checkout intact.

Fetch and worktree registration may update a Repository Store's shared Git metadata, but preparation preserves its checked-out branch, index, tracked and untracked content, remotes, hooks, Git identity, and local or global Git configuration. It never switches, resets, cleans, prunes, repairs, or uses the Store as a delivery workspace.

For a new Repository Delivery, fetch without switching the Store, resolve and record the exact Base Branch launch commit, create its unique delivery branch, and create one persistent Execution Worktree at the host-provided destination. Reuse an existing worktree only when it belongs to the intended Repository Reference and delivery branch and its provenance follows from the current context, Execution Checkpoint, handoff, completed Human Response, or Resumption Record. Preserve unknown state for human reconciliation.

Bootstrap from the Execution Worktree through applicable `AGENTS.md`, then referenced repository scripts and documents, then checked-in README, devcontainer, or CI guidance. Materialize an ignored or untracked input only when repository instructions require it and define the safe method. Use host facilities for secrets. Durable artifacts contain no secret value. External package caches may be shared; repository-local mutable outputs remain in their worktree.

Diagnose a preparation failure and apply documented remediation before retrying. An unchanged command receives at most two additional attempts. A documented remediation that materially changes the environment starts one new bounded attempt series. When recovery still requires a human, preserve every safe prepared delivery and enter the human boundary with an Execution Checkpoint and one Environment Preparation Blocker request. Cleanup, disk-pressure reclamation, destructive repair, worktree pruning, and lock deletion remain execution-host or human responsibilities outside this workflow.
