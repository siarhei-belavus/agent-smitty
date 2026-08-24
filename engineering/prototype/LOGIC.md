# Logic prototype

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

### 4. Choose the interaction shell

Use a **terminal app** when the logic must run inside the host project's runtime, depends on its language or libraries, or will be driven live by a developer.

Use a **single self-contained HTML file** when the prototype must travel to another person, be reviewed asynchronously, or be driven by a non-developer.

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

Choose scenarios that expose the happy path, a hard edge case, and an action that should be illegal. Keep the page restrained so the state and controls carry the prototype. Do not add a framework, server, build step, or animation.

### 6. Hand it over

Expose a terminal prototype through the project's task runner. If the project has no task runner, put the run command at the top of the prototype's README. For HTML, give the file a clear name and direct-open path. Give the user the run command or HTML file. Add actions or scenarios as feedback sharpens the question.

## Anti-patterns

- **Don't generalise.** No "what if we wanted to support X later." The prototype answers one question.
- **Don't blur the logic and its shell together.** If the reducer / state machine references `document`, button handlers, `console.log`, prompts, or terminal escape codes, it's no longer portable. Keep either shell thin over a pure module.
- **Don't ship the interaction shell into production.** The shell is optimised for driving the prototype by hand. The logic module behind it is the bit worth keeping.
