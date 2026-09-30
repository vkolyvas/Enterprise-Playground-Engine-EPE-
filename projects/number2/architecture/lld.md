---
checksum_sha256: 16b41c29bb71672959db6c7cf4eb745d21d7e3d23ce396459c52e9ca60864376
contract: architecture.lld
customer: Tele-MANAS
generated_at: '2026-09-30T14:55:51.439030+00:00'
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

# Low-Level Design — Component Detail

> Architecture-stage placeholder; details to be elaborated once DEC-001, DEC-002, DEC-003, DEC-005, DEC-007, DEC-008 are resolved.

## COMP-001 Citizen Channel (Mobile + Web + IVR)
- Interfaces: REST/GraphQL to COMP-002, SIP/SDP to COMP-015 (CTI).
- Configs: per-state tenant, language packs, accessibility.
- Failure modes: IVR outage → fall back to alternate commercial IVR; mobile/web outage → interactive voice fallback.
- Runbook: R-001 — IVR failover; R-002 — channel health checks.

## COMP-002 Tele-MANAS Core Services
- Stateless microservices, containerised; autoscaling group.
- Session orchestration, MHP workflow engine.
- Failure modes: regional outage → multi-AZ active-active.
- Runbook: R-003 — session failover, queue drain.

## COMP-003 E-Sanjeevani Adapter
- OAuth2 client credentials; mTLS.
- Failure modes: partner outage → queue and retry; degradation to audio-only consult.
- Runbook: R-004 — partner outage, retry-with-backoff.

## COMP-004 ABDM Gateway
- Modules: ABHA, HIE-CM, HRP, UHI (pending Q-005 confirmation).
- Consent Artefact handling; data-pull/data-push.
- Failure modes: gateway throttle → back-pressure; consent denial → fallback to manual.
- Runbook: R-005 — consent failure, audit evidence.

## COMP-005 E-Manas EHR
- FHIR R4 store; HSM-encrypted PHI.
- Backup: continuous + nightly; cross-region replication.
- Failure modes: DB outage → read-replica promotion.
- Runbook: R-006 — restore drill, RTO/RPO validation.

## COMP-006 Governance & Dashboard Module
- Aggregates from COMP-002, COMP-005, COMP-010.
- RBAC-scoped views per Steering Committee / PMO / state cell.
- Failure modes: stale data tolerated, dashboards read-mostly.
- Runbook: R-007 — KPI integrity checks.

## COMP-007 Training Module
- SCORM/xAPI compliant LMS.
- MHP certification tracking.
- Failure modes: LMS down → async content delivery.
- Runbook: R-008 — content staging, version rollback.

## COMP-008 Integration Bus
- API Gateway + event mesh (Kafka-class).
- Schema registry, message replay.
- Failure modes: broker outage → DLQ; partner outage → circuit breaker.
- Runbook: R-009 — replay, DLQ inspection.

## COMP-009 IAM/AAA
- ABHA-federated SSO; IIITB IdP for staff.
- RBAC + ABAC; JIT elevation for break-glass.
- Audit logs to SIEM.
- Failure modes: IdP down → cached tokens for read-only.
- Runbook: R-010 — break-glass procedure.

## COMP-010 Observability & SRE
- Metrics (Prometheus), logs (EFK), traces (OpenTelemetry), APM.
- SLA calculators feed COMP-006.
- Failure modes: telemetry loss → local buffers.
- Runbook: R-011 — restore observability pipeline.

## COMP-011 DevSecOps & Release Engineering
- Git-based source, signed builds, SLSA L3.
- Blue/green deployment, automated rollback.
- Release notes auto-generated.
- Failure modes: bad release → automated rollback via health checks.
- Runbook: R-012 — rollback procedure.

## COMP-012 L1/L2 Support Operations
- Service desk; ticketing integrated with COMP-010 alerts.
- Shift roster (Bengaluru on-site + remote).
- Failure modes: shift gap → on-call rotation.
- Runbook: R-013 — escalation matrix aligned to grievance policy (3-day / 30-day).

## COMP-013 Data Protection & Compliance Plane
- HSM-backed KMS, DLP, key rotation (90 days).
- Field-level encryption for PHI; tokenisation of identifiers.
- Failure modes: KMS outage → fail-closed for writes.
- Runbook: R-014 — key rotation, incident response.

## COMP-014 State/UT Rollout Orchestrator
- Phased rollout workflows; data migration toolkit.
- Training delivery orchestration.
- Failure modes: state-specific failures isolated per tenant.
- Runbook: R-015 — per-state rollback.

## COMP-015 Commercial IVR/CTI Bridge
- SIP/PRI trunking; CTI middleware.
- UI upgrade approach pending DEC-007.
- Failure modes: vendor outage → secondary IVR; recording loss → buffered retries.
- Runbook: R-016 — IVR vendor failover.

## Data Model Highlights (high level)
- Patient: ABHA ID, alias, demographics, consent records.
- Encounter: counsellor/MHP, E-Sanjeevani session ref, FHIR resources.
- Observation/Note: encrypted, signed.
- AuditEvent: actor, action, target, timestamp, consent reference.
- Dashboard fact tables (de-identified).