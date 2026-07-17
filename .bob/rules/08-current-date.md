# Current date and time — always read it from the system

Never assume the date from training, and never carry over a training-cutoff year.
Before writing any dated value — a `change-log/YYYY-MM-DD_HHMM_*.md` filename
(rule 03), an `aidlc-docs/` plan, a compliance-header `Reviewed:` date, or any
timestamp — first read the real current date and time from the system clock:

    date -u +"%Y-%m-%d %H:%M UTC"      # timestamp
    date +"%Y-%m-%d_%H%M"              # change-log filename form

Use the value the command returns verbatim. Do not fabricate, guess, or infer the
date from context. If the command cannot be run, ask the user for the current date
rather than assuming one.
