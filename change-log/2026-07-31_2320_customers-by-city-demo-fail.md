# Add intentional customers-by-city violation

## Prompt

Create an intentionally noncompliant SQL pull request for the governed AIDLC
demonstration and verify that the independent GitHub gate blocks it.

## Files changed

- `api/reports.py`: Added a demo route containing intentional string-built SQL.
- `aidlc-docs/customers-by-city/01-inception.md`: Recorded the demonstration plan.
- `change-log/2026-07-31_2320_customers-by-city-demo-fail.md`: Recorded the intent.

## Controls applied

- `02-compliance-headers.md`: Applied AC-3, SI-10, CIP-007 R5, and CIP-011 R1.
- `03-audit-and-change-log.md`: Recorded the deliberately rejected design.
- `07-aidlc-planning.md`: Added an unblocked, append-only plan.
- `01-secure-coding.md`: Intentionally violated to demonstrate enforcement.

## Risk notes

The SQL injection risk is deliberate and confined to an unmergeable draft demo
branch. The PR must remain blocked and must never be deployed or merged.

## Approval

Approved by the repository owner solely as a controlled negative demonstration
artifact. This approval does not authorize merge or deployment.
