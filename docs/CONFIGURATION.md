# EPE — Configuration

All runtime behavior is driven from `config/*.yaml`. Stage engines, ingestion,
retrieval, validation, and the LLM layer all read from this directory. No
provider-, model-, or vendor-specific code may leak outside the abstraction
boundary defined here.

## 1. Configuration Files

```
config/
├── system.yaml          # paths, logging, environment
├── stages.yaml          # per-stage: knowledge, LLM, retrieval, gates
├── tools.yaml           # external tools (PDF libs, etc.)
├── models.yaml          # LLM, embedding, reranker providers
├── ingestion.yaml       # per-format extractors and classifier rules
├── embeddings.yaml      # embedding model + dimensions + batching
├── retrieval.yaml       # strategy, top_k, rerank
├── validation.yaml      # gate predicates and severity levels
└── output.yaml          # output contract paths and schemas
```

## 2. `system.yaml`

```yaml
paths:
  projects_root: projects
  knowledge_root: knowledge
  sources_root: sources
  schemas_root: schemas
  templates_root: templates

logging:
  level: INFO
  json: true

environment: dev                 # dev | staging | prod
```

## 3. `models.yaml`

```yaml
embedding:
  provider: local
  model: bge-m3
  dimensions: 1024
  batch_size: 32
  normalize: true

vector_store:
  provider: pgvector             # pgvector | chroma | qdrant | in_memory
  database: epe
  collection_prefix: epe_

llm:
  provider: anthropic
  model: claude-sonnet-4-5
  max_tokens: 8192
  temperature: 0.2
  timeout_s: 120
  retries: 3

reranker:
  enabled: true
  provider: local
  model: bge-reranker-v2-m3
```

## 4. `stages.yaml`

```yaml
stages:

  product:
    llm: llm
    retrieval:
      strategy: hybrid
      semantic: true
      keyword: true
      rerank: true
      top_k: 12
    knowledge:
      - global
      - product
    inputs:
      - sources/processed
      - knowledge/global
      - knowledge/product
    outputs:
      - product/definition
      - product/catalog
      - product/guardrails
      - product/readiness
    gates:
      - gate.product.definition_complete
      - gate.product.readiness_approved

  presales:
    llm: llm
    retrieval:
      strategy: hybrid
      semantic: true
      keyword: true
      rerank: true
      top_k: 16
    knowledge:
      - global
      - product
      - presales
    inputs:
      - product/readiness
      - product/catalog
      - sources/processed
      - knowledge/presales
    outputs:
      - presales/discovery
      - presales/qualification
      - presales/scope
      - presales/sow
      - presales/handover
    gates:
      - gate.presales.qualification
      - gate.presales.scope
      - gate.presales.handover

  architecture:
    llm: llm
    retrieval:
      strategy: hybrid
      top_k: 20
    knowledge:
      - global
      - product
      - presales
      - architecture
    inputs:
      - presales/handover
      - product/readiness
      - sources/processed
      - knowledge/architecture
    outputs:
      - architecture/validation
      - architecture/hld
      - architecture/security
      - architecture/lld
      - architecture/cost
      - architecture/blueprint
    gates:
      - gate.architecture.requirements
      - gate.architecture.hld
      - gate.architecture.lld

  delivery:
    llm: llm
    retrieval:
      strategy: hybrid
      top_k: 16
    knowledge:
      - global
      - architecture
      - delivery
    inputs:
      - architecture/blueprint
      - architecture/lld
      - sources/processed
      - knowledge/delivery
    outputs:
      - delivery/plan
      - delivery/test
      - delivery/acceptance
      - delivery/onboarding
      - delivery/operations
      - delivery/handover
      - delivery/feedback
    gates:
      - gate.delivery.deployment
      - gate.delivery.acceptance
```

## 5. `ingestion.yaml`

```yaml
extractors:
  pdf: epe.ingestion.extractors.pdf
  docx: epe.ingestion.extractors.docx
  xlsx: epe.ingestion.extractors.xlsx
  pptx: epe.ingestion.extractors.pptx
  md: epe.ingestion.extractors.markdown
  txt: epe.ingestion.extractors.text

classifier:
  rules: epe/ingestion/classifier/rules.yaml
  fallback: heuristic

chunking:
  strategy: by_section
  max_tokens: 512
  overlap: 64

deduplication:
  enabled: true
  by: sha256
```

## 6. `retrieval.yaml`

```yaml
default:
  strategy: hybrid
  top_k: 12
  semantic: true
  keyword: true
  rerank: true

per_stage_overrides:
  product: { top_k: 12 }
  presales: { top_k: 16 }
  architecture: { top_k: 20 }
  delivery: { top_k: 16 }
```

## 7. `validation.yaml`

```yaml
severity_levels:
  - info
  - warning
  - error
  - blocker

gate_predicates:
  gate.product.readiness_approved:
    module: epe.validation.product.readiness_complete
    severity: blocker
  gate.presales.handover:
    module: epe.validation.presales.handover_complete
    severity: blocker
  gate.architecture.lld:
    module: epe.validation.architecture.lld_complete
    severity: blocker
  gate.delivery.acceptance:
    module: epe.validation.delivery.acceptance_complete
    severity: blocker
```

## 8. `output.yaml`

```yaml
contracts:
  product:
    schema: schemas/product.schema.yaml
    paths:
      definition: product/definition.md
      catalog: product/catalog.md
      guardrails: product/guardrails.md
      readiness: product/readiness.md
  presales:
    schema: schemas/presales.schema.yaml
    paths:
      discovery: presales/discovery.md
      qualification: presales/qualification.md
      scope: presales/scope.md
      sow: presales/sow.md
      handover: presales/handover.md
  architecture:
    schema: schemas/architecture.schema.yaml
    paths:
      validation: architecture/validation.md
      hld: architecture/hld.md
      security: architecture/security.md
      lld: architecture/lld.md
      cost: architecture/cost.md
      blueprint: architecture/blueprint.md
  delivery:
    schema: schemas/delivery.schema.yaml
    paths:
      plan: delivery/plan.md
      test: delivery/test.md
      acceptance: delivery/acceptance.md
      onboarding: delivery/onboarding.md
      operations: delivery/operations.md
      handover: delivery/handover.md
      feedback: delivery/feedback.md
```

## 9. Loading Order

1. `system.yaml` loads first and provides paths.
2. `models.yaml` loads second.
3. `stages.yaml` loads third and references `models.yaml` by name.
4. `retrieval.yaml` loads fourth.
5. `validation.yaml` loads fifth and references `stages.yaml`.
6. `output.yaml` loads sixth and references schemas.

A `EpeConfig` Pydantic model enforces that every reference resolves.

## 10. Cross-References

- See `docs/ARCHITECTURE.md` for where config is consumed.
- See `docs/OUTPUT_CONTRACTS.md` for the output schema references.
- See `docs/VALIDATION.md` for the gate predicate semantics.
