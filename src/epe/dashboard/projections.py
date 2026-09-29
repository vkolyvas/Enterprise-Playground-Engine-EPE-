"""Read-only projections used by the FastAPI dashboard.

These functions read Markdown artifacts and lifecycle state. They never mutate
project state. Adding/removing the dashboard loses zero decisions, requirements,
or risks.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml

from epe.core.frontmatter import read_doc


def project_list(projects_root: Path) -> list[dict]:
    if not projects_root.exists():
        return []
    out: list[dict] = []
    for child in sorted(projects_root.iterdir()):
        if not child.is_dir() or child.name.startswith("_") or child.name.startswith("."):
            continue
        state_path = child / "state.yaml"
        if not state_path.exists():
            continue
        try:
            data = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        out.append(
            {
                "project_id": data.get("project_id", child.name),
                "stage": data.get("stage"),
                "status": data.get("status"),
                "customer": data.get("customer"),
            }
        )
    return out


def project_state(state_path: Path) -> dict:
    if not state_path.exists():
        return {}
    return yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}


def project_summary(project_root: Path) -> dict:
    """Build the dashboard summary for a single project."""
    state_path = project_root / "state.yaml"
    state = project_state(state_path)

    artifacts = []
    for stage in ("product", "presales", "architecture", "delivery"):
        for path in sorted((project_root / stage).glob("*.md")):
            try:
                doc = read_doc(path)
                artifacts.append(
                    {
                        "stage": stage,
                        "name": path.name,
                        "contract": doc.metadata.get("contract"),
                        "status": doc.metadata.get("status"),
                        "approved_by": doc.metadata.get("approved_by"),
                        "approved_at": doc.metadata.get("approved_at"),
                        "checksum_sha256": doc.metadata.get("checksum_sha256"),
                        "rel_path": str(path.relative_to(project_root)),
                    }
                )
            except Exception:
                continue

    # Traceability graph
    from epe.validation.traceability import build_traceability_graph

    graph = build_traceability_graph(project_root)

    # Counts
    body_texts = []
    for a in artifacts:
        path = project_root / a["rel_path"]
        try:
            body_texts.append(read_doc(path).body)
        except Exception:
            pass
    all_body = "\n".join(body_texts)
    counts = {
        "requirements": len(_find_ids(all_body, "REQ-")),
        "capabilities": len(_find_ids(all_body, "CAP-")),
        "decisions": len(_find_ids(all_body, "DEC-")),
        "components": len(_find_ids(all_body, "COMP-")),
        "tasks": len(_find_ids(all_body, "TASK-")),
        "tests": len(_find_ids(all_body, "TEST-")),
        "questions": len(_find_ids(all_body, "Q-")),
    }

    # Status counts
    status_counter = Counter(a["status"] for a in artifacts)

    # Handover readiness — derived from existing artifacts and their approval
    readiness = _handover_readiness(artifacts)

    return {
        "project_id": state.get("project_id", project_root.name),
        "stage": state.get("stage"),
        "lifecycle_status": state.get("status"),
        "gates": state.get("gates", {}),
        "history": state.get("history", []),
        "artifacts": artifacts,
        "counts": counts,
        "status_counts": dict(status_counter),
        "traceability": {
            "nodes": len(graph.get("nodes", {})),
            "edges": len(graph.get("edges", [])),
            "orphan": graph.get("orphan", []),
        },
        "handover_readiness": readiness,
    }


def _find_ids(text: str, prefix: str) -> list[str]:
    import re
    return re.findall(rf"\b{re.escape(prefix)}\d+\b", text)


def _handover_readiness(artifacts: list[dict]) -> dict:
    by_stage: dict[str, list[dict]] = {stage: [] for stage in ("product", "presales", "architecture", "delivery")}
    for a in artifacts:
        by_stage.setdefault(a["stage"], []).append(a)
    approved = lambda arts: sum(1 for a in arts if a["status"] == "approved")
    total = lambda arts: len(arts)

    pct = lambda arts: (approved(arts) / total(arts) * 100) if total(arts) else 0.0

    return {
        "product_to_presales": pct(by_stage["product"]),
        "presales_to_architecture": pct(by_stage["presales"]),
        "architecture_to_delivery": pct(by_stage["architecture"]),
    }


def project_dashboard_markdown(project_root: Path) -> str:
    """Render the human-readable dashboard as Markdown."""
    summary = project_summary(project_root)
    pid = summary["project_id"]
    stage = summary.get("stage") or "—"
    status = summary.get("lifecycle_status") or "—"
    counts = summary["counts"]
    hr = summary["handover_readiness"]

    def bar(pct: float) -> str:
        full = int(round(pct / 10))
        return "█" * full + "░" * (10 - full)

    lines = [
        f"# EPE — Project {pid}",
        "",
        f"- **Stage**: {stage}",
        f"- **Status**: {status}",
        "",
        "## Handover readiness",
        "",
        f"- Product → Presales:        `{bar(hr['product_to_presales'])}` {hr['product_to_presales']:.0f}%",
        f"- Presales → Architecture:   `{bar(hr['presales_to_architecture'])}` {hr['presales_to_architecture']:.0f}%",
        f"- Architecture → Delivery:   `{bar(hr['architecture_to_delivery'])}` {hr['architecture_to_delivery']:.0f}%",
        "",
        "## Counts",
        "",
        f"- Requirements: {counts['requirements']}",
        f"- Capabilities: {counts['capabilities']}",
        f"- Decisions: {counts['decisions']}",
        f"- Components: {counts['components']}",
        f"- Tasks: {counts['tasks']}",
        f"- Tests: {counts['tests']}",
        f"- Open questions: {counts['questions']}",
        "",
        "## Artifacts",
        "",
    ]
    for stage_name in ("product", "presales", "architecture", "delivery"):
        stage_arts = [a for a in summary["artifacts"] if a["stage"] == stage_name]
        if not stage_arts:
            continue
        lines.append(f"### {stage_name}")
        lines.append("")
        for a in stage_arts:
            status = a["status"] or "—"
            lines.append(f"- {a['name']} — `{a['contract']}` — status: {status}")
        lines.append("")
    return "\n".join(lines)
