---
checksum_sha256: 6c3ee321e87ab374b028fd4025536a752c868878d962e245246b0f6bb97c3229
contract: delivery.onboarding
customer: E-Health Research Centre, IIIT Bangalore
generated_at: '2026-09-30T08:06:42.108633+00:00'
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

# Customer Onboarding — Tele-MANAS IT Services

**Welcome to the Tele-MANAS Platform Support engagement.**
This guide is for IIIT Bangalore (E-Health Research Centre) stakeholders, MOHFW/NIMHANS observers, partner agencies, and end-user groups. It explains how to engage with the delivery team, how to access support, and how training is delivered.

---

## 1. Key Contacts

| Role | Name / Team | Contact | Hours |
|------|-------------|---------|-------|
| Delivery Manager | [TBA] | email / phone | Business hours + on-call |
| Solution Lead / Architect | [TBA] | email | Business hours |
| Tech Lead | [TBA] | email | Business hours |
| Security Lead | [TBA] | email / IR hotline | 24×7 for IR |
| Test Lead | [TBA] | email | Business hours |
| QA Lead | [TBA] | email | Business hours |
| Commercial Lead | [TBA] | email | Business hours |
| L1/L2 Service Desk | Service Desk | phone / ITSM portal | Per shift rota (F-09) |
| IIITB PMO | [TBA] | email | Business hours |
| Steering Committee Secretariat | Delivery Manager | email | Per cadence |

**Out-of-hours IR:** pager through Security Lead; IIITB escalation matrix per COMP-002 runbook.

---

## 2. Onboarding Steps for New Customer Users

1. **Nominate** a primary and backup focal at IIITB per workstream (platform, security, commercial, integration).
2. **Sign** NDA and confidentiality undertaking (TASK-108) before access is granted.
3. **Provision** access: IIITB IdP federation (D-14); role assignment per need-to-know (COMP-010).
4. **Tour**: walk-through of documentation portal, ITSM, status dashboards.
5. **Confirm** preferred communication channels and meeting cadence.
6. **Pilot access**: read-only access to non-prod for stakeholder review.
7. **Activate** UAT credentials for IIITB/MOHFW/NIMHANS users (TEST-010).
8. **Subscribe** to release notes, known-issues register, and incident advisories.

---

## 3. Training Plan

| Audience | Module | Format | Duration | Frequency |
|----------|--------|--------|----------|-----------|
| IIITB PMO + Steering Committee | Engagement overview, governance, status reporting | Briefing | 1 hr | Kick-off + annually |
| IIITB/MOHFW/NIMHANS UAT users | UAT process, defect logging, release acceptance | Workshop + sandbox | 2 hrs | Per release train |
| Integration partners (TMC, GRS, CTI/IVR, EHR owners) | Contract testing, deployment-script co-authoring | Workshop | 2 hrs | On integration kick-off + change |
| L1/L2 Service Desk (IIITB side, if any) | ITSM tool, severity matrix, escalation | Hands-on | 3 hrs | On joining + yearly refresher |
| Accessibility reviewers | WCAG 2.1 AA, multilingual framework, assistive-tech testing | Workshop | 2 hrs | Per release audit cycle |
| End-user community (clinicians, callers) | Channel usage, IVR fallback, multilingual UI | Recorded video + FAQ | As needed | On new feature |

---

## 4. How to Get Help

| Channel | When to use | SLA target (post F-01 confirmation) |
|---------|-------------|--------------------------------------|
| ITSM portal | All non-urgent issues | Per severity matrix |
| Phone (Service Desk) | Urgent operational issues | Per severity matrix |
| Email (Delivery Manager) | Commercial / governance | Business-day response |
| Security IR hotline | Suspected breach / confidentiality event | Immediate (24×7) |
| Steering Committee | Risks, decisions, escalations | Per cadence |

---

## 5. Release & Change Communication

- **Release notes** published ≥ X business days before go-live (per REQ-007 / AC-06).
- **Known issues** register updated weekly.
- **Change advisory** for canary deployments to IIITB PMO.
- **Post-release monitoring report** shared within 48 hours of full promotion.

---

## 6. Audit & Compliance Cadence (per F-11, AC-09)

- Quarterly internal audits (TASK-204).
- Annual external audit / pen-test (TEST-007).
- Customer-initiated inspection rights per RFP clause (records + sites subject to Regulator/IIITB inspection).

---

## 7. Accessibility & Inclusion (AC-16)

- WCAG 2.1 AA conformance (TEST-008).
- Multilingual UI (English + scheduled Indian languages per IIITB direction).
- IVR fallback for low-bandwidth / non-smartphone users.
- Assistive-tech support; feedback channel for end-users.

---

## 8. What We Ask From You (Customer)

- Confirm interface owners for TMC, GRS, CTI/IVR, EHR (F-02).
- Confirm SLA targets (F-01) and shift pattern (F-09).
- Provide IIITB IdP federation (D-14) and cloud/infra tenancy decision (D-12).
- Provide audit cadence (F-11) and Steering Committee cadence (F-07).
- Nominate UAT participants and integration testers.