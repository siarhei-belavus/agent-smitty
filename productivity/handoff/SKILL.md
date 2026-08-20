---
name: handoff
description: Compact the current task into a handoff document for another task or repository to pick up.
argument-hint: "What will the next task focus on?"
---

Write a handoff document summarising the current conversation so another task can continue the work. Save it to the temporary directory of the user's OS by default. If the user explicitly asks to save it to the backlog, save it in the current workspace's `.backlog` directory.

Include a "suggested skills" section naming which skills the next task should use.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next task will focus on and tailor the document accordingly.
