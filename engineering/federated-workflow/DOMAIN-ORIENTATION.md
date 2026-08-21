# Domain orientation

Every configured repository owns `docs/agents/domain.md` with this shape:

```markdown
# Domain Orientation

## Canonical domain sources

- Context Document: `<repo-relative path>`
- Context Map: `<repo-relative path>`

## Architecture decisions

- Repository ADRs: `<repo-relative directory>`
- Context ADRs: `<routing rule or repo-relative directories>`
```

Use `Context Document` for a single-context repository. Use `Context Map` when multiple contexts need routing; its entries select the Canonical Context Document for each context. Omit the unused field rather than adding an empty value.

Route terms and definitions to their Canonical Context Document. Route context topology, participants, External Systems, and relationships to the owning Context Map. Route context and repository architecture decisions to their configured ADR owner. When `## Domain Federation` is present, route federation-wide architecture decisions to its Home Repository.

Paths are repository-relative unless the configured federation contract requires a Repository-qualified Context Pointer. If a selected canonical owner or artifact is unavailable, report it and preserve the proposed change for routing; do not create a local substitute, duplicate canonical content, or infer another owner.
