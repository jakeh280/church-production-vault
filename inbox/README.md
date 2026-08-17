# inbox/

Drop source material here: **photos of your rack, patch panel, labels, or console**, plus manuals, spec sheets, quotes, meeting notes, exported transcripts, anything you want the vault to absorb.

Phone photos are the fastest way to document a room, and agents read them well. The agent writes down only what's legibly visible and flags anything it couldn't read clearly rather than guessing at a model number, so a blurry label becomes an open question, not a wrong fact.

Then tell the agent to ingest it. It reads the file, discusses the takeaways with you, writes or updates the wiki pages, updates the index, and logs the action.

**After ingest, files move to `_processed/`**, or get deleted outright if they contain anything sensitive (see `CLAUDE.md` → What Never Goes in This Vault).

**This folder is gitignored.** Nothing here is ever committed or synced to a remote. That is deliberate: source drops are often binaries, and binaries cannot be scanned for secrets.
