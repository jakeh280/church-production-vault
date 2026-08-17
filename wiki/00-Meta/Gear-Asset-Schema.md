---
title: Gear Asset Schema
type: meta
tags: [meta, reference, gear]
updated: 2026-08-16
status: active
source: template, distilled from CLAUDE.md
---
# Gear Asset Schema

Reference for creating and maintaining `type: gear-asset` pages in `01-Production/Gear-Assets/`. See [[Gear-Register]] for the aggregated Base view.

One page per item, or per identical batch. System-reference pages (the whole audio rig, the video routing chain) stay separate and describe the *system*; asset pages track individual *units* through their life.

## Frontmatter

```yaml
---
title: Wireless handheld TX (spare)
type: gear-asset
tags: [production, audio, gear]
asset: <model or short name>
manufacturer: <make>
category: audio            # audio / video / lighting / computer / other
status: spare              # in-service / spare / broken / retired
location: <where it physically is>
quantity: 1
acquired: YYYY-MM          # optional, month/year if known
cost:                      # optional, if known
updated: YYYY-MM-DD
needs_attention: false     # true = wants a human decision or action (type=checkbox)
status_note: ""
---
```

## `needs_attention`: a triage flag, not a health reading

`status` is the **lifecycle** state (in-service / spare / broken / retired). `needs_attention` is independent: it flags items that **want a human decision or action**, and it drives the [[Gear-Register]] "Needs Attention" view, the same pattern as `open_questions` → [[Open-Confirmations]].

- **`true`**, degraded *and* a decision or action is open: a discontinued fixture needing a replacement call, a pending lamp order. An item can be `status: in-service` **and** `needs_attention: true`, running, but not settled.
- **`false`**, either genuinely healthy, **or** a known issue that has been consciously triaged and accepted (e.g. "converter drops signal occasionally; power-cycle workaround accepted, not prioritized"). Record the reasoning in `status_note`, the issue stays documented, it just stops nagging the attention view.

**It is a condition flag, not a task tracker.** The *work* lives wherever the team tracks work; the *spend or repair* is a `type: gear-event` page. The asset page links to that work. It must never restate task status (assignee, due date, progress) or it duplicates a live system and drifts. Flip the flag to `false` when the decision lands; the gear-event preserves the history.

Gear being *deployed or moved* is project work, not `needs_attention`. The flag is for degraded units, not active installs.

## Body sections

- **Overview**: what it is, where it lives, its role in the system
- **Lifecycle**: purchase → deployment → changes, as dated entries. Append; never delete
- **Issue / troubleshooting log**: append dated entries; never delete
- **Links**: to the system gear page, the relevant procedures, and the manual

## SSOT: count and location

> [!warning] The asset page is the single source of truth for `quantity` and `location`.
> Never restate those values in census tables or gear-summary prose. Point at the asset page, or let [[Gear-Register]] aggregate them. A summary page may note *that* an item has spares; the *number* lives only here.

This is the most common drift trap in the whole vault. Two pages both saying "we have 4" is two pages that will disagree the day someone breaks one.

## Related: gear events

Purchases, repairs, service calls, and replacements are `type: gear-event` pages in `01-Production/Gear-Events/`, see [[Obsidian-Conventions]] for the frontmatter. They carry the queryable money and dates; the narrative stays in the asset's Lifecycle section. [[Gear-Spend-Register]] aggregates them.
