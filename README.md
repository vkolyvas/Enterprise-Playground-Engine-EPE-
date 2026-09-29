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
knowledge/            five namespaces (global, product, presales, architecture, delivery)
sources/              incoming / classified / processed / rejected
projects/             one directory per project
schemas/              JSON Schema for output contracts
templates/            per-stage Markdown templates
workflows/            per-stage workflow YAML
tests/                pytest suite
```

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
