---
title: Templates
type: meta
tags: [meta]
updated: 2026-08-16
status: active
source: template
---
# Templates

Page shapes to copy when creating new notes. **Copy them, don't edit them in place.**

This folder is excluded from every `.base` view and from `link_check.py`, so the placeholder frontmatter and placeholder `[[links]]` in here never pollute the real vault.

| Template | Use for |
|----------|---------|
| `_Gear-System.md` | A system or subsystem, the audio rig, the video chain, the lighting setup |
| `_Gear-Asset.md` | One individual unit (or one identical batch) tracked through its life |
| `_Gear-Event.md` | A purchase, repair, service call, or replacement |
| `_Procedure.md` | A step-by-step runbook someone follows live |
| `_Troubleshooting.md` | A known problem and its fix |
| `_Vendor.md` | An integrator, rental house, repair shop, or service contact |
| `_Meeting-Summary.md` | Meeting notes, filename `YYYY-MM-DD-Short-Title.md` |
| `_Event.md` | A one-off or annual event, Christmas, Easter, a conference |
| `_Live-Doc-Pointer.md` | Something that changes weekly and lives in another system |
| `_Log-Day.md` | A daily log file, one per day, append only |

Every template leaves `verified:` blank on purpose. A page is unverified until a human confirms it against reality.
