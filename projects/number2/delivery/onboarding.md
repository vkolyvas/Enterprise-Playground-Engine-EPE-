---
checksum_sha256: d933c3fc31d39a9677a4c82997ac28c5cd4f976fe648bbac3d603b9a43c7c963
contract: delivery.onboarding
customer: Tele-MANAS
generated_at: '2026-09-30T14:58:23.163099+00:00'
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

# Customer Onboarding — Tele-MANAS (OPP-number2)

> Audience: IIITB / Tele-MANAS programme office, State/UT cell coordinators, MHPs, counsellors, L1 support agents.

## 1. Welcome and Scope
This document explains how your teams will be brought onto the Tele-MANAS platform built under RFP IIITB/EHRC/2022/IT-01. Onboarding covers the Citizen Channel (COMP-001), Tele-MANAS Core (COMP-002), Governance Dashboard (COMP-006), Training module (COMP-007), and L1/L2 support (COMP-012).

## 2. Onboarding Phases

| Phase | Duration | Activities | Owner |
|-------|----------|-----------|-------|
| O-1 Programme kick-off | Week 0 | Steering Committee alignment, RACI confirmation, communications plan | PMO |
| O-2 Identity & access | Week 1–2 | IIITB IdP account provisioning, ABHA linking for staff, RBAC assignment (COMP-009) | Security Lead |
| O-3 Training | Week 2–6 | MHP certification, counsellor workflow, L1 agent certification via COMP-007 LMS | Training Lead |
| O-4 Channel orientation | Week 4–6 | Mobile/web citizen app walk-through, IVR prompts in supported languages | Product Manager |
| O-5 Governance review | Week 6 | Dashboard walkthrough, KPI dictionary (COMP-006), grievance workflow | PMO |
| O-6 Pilot State onboarding | Week 6–10 | Per-state tenant config, training delivery, go-live readiness review (COMP-014) | Rollout Lead |

## 3. Training Plan (aligned to COMP-007)
- **MHP Certification Track** — clinical workflows, MHP escalation, E-Sanjeevani video consult, EHR documentation (REQ-004). Estimated 16 hours.
- **Counsellor Track** — L1 triage script, de-escalation, referral to MHP. 8 hours.
- **L1 Support Agent Track** — ticket logging, severity matrix, escalation matrix (COMP-012 / R-013). 6 hours.
- **State Cell Coordinator Track** — dashboard interpretation, rollout playbook, grievance reporting. 4 hours.
- **Administrator Track** — RBAC, ABHA federation, break-glass procedure, audit retrieval. 8 hours.
- LMS delivers SCORM/xAPI; certificates issued and tracked per user.

## 4. Channels Provided
- Mobile application (Android/iOS) — download via official store links issued by IIITB.
- Web portal — accessible to authorised staff only.
- IVR — toll-free number per State/UT, multilingual prompts (REQ-001).

## 5. Support Contacts

| Role | Contact | Hours | Channel |
|------|---------|-------|---------|
| Programme Manager (Bidder) | pm.telemas@<vendor> | Mon–Fri 09:00–18:00 IST | Email, phone, Teams |
| Delivery Manager (Bidder) | dm.telemas@<vendor> | Mon–Sat 09:00–19:00 IST | Email, phone |
| L1 Service Desk | helpdesk.telemas@<vendor> | 24×7 | Phone, ticket portal |
| L2 On-call Engineer | l2.telemas@<vendor> | 24×7 | Phone, PagerDuty |
| Customer Success Manager | cs.telemas@<vendor> | Mon–Fri 09:00–18:00 IST | Email, Teams |
| Security Incident Response | sec.telemas@<vendor> | 24×7 | Email, phone (incident hotline) |
| IIITB PMO | pmo@iiitb.ac.in | Mon–Fri 09:00–17:30 IST | Email |
| Grievance Redressal (per RFP) | grievance.telemas@<vendor> | 24×7 (response within SLA) | Phone, portal |

## 6. What Customers Need to Do Before Go-Live
1. Nominate State/UT cell coordinators and share contact details.
2. Provide staff lists for IAM provisioning (TASK-010) at least 10 working days before tenant cutover.
3. Confirm clinical workflow sign-off with NIMHANS (DEP-007).
4. Confirm IVR toll-free numbers and language packs per State/UT.
5. Attend Dashboard Orientation (O-5) and nominate dashboard owners.
6. Acknowledge the Steering Committee cadence (TASK-015).

## 7. Post Go-Live
- Hyper-care window of 30 days per pilot State/UT (RSK-004).
- Weekly health reports delivered to IIITB PMO.
- Monthly Steering Committee review with KPI pack from COMP-006.
- Quarterly satisfaction survey feeds delivery/feedback.md.