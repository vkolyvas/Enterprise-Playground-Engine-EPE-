# EPE Lifecycle Document Operating System — Implementation Plan

## Context

The existing EPE has a functioning four-stage lifecycle (Product → Presales → Architecture → Delivery) with 22 artifact types produced by LLM-driven stage engines. The gap identified by the user is **not document volume** but **traceability**: information is not carried forward between stages, requirements cannot be traced from Product to Delivery, and documents lack machine-readable lineage metadata.

**Core principle from user:** "Without Requirement → Solution → Decision → Test → Evidence → Handover, EPE becomes a sophisticated folder/template generator. With it, it starts looking like an actual enterprise solution lifecycle platform."

---

## What Exists vs. What Needs to Be Built

| What | Status |
|------|--------|
| Four-stage lifecycle state machine | ✅ Implemented |
| 22 artifact types produced by stage engines | ✅ Implemented |
| YAML frontmatter on all artifacts | ✅ Implemented |
| Document status (draft/in_review/approved/rejected) | ✅ Implemented |
| Gate predicates per stage | ✅ Implemented |
| Traceability graph derivation (IDs in frontmatter) | ✅ Implemented |
| Handover execution with approval stamping | ✅ Implemented |
| Feedback loop (delivery → product) | ✅ Implemented |
| **Cross-stage document lineage (Requirement → Delivery)** | ❌ Missing |
| **CustomerRequirement entity (distinct from Requirement)** | ❌ Missing |
| **Evidence entity** | ❌ Missing |
| **Document completeness gate enforcement** | ❌ Partial |
| **Document registry/view across all stages** | ❌ Missing |
| **Enhanced document metadata (owner, version, inputs, outputs, type)** | ❌ Missing |
| **Document lifecycle UI dashboard** | ❌ Missing |
| **Lifecycle document validator script** | ❌ Missing |

---

## Implementation Milestones

### M1 — Traceability Spine (Core Data Model)

**Goal:** Add the five missing entity types and their relationships to create a formal traceability backbone.

**Files to create:**
- `src/epe/tracking/models.py` — Pydantic models for:
  - `CustomerRequirement` (`src/epe/tracking/customer_requirement.py`)
  - `SolutionComponent` — already partially exists as `COMP-NNN` in data model
  - `Evidence` — artifact evidence record
  - `Deliverable` — formal deliverable with stage/gate/owner metadata
  - `DocumentLink` — typed relationship between documents (INPUTS/OUTPUTS/SUPPORTED_BY/APPROVES)

- `src/epe/tracking/registry.py` — `DocumentRegistry` class:
  - Scans `projects/<id>/<stage>/` for all `.md` files
  - Reads frontmatter, builds `DocumentRecord` with enhanced metadata
  - Exposes `get_inputs(document_id)` and `get_outputs(document_id)`
  - Computes cross-stage lineage graph

- `src/epe/tracking/lineage.py` — `LineageComputer`:
  - Given a `CustomerRequirement`, traces forward through stages
  - Given a `Requirement`, traces to `SolutionComponent` → `TASK` → `TEST` → `Evidence`
  - Detects broken lineage chains

**Files to modify:**
- `docs/DATA_MODEL.md` — add `CustomerRequirement`, `Evidence`, `Deliverable` entity schemas
- `src/epe/core/paths.py` — add `projects/<id>/.registry/` directory

**Schema additions to frontmatter:**
```yaml
id: DOC-ARCH-001           # new lifecycle-scoped document ID
type: deliverable          # template | instance | evidence | decision | deliverable | reference
owner: lead_architect       # new
version: 1.0                # new — semantic version, not just generated_at
inputs:                     # new — upstream document IDs this doc consumes
  - DOC-PROD-014
  - DOC-PRE-008
outputs:                    # new — downstream document IDs this doc produces
  - DOC-ARCH-003
requirements: [REQ-014]     # new — formal linkage
risks: [RSK-003]
decisions: [DEC-001]
supersedes: DOC-ARCH-001    # new — for versioned documents
superseded_by: null
```

**Decision:** Keep the 22 existing artifact filenames unchanged to preserve backward compatibility. The enhanced metadata is additive — existing artifacts gain new fields without renaming.

---

### M2 — Document Completeness Validation

**Goal:** Gate transitions on content completeness, not just file existence.

**Files to create:**
- `src/epe/validation/completeness.py` — `DocumentCompletenessValidator`:
  - Checks required sections present (extends `REQUIRED_SECTIONS` from `validation/engine.py`)
  - Checks frontmatter completeness (all required fields present)
  - Checks ID references are resolvable (REQ/DEC/CAP/TASK/TEST IDs cited in body exist)
  - Returns per-document completeness score

- `src/epe/validation/gate_validator.py` — `GateDocumentValidator`:
  - Aggregates completeness results per stage
  - Determines if a stage gate should pass based on ALL required documents being complete
  - Exposes: `READY`, `BLOCKED`, `WARNING`, `IN_PROGRESS`

**Files to modify:**
- `src/epe/validation/engine.py` — extend `REQUIRED_SECTIONS` with the additional section requirements from the user's document lists
- `src/epe/validation/product.py`, `presales.py`, `architecture.py`, `delivery.py` — add document completeness predicates

---

### M3 — Handover Enhancement

**Goal:** Formal handoff packages with document manifests.

**Files to create:**
- `src/epe/orchestration/handover_extended.py` — extend `execute_handover()`:
  - Generate a `handover-manifest.yaml` listing all artifacts, their versions, completeness status
  - Attach `handover_manifest` field to the handover record
  - Validate that all upstream requirements are linked in downstream artifacts

**Files to modify:**
- `src/epe/orchestration/handover.py` — extend `HandoverRecord` with `manifest: list[dict]` field
- `src/epe/stages/{product,presales,architecture,delivery}/engine.py` — add input/output linkage to frontmatter when writing artifacts

---

### M4 — Lifecycle Document Dashboard View

**Goal:** Add a read-only lifecycle document view to the FastAPI dashboard.

**Files to create:**
- `src/epe/dashboard/lifecycle_view.py` — `LifecycleDocumentView`:
  - `GET /projects/{id}/lifecycle/documents` — all documents across stages with status, owner, completeness
  - `GET /projects/{id}/lifecycle/stages` — per-stage document summary with gate status
  - `GET /projects/{id}/lifecycle/lineage/{doc_id}` — full lineage for a specific document
  - `GET /projects/{id}/lifecycle/gates` — gate readiness matrix

**Files to modify:**
- `src/epe/dashboard/projections.py` — add `lifecycle_document_summary()` projection
- `src/epe/dashboard/app.py` — mount new routes

**UI display format:**
```
┌─────────────────────────────────────────────────────────────┐
│ EPE LIFECYCLE — {project_id}                                │
├────────────┬────────────┬────────────┬─────────────────────┤
│ PRODUCT ✓  │ PRESALES ✓ │ ARCHITECT ⚠ │ DELIVERY ○     │
└────────────┴────────────┴────────────┴─────────────────────┘

PRODUCT     4/4 docs  ✓  Approved: 4  Gate: READY
PRESALES    5/5 docs  ✓  Approved: 3  Gate: READY
ARCHITECTURE 6/6 docs ⚠  Approved: 2  Gate: BLOCKED (hld incomplete)
DELIVERY    7/7 docs   ○  Approved: 0  Gate: IN_PROGRESS
```

---

### M5 — Lifecycle Validator Script

**Goal:** Standalone script to validate lifecycle integrity across all stages.

**Files to create:**
- `scripts/validate_lifecycle.py` — `LifecycleValidator`:
  - `--project <id>` — validate a specific project
  - `--all` — validate all projects
  - Checks: missing mandatory documents, invalid frontmatter, duplicate IDs, broken references, requirements without owners, tests without requirements, approved docs with unresolved dependencies
  - Returns non-zero exit code on failure

**Checks to implement:**
1. All mandatory documents exist (per stage)
2. Frontmatter has all required fields
3. No duplicate document IDs
4. All `REQ-*` / `DEC-*` / `CAP-*` etc. IDs referenced in body have corresponding files
5. Every requirement has an owner
6. Every requirement has acceptance criteria
7. Every architecture component has an upstream requirement
8. Every test has a linked requirement
9. Approved documents have no unresolved mandatory dependencies
10. Handover documents reference upstream stage artifacts

---

### M6 — Document Templates (Optional Enhancement)

**Goal:** Provide structured templates in `templates/` for document generation, reducing LLM hallucination risk.

**Files to create:**
- `templates/product/problem-statement.md.j2`
- `templates/product/prd.md.j2`
- `templates/product/feature-matrix.md.j2`
- `templates/presales/discovery-questionnaire.md.j2`
- `templates/presales/requirements-matrix.md.j2`
- `templates/presales/fit-gap-analysis.md.j2`
- `templates/presales/poc-plan.md.j2`
- `templates/presales/poc-success-criteria.md.j2`
- `templates/architecture/hld.md.j2`
- `templates/architecture/lld.md.j2`
- `templates/architecture/adr.md.j2`
- `templates/delivery/test-plan.md.j2`
- `templates/delivery/uat-results.md.j2`
- `templates/delivery/as-built.md.j2`
- `templates/delivery/handover.md.j2`

**Template structure:**
```jinja2
---
id: {{ doc_id }}
title: {{ title }}
stage: {{ stage }}
type: {{ doc_type }}
status: draft
owner: {{ owner }}
version: 1.0
created: {{ created_date }}
inputs:
{% for inp in inputs %}
  - {{ inp }}
{% endfor %}
outputs:
{% for out in outputs %}
  - {{ out }}
{% endfor %}
requirements: []
risks: []
decisions: []
---
# {{ title }}

{{ body }}
```

**Decision:** Templates are optional — they supplement (not replace) the current LLM-driven generation. Stage engines can optionally use templates as prompt scaffolding.

---

### M7 — End-to-End Demonstration

**Goal:** Prove the full traceability spine works by running a project through all stages.

1. Create a new project or use `Tele-MANAS-IT-Services-RFP`
2. Run Product → Presales → Architecture → Delivery
3. Verify document registry captures all 22 artifacts
4. Verify cross-stage lineage (e.g., customer requirement in `scope.md` traces to component in `hld.md` traces to task in `plan.md` traces to test in `test.md`)
5. Verify gate status reflects document completeness
6. Run `scripts/validate_lifecycle.py` against the project

---

## Files to Create (Summary)

| Path | Purpose |
|------|---------|
| `src/epe/tracking/__init__.py` | Package init |
| `src/epe/tracking/models.py` | Core Pydantic models for new entities |
| `src/epe/tracking/registry.py` | Document registry and scanner |
| `src/epe/tracking/lineage.py` | Lineage computation |
| `src/epe/validation/completeness.py` | Document completeness validator |
| `src/epe/validation/gate_validator.py` | Gate-level document validator |
| `src/epe/orchestration/handover_extended.py` | Enhanced handover with manifests |
| `src/epe/dashboard/lifecycle_view.py` | Lifecycle document dashboard routes |
| `scripts/validate_lifecycle.py` | Standalone validation script |
| `templates/product/*.md.j2` | Product stage templates |
| `templates/presales/*.md.j2` | Presales stage templates |
| `templates/architecture/*.md.j2` | Architecture stage templates |
| `templates/delivery/*.md.j2` | Delivery stage templates |

## Files to Modify (Summary)

| Path | Change |
|------|--------|
| `docs/DATA_MODEL.md` | Add CustomerRequirement, Evidence, Deliverable schemas |
| `src/epe/core/paths.py` | Add `.registry/` directory |
| `src/epe/core/frontmatter.py` | Extend frontmatter schema with new fields |
| `src/epe/validation/engine.py` | Extend REQUIRED_SECTIONS |
| `src/epe/validation/{product,presales,architecture,delivery}.py` | Add document completeness predicates |
| `src/epe/orchestration/handover.py` | Extend HandoverRecord with manifest |
| `src/epe/stages/*/engine.py` | Add input/output linkage to frontmatter |
| `src/epe/dashboard/projections.py` | Add lifecycle document projections |
| `src/epe/dashboard/app.py` | Mount new routes |
| `tests/test_tracking.py` | New tests for traceability spine |

## Implementation Order

```
M1 (Traceability Spine)  ← MUST be first — everything builds on this
    ↓
M2 (Document Completeness Validation)
    ↓
M3 (Handover Enhancement)
    ↓
M4 (Lifecycle Document Dashboard)
    ↓
M5 (Lifecycle Validator Script)
    ↓
M6 (Document Templates)   ← Optional, can run in parallel
    ↓
M7 (End-to-End Demo)
```

## Key Architectural Decisions

1. **No new document types at the filesystem level** — the 22 existing artifact files remain unchanged. Enhanced metadata is added to frontmatter. This preserves backward compatibility with existing generated artifacts.

2. **No database** — all state remains in YAML frontmatter and the filesystem. The registry is derived on demand.

3. **Document ID scheme** — introduce `DOC-<STAGE>-NNN` for cross-stage document identification while preserving existing `DOC-NNN` for source documents.

4. **Templates are additive** — they provide structure but don't change how stage engines work (engines still use prompts + LLM).

5. **Completeness is not the same as approval** — a document can be complete (all sections present, all IDs resolvable) but not yet approved. Both completeness AND approval are required for gate passage.

---

## Acceptance Criteria

The feature is complete when:

1. `scripts/validate_lifecycle.py --project <id>` returns 0 with no errors for a project that has run through all four stages
2. The dashboard endpoint `GET /projects/{id}/lifecycle/documents` returns all 22+ documents with correct metadata (owner, version, status, inputs, outputs)
3. A customer requirement captured in Presales can be traced through Architecture to Delivery task to Test to Evidence
4. The gate status for each stage reflects actual document completeness, not just file existence
5. A handover manifest lists all artifacts with their completeness status
6. All existing tests pass
