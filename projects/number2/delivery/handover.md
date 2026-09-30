---
checksum_sha256: 872862784bc3eb2c750a9a3f8d5d51108aaa6f7b5feb6a179a21691156bba44c
contract: delivery.handover_d
customer: Tele-MANAS
generated_at: '2026-09-30T14:58:23.188390+00:00'
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

# Customer Handover — Tele-MANAS (OPP-number2)

> Formal transfer of the live Tele-MANAS service from Delivery to Customer Operations (IIITB PMO + State/UT cells), post M6 pilot acceptance.

## 1. Service in Scope
All 15 components (COMP-001..COMP-015) under the Solution Baseline, deployed on the hybrid topology (DEC-006), integrated with ABDM (COMP-004) and E-Sanjeevani (COMP-003).

## 2. Pre-Handover Checklist (from Solution Baseline §8)
- [ ] All DEC-NNN resolved or formally accepted as deferred (TASK-001..010)
- [ ] All Q-NNN resolved or formally accepted as deferred (TASK-011, 012)
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

## 3. Handover Artefacts

| Artefact | Source | Location |
|----------|--------|----------|
| Solution Baseline (this contract) | Architecture | delivery/ plan/test/acceptance/onboarding/operations |
| Low-Level Design | Architecture | LLD attached |
| As-Built Configuration | Delivery | docs://telemas/as-built |
| DR Runbook and last drill report | SRE | evidence://telemas/test010 |
| Pen-test closure report | Security | evidence://telemas/test011 |
| ISO 27001 certificate / undertaking | Security | evidence://telemas/test012 |
| ABDM HIE-CM attestation | Integration | evidence://telemas/test003 |
| Steering Committee minutes | PMO | docs://telemas/governance |
| SLA evidence log | PMO | evidence://telemas/sla |
| Training completion reports | Training Lead | evidence://telemas/training |
| Subcontractor register | Delivery Manager | docs://telemas/subcontractors |

## 4. Roles and Responsibilities Post-Handover

| Area | Customer (IIITB) | Delivery (Bidder) |
|------|------------------|--------------------|
| Service ownership | IIITB PMO | Transitioned |
| L1/L2 support | Bidder (per contract) | Bidder |
| Major incident comms | Joint | Bidder-led |
| Change advisory | Joint (customer veto on prod) | Bidder proposes |
| Security operations | Joint | Bidder operates platform |
| ABDM/E-Sanjeevani relationship | IIITB / MoHFW | Bidder supports |
| Audit liaison | IIITB | Bidder provides evidence |

## 5. Service Level Commitments (post-handover)
- SLA targets per operations.md §2, formalised in the contract.
- Monthly SLA report delivered by 5th business day of following month.
- Quarterly Service Review with IIITB PMO.
- Annual true-up of capacity (REQ-003) and roadmap refresh.

## 6. Knowledge Transfer Sessions (conducted in last 4 weeks of M6)
1. Architecture walkthrough — Enterprise Architect.
2. Operations dashboard tour — SRE.
3. Security & compliance briefing — Security Lead.
4. Release management demo — DevSecOps Lead.
5. Support process simulation — Delivery Manager.
6. Grievance workflow rehearsal — PMO.

## 7. Handover Sign-Off

### Delivery Lead (Bidder)
- Name: __________________________  Role: Delivery Manager
- Signature: ______________________  Date: __________
- Statement: "I confirm that the service has been delivered per the Solution Baseline, all acceptance criteria are met or formally waived, and all artefacts listed in §3 have been transferred."

### Customer Representative (IIITB)
- Name: __________________________  Role: ______________________
- Signature: ______________________  Date: __________
- Statement: "On behalf of IIITB, I accept handover of the Tele-MANAS service into live operation."

### Steering Committee Chair
- Name: __________________________
- Signature: ______________________  Date: __________

## 8. Post-Handover Support Window
- Hyper-care: 90 days post-handover with 24×7 P1 response.
- Steady-state support: per contract terms; renewal gates per ASM-006.
- Option for additional 2-year renewal as per RFP cover letter.