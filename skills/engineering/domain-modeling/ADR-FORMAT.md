# ADR Format

ADRs use sequential numbering in their configured ADR directory: `0001-slug.md`, `0002-slug.md`, etc.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

Use one paragraph unless an optional section adds information the paragraph cannot carry clearly.

Use established domain terms in the title and body so the decision can be found by the concepts it governs. Name the subject and decision, not only the implementation mechanism.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

## Numbering

Scan the configured ADR directory for the highest existing number and increment by one.
