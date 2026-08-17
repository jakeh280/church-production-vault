#!/usr/bin/env python3
"""Frontmatter YAML safety: quote property values that break Obsidian's parser.

Obsidian frequently writes values that aren't valid YAML scalars:
  - values containing a [[wikilink]]  -> YAML reads `[[` as a nested flow sequence
  - values containing a `colon: space` -> YAML reads it as a nested mapping key
Both flag the page's Properties as invalid. This wraps exactly those values in
double quotes (escaping internal quotes), leaving everything else untouched.

Usage:
  python3 scripts/fm_fix.py            # check only (default); exits 1 if fixes needed
  python3 scripts/fm_fix.py --apply    # write the fixes

Safe to re-run (idempotent). Pairs with the "no hard-wrap" rule in CLAUDE.md.
"""
import re, glob, sys

def main():
    apply = "--apply" in sys.argv
    changed = []
    for f in sorted(glob.glob("wiki/**/*.md", recursive=True)):
        t = open(f, encoding="utf-8").read()
        if not t.startswith("---\n"):
            continue
        end = t.find("\n---", 4)
        if end == -1:
            continue
        fm, rest = t[4:end + 1], t[end + 1:]
        out, file_changed = [], False
        for ln in fm.split("\n"):
            m = re.match(r'^([A-Za-z_][\w-]*):[ \t](.+?)[ \t]*$', ln)
            if not m:
                out.append(ln); continue
            key, val = m.group(1), m.group(2)
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                out.append(ln); continue
            if ('[[' in val) or (re.search(r':[ \t]', val) is not None):
                esc = val.replace('\\', '\\\\').replace('"', '\\"')
                out.append(f'{key}: "{esc}"'); file_changed = True
            else:
                out.append(ln)
        if file_changed:
            changed.append(f)
            if apply:
                open(f, "w", encoding="utf-8").write("---\n" + "\n".join(out) + rest)
    verb = "Fixed" if apply else "Would fix"
    print(f"{verb} {len(changed)} file(s) with unsafe frontmatter:")
    for c in changed:
        print("  ", c)
    sys.exit(0 if (apply or not changed) else 1)

if __name__ == "__main__":
    main()
