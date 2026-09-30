---
checksum_sha256: 6deda902f1c127cee5c5deb4f97628c1f5746b77db5da18574f8bc7557a31926
contract: delivery.acceptance
customer: Tele-MANAS
generated_at: '2026-09-30T14:58:23.159913+00:00'
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

# Acceptance — Tele-MANAS (OPP-number2)

> Source: Solution Baseline §4 Acceptance Criteria. Status fields marked "Pending" reflect pre-execution; once M5/M6 evidence is captured, each row is updated with PASS/FAIL and evidence references.

## 1. Test Execution Register

| TEST-ID | Planned Window | Status | Evidence Reference | Notes |
|---------|----------------|--------|--------------------|-------|
| TEST-001 | M3/M5 | Pending | evidence://telemas/test001 (to be populated) | Bilingual prompt corpus attached |
| TEST-002 | M4/M5 | Pending | evidence://telemas/test002 | Session log + E-Sanjeevani ack |
| TEST-003 | M4/M5 | Pending | evidence://telemas/test003 | ABDM conformance certificate |
| TEST-004 | M4/M5 | Pending | evidence://telemas/test004 | KMS key attestation, audit hash chain |
| TEST-005 | M5 | Pending | evidence://telemas/test005 | Dashboard screenshots per role |
| TEST-006 | M5 | Pending | evidence://telemas/test006 | Pen-test report (anonymised) |
| TEST-007 | M5 | Pending | evidence://telemas/test007 | Alert routing drill log |
| TEST-008 | M1/M5 | Pending | evidence://telemas/test008 | Rollback drill video, SLSA provenance |
| TEST-009 | M5/M6 | Pending | evidence://telemas/test009 | Ticket SLA dashboard export |
| TEST-010 | M5 | Pending | evidence://telemas/test010 | DR drill report (RTO/RPO) |
| TEST-011 | M5 | Pending | evidence://telemas/test011 | VA/PT/red-team closure report |
| TEST-012 | M5 | Pending | evidence://telemas/test012 | ISO 27001 certificate / undertaking; ABDM attestation |
| TEST-013 | M5 | Pending | evidence://telemas/test013 | OWASP MASVS report |
| TEST-014 | M4/M5 | Pending | evidence://telemas/test014 | Partner conformance packs |
| TEST-015 | M6 | Pending | evidence://telemas/test015 | State pilot acceptance letter |

## 2. Acceptance Criteria Tracker

| # | Criterion (Baseline §4) | Owner | Verification | Status |
|---|--------------------------|-------|--------------|--------|
| AC-1 | All REQs (REQ-001..REQ-013) demonstrably delivered | Enterprise Architect | Requirement traceability matrix + test evidence | Pending |
| AC-2 | SLA targets (DEC-002) met for 3 consecutive months | PM + SRE | Monthly SLA pack from COMP-006/010 | Pending (post-M6) |
| AC-3 | ISO 27001 certification achieved (or undertaking accepted) | Security Lead | TEST-012 certificate / undertaking | Pending |
| AC-4 | ABDM HIE-CM conformance attestation | Integration Architect | TEST-003 attestation | Pending |
| AC-5 | DR drill passes with documented RTO/RPO | SRE | TEST-010 report | Pending |
| AC-6 | Steering Committee approval of dashboards, KPIs, release plan | PMO | Steering Committee minutes | Pending |
| AC-7 | Liquidated damages threshold not breached | PM + Commercials | SLA evidence log (TASK-014) | Pending |
| AC-8 | Code/IP terms (Q-007) closed | Legal + Architect | TASK-012 closure note | Pending |

## 3. Non-Conformance & Waiver Log
- (Empty — to be populated upon M5/M6 execution. Any deviation from Baseline §4 must be recorded with waiver authority and compensating control.)

## 4. Sign-Off

### Architecture Sign-Off
- Name: __________________________  Role: Enterprise Architect
- Signature: ______________________  Date: __________
- Statement: "I confirm the delivered solution conforms to the Solution Baseline and LLD; all DEC-NNN affecting acceptance are resolved or formally deferred with waiver."

### Customer (IIITB / Tele-MANAS) Sign-Off
- Name: __________________________  Role: ______________________
- Signature: ______________________  Date: __________
- Statement: "On behalf of IIITB, I accept the deliverables against the RFP requirements and the Solution Baseline."

### Delivery Lead Sign-Off
- Name: __________________________  Role: Delivery Manager
- Signature: ______________________  Date: __________