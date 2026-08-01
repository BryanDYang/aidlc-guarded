# Normalize demo branches

## Prompt

Clean up the demo repositories and branches while preserving recoverable
copies of the existing work.

## Files changed

- `.bob/mcp.json`
- `README.md`
- `change-log/log.json` (removed)
- `change-log/2026-07-31_2300_normalize-demo-branches.md`

## Controls applied

- Restored the portable Bob marketplace endpoint from `main` so the demo branch
  no longer carries a machine-specific local port.
- Preserved the original branch tips with dated backup tags before retiring
  experimental smoke-test branches.
- Kept the generated `gh-pages` branch separate and unchanged.
- Removed the timestamp marker and temporary JSON record left by the completed
  WXO pipeline smoke test.

## Risk notes

The endpoint is local development metadata rather than a credential. No API
keys, tokens, dashboard records, or governance logic were changed.

## Approval

Approved by the repository owner through the repository-cleanup request.
