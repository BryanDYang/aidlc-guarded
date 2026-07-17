# Change log — add Outlook email + OpenPages tools to governance agent

**Date:** 2026-07-17 22:06 UTC

## Prompt
Add the three missing tools shown in architecture-wxo-governance.drawio to the
aidlc-governance-agent repo: Outlook email notification, OpenPages Issue
create/update per violation, and OpenPages metrics trend update.

## Files changed

### aidlc-governance-agent repo
- `tools/send_outlook_email_tool.py` — new tool; sends HTML governance alert via
  Microsoft Graph API (client-credentials OAuth, app-only). Called on FAIL /
  high-critical severity. Fail-open: never raises, returns error string on failure.
- `tools/openpages_issue_tool.py` — new tool; creates or updates one OpenPages
  Issue per rule violation using the field mapping from the architecture diagram.
  Dedup key: repo + pr_number + rule. Auto-closes on PASS verdict.
- `tools/openpages_metrics_tool.py` — new tool; increments per-repo pass/fail
  counters and per-rule/per-actor violation tallies in a single OpenPages metrics
  record. Called on every verdict (PASS + FAIL).
- `agents/governance-agent.yaml` — added 3 new tools to the `tools:` list;
  expanded instructions with explicit 5-step verdict-handling sequence so the
  agent calls all tools in the correct order.
- `deploy.sh` — added 3 new `orchestrate tools import` calls for the new tools.
- `.env.example` — added OUTLOOK_* and OPENPAGES_* variable blocks with comments.

## Controls applied
- **AU-2 / AU-12 / CIP-007 R4** — Outlook email is the human-facing audit alert;
  OpenPages Issues are the machine-readable per-violation record (AIDLC Gap ④).
- **SC-28 / CIP-011** — all credentials read from environment variables; none
  hardcoded (rule 01).
- **CM-2 / CIP-010 R1** — no new third-party libraries added; all tools use stdlib
  `urllib.request` only (rule 04 compliance).

## Risk notes
- All three tools are fail-open by design (matching the pattern of notify-wxo.py)
  — an Outlook or OpenPages outage can never freeze the gate.
- OpenPages custom field names (AIDLC_DedupKey, AIDLC_Repo, etc.) must be
  created in the OpenPages schema before the tool will persist them. The tool
  itself will not error — fields it cannot write are silently dropped by the API.
- OPENPAGES_ISSUE_TYPE and OPENPAGES_METRICS_TYPE must match object types that
  exist in the target OpenPages instance.
- No high-risk generation; no regulated-record hard delete; no human approval gate
  required.

## Approval
Standard feature addition — no destructive operations.
