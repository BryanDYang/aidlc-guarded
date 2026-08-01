# IBM Bob × Utility Co — AIDLC Governance at the Source

> Governance is built *into how the code gets made* — IBM Bob follows an always-on rulebook and plans before it builds — and then **re-proven at the one place every change must pass through: the merge into `main`.** Nothing risky reaches the trunk unchecked, and the check can't be quietly turned off.

This repository is the governed implementation used by the demo. The current
rough-demo flow compares a compliant pull request with an intentionally
violating pull request; it does not require a separate unguarded repository.

## The story

AI writes code faster than review was built to handle. For a regulated or
operational environment, "review it later" does not scale. The AWS **AIDLC**
framework names four gaps: **①** is policy actually enforced? **②** is the
generated code safe? **③** who made the change? **④** is there an authoritative
record?

Bob closes **① and ②** by moving governance to two places that hold:
1. **Into the assistant** — an always-on Constitution and a *plan-first* mode, so the safe way is the default way while code is written.
2. **To the source** — a merge-gate check that re-proves compliance on the diff before it can join `main`.

**Why "at the source" is the right place:** the merge into `main` is the single door every change walks through. Signs saying "please write safe code" get ignored; a guard on the one door everyone uses can't be skipped (it runs on the server, not a laptop), it's the last line before harm, and every attempt is logged.

## How it works

```mermaid
flowchart LR
    Dev([Developer]) -- "plain request" --> Bob[IBM Bob]
    subgraph GEN["1 - While writing (always on)"]
      direction TB
      R["Constitution: .bob/rules 00-08"]
      M["AIDLC Planning mode"]
      S["AIDLC skill"]
    end
    Bob --- GEN
    Bob -- "plan + code + change-log" --> PR["Pull request into main"]
    subgraph GATE["2 - At the source (CI gate)"]
      direction TB
      G["Deterministic guard (no AI)"]
      A["Headless Bob audit (10 checks)"]
    end
    PR --> GATE
    GATE -- "PASS" --> Merge([Merge to main])
    GATE -- "FAIL" --> Block([Blocked + reason])
    GATE --> Dash[["Governance dashboard"]]
```

Governance can't self-certify: the gate **pins the rulebook from `main`**, so a PR can't hand Bob a weakened Constitution to judge itself.

## The Constitution — `.bob/rules/`

Always-loaded, plain-English policies:

| Rule | Enforces |
|---|---|
| **00 · safe-constitution** | Five non-negotiable principles + a **canary token** the CI uses to prove the rules loaded. |
| **01 · secure-coding** | No inline secrets (read from env), parameterized SQL only, validate all input. |
| **02 · compliance-headers** | Every new public function/route carries a **NIST 800-53 / NERC CIP** control header. |
| **03 · audit-and-change-log** | Every code change writes a complete `change-log/` record. |
| **04 · approved-libraries** | Only allow-listed libraries; refuse others. |
| **05 · destructive-operations** | No hard deletes of regulated records; high-risk actions need a human. |
| **06 · governance-protection** | The Constitution can't be weakened by a PR. |
| **07 · aidlc-planning** | Plan first (Planning mode) before code; plans are **append-only**, **no open `[BLOCKER]`**. |
| **08 · current-date** | Read the real date from the system clock — never assume the training date. |

Plus **`.bobignore`** — Bob physically can't read `.env`, keys, or certs.

**Mode & skill:** the **AIDLC Planning mode** (`.bob/custom_modes.yaml`) clarifies open questions (marking `[BLOCKER]`s), writes the plan under `aidlc-docs/`, and only builds once blockers clear. The **AIDLC skill** (`.bob/skills/aidlc/`) runs the **Inception → Construction → Operations** workflow with a human approval gate at each phase.

## How the GitHub gate works

Every PR into `main` runs `.github/workflows/guardrail-gate.yml`:

```mermaid
flowchart TB
    S([PR into main]) --> P["1 - Pin rulebook from main"]
    P --> G{"2 - Deterministic guard:<br/>touches .bob / governance / .github / .bobignore?"}
    G -- "yes" --> F1([FAIL - governance is admin-only])
    G -- "no" --> C{"3 - Canary: did rules load?"}
    C -- "missing" --> F2([FAIL - no rules, no audit])
    C -- "ok" --> A["4 - Headless Bob audit (advanced mode)<br/>read-only 10-point review of the diff"]
    A --> V{"5 - Verdict"}
    V -- "PASS" --> OK([green, mergeable])
    V -- "FAIL" --> F3([blocked, fail-closed])
    OK --> D[["6 - PR comment + dashboard"]]
    F1 --> D
    F2 --> D
    F3 --> D
```

**The 10 audit checks:** inline secrets · string-built SQL · missing input validation · hard deletes · missing compliance header · unapproved libraries · bulk/unauth actions · **governance tampering** · **missing/incomplete change-log** · **missing/blocked AIDLC plan**.

Enforcement is layered — **deterministic** where it must be, **judgment** where it helps:

| Control | Effect | Type |
|---|---|---|
| Branch protection | No direct pushes to `main`; PRs only | deterministic |
| Deterministic guard | Touch `.bob/` / `governance/` / `.github/` / `.bobignore` → instant fail | deterministic |
| CODEOWNERS | Those paths need owner review to merge | deterministic |
| Required check | `bob-guardrail-audit` must be green to merge | deterministic |
| Bob audit | Reasons about code content (safe SQL? complete plan?) | LLM judgment |

**Net effect:** governance and the CI workflow itself can only change by an admin, never through a PR.

**Dashboard** (published from `gh-pages`): pass/fail, violations by rule,
group-by-contributor, and verdict history. The local `sce-demo` branch contains
an empty data file; populated records are written to `gh-pages` by CI.

## Run it

**1 · Prepare the demo PR set** — opens 2 compliant + 10 violating PRs. Run
this only before the presentation from a clean demo worktree; it resets and
force-pushes the demo branches:

```bash
bash ci-demo/run-demo-prs.sh
```

**2 · Try the happy path in Bob** — paste this into Bob in this workspace:

> Using AIDLC, add a GET /reports/customers-by-status endpoint that returns the number of customers in each account status. Show me the plan and wait for my approval before changing code.

Bob plans it (`aidlc-docs/`), writes compliant code + a change-log, and opens a PR — the gate returns **PASS** and it lands as a green PR on the dashboard.

## App context

A small **Flask + SQLite** service for a fictional utility (customers, meters, outages, reports):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py                    # PORT env var, default 5060
```

Local browser preview using a browser-safe port:

```bash
PORT=5080 python app.py
# open http://127.0.0.1:5080/dashboard/
```

The local dashboard data file is empty by design. For populated audit history,
view the GitHub Pages deployment or serve the `origin/gh-pages` branch as
described in the parent [`README.md`](../README.md).

## Optional enterprise extension

The final workflow step can send verdicts to the sibling
`aidlc-governance-agent` when `WXO_API_KEY` and `WXO_AGENT_URL` are configured.
That integration—and its OpenPages or notification tools—is optional and
fail-open. It is not required for the Bob → PR gate → GitHub evidence demo.

---

*Build-layer governance for the AWS AIDLC framework, shown with IBM Bob. Gaps ① and ② are closed here; Gaps ③ (agent identity — Vault/SPIFFE) and ④ (a shared audit spine — Confluent / watsonx.governance) are platform-layer, which this build-layer record is designed to feed.*
# smoke test Sat Jul 18 07:01:43 PDT 2026
