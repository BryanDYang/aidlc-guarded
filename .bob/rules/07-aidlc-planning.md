# AIDLC planning before implementation (plan-first, append-only)

No application-code change ships without a plan. Before adding or modifying code
in this repo (for example anything under `api/`, `app.py`, `db.py`, `seed.py`),
the change must be planned in **AIDLC Planning mode**, which produces a planning
document under `aidlc-docs/`.

This applies to **every** code-adding change — any commit or pull request —
whether or not the AIDLC skill was invoked by name. If a request would add code
without a plan, plan it first: clarify open questions, resolve every `[BLOCKER]`,
write `aidlc-docs/<feature>/01-inception.md`, then implement.

Rules for the planning record:

- **Required.** A code change must add a new `aidlc-docs/…` planning document for
  that change. Code with no plan is a finding.
- **Unblocked.** The plan must have no unresolved `[BLOCKER]` markers. Planning is
  not complete — and implementation must not begin — while a blocker is open.
- **Append-only.** Planning records are immutable history. A change may add new
  planning documents but must never modify or delete previously committed ones.

## Workflow — mode transitions (mandatory, not optional)

- **On start — switch to Planning mode.** The moment a request would add or change
  application code, switch to the 🔵 **AIDLC Planning mode** (`aidlc-planning`)
  before anything else. Do not write code, run commands, or edit non-markdown
  files first. Planning is the entry point for every code task, not just high-risk
  ones.
- **Resolve blockers before building.** In Planning mode, clarify open questions
  and mark must-answer items `[BLOCKER]`. Do **not** begin implementation while any
  `[BLOCKER]` is open — planning is not complete until every blocker is resolved.
- **Then, and only then, build.** Once every `[BLOCKER]` is resolved and the plan
  is approved, leave Planning mode for a build context and implement the change —
  with its compliance header, parameterized SQL, approved libraries, and a
  `change-log/` entry (rule 03).

This is the build-layer proof that the AIDLC workflow was followed before code
was written. It pairs with rule 03 (the per-change change-log): the plan says
what will be built and why; the change-log records what was built.
