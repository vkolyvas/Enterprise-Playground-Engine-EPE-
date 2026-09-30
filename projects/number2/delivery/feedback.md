---
checksum_sha256: b2229a3df730553e80a63004a021d235ba83990b97886839f08294bf26e718a1
contract: delivery.feedback
customer: Tele-MANAS
generated_at: '2026-09-30T14:58:23.206996+00:00'
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

# Delivery Feedback — Tele-MANAS (OPP-number2)

> Consumed by Product and Architecture to refine the next release cycle. Each item links to a REQ/COMP/TASK/TEST identifier.

## 1. Feedback Capture Channels
- Customer satisfaction surveys (quarterly).
- L1/L2 ticket trends (COMP-012).
- Incident post-mortems (linked to COMP-010, COMP-012).
- Cost variance reports from PMO.
- Deployment telemetry from DevSecOps (COMP-011).
- Operational lessons logged by SRE.

## 2. Feedback Register

| FB-ID | Date | Category | Description | Linked REQ | Linked COMP | Linked TASK | Linked TEST | Owner | Action / Resolution | Status |
|-------|------|----------|-------------|------------|-------------|-------------|-------------|-------|---------------------|--------|
| FB-001 | TBD | Incident | (Example) P1 IVR outage on DD-MM-YYYY | REQ-001 | COMP-001, COMP-015 | TASK-007 | TEST-001 | SRE | Triggered R-001/R-016; failover to secondary IVR; root cause analysis attached | Open |
| FB-002 | TBD | Cost variance | (Example) Hybrid cloud cost overrun vs plan | REQ-003 | COMP-002, COMP-010 | TASK-005 | TEST-007 | PM | Capacity model re-baselined; rightsizing initiative raised to CAB | Open |
| FB-003 | TBD | Usage telemetry | (Example) Mobile channel adoption 35% lower than forecast in pilot State | REQ-001 | COMP-001 | TASK-007 | TEST-013 | Product | UX research commissioned; language pack gap analysis | Open |
| FB-004 | TBD | Deployment problem | (Example) Blue/green rollback exceeded 5-min target during release vX.Y.Z | REQ-008 | COMP-011 | TASK-009 | TEST-008 | DevSecOps | R-012 invoked; health-check tuning ticket raised | Open |
| FB-005 | TBD | Customer feedback | (Example) State cell requests offline mode for counsellor workflow | REQ-001, REQ-005 | COMP-001, COMP-006 | TASK-007 | TEST-001, TEST-005 | Product | Logged as candidate for M+1 backlog; prioritisation at next CAB | Open |
| FB-006 | TBD | Operational lesson | (Example) ABDM consent artefact storage grew faster than projected | REQ-007 | COMP-004 | TASK-004 | TEST-003 | Integration | Storage tiering proposal raised to Architecture | Open |
| FB-007 | TBD | SLA | (Example) One month missed IVR P95 due to commercial vendor outage | REQ-001, REQ-009 | COMP-015 | TASK-007 | TEST-001 | PM | Penalty modelled per RSK-009; vendor risk register updated | Open |
| FB-008 | TBD | Security | (Example) JIT break-glass used twice in quarter — governance review | REQ-011 | COMP-009, COMP-013 | TASK-010 | TEST-006 | Security | Quarterly access review tightened; report to Steering | Open |
| FB-009 | TBD | Subcontracting | (Example) Sub-vendor change requires RFP §8.37 review | All | — | TASK-013 | — | Delivery Manager | Vendor risk register updated; flow-down clauses re-checked | Open |
| FB-010 | TBD | Compliance | (Example) ISO 27001 surveillance finding — minor non-conformance | REQ-011 | COMP-013 | TASK-003 | TEST-012 | Security | Remediation plan accepted by auditor; closure tracked | Open |

## 3. Trending & Themes
(Updated monthly by PMO. Themes to call out:)
- Channel adoption vs. forecast
- SLA attainment vs. target
- Security findings severity mix
- Cost-to-serve per session
- Time-to-rollout per State/UT
- Subcontractor concentration (RSK-010)

## 4. Routing
- Product-impact items → Product Manager for backlog prioritisation.
- Architecture-impact items → Enterprise Architect for next LLD iteration.
- Operational items → SRE for runbook/alert tuning.
- Commercial items → PM + commercials lead.
- Security/compliance items → Security Lead for audit trail.

## 5. Closing the Loop
Each FB-ID must be reviewed at the monthly PMO meeting, with status update and named owner. Lessons that affect the Solution Baseline or LLD must be promoted to Architecture via formal change request.