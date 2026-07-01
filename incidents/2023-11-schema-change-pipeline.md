---
title: Silent data pipeline failure from an upstream schema change
date: "2023-11"
severity: SEV2
client: Fintech client, internal reporting pipeline
---
**Symptom**

Dashboards quietly showed stale numbers for roughly six hours. No alerts fired.

**Investigation**

Worked backward through consumer logs and found an upstream schema change that broke message parsing for one consumer — but the consumer kept acknowledging messages instead of failing loudly.

**Root cause**

The consumer swallowed parsing errors instead of surfacing them, so broken messages were silently dropped rather than retried or flagged.

**Fix**

Patched the consumer to fail loudly on parse errors and backfilled the missing six hours of data.

**Prevention**

Added schema validation at the pipeline boundary, a dead-letter queue for unparseable messages, and alerting on message-age drift.
