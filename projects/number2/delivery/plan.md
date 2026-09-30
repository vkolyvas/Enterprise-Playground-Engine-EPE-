---
checksum_sha256: 806e7381458658f364750da23ec16d6556efe06be1211a1583ec5a3e72c5682a
contract: delivery.plan
customer: Tele-MANAS
generated_at: '2026-09-30T14:58:23.153983+00:00'
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

# Delivery Plan — Tele-MANAS (OPP-number2)

> Source: Solution Baseline §1–§8; LLD component detail.

## 1. Sequencing Strategy
The plan is organised into seven milestones (M0–M6). The first three are pre-implementation activities (Architecture-into-Delivery handover, vendor discovery, environment stand-up). M3–M5 cover build, integrate and certify. M6 covers hyper-care and steady-state transition. All DEC-NNN items must be closed in the M0 handover workshop (RSK-006).

## 2. Milestone Plan

| Milestone | Window | Scope | Entry Criteria | Exit Criteria | Dependencies |
|-----------|--------|-------|----------------|---------------|--------------|
| M0 — Handover & Decisions | W0–W2 | DEC-001..010, Q-007, Q-009, Q-010, Q-012 resolved; PMO/Steering KPIs baselined (TASK-001, 002, 003, 007, 008, 010, 011, 012, 015) | Contract award | All DEC-NNN signed off per Handover Checklist §8 | DEP-004, DEP-009 |
| M1 — Foundation & DevSecOps | W3–W8 | Hybrid topology stood up (DEC-006); DevSecOps pipeline (TASK-009); IAM baseline (TASK-010); Observability stack (LLD COMP-010, 011); KMS/HSM (COMP-013) | M0 signed | Environments (dev/sit/uat/preprod/prod) available; blue/green proven in UAT | DEP-005 |
| M2 — Discovery Sprints | W4–W9 (parallel) | IVR vendor discovery (RSK-007), Karnataka E-Manas code/design discovery (TASK-011, RSK-008) | M0 signed | Discovery reports approved by Architect | DEP-003, DEP-006 |
| M3 — Core Build | W8–W20 | Tele-MANAS Core (COMP-002), Citizen Channel (COMP-001), Integration Bus (COMP-008), Training module (COMP-007) | M1 + M2 | Component-level FAT passed; unit/contract tests green | DEP-007 |
| M4 — Integration & Conformance | W18–W30 | ABDM Gateway (COMP-004), E-Sanjeevani Adapter (COMP-003), E-Manas EHR (COMP-005), Commercial IVR Bridge (COMP-015) — IVR upgrade per DEC-007 | M3 | ABDM HIE-CM conformance attested; E-Sanjeevani 95% success (TEST-002, 003) | DEP-001, DEP-002, DEP-003 |
| M5 — UAT, Security, DR | W28–W38 | Governance & Dashboards (COMP-006), IAM hardening, VA/PT/red-team, DR drill, ISO 27001 audit readiness, Grievance + SLA evidence logging (TASK-014) | M4 | All TEST-001..015 passing; zero critical/high; RTO/RPO met (TEST-010, 011, 012) | DEP-008 |
| M6 — Pilot Rollout & Hyper-care | W36–W52 | Pilot State/UT rollout (COMP-014); L1/L2 support live (COMP-012); Steering Committee go-live approval; transition to steady-state ops | M5 | Pilot acceptance signed (TEST-015); SLA sustained 30 days | DEP-010 |

## 3. Task-to-Milestone Map (from Solution Baseline §2)

| TASK-ID | Task | Owner Role | Milestone | Status |
|---------|------|-----------|-----------|--------|
| TASK-001 | Confirm DEC-001 product/custom boundary | Enterprise Architect | M0 | Not Started |
| TASK-002 | Define SLA targets (DEC-002) with IIITB | PM + Architect | M0 | Not Started |
| TASK-003 | Confirm certifications (DEC-003) | Security Lead | M0 | Not Started |
| TASK-004 | Finalise ABDM + E-Sanjeevani integration design (DEC-004) | Integration Architect | M4 | Not Started |
| TASK-005 | Capacity model based on peak concurrency (DEC-005) | SRE + Architect | M1 | Not Started |
| TASK-006 | Deployment topology decision (DEC-006) | Infra Architect | M1 | Not Started |
| TASK-007 | IVR UI upgrade approach (DEC-007) | Product Manager | M2 | Not Started |
| TASK-008 | Shift roster and location (DEC-008) | Delivery Manager | M0 | Not Started |
| TASK-009 | DevSecOps pipeline build (DEC-009) | DevSecOps Lead | M1 | Not Started |
| TASK-010 | IAM model with ABHA (DEC-010) | Security Lead | M1 | Not Started |
| TASK-011 | Karnataka E-Manas code/design inheritance (Q-012) | Architect | M2 | Not Started |
| TASK-012 | Confirm IP/licensing (Q-007) | Legal + Architect | M0 | Not Started |
| TASK-013 | Subcontracting controls (RFP §8.37) | Delivery Manager | M1 | Not Started |
| TASK-014 | Grievance and SLA evidence logging | PMO | M5 | Not Started |
| TASK-015 | Steering Committee / PMO KPI definition (Q-010) | PMO | M0 | Not Started |

## 4. Prerequisites
- Contract award and Performance Security / EMD per RFP §7.2.
- IIITB IdP provisioning for staff SSO (DEP-004).
- MeghRaj / Govt Cloud tenancy (DEP-005).
- ABDM sandbox credentials and E-Sanjeevani API access (DEP-001, DEP-002).
- Karnataka E-Manas source artefacts (DEP-006).
- NIMHANS clinical workflow sign-off (DEP-007).
- Banking of Liquidated Damages caps into commercials (RSK-009).

## 5. Governance Cadence
- Weekly Delivery stand-up (PM + Workstream Leads).
- Fortnightly PMO review (PMO + IIITB).
- Monthly Steering Committee (TASK-015 KPIs, dashboards from COMP-006).
- Quarterly Change-Control Board (RSK-002).

## 6. Risk-Linked Milestone Gates
- M0 gate validates RSK-006, RSK-007, RSK-008 mitigations are active.
- M4 gate requires ABDM/E-Sanjeevani conformance evidence (RSK-003).
- M5 gate requires pen-test closure and DR drill (RSK-005, ASM-004).
- M6 gate enforces subcontracting caps (RSK-010) and SLA evidence (RSK-009).