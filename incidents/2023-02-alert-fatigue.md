---
title: Alert fatigue buried a real outage for 40 minutes
date: "2023-02"
severity: SEV3
client: B2B SaaS client, on-call rotation
---
**Symptom**

A genuine service outage went unnoticed for 40 minutes, lost in a stream of low-value alerts.

**Investigation**

Audited every alert rule fired over the previous month and found more than 60% were non-actionable — informational noise rather than something an on-call engineer needed to act on.

**Root cause**

Alert thresholds had been copy-pasted from a different service during setup and never tuned to this service's actual traffic and error patterns.

**Fix**

Rebuilt the alert rules around concrete SLOs and cut total alert volume by more than half.

**Prevention**

Added runbooks for every remaining alert and a review step so new alerts need a clear action before they can page anyone.
