---
description: Find, score & rank jobs → results.md
argument-hint: [optional extra keywords or focus, e.g. "remote senior react"]
---

# Search routine — Find, score & rank jobs

Source listings for the **active profile**, score them, and write a ranked results file.
(Claude Code exposes this as `/search`; any assistant can run it by asking for a
"Search".)

## Resolve config first

1. Read `config/config.yaml` and the active profile
   (`config/profiles/<active_profile>.yaml`). Compute the effective settings by layering
   `profile.overrides` on top of the global defaults (**profile.overrides wins**):
   effective `sources`, `scoring.weights`, `reject_rules`, `max_score`. Note the
   profile's `role`, `stack`, and `preferences.preferred_locations` — they drive queries.
2. `$ARGUMENTS`, if present, narrows the search (extra keywords/focus).

## Source — use the strongest strategy your assistant supports

Work down this ladder. **Combine strategies** — you want jobs, not one perfect method.

### A. Sub-agent fan-out (best — parallel & robust)

If you can spawn sub-agents (Claude Code: the **Agent** tool, e.g. `Explore` /
`general-purpose`), dispatch **one sub-agent per effective source, concurrently**. Give
each agent: the profile's role + stack + preferred locations + `$ARGUMENTS`, the source
to cover, and this extraction schema — ask it to return a JSON array of:

```json
{ "company": "", "position": "", "location": "", "salary": "",
  "apply_url": "", "source": "", "matched_signals": ["remote", "react"] }
```

Then merge all sub-agents' results and dedupe by (company + position).

### B. Public job APIs (always try these — reliable, no login, rarely empty)

Fetch these directly (a web-fetch tool is enough — no browser needed):

- **RemoteOK** — `https://remoteok.com/api` → JSON array; **skip element 0** (it's
  metadata/legal). Fields: `position`, `company`, `location`, `tags`, `apply_url`,
  `salary_min`, `salary_max`, `url`.
- **Hacker News "Who is hiring"** — find the latest thread via
  `https://hn.algolia.com/api/v1/search?tags=story&query=who%20is%20hiring`, then read its
  comments (`.../items/<id>`) for roles matching the profile.
- **Arbeitnow** — `https://www.arbeitnow.com/api/job-board-api` (paginate with `?page=N`).
  Fields: `title`, `company_name`, `location`, `remote`, `tags`, `url`.
- **Company ATS boards** (for companies the user targets — all public JSON):
  - Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<company>/jobs`
  - Lever: `https://api.lever.co/v0/postings/<company>?mode=json`
  - Ashby: `https://api.ashbyhq.com/posting-api/job-board/<company>`

### C. Browser automation (for JS-rendered or login-gated boards)

For LinkedIn / Wellfound / YC etc., drive a real browser:

- **Playwright MCP** if available (Claude Code: `mcp__plugin_playwright_playwright__*` —
  load via `ToolSearch` first), or **Claude in Chrome** to use the user's logged-in
  session (`select:mcp__claude-in-chrome__tabs_context_mcp`). Open a NEW tab per source.
- Navigate the source's search for the profile's role/stack/location and read the
  rendered listings.

### D. Manual paste (fallback)

No web/browser tools? Ask the user to paste job URLs or descriptions; score those.

### Guardrails (every strategy)

- **Login wall / captcha / bot-block → STOP.** Ask the user to log in or solve it, or
  switch that source to a public API (Strategy B). **Never bypass** either.
- **Never silently return nothing.** If a source yields no jobs, say so and move to the
  next source/strategy. Report what you tried.
- **Extract** per job: Company, Position, Location, Salary (if shown), Apply Link, and
  the matched signals (needed for scoring).

## Filter, score, rank

3. Drop any job matching the effective `reject_rules` (internship, fresher, unpaid,
   commission-only, <3 yrs required, PHP-only, WordPress-only, plus profile additions).
4. Score each remaining job additively from the effective weights, capped at `max_score`.
   Use the profile's `priority` order to break ties.
5. Sort by score descending.

## Write

6. Write `output/<active_profile>/jobs/results.md` as a Markdown table with columns:
   Score · Company · Position · Location · Salary · Apply Link. Above the table, note:
   profile id, date, **which sources/strategies were used**, # found, # rejected, and
   **any source that returned nothing**.
7. Briefly summarize the top matches and suggest the **Apply** routine (`/apply` in
   Claude Code) for any the user wants to pursue. If nothing was found anywhere, tell the
   user plainly and suggest pasting listings or connecting a browser/Playwright tool.
