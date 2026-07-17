# Approved third-party libraries (supply-chain governance)

AI agents readily reach for whatever library a tutorial used. Unreviewed
dependencies are a software supply-chain exposure and a CIP-010 R1.1 baseline
deviation. Only libraries on this allowlist may be added to `requirements.txt`.

If asked to add something not on the list, **refuse**, name the closest approved
equivalent, and surface the exact `pip install` command so the developer can
review it before approving. Never install silently.

## Approved

- flask (web framework)
- sqlalchemy (database ORM)
- pydantic (validation)
- requests (HTTP client)
- python-dotenv (env loading)
- reportlab (PDF generation)
- openpyxl (xlsx I/O)
- pytest, pytest-cov (testing)
- ruff, mypy (linting and types)
- structlog (structured logging)

## Common substitutions to propose

| If asked for... | Propose instead | Why |
|-----------------|-----------------|-----|
| fpdf / fpdf2    | reportlab       | approved PDF path |
| pandas (for a CSV read) | csv (stdlib) / openpyxl | avoid a heavy unreviewed dep for a light task |
| a raw driver + manual SQL | sqlalchemy | keeps queries parameterized (rule 01) |

Adding a library is a configuration change: it must also produce a change-log
entry (rule 03) with the CM-2 / CIP-010 R1 control noted.
