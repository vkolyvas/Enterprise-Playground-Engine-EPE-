---
checksum_sha256: 71339307c4f4a5dfb0ed65b4485e0a9880dad23514546e37964553e6572f5f8f
contract: presales.scope
customer: Tele-MANAS
generated_at: '2026-09-30T14:54:19.302485+00:00'
generated_by: presales-engine
opportunity: OPP-number2
project_id: number2
provenance:
  source_documents:
  - 'DOC-B585FB4B498A — RFP: Software Development and Platform Support Services for
    National Tele-Mental Health Initiative, IIITB/EHRC/2022/IT-01, 25-Oct-2022 (Tele-MANAS)'
stage: presales
status: draft
version: 1
---

# Scope — Tele-MANAS (OPP-number2)

> Note on capabilities: the Product Catalog provided in the contract is empty (no CAP-NNN rows). All capabilities below reference the catalog by capability ID where a CAP exists; otherwise they are tracked as Custom (CUS-NNN) and flagged for Architecture.

## In-Scope

### REQ-001 — Voice/IVR Teleconsultation Platform Support
- Train IVR Users across States/UTs. [DOC-B585FB4B498A]
- Provide Level 1 Support for IVR Users across States/UTs. [DOC-B585FB4B498A]
- Develop Tele-MANAS components to store caller information and manage counsellor / mental-health-professional workflows. [DOC-B585FB4B498A]
- Upgrade the IVR UI for counsellors and mental-health professionals. [DOC-B585FB4B498A]
- *Capability link:* Voice/IVR Teleconsultation (no CAP row in catalog — see Gap).

### REQ-002 — Video Consultation via E-Sanjeevani
- E-Sanjeevani is recommended as the video platform; vendor shall integrate and support it within Tele-MANAS. [DOC-B585FB4B498A]
- *Capability link:* E-Sanjeevani Integration (no CAP row in catalog — see Gap).

### REQ-003 — National Tele-MANAS Platform Build
- Build unified National Tele-MANAS platform used by central agency (NIMHANS) and state/UT facilities. [DOC-B585FB4B498A]
- *Capability link:* Tele-MANAS Core (no CAP row in catalog).

### REQ-004 — National E-Manas Platform
- Leverage Karnataka E-Manas to build a National E-Manas with EHR recording of teleconsultations. [DOC-B585FB4B498A]
- Integrate with Ayushman Bharat Digital Mission (ABDM). [DOC-B585FB4B498A]
- *Capability link:* E-Manas / EHR (no CAP row in catalog).

### REQ-005 — Governance and Dashboards
- Governance and dashboard modules for monitoring, tracking and reporting of the Tele-MANAS programme. [DOC-B585FB4B498A]
- *Capability link:* Governance & Analytics (no CAP row in catalog).

### REQ-006 — Training Module Plug-ins
- Plug-ins for facilitating access to training modules for tele-consultants across facilities. [DOC-B585FB4B498A]
- *Capability link:* Training Enablement (no CAP row in catalog).

### REQ-007 — ABDM Integration
- Integrate Tele-MANAS components with the ABDM framework. [DOC-B585FB4B498A]
- *Capability link:* ABDM Integration (no CAP row in catalog).

### REQ-008 — Platform Enhancements, Maintenance & Support
- Development/implementation of new solution components, project coordination tracking and reporting, platform enhancements, maintenance and support. [DOC-B585FB4B498A]
- Documenting release notes and known issues; monitoring platform performance post-release; reporting on roll-out issues; producing deployment scripts with L3 team. [DOC-B585FB4B498A]
- *Capability link:* Managed Services / DevOps Support (no CAP row in catalog).

### REQ-009 — Shift-based L1/L2 Technical Support
- Tech Support Engineers on shift rotation to ensure smooth teleconsultation operations (L1 and L2). [DOC-B585FB4B498A]
- *Capability link:* L1/L2 Support (no CAP row in catalog).

### REQ-010 — Steering Committee & Programme Governance Participation
- Project progress, risk, resourcing, next steps reporting to Steering Committee; maintain records; participate in-person when required. [DOC-B585FB4B498A]
- *Capability link:* Programme Governance (no CAP row in catalog).

### REQ-011 — Compliance, Security & Scalability
- Components must be scalable, support relevant security certifications, and comply with relevant healthcare standards and guidelines. [DOC-B585FB4B498A]
- *Capability link:* Security/Compliance baseline (no CAP row in catalog).

## Out-of-Scope (per evidence)
- The RFP lists scope explicitly in Section 2; anything not enumerated (e.g., physical devices, drug procurement, clinical content authoring beyond training plug-ins) is not in retrieved evidence — assume out-of-scope unless added via amendment.
- Underlying E-Sanjeevani platform product itself is not being built by the vendor — only integrated with. [DOC-B585FB4B498A]
- ABDM core framework is not being built by the vendor — only integrated with. [DOC-B585FB4B498A]

## Assumptions
- A1. IIITB will provide the planned architecture, technology standards and code-collaboration model; vendor executes under that leadership. [DOC-B585FB4B498A]
- A2. NIMHANS retains clinical-content ownership; vendor does not author clinical protocols.
- A3. Existing commercial IVR platform (launched 10-Oct-22) continues to be the runtime substrate; vendor integrates with it. [DOC-B585FB4B498A]
- A4. State/UT rollout sequencing is decided by IIITB based on priorities; vendor scales staff accordingly. [DOC-B585FB4B498A]
- A5. Karnataka E-Manas IP/architecture is accessible to the vendor. [DOC-B585FB4B498A]

## Dependencies
- D1. IIITB planned architecture and tech-stack decisions. [DOC-B585FB4B498A]
- D2. NIMHANS clinical workflow specifications. [DOC-B585FB4B498A]
- D3. ABDM framework availability and conformance specifications. [DOC-B585FB4B498A]
- D4. E-Sanjeevani platform APIs and SLAs.
- D5. State/UT readiness (telephone lines, counsellor availability). [DOC-B585FB4B498A]
- D6. L3 vendor / deployment team for deployment scripts. [DOC-B585FB4B498A]

## Product Capabilities Used
- The Product Catalog provided is empty in the contract input; no CAP-NNN exist. All in-scope REQs above are therefore marked as **Custom (to be designed/developed by the vendor under IIITB supervision)** unless and until CAP mappings are provided.
- **Action for Product team:** populate CAP rows for: Voice/IVR, E-Sanjeevani Integration, Tele-MANAS Core, E-Manas/EHR, Governance & Dashboards, Training Plug-ins, ABDM Integration, Managed Services, L1/L2 Support.

## Product Gaps (vs Product Readiness)
- Product Readiness contract is a template with no populated sections. We cannot confirm product/architecture boundaries yet. **Gap — flagged for Architecture (DEC-001).**

## Custom Requirements
- CUS-001. UI upgrade of the IVR for counsellors and MHPs. [DOC-B585FB4B498A]
- CUS-002. National E-Manas uplift from Karnataka base + ABDM conformance. [DOC-B585FB4B498A]
- CUS-003. Governance and dashboard modules (programme-wide). [DOC-B585FB4B498A]
- CUS-004. Training plug-ins for tele-consultants. [DOC-B585FB4B498A]
- CUS-005. Shift-roster-based L1/L2 technical support staffing. [DOC-B585FB4B498A]
- CUS-006. Deployment scripting collaboration with L3. [DOC-B585FB4B498A]

## Integrations
- ABDM (Ayushman Bharat Digital Mission). [DOC-B585FB4B498A]
- E-Sanjeevani video platform. [DOC-B585FB4B498A]
- Commercial IVR platform (existing, launched 10-Oct-2022). [DOC-B585FB4B498A]
- Karnataka E-Manas (as base for National E-Manas). [DOC-B585FB4B498A]
- Computer Telephony Integration (CTI) — referenced in glossary. [DOC-B585FB4B498A]
- Mobile app / website channels (per RFP functional matrix). [DOC-B585FB4B498A]

## Security
- Confidentiality of all materials marked "Confidential" by IIITB / Govt / NIMHANS. [DOC-B585FB4B498A]
- Compliance with healthcare standards and security certifications (specifics to be confirmed by Architecture). [DOC-B585FB4B498A]
- Access-control and data-handling aligned with ABDM. [DOC-B585FB4B498A]

## SLA
- Service is shift-based; L1 and L2 support delivered via Tech Support Engineers on rotation. [DOC-B585FB4B498A]
- Specific availability, response and resolution targets are **not stated** in retrieved evidence — flagged as Gap (DEC-002).
- Liquidated damages and performance security apply for unexcused delay. [DOC-B585FB4B498A]

## Commercial Constraints
- Contract type: IT Services. [DOC-B585FB4B498A]
- Term: 7 years + 2-year optional renewal at mutually agreed price. [DOC-B585FB4B498A]
- EMD and tender processing fees (DD/NEFT to IIITB). [DOC-B585FB4B498A]
- Performance security, liquidated damages, "No Claim" certificate on completion. [DOC-B585FB4B498A]
- IIITB reserves right to accept/reject any/all bids; to amend the contract. [DOC-B585FB4B498A]
- Notification of award + written acceptance constitutes binding contract. [DOC-B585FB4B498A]
- Grievance process (Stage-I, Stage-II, Director appeal) with strict 3-day escalation windows. [DOC-B585FB4B498A]