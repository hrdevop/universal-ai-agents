---
description: Browser-assisted job search → scored, ranked results.md
argument-hint: [optional extra keywords or focus, e.g. "remote senior react"]
---

# /search — Find, score & rank jobs

Source listings for the **active profile** using the user's real browser session,
score them, and write a ranked results file. Never bypass logins or captchas.

## Resolve config first

1. Read `config/config.yaml` and the active profile
   (`config/profiles/<active_profile>.yaml`). Compute the effective settings by
   layering `profile.overrides` on top of the global defaults
   (**profile.overrides wins**): effective `sources`, `scoring.weights`,
   `reject_rules`, `max_score`.
2. `$ARGUMENTS`, if present, narrows the search (extra keywords/focus).

## Source (browser-assisted via Claude in Chrome)

3. Load the browser tools before calling them:
   `ToolSearch` with `select:mcp__claude-in-chrome__tabs_context_mcp` (and other
   `mcp__claude-in-chrome__*` tools as needed), then call `tabs_context_mcp` to see
   the user's tabs. Open a NEW tab per source rather than reusing the user's tabs.
4. For each effective source (LinkedIn, Wellfound, RemoteOK, YC Jobs, company
   career pages), navigate to a relevant search for the profile's role/stack and
   read the listings.
   - If a site shows a **login wall or captcha**, STOP and ask the user to log in
     or solve it in their browser. Never attempt to bypass it. Then continue.
5. **Extract** per job: Company, Position, Location, Salary (if shown), Apply Link.

## Filter, score, rank

6. Drop any job matching the effective `reject_rules`
   (internship, fresher, unpaid, commission-only, <3 yrs required, PHP-only,
   WordPress-only, plus profile additions).
7. Score each remaining job additively from the effective weights, capped at
   `max_score`. Use the profile's `priority` order to break ties.
8. Sort by score descending.

## Write

9. Write `output/<active_profile>/jobs/results.md` as a Markdown table with
   columns: Score · Company · Position · Location · Salary · Apply Link.
   Above the table, note: profile id, date, # sources searched, # found, # rejected.
10. Briefly summarize the top matches to the user and suggest `/apply` for any they
    want to pursue.
