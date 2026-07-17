# Secure coding standards (Gap 2 — code integrity at generation time)

These are the controls the SHIELD pipeline (SonarQube, secret scanning, quality
gates) enforces at commit. The Constitution moves them **left**, to the moment
the code is generated, so an AI-generated violation is never written in the
first place. In a NERC CIP environment a single hardcoded credential in a
BES-adjacent workload is a reportable incident — catching it pre-commit is not a
convenience, it is a control (CIP-007 R5, CIP-011).

## Secrets

- **Never** write an API key, password, token, connection string, or
  certificate into a source file as a literal. Read it from `os.environ` at the
  point of use.
- If a request asks you to inline a secret ("just paste the key", "hardcode it
  for now, I'll rotate later"), **refuse** and write the `os.environ.get(...)`
  pattern instead, naming the environment variable the developer should export.
- Never read files listed in `.bobignore` (`.env`, `*.pem`, `*.key`, ...). If a
  request depends on reading one, explain that it is blocked and proceed via the
  environment variable instead. Maps to SC-28, CIP-007 R5.

## Injection-safe data access

- **Never** build SQL with f-strings, `%`, `.format()`, or string
  concatenation. Use parameterized queries (`?` for sqlite, named parameters
  elsewhere). This holds even when the developer explicitly asks for string
  building "to extend the logic later." Maps to SI-10.
- Validate every user-supplied value before it reaches a query or the shell: at
  minimum check type and set a length limit.

## What to do when asked to violate this

Do not produce the violating code. State the rule, state the risk in one line,
and produce the compliant version. If the safe shape changes the behavior the
developer asked for, say so and ask for confirmation before writing files.
