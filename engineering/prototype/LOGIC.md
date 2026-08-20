# Logic Prototype

A tiny interactive demo that lets the user drive a state model by hand. Use this when the question is about **business logic, state transitions, or data shape** — the kind of thing that looks reasonable on paper but only feels wrong once you push it through real cases.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where the user wants to **press buttons and watch state change**.

If the question is "what should this look like" — wrong branch. Use [UI.md](UI.md).

## Process

### 1. State the question

Before writing code, write down what state model and what question you're prototyping. One paragraph, in the prototype's README or a comment at the top of the file. A logic prototype that answers the wrong question is pure waste — make the question explicit so it can be checked later, whether the user is watching now or returning to it AFK.

### 2. Pick the language

Use whatever the host project uses. If the project has no obvious runtime (e.g. a docs repo), ask.

Match the project's existing conventions for tooling — don't add a new package manager or runtime just for the prototype.

### 3. Isolate the logic in a portable module

Put the actual logic — the bit that's answering the question — behind a small, pure interface that could be lifted out and dropped into the real codebase later. The interaction shell around it is throwaway; the logic module shouldn't be.

The right shape depends on the question:

- **A pure reducer** — `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine** — explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state — just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick whichever shape best fits the question being asked, *not* whichever is easiest to wire to the interaction shell. Keep it pure: no I/O, DOM access, terminal code, or `console.log` for control flow. The shell calls into it; nothing flows the other direction.

This is what makes the prototype useful past its own lifetime: when the question's been answered, the validated reducer / machine / function set can be lifted into the real module on its own.

### 4. Choose the interaction shell

Use a **terminal app** when the logic must run inside the host project's runtime, depends on its language or libraries, or will be driven live by a developer.

Use a **single self-contained HTML file** when the prototype must travel to another person, be reviewed asynchronously, or be driven by a non-developer. The file must open directly in a browser with no server, framework, bundler, or install step.

If both shapes would work, prefer HTML for portability. The state model remains a pure module either way.

### 5A. Build the smallest TUI that exposes the state

Build it as a **lightweight TUI** — on every tick, clear the screen (`console.clear()` / `print("\033[2J\033[H")` / equivalent) and re-render the whole frame. The user should always see one stable view, not an ever-growing scrollback.

Each frame has two parts, in this order:

1. **Current state**, pretty-printed and diff-friendly (one field per line, or formatted JSON). Use **bold** for field names or section headers and **dim** for less important context (timestamps, IDs, derived values). Native ANSI escape codes are fine — `\x1b[1m` bold, `\x1b[2m` dim, `\x1b[0m` reset. No need to pull in a styling library unless one is already in the project.
2. **Keyboard shortcuts**, listed at the bottom: `[a] add user  [d] delete user  [t] tick clock  [q] quit`. Bold the key, dim the description, or vice-versa — whatever reads cleanly.

Behaviour:

1. **Initialise state** — a single in-memory object/struct. Render the first frame on start.
2. **Read one keystroke (or one line)** at a time, dispatch to a handler that mutates state.
3. **Re-render** the full frame after every action — don't append, replace.
4. **Loop until quit.**

The whole frame should fit on one screen.

### 5B. Build a shareable HTML demo

Keep the state model and actions in plain JavaScript inside one HTML file. The page has four parts:

1. **Current state** rendered in full after every action.
2. **Last transition** showing the action and the observable change it produced.
3. **Free-play controls**, one button per action, always available.
4. **Guided scenarios**, one tab per awkward case. Starting a scenario resets to a known initial state, then presents its real action buttons in order so the same case can be replayed.

Choose scenarios that expose the happy path, a hard edge case, and an action that should be illegal. Keep the page restrained so the state and controls carry the prototype. Do not add a framework, server, build step, persistence, or animation.

### 6. Make it trivial to run

For a TUI, add a script to the project's existing task runner (`package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`). The user should run `pnpm run <prototype-name>` or equivalent — never need to remember a path.

If the host project has no task runner, put the command at the top of the prototype's README. For HTML, the artifact itself is the entry point: give it a clear filename and open it directly.

### 7. Hand it over

Give the user the run command or HTML file. They'll drive it themselves; the interesting moments are when they say "wait, that shouldn't be possible" or "huh, I assumed X would be different" — those are the bugs in the _idea_, which is the whole point. If they want new actions or scenarios added, add them. Prototypes evolve.

### 8. Capture the answer and the prototype

Once the prototype has answered its question, capture the answer, then capture the prototype the way the [SKILL](SKILL.md) describes. The logic-specific mapping: the validated reducer / machine / function set lifts into the real module (the decision, absorbed); the interaction shell rides along to the throwaway branch that keeps the prototype as a primary source.

## Anti-patterns

- **Don't add tests.** A prototype that needs tests is no longer a prototype.
- **Don't wire it to the real database.** Use an in-memory store unless the question is specifically about persistence.
- **Don't generalise.** No "what if we wanted to support X later." The prototype answers one question.
- **Don't blur the logic and its shell together.** If the reducer / state machine references `document`, button handlers, `console.log`, prompts, or terminal escape codes, it's no longer portable. Keep either shell thin over a pure module.
- **Don't add infrastructure for HTML.** One file the recipient opens directly; a framework, bundler, or server defeats the shareable shape.
- **Don't ship the interaction shell into production.** The shell is optimised for driving the prototype by hand. The logic module behind it is the bit worth keeping.
