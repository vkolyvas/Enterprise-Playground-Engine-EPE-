---
checksum_sha256: 50de1f5c3c5522a7395467ea82218d4160d560b874122ce21011a637dfcdfa6b
contract: architecture.validation
customer: Tele-MANAS
generated_at: '2026-09-30T14:55:51.436542+00:00'
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

# Architecture Validation — Tele-MANAS (OPP-number2)

## Provenance
- Source: RFP IIITB/EHRC/2022/IT-01, 25-Oct-2022 [DOC-B585FB4B498A]
- Presales Handover sections 1–14
- Product Readiness sections all empty (DEC-001)
- Product Catalog has zero CAP rows (all REQs mapped to CAP-TBD-*)

## Per-Requirement Validation

| REQ-ID  | Status   | Reasoning | Contradictions / Gaps |
|---------|----------|-----------|-----------------------|
| REQ-001 Voice/IVR teleconsultation (training, L1, caller-info, counsellor/MHP workflow, IVR UI upgrade) | warning | IVR already live 10-Oct-2022, but commercial IVR vendor identity, contract status, APIs not documented (Q-009). IVR UI upgrade approach undecided (DEC-007). CAP-TBD-IVR unresolved. | Live commercial IVR dependency on external vendor; no SLA baseline documented. |
| REQ-002 E-Sanjeevani video consultation integration | warning | E-Sanjeevani is an external MoHFW platform; integration contract, API access, identity bridging not specified (DEC-004). | Possible cross-MOHFW governance friction; no documented API catalog reference. |
| REQ-003 National Tele-MANAS platform (central + state/UT) | warning | Scale (states/UTs, peak concurrent calls, EHR volume) undefined (Q-002, DEC-005). | Capacity-planning cannot be completed. |
| REQ-004 National E-Manas with EHR | warning | Karnataka E-Manas is the base; portability, data migration, schema ownership, IP/licensing (Q-007) undefined. | Risk of inheriting legacy technical debt without design docs (Q-012). |
| REQ-005 Governance and dashboard modules | warning | Reporting KPIs/cadence for Steering Committee and PMO undefined (Q-010). | Open reporting requirements. |
| REQ-006 Training module plug-ins for tele-consultants | warning | LMS/CMS platform not specified; CAP-TBD-TRAIN unresolved. | Multi-language mental-health training not addressed. |
| REQ-007 ABDM integration | warning | ABDM module scope (ABHA, HIE-CM, HRP, UHI) unconfirmed (Q-005, DEC-004). | No ABDM conformance evidence path. |
| REQ-008 Platform enhancements, maintenance, release notes, deployment scripting | warning | Release/change/CI/CD pipeline approach undecided (DEC-009). L3 deployment-script scope ambiguous (RFP §2.2 bullet). | DevOps toolchain not selected. |
| REQ-009 Shift-based L1/L2 technical support staffing | warning | Shift roster, locations (on-site vs remote), pyramid undefined (DEC-008, Q-011). RFP only indicative headcount (1 PM, 1 Architect, 1 Tech Lead, 3 Prog, 3 L3, 2 Jr, 1 PM-Support, 1 Roll-out Lead, 6 Tech Support Eng = 19). | Actual SLA targets (Q-001, DEC-002) and on-site expectation at Bengaluru (RFP §4.2 #10) drive staffing. |
| REQ-010 Steering Committee/PMO governance participation | warning | Cadence, agenda templates, escalation flow (3-day grievance, 30-day Stage-II) defined in RFP but reporting KPIs undefined (Q-010). | Risk of inconsistent governance artefacts. |
| REQ-011 Compliance with healthcare standards and security certifications; scalability | warning | Specific certifications (ISO 27001 explicitly mentioned; ABDM HIE-CM; DISHA; MeitY cyber) undefined (Q-003, DEC-003). | Cannot baseline compliance scope. |
| REQ-012 Mobile app / website service channels | warning | Functional matrix referenced but not provided; CAP-TBD-CHAN unresolved. | Cannot define channel APIs. |
| REQ-013 Linkages to other digital platforms for mental-health care | warning | Target platforms unspecified (e.g., NIMHANS records, state health MIS, ICMR). | Open integration landscape. |

## Findings (severity-ordered)

### Critical
- F-C-01. Product Catalog is empty; every REQ has a CAP-TBD placeholder. Architecture cannot confirm product-vs-custom boundary (DEC-001).
- F-C-02. SLA targets not defined (DEC-002 / Q-001). All availability, RTO/RPO, response/resolution targets open.
- F-C-03. Healthcare/security certification scope undefined (DEC-003 / Q-003). RFP explicitly cites ISO 27001 and "data & information security undertaking" (Annexure 4) but ABDM HIE-CM, MeitY cyber, DISHA scope not confirmed.
- F-C-04. Scale targets (peak concurrent calls, state/UT rollout sequence, EHR volume) missing (DEC-005 / Q-002). Capacity model cannot be sized.
- F-C-05. Deployment topology (cloud / on-prem / hybrid) and data-residency for health data not confirmed (DEC-006 / Q-004). Data-protection strategy blocked.
- F-C-06. ABDM and E-Sanjeevani integration architecture undefined (DEC-004 / Q-005). Cross-ministry dependencies unmanaged.
- F-C-07. Build vs host responsibility not confirmed (Q-006). Operating model ambiguous.
- F-C-08. IP ownership/licensing of code developed under contract not defined (Q-007). Long-term sustainability and handover unclear.

### High
- F-H-01. Staffing location: RFP mandates Bengaluru delivery (RFP §4.2 #10) but vendor may want distributed model (Q-011, DEC-008).
- F-H-02. IVR commercial vendor identity unknown (Q-009 / DEC-007). Upgrade and integration risk.
- F-H-03. Karnataka E-Manas inheritance — no code/design repository artefacts listed (Q-012). Onboarding risk.
- F-H-04. Budget envelope / commercials structure not provided (Q-008). Pricing model (T&M vs milestone vs hybrid) undecided.
- F-H-05. 7+2-year contract horizon with periodic scope changes (R-002) — change-control mechanism must be contractual.
- F-H-06. Architecture autonomy limited by IIITB tech leadership (R-001) — joint architecture board governance not yet defined.
- F-H-07. Liquidated damages and performance security create financial risk if SLAs are missed (RFP §8.18–8.20).

### Medium
- F-M-01. Multi-stakeholder confidentiality (IIITB, NIMHANS, MeitY, DoT, MoHFW) requires data-classification scheme (R-005).
- F-M-02. Reporting KPIs for Steering Committee and PMO undefined (Q-010).
- F-M-03. Subcontracting controls (RFP §8.37) need to be mirrored in architecture (no subcontractor on critical-path data plane).
- F-M-04. Grievance and appellate timelines (3 days / 30 days) require contractual logging and evidence retention.
- F-M-05. State/UT rollout variability (R-004) — phased staffing, training and data-migration toolkit needed.

### Low / Informational
- F-L-01. "No Claim" certificate requirement needs acceptance/exclusion clause in handover.
- F-L-02. EMD/tender processing fee mechanics are non-architectural but flagged for completeness.

## Contradictions
- CT-01. RFP states contract is 3 years with yearly renewals, but Cover Letter (Annexure 2) and Section 7 mention 7+2 years. Treat 7+2 as the contractual horizon with renewal checkpoints.
- CT-02. "Vendor single-point-of-responsibility" (Section 9) vs "Working under the technology leadership and supervision of IIITB" (Section 2.2) — delivery model is collaborative under IIITB tech leadership, not vendor-autonomous.
- CT-03. RFP §4.2 #10 mandates Bengaluru delivery; RFP §2.2 allows remote collaboration — on-site minimums to be defined (DEC-008).