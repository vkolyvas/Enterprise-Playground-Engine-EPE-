# EPE — Product Requirements Document

## 1. Purpose

EPE (Enterprise Playground Engine) is a document-driven, configuration-driven,
AI-assisted engineering workflow platform that supports the full lifecycle of
an enterprise engagement:

```
PRODUCT → PRESALES → SOLUTION ARCHITECTURE → SERVICE DELIVERY
                                                       │
                                                       ▼
                                                  PRODUCT (feedback)
```

## 2. Problem Statement

Enterprise engagements span four distinct teams. Each team has its own tools,
artifacts, vocabulary, and decision rights. AI assistants applied to one stage
in isolation produce output that the next team cannot reliably consume, audit,
or trust.

EPE unifies the four stages through:

1. **A normalized Markdown contract** at every stage boundary.
2. **A shared knowledge layer** with provenance and authority metadata.
3. **A configurable AI stack** that does not bind the system to one provider.
4. **Explicit validation gates** at every handover.
5. **A lifecycle state machine** that prevents incomplete handoffs.

## 3. Non-Goals

- EPE is not a replacement for human engineers, architects, or product managers.
- EPE is not a fully autonomous agent system. The initial target is
  **AI-assisted engineering workflow with deterministic artifacts, explicit
  gates, and human approval.**
- EPE is not a CRM, PSA, ITSM, or requirements management tool. It produces
  Markdown artifacts that can be exported to those systems.

## 4. Target Users

| Role          | Primary interaction                                  |
|---------------|------------------------------------------------------|
| Product Mgmt  | Product engine, readiness review, roadmap feedback    |
| Presales      | Discovery, qualification, scoping, SOW, handover     |
| Architecture  | Requirements validation, HLD/LLD, blueprint review   |
| Delivery      | Deployment, validation, operations, optimization     |
| Program Mgmt  | Lifecycle dashboard, gate approvals, traceability    |

## 5. Success Criteria

A pilot project (e.g. MAP-9982) must demonstrate:

- 100% of requirements trace from a customer document to an acceptance test.
- Every stage handover is rejected by the validation engine if a mandatory
  field, decision, or artifact is missing.
- Every AI-generated claim carries provenance back to a source document.
- The lifecycle state machine blocks stage transitions until gates pass.
- The dashboard reflects real artifact state, not duplicated business logic.

## 6. Quality Bar

EPE treats Markdown artifacts and metadata as the engineering plane. The
dashboard is a projection only. Removing the dashboard must not lose a single
decision, requirement, or risk.

## 7. Phased Delivery

| Phase | Scope                                                            |
|-------|------------------------------------------------------------------|
| 0     | Engineering contract (this document + 8 others)                  |
| 1     | Repository scaffolding                                           |
| 2     | Ingestion subsystem                                              |
| 3     | Knowledge engine                                                 |
| 4     | Four stage engines (Product, Presales, Architecture, Delivery)   |
| 5     | Lifecycle orchestration and state machine                        |
| 6     | Validation engine                                                |
| 7     | Dashboard (FastAPI service + read-only projection)              |
| 8     | Pilot project end-to-end                                         |
| 9     | Real-project validation against success criteria                 |

## 8. Acceptance for this Phase

Phase 0 is accepted when:

- All nine contract documents exist under `docs/`.
- Every document cross-references at least one other contract document.
- `OUTPUT_CONTRACTS.md` defines an input/output schema for each stage.
- The four stages can be described end-to-end from `PRD.md` to `SECURITY.md`
  with no missing link.
