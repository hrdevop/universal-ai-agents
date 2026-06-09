# Contributing

Thanks for helping grow **Claude Code Agents**! This repo is a collection of
self-contained agents — the easiest way to contribute is to add a new one or
improve an existing one.

## Adding a new agent

Each agent lives in its own folder and is fully isolated, so you never have to
touch another agent to add yours.

1. **Create the folder:** `agents/<your-agent-name>/` (lowercase-kebab-case).
2. **Copy the skeleton** from an existing agent (e.g. `agents/job-application/`):
   - `CLAUDE.md` — the agent's operating manual (its rules, workflow, config model).
   - `README.md` — a short user guide and quick start.
   - `.claude/commands/*.md` — its slash commands.
   - `config/config.example.yaml` — a **template** config (tracked in git).
   - `templates/`, and any other assets it needs.
3. **Keep personal data out of git.** Real configs and generated output must match
   the patterns in the root [`.gitignore`](.gitignore):
   - `agents/*/config/config.yaml` — gitignored (local state)
   - `agents/*/config/profiles/*.yaml` except `example.yaml` — gitignored
   - `agents/*/output/*/` — gitignored (keep an `output/.gitkeep`)
4. **Register it** by adding a row to the agents table in [README.md](README.md).

## Principles to keep

- **Configurable, not hardcoded** — the same agent should work for any user via
  config; never bake in one person's data.
- **Human-in-the-loop** — agents propose; the user approves outward-facing actions.
  No captcha bypassing, no auto-submitting, no fabricated information.
- **Self-contained** — no cross-agent imports or shared mutable state.

## Improving an existing agent

Open a PR with a clear description of the change. For behavior changes, update that
agent's `CLAUDE.md` and command files so the docs and behavior stay in sync.

## Reporting issues

Use the issue tracker for bugs, ideas, and agent suggestions. Please don't include
real personal data (resumes, emails, API keys) in issues or PRs.
