---
checksum_sha256: 87218670bc5bf550cbb98692df21e6186439eda74d789bc61140170f770cbd59
contract: architecture.security
customer: Tele-MANAS
generated_at: '2026-09-30T14:55:51.438345+00:00'
generated_by: architecture-engine
opportunity: OPP-number2
project_id: number2
provenance:
  source_documents:
  - DOC-B585FB4B498A — RFP IIITB/EHRC/2022/IT-01, 25-Oct-2022 (and annexures), as
    retrieved
  - Presales Handover sections 1–14
  - Product Readiness (empty sections)
  - Product Catalog (empty)
stage: architecture
status: draft
version: 1
---

# Security Architecture — Tele-MANAS (OPP-number2)

## 1. Threat Model (STRIDE summary)

| Threat                          | Asset                          | Likelihood | Mitigation |
|---------------------------------|--------------------------------|-------------|------------|
| Spoofing identity               | Citizen/staff identity         | Medium      | ABHA SSO, mTLS, MFA for staff (COMP-009) |
| Tampering of clinical records   | EHR (COMP-005)                 | Medium      | Signed FHIR bundles, append-only audit (COMP-009 + COMP-013) |
| Repudiation of actions          | Audit logs                     | Low/Medium  | Immutable WORM audit, time-stamping (COMP-009) |
| Information disclosure          | PHI, voice recordings          | High        | Encryption, DLP, residency (COMP-013) |
| Denial of service               | Tele-MANAS, IVR                | Medium      | WAF, rate-limiting, DR (COMP-002, COMP-015) |
| Elevation of privilege          | Staff roles                    | Medium      | RBAC + ABAC, JIT access, just-enough privilege |
| Supply-chain compromise         | Third-party (commercial IVR, E-Sanjeevani, ABDM) | Medium | Conformance testing, sandbox, SBOM, vendor risk reviews |
| Insider misuse                  | Multi-stakeholder access       | Medium      | Joint architecture board, segregation of duties (R-001, R-005) |
| Data residency violation        | Health data                    | Medium      | DC pinning, geo-fencing (DEC-006) |
| Voice/IVR recording tampering   | CTI stream                     | Low/Medium  | Signed recordings, replay protection |

## 2. Controls Mapped to Requirements

| REQ    | Controls |
|--------|----------|
| REQ-001 | TLS for IVR signalling, recording encryption, PCI-style isolation for caller-info store |
| REQ-002 | E-Sanjeevani integration via signed OAuth2, mutual TLS |
| REQ-003 | Per-state tenant isolation, encryption keys per state |
| REQ-004 | FHIR R4 EHR, field-level encryption for PII/PHI, ABHA linking |
| REQ-005 | Dashboard RBAC, no-PII drill-down by default |
| REQ-006 | LMS isolated tenant, content signing |
| REQ-007 | ABDM HIE-CM, HRP, UHI conformance, consent management |
| REQ-008 | Signed releases, SLSA provenance, deployment RBAC |
| REQ-009 | NOC zero-trust, MFA for ops consoles |
| REQ-010 | Audit retention aligned with governance record requirements |
| REQ-011 | ISO 27001 ISMS, ABDM HIE-CM, MeitY cyber, DISHA, HIPAA-equivalent controls |
| REQ-012 | App attestation, OWASP MASVS |
| REQ-013 | API gateway throttling, signed event payloads, schema validation |

## 3. Identity & Access
- Citizens: ABHA-linked identity via ABDM (COMP-004); optional alias ID for privacy.
- Staff (IIITB, NIMHANS, vendor): IIITB IdP with MFA, federated to ABDM where required.
- Counsellors: ABHA-linked practitioner ID (HPR) for clinical actions.
- Vendors/subcontractors: scoped, time-bound access; no PHI access unless justified.
- Service-to-service: workload identity (mTLS + short-lived tokens).

## 4. Data Protection
- At-rest: AES-256 with HSM-backed KMS (COMP-013).
- In-transit: TLS 1.3, mTLS for internal east-west.
- In-use: confidential compute for analytics on PHI.
- Tokenisation of identifiers (Aadhaar/phone) at the edge.
- Data residency enforced by DC pinning (DEC-006); no PHI to non-Govt cloud regions.
- DLP on egress channels.
- Retention: 7 years for clinical records per Indian healthcare guidance; voice recordings 6 months (configurable).

## 5. Network
- Segmented zones: Citizen DMZ, App tier, Data tier, ABDM zone, Ops zone.
- WAF + API Gateway (COMP-008) with schema validation and OWASP rules.
- Egress proxy with allow-list to ABDM, E-Sanjeevani, IIITB IdP, MeghRaj.
- Private connectivity ( peering / leased line) to ABDM and IIITB DC.
- No direct internet to data tier.

## 6. Logging, Monitoring, Audit
- Centralised SIEM with retention ≥ 1 year hot, 7 years cold.
- Immutable audit trail for clinical record access and consent actions.
- Application logs (COMP-010) feed SLA dashboards.
- Security telemetry → 24x7 SOC (vendor + IIITB shared model).
- Quarterly red-team and annual third-party VA.

## 7. Compliance
- ISO 27001 ISMS aligned (Annexure 4 undertaking).
- ABDM HIE-CM, HRP, UHI conformance.
- MeitY cyber security guidelines.
- DISHA (Digital Information Security in Healthcare Act) readiness.
- CERT-In incident reporting within 6 hours.
- DPDP Act 2023 compliance for personal data.

## 8. Open Security Questions
- Q-003 (mandatory certifications).
- Q-009 (commercial IVR vendor security posture).
- DEC-003 (compliance scope final).
- DEC-010 (ABHA rollout timeline and fallback identity mechanism for citizens without ABHA).