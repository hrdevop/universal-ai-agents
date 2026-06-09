---
description: Onboard a new user — interview them and generate their profile
---

# /setup — Interactive onboarding

Create (or update) a user profile so this person can run the Job Application Agent.
Do NOT write any code; this is a guided interview that produces a YAML file.

## Steps

0. **Bootstrap config (fresh clone):** if `config/config.yaml` does not exist,
   create it by copying `config/config.example.yaml`. The example ships in git;
   `config/config.yaml` is gitignored and holds this machine's local state.

1. **Interview the user** with `AskUserQuestion` (batch related questions; keep it
   to a few screens). Collect:
   - Full name
   - Location (city, country)
   - Current/target role/title
   - Tech stack / skills they ACTUALLY have (this becomes the only truthful basis
     for resumes — stress that nothing outside it will ever be claimed)
   - Salary targets (local and/or remote — let them skip dimensions that don't apply)
   - Preferred locations (e.g. Remote, India, UAE, ...)
   - Priority order of signals (what matters most: remote? a specific tech?)
   - Anything they want to always reject (on top of the global reject rules)
   - Which sources to search (default to all in `config/config.yaml`)
   - Optional contact details (email, LinkedIn, portfolio)

2. **Derive the profile id**: slugify the name to lowercase-kebab-case
   (e.g. "Alice Example" → `alice-example`). If `config/profiles/<id>.yaml`
   already exists, confirm whether to overwrite or pick a new id.

3. **Write `config/profiles/<id>.yaml`** following the shape of
   `config/profiles/example.yaml`. Put any reweighting under `overrides.scoring`.
   Only include fields the user actually provided.

4. **Activate the profile**: set `active_profile: <id>` in `config/config.yaml`.

5. **Scaffold outputs**: create
   `output/<id>/{jobs,resumes,coverletters,reports,data}/` and write
   `output/<id>/data/applied.json` as `[]` (only if it doesn't already exist).

6. **Confirm**: show the user their profile id, the path written, and that they're
   now the active profile. Tell them they can run `/search` next, or `/use <id>`
   to switch profiles later.
