---
checksum_sha256: bdc90d81d99d9cb0e869ee71a85cb6ee5d91731b37445f272fca0bd5c13f0e69
contract: architecture.blueprint
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:02:42.866410+00:00'
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

# Implementation Blueprint — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore
**RFP Reference:** IIITB/EHRC/2022/IT-01, 25-Oct-2022
**Source(s):** [DOC-B585FB4B498A]

This blueprint is the handover artefact consumed after bid award. It identifies components, implementation tasks, test plan, rollout, acceptance criteria, risks, and dependencies.

---

## 1. Components

| Component | Purpose | Mapped REQs |
|-----------|---------|----------------|
| COMP-001 | Application Platform (UI/Functional/Back-end) | REQ-001, REQ-019 |
| COMP-002 | Platform Operations & L1/L2 Support | REQ-005, REQ-006 |
| COMP-003 | Integration & Test Harness | REQ-003, REQ-008 |
| COMP-004 | Documentation & Knowledge Repository | REQ-002, REQ-007 |
| COMP-005 | Migration & Upgrade Pipeline | REQ-004 |
| COMP-006 | Release & Deployment Management | REQ-007, REQ-008 |
| COMP-007 | Application Maintenance & Quality Engineering | REQ-009 |
| COMP-008 | Commercial & Contract Operations | REQ-010, REQ-016, REQ-017, REQ-021 |
| COMP-009 | Security & Compliance Framework | REQ-011 |
| COMP-010 | Confidentiality & Data Governance | REQ-012 |
| COMP-011 | Bangalore Delivery Operations | REQ-013 |
| COMP-012 | Bid Submission & Governance | REQ-014, REQ-015, REQ-020, REQ-022 |
| COMP-013 | Governance & Steering Committee Liaison | REQ-018 |
| COMP-014 | Accessibility & Inclusion Engineering | REQ-019 |

---

## 2. Implementation Tasks (TASK-NNN)

### 2.1 Bid Stage (Pre-Award)

| Task ID | Description | Component | Owner |
|---------|-------------|-----------|--------|
| TASK-001 | Compile Envelope I (Technical + masked Annexure 9) per REQ-014. | COMP-012 | Bid Manager |
| TASK-002 | Compile Envelope II (Commercial) per REQ-014. | COMP-008, COMP-012 | Bid Manager |
| TASK-003 | Execute Annexure 04 undertaking (REQ-011) and Annexure 6 No Deviation (REQ-015). | COMP-012, COMP-009 | Bid Manager |
| TASK-004 | Submit Bangalore Self-Declaration (REQ-013). | COMP-011, COMP-012 | Bid Manager |
| TASK-005 | Pay tender processing fee and EMD via DD/NEFT (REQ-022). | COMP-012 | Finance |
| TASK-006 | Validate eligibility pack against Certificate of Incorporation, audited financials, ISO 27001 (REQ-020). | COMP-012 | Bid Manager |
| TASK-007 | Resolve pre-bid open questions (F-01..F-09, Q-001..Q-010). | COMP-001..COMP-013 | Solution Lead |
| TASK-008 | Finalise SLA targets, scope of integrations, audit cadence, data residency position (per F-01..F-03, F-11). | COMP-009, COMP-010 | Solution Lead |

### 2.2 Mobilisation (Post-Award, Months 0–3)

| Task ID | Description | Component | Owner |
|---------|-------------|-----------|--------|
| TASK-101 | Set up Bangalore onsite/near-site facility (clean desk, screen privacy, visitor logs). | COMP-011 | Delivery Manager |
| TASK-102 | Recruit and onboard delivery team per indicative role-mix (Annexure 9). | COMP-002, COMP-011 | HR / Delivery Manager |
| TASK-103 | Establish shift rotation plan (per F-09) and on-call rota. | COMP-002 | Delivery Manager |
| TASK-104 | Stand up CI/CD pipeline; integrate security tooling. | COMP-006, COMP-007, COMP-009 | Tech Lead |
| TASK-105 | Stand up SIEM, logging, monitoring, ITSM. | COMP-002, COMP-009 | Security Lead |
| TASK-106 | Stand up documentation repository and knowledge base. | COMP-004 | Tech Lead |
| TASK-107 | Establish Steering Committee cadence with IIITB PMO (per F-07). | COMP-013 | Delivery Manager |
| TASK-108 | Sign NDA and confidentiality undertakings for all staff. | COMP-010 | HR / Legal |
| TASK-109 | Baseline ISO 27001 ISMS / Annexure 04 controls; confirm scope with IIITB (F-04). | COMP-009 | Security Lead |
| TASK-110 | Confirm integration interfaces with TMC, GRS, CTI/IVR, EHR owners (F-02). | COMP-003 | Solution Architect |
| TASK-111 | Confirm Level 3 ownership and handoff model (F-08). | COMP-003, COMP-006 | Tech Lead |
| TASK-112 | Confirm data residency position (F-03). | COMP-009, COMP-010 | Security Lead |
| TASK-113 | Confirm audit cadence with IIITB (F-11). | COMP-009 | Security Lead |
| TASK-114 | Confirm "market price" definition and pass-through trigger (F-05). | COMP-008 | Commercial Lead |

### 2.3 Steady-State Delivery (Months 3–36, with yearly renewals)

| Task ID | Description | Component | Owner |
|---------|-------------|-----------|--------|
| TASK-201 | Iterative development across UI/functional/back-end per release train. | COMP-001 | Tech Lead |
| TASK-202 | Documentation updates per layer (COMP-004) per release. | COMP-004 | All |
| TASK-203 | Integration testing coordination with Level 3 and external integrators. | COMP-003 | Test Lead |
| TASK-204 | Quarterly internal audits and external audit support. | COMP-009 | Security Lead |
| TASK-205 | Migration, enhancement, and upgrade waves per release calendar. | COMP-005 | Tech Lead |
| TASK-206 | Release notes, known-issues register, post-release monitoring. | COMP-006 | Tech Lead |
| TASK-207 | Defect management and preventive maintenance. | COMP-007 | QA Lead |
| TASK-208 | Shift-based L1/L2 support and incident response. | COMP-002 | Delivery Manager |
| TASK-209 | Monthly Steering Committee status and minutes. | COMP-013 | Delivery Manager |
| TASK-210 | Quarterly market price benchmarking for pass-through (F-05). | COMP-008 | Commercial Lead |
| TASK-211 | Yearly renewal evidence pack and performance report. | COMP-008, COMP-013 | Commercial Lead |
| TASK-212 | Accessibility audits and language additions. | COMP-014 | Tech Lead |
| TASK-213 | Maintain confidentiality controls; periodic access recertification. | COMP-010 | Security Lead |

---

## 3. Test Plan (TEST-NNN)

| Test ID | Description | Component | Type |
|---------|-------------|-----------|------|
| TEST-001 | Unit tests per layer (UI/functional/back-end) with coverage thresholds. | COMP-001 | Unit |
| TEST-002 | Integration tests across services and integration adapters. | COMP-003 | Integration |
| TEST-003 | Contract tests for TMC, GRS, CTI/IVR, EHR interfaces. | COMP-003 | Contract |
| TEST-004 | End-to-end teleconsultation scenarios (smoke + regression). | COMP-001, COMP-003 | E2E |
| TEST-005 | Performance and load tests against NFRs (F-01). | COMP-001 | Performance |
| TEST-006 | Security tests: SAST, DAST, SCA, secrets scanning in CI. | COMP-007, COMP-009 | Security |
| TEST-007 | Penetration test (annual external). | COMP-009 | Security |
| TEST-008 | Accessibility audit (WCAG 2.1 AA) per release. | COMP-014 | Accessibility |
| TEST-009 | DR/backup restore test (per F-01 RTO/RPO). | COMP-005, COMP-009 | DR |
| TEST-010 | UAT with IIITB/MOHFW/NIMHANS stakeholders. | COMP-001, COMP-013 | UAT |
| TEST-011 | Migration rehearsal in pre-prod. | COMP-005 | Migration |
| TEST-012 | Shift handover / on-call drill (L1/L2). | COMP-002 | Operational |
| TEST-013 | Audit evidence pack walk-through with IIITB. | COMP-009 | Audit |

---

## 4. Rollout Strategy

1. **Discovery (Weeks 1–4):** Confirm interfaces (F-02), SLA targets (F-01), data residency (F-03), audit cadence (F-11), Level 3 ownership (F-08).
2. **Foundation (Weeks 5–12):** Stand up Bangalore facility, CI/CD, monitoring, security baseline, documentation repository.
3. **Iterative Delivery (Months 4–36):** Release train (e.g., monthly); layered development; continuous integration testing; quarterly migrations/enhancements.
4. **Yearly Renewal Gates:** Annual performance review; renewal decision per REQ-010.
5. **Exit/Extension:** Final "No Claim" certificate (REQ-017); optional 2-year extension (F-17).

### Rollout Principles
- Canary deployments with automated rollback hooks.
- Masked data only in non-prod.
- All releases signed and audit-logged.
- Post-release monitoring window (per REQ-007) with go/no-go criteria.

---

## 5. Acceptance Criteria

| ID | Criterion | Mapped REQ(s) |
|----|-----------|----------------|
| AC-01 | Layered application delivered across UI/functional/back-end with layer-specific documentation. | REQ-001, REQ-002 |
| AC-02 | All integration testing artefacts (contract tests, mocks) operational and integrated into CI. | REQ-003, REQ-008 |
| AC-03 | Migration and upgrade pipeline executed at least once per quarter with rollback evidence. | REQ-004 |
| AC-04 | Platform availability and stability targets met (pending F-01 confirmation). | REQ-005 |
| AC-05 | Shift-based L1/L2 support active with documented SOPs and on-call coverage. | REQ-006 |
| AC-06 | Release notes, known issues register, and post-release monitoring reports published per release. | REQ-007 |
| AC-07 | Best-practice maintenance evidenced by defect trends, tech debt register, and code-quality gates. | REQ-009 |
| AC-08 | Yearly renewal package delivered with performance evidence. | REQ-010 |
| AC-09 | ISO 27001 (or Annexure 04 equivalent) controls operational and audited. | REQ-011 |
| AC-10 | Confidentiality controls validated; no unauthorised disclosures; periodic access recertification. | REQ-012 |
| AC-11 | Bangalore Self-Declaration in force; staff onsite/near-site per plan. | REQ-013 |
| AC-12 | Bid pack compliant with two-stage offline format and mandatory annexures. | REQ-014, REQ-015, REQ-022 |
| AC-13 | Pass-through governance evidenced via quarterly benchmarking (F-05). | REQ-016 |
| AC-14 | "No Claim" certificate executed at contract closure with all entitlements settled. | REQ-017 |
| AC-15 | Steering Committee meetings held per cadence; minutes shared with PMO. | REQ-018 |
| AC-16 | Accessibility (WCAG 2.1 AA) and multilingual coverage evidenced. | REQ-019 |
| AC-17 | Eligibility pack accepted by IIITB in Stage 1. | REQ-020 |
| AC-18 | Contract signed exclusively between IIITB and Bidder. | REQ-021 |

---

## 6. Risks & Mitigations

| Risk ID | Risk | Severity | Mitigation | Linked Finding/Component |
|---------|------|----------|------------|---------------------------|
| R-01 | Pre-bid query cut-off missed; bid disqualified. | High | Calendar lock; bid manager weekly checkpoint. | F-14 |
| R-02 | SLA penalty exposure due to undefined quantitative targets (F-01). | High | Pre-bid query; contractually cap or define penalty cap. | F-01, COMP-002 |
| R-03 | Data residency unclear; could force redesign or breach local laws (F-03). | High | Pre-bid query; default to India-only storage; legal review. | F-03, COMP-009, COMP-010 |
| R-04 | "No Claim" certificate signed before entitlements settled. | Medium | Settlement checklist; legal sign-off. | F-12, COMP-008 |
| R-05 | Pass-through obligation compresses margin (F-05). | Medium | Market-indexed rate card; quarterly benchmark trigger (DEC-008). | F-05, COMP-008 |
| R-06 | Yearly renewal not granted; revenue cliff (F-13). | Medium | Size fixed costs to Year 1; renewal upside optionality. | F-13, COMP-008 |
| R-07 | Integration interfaces ambiguous; rework risk (F-02). | High | Pre-bid query; phased integration design with mocks. | F-02, COMP-003 |
| R-08 | Level 3 ownership unclear; deployment-script coordination delays (F-08). | Medium | Define shared release process early; contractual SLA for Level 3 handoff. | F-08, COMP-006 |
| R-09 | Audit cadence undefined; over- or under-audit cost (F-11). | Medium | Pre-bid query; align internal/external audit windows. | F-11, COMP-009 |
| R-10 | Bangalore onsite constraint limits talent pool in niche skills. | Medium | Hybrid near-site policy; relocation support; cross-training. | F-09, COMP-011 |
| R-11 | Confidentiality breach involving PHI; regulatory and reputational exposure. | Critical | Encryption + RBAC + audit + IR + breach response runbook. | COMP-009, COMP-010 |
| R-12 | Hardware upgrade scope creep (F-06). | Medium | Clarify scope in pre-bid; treat infra upgrades only. | F-06, COMP-005 |

---

## 7. Dependencies

| Dependency | Type | Owner | Linked Component(s) |
|------------|------|--------|----------------------|
| D-01: IIITB clarification on SLA targets (F-01). | External (Customer) | Bid/Solution Lead | COMP-002, COMP-005, COMP-006 |
| D-02: IIITB clarification on integration interfaces (F-02). | External (Customer / TMC, GRS, CTI/IVR, EHR owners) | Solution Architect | COMP-003, COMP-001 |
| D-03: IIITB clarification on data residency (F-03). | External (Customer / Legal) | Security Lead | COMP-009, COMP-010 |
| D-04: IIITB clarification on Annexure 04 equivalence (F-04). | External (Customer) | Security Lead | COMP-009 |
| D-05: IIITB clarification on "market price" definition (F-05). | External (Customer / Commercial) | Commercial Lead | COMP-008 |
| D-06: IIITB clarification on shift pattern (F-09). | External (Customer / Operations) | Delivery Manager | COMP-002 |
| D-07: Steering Committee cadence (F-07). | External (Customer / PMO) | Delivery Manager | COMP-013 |
| D-08: Level 3 team ownership and handoff model (F-08). | External (Customer / Level 3 team) | Tech Lead | COMP-003, COMP-006 |
| D-09: Audit cadence (F-11). | External (Customer / MOHFW / NIMHANS) | Security Lead | COMP-009 |
| D-10: Pre-bid query and bid submission deadlines (F-10). | External (Customer) | Bid Manager | COMP-012 |
| D-11: ISO 27001 certification body selection (if certification route chosen). | External (Auditor) | Security Lead | COMP-009 |
| D-12: Cloud/infra tenancy (IIITB-provided or bidder-managed). | External (Customer) | Tech Lead | COMP-001, COMP-005 |
| D-13: Bidder letter extension language (F-17). | External (Customer) | Commercial Lead | COMP-008 |
| D-14: IIITB IdP federation for staff SSO. | External (Customer) | Security Lead | COMP-009 |

---

## 8. Decision References

- DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, DEC-006, DEC-007, DEC-008, DEC-009, DEC-010 (from hld.md) all flow into this blueprint.
- DEC-006 (Security Framework) and DEC-007 (Release Management) underpin the Secure SDLC and audit-evidence generation plan.
- DEC-005 (Bangalore Operating Model) anchors the delivery setup in TASK-101..TASK-103.