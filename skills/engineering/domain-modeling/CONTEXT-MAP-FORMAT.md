# CONTEXT-MAP.md format

## Structure

```md
# {Product or system name} Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — accepts and tracks customer orders.
- [Fulfillment](./src/fulfillment/CONTEXT.md) — prepares and dispatches accepted orders.

## External Systems

- **Payment processor** — authorizes and settles customer payments.

## Relationships

- **Ordering → Fulfillment**: hands off an accepted Order for fulfillment.
- **Ordering → Payment processor**: requests payment authorization for an Order.
```

## Rules

- Give every context one entry, one repository-relative link to its Canonical Context Document, and one sentence stating its responsibility.
- Keep term definitions in the linked Canonical Context Documents. The map contains context responsibilities and topology.
- List an External System only when a mapped context has a domain handoff with it.
- Name every relationship endpoint in `Contexts` or `External Systems` and describe the domain handoff rather than its transport or code-level implementation.
- Omit `External Systems` or `Relationships` when the section would be empty.
