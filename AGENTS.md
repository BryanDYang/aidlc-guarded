# Project context — Utility Co Grid Services API (governed)

This is a small Flask outage and customer-service API for a fictional PG&E grid
operations desk. It tracks customers, their meters, and grid outages, with a
couple of reporting endpoints. Endpoints live under `api/` as Flask blueprints;
SQLite storage, schema in `db.py`, sample data in `seed.py`. Help the developer
extend it.

## Governance — read this first

All AI-assisted work in this repo is bound by the **Utility Co AI Safe Constitution**
in `.bob/rules/`. Those rules are non-negotiable and apply to every request in
every mode. Prefer to refuse a request or propose a compliant alternative over
violating a rule. Every change writes a `change-log/` entry (rule 03).

For multi-phase feature work, use the **AIDLC skill** (`.bob/skills/aidlc/`):
say "Using AIDLC, ..." to run the Inception → Construction → Operations
workflow. The skill operates inside the Constitution — governance and workflow
are layered, not alternatives.
