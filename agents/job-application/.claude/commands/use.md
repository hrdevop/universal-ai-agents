---
description: Switch the active profile
argument-hint: <profile-id>
---

# /use — Switch active profile

Make `$ARGUMENTS` the active profile for subsequent runs.

## Steps

0. If `config/config.yaml` does not exist (fresh clone), create it by copying
   `config/config.example.yaml` first.
1. If no argument was given, list the available profiles (filenames in
   `config/profiles/`, minus `example`) and ask which to use.
2. Verify `config/profiles/$ARGUMENTS.yaml` exists. If not, list the available
   profiles and stop — suggest `/setup` to create a new one.
3. Set `active_profile: $ARGUMENTS` in `config/config.yaml`.
4. Ensure `output/$ARGUMENTS/{jobs,resumes,coverletters,reports,data}/` exist and
   that `output/$ARGUMENTS/data/applied.json` exists (create as `[]` if missing).
5. Confirm the switch and show a one-line summary of that profile (name, role,
   how many entries are already in their tracker).
