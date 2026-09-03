---
name: wait-what
description: "Stop. That last message did not land: re-pitch it."
disable-model-invocation: true
---

Re-pitch the last answer. Supply the context the user was missing and use ASD-STE100 Simplified Technical English.

Use the applicable canonical domain vocabulary. If `docs/agents/domain.md` exists, perform its Domain Orientation. Otherwise, follow `CONTEXT-MAP.md` to the relevant `CONTEXT.md`, or use the root `CONTEXT.md` in a single-context repository. If no applicable glossary exists, proceed without one. Treat domain documentation as read-only for this re-pitch.
