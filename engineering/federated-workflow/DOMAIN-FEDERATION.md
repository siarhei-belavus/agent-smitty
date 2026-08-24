# Domain federation configuration

A Domain Federation is a group of repositories that share one canonical cross-repository Context Map and one portable Home identity.

**Home** is the repository role that owns that map and federation-wide ADRs. **Member** is a repository role that binds to the same Home identity.

The Home-owned cross-repository map is the **Federated Context Map**. A **Participant** has a confirmed responsibility in a context but does not own that context's language. A reciprocal federation binding records the same portable Home identity in Home and each Member.

A configured Home or Member adds one reciprocal binding to `docs/agents/domain.md`:

```markdown
## Domain Federation

- Role: `Home` or `Member`
- Home Repository ID: `<id>`
- Home Remote: `<remote>`
- Home Base Branch: `<branch>`
```

The Home owns the canonical `CONTEXT-MAP.md`:

```markdown
# <name> Federated Context Map

## Contexts

- [<Context>](<repository-id>:<path-to-CONTEXT.md>) — <responsibility>.
  - Owner: `<id>`; Remote: `<remote>`; Base Branch: `<branch>`.
  - Participant: `<id>`; Remote: `<remote>`; Base Branch: `<branch>`.
    Responsibility: <one line>.

## External Systems

- **<System>** — <relationship to the product boundary>.

## Relationships

- **<Context> → <Context or External System>**: <domain handoff>.
```

Each context has exactly one owner and an existing, substantive canonical `CONTEXT.md`. A member that owns no context appears under every context in which it has a confirmed responsibility. External repositories appear only under their External System.

Repository-qualified pointers never mix with relative links. Identities contain Repository ID, remote, and Base Branch; configuration contains no local path, registry, or copied glossary. UI/deployment absence of a confirmed canonical context is preserved rather than filled with invented language.
