---
checksum_sha256: 4812f87f30b1fffdf1441a727f45dc90c6ea073c645bccf7002dea8c4712b1ad
contract: delivery.handover_d
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:06:42.109534+00:00'
generated_by: delivery-engine
opportunity: OPP-TeleMANAS-001
project_id: Tele-MANAS-IT-Services-RFP
provenance:
  source_documents:
  - Architecture Blueprint — Tele-MANAS IT Services (DOC-B585FB4B498A) — Components,
    Tasks, Tests, Rollout, Acceptance, Risks, Dependencies
  - Architecture LLD — Tele-MANAS IT Services — per-component detailed design
  - 'RFP IIITB/EHRC/2022/IT-01, 25-Oct-2022 — Software Development and Platform Support
    Services for National Tele-Mental Health Initiative (retrieved excerpts: contents,
    glossary, eligibility, envelope structure, audit/inspection rights, governance,
    cover letter, Bangalore self-declaration context, indicative role-mix Annexure
    9)'
  - Opportunity record OPP-TeleMANAS-001
stage: delivery
status: draft
version: 1
---

# Customer Handover — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore

This document is the formal handover pack delivered to IIITB at the point of live service acceptance (Milestone 3 → Steady-State transition, and again at each Yearly Renewal Gate per REQ-010). It is jointly signed by the Bidder Delivery Manager and the IIITB PMO.

---

## 1. Handover Summary

| Item | Status | Reference |
|------|--------|-----------|
| Service in production | YES / NO | (Release calendar) |
| All AC-01..AC-18 satisfied | YES / NO | delivery/acceptance.md |
| Open risks | List | Risk register |
| Open defects | List | Defect tracker |
| Known issues | List | Known-issues register (REQ-007) |
| Outstanding clarifications | List | F-XX items |
| Audit evidence pack | Delivered | ISMS pack |
| Steering Committee cadence | Confirmed (F-07) | Calendar |
| Commercial position | Confirmed (F-05) | Rate card + benchmark |

---

## 2. Service Description (as handed over)

- **Service:** Software Development and Platform Support Services for the National Tele-Mental Health Initiative (Tele-MANAS).
- **Customer:** E-Health Research Centre, IIIT Bangalore.
- **Period:** Initial 3-year contract; yearly renewals per REQ-010; optional 2-year extension per F-17.
- **In-scope components:** COMP-001..COMP-014 (see architecture blueprint).
- **Out-of-scope:** Hardware upgrade scope clarifications per F-06 / R-12; Level 3 ownership per F-08.

---

## 3. Service Boundaries & Interfaces

- **Application Platform (COMP-001):** UI / functional / back-end layers with WCAG 2.1 AA and multilingual coverage (COMP-014).
- **Operations (COMP-002):** Shift-based L1/L2 (shift pattern per F-09).
- **Integrations (COMP-003):** TMC, GRS, CTI/IVR, EHR per F-02 confirmed interfaces.
- **Release & Deployment (COMP-006):** CI/CD, canary, rollback hooks.
- **Migration & Upgrade (COMP-005):** Quarterly waves per release calendar.
- **Security & Compliance (COMP-009):** ISO 27001 / Annexure 04 controls.
- **Confidentiality & Data Governance (COMP-010):** PHI handling, breach response.
- **Bangalore Delivery (COMP-011):** Onsite / near-site operating model.
- **Governance / Steering Committee (COMP-013):** Cadence per F-07.

---

## 4. Operational Tooling Handover

| Tool | Purpose | Access Path | Owner |
|------|---------|-------------|-------|
| ITSM | Ticket lifecycle | Portal / email | Delivery Manager |
| APM | Performance / SLOs | Dashboard | Tech Lead |
| SIEM | Security monitoring | Dashboard | Security Lead |
| Documentation portal | Knowledge base (COMP-004) | URL | Tech Lead |
| CI/CD | Build & deploy | Restricted | Tech Lead |
| Audit log store | Tamper-evident audit (AuditEvent) | Restricted | Security Lead |

---

## 5. SLAs / SLOs (post F-01)

(Per operations.md; values inserted upon F-01 confirmation.)

| Service | Target |
|---------|--------|
| Availability | __% / month |
| Sev-1 ack | __ min |
| Sev-1 mitigation | __ hrs |
| DR RTO / RPO | __ hrs / __ min |

---

## 6. Commercial Position

- **Contract value:** per Annexure 9 line-item rates.
- **Quantity governance:** per RFP clause; ceiling alerts active.
- **Pass-through trigger:** quarterly market benchmark per F-05 (TASK-210).
- **Renewal cycle:** yearly (TASK-211).
- **Closure:** "No Claim" certificate per REQ-017 (AC-14).
- **Contract parties:** exclusively IIITB ↔ Bidder (AC-18, REQ-021).

---

## 7. Security & Compliance Position

- **ISMS baselined:** YES / NO (TASK-109).
- **ISO 27001 certification status:** per Annexure 04 (D-04 / R-03 path).
- **Last external pen-test:** date and report reference (TEST-007).
- **Last DR drill:** date and outcome (TEST-009).
- **Access recertification:** last run date (TASK-213).
- **Audit cadence:** per F-11 (TASK-113, TASK-204).
- **Data residency:** per F-03 (TASK-112).

---

## 8. Documentation Delivered

- Layer docs (UI / functional / back-end) — REQ-001, REQ-002.
- API / contract specs.
- Operational runbooks (operations.md).
- Onboarding guide (onboarding.md).
- Release notes index.
- Known-issues register.
- Audit evidence pack.
- Test reports (per release).
- Steering Committee minutes archive.

---

## 9. Open Items at Handover

| Item ID | Description | Owner | Target Date |
|---------|-------------|-------|-------------|
| OH-01 | F-01 SLA targets to be inserted into operations.md once confirmed | Solution Lead | Pre-go-live |
| OH-02 | F-02 integration interface catalogue | Solution Architect | Pre-canary |
| OH-03 | F-03 data residency confirmation | Security Lead | Pre-foundation |
| OH-04 | F-05 market price index selection | Commercial Lead | Pre-steady-state |
| OH-05 | F-09 shift pattern confirmation | Delivery Manager | Pre-foundation |
| OH-06 | F-11 audit cadence confirmation | Security Lead | Pre-Milestone-2 |
| OH-07 | D-14 IdP federation | Security Lead | Pre-Milestone-2 |
| OH-08 | D-12 infra tenancy | Tech Lead | Pre-Milestone-2 |

---

## 10. Customer Responsibilities Going Forward

- Operate Steering Committee; provide secretariat support if needed.
- Provide timely decisions on F-01..F-11 clarifications.
- Provide Level 3 ownership and integration interface owners.
- Provide IIITB IdP federation and infra tenancy decisions.
- Approve release notes / change windows.
- Participate in UAT (TEST-010) and audit walks (TEST-013).
- Initiate renewal decision per yearly cycle (REQ-010).

---

## 11. Sign-off

**Bidder Delivery Manager:**  ____________________________   Date: ___________

**IIITB PMO Representative:**  ____________________________   Date: ___________

**IIITB Security Representative:**  ____________________________   Date: ___________

**IIITB Commercial Representative:**  ____________________________   Date: ___________

---

## 12. Renewal & Closure References

- **Renewal cadence:** yearly per REQ-010 (TASK-211).
- **Closure path:** "No Claim" certificate per REQ-017 (AC-14).
- **Extension option:** 2-year per F-17 (D-13).
- **Audit inspections:** Regulator / IIITB inspection rights preserved.