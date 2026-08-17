# inbox/

Drop source material here: manuals, spec sheets, quotes, meeting notes, exported transcripts, photos of a rack, anything you want the vault to absorb.

Then tell the agent to ingest it. It reads the file, discusses the takeaways with you, writes or updates the wiki pages, updates the index, and logs the action.

**After ingest, files move to `_processed/`**, or get deleted outright if they contain anything sensitive (see `CLAUDE.md` → What Never Goes in This Vault).

**This folder is gitignored.** Nothing here is ever committed or synced to a remote. That is deliberate: source drops are often binaries, and binaries cannot be scanned for secrets.
