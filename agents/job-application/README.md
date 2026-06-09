# Job Application Agent

A configurable, **multi-user** job-search-and-application assistant that runs on **any
AI coding assistant** (Claude, Gemini, Cursor, Copilot, …). It sources roles, scores
them against *your* priorities, tailors a truthful resume + cover letter per job, and
tracks everything — and it never submits anything without your explicit OK.

It's config-driven: nothing about any one person is baked in. Each user has their
own profile, their own scoring weights, and their own private output folder.

## Works with any assistant

The canonical manual is [`AGENTS.md`](AGENTS.md), read natively by Cursor, Codex,
Gemini CLI, Windsurf, Aider, Zed, Cline, and more. Claude Code reads it via `CLAUDE.md`
and adds slash commands; Gemini CLI via `GEMINI.md`. The workflows below are **routines**
you can trigger by name in any assistant — in Claude Code they're also slash commands.

## Quick start

| Routine | Claude Code | Any assistant |
|---------|-------------|---------------|
| Generate your profile | `/setup` | "run the **Setup** routine" |
| Find & rank jobs | `/search` | "do a **Search**" |
| Tailor + apply (with your OK) | `/apply <job>` | "**Apply** to <job>" |
| Daily summary | `/report` | "run the **Report**" |
| Switch user | `/use <id>` | "**Switch** to profile <id>" |

## How it works

- **Profiles** live in `config/profiles/<id>.yaml` — your name, role, real skills,
  salary targets, preferred locations, and any scoring tweaks. Copy
  `config/profiles/example.yaml` or just run `/setup`.
- **Global defaults** live in `config/config.yaml` — sources, default scoring
  weights, reject rules, the daily cap, and the confirmation prompt.
- **Your overrides win.** Anything under `overrides:` in your profile beats the
  global default, so you weight scoring to *your* stack — that's what makes this
  multi-user instead of one-size-fits-all.
- **Outputs are private per user**, under `output/<id>/`:

  ```text
  output/<id>/
    jobs/results.md              # ranked matches
    resumes/<company>-resume.md  # tailored, per job
    coverletters/<company>.md    # ≤250 words, per job
    data/applied.json            # your application tracker
    reports/daily-report.md      # daily summary
  ```

## Scoring

Each job earns points for the signals you care about (default: React, Next.js,
React Native, AWS, Remote — +20 each, capped at 100). Reweight them in your
profile's `overrides.scoring`. Jobs matching the reject rules (internship, fresher,
unpaid, commission-only, <3 yrs required, PHP-only, WordPress-only — plus your own
additions) are dropped before scoring.

## Sourcing

Jobs are read using whatever web access your assistant has — a browser-automation tool
driving your own session (e.g. Claude in Chrome, Playwright MCP), a web-fetch/search
tool, or, if it has none, listings **you paste in**. Sources include LinkedIn,
Wellfound, RemoteOK, YC Jobs, and company career pages. The agent respects your logins
and will **pause and ask you** to handle any captcha or login wall — it never bypasses
them.

## The rules it always follows

- Never fabricates anything — resumes/cover letters use only the real facts in your
  profile.
- Never submits an application without your explicit `yes`.
- Never bypasses captchas or auto-solves hiring assessments.
- Caps at 20 applications/day; prefers quality over quantity.

See [`AGENTS.md`](AGENTS.md) for the full operating manual and `.claude/commands/` for
the detailed step-by-step of each routine.
