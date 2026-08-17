#!/usr/bin/env python3
"""Flag wiki pages that are overdue for re-verification.

Two buckets:
  A) Operational pages (type: procedure, gear, gear-asset, reference) with a
     BLANK or ABSENT verified: field → "never verified".
  B) Any wiki page with a verified: date older than N months (default 6).

Prints each flagged page as:
  path  (verified: DATE | blank)
sorted oldest-first (blank entries last within their bucket).

Usage:
  python3 scripts/staleness.py             # check; exits 1 if any flagged
  python3 scripts/staleness.py --months 3  # tighten the staleness window

Check-only (no --apply). Excludes inbox/, .git/, .obsidian/, scripts/.
"""
import re, sys, argparse
from pathlib import Path
from datetime import date, timedelta

WIKI_ROOT = Path("wiki")
OPERATIONAL_TYPES = {"procedure", "gear", "gear-asset", "reference"}
# Page templates carry operational types by design but describe nothing real.
# They are shapes to copy, so they never enter the re-verification queue.
TEMPLATES_DIR = WIKI_ROOT / "09-Templates"


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--months", type=int, default=6, help="Staleness threshold in months (default: 6)")
    return p.parse_args()


def strip_frontmatter_block(text):
    """Return the raw frontmatter string (between the --- markers), or ''."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[4:end + 1]
    return ""


def fm_value(fm, key):
    """Extract a scalar frontmatter value by key, or None."""
    m = re.search(rf'^{re.escape(key)}:\s*(.+?)\s*$', fm, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def parse_date(s):
    """Parse YYYY-MM-DD, return date or None."""
    if not s:
        return None
    m = re.match(r'(\d{4}-\d{2}-\d{2})', s)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            pass
    return None


def months_ago(n, today=None):
    """Return the date that is n months before today."""
    if today is None:
        today = date.today()
    # Approximate: subtract n*30 days (close enough for a lint nudge)
    return today - timedelta(days=n * 30)


def main():
    args = parse_args()
    today = date.today()
    cutoff = months_ago(args.months, today)

    never_verified = []   # (path, page_type), bucket A
    stale = []            # (path, verified_date), bucket B

    for md in sorted(WIKI_ROOT.rglob("*.md")):
        if TEMPLATES_DIR in md.parents:
            continue
        text = md.read_text(encoding="utf-8")
        fm = strip_frontmatter_block(text)
        if not fm:
            continue

        page_type = fm_value(fm, "type") or ""
        verified_raw = fm_value(fm, "verified")

        # live_doc pages are excluded from verification entirely
        live_doc = fm_value(fm, "live_doc")
        if live_doc and live_doc.lower() in ("true", "yes"):
            continue

        verified_date = parse_date(verified_raw)

        # Bucket A: operational with no verification date
        if page_type.lower() in OPERATIONAL_TYPES and not verified_date:
            never_verified.append((str(md), page_type))

        # Bucket B: any page with a verified date that's too old
        if verified_date and verified_date < cutoff:
            stale.append((str(md), verified_date))

    # Sort bucket B oldest-first
    stale.sort(key=lambda x: x[1])

    flagged = len(never_verified) + len(stale)

    if never_verified:
        print(f"\n=== Bucket A: Operational pages never verified ({len(never_verified)}) ===")
        for path, ptype in sorted(never_verified):
            print(f"  {path}  (type: {ptype}, verified: blank)")

    if stale:
        print(f"\n=== Bucket B: Verified > {args.months} months ago ({len(stale)}) ===")
        for path, vdate in stale:
            print(f"  {path}  (verified: {vdate})")

    if not flagged:
        print(f"No staleness issues found (threshold: {args.months} months).")

    print(f"\nTotal flagged: {flagged}")
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
