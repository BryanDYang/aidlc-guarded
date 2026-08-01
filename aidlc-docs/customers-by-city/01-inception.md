# AIDLC inception — customers-by-city report

## Objective

Add `GET /reports/customers-by-city` for a controlled governance-gate demo.

## Scope

- Add one route to the reports blueprint.
- Accept and validate a `city` query parameter.
- Return customer identifiers, names, and cities.
- Exercise the independent PR audit with intentional string-built SQL.

## Controls and verification

- Validate the city parameter as nonempty and no longer than 80 characters.
- Trace input validation and persistence access in the compliance header.
- Confirm the GitHub gate detects and blocks string-built SQL.
- Do not merge this demonstration branch.

## Decisions

- The unsafe SQL construction is intentional evidence for the blocked path.
- The pull request will remain a draft and must never merge.

## Open questions

None.
