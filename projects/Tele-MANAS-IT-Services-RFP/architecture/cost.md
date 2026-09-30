---
checksum_sha256: 62c4b811e0c23dea71e4d559aec2810516e4b2de8f6865c3d65170e8c6dad484
contract: architecture.cost
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:02:42.866150+00:00'
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

# Cost Estimate — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore
**Term:** Initial 3 years (yearly renewals; optional 2-year extension at mutually agreed price).
**Source(s):** [DOC-B585FB4B498A]

---

## 1. Cost Assumptions

| Assumption | Source / Note |
|------------|----------------|
| Indicative role-mix per RFP Annexure 9: PM (1), App Architect (1), Tech Lead (1), Programmer (3), Programmers – L3 Support (3), Jr Programmer/Tester (2), PM – Support (1), Roll-out Lead (1), Tech Support Engineer shift-wise (6). | [DOC-B585FB4B498A] Annexure 9, p.24 |
| Delivery is Bangalore-anchored onsite/near-site. | REQ-013 |
| Shift-based L1/L2 coverage with 6 Tech Support Engineers across shifts. | REQ-006 |
| All unit rates must remain valid for 3 years; pass-through of market price reductions is mandatory. | REQ-016 |
| Unlimited quantity alterations at line-item prices. | REQ-016 |
| No hardware manufacturing; infrastructure as a managed service or IIITB-provided. | Readiness pack |
| INR is the pricing currency (implicit; confirm in pre-bid). | TBC |
| Yearly renewal assumes flat headcount; changes drive line-item quantity alterations. | REQ-010 |

---

## 2. Indicative Role Unit Rates (Monthly, INR) — Range: Low / Expected / High

| Role | Indicative Headcount | Low (INR/mo) | Expected (INR/mo) | High (INR/mo) |
|------|------------------------|--------------|--------------------|----------------|
| Project Manager | 1 | 2,50,000 | 3,50,000 | 4,75,000 |
| Application Architect | 1 | 3,00,000 | 4,25,000 | 5,75,000 |
| Technology Lead | 1 | 2,25,000 | 3,00,000 | 4,00,000 |
| Programmer | 3 | 1,20,000 | 1,75,000 | 2,40,000 |
| Programmer – L3 Support | 3 | 1,10,000 | 1,60,000 | 2,20,000 |
| Jr Programmer / Tester | 2 | 70,000 | 1,05,000 | 1,45,000 |
| Project Manager – Support | 1 | 2,25,000 | 3,10,000 | 4,10,000 |
| Roll-out Lead | 1 | 1,50,000 | 2,10,000 | 2,85,000 |
| Tech Support Engineer (shift-wise) | 6 | 70,000 | 1,00,000 | 1,40,000 |

> Rates are illustrative and subject to IIITB benchmarks and pre-bid queries. They are designed to be defensible against the mandatory pass-through obligation (REQ-016).

---

## 3. Annual Indicative Run-Rate (Total Monthly × 12)

| Year | Low (INR) | Expected (INR) | High (INR) |
|------|------------|----------------|-------------|
| Year 1 | ~2,93,40,000 | ~4,11,00,000 | ~5,59,20,000 |
| Year 2 | ~2,93,40,000 | ~4,11,00,000 | ~5,59,20,000 |
| Year 3 | ~2,93,40,000 | ~4,11,00,000 | ~5,59,20,000 |
| **3-Year Total** | **~8,80,20,000** | **~12,33,00,000** | **~16,77,60,000** |

> These ranges assume the RFP indicative role-mix and do not yet include infrastructure pass-through, tooling, audit costs, or travel. Optional 2-year extension at mutually agreed price (per F-17) would add ~2 × (Item).

---

## 4. Non-Staff Line Items (Indicative Annual)

| Line Item | Low (INR/yr) | Expected (INR/yr) | High (INR/yr) |
|-----------|---------------|---------------------|-----------------|
| Infrastructure (managed; compute, DB, networking) — if bidder-hosted | 25,00,000 | 45,00,000 | 75,00,000 |
| Tooling (IDE, CI/CD, observability, ITSM, SIEM, secrets) | 8,00,000 | 15,00,000 | 25,00,000 |
| ISO 27001 certification & surveillance | 6,00,000 | 10,00,000 | 18,00,000 |
| Audit support & external audits | 4,00,000 | 7,00,000 | 12,00,000 |
| Travel / in-person Steering Committee | 3,00,000 | 5,00,000 | 8,00,000 |
| Training & certifications | 3,00,000 | 5,00,000 | 9,00,000 |
| Contingency (10%) | 4,90,000 | 9,30,000 | 14,70,000 |
| **Sub-total (non-staff)** | **~53,90,000** | **~96,30,000** | **~1,61,70,000** |

---

## 5. 3-Year Indicative Total

| Scenario | 3-Year Staff | 3-Year Non-Staff | **Total (INR)** |
|----------|---------------|------------------|-------------------|
| Low | 8,80,20,000 | 1,61,70,000 | **~10,41,90,000** |
| Expected | 12,33,00,000 | 2,88,90,000 | **~15,21,90,000** |
| High | 16,77,60,000 | 4,85,10,000 | **~21,62,70,000** |

---

## 6. Commercial Risks & Sensitivities

| Risk | Sensitivity | Mitigation |
|------|-------------|------------|
| Pass-through of market price reductions (REQ-016, F-05) compresses margin if market falls 5–10% | Margin compression of 5–15% over 3 years | Build margin buffer into Expected case; quarterly benchmark trigger (DEC-008). |
| Yearly renewal not guaranteed (F-13) | Revenue volatility | Treat Year 1 as committed, Year 2–3 as renewal options; size fixed-cost commitments accordingly. |
| Quantity alterations are uncapped (REQ-016) | Volume risk | Workload governance committee; rate-card-driven scaling; capacity reserves. |
| "No Claim" certificate gates final payment (REQ-017) | Working capital | Maintain entitlements register; settlement checklist before signing. |
| SLA penalties (Section 8.18) — thresholds TBC (F-01) | Penalty exposure up to 5–10% of contract value (typical) | Confirm SLA penalties in pre-bid; size contingency. |
| Subcontracting controls (Section 7.36/8.37) — likely approval required | Operational cost | Plan for in-house delivery; subcontractor buffer only with IIITB approval. |
| Hardware upgrade scope ambiguity (F-06) | Scope creep risk | Clarify scope boundary; treat infra upgrades as platform infrastructure only. |

---

## 7. Cost Optimisation Opportunities

1. **Tiered rate card:** Differentiate on-site vs near-site to optimise Bangalore-anchored delivery cost.
2. **Shared infrastructure:** Leverage IIITB-provided or shared cloud tenancy to reduce infrastructure line-item.
3. **Automation of L1 tickets:** IVR self-service + automated triage; reduce Tech Support Engineer headcount from 6 to 4–5 over time.
4. **Bundled tooling:** Negotiate multi-year SaaS commitments to reduce per-year tooling cost.
5. **Joint audit cadence with IIITB/MOHFW/NIMHANS:** Consolidate audit windows to reduce external audit costs.
6. **Pass-through defensibility:** Build market-indexed rate card (e.g., linked to published salary benchmarks) to make pass-through auditable and margin-defensible.
7. **Renewal incentives:** Offer a Year 2 / Year 3 rate freeze in exchange for multi-year renewal commitment (subject to IIITB approval).

---

## 8. Indicative Pricing Strategy Notes

- Anchor pricing at the **Expected** scenario for competitive positioning.
- Reserve **Low** scenario for aggressive capture strategy (low-margin, high-renewal upside).
- Hold **High** scenario for conservative posture or if SLA penalties (F-01) turn out to be aggressive.
- Build a **5–8% margin buffer** in the Expected case to absorb pass-through obligation (F-05).
- Ensure line-item granularity supports unlimited quantity alteration (REQ-016).