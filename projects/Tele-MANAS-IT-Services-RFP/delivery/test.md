---
checksum_sha256: efa3ce9b65449dc8009771067c0eb1a3f7c8c433f42c37380b1146c9802dc869
contract: delivery.test
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:06:42.107819+00:00'
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

# Test Plan — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore

Each test from the architecture blueprint (TEST-NNN) is mapped below to its REQ-NNN(s), COMP-NNN(s), and the AC-NNN acceptance criterion it evidences. Test types, prerequisites and exit evidence are also captured.

---

## Test Mapping Table

| Test ID | Description | Type | REQ-NNN | COMP-NNN | AC-NNN | Prerequisite | Exit Evidence |
|---------|-------------|------|---------|----------|--------|--------------|---------------|
| TEST-001 | Unit tests per layer (UI/functional/back-end) with coverage thresholds | Unit | REQ-001, REQ-002 | COMP-001 | AC-01 | Code merged to main | Coverage report ≥ threshold per layer |
| TEST-002 | Integration tests across services and integration adapters | Integration | REQ-003, REQ-008 | COMP-003 | AC-02 | Contract definitions stable | Green integration suite in CI; defect log |
| TEST-003 | Contract tests for TMC, GRS, CTI/IVR, EHR interfaces | Contract | REQ-003 | COMP-003 | AC-02 | F-02 interfaces confirmed | Pact/equivalent reports per interface; partner sign-off |
| TEST-004 | End-to-end teleconsultation scenarios (smoke + regression) | E2E | REQ-001, REQ-005 | COMP-001, COMP-003 | AC-01, AC-04 | Test data + integrations stubbed | E2E suite green in pre-prod |
| TEST-005 | Performance and load tests against NFRs (F-01) | Performance | REQ-005 | COMP-001 | AC-04 | F-01 NFR targets confirmed | Load-test report; latency/throughput against NFRs |
| TEST-006 | Security tests: SAST, DAST, SCA, secrets scanning in CI | Security | REQ-011, REQ-009 | COMP-007, COMP-009 | AC-07, AC-09 | Tooling integrated in CI | Scan reports; zero Critical/High unaddressed |
| TEST-007 | Penetration test (annual external) | Security | REQ-011 | COMP-009 | AC-09 | Pre-prod stable | Pen-test report; remediation log |
| TEST-008 | Accessibility audit (WCAG 2.1 AA) per release | Accessibility | REQ-019 | COMP-014 | AC-16 | UI builds available | Audit report; conformance statement |
| TEST-009 | DR/backup restore test (per F-01 RTO/RPO) | DR | REQ-004, REQ-005, REQ-011 | COMP-005, COMP-009 | AC-03, AC-04 | RTO/RPO confirmed (F-01) | Successful restore within RTO/RPO |
| TEST-010 | UAT with IIITB/MOHFW/NIMHANS stakeholders | UAT | REQ-001, REQ-018 | COMP-001, COMP-013 | AC-01, AC-15 | E2E + perf green | UAT sign-off; punch-list closed |
| TEST-011 | Migration rehearsal in pre-prod | Migration | REQ-004 | COMP-005 | AC-03 | Schema + data migrations ready | Successful rehearsal; rollback evidence |
| TEST-012 | Shift handover / on-call drill (L1/L2) | Operational | REQ-006 | COMP-002 | AC-05 | Shift rota in place | Drill report; mean response/resolution times |
| TEST-013 | Audit evidence pack walk-through with IIITB | Audit | REQ-011 | COMP-009 | AC-09 | ISMS baselined | Walk-through minutes; finding closure |

---

## Per-Component Coverage Matrix

| Component | Tests Covering It | REQs Evidenced |
|-----------|-------------------|----------------|
| COMP-001 (Application Platform) | TEST-001, TEST-004, TEST-005, TEST-010 | REQ-001, REQ-019 |
| COMP-002 (Platform Ops & L1/L2) | TEST-012 | REQ-005, REQ-006 |
| COMP-003 (Integration & Test Harness) | TEST-002, TEST-003, TEST-004 | REQ-003, REQ-008 |
| COMP-004 (Documentation) | TEST-001 (doc-drift CI hook), TEST-008 (audit refs) | REQ-002, REQ-007 |
| COMP-005 (Migration & Upgrade) | TEST-009, TEST-011 | REQ-004 |
| COMP-006 (Release & Deployment) | TEST-002 (CI gate), TEST-006 (CI security) | REQ-007, REQ-008 |
| COMP-007 (Maintenance & QE) | TEST-006 | REQ-009 |
| COMP-008 (Commercial & Contract) | (Audit walk-through TEST-013 references line items) | REQ-010, REQ-016, REQ-017, REQ-021 |
| COMP-009 (Security & Compliance) | TEST-006, TEST-007, TEST-009, TEST-013 | REQ-011 |
| COMP-010 (Confidentiality & Data Gov) | TEST-006, TEST-007, TEST-009 | REQ-012 |
| COMP-011 (Bangalore Delivery) | TEST-012 (on-call drill) | REQ-013 |
| COMP-012 (Bid Submission) | (Pre-award; covered by AC-12, AC-17) | REQ-014, REQ-015, REQ-020, REQ-022 |
| COMP-013 (Governance / SC) | TEST-010 (UAT), TEST-013 (audit) | REQ-018 |
| COMP-014 (Accessibility) | TEST-008 | REQ-019 |

---

## Test Gates by Release Train

- **Pre-merge gate:** TEST-001 + TEST-006 (SAST/SCA/secrets) must be green.
- **Pre-stage gate:** TEST-002 + TEST-003 must be green.
- **Pre-canary gate:** TEST-004 + TEST-005 must be green against NFRs.
- **Pre-promote-to-prod gate:** TEST-008 (accessibility) green; TEST-009 (DR) within last quarter.
- **Pre-renewal gate:** TEST-013 (audit walk-through) closed; TEST-012 (operational drill) within last 6 months.

---

## Quarterly Audit Pack (feeds TEST-013 / AC-09)

- Latest TEST-006, TEST-007 reports.
- DR drill (TEST-009) record.
- Internal audit report (TASK-204).
- Remediation tracker.