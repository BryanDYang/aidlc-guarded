#!/usr/bin/env python3
"""Build one enriched dashboard record from a verdict + PR/user metadata and
append it to the dashboard log (a JSON array).

Reads the normalized verdict written by parse-verdict.py at $VERDICT_JSON. If
that file is missing (the audit job errored before producing one), the record is
recorded as verdict ERROR so nothing is silently dropped. PR/commit/user
metadata comes from DB_* environment variables set by the workflow from the
GitHub Actions event context.

Usage:  dashboard-record.py <violations.json>   # appends one record in place
"""

import json
import os
import sys
from datetime import datetime, timezone

SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def severity_for(v):
    """Map a violation to a severity from its rule/detail/file text."""
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
    if any(k in text for k in ("header", "compliance", "rule 02", "02-", "validation", "input")):
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
    # Job errored before a verdict existed — record it, don't drop it.
    return "ERROR", []


def main():
    if len(sys.argv) < 2:
        print("usage: dashboard-record.py <violations.json>", file=sys.stderr)
        sys.exit(1)
    log_path = sys.argv[1]

    verdict, violations = load_verdict()
    for v in violations:
        v["severity"] = severity_for(v)
    max_sev = "low"
    for v in violations:
        if SEVERITY_ORDER[v["severity"]] > SEVERITY_ORDER[max_sev]:
            max_sev = v["severity"]

    e = os.environ.get
    record = {
        "id": f"{e('DB_RUN_ID', '')}-{e('DB_SHA', '')[:7]}",
        "timestamp": e("DB_TIMESTAMP") or datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "severity": max_sev if violations else ("none" if verdict == "PASS" else "high"),
        "violation_count": len(violations),
        "violations": violations,
        "actor": e("DB_ACTOR", "unknown"),
        "triggered_by": e("DB_TRIGGERED_BY", ""),
        "pr_number": e("DB_PR_NUMBER", ""),
        "pr_title": e("DB_PR_TITLE", ""),
        "pr_url": e("DB_PR_URL", ""),
        "branch": e("DB_BRANCH", ""),
        "base_ref": e("DB_BASE", ""),
        "sha": e("DB_SHA", "")[:7],
        "commit_message": e("DB_COMMIT_MSG", ""),
        "repo": e("DB_REPO", ""),
        "run_url": e("DB_RUN_URL", ""),
    }

    try:
        with open(log_path) as f:
            log = json.load(f)
        if not isinstance(log, list):
            log = []
    except (FileNotFoundError, json.JSONDecodeError):
        log = []

    # Newest first; de-dup by id so a re-run of the same job replaces its record.
    log = [r for r in log if r.get("id") != record["id"]]
    log.insert(0, record)

    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

    print(f"recorded: {record['verdict']} for PR #{record['pr_number']} "
          f"by {record['actor']} ({record['violation_count']} violation(s))")


if __name__ == "__main__":
    main()
