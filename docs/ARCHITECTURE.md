# EPE — Architecture

## 1. Architectural Principles

1. **Document-first.** Markdown artifacts are the canonical interoperability
   protocol between stages. No internal agent-to-agent RPC.
2. **Configuration-driven.** No provider, model, embedding, vector store, or
   prompt template may be hard-coded into stage logic.
3. **Stage-independent.** Each stage engine must be runnable in isolation
   given its declared inputs.
4. **Provenance mandatory.** Every claim must reference a source.
5. **Gate-enforced.** No downstream stage may consume an incomplete upstream
   contract silently.
6. **Human readable, machine consumable.** The same `.md` file is for both.
7. **Provider-agnostic.** Claude, embeddings, and vector stores are swappable
   via `config/`.
8. **Dashboard is a projection.** Removing the dashboard must lose zero
   decisions, requirements, or risks.

## 2. Layers

```
┌──────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                         │
│   CLI (scripts/)   |   FastAPI dashboard (dashboard/)    │
└────────────────────────────┬─────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────┐
│                  ORCHESTRATION LAYER                      │
│   Lifecycle state machine, handover contracts, gates     │
└────────────────────────────┬─────────────────────────────┘
                             │
┌────────────┬───────────────┼───────────────┬─────────────┐
│            │               │               │             │
▼            ▼               ▼               ▼             ▼
PRODUCT    PRESALES     ARCHITECTURE      DELIVERY     INGESTION
engine     engine        engine           engine       subsystem
│            │               │               │             │
└────────────┴───────┬───────┴───────────────┴─────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│                  KNOWLEDGE LAYER                          │
│   Namespaces · embeddings · vector store · hybrid ret.   │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│              INFRASTRUCTURE LAYER                         │
│   LLM provider · embeddings · vector DB · filesystem     │
└────────────────────────────────────────────────────────────┘
```

## 3. Module Layout

```
src/epe/
├── core/                 # config loader, paths, errors, logging
├── ingestion/            # PDF/DOCX/XLSX/PPTX/MD extractors, classifier
├── knowledge/            # namespaces, embeddings, vector store, retrieval
├── stages/
│   ├── product/
│   ├── presales/
│   ├── architecture/
│   └── delivery/
├── orchestration/        # lifecycle, gates, handovers, state machine
├── validation/           # structural, content, traceability, security
├── dashboard/            # FastAPI service + read-only projections
└── cli.py                # top-level CLI entry
```

## 4. Data Flow

```
source documents
       │
       ▼
[ingestion] classify → extract → normalize → metadata
       │
       ▼
[knowledge] chunk → embed → store → retrieve
       │
       ▼
[stage engine] context → retrieve → analyze → validate → write artifact
       │
       ▼
[orchestration] gate check → state transition → emit handover
       │
       ▼
[dashboard] projection only
```

## 5. Configuration Model

All runtime behavior is driven from `config/*.yaml`. Stage engines read
`config/stages.yaml` to learn:

- which knowledge namespaces they may access
- which LLM provider / model to use
- which retrieval strategy (semantic / keyword / hybrid / rerank)
- which validation gates apply
- which output contracts to enforce

See `docs/CONFIGURATION.md`.

## 6. Inter-Stage Contracts

Each stage consumes a contract and produces a contract. The canonical
interoperability layer is the Markdown file with structured frontmatter.

| From → To              | Contract file                              |
|------------------------|--------------------------------------------|
| Product → Presales     | `product/readiness.md`                     |
| Presales → Architecture| `presales/handover.md`                     |
| Architecture → Delivery| `architecture/solution-baseline.md` |
| Delivery → Product     | `delivery/feedback.md`                     |

See `docs/OUTPUT_CONTRACTS.md`.

## 7. Lifecycle State Machine

States:

```
PRODUCT_READY
PRESALES_ACTIVE
PRESALES_READY
ARCHITECTURE_ACTIVE
ARCHITECTURE_READY
DELIVERY_ACTIVE
SERVICE_LIVE
OPTIMIZATION
```

A transition requires all gates for the destination state to be `passed`.
The state machine is the single source of truth for "what is the project
doing right now?".

See `docs/WORKFLOW.md`.

## 8. Failure Modes and Isolation

- An ingestion failure isolates the source document; the rest of the batch
  continues.
- A knowledge-layer failure surfaces as a retrieval error to the stage
  engine, never as a silent empty result.
- A stage validation failure halts the engine before any artifact is written.
- An orchestration gate failure halts the state transition.

## 9. Security Posture

See `docs/SECURITY.md`. In short:

- Source documents carry sensitivity metadata and access scope.
- Knowledge namespaces inherit access scope from sources.
- AI prompts never include secrets.
- AI responses are validated against the output schema before any artifact
  is written.

## 10. Extensibility

To add a new document type:

1. Add an extractor under `src/epe/ingestion/extractors/`.
2. Register it in `config/ingestion.yaml`.
3. Add a test under `tests/ingestion/`.

To add a new stage:

1. Create `src/epe/stages/<stage>/`.
2. Add its contract to `docs/OUTPUT_CONTRACTS.md`.
3. Add its gates to `docs/VALIDATION.md`.
4. Wire it into `config/stages.yaml` and the state machine.

To swap LLM provider:

1. Implement `LLMProvider` in `src/epe/knowledge/providers/`.
2. Register it in `config/models.yaml`.

## 11. Cross-References

- Data model: `docs/DATA_MODEL.md`
- Workflow and gates: `docs/WORKFLOW.md`
- Configuration: `docs/CONFIGURATION.md`
- Knowledge model: `docs/KNOWLEDGE_MODEL.md`
- Output contracts: `docs/OUTPUT_CONTRACTS.md`
- Validation: `docs/VALIDATION.md`
- Security: `docs/SECURITY.md`
