# EPE — Data Model

## 1. Canonical Entities

| Entity               | Backing store                | Identity                |
|----------------------|------------------------------|-------------------------|
| SourceDocument       | `sources/processed/` + meta  | `document_id`           |
| ClassifiedRecord     | `sources/classified/`        | `document_id`           |
| KnowledgeChunk       | Vector store + chunk index   | `chunk_id`              |
| Requirement          | `projects/<id>/requirements/`| `REQ-NNN`               |
| Decision             | `projects/<id>/decisions/`   | `DEC-NNN`               |
| Risk                 | `projects/<id>/risks/`       | `RSK-NNN`               |
| OpenQuestion         | `projects/<id>/questions/`   | `Q-NNN`                 |
| ProductCapability    | `projects/<id>/product/`     | `CAP-NNN`               |
| PresalesHandover     | `projects/<id>/presales/`    | per-project             |
| ArchitectureDecision | `projects/<id>/architecture/`| `ADR-NNN`               |
| DeliveryTask         | `projects/<id>/delivery/`   | `TASK-NNN`              |
| AcceptanceTest       | `projects/<id>/delivery/`   | `TEST-NNN`              |
| LifecycleState       | `projects/<id>/state.yaml`  | per-project             |

## 2. SourceDocument

```yaml
document_id: DOC-00182
filename: customer_requirements.pdf
source_path: sources/incoming/customer_requirements.pdf
sha256: <hex>

document_type: requirements      # requirements | architecture | pricing |
                                 # compliance | vendor | market | internal
domain: customer                  # customer | vendor | internal | market
stage_relevance:
  - presales
  - architecture

authority: customer               # customer | vendor | internal | market
confidence: high                  # high | medium | low

version: 1.0
received_at: 2026-09-29T10:00:00Z

topics:
  - networking
  - security
  - cloud
  - identity

contains:
  requirements: true
  architecture: false
  pricing: false
  compliance: true

sensitivity: confidential         # public | internal | confidential | restricted
retention: P7Y
```

## 3. Requirement

Frontmatter:

```yaml
id: REQ-023
title: SSO via SAML 2.0
source: DOC-00182
source_quote: "Single sign-on is mandatory using SAML 2.0 with our IdP"
priority: must                    # must | should | could | wont
status: confirmed                 # draft | confirmed | rejected | deferred
type: security                    # functional | non-functional | security | operational
created_at: 2026-09-29T10:00:00Z
created_by: presales
```

Body: free-form Markdown.

Traceability links live in the body, not the frontmatter, to keep git diffs
readable:

```markdown
## Traceability
- Presales: PRES-014
- Architecture: ARCH-031
- Delivery: TASK-087
- Test: TEST-044
```

## 4. Decision (ADR-style)

```yaml
id: DEC-001
title: Use managed Postgres over self-hosted
date: 2026-09-29
stage: architecture
status: proposed                  # proposed | accepted | superseded | rejected
decision_makers: [architect, lead]
```

Body follows a standard ADR template (Context, Decision, Consequences).

## 5. Risk

```yaml
id: RSK-001
title: Vendor lock-in for managed Postgres
stage: architecture
likelihood: medium
impact: high
status: open                      # open | mitigated | accepted | closed
mitigation: ...
```

## 6. OpenQuestion

```yaml
id: Q-001
stage: presales
question: "What is the customer's RTO for the identity service?"
blocking: true
owner: presales
```

## 7. Capability

```yaml
id: CAP-001
name: SSO with SAML 2.0
classification: standard          # standard | configurable | custom | unsupported
depends_on: [CAP-005]
```

## 8. ArchitectureDecision (ADR inside Architecture)

Identical schema to `Decision` with `stage: architecture`.

## 9. DeliveryTask

```yaml
id: TASK-087
title: Deploy identity service
implements: ARCH-031
acceptance: TEST-044
status: todo
```

## 10. AcceptanceTest

```yaml
id: TEST-044
title: SAML SSO end-to-end
covers: REQ-023
status: not_run
```

## 11. LifecycleState

```yaml
project_id: MAP-9982
stage: architecture
status: active                    # active | waiting | blocked | done

gates:
  product:
    status: approved
  presales:
    qualification: passed
    scope: approved
    handover: ready
  architecture:
    requirements: pending
    hld: pending
    lld: pending
  delivery:
    deployment: blocked

history:
  - from: presales
    to: architecture
    at: 2026-09-29T10:00:00Z
    reason: handover approved
```

## 12. Traceability Graph

The traceability graph is **derived**, not stored. It is computed by walking
the frontmatter `*_id` and body links. The validation engine rebuilds it on
demand and writes a `traceability.json` projection under each project.

Edges:

```
source_document ──▶ requirement ──▶ architecture_component ──▶ delivery_task ──▶ acceptance_test
                                  │
                                  └─▶ decision
                                  └─▶ risk
                                  └─▶ open_question
```

## 13. Cross-References

- See `docs/OUTPUT_CONTRACTS.md` for how each entity is produced.
- See `docs/VALIDATION.md` for how the traceability graph is enforced.
- See `docs/KNOWLEDGE_MODEL.md` for the chunk-level knowledge entities.
