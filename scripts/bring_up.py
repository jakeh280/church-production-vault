#!/usr/bin/env python3
"""Surface time-sensitive items buried in the vault, the "bring-up" / tickler report.

This is the *data-gathering* half of the vault's proactive layer. It does NOT judge
or decide; it finds dates that a human (or the nightly Gemini pass) should look at:
deadlines, balances due, subscription renewals, quote expirations, end-of-life
warnings. The reasoning half, "so what should we DO about this?", is the model's
job (see System.md → "Proactive agent"). Scripts gather; the model reasons.

Read-only. Always exits 0 (it's a reporter, not a gate). Excludes 10-Log/ (history)
and inbox/.

What it scans:
  - Page BODIES for an actionable keyword (due / balance / renew / expire(s/d) /
    end-of-life / EOL / lamp life / warranty / deadline / payment) appearing on the
    same line as a parseable date, and buckets each by how soon: OVERDUE,
    within 30 days, within 90 days.

Usage:
  python3 scripts/bring_up.py            # default horizon 90 days
  python3 scripts/bring_up.py --days 60
"""
import re, sys, argparse
from datetime import date, datetime
from pathlib import Path

WIKI_ROOT = Path("wiki")
SKIP_DIRS = {WIKI_ROOT / "10-Log"}

KEYWORD_RE = re.compile(
    r"\b(due|balance|renew\w*|expir\w*|end[- ]of[- ]life|eol|lamp life|"
    r"warrant\w*|deadline|payment|invoice)\b",
    re.IGNORECASE,
)

# Date formats we attempt, most specific first.
MONTHS = ("january february march april may june july august september "
          "october november december").split()
MONTH_RE = "|".join(MONTHS) + "|" + "|".join(m[:3] for m in MONTHS)

DATE_PATTERNS = [
    # 2026-06-26  /  2026-6-26
    (re.compile(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b"),
     lambda m: date(int(m.group(1)), int(m.group(2)), int(m.group(3)))),
    # 6/26/2026  /  06/26/26
    (re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b"),
     lambda m: date(_yr(m.group(3)), int(m.group(1)), int(m.group(2)))),
    # June 26, 2026  /  Jun 26 2026
    (re.compile(rf"\b({MONTH_RE})\.?\s+(\d{{1,2}}),?\s+(\d{{4}})\b", re.IGNORECASE),
     lambda m: date(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))),
]


def _yr(s):
    n = int(s)
    return n if n > 99 else 2000 + n


def _mon(s):
    s = s.lower()[:3]
    return [m[:3] for m in MONTHS].index(s) + 1


def parse_dates(line):
    out = []
    for rx, fn in DATE_PATTERNS:
        for m in rx.finditer(line):
            try:
                out.append(fn(m))
            except (ValueError, IndexError):
                pass
    return out


def strip_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[(nl + 1) if nl != -1 else end + 4:]
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90, help="horizon in days (default 90)")
    args = ap.parse_args()

    today = date.today()
    overdue, soon, later = [], [], []

    for md in sorted(WIKI_ROOT.rglob("*.md")):
        if any(d in md.parents for d in SKIP_DIRS):
            continue
        body = strip_frontmatter(md.read_text(encoding="utf-8"))
        in_fence = False
        for line in body.splitlines():
            st = line.lstrip()
            if st.startswith("```") or st.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence or not KEYWORD_RE.search(line):
                continue
            for d in parse_dates(line):
                delta = (d - today).days
                item = (d, md.stem, line.strip())
                if delta < 0:
                    # Only recent overdue items: older than the horizon are almost
                    # always resolved/historical and would just add noise nightly.
                    if delta >= -args.days:
                        overdue.append(item)
                elif delta <= 30:
                    soon.append(item)
                elif delta <= args.days:
                    later.append(item)

    def show(title, items):
        if not items:
            return
        print(f"\n{title} ({len(items)})")
        for d, page, line in sorted(items):
            snippet = (line[:110] + "…") if len(line) > 110 else line
            print(f"  {d.isoformat()}  [[{page}]]")
            print(f"      {snippet}")

    print(f"── Bring-Up Report ── today {today.isoformat()}, horizon {args.days}d ──")
    show("⚠ OVERDUE", overdue)
    show("▲ Within 30 days", soon)
    show(f"• Within {args.days} days", later)
    if not (overdue or soon or later):
        print("\nNothing time-sensitive found in range.")
    sys.exit(0)


if __name__ == "__main__":
    main()
