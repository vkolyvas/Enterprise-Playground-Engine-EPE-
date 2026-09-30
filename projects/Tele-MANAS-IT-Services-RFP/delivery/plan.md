---
checksum_sha256: 87a60a3c958d7ad1a64aa9879e49123e7049fdcfacac9db94311ed4788669cb7
contract: delivery.plan
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:06:42.106884+00:00'
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

# Delivery Plan — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore
**RFP Reference:** IIITB/EHRC/2022/IT-01, 25-Oct-2022

This plan sequences all TASK-NNNs from the architecture blueprint into milestones with owners, dependencies, prerequisites, and status. Status values: `Not Started`, `In Progress`, `Blocked`, `Done`, `Deferred`.

---

## Milestone 0 — Bid Stage (Pre-Award)

**Window:** Bid window per F-10 / RFP schedule
**Gate:** Stage 1 eligibility (AC-17) + Stage 2 technical + commercial envelopes accepted

| Task ID | Description | Component | Owner | Prerequisite | Depends On | Status |
|---------|-------------|-----------|-------|--------------|------------|--------|
| TASK-001 | Compile Envelope I (Technical + masked Annexure 9) per REQ-014 | COMP-012 | Bid Manager | Eligibility pack ready | TASK-006 | Not Started |
| TASK-002 | Compile Envelope II (Commercial) per REQ-014 | COMP-008, COMP-012 | Bid Manager | Line-item pricing sealed | TASK-114 | Not Started |
| TASK-003 | Execute Annexure 04 undertaking (REQ-011) and Annexure 6 No Deviation (REQ-015) | COMP-012, COMP-009 | Bid Manager | Security lead sign-off on Annexure 04 | D-04 | Not Started |
| TASK-004 | Submit Bangalore Self-Declaration (REQ-013) | COMP-011, COMP-012 | Bid Manager | Authorised signatory available | — | Not Started |
| TASK-005 | Pay tender processing fee and EMD via DD/NEFT (REQ-022) | COMP-012 | Finance | Bank instruments ready | — | Not Started |
| TASK-006 | Validate eligibility pack (CoI, audited financials, ISO 27001) per REQ-020 | COMP-012 | Bid Manager | Documents in hand | — | Not Started |
| TASK-007 | Resolve pre-bid open questions (F-01..F-09, Q-001..Q-010) | COMP-001..COMP-013 | Solution Lead | Customer Q&A channel open | D-01..D-10 | In Progress |
| TASK-008 | Finalise SLA targets, integration scope, audit cadence, data residency (F-01, F-02, F-03, F-11) | COMP-009, COMP-010 | Solution Lead | Customer clarifications received | D-01, D-02, D-03, D-09 | Blocked |

**Exit Criteria (AC-12, AC-17, AC-18):** Two offline envelopes submitted before cut-off; eligibility accepted by IIITB.

---

## Milestone 1 — Discovery & Confirmation (Weeks 1–4)

**Window:** Post-award, Weeks 1–4
**Gate:** All F-01..F-11 clarifications confirmed in writing

| Task ID | Description | Component | Owner | Prerequisite | Depends On | Status |
|---------|-------------|-----------|-------|--------------|------------|--------|
| TASK-110 | Confirm integration interfaces with TMC, GRS, CTI/IVR, EHR owners (F-02) | COMP-003 | Solution Architect | Customer kick-off done | D-02 | Not Started |
| TASK-111 | Confirm Level 3 ownership and handoff model (F-08) | COMP-003, COMP-006 | Tech Lead | Level 3 team identified | D-08 | Not Started |
| TASK-112 | Confirm data residency position (F-03) | COMP-009, COMP-010 | Security Lead | Legal review | D-03 | Not Started |
| TASK-113 | Confirm audit cadence with IIITB (F-11) | COMP-009 | Security Lead | MOHFW/NIMHANS input | D-09 | Not Started |
| TASK-114 | Confirm "market price" definition and pass-through trigger (F-05) | COMP-008 | Commercial Lead | Customer commercial cell input | D-05 | Not Started |

**Exit Criteria:** Signed clarification log; updated risk register (R-02, R-03, R-07, R-08 closed or downgraded).

---

## Milestone 2 — Foundation / Mobilisation (Weeks 5–12)

**Window:** Post-award Months 0–3
**Gate:** Foundation services live; first audit-evidence walk-through (AC-09)

| Task ID | Description | Component | Owner | Prerequisite | Depends On | Status |
|---------|-------------|-----------|-------|--------------|------------|--------|
| TASK-101 | Set up Bangalore onsite/near-site facility (clean desk, screen privacy, visitor logs) | COMP-011 | Delivery Manager | Lease/workspace approved | — | Not Started |
| TASK-102 | Recruit and onboard delivery team per indicative role-mix (Annexure 9) | COMP-002, COMP-011 | HR / Delivery Manager | Hiring plan approved | — | Not Started |
| TASK-103 | Establish shift rotation plan (F-09) and on-call rota | COMP-002 | Delivery Manager | Shift pattern confirmed | D-06 | Blocked |
| TASK-104 | Stand up CI/CD pipeline; integrate security tooling | COMP-006, COMP-007, COMP-009 | Tech Lead | Cloud/infra tenancy decided | D-12 | Not Started |
| TASK-105 | Stand up SIEM, logging, monitoring, ITSM | COMP-002, COMP-009 | Security Lead | Tooling licences in place | TASK-104 | Not Started |
| TASK-106 | Stand up documentation repository and knowledge base | COMP-004 | Tech Lead | Repo platform selected | — | Not Started |
| TASK-107 | Establish Steering Committee cadence with IIITB PMO (F-07) | COMP-013 | Delivery Manager | PMO contact established | D-07 | Not Started |
| TASK-108 | Sign NDA and confidentiality undertakings for all staff | COMP-010 | HR / Legal | NDA template approved | TASK-102 | Not Started |
| TASK-109 | Baseline ISO 27001 ISMS / Annexure 04 controls; confirm scope with IIITB (F-04) | COMP-009 | Security Lead | Annexure 04 equivalence clarified | D-04, D-11 | Not Started |

**Exit Criteria (AC-05, AC-09, AC-10, AC-11):** Onsite operating, monitoring live, ISMS baselined, NDAs signed, first Steering Committee held.

---

## Milestone 3 — First Release Train (Months 4–9)

**Window:** Months 4–9
**Gate:** First production release accepted (AC-01, AC-02, AC-06, AC-16); UAT passed (TEST-010)

| Task ID | Description | Component | Owner | Prerequisite | Depends On | Status |
|---------|-------------|-----------|-------|--------------|------------|--------|
| TASK-201 | Iterative development across UI/functional/back-end per release train | COMP-001 | Tech Lead | Foundation services live | TASK-104, TASK-110 | Not Started |
| TASK-202 | Documentation updates per layer (COMP-004) per release | COMP-004 | All | Doc drift CI hook in place | TASK-106, TASK-201 | Not Started |
| TASK-203 | Integration testing coordination with Level 3 and external integrators | COMP-003 | Test Lead | Contract tests defined | TASK-110, TASK-111 | Not Started |
| TASK-205 | Migration, enhancement, and upgrade waves per release calendar (first wave) | COMP-005 | Tech Lead | Schema migration tool ready | TASK-104 | Not Started |
| TASK-206 | Release notes, known-issues register, post-release monitoring | COMP-006 | Tech Lead | APM dashboards live | TASK-104, TASK-105 | Not Started |
| TASK-207 | Defect management and preventive maintenance | COMP-007 | QA Lead | Defect tracker configured | TASK-104 | Not Started |
| TASK-208 | Shift-based L1/L2 support and incident response | COMP-002 | Delivery Manager | Shifts staffed | TASK-103, TASK-102 | Not Started |
| TASK-212 | Accessibility audits and language additions | COMP-014 | Tech Lead | Multilingual framework in place | TASK-201 | Not Started |

**Exit Criteria:** Go/no-go passed (TASK-206 window); first acceptance pack delivered (AC-01..AC-07, AC-16).

---

## Milestone 4 — Steady-State Operations (Months 10–24)

**Window:** Months 10–24
**Gate:** Year 1 renewal evidence pack (AC-08) accepted; Year 2 renewal decision

| Task ID | Description | Component | Owner | Prerequisite | Depends On | Status |
|---------|-------------|-----------|-------|--------------|------------|--------|
| TASK-203 | Integration testing coordination (continuous) | COMP-003 | Test Lead | — | — | Not Started |
| TASK-204 | Quarterly internal audits and external audit support | COMP-009 | Security Lead | ISMS baselined | TASK-109 | Not Started |
| TASK-205 | Migration/upgrade waves (quarterly) | COMP-005 | Tech Lead | — | — | Not Started |
| TASK-206 | Release notes and post-release monitoring (continuous) | COMP-006 | Tech Lead | — | — | Not Started |
| TASK-207 | Defect management (continuous) | COMP-007 | QA Lead | — | — | Not Started |
| TASK-208 | Shift-based L1/L2 support (continuous) | COMP-002 | Delivery Manager | — | — | Not Started |
| TASK-209 | Monthly Steering Committee status and minutes | COMP-013 | Delivery Manager | Cadence agreed | TASK-107 | Not Started |
| TASK-210 | Quarterly market price benchmarking for pass-through (F-05) | COMP-008 | Commercial Lead | Market index selected | TASK-114 | Not Started |
| TASK-211 | Yearly renewal evidence pack (Year 1) | COMP-008, COMP-013 | Commercial Lead | Performance evidence ready | TASK-209 | Not Started |
| TASK-213 | Maintain confidentiality controls; periodic access recertification | COMP-010 | Security Lead | — | — | Not Started |

**Exit Criteria (AC-08, AC-13, AC-15):** Renewal pack accepted; no critical audit findings; pass-through trigger matrix demonstrated.

---

## Milestone 5 — Steady-State Operations Year 2–3 (Months 25–36)

**Window:** Months 25–36
**Gate:** Year 2 + Year 3 renewals granted

| Task ID | Description | Component | Owner | Prerequisite | Depends On | Status |
|---------|-------------|-----------|-------|--------------|------------|--------|
| TASK-211 | Yearly renewal evidence pack (Year 2, Year 3) | COMP-008, COMP-013 | Commercial Lead | — | TASK-209 | Not Started |
| TASK-204 | Quarterly audits (continuous) | COMP-009 | Security Lead | — | — | Not Started |
| TASK-205 | Migration/upgrade waves (continuous) | COMP-005 | Tech Lead | — | — | Not Started |

---

## Milestone 6 — Closure / Extension (End of Year 3)

**Window:** Final 90 days of contract
**Gate:** "No Claim" certificate executed (AC-14); extension decision per F-17

| Task ID | Description | Component | Owner | Prerequisite | Depends On | Status |
|---------|-------------|-----------|-------|--------------|------------|--------|
| TASK-211 (final) | Final performance evidence pack | COMP-008, COMP-013 | Commercial Lead | Year 3 signed off | — | Not Started |
| Closure task | Execute "No Claim" certificate (REQ-017) after entitlements settled | COMP-008 | Commercial Lead + Legal | Settlement checklist complete | — | Not Started |
| Extension task | Optional 2-year extension per F-17 | COMP-008 | Commercial Lead | IIITB initiates | D-13 | Not Started |

**Exit Criteria (AC-14, AC-18):** Settlements closed; contract executed exclusively between IIITB and Bidder.

---

## Cross-Cutting Dependency Log

- D-01 SLA targets → unblocks TASK-008, TASK-103, TEST-005, AC-04
- D-02 Integration interfaces → unblocks TASK-110, TASK-203, TEST-003, AC-02
- D-03 Data residency → unblocks TASK-112, R-03, COMP-009/010 design
- D-04 Annexure 04 equivalence → unblocks TASK-109, AC-09
- D-05 "Market price" definition → unblocks TASK-114, TASK-210, AC-13
- D-06 Shift pattern → unblocks TASK-103, AC-05
- D-07 Steering Committee cadence → unblocks TASK-107, TASK-209, AC-15
- D-08 Level 3 ownership → unblocks TASK-111, TASK-203, TASK-206
- D-09 Audit cadence → unblocks TASK-113, TASK-204, AC-09
- D-10 Bid deadlines → unblocks TASK-001, TASK-002, TASK-005
- D-11 Auditor selection → unblocks TASK-109
- D-12 Cloud/infra tenancy → unblocks TASK-104
- D-13 Extension language → unblocks closure/extension task
- D-14 IIITB IdP federation → unblocks SSO delivery (COMP-009)