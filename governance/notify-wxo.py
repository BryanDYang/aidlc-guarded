#!/usr/bin/env python3
"""Send the merge-gate verdict to the watsonx Orchestrate governance agent.

Best-effort, fail-open: this NEVER blocks the gate. It builds one normalized
governance event (schema aidlc-governance-event/v1) from the verdict at
$VERDICT_JSON plus the DB_* metadata the workflow already exports, exchanges the
wxO API key for an IBM Cloud IAM bearer token, and POSTs the event to the wxO
agent's chat endpoint. The agent then records it in watsonx.governance and emails
on violation. Any failure here is logged and swallowed (exit 0) so a governance
or wxO outage can never freeze the trunk.

Multi-repo: the event carries `repo` and `project`, so a single wxO agent can
serve every repo and watsonx.governance can group by repo/project/actor/rule.

Env:
  VERDICT_JSON     path to the normalized verdict {"verdict","violations"[]}
  WXO_API_KEY      wxO / IBM Cloud API key (exchanged for an IAM token)
  WXO_AGENT_URL    full chat-completions URL of the governance agent
  WXO_IAM_URL      IAM token endpoint (default https://iam.cloud.ibm.com/identity/token)
  DB_PROJECT       logical project key for grouping (default derived from repo)
  DB_* (as dashboard-record.py) actor, pr, sha, repo, run url, timestamps...
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SEVERITY_ORDER = {"none": -1, "low": 0, "medium": 1, "high": 2, "critical": 3}


def severity_for(v):
    """Map a violation to a severity from its rule/detail/file text.

    Kept in sync with dashboard-record.py so the dashboard and wx.gov agree.
    """
    text = " ".join(str(v.get(k, "")) for k in ("rule", "detail", "file")).lower()
    if any(k in text for k in ("tamper", "governance", "canary", ".bob/", "rule 06", "06-")):
        return "critical"
    if any(k in text for k in ("secret", "api key", "apikey", "credential", "token", "01-secure")):
        return "critical"
    if any(k in text for k in ("sql", "injection", "f-string", "fstring", "format")):
        return "high"
    if any(k in text for k in ("delete", "destructive", "drop", "hard-delete", "rule 05", "05-")):
        return "high"
    if any(k in text for k in ("bulk", "unauthenticated", "tfc", "mass")):
        return "high"
    if any(k in text for k in ("aidlc", "planning", "inception", "blocker", "07-")):
        return "high"
    if any(k in text for k in ("library", "requirements", "unapproved", "rule 04", "04-")):
        return "medium"
    return "medium"


def load_verdict():
    path = os.environ.get("VERDICT_JSON")
    if path and os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
            return data.get("verdict", "UNPARSEABLE"), (data.get("violations") or [])
        except (json.JSONDecodeError, OSError):
            pass
    return "ERROR", []


def build_event():
    e = os.environ.get
    verdict, violations = load_verdict()
    for v in violations:
        v.setdefault("severity", severity_for(v))
    max_sev = "none"
    for v in violations:
        if SEVERITY_ORDER[v["severity"]] > SEVERITY_ORDER[max_sev]:
            max_sev = v["severity"]

    repo = e("DB_REPO", "")
    project = e("DB_PROJECT") or (repo.split("/")[-1].upper() if repo else "UNKNOWN")
    return {
        "schema": "aidlc-governance-event/v1",
        "source": "github-actions",
        "repo": repo,
        "project": project,
        "actor": e("DB_ACTOR", "unknown"),
        "triggered_by": e("DB_TRIGGERED_BY", ""),
        "pr_number": e("DB_PR_NUMBER", ""),
        "pr_title": e("DB_PR_TITLE", ""),
        "pr_url": e("DB_PR_URL", ""),
        "branch": e("DB_BRANCH", ""),
        "base_ref": e("DB_BASE", ""),
        "sha": e("DB_SHA", "")[:7],
        "commit_message": e("DB_COMMIT_MSG", ""),
        "verdict": verdict,
        "severity": max_sev if violations else ("none" if verdict == "PASS" else "high"),
        "violation_count": len(violations),
        "violations": violations,
        "run_url": e("DB_RUN_URL", ""),
        "timestamp": e("DB_TIMESTAMP") or datetime.now(timezone.utc).isoformat(),
    }


def iam_token(api_key, iam_url):
    data = urllib.parse.urlencode({
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }).encode()
    req = urllib.request.Request(
        iam_url, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["access_token"]


def post_to_agent(agent_url, token, event):
    # The agent takes a single user message whose content is the event JSON.
    body = json.dumps({
        "stream": False,
        "messages": [{"role": "user", "content": json.dumps(event)}],
    }).encode()
    req = urllib.request.Request(
        agent_url, data=body,
        headers={"Authorization": "Bearer " + token,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read().decode()[:500]


def main():
    event = build_event()
    print("governance event:", json.dumps(event)[:400])

    api_key = os.environ.get("WXO_API_KEY", "")
    agent_url = os.environ.get("WXO_AGENT_URL", "")
    iam_url = os.environ.get("WXO_IAM_URL", "https://iam.cloud.ibm.com/identity/token")
    if not api_key or not agent_url:
        print("WXO_API_KEY / WXO_AGENT_URL not set — skipping wxO notification "
              "(gate is unaffected).")
        return 0
    try:
        token = iam_token(api_key, iam_url)
        status, snippet = post_to_agent(agent_url, token, event)
        print(f"wxO agent responded HTTP {status}: {snippet}")
    except Exception as exc:  # noqa: BLE001 — fail-open by design
        print(f"wxO notification failed (ignored, gate unaffected): {exc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
