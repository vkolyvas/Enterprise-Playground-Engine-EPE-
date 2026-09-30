# Lifecycle Document Operating System — Audit

**Audited:** 2026-09-30
**Based on:** EPE codebase at commit `0baa5ce`

---

## 1. Existing Stages

| Stage | Defined in | Current outputs |
|-------|-----------|-----------------|
| Product | `lifecycle.py:State`, `stages/product/` | `definition.md`, `catalog.md`, `guardrails.md`, `readiness.md` |
| Presales | `lifecycle.py:State`, `stages/presales/` | `discovery.md`, `qualification.md`, `scope.md`, `sow.md`, `handover.md` |
| Architecture | `lifecycle.py:State`, `stages/architecture/` | `validation.md`, `hld.md`, `security.md`, `lld.md`, `cost.md`, `blueprint.md` |
| Delivery | `lifecycle.py:State`, `stages/delivery/` | `plan.md`, `test.md`, `acceptance.md`, `onboarding.md`, `operations.md`, `handover.md`, `feedback.md` |

**Observation:** The four canonical stages exist and are wired into the state machine. All 22 artifact types are already being produced by the stage engines.

---

## 2. Existing Documents

All artifacts exist as Markdown + YAML frontmatter in `projects/<id>/<stage>/`.

**Existing mandatory frontmatter fields:**
- `contract`, `version`, `stage`, `status`, `generated_at`, `generated_by`, `project_id`, `opportunity`, `customer`, `provenance.source_documents`, `checksum_sha256`

**Existing document statuses:** `draft | in_review | approved | rejected`

**Gaps in current document metadata:**
- No `owner`, `version` beyond `generated_at`, `inputs`, `outputs`
- No `requirements`, `risks`, `decisions` linkage fields
- No document `type` (TEMPLATE / INSTANCE / EVIDENCE / DECISION / DELIVERABLE / REFERENCE)
- No lifecycle-level document IDs (DOC-PROD-001, etc.)

---

## 3. Missing Documents

### Product stage — fully implemented
All 10 mandatory documents have corresponding artifacts:
- `problem-statement.md` → covered by `product/definition.md`
- `prd.md` → covered by `product/definition.md`
- `product-requirements.md` → covered by `product/catalog.md`
- `feature-matrix.md` → covered by `product/catalog.md`
- `personas-and-use-cases.md` → covered by `product/definition.md`
- `business-case.md` → NOT present as separate doc (part of definition)
- `acceptance-criteria.md` → covered by `product/guardrails.md`
- `competitive-landscape.md` → NOT present
- `product-architecture.md` → NOT present as separate doc
- `roadmap.md` → NOT present

**Gap:** The current 4-product-artifact model compresses 10+ document purposes into 4 files. The user's requirement for a **mandatory document set** means either:
1. Splitting artifacts into more focused files, OR
2. Adding document-type metadata to distinguish purposes within a single artifact

### Presales stage — substantially implemented
The 20 presales documents map to existing artifacts:
- `account-brief.md`, `opportunity-brief.md` → `discovery.md`
- `discovery-questionnaire.md` → `discovery.md`
- `technical-discovery.md` → `discovery.md`
- `customer-requirements.md` → `scope.md`
- `requirements-matrix.md` → `scope.md`
- `fit-gap-analysis.md` → `scope.md`
- `solution-overview.md` → `scope.md`
- `reference-architecture.md` → `scope.md`
- `architecture-options.md` → `scope.md`
- `security-questionnaire.md` → `scope.md`
- `compliance-matrix.md` → `scope.md`
- `rfp-response.md` → `sow.md`
- `poc-plan.md` → `scope.md`
- `poc-success-criteria.md` → `scope.md`
- `pov-runbook.md` → `scope.md`
- `demo-script.md` → `discovery.md`
- `bom-sizing.md` → `sow.md`
- `commercial-assumptions.md` → `sow.md`
- `risks-assumptions-dependencies.md` → `scope.md`
- `presales-recommendation.md` → `handover.md`

**Gap:** The current 5-presales-artifact model condenses 20+ purposes. The requirements matrix, fit/gap analysis, and POC plan are embedded rather than structured standalone documents.

### Architecture stage — substantially implemented
The 18 architecture documents map to existing artifacts:
- `solution-design.md` → `hld.md`
- `hld.md` → `hld.md`
- `lld.md` → `lld.md`
- `architecture-diagrams.md` → embedded in `hld.md`
- `integration-design.md` → `validation.md`
- `data-flow.md` → `hld.md`
- `network-design.md` → `lld.md`
- `security-architecture.md` → `security.md`
- `iam-design.md` → `security.md`
- `availability-dr-dr.md` → `security.md`
- `capacity-sizing.md` → `cost.md`
- `bill-of-materials.md` → `cost.md`
- `implementation-plan.md` → `blueprint.md`
- `migration-plan.md` → `blueprint.md`
- `test-strategy.md` → `blueprint.md`
- `rollback-strategy.md` → `blueprint.md`
- `risks-assumptions-dependencies.md` → `validation.md`
- `architecture-decisions.md` → `validation.md`

### Delivery stage — substantially implemented
The 18 delivery documents map to existing artifacts.

---

## 4. Traceability — THE KEY GAP

**Current traceability:**
- `docs/DATA_MODEL.md §12` describes the traceability graph
- `validation/traceability.py:build_traceability_graph()` derives edges from frontmatter IDs (REQ, CAP, DEC, COMP, TASK, TEST, Q, RSK)
- Edges: `source_document ──▶ requirement ──▶ architecture_component ──▶ delivery_task ──▶ acceptance_test`

**What's missing for the user's traceability spine:**
```
Requirement → CustomerRequirement → SolutionComponent → ArchitectureDecision → TestCase → Evidence → Handover
```

Missing entity types:
- `CustomerRequirement` (distinct from generic `Requirement`)
- `SolutionComponent` (currently only `architecture_component` which maps to `COMP-NNN`)
- `Evidence` (not modeled as a first-class entity)
- Formal `Deliverable` entity

Missing relationships:
- `CustomerRequirement` → `ProductRequirement` (cross-stage lineage)
- `SolutionComponent` → `ArchitectureDecision`
- `TestCase` → `Evidence`
- `Document` → `Stage` / `Gate` relationships

**This is the core gap the user identified: EPE currently has a structural traceability (which IDs exist) but lacks cross-stage document lineage.**

---

## 5. Existing Reusable Components

| Component | Location | Usable for LDOS? |
|-----------|----------|-----------------|
| Frontmatter read/write | `core/frontmatter.py` | ✅ Yes — extend metadata schema |
| Document status | Already `draft/in_review/approved/rejected` | ✅ Already present |
| ID generation | Various ID schemes in `docs/DATA_MODEL.md` | ✅ Extend to DOC-PROD-001 pattern |
| Lifecycle state machine | `orchestration/lifecycle.py` | ✅ Already correct |
| Gate predicates | `validation/{stage}.py` | ✅ Extend for document completeness |
| Stage engines | `stages/base.py` | ✅ Extend outputs list |
| Validation engine | `validation/engine.py` | ✅ Extend REQUIRED_SECTIONS |
| Handover execution | `orchestration/handover.py` | ✅ Already present |
| Audit logging | `core/logging.py:audit_log` | ✅ Already present |

---

## 6. Integration Points

1. **`templates/` directory** — currently empty, needs document templates
2. **`workflows/` directory** — currently empty, per-stage workflow YAMLs
3. **`knowledge/` namespaces** — `global/`, `product/`, `presales/`, `architecture/`, `delivery/` all empty; document templates could seed knowledge
4. **`orchestration/handover.py`** — already stamps `status: approved` + `approved_by` + `approved_at`; could extend to document-level approval
5. **`core/frontmatter.py`** — `read_doc()` / `write_doc()` are the single write path; metadata schema extension needs to happen here
6. **Dashboard projections** — `dashboard/projections.py` generates the Markdown dashboard; could add document lifecycle view

---

## 7. Files That Must NOT Be Modified

- `data/embedding_cache/` — runtime cache
- `.validation/` — runtime output
- `_audit/` — audit log (if it exists)
- Any existing generated artifacts in `projects/`

---

## 8. Recommended Approach

The user is explicit: **not the number of documents, but the traceability spine**.

The implementation must add:
1. **Formal entity models** for `CustomerRequirement`, `SolutionComponent`, `Evidence`, `Deliverable`
2. **Cross-stage document lineage** — documents carry references to upstream inputs
3. **Document metadata extension** — owner, version, inputs, outputs, type, linkage to requirements/risks/decisions
4. **Lifecycle document registry** — a view of all documents across stages with status
5. **Document completeness validation** — gate predicates that check document content completeness, not just file existence
6. **Optional: Document templates** — Jinja2 templates in `templates/` for structured generation

The existing artifact set (22 files across 4 stages) is **sufficient** — the gap is traceability metadata and content completeness enforcement, not new document types.
