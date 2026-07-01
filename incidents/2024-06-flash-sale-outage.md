---
title: Cascading failure during a flash-sale traffic spike
date: "2024-06"
severity: SEV1
client: E-commerce platform, ~5M monthly users
---
**Symptom**

Checkout latency spiked within minutes of a promotional traffic surge, followed by a wave of 500 errors across the checkout service.

**Investigation**

Traced request timeouts back to the database layer, where connections were queuing far past the configured pool limits with no backpressure to slow incoming traffic.

**Root cause**

An undersized connection pool combined with no backpressure or queueing meant a normal traffic spike behaved like a denial-of-service event.

**Fix**

Added a request queue in front of checkout, resized the pool, and configured autoscaling triggers ahead of the next promotional event.

**Prevention**

Added load testing to the pre-launch checklist for any marketing event, plus connection-pool saturation alerts tied to an SLO.
