"""Top-level EPE CLI.

Commands:
  epe project create <id>
  epe ingest --project <id>
  epe stage run <stage> --project <id> [--opportunity OPP-...] [--customer NAME]
  epe handover <from> <to> --project <id> --by <approver>
  epe validate <artifact> --project <id>
  epe validate <project-id> --stage <stage>
  epe lifecycle show --project <id>
  epe lifecycle transition <to-state> --project <id>
  epe dashboard render --project <id>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
import yaml

from epe.core.config import load_config
from epe.core.logging import audit_log, get_logger, setup_logging
from epe.core.paths import EpePaths
from epe.ingestion.pipeline import IngestionPipeline
from epe.knowledge.engine import KnowledgeEngine
from epe.knowledge.providers import make_llm_provider
from epe.orchestration.handover import execute_handover
from epe.orchestration.lifecycle import Lifecycle, State, create_lifecycle, transition
from epe.orchestration.project import create_project
from epe.stages.base import StageContext, run_stage
from epe.validation.engine import run_validators, write_report

logger = get_logger("cli")


def _build_paths(project_id: str | None = None) -> tuple:
    config = load_config()
    setup_logging(config)
    paths = EpePaths(config, project_id=project_id)
    return config, paths


def _build_knowledge(config, paths) -> KnowledgeEngine:
    return KnowledgeEngine(config, paths, project_id=paths.project_id)


@click.group()
def main() -> None:
    """EPE — Enterprise Playground Engine CLI."""


@main.group()
def project() -> None:
    """Project lifecycle commands."""


@project.command("create")
@click.argument("project_id")
@click.option("--customer", default=None)
def project_create(project_id: str, customer: str | None) -> None:
    config, paths = _build_paths(project_id=project_id)
    p = create_project(paths, project_id=project_id, customer=customer)
    click.echo(f"Created project {p.project_id} at {p.paths.project_root}")
    # also create the lifecycle
    if not p.paths.project_state.exists():
        click.echo("Note: state.yaml was initialized by create_project().")


@main.command()
@click.option("--project", "project_id", required=True)
@click.option("--source", "source_dir", default=None,
              help="Directory of source files to ingest (default: sources/incoming).")
def ingest(project_id: str, source_dir: str | None) -> None:
    config, paths = _build_paths(project_id=project_id)
    pipeline = IngestionPipeline(paths, project_id=project_id)
    src = Path(source_dir) if source_dir else paths.sources_incoming
    click.echo(f"Ingesting from {src}")
    report = pipeline.ingest_directory(src, project_id=project_id)
    click.echo(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))


@main.group()
def stage() -> None:
    """Stage engine commands."""


@stage.command("run")
@click.argument("stage_name", type=click.Choice(["product", "presales", "architecture", "delivery"]))
@click.option("--project", "project_id", required=True)
@click.option("--opportunity", default=None)
@click.option("--customer", default=None)
@click.option("--dry-run", is_flag=True)
def stage_run(stage_name: str, project_id: str, opportunity: str | None,
              customer: str | None, dry_run: bool) -> None:
    config, paths = _build_paths(project_id=project_id)
    paths.ensure_project_layout()
    knowledge = _build_knowledge(config, paths)
    # Load indexed chunks and global knowledge namespace before running any stage.
    knowledge.load_from_processed(paths.sources_processed / project_id)
    for ns in config.stage(stage_name).knowledge:
        knowledge.load_namespace(ns)
    llm = make_llm_provider(config.models.llm)
    ctx = StageContext(
        config=config,
        paths=paths,
        knowledge=knowledge,
        llm=llm,
        project_id=project_id,
        opportunity=opportunity,
        customer=customer,
    )
    result = run_stage(stage_name, ctx, dry_run=dry_run)
    click.echo(f"Stage {stage_name} complete. Outputs:")
    for name, p in result.outputs.items():
        click.echo(f"  - {name}: {p}")
    if result.findings:
        click.echo(f"Findings: {len(result.findings)}")
        for f in result.findings[:10]:
            click.echo(f"  - {f.get('severity')}: {f.get('message')}")


@main.command()
@click.argument("from_stage", type=click.Choice(["product", "presales", "architecture", "delivery"]))
@click.argument("to_stage", type=click.Choice(["product", "presales", "architecture", "delivery"]))
@click.option("--project", "project_id", required=True)
@click.option("--by", "approved_by", required=True)
@click.option("--rationale", default=None)
def handover(from_stage: str, to_stage: str, project_id: str, approved_by: str,
             rationale: str | None) -> None:
    config, paths = _build_paths(project_id=project_id)
    record = execute_handover(
        paths=paths,
        from_stage=from_stage,
        to_stage=to_stage,
        approved_by=approved_by,
        rationale=rationale,
    )
    click.echo(f"Handover approved: {record.from_stage} -> {record.to_stage}")
    click.echo(f"  Artifact: {record.artifact_path}")
    click.echo(f"  Approved by: {record.approved_by}")


@main.command()
@click.argument("target")
@click.option("--project", "project_id", default=None)
@click.option("--stage", "stage_name", default=None)
def validate(target: str, project_id: str | None, stage_name: str | None) -> None:
    config, paths = _build_paths(project_id=project_id)
    target_path = Path(target)
    if target_path.is_dir():
        # validate all artifacts in a stage directory
        stage_name = stage_name or target_path.name
        files = sorted(target_path.glob("*.md"))
    else:
        files = [target_path]

    for f in files:
        click.echo(f"\n=== {f} ===")
        report = run_validators(f, project_paths=paths)
        click.echo(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
        write_report(report, paths.project_validation_dir)


@main.group()
def lifecycle() -> None:
    """Lifecycle state machine."""


@lifecycle.command("show")
@click.option("--project", "project_id", required=True)
def lifecycle_show(project_id: str) -> None:
    _, paths = _build_paths(project_id=project_id)
    lc = Lifecycle.load(paths.project_state)
    click.echo(json.dumps(lc.state.raw, indent=2, ensure_ascii=False))


@lifecycle.command("transition")
@click.argument("to_state", type=click.Choice([s.value for s in State]))
@click.option("--project", "project_id", required=True)
def lifecycle_transition(to_state: str, project_id: str) -> None:
    config, paths = _build_paths(project_id=project_id)
    target = State(to_state)
    lc = transition(paths.project_state, target)
    click.echo(f"Transitioned to {to_state}")
    click.echo(json.dumps(lc.state.raw, indent=2, ensure_ascii=False))


@main.group()
def dashboard() -> None:
    """Dashboard commands."""


@dashboard.command("render")
@click.option("--project", "project_id", required=True)
def dashboard_render(project_id: str) -> None:
    from epe.dashboard.projections import project_dashboard_markdown
    _, paths = _build_paths(project_id=project_id)
    proj_root = paths.projects_root / project_id
    click.echo(project_dashboard_markdown(proj_root))


if __name__ == "__main__":
    main()
