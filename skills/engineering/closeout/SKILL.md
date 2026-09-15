---
name: closeout
description: Close a completed delivery, record acceptance, and remove its worktrees and branches.
disable-model-invocation: true
---

# Closeout

Finish the current delivery after acceptance. Invoking this skill authorizes the task's completion comment, tracker transition, and removal of its disposable worktrees and local and remote branches. Honor any narrower scope in the user's request.

Use the conversation and existing delivery records to resolve the task. Reuse the user's acceptance and earlier permissions. Ask only for missing information that prevents a specific action. Continue independent work while that action remains blocked.

## 1. Establish scope and completion

Read the applicable project instructions and Work Tracker, Code Host, and routing-label bindings. Use their configured providers and authentication. Read operational runbooks when checking build or deployment systems.

Identify the delivery ticket, repositories, final MR or PR revisions, deployment evidence where required, and acceptance. Include follow-up fixes and throwaway prototypes from this task. Interpret "all worktrees and branches" within this task's scope unless the user explicitly names a broader scope.

Check the current ticket and merge states. Match the accepted delivery to its final revision and, when deployment is part of completion, the successful build and deployed artifact. Reuse recorded checks that still apply to that revision. Distinguish user acceptance from checks performed by the agent. Invocation authorizes closure but does not establish that a missing build, deployment, or acceptance check passed.

If delivery remains incomplete, preserve the resources needed to finish it and report the concrete missing condition. Close only tickets whose own completion criteria are satisfied. Leave parent specifications and unrelated tickets under their existing lifecycle.

Done when every scoped delivery has a supported completion decision and every repository is identified.

## 2. Inventory cleanup candidates

For each repository, inspect worktrees, local branches, exact remote branch heads, and task-owned running processes. Record each candidate's path, branch, head SHA, and ownership evidence from the task or delivery record. A name prefix alone is insufficient ownership evidence.

Inspect each candidate worktree's tracked and untracked changes. Account for ignored files that removal would also delete. Known generated dependencies are disposable; retain unknown files and human edits. Preserve the user's main checkout, its current branch, and unrelated worktrees.

For delivered branches, confirm the provider reports the corresponding MR or PR merged and the candidate head matches the delivered source revision. Squash and rebase merges can make Git ancestry checks insufficient. A throwaway prototype may be unmerged if its ownership and disposable purpose are established. Preserve branches with later commits until those commits are accounted for.

Done when every candidate is either safe to remove or retained with a concrete reason.

## 3. Record and close

Before deleting local evidence, publish a concise completion record through the configured tracker. Include the final result, MR or PR links, revision, applicable build and deployment links, artifact identifier, and acceptance evidence. If no tracker applies, preserve the record outside worktrees scheduled for deletion. Reuse an equivalent existing record on repeated invocation.

Use the tracker's available completion transitions and required fields. Choose the normal completion path and resolution. For Jira, inspect transitions and required fields at the current status rather than hardcoding IDs. A validator may require a comment even when transition metadata omits it. Read validation errors and correct the specific payload. After an uncertain write response, re-read state before retrying.

Preserve historical coordination comments. A new acceptance record can resolve an earlier request for human verification. Remove obsolete routing labels and release this task's agent claim only as the project binding requires. Preserve unrelated labels and human ownership.

Done when the completion record is readable and a fresh tracker read confirms the intended status and resolution, or the exact blocker is recorded. If closure fails, retain any resources needed to retry it.

## 4. Remove task resources

Stop only processes whose ownership was established, such as this task's development server or port forward. Run removal commands from a retained directory.

Recheck candidate heads and worktree status immediately before deletion. Remove clean disposable worktrees with `git worktree remove` using exact paths. If removal refuses, inspect the reason and preserve unexplained contents instead of forcing deletion.

Delete the verified task branches after their worktrees are removed. Use ordinary local branch deletion where possible. Forced local branch deletion is appropriate for a verified squash merge or an established throwaway prototype under the invocation's cleanup authorization.

Delete a remote branch only if its current head still matches the approved candidate. Use an exact expected-SHA lease or an equivalent conditional provider operation to protect concurrent updates. Treat an already absent branch as complete. Remove only corresponding stale remote-tracking refs.

Done when every safe candidate has been removed or has a recorded removal failure, and all retained resources remain intact.

## 5. Verify and report

Verify removed worktree paths and registrations are absent, deleted local and remote branch refs are absent, and the ticket remains complete. On repeated invocation, perform only missing work without duplicating comments or transitions.

Report the ticket link and final status, counts of removed worktrees and branches, and any retained resources with reasons. If an action was blocked, distinguish completed closure from incomplete cleanup. Archive the conversation only when the user requests it.

Done when every scoped resource has a verified outcome and the user has the concise closeout result.
