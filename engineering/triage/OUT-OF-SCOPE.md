# Out-of-scope records

## Match a record

During triage, read every file in `.out-of-scope/`. Match requests by concept, not keyword. For example, "night theme" matches `dark-mode.md`. Surface the matching record and its prior reasoning, then ask the maintainer whether the recorded decision still holds.

- If the request concerns the same concept and the decision holds, append it under `Prior requests` and return to triage's Rejected (enhancement) outcome.
- If the request concerns the same concept and the decision is reconsidered, update or delete the record and continue normal triage.
- If the request is related but distinct, leave the record unchanged and continue normal triage.

## Directory structure

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

One file per **concept**, not per issue. Multiple issues requesting the same thing are grouped under one file.

## File format

The file should be written in a relaxed, readable style — more like a short design document than a database entry. Use paragraphs, code samples, and examples to make the reasoning clear and useful to someone encountering it for the first time.

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42 — "Add dark mode support"
- #87 — "Night theme for accessibility"
- #134 — "Dark theme option"
```

### Naming the file

Use a short, descriptive kebab-case name for the concept: `dark-mode.md`, `plugin-system.md`, `graphql-api.md`. The name should be recognizable enough that someone browsing the directory understands what was rejected without opening the file.

### Writing the reason

The reason should be substantive — not "we don't want this" but why. Good reasons reference:

- Project scope or philosophy ("This project focuses on X; theming is a downstream concern")
- Technical constraints ("Supporting this would require Y, which conflicts with our Z architecture")
- Strategic decisions ("We chose to use A instead of B because...")

The reason should be durable. Avoid referencing temporary circumstances ("we're too busy right now") — those aren't real rejections, they're deferrals.

## Record a rejection

When triage selects rejected-enhancement recording, append the request under `Prior requests` in the matching concept file or create the file from the schema above.

## Updating or removing out-of-scope files

When the recorded decision changes, update or delete its concept file. Do not reopen old issues; they are historical records. The request that triggered reconsideration proceeds through normal triage.
