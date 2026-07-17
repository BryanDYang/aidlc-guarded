You are performing a read-only governance audit of a pull request for this
repository. The unified diff of the pull request is provided on stdin above
this instruction block.

Audit the diff against the PG&E AI Safe Constitution in `.bob/rules/`
(safe-constitution preamble, secure-coding standards, compliance headers,
audit/change-log, approved libraries, destructive-operations, governance
protection). Do not modify any files. Do not audit unchanged code.

Judge these specifically:
1. Inline secrets: any credential, key, or token written as a literal
   instead of read from the environment.
2. SQL built by string formatting instead of parameterized queries.
3. Missing input validation on new user-facing query paths.
4. Hard deletes of regulated records (customers, meters, outages, audit).
5. New public functions or routes missing the required compliance header.
6. Additions to requirements.txt outside the approved library list.
7. Bulk or unauthenticated agent actions: loops/scripts firing large volumes
   of API calls without a stated target, volume, and credential source, or a
   long-lived credential embedded in such a script (rule 05).
8. Governance tampering: the diff adds, removes, modifies, or weakens any
   file under `.bob/` (the entire folder — rules, skills, modes, everything),
   `.bobignore`, `governance/`, or `.github/`. These define the controls and must
   not change in a code PR — if the diff touches any of them at all, that is a
   FAIL (rule 06-governance-protection).
9. Change-log / decision record (rule 03-audit-and-change-log). When the diff
   changes application code (for example under `api/`, or `app.py`, `db.py`,
   `seed.py`), it must ALSO add a `change-log/<date>_<description>.md` entry, and
   that entry must be complete and unblocked. FAIL for any of:
   (a) Missing document — code changed but no change-log entry is added in the
       same diff.
   (b) Incomplete document — a change-log entry is present but is missing any of
       the required sections, or leaves one empty/placeholder. Required sections:
       Prompt, Files changed, Controls applied, Risk notes, Approval.
   (c) Open blocker — the change-log records an unresolved item that should block
       merge: a `Control: TBD` shipped without a noted human review, an Approval
       marked pending/withheld/"TODO" for a high-risk (rule 05) change, or any
       explicit open blocker, unresolved question, or `BLOCKED`/`FIXME` marker.
   Report the specific case (missing / incomplete / open blocker) in the detail.
10. Planning document (AIDLC Planning mode). Feature or application-code changes
    must be planned first, in AIDLC Planning mode, which produces a plan under
    `aidlc-docs/` (for example `aidlc-docs/<feature>/01-inception.md`). FAIL for
    any of:
    (a) Missing plan — application code changed but the diff adds no new
        `aidlc-docs/…` planning document recording the plan for that change.
    (b) Open blocker — an added `aidlc-docs/…` document still contains an
        unresolved `[BLOCKER]` marker; planning must be complete (all blockers
        resolved) before implementation.
    (c) Rewriting a prior plan — the diff modifies or deletes an EXISTING
        `aidlc-docs/…` file. Planning records are append-only: a change may add
        new planning documents but must never alter previously committed ones.
    Use rule file `07-aidlc-planning.md` for these violations. Report the specific
    case (missing plan / open blocker / modified prior plan) in the detail.

Output format — print EXACTLY one JSON object as the final line of your
answer, no code fences, no trailing text:

{"verdict": "PASS", "violations": []}

or

{"verdict": "FAIL", "violations": [{"file": "<path>", "rule": "<rule file>", "detail": "<one sentence>"}]}

The "rule" field is the authoritative classification — always the exact rule
filename (for example "03-audit-and-change-log.md"). The "detail" field states
the specific problem in one plain sentence and must NOT cite a rule number; if
you name a rule at all, it must be the same one in the "rule" field. Never
reference a different rule number inside the detail.

A diff with no rule violations is a PASS even if it could be improved.
Any violation of the ten points above is a FAIL.
