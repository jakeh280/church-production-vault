---
title: Obsidian Conventions (House Style)
type: meta
tags: [meta, reference]
updated: 2026-08-16
status: active
source: template, house style / project meta
---
# Obsidian Conventions (House Style)

How this vault uses Obsidian features, so the agent and any human editor stay consistent.

> [!info] You don't need Obsidian to use this vault
> Every file is plain Markdown and works in any editor. Obsidian is what makes the wikilinks clickable, the callouts render, the graph view work, and the `.base` files show up as sortable tables. **Bases require Obsidian 1.9.10 or newer**, 1.10+ is recommended. Without Obsidian the vault still functions; the `.base` files just sit there as inert YAML.

## Properties (frontmatter)

Every file carries the frontmatter defined in `CLAUDE.md`. Property types Obsidian recognizes:

- **text**: single line (URLs and links must be quoted)
- **list**: `tags:` and similar, one `- value` per line
- **number**: literal only, no expressions
- **checkbox**: `true` / `false`
- **date**, `YYYY-MM-DD` · **datetime**, `YYYY-MM-DDTHH:MM:SS`

Keep `updated:` and `verified:` as `date`. One property name per note, no duplicates.

> [!tip] Frontmatter that won't break Obsidian
> Quote any property value containing a `[[wikilink]]` or a `colon-space`, e.g. `vendor: "[[Riverbend-AV]]"`, `source: "Chris (verbal) re: lamp box"`. A raw `[[` reads as a YAML list and `: ` as a nested key, both of which flag the page's properties as invalid. `python3 scripts/fm_fix.py --apply` fixes these in bulk.

## Callouts (use these, not plain blockquotes)

Syntax: `> [!type] Optional Title`, then `>` lines for the body. Add `+` (expanded) or `-` (collapsed) to make it foldable.

House usage:

- `> [!warning]`: unverified high-stakes content, or a flagged contradiction
- `> [!question]`: an unconfirmed claim; pair it with `open_questions: true`
- `> [!tip]`: posted station reminder cards
- `> [!info]`: context and notes
- `> [!quote]`: verbatim call-outs
- `> [!example]`: worked examples

Built-in types: note, abstract/summary/tldr, info, todo, tip/hint/important, success/check/done, question/help/faq, warning/caution/attention, failure/fail/missing, danger/error, bug, example, quote/cite.

```markdown
> [!warning] Not yet verified
> Confirm before relying on this live.

> [!question] To confirm
> Cam 3 transmitter brand, not yet sourced.
```

**Callout bodies are not hard-wrapped.** Each prose paragraph inside a callout is one continuous `> …` line. See the no-hard-wrap rule in `CLAUDE.md`.

## Bases (`.base` files)

Native database views over frontmatter. Structure: `filters`, `formulas`, `properties` (display names), `views`. Filter functions include `file.hasTag()`, `file.hasLink()`, `file.inFolder(path)`; operators `==` `!=` `>` `<` `>=` `<=` and `&&` `||` `!`.

Bases live in `wiki/08-Bases/`. This vault ships five: [[Gear-Register]], [[Gear-Spend-Register]], [[Open-Confirmations]], [[Verification-Dashboard]], [[Log]].

**Syntax gotchas, learned the hard way:**

- `file.inFolder("wiki/01-Production")`, the path must include the `wiki/` prefix. **No second argument**, `, true` does not work and breaks the filter. `inFolder` is recursive by default.
- **Boolean fields:** use `== true` / `!= true`, not `.isEmpty()`, which throws a type error on booleans. Example: `live_doc != true` excludes pointer pages.
- **Date fields:** `.isEmpty()` works when set through the UI filter builder; hand-editing raw `.base` YAML may need the UI to re-serialize. When in doubt, set filters interactively in Obsidian rather than editing the YAML.
- Formulas are fine with `.isEmpty()` on date properties: `if(note.verified.isEmpty(), "⚠️ UNVERIFIED", "✅ " + note.verified)`.
- A filter line beginning with `!` must be quoted in YAML: `- '!file.inFolder("wiki/09-Templates")'`.

```yaml
filters:
  and:
    - file.inFolder("wiki/01-Production")
    - live_doc != true
views:
  - type: table
    name: Procedures
    order:
      - file.name
      - note.verified
```

**If you rename or renumber a folder, update the Base filters in the same edit.** `Verification-Dashboard.base` and `Log.base` both filter on a hardcoded path, and a stale filter fails silently. The view just shows nothing.

## Gear events: spend & service log

Every time money is spent on gear, a **purchase** *or* a **repair / service / replacement**, create a `type: gear-event` page in `01-Production/Gear-Events/`, filename `YYYY-MM-DD-Short-Title.md`. Frontmatter: `kind` (purchase / service / repair / replace), `date`, `cost`, `vendor`, `asset` (a wikilink to the gear-asset page if one exists).

The event page holds the **queryable money and date**; the **narrative** of what happened stays in the asset page's `## Lifecycle` section. Don't duplicate the prose. Link. [[Gear-Spend-Register]] aggregates all events chronologically, and answers both "what did we spend on gear this year" and "what's this unit's full service history" from one source.

## Canvas

`wiki/07-Canvas/` holds Obsidian `.canvas` files: the right tool for signal flow, rack layouts, and room diagrams, where a picture genuinely beats a paragraph. Canvas nodes can embed wiki pages, so a signal-flow canvas can link straight to the gear page for each box. `scripts/link_check.py` parses `.canvas` files for links, so canvas references count toward the link graph.
