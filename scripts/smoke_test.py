"""Smoke test: end-to-end EPE run with the stub LLM.

This runs all four stage engines in dry-run mode, executes handovers, and
prints a dashboard. It does not require an Anthropic API key.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Make src/ importable when running directly
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from epe.core.config import load_config  # noqa: E402
from epe.core.logging import setup_logging  # noqa: E402
from epe.core.paths import EpePaths  # noqa: E402
from epe.dashboard.projections import project_dashboard_markdown  # noqa: E402
from epe.ingestion.pipeline import IngestionPipeline  # noqa: E402
from epe.knowledge.engine import KnowledgeEngine  # noqa: E402
from epe.knowledge.providers import StubLLMProvider  # noqa: E402
from epe.orchestration.handover import execute_handover  # noqa: E402
from epe.orchestration.lifecycle import Lifecycle, State, create_lifecycle  # noqa: E402
from epe.orchestration.project import create_project  # noqa: E402
from epe.stages.base import StageContext, run_stage  # noqa: E402


def main(project_id: str = "MAP-9982") -> int:
    config = load_config()
    setup_logging(config)
    paths = EpePaths(config, project_id=project_id)

    print(f"==> Creating project {project_id}")
    create_project(paths, project_id=project_id, customer="Acme Manufacturing")
    create_lifecycle(paths.project_state)

    # Seed a sample source document so the pipeline has something to ingest.
    print("==> Seeding source document")
    src = paths.sources_incoming
    src.mkdir(parents=True, exist_ok=True)
    sample = src / "customer_rfp.md"
    sample.write_text(
        "# Customer RFP\n\n"
        "Acme Manufacturing is requesting a managed cloud platform. "
        "Single sign-on must use SAML 2.0 with their existing IdP. "
        "The platform must be ISO 27001 certified and SOC 2 Type II. "
        "The customer requires a 99.95% SLA and RPO of 15 minutes, RTO of 4 hours. "
        "Data residency must remain in EU. "
        "Networking: dedicated transit, BGP peering, DDoS protection. "
        "Must integrate with their ServiceNow CMDB and Splunk SIEM.\n",
        encoding="utf-8",
    )

    print("==> Ingesting sources")
    pipeline = IngestionPipeline(paths, project_id=project_id)
    report = pipeline.ingest_directory(src, project_id=project_id)
    print(json.dumps(report.to_dict()["summary"], indent=2))

    # Knowledge engine
    print("==> Building knowledge engine")
    knowledge = KnowledgeEngine(config, paths, project_id=project_id)
    knowledge.load_from_processed(paths.sources_processed / project_id)
    knowledge.load_namespace("global")
    print(f"Indexed {len(knowledge.store)} knowledge items")

    # Stage engines (dry-run uses StubLLMProvider)
    llm = StubLLMProvider()
    ctx = StageContext(
        config=config,
        paths=paths,
        knowledge=knowledge,
        llm=llm,
        project_id=project_id,
        opportunity="OPP-9982",
        customer="Acme Manufacturing",
    )

    for stage in ("product", "presales", "architecture", "delivery"):
        print(f"==> Running stage {stage}")
        result = run_stage(stage, ctx, dry_run=True)
        for name, p in result.outputs.items():
            print(f"   - {name}: {p.name}")

    # Handovers (only if artifacts exist — for dry-run they do)
    print("==> Executing handovers")
    for f, t in (("product", "presales"), ("presales", "architecture"),
                 ("architecture", "delivery")):
        record = execute_handover(
            paths=paths,
            from_stage=f,
            to_stage=t,
            approved_by="smoke-test",
            rationale="Pilot dry-run.",
        )
        print(f"   - {record.from_stage} -> {record.to_stage}: approved")

    # Lifecycle transitions (state machine requires going through the active states)
    print("==> Walking lifecycle")
    lc = Lifecycle.load(paths.project_state)
    for target in (
        State.PRODUCT_READY,
        State.PRESALES_ACTIVE,
        State.PRESALES_READY,
        State.ARCHITECTURE_ACTIVE,
        State.ARCHITECTURE_READY,
        State.DELIVERY_ACTIVE,
    ):
        lc.transition(target)
        print(f"   - now in {lc.state.current.value}")

    # Dashboard
    print("==> Dashboard")
    proj_root = paths.projects_root / project_id
    print(project_dashboard_markdown(proj_root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
