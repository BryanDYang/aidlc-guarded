# Change log — 2026-07-16_1629 add-ci-demo-suite

## Prompt
User asked whether ci-demo/run-demo-prs.sh exists and noted it was referenced in the
README but missing. Task: create the full demo suite.

## Files changed
- `ci-demo/run-demo-prs.sh`: Main driver script. Creates/resets 12 demo branches,
  applies each payload, and opens draft PRs via `gh pr create`. Includes branch
  checkout guards, label creation, and a final summary with the Actions URL.
- `ci-demo/payloads/demo01-compliant-report.py`: Compliant payload — new
  `/reports/customers-by-status` endpoint with header, parameterized SQL,
  change-log, and AIDLC plan.
- `ci-demo/payloads/demo02-compliant-schema.py`: Compliant payload — additive
  `outages.notes` column migration with all required governance artefacts.
- `ci-demo/payloads/demo03-violation-inline-secret.py`: Check 1 violation —
  hardcoded API key literal in `api/notify.py`.
- `ci-demo/payloads/demo04-violation-string-sql.py`: Check 2 violation — f-string
  SQL in `api/search.py`.
- `ci-demo/payloads/demo05-violation-no-validation.py`: Check 3 violation — no
  length/type check on query param in `api/meter_search.py`.
- `ci-demo/payloads/demo06-violation-hard-delete.py`: Check 4 violation — hard
  `DELETE` on customers table.
- `ci-demo/payloads/demo07-violation-no-header.py`: Check 5 violation — new route
  with no compliance header block.
- `ci-demo/payloads/demo08-violation-unapproved-lib.py`: Check 6 violation — adds
  `pandas` to `requirements.txt`.
- `ci-demo/payloads/demo09-violation-bulk-api-calls.py`: Check 7 violation — bash
  script with unbounded API loop and embedded long-lived credential.
- `ci-demo/payloads/demo10-violation-governance-tamper.py`: Check 8 violation —
  creates a file inside `.bob/rules/`; triggers the deterministic guard before Bob.
- `ci-demo/payloads/demo11-violation-no-changelog.py`: Check 9 violation — code
  change with no `change-log/` entry.
- `ci-demo/payloads/demo12-violation-no-aidlc-plan.py`: Check 10 violation — code
  change with change-log but no `aidlc-docs/` planning document.

## Controls applied
- CM-2, CM-6, CIP-010 R1 — new demo files are configuration/tooling, not application
  code; no application schema or business logic changed.
- AU-2, AU-12, CIP-010 R1 — this change-log entry.

## Risk notes
All changes are under `ci-demo/` (demo tooling, not application code). No
production routes, schema, or regulated data are modified. The violation payloads
write to staging branch files only; they are never merged to main. No secrets,
no unapproved libraries, no hard deletes, no governance files modified.

## Approval
N/A — demo/tooling addition only; no high-risk (rule 05) action.
