---
checksum_sha256: 2fb1be425f03ad088ede8c9dc54829d40dcde1e28b821af49b8dba3fcc94c417
contract: delivery.operations
customer: Tele-MANAS
generated_at: '2026-09-30T14:58:23.163653+00:00'
generated_by: delivery-engine
opportunity: OPP-number2
project_id: number2
provenance:
  source_documents:
  - Architecture solution baseline (SOLUTION_BASELINE) for Tele-MANAS OPP-number2
  - Architecture Low-Level Design (LLD) — component detail and runbooks R-001..R-016
  - RFP IIITB/EHRC/2022/IT-01 (25-Oct-2022) — untrusted reference excerpts covering
    SLA/penalties (RFP §8.18–8.20), subcontracting (RFP §8.37), staffing profile,
    Steering Committee, certification and eligibility clauses, and commercial/EMD
    terms
stage: delivery
status: draft
version: 1
---

# Operations — Tele-MANAS (OPP-number2)

> Source: Solution Baseline §1, §3, §5; LLD runbooks R-001..R-016.

## 1. Service Description
The Tele-MANAS service delivers multilingual mental-health teleconsultation via IVR, mobile and web channels integrated with E-Sanjeevani, ABDM, and E-Manas EHR. Operations cover components COMP-001..COMP-015.

## 2. SLO / SLA Targets (placeholders — final values from TASK-002 / DEC-002)

| SLO | Target | Measurement Source | Reporting |
|-----|--------|--------------------|-----------|
| Platform availability | ≥ 99.5% monthly | COMP-010 uptime | COMP-006 dashboard |
| IVR answer time (P50/P95) | ≤ 5s / ≤ 15s | COMP-010/015 | Daily |
| Mobile/web API latency P95 | ≤ 800 ms | COMP-010 | Daily |
| E-Sanjeevani session success | ≥ 95% | TEST-002 baseline | Weekly |
| ABDM conformance uptime | ≥ 99.0% | COMP-004 | Daily |
| EHR read/write P95 | ≤ 500 ms | COMP-005/010 | Daily |
| Security patch SLA — critical | ≤ 7 days | COMP-011 | Weekly |
| Incident response — Sev1 | Ack ≤ 15 min, mitigate ≤ 4 h | COMP-012 | Real-time |
| Grievance acknowledgement | ≤ 3 working days | COMP-012 | Weekly |
| Grievance resolution | ≤ 30 working days | COMP-012 | Weekly |
| DR RTO / RPO | Per agreed target (TEST-010) | COMP-002/005/013 | Quarterly drill |

## 3. Monitoring Stack (COMP-010)
- Metrics: Prometheus + Thanos for long-term retention.
- Logs: EFK with PHI redaction via DLP rules (COMP-013).
- Traces: OpenTelemetry across COMP-001..COMP-009.
- APM: business KPIs (sessions, escalations, consent denials).
- Synthetic probes: IVR dials every 5 min, mobile/web heartbeat every 60 s.

## 4. Alerting Matrix

| Alert | Condition | Route | Runbook |
|-------|-----------|-------|---------|
| P1 — Platform down | Availability < 95% over 5 min | L2 on-call → PM → Customer | R-003, R-011 |
| P1 — IVR outage | > 10% calls failing | L2 + Commercial IVR vendor | R-001, R-016 |
| P2 — ABDM throttle | Error rate > 5% | Integration team | R-005 |
| P2 — E-Sanjeevani degradation | Success < 95% over 15 min | Integration team | R-004 |
| P2 — EHR latency breach | P95 > 1s for 10 min | SRE + EHR team | R-006 |
| P3 — Dashboard stale | KPI lag > 30 min | SRE | R-007 |
| Security — break-glass used | JIT elevation | Security on-call | R-010 |
| Compliance — key rotation overdue | > 90 days | Security on-call | R-014 |
| DR — replication lag | > 5 min | SRE | R-006 |

## 5. Runbooks (LLD §R-001..R-016)
| ID | Runbook | Component | Trigger |
|----|---------|-----------|---------|
| R-001 | IVR failover | COMP-001/015 | IVR outage |
| R-002 | Channel health checks | COMP-001 | Periodic / alert |
| R-003 | Session failover, queue drain | COMP-002 | Core outage |
| R-004 | Partner outage, retry-with-backoff | COMP-003 | E-Sanjeevani degradation |
| R-005 | Consent failure, audit evidence | COMP-004 | ABDM consent failure |
| R-006 | Restore drill, RTO/RPO validation | COMP-005 | DR exercise |
| R-007 | KPI integrity checks | COMP-006 | Stale data |
| R-008 | Content staging, version rollback | COMP-007 | LMS content issue |
| R-009 | Replay, DLQ inspection | COMP-008 | Broker outage |
| R-010 | Break-glass procedure | COMP-009 | IdP failure |
| R-011 | Restore observability pipeline | COMP-010 | Telemetry loss |
| R-012 | Rollback procedure | COMP-011 | Failed release |
| R-013 | Escalation matrix (grievance) | COMP-012 | Ticket breach risk |
| R-014 | Key rotation, incident response | COMP-013 | Rotation due / incident |
| R-015 | Per-state rollback | COMP-014 | Tenant failure |
| R-016 | IVR vendor failover | COMP-015 | Vendor outage |

## 6. Escalation Matrix

| Level | Role | Response Time | Authority |
|-------|------|---------------|-----------|
| L1 | Service desk agent | ≤ 15 min acknowledge | Log, categorise, route |
| L2 | On-call engineer | ≤ 30 min acknowledge | Mitigate, invoke runbook |
| L3 | Integration / SRE lead | ≤ 1 h acknowledge | Code/config change |
| L4 | Delivery Manager | ≤ 2 h acknowledge | Customer comms, change board |
| L5 | Steering Committee chair | Next business day | Major incident / contractual |

## 7. Operational Cadence
- 24×7 L1/L2 coverage (COMP-012, Bengaluru on-site + remote per TASK-008).
- Daily SRE huddle, weekly change advisory board.
- Monthly Steering Committee (TASK-015).
- Quarterly DR drill (TEST-010).
- Annual ISO 27001 surveillance audit (TEST-012).

## 8. Compliance & Audit Operations
- ABDM HIE-CM conformance attestation renewal annually (TEST-003).
- ISO 27001 surveillance (TEST-012).
- Subcontractor audits against RFP §8.37 caps (TASK-013).
- Liquidated damages tracking via SLA evidence logging (TASK-014, RSK-009).
- All audit events retained immutably per COMP-005/013.

## 9. Operational Risks
See Solution Baseline §5 (RSK-001..RSK-010). Operational mitigations are embedded in the runbooks above and the alert matrix in §4.