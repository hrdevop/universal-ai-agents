---
description: Onboard a new user — import their resume (or interview) and generate their profile
---

# Setup routine — onboarding

Create (or update) a user profile so this person can run the Job Application Agent.
This produces a YAML profile — no code. Prefer **importing the user's resume** so most
fields fill in automatically; fall back to a short interview for the rest.

## Steps

0. **Bootstrap config (fresh clone):** if `config/config.yaml` does not exist,
   create it by copying `config/config.example.yaml`. The example ships in git;
   `config/config.yaml` is gitignored and holds this machine's local state.

1. **Offer to import a resume (the fast path).** Ask the user to either give a **file
   path** to their resume (PDF / DOCX / Markdown / TXT) or **paste its text**.
   - Read it with whatever file-reading capability you have (a Read/file tool; many
     assistants can read PDFs directly). If you can't read the format, ask the user to
     paste the text or export to PDF/Markdown.
   - **Extract** what's actually in the resume — never invent:
     - `name`, `location`, current/target `role`
     - `contact`: email, phone, LinkedIn, portfolio
     - `stack`: the skills/technologies the resume actually lists
     - `experience`: real roles — `company`, `title`, `dates`, a few `highlights`
   - If the user has no resume, **skip to a short interview** for the fields above.

2. **Ask only what a resume can't tell you** (`AskUserQuestion`, one short screen) —
   these are job-search preferences, not resume facts:
   - Salary targets (local and/or remote — skip dimensions that don't apply)
   - Preferred locations (e.g. Remote, India, UAE, …)
   - Priority order of signals (what matters most: remote? a specific tech?)
   - Anything to always reject (on top of the global reject rules)
   - Which sources to search (default to all in `config/config.yaml`)
   - Optionally, where their master resume lives, to save as `resume_source`.

3. **Review the draft before writing.** Show the assembled profile and ask the user to
   confirm or correct it — especially `stack` and `experience`, since those are the
   **only** truthful basis for tailored resumes. Nothing outside what they confirm will
   ever be claimed. Fix anything they flag.

4. **Derive the profile id**: slugify the name to lowercase-kebab-case
   (e.g. "Alice Example" → `alice-example`). If `config/profiles/<id>.yaml` already
   exists, confirm whether to overwrite or pick a new id.

5. **Write `config/profiles/<id>.yaml`** following the shape of
   `config/profiles/example.yaml` (include `experience` and `resume_source` if obtained;
   put any reweighting under `overrides.scoring`). Only include fields actually provided.

6. **Activate the profile**: set `active_profile: <id>` in `config/config.yaml`.

7. **Scaffold outputs**: create
   `output/<id>/{jobs,resumes,coverletters,reports,data}/` and write
   `output/<id>/data/applied.json` as `[]` (only if it doesn't already exist).

8. **Confirm**: show the user their profile id, the path written, and that they're now
   the active profile. Tell them they can run the **Search** routine (`/search`) next,
   or **Switch** (`/use <id>`) to change profiles later.
