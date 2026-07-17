# Audit trail and change log (Gap 4 — an authoritative record)

PG&E has eleven developer agents in individual IDEs today with no shared system
of record. A full control plane (watsonx Orchestrate + Confluent as the
immutable audit spine) is the platform-layer answer. At the **build layer**,
the minimum obligation is that no AI-assisted change is unaccounted for: every
change Bob makes writes its own record.

After **every** change you make to code in this repo, write a file in
`change-log/`. Create the folder if it does not exist.

File name: `YYYY-MM-DD_HHMM_short-description.md`

Each entry contains:

- **Prompt** — the user's request, verbatim.
- **Files changed** — each path with a one-line summary of the change.
- **Controls applied** — which Constitution rules and which NIST / NERC CIP
  controls governed the change (cross-reference the compliance header).
- **Risk notes** — anything a human reviewer should see: a refused sub-request,
  a `Control: TBD`, a regulated-record touch, a substituted library.
- **Approval** — for any high-risk generation (rule 05), note that human
  confirmation was requested before files were written.

This is decision lineage for CIP-010 R1 (baseline configuration change tracking)
and AU-2/AU-12. It is deliberately local and lightweight — a placeholder for the
Confluent event spine, not a replacement for it. Treat it as the seam where
Bob's per-change record would flow into the platform audit layer.
