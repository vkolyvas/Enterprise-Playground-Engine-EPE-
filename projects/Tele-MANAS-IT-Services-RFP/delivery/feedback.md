---
checksum_sha256: 0129f1d7926612723ed5af594e468d2eef589cf9b5a82209fa20d1beacdc76f3
contract: delivery.feedback
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:06:42.109957+00:00'
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

# Feedback — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore

This artefact is consumed by Product and Bid leadership. Each entry links a feedback item to the relevant REQ-NNN, COMP-NNN, TASK-NNN, and/or TEST-NNN so that improvement actions can be routed.

---

## 1. Incident & Defect Feedback

| FB ID | Date | Item | Linked REQ | Linked COMP | Linked TASK | Linked TEST | Severity | Resolution | Lessons / Improvement |
|-------|------|------|------------|-------------|-------------|-------------|----------|------------|------------------------|
| FB-I-001 | | Sev-1 incident summary | REQ-005 | COMP-001, COMP-002 | TASK-208 | TEST-004 | | | |
| FB-I-002 | | Recurring Sev-2 pattern | REQ-006 | COMP-002 | TASK-208 | TEST-012 | | | |
| FB-I-003 | | Integration partner downtime impact | REQ-003 | COMP-003 | TASK-203 | TEST-003 | | | |
| FB-I-004 | | Suspected PHI exposure (R-11 trigger) | REQ-011, REQ-012 | COMP-009, COMP-010 | TASK-213 | TEST-006 | | | |

---

## 2. Cost Variance Feedback

| FB ID | Period | Line Item | Planned | Actual | Variance | Linked REQ | Linked COMP | Linked TASK | Notes |
|-------|--------|-----------|---------|--------|----------|------------|-------------|-------------|-------|
| FB-C-001 | | Resource mix (Annexure 9) | | | | REQ-013 | COMP-011 | TASK-102 | |
| FB-C-002 | | Pass-through trigger | | | | REQ-016 | COMP-008 | TASK-210 | F-05 |
| FB-C-003 | | Renewal-year commercial change | | | | REQ-010 | COMP-008 | TASK-211 | |
| FB-C-004 | | Audit cost (annual external) | | | | REQ-011 | COMP-009 | TASK-204 | |

---

## 3. Usage Telemetry

| FB ID | Metric | Source | Linked REQ | Linked COMP | Linked TASK | Observation |
|-------|--------|--------|------------|-------------|-------------|-------------|
| FB-U-001 | Teleconsultation sessions / day | APM | REQ-005 | COMP-001 | TASK-201 | |
| FB-U-002 | Peak concurrent users | APM | REQ-005 | COMP-001 | TASK-201 | (feeds TEST-005) |
| FB-U-003 | Multilingual usage distribution | UI telemetry | REQ-019 | COMP-014 | TASK-212 | |
| FB-U-004 | IVR fallback rate | Telephony logs | REQ-019 | COMP-014 | TASK-212 | (low-bandwidth resilience) |
| FB-U-005 | Grievances raised / resolved | App | REQ-001 | COMP-001 | TASK-201 | (R-05 margin not affected) |
| FB-U-006 | Accessibility feature usage (screen reader, high-contrast) | UI telemetry | REQ-019 | COMP-014 | TASK-212 | |

---

## 4. Deployment / Release Feedback

| FB ID | Release | Item | Linked REQ | Linked COMP | Linked TASK | Linked TEST | Outcome |
|-------|---------|------|------------|-------------|-------------|-------------|---------|
| FB-D-001 | | Canary metrics | REQ-007 | COMP-006 | TASK-206 | TEST-004 | |
| FB-D-002 | | Rollback triggered (yes/no) | REQ-004 | COMP-005, COMP-006 | TASK-205, TASK-206 | TEST-009, TEST-011 | |
| FB-D-003 | | Migration duration vs plan | REQ-004 | COMP-005 | TASK-205 | TEST-011 | |
| FB-D-004 | | Deployment-script co-authoring friction with Level 3 | REQ-008 | COMP-003, COMP-006 | TASK-111, TASK-203 | TEST-003 | (R-08) |
| FB-D-005 | | Release notes clarity feedback | REQ-007 | COMP-004, COMP-006 | TASK-202, TASK-206 | — | |

---

## 5. Customer Feedback

| FB ID | Date | Source | Feedback Theme | Linked REQ | Linked COMP | Linked TASK | Action |
|-------|------|--------|----------------|------------|-------------|-------------|--------|
| FB-CU-001 | | IIITB PMO | Governance / SC effectiveness | REQ-018 | COMP-013 | TASK-209 | |
| FB-CU-002 | | IIITB Security | Audit findings / cycle | REQ-011 | COMP-009 | TASK-204, TASK-213 | |
| FB-CU-003 | | End-user (clinician) | Multilingual UX | REQ-019 | COMP-014 | TASK-212 | |
| FB-CU-004 | | End-user (caller) | IVR fallback quality | REQ-019 | COMP-014 | TASK-212 | |
| FB-CU-005 | | Integration partner | Contract test stability | REQ-003 | COMP-003 | TASK-203, TASK-111 | |
| FB-CU-006 | | MOHFW observer | Renewal evidence pack | REQ-010 | COMP-008, COMP-013 | TASK-211 | |

---

## 6. Operational Lessons Learned

| FB ID | Theme | Observation | Linked REQ | Linked COMP | Linked TASK | Linked TEST | Improvement |
|-------|-------|-------------|------------|-------------|-------------|-------------|-------------|
| FB-O-001 | Shift handover | Handover gaps caused delay | REQ-006 | COMP-002 | TASK-103, TASK-208 | TEST-012 | Improve handover checklist |
| FB-O-002 | On-call escalation | Late L2 engagement | REQ-006 | COMP-002 | TASK-103 | TEST-012 | Tighten escalation triggers |
| FB-O-003 | Steering Committee cadence | Cadence needs adjustment | REQ-018 | COMP-013 | TASK-107, TASK-209 | — | Reconfirm F-07 |
| FB-O-004 | Bangalore onsite constraint | Talent gap in niche skills | REQ-013 | COMP-011 | TASK-102 | — | R-10 mitigation: hybrid near-site |
| FB-O-005 | Pre-bid query cut-off | Tight window | REQ-014 | COMP-012 | TASK-007 | — | R-01: calendar lock |
| FB-O-006 | Data residency ambiguity | Required design rework | REQ-011, REQ-012 | COMP-009, COMP-010 | TASK-112 | — | R-03: pre-bid query, default India-only |
| FB-O-007 | Pass-through margin compression | Trigger matrix too sensitive | REQ-016 | COMP-008 | TASK-210 | — | R-05: recalibrate matrix |
| FB-O-008 | Renewal cycle | Evidence not bundled | REQ-010 | COMP-008, COMP-013 | TASK-211 | — | R-06: monthly assembly |
| FB-O-009 | Hardware upgrade scope creep | Scope ambiguity | REQ-004 | COMP-005 | TASK-205 | — | R-12: clarify F-06 |
| FB-O-010 | Integration ambiguity | Rework cost | REQ-003 | COMP-003 | TASK-110, TASK-203 | TEST-003 | R-07: phased design + mocks |

---

## 7. Risk & Decision Backlog (carried forward)

| FB ID | Linked Risk | Linked Decision | Suggested Action | Owner |
|-------|-------------|------------------|------------------|-------|
| FB-R-001 | R-01 | — | Calendar lock for pre-bid queries | Bid Manager |
| FB-R-002 | R-02 | — | Define SLA penalty cap in contract | Commercial Lead |
| FB-R-003 | R-03 | — | Default to India-only data residency | Security Lead |
| FB-R-004 | R-04 | — | Settlement checklist before "No Claim" | Commercial Lead |
| FB-R-005 | R-05 | DEC-008 | Recalibrate market-index trigger | Commercial Lead |
| FB-R-006 | R-06 | — | Size fixed costs to Year 1 | Commercial Lead |
| FB-R-007 | R-07 | — | Phased integration with mocks | Solution Architect |
| FB-R-008 | R-08 | — | Contractual SLA for Level 3 handoff | Tech Lead |
| FB-R-009 | R-09 | — | Align internal/external audit windows | Security Lead |
| FB-R-010 | R-10 | DEC-005 | Hybrid near-site policy | Delivery Manager |
| FB-R-011 | R-11 | DEC-006 | Reinforce encryption + RBAC + IR | Security Lead |
| FB-R-012 | R-12 | — | Clarify hardware upgrade scope | Tech Lead |

---

## 8. Submission to Product

- **Cadence:** monthly consolidation of all FB-* into a Product feedback pack.
- **Format:** this document + attachments (incident postmortems, benchmark reports, telemetry charts).
- **Routing:** Product Owner → Bid Leadership → Engineering → Security → Commercial.
- **Closure loop:** each item must map to either a backlog entry, a DEC-NNN, a risk update, or a documented acceptance that no action is required.