#!/usr/bin/env python3
"""Parse the machine-readable verdict out of the Bob audit output.

Reads the raw audit output on stdin, finds the LAST JSON object containing a
"verdict" key, validates it, and writes a markdown summary to the path given
as argv[1] (for the PR comment).

Fail-closed contract:
  exit 0  -> verdict PASS
  exit 2  -> verdict FAIL (violations listed)
  exit 3  -> no parseable verdict (treated as failure by the workflow)

Side output: if the VERDICT_JSON environment variable is set, the normalized
verdict object ({"verdict": ..., "violations": [...]}) is also written there, so
the dashboard-recording step has a clean machine-readable payload to enrich.
"""

import json
import os
import re
import sys


def main():
    raw = sys.stdin.read()
    summary_path = sys.argv[1] if len(sys.argv) > 1 else None

    verdict = None
    for m in re.finditer(r"\{[^{}]*\"verdict\"(?:[^{}]|\{[^{}]*\})*\}", raw):
        try:
            candidate = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if candidate.get("verdict") in ("PASS", "FAIL"):
            verdict = candidate

    if verdict is None:
        write_summary(summary_path, "UNPARSEABLE", [], raw)
        write_verdict_json("UNPARSEABLE", [], raw)
        print("FAIL-CLOSED: no parseable verdict in audit output.")
        sys.exit(3)

    violations = verdict.get("violations") or []
    write_summary(summary_path, verdict["verdict"], violations, raw)
    write_verdict_json(verdict["verdict"], violations, raw)

    if verdict["verdict"] == "PASS":
        print("Bob audit verdict: PASS")
        sys.exit(0)
    print(f"Bob audit verdict: FAIL ({len(violations)} violation(s))")
    for v in violations:
        print(f"  - {v.get('file', '?')}: {v.get('detail', '?')} [{v.get('rule', '?')}]")
    sys.exit(2)


def write_summary(path, verdict, violations, raw):
    if not path:
        return
    lines = ["## Guardrail audit", "", f"**Verdict: {verdict}**", ""]
    if verdict == "UNPARSEABLE":
        lines += [
            "The audit produced no machine-readable verdict, so the gate",
            "fails closed. Raw output tail:",
            "```",
            raw[-1500:],
            "```",
        ]
    elif violations:
        lines.append("| File | Rule | Detail |")
        lines.append("|---|---|---|")
        for v in violations:
            lines.append(
                f"| `{v.get('file', '?')}` | {v.get('rule', '?')} | {v.get('detail', '?')} |"
            )
    else:
        lines.append("No rule violations found in the diff.")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def write_verdict_json(verdict, violations, raw):
    path = os.environ.get("VERDICT_JSON")
    if not path:
        return
    payload = {"verdict": verdict, "violations": violations}
    if verdict == "UNPARSEABLE":
        payload["raw_tail"] = raw[-1500:]
    with open(path, "w") as f:
        json.dump(payload, f)


if __name__ == "__main__":
    main()
