<!-- Thanks for contributing! Keep PRs focused and self-contained. -->

## What does this PR do?



## Checklist

- [ ] Scoped to one agent (or repo-wide infra) — no unrelated changes
- [ ] If adding/changing an agent: `AGENTS.md` is the canonical manual, and
      `CLAUDE.md` / `GEMINI.md` are thin `@AGENTS.md` adapters (no duplicated content)
- [ ] No personal data committed — only `config.example.yaml` and
      `config/profiles/example.yaml` are tracked; real configs / `output/` stay gitignored
- [ ] Human-in-the-loop preserved — no captcha bypass, no auto-submit, no fabrication
- [ ] `python3 scripts/validate-agents.py` passes locally (CI runs it too)
- [ ] New agent? Added a row to the table in `README.md`
