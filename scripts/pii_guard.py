#!/usr/bin/env python3
"""PII / secret scanner, designed to run as a git pre-commit hook.

By default scans only STAGED files (git diff --cached). Use --all to scan
all of wiki/ and inbox/. Flags lines that look like ACTUAL SECRET VALUES,
not descriptive prose (the bare word in prose is fine; an actual assigned
value is not).  pii-guard-ok

Patterns flagged:
  - key=value pairs: password/secret/token/api_key/client_secret followed by
    an actual value (not just the word "blank", "stripped", "rotated", etc.)
  - US Social Security Numbers: NNN-NN-NNNN
  - PEM private key headers
  - AWS access key IDs (AKIA...)
  - Bearer / JWT-ish long base64url tokens (eyJ...)
  - salary followed by a numeric amount or $ sign

Suppression: any line containing  pii-guard-ok  is skipped.

Usage:
  python3 scripts/pii_guard.py            # scan staged files (pre-commit mode)
  python3 scripts/pii_guard.py --all      # scan all wiki/ and inbox/
  python3 scripts/pii_guard.py --install-hook  # write .git/hooks/pre-commit

Exit 1 if any hit (blocks commit), else 0.
"""
import re, sys, subprocess, argparse
from pathlib import Path

VAULT_ROOT = Path(".")
SCAN_DIRS = ["wiki", "inbox"]

# Patterns that indicate the value is descriptive prose, not an actual secret.
# A value that matches ANY of these is skipped.
PROSE_VALUE_RE = re.compile(
    r'^(blank|empty|stripped|removed|rotated|redacted|none|n/?a|tbd|see|not|'
    r'confirm|here|above|below|omitted|placeholder|stored|ask|contact|check|'
    r'pending|unknown|set|use|via|required|configured|enabled|disabled|'
    r'default|yes|no|managed|protected|secured|unset|hidden|private|public|'
    r'\[.*\]|<.*>)$',
    re.IGNORECASE
)


def looks_like_secret(value):
    """Return True if the captured value looks like an actual secret, not prose.

    Safety-gate posture: flag unless the value is *clearly* descriptive prose
    (PROSE_VALUE_RE) or a markdown link/emphasis token. We deliberately do NOT
    exempt short pure-alpha values, a weak credential like a one-word
    passphrase must still trip the gate. False positives are cheap (suppress with the
    `pii-guard-ok` marker); a missed credential reaching a cloud repo is not.
    """
    v = value.strip().strip('*_`"\'.,;')
    if not v:
        return False
    if PROSE_VALUE_RE.match(v):
        return False
    # Markdown link to an external doc (e.g. `[sheet](https://…)`) is not a secret.
    if v.startswith('[') or v.startswith('('):
        return False
    return True


PATTERNS = [
    (
        "credential key=value",
        re.compile(
            r'(?:password|passwd|pwd|secret|token|api[_-]?key|client[_-]?secret)'
            r'\s*[:=]\s*(\S+)',
            re.IGNORECASE
        ),
        lambda m: looks_like_secret(m.group(1)),
    ),
    (
        "SSN",
        re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        None,
    ),
    (
        "private key header",
        re.compile(r'-----BEGIN .*PRIVATE KEY-----'),  # pii-guard-ok (self-match)
        None,
    ),
    (
        "AWS access key",
        re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
        None,
    ),
    (
        "JWT/bearer token",
        re.compile(r'\beyJ[A-Za-z0-9_-]{20,}'),
        None,
    ),
    (
        "salary amount",
        re.compile(r'\bsalary\b.*?(\$[\d,]+|\d[\d,]+\s*(?:k\b|per\s+year|\/yr))', re.IGNORECASE),
        None,
    ),
]

SUPPRESS_MARKER = "pii-guard-ok"


def is_text_file(path):
    """Binary-vs-text heuristic: a NUL byte in the first chunk means binary.

    This is git's own classifier. We deliberately do NOT decode a fixed-size
    byte slice as UTF-8, slicing at a fixed offset can split a multibyte
    character and falsely flag a valid UTF-8 file as binary (which, since the
    pre-commit binary gate relies on this, would wrongly block a legit commit).
    PDFs/PNGs/XLSX contain NUL bytes; UTF-8 markdown does not.
    """
    try:
        chunk = path.read_bytes()[:8192]
    except OSError:
        return False
    return b"\x00" not in chunk


def staged_files():
    """Return list of Path objects for staged text files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        return []
    paths = []
    for line in result.stdout.splitlines():
        p = Path(line)
        if p.exists() and is_text_file(p):
            paths.append(p)
    return paths


def staged_binary_files():
    """Return staged (added/copied/modified) files that are NOT text.

    The text scanner cannot see inside a PDF/PNG/XLSX, so a binary added to a
    commit gets *silently skipped*, which is exactly how vendor invoice PDFs
    once reached the remote unscanned. In pre-commit mode we therefore BLOCK any
    staged binary outright: source binaries belong in inbox/ (gitignored) or in
    their native system, not in the versioned vault. Escape hatch for a genuine
    exception: `git commit --no-verify`.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        return []
    binaries = []
    for line in result.stdout.splitlines():
        p = Path(line)
        if p.exists() and not is_text_file(p):
            binaries.append(p)
    return binaries


def all_scan_files():
    paths = []
    for d in SCAN_DIRS:
        for p in Path(d).rglob("*"):
            if p.is_file() and is_text_file(p):
                paths.append(p)
    return paths


def scan_file(path):
    """Return list of (lineno, reason, line_text) for hits."""
    hits = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return hits
    for lineno, line in enumerate(lines, start=1):
        if SUPPRESS_MARKER in line:
            continue
        for reason, pattern, validator in PATTERNS:
            m = pattern.search(line)
            if m:
                if validator is not None and not validator(m):
                    continue
                hits.append((lineno, reason, line.rstrip()))
                break  # one reason per line is enough
    return hits


def in_git_repo():
    """True if cwd is inside a git work tree. A downloaded vault is not."""
    return subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True).returncode == 0


def install_hook():
    """Install the pre-commit hook so it TRAVELS with the repo.

    The hook script lives in tracked scripts/git-hooks/ (so a fresh clone, e.g.
    the iMac, already has the file), and we point git at it via core.hooksPath.
    Because core.hooksPath is local config (not cloned), a new machine still runs
    this once during bring-up: `python3 scripts/pii_guard.py --install-hook`.

    A vault that was downloaded rather than cloned has no repo at all. Writing the
    hook file there and reporting success would be a lie: core.hooksPath never gets
    set, and the guard is silently absent the day the user finally runs `git init`.
    Refuse instead, and say what to do.
    """
    if not in_git_repo():
        print(
            "Not a git repository, so there is no pre-commit stage to guard.\n"
            "This is fine: a downloaded vault works without git. Nothing leaves\n"
            "your machine, because nothing is being committed or synced.\n"
            "If you want version history and a private backup, run `git init`\n"
            "here first, then run this command again."
        )
        return False

    hooks_dir = Path("scripts/git-hooks")
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "pre-commit"
    hook_path.write_text(
        "#!/bin/sh\n"
        "# pii_guard pre-commit hook, tracked in scripts/git-hooks/ so it travels.\n"
        "# Wired up via:  python3 scripts/pii_guard.py --install-hook\n"
        "python3 scripts/pii_guard.py\n"
    )
    hook_path.chmod(0o755)
    subprocess.run(["git", "config", "core.hooksPath", "scripts/git-hooks"], check=False)
    # Retire the old per-clone hook so it can't run twice.
    legacy = Path(".git/hooks/pre-commit")
    if legacy.exists():
        legacy.unlink()
    print(f"Installed pre-commit hook at {hook_path} and set core.hooksPath=scripts/git-hooks")
    return True


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--all", action="store_true", help="Scan all wiki/ and inbox/ instead of staged files")
    parser.add_argument("--install-hook", action="store_true", help="Write .git/hooks/pre-commit stub and exit")
    args = parser.parse_args()

    if args.install_hook:
        sys.exit(0 if install_hook() else 1)

    # Staged mode is meaningless without a repo, and silence would read as "clean".
    # A downloaded vault has no staged files ever, so scanning them would report an
    # all-clear without opening a single file: the same lie install_hook used to
    # tell. Send them to --all, which actually reads the vault.
    if not args.all and not in_git_repo():
        print(
            "Not a git repository, so there are no staged files to scan and this\n"
            "check has nothing to say. To actually scan the vault's contents, run:\n"
            "  python3 scripts/pii_guard.py --all"
        )
        sys.exit(1)

    # Pre-commit (staged) mode: block any staged binary outright before the text
    # scan: a binary can hide secrets the scanner can't read (root cause of the
    # invoice-PDF leak). --all is a content audit and skips this gate.
    if not args.all:
        binaries = staged_binary_files()
        if binaries:
            print("Binary file(s) staged for commit, blocked:")
            for p in binaries:
                print(f"  {p}")
            print("\nBinaries (PDF/image/xlsx/etc.) don't belong in the versioned vault, they")
            print("can't be scanned for secrets. Keep them in inbox/ (gitignored) or their")
            print("native system. Genuine exception: re-run with  git commit --no-verify .")
            sys.exit(1)

    files = all_scan_files() if args.all else staged_files()

    total_hits = 0
    for path in sorted(files):
        hits = scan_file(path)
        for lineno, reason, text in hits:
            print(f"  {path}:{lineno}  [{reason}]  {text[:120]}")
            total_hits += 1

    if total_hits:
        print(f"\nPII/secret scan: {total_hits} hit(s), commit blocked.")
        print("Review the lines above. If a hit is a false positive, add  # pii-guard-ok  to that line.")
    else:
        mode = "all files" if args.all else "staged files"
        print(f"PII/secret scan clean ({mode}).")

    sys.exit(1 if total_hits else 0)


if __name__ == "__main__":
    main()
