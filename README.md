<div align="center">

# Universal AI Agents

**Configurable, vendor-neutral AI agents that work with _any_ AI coding assistant** —
Claude, Gemini, Cursor, Copilot, Windsurf, and more — through the open
[`AGENTS.md`](https://agents.md) standard.

[![validate](https://github.com/hrdevop/universal-ai-agents/actions/workflows/validate.yml/badge.svg)](https://github.com/hrdevop/universal-ai-agents/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AGENTS.md](https://img.shields.io/badge/standard-AGENTS.md-0a7cff)](https://agents.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

Each agent lives in its own folder under [`agents/`](agents/) and is **fully
self-contained** — its own operating manual (`AGENTS.md`), its own routines, its own
configuration. Nothing personal is hardcoded; every agent is driven by config files you
control, so the same agent works for anyone, on any assistant.

## Why this exists

Most "AI agent" recipes are written for one tool and one person — they bake a specific
assistant and a specific user's details right into the prompt. This project flips that:

- **Write once, run in any assistant.** The brain is a standard `AGENTS.md`; tool files
  are thin adapters. No rewrite to move from Claude to Gemini to Cursor.
- **One agent, many users.** Your details live in a config profile, not the prompt — so
  the same agent serves you, your friend, or your whole team without edits.
- **Safe by design.** Agents prepare and propose; *you* approve anything outward-facing.
  No fabrication, no captcha bypassing, no silent auto-submitting.

## Works with any assistant

The canonical instructions for every agent live in an `AGENTS.md` file — the cross-tool
standard read **natively** by 20+ tools. A few assistants use their own filename, so each
agent ships thin adapters that just point back to `AGENTS.md` (zero duplication).

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
| _More on the way_ | Outreach, research, content, and more. [Suggest one →](../../issues/new/choose) | 🛠️ Planned |

## Quick start

Each agent runs from inside its own directory — open it in whichever assistant you use.

```bash
git clone https://github.com/hrdevop/universal-ai-agents.git
cd universal-ai-agents/agents/job-application
# then open THIS folder in your assistant:
#   Claude Code  →  run  claude   (then /setup)
#   Gemini CLI   →  run  gemini
#   Cursor       →  open the folder; it reads AGENTS.md
#   …            →  any AGENTS.md-aware tool
```

Then follow that agent's [README](agents/job-application/README.md). The Job Application
Agent walks you through **Setup → Search → Apply → Report**. In Claude Code those are
`/setup`, `/search`, `/apply`, `/report`; in any other assistant, just ask for the
routine by name ("run the Setup routine").

## See it in action

```text
You:   run a Search for remote senior react roles
Agent: → output/you/jobs/results.md
```

| Score | Company | Position | Location | Salary | Apply |
|------:|---------|----------|----------|--------|-------|
| 100 | Acme | Senior React Engineer | Remote | $130k | [link] |
| 60  | Globex | Frontend Engineer | Remote | — | [link] |

```text
You:   apply to Acme
Agent: tailored resume + cover letter written. Then:

         Company:      Acme
         Position:     Senior React Engineer
         Score:        100
         Resume:       output/you/resumes/acme-resume.md
         Cover letter: output/you/coverletters/acme.md

         Apply? (yes/no)        ← nothing is sent until you say yes
```

## Repository layout

```text
universal-ai-agents/
├── README.md                       # you are here — the agent index
├── AGENTS.md                       # repo-wide conventions (canonical)
├── CLAUDE.md · GEMINI.md           # thin adapters → @AGENTS.md
├── CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md · LICENSE
├── scripts/validate-agents.py      # convention checker (run by CI)
├── .github/
│   ├── workflows/validate.yml      # CI: validates every push & PR
│   ├── copilot-instructions.md     # Copilot adapter
│   ├── ISSUE_TEMPLATE/             # "Suggest an agent" · "Bug report"
│   └── pull_request_template.md
├── .cursor/rules/agents.mdc        # Cursor adapter
└── agents/
    └── job-application/            # one self-contained agent
        ├── AGENTS.md               # the agent's operating manual (canonical)
        ├── CLAUDE.md · GEMINI.md   # thin adapters → @AGENTS.md
        ├── README.md               # full usage guide
        ├── .claude/commands/       # Claude slash commands (others run routines by name)
        ├── config/                 # config.example.yaml + per-user profiles
        ├── templates/              # resume & cover-letter templates
        └── output/                 # generated results & tracker (gitignored)
```

## Design principles

- **Vendor-neutral** — `AGENTS.md` is the single source of truth; tool files only point
  to it.
- **Configurable, not hardcoded** — profiles and weights live in YAML; the same agent
  serves everyone.
- **Self-contained** — each agent is isolated, so adding one never breaks another.
- **Human-in-the-loop** — agents prepare and propose; you approve anything
  outward-facing. No captcha bypassing, no auto-submitting, no fabrication.
- **Privacy by default** — personal profiles and generated output are gitignored, never
  published. CI fails the build if any personal data is committed.

## Adding a new agent

See [CONTRIBUTING.md](CONTRIBUTING.md): copy an existing agent, write its `AGENTS.md`
(+ thin `CLAUDE.md`/`GEMINI.md` adapters) and routines, then run the validator:

```bash
pip install pyyaml && python3 scripts/validate-agents.py
```

CI runs the same check on every push and PR, so structure and privacy stay guaranteed as
the collection grows.

## FAQ

**Do I need Claude Code?** No. Any `AGENTS.md`-aware assistant works; Claude Code just
adds slash-command shortcuts.

**Will my personal data end up on GitHub?** No. Real configs, profiles, and all
generated output are gitignored — only `example` templates are tracked, and CI enforces
it.

**Can I run it for several people?** Yes — one profile per person, isolated output per
person. See the agent's [README](agents/job-application/README.md#using-it-for-more-than-one-person).

**Does it auto-apply to jobs?** Never without your explicit `yes`. The confirmation gate
is mandatory and can't be disabled.

## Community

- 💡 [Suggest an agent or report a bug](../../issues/new/choose)
- 🤝 [Contributing guide](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md)
- 🔒 [Security policy](SECURITY.md)

## License

[MIT](LICENSE) © 2026 Hansraj Rana
