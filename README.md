# Agent Smitty

Agent Smitty is the source repository for Serge's reusable coding-agent skills.
The skills are grouped by purpose under `skills/`, while each skill keeps a
globally unique `name` in its `SKILL.md` front matter.

## Install for Codex

Run the installer from the repository checkout:

```sh
./bin/install-codex-skills
```

It creates one symlink per skill under `~/.agents/skills` and links shared
resource directories required by skill references. Running the installer again
is safe. It refuses to overwrite an unrelated file or link with the same name.

Use an explicit target for another agent home or an isolated CI workspace:

```sh
./bin/install-codex-skills --target "$AGENT_HOME/.agents/skills"
```

## Use in CI

Clone a pinned commit rather than a moving branch, then install into the home
directory used by Codex:

```sh
git clone https://github.com/siarhei-belavus/agent-smitty.git
git -C agent-smitty checkout "$SKILLS_REF"
agent-smitty/bin/install-codex-skills --target "$HOME/.agents/skills"
```

The repository is private. CI needs read-only GitHub credentials scoped to this
repository.

## Verify changes

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```
