---
name: lint
description: Periodic health check on the vault, run the deterministic scripts, then audit for contradictions, duplicated facts, provenance gaps, staleness, orphans, and drift traps. Report findings, fix what's safe, ask about what isn't.
---

# Lint

The vault's immune system. Run this every few weeks, or after a burst of ingests.

Lint **nudges**. It never confirms anything, `verified:` records that a human checked reality, and no model may set it.

## Phase 1: the deterministic checks

Run these first. They do in seconds what would take you many tool calls:

```bash
python3 scripts/health.py
python3 scripts/link_check.py
python3 scripts/staleness.py
python3 scripts/bring_up.py
python3 scripts/reflow.py
python3 scripts/fm_fix.py
```

`reflow.py` and `fm_fix.py` are safe to auto-fix with `--apply`. They're mechanical. The rest are reporters; act on what they surface.

Then check the Bases directly, they hold the derived state: [[Open-Confirmations]], [[Verification-Dashboard]], [[Gear-Register]].

## Phase 2: the judgment passes

These are yours. Scripts can't do them.

**1. Contradictions.** The same fact stated two different ways on two pages. The more specific page usually wins; the summary defers with a link. When you genuinely can't tell which is right, don't pick. Flag both with `[!question]`, set `open_questions: true`, and ask.

**2. SSOT value-collisions.** Any specific operational value, an IP, a channel number, a level, a time, a model number, appearing *verbatim* in the body of more than one page. Decide which page owns it (the page where an operator *acts* on it), and convert every other occurrence to a `[[wikilink]]`. Catalog lines in `wiki/index.md` are exempt.

**3. Provenance gaps.** Factual pages with no `source:` field, or `source: agent-inferred` claims that have sat unconfirmed for months. List them for sourcing. The user is the only one who can upgrade them.

**4. Open questions.** Every page with `open_questions: true` or an inline `[!question]`. Confirm the flag and the callout agree: a page flagged with no callout, or a callout with no flag, is a bookkeeping error. Then check whether any of them are now answerable.

**5. Orphans & missing links.** Pages with no inbound links: either they need linking from a hub page, or they need deleting. And the inverse: obvious cross-links that should exist and don't (a procedure that names gear without linking it).

**6. Drift traps.** Counts, dates, or rosters typed into prose that will silently go stale. Especially **derived-state lists**, any hand-typed list of open questions, verification status, or asset counts that a Base already derives. Replace with a link to the Base; never maintain a second copy.

**7. Placeholder leakage.** Literal `YYYY-MM-DD` or `[bracket]` placeholders left in real pages. `wiki/09-Templates/` is exempt.

## Reporting

Give the user a short report grouped by severity, not a wall of every finding:

- **Fixed**: what you changed mechanically, one line each
- **Needs a decision**: contradictions and SSOT collisions where you couldn't safely pick a winner
- **Needs a human**: pages due for re-verification, unsourced claims, open questions that are now stale

Then log the pass in `wiki/10-Log/<today>.md` and commit:

```bash
git add wiki/ && git commit -m "lint: <what you resolved>"
```

## Don't over-fix

A vault that gets aggressively normalized every few weeks loses the texture that makes it useful. Leave prose alone if it reads well. Leave a page's structure alone if it works. Fix drift, duplication, and untruth, not style.
