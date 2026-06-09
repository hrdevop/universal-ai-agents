# AGENTS.md — Job Application Agent

Operating manual for this agent. It is **vendor-neutral**: any AI coding assistant
that reads `AGENTS.md` (Cursor, Codex, Gemini CLI, Windsurf, Aider, Zed, Cline, and
more) can run it. Claude Code reads it via `CLAUDE.md` (`@AGENTS.md`); Gemini CLI via
`GEMINI.md`. The thin per-tool files in this folder all point back here — **this file
is the single source of truth.**

## What this agent is

A **configurable, multi-user Job Application Agent**. It is not a software codebase —
there is no build, test, or lint step. "Running" it means executing the
search → score → tailor → confirm → track workflow for whichever user's profile is
active, and writing the results into that user's namespaced output directory.

Nothing personal is hardcoded. Each user supplies their own data via a profile file;
behavior is driven entirely by configuration plus this manual. To onboard someone,
run the **Setup** routine.

## Configuration model (read this before doing anything)

Two layers, resolved at the start of every run:

1. **`config/config.yaml`** — global defaults: `active_profile`, `sources`,
   `scoring.weights` + `max_score`, `reject_rules`, `application` (daily cap,
   confirmation prompt), `tracker.statuses`. (On a fresh clone this file does not
   exist yet — create it by copying `config/config.example.yaml`.)
2. **`config/profiles/<id>.yaml`** — one file per user: `name`, `location`, `role`,
   `stack`, `salary_targets`, `preferences`, optional `overrides`, `contact`, and
   optional `resume_source` (path/URL to their master resume) + `experience` (real work
   history). The **Setup** routine can import most of these automatically by reading the
   user's resume — see Routines below.

**Resolution precedence: `profile.overrides` > `config.yaml` defaults.** A profile's
`overrides.scoring` / `overrides.reject_rules` / `overrides.sources` replace the
matching global values, letting each user weight scoring to their own stack. Always
compute the effective settings by layering the profile's overrides on top of the
global config before sourcing or scoring.

The **active profile** (`config.yaml: active_profile`) decides whose run this is and
where output goes. If no active profile exists or `config/profiles/` is empty, run the
**Setup** routine first — do not invent a profile. `config/profiles/example.yaml` is a
documented template, not a real user; never treat it as active.

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

## Routines (the operating surface)

These are the agent's workflows. **Any assistant can run them by name in natural
language** ("run the Setup routine", "do a Search"). **Claude Code** additionally
exposes them as slash commands (`.claude/commands/`), shown in parentheses.

| Routine | (Claude slash) | What it does |
|---------|----------------|--------------|
| **Setup** | `/setup` | Import the user's resume (or interview) to auto-fill `config/profiles/<id>.yaml`, activate it, scaffold their output dirs |
| **Switch profile** | `/use <id>` | Change the active profile (ensures their output dirs exist) |
| **Search** | `/search` | Source listings → filter → score → ranked `results.md` |
| **Apply** | `/apply <job>` | Tailor resume + cover letter, show summary, **confirmation gate**, update tracker |
| **Report** | `/report` | Write the daily report for the active profile |

The detailed step-by-step for each routine lives in `.claude/commands/*.md` and is
written to be readable by any assistant, not just Claude Code.

## Scoring

Additive: each matched signal adds its configured points, capped at `max_score`
(default 100). Defaults weight React / Next.js / React Native / AWS / Remote at +20
each, but the **effective** weights come from the resolved config — never assume the
defaults; read them. Break ties using the profile's `preferences.priority` order.
Apply `reject_rules` (effective set) **before** scoring; never surface a rejected job.

## Sourcing (tool-agnostic) — combine strategies, strongest first

Don't rely on one method (that's how Search comes up empty). Work down this ladder and
combine — full step-by-step in `.claude/commands/search.md`:

1. **Sub-agent fan-out (best).** If your assistant can spawn sub-agents (Claude Code: the
   **Agent** tool), dispatch one per source concurrently; each returns structured job
   records, then merge and dedupe.
2. **Public job APIs (always try — no login, rarely empty).** Fetch directly with any
   web tool: RemoteOK `https://remoteok.com/api` (skip element 0), Arbeitnow
   `https://www.arbeitnow.com/api/job-board-api`, Hacker News "Who is hiring" via
   `https://hn.algolia.com/api/v1/search?tags=story&query=who%20is%20hiring`, and company
   ATS boards (Greenhouse `boards-api.greenhouse.io/v1/boards/<co>/jobs`, Lever
   `api.lever.co/v0/postings/<co>?mode=json`, Ashby `api.ashbyhq.com/posting-api/job-board/<co>`).
3. **Browser automation** for JS-rendered / gated boards — a Playwright MCP, or Claude in
   Chrome for the user's logged-in session.
4. **Manual paste** fallback — the user pastes URLs/descriptions; score those.

Guardrails, every strategy:
- On a **login wall, captcha, or bot-block**, STOP and ask the user to log in / solve it
  — or switch that source to a public API. **Never bypass.**
- **Never silently return nothing** — if a source is empty, say so and try the next one;
  report what was tried.
- Extract per job: Company, Position, Location, Salary (if shown), Apply Link, and the
  matched signals (for scoring).

## Tracking — `output/<id>/data/applied.json`

JSON array, one object per job: `{ "company": "", "role": "", "date": "", "status": "" }`.
`status` ∈ `tracker.statuses` (`Prepared` → `Applied` → `Interview` → `Rejected` →
`Offer`). Set `Prepared` when materials are generated; `Applied` only after a confirmed
submission. Dates are ISO (`YYYY-MM-DD`).

## Hard rules (non-negotiable, apply to every user and every assistant)

- Never fabricate information — resumes/cover letters draw only from the active
  profile's real data. Tailor emphasis; never invent employers, projects, or skills.
- Never bypass captchas or login walls — pause and ask the user.
- Never auto-solve hiring assessments — hand them to the user.
- **Never submit an application without an explicit `yes` at the confirmation gate.**
  This gate is mandatory and is honored even if a config somehow disables it.
- Respect the daily cap (`application.daily_cap`, default 20). Prefer quality over
  quantity.
