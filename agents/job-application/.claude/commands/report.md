---
description: Generate the daily report for the active profile
---

# /report — Daily report

Summarize today's activity for the active profile.

## Steps

1. Read `config/config.yaml` to get the active profile.
2. Read `output/<active_profile>/jobs/results.md` and
   `output/<active_profile>/data/applied.json`.
3. Write `output/<active_profile>/reports/daily-report.md` for today
   (`YYYY-MM-DD`) including:
   - **Jobs Found** — count from the latest results.md
   - **Top Matches** — the highest-scored handful (Score · Company · Position)
   - **Applications Prepared** — tracker entries with `status: Prepared`
   - **Applications Submitted** — tracker entries with `status: Applied` dated today
   - **Interview Requests** — tracker entries with `status: Interview`
4. Show the report to the user.
