# Operations artifact template → aidlc-docs/<feature>/03-operations.md

```
# Operations — <feature name>
Date: <YYYY-MM-DD>   Construction approved: <yes + when>

## Deployment & rollback
- Deploy steps: <...>
- Rollback: <...>
- Configuration / baseline change (CIP-010 R1): <what changed>

## Observability
- Log: <events / fields>
- Alert on: <conditions>
- Runbook: <link or steps>

## Handoff to the platform layer (honest scope)
These runtime concerns are NOT owned by Bob or this workflow. Named here and
handed off — not faked:
- Non-human identity for any service/API calls this feature makes
  → IBM Vault + SPIFFE/SPIRE (Gap 3). Owner: <team>.
- Cross-agent audit spine / A2A policy enforcement
  → watsonx Orchestrate + IBM Confluent (Gap 4). Owner: <team>.
- Runtime policy drift detection across all IDEs
  → watsonx.governance. Owner: <team>.

## GATE
Documented, not deployed. Regulated-environment deploys do not originate from
the IDE. Awaiting human sign-off.
```
