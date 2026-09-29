# EPE — Validation

## 1. Purpose

Every artifact produced by a stage engine passes through six layers of
validation before it is accepted into the lifecycle:

1. **Structural** — file exists, frontmatter parses, required fields present.
2. **Content** — required Markdown sections exist with non-empty bodies.
3. **Traceability** — every claim links to a source; every requirement
   traces forward to a task and a test.
4. **Consistency** — no contradictions within or across artifacts.
5. **Security** — no secrets, no disallowed content, sensitivity honored.
6. **Completeness** — every gate for the destination state is satisfied.

The validation engine produces a `ValidationReport` with findings and an
overall verdict: `pass | fail | waive`.

## 2. ValidationReport

```yaml
contract: <dot.path>
project_id: MAP-9982
artifact_path: architecture/hld.md
validated_at: 2026-09-29T10:00:00Z
validators:
  - structural
  - content
  - traceability
  - consistency
  - security
  - completeness

findings:
  - id: F-001
    validator: structural
    severity: blocker            # info | warning | error | blocker
    location: architecture/hld.md:14
    message: "Missing required section 'Logical Components'"
    remediation: "Add a 'Logical Components' section with at least one component entry."

  - id: F-002
    validator: traceability
    severity: error
    location: architecture/hld.md:38
    message: "Component COMP-007 has no upstream requirement reference"
    remediation: "Link COMP-007 to at least one REQ-NNN."

summary:
  info: 0
  warning: 2
  error: 1
  blocker: 1

verdict: fail                     # pass | fail | waive
```

A `blocker` finding forces `verdict: fail`. A `waive` verdict requires a
human approver and a documented justification.

## 3. Validator Modules

Validators live under `src/epe/validation/`:

```
validation/
├── structural.py          # frontmatter + section presence
├── content.py             # required bodies, lengths, patterns
├── traceability.py        # graph walk + missing edges
├── consistency.py         # contradiction detection across artifacts
├── security.py            # secrets scan, sensitivity, ACL
└── completeness.py        # gate aggregation
```

Each module exposes `validate(artifact_path, project_context) -> list[Finding]`.

## 4. Gate Predicates

Every gate in `config/validation.yaml` maps to a Python predicate. Examples:

```python
# src/epe/validation/product/readiness_complete.py

def run(artifact_path: Path, ctx: ProjectContext) -> Verdict:
    report = validate(artifact_path, ctx, validators=[
        "structural", "content", "traceability", "completeness"
    ])
    if any(f.severity == "blocker" for f in report.findings):
        return Verdict.FAIL
    return Verdict.PASS if report.verdict == "pass" else Verdict.FAIL
```

The lifecycle orchestrator calls `run` for each gate on every transition
attempt.

## 5. Traceability Validation

### 5.1 Required edges

For every `REQ-NNN` in `presales/scope.md`:

- at least one `DEC-NNN` or `COMP-NNN` in architecture referencing it
- at least one `TASK-NNN` in delivery referencing the component
- at least one `TEST-NNN` covering the requirement

For every `CAP-NNN` in `product/catalog.md` referenced by presales:

- the capability must exist and its `classification` is not `unsupported`
- if `custom`, an architecture decision must exist

### 5.2 Graph projection

The validation engine writes `traceability.json` per project:

```json
{
  "nodes": {
    "REQ-023": {"stage": "presales", "path": "presales/scope.md"},
    "ARCH-031": {"stage": "architecture", "path": "architecture/lld.md"},
    "TASK-087": {"stage": "delivery", "path": "delivery/plan.md"},
    "TEST-044": {"stage": "delivery", "path": "delivery/test.md"}
  },
  "edges": [
    {"from": "REQ-023", "to": "ARCH-031", "type": "implements"},
    {"from": "ARCH-031", "to": "TASK-087", "type": "realizes"},
    {"from": "TASK-087", "to": "TEST-044", "type": "verified_by"}
  ],
  "missing": [],
  "orphan_requirements": [],
  "orphan_components": []
}
```

### 5.3 Ungrounded claims

Any Markdown paragraph in an artifact that does not cite at least one
`DOC-NNN`, `CAP-NNN`, `REQ-NNN`, `DEC-NNN`, `TASK-NNN`, or `TEST-NNN` in
the same paragraph (inline reference) is flagged as
`severity: warning, validator: traceability, kind: ungrounded`. Summaries
of cited claims are allowed; unsourced assertions are not.

## 6. Consistency Validation

The consistency validator walks all artifacts in a project and checks:

- A requirement marked `status: rejected` in presales must not appear
  in any later artifact.
- A decision marked `status: superseded` must not be the most recent
  decision on its topic.
- Two architecture components must not claim ownership of the same
  capability without an explicit conflict resolution decision.
- The same `REQ-NNN` must not be classified differently across artifacts.

## 7. Security Validation

The security validator enforces:

- No `BEGIN PRIVATE KEY`, AWS access key, GitHub PAT, or generic
  high-entropy secret patterns.
- No `sensitivity: restricted` content embedded in `sensitivity: public`
  outputs.
- No customer PII inside `knowledge/global/` or `knowledge/product/`.
- All retrievals that produced a chunk must respect the chunk's
  `sensitivity` against the calling stage's namespace ACL.

## 8. Completeness Validation

Completeness is the conjunction of gate predicates. It is invoked by the
lifecycle orchestrator at every state transition. A transition is allowed
only if all destination gates pass.

## 9. CLI

```bash
epe validate <project-id> --artifact <path>     # single artifact
epe validate <project-id> --stage <stage>        # all artifacts in a stage
epe validate <project-id> --gates               # just the gates
```

Output: `ValidationReport` printed as YAML; written to
`projects/<id>/.validation/<artifact>.yaml`.

## 10. Cross-References

- See `docs/OUTPUT_CONTRACTS.md` for the artifact schemas.
- See `docs/DATA_MODEL.md` for the entity IDs that traceability walks.
- See `docs/SECURITY.md` for sensitivity policy.
- See `docs/WORKFLOW.md` for how gates are wired to transitions.
