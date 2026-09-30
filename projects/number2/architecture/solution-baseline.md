---
checksum_sha256: 1faddad8b55440e9782c7ccedb3394ac3c5e9f1529862f260bd76346cb480351
contract: architecture.solution_baseline
customer: Tele-MANAS
generated_at: '2026-09-30T14:55:51.440294+00:00'
generated_by: architecture-engine
opportunity: OPP-number2
project_id: number2
provenance:
  source_documents:
  - DOC-B585FB4B498A — RFP IIITB/EHRC/2022/IT-01, 25-Oct-2022 (and annexures), as
    retrieved
  - Presales Handover sections 1–14
  - Product Readiness (empty sections)
  - Product Catalog (empty)
stage: architecture
status: draft
version: 1
---

# Solution Baseline — Tele-MANAS (OPP-number2)

> Handover from Architecture to Delivery. All DEC-NNN and Q-NNN items remain open and must be resolved in Architecture-into-Delivery handover workshop.

## 1. Components
COMP-001 Citizen Channel; COMP-002 Tele-MANAS Core; COMP-003 E-Sanjeevani Adapter; COMP-004 ABDM Gateway; COMP-005 E-Manas EHR; COMP-006 Governance & Dashboard; COMP-007 Training; COMP-008 Integration Bus; COMP-009 IAM/AAA; COMP-010 Observability & SRE; COMP-011 DevSecOps & Release Engineering; COMP-012 L1/L2 Support Ops; COMP-013 Data Protection & Compliance; COMP-014 State/UT Rollout Orchestrator; COMP-015 Commercial IVR/CTI Bridge.

## 2. Implementation Tasks

| TASK-ID   | Task | Owner Role | REQs | DEC refs |
|-----------|------|-----------|------|----------|
| TASK-001 | Confirm DEC-001 product/custom boundary | Enterprise Architect | All | DEC-001 |
| TASK-002 | Define SLA targets (DEC-002) with IIITB | PM + Architect | REQ-009, REQ-011 | DEC-002 |
| TASK-003 | Confirm certifications (DEC-003) | Security Lead | REQ-011 | DEC-003 |
| TASK-004 | Finalise ABDM + E-Sanjeevani integration design (DEC-004) | Integration Architect | REQ-002, REQ-007 | DEC-004 |
| TASK-005 | Capacity model based on peak concurrency (DEC-005) | SRE + Architect | REQ-003 | DEC-005 |
| TASK-006 | Deployment topology decision (DEC-006) | Infra Architect | REQ-011 | DEC-006 |
| TASK-007 | IVR UI upgrade approach (DEC-007) | Product Manager | REQ-001 | DEC-007 |
| TASK-008 | Shift roster and location (DEC-008) | Delivery Manager | REQ-009 | DEC-008 |
| TASK-009 | DevSecOps pipeline build (DEC-009) | DevSecOps Lead | REQ-008 | DEC-009 |
| TASK-010 | IAM model with ABHA (DEC-010) | Security Lead | REQ-011 | DEC-010 |
| TASK-011 | Karnataka E-Manas code/design inheritance (Q-012) | Architect | REQ-004 | — |
| TASK-012 | Confirm IP/licensing (Q-007) | Legal + Architect | REQ-004, REQ-008 | — |
| TASK-013 | Subcontracting controls (RFP §8.37) | Delivery Manager | All | — |
| TASK-014 | Grievance and SLA evidence logging | PMO | REQ-010 | — |
| TASK-015 | Steering Committee / PMO KPI definition (Q-010) | PMO | REQ-005, REQ-010 | — |

## 3. Test Plan

| TEST-ID  | Test | Components | Acceptance |
|----------|------|-----------|------------|
| TEST-001 | Functional: IVR flows (training, L1, counsellor workflow) | COMP-001, COMP-015 | All call flows pass with NFR-defined response times |
| TEST-002 | Integration: E-Sanjeevani video | COMP-003 | 95% successful session establishments |
| TEST-003 | Integration: ABDM ABHA, HIE-CM, HRP, UHI (per DEC-004) | COMP-004 | Conformance test pass; consent flows verified |
| TEST-004 | EHR: FHIR R4 CRUD, encryption, audit | COMP-005, COMP-013 | All PHI encrypted, audit immutable |
| TEST-005 | Dashboards: KPI accuracy, RBAC | COMP-006 | Dashboards reflect real-time data within agreed lag |
| TEST-006 | IAM: ABHA SSO, MFA, RBAC, JIT | COMP-009 | Pen-test pass; no privilege escalation |
| TEST-007 | Observability: SLA dashboards | COMP-010 | All NFR metrics captured, alerted |
| TEST-008 | DevSecOps: blue/green, rollback | COMP-011 | Rollback < 5 min, signed artefacts |
| TEST-009 | L1/L2 support: shift handover, escalation | COMP-012 | Tickets triaged within SLA |
| TEST-010 | DR drill: failover | COMP-002, COMP-005, COMP-013 | RTO/RPO met |
| TEST-011 | Security: VA, PT, red-team | COMP-009, COMP-013 | Zero critical/high open |
| TEST-012 | Compliance: ISO 27001 audit, ABDM HIE-CM | All | Audit findings remediated |
| TEST-013 | Multi-channel: mobile, web | COMP-001 | OWASP MASVS pass |
| TEST-014 | Cross-platform linkages (REQ-013) | COMP-008 | All partner integrations in conformance |
| TEST-015 | State rollout (pilot) | COMP-014 | Successful onboarding per playbook |

## 4. Acceptance Criteria
- All REQs (REQ-001..REQ-013) demonstrably delivered.
- SLA targets (DEC-002) met for 3 consecutive months.
- ISO 27001 certification achieved (or undertaking accepted).
- ABDM HIE-CM conformance attestation.
- DR drill passes with documented RTO/RPO.
- Steering Committee approval of dashboards, KPIs, and release plan.
- Liquidated damages threshold not breached.
- Code/IP terms (Q-007) closed.

## 5. Risks & Mitigations

| RSK-ID   | Risk | Mitigation |
|----------|------|-----------|
| RSK-001 | Architecture autonomy limited by IIITB tech leadership (R-001) | Joint architecture board, decision log, escalation to Steering Committee |
| RSK-002 | Long 7+2-year horizon with scope creep (R-002) | Change-control board, T&M fallback pricing, clear out-of-scope clause |
| RSK-003 | ABDM/E-Sanjeevani dependency (R-003) | Conformance testing, sandbox, dual integration paths where feasible |
| RSK-004 | State/UT rollout variability (R-004) | Phased staffing, playbook, training toolkit |
| RSK-005 | Multi-stakeholder confidentiality (R-005) | Data classification, RBAC, audit |
| RSK-006 | Open DEC/Q items block detailed design | Architecture-to-Delivery handover workshop within 2 weeks of award |
| RSK-007 | IVR vendor unknowns (Q-009) | Vendor discovery sprint, contractual review |
| RSK-008 | Karnataka E-Manas inheritance unknowns (Q-012) | Code/design discovery sprint |
| RSK-009 | SLA/liquidated damages exposure (RFP §8.18–8.20) | Conservative targets, insurance, penalty modelling |
| RSK-010 | Subcontracting constraints (RFP §8.37) | Vendor risk register, contractual sub-flow-down |

## 6. Assumptions

| ASM-ID   | Assumption |
|----------|-----------|
| ASM-001 | RFP indicative headcount (19) is the staffing baseline |
| ASM-002 | Bengaluru on-site for PM/Architect/Tech Lead/Roll-out Lead |
| ASM-003 | Hybrid topology is acceptable (DEC-006 selected) |
| ASM-004 | ISO 27001 is the minimum certification |
| ASM-005 | ABDM modules ABHA + HIE-CM are in scope; HRP/UHI pending |
| ASM-006 | 7+2-year horizon with renewal gates |
| ASM-007 | Vendor single-point-of-responsibility under IIITB tech leadership |
| ASM-008 | Performance security + EMD already accounted in commercials |
| ASM-009 | Subcontracting allowed within RFP §8.37 caps |
| ASM-010 | Karnataka E-Manas code is reference-only unless IP terms allow reuse |

## 7. Dependencies

| DEP-ID   | Dependency |
|----------|-----------|
| DEP-001 | ABDM national infrastructure availability and conformance |
| DEP-002 | E-Sanjeevani API access and identity bridging |
| DEP-003 | Commercial IVR vendor continuity and contract |
| DEP-004 | IIITB IdP for staff identity and SSO |
| DEP-005 | MeghRaj / Govt Cloud provisioning timelines |
| DEP-006 | Karnataka E-Manas source artefacts |
| DEP-007 | NIMHANS clinical workflow sign-off |
| DEP-008 | Steering Committee and PMO cadence |
| DEP-009 | MeitY/DoT/MoHFW programme-level coordination |
| DEP-010 | State/UT cell readiness and rollout windows |

## 8. Handover Checklist to Delivery
- [ ] All DEC-NNN resolved or formally accepted as deferred
- [ ] All Q-NNN resolved or formally accepted as deferred
- [ ] Product/Architecture boundary (DEC-001) signed off
- [ ] SLA targets (DEC-002) signed off
- [ ] Certifications (DEC-003) signed off
- [ ] Scale targets (DEC-005) signed off
- [ ] Topology (DEC-006) signed off
- [ ] IVR upgrade approach (DEC-007) signed off
- [ ] Staffing plan (DEC-008) signed off
- [ ] DevSecOps pipeline (DEC-009) agreed
- [ ] IAM model (DEC-010) agreed
- [ ] Risk register, assumptions, dependencies baselined