# Claude Code Guidance

You are working inside the **EPE** repository. Before making changes, read:

1. `docs/PRD.md` — purpose and success criteria.
2. `docs/ARCHITECTURE.md` — layering and module layout.
3. `docs/DATA_MODEL.md` — entities and identifiers.
4. `docs/WORKFLOW.md` — state machine and gates.
5. `docs/CONFIGURATION.md` — config files and loading order.
6. `docs/KNOWLEDGE_MODEL.md` — namespaces and retrieval.
7. `docs/OUTPUT_CONTRACTS.md` — what each stage must produce.
8. `docs/VALIDATION.md` — gate predicates and validators.
9. `docs/SECURITY.md` — sensitivity and ACL rules.

## Working principles

- **Document-first.** Markdown contracts are the canonical interop layer.
- **Configuration-driven.** No provider/model may be hard-coded outside `config/`.
- **Stage-independent.** Each engine runs given its declared inputs.
- **Provenance mandatory.** Every claim cites a source.
- **Gate-enforced.** No downstream stage consumes an incomplete upstream
  contract.
- **Tests required.** New behavior must come with tests.

## Editing rules

- Touch only the files you are asked to change.
- Do not edit `_audit/`, `.validation/`, or `data/embedding_cache/`.
- Keep `pyproject.toml` dependency surface minimal; new optional deps go
  under `[project.optional-dependencies]`.
- Keep `config/*.yaml` backward compatible unless you are explicitly
  evolving a schema.

## When asked to implement a feature

1. Read the relevant `docs/` file first.
2. Find the existing pattern in `src/epe/` that the feature belongs to.
3. Implement the smallest change that satisfies the contract.
4. Add a test under `tests/` mirroring the package layout.
5. Update the relevant `docs/` file if the contract changes.

## When something is unclear

Ask. Do not invent semantics that conflict with the nine contract
documents.
