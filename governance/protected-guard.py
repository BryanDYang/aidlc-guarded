#!/usr/bin/env python3
"""Deterministic governance guard — a pure path check, no model judgment.

Reads changed file paths (one per line) on stdin. If any touch a protected,
admin-only governance path, writes a FAIL verdict (to $VERDICT_JSON and to the
markdown summary path in argv[1]) and exits 2. Otherwise exits 0.

Protected paths: everything under `.bob/`, plus `.bobignore`, `governance/`, and
`.github/`. These define the controls and can only change via an admin push to
main, never through a pull request. This runs before the LLM audit so tampering
is blocked by math, not by a model's opinion.
"""

import json
import os
import re
import sys

PROTECTED = re.compile(r"^(\.bob/|\.bobignore$|governance/|\.github/)")


def main():
    changed = [l.strip() for l in sys.stdin if l.strip()]
    hits = [f for f in changed if PROTECTED.match(f)]
    summary_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not hits:
        print("Deterministic guard: no protected governance files touched.")
        sys.exit(0)

    detail = ("Protected governance file modified in a pull request; the .bob/, "
              "governance/, .github/, and .bobignore paths are admin-only and "
              "cannot change through a PR (deterministic block).")
    violations = [{"file": f, "rule": "06-governance-protection.md", "detail": detail}
                  for f in hits]

    vj = os.environ.get("VERDICT_JSON")
    if vj:
        with open(vj, "w") as f:
            json.dump({"verdict": "FAIL", "violations": violations}, f)

    if summary_path:
        lines = ["## Guardrail audit", "", "**Verdict: FAIL**", "",
                 "Deterministic governance guard — this PR modifies protected, "
                 "admin-only governance files and cannot merge.", "",
                 "| File | Rule | Detail |", "|---|---|---|"]
        for f in hits:
            lines.append(f"| `{f}` | 06-governance-protection.md | "
                         "Protected governance file modified in a PR (deterministic block). |")
        with open(summary_path, "w") as f:
            f.write("\n".join(lines) + "\n")

    print("Deterministic guard FAIL — protected files touched:")
    for f in hits:
        print("  " + f)
    sys.exit(2)


if __name__ == "__main__":
    main()
