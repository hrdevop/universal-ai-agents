# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`claude-code-agents` is a **monorepo of self-contained AI agents** for Claude Code.
It is not a single application — each agent under [`agents/`](agents/) is an
independent unit with its own operating manual, slash commands, and configuration.

## How agents are organized

```text
agents/<agent-name>/
  CLAUDE.md            # that agent's operating manual (loaded when you cd in)
  README.md            # that agent's user guide
  .claude/commands/    # that agent's slash commands
  config/              # config.example.yaml (tracked) + local config.yaml (gitignored)
  ...                  # whatever else the agent needs
```

**To run or work on an agent, `cd` into its folder and launch Claude Code there.**
Each agent's own `CLAUDE.md` then governs behavior — this root file only describes
repo-wide conventions. Do not run an agent from the repo root; its relative paths
(`config/...`, `output/...`) and slash commands resolve from the agent directory.

## Conventions every agent follows

- **Config-driven, not hardcoded.** No personal data in tracked files. A committed
  `config.example.yaml` is the template; the real `config/config.yaml` and any
  `config/profiles/*.yaml` (except `example.yaml`) and `output/` are **gitignored**.
  See [`.gitignore`](.gitignore). Never commit a user's personal profile or
  generated output.
- **Human-in-the-loop.** Agents prepare and propose; the user approves anything
  outward-facing. Never bypass captchas/logins, never auto-submit, never fabricate.
- **Self-contained.** Adding or changing one agent must not affect another.

## Adding a new agent

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: copy an existing agent's folder
structure, write its `CLAUDE.md` + commands + `config.example.yaml`, keep personal
data gitignored, and add a row to the agents table in [README.md](README.md).
