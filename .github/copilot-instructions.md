# Copilot instructions — universal-ai-agents

This repo is a vendor-neutral monorepo of self-contained AI agents. The **canonical**
instructions live in `AGENTS.md` files: repo-wide conventions in the root
[`AGENTS.md`](../AGENTS.md), and each agent's operating manual in
`agents/<name>/AGENTS.md` (e.g. [`agents/job-application/AGENTS.md`](../agents/job-application/AGENTS.md)).
**Read the `AGENTS.md` for the agent you're working in and follow it.**

When working inside an agent folder, these non-negotiable rules always apply:

- **Config-driven, never hardcoded.** Personal data lives in gitignored
  `config/config.yaml`, `config/profiles/*.yaml`, and `output/` — never commit it. The
  tracked templates are `config.example.yaml` and `config/profiles/example.yaml`.
- **Human-in-the-loop.** Prepare and propose; the user approves anything
  outward-facing. Never bypass captchas or login walls, never auto-submit forms or
  applications, never auto-solve assessments, and never fabricate information.
- **Self-contained agents.** Don't let a change to one agent affect another.

See [CONTRIBUTING.md](../CONTRIBUTING.md) to add a new agent.
