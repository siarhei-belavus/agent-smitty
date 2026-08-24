---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
disable-model-invocation: true
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability. Load `codebase-design`, the domain glossary, and applicable ADRs before scanning.

## Process

### 1. Explore

**Scope before you scan — YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction — a module, a subsystem, a pain point — take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots — the files and areas that keep coming up — and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`CONTEXT.md`) and any ADRs in the area you're touching first.

Then delegate a bounded codebase exploration to a subagent. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to each candidate.

### 2. Present candidates as an HTML report

Render and open the candidate report through [HTML-REPORT.md](HTML-REPORT.md).

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, use `grill-with-docs` as an output-only planning session to walk its constraints, dependencies, module shape, seam, and surviving tests. Keep its returned deltas with the selected idea for the specification flow:

- **Naming a proposed deepened module after a concept not in `CONTEXT.md`?** Return the complete proposed glossary delta without presenting the future module as current truth.
- **Sharpening a fuzzy term during the conversation?** Preserve the complete clarified-language delta for the subsequent planning flow.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only that explicit approval grants `domain-modeling` canonical capture limited to the routed ADR. Skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Use the `codebase-design` skill and its design-it-twice parallel sub-agent pattern.
