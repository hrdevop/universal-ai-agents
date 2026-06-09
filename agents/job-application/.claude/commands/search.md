---
description: Find, score & rank jobs → results.md
argument-hint: [optional extra keywords or focus, e.g. "remote senior react"]
---

# Search routine — Find, score & rank jobs

Source listings for the **active profile**, score them, and write a ranked results
file. Never bypass logins or captchas. (Claude Code exposes this as `/search`; any
assistant can run it by asking for a "Search".)

## Resolve config first

1. Read `config/config.yaml` and the active profile
   (`config/profiles/<active_profile>.yaml`). Compute the effective settings by
   layering `profile.overrides` on top of the global defaults
   (**profile.overrides wins**): effective `sources`, `scoring.weights`,
   `reject_rules`, `max_score`.
2. `$ARGUMENTS`, if present, narrows the search (extra keywords/focus).

## Source (use whatever web/browser capability you have)

3. Pick the best web access your assistant offers:
   - **Browser automation** driving the user's real session — e.g. Claude in Chrome
     (load it first with `ToolSearch` → `select:mcp__claude-in-chrome__tabs_context_mcp`
     and other `mcp__claude-in-chrome__*` tools), a Playwright/Puppeteer MCP, or a
     built-in browser tool. Open a NEW tab per source; don't hijack the user's tabs.
   - **Web fetch/search** for public listings and company career pages.
   - **No web access?** Ask the user to paste the listings or URLs and score those.
4. For each effective source (LinkedIn, Wellfound, RemoteOK, YC Jobs, company
   career pages), find listings relevant to the profile's role/stack and read them.
   - If a site shows a **login wall or captcha**, STOP and ask the user to log in
     or solve it. Never attempt to bypass it. Then continue.
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
10. Briefly summarize the top matches to the user and suggest the **Apply** routine
    (`/apply` in Claude Code) for any they want to pursue.
