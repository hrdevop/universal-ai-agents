# Universal AI Agents

> A growing collection of **configurable, vendor-neutral AI agents** that work with
> **any** AI coding assistant — Claude, Gemini, Cursor, Copilot, and more — through the
> open [`AGENTS.md`](https://agents.md) standard.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AGENTS.md](https://img.shields.io/badge/standard-AGENTS.md-0a7cff)](https://agents.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Each agent lives in its own folder under [`agents/`](agents/) and is **fully
self-contained** — its own operating manual (`AGENTS.md`), its own routines, its own
configuration. Nothing personal is hardcoded; every agent is driven by config files you
control, so the same agent works for anyone, on any assistant.

## Works with any assistant

The canonical instructions for every agent live in an `AGENTS.md` file — the cross-tool
standard read **natively** by 20+ tools. A couple of assistants use their own filename,
so each agent ships thin adapters that just point back to `AGENTS.md` (zero duplication).

| Assistant | How it reads the agent |
|-----------|------------------------|
| **Cursor, OpenAI Codex, Windsurf, Aider, Zed, Cline, Jules, Devin, Warp, JetBrains Junie, …** | `AGENTS.md` natively |
| **Claude Code** | `CLAUDE.md` → `@AGENTS.md` (plus `/setup /search …` slash commands) |
| **Gemini CLI** | `GEMINI.md` → `@AGENTS.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` → `AGENTS.md` |

Don't see your tool? If it reads `AGENTS.md`, it already works.

## Agents

| Agent | What it does | Status |
|-------|--------------|--------|
| [**Job Application Agent**](agents/job-application/) | Finds jobs (via your assistant's browser/web tools or pasted listings), scores them against *your* priorities, tailors a truthful resume + cover letter per role, and tracks every application — never submitting without your explicit OK. | ✅ Available |
| _More on the way_ | Outreach, research, content, and more. [Suggest one →](../../issues) | 🛠️ Planned |

## Quick start

Each agent is run from inside its own directory — open it in whichever assistant you use.

```bash
git clone https://github.com/hrdevop/universal-ai-agents.git
cd universal-ai-agents/agents/job-application
# then open this folder in your assistant:
#   Claude Code  →  run  claude   (then /setup)
#   Gemini CLI   →  run  gemini
#   Cursor       →  open the folder; it reads AGENTS.md
#   ...           →  any AGENTS.md-aware tool
```

Then follow that agent's README — e.g. the Job Application Agent walks you through
Setup → Search → Apply → Report. In Claude Code those are `/setup`, `/search`,
`/apply`, `/report`; in any other assistant, just ask for them by name.

## Repository layout

```text
universal-ai-agents/
├── README.md                     # you are here — the agent index
├── AGENTS.md                     # repo-wide conventions (canonical)
├── CLAUDE.md / GEMINI.md         # thin adapters → @AGENTS.md
├── .github/copilot-instructions.md
├── .cursor/rules/agents.mdc
├── LICENSE · CONTRIBUTING.md
└── agents/
    └── job-application/           # one self-contained agent
        ├── AGENTS.md              # the agent's operating manual (canonical)
        ├── CLAUDE.md / GEMINI.md  # thin adapters → @AGENTS.md
        ├── README.md
        ├── .claude/commands/      # Claude slash commands (others run the routines by name)
        ├── config/                # config.example.yaml + per-user profiles
        ├── templates/             # resume & cover-letter templates
        └── output/                # generated results & tracker (gitignored)
```

## Design principles

- **Vendor-neutral** — `AGENTS.md` is the single source of truth; tool files only
  point to it.
- **Configurable, not hardcoded** — profiles and weights live in YAML; the same agent
  serves everyone.
- **Self-contained** — each agent is isolated, so adding one never breaks another.
- **Human-in-the-loop** — agents prepare and propose; you approve anything
  outward-facing. No captcha bypassing, no auto-submitting, no fabrication.
- **Privacy by default** — personal profiles and generated output are gitignored,
  never published.

## Adding a new agent

See [CONTRIBUTING.md](CONTRIBUTING.md) — copy an existing agent, write its `AGENTS.md`
(+ thin `CLAUDE.md`/`GEMINI.md` adapters) and routines, and add a row to the table above.

## License

[MIT](LICENSE) © 2026 Hansraj Rana
