# EPE — Operator Runbook

## 1. Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## 2. End-to-end smoke test

```bash
.venv/bin/python scripts/smoke_test.py
```

The script:
- creates project `MAP-9982`
- seeds a sample RFP
- ingests, indexes, runs all four stages (dry-run, stub LLM)
- executes all three handovers
- walks the lifecycle to `delivery_active`
- prints the Markdown dashboard

## 3. Running a real stage

```bash
export ANTHROPIC_API_KEY=sk-ant-...
epe project create MAP-9982
epe ingest --project MAP-9982
epe stage run product  --project MAP-9982
epe stage run presales --project MAP-9982 --opportunity OPP-9982 --customer "Acme"
epe stage run architecture --project MAP-9982 --opportunity OPP-9982 --customer "Acme"
epe stage run delivery --project MAP-9982 --opportunity OPP-9982 --customer "Acme"

epe handover product presales --project MAP-9982 --by product_lead
epe handover presales architecture --project MAP-9982 --by presales_lead
epe handover architecture delivery --project MAP-9982 --by lead_architect

epe validate projects/MAP-9982/presales/handover.md --project MAP-9982
epe lifecycle transition presales_active --project MAP-9982
```

## 4. Running the dashboard

```bash
uvicorn epe.dashboard.app:app --reload --port 8088
# or via docker
docker build -t epe .
docker run --rm -p 8088:8088 -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY epe
```

Endpoints:
- `GET /health` — liveness probe
- `GET /projects` — list all projects
- `GET /projects/{id}` — full project summary (gates, artifacts, traceability, counts)
- `GET /projects/{id}/state` — raw lifecycle state
- `GET /projects/{id}/dashboard.md` — human-readable Markdown dashboard

## 5. Validation

The validation engine writes per-artifact reports under
`projects/<id>/.validation/`. A `blocker` finding marks the artifact as
failing its gate.

```bash
epe validate projects/MAP-9982 --stage presales
```

## 6. Adding a document type

1. Implement `epe.ingestion.extractors.<format>.extract(path)`.
2. Add the format to `epe.ingestion.extractors.extract`'s dispatch table.
3. Add tests under `tests/test_ingestion.py`.

## 7. Adding a stage

1. Create `src/epe/stages/<stage>/` with `engine.py`, `prompts.py`, `parser.py`.
2. Register it in `src/epe/stages/base.py:load_stage_engine`.
3. Add the stage's outputs to `epe.stages.base.StageEngine._output_path`.
4. Add config to `config/stages.yaml` and `config/validation.yaml`.
5. Add required sections to `epe.validation.engine.REQUIRED_SECTIONS`.

## 8. Adding a validator

1. Implement `validate(artifact_path, context) -> Iterable[Finding]` under
   `src/epe/validation/`.
2. Register it in `epe.validation.engine.run_validators`'s `mapping` dict.
3. Pass it via `--validators` on the CLI, or include it in the default
   validator list.

## 9. Troubleshooting

| Symptom                                | Check                                                        |
|----------------------------------------|--------------------------------------------------------------|
| `ConfigurationError: paths keys`       | `config/system.yaml` is missing required path keys.          |
| `GateFailure: gate.product.*`          | Run the corresponding stage engine to produce the artifact.  |
| LLM hallucinations                     | Re-run; check that `knowledge.load_from_processed` indexed the source. |
| Vector store miss                      | Knowledge engine not loaded for the stage's namespace.       |
| Dashboard 404                          | Project not initialized; run `epe project create`.           |
