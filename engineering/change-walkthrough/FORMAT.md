# Walkthrough Format

Use this rendering contract for every user-visible walkthrough response. Structure is part of the semantic zoom: the human should recognise their location before reading the explanation.

## Visual vocabulary

Use these markers consistently:

- `✓` walked
- `→` current
- `○` pending
- `↷` skipped
- `!` detour
- `△` existing review attention
- `◇` follow-up candidate discovered through walkthrough discussion
- `□` unchanged entry or context
- `■` changed behaviour
- `★` observable result
- `→` before a node marks the current step

Keep headings short, paragraphs brief, and supporting links in a final `Related` line. Put navigation last. Show one primary code excerpt per step. Translate structural labels into the language used by the human; the English labels below define the structure, not mandatory user-visible wording.

## Opening view

```markdown
# Change Walkthrough

## What this change set is about

**Goal**

<One observable outcome. Use a short Goals list when the change set has independent goals.>

| Before | After |
| --- | --- |
| <Relevant observable behaviour or problem> | <Intended observable behaviour> |

- **Scope:** <Affected users, workflows, or domain area>
- **Source:** <Authoritative source, or **Inferred intent** with its strongest evidence>

## Atlas

- `✓` 1. <Walked scenario>
- `→` 2. <Current scenario>
- `○` 3. <Pending scenario>
- `↷` 4. <Skipped scenario>

**Detours:** <count> · **Attention flags:** <count>

**Recommended start:** <scenario and one-sentence reason>

**Navigate:** `start` · `choose a scenario` · `inspect a detour`
```

Omit status rows that do not yet exist. Preserve the shape when there are multiple goals by associating each atlas route with its goal.

## Scenario view

````markdown
## Scenario <n>/<total> — <Behavioural name>

**Outcome:** <What an external observer can see when this route completes>

### Route

> □ <unchanged entry or context>  
> ■ <changed behaviour>  
> → **■ <current changed behaviour>**  
> ★ <observable result>

**Legend:** `□` context · `■` changed · `→` current · `★` result

### Step <n> of <total> — <Plain-language current node>

<The node's role in the scenario in one short paragraph.>

**Flow:** `<incoming data/control>` → **<current responsibility>** → `<outgoing data/control>`

**Key code:** [path/to/file.ext](/absolute/path/to/file.ext:line)

```language
<smallest self-contained excerpt, normally 5–20 lines>
```

**Evidence:** [path/to/test.ext](/absolute/path/to/test.ext:line) — <observable behaviour it demonstrates>

**Related:** [supporting location](/absolute/path/to/file.ext:line) · [another location](/absolute/path/to/file.ext:line)

---

**Navigate:** `deeper` · `next` · `back to the map`
````

Show the full route as one compact Markdown blockquote, as in the template above. Do not use a fenced code block or decorative box-drawing frame for a linear route. Show the full route and legend only on the first step of a scenario. For later steps and deeper answers, replace them with this compact breadcrumb:

```markdown
**Where we are:** Step <n> of <total> — <plain-language step name>
```

Localize that sentence into the human's language. Omit `Related` when empty. When no direct test exists, render `**Evidence:** No direct test found.` When existing review findings apply, insert this before navigation:

```markdown
> **△ Attention:** <finding summary and link to its evidence>
```

When a question or discussion exposes a concrete actionable problem, insert this before navigation:

```markdown
> **◇ Follow-up candidate:** <problem and impact, grounded in exact evidence>
>
> **Suggested MR comment:** <concise comment stating the problem and desired final state>
>
> I can add this comment to <MR link> if you want.
```

Write the suggested comment in English by default, even when the surrounding walkthrough uses another language. Use another language only when the user explicitly requests it. Do not use this block for an ordinary explanation or design preference. Do not post the comment during the read-only walkthrough; wait for a separate explicit instruction.

## Deeper view

Retain the scenario heading and compact current-step breadcrumb. Add only the detail the human requested, under one precise heading such as:

```markdown
#### Caller
#### Validation rule
#### Before → After
#### Test setup
#### Failure path
```

End with the same navigation line. A deeper view adds resolution without opening unrelated regions.

## Detour view

````markdown
## ! Detour — <Short name>

**Location:** [path/to/file.ext](/absolute/path/to/file.ext:line)

**Why it is off-map:** <Why the hunk is not explained by a mapped scenario>

**Possible connection — inference:** <Plausible relation, or "None found">

```diff
<smallest hunk that exposes the detour>
```

---

**Navigate:** `inspect now` · `leave for the end` · `back to the map`
````

## Checkpoint and completion

```markdown
## Walkthrough checkpoint

- **Change set:** `<fixed-point> → <target>`
- **Position:** Scenario <n>, step <n> — <name>

| Route | Status |
| --- | --- |
| <scenario> | ✓ walked |
| <scenario> | → current |
| <scenario> | ○ pending |

**Outstanding detours**

- [<detour>](/absolute/path/to/file.ext:line)

**Follow-up candidates**

- `<candidate>` — `posted | declined | outstanding`

**Resume with:** `<next step or route>`
```

Omit the follow-up section when no candidate was raised. For a completed walkthrough, title the section `Walkthrough complete`, show every route's final status, and list skipped regions, remaining detours, and follow-up candidate statuses explicitly.
