# Align active demo documentation

## Prompt

Audit and correct the AIDLC documentation so the active files consistently
describe the rough demo, local dashboard behavior, and optional enterprise
extensions.

## Files changed

- `README.md`
- `AGENTS.md`
- `governance/audit-prompt.md`
- `aidlc-guardrail-gate-setup-roadmap-guide.html`
- `aidlc-guardrail-gate-prod-considerations.html`
- `change-log/2026-07-31_2200_align-active-demo-documentation.md`

## Controls applied

- Used customer-neutral Utility Co language.
- Preserved the ten audit checks and existing enforcement behavior.
- Documented that the populated dashboard is published from `gh-pages`.
- Documented Orchestrate, OpenPages, and notification flows as optional,
  fail-open extensions for the rough demo.

## Risk notes

The audit prompt branding changed from a real-company reference to the
fictional Utility Co name. Audit logic, rule filenames, verdict format, and
canary token are unchanged.

## Approval

Approved by the repository owner through the documentation-correction request.
