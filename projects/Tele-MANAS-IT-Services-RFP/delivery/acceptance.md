---
checksum_sha256: 89564336bb0e809bf7276a276c690a4a4331986f9636535a1d49adf6e95298f2
contract: delivery.acceptance
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:06:42.108169+00:00'
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

# Acceptance — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore

This document records executed tests and acceptance evidence against AC-01..AC-18 (per blueprint). Each AC is signed off by the Bidder Architect and the IIITB Customer Representative. Status values: `Pending`, `In Progress`, `Passed`, `Failed`, `Waived`.

---

## Acceptance Register

| AC ID | Criterion | REQ(s) | Tests Invoked | Evidence Reference | Status | Date | Architect Sign-off | Customer Sign-off |
|-------|-----------|--------|---------------|--------------------|--------|------|---------------------|--------------------|
| AC-01 | Layered application delivered across UI/functional/back-end with layer-specific documentation | REQ-001, REQ-002 | TEST-001, TEST-004, TEST-010 | Layer doc-set v1.0; coverage report; UAT minutes | Pending | — | _________________ | _________________ |
| AC-02 | All integration testing artefacts (contract tests, mocks) operational and integrated into CI | REQ-003, REQ-008 | TEST-002, TEST-003 | Pact reports; CI dashboard | Pending | — | _________________ | _________________ |
| AC-03 | Migration and upgrade pipeline executed ≥ once per quarter with rollback evidence | REQ-004 | TEST-009, TEST-011 | Migration log; rollback drill evidence | Pending | — | _________________ | _________________ |
| AC-04 | Platform availability and stability targets met (pending F-01) | REQ-005 | TEST-005, TEST-009 | Perf report; APM availability SLO board | Pending | — | _________________ | _________________ |
| AC-05 | Shift-based L1/L2 support active with documented SOPs and on-call coverage | REQ-006 | TEST-012 | Shift roster; SOP set; on-call drill minutes | Pending | — | _________________ | _________________ |
| AC-06 | Release notes, known issues register, post-release monitoring reports published per release | REQ-007 | TEST-002/004/006 (CI gates) | Release note index; post-release report | Pending | — | _________________ | _________________ |
| AC-07 | Best-practice maintenance evidenced by defect trends, tech debt register, code-quality gates | REQ-009 | TEST-006 | Defect dashboard; tech-debt backlog; gate report | Pending | — | _________________ | _________________ |
| AC-08 | Yearly renewal package delivered with performance evidence | REQ-010 | (Cross-cuts) | Renewal pack; Steering minutes | Pending | — | _________________ | _________________ |
| AC-09 | ISO 27001 (or Annexure 04 equivalent) controls operational and audited | REQ-011 | TEST-006, TEST-007, TEST-013 | ISMS pack; audit minutes; pen-test report | Pending | — | _________________ | _________________ |
| AC-10 | Confidentiality controls validated; no unauthorised disclosures; periodic access recertification | REQ-012 | TEST-006, TEST-013 | Access recertification log; IR drill record | Pending | — | _________________ | _________________ |
| AC-11 | Bangalore Self-Declaration in force; staff onsite/near-site per plan | REQ-013 | TEST-012 | Signed declaration; HR roster; facility checklist | Pending | — | _________________ | _________________ |
| AC-12 | Bid pack compliant with two-stage offline format and mandatory annexures | REQ-014, REQ-015, REQ-022 | (Pre-award) | Bid acknowledgement; annexure checklist | Pending | — | _________________ | _________________ |
| AC-13 | Pass-through governance evidenced via quarterly benchmarking (F-05) | REQ-016 | (Commercial) | Quarterly benchmark report; trigger log | Pending | — | _________________ | _________________ |
| AC-14 | "No Claim" certificate executed at contract closure with all entitlements settled | REQ-017 | (Closure) | Settlement checklist; signed certificate | Pending | — | _________________ | _________________ |
| AC-15 | Steering Committee meetings held per cadence; minutes shared with PMO | REQ-018 | TEST-010 (UAT presence), TEST-013 | SC minutes archive | Pending | — | _________________ | _________________ |
| AC-16 | Accessibility (WCAG 2.1 AA) and multilingual coverage evidenced | REQ-019 | TEST-008 | Accessibility audit; language coverage matrix | Pending | — | _________________ | _________________ |
| AC-17 | Eligibility pack accepted by IIITB in Stage 1 | REQ-020 | (Pre-award) | Stage 1 acceptance letter | Pending | — | _________________ | _________________ |
| AC-18 | Contract signed exclusively between IIITB and Bidder | REQ-021 | (Award) | Signed contract cover page | Pending | — | _________________ | _________________ |

---

## Test Execution Log (Template)

For each release train, the following entries are recorded. Fill per cycle:

| Test ID | Date | Env | Result | Evidence Link | Defects Raised | Notes |
|---------|------|-----|--------|---------------|----------------|-------|
| TEST-001 | | | PASS/FAIL | | | |
| TEST-002 | | | PASS/FAIL | | | |
| TEST-003 | | | PASS/FAIL | | | |
| TEST-004 | | | PASS/FAIL | | | |
| TEST-005 | | | PASS/FAIL | | | |
| TEST-006 | | | PASS/FAIL | | | |
| TEST-007 | | | PASS/FAIL | | | |
| TEST-008 | | | PASS/FAIL | | | |
| TEST-009 | | | PASS/FAIL | | | |
| TEST-010 | | | PASS/FAIL | | | |
| TEST-011 | | | PASS/FAIL | | | |
| TEST-012 | | | PASS/FAIL | | | |
| TEST-013 | | | PASS/FAIL | | | |

---

## Sign-off Block

**Bidder Architect (Solution Lead):**  ____________________________   Date: ___________

**Customer Representative (IIITB PMO):** ____________________________   Date: ___________

**Customer Representative (IIITB Security):** ____________________________   Date: ___________

**Customer Representative (IIITB Commercial):** ____________________________   Date: ___________

---

## Open Items / Exceptions

| Item ID | Description | Linked AC | Owner | Target Resolution |
|---------|-------------|-----------|-------|-------------------|
| OE-01 | F-01 SLA/RTO/RPO pending confirmation | AC-04 | Solution Lead | Pre-prod gate |
| OE-02 | F-02 integration interfaces pending | AC-02 | Solution Architect | Pre-merge gate |
| OE-03 | F-03 data residency pending | AC-09, AC-10 | Security Lead | Pre-foundation |
| OE-04 | F-05 market price definition pending | AC-13 | Commercial Lead | Pre-steady-state |