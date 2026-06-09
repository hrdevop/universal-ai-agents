# AGENTS.md

Repo-wide guidance for **any** AI coding assistant working in this repository.
`AGENTS.md` is the cross-tool standard read natively by Cursor, Codex, Gemini CLI,
Copilot, Windsurf, Aider, Zed, Cline, Jules, and 20+ others. Tool-specific files
(`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules/`) all
point back to the `AGENTS.md` files — **these are the single source of truth.**

## What this repository is

`universal-ai-agents` is a **vendor-neutral monorepo of self-contained AI agents**.
It is not a single application — each agent under [`agents/`](agents/) is an
independent unit with its own `AGENTS.md` operating manual, its own routines, and its
own configuration. The same agent runs under whichever assistant you prefer.

## How agents are organized

```text
agents/<agent-name>/
  AGENTS.md            # that agent's operating manual (the brain)
  CLAUDE.md            # thin: @AGENTS.md (Claude Code)
  GEMINI.md            # thin: @AGENTS.md (Gemini CLI)
  README.md            # that agent's user guide
  .claude/commands/    # Claude Code slash commands (other tools run the same routines by name)
  config/              # config.example.yaml (tracked) + local config.yaml (gitignored)
  ...                  # whatever else the agent needs
```

**To run or work on an agent, open its folder (`agents/<name>/`) in your assistant.**
That agent's `AGENTS.md` then governs behavior — this root file only describes
repo-wide conventions. Agents use relative paths (`config/...`, `output/...`), so work
from inside the agent directory.

## Conventions every agent follows

- **Vendor-neutral first.** The canonical manual is `AGENTS.md`. Tool adapters
  (`CLAUDE.md`, `GEMINI.md`, etc.) only import or point to it — never duplicate it.
- **Config-driven, not hardcoded.** No personal data in tracked files. A committed
  `config.example.yaml` is the template; the real `config/config.yaml`, any
  `config/profiles/*.yaml` (except `example.yaml`), and `output/` are **gitignored**
  (see [`.gitignore`](.gitignore)). Never commit a user's profile or generated output.
- **Human-in-the-loop.** Agents prepare and propose; the user approves anything
  outward-facing. Never bypass captchas/logins, never auto-submit, never fabricate.
- **Self-contained.** Adding or changing one agent must not affect another.

## Adding a new agent

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: copy an existing agent's folder,
write its `AGENTS.md` (canonical) plus thin `CLAUDE.md`/`GEMINI.md` adapters, its
routines, and a `config.example.yaml`; keep personal data gitignored; and add a row to
the agents table in [README.md](README.md).
