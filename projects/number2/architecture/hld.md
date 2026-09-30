---
checksum_sha256: b789914dd418b6266217f9349cbcba450edb118df518071a985c32e20af31581
contract: architecture.hld
customer: Tele-MANAS
generated_at: '2026-09-30T14:55:51.437661+00:00'
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

# High-Level Design — Tele-MANAS (OPP-number2)

## 1. Drivers (linked to REQs)
- National-scale tele-mental-health platform unifying state cells (REQ-003).
- EHR + ABDM integration (REQ-004, REQ-007).
- Voice/IVR enhancement on already-live commercial IVR (REQ-001).
- Video consultation via E-Sanjeevani (REQ-002).
- Governance, training, dashboards (REQ-005, REQ-006).
- Long-term (7+2 years) platform support with shift-based L1/L2 (REQ-008, REQ-009, REQ-010).
- Healthcare/security compliance and scalability (REQ-011).
- Multi-channel access (mobile/web) and cross-platform linkages (REQ-012, REQ-013).

## 2. Constraints (from handover & RFP)
- IIITB tech leadership and Bengaluru delivery mandate (RFP §2.2, §4.2 #10).
- Single-point-of-responsibility vendor model.
- ISO 27001 and data-security undertaking (Annexure 4).
- Liquidated damages and performance security risk.
- 3-day grievance / 30-day Stage-II timelines.

## 3. Options Considered

### Option A — Fully Managed Cloud (Hyperscaler, single tenant)
- Build new platform on a single hyperscaler (Azure/ AWS Government Cloud / MeghRaj / NIC).
- Pros: fastest to scale, mature PaaS, native ABDM/India-Stack alignment.
- Cons: data-residency uncertainty, multi-cloud not allowed, vendor lock-in, IIITB-supervision constraint complicates shared control plane.

### Option B — Hybrid (IIITB/State DC + NIC Cloud for control plane, MeghRaj for analytics)
- Keep sensitive health data in IIITB/NIMHANS-controlled DC; leverage MeghRaj/Govt cloud for elastic voice/video and analytics.
- Pros: data-residency compliance, IIITB tech leadership preserved, ABDM HIE-CM compatible, optimised cost.
- Cons: higher integration complexity, dual ops model, requires strong network/identity federation.

### Option C — On-Prem / State-Housed (per state/UT)
- Each state runs its own stack on-prem.
- Pros: maximum locality, no cloud dependency.
- Cons: inconsistent operations, costly at national scale, slow ABDM rollout, contradicts national unified platform goal (REQ-003).

### Selected: **Option B — Hybrid with IIITB/NIMHANS-controlled core and MeghRaj/Govt-Cloud elastic edge**
- Rationale: balances data-residency (F-C-05), IIITB tech leadership (R-001), ABDM conformance (F-C-03), and elastic national scale (F-C-04).
- Decisions: DEC-006 (selected), DEC-004 (federated integration), DEC-009 (CI/CD on MeghRaj/IIITB DC), DEC-010 (federated IAM with ABHA as citizen identity).

## 4. Logical Components (COMP-NNN)

| COMP-ID     | Component                    | Purpose / Capability | REQs satisfied | DEC refs |
|-------------|------------------------------|----------------------|----------------|----------|
| COMP-001 | Citizen Channel (Mobile + Web + IVR) | Multi-channel entry: IVR, mobile app, web portal | REQ-001, REQ-012 | DEC-007 |
| COMP-002 | Tele-MANAS Core Services | Session orchestration, counsellor routing, MHP workflow, audit | REQ-001, REQ-003 | DEC-005 |
| COMP-003 | E-Sanjeevani Adapter | Video consultation bridge | REQ-002 | DEC-004 |
| COMP-004 | ABDM Gateway (ABHA, HIE-CM, HRP, UHI) | ABDM conformance, identity and record exchange | REQ-007 | DEC-004, DEC-010 |
| COMP-005 | E-Manas EHR (National) | Clinical record store, FHIR-based | REQ-004 | DEC-003, DEC-006 |
| COMP-006 | Governance & Dashboard Module | KPI dashboards for Steering Committee / PMO / state cells | REQ-005, REQ-010 | DEC-002 |
| COMP-007 | Training & Capacity-Building Module | LMS plug-ins, MHP certification tracking | REQ-006 | DEC-008 |
| COMP-008 | Integration Bus (API Gateway + Event Mesh) | Centralised, audited integration to ABDM, E-Sanjeevani, state MIS | REQ-013 | DEC-004, DEC-009 |
| COMP-009 | Identity, Access & Audit (IAM/AAA) | ABHA-federated identity, RBAC, audit logging | REQ-011 | DEC-010 |
| COMP-010 | Observability & SRE (Logs/Metrics/Traces/APM) | SLA monitoring, anomaly detection | REQ-008, REQ-011 | DEC-002, DEC-009 |
| COMP-011 | DevSecOps & Release Engineering | CI/CD, IaC, deployment scripting, release notes | REQ-008 | DEC-009 |
| COMP-012 | L1/L2 Support Operations (NOC/Service Desk) | Shift-based support, ticket routing | REQ-009 | DEC-008 |
| COMP-013 | Data Protection & Compliance Plane | Encryption (at-rest/in-transit/in-use), DLP, key management | REQ-011 | DEC-003, DEC-006 |
| COMP-014 | State/UT Rollout Orchestrator | Phased rollout tooling, data migration, training delivery | REQ-003, REQ-006 | DEC-008 |
| COMP-015 | Commercial IVR/CTI Bridge | Bridge to live commercial IVR (10-Oct-22) | REQ-001 | DEC-007 |

## 5. Data Flows (high level)
1. Citizen → COMP-001 (IVR / mobile / web) → COMP-002 (session) → COMP-015 (CTI to commercial IVR).
2. COMP-002 → COMP-003 (video via E-Sanjeevani).
3. COMP-002 → COMP-005 (EHR record update) → COMP-004 (ABDM HIE-CM/HRP publish).
4. COMP-004 → ABDM national infrastructure (consent, fetch, push).
5. COMP-005 ↔ COMP-008 ↔ COMP-013 (audit, encryption, residency enforcement).
6. COMP-006 ← COMP-002 + COMP-005 + COMP-010 (dashboards).
7. COMP-012 receives events from COMP-010; runs L1/L2; escalates to COMP-002 ops team.

## 6. NFR Mapping
- Availability 99.9% (assumed pending DEC-002) → COMP-002 multi-AZ, COMP-010 active health checks, COMP-012 24x7.
- RTO ≤ 30 min / RPO ≤ 5 min (assumed) → COMP-005 + COMP-013 continuous backup + DR runbook.
- Scalability: stateless app tier (COMP-002), autoscaling; CDR-grade EHR DB.
- Performance: peak concurrent calls (TBD pending Q-002) — capacity buffer 2x peak.
- Security: encryption everywhere, ABHA SSO, immutable audit (COMP-009 + COMP-013).
- Maintainability: IaC, blue/green, documented release notes (COMP-011).
- Compliance: ISO 27001, ABDM HIE-CM, MeitY cyber guidelines (DEC-003).
- Observability: SLA dashboards (COMP-010) feed Steering Committee (COMP-006).

## 7. Decision Register Summary
- DEC-001 Partial: configurable product + custom development under IIITB tech leadership (CT-02).
- DEC-002 Open: SLA targets awaiting Q-001 answer.
- DEC-003 Open: certifications awaiting Q-003; ISO 27001 baseline assumed.
- DEC-004 Selected: federated ABDM + E-Sanjeevani via COMP-004 / COMP-008.
- DEC-005 Open: scale pending Q-002.
- DEC-006 Selected: hybrid topology with IIITB core + Govt-Cloud edge.
- DEC-007 Open: IVR UI upgrade approach pending Q-009.
- DEC-008 Open: shift roster / locations pending Q-011; baseline Bengaluru on-site + remote L2.
- DEC-009 Selected: DevSecOps with IaC, blue/green, automated deployment scripting.
- DEC-010 Selected: ABHA-federated identity with IIITB IdP for staff.