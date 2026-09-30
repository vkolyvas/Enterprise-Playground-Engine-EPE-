---
checksum_sha256: ee5ec76605e17932a7c2940311b22171d4c65c42e41fa3edf34c9f3e1b6a16fb
contract: architecture.lld
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:02:42.865869+00:00'
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

# Low-Level Design (LLD) — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore
**Source(s):** [DOC-B585FB4B498A]

This LLD provides per-component detailed design: interfaces, data models, configurations, failure modes, and runbook stubs.

---

## COMP-001 — Application Platform

**Purpose:** Layered (UI / functional / back-end) Tele-MANAS application with accessibility features.
**Mapped REQs:** REQ-001, REQ-019

### Logical View

- **UI tier:** Responsive web (WCAG 2.1 AA-aligned); mobile-first; multilingual (English + scheduled Indian languages per IIITB direction).
- **Functional tier:** Business services (patient intake, teleconsultation session, grievance capture, escalation).
- **Back-end tier:** Data access services; repositories; domain model.

### Interfaces

- **Inbound:** HTTPS/REST (JSON); WebSocket for real-time teleconsultation.
- **Outbound:** REST/gRPC to COMP-003 (Integration Adapter Plane).
- **Admin:** Internal REST for PMO/staff.

### Data Model (Conceptual)

- `Patient` (id, demographics, contact, identity-proof method).
- `Episode` (id, patient_id, opened_at, status, channel).
- `Consultation` (id, episode_id, clinician_id, started_at, ended_at, notes).
- `Grievance` (id, episode_id, category, status, escalated_at).
- `AuditEvent` (id, actor, action, resource, timestamp, hash).

### Failure Modes
- **UI unavailability:** Activate IVR fallback; degrade gracefully.
- **Functional tier fault:** Circuit breakers; retry with backoff; queue overflow to async worker.
- **Back-end/DB fault:** Read replica fallback; failover; degraded mode.

### Runbook Stub
1. Detect alert (5xx surge, latency, error rate).
2. On-call L1 triage (COMP-002); escalate to L2.
3. Roll back to last green release (COMP-006).
4. Open incident; notify IIITB PMO.

---

## COMP-002 — Platform Operations & L1/L2 Support

**Purpose:** Shift-based Level 1/Level 2 support for teleconsultation and platform operations.
**Mapped REQs:** REQ-005, REQ-006

### Operating Model

- **Indicative staffing (per RFP Annexure 9):** Tech Support Engineer × 6 (shift-wise) for Level 1/Level 2 coverage; Project Manager — Support × 1.
- **Shift pattern:** To be confirmed (F-09); recommend 3-shift rotation covering extended hours including weekends/holidays, given national teleconsultation footprint.
- **Channels:** Phone, email, ITSM portal, on-call escalation.

### Interfaces

- ITSM tool (e.g., service desk) for ticket lifecycle.
- Monitoring stack integration (SIEM, APM).
- Knowledge base (COMP-004) for SOPs.

### Failure Modes
- **L1 capacity shortfall:** Cross-shift backup; surge protocol.
- **Critical incident after-hours:** On-call rota; L2 pager; IIITB escalation matrix.

### Runbook Stub
1. Receive ticket via ITSM/phone.
2. Triage by severity; assign SLA timer.
3. Run SOP; escalate to L2/Level 3/IIITB per matrix.
4. Resolve, document, close.
5. Weekly trend report to PMO (COMP-013).

---

## COMP-003 — Integration & Test Harness

**Purpose:** Integration testing support and cross-team coordination with Level 3 and external integrators.
**Mapped REQs:** REQ-003, REQ-008

### Components

- **Contract tests:** Per-integration contract test suite (Pact/equivalent).
- **Mock services:** Sandbox stubs for TMC, GRS, CTI/IVR, EHR (interfaces pending F-02).
- **Test data management:** Masked/synthetic test data; no raw PHI in non-prod.
- **CI gate:** Automated integration test execution on every PR.

### Interfaces
- Inbound: Service contracts from COMP-001.
- Outbound: Test reports; defect reports.

### Failure Modes
- **Flaky tests:** Quarantine; root-cause; quarantine window.
- **Integration partner unavailable:** Mock fallback; communicate to IIITB.

### Runbook Stub
1. PR triggers integration test pipeline.
2. Failures triaged by integration test team.
4. Coordinate deployment-script co-authoring with Level 3.

---

## COMP-004 — Documentation & Knowledge Repository

**Purpose:** Layer-specific documentation; SOPs; runbooks; release notes; known issues register.
**Mapped REQs:** REQ-002, REQ-007

### Components

- UI layer docs (component specs, accessibility notes).
- Functional layer docs (service contracts, business rules).
- Back-end layer docs (data model, API specs).
- Operational docs (runbooks, SOPs).
- Release notes and known-issues register.

### Interfaces
- Markdown/HTML export; indexable search; integrated with ITSM.

### Failure Modes
- **Doc drift:** CI check that published API specs match implementation.

### Runbook Stub
1. Update doc on PR merge.
2. Review on release.
3. Publish to repository.

---

## COMP-005 — Migration & Upgrade Pipeline

**Purpose:** Migration, enhancement, and upgrade services.
**Mapped REQs:** REQ-004

### Components

- **Schema migration tool:** Versioned migrations; rollback scripts.
- **Data migration tool:** ETL with masked staging; reconciliation.
- **Upgrade orchestrator:** Phased rollout (canary → beta → full); automated rollback.

### Failure Modes
- **Migration failure:** Rollback to last snapshot; reconcile; communicate.
- **Upgrade rollback:** Trigger automated rollback; impact assessment.

### Runbook Stub
1. Plan migration/upgrade with IIITB (COMP-013).
2. Stage in pre-prod; run validation tests.
4. Execute in prod with canary.
5. Monitor; rollback if KPIs breach.

---

## COMP-006 — Release & Deployment Management

**Purpose:** Release notes, deployment scripts (with Level 3), automated deployments, post-release monitoring.
**Mapped REQs:** REQ-007, REQ-008

### Components

- **CI/CD pipeline:** Build → test → stage → canary → full.
- **Deployment scripts:** Co-authored with Level 3 (F-08); versioned.
- **Release notes:** Generated from PR/issue tracker.
- **Known-issues register:** Linked to releases.
- **Post-release monitoring:** APM dashboards; SLO tracking; rollback hooks.

### Failure Modes
- **Failed deployment:** Automated rollback; incident.
- **Post-release regression:** Trigger hotfix or rollback.

### Runbook Stub
1. Create release branch.
2. Generate release notes.
3. Deploy to canary.
4. Validate SLOs.
5. Promote or rollback.
6. Publish known issues.

---

## COMP-007 — Application Maintenance & Quality Engineering

**Purpose:** Best-practice maintenance, defect management, preventive maintenance, code-quality gates.
**Mapped REQs:** REQ-009

### Components

- **Defect tracker:** SLA-driven; root-cause tracking.
- **Code-quality gates:** SAST, SCA, coverage thresholds.
- **Tech debt register:** Tracked and prioritised.

### Runbook Stub
1. Triage defect.
2. Assign severity/SLA.
3. Fix; verify; close.
4. Capture lessons-learned.

---

## COMP-008 — Commercial & Contract Operations

**Purpose:** Commercial artefacts; line-item pricing; renewals; quantity alterations; pass-through governance; "No Claim" certificate handling.
**Mapped REQs:** REQ-010, REQ-016, REQ-017, REQ-021

### Components

- **Pricing catalogue:** Line-item unit rates; role-mix rate card (per RFP indicative role-mix).
- **Quantity governance:** Tracked alterations; ceiling alerts.
- **Pass-through governance:** Quarterly market price benchmarking; trigger matrix (per F-05).
- **Renewal tracker:** Yearly renewal milestones; performance evidence.
- **"No Claim" certificate workflow:** Entitlements register; final settlement checklist.

### Runbook Stub
1. Receive commercial change request.
2. Validate against line-item rates and quantity governance.
3. Apply pass-through if triggered.
4. Update contract ops record.

---

## COMP-009 — Security & Compliance Framework

**Purpose:** ISO 27001 (or equivalent undertaking); Annexure 04; control mapping; audit support.
**Mapped REQs:** REQ-011

### Components

- **ISMS:** Policy pack; risk register; Statement of Annexure.
- **Control mapping:** ISO 27001 Annex A controls mapped to components C-01..C-17.
- **Audit support:** Quarterly internal audits; annual external; ad-hoc (F-11).

### Runbook Stub
1. Conduct scheduled audit.
2. Capture findings; track remediation.
3. Report to IIITB PMO.

---

## COMP-010 — Confidentiality & Data Governance

**Purpose:** Confidentiality controls for IIITB/Government/NIMHANS information including health/patient records.
**Mapped REQs:** REQ-012

### Components

- **Data classification:** Public / Internal / Confidential / Restricted.
- **Data handling matrix:** Per-class controls.
- **PHI access policy:** Need-to-know; time-bound; logged.
- **Breach response:** Notification matrix; coordinated disclosure.

### Runbook Stub
1. Classify data asset.
2. Apply handling controls.
3. On suspected breach: trigger IR; notify IIITB.

---

## COMP-011 — Bangalore Delivery Operations

**Purpose:** Onsite/near-site delivery operating model from Bangalore.
**Mapped REQs:** REQ-013

### Components

- Bangalore Self-Declaration (signed).
- Onsite facility setup (clean desk, screen privacy, visitor logs).
- Travel/relocation policy for staff.

### Runbook Stub
1. Onboard staff in Bangalore.
2. Apply onsite controls.
3. Quarterly compliance attestation.

---

## COMP-012 — Bid Submission & Governance

**Purpose:** Two-stage offline bid; Envelope I/II; Annexure 6; tender fee/EMD.
**Mapped REQs:** REQ-014, REQ-015, REQ-020, REQ-022

### Components

- **Envelope I:** Technical + masked Annexure 9 commercial.
- **Envelope II:** Commercial.
- **Mandatory annexures:** Annexure 2 Cover Letter, Annexure 4 Undertaking, Annexure 6 No Deviation, Annexure 9 Rate Card, Bangalore Self-Declaration, eligibility proofs (REQ-020), tender fee/EMD.

### Runbook Stub
1. Compile Stage 1 eligibility pack.
2. Compile Stage 2 technical bid.
3. Compile commercial bid.
4. Submit offline; track acknowledgement.

---

## COMP-013 — Governance & Steering Committee Liaison

**Purpose:** Steering Committee participation; PMO interface; records management.
**Mapped REQs:** REQ-018

### Components

- **Steering Committee cadence:** TBD (F-07); assume monthly with quarterly in-person (per RFP guidance).
- **PMO interface:** Status, risks, decisions log.
- **Records management:** Proceedings shared with PMO.

### Runbook Stub
1. Prepare monthly status pack.
2. Present to Steering Committee.
3. Capture minutes; circulate.

---

## COMP-014 — Accessibility & Inclusion Engineering

**Purpose:** Affordability/accessibility/availability for under-served populations.
**Mapped REQs:** REQ-019

### Components

- WCAG 2.1 AA conformance.
- Multilingual UI framework.
- Low-bandwidth resilience (progressive enhancement, IVR fallback).
- Assistive-tech support.

### Runbook Stub
1. Accessibility audit per release.
2. Language coverage review.
3. Bandwidth test.