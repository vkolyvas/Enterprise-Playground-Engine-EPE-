---
checksum_sha256: 04a10ba21808d425c0b903705c9ba6dc4f317b970606703283aed5c7bdea7cea
contract: architecture.security
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:02:42.865588+00:00'
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

# Security Architecture — Tele-MANAS IT Services

**Opportunity:** OPP-TeleMANAS-001
**Customer:** E-Health Research Centre, IIIT Bangalore
**Source(s):** [DOC-B585FB4B498A]

---

## 1. Threat Model Summary (STRIDE)

| Threat | Description | Affected Assets | Mitigation |
|--------|-------------|-----------------|------------|
| **S — Spoofing** | Forged identity of users (patients/callers) or service accounts to gain PHI access. | Authentication surface, API gateway, IVR/CTI | MFA for staff; certificate-based service identity; OTP for patient identity proofing (per IIITB direction). |
| **T — Tampering** | Modification of health records, audit logs, or release artefacts. | PHI store, audit logs, deployment scripts | Append-only audit log; code signing; integrity verification of artefacts. |
| **R — Repudiation** | Denial of actions performed on PHI (e.g., staff viewing records). | Audit logs, user actions | Centralised immutable audit log; non-repudiation via digital signatures on critical actions. |
| **I — Information Disclosure** | PHI leakage to unauthorised parties (insider, external attacker). | PHI store, logs, support screens | Encryption at rest/in transit; strict RBAC + ABAC; DLP; least privilege. |
| **D — Denial of Service** | Disruption of teleconsultation services. | UI, API gateway, CTI/IVR | HA pattern, rate limiting, WAF, capacity headroom. |
| **E — Elevation of Privilege** | Staff or service accounts gaining admin-level access. | Privileged roles, infra control plane | PAM, just-in-time access, segregation of duties, periodic recertification. |

### 1.1 Key Risks

- **Insider risk:** Bangalore-anchored L1/L2 staff with broad platform access; mitigated by RBAC, audit, PAM.
- **Integration risk:** Implied integrations with TMC, GRS, CTI/IVR, EHR (F-02) introduce trust-boundary crossings; mitigated by mTLS, signed payloads, contract testing.
- **Data residency risk:** Cross-border transfer of PHI is not addressed (F-03); default to India-only storage and processing unless IIITB clarifies.
- **Vendor dependency:** Level 3 ownership outside our control (F-08); mitigated by signed deployment scripts and shared release process.

---

## 2. Controls Mapped to Requirements

| Control | Description | Mapped REQ(s) | Component(s) |
|---------|-------------|----------------|--------------|
| C-01: ISO 27001-aligned ISMS | ISMS scoped to Tele-MANAS platform; Statement of Annexure certified. | REQ-011 | COMP-009 |
| C-02: Annexure 04 undertaking | Bidder executes Annexure 04 data and information security undertaking. | REQ-011 | COMP-012, COMP-009 |
| C-03: Confidentiality framework | Confidentiality procedures for IIITB/Government/NIMHANS information including health/patient records. | REQ-012 | COMP-010 |
| C-04: Access control (RBAC + ABAC) | Role- and attribute-based access; least privilege; periodic access reviews. | REQ-011, REQ-012 | COMP-009, COMP-010 |
| C-05: Identity & MFA | MFA for all human access; SSO via IIITB-approved IdP; service accounts via certificates/managed identities. | REQ-011, REQ-012 | COMP-009 |
| C-06: Encryption | AES-256 at rest; TLS 1.2+ in transit; HSM/KMS-managed keys; per-tenant key separation. | REQ-011, REQ-012 | COMP-009, COMP-010 |
| C-07: Logging & monitoring | Centralised, immutable audit log of all PHI access; 24×7 monitoring; alerting on anomalies. | REQ-005, REQ-011, REQ-012 | COMP-002, COMP-009 |
| C-08: Audit support | Evidence pack for IIITB/MOHFW/NIMHANS audits (F-11). | REQ-011 | COMP-009 |
| C-09: Secure SDLC | SAST/DAST/SCA in CI/CD; secrets management; code review; signed releases. | REQ-007, REQ-009, REQ-011 | COMP-006, COMP-007, COMP-009 |
| C-10: Vulnerability management | Regular patching; dependency scanning; penetration testing cadence (aligned to F-11). | REQ-011 | COMP-009 |
| C-11: Backup & DR | Encrypted backups; tested DR (RTO/RPO pending F-01). | REQ-005, REQ-011 | COMP-005, COMP-009 |
| C-12: Network segmentation | DMZ for public-facing UI; private subnets for back-end; jump host for admin; WAF and IDS/IPS. | REQ-011 | COMP-009 |
| C-13: DLP | Data-loss prevention on support endpoints and egress channels. | REQ-012 | COMP-009, COMP-010 |
| C-14: PAM | Privileged access management for admin operations; just-in-time elevation. | REQ-011, REQ-012 | COMP-009 |
| C-15: Incident response | IR runbook; tabletop exercises; coordinated disclosure with IIITB/MOHFW/NIMHANS. | REQ-005, REQ-011 | COMP-002, COMP-009 |
| C-16: Subcontractor controls | Security clauses for any subcontractor; right-to-audit; approved subcontractor list. | REQ-011, REQ-012 | COMP-009, COMP-012 |
| C-17: Bangalore delivery controls | Onsite/near-site controls; visitor management; clean-desk; screen privacy. | REQ-013 | COMP-011 |

---

## 3. Identity

- **Human users:**
  - IIITB/PMO staff: SSO via IIITB IdP; MFA mandatory.
  - Bidder delivery staff: SSO via IIITB-approved IdP or federated identity; MFA; just-in-time access.
  - Patient/caller identity: per IIITB direction (e.g., OTP-based identity proofing for teleconsultation).
- **Service accounts:**
  - Managed identities/certificates; no static secrets; key rotation policy (≤90 days).
  - Distinct identities per environment (dev/test/prod).
- **Privileged access:**
  - PAM with just-in-time elevation; session recording for admin sessions; quarterly recertification.

---

## 4. Data Protection

- **Data classes:**
  - Public (programme information, public-facing content).
  - Internal (operational data, non-PHI).
  - Confidential (PHI, audit logs, credentials).
  - Restricted (master keys, root credentials).
- **At rest:** AES-256; KMS-managed keys; per-tenant separation.
- **In transit:** TLS 1.2+ minimum; mTLS for service-to-service and integration adapters (TMC, GRS, CTI/IVR, EHR).
- **In use:** Tokenisation/masking for support screens; no raw PHI in test environments (production-like data masked or synthetic).
- **Data residency (subject to F-03):** Default to India-only storage and processing; no cross-border transfer without IIITB written approval (consistent with REQ-012 spirit).
- **Retention:** Audit log retention aligned to Indian healthcare norms (≥7 years, confirm with IIITB); PHI retention per IIITB policy.

---

## 5. Network

- **Topology:**
  - Public-facing tier in DMZ (WAF, DDoS protection, rate limiting).
  - Application tier in private subnet.
  - Data tier in isolated subnet with no internet egress.
  - Admin access via hardened jump host with PAM session recording.
- **Segmentation:** Microsegmentation between tiers; security groups per role.
- **Egress:** Allow-listed destinations only; DLP on egress.
- **Remote access:** VPN/MFA for staff; zero-trust posture preferred.

---

## 6. Logging & Audit

- **Centralised SIEM:** All authn/authz events, PHI access, admin actions, deployment events.
- **Audit log integrity:** Append-only, tamper-evident (e.g., hash chain or WORM storage).
- **Retention:** ≥7 years (subject to IIITB direction).
- **Monitoring:** 24×7 alerts on anomalies; SLA-driven escalation to L1/L2 (COMP-002) and IR (COMP-009).
- **Audit cadence (subject to F-11):** Quarterly internal audits; annual external audit; ad-hoc IIITB/MOHFW/NIMHANS audits on request.

---

## 7. Compliance

- **ISO 27001:** Adopt and maintain ISMS scoped to Tele-MANAS; certificate or Annexure 04 equivalent (F-04).
- **Annexure 04 undertaking:** Executed at bid; reaffirmed at award.
- **Confidentiality:** NDA-equivalent obligations for all staff; specific clauses for IIITB/Government/NIMHANS information.
- **Sectoral standards:** Aligned with applicable healthcare standards/guidelines referenced in RFP Section 2.1 (e.g., DISHA, ABDM where applicable; confirm with IIITB).
- **Subcontractor obligations:** Flow-down of security and confidentiality clauses.

---

## 8. Security Decision References

- **DEC-006:** ISO 27001 / Annexure 04 framework (REQ-011, REQ-012).
- **DEC-007:** Secure release pipeline and audit logging (REQ-007, REQ-011).
- **DEC-005:** Bangalore onsite controls (REQ-013).