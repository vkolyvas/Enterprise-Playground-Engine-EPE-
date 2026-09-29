# EPE — Knowledge Model

## 1. Namespaces

EPE organizes knowledge into five namespaces, each with its own access scope
and provenance policy.

```
knowledge/
├── global/         # glossary, standards, policies, guardrails
├── product/        # product definitions, catalogs, roadmaps
├── presales/       # playbooks, qualification templates, SOW examples
├── architecture/   # reference architectures, patterns, standards
└── delivery/       # runbooks, deployment patterns, operations guides
```

A stage engine may only read namespaces listed in its
`config/stages.yaml` entry. Any access outside that list is a configuration
error and is rejected at engine initialization.

## 2. Knowledge Item

Every chunk in the knowledge layer is a `KnowledgeItem`:

```yaml
chunk_id: KNW-product-0007
namespace: product
source_document_id: DOC-00031
source_path: knowledge/product/managed-postgres.md
section: "Capacity Planning"
position: 12
sha256: <hex>

text: |
  Managed Postgres instances are sized by vCPU and memory...

metadata:
  topics: [postgres, capacity, sizing]
  entities: [PostgreSQL, RDS]
  authority: vendor             # vendor | internal | customer | market
  confidence: high
  sensitivity: internal
  valid_from: 2026-01-01
  valid_until: 2027-01-01

embedding:
  provider: local
  model: bge-m3
  dimensions: 1024
  vector: <opaque>
```

## 3. Ingestion → Knowledge Flow

```
source document
   │
   ▼ extract
text + structure
   │
   ▼ chunk
KnowledgeChunk(s)
   │
   ▼ embed
KnowledgeItem(s) with embedding.vector
   │
   ▼ store
vector store  +  knowledge index (yaml/json sidecar)
   │
   ▼ retrieve
top_k KnowledgeItem(s) + provenance
```

The knowledge index (sidecar) is what makes retrieval **explainable**: the
LLM never sees a chunk without being able to cite it.

## 4. Retrieval Modes

| Mode    | Use when                                          |
|---------|---------------------------------------------------|
| keyword | exact terms (compliance, vendor names, product SKUs) |
| semantic| conceptual similarity, paraphrased requirements   |
| hybrid  | both, fused by reciprocal rank                     |
| rerank  | applied on top of hybrid for precision             |

Default is hybrid + rerank, configured per-stage in `config/stages.yaml`.

## 5. Provenance and Authority

Every retrieval result carries:

- `chunk_id`
- `source_document_id`
- `source_path` and section/position
- `authority` (vendor > internal > customer > market, configurable)
- `confidence`
- `sensitivity`

Stage prompts **must** surface provenance to the LLM in the prompt context
and **must** require the LLM to emit provenance in the response schema.

If a stage cannot cite its claims, the validation engine flags them as
`ungrounded` and the artifact fails its gate.

## 6. Knowledge Updates

- New ingestion adds chunks; old chunks are versioned, not overwritten.
- A chunk is **superseded** by a newer chunk from the same source on the
  same section when `version` increments.
- A chunk is **invalidated** when its `valid_until` passes.

The retrieval layer prefers valid, higher-authority, higher-confidence
chunks and can filter by metadata (topic, entity, sensitivity).

## 7. Cross-Stage Knowledge Sharing

- **Product** writes its output to `knowledge/product/`, which becomes
  read-only knowledge for Presales, Architecture, and Delivery.
- **Architecture** writes reference architectures to `knowledge/architecture/`,
  which becomes read-only for Delivery.
- **Delivery** writes operational runbooks and feedback to `knowledge/delivery/`
  and `projects/<id>/delivery/feedback.md`, which feeds back into Product
  knowledge for the next iteration.

## 8. Sensitivity and Access

Each namespace and each item carries a `sensitivity` field:

| Level        | Read scope                                       |
|--------------|--------------------------------------------------|
| public       | all stages                                       |
| internal     | all EPE users                                    |
| confidential | per-project access only                          |
| restricted   | per-item ACL, enforced by the retrieval layer    |

The retrieval layer enforces sensitivity before any chunk is returned to a
stage prompt.

## 9. Cross-References

- See `docs/ARCHITECTURE.md` for the layering.
- See `docs/CONFIGURATION.md` for `models.yaml`, `embeddings.yaml`, and
  `retrieval.yaml`.
- See `docs/DATA_MODEL.md` for the entities that own knowledge.
