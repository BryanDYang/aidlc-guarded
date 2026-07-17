# Open-questions template → aidlc-docs/<feature>/00-open-questions.md

This is the FIRST artifact of Inception, written before any planning. It is the
governed equivalent of Kiro's clarify-before-you-build step: surface everything
that is ambiguous or risky, get human answers, and only then plan. A change that
starts without its open questions answered is how things break in production.

```
# Open questions — <feature name>
Status: AWAITING ANSWERS   Date: <YYYY-MM-DD>   Requested by: <user>

Answer inline under each question (edit this file, or answer in chat and Bob
updates it). Bob will NOT proceed to planning until every BLOCKER is answered.

## A. Procedural / scope
1. [BLOCKER] What is the single outcome this change must achieve? (one sentence)
   → <answer>
2. [BLOCKER] In / out of scope — what should this explicitly NOT do?
   → <answer>
3. Who is the end user / caller of this capability?
   → <answer>

## B. Data & compliance (drives the risk tier)
4. [BLOCKER] Does this read, write, or delete customer / meter / outage / audit
   records? (rule 05 — regulated data)
   → <answer>
5. [BLOCKER] Any secrets, credentials, or external endpoints involved? (rule 01)
   → <answer>
6. Is any part of this BES-adjacent / in NERC CIP scope? Which CIP requirement?
   → <answer>

## C. Design constraints
7. New third-party libraries needed? (rule 04 — must be on the allowlist)
   → <answer>
8. Backward-compatibility / migration concerns on existing endpoints or schema?
   → <answer>
9. What does "done" look like — acceptance criteria / how will we test it?
   → <answer>

## D. Assumptions Bob is making (correct any that are wrong)
- <assumption 1>
- <assumption 2>

---
When all [BLOCKER] items are answered, set Status: READY and tell Bob to
continue. Bob then writes 01-inception.md and stops at the Inception gate.
```
