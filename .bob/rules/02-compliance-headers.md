# Compliance headers (NERC CIP / NIST control traceability)

Every new public function, route handler, or module must begin with a header
comment that ties the code to the control it implements. This is what makes an
AI-generated change auditable after the fact and gives CIP-010 configuration
change management a machine-readable anchor.

Exact format:

```
# ---------------------------------------------------------------------------
# Function: <name>
# Owner:    grid-platform-team
# Control:  <NIST 800-53 control id>   (NERC CIP: <CIP requirement>)
# Reviewed: <YYYY-MM-DD>
# ---------------------------------------------------------------------------
```

Pick the control that best matches what the code does:

| The code does...                         | NIST control  | NERC CIP        |
|------------------------------------------|---------------|-----------------|
| Authentication / session handling        | AC-2, IA-2    | CIP-007 R5      |
| Authorization / access checks            | AC-6          | CIP-004, CIP-007|
| Database / persistence                   | AC-3          | CIP-011 R1      |
| Secrets, encryption, data at rest        | SC-13, SC-28  | CIP-007 R5, CIP-011|
| Logging, audit, change tracking          | AU-2, AU-12   | CIP-007 R4, CIP-010 R1|
| Input validation                         | SI-10         | CIP-007 R5      |
| Configuration / dependency management    | CM-2, CM-6    | CIP-010 R1      |
| Network / transport security             | SC-8, SC-23   | CIP-005         |

If nothing fits, write `Control: TBD` **and** flag it for human review in the
change-log (rule 03). A `TBD` control that ships without review is itself a
finding.
