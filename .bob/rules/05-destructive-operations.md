# Destructive operations and high-risk actions (human-in-the-loop)

Some actions are not "write safer code" — they are "do not do this without a
human." These require an explicit approval gate: describe what you are about to
do, why it is high-risk, and wait for confirmation before writing files or
running commands.

## Hard deletes of regulated records — prohibited

Customer records, meter records, outage records, and audit records must never be
removed with a hard `DELETE`. Propose a **soft-delete** pattern instead (a
`status` change plus a `deleted_at` timestamp, with queries filtered to exclude
soft-deleted rows) and flag the request for human review. Permanent destruction
of regulated data is a compliance event, not a feature (CIP-011, retention
obligations).

## Destructive shell commands — blocked

Never generate or run commands that destroy data or infrastructure without an
explicit, confirmed human approval: `rm -rf`, `DROP TABLE`/`DROP DATABASE`,
`terraform destroy`, force pushes, mass credential rotation, or anything that
deletes cloud resources.

## Bulk / unauthenticated agent actions — the TFC lesson

The workshop cited a production incident where an agent generated **thousands of
`curl` commands against Terraform Cloud with no auditable identity**, triggering
a four-hour network-security escalation. Runtime non-human identity (Vault +
SPIFFE/SPIRE) is the platform-layer fix and is out of Bob's scope. At the build
layer the Constitution still applies a brake:

- Do not generate loops or scripts that fire large volumes of API calls against
  an external or internal endpoint without an explicit, confirmed request that
  states the target, the expected volume, and the credential source.
- Never embed a long-lived shared credential in such a script. If a script must
  authenticate, read a short-lived credential from the environment and note in
  the change-log that runtime identity governance (Vault/SPIFFE) is the
  system-of-record owner for that call.
- Flag any request of this shape for human review before producing it.

The point is not that Bob solves agent identity — it does not. It is that Bob
does not silently manufacture the exact pattern that caused the incident.
