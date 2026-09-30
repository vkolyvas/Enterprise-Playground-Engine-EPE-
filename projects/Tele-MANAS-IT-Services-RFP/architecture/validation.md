---
checksum_sha256: 95a866d4df60305f1b12b438b79d5f62c59965187899a04fff33217737d5fac3
contract: architecture.validation
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:02:42.864582+00:00'
generated_by: architecture-engine
opportunity: OPP-TeleMANAS-001
project_id: Tele-MANAS-IT-Services-RFP
provenance:
  source_documents:
  - RFP IIITB/EHRC/2022/IT-01, 25-Oct-2022 [DOC-B585FB4B498A]
  - Presales handover for OPP-TeleMANAS-001
  - Product readiness pack for Tele-MANAS IT Services RFP
  - Retrieved evidence excerpts from RFP Sections 2 (Scope of Work), 4 (Eligibility),
    5 (Agreements), 7 (Bid Submission), 7.20 (Signing of Contract), 8 (Terms & Conditions),
    Annexure 4 (Undertaking), Annexure 6 (No Deviation), Annexure 9 (Rate Card), Annexure
    10 (Self-Declaration)
stage: architecture
status: draft
version: 1
---

# Architecture Validation — Tele-MANAS IT Services RFP (OPP-TeleMANAS-001)

**Customer:** E-Health Research Centre, IIIT Bangalore
**RFP Reference:** IIITB/EHRC/2022/IT-01, 25-Oct-2022
**Source(s):** [DOC-B585FB4B498A]

This validation assesses every tagged requirement (REQ-001..REQ-022) against the Presales handover, readiness pack, and retrieved evidence. Each REQ is given a status (pass / warning / fail), reasoning, and any contradictions or gaps identified.

---

## 1. Per-Requirement Validation

| REQ | Description | Status | Reasoning | Contradictions / Gaps |
|-----|-------------|--------|-----------|------------------------|
| REQ-001 | Deliver Tele-MANAS application development across UI, functional and back-end layers. | pass | Explicitly required; supported by Section 2.2 SOW and CAP-01. Component COMP-001 (Application Platform) addresses it. | None. |
| REQ-002 | Provide documentation across UI, functional and back-end layers for development and testing. | pass | Explicitly required; addressed by COMP-004 (Documentation & Knowledge Repository). | None. |
| REQ-003 | Perform integration testing support and cross-team collaboration. | pass | Required; addressed by COMP-003 (Integration & Test Harness). | None. |
| REQ-004 | Deliver migration, enhancement and software/hardware upgrade services. | pass | Required; addressed by COMP-005 (Migration & Upgrade Pipeline). | Scope ambiguity: RFP says "software/hardware upgrade services" but readiness pack says "no device/hardware manufacturing." Clarify whether hardware upgrade means platform infrastructure only, not device manufacturing. |
| REQ-005 | Provide platform support with continued availability and stability of software/hardware. | pass | Required; addressed by COMP-002 (Platform Operations & L1/L2 Support). | Quantitative availability/stability targets are not specified in the retrieved evidence — flagged as gap Q-001. |
| REQ-006 | Deliver shift-based Level 1 and Level 2 support covering teleconsultations and platform operations. | pass | Required; addressed by COMP-002; indicative Tech Support Engineer headcount of 6 (shift-wise) provided. | Shift roster pattern, peak hours, and follow-the-sun expectations are not specified — flagged as gap Q-002. |
| REQ-007 | Document release notes, known issues, and roll-out issues; close-monitor post-release performance. | pass | Required; addressed by COMP-006 (Release & Deployment Management). | None. |
| REQ-008 | Coordinate with Level 3 support team for deployment scripts and smoother automated deployments. | pass | Required; addressed by COMP-006 and COMP-003. | Identity/ownership of the Level 3 team (IIITB internal vs. separate program) is not confirmed — flagged as gap Q-003. |
| REQ-009 | Maintain application using best-practice/industry-standard maintenance practices. | pass | Required; addressed by COMP-007 (Application Maintenance & Quality Engineering). | "Best practice" framework not specified; assume ITIL/ISO 20000-aligned but confirm. |
| REQ-010 | Provide multi-year platform operation support: initial 3-year contract with yearly renewals. | pass | Required; addressed by COMP-008 (Commercial & Contract Operations). | Renewal is contingent on multiple external factors (funds, approvals, government guidance) — commercial risk, not technical gap. |
| REQ-011 | Implement data privacy and information-security controls per ISO 27001 or equivalent undertaking; execute Annexure 04 undertaking. | warning | Annexure 04 undertaking is mandatory at bid stage. ISO 27001 certificate is eligibility-critical. Addressed by COMP-009 (Security & Compliance Framework). | "Equivalent undertaking" scope/terms are not defined — flagged as gap Q-005. Data localisation constraints not stated — flagged as gap Q-009. |
| REQ-012 | Maintain confidentiality of IIITB/Government/NIMHANS information including health/patient records; no use/disclosure without prior written approval. | pass | Required; addressed by COMP-009 and COMP-010 (Confidentiality & Data Governance). | None. |
| REQ-013 | Operate an onsite/near-site delivery model from Bangalore; submit Bangalore Self-Declaration. | pass | Required; addressed by COMP-011 (Bangalore Delivery Operations). Bangalore Self-Declaration is a Stage-1 disqualifier. | None. |
| REQ-014 | Submit bid via two-stage offline process: Envelope I (Technical + masked Annexure 9 commercial) and Envelope II (Commercial). | pass | Required; addressed by COMP-012 (Bid Submission & Governance). Note Annexure 9 masked commercial is part of Envelope I. | None. |
| REQ-015 | Submit Annexure 6 No Deviation acceptance. | pass | Required; addressed by COMP-012. Annexure 6 is mandatory at bid. | None. |
| REQ-016 | Pass through market price reductions to IIITB during the contract; honour 3-year quote validity; accommodate unlimited quantity alterations at line-item prices. | warning | Required; addressed by COMP-008. Pass-through trigger definition ("market price") is not specified — flagged as gap Q-008. | Commercial risk: pass-through obligation can compress margin; tracked in cost.md. |
| REQ-017 | Execute "No Claim" certificate in favor of IIITB as a condition for final payment. | pass | Required; addressed by COMP-008. | Operational risk: ensure all entitlements settled before signing — tracked as risk R-04. |
| REQ-018 | Participate in Steering Committee meetings (in-person when required and feasible); maintain records with PMO. | pass | Required; addressed by COMP-013 (Governance & Steering Committee Liaison). | Cadence not specified — flagged as gap Q-010. |
| REQ-019 | Support ICT-driven reach to under-served/marginal populations for mental health (affordability/accessibility/availability). | pass | Programme-level requirement; addressed by COMP-001 (application capability) and COMP-014 (Accessibility & Inclusion Engineering). | None. |
| REQ-020 | Bidder must be a Government Organization/PSU/Public/Partnership/Private limited company or subsidiary; ≥5 years operating; profitable in 2 of last 3 FYs (2019-20, 2020-21, 2021-22). | pass | Eligibility criteria; addressed by COMP-012. | Note: 2019-20 and 2020-21 financials predate any prospective bidder audit posture; confirm in Stage 1 pack. |
| REQ-021 | Contract exclusively between IIITB and Bidder; no direct contracting with MOHFW. | pass | Required; addressed by COMP-008. | None. |
| REQ-022 | Pay tender processing fee and EMD via Demand Draft or NEFT to IIIT Bangalore; submit bid offline. | pass | Required; addressed by COMP-012. | None. |

---

## 2. Findings

### 2.1 Critical Findings

| ID | Severity | Finding | Linked REQ(s) | Notes |
|----|----------|---------|----------------|-------|
| F-01 | CRITICAL | Quantitative SLA targets (uptime %, response/resolution, RTO/RPO) are not stated in retrieved evidence. Cannot commit to specific SLA penalties or operational design without clarification. | REQ-005, REQ-006, REQ-009 | Open question Q-001. Must be resolved before Stage 2 technical bid authoring. |
| F-02 | CRITICAL | External system integration owners/interfaces (TMC, GRS, CTI/IVR, EHR) are referenced in the glossary but interfaces, owners, and protocols are undefined. | REQ-003, REQ-008 | Open question Q-003. Blocks detailed LLD for COMP-003 and COMP-001. |
| F-03 | CRITICAL | Data residency / data localisation / cross-border transfer rules for health/patient records are not specified. Direct impact on infrastructure region selection, encryption posture, and Annexure 04 undertaking language. | REQ-011, REQ-012 | Open question Q-009. Required for COMP-009 and COMP-010 design. |

### 2.2 High Findings

| ID | Severity | Finding | Linked REQ(s) | Notes |
|----|----------|---------|----------------|-------|
| F-04 | HIGH | Annexure 04 "equivalent undertaking" acceptability is undefined; may force a full ISO 27001 certification prerequisite. | REQ-011 | Open question Q-005. |
| F-05 | HIGH | Pass-through of "market price reductions" is mandatory but "market" is undefined; could expose margin or trigger disputes. | REQ-016 | Open question Q-008. |
| F-06 | HIGH | Hardware upgrade scope is ambiguous (Section 2 calls it out; readiness pack excludes hardware manufacturing). | REQ-004 | Confirm scope boundary with IIITB during pre-bid. |
| F-07 | HIGH | Steering Committee cadence, named IIITB sponsor, and PMO interface are not defined; affects governance design. | REQ-018 | Open question Q-010. |
| F-08 | HIGH | Level 3 support team identity and ownership (IIITB internal vs. external program team) is unconfirmed; affects handoff and deployment-script co-authoring model. | REQ-008 | Open question Q-003. |
| F-09 | HIGH | Shift roster pattern, peak hours, and follow-the-sun expectations for Level 1/Level 2 teleconsultation support are not specified. | REQ-006 | Open question Q-002. |

### 2.3 Medium Findings

| ID | Severity | Finding | Linked REQ(s) | Notes |
|----|----------|---------|----------------|-------|
| F-10 | MEDIUM | Pre-bid query cut-off and bid submission deadlines not captured in retrieved evidence. | REQ-014, REQ-022 | Open question Q-006. |
| F-11 | MEDIUM | Audit cadence (internal/external, IIITB/MOHFW/NIMHANS-driven) not specified. | REQ-011 | Open question Q-007. |
| F-12 | MEDIUM | "No Claim" certificate surrendering post-settlement claim rights; final payment is gated. | REQ-017 | Ensure all entitlements are settled before signing — operational risk R-04. |
| F-13 | MEDIUM | Yearly renewals contingent on external factors (funds, approvals, government guidance). Renewal is not guaranteed. | REQ-010 | Commercial risk — addressed in cost.md. |
| F-14 | MEDIUM | Two-stage offline submission with strict pre-bid query cut-off; any delay may disqualify. | REQ-014, REQ-022 | Operational risk R-01. |
| F-15 | MEDIUM | Best-practice maintenance framework (e.g., ITIL/ISO 20000) not specified by IIITB. | REQ-009 | Assume ITIL-aligned and confirm. |

### 2.4 Low / Informational Findings

| ID | Severity | Finding | Linked REQ(s) | Notes |
|----|----------|---------|----------------|-------|
| F-16 | LOW | Bidder profitability window (2019-20, 2020-21, 2021-22) includes COVID-impacted FYs. Eligibility must be confirmed against actuals. | REQ-020 | Qualification eligibility. |
| F-17 | LOW | Optional 2-year extension beyond 7 years at mutually agreed price — only confirmed in bidder letter acceptance; Customer-side firmness unclear. | REQ-010 | Open question Q-004. |
| F-18 | LOW | Annexure 6 No Deviation acceptance is mandatory; partial deviations likely disqualifying at Stage 1. | REQ-015 | Bid management. |

---

## 3. Validation Summary

- **Pass:** 17 of 22 REQs (REQ-001..003, 005..006, 007..008, 009..010, 012..015, 017..022).
- **Warning:** 2 of 22 REQs (REQ-011, REQ-016).
- **Fail:** 0 REQs (no outright architectural failures identified at the requirement stage; however, three CRITICAL findings F-01..F-03 must be resolved before detailed design is committed).

The 10 open questions and 18 findings must be resolved (or formally risk-accepted) before final bid submission to avoid Stage-1 disqualification or post-award delivery gaps.