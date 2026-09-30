---
checksum_sha256: a91893b9c423e30f81bc29db12d187844d527fde1e5dcd8c6f68d906c51913af
contract: architecture.cost
customer: Tele-MANAS
generated_at: '2026-09-30T14:55:51.439668+00:00'
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

# Cost Architecture — Tele-MANAS (OPP-number2)

## 1. Cost Categories & Line Items

| # | Line Item | Unit | Notes |
|---|-----------|------|-------|
| LI-01 | Project Manager | FTE-year | 1 PM, on-site Bengaluru (RFP §4.2 #10) |
| LI-02 | Application Architect | FTE-year | 1 Architect |
| LI-03 | Technology Lead | FTE-year | 1 Tech Lead |
| LI-04 | Programmers | FTE-year | 3 |
| LI-05 | L3 Support Programmers | FTE-year | 3 |
| LI-06 | Jr Programmer/Tester | FTE-year | 2 |
| LI-07 | PM – Support | FTE-year | 1 |
| LI-08 | Roll-out Lead | FTE-year | 1 |
| LI-09 | Tech Support Engineers (shift) | FTE-year | 6 |
| LI-10 | IIITB/NIMHANS-licensed infra (Govt cloud + on-prem) | INR/year | DEC-006 hybrid |
| LI-11 | Commercial IVR (existing + UI upgrade) | INR/year + one-time | Q-009, DEC-007 |
| LI-12 | ABDM conformance & certification | one-time + recurring | ISO 27001, ABDM HIE-CM |
| LI-13 | Security tooling (SIEM, WAF, DLP, HSM, VA) | INR/year | recurring |
| LI-14 | Observability stack (APM/logging/monitoring) | INR/year | recurring |
| LI-15 | L1/L2 tooling (service desk, ITSM) | INR/year | recurring |
| LI-16 | Training delivery (LMS, content) | one-time + recurring | per state rollout |
| LI-17 | Travel & on-site allowances | INR/year | Bengaluru on-site |
| LI-18 | Subcontracting (if any, subject to RFP §8.37) | INR/year | capped |
| LI-19 | Performance security / liquidated damages buffer | INR | per RFP §8.18–8.20 |
| LI-20 | Contingency (10%) | INR/year | standard |

## 2. Assumptions
- AS-C-01. RFP indicative headcount of 19 is the staffing baseline; phased scale-up to follow state/UT rollout (Q-002).
- AS-C-02. Bengaluru on-site minimums apply for PM, Architect, Tech Lead, Roll-out Lead (RFP §4.2 #10).
- AS-C-03. 7-year initial term with optional 2-year renewal; commercials treated as a 9-year envelope (RFP §7).
- AS-C-04. Hybrid deployment: 40% capex-like on IIITB-controlled DC, 60% opex on MeghRaj/Govt cloud.
- AS-C-05. ISO 27001 certification included; ABDM HIE-CM readiness included.
- AS-C-06. No major capex on voice/IVR replacement (DEC-007 → UI upgrade only).

## 3. Ranges (indicative, INR crore; subject to Q-008)

| Bucket | Low | Expected | High | Driver |
|--------|-----|----------|------|--------|
| People (7-year) | 90 | 130 | 180 | FTE rates, pyramid, attrition |
| Infra (cloud + DC, 7-year) | 30 | 50 | 80 | Gov cloud pricing variability |
| IVR & CTI | 5 | 10 | 18 | DEC-007 / Q-009 |
| Security & compliance | 8 | 14 | 22 | DEC-003 scope |
| Tools (DevSecOps, ITSM, LMS, observability) | 6 | 10 | 15 | toolchain |
| Rollout, training, travel | 6 | 10 | 16 | state/UT count |
| Contingency (10%) | 15 | 22 | 33 | |
| **Total envelope (7-year)** | **160** | **246** | **364** | |

## 4. Optimisation Opportunities
- OPT-01. Pooled Gov-cloud tenancy across states → reduce infra cost 15–25%.
- OPT-02. Shared L1/L2 between Tele-MANAS and E-Manas → reduce shift staffing 10%.
- OPT-03. Open-source FHIR store + ABDM-recommended components → reduce license cost.
- OPT-04. Reuse Karnataka E-Manas components (subject to IP, Q-007) → reduce dev cost 20%.
- OPT-05. Tiered SLA (gold/silver/bronze per state maturity) → optimise L2 staffing.
- OPT-06. Multi-year cloud reservations → 20–30% infra savings.
- OPT-07. Centralised SIEM & SOC shared with other IIITB programmes.
- OPT-08. LMS content reuse (MoHFW/NIMHANS existing material) → reduce training cost.

## 5. Cost Risks
- CR-01. Vendor rate card (Annexure 9, Section A) not provided (Q-008).
- CR-02. Scope expansion via change-control (R-002) over 7+2 years.
- CR-03. Liquidated damages if SLAs missed (RFP §8.18–8.20).
- CR-04. Subcontracting controls (RFP §8.37) may limit cost arbitrage.
- CR-05. Gov cloud pricing changes over horizon.
- CR-06. ABDM/E-Sanjeevani integration rework if upstream APIs change.