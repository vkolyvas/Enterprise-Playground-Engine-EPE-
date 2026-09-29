# EPE — Output Contracts

The four stage engines produce Markdown artifacts with YAML frontmatter. Each
artifact is a contract: it declares its inputs, its outputs, and the schema
the validation engine enforces.

This document is the canonical reference for those schemas.

---

## 1. Product

### 1.1 `product/definition.md`

```yaml
---
contract: product.definition
version: 1
stage: product
status: draft                  # draft | validated | approved
generated_at: 2026-09-29T10:00:00Z
generated_by: product-engine
provenance:
  source_documents: [DOC-00012, DOC-00013]
---
```

Required sections:
- Product name and one-line description
- Problem statement
- Target users and personas
- Use cases (must/should/could)
- Out-of-scope (explicit non-goals)
- Differentiators
- Evidence references (with document IDs)

### 1.2 `product/catalog.md`

```yaml
---
contract: product.catalog
version: 1
---
```

Required: a Markdown table or list of capabilities with columns:

| ID    | Capability | Classification | Depends on | Notes |
|-------|------------|----------------|------------|-------|

`classification` ∈ `standard | configurable | custom | unsupported`.

### 1.3 `product/guardrails.md`

```yaml
---
contract: product.guardrails
version: 1
---
```

Required sections:
- Technical limits (capacity, latency, throughput)
- Compliance posture (e.g. SOC2, ISO27001, GDPR)
- Data residency
- Commercial constraints (pricing model, minimums)
- Things we will NOT do (hard refusals)

### 1.4 `product/readiness.md`  ← Product → Presales contract

```yaml
---
contract: product.readiness
version: 1
stage: product
status: approved              # gate product.readiness_approved
approved_by: <human>
approved_at: 2026-09-29T10:00:00Z
---

# Product Readiness

## What is the product?
## Who is it for?
## What problems does it solve?
## What does it contain?
## What does it NOT contain?
## What can Presales sell?
## What requires Architecture?
## What are the technical limits?
## What are the commercial constraints?
## What evidence exists?
## What is configurable?
## What is custom?

## Handover
- This artifact is the contract consumed by `presales`.
- See `docs/OUTPUT_CONTRACTS.md §2`.
```

---

## 2. Presales

### 2.1 `presales/discovery.md`

```yaml
---
contract: presales.discovery
version: 1
opportunity: OPP-00124
customer: <name>
stage: presales
status: draft
---
```

Required sections: stakeholders, business objectives, current state, drivers,
timeline, success criteria.

### 2.2 `presales/qualification.md`

```yaml
---
contract: presales.qualification
version: 1
---
```

Required: BANT/MEDDIC fields mapped to structured YAML; verdict (`qualified |
deferred | disqualified`) and rationale.

### 2.3 `presales/scope.md`

```yaml
---
contract: presales.scope
version: 1
---
```

Required: in-scope, out-of-scope, assumptions, dependencies, product
capabilities used (with `CAP-NNN`), product gaps, custom requirements,
integrations, security, SLA, commercial constraints.

### 2.4 `presales/sow.md`

```yaml
---
contract: presales.sow
version: 1
---
```

Standard SOW structure: parties, scope reference, deliverables, timeline,
acceptance, pricing summary, assumptions, signatures.

### 2.5 `presales/handover.md`  ← Presales → Architecture contract

```yaml
---
contract: presales.handover
version: 1
opportunity: OPP-00124
customer: <name>
stage: presales
status: approved              # gate presales.handover
approved_by: <human>
approved_at: 2026-09-29T10:00:00Z
---

# Presales → Architecture Handover

## Opportunity
## Customer
## Business Objective
## Confirmed Requirements (REQ-NNN list)
## Technical Requirements
## Non-Functional Requirements
## Assumptions
## Constraints
## Product Capabilities Used (CAP-NNN list)
## Product Gaps
## Custom Requirements
## Integrations
## Security Requirements
## SLA Requirements
## Commercial Constraints
## Open Questions (Q-NNN list)
## Architecture Decisions Required (DEC-NNN list)
## Acceptance Criteria (TEST-NNN list, may be empty)

## Handover
- This artifact is the contract consumed by `architecture`.
- See `docs/OUTPUT_CONTRACTS.md §3`.
```

---

## 3. Architecture

### 3.1 `architecture/validation.md`

```yaml
---
contract: architecture.validation
version: 1
opportunity: OPP-00124
stage: architecture
status: draft
---
```

Required: per-requirement validation table, contradictions, unsupported
items, security flags, capacity flags, availability flags, dependencies,
cost risks, vendor dependencies, operational gaps.

### 3.2 `architecture/hld.md`

```yaml
---
contract: architecture.hld
version: 1
---
```

Required sections: drivers, constraints, options considered (≥2),
selected option with rationale, logical components, data flows, NFR
mapping, decision references (DEC-NNN).

### 3.3 `architecture/security.md`

```yaml
---
contract: architecture.security
version: 1
---
```

Required: threat model summary, controls mapped to requirements, identity,
data protection, network, logging, audit, compliance.

### 3.4 `architecture/lld.md`

```yaml
---
contract: architecture.lld
version: 1
---
```

Required: per-component detailed design, interfaces, data models,
configurations, failure modes, runbook stubs.

### 3.5 `architecture/cost.md`

```yaml
---
contract: architecture.cost
version: 1
---
```

Required: line items, assumptions, ranges, optimization opportunities.

### 3.6 `architecture/blueprint.md`  ← Architecture → Delivery contract

```yaml
---
contract: architecture.blueprint
version: 1
opportunity: OPP-00124
stage: architecture
status: approved              # gate architecture.blueprint
approved_by: <human>
approved_at: 2026-09-29T10:00:00Z
---

# Implementation Blueprint

## Scope Reference (presales/handover.md)
## Components (with COMP-NNN)
## Implementation Tasks (TASK-NNN)
## Environment Plan
## Configuration Plan
## Test Plan (TEST-NNN)
## Rollout Strategy
## Acceptance Criteria
## Risks and Mitigations
## Dependencies

## Handover
- This artifact is the contract consumed by `delivery`.
- See `docs/OUTPUT_CONTRACTS.md §4`.
```

---

## 4. Delivery

### 4.1 `delivery/plan.md`

```yaml
---
contract: delivery.plan
version: 1
opportunity: OPP-00124
stage: delivery
status: draft
---
```

Required: sequencing, milestones, owners, dependencies, prerequisites.

### 4.2 `delivery/test.md`

```yaml
---
contract: delivery.test
version: 1
---
```

Required: per-test mapping to requirements and architecture components.

### 4.3 `delivery/acceptance.md`

```yaml
---
contract: delivery.acceptance
version: 1
---
```

Required: executed test results, evidence references, sign-off.

### 4.4 `delivery/onboarding.md`

```yaml
---
contract: delivery.onboarding
version: 1
---
```

Required: customer-facing onboarding steps, training plan, support contacts.

### 4.5 `delivery/operations.md`

```yaml
---
contract: delivery.operations
version: 1
---
```

Required: monitoring, alerting, SLO/SLA, runbooks, escalation.

### 4.6 `delivery/handover.md`

```yaml
---
contract: delivery.handover
version: 1
---
```

Required: customer handover of the live service.

### 4.7 `delivery/feedback.md`  ← Delivery → Product (feedback loop)

```yaml
---
contract: delivery.feedback
version: 1
---
```

Required: incidents, cost variance, usage telemetry, deployment problems,
customer feedback, operational lessons. Each item links back to its source
requirement or architecture component.

---

## 5. Common Frontmatter

Every contract includes:

```yaml
contract: <dot.path>
version: <int>
stage: product | presales | architecture | delivery
status: draft | in_review | approved | rejected
generated_at: <ISO8601>
generated_by: <engine-name>
provenance:
  source_documents: [DOC-NNN, ...]
checksum_sha256: <hex>
```

`status: approved` requires a human `approved_by` field with a non-empty
name. Engines cannot self-approve.

## 6. Cross-References

- See `docs/ARCHITECTURE.md` for how contracts flow between stages.
- See `docs/VALIDATION.md` for what each contract must pass.
- See `docs/DATA_MODEL.md` for the entity schemas referenced inside
  contracts (`REQ-NNN`, `DEC-NNN`, `TASK-NNN`, `TEST-NNN`).
