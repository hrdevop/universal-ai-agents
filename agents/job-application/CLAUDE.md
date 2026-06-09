# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software codebase** — it is a **configurable, multi-user Job
Application Agent**. There is no build, test, or lint step. "Running" it means
executing the search → score → tailor → confirm → track workflow for whichever
user's profile is active, and writing the results into that user's namespaced
output directory.

Nothing personal is hardcoded here. Each user supplies their own data via a
profile file; the agent's behavior is driven entirely by configuration plus this
manual. To onboard a new person, run `/setup`.

## Configuration model (read this before doing anything)

Two layers, resolved at the start of every run:

1. **`config/config.yaml`** — global defaults: `active_profile`, `sources`,
   `scoring.weights` + `max_score`, `reject_rules`, `application` (daily cap,
   confirmation prompt), `tracker.statuses`.
2. **`config/profiles/<id>.yaml`** — one file per user: `name`, `location`,
   `role`, `stack`, `salary_targets`, `preferences`, optional `overrides`, `contact`.

**Resolution precedence: `profile.overrides` > `config.yaml` defaults.** A profile's
`overrides.scoring` / `overrides.reject_rules` / `overrides.sources` replace the
matching global values, letting each user weight scoring to their own stack. Always
compute the effective settings by layering the profile's overrides on top of the
global config before sourcing or scoring.

The **active profile** (`config.yaml: active_profile`) decides whose run this is and
where output goes. If no active profile exists or `config/profiles/` is empty, tell
the user to run `/setup` first — do not invent a profile.

`config/profiles/example.yaml` is a documented template, not a real user; never
treat it as active.

## Output layout (namespaced per user)

Everything a run produces goes under `output/<active_profile>/`:

| Path | Purpose |
|------|---------|
| `output/<id>/jobs/results.md` | Ranked search results, score desc |
| `output/<id>/resumes/{company}-resume.md` | Per-job tailored resume |
| `output/<id>/coverletters/{company}.md` | Per-job cover letter (≤250 words) |
| `output/<id>/data/applied.json` | Application tracker (durable state) |
| `output/<id>/reports/daily-report.md` | Daily run summary |

`{company}` = company name lowercased and kebab-cased (`Acme Corp` → `acme-corp`).
Read `output/<id>/data/applied.json` at the start of a run to avoid re-preparing or
re-applying to jobs already in flight. Users never share output dirs.

## Slash commands (the operating surface)

| Command | What it does |
|---------|--------------|
| `/setup` | Interview a new user, write `config/profiles/<id>.yaml`, activate it, scaffold their output dirs |
| `/use <id>` | Switch the active profile (ensures their output dirs exist) |
| `/search` | Browser-assisted sourcing → filter → score → ranked `results.md` |
| `/apply <job>` | Tailor resume + cover letter, show summary, **confirmation gate**, update tracker |
| `/report` | Write the daily report for the active profile |

The full instructions for each live in `.claude/commands/`.

## Scoring

Additive: each matched signal adds its configured points, capped at `max_score`
(default 100). Defaults weight React / Next.js / React Native / AWS / Remote at +20
each, but the **effective** weights come from the resolved config — never assume the
defaults; read them. Break ties using the profile's `preferences.priority` order.
Apply `reject_rules` (effective set) **before** scoring; never surface a rejected job.

## Sourcing — browser-assisted (Claude in Chrome)

Listings are read from the user's real browser session, not scraped behind their
back:

- Load the MCP tools before use: `ToolSearch` →
  `select:mcp__claude-in-chrome__tabs_context_mcp` (and other
  `mcp__claude-in-chrome__*` tools as needed), then call `tabs_context_mcp`.
- Open a **new tab** per source; don't hijack the user's existing tabs.
- On a **login wall or captcha**, STOP and ask the user to log in / solve it in
  their browser, then continue. **Never bypass either.**

## Tracking — `output/<id>/data/applied.json`

JSON array, one object per job: `{ "company": "", "role": "", "date": "", "status": "" }`.
`status` ∈ `tracker.statuses` (`Prepared` → `Applied` → `Interview` → `Rejected` →
`Offer`). Set `Prepared` when materials are generated; `Applied` only after a
confirmed submission. Dates are ISO (`YYYY-MM-DD`).

## Hard rules (non-negotiable, apply to every user)

- Never fabricate information — resumes/cover letters draw only from the active
  profile's real data. Tailor emphasis; never invent employers, projects, or skills.
- Never bypass captchas or login walls — pause and ask the user.
- Never auto-solve hiring assessments — hand them to the user.
- **Never submit an application without an explicit `yes` at the confirmation gate.**
  This gate is mandatory and is honored even if a config somehow disables it.
- Respect the daily cap (`application.daily_cap`, default 20). Prefer quality over
  quantity.
