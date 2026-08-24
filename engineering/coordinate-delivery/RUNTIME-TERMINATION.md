# Runtime Termination

Read [lifecycle artifact contracts](../federated-workflow/LIFECYCLE-ARTIFACTS.md) before reconstructing a checkpoint.

Read authoritative runtime state through the execution-host binding and resolve liveness through its provider evidence. A termination source is valid only when its provider record identifies the interrupted Coordinator Activation through its runtime-provided URL or equivalent reference, reconstructed checkpoint, and observed termination outcome. Use runtime-reference evidence only for observability and liveness diagnosis. Indeterminate liveness enters the [human-boundary branch](HUMAN-BOUNDARY.md) before claim release.

For proven termination, reconstruct and validate the checkpoint from durable Work Tracker and Code Host state, return the ticket to unassigned `ready-for-agent`, reacquire the Workflow Identity claim, and return to the [Resume Gate](RECOVERY.md) with runtime termination qualified as the sole source. Local-only work remains excluded until human reconciliation establishes provenance.

**Complete when:** provider/runtime evidence proves termination and binds to the checkpoint, or one human boundary owns the unresolved liveness; elapsed time and live memory decide nothing.
