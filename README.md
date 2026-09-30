# EPE — Enterprise Playground Engine

Document-driven, configuration-driven, AI-assisted engineering workflow platform
for enterprise engagements.

## Stages

```
PRODUCT → PRESALES → SOLUTION ARCHITECTURE → SERVICE DELIVERY
                                                   │
                                                   ▼
                                                  PRODUCT (feedback)
```

Each stage consumes a validated Markdown contract and produces a validated
Markdown contract. The Markdown artifact is the engineering plane; the
dashboard is a projection.

---

## Full Pipeline: RFP to Live Service

### Stage 1: INTAKE — RFP Arrives
**Input:** `sources/incoming/<RFP>.pdf`

| File | Purpose |
|------|---------|
| `<RFP>.pdf` | Raw procurement document |
| `sources/classified/<id>/metadata.yaml` | Extracted document metadata |
| `sources/processed/<id>/chunks/*.json` | Embedded chunks for retrieval |

```bash
epe ingest --project <id>
```

---

### Stage 2: PRODUCT — Define the Product
**Input:** RFP chunks from knowledge base

| Output File | Content |
|------------|---------|
| `product/definition.md` | Product name, problem statement, users, use cases |
| `product/catalog.md` | Capabilities (CAP-NNN) |
| `product/guardrails.md` | Technical limits, compliance posture |
| `product/readiness.md` | Is product ready for presales? |

**Entity IDs:** `CAP-NNN` (capabilities)

```bash
epe stage run product --project <id> --customer "Acme"
```

---

### Stage 3: PRESALES — Qualify and Scope
**Input:** `product/readiness.md`, `product/catalog.md`

| Output File | Content |
|------------|---------|
| `presales/discovery.md` | Stakeholder discovery, assumptions |
| `presales/qualification.md` | Opportunity qualification |
| `presales/scope.md` | Scoped vs out-of-scope |
| `presales/sow.md` | Statement of work |
| `presales/handover.md` | **Handover contract to Architecture** |

**Entity IDs:** `CUST-NNN` (customer requirements), `REQ-NNN` (requirements)
**Gate:** `presales/handover.md` approved → triggers Architecture

```bash
epe stage run presales --project <id> --opportunity OPP-001
```

---

### Stage 4: ARCHITECTURE — Design the Solution
**Input:** `presales/handover.md`

| Output File | Content |
|------------|---------|
| `architecture/validation.md` | Per-REQ validation, contradictions, open questions |
| `architecture/hld.md` | High-level design: drivers, components, data flows |
| `architecture/security.md` | Threat model, controls, identity, compliance |
| `architecture/lld.md` | Per-component detailed design |
| `architecture/cost.md` | Line items, assumptions, ranges, optimization |
| `architecture/solution-baseline.md` | **SM→Delivery handover contract** |

**Entity IDs:** `COMP-NNN`, `DEC-NNN`, `TASK-NNN`, `TEST-NNN`, `RSK-NNN`, `ASM-NNN`, `DEP-NNN`
**Per-entity files:** `entities/{req,comp,dec,task,test,rsk,asm,dep}/*.md`
**Gate:** `architecture/solution-baseline.md` approved → triggers Delivery

```bash
epe stage run architecture --project <id> --opportunity OPP-001
```

---

### Stage 5: DELIVERY — Build and Deploy
**Input:** `architecture/solution-baseline.md`, `architecture/lld.md`

| Output File | Content |
|------------|---------|
| `delivery/plan.md` | Sequencing, milestones, owners |
| `delivery/test.md` | Test plan mapping TEST-NNN → REQ-NNN |
| `delivery/acceptance.md` | Executed tests with results |
| `delivery/onboarding.md` | Customer-facing onboarding |
| `delivery/operations.md` | Monitoring, alerting, SLA, runbooks |
| `delivery/handover.md` | **Delivery→Customer handover** |
| `delivery/feedback.md` | **Feedback to Product** |

**Evidence:** `evidence/EVD-*.md` — one per TEST with PASS/FAIL result
**Entity IDs:** `EVD-NNN` (evidence records)
**Gate:** All acceptance tests pass → triggers Service Live

```bash
epe stage run delivery --project <id> --opportunity OPP-001
```

---

## Project Structure

```
projects/<id>/
├── sources/
│   ├── incoming/              ← Raw RFP (drop files here)
│   ├── classified/            ← Document metadata
│   └── processed/            ← Chunked + embedded
├── product/                   ← Definition, catalog, guardrails, readiness
├── presales/                  ← Discovery, qualification, scope, SOW, handover
├── architecture/
│   ├── *.md                  ← 6 artifacts
│   └── solution-baseline.md   ← SM→Delivery contract
├── delivery/
│   ├── *.md                  ← 7 artifacts
│   └── handover.md           ← Customer handover
├── entities/                  ← Per-entity files
│   ├── req/                  ← REQ-NNN requirements
│   ├── comp/                 ← COMP-NNN components
│   ├── dec/                  ← DEC-NNN decisions
│   ├── task/                 ← TASK-NNN tasks
│   ├── test/                 ← TEST-NNN tests
│   ├── rsk/                  ← RSK-NNN risks
│   ├── asm/                  ← ASM-NNN assumptions
│   ├── dep/                  ← DEP-NNN dependencies
│   └── evd/                  ← EVD-NNN evidence
├── decisions/                 ← Decision registry
├── requirements/             ← Requirements registry
├── risks/                    ← Risk registry
├── evidence/                 ← Evidence records (EVD-*.md)
├── questions/                ← Open questions
└── state.yaml               ← Lifecycle state machine
```

---

## Traceability Spine

Every entity is tracked and traceable:

```
CUST → REQ → COMP → DEC → TEST → EVD → ACCEPTANCE → AS-BUILT
                    ↳ ASM (affects REQ)
                    ↳ DEP (blocks REQ)
                    ↳ CHG (modifies entities)
```

---

## Entity ID Reference

| Prefix | Entity | Description |
|--------|--------|-------------|
| `CUST-NNN` | Customer Requirement | Raw customer need |
| `REQ-NNN` | Requirement | Refined requirement |
| `CAP-NNN` | Capability | Product capability |
| `COMP-NNN` | Component | Solution component |
| `DEC-NNN` | Decision | Architecture decision |
| `TASK-NNN` | Task | Implementation task |
| `TEST-NNN` | Test | Acceptance test |
| `EVD-NNN` | Evidence | Test evidence record |
| `RSK-NNN` | Risk | Identified risk |
| `ASM-NNN` | Assumption | Working assumption |
| `DEP-NNN` | Dependency | External dependency |
| `CHG-NNN` | Change Request | Proposed change |

---

## Diagrams

EPE generates draw.io diagrams for visualization via the `DiagramRouter`:

```python
from epe.diagram.router import DiagramRouter, DiagramRequest, DiagramType

router = DiagramRouter()
router.render(DiagramRequest(
    diagram_type=DiagramType.LIFECYCLE_FLOW,
    project_id='<id>',
    output_path='docs/diagrams/lifecycle.drawio'
))
```

| Diagram Type | MCP Server | Purpose |
|-------------|------------|---------|
| `LIFECYCLE_FLOW` | jgraph/drawio-mcp | Stage-to-stage flow |
| `TRACEABILITY_SPINE` | jgraph/drawio-mcp | Entity relationships |
| `COMPONENT_MAP` | lgazo/drawio-mcp-server | Component map |
| `AZURE_ARCH` | Azure-DrawIO-MCP | Azure architecture |

**MCP Servers** (configured in `~/.claude/settings.json`):
- `jgraph/drawio-mcp` — inline diagram rendering
- `Azure-DrawIO-MCP` — Azure-specific architectures
- `lgazo/drawio-mcp-server` — full programmatic diagram control

---

## Quickstart

```bash
# 1. Install
python -m venv .venv && source .venv/bin/activate
pip install -e ".[all]"

# 2. Set the LLM key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Create a project
epe project create MAP-9982

# 4. Ingest source documents into sources/incoming/
epe ingest --project MAP-9982

# 5. Run a stage engine
epe stage run product  --project MAP-9982
epe stage run presales --project MAP-9982
epe stage run architecture --project MAP-9982
epe stage run delivery --project MAP-9982

# 6. Inspect the dashboard
uvicorn epe.dashboard.app:app --reload --port 8088
```

---

## Layout

```
docs/                 engineering contract
config/               runtime configuration
src/epe/              Python package
  core/               config loader, paths, errors, logging
  ingestion/          PDF/DOCX/XLSX/PPTX/MD extractors, classifier
  knowledge/          namespaces, embeddings, vector store, retrieval
  stages/             four stage engines
  orchestration/      lifecycle, gates, handovers, state machine
  validation/         structural, content, traceability, security
  dashboard/          FastAPI service
  diagram/            draw.io diagram router
knowledge/            five namespaces (global, product, presales, architecture, delivery)
sources/              incoming / classified / processed / rejected
projects/             one directory per project
schemas/              JSON Schema for output contracts
templates/            per-stage Markdown templates
workflows/            per-stage workflow YAML
tests/                pytest suite
docs/diagrams/         draw.io diagrams
```

---

## Engineering Contract

The contract for the system is in `docs/`:

- `PRD.md`
- `ARCHITECTURE.md`
- `DATA_MODEL.md`
- `WORKFLOW.md`
- `CONFIGURATION.md`
- `KNOWLEDGE_MODEL.md`
- `OUTPUT_CONTRACTS.md`
- `VALIDATION.md`
- `SECURITY.md`

## License

Apache-2.0
