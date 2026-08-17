---
title: Wiki Index
type: meta
tags: [meta]
updated: 2026-08-16
status: active
source: agent-maintained catalog
---
# Wiki Index

**Read this first on every query** to locate the relevant pages. **Update it on every ingest**. A page that isn't listed here is invisible to future questions.

One row per page: the link, a one-line summary of what's actually on it, and the type. Summary lines are exempt from the SSOT value-collision rule; everything else on this page is not.

---

## 00-Meta: how the vault works

| Page | Summary | Type |
|------|---------|------|
| [[System]] | The vault's memory of itself: architecture, integrations, approval gate, structural decisions, open work | meta |
| [[Team-Structure]] | Roles and reporting lines. No personnel detail, ever | meta |
| [[Obsidian-Conventions]] | House style, properties, callouts, Bases syntax and its gotchas, gear-event convention, canvas | reference |
| [[Gear-Asset-Schema]] | Frontmatter and body conventions for `type: gear-asset` pages; the `needs_attention` triage rule | reference |
| [[Maintenance-Scripts]] | What each script in `scripts/` does, and the pre-commit guard | reference |

## 08-Bases: derived views (never hand-maintained)

| Base | Shows |
|------|-------|
| [[Gear-Register]] | Every `gear-asset`, full register, needs-attention, broken, spares, active |
| [[Gear-Spend-Register]] | Every `gear-event`, purchases, service, repairs, with cost and vendor |
| [[Open-Confirmations]] | Every page flagged `open_questions: true` |
| [[Verification-Dashboard]] | Operational pages by verification state; excludes `live_doc` pointers |
| [[Log]] | Every daily log file, chronologically |

## 09-Templates

Page shapes to copy, see [[_README]]. Excluded from every Base and from link checking.

---

## Example content: delete all of this during setup

> [!warning] Fictional, and it must not survive setup
> Every page below describes a **made-up church (Northgate Church, Springfield)**. It ships with the template so the conventions are visible by imitation rather than only described. None of it is real, none of it is verified, and leaving it in place is how a fictional vendor ends up in a real purchase conversation six months from now. The setup interview deletes these files and rewrites this index.

| Page | Summary | Type |
|------|---------|------|
| [[Audio-System]] | Auditorium audio rig; the post-fader stream matrix and why it matters | gear |
| [[Handheld-Wireless-TX]] | Four handheld transmitters; one faulty, flagged `needs_attention` | gear-asset |
| [[2026-03-02-Console-Firmware-Service]] | Firmware service call under the vendor agreement, no charge | gear-event |
| [[Sunday-Startup]] | Weekend runbook for whoever is first in the booth | procedure |
| [[No-Audio-In-Stream]] | The most common stream failure and its real cause | troubleshooting |
| [[Weekly-Patch-Sheet]] | Live-doc pointer, the sheet lives in the shared drive, not here | reference |
| [[Riverbend-AV]] | Integrator who installed and services the audio system | vendor |
| [[2026-08-04-Production-Team-Sync]] | Team sync, handheld fault, stream audio incidents, two decisions | meeting |
| [[2026-08-04]] | A day of log entries, showing the format | log |

---

## How to keep this index useful

Write the summary for someone deciding **whether to open the page**, not for someone who already knows what's on it. "Auditorium audio rig; the post-fader stream matrix and why it matters" tells you when to click. "Audio system page" does not.

When a page's purpose changes, change its row. An index that describes what a page used to be is worse than no index.
