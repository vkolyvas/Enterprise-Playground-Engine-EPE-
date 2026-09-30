---
checksum_sha256: 4962f7369de80278292e7b44245076a8b9e854084eb66f826c3f7ae1c1026af2
contract: architecture.hld
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:02:42.865259+00:00'
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

# High-Level Design (HLD) — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore
**Source(s):** [DOC-B585FB4B498A]

---

## 1. Drivers

| Driver | Source | Implication |
|--------|--------|-------------|
| D-01: Layered application delivery across UI, functional, back-end with per-layer documentation. | REQ-001, REQ-002 | Mandatory layered architecture; each layer must have independent deliverables and documentation discipline. |
| D-02: Continuous platform availability and stability. | REQ-005 | Architecture must support HA, observability, and incident response. |
| D-03: Shift-based Level 1/Level 2 teleconsultation support. | REQ-006 | Operational staffing model and runbook set. |
| D-04: Migration, enhancement and upgrade services. | REQ-004 | Architecture must be modular and refactor-friendly. |
| D-05: Integration testing collaboration across teams including Level 3. | REQ-003, REQ-008 | Independent testable integration layer and contract testing. |
| D-06: ISO 27001 / Annexure 04 security and confidentiality for health/patient data. | REQ-011, REQ-012 | Security-by-design across identity, data, network, audit. |
| D-07: Bangalore-anchored onsite/near-site delivery. | REQ-013 | Operational staffing concentrated in Bangalore. |
| D-08: ICT-driven accessibility for under-served/marginal populations. | REQ-019 | Accessibility engineering, multilingual UI, low-bandwidth resilience. |
| D-09: Multi-year contract with yearly renewals and quantity flexibility. | REQ-010, REQ-016 | Composable commercial line items; cost model must support unit-rate scaling. |

---

## 2. Architecture Options Considered

### Option A1: Layered Monolith + Module-Based Modularisation (Recommended)

- **Description:** A single deployable, internally modularised platform with strict layer boundaries (UI → functional services → back-end data access). Modularity enables parallel teams (UI, functional, back-end) and is appropriate where TMC/GRS/CTI/EHR interfaces are not yet finalised. Designed to evolve toward microservices when integration boundaries firm up.
- **Pros:**
  - Faster initial delivery and lower operational overhead.
  - Aligns with RFP scope (single IIITB-owned platform, Level 3 ownership outside our scope).
  - Easier to maintain in a Bangalore-anchored team with shift-based L1/L2.
  - Lower cost of compliance (single audit scope for ISO 27001).
  - Migration/upgrade path is internal.
- **Cons:**
  - Slower scale-out at extreme load (mitigated by HA pattern and DB read replicas).
  - Refactoring needed before microservice extraction if scope grows.
- **Fit to drivers:** Strong on D-01, D-02, D-03, D-04, D-06, D-07.

### Option A2: Greenfield Microservices with Service Mesh

- **Description:** Decompose Tele-MANAS into independently deployable microservices (UI, IVR adapter, EHR adapter, TMC gateway, GRS, notifications, etc.) fronted by an API gateway and service mesh (mTLS, retries, circuit breakers).
- **Pros:**
  - Independent deployment and scaling per integration (TMC, GRS, CTI/IVR, EHR).
  - Native resilience (circuit breakers, retries) for teleconsultation traffic.
  - Supports large parallel teams.
- **Cons:**
  - Higher cost (more infrastructure, observability tooling, platform engineering).
  - Higher operational complexity for a 3-year IT services scope with shift-based L1/L2 in Bangalore.
  - Distributed-tracing and observability become mandatory, raising the security/audit footprint.
  - Over-engineered if integration scope (Q-003) is narrower than presumed.
- **Fit to drivers:** Strong on D-04, D-05, D-08; weaker on D-07 (operations complexity) and D-09 (cost).

### Selected Option: **A1 — Layered Monolith with Internal Modularisation (with an Integration Adapter Plane)**

A1 is selected because:
1. The RFP scope is a **single IIITB-owned platform** with implied integration points whose interfaces are not yet confirmed (F-02). A monolith reduces integration risk during the discovery phase.
2. The Bangalore-anchored, shift-based L1/L2 model (REQ-006, REQ-013) favours a single operational footprint over a distributed microservices estate.
3. The cost envelope (see cost.md) favours A1's lower infrastructure and operational complexity.
4. The architecture must be **modular enough** to permit future microservice extraction for high-load components (e.g., CTI/IVR adapters, EHR gateway) without re-architecting — captured in DEC-001 and DEC-004.

---

## 3. Logical Components

| ID | Component | Purpose | Mapped REQs |
|----|-----------|---------|----------------|
| COMP-001 | Application Platform | Layered (UI / functional / back-end) Tele-MANAS application with accessibility features. | REQ-001, REQ-019 |
| COMP-002 | Platform Operations & L1/L2 Support | Shift-based Level 1/Level 2 support; teleconsultation operations; incident triage. | REQ-005, REQ-006 |
| COMP-003 | Integration & Test Harness | Integration testing support; contract testing; cross-team coordination with Level 3. | REQ-003, REQ-008 |
| COMP-004 | Documentation & Knowledge Repository | Layer-specific documentation; SOPs; runbooks; release notes; known issues register. | REQ-002, REQ-007 |
| COMP-005 | Migration & Upgrade Pipeline | Migration, enhancement, and upgrade planning; data migration tools; staged rollout. | REQ-004 |
| COMP-006 | Release & Deployment Management | Release notes; deployment scripts (co-authored with Level 3); automated deployments; post-release monitoring. | REQ-007, REQ-008 |
| COMP-007 | Application Maintenance & Quality Engineering | Best-practice maintenance; defect management; preventive maintenance; code-quality gates. | REQ-009 |
| COMP-008 | Commercial & Contract Operations | Commercial artefacts; line-item pricing; renewals; quantity alterations; pass-through governance; "No Claim" certificate handling. | REQ-010, REQ-016, REQ-017, REQ-021 |
| COMP-009 | Security & Compliance Framework | ISO 27001 (or equivalent undertaking); Annexure 04; control mapping; audit support. | REQ-011 |
| COMP-010 | Confidentiality & Data Governance | Confidentiality controls for IIITB/Government/NIMHANS information including health/patient records. | REQ-012 |
| COMP-011 | Bangalore Delivery Operations | Onsite/near-site delivery operating model from Bangalore; Self-Declaration. | REQ-013 |
| COMP-012 | Bid Submission & Governance | Two-stage offline bid; Envelope I (Technical + masked Annexure 9); Envelope II (Commercial); Annexure 6 No Deviation; tender fee/EMD. | REQ-014, REQ-015, REQ-020, REQ-022 |
| COMP-013 | Governance & Steering Committee Liaison | Steering Committee participation; PMO interface; records management. | REQ-018 |
| COMP-014 | Accessibility & Inclusion Engineering | Affordability/accessibility/availability for under-served populations; multilingual UI; low-bandwidth resilience. | REQ-019 |

---

## 4. Data Flows (Logical)

1. **End User → COMP-001 (UI):** Teleconsultation session initiated from under-served/marginal population via web/mobile UI. Accessibility layer (COMP-014) mediates IVR/voice fallback.
2. **COMP-001 (UI) → COMP-001 (Functional):** Functional services receive UI requests; orchestrate business logic.
3. **COMP-001 (Functional) → COMP-001 (Back-end):** Back-end tier accesses patient/health records and platform data.
4. **COMP-001 (Functional) → COMP-003 (Integration Plane):** Outbound integrations to TMC, GRS, CTI/IVR, EHR (interfaces pending confirmation per F-02).
6. **COMP-003 ↔ Level 3 Team:** Contract-tested APIs; deployment-script co-authoring; release notes (REQ-007).
8. **COMP-002 (L1/L2) ↔ COMP-001 + COMP-006:** Ticket intake, runbook execution, post-release monitoring.
9. **COMP-005 → COMP-001:** Migration scripts and upgrade payloads staged and rolled out.
10. **COMP-009/COMP-010 (Security/Confidentiality) → all components:** Policy enforcement, audit logging, access reviews.
11. **COMP-013 (Steering Committee) → IIITB/PMO:** Status, risks, resource asks, decisions.

---

## 5. NFR Mapping

| NFR | Target (TBC) | Component(s) | Decision Reference |
|-----|--------------|---------------|---------------------|
| Availability | 99.9% (pending IIITB confirmation — F-01) | COMP-001, COMP-002, COMP-006 | DEC-002 |
| Response time (P95) | ≤ 2 s for interactive UI (pending confirmation — F-01) | COMP-001, COMP-003 | DEC-002 |
| RTO / RPO | To be confirmed by IIITB (F-01) | COMP-005, COMP-006 | DEC-002, DEC-004 |
| Confidentiality | Health/patient records encrypted at rest (AES-256) and in transit (TLS 1.2+); key management | COMP-010, COMP-009 | DEC-006 |
| Auditability | Centralised immutable audit log of all PHI access; 7-year retention (alignment to project/Indian healthcare norms — confirm) | COMP-009, COMP-010 | DEC-006 |
| Maintainability | Layered separation; documented APIs; code-quality gates | COMP-001, COMP-007 | DEC-001, DEC-007 |
| Scalability | Horizontal scale of UI and functional tiers; DB read replicas | COMP-001, COMP-005 | DEC-002 |
| Accessibility | WCAG 2.1 AA target; multilingual; low-bandwidth fallback | COMP-014 | DEC-001 |
| Testability | Automated unit/integration/contract tests; CI/CD gates | COMP-003, COMP-006, COMP-007 | DEC-003, DEC-007 |
| Operability | Shift-based L1/L2; runbooks; observability stack | COMP-002, COMP-006 | DEC-005 |

---

## 6. Architecture Decision References

| DEC ID | Decision | Satisfies REQ(s) |
|--------|----------|-------------------|
| DEC-001 | Adopt a layered architecture (UI / functional / back-end) with an Integration Adapter Plane; modular monolith today, microservice-ready boundaries for future extraction. | REQ-001, REQ-002, REQ-019 |
| DEC-002 | Design for HA, observability, and quantified availability (pending F-01); include DR posture. | REQ-005, REQ-006 |
| DEC-003 | Establish an Integration & Test Harness with contract testing, dedicated integration test team coordination, and a cross-team coordination cadence (with Level 3). | REQ-003, REQ-008 |
| DEC-004 | Build a Migration & Upgrade Pipeline with versioned artefacts, staged rollout, and rollback plans; cadence aligned to IIITB release windows. | REQ-004, REQ-007 |
| DEC-005 | Operate a Bangalore-anchored onsite/near-site delivery model with shift-based L1/L2 coverage; runbooks and SOPs owned by COMP-002. | REQ-006, REQ-013 |
| DEC-006 | Implement an ISO 27001-aligned (or Annexure 04-equivalent) Security & Compliance Framework with confidentiality controls for health/patient records. | REQ-011, REQ-012 |
| DEC-007 | Implement release & deployment management with deployment scripts co-authored with Level 3, automated CI/CD gates, release notes, known-issues register, and post-release monitoring. | REQ-007, REQ-008 |
| DEC-008 | Adopt a unit-rate-driven commercial model with line-item pricing that supports unlimited quantity alterations and pass-through of market price reductions per F-013. | REQ-010, REQ-016, REQ-017 |
| DEC-009 | Steer governance through a Steering Committee Liaison (COMP-013) and PMO-aligned reporting cadence. | REQ-018 |
| DEC-010 | Embed Accessibility & Inclusion Engineering (WCAG 2.1 AA, multilingual, low-bandwidth) into the application lifecycle. | REQ-019 |