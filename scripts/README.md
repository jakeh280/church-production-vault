# scripts/

Vault maintenance tooling. For usage, conventions, and the script table see `CLAUDE.md` → **Maintenance Scripts**, or `wiki/00-Meta/Maintenance-Scripts.md` for the detailed docs.

All scripts are read-only reporters unless noted. Run them from the vault root:

```bash
python3 scripts/health.py
python3 scripts/link_check.py
python3 scripts/staleness.py
python3 scripts/bring_up.py
python3 scripts/reflow.py --apply
python3 scripts/fm_fix.py --apply
python3 scripts/pii_guard.py --all
```

Install the pre-commit guard once per machine:

```bash
python3 scripts/pii_guard.py --install-hook
```
