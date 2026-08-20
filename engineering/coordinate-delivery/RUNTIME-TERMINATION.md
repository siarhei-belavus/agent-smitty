# Runtime Termination

Read this file when an assigned claim or interrupted activation may need recovery.

Resolve liveness through execution-host evidence. A termination source is valid only when its provider record identifies the interrupted activation, reconstructed checkpoint, and observed termination outcome. Indeterminate liveness enters the [human-boundary branch](HUMAN-BOUNDARY.md) before claim release.

For proven termination, reconstruct and validate the checkpoint from durable Work Tracker and Code Host state, return the ticket to unassigned `ready-for-agent`, reacquire the Workflow Identity claim, and return to the [Resume Gate](RECOVERY.md) with runtime termination qualified as the sole source. Local-only work remains excluded until human reconciliation establishes provenance.

**Complete when:** provider/runtime evidence proves termination and binds to the checkpoint, or one human boundary owns the unresolved liveness; elapsed time and live memory decide nothing.
