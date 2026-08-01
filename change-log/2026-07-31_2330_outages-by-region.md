# Add outages-by-region report

## Prompt

Create a second compliant demonstration PR with a read-only outage summary by
region.

## Files changed

- `api/reports.py`: Added the region-level aggregate report and route.
- `aidlc-docs/outages-by-region/01-inception.md`: Recorded the approved plan.
- `change-log/2026-07-31_2330_outages-by-region.md`: Recorded this change.

## Controls applied

- `01-secure-coding.md`: Used a fixed query without string interpolation.
- `02-compliance-headers.md`: Applied NIST AC-3 and NERC CIP-011 R1.
- `03-audit-and-change-log.md`: Recorded the implementation decision.
- `07-aidlc-planning.md`: Added an unblocked, append-only plan.

## Risk notes

The endpoint is read-only, returns aggregate operational information, adds no
dependency, and performs no destructive operation.

## Approval

Approved by the repository owner as a compliant demonstration artifact.
