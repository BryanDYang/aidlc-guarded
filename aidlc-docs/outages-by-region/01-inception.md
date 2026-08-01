# AIDLC inception — outages-by-region report

## Objective

Add a read-only report that summarizes outage counts and affected customers by
region.

## Scope

- Add `GET /reports/outages-by-region` to the reports blueprint.
- Use a fixed aggregate query without user input.
- Return region-level totals only.

## Controls and verification

- Apply NIST AC-3 and NERC CIP-011 R1 traceability.
- Keep the operation fixed, parameter-safe, and read-only.
- Verify HTTP 200 and the expected aggregate fields.
- Record the completed implementation in `change-log/`.

## Decisions

- Reuse the existing reports blueprint and database connection helper.
- Expose only operational aggregates.

## Open questions

None.
