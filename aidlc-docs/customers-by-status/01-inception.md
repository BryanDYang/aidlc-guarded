# AIDLC inception — customers-by-status report

## Objective

Add a read-only `GET /reports/customers-by-status` endpoint that returns the
number of customers in each account status.

## Scope

- Add one route to the existing reports blueprint.
- Execute a fixed aggregate query with no user-provided SQL values.
- Return a JSON array containing `account_status` and `count`.

## Controls and verification

- Trace the database operation to NIST AC-3 and NERC CIP-011 R1.
- Keep the query fixed and read-only.
- Verify the endpoint returns HTTP 200 and grouped counts.
- Record the completed change in `change-log/`.

## Decisions

- Reuse the existing reports blueprint and database helper.
- Return only aggregate counts; expose no customer names or contact data.

## Open questions

None.
