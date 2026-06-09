---
description: Prepare a tailored resume + cover letter, confirm, then track
argument-hint: <company name or row # from results.md>
---

# Apply routine — Prepare & (with approval) apply

> Claude Code exposes this as `/apply`; any assistant can run it by asking to "Apply"
> to a job from the results.

Prepare application materials for one job from the active profile's
`output/<active_profile>/jobs/results.md`, then gate on explicit confirmation.

## Resolve

1. Read `config/config.yaml` + the active profile. Identify the target job from
   `$ARGUMENTS` (company name or the row number in `results.md`). If ambiguous,
   show the candidates and ask which one.
2. Let `company` = the company name slugified to lowercase-kebab-case.

## Enforce the daily cap

3. Read `output/<active_profile>/data/applied.json`. Count entries with
   `status: Applied` and today's date. If that count is already at
   `application.daily_cap`, STOP and tell the user the cap is reached.

## Prepare materials

4. Analyze the job description. Fill `templates/resume.md.tmpl` using ONLY facts
   from the profile (tailor emphasis, never fabricate) →
   `output/<active_profile>/resumes/<company>-resume.md`.
5. Fill `templates/coverletter.md.tmpl` (≤250 words, personalized, names the
   overlapping technologies, no generic AI filler) →
   `output/<active_profile>/coverletters/<company>.md`.
6. Upsert a tracker row in `applied.json` with `status: "Prepared"`, today's date
   (`YYYY-MM-DD`), the company and role.

## Confirmation gate (mandatory)

7. Display:
   - Company
   - Position
   - Score
   - Resume path
   - Cover letter path
8. Ask exactly the configured prompt: **`Apply? (yes/no)`**
   (`application.confirmation_prompt`). Do not proceed on anything but a clear
   `yes`. This gate is mandatory and is never skipped, regardless of config.

## On approval

9. Help the user submit. If your assistant has browser automation (Claude in Chrome,
   Playwright MCP, a built-in browser tool), open the apply link and fill what can be
   filled from the materials, handing off anything requiring their judgment. If it
   doesn't, give the user the apply link plus the resume/cover-letter paths to submit
   themselves. Either way: never bypass captchas and never auto-solve assessments —
   pause and ask the user for those.
10. Update the tracker row to `status: "Applied"` with today's date. Confirm done
    and report remaining daily-cap headroom.
