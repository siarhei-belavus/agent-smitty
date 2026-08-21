# Domain federation configuration

A configured Home or Member adds one reciprocal binding to `docs/agents/domain.md`:

```markdown
## Domain Federation

- Role: `Home` or `Member`
- Home Repository ID: `<id>`
- Home Remote: `<remote>`
- Home Base Branch: `<branch>`
```

The Home binds to itself. A member binds to the same portable Home identity.

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

Each context has exactly one owner and an existing, substantive canonical `CONTEXT.md`. Participants do not co-own its language. A member that owns no context appears under every context in which it has a confirmed responsibility. External repositories appear only under their External System.

Repository-qualified pointers never mix with relative links. Identities contain Repository ID, remote, and Base Branch; configuration contains no local path, registry, or copied glossary. UI/deployment absence of a confirmed canonical context is preserved rather than filled with invented language.
