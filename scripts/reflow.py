#!/usr/bin/env python3
"""Un-wrap hard-wrapped prose paragraphs into one continuous line per paragraph.

Earlier sessions hard-wrapped body text at ~80-90 columns, which Obsidian renders
as unwanted mid-paragraph breaks. This joins consecutive plain paragraph lines -
*including prose inside callouts / blockquotes*, while deliberately leaving
untouched:
  - frontmatter, fenced code blocks
  - headings (#), tables (|), lists (-, *, +, 1.)
  - callout header lines (> [!type] ...), blank callout separators (>)
  - horizontal rules, indented lines, image/embed lines
  - intentional two-space hard breaks and trailing-backslash breaks

Usage:
  python3 scripts/reflow.py            # check only (default); exits 1 if reflow needed
  python3 scripts/reflow.py --apply    # write the changes

Enforces the "no hard-wrapping prose" rule in CLAUDE.md. Conservative by design;
review `git diff` after --apply.
"""
import re, glob, sys

def is_boundary(s):
    """`s` is a line with any blockquote '>' prefix already stripped."""
    if s == "": return True
    if s[:1] in (" ", "\t"): return True
    if s[0] in "#|": return True
    if re.match(r'^\[!', s): return True          # callout header: [!type] ...
    if re.match(r'^[-*+] ', s): return True
    if re.match(r'^- \[', s): return True
    if re.match(r'^\d+\. ', s): return True
    if re.match(r'^[-*_]{3,}$', s): return True
    if s.startswith('!['): return True
    return False

def mergeable(s):
    if is_boundary(s): return False
    if s.endswith('  '): return False
    if s.rstrip().endswith('\\'): return False
    return True

def merge_lines(lines):
    """Join runs of mergeable prose lines; emit boundaries as-is."""
    out, buf = [], []
    def flush():
        if buf:
            out.append(" ".join(x.strip() for x in buf)); buf.clear()
    for L in lines:
        if mergeable(L):
            buf.append(L)
        else:
            flush(); out.append(L)
    flush()
    return out

def reflow_text(t):
    pre, body = "", t
    if t.startswith("---\n"):
        e = t.find("\n---", 4)
        if e != -1:
            nl = t.find("\n", e + 1)
            pre, body = t[:nl + 1], t[nl + 1:]
    lines = body.split("\n")
    out, fence, i, n = [], False, 0, len(lines)
    while i < n:
        L = lines[i]
        if L.lstrip().startswith("```"):
            fence = not fence; out.append(L); i += 1; continue
        if fence:
            out.append(L); i += 1; continue
        # Blockquote / callout block: reflow prose *within* the quote,
        # preserving the block's leading indentation (nested callouts).
        if L.lstrip().startswith(">"):
            indent = L[:len(L) - len(L.lstrip())]
            block = []
            while i < n and lines[i].lstrip().startswith(">"):
                block.append(lines[i]); i += 1
            inner = [re.sub(r'^\s*> ?', '', b) for b in block]
            out.extend(indent + (">" if m == "" else "> " + m) for m in merge_lines(inner))
            continue
        # Plain block: gather until a fence/blockquote, reflow within.
        block = []
        while i < n and not lines[i].lstrip().startswith(("```", ">")):
            block.append(lines[i]); i += 1
        out.extend(merge_lines(block))
    return pre + "\n".join(out)

def main():
    apply = "--apply" in sys.argv
    changed = []
    for f in sorted(glob.glob("wiki/**/*.md", recursive=True)):
        t = open(f, encoding="utf-8").read()
        new = reflow_text(t)
        if new != t:
            changed.append(f)
            if apply:
                open(f, "w", encoding="utf-8").write(new)
    verb = "Reflowed" if apply else "Would reflow"
    print(f"{verb} {len(changed)} file(s)")
    for c in changed:
        print("  ", c)
    sys.exit(0 if (apply or not changed) else 1)

if __name__ == "__main__":
    main()
