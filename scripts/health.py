#!/usr/bin/env python3
"""Vault health metrics, emit JSON to stdout, human summary to stderr.

Metrics (flat JSON, stable keys):
  total_pages. All wiki/*.md files
  with_source, pages that have a non-empty source: field
  operational_missing_source, type in {procedure,gear,gear-asset,reference}
                              AND source blank/absent
  verified_count, pages with a non-empty verified: date
  operational_unverified, operational pages with blank/absent verified:
                            (same as staleness.py bucket A)
  stale_over_6mo, pages with verified: date older than 6 months
  open_questions, pages with open_questions: true (as boolean or
                            string "true")
  unresolved_links, count of unresolved [[wikilink]] targets in bodies
  orphans, wiki pages with zero inbound body-wikilinks from
                            OTHER wiki pages; excludes 00-Meta, 10-Log, index.md

Usage:
  python3 scripts/health.py              # JSON to stdout, summary to stderr
  python3 scripts/health.py | jq .       # pretty-print metrics

Always exits 0 (reporter, not a gate).
"""
import re, sys, json
from pathlib import Path
from datetime import date, timedelta

WIKI_ROOT = Path("wiki")
HISTORY_FILE = WIKI_ROOT / "00-Meta" / "health-history.jsonl"
BASES_DIR = WIKI_ROOT / "08-Bases"
OPERATIONAL_TYPES = {"procedure", "gear", "gear-asset", "reference"}
ORPHAN_EXCLUDE_DIRS = {"00-Meta", "10-Log"}
# Templates are shapes to copy, not vault content: excluded from every metric.
TEMPLATES_DIR = WIKI_ROOT / "09-Templates"
ORPHAN_EXCLUDE_FILES = {"index.md"}

# ── shared helpers ──────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r'!?\[\[([^\]]+)\]\]')
INLINE_CODE_RE = re.compile(r'`[^`]*`')


def strip_frontmatter(text):
    """Return (fm_text, body_text)."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            nl = text.find("\n", end + 1)
            body_start = nl + 1 if nl != -1 else end + 4
            return text[:body_start], text[body_start:]
    return "", text


def fm_block(text):
    """Return raw frontmatter block string (between --- markers)."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[4:end + 1]
    return ""


def fm_value(fm, key):
    m = re.search(rf'^{re.escape(key)}:\s*(.+?)\s*$', fm, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def parse_date(s):
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
    today = today or date.today()
    return today - timedelta(days=n * 30)


def parse_aliases(fm):
    aliases = []
    block_m = re.search(r'^aliases:\s*\[([^\]]*)\]', fm, re.MULTILINE)
    if block_m:
        for part in block_m.group(1).split(","):
            s = part.strip().strip('"').strip("'")
            if s:
                aliases.append(s)
    list_m = re.findall(r'^aliases:\s*$((?:\n[ \t]*-[^\n]+)+)', fm, re.MULTILINE)
    for block in list_m:
        for item in re.findall(r'-\s*(.+)', block):
            s = item.strip().strip('"').strip("'")
            if s:
                aliases.append(s)
    return aliases


def collect_known_names():
    known = set()
    for md in WIKI_ROOT.rglob("*.md"):
        known.add(md.stem.lower())
        fm = fm_block(md.read_text(encoding="utf-8"))
        for alias in parse_aliases(fm):
            known.add(alias.lower())
    if BASES_DIR.exists():
        for base in BASES_DIR.glob("*.base"):
            known.add(base.stem.lower())
    for canvas in WIKI_ROOT.rglob("*.canvas"):
        known.add(canvas.stem.lower())
    return known


def link_target(raw):
    # Normalize the table-escaped alias pipe (\|) before splitting, matching
    # link_check.py: otherwise a [[Page\|Alias]] in a table is miscounted as
    # unresolved (trailing backslash left on the target).
    raw = raw.replace("\\|", "|")
    return raw.split("#")[0].split("|")[0].strip()


# ── metric collection ────────────────────────────────────────────────────────

def collect_metrics():
    today = date.today()
    cutoff_6mo = months_ago(6, today)

    all_pages = sorted(p for p in WIKI_ROOT.rglob("*.md") if TEMPLATES_DIR not in p.parents)
    known_names = collect_known_names()

    total_pages = len(all_pages)
    with_source = 0
    operational_missing_source = 0
    verified_count = 0
    operational_unverified = 0
    stale_over_6mo = 0
    open_questions = 0

    # For orphan detection: build inbound-link map keyed by lower stem
    inbound = {md.stem.lower(): set() for md in all_pages}
    # Also collect unresolved links while we walk
    unresolved_count = 0

    page_data = []  # (md, fm_str, body_str)
    for md in all_pages:
        text = md.read_text(encoding="utf-8")
        fm = fm_block(text)
        _, body = strip_frontmatter(text)
        page_data.append((md, fm, body))

    for md, fm, body in page_data:
        page_type = (fm_value(fm, "type") or "").lower()
        source_val = fm_value(fm, "source")
        verified_raw = fm_value(fm, "verified")
        oq_raw = fm_value(fm, "open_questions")
        live_doc = fm_value(fm, "live_doc")

        is_live = live_doc and live_doc.lower() in ("true", "yes")
        is_operational = page_type in OPERATIONAL_TYPES

        # source
        if source_val:
            with_source += 1
        if is_operational and not source_val:
            operational_missing_source += 1

        # verified
        verified_date = parse_date(verified_raw)
        if not is_live:
            if verified_date:
                verified_count += 1
                if verified_date < cutoff_6mo:
                    stale_over_6mo += 1
            if is_operational and not verified_date:
                operational_unverified += 1

        # open_questions
        if oq_raw and oq_raw.lower() in ("true", "yes"):
            open_questions += 1

        # links: build inbound map + count unresolved (skip code blocks/spans).
        # Append-only logs legitimately link to renamed/deleted/planned pages,
        # those are not defects, so (like link_check.py) we don't count unresolved
        # found inside 10-Log/, though log links still count as inbound elsewhere.
        is_log = (WIKI_ROOT / "10-Log") in md.parents
        in_fence = False
        for lineno, line in enumerate(body.splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in WIKILINK_RE.finditer(INLINE_CODE_RE.sub("", line)):
                raw = m.group(1)
                tgt = link_target(raw)
                if not tgt:
                    continue
                tgt_lower = tgt.lower()
                if tgt_lower in known_names:
                    # record inbound link
                    if tgt_lower in inbound:
                        inbound[tgt_lower].add(md.stem.lower())
                elif not is_log:
                    unresolved_count += 1

    # Orphans: pages with zero inbound links, excluding exempt dirs/files
    orphan_count = 0
    for md in all_pages:
        # Exclude by parent folder name
        parts = md.parts
        if any(p in ORPHAN_EXCLUDE_DIRS for p in parts):
            continue
        if md.name in ORPHAN_EXCLUDE_FILES:
            continue
        stem = md.stem.lower()
        others = inbound.get(stem, set()) - {stem}  # exclude self-links
        if not others:
            orphan_count += 1

    return {
        "total_pages": total_pages,
        "with_source": with_source,
        "operational_missing_source": operational_missing_source,
        "verified_count": verified_count,
        "operational_unverified": operational_unverified,
        "stale_over_6mo": stale_over_6mo,
        "open_questions": open_questions,
        "unresolved_links": unresolved_count,
        "orphans": orphan_count,
    }


def record_history(metrics):
    """Append today's metrics as one JSON line to the trend history, and return
    the previous entry (or None) so the caller can show deltas. Idempotent per
    day: a second run on the same date overwrites that day's line rather than
    duplicating it, so the digest can run safely more than once."""
    entry = {"date": date.today().isoformat(), **metrics}
    prev = None
    rows = []
    if HISTORY_FILE.exists():
        for ln in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            try:
                row = json.loads(ln)
            except json.JSONDecodeError:
                continue
            if row.get("date") == entry["date"]:
                continue  # drop a same-day prior run; we re-append below
            rows.append(row)
    if rows:
        prev = rows[-1]
    rows.append(entry)
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8"
    )
    return prev


def main():
    record = "--record" in sys.argv[1:]
    metrics = collect_metrics()
    print(json.dumps(metrics, indent=2))

    prev = record_history(metrics) if record else None

    # Human summary to stderr
    lines = [
        "── Vault Health ──────────────────────────────────",
        f"  Pages total:                {metrics['total_pages']}",
        f"  With source:                {metrics['with_source']}  ({metrics['total_pages'] - metrics['with_source']} missing)",
        f"  Operational missing source: {metrics['operational_missing_source']}",
        f"  Verified pages:             {metrics['verified_count']}",
        f"  Operational unverified:     {metrics['operational_unverified']}",
        f"  Stale (> 6 mo):             {metrics['stale_over_6mo']}",
        f"  Open questions:             {metrics['open_questions']}",
        f"  Unresolved links:           {metrics['unresolved_links']}",
        f"  Orphans:                    {metrics['orphans']}",
        "──────────────────────────────────────────────────",
    ]
    if prev:
        def d(k):
            delta = metrics[k] - prev.get(k, metrics[k])
            return f" ({'+' if delta >= 0 else ''}{delta} since {prev['date']})" if delta else ""
        lines.append(f"  Trend: pages{d('total_pages')} · verified{d('verified_count')} · "
                     f"open-q{d('open_questions')} · unverified{d('operational_unverified')}")
        lines.append("──────────────────────────────────────────────────")
    sys.stderr.write("\n".join(lines) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
