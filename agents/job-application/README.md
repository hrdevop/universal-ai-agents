# Job Application Agent

A configurable, **multi-user** job-search-and-application assistant that runs on **any
AI coding assistant** (Claude Code, Gemini CLI, Cursor, Copilot, Windsurf, …). It finds
roles, scores them against *your* priorities, tailors a truthful resume + cover letter
per job, tracks every application — and **never submits anything without your explicit
OK**.

It's config-driven: nothing about any one person is baked in. Each user has their own
profile, their own scoring weights, and their own private output folder.

```text
Setup ──▶ Search ──▶ (review ranked list) ──▶ Apply ──▶ confirm? ──▶ Track ──▶ Report
  │                                              │
  └── your profile drives everything             └── nothing is sent until you say "yes"
```

## Contents

- [Works with any assistant](#works-with-any-assistant)
- [Prerequisites](#prerequisites)
- [Install & first run](#install--first-run)
- [Configuration](#configuration)
- [The five routines](#the-five-routines)
- [How scoring works](#how-scoring-works)
- [Where your files live](#where-your-files-live)
- [The application tracker](#the-application-tracker)
- [Sourcing options](#sourcing-options)
- [Using it for more than one person](#using-it-for-more-than-one-person)
- [Privacy & safety](#privacy--safety)
- [Per-assistant cheat sheet](#per-assistant-cheat-sheet)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [A good daily workflow](#a-good-daily-workflow)

## Works with any assistant

The canonical manual is [`AGENTS.md`](AGENTS.md), read natively by Cursor, Codex,
Gemini CLI, Windsurf, Aider, Zed, Cline, and 20+ more. Claude Code reads it via
`CLAUDE.md` (and adds slash commands); Gemini CLI via `GEMINI.md`. The workflows below
are **routines** — in Claude Code they're slash commands; in any other assistant you
trigger them by name in plain language.

| Routine | Claude Code | Any assistant |
|---------|-------------|---------------|
| Generate your profile | `/setup` | "run the **Setup** routine" |
| Find & rank jobs | `/search` | "do a **Search** for remote React roles" |
| Tailor + apply (with your OK) | `/apply <job>` | "**Apply** to the Acme job" |
| Daily summary | `/report` | "run the **Report**" |
| Switch user | `/use <id>` | "**Switch** to profile alice" |

## Prerequisites

- An AGENTS.md-aware AI coding assistant (Claude Code, Gemini CLI, Cursor, Copilot, …).
- `git` to clone the repo.
- Optional but recommended: a **browser-automation tool** for your assistant (e.g.
  Claude in Chrome, or a Playwright MCP) so it can read job boards in your own logged-in
  session. Without one, you simply paste listings — see [Sourcing](#sourcing-options).

## Install & first run

```bash
# 1. Clone the collection and enter THIS agent's folder
git clone https://github.com/hrdevop/universal-ai-agents.git
cd universal-ai-agents/agents/job-application

# 2. Open this folder in your assistant, e.g.
#    Claude Code →  claude
#    Gemini CLI  →  gemini
#    Cursor      →  open the folder; it reads AGENTS.md automatically
```

Then, inside your assistant:

```text
1. Run Setup     → answer a few questions; it writes your profile + creates config.yaml
2. Run Search    → it finds & scores jobs, writes a ranked results.md
3. Run Apply     → it tailors a resume + cover letter, shows a summary, asks "Apply? (yes/no)"
4. Run Report    → it writes a daily summary of what happened
```

> First-time note: the agent ships only templates. The Setup routine copies
> `config/config.example.yaml` → `config/config.yaml` and creates your profile — both
> are kept **out of git** so your data stays local.

## Configuration

Two layers, resolved at the start of every run. **Your profile's `overrides` win over
the global defaults** — that's what lets the same agent serve very different people.

### 1. Global defaults — `config/config.yaml`

Created from `config.example.yaml` on first run. Controls the shared behavior:

```yaml
active_profile: alice          # whose run this is (set by Setup / Switch)
sources: [linkedin, wellfound, remoteok, yc_jobs, company_career_pages]
scoring:
  weights: { react: 20, nextjs: 20, react_native: 20, aws: 20, remote: 20 }
  max_score: 100
reject_rules: [internship, fresher, unpaid, commission_only,
               min_experience_lt_3_years, php_only, wordpress_only]
application:
  daily_cap: 20
  confirmation_prompt: "Apply? (yes/no)"
tracker:
  statuses: [Prepared, Applied, Interview, Rejected, Offer]
```

### 2. Your profile — `config/profiles/<you>.yaml`

The single source of truth for *your* resumes and cover letters. The agent will **never
claim anything outside `stack`**.

```yaml
name: Alice Example
location: Berlin, Germany
role: Senior Backend Engineer
stack: [Python, Go, PostgreSQL, Kubernetes, AWS, Docker, REST APIs, gRPC]
salary_targets: { remote_usd_min: 90000 }
preferences:
  priority: [remote, aws]              # tie-breakers, most important first
  preferred_locations: [Remote, Germany, Netherlands]
overrides:                             # <-- these beat config.yaml
  scoring:
    weights: { python: 20, go: 20, kubernetes: 20, aws: 20, remote: 20 }
  reject_rules: [frontend_only]
  sources: [linkedin, remoteok, yc_jobs]
contact: { email: "", linkedin: "", portfolio: "" }
```

**Override example:** with the profile above, a remote Go + Kubernetes role scores
`20 (remote) + 20 (go) + 20 (kubernetes) = 60`, even though the global defaults know
nothing about Go or Kubernetes. Reweighting in `overrides.scoring` is how you make the
ranking reflect *your* stack.

## The five routines

Examples below show the Claude Code slash command; in other assistants, ask for the
routine by name.

### Setup — create your profile

```text
You: /setup
Agent: (interviews you) name? location? role? your real skills? salary targets?
       preferred locations? what matters most? anything to always reject?
   →  writes config/profiles/alice.yaml
   →  sets active_profile: alice in config.yaml
   →  scaffolds output/alice/ with an empty tracker
```

Run it once per person. Re-running for an existing profile asks before overwriting.

### Search — find, score & rank

```text
You: /search remote senior python
Agent: reads your sources (browser/web/paste) → drops rejected categories →
       scores with YOUR weights → sorts high→low
   →  writes output/alice/jobs/results.md
```

`output/alice/jobs/results.md` looks like:

| Score | Company | Position | Location | Salary | Apply |
|------:|---------|----------|----------|--------|-------|
| 80 | Acme | Senior Backend Engineer | Remote | $120k | [link] |
| 60 | Globex | Platform Engineer | Berlin | — | [link] |

### Apply — tailor, confirm, track

This is the careful one. It prepares materials, then **stops at a confirmation gate**.

```text
You: /apply Acme
Agent: analyzes the JD, fills your resume + cover letter (truthfully) →
   →  output/alice/resumes/acme-resume.md
   →  output/alice/coverletters/acme.md
   →  marks the job "Prepared" in the tracker, then shows:

       Company:      Acme
       Position:     Senior Backend Engineer
       Score:        80
       Resume:       output/alice/resumes/acme-resume.md
       Cover letter: output/alice/coverletters/acme.md

       Apply? (yes/no)

You: yes
Agent: helps you submit (opens the link / fills what it can, or hands you the link +
       files), then flips the tracker row to "Applied". On "no", nothing is sent.
```

It enforces the daily cap (default 20 *submitted* applications/day) and will pause for
you to handle any login, captcha, or assessment — it never does those itself.

### Report — daily summary

```text
You: /report
   →  writes output/alice/reports/daily-report.md:
      Jobs Found · Top Matches · Applications Prepared · Submitted Today · Interview Requests
```

### Switch — change the active person

```text
You: /use bob      # makes Bob the active profile; his output lives under output/bob/
```

## How scoring works

Each job earns points for the signals in your effective weights (profile overrides,
else global defaults), **capped at `max_score`** (default 100):

| Signal matched | Points (default) |
|----------------|-----------------:|
| Remote | +20 |
| React | +20 |
| Next.js | +20 |
| React Native | +20 |
| AWS | +20 |

- A fully-matching remote React/Next/RN/AWS role → **100**.
- A remote React + Next.js role (no RN, no AWS) → `20+20+20` = **60**.
- Ties are broken by your `preferences.priority` order.
- **Reject rules are applied *before* scoring** — a rejected job never appears at all.

## Where your files live

Everything you generate is private to your profile, under `output/<you>/`:

```text
output/alice/
  jobs/results.md              # latest ranked matches
  resumes/<company>-resume.md  # one tailored resume per job
  coverletters/<company>.md    # one cover letter per job (≤250 words)
  data/applied.json            # your application tracker (the durable state)
  reports/daily-report.md      # daily summary
```

`<company>` is lowercased and kebab-cased — `Acme Corp` → `acme-corp`.

## The application tracker

`output/<you>/data/applied.json` is a JSON array, one object per job:

```json
[
  { "company": "Acme", "role": "Senior Backend Engineer", "date": "2026-06-09", "status": "Applied" }
]
```

Status moves through: **Prepared → Applied → Interview → Rejected → Offer**. The agent
sets `Prepared` when materials are generated and `Applied` only after you confirm a
submission. Update `Interview` / `Offer` / `Rejected` yourself as things progress (just
ask the agent, or edit the file).

## Sourcing options

The agent reads listings with whatever web access your assistant has — pick the best
available:

1. **Browser-assisted (recommended).** A browser-automation tool drives your real,
   logged-in session (e.g. Claude in Chrome, Playwright MCP). Best results on LinkedIn /
   Wellfound where you're signed in.
2. **Web fetch/search.** For public listings and company career pages.
3. **Manual paste.** No web tools? Paste job URLs or descriptions and the agent scores,
   tailors, and tracks them all the same.

On any **login wall or captcha**, the agent stops and asks you to handle it — it never
bypasses either.

## Using it for more than one person

Each person is a profile under `config/profiles/`, with isolated output under
`output/<id>/`. Run `/setup` once per person, and `/use <id>` to switch who's active.
Nobody can see or overwrite anyone else's results.

## Privacy & safety

- **Your data never leaves your machine via git.** `config/config.yaml`, your real
  `config/profiles/*.yaml`, and everything in `output/` are gitignored. Only the
  `example` templates are tracked.
- **Hard rules the agent always follows:**
  - Never fabricates — resumes/cover letters use only the real facts in your profile.
  - Never submits an application without your explicit `yes`.
  - Never bypasses captchas/logins; never auto-solves hiring assessments.
  - Caps at `daily_cap` submitted applications/day; prefers quality over quantity.

## Per-assistant cheat sheet

| | Claude Code | Gemini CLI | Cursor / Codex / Windsurf / others |
|--|--|--|--|
| Reads instructions from | `CLAUDE.md` → `@AGENTS.md` | `GEMINI.md` → `@AGENTS.md` | `AGENTS.md` natively |
| Trigger a routine | `/setup`, `/search`, `/apply`, `/report`, `/use` | "run the Setup routine", … | "run the Setup routine", … |
| Browser sourcing | Claude in Chrome (if connected) | its browser/web tool, else paste | its browser/web tool, else paste |

## Troubleshooting & FAQ

**"No active profile" / it asks me to run Setup.** There's no `config/config.yaml` or no
profile yet. Run **Setup** (it bootstraps both from the examples).

**Search returns nothing / can't open a site.** Your assistant likely has no browser
tool, or you're not logged in. Either connect a browser tool, or paste the listings/URLs
and ask it to score them.

**The ranking ignores my main skill.** Add it to your profile's `overrides.scoring.weights`
— the defaults only know React/Next/RN/AWS/Remote.

**It won't submit / keeps asking to confirm.** By design. The `Apply? (yes/no)` gate is
mandatory; reply `yes` to proceed, `no` to stop.

**Can I edit my resume/cover letter before sending?** Yes — they're plain Markdown in
`output/<you>/`. Edit them, then submit.

**Where do I change the daily cap or confirmation wording?** `config/config.yaml`
(`application.daily_cap`, `application.confirmation_prompt`). The confirmation gate
itself can't be disabled.

## A good daily workflow

```text
morning →  /search           # refresh the ranked list
        →  scan results.md, pick the top few that fit
        →  /apply <each>      # tailor, review, confirm one by one
        →  /report            # log the day
later   →  update statuses as interviews/offers come in
```

---

See [`AGENTS.md`](AGENTS.md) for the full operating manual, `.claude/commands/` for each
routine's step-by-step, and the [repo README](../../README.md) for the wider collection.
