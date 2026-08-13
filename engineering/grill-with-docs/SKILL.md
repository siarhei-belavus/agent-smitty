---
name: grill-with-docs
description: A one-session interview that sharpens a plan or design through grilling and domain modeling, ready for specification synthesis.
disable-model-invocation: true
---

Run a `/grilling` session using the `/domain-modeling` skill. This is planning, so do not grant canonical capture. Keep every returned Domain Model Delta at full fidelity in the current conversation and carry the complete set forward to `/to-spec`.

When another workflow invokes this skill, return the complete deltas to that workflow. The outer workflow owns any durable capture; this skill neither selects nor infers a persistence destination.
