# Job Application Agent

A configurable, **multi-user** job-search-and-application assistant driven by
Claude Code. It sources roles from your browser, scores them against *your*
priorities, tailors a truthful resume + cover letter per job, and tracks
everything — and it never submits anything without your explicit OK.

It's config-driven: nothing about any one person is baked in. Each user has their
own profile, their own scoring weights, and their own private output folder.

## Quick start

```text
1. /setup          # answer a few questions — generates your profile
2. /search         # finds & scores jobs in your browser, writes a ranked list
3. /apply <job>    # tailors materials, asks "Apply? (yes/no)", then tracks it
4. /report         # daily summary of what happened
```

Already have multiple people using this? Switch between them with `/use <id>`.

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

Jobs are read from **your own browser session** (Claude in Chrome) across LinkedIn,
Wellfound, RemoteOK, YC Jobs, and company career pages. The agent respects your
logins and will **pause and ask you** to handle any captcha or login wall — it never
bypasses them.

## The rules it always follows

- Never fabricates anything — resumes/cover letters use only the real facts in your
  profile.
- Never submits an application without your explicit `yes`.
- Never bypasses captchas or auto-solves hiring assessments.
- Caps at 20 applications/day; prefers quality over quantity.

See `CLAUDE.md` for the full operating manual and `.claude/commands/` for what each
slash command does.
