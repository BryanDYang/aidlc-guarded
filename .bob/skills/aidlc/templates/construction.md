# Construction artifact template → aidlc-docs/<feature>/02-construction.md

```
# Construction — <feature name>
Date: <YYYY-MM-DD>   Inception approved: <yes + when>

## Design
- Component(s): <files/modules touched or added>
- Interfaces: <routes, function signatures>
- Data access: parameterized (rule 01) — <how>

## Implementation summary
| File | Change | Control header | change-log entry |
|------|--------|----------------|------------------|
| api/<x>.py | <one line> | <NIST / CIP> | <filename> |

## Controls applied
- Secrets: <from env / none>            (rule 01)
- Compliance headers: <added to N funcs> (rule 02)
- Libraries: <approved list only>        (rule 04)
- Destructive ops: <none / soft-delete>  (rule 05)

## Tests
- <test file> — <what it covers>
- Result: <pass/fail summary>

## GATE
Awaiting user approval to open a PR toward main. The CI guardrail gate will
independently re-audit this diff against the rulebook pinned from main.
```
