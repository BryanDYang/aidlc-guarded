# Add customers-by-status report

## Prompt

Using AIDLC, add a GET /reports/customers-by-status endpoint that returns the
number of customers in each account status.

## Files changed

- `api/reports.py`: Added the read-only aggregate report route.
- `aidlc-docs/customers-by-status/01-inception.md`: Recorded the approved plan.
- `change-log/2026-07-31_2315_customers-by-status.md`: Recorded this decision.

## Controls applied

- `01-secure-coding.md`: Used a fixed aggregate query with no interpolated SQL.
- `02-compliance-headers.md`: Applied NIST AC-3 and NERC CIP-011 R1 traceability.
- `03-audit-and-change-log.md`: Recorded the implementation decision.
- `07-aidlc-planning.md`: Added an unblocked, append-only plan.

## Risk notes

The endpoint is read-only and returns aggregate counts without customer PII.
It adds no dependencies and performs no destructive operation.

## Approval

Approved by the repository owner as the compliant demonstration change.
