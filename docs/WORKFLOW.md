# EPE — Workflow and Lifecycle

## 1. Lifecycle States

```
[NEW]
   │
   ▼
PRODUCT_ACTIVE
   │
   ▼ gates.product.readiness = approved
PRODUCT_READY
   │
   ▼
PRESALES_ACTIVE
   │
   ▼ gates.presales.qualification = passed
   ▼ gates.presales.scope = approved
   ▼ gates.presales.handover = ready
PRESALES_READY
   │
   ▼
ARCHITECTURE_ACTIVE
   │
   ▼ gates.architecture.requirements = passed
   ▼ gates.architecture.hld = approved
   ▼ gates.architecture.lld = approved
ARCHITECTURE_READY
   │
   ▼
DELIVERY_ACTIVE
   │
   ▼ gates.delivery.deployment = done
   ▼ gates.delivery.acceptance = passed
SERVICE_LIVE
   │
   ▼
OPTIMIZATION
   │
   ▼ optional: feedback to PRODUCT_ACTIVE
```

## 2. Stage Pipelines

### 2.1 Product

```
IDEATE → DEFINE → VALIDATE → PACKAGE → READINESS
```

### 2.2 Presales

```
DISCOVERY → QUALIFICATION → REQUIREMENTS → PRODUCT_MAPPING
   → GAP_ANALYSIS → SCOPING → SOW → HANDOVER
```

### 2.3 Architecture

```
REQUIREMENT_VALIDATION → ARCHITECTURE_OPTIONS → TRADE_OFFS
   → HLD → SECURITY → INTEGRATION → CAPACITY → COST
   → LLD → IMPLEMENTATION_BLUEPRINT
```

### 2.4 Delivery

```
PLAN → PROVISION → CONFIGURE → TEST → VALIDATE
   → ONBOARD → HANDOVER → OPERATE → OPTIMIZE
```

## 3. Gates

Every transition is gated. A gate has:

- **id**
- **stage**
- **owner** (the role that signs off)
- **predicate** (the validation rule that produces pass/fail)
- **status** (pending | in_review | passed | failed | waived)

Example:

```yaml
- id: gate.architecture.hld
  stage: architecture
  owner: lead_architect
  predicate: epe.validation.architecture.hld_complete
  status: pending
```

A transition is allowed only if every gate for the destination state is
`passed` or `waived`.

## 4. Handover Contracts

A handover is a **transaction**, not just a file. It has:

1. **Upstream artifact** (must exist and validate)
2. **Downstream consumer** (must be ready)
3. **Completeness check** (all required fields present)
4. **Conflict check** (no unresolved contradictions)
5. **Approval gate** (human sign-off)
6. **Handover artifact** (the `.md` contract)
7. **Traceability record** (the edges that crossed the boundary)

The state machine refuses to advance until the handover is complete.

## 5. Stage Engine Internal Lifecycle

Every stage engine follows the same internal structure:

```
INPUT
  ↓
CONTEXT BUILDER
  ↓
KNOWLEDGE RETRIEVAL
  ↓
ANALYSIS
  ↓
DECISION
  ↓
VALIDATION
  ↓
OUTPUT
  ↓
HANDOVER
```

Engines are **stateless across runs** — they read their declared inputs and
write their declared outputs. All persistent state lives in the project
filesystem.

## 6. Concurrent Work

The state machine permits:

- Multiple presales engagements to be active for one product.
- Architecture to begin on a delivered handover while Presales continues on
  a different opportunity.
- Delivery on one opportunity while Architecture continues on the next.

The state machine does **not** permit:

- Architecture to begin before Presales handover is approved.
- Delivery to begin before Architecture blueprint is approved.

## 7. Feedback Loop

Delivery writes `delivery/feedback.md`, which is consumed by Product as
fresh knowledge for the next iteration:

```
DELIVERY_OPERATE
   │
   ▼
delivery/feedback.md  (incidents, cost, usage, lessons)
   │
   ▼
PRODUCT_KB update
   │
   ▼
IDEATE  (next cycle)
```

## 8. Cross-References

- See `docs/ARCHITECTURE.md` for the layering.
- See `docs/OUTPUT_CONTRACTS.md` for the file-level contracts.
- See `docs/VALIDATION.md` for the predicates.
- See `docs/DATA_MODEL.md` for the lifecycle state schema.
