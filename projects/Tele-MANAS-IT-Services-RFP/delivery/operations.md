---
checksum_sha256: 4fdd3d37b80f76a70c711c9b32c40645ddd9f4ee2e904f561edf368312a34fac
contract: delivery.operations
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:06:42.109063+00:00'
generated_by: delivery-engine
opportunity: OPP-TeleMANAS-001
project_id: Tele-MANAS-IT-Services-RFP
provenance:
  source_documents:
  - Architecture Blueprint — Tele-MANAS IT Services (DOC-B585FB4B498A) — Components,
    Tasks, Tests, Rollout, Acceptance, Risks, Dependencies
  - Architecture LLD — Tele-MANAS IT Services — per-component detailed design
  - 'RFP IIITB/EHRC/2022/IT-01, 25-Oct-2022 — Software Development and Platform Support
    Services for National Tele-Mental Health Initiative (retrieved excerpts: contents,
    glossary, eligibility, envelope structure, audit/inspection rights, governance,
    cover letter, Bangalore self-declaration context, indicative role-mix Annexure
    9)'
  - Opportunity record OPP-TeleMANAS-001
stage: delivery
status: draft
version: 1
---

# Operations Manual — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore

This document defines the operational posture: monitoring, alerting, SLO/SLA targets (placeholders pending F-01), runbooks, and escalation matrix.

---

## 1. SLO / SLA Targets

> Placeholder values below pending IIITB confirmation per F-01. Penalty cap and severity definitions to be finalised during contract finalisation (R-02).

| Service | Indicator | Target (placeholder) | Measurement |
|---------|-----------|----------------------|-------------|
| Platform availability | Uptime per month | ≥ 99.X% | APM availability SLO board |
| Teleconsultation session success | Sessions completed without error | ≥ 99.X% | Application logs |
| API latency | p95 response time | ≤ X ms | APM |
| Incident response — Critical (Sev-1) | Acknowledgement | ≤ 15 min | ITSM |
| Incident response — Critical (Sev-1) | Mitigation / workaround | ≤ X hrs | ITSM |
| Incident response — High (Sev-2) | Acknowledgement | ≤ 30 min | ITSM |
| Incident resolution — Sev-2 | Resolution | ≤ X hrs | ITSM |
| Change release lead time | Notice before go-live | ≥ X business days | Release calendar |
| DR RTO / RPO | Recovery time / point | TBD per F-01 | DR drill (TEST-009) |
| Audit findings closure | Critical findings | ≤ 30 days | Audit tracker |
| Steering Committee cadence | Frequency | Per F-07 confirmation | Meeting minutes |

---

## 2. Monitoring Stack (per COMP-002, COMP-009)

- **APM:** application performance (latency, throughput, errors).
- **Infrastructure metrics:** CPU, memory, disk, network.
- **SIEM:** centralised logs, correlation, alerting.
- **Synthetic monitoring:** key user journeys (teleconsultation, grievance).
- **Real-user monitoring:** session quality.
- **Uptime monitoring:** external probes.
- **Audit log integrity:** tamper-evident hashes (COMP-001 AuditEvent).

---

## 3. Alerting & Severity Matrix

| Severity | Definition | Initial Response | Customer Notification |
|----------|-----------|------------------|-----------------------|
| Sev-1 (Critical) | Total outage, PHI exposure risk, breach | Immediate on-call page | Within 15 min to IIITB PMO + Security |
| Sev-2 (High) | Major degradation, integration failure | 30 min ack | Within 1 hr to IIITB PMO |
| Sev-3 (Medium) | Partial degradation, workaround available | 2 hr ack | Daily summary |
| Sev-4 (Low) | Minor issue, cosmetic, info | Next business day | Weekly summary |

**Alerting channels:** SIEM → ITSM → on-call rota (TASK-103) → IIITB PMO.

---

## 4. Runbooks (by Component)

### COMP-001 — Application Platform
1. Detect alert (5xx surge, latency, error rate).
2. On-call L1 triage; escalate L2.
3. Roll back to last green release (COMP-006).
4. Open incident; notify IIITB PMO.
5. If PHI impact suspected → trigger COMP-010 IR.

### COMP-002 — L1/L2 Support
1. Receive ticket via ITSM/phone.
2. Triage by severity; assign SLA timer.
3. Run SOP; escalate to L2/Level 3/IIITB per matrix.
4. Resolve, document, close.
5. Weekly trend report to PMO (COMP-013).

### COMP-003 — Integration & Test Harness
1. PR triggers integration test pipeline.
2. Failures triaged; quarantine flaky.
3. Coordinate deployment-script co-authoring with Level 3.
4. Communicate integration partner downtime to IIITB.

### COMP-005 — Migration & Upgrade
1. Plan with IIITB (COMP-013).
2. Stage in pre-prod; run validation tests (TEST-011).
3. Execute canary in prod.
4. Monitor SLOs; rollback if KPIs breach.
5. Capture lessons-learned.

### COMP-006 — Release & Deployment
1. Create release branch.
2. Generate release notes.
3. Deploy to canary.
4. Validate SLOs.
5. Promote or rollback.
6. Publish known issues.

### COMP-007 — Defect Management
1. Triage defect.
2. Assign severity/SLA.
3. Fix; verify; close.
4. Capture root cause; update tech-debt register.

### COMP-008 — Commercial Operations
1. Receive commercial change request.
2. Validate against line-item rates and quantity governance.
3. Apply pass-through if triggered (TASK-210).
4. Update contract ops record.

### COMP-009 — Security Audit
1. Conduct scheduled audit.
2. Capture findings; track remediation.
3. Report to IIITB PMO.

### COMP-010 — Confidentiality / Breach Response
1. Classify data asset involved.
2. Contain; preserve evidence.
3. Trigger breach notification matrix.
4. Coordinate disclosure with IIITB.
5. Post-incident review.

### COMP-011 — Bangalore Facility
1. Quarterly compliance attestation.
2. Clean-desk audits; visitor log review.
3. Relocation / onsite exception handling.

### COMP-013 — Steering Committee
1. Prepare monthly status pack.
2. Present to SC.
3. Capture minutes; circulate to PMO.

### COMP-014 — Accessibility
1. Accessibility audit per release (TEST-008).
2. Language coverage review.
3. Low-bandwidth test.

---

## 5. Escalation Matrix

| Level | Role | When to Escalate | Response SLA |
|-------|------|------------------|--------------|
| L1 | Service Desk | All inbound | Per severity |
| L2 | On-call Engineer | L1 cannot resolve within SLA | Per severity |
| L3 | Level 3 team (TMC/GRS/CTI/EHR owners) | Integration / deployment-script issues | Per partner agreement (F-08) |
| Bidder Tech Lead | Tech Lead | Sev-2+ not resolved within SLA | Within 1 hr |
| Bidder Security Lead | Security Lead | Suspected breach / Sev-1 security event | Immediate |
| Bidder Delivery Manager | Delivery Manager | Cross-component impact; risk to renewal | Same business day |
| IIITB PMO | PMO | Customer-facing impact; renewal-affecting | Within SLA window |
| Steering Committee | SC Chair | Strategic decisions; unresolved escalations | Per cadence |

---

## 6. On-Call & Shift Coverage

- Shift pattern pending F-09 (R-10 mitigation).
- On-call rota maintained in ITSM.
- Holiday coverage matrix; cross-shift backup.

---

## 7. Backup, DR, and Business Continuity

- Backup frequency and retention per RPO (pending F-01).
- DR drill quarterly (TEST-009).
- Multi-AZ redundancy for production.
- Failover tested in pre-prod (TEST-011).

---

## 8. Audit & Compliance Operations

- Quarterly internal audit (TASK-204).
- Annual external audit (TEST-007).
- Audit evidence pack walk-through (TEST-013).
- Regulator/IIITB inspection rights honoured.

---

## 9. Change & Release Management

- All releases go through CI gates (TEST-001, TEST-002, TEST-006).
- Canary → full rollout.
- Post-release monitoring window (AC-06).
- Known-issues register published.

---

## 10. Commercial Operations

- Quarterly market price benchmarking (TASK-210) → pass-through trigger matrix.
- Quantity alteration tracking with ceiling alerts.
- Renewal evidence pack assembled monthly, frozen at renewal gate (TASK-211).
- "No Claim" certificate workflow at closure (REQ-017).