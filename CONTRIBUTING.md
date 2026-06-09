# Contributing

Thanks for helping grow **Universal AI Agents**! This repo is a vendor-neutral
collection of self-contained agents — the easiest way to contribute is to add a new
one or improve an existing one.

## Adding a new agent

Each agent lives in its own folder and is fully isolated, so you never have to
touch another agent to add yours.

1. **Create the folder:** `agents/<your-agent-name>/` (lowercase-kebab-case).
2. **Copy the skeleton** from an existing agent (e.g. `agents/job-application/`):
   - `AGENTS.md` — the agent's operating manual (its rules, workflow, config model).
     **This is the canonical, vendor-neutral source of truth.**
   - `CLAUDE.md` and `GEMINI.md` — thin adapters, each just `@AGENTS.md` (so Claude
     Code and Gemini CLI read the same brain). Don't duplicate content into them.
   - `README.md` — a short user guide and quick start.
   - `.claude/commands/*.md` — the routines' step-by-step (Claude exposes them as
     slash commands; other assistants run them by name). Write them tool-agnostically.
   - `config/config.example.yaml` — a **template** config (tracked in git).
   - `templates/`, and any other assets it needs.
3. **Keep personal data out of git.** Real configs and generated output must match
   the patterns in the root [`.gitignore`](.gitignore):
   - `agents/*/config/config.yaml` — gitignored (local state)
   - `agents/*/config/profiles/*.yaml` except `example.yaml` — gitignored
   - `agents/*/output/*/` — gitignored (keep an `output/.gitkeep`)
4. **Register it** by adding a row to the agents table in [README.md](README.md).
5. **Validate** before opening a PR:

   ```bash
   pip install pyyaml
   python3 scripts/validate-agents.py
   ```

   This checks every agent has its `AGENTS.md` + adapters, that YAML parses, and that
   no personal data is tracked. CI ([`.github/workflows/validate.yml`](.github/workflows/validate.yml))
   runs the same check on every push and PR.

## Principles to keep

- **Configurable, not hardcoded** — the same agent should work for any user via
  config; never bake in one person's data.
- **Human-in-the-loop** — agents propose; the user approves outward-facing actions.
  No captcha bypassing, no auto-submitting, no fabricated information.
- **Self-contained** — no cross-agent imports or shared mutable state.

## Improving an existing agent

Open a PR with a clear description of the change. For behavior changes, update that
agent's `AGENTS.md` (the canonical manual) and command files so the docs and behavior
stay in sync — the `CLAUDE.md`/`GEMINI.md` adapters need no edits since they just
import `AGENTS.md`.

## Reporting issues

Use the issue tracker for bugs, ideas, and agent suggestions. Please don't include
real personal data (resumes, emails, API keys) in issues or PRs.
