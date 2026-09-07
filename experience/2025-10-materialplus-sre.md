---
role: Site Reliability Engineer
company: Material+
start: "2025-10"
---
- Sole SRE owner for a multi-tenant GenAI platform spanning 11 production client environments on Amazon EKS and EC2; resolved 30+ production incidents by root-causing systemic failures — stale pod IPs in NGINX ingress pools (HTTP 503s), node memory limits, expired SSL certificates, and stuck ingestion pipelines — and adding automated recovery.
- Managed Terraform IaC for three enterprise client accounts; resolved state drift, imported unmanaged Azure resources into state, and performed zero-downtime EKS/AKS cluster and AMI upgrades.
- Designed a cross-account, tag-driven RDS/Aurora/DocumentDB start-stop automation (Terraform, Lambda, EventBridge Scheduler) with Aurora 7-day auto-restart handling, per-instance override tags, SNS failure alerts, and a kill switch — cutting non-production DB compute costs by 70%.
- Led recurring AWS/Azure cost-optimization audits, identifying $36,000 in annualized savings opportunities.
- Integrated automated Prowler security scans into Bitbucket Pipelines and triaged 3,400+ findings; remediated Tenable findings and Apache CVEs, enforced SQS/SNS encryption, and built cron-based ingestion pipeline monitoring with automated recovery.
