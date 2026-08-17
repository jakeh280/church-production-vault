#!/usr/bin/env python3
"""Check for unresolved wikilinks in wiki page bodies.

Scans every wiki page BODY (frontmatter excluded) for [[wikilinks]] and
![[embeds]]. A link target resolves if it matches (case-insensitively):
  - the basename (no .md) of any wiki page, OR
  - any alias listed in a page's frontmatter aliases: list, OR
  - the basename of any .base file in wiki/08-Bases/.

Unresolved targets are printed with file path, line number, and a suggestion
via difflib when a close match exists among known names.

Usage:
  python3 scripts/link_check.py          # check only; exits 1 if unresolved found
  python3 scripts/link_check.py --help

Check-only (no --apply). Excludes inbox/, .git/, .obsidian/, scripts/, 09-Templates/, and the
append-only 10-Log/ folder (historical record, see LOG_DIR note below).
"""
import re, sys, difflib
from pathlib import Path

WIKI_ROOT = Path("wiki")
BASES_DIR = WIKI_ROOT / "08-Bases"
# Append-only daily logs are a historical record: they legitimately reference pages
# that were later renamed, deleted, or are still planned. Those are not broken links
# to fix, so logs still contribute to the known-name set (links TO a log resolve),
# but we don't *report* unresolved links found inside them.
LOG_DIR = WIKI_ROOT / "10-Log"
# Page templates legitimately contain placeholder links like [[Owning-Gear-Page]].
# They are shapes to copy, not real pages, so we do not report links found in them.
TEMPLATES_DIR = WIKI_ROOT / "09-Templates"

# Matches [[Target]], [[Target#Section]], [[Target|Display]], ![[Target#heading]]
WIKILINK_RE = re.compile(r'!?\[\[([^\]]+)\]\]')
# Inline code span: stripped before link scanning so `[[wikilink]]` shown as a
# documentation example is not treated as a real link.
INLINE_CODE_RE = re.compile(r'`[^`]*`')


def strip_frontmatter(text):
    """Return (frontmatter_text, body_text). Body starts after closing ---."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            nl = text.find("\n", end + 1)
            body_start = nl + 1 if nl != -1 else end + 4
            return text[:body_start], text[body_start:]
    return "", text


def parse_aliases(frontmatter):
    """Extract alias strings from a frontmatter block."""
    aliases = []
    # Match  aliases: [a, b, c]  or  aliases:\n  - a\n  - b
    block_m = re.search(r'^aliases:\s*\[([^\]]*)\]', frontmatter, re.MULTILINE)
    if block_m:
        for part in block_m.group(1).split(","):
            s = part.strip().strip('"').strip("'")
            if s:
                aliases.append(s)
    list_m = re.findall(r'^aliases:\s*$((?:\n[ \t]*-[^\n]+)+)', frontmatter, re.MULTILINE)
    for block in list_m:
        for item in re.findall(r'-\s*(.+)', block):
            s = item.strip().strip('"').strip("'")
            if s:
                aliases.append(s)
    return aliases


def collect_known_names():
    """Return a set of lower-cased known resolvable names."""
    known = set()
    for md in WIKI_ROOT.rglob("*.md"):
        known.add(md.stem.lower())
        text = md.read_text(encoding="utf-8")
        fm, _ = strip_frontmatter(text)
        for alias in parse_aliases(fm):
            known.add(alias.lower())
    if BASES_DIR.exists():
        for base in BASES_DIR.glob("*.base"):
            known.add(base.stem.lower())
    # Canvas files are valid link targets too (e.g. [[Production-System-Overview]]).
    for canvas in WIKI_ROOT.rglob("*.canvas"):
        known.add(canvas.stem.lower())
    return known


def extract_link_target(raw):
    """From [[raw]] content, extract the page name (before # or |).

    Obsidian requires the alias pipe to be escaped as ``\\|`` inside a Markdown
    table cell (an unescaped ``|`` would close the cell). Normalize that back to
    a plain pipe first, so a table-escaped aliased link like ``[[Page\\|Alias]]``
    resolves exactly as ``[[Page|Alias]]`` would in body prose, otherwise the
    split leaves a trailing backslash on the target and reports a false positive.
    """
    # Strip leading ! for embeds: already stripped before we get here
    raw = raw.replace("\\|", "|")
    target = raw.split("#")[0].split("|")[0].strip()
    return target


def main():
    known = collect_known_names()
    known_list = sorted(known)  # stable list for difflib

    unresolved = []  # list of (path, lineno, target, suggestions)

    for md in sorted(WIKI_ROOT.rglob("*.md")):
        if LOG_DIR in md.parents:
            continue  # append-only logs, historical record, not a fix queue
        if TEMPLATES_DIR in md.parents:
            continue  # templates hold placeholder links, not real ones
        text = md.read_text(encoding="utf-8")
        fm, body = strip_frontmatter(text)
        fm_lines = fm.count("\n") + (1 if fm else 0)

        in_fence = False
        for lineno_body, line in enumerate(body.splitlines(), start=1):
            lineno = fm_lines + lineno_body
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            scan_line = INLINE_CODE_RE.sub("", line)
            for m in WIKILINK_RE.finditer(scan_line):
                raw = m.group(1)
                target = extract_link_target(raw)
                if not target:
                    continue
                if target.lower() in known:
                    continue
                # Unresolved: look for close matches
                suggestions = difflib.get_close_matches(
                    target.lower(), known_list, n=2, cutoff=0.6
                )
                unresolved.append((str(md), lineno, target, suggestions))

    if unresolved:
        print(f"Unresolved wikilinks: {len(unresolved)}")
        for path, lineno, target, suggestions in unresolved:
            print(f"  {path}:{lineno}  [[{target}]]")
            for s in suggestions:
                print(f"      → did you mean [[{s}]]?")
    else:
        print("All wikilinks resolved.")

    sys.exit(1 if unresolved else 0)


if __name__ == "__main__":
    main()
