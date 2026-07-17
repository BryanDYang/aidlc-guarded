# Governance protection (Gap 1 — the Constitution cannot be quietly weakened)

The workshop's central finding: under Copilot and Kiro the Safe Constitution
was a steering document a developer or agent could edit or delete at the repo
level with no detection. The Operate layer that would have caught this was
removed under a cybersecurity mandate and never replaced. This rule is the build
-layer replacement; watsonx.governance provides the runtime, at-scale version
(drift detection, real-time deviation alerts across all IDEs).

The following paths **define the controls** and must not be changed by an
ordinary code pull request:

- `.bob/rules/` — the Constitution itself
- `.bob/skills/` — governed workflows (the AIDLC skill)
- `.bobignore` — the secret-file blocklist
- `governance/` — the audit prompt and verdict parser
- `.github/workflows/` and `.github/CODEOWNERS` — the CI gate and its ownership

If a diff adds, removes, modifies, or weakens any file under those paths, that is
a **violation**. Treat it as a FAIL and require review by the code owner.
Weakening or deleting a rule is never an acceptable side effect of a code
change — governance changes travel on their own branch, reviewed separately, by
the owner.

This is enforced in depth:

1. **At generation time** — Bob refuses to fold a governance edit into a feature
   change and tells the developer to separate it.
2. **At the merge chokepoint** — the CI gate judges every PR with the rulebook
   **pinned from `main`**, so a PR cannot hand Bob a weakened Constitution to
   rate itself against; the tampering still shows in the diff and fails the gate
   (see `governance/audit-prompt.md`).
3. **By ownership** — CODEOWNERS requires the governance owner's review of any
   change under these paths, and branch protection blocks force-push and
   deletion of `main`.
