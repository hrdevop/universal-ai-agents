# Claude Code Agents

> A growing collection of **configurable, autonomous AI agents** for [Claude Code](https://claude.com/claude-code) — practical, ready-to-run automations you drive from your terminal.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-blueviolet)](https://claude.com/claude-code)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Each agent lives in its own folder under [`agents/`](agents/) and is **fully
self-contained** — its own operating manual (`CLAUDE.md`), its own slash commands,
its own configuration. Nothing personal is hardcoded; every agent is driven by
config files you control, so the same agent works for anyone.

## Agents

| Agent | What it does | Status |
|-------|--------------|--------|
| [**Job Application Agent**](agents/job-application/) | Finds jobs in your browser, scores them against *your* priorities, tailors a truthful resume + cover letter per role, and tracks every application — never submitting without your explicit OK. | ✅ Available |
| _More on the way_ | Outreach, research, content, and more. [Suggest one →](../../issues) | 🛠️ Planned |

## Quick start

Each agent is run from inside its own directory.

```bash
git clone https://github.com/hrdevop/claude-code-agents.git
cd claude-code-agents/agents/job-application
claude          # launch Claude Code here, then run /setup
```

From there, follow that agent's README — e.g. the Job Application Agent walks you
through `/setup` → `/search` → `/apply` → `/report`.

## Repository layout

```text
claude-code-agents/
├── README.md            # you are here — the agent index
├── LICENSE              # MIT
├── CONTRIBUTING.md      # how to add a new agent
├── CLAUDE.md            # repo-wide conventions for Claude Code
└── agents/
    └── job-application/ # one self-contained agent
        ├── CLAUDE.md         # the agent's operating manual
        ├── README.md         # the agent's user guide
        ├── .claude/commands/ # /setup /use /search /apply /report
        ├── config/           # global defaults + per-user profiles
        ├── templates/        # resume & cover-letter templates
        └── output/           # generated results & tracker (gitignored)
```

## Design principles

- **Configurable, not hardcoded** — profiles and weights live in YAML; the same
  agent serves everyone.
- **Self-contained** — each agent is isolated, so adding one never breaks another.
- **Human-in-the-loop** — agents prepare and propose; you approve anything
  outward-facing. No captcha bypassing, no auto-submitting, no fabrication.
- **Privacy by default** — personal profiles and generated output are gitignored,
  never published.

## Adding a new agent

See [CONTRIBUTING.md](CONTRIBUTING.md) — copy the structure of an existing agent,
write its `CLAUDE.md` and commands, and add a row to the table above.

## License

[MIT](LICENSE) © 2026 Hansraj Rana
