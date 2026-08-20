# Durable Lifecycle Artifact Contracts

Publish these records through the configured Work Tracker log using permanent provider IDs, stable record IDs, canonical ticket references, and exact revisions. Provider formatting may vary while preserving meaning.

## Execution Checkpoint

Record:

- stable checkpoint, ticket, Coordinator Activation and Execution Attempt IDs, trigger, and provider timestamp;
- ticket state, routing, assignee, dependencies, and authority pointers;
- each Repository Delivery's base, branch, exact Published Delivery Head, Review Proposal, preserved worktree state, and outcome;
- exact-head repository validation, Standards, cross-repository, and Bundle Spec evidence IDs and influencing sets;
- affected and preserved Repository Deliveries plus invalidated, preserved, and pending evidence;
- active Human Action Request ID or explicit absence;
- next permissible step and prerequisites;
- local-only exclusions, runtime evidence pointers, and limitations.

Retain append-only history and identify the current checkpoint.

## Human Action Request

Record:

- stable request ID, status (`active`, `completed`, or `superseded`), reason, checkpoint, ticket, and accountable owner;
- required action, response location, completion criteria, and next routing transition;
- for planned verification, prerequisites, reproducible steps, pass/fail criteria, expected evidence, and accountable owner;
- for escalation, trigger, evidence, affected decisions and deliveries, pointers, and required reconciliation;
- predecessor and successor IDs when Validation Indeterminacy supersedes planned verification.

Complete or supersede the active request before its successor becomes active. A durable re-read must yield exactly one active request or a completed chain.

## Human Response

The accountable human supplies one free-form durable response through the request's Work Tracker surface. Its prose has no provider-specific schema. Identify its permanent provider ID and request relationship.

Reconcile it against the requested action and completion criteria. Record whether it completes, supersedes, or leaves the request indeterminate and identify accepted authority and evidence. Resumption also requires the open ticket to return to unassigned `ready-for-agent`.

## Resumption Plan

For `replan`, record a human-produced or explicitly delegated execution-ready plan with its stable ID, authority, source response, accepted intent, affected and preserved deliveries, treatment of checkpoint worktrees/heads/proposals/evidence, next executable work, settled boundaries, and completion criteria. Missing material choices stay at the human boundary.

## Resumption Record

Publish after a successful Resume Gate and before the next attempt. Record:

- stable record, ticket, new activation, and next attempt IDs;
- exactly one response, feedback, or runtime-termination source;
- `continue` or `replan`, checkpoint, and plan when applicable;
- affected and preserved Repository Deliveries;
- previous and launch exact Published Delivery Heads and reused proposals;
- invalidated evidence, preserved identical-head evidence, and required refresh;
- re-read claim/routing, next permissible step, and limitations.

Re-read the permanent record and verify launch heads against provider truth before starting the attempt.
