# Change log — fix canary token mismatch in smoke test

**Date:** 2026-07-17 20:18 UTC

## Prompt
Workflow run failed: smoke test grep for `UTILITY-SAFE-CONSTITUTION-CANARY-4A17` did not match Bob's actual output of `PGE-SAFE-CONSTITUTION-CANARY-4A17`, causing exit 1 before the real audit ran.

## Files changed
- `.github/workflows/guardrail-gate.yml` — corrected the hardcoded canary token string on line 70 from `UTILITY-SAFE-CONSTITUTION-CANARY-4A17` to `PGE-SAFE-CONSTITUTION-CANARY-4A17` to match `.bob/rules/00-safe-constitution.md`.

## Controls applied
- **AU-2 / CIP-010 R1** — smoke test is the guard that proves workspace rules were loaded before any audit verdict is trusted; a mismatched token silently bypassed this check.
- **Rule 06 (governance protection)** — the fix keeps the canary check intact; no governance path was weakened.

## Root cause
The original workflow was authored with a placeholder prefix (`UTILITY-`) that was never updated to match the actual workspace ruleset prefix (`PGE-`). Bob returned the correct token; the grep pattern was simply wrong.

## Risk notes
- The MCP marketplace connection error (`fetch failed`) is benign and expected in the headless Actions runner — no marketplace credentials are present. It does not affect the audit.
- No governance file content was modified; only the token string used to verify governance-file loading was corrected.
- No high-risk generation; no human approval gate required.

## Approval
Standard fix — no destructive operation, no regulated-record touch.
