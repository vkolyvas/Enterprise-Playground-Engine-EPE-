---
checksum_sha256: 3bf791e29cebe0a034711df2b31284713c193db7f4803d3c56106bcdb7510e90
contract: presales.handover
customer: Tele-MANAS
generated_at: '2026-09-30T14:54:19.303346+00:00'
generated_by: presales-engine
opportunity: OPP-number2
project_id: number2
provenance:
  source_documents:
  - 'DOC-B585FB4B498A — RFP: Software Development and Platform Support Services for
    National Tele-Mental Health Initiative, IIITB/EHRC/2022/IT-01, 25-Oct-2022 (Tele-MANAS)'
stage: presales
status: draft
version: 1
---

# Presales → Architecture Handover — Tele-MANAS (OPP-number2)

## 1. Opportunity Summary
- **Project:** number2 — Software Development and Platform Support Services for National Tele-Mental Health Initiative. [DOC-B585FB4B498A]
- **Customer:** Tele-MANAS via IIITB EHRC. [DOC-B585FB4B498A]
- **RFP:** IIITB/EHRC/2022/IT-01, 25-Oct-2022. [DOC-B585FB4B498A]
- **Verdict:** Qualified (conditional). See `presales/qualification.md`.

## 2. Business Context & Drivers
- National-scale tele-mental-health for under-served populations; unify state cells; EHR + ABDM integration; governance dashboards; training enablement. [DOC-B585FB4B498A]
- Voice/IVR already live (10-Oct-2022); national uplift now required. [DOC-B585FB4B498A]

## 3. Requirements (with IDs)
> Each requirement has a unique REQ-NNN ID. Capability references use CAP-NNN from the Product Catalog. The catalog provided is empty, so all CAP references are **to be assigned by Product/Architecture** — gaps tagged here.

| REQ-ID | Description | Source | CAP Reference |
|---|---|---|---|
| REQ-001 | Voice/IVR teleconsultation: training, L1 support, caller-info store, counsellor/MHP workflow, IVR UI upgrade | [DOC-B585FB4B498A] | CAP-TBD-IVR |
| REQ-002 | E-Sanjeevani video consultation integration | [DOC-B585FB4B498A] | CAP-TBD-ESANJ |
| REQ-003 | National Tele-MANAS platform (central + state/UT) | [DOC-B585FB4B498A] | CAP-TBD-TMANAS |
| REQ-004 | National E-Manas with EHR for teleconsultations | [DOC-B585FB4B498A] | CAP-TBD-EMANAS |
| REQ-005 | Governance and dashboard modules | [DOC-B585FB4B498A] | CAP-TBD-DASH |
| REQ-006 | Training module plug-ins for tele-consultants | [DOC-B585FB4B498A] | CAP-TBD-TRAIN |
| REQ-007 | ABDM (Ayushman Bharat Digital Mission) integration | [DOC-B585FB4B498A] | CAP-TBD-ABDM |
| REQ-008 | Platform enhancements, maintenance, release notes, deployment scripting | [DOC-B585FB4B498A] | CAP-TBD-OPS |
| REQ-009 | Shift-based L1/L2 technical support staffing | [DOC-B585FB4B498A] | CAP-TBD-SUP |
| REQ-010 | Steering Committee/PMO governance participation | [DOC-B585FB4B498A] | CAP-TBD-GOV |
| REQ-011 | Compliance with healthcare standards and security certifications; scalability | [DOC-B585FB4B498A] | CAP-TBD-SEC |
| REQ-012 | Mobile app / website service channels (per RFP functional matrix) | [DOC-B585FB4B498A] | CAP-TBD-CHAN |
| REQ-013 | Linkages to other digital platforms for mental-health care | [DOC-B585FB4B498A] | CAP-TBD-LINK |

## 4. In-Scope, Out-of-Scope, Assumptions, Dependencies
See `presales/scope.md` sections "In-Scope", "Out-of-Scope", "Assumptions", "Dependencies".

## 5. Integrations
- ABDM. [DOC-B585FB4B498A]
- E-Sanjeevani. [DOC-B585FB4B498A]
- Commercial IVR (live 10-Oct-22). [DOC-B585FB4B498A]
- Karnataka E-Manas (base). [DOC-B585FB4B498A]
- CTI (Computer Telephony Integration). [DOC-B585FB4B498A]
- Mobile app / website channels. [DOC-B585FB4B498A]

## 6. Security & Compliance
- Healthcare standards and security certifications (specifics to be confirmed — DEC-003). [DOC-B585FB4B498A]
- Confidentiality of "Confidential" information per RFP. [DOC-B585FB4B498A]
- ABDM conformance. [DOC-B585FB4B498A]

## 7. SLA
- Shift-based L1/L2; specific availability / response / resolution targets to be defined (DEC-002). [DOC-B585FB4B498A]
- Liquidated damages and performance security per RFP. [DOC-B585FB4B498A]

## 8. Commercial Constraints
- 7-year term + 2-year optional renewal at mutually agreed price. [DOC-B585FB4B498A]
- EMD, tender processing fee, performance security, "No Claim" certificate. [DOC-B585FB4B498A]
- IIITB reserves right to accept/reject any/all bids and to amend the Contract. [DOC-B585FB4B498A]
- Strict 3-day grievance escalation windows. [DOC-B585FB4B498A]

## 9. Stakeholders & Governance
- IIITB EHRC (buyer); NIMHANS (clinical); MeitY, DoT, MoHFW (programme); Steering Committee; PMO; Grievance Committees (Stage-I/II); Director, IIITB (appellate). [DOC-B585FB4B498A]
- Vendor single-point-of-responsibility. [DOC-B585FB4B498A]

## 10. Product Readiness & Capability Mapping
- Product Readiness contract sections are empty in the input; cannot confirm product/architecture boundaries yet (DEC-001).
- Product Catalog provided has **no CAP rows** — every REQ references a placeholder CAP-TBD-* to be confirmed.

## 11. Architecture Decisions Needed (DEC-NNN)
- **DEC-001.** Determine which REQs are delivered as configurable product vs custom development under IIITB tech leadership.
- **DEC-002.** Define SLA targets (availability, RTO/RPO, response/resolution by priority) for L1/L2, Tele-MANAS, E-Manas, ABDM integrations.
- **DEC-003.** Identify applicable healthcare standards and security certifications (e.g., ISO 27001, ABDM HIE-CM, DISHA/ABDM, MeitY cyber guidelines).
- **DEC-004.** Define integration architecture with ABDM and E-Sanjeevani (APIs, identity, data exchange, message queues).
- **DEC-005.** Confirm scale targets (peak concurrent calls, states/UTs, EHR volume) and capacity/scaling model.
- **DEC-006.** Confirm deployment topology (cloud/On-prem/hybrid) under IIITB supervision and data-residency for health data.
- **DEC-007.** Define IVR UI upgrade approach on the commercial IVR platform (10-Oct-22).
- **DEC-008.** Shift roster, locations (on-site at IIITB vs remote), and staffing pyramid.
- **DEC-009.** Release, change and deployment pipeline (including L3 deployment scripts). [DOC-B585FB4B498A]
- **DEC-010.** Identity, access, audit and monitoring model aligned with ABDM and NIMHANS.

## 12. Open Questions (Q-NNN)
- **Q-001.** What are the concrete SLA targets expected by IIITB (uptime, RTO, RPO, support response/resolution by priority)?
- **Q-002.** What are the expected call volumes, peak concurrency, States/UT rollout sequence and timelines?
- **Q-003.** Which healthcare/security certifications are mandatory for the platform components?
- **Q-004.** What is the target cloud/infra footprint (Govt cloud, IIITB data centre, hybrid)?
- **Q-005.** What ABDM modules are in-scope (ABHA, HIE-CM, HRP, UHI)?
- **Q-006.** Does the Vendor build/host the platform or operate it on IIITB/NIMHANS-owned infrastructure?
- **Q-007.** What is the licensing/IP ownership of code developed under this contract?
- **Q-008.** What is the budget envelope / commercials structure expected?
- **Q-009.** Which existing commercial IVR platform is in use (vendor, contract status)?
- **Q-010.** What are the reporting cadences and KPIs for the Steering Committee and PMO?
- **Q-011.** What is the staffing location/rotation expectation (on-site at IIITB Bengaluru vs distributed)?
- **Q-012.** Are there reference architectures, design documents or code repositories that the Vendor will inherit?

## 13. Risks & Mitigations
- **R-001.** Architecture autonomy limited by IIITB tech leadership — mitigate via joint architecture board and clear decision logs.
- **R-002.** Long 7+2 year horizon with periodic scope changes — mitigate via change-control and time-and-material provisions.
- **R-003.** ABDM / E-Sanjeevani dependency risk — mitigate via conformance testing and sandbox environments.
- **R-004.** State/UT rollout variability — mitigate via phased staffing and training plans.
- **R-005.** Confidentiality exposure with multiple government stakeholders — mitigate via strict data classification and access controls.

## 14. Provenance & Source Documents
- [DOC-B585FB4B498A] — RFP IIITB/EHRC/2022/IT-01 dated 25-Oct-2022 (and its annexures), as retrieved.

---
*Architecture stage to confirm CAP-NNN mappings, fill Product Readiness sections, and resolve DEC-NNN and Q-NNN before solution design.*