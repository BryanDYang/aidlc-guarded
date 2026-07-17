---
name: aidlc
description: >-
  Run PG&E's AI Development Life Cycle (AIDLC) workflow — the Inception →
  Construction → Operations methodology — for a feature, migration, or service.
  Use when the user says "Using AIDLC", "run the AIDLC workflow", "do this the
  AIDLC way", or asks to take a change through structured phases with
  human approval gates and governed artifacts. Adapted from the AWS AI-DLC
  framework; operates inside the PG&E AI Safe Constitution.
---

# AIDLC workflow — Inception → Construction → Operations

You are running PG&E's AI Development Life Cycle. This skill is a **workflow**,
not a set of guardrails: the always-on guardrails live in `.bob/rules/` (the
Safe Constitution) and apply throughout. This skill governs *how a change moves
through phases*, with a human approving each phase boundary and every phase
leaving an artifact in `aidlc-docs/`.

## Operating principles

1. **The agent proposes, the human approves.** Never cross a phase boundary
   without explicit user confirmation. At each gate, present what you found /
   built and ask to proceed.
2. **Be adaptive.** Only run the stages that add value for this request. A
   one-line fix does not need a full risk assessment; a new BES-adjacent
   endpoint does. State which stages you are skipping and why.
3. **Everything is an artifact.** Each phase writes a markdown file under
   `aidlc-docs/` (create the folder if missing). These are the observable
   record of the workflow — the AIDLC counterpart to the change-log.
4. **The Constitution wins.** If any stage would require violating a rule in
   `.bob/rules/`, stop and follow the rule (refuse / propose an alternative).
   Governance is not suspended inside the workflow.

## Phase 1 — Inception (🔵 what and why)

Determine what to build and why *before* writing code. Inception has two steps
with a human checkpoint between them — **clarify, then plan.** Do not collapse
them.

### Step 1a — Clarify first (open questions before planning)

Before any planning, analysis, or design, surface what you do not know. Read
`templates/open-questions.md` and produce
`aidlc-docs/<feature>/00-open-questions.md`:

- Ask the **procedural and scope** questions (what is the outcome, what is
  explicitly out of scope, who is the caller).
- Ask the **data & compliance** questions that set the risk tier: does this
  touch regulated or BES-adjacent records (rule 05)? secrets or external calls
  (rule 01)? NERC CIP scope? new libraries (rule 04)?
- List the **assumptions you are making** so the human can correct them.
- Mark the must-answer items `[BLOCKER]`.

Then **stop and hand it back.** Present the questions in chat *and* write them to
the file. The human answers — in chat, or by editing the file — and you fold
their answers back in. **Do not proceed to planning while any `[BLOCKER]` is
unanswered.** Deeper/riskier work means more questions, not fewer; it is always
cheaper to ask now than to unwind a wrong build later.

### Step 1b — Plan (only after blockers are answered)

Once the open questions resolve, read `templates/inception.md` and produce
`aidlc-docs/<feature>/01-inception.md`:

- Identify user stories / acceptance criteria.
- Do the **risk and compliance triage** (now informed by the answers): controls
  that apply (rule 02), regulated-data handling (rule 05), secrets (rule 01).
- Decompose into work units.

**Gate:** present the inception summary and the risk triage. Do not design or
code until the user approves. For high-risk work, recommend running this phase
in the **🔵 AIDLC Planning mode** (`.bob/custom_modes.yaml`), where `execute` is
withheld and `edit` is restricted to markdown — so Bob can write the plan but
physically cannot write application code or run commands during planning.
Enforcement by permission, not just intent.

## Phase 2 — Construction (🟢 how)

Only after Inception is approved. Read `templates/construction.md` and produce
`aidlc-docs/<feature>/02-construction.md`.

- Component/interface design for each work unit.
- Implement, following the Constitution: parameterized queries, secrets from
  env, compliance headers, approved libraries only.
- Write or update tests; state the testing strategy.
- Every code change still writes its own `change-log/` entry (rule 03) — the
  construction artifact summarizes; the change-log is the per-change record.

**Gate:** present the diff summary, the tests, and the controls applied. Ask
before merging toward `main` (where the CI guardrail gate will independently
re-audit the diff).

## Phase 3 — Operations (🟡 deploy and observe)

Read `templates/operations.md` and produce `aidlc-docs/<feature>/03-operations.md`.

- Deployment / rollback notes; configuration changes (CIP-010 R1 baseline).
- Observability: what to log, what to alert on, the runbook.
- **Honest scope line:** runtime concerns this skill cannot own — non-human
  agent identity for any service calls (Gap 3: Vault + SPIFFE/SPIRE) and the
  cross-agent audit spine (Gap 4: watsonx Orchestrate + Confluent) — are named
  here and handed to the platform layer, not faked.

**Gate:** present the operations plan. This phase documents; it does not deploy
to a regulated environment from the IDE.

## Output

At the end, list every artifact written under `aidlc-docs/` and every
`change-log/` entry, and restate any items flagged for human review or handed to
the platform layer. That list is the workshop's observability evidence.
