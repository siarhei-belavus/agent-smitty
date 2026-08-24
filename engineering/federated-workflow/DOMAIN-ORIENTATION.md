# Domain orientation

Read [repository identity](REPOSITORY-IDENTITY.md) before resolving repository identities.

Domain Orientation is a repository-owned routing table to the canonical domain sources and ADR owners an agent must use.

A Canonical Context Document is the routed `CONTEXT.md` that owns one context's domain language. A Context Map is the canonical topology of contexts and their relationships; each context entry routes to its Canonical Context Document.

An External System is an independently owned system outside the mapped product boundary. A Context Relationship is a domain handoff from one mapped context to another context or an External System.

A Repository-qualified Context Pointer identifies a canonical document as `<Repository ID>:<repo-relative path>`. Resolve its Repository ID through the configured portable repository identity.

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

Use `Context Document` for a single-context repository. Use `Context Map` when multiple contexts need routing. Omit the unused field rather than adding an empty value.

When `docs/agents/domain.md` contains `## Domain Federation`, read [domain federation configuration](DOMAIN-FEDERATION.md) before applying that section.

Route terms and definitions to their Canonical Context Document. Route context topology, participants, External Systems, and relationships to the owning Context Map. Route context and repository architecture decisions to their configured ADR owner. When `## Domain Federation` is present, route federation-wide architecture decisions to Home.

Paths are repository-relative unless the configured federation contract requires a Repository-qualified Context Pointer. If a selected canonical owner or artifact is unavailable, report it and preserve the proposed change for routing; do not create a local substitute, duplicate canonical content, or infer another owner.
