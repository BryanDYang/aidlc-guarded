# Inception artifact template → aidlc-docs/<feature>/01-inception.md

```
# Inception — <feature name>
Date: <YYYY-MM-DD>   Author (agent): Bob   Requested by: <user>

## Problem / request
<one-paragraph statement of what the user asked for, verbatim prompt quoted>

## User stories / acceptance criteria
- As a <role>, I want <capability>, so that <outcome>.
  - AC: <testable criterion>

## Risk & compliance triage
| Question | Answer | Rule / control |
|----------|--------|----------------|
| Touches regulated or BES-adjacent records? | <yes/no + which> | 05 / CIP-011 |
| Handles secrets or credentials? | <yes/no> | 01 / SC-28, CIP-007 R5 |
| Makes external / internal API calls? | <yes/no + endpoint> | 05 / — |
| New dependencies required? | <yes/no + which> | 04 / CIP-010 R1 |
| Applicable NIST / NERC CIP controls | <list> | 02 |
| Risk tier | <low / medium / high> | — |

## Work-unit decomposition
1. <unit> — <one line>
2. ...

## Recommendation
<proceed / proceed-in-Inception-mode-first / needs-human-decision>, because <reason>.

## GATE
Awaiting user approval to enter Construction. Stages skipped this run: <list + why>.
```
